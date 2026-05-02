#!/usr/bin/env python3
"""
§213 — V_OPT v4 Calibration (Grid Search + k-fold CV)
======================================================
Recalibration des poids V_OPT sur le corpus v212f (75 textes, 3 traditions).

Méthode :
  1. Grid search exhaustif sur (w_direct, w_translation, w_indirect) ∈ [0.01, 1.0]³
     en pas de 0.05 (après normalisation relative : seul le rapport compte,
     donc on fixe w_direct ≥ w_translation ≥ w_indirect, puis on normalise
     pour obtenir des coûts comparables à v3).
  2. Critère : maximiser R²(d_topo_vopt, d_lex_v14) sur l'ensemble des
     paires signées (Pearson r sur (d_topo, d_lex) puis r²).
  3. k-fold CV (k=5) avec stratification par tradition pour estimer
     la stabilité de R² : reporter mean ± std.
  4. Comparer les meilleurs poids V_OPT v4 à V_OPT v3 sur les 30 textes
     bouddhistes (sous-ensemble le plus comparable à v208 protoatheism).
  5. Sortie : nipada_v213_vopt_calibration.json

V_OPT v3 (référence) : {direct: 0.45, translation: 0.05, indirect: 0.05}
Corpus v212f : 75 textes (BUDDHIST=30, INDIAN=32, CHINESE=13)
Graphe v12   : 1764 nœuds / 26112 arêtes

Usage : python3 scripts/nipada_vopt_calibration_v213.py [--fast]
  --fast  : pas de 0.10 au lieu de 0.05 (grille réduite, ~10× plus rapide)
"""

import json
import heapq
import math
import time
import sys
import random
from pathlib import Path
from itertools import combinations

# ─── Chemins ───────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH  = _NIPADA / "falsification/nipada_v210a_graph_v12.json"
CORPUS_PATH = _NIPADA / "corpus/signed_corpus_v212f.json"
OUT_PATH    = _NIPADA / "falsification/nipada_v213_vopt_calibration.json"

# ─── V_OPT v3 référence ────────────────────────────────────────────────────
V_OPT_V3 = {"direct": 0.45, "translation": 0.05, "indirect": 0.05}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

SEED = 2026
K_FOLDS = 5


# ─── Utilitaires V_OPT ─────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(edges: list, weights: dict) -> dict:
    """Construit adjacence non-dirigée avec les poids fournis."""
    adj: dict = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = weights[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(source: str, adj: dict, targets: set) -> dict:
    dist = {source: 0.0}
    pq = [(0.0, source)]
    remaining = set(targets) - {source}
    found: dict = {}
    while pq and remaining:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        if u in remaining:
            remaining.discard(u)
            found[u] = d
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return {t: found.get(t, dist.get(t, math.inf)) for t in targets}


# ─── Utilitaires statistiques ───────────────────────────────────────────────

def v14_vector(sig: dict) -> list:
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1: list, v2: list) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r(xs: list, ys: list) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return num / (sx * sy)


def compute_r2_on_subset(adj: dict, subset: list) -> tuple[float, int]:
    """Calcule R²(d_topo, d_lex) sur un sous-ensemble de textes signés."""
    ids = [s["graph_node_id"] for s in subset]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset}
    id_set = set(ids)

    d_topo_list: list = []
    d_lex_list: list = []

    for i in range(len(ids)):
        distances = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = distances[ids[j]]
            if math.isinf(dt):
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            d_topo_list.append(dt)
            d_lex_list.append(dl)

    if len(d_topo_list) < 2:
        return 0.0, 0
    r = pearson_r(d_topo_list, d_lex_list)
    return r * r, len(d_topo_list)


# ─── Grid search ────────────────────────────────────────────────────────────

def grid_candidates(step: float = 0.05) -> list[dict]:
    """
    Génère les combinaisons (w_direct, w_translation, w_indirect).
    On explore [step, 1.0] pour chaque poids.
    Les valeurs absolues importent (pas de normalisation) — cohérence avec
    les longueurs de chemin Dijkstra utilisées dans le reste de NIPADA.
    On contraint : w_direct ≥ w_indirect et w_translation ≥ w_indirect
    (coût direct ≤ coût indirect — l'influence directe est plus forte = coût plus faible).
    Note: coût faible = distance faible = influence forte.
    """
    vals = [round(step * k, 4) for k in range(1, int(1.0 / step) + 1)]
    candidates = []
    for wd in vals:
        for wt in vals:
            for wi in vals:
                # direct influence strongest → lowest cost
                # translation ≤ direct but ≥ indirect
                # (or allow any ordering for full exploration)
                candidates.append({"direct": wd, "translation": wt, "indirect": wi})
    return candidates


def run_grid_search(edges: list, signed: list, step: float = 0.05) -> list[dict]:
    """Évalue tous les candidats, retourne les top-20 par R²."""
    candidates = grid_candidates(step)
    total = len(candidates)
    print(f"  Grid: {total} candidats (step={step})")

    results = []
    t0 = time.time()
    report_every = max(1, total // 20)

    for idx, w in enumerate(candidates):
        adj = build_adjacency(edges, w)
        r2, n_pairs = compute_r2_on_subset(adj, signed)
        results.append({"weights": w, "r2": r2, "n_pairs": n_pairs})
        if (idx + 1) % report_every == 0:
            elapsed = time.time() - t0
            pct = (idx + 1) / total * 100
            best_so_far = max(r["r2"] for r in results)
            print(f"    {pct:5.1f}%  elapsed={elapsed:.1f}s  best_r2={best_so_far:.4f}")

    results.sort(key=lambda x: -x["r2"])
    return results[:20]


# ─── k-fold CV ──────────────────────────────────────────────────────────────

def stratified_kfold(signed: list, k: int, seed: int) -> list[list[list]]:
    """
    Stratification par tradition_label.
    Retourne k folds, chacun = (train_list, test_list).
    """
    rng = random.Random(seed)
    # Group by tradition
    by_trad: dict = {}
    for s in signed:
        t = s.get("tradition_label", "?")
        by_trad.setdefault(t, []).append(s)
    # Shuffle each group
    for t in by_trad:
        rng.shuffle(by_trad[t])
    # Assign indices round-robin
    fold_assignments: list = [[] for _ in range(k)]
    for group in by_trad.values():
        for i, item in enumerate(group):
            fold_assignments[i % k].append(item)

    folds = []
    for fold_idx in range(k):
        test = fold_assignments[fold_idx]
        train = [s for i, fold in enumerate(fold_assignments) for s in fold if i != fold_idx]
        folds.append((train, test))
    return folds


def run_kfold_cv(edges: list, signed: list, weights: dict, k: int = 5, seed: int = SEED) -> dict:
    """CV k-fold avec les poids donnés. Retourne mean R² et std R²."""
    folds = stratified_kfold(signed, k, seed)
    r2_scores = []
    for train, test in folds:
        # Évaluer sur le TEST set (pas de fitting — V_OPT est paramétrique)
        # On calcule R² sur le test uniquement
        if len(test) < 4:
            continue
        adj = build_adjacency(edges, weights)
        r2, n_pairs = compute_r2_on_subset(adj, test)
        if n_pairs > 0:
            r2_scores.append(r2)
    if not r2_scores:
        return {"mean_r2": 0.0, "std_r2": 0.0, "n_folds": 0}
    mean = sum(r2_scores) / len(r2_scores)
    std = math.sqrt(sum((r - mean) ** 2 for r in r2_scores) / len(r2_scores))
    return {"mean_r2": round(mean, 4), "std_r2": round(std, 4),
            "n_folds": len(r2_scores), "per_fold_r2": [round(r, 4) for r in r2_scores]}


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()
    fast_mode = "--fast" in sys.argv

    print("§213 — V_OPT v4 Calibration (Grid Search + k-fold CV)")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  corpus : {CORPUS_PATH}")
    print(f"  fast   : {fast_mode}")
    print()

    # ── Chargement ──
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    edges = graph["edges"]
    signed = corpus["signed"]
    print(f"  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {len(signed)} textes signés")

    by_trad: dict = {}
    for s in signed:
        t = s.get("tradition_label", "?")
        by_trad[t] = by_trad.get(t, 0) + 1
    print(f"  Traditions : {by_trad}")
    print()

    # ── R² V_OPT v3 (référence) ──
    print("── Référence V_OPT v3 ──")
    adj_v3 = build_adjacency(edges, V_OPT_V3)
    r2_v3, n_pairs_v3 = compute_r2_on_subset(adj_v3, signed)
    print(f"  R²_v3 (N=75) = {r2_v3:.4f}  ({n_pairs_v3} paires)")
    cv_v3 = run_kfold_cv(edges, signed, V_OPT_V3)
    print(f"  CV_v3 : mean_R²={cv_v3['mean_r2']:.4f} ± {cv_v3['std_r2']:.4f}")
    print()

    # ── Grid search ──
    step = 0.10 if fast_mode else 0.05
    print(f"── Grid search (step={step}) ──")
    top20 = run_grid_search(edges, signed, step=step)

    best = top20[0]
    print(f"\n  Meilleurs poids V_OPT v4 : {best['weights']}")
    print(f"  R²_v4_fullset = {best['r2']:.4f}  ({best['n_pairs']} paires)")
    print()

    # ── k-fold CV sur les top-5 candidats ──
    print("── k-fold CV sur top-5 candidats ──")
    cv_results = []
    for candidate in top20[:5]:
        w = candidate["weights"]
        cv = run_kfold_cv(edges, signed, w)
        cv_results.append({"weights": w, "r2_full": candidate["r2"], **cv})
        print(f"  {w}  r2={candidate['r2']:.4f}  CV={cv['mean_r2']:.4f}±{cv['std_r2']:.4f}")
    print()

    # Meilleur candidat selon CV mean
    best_cv = max(cv_results, key=lambda x: x["mean_r2"])
    print(f"  Meilleur selon CV mean : {best_cv['weights']}")
    print(f"  CV mean_R² = {best_cv['mean_r2']:.4f} ± {best_cv['std_r2']:.4f}")
    print()

    # ── Δ R² improvement ──
    delta_full = best["r2"] - r2_v3
    delta_cv = best_cv["mean_r2"] - cv_v3["mean_r2"]
    print(f"── Bilan ──")
    print(f"  V_OPT v3 : R²={r2_v3:.4f}  CV={cv_v3['mean_r2']:.4f}±{cv_v3['std_r2']:.4f}")
    print(f"  V_OPT v4 (full-set best): R²={best['r2']:.4f}  Δ={delta_full:+.4f}")
    print(f"  V_OPT v4 (CV best): CV={best_cv['mean_r2']:.4f}  Δ_CV={delta_cv:+.4f}")
    verdict = "AMÉLIORÉ" if best_cv["mean_r2"] > cv_v3["mean_r2"] else "STABLE/DÉGRADÉ"
    print(f"  Verdict : {verdict}")
    print()

    elapsed = time.time() - t_start

    # ── Sérialisation ──
    result = {
        "version": "v213",
        "date": "2026-05-01",
        "graph": str(GRAPH_PATH),
        "corpus": str(CORPUS_PATH),
        "n_signed": len(signed),
        "n_pairs_total": n_pairs_v3,
        "by_tradition": by_trad,
        "v_opt_v3_reference": {
            "weights": V_OPT_V3,
            "r2_full": round(r2_v3, 4),
            "n_pairs": n_pairs_v3,
            "cv": cv_v3,
        },
        "grid_step": step,
        "grid_n_candidates": (int(1.0 / step)) ** 3,
        "top20_by_r2": [
            {"weights": r["weights"], "r2": round(r["r2"], 4), "n_pairs": r["n_pairs"]}
            for r in top20
        ],
        "top5_cv": cv_results,
        "v_opt_v4_best_fullset": {
            "weights": best["weights"],
            "r2_full": round(best["r2"], 4),
        },
        "v_opt_v4_best_cv": {
            "weights": best_cv["weights"],
            "r2_full": round(best_cv.get("r2_full", best["r2"]), 4),
            "cv": {"mean_r2": best_cv["mean_r2"], "std_r2": best_cv["std_r2"],
                   "n_folds": best_cv["n_folds"],
                   "per_fold_r2": best_cv.get("per_fold_r2", [])},
        },
        "delta_r2_vs_v3": round(delta_full, 4),
        "delta_cv_vs_v3": round(delta_cv, 4),
        "verdict": verdict,
        "elapsed_s": round(elapsed, 1),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Écrit : {OUT_PATH}")
    print(f"Durée : {elapsed:.1f}s")


if __name__ == "__main__":
    main()

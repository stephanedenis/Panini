#!/usr/bin/env python3
"""
§220 — V_OPT v5 Calibration sur graph v13 (Grid Search + k-fold CV)
=====================================================================
Recalibration des poids V_OPT sur :
  - graph v13 (nipada_v219_graph_v13.json) : +11 arêtes cross-tradition
  - corpus v212f (75 textes, 3 traditions)

Méthode identique à §213 mais parallélisée via multiprocessing.Pool.
V_OPT v4 (référence) : {direct: 0.1, translation: 0.1, indirect: 1.0}
  R²_v4 (graph v12) = 0.0482, CV = 0.0792 ± 0.0604
  R²_v4 (graph v13) = 0.1442, CV = 0.1524 ± 0.0420  (BUDDHIST_AXIAL connecté)

Usage:
    python3 scripts/nipada_vopt_calibration_v220.py [--fine]
    --fine : step=0.05 (défaut step=0.10)
    --workers N : nombre de workers (défaut: nproc-2)
"""

import json
import heapq
import math
import time
import sys
import random
import os
import multiprocessing as mp
from pathlib import Path

# ─── Chemins ───────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH  = _NIPADA / "falsification/nipada_v219_graph_v13.json"
CORPUS_PATH = _NIPADA / "corpus/signed_corpus_v212f.json"
OUT_PATH    = _NIPADA / "falsification/nipada_v220_vopt_calibration.json"

# ─── V_OPT v4 référence ────────────────────────────────────────────────────
V_OPT_V4 = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}

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


def build_adjacency(edges, weights):
    adj = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = weights[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(source, adj, targets):
    dist = {source: 0.0}
    pq = [(0.0, source)]
    remaining = set(targets) - {source}
    found = {}
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

def v14_vector(sig):
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r(xs, ys):
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


def compute_r2_on_subset(adj, subset):
    ids = [s["graph_node_id"] for s in subset]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset}
    id_set = set(ids)
    d_topo_list = []
    d_lex_list = []
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


# ─── Grid search parallélisé ────────────────────────────────────────────────

def grid_candidates(step=0.10):
    vals = [round(step * k, 4) for k in range(1, int(1.0 / step) + 1)]
    candidates = []
    for wd in vals:
        for wt in vals:
            for wi in vals:
                candidates.append({"direct": wd, "translation": wt, "indirect": wi})
    return candidates


# Variables globales pour les workers (évite sérialisation répétée)
_EDGES_GLOBAL = None
_SIGNED_GLOBAL = None


def _worker_init(edges_pkl, signed_pkl):
    """Initialise les données dans chaque worker."""
    global _EDGES_GLOBAL, _SIGNED_GLOBAL
    _EDGES_GLOBAL = edges_pkl
    _SIGNED_GLOBAL = signed_pkl


def _eval_candidate(w):
    """Évalue un candidat (appelé dans un worker)."""
    adj = build_adjacency(_EDGES_GLOBAL, w)
    r2, n_pairs = compute_r2_on_subset(adj, _SIGNED_GLOBAL)
    return {"weights": w, "r2": r2, "n_pairs": n_pairs}


def run_grid_search(edges, signed, step=0.10, n_workers=14):
    candidates = grid_candidates(step)
    total = len(candidates)
    print(f"  Grid: {total} candidats (step={step}, workers={n_workers})")

    t0 = time.time()
    results = []
    chunk = max(1, total // (n_workers * 4))  # lots équilibrés

    with mp.Pool(
        processes=n_workers,
        initializer=_worker_init,
        initargs=(edges, signed),
    ) as pool:
        for i, res in enumerate(pool.imap_unordered(_eval_candidate, candidates, chunksize=chunk)):
            results.append(res)
            if (i + 1) % max(1, total // 10) == 0:
                elapsed = time.time() - t0
                pct = (i + 1) / total * 100
                best_so_far = max(r["r2"] for r in results)
                print(f"    {pct:5.1f}%  elapsed={elapsed:.1f}s  best_r2={best_so_far:.4f}")

    elapsed = time.time() - t0
    print(f"  Grid terminé en {elapsed:.1f}s ({total/elapsed:.0f} candidats/s)")
    results.sort(key=lambda x: -x["r2"])
    return results[:20]


# ─── k-fold CV ──────────────────────────────────────────────────────────────

def stratified_kfold(signed, k, seed):
    rng = random.Random(seed)
    by_trad = {}
    for s in signed:
        t = s.get("tradition_label", "?")
        by_trad.setdefault(t, []).append(s)
    for t in by_trad:
        rng.shuffle(by_trad[t])
    fold_assignments = [[] for _ in range(k)]
    for group in by_trad.values():
        for i, item in enumerate(group):
            fold_assignments[i % k].append(item)
    folds = []
    for fold_idx in range(k):
        test = fold_assignments[fold_idx]
        train = [s for i, fold in enumerate(fold_assignments) for s in fold if i != fold_idx]
        folds.append((train, test))
    return folds


def run_kfold_cv(edges, signed, weights, k=5, seed=SEED):
    folds = stratified_kfold(signed, k, seed)
    r2_scores = []
    for train, test in folds:
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

    print("§220 — V_OPT v5 Calibration (graph v13 + corpus v212f) [multiprocessing]")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  corpus : {CORPUS_PATH}")
    step = 0.05 if "--fine" in sys.argv else 0.10

    # Détecter nombre de workers
    n_cpu = os.cpu_count() or 4
    n_workers_default = max(1, n_cpu - 2)
    n_workers = n_workers_default
    for i, arg in enumerate(sys.argv):
        if arg == "--workers" and i + 1 < len(sys.argv):
            n_workers = int(sys.argv[i + 1])

    print(f"  step   : {step}  (--fine pour step=0.05)")
    print(f"  workers: {n_workers}/{n_cpu} (--workers N pour changer)")
    print()

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    edges = graph["edges"]
    signed = corpus["signed"]
    print(f"  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {len(signed)} textes signés")
    by_trad = {}
    for s in signed:
        t = s.get("tradition_label", "?")
        by_trad[t] = by_trad.get(t, 0) + 1
    print(f"  Traditions : {by_trad}")
    print()

    # Référence V_OPT v4
    print("── Référence V_OPT v4 (graph v13) ──")
    adj_v4 = build_adjacency(edges, V_OPT_V4)
    r2_v4, n_pairs_v4 = compute_r2_on_subset(adj_v4, signed)
    print(f"  R²_v4 (N=75) = {r2_v4:.4f}  ({n_pairs_v4} paires)")
    cv_v4 = run_kfold_cv(edges, signed, V_OPT_V4)
    print(f"  CV_v4 : mean_R²={cv_v4['mean_r2']:.4f} ± {cv_v4['std_r2']:.4f}")
    print()

    # Grid search parallélisé
    print(f"── Grid search (step={step}, workers={n_workers}) ──")
    top20 = run_grid_search(edges, signed, step=step, n_workers=n_workers)
    best = top20[0]
    print(f"\n  Meilleurs poids V_OPT v5 : {best['weights']}")
    print(f"  R²_v5_fullset = {best['r2']:.4f}  ({best['n_pairs']} paires)")
    print()

    # k-fold CV top-5
    print("── k-fold CV sur top-5 candidats ──")
    cv_results = []
    for candidate in top20[:5]:
        w = candidate["weights"]
        cv = run_kfold_cv(edges, signed, w)
        cv_results.append({"weights": w, "r2_full": candidate["r2"], **cv})
        print(f"  {w}  r2={candidate['r2']:.4f}  CV={cv['mean_r2']:.4f}±{cv['std_r2']:.4f}")
    print()

    best_cv = max(cv_results, key=lambda x: x["mean_r2"])
    print(f"  Meilleur selon CV mean : {best_cv['weights']}")
    print(f"  CV mean_R² = {best_cv['mean_r2']:.4f} ± {best_cv['std_r2']:.4f}")
    print()

    delta_full = best["r2"] - r2_v4
    delta_cv = best_cv["mean_r2"] - cv_v4["mean_r2"]
    print("── Bilan ──")
    print(f"  V_OPT v4 (graph v12) : R²={r2_v4:.4f}  CV={cv_v4['mean_r2']:.4f}±{cv_v4['std_r2']:.4f}")
    print(f"  V_OPT v5 (graph v13 full-set): R²={best['r2']:.4f}  Δ={delta_full:+.4f}")
    print(f"  V_OPT v5 (graph v13 CV best) : CV={best_cv['mean_r2']:.4f}  Δ_CV={delta_cv:+.4f}")
    verdict = "AMÉLIORÉ" if best_cv["mean_r2"] > cv_v4["mean_r2"] else "STABLE/DÉGRADÉ"
    print(f"  Verdict : {verdict}")
    print()

    elapsed = time.time() - t_start
    result = {
        "section": "§220",
        "description": "V_OPT v5 calibration sur graph v13 (BUDDHIST_AXIAL connecté)",
        "graph": str(GRAPH_PATH),
        "corpus": str(CORPUS_PATH),
        "n_signed": len(signed),
        "n_pairs_total": n_pairs_v4,
        "by_tradition": by_trad,
        "v_opt_v4_reference_on_v13": {
            "weights": V_OPT_V4,
            "r2_full": round(r2_v4, 4),
            "n_pairs": n_pairs_v4,
            "cv": cv_v4,
        },
        "grid_step": step,
        "grid_n_candidates": (int(1.0 / step)) ** 3,
        "top20_by_r2": [
            {"weights": r["weights"], "r2": round(r["r2"], 4), "n_pairs": r["n_pairs"]}
            for r in top20
        ],
        "top5_cv": cv_results,
        "v_opt_v5_best_fullset": {
            "weights": best["weights"],
            "r2_full": round(best["r2"], 4),
        },
        "v_opt_v5_best_cv": {
            "weights": best_cv["weights"],
            "r2_full": round(best_cv.get("r2_full", best["r2"]), 4),
            "cv": {
                "mean_r2": best_cv["mean_r2"],
                "std_r2": best_cv["std_r2"],
                "n_folds": best_cv["n_folds"],
                "per_fold_r2": best_cv.get("per_fold_r2", []),
            },
        },
        "delta_r2_vs_v4": round(delta_full, 4),
        "delta_cv_vs_v4": round(delta_cv, 4),
        "verdict": verdict,
        "elapsed_s": round(elapsed, 1),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Écrit : {OUT_PATH}")
    print(f"Durée : {elapsed:.1f}s")


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)  # Linux : fork pour partager la mémoire
    main()

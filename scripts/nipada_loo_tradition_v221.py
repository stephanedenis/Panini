#!/usr/bin/env python3
"""
§221 — LOO v2 Tradition-Out Validation (graph v13 + V_OPT v5)
==============================================================
Leave-One-Tradition-Out (LOO) sur :
  - graph v13 (nipada_v219_graph_v13.json) : BUDDHIST_AXIAL connecté
  - corpus v212f (75 textes)
  - V_OPT v5 (chargé depuis nipada_v220_vopt_calibration.json, fallback v4)

Comparaison avec §214 (graph v12) :
  - R²_all v12 : ?  → v13 : ?
  - Vérifier si BUDDHIST_AXIAL intra-R² change (était isolé → distances infinies)

Usage:
    python3 scripts/nipada_loo_tradition_v221.py
"""

import json
import heapq
import math
import time
import multiprocessing as mp
import os
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH  = _NIPADA / "falsification/nipada_v219_graph_v13.json"
CORPUS_PATH = _NIPADA / "corpus/signed_corpus_v212f.json"
V220_PATH   = _NIPADA / "falsification/nipada_v220_vopt_calibration.json"
V214_PATH   = _NIPADA / "falsification/nipada_v214_loo_tradition.json"
OUT_PATH    = _NIPADA / "falsification/nipada_v221_loo_tradition.json"

# Fallback si §220 pas encore disponible
V_OPT_V4 = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

LOO_TRADITIONS = ["BUDDHIST_AXIAL", "INDIAN_AXIAL", "CHINESE_AXIAL"]


# ─── V_OPT helpers ─────────────────────────────────────────────────────────

def classify_channel(ch):
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


# ─── Statistiques ──────────────────────────────────────────────────────────

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


def compute_r2_subset(adj, subset_a, subset_b=None):
    """Calcule R²(d_topo, d_lex). Si subset_b=None, paires intra subset_a."""
    intra = subset_b is None
    if intra:
        ids_a = [s["graph_node_id"] for s in subset_a]
        ids_b = ids_a
        sigs_a = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_a}
        sigs_b = sigs_a
    else:
        ids_a = [s["graph_node_id"] for s in subset_a]
        ids_b = [s["graph_node_id"] for s in subset_b]
        sigs_a = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_a}
        sigs_b = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_b}

    target_b = set(ids_b)
    d_topo_list = []
    d_lex_list = []
    for i, id_a in enumerate(ids_a):
        distances = dijkstra_from(id_a, adj, target_b)
        start_j = i + 1 if intra else 0
        iter_b = ids_a[i + 1:] if intra else ids_b
        for id_b in iter_b:
            dt = distances.get(id_b, math.inf)
            if math.isinf(dt):
                continue
            dl = l2_distance(sigs_a[id_a], sigs_b[id_b])
            d_topo_list.append(dt)
            d_lex_list.append(dl)

    if len(d_topo_list) < 2:
        return 0.0, len(d_topo_list)
    r = pearson_r(d_topo_list, d_lex_list)
    return r * r, len(d_topo_list)


# ─── Worker parallèle pour les LOO ─────────────────────────────────────────

_ADJ_GLOBAL = None
_BY_TRAD_GLOBAL = None
_SIGNED_GLOBAL = None


def _worker_init_loo(adj, by_trad, signed):
    global _ADJ_GLOBAL, _BY_TRAD_GLOBAL, _SIGNED_GLOBAL
    _ADJ_GLOBAL = adj
    _BY_TRAD_GLOBAL = by_trad
    _SIGNED_GLOBAL = signed


def _eval_loo_trad(trad):
    """Calcule tous les R² pour une tradition LOO."""
    subset_t = _BY_TRAD_GLOBAL.get(trad, [])
    others = [s for s in _SIGNED_GLOBAL if s.get("tradition_label") != trad]
    other_trads = [t for t in LOO_TRADITIONS if t != trad]

    # Intra-t
    r2_intra, n_intra = compute_r2_subset(_ADJ_GLOBAL, subset_t)

    # Cross t vs each other tradition
    cross = {}
    for ot in other_trads:
        ot_subset = _BY_TRAD_GLOBAL.get(ot, [])
        r2_c, n_c = compute_r2_subset(_ADJ_GLOBAL, subset_t, ot_subset)
        cross[ot] = {"r2": round(r2_c, 4), "n_pairs": n_c}

    # LOO-train (autres) intra
    r2_train, n_train = compute_r2_subset(_ADJ_GLOBAL, others)

    # LOO-test: paires entre subset_t et all others
    r2_test, n_test = compute_r2_subset(_ADJ_GLOBAL, subset_t, others)

    return trad, {
        "n_texts": len(subset_t),
        "r2_intra": round(r2_intra, 4),
        "n_pairs_intra": n_intra,
        "r2_train_intra": round(r2_train, 4),
        "n_pairs_train": n_train,
        "r2_test_cross": round(r2_test, 4),
        "n_pairs_test": n_test,
        "cross_vs_others": cross,
    }


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()
    print("§221 — LOO v2 (graph v13 + V_OPT v5)")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  corpus : {CORPUS_PATH}")

    # Charger V_OPT v5 (ou fallback v4)
    if V220_PATH.exists():
        v220 = json.loads(V220_PATH.read_text())
        vopt = v220.get("v_opt_v5_best_cv", {}).get("weights", V_OPT_V4)
        vopt_version = "v5"
        print(f"  V_OPT v5 chargé : {vopt}")
    else:
        vopt = V_OPT_V4
        vopt_version = "v4 (fallback)"
        print(f"  V_OPT v4 (fallback) : {vopt}")

    graph = json.loads(GRAPH_PATH.read_text())
    corpus = json.loads(CORPUS_PATH.read_text())
    edges = graph["edges"]
    signed = corpus["signed"]

    print(f"  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {len(signed)} textes")

    by_trad = {}
    for s in signed:
        t = s.get("tradition_label", "?")
        by_trad.setdefault(t, []).append(s)
    for t, texts in sorted(by_trad.items()):
        print(f"    {t}: {len(texts)} textes")
    print()

    adj = build_adjacency(edges, vopt)

    # R² global
    print("── R² global ──")
    r2_all, n_all = compute_r2_subset(adj, signed)
    print(f"  R²_all = {r2_all:.4f}  ({n_all} paires)")

    # LOO parallèle (3 traditions, 3 workers suffit)
    n_workers = min(3, os.cpu_count() or 1)
    print(f"\n── LOO par tradition (workers={n_workers}) ──")

    with mp.Pool(
        processes=n_workers,
        initializer=_worker_init_loo,
        initargs=(adj, by_trad, signed),
    ) as pool:
        loo_list = pool.map(_eval_loo_trad, LOO_TRADITIONS)

    loo_results = dict(loo_list)

    # Affichage
    for trad in LOO_TRADITIONS:
        res = loo_results[trad]
        print(f"\n  {trad} ({res['n_texts']} textes):")
        print(f"    R²_intra   = {res['r2_intra']:.4f}  ({res['n_pairs_intra']} paires)")
        print(f"    R²_test_cross = {res['r2_test_cross']:.4f}  ({res['n_pairs_test']} paires trad vs others)")
        print(f"    R²_train   = {res['r2_train_intra']:.4f}  ({res['n_pairs_train']} paires sans cette trad)")
        for ot, cv in res["cross_vs_others"].items():
            print(f"    vs {ot}: R²={cv['r2']:.4f}  ({cv['n_pairs']} paires)")

    # Comparer avec §214 (v12)
    if V214_PATH.exists():
        v214 = json.loads(V214_PATH.read_text())
        r2_all_v12 = v214.get("r2_all", 0.0)
        print(f"\n── Δ vs §214 (graph v12) ──")
        print(f"  R²_all v12={r2_all_v12:.4f} → v13={r2_all:.4f}  (Δ={r2_all - r2_all_v12:+.4f})")
        for trad in LOO_TRADITIONS:
            r2_intra_v12 = v214.get("intra_tradition", {}).get(trad, {}).get("r2", 0.0)
            r2_intra_v13 = loo_results[trad]["r2_intra"]
            print(f"  {trad} intra: v12={r2_intra_v12:.4f} → v13={r2_intra_v13:.4f}  (Δ={r2_intra_v13 - r2_intra_v12:+.4f})")

    # Verdict
    mean_intra = sum(loo_results[t]["r2_intra"] for t in LOO_TRADITIONS) / len(LOO_TRADITIONS)
    verdict = "INTRA_DOMINATED" if mean_intra > r2_all * 1.5 else "BALANCED"
    print(f"\n  Mean R²_intra = {mean_intra:.4f}  (vs R²_all={r2_all:.4f})")
    print(f"  Verdict : {verdict}")

    elapsed = time.time() - t_start

    result = {
        "section": "§221",
        "description": "LOO v2 sur graph v13 + V_OPT v5",
        "vopt_version": vopt_version,
        "vopt_weights": vopt,
        "graph_version": "v13",
        "corpus_version": corpus.get("version"),
        "n_signed": len(signed),
        "n_pairs_all": n_all,
        "r2_all": round(r2_all, 4),
        "loo_results": {t: loo_results[t] for t in LOO_TRADITIONS},
        "mean_r2_intra": round(mean_intra, 4),
        "verdict": verdict,
        "elapsed_s": round(elapsed, 1),
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nÉcrit : {OUT_PATH}")
    print(f"Durée : {elapsed:.1f}s")


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)
    main()

#!/usr/bin/env python3
"""
§227 — Outlier analysis par œuvre
====================================
Pour chaque texte signé, calcule sa contribution marginale au R² global.
Identifie les top-K outliers positifs (qui augmentent R²) et négatifs
(qui le font baisser).

Stratégie : LOO par texte — retirer un texte à la fois et mesurer ΔR².
  ΔR²_i = R²_full - R²_without_i
  ΔR²_i > 0 → texte renforce le signal
  ΔR²_i < 0 → texte bruite le signal

Parallélisé : chaque leave-one-out est un worker indépendant.

Usage:
    python3 scripts/nipada_outlier_v227.py [--top-k N]
    --top-k N : nombre de top outliers à reporter (défaut 10)
"""

import json
import heapq
import math
import time
import sys
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
OUT_PATH    = _NIPADA / "falsification/nipada_v227_outliers.json"

V_OPT_FALLBACK = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}
TOP_K_DEFAULT = 10

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]


# ─── Core helpers ──────────────────────────────────────────────────────────

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


def v14_vector(sig):
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r2(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return (num / (sx * sy)) ** 2


def compute_r2(adj, subset):
    ids = [s["graph_node_id"] for s in subset]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset}
    id_set = set(ids)
    d_topo, d_lex = [], []
    for i in range(len(ids)):
        dists = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = dists[ids[j]]
            if math.isinf(dt):
                continue
            d_topo.append(dt)
            d_lex.append(l2_distance(sigs[ids[i]], sigs[ids[j]]))
    if len(d_topo) < 2:
        return 0.0, 0
    return pearson_r2(d_topo, d_lex), len(d_topo)


# ─── Worker LOO-par-texte ──────────────────────────────────────────────────

_ADJ_GLOBAL = None
_SIGNED_GLOBAL = None


def _init_worker_loo(adj, signed):
    global _ADJ_GLOBAL, _SIGNED_GLOBAL
    _ADJ_GLOBAL = adj
    _SIGNED_GLOBAL = signed


def _eval_loo_text(i):
    """R² du corpus sans le texte i."""
    subset = [s for j, s in enumerate(_SIGNED_GLOBAL) if j != i]
    r2, n_pairs = compute_r2(_ADJ_GLOBAL, subset)
    return i, r2, n_pairs


# ─── Analyse des distances (d_topo vs d_lex) par texte ─────────────────────

def per_text_distances(adj, signed):
    """Pour chaque texte : d_topo moyen et d_lex moyen vers ses voisins finis."""
    ids = [s["graph_node_id"] for s in signed]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    result = {}
    for i in range(len(ids)):
        dists = dijkstra_from(ids[i], adj, id_set)
        dt_list = []
        dl_list = []
        for j in range(len(ids)):
            if i == j:
                continue
            dt = dists[ids[j]]
            if math.isinf(dt):
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            dt_list.append(dt)
            dl_list.append(dl)
        if dt_list:
            result[ids[i]] = {
                "mean_d_topo": round(sum(dt_list) / len(dt_list), 4),
                "mean_d_lex": round(sum(dl_list) / len(dl_list), 4),
                "n_reachable": len(dt_list),
            }
        else:
            result[ids[i]] = {"mean_d_topo": None, "mean_d_lex": None, "n_reachable": 0}
    return result


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()

    top_k = TOP_K_DEFAULT
    for i, arg in enumerate(sys.argv):
        if arg == "--top-k" and i + 1 < len(sys.argv):
            top_k = int(sys.argv[i + 1])

    n_cpu = os.cpu_count() or 4
    n_workers = max(1, n_cpu - 2)

    print("§227 — Outlier analysis par œuvre (graph v13)")
    print(f"  top_k={top_k}, workers={n_workers}/{n_cpu}")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  corpus : {CORPUS_PATH}")

    # V_OPT v5 ou fallback
    if V220_PATH.exists():
        v220 = json.loads(V220_PATH.read_text())
        vopt = v220.get("v_opt_v5_best_cv", {}).get("weights", V_OPT_FALLBACK)
        vopt_version = "v5"
        print(f"  V_OPT v5 : {vopt}")
    else:
        vopt = V_OPT_FALLBACK
        vopt_version = "v4 (fallback)"
        print(f"  V_OPT v4 (fallback) : {vopt}")

    graph = json.loads(GRAPH_PATH.read_text())
    corpus = json.loads(CORPUS_PATH.read_text())
    edges = graph["edges"]
    signed = corpus["signed"]
    print(f"  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {len(signed)} textes signés\n")

    adj = build_adjacency(edges, vopt)

    # R² global
    r2_full, n_full = compute_r2(adj, signed)
    print(f"  R²_full = {r2_full:.4f}  ({n_full} paires)")

    # Distances moyennes par texte
    print("  Calcul des distances moyennes par texte...", end=" ", flush=True)
    t_dist = time.time()
    dist_stats = per_text_distances(adj, signed)
    print(f"ok ({time.time()-t_dist:.1f}s)")

    # LOO par texte (parallèle)
    print(f"\n── LOO par texte ({len(signed)} textes, {n_workers} workers) ──")
    t_loo = time.time()
    with mp.Pool(
        processes=n_workers,
        initializer=_init_worker_loo,
        initargs=(adj, signed),
    ) as pool:
        loo_raw = pool.map(_eval_loo_text, range(len(signed)))

    elapsed_loo = time.time() - t_loo
    print(f"  LOO terminé ({elapsed_loo:.1f}s)")

    # Calcul des deltas
    text_stats = []
    for i, r2_loo, n_loo in loo_raw:
        s = signed[i]
        delta = r2_full - r2_loo  # positif = texte renforce R²
        nid = s["graph_node_id"]
        ds = dist_stats.get(nid, {})
        text_stats.append({
            "index": i,
            "graph_node_id": nid,
            "title": s.get("title", nid),
            "tradition": s.get("tradition_label", "?"),
            "r2_without": round(r2_loo, 4),
            "delta_r2": round(delta, 4),
            "n_pairs_without": n_loo,
            "mean_d_topo": ds.get("mean_d_topo"),
            "mean_d_lex": ds.get("mean_d_lex"),
            "n_reachable": ds.get("n_reachable", 0),
        })

    # Trier par ΔR² décroissant
    text_stats.sort(key=lambda x: x["delta_r2"], reverse=True)

    top_positive = text_stats[:top_k]
    top_negative = sorted(text_stats, key=lambda x: x["delta_r2"])[:top_k]

    print(f"\n── Top-{top_k} textes qui renforcent R² (ΔR²_i > 0) ──")
    for t in top_positive:
        print(f"  Δ={t['delta_r2']:+.4f}  {t['graph_node_id']:35s}  [{t['tradition']}]")

    print(f"\n── Top-{top_k} textes qui bruitent R² (ΔR²_i < 0) ──")
    for t in top_negative:
        print(f"  Δ={t['delta_r2']:+.4f}  {t['graph_node_id']:35s}  [{t['tradition']}]")

    elapsed = time.time() - t_start

    result = {
        "section": "§227",
        "description": "Outlier analysis par œuvre — LOO individuel",
        "graph_version": "v13",
        "corpus_version": corpus.get("version"),
        "vopt_version": vopt_version,
        "vopt_weights": vopt,
        "n_signed": len(signed),
        "r2_full": round(r2_full, 4),
        "n_pairs_full": n_full,
        "all_texts": text_stats,
        "top_k": top_k,
        "top_positive": top_positive,
        "top_negative": top_negative,
        "elapsed_s": round(elapsed, 1),
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nÉcrit : {OUT_PATH}")
    print(f"Durée totale : {elapsed:.1f}s")


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)
    main()

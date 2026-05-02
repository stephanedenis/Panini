#!/usr/bin/env python3
"""
§223 — Significance test R² v5 (permutation des paires)
=========================================================
Test de significativité de R²_v5 par permutation des paires (d_topo, d_lex).

Contrairement au §222 (shuffle des labels/channels), ici on mélange
directement les vecteurs de distances :
  - On calcule toutes les N(N-1)/2 paires (d_topo_i, d_lex_i)
  - On permute les d_lex en gardant d_topo fixe
  → Distribution nulle sous H0 : "aucune corrélation topo-lex"

N_PERM = 1000 (parallélisé sur N-2 workers).
Résultats : p-value, IC 95%, z-score, delta R²_v5 vs R²_v4.

Usage:
    python3 scripts/nipada_significance_v223.py [--perms N]
"""

import json
import heapq
import math
import random
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
OUT_PATH    = _NIPADA / "falsification/nipada_v223_significance.json"

V_OPT_FALLBACK = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}
N_PERM_DEFAULT = 1000
SEED = 2023

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


def build_pairs(adj, signed):
    """Calcule toutes les paires finies (d_topo, d_lex)."""
    ids = [s["graph_node_id"] for s in signed]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    pairs = []
    for i in range(len(ids)):
        dists = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = dists[ids[j]]
            if math.isinf(dt):
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            pairs.append((dt, dl))
    return pairs


# ─── Worker parallèle ──────────────────────────────────────────────────────

_DTOPO_GLOBAL = None
_DLEX_GLOBAL = None


def _init_worker_perm(dtopo, dlex):
    global _DTOPO_GLOBAL, _DLEX_GLOBAL
    _DTOPO_GLOBAL = dtopo
    _DLEX_GLOBAL = dlex


def _worker_perm(seed):
    rng = random.Random(seed)
    shuffled_lex = list(_DLEX_GLOBAL)
    rng.shuffle(shuffled_lex)
    return pearson_r2(_DTOPO_GLOBAL, shuffled_lex)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()

    n_perm = N_PERM_DEFAULT
    for i, arg in enumerate(sys.argv):
        if arg == "--perms" and i + 1 < len(sys.argv):
            n_perm = int(sys.argv[i + 1])

    n_cpu = os.cpu_count() or 4
    n_workers = max(1, n_cpu - 2)

    print("§223 — Significance test R² (permutation paires d_topo vs d_lex)")
    print(f"  n_perm={n_perm}, workers={n_workers}/{n_cpu}")
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
    print(f"  Corpus : {len(signed)} textes signés")

    adj = build_adjacency(edges, vopt)

    # Calcul des paires (une seule fois)
    print("\n  Calcul des paires (d_topo, d_lex)...", end=" ", flush=True)
    t_pairs = time.time()
    pairs = build_pairs(adj, signed)
    print(f"{len(pairs)} paires finies ({time.time()-t_pairs:.1f}s)")

    d_topo = [p[0] for p in pairs]
    d_lex  = [p[1] for p in pairs]

    r2_obs = pearson_r2(d_topo, d_lex)
    print(f"  R²_obs = {r2_obs:.4f}  ({len(pairs)} paires)\n")

    # Permutation test parallèle
    mp.set_start_method("fork", force=True)
    print(f"── Permutation test ({n_perm} perms, {n_workers} workers) ──")
    t_perm = time.time()
    seeds = list(range(SEED, SEED + n_perm))
    chunk = max(1, n_perm // (n_workers * 4))
    r2_perms = []

    with mp.Pool(
        processes=n_workers,
        initializer=_init_worker_perm,
        initargs=(d_topo, d_lex),
    ) as pool:
        for i, r2_p in enumerate(pool.imap_unordered(_worker_perm, seeds, chunksize=chunk)):
            r2_perms.append(r2_p)
            if (i + 1) % max(1, n_perm // 10) == 0:
                print(f"  {(i+1)/n_perm*100:.0f}%  elapsed={time.time()-t_perm:.1f}s")

    elapsed_perm = time.time() - t_perm
    mean_p = sum(r2_perms) / len(r2_perms)
    std_p = math.sqrt(sum((r - mean_p) ** 2 for r in r2_perms) / len(r2_perms))
    p_value = sum(1 for r in r2_perms if r >= r2_obs) / len(r2_perms)
    z_score = (r2_obs - mean_p) / std_p if std_p > 0 else float("inf")

    # Intervalle de confiance 95% de R²_obs (bootstrap approximation via permutations)
    r2_sorted = sorted(r2_perms)
    ci_lo = r2_sorted[int(0.025 * len(r2_sorted))]
    ci_hi = r2_sorted[int(0.975 * len(r2_sorted))]

    # Comparaison avec v4 référence
    delta_vs_v4 = r2_obs - 0.1442  # R²_v4 sur graph v13

    print(f"\n── Résultats ──")
    print(f"  R²_obs       = {r2_obs:.4f}")
    print(f"  Mean_R²_perm = {mean_p:.4f} ± {std_p:.4f}")
    print(f"  IC 95% null  = [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"  p-value      = {p_value:.4f}  ({'SIGNIFICATIF p<0.01' if p_value < 0.01 else 'SIGNIFICATIF p<0.05' if p_value < 0.05 else 'NON SIGNIFICATIF'})")
    print(f"  z-score      = {z_score:.2f}")
    print(f"  Δ vs V_OPT v4 (R²=0.1442) = {delta_vs_v4:+.4f}")

    elapsed = time.time() - t_start

    result = {
        "section": "§223",
        "description": "Significance test R²_v5 par permutation des paires",
        "graph_version": "v13",
        "corpus_version": corpus.get("version"),
        "vopt_version": vopt_version,
        "vopt_weights": vopt,
        "n_signed": len(signed),
        "n_pairs_finite": len(pairs),
        "r2_observed": round(r2_obs, 4),
        "permutation_test": {
            "n_perm": n_perm,
            "mean_r2_perm": round(mean_p, 4),
            "std_r2_perm": round(std_p, 4),
            "ci_95_null": [round(ci_lo, 4), round(ci_hi, 4)],
            "p_value": round(p_value, 4),
            "z_score": round(z_score, 3),
            "significant_p01": p_value < 0.01,
            "significant_p05": p_value < 0.05,
            "elapsed_s": round(elapsed_perm, 1),
        },
        "delta_r2_vs_v4_on_v13": round(delta_vs_v4, 4),
        "r2_v4_reference": 0.1442,
        "elapsed_s": round(elapsed, 1),
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nÉcrit : {OUT_PATH}")
    print(f"Durée totale : {elapsed:.1f}s")


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)
    main()

#!/usr/bin/env python3
"""
§222 — Falsification : permutation tests sur graph v13 + corpus v212f
======================================================================
Deux tests de falsification :

Test A — Channel-shuffle :
  Réassigner aléatoirement les `channel` labels des arêtes tout en gardant
  la topologie (src, tgt). Si R² est dû au canal (direct vs indirect), la
  distribution shufflée doit couvrir R²_obs.

Test B — Node-label shuffle :
  Réassigner aléatoirement les signatures V14 des textes signés tout en
  gardant les positions dans le graphe. Si R² est un artefact des labels,
  la distribution shufflée doit couvrir R²_obs.

Les deux tests : N_PERM=1000 permutations, parallélisées sur N-2 workers.
p-value = fraction des R²_perm ≥ R²_obs.

Usage:
    python3 scripts/nipada_falsification_v222.py [--perms N]
    --perms N : nombre de permutations (défaut 1000)
"""

import json
import heapq
import math
import time
import sys
import random
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
OUT_PATH    = _NIPADA / "falsification/nipada_v222_falsification.json"

V_OPT_FALLBACK = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}
N_PERM_DEFAULT = 1000
SEED = 2026

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


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return num / (sx * sy)


def compute_r2(adj, signed):
    ids = [s["graph_node_id"] for s in signed]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    d_topo, d_lex = [], []
    for i in range(len(ids)):
        distances = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = distances[ids[j]]
            if math.isinf(dt):
                continue
            d_topo.append(dt)
            d_lex.append(l2_distance(sigs[ids[i]], sigs[ids[j]]))
    if len(d_topo) < 2:
        return 0.0, 0
    r = pearson_r(d_topo, d_lex)
    return r * r, len(d_topo)


# ─── Workers globaux ───────────────────────────────────────────────────────

_EDGES_GLOBAL = None
_CHANNELS_GLOBAL = None  # liste des channels (même ordre que edges)
_SIGNED_GLOBAL = None
_WEIGHTS_GLOBAL = None
_SIGS_GLOBAL = None       # liste de signatures (même ordre que signed)


def _init_workers(edges, channels, signed, weights, sigs):
    global _EDGES_GLOBAL, _CHANNELS_GLOBAL, _SIGNED_GLOBAL, _WEIGHTS_GLOBAL, _SIGS_GLOBAL
    _EDGES_GLOBAL = edges
    _CHANNELS_GLOBAL = channels
    _SIGNED_GLOBAL = signed
    _WEIGHTS_GLOBAL = weights
    _SIGS_GLOBAL = sigs


# ─── Test A : channel shuffle ───────────────────────────────────────────────

def _worker_channel_perm(seed):
    rng = random.Random(seed)
    shuffled = list(_CHANNELS_GLOBAL)
    rng.shuffle(shuffled)
    # Reconstruire edges avec channels mélangés
    edges_perm = []
    for e, ch in zip(_EDGES_GLOBAL, shuffled):
        edges_perm.append({**e, "channel": ch})
    adj_perm = build_adjacency(edges_perm, _WEIGHTS_GLOBAL)
    r2, _ = compute_r2(adj_perm, _SIGNED_GLOBAL)
    return r2


# ─── Test B : node-label (signature) shuffle ───────────────────────────────

def _worker_nodelabel_perm(seed):
    rng = random.Random(seed)
    shuffled_sigs = list(_SIGS_GLOBAL)
    rng.shuffle(shuffled_sigs)
    # Reconstruire signed avec signatures mélangées
    signed_perm = []
    for s, sig in zip(_SIGNED_GLOBAL, shuffled_sigs):
        signed_perm.append({**s, "v14_signature": sig})
    # Adjacence inchangée
    adj = build_adjacency(_EDGES_GLOBAL, _WEIGHTS_GLOBAL)
    r2, _ = compute_r2(adj, signed_perm)
    return r2


def run_permutation_test(worker_fn, n_perm, n_workers, r2_obs, test_name):
    seeds = list(range(SEED, SEED + n_perm))
    t0 = time.time()
    results = []
    chunk = max(1, n_perm // (n_workers * 4))
    reported = set()
    with mp.Pool(processes=n_workers) as pool:
        for i, r2_perm in enumerate(pool.imap_unordered(worker_fn, seeds, chunksize=chunk)):
            results.append(r2_perm)
            milestone = (i + 1) * 10 // n_perm
            if milestone not in reported and (i + 1) % max(1, n_perm // 10) == 0:
                reported.add(milestone)
                pct = (i + 1) / n_perm * 100
                print(f"    {test_name}: {pct:.0f}%  elapsed={time.time()-t0:.1f}s")

    elapsed = time.time() - t0
    p_value = sum(1 for r in results if r >= r2_obs) / len(results)
    mean_perm = sum(results) / len(results)
    std_perm = math.sqrt(sum((r - mean_perm) ** 2 for r in results) / len(results))
    z_score = (r2_obs - mean_perm) / std_perm if std_perm > 0 else float("inf")
    print(f"    {test_name}: R²_obs={r2_obs:.4f}  mean_perm={mean_perm:.4f}±{std_perm:.4f}"
          f"  p={p_value:.4f}  z={z_score:.2f}  ({elapsed:.1f}s)")
    return {
        "r2_observed": round(r2_obs, 4),
        "n_perm": n_perm,
        "mean_r2_perm": round(mean_perm, 4),
        "std_r2_perm": round(std_perm, 4),
        "p_value": round(p_value, 4),
        "z_score": round(z_score, 3),
        "elapsed_s": round(elapsed, 1),
        "significant_p01": p_value < 0.01,
        "significant_p05": p_value < 0.05,
    }


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()

    n_perm = N_PERM_DEFAULT
    for i, arg in enumerate(sys.argv):
        if arg == "--perms" and i + 1 < len(sys.argv):
            n_perm = int(sys.argv[i + 1])

    n_cpu = os.cpu_count() or 4
    n_workers = max(1, n_cpu - 2)

    print("§222 — Falsification : permutation tests (graph v13)")
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

    print(f"\n  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {len(signed)} textes signés")

    # Données partagées
    channels = [e["channel"] for e in edges]
    sigs = [s["v14_signature"] for s in signed]

    # R² observé
    adj_obs = build_adjacency(edges, vopt)
    r2_obs, n_pairs_obs = compute_r2(adj_obs, signed)
    print(f"\n  R²_obs = {r2_obs:.4f}  ({n_pairs_obs} paires)\n")

    # Initialiser workers (fork partage la mémoire)
    mp.set_start_method("fork", force=True)

    # Test A : channel shuffle
    print("── Test A : channel shuffle ──")
    with mp.Pool(
        processes=n_workers,
        initializer=_init_workers,
        initargs=(edges, channels, signed, vopt, sigs),
    ) as pool:
        seeds = list(range(SEED, SEED + n_perm))
        chunk = max(1, n_perm // (n_workers * 4))
        results_a = []
        t0 = time.time()
        for i, r2_perm in enumerate(pool.imap_unordered(_worker_channel_perm, seeds, chunksize=chunk)):
            results_a.append(r2_perm)
            if (i + 1) % max(1, n_perm // 10) == 0:
                print(f"    A: {(i+1)/n_perm*100:.0f}%  elapsed={time.time()-t0:.1f}s")

    elapsed_a = time.time() - t0
    p_a = sum(1 for r in results_a if r >= r2_obs) / len(results_a)
    mean_a = sum(results_a) / len(results_a)
    std_a = math.sqrt(sum((r - mean_a) ** 2 for r in results_a) / len(results_a))
    z_a = (r2_obs - mean_a) / std_a if std_a > 0 else float("inf")
    print(f"    A terminé: R²_obs={r2_obs:.4f}  mean_perm={mean_a:.4f}±{std_a:.4f}"
          f"  p={p_a:.4f}  z={z_a:.2f}  ({elapsed_a:.1f}s)")
    result_a = {
        "r2_observed": round(r2_obs, 4), "n_perm": n_perm,
        "mean_r2_perm": round(mean_a, 4), "std_r2_perm": round(std_a, 4),
        "p_value": round(p_a, 4), "z_score": round(z_a, 3),
        "elapsed_s": round(elapsed_a, 1),
        "significant_p01": p_a < 0.01, "significant_p05": p_a < 0.05,
    }

    # Test B : node-label shuffle
    print("\n── Test B : node-label shuffle ──")
    with mp.Pool(
        processes=n_workers,
        initializer=_init_workers,
        initargs=(edges, channels, signed, vopt, sigs),
    ) as pool:
        seeds_b = list(range(SEED + 10000, SEED + 10000 + n_perm))
        results_b = []
        t0 = time.time()
        for i, r2_perm in enumerate(pool.imap_unordered(_worker_nodelabel_perm, seeds_b, chunksize=chunk)):
            results_b.append(r2_perm)
            if (i + 1) % max(1, n_perm // 10) == 0:
                print(f"    B: {(i+1)/n_perm*100:.0f}%  elapsed={time.time()-t0:.1f}s")

    elapsed_b = time.time() - t0
    p_b = sum(1 for r in results_b if r >= r2_obs) / len(results_b)
    mean_b = sum(results_b) / len(results_b)
    std_b = math.sqrt(sum((r - mean_b) ** 2 for r in results_b) / len(results_b))
    z_b = (r2_obs - mean_b) / std_b if std_b > 0 else float("inf")
    print(f"    B terminé: R²_obs={r2_obs:.4f}  mean_perm={mean_b:.4f}±{std_b:.4f}"
          f"  p={p_b:.4f}  z={z_b:.2f}  ({elapsed_b:.1f}s)")
    result_b = {
        "r2_observed": round(r2_obs, 4), "n_perm": n_perm,
        "mean_r2_perm": round(mean_b, 4), "std_r2_perm": round(std_b, 4),
        "p_value": round(p_b, 4), "z_score": round(z_b, 3),
        "elapsed_s": round(elapsed_b, 1),
        "significant_p01": p_b < 0.01, "significant_p05": p_b < 0.05,
    }

    # Bilan
    elapsed = time.time() - t_start
    verdict_a = f"p={p_a:.4f} {'SIGNIFICATIF p<0.05' if p_a < 0.05 else 'NON SIGNIFICATIF'}"
    verdict_b = f"p={p_b:.4f} {'SIGNIFICATIF p<0.05' if p_b < 0.05 else 'NON SIGNIFICATIF'}"
    print(f"\n── Bilan ──")
    print(f"  Test A (channel shuffle)    : {verdict_a}  z={z_a:.2f}")
    print(f"  Test B (node-label shuffle) : {verdict_b}  z={z_b:.2f}")

    result = {
        "section": "§222",
        "description": "Falsification permutation tests sur graph v13 + corpus v212f",
        "graph_version": "v13",
        "corpus_version": corpus.get("version"),
        "vopt_version": vopt_version,
        "vopt_weights": vopt,
        "n_signed": len(signed),
        "n_pairs_observed": n_pairs_obs,
        "r2_observed": round(r2_obs, 4),
        "test_A_channel_shuffle": result_a,
        "test_B_nodelabel_shuffle": result_b,
        "elapsed_s": round(elapsed, 1),
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nÉcrit : {OUT_PATH}")
    print(f"Durée totale : {elapsed:.1f}s")


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)
    main()

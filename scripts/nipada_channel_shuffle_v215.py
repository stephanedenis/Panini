#!/usr/bin/env python3
"""
§215 — Channel-Shuffle Falsification Test
==========================================
Test de falsification : mélanger les labels `channel` des arêtes
(en préservant la structure du graphe) et observer si R² s'effondre.

Hypothèse :
  - Si R²_real > p95(R²_shuffled) → V_OPT capture la sémantique des canaux
  - Sinon → V_OPT exploite seulement la topologie

V_OPT v3 : (w_direct=0.45, w_translation=0.05, w_indirect=0.05)
Graphe    : nipada_v210a_graph_v12.json (1764 nodes / 26112 edges)
Signed    : signed_corpus_v208.json     (37 nœuds avec V14 signatures)

Usage : python3 scripts/nipada_channel_shuffle_v215.py
Sortie : research/nipada/falsification/nipada_v215_channel_shuffle.json
"""

import json
import heapq
import random
import math
import time
from pathlib import Path

# ─── Chemins ───────────────────────────────────────────────────────────────
# Les données de recherche sont dans le repo Panini-Research (submodule ou standalone)
_SCRIPT_DIR  = Path(__file__).resolve().parent
# Chercher les données : d'abord submodule research/, sinon Panini-Research adjacent
_CANDIDATES  = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH   = _NIPADA / "falsification/nipada_v210a_graph_v12.json"
SIGNED_PATH  = _NIPADA / "corpus/signed_corpus_v208.json"
OUT_PATH     = _NIPADA / "falsification/nipada_v215_channel_shuffle.json"

# ─── V_OPT v3 ──────────────────────────────────────────────────────────────
V_OPT_V3 = {"direct": 0.45, "translation": 0.05, "indirect": 0.05}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

N_SHUFFLE = 100
SEED      = 2026


# ─── Primitives ────────────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    """Classifie un label de canal en direct / translation / indirect."""
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def edge_cost(channel: str) -> float:
    """Coût d'arête Dijkstra selon le type de canal."""
    return V_OPT_V3[classify_channel(channel)]


def build_adjacency(edges: list, channels: list | None = None) -> dict:
    """
    Construit une adjacence non-dirigée.
    Si `channels` est fourni, remplace les labels de canaux originaux.
    """
    adj: dict = {}
    for i, e in enumerate(edges):
        src, tgt = e["src"], e["tgt"]
        ch = channels[i] if channels is not None else e["channel"]
        cost = edge_cost(ch)
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(source: str, adj: dict, targets: set) -> dict:
    """Dijkstra depuis `source` avec early-stop quand tous les targets sont trouvés."""
    dist      = {source: 0.0}
    pq        = [(0.0, source)]
    remaining = set(targets) - {source}
    found     = {}
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
    result = {t: found.get(t, dist.get(t, math.inf)) for t in targets}
    return result


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
    sx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return num / (sx * sy)


def compute_r2(adj: dict, signed: list) -> tuple:
    """Calcule R² = pearson_r(d_topo, d_lex)² sur toutes les paires signées."""
    n     = len(signed)
    ids   = [s["graph_node_id"] for s in signed]
    sigs  = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)

    d_topo_list = []
    d_lex_list  = []

    for i in range(n):
        distances = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, n):
            dt = distances[ids[j]]
            if math.isinf(dt):
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            d_topo_list.append(dt)
            d_lex_list.append(dl)

    if len(d_topo_list) < 2:
        return 0.0
    r = pearson_r(d_topo_list, d_lex_list)
    return r * r, len(d_topo_list)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("§215 — Channel-Shuffle Falsification Test")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  signed : {SIGNED_PATH}")
    print()

    graph  = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    corpus = json.loads(SIGNED_PATH.read_text(encoding="utf-8"))

    edges  = graph["edges"]
    signed = [s for s in corpus["signed"] if s["matched"]]
    all_channels = [e["channel"] for e in edges]

    print(f"  edges  : {len(edges)}")
    print(f"  signed : {len(signed)}")
    print(f"  pairs  : {len(signed) * (len(signed)-1) // 2}")
    print()

    # ── Distribution des channels réels ──────────────────────────────────
    from collections import Counter
    type_counts = Counter(classify_channel(ch) for ch in all_channels)
    print("  Channels classification :", dict(type_counts))
    print()

    # ── R² réel ──────────────────────────────────────────────────────────
    print("  Calcul R²_real ...", flush=True)
    adj_real  = build_adjacency(edges)
    r2_real, n_pairs_used = compute_r2(adj_real, signed)
    print(f"  R²_real = {r2_real:.6f}  (n_pairs = {n_pairs_used})")
    print()

    # ── Shuffle ──────────────────────────────────────────────────────────
    rng = random.Random(SEED)
    r2_shuffled = []
    for k in range(N_SHUFFLE):
        shuffled_channels = all_channels[:]
        rng.shuffle(shuffled_channels)
        adj_shuf = build_adjacency(edges, channels=shuffled_channels)
        r2_s, _ = compute_r2(adj_shuf, signed)
        r2_shuffled.append(r2_s)
        if (k + 1) % 10 == 0:
            print(f"  shuffle {k+1:3d}/{N_SHUFFLE} | running mean R²_shuf = "
                  f"{sum(r2_shuffled)/len(r2_shuffled):.6f}", flush=True)

    r2_shuffled_sorted = sorted(r2_shuffled)
    p95_idx = int(0.95 * N_SHUFFLE) - 1
    r2_p95  = r2_shuffled_sorted[p95_idx]
    r2_mean = sum(r2_shuffled) / len(r2_shuffled)
    r2_std  = math.sqrt(sum((x - r2_mean) ** 2 for x in r2_shuffled) / len(r2_shuffled))

    verdict = "PASS" if r2_real > r2_p95 else "REVUE"
    elapsed = time.time() - t0

    print()
    print(f"  R²_real              = {r2_real:.6f}")
    print(f"  R²_shuffled mean±σ   = {r2_mean:.6f} ± {r2_std:.6f}")
    print(f"  R²_shuffled p95      = {r2_p95:.6f}")
    print(f"  Verdict              : {verdict}")
    print(f"  Elapsed              : {elapsed:.1f}s")
    print()

    if verdict == "PASS":
        print("  ✓ V_OPT capture la sémantique des canaux (R²_real > p95)")
    else:
        print("  ✗ V_OPT exploite seulement la topologie (R²_real ≤ p95)")

    # ── Sauvegarde ───────────────────────────────────────────────────────
    result = {
        "version"          : "v215",
        "graph_in"         : str(GRAPH_PATH.name),
        "n_edges"          : len(edges),
        "n_signed"         : len(signed),
        "n_pairs_used"     : n_pairs_used,
        "v_opt_v3"         : V_OPT_V3,
        "n_shuffles"       : N_SHUFFLE,
        "seed"             : SEED,
        "channels_type_counts": dict(type_counts),
        "r2_real"          : r2_real,
        "r2_shuffled_mean" : r2_mean,
        "r2_shuffled_std"  : r2_std,
        "r2_shuffled_p95"  : r2_p95,
        "r2_shuffled_all"  : r2_shuffled,
        "verdict"          : verdict,
        "elapsed_s"        : round(elapsed, 1),
    }
    OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  → Résultat écrit : {OUT_PATH}")


if __name__ == "__main__":
    main()

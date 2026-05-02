#!/usr/bin/env python3
"""
§214 — LOO Tradition-Out Validation
====================================
Leave-One-Tradition-Out (LOO) validation de la corrélation V_OPT v4 ↔ V14.

Pour chaque tradition t ∈ {BUDDHIST_AXIAL, INDIAN_AXIAL, CHINESE_AXIAL} :
  1. Ensemble train : corpus v212f sans les textes de t
  2. Ensemble test  : textes de t uniquement
  3. R²_test(t) = R²(d_topo_vopt4, d_lex_v14) sur les paires intra-t
  4. Comparer à R²_all (toutes paires cross-tradition)

Supplémentaire :
  - R² intra-tradition (train ∪ test → sous-ensemble homogène)
  - R² cross-tradition (toutes paires inter-tradition)

V_OPT v4 : {direct: 0.1, translation: 0.1, indirect: 1.0}
Corpus v212f : 75 textes (BUDDHIST=30, INDIAN=32, CHINESE=12, DAOISM=1)
Graphe v12   : 1764 nœuds / 26112 arêtes

Usage : python3 scripts/nipada_loo_tradition_v214.py
"""

import json
import heapq
import math
import time
from pathlib import Path

# ─── Chemins ───────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH   = _NIPADA / "falsification/nipada_v210a_graph_v12.json"
CORPUS_PATH  = _NIPADA / "corpus/signed_corpus_v212f.json"
V213_PATH    = _NIPADA / "falsification/nipada_v213_vopt_calibration.json"
OUT_PATH     = _NIPADA / "falsification/nipada_v214_loo_tradition.json"

# ─── V_OPT v4 ──────────────────────────────────────────────────────────────
V_OPT_V4 = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# Traditions cibles pour le LOO (DAOISM exclu : 1 seul texte)
LOO_TRADITIONS = ["BUDDHIST_AXIAL", "INDIAN_AXIAL", "CHINESE_AXIAL"]


# ─── V_OPT helpers ─────────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(edges: list, weights: dict) -> dict:
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


# ─── Statistiques ──────────────────────────────────────────────────────────

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


def compute_r2_pairs(adj: dict, subset_a: list, subset_b: list) -> tuple[float, int]:
    """
    Calcule R²(d_topo, d_lex) pour les paires (a, b) avec a ∈ subset_a, b ∈ subset_b.
    Si subset_a == subset_b, calcule les paires intra (i < j).
    Si subset_a != subset_b, calcule toutes les paires croisées.
    """
    if subset_a is subset_b or subset_a == subset_b:
        # paires intra
        ids = [s["graph_node_id"] for s in subset_a]
        sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_a}
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
    else:
        # paires croisées
        ids_a = [s["graph_node_id"] for s in subset_a]
        ids_b = [s["graph_node_id"] for s in subset_b]
        sigs_a = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_a}
        sigs_b = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in subset_b}
        target_b = set(ids_b)
        d_topo_list = []
        d_lex_list = []
        for id_a in ids_a:
            distances = dijkstra_from(id_a, adj, target_b)
            for id_b in ids_b:
                dt = distances[id_b]
                if math.isinf(dt):
                    continue
                dl = l2_distance(sigs_a[id_a], sigs_b[id_b])
                d_topo_list.append(dt)
                d_lex_list.append(dl)

    if len(d_topo_list) < 2:
        return 0.0, len(d_topo_list)
    r = pearson_r(d_topo_list, d_lex_list)
    return r * r, len(d_topo_list)


def compute_r2_intra(adj: dict, subset: list) -> tuple[float, int]:
    return compute_r2_pairs(adj, subset, subset)


def compute_r2_cross(adj: dict, subset_a: list, subset_b: list) -> tuple[float, int]:
    return compute_r2_pairs(adj, subset_a, subset_b)


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()

    # Chargement
    print("§214 — LOO Tradition-Out Validation")
    print(f"  graphe : {GRAPH_PATH}")
    print(f"  corpus : {CORPUS_PATH}")

    with open(GRAPH_PATH) as f:
        graph = json.load(f)
    edges = graph["edges"]

    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
    signed = corpus["signed"]

    n_all = len(signed)
    print(f"\n  Graphe : {len(graph['nodes'])} nœuds, {len(edges)} arêtes")
    print(f"  Corpus : {n_all} textes signés")

    # Index par tradition
    by_trad: dict = {}
    for s in signed:
        trad = s.get("tradition_label", "UNKNOWN")
        by_trad.setdefault(trad, []).append(s)
    for trad, texts in sorted(by_trad.items()):
        print(f"    {trad}: {len(texts)} textes")

    # Adjacence V_OPT v4
    adj = build_adjacency(edges, V_OPT_V4)

    # ── R²_all (toutes paires) ──
    print("\n── R² global (toutes paires) ──")
    r2_all, n_all_pairs = compute_r2_intra(adj, signed)
    print(f"  R²_all = {r2_all:.4f}  ({n_all_pairs} paires)")

    # ── R² intra-tradition ──
    print("\n── R² intra-tradition ──")
    intra_results = {}
    for trad in LOO_TRADITIONS:
        subset = by_trad.get(trad, [])
        r2, n_pairs = compute_r2_intra(adj, subset)
        intra_results[trad] = {"r2": r2, "n_pairs": n_pairs, "n_texts": len(subset)}
        print(f"  {trad} (N={len(subset)}): R²={r2:.4f}  ({n_pairs} paires)")

    # ── LOO : cross-tradition (tradition hors v.s. reste) ──
    print("\n── LOO : R² cross (held-out vs. train) ──")
    loo_cross_results = {}
    for held_out_trad in LOO_TRADITIONS:
        held_out = by_trad.get(held_out_trad, [])
        train = [s for s in signed if s.get("tradition_label") != held_out_trad]
        r2_cross, n_cross = compute_r2_cross(adj, held_out, train)
        loo_cross_results[held_out_trad] = {
            "r2_cross": r2_cross,
            "n_pairs_cross": n_cross,
            "n_held_out": len(held_out),
            "n_train": len(train),
        }
        print(f"  LOO held-out={held_out_trad} (N_test={len(held_out)}, N_train={len(train)}): "
              f"R²_cross={r2_cross:.4f}  ({n_cross} paires)")

    # ── LOO : intra held-out (généralisation) ──
    print("\n── LOO : R² intra held-out (pairs within held-out tradition) ──")
    loo_intra_results = {}
    for held_out_trad in LOO_TRADITIONS:
        held_out = by_trad.get(held_out_trad, [])
        r2_intra, n_intra = compute_r2_intra(adj, held_out)
        loo_intra_results[held_out_trad] = {
            "r2_intra_test": r2_intra,
            "n_pairs_intra": n_intra,
            "n_texts": len(held_out),
        }
        print(f"  LOO held-out={held_out_trad}: R²_intra_test={r2_intra:.4f}  ({n_intra} paires)")

    # ── Synthèse ──
    print("\n── Synthèse ──")
    print(f"  R²_all (cross-tradition)      : {r2_all:.4f}")
    for trad in LOO_TRADITIONS:
        ri = intra_results[trad]["r2"]
        rc = loo_cross_results[trad]["r2_cross"]
        print(f"  {trad:20s}  intra={ri:.4f}  cross_with_others={rc:.4f}")

    # Verdict : le signal est-il dominé par les paires intra-tradition ?
    mean_intra = sum(intra_results[t]["r2"] for t in LOO_TRADITIONS) / len(LOO_TRADITIONS)
    verdict = "INTRA_DOMINATED" if mean_intra > r2_all * 1.5 else "BALANCED"
    print(f"\n  Mean R²_intra = {mean_intra:.4f}  (vs R²_all={r2_all:.4f})")
    print(f"  Verdict : {verdict}")

    # ── Écriture JSON ──
    result = {
        "version": "v214",
        "date": "2026-05-01",
        "vopt_v4_weights": V_OPT_V4,
        "corpus_version": corpus.get("version"),
        "n_signed": n_all,
        "n_pairs_all": n_all_pairs,
        "r2_all": r2_all,
        "intra_tradition": {
            t: {
                "r2": intra_results[t]["r2"],
                "n_pairs": intra_results[t]["n_pairs"],
                "n_texts": intra_results[t]["n_texts"],
            }
            for t in LOO_TRADITIONS
        },
        "loo_cross": {
            t: loo_cross_results[t]
            for t in LOO_TRADITIONS
        },
        "loo_intra_test": {
            t: loo_intra_results[t]
            for t in LOO_TRADITIONS
        },
        "mean_r2_intra": mean_intra,
        "verdict": verdict,
        "duration_s": round(time.time() - t_start, 1),
    }

    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nÉcrit : {OUT_PATH}")
    print(f"Durée : {result['duration_s']}s")


if __name__ == "__main__":
    main()

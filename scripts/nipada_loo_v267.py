#!/usr/bin/env python3
"""
§267 — LOO (Leave-One-Out) analysis sur graphe v18p, corpus 116 textes.

Pour chaque texte du corpus mergé (v263_clean + v264_prophetic),
retire le texte et recalcule R². ΔR² = R²_without - R²_baseline.

  ΔR² > 0  → le texte *dégrade* le modèle (outlier)
  ΔR² < 0  → le texte *améliore* le modèle (contributeur)

Charge :
  - signed_corpus_v263_clean.json    (100 textes)
  - signed_corpus_v264_prophetic.json (16 textes)
  - nipada_v266_graph_v18p.json      (graphe v18p, §266 officiel)

Sortie :
  nipada/falsification/nipada_v267_loo_v18p.json

Usage :
  python3 nipada_loo_v267.py
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Localisation du répertoire nipada ────────────────────────────────────────
_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

FALSI_DIR  = _NIPADA / "falsification"
CORPUS_DIR = _NIPADA / "corpus"

GRAPH_PATH = FALSI_DIR / "nipada_v266_graph_v18p.json"
C263_PATH  = CORPUS_DIR / "signed_corpus_v263_clean.json"
C264_PATH  = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
OUT_PATH   = FALSI_DIR / "nipada_v267_loo_v18p.json"

VOPT_DEFAULT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]


# ── Fonctions core ────────────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(
    edges: list[dict], weights: dict[str, float]
) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = weights[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(
    source: str,
    adj: dict[str, list[tuple[str, float]]],
    targets: set[str],
) -> dict[str, float]:
    import heapq
    dist = {source: 0.0}
    pq   = [(0.0, source)]
    remaining = set(targets) - {source}
    found: dict[str, float] = {}
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


def v14_vector(sig: dict[str, float]) -> list[float]:
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1: list[float], v2: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r2(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return (num / (sx * sy)) ** 2


def merge_corpora(c1: list[dict], c2: list[dict]) -> list[dict]:
    out: dict[str, dict] = {}
    for s in c1:
        out[s["graph_node_id"]] = s
    for s in c2:
        out[s["graph_node_id"]] = s
    return list(out.values())


def eval_corpus_fast(
    adj: dict[str, list[tuple[str, float]]],
    signed: list[dict],
) -> tuple[float, int, int]:
    """Retourne (r2, n_finite, n_inf)."""
    ids    = [s["graph_node_id"] for s in signed]
    sigs   = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    d_topo: list[float] = []
    d_lex:  list[float] = []
    inf_count = 0

    for i in range(len(ids)):
        dists = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = dists[ids[j]]
            if math.isinf(dt):
                inf_count += 1
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            d_topo.append(dt)
            d_lex.append(dl)

    return pearson_r2(d_topo, d_lex), len(d_topo), inf_count


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    t0 = time.time()

    print("=" * 70)
    print("§267 — LOO (Leave-One-Out) analysis — graphe v18p, 116 textes")
    print("=" * 70)

    # ── Chargement ───────────────────────────────────────────────────────────
    for p in [GRAPH_PATH, C263_PATH, C264_PATH]:
        if not p.exists():
            sys.exit(f"ERROR: fichier manquant: {p}")

    graph  = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    n_nodes = len(graph["nodes"])
    n_edges = len(graph["edges"])
    print(f"\nGraphe v18p : {n_nodes} nœuds, {n_edges} arêtes")

    vopt = VOPT_DEFAULT
    edges = graph["edges"]

    s263 = json.loads(C263_PATH.read_text(encoding="utf-8")).get("signed", [])
    s264 = json.loads(C264_PATH.read_text(encoding="utf-8")).get("signed", [])
    sall = merge_corpora(s263, s264)
    print(f"Corpus : {len(s263)} + {len(s264)} = {len(sall)} textes")

    # ── Baseline ─────────────────────────────────────────────────────────────
    print("\nBaseline (116 textes)...")
    adj_full = build_adjacency(edges, vopt)
    r2_base, n_base, ninf_base = eval_corpus_fast(adj_full, sall)
    print(f"  R² = {r2_base:.4f}  ({n_base} paires finies, {ninf_base} inf)")

    # ── LOO loop ──────────────────────────────────────────────────────────────
    print(f"\nLOO sur {len(sall)} textes (graphe inchangé, corpus réduit)...")
    print(f"  Note : les arêtes sont conservées — seules les paires sont retirées.")
    print()

    # En-tête tableau
    print(f"  {'texte':<45} {'R²':>6}  {'n':>4}  {'ΔR²':>8}  {'signe'}")
    print("  " + "-" * 75)

    results: list[dict] = []
    for idx, text in enumerate(sall):
        gid = text["graph_node_id"]
        lid = text.get("local_id", gid)
        corpus_without = [s for s in sall if s["graph_node_id"] != gid]
        r2_wo, n_wo, _ = eval_corpus_fast(adj_full, corpus_without)
        delta = round(r2_wo - r2_base, 4)
        flag  = "OUTLIER" if delta > 0.001 else ("contrib" if delta < -0.001 else "neutre")
        stars = "★★" if abs(delta) >= 0.01 else ("★" if abs(delta) >= 0.003 else "·")
        corpus_type = "prophétique" if text in s264 else "base"
        print(f"  {lid:<45} {r2_wo:.4f}  {n_wo:>4}  {delta:>+.4f}  {stars} {flag} [{corpus_type}]")
        results.append({
            "rank": 0,
            "local_id": lid,
            "graph_node_id": gid,
            "corpus_type": corpus_type,
            "r2_without": round(r2_wo, 4),
            "n_pairs_without": n_wo,
            "delta_r2": delta,
            "flag": flag,
        })

    # ── Classement ────────────────────────────────────────────────────────────
    outliers     = sorted([r for r in results if r["flag"] == "OUTLIER"],
                          key=lambda x: -x["delta_r2"])
    contributors = sorted([r for r in results if r["flag"] == "contrib"],
                          key=lambda x: x["delta_r2"])
    neutral      = [r for r in results if r["flag"] == "neutre"]

    # Assign ranks
    for i, r in enumerate(sorted(results, key=lambda x: -x["delta_r2"]), 1):
        r["rank"] = i

    print(f"\n{'='*70}")
    print(f"OUTLIERS (ΔR² > +0.001)  : {len(outliers)}")
    for r in outliers[:10]:
        print(f"  {r['local_id']:<45}  ΔR²={r['delta_r2']:>+.4f}  [{r['corpus_type']}]")

    print(f"\nCONTRIBUTEURS (ΔR² < -0.001) : {len(contributors)}")
    for r in contributors[:10]:
        print(f"  {r['local_id']:<45}  ΔR²={r['delta_r2']:>+.4f}  [{r['corpus_type']}]")

    print(f"\nNEUTRES (|ΔR²| ≤ 0.001) : {len(neutral)}")

    # ── Analyse textes prophétiques ───────────────────────────────────────────
    proph_results = [r for r in results if r["corpus_type"] == "prophétique"]
    proph_outliers = [r for r in proph_results if r["flag"] == "OUTLIER"]
    proph_contrib  = [r for r in proph_results if r["flag"] == "contrib"]
    proph_neutral  = [r for r in proph_results if r["flag"] == "neutre"]

    print(f"\n{'='*70}")
    print(f"ANALYSE TEXTES PROPHÉTIQUES (16) :")
    print(f"  Outliers     : {len(proph_outliers)}")
    print(f"  Contributeurs: {len(proph_contrib)}")
    print(f"  Neutres      : {len(proph_neutral)}")
    for r in sorted(proph_results, key=lambda x: x["delta_r2"]):
        print(f"  {r['local_id']:<45}  ΔR²={r['delta_r2']:>+.4f}  {r['flag']}")

    elapsed = time.time() - t0
    print(f"\nTerminé en {elapsed:.1f}s")

    # ── Sauvegarde ────────────────────────────────────────────────────────────
    out = {
        "section": "§267",
        "analysis": "LOO Leave-One-Out",
        "graph": "v18p",
        "graph_path": str(GRAPH_PATH.name),
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        "corpus_n263": len(s263),
        "corpus_n264": len(s264),
        "corpus_total": len(sall),
        "r2_baseline": round(r2_base, 4),
        "n_pairs_baseline": n_base,
        "n_pairs_infinite_baseline": ninf_base,
        "n_outliers": len(outliers),
        "n_contributors": len(contributors),
        "n_neutral": len(neutral),
        "prophetic_outliers": len(proph_outliers),
        "prophetic_contributors": len(proph_contrib),
        "prophetic_neutral": len(proph_neutral),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "elapsed_s": round(elapsed, 1),
        "results": sorted(results, key=lambda x: -x["delta_r2"]),
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSauvegardé : {OUT_PATH}")


if __name__ == "__main__":
    main()

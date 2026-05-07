#!/usr/bin/env python3
"""
§268c — Revalidation NiPaDa avec mengzi (Legge tr., IA).

Contexte:
  §268a = DIAGNOSTIC NÉGATIF: extraction v208 invalide (calibration mismatch).
  §268b = NÉGATIF: textes islamiques (v226) violent H₀ (pente d_lex/d_topo trop faible).
  §268c = Test mengzi: Confucianisme chinois, d_topo=0.2 vers liezi (connexion directe).

Usage:
    python3 nipada_revalidation_v268c.py

Produit:
    Panini-Research/nipada/falsification/nipada_v268c_revalidation_v18p.json
"""

from __future__ import annotations

import json
import math
import heapq
import sys
from pathlib import Path
from typing import Any

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

GRAPH_FILE      = FALSI_DIR / "nipada_v266_graph_v18p.json"
CORPUS_V263     = CORPUS_DIR / "signed_corpus_v263_clean.json"
CORPUS_V264     = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
CORPUS_V268C    = CORPUS_DIR / "signed_corpus_v268c_mengzi.json"

OUT_REPORT      = FALSI_DIR / "nipada_v268c_revalidation_v18p.json"

R2_BASELINE     = 0.6248
N_PAIRS_BASELINE = 1025

VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}
V14_ATOMS = [
    "ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS",
    "MODALITÉ","NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE",
    "SYMÉTRIE","ÉQUATION"
]


def classify_channel(ch: str) -> str:
    low = ch.lower()
    if "traduction" in low or low == "idem traduction":
        return "translation"
    if "direct" in low:
        return "direct"
    return "indirect"


def load_corpus(*paths: Path) -> list[dict[str, Any]]:
    all_texts: list[dict[str, Any]] = []
    for p in paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        all_texts.extend(d.get("signed", d.get("texts", [])))
    return all_texts


def dijkstra(src: str, adj: dict[str, list]) -> dict[str, float]:
    dist: dict[str, float] = {src: 0.0}
    heap: list = [(0.0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, math.inf):
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def l2(sa: dict, sb: dict) -> float:
    return math.sqrt(sum((sa.get(a, 0.0) - sb.get(a, 0.0))**2 for a in V14_ATOMS))


def pearson_r2(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx)**2 for x in xs))
    dy = math.sqrt(sum((y - my)**2 for y in ys))
    if dx == 0 or dy == 0:
        return float("nan")
    return (num / (dx * dy))**2


def compute_pairs(texts: list[dict], adj: dict) -> tuple[list[float], list[float]]:
    ids = [t["graph_node_id"] for t in texts]
    sigs = {t["graph_node_id"]: t["v14_signature"] for t in texts}
    dtopo_list: list[float] = []
    dlex_list: list[float] = []
    for i, src in enumerate(ids):
        dist = dijkstra(src, adj)
        for tgt in ids[i+1:]:
            d = dist.get(tgt, math.inf)
            if math.isfinite(d):
                dtopo_list.append(d)
                dlex_list.append(l2(sigs[src], sigs[tgt]))
    return dtopo_list, dlex_list


def main() -> int:
    print("§268c — Revalidation NiPaDa (mengzi)")
    print("=" * 55)

    print("\n[1] Chargement corpus…")
    texts_base = load_corpus(CORPUS_V263, CORPUS_V264)
    texts_new  = load_corpus(CORPUS_V268C)
    base_ids = set(t["graph_node_id"] for t in texts_base)
    new_texts = [t for t in texts_new if t["graph_node_id"] not in base_ids]
    new_ids = [t["graph_node_id"] for t in new_texts]
    all_texts = texts_base + new_texts

    print(f"  Base (v263+v264): {len(texts_base)} textes")
    print(f"  Nouveaux: {len(new_texts)} textes ({new_ids})")
    for t in new_texts:
        sig = t["v14_signature"]
        print(f"    {t['graph_node_id']:<45} EQ={sig.get('ÉQUATION',0):.3f} ÊTRE={sig.get('ÊTRE',0):.3f}")

    d = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
    edges = d["edges"]
    print(f"\n[2] Graphe v18p: {len(d['nodes'])} nœuds, {len(edges)} arêtes")

    adj: dict[str, list] = {}
    for e in edges:
        s, t = e["src"], e["tgt"]
        ch = e.get("channel", "")
        w = VOPT[classify_channel(ch)]
        adj.setdefault(s, []).append((t, w))
        adj.setdefault(t, []).append((s, w))

    print("\n[3] Calcul des paires…")
    xs, ys = compute_pairs(all_texts, adj)
    n_pairs = len(xs)
    n_inf = len(all_texts) * (len(all_texts) - 1) // 2 - n_pairs
    r2 = pearson_r2(xs, ys)
    print(f"  N_textes = {len(all_texts)}")
    print(f"  N_pairs_finis = {n_pairs} (+{n_pairs - N_PAIRS_BASELINE} vs baseline)")
    print(f"  R² §268c = {r2:.6f} (baseline §267 = {R2_BASELINE:.6f})")
    delta_r2 = r2 - R2_BASELINE
    print(f"  ΔR²      = {delta_r2:+.6f}")

    print("\n[4] LOO analyse (nouveaux textes)…")
    loo_results = []
    for nid in new_ids:
        subset = [t for t in all_texts if t["graph_node_id"] != nid]
        xs2, ys2 = compute_pairs(subset, adj)
        r2_without = pearson_r2(xs2, ys2) if xs2 else float("nan")
        delta = r2 - r2_without
        role = "neutral" if abs(delta) < 0.001 else ("contributor" if delta > 0 else "outlier")
        loo_results.append({"id": nid, "r2_without": round(r2_without, 6),
                            "delta_r2": round(delta, 6), "role": role})
        print(f"  {nid:<45} ΔR²={delta:+.6f} [{role}] (R²_sans={r2_without:.6f})")

    # Paires détaillées pour mengzi
    print("\n[5] Paires mengzi détaillées (top 10 proches):")
    if new_texts:
        mengzi_sig = new_texts[0]["v14_signature"]
        dist = dijkstra("mengzi", adj)
        pairs = [(n, d, l2(mengzi_sig, t_sig))
                 for t in texts_base
                 for n, t_sig in [(t["graph_node_id"], t["v14_signature"])]
                 if math.isfinite(d := dist.get(n, math.inf))]
        for n, d_topo, d_lex in sorted(pairs, key=lambda x: x[1])[:10]:
            print(f"  {n:<45} d_topo={d_topo:.3f} d_lex={d_lex:.4f}")

    report = {
        "section": "§268c",
        "description": "Revalidation NiPaDa — mengzi (Legge, IA)",
        "graph_version": "v18p",
        "vopt": VOPT,
        "n_texts_total": len(all_texts),
        "n_texts_new": len(new_texts),
        "new_text_ids": new_ids,
        "r2_268c": round(r2, 6),
        "r2_baseline_267": R2_BASELINE,
        "delta_r2": round(delta_r2, 6),
        "n_pairs_268c": n_pairs,
        "n_pairs_baseline": N_PAIRS_BASELINE,
        "delta_n_pairs": n_pairs - N_PAIRS_BASELINE,
        "n_inf_pairs": n_inf,
        "n_new_contributors": sum(1 for r in loo_results if r["role"] == "contributor"),
        "n_new_neutrals": sum(1 for r in loo_results if r["role"] == "neutral"),
        "n_new_outliers": sum(1 for r in loo_results if r["role"] == "outlier"),
        "loo_results": loo_results,
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[6] Rapport: {OUT_REPORT}")
    print("\n=== §268c TERMINÉ ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

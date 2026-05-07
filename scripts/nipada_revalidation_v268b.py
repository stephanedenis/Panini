#!/usr/bin/env python3
"""
§268b — Revalidation NiPaDa avec extension islamique (v226) correctement calibrée.

Contexte:
  §268a (Phase A) = DIAGNOSTIC NÉGATIF: extraction v208 invalide (mismatch calibration).
  §268b (Phase B) = Extension genuine via fetch+signature du pipeline v263:
    - 4 textes islamiques (v226): ibn_rushd_tahafut_tahafut, ibn_rushd_fasl_maqal,
      ghazali_ihya, rumi_mathnawi
    - Signatures obtenues par fetch URL → HTML extraction → freq_signature (V14)
    - Même pipeline que v263: calibration homogène

Usage:
    python3 nipada_revalidation_v268b.py

Produit:
    Panini-Research/nipada/falsification/nipada_v268b_revalidation_v18p.json
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

GRAPH_FILE     = FALSI_DIR / "nipada_v266_graph_v18p.json"
CORPUS_V263    = CORPUS_DIR / "signed_corpus_v263_clean.json"
CORPUS_V264    = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
CORPUS_V226    = CORPUS_DIR / "signed_corpus_v226_islamic.json"

OUT_REPORT     = FALSI_DIR / "nipada_v268b_revalidation_v18p.json"

# Baseline §267
R2_BASELINE = 0.6248
N_PAIRS_BASELINE = 1025
N_TEXTS_BASELINE = 116

# VOPT v5
VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

V14_ATOMS = [
    "ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS",
    "MODALITÉ","NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE",
    "SYMÉTRIE","ÉQUATION"
]


def load_corpus(*paths: Path) -> list[dict[str, Any]]:
    """Charger et fusionner des corpus signés."""
    all_texts: list[dict[str, Any]] = []
    for p in paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        texts = d.get("signed", d.get("texts", []))
        all_texts.extend(texts)
    return all_texts


def load_graph(path: Path) -> tuple[dict, list]:
    d = json.loads(path.read_text(encoding="utf-8"))
    return d["nodes"], d["edges"]


def build_adj(edges: list[dict]) -> dict[str, dict[str, float]]:
    adj: dict[str, dict[str, float]] = {}
    for e in edges:
        s, t = e["src"], e["tgt"]
        w = float(e.get("weight", 1.0))
        if w < adj.get(s, {}).get(t, float("inf")):
            adj.setdefault(s, {})[t] = w
        if w < adj.get(t, {}).get(s, float("inf")):
            adj.setdefault(t, {})[s] = w
    return adj


def dijkstra(src: str, adj: dict[str, list[tuple[str, float]]]) -> dict[str, float]:
    dist: dict[str, float] = {src: 0.0}
    heap: list[tuple[float, str]] = [(0.0, src)]
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


def l2_distance(sig_a: dict, sig_b: dict) -> float:
    return math.sqrt(sum((sig_a.get(a, 0.0) - sig_b.get(a, 0.0))**2 for a in V14_ATOMS))


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


def classify_channel(ch: str) -> str:
    low = ch.lower()
    if "traduction" in low or low == "idem traduction":
        return "translation"
    if "direct" in low:
        return "direct"
    return "indirect"


def compute_pairs(
    texts: list[dict], adj: dict[str, list[tuple[str, float]]]
) -> tuple[list[float], list[float]]:
    """Calculer toutes les paires (d_topo, d_lex) finies."""
    ids = [t["graph_node_id"] for t in texts]
    sigs = {t["graph_node_id"]: t["v14_signature"] for t in texts}
    id_set = set(ids)

    dtopo_list: list[float] = []
    dlex_list: list[float] = []

    for i, src in enumerate(ids):
        dist = dijkstra(src, adj)
        for tgt in ids[i+1:]:
            d_topo = dist.get(tgt, math.inf)
            if math.isfinite(d_topo):
                d_lex = l2_distance(sigs[src], sigs[tgt])
                dtopo_list.append(d_topo)
                dlex_list.append(d_lex)

    return dtopo_list, dlex_list


def loo_analysis(
    all_texts: list[dict],
    base_ids: set[str],
    new_ids: list[str],
    adj: dict[str, list[tuple[str, float]]],
    r2_with_all: float,
) -> list[dict]:
    """LOO pour chaque nouveau texte : ΔR² = R²_without - R²_with_all."""
    results = []
    for nid in new_ids:
        subset = [t for t in all_texts if t["graph_node_id"] != nid]
        xs, ys = compute_pairs(subset, adj)
        r2_without = pearson_r2(xs, ys) if xs else float("nan")
        delta = r2_with_all - r2_without
        role = "neutral"
        if abs(delta) < 0.001:
            role = "neutral"
        elif delta > 0:
            role = "contributor"
        else:
            role = "outlier"
        results.append({
            "id": nid,
            "r2_without": round(r2_without, 6),
            "delta_r2": round(delta, 6),
            "role": role,
        })
    return results


def main() -> int:
    print("§268b — Revalidation NiPaDa (extension islamique v226)")
    print("=" * 60)

    # ── Chargement ──────────────────────────────────────────────
    print("\n[1] Chargement des corpus…")
    texts_base = load_corpus(CORPUS_V263, CORPUS_V264)
    texts_226  = load_corpus(CORPUS_V226)
    print(f"  Base (v263+v264): {len(texts_base)} textes")
    print(f"  Nouveaux (v226 islamique): {len(texts_226)} textes")

    # Dédupliquer
    base_ids = set(t["graph_node_id"] for t in texts_base)
    new_texts = [t for t in texts_226 if t["graph_node_id"] not in base_ids]
    new_ids = [t["graph_node_id"] for t in new_texts]
    print(f"  Nouveaux non-dupliqués: {len(new_texts)}")
    for t in new_texts:
        sig = t["v14_signature"]
        print(f"    {t['graph_node_id']:<45} EQ={sig.get('ÉQUATION',0):.3f} ÊTRE={sig.get('ÊTRE',0):.3f}")

    all_texts = texts_base + new_texts

    nodes, edges = load_graph(GRAPH_FILE)
    print(f"\n[2] Graphe v18p: {len(nodes)} nœuds, {len(edges)} arêtes")

    # Construire adjacence avec VOPT v5 (channel → poids)
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        s, t = e["src"], e["tgt"]
        ch = e.get("channel", "")
        etype = classify_channel(ch)
        w = VOPT[etype]
        adj.setdefault(s, []).append((t, w))
        adj.setdefault(t, []).append((s, w))

    # ── Régression globale §268b ─────────────────────────────────
    print("\n[3] Calcul des paires (d_topo, d_lex)…")
    xs, ys = compute_pairs(all_texts, adj)
    n_pairs = len(xs)
    n_inf = len(all_texts) * (len(all_texts) - 1) // 2 - n_pairs
    r2 = pearson_r2(xs, ys)
    print(f"  N_textes = {len(all_texts)}")
    print(f"  N_pairs_finis = {n_pairs} (+{n_pairs - N_PAIRS_BASELINE} vs baseline)")
    print(f"  N_pairs_inf   = {n_inf}")
    print(f"  R² §268b = {r2:.6f} (baseline §267 = {R2_BASELINE:.6f})")
    delta_r2 = r2 - R2_BASELINE
    print(f"  ΔR²      = {delta_r2:+.6f}")

    # ── LOO pour nouveaux textes ─────────────────────────────────
    print("\n[4] LOO analyse (nouveaux textes)…")
    loo_results = loo_analysis(all_texts, base_ids, new_ids, adj, r2)
    n_contrib = sum(1 for r in loo_results if r["role"] == "contributor")
    n_neutral = sum(1 for r in loo_results if r["role"] == "neutral")
    n_outlier = sum(1 for r in loo_results if r["role"] == "outlier")
    print(f"  Contributeurs: {n_contrib}, Neutres: {n_neutral}, Outliers: {n_outlier}")
    for r in sorted(loo_results, key=lambda x: x["delta_r2"]):
        print(f"    {r['id']:<45} ΔR²={r['delta_r2']:+.6f} [{r['role']}]")

    # ── Rapport ──────────────────────────────────────────────────
    report = {
        "section": "§268b",
        "description": "Revalidation NiPaDa — extension islamique via pipeline v263",
        "graph_version": "v18p",
        "vopt": VOPT,
        "n_texts_total": len(all_texts),
        "n_texts_new": len(new_texts),
        "new_text_ids": new_ids,
        "r2_268b": round(r2, 6),
        "r2_baseline_267": R2_BASELINE,
        "delta_r2": round(delta_r2, 6),
        "n_pairs_268b": n_pairs,
        "n_pairs_baseline": N_PAIRS_BASELINE,
        "delta_n_pairs": n_pairs - N_PAIRS_BASELINE,
        "n_inf_pairs": n_inf,
        "n_new_contributors": n_contrib,
        "n_new_neutrals": n_neutral,
        "n_new_outliers": n_outlier,
        "loo_results": loo_results,
        "notes": (
            "Phase B de §268. Calibration homogène: textes islamiques fetchés via URL "
            "(pipeline identique à v263). Contraste avec §268a où les signatures v208 "
            "(excerpts locaux) créaient un écart de calibration (ÉQUATION +0.040)."
        ),
    }

    OUT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[5] Rapport: {OUT_REPORT}")
    print("\n=== §268b TERMINÉ ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

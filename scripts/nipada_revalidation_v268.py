#!/usr/bin/env python3
"""
§268 — Revalidation H₀ avec corpus étendu (132 textes).

Corpus : v263_clean (100) + v264_prophetic (16) + v268_extension (16) = 132 textes.
Graphe : v18p (§266 officiel, inchangé).

Mesures :
  - R² baseline §267 : 0.6248 (116 textes, 1025 paires finies)
  - R² §268          : corpus 132 textes, N paires finies
  - Analyse de chaque nouveau texte (ΔR², flag contributeur/neutre/outlier)

Sortie :
  nipada/falsification/nipada_v268_revalidation_v18p.json
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Localisation ──────────────────────────────────────────────────────────────
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
C268_PATH  = CORPUS_DIR / "signed_corpus_v268_extension.json"
OUT_PATH   = FALSI_DIR  / "nipada_v268_revalidation_v18p.json"

VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}
R2_BASELINE_267 = 0.6248   # référence §267 (116 textes)
N_PAIRS_267     = 1025     # référence §267

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]


# ── Fonctions utilitaires ─────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    low = ch.lower()
    if "traduction" in low or low == "idem traduction":
        return "translation"
    if "direct" in low:
        return "direct"
    return "indirect"


def build_adjacency(edges: list[dict], w: dict[str, float]) -> dict:
    adj: dict = {}
    for e in edges:
        s, t = e["src"], e["tgt"]
        cost = w[classify_channel(e["channel"])]
        adj.setdefault(s, []).append((t, cost))
        adj.setdefault(t, []).append((s, cost))
    return adj


def dijkstra_from(src: str, adj: dict, targets: set[str]) -> dict[str, float]:
    import heapq
    dist = {src: 0.0}
    pq   = [(0.0, src)]
    remaining = set(targets) - {src}
    found: dict[str, float] = {}
    while pq and remaining:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        if u in remaining:
            remaining.discard(u)
            found[u] = d
        for v, cost in adj.get(u, []):
            nd = d + cost
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return {t: found.get(t, dist.get(t, math.inf)) for t in targets}


def v14_vec(sig: dict) -> list[float]:
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2(v1: list[float], v2: list[float]) -> float:
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


def merge_corpora(*corpora: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for corpus in corpora:
        for s in corpus:
            seen[s["graph_node_id"]] = s
    return list(seen.values())


def eval_corpus(adj: dict, signed: list[dict]) -> tuple[float, int, int]:
    ids    = [s["graph_node_id"] for s in signed]
    sigs   = {s["graph_node_id"]: v14_vec(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    d_topo, d_lex = [], []
    n_inf = 0
    for i, src in enumerate(ids):
        dists = dijkstra_from(src, adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = dists[ids[j]]
            if math.isinf(dt):
                n_inf += 1
                continue
            d_topo.append(dt)
            d_lex.append(l2(sigs[src], sigs[ids[j]]))
    return pearson_r2(d_topo, d_lex), len(d_topo), n_inf


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    t0 = time.time()
    print("=" * 70)
    print("§268 — Revalidation H₀  |  corpus 132 textes  |  graphe v18p")
    print("=" * 70)

    for p in [GRAPH_PATH, C263_PATH, C264_PATH, C268_PATH]:
        if not p.exists():
            sys.exit(f"ERROR: fichier manquant: {p}")

    graph  = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    print(f"\nGraphe v18p : {len(graph['nodes'])} nœuds, {len(graph['edges'])} arêtes")

    adj = build_adjacency(graph["edges"], VOPT)

    s263 = json.loads(C263_PATH.read_text(encoding="utf-8"))["signed"]
    s264 = json.loads(C264_PATH.read_text(encoding="utf-8"))["signed"]
    s268 = json.loads(C268_PATH.read_text(encoding="utf-8"))["signed"]

    sall = merge_corpora(s263, s264, s268)
    n_new = len(s268)
    print(f"Corpus      : {len(s263)} (v263) + {len(s264)} (v264) + {n_new} (v268) = {len(sall)} textes")

    # ── R² baseline §267 (reproduit sur 116 textes) ──────────────────────────
    print("\n1) Reproduction baseline §267 (116 textes)…", end="", flush=True)
    t_b = time.time()
    sbase = merge_corpora(s263, s264)
    r2_b, n_b, ninf_b = eval_corpus(adj, sbase)
    print(f"  R²={r2_b:.4f}  n={n_b}  inf={ninf_b}  ({time.time()-t_b:.1f}s)")
    assert abs(r2_b - R2_BASELINE_267) < 0.002, \
        f"⚠ Baseline diverge : attendu {R2_BASELINE_267}, obtenu {r2_b:.4f}"

    # ── R² §268 (132 textes) ─────────────────────────────────────────────────
    print("\n2) R² §268 (132 textes)…", end="", flush=True)
    t_268 = time.time()
    r2_268, n_268, ninf_268 = eval_corpus(adj, sall)
    dt_268 = time.time() - t_268
    delta_r2 = r2_268 - r2_b
    delta_n  = n_268 - n_b
    print(f"  R²={r2_268:.4f}  n={n_268}  inf={ninf_268}  ({dt_268:.1f}s)")
    print(f"  ΔR² vs §267 : {delta_r2:+.4f}  |  Δn paires : {delta_n:+d}")

    # ── Analyse par nouveau texte (LOO partiel) ───────────────────────────────
    print("\n3) LOO partiel — impact de chaque nouveau texte sur R²…")
    new_results = []
    DELTA_CONTRIB  = -0.001
    DELTA_OUTLIER  =  0.001

    for s in s268:
        # corpus sans ce texte (tous sauf lui)
        partial = [x for x in sall if x["graph_node_id"] != s["graph_node_id"]]
        r2_without, n_without, _ = eval_corpus(adj, partial)
        dr = r2_without - r2_268
        flag = ("contributeur" if dr < DELTA_CONTRIB
                else "outlier" if dr > DELTA_OUTLIER
                else "neutre")
        trad = s.get("catalog", s.get("tradition_label", "?"))
        new_results.append({
            "local_id":       s["graph_node_id"],
            "tradition":      trad,
            "n_pairs_without": n_without,
            "r2_without":     round(r2_without, 6),
            "delta_r2":       round(dr, 6),
            "flag":           flag,
        })
        sym = "★" if flag == "contributeur" else ("✗" if flag == "outlier" else "·")
        print(f"  {sym} {s['graph_node_id']:<42}  ΔR²={dr:+.4f}  [{flag}]  ({trad})")

    n_contrib  = sum(1 for r in new_results if r["flag"] == "contributeur")
    n_outlier  = sum(1 for r in new_results if r["flag"] == "outlier")
    n_neutre   = sum(1 for r in new_results if r["flag"] == "neutre")
    print(f"\n  {n_contrib} contributeurs | {n_neutre} neutres | {n_outlier} outliers")

    # ── Sauvegarde ────────────────────────────────────────────────────────────
    output = {
        "section":             "§268",
        "description":         "Revalidation H₀ avec corpus étendu (v263+v264+v268)",
        "generated":           datetime.now(timezone.utc).isoformat(),
        "graph_version":       "v18p",
        "vopt":                VOPT,
        "corpus": {
            "n_v263":    len(s263),
            "n_v264":    len(s264),
            "n_v268":    len(s268),
            "n_total":   len(sall),
        },
        "r2_baseline_267":     round(r2_b, 6),
        "n_pairs_baseline_267": n_b,
        "r2_268":              round(r2_268, 6),
        "n_pairs_268":         n_268,
        "n_inf_268":           ninf_268,
        "delta_r2":            round(delta_r2, 6),
        "delta_n_pairs":       delta_n,
        "n_new_contributors":  n_contrib,
        "n_new_neutrals":      n_neutre,
        "n_new_outliers":      n_outlier,
        "new_texts_analysis":  sorted(new_results, key=lambda r: r["delta_r2"]),
        "elapsed_seconds":     round(time.time() - t0, 1),
    }

    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), "utf-8")
    print(f"\nSauvegardé → {OUT_PATH}")
    print(f"Durée totale : {output['elapsed_seconds']}s")

    # ── Résumé console ────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("RÉSUMÉ §268")
    print("=" * 70)
    print(f"  Corpus : 116 → 132 textes  (+16)")
    print(f"  Paires : {n_b} → {n_268}  ({delta_n:+d})")
    print(f"  R²     : {r2_b:.4f} → {r2_268:.4f}  ({delta_r2:+.4f})")
    verdict = ("✅ H₀ confirmée avec corpus étendu"
               if r2_268 >= 0.60
               else "⚠ R² dégradé — analyser les outliers")
    print(f"  Verdict : {verdict}")
    print()
    if n_contrib:
        print("  Top contributeurs (nouveaux) :")
        for r in sorted(new_results, key=lambda x: x["delta_r2"])[:5]:
            if r["flag"] == "contributeur":
                print(f"    ★ {r['local_id']:<40}  ΔR²={r['delta_r2']:+.4f}  ({r['tradition']})")
    if n_outlier:
        print("  Top outliers (nouveaux) :")
        for r in sorted(new_results, key=lambda x: -x["delta_r2"])[:5]:
            if r["flag"] == "outlier":
                print(f"    ✗ {r['local_id']:<40}  ΔR²={r['delta_r2']:+.4f}  ({r['tradition']})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""§210b — Re-calibration V_OPT v3 sur graph v12 (densifié + edges inférées).

Méthode : grid search 3D §177 sur paires signées V14 (37 nodes → 666 paires).
  - Contrainte : w_indirect ≤ w_translation ≤ w_direct
  - Grid : [0.05, 0.95] pas 0.05
  - Split TRAIN/TEST 70/30 sur paires
  - Métrique : R²(d_lex, d_graph) + perm test

Sortie :
  - `research/nipada/falsification/nipada_v210b_calibration_v_opt_v3.json`
  - `docs/rapports/CALIBRATION_VOPT_V3_DENSIFIED_v0.4.0.md`
"""
from __future__ import annotations

import heapq
import importlib.util
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
GRAPH_V12 = ROOT / "research/nipada/falsification/nipada_v210a_graph_v12.json"
OUT_JSON = ROOT / "research/nipada/falsification/nipada_v210b_calibration_v_opt_v3.json"
OUT_MD = ROOT / "docs/rapports/CALIBRATION_VOPT_V3_DENSIFIED_v0.4.0.md"

spec = importlib.util.spec_from_file_location(
    "nipada_calibration_v177", SCRIPTS / "nipada_calibration_v177.py")
v177 = importlib.util.module_from_spec(spec); sys.modules["v177"] = v177
spec.loader.exec_module(v177)


def cosine(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na > 0 and nb > 0 else 0.0


def build_adj(edges_with_channels, weight_map):
    """edges = [(src, tgt, ch)]. Retourne adj dict {node: [(neighbor, cost)]}."""
    adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for src, tgt, ch in edges_with_channels:
        cat = v177.classify_channel(ch)
        w = weight_map[cat]
        cost = -math.log(w) if w > 0 else math.inf
        # bidirectionnel (graphe non-dirigé pour les distances)
        adj[src].append((tgt, cost))
        adj[tgt].append((src, cost))
    # pour chaque (src,tgt) garder le min cost (équivalent max poids)
    for nid, neigh in adj.items():
        best: dict[str, float] = {}
        for tgt, c in neigh:
            if tgt not in best or c < best[tgt]:
                best[tgt] = c
        adj[nid] = list(best.items())
    return adj


def dijkstra(adj, source, targets):
    """Distances de `source` vers chaque node de `targets`."""
    targets = set(targets)
    dist: dict[str, float] = {source: 0.0}
    heap: list[tuple[float, str]] = [(0.0, source)]
    found: dict[str, float] = {}
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, math.inf):
            continue
        if u in targets:
            found[u] = d
            if len(found) == len(targets):
                return found
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return found


def main() -> int:
    graph = json.loads(GRAPH_V12.read_text(encoding="utf-8"))
    nodes = graph["nodes"]
    edges = [(e["src"], e["tgt"], e["channel"]) for e in graph["edges"]]
    print(f"Graph v12 : {len(nodes)} nodes / {len(edges)} edges")

    signed = {nid: n for nid, n in nodes.items() if n.get("v14_signature")}
    work_ids = sorted(signed.keys())
    print(f"Signés V14 : {len(signed)}")

    pairs = []
    for i, a in enumerate(work_ids):
        for b in work_ids[i + 1:]:
            d_lex = 1.0 - cosine(signed[a]["v14_signature"], signed[b]["v14_signature"])
            pairs.append({"a": a, "b": b, "d_lex": d_lex})
    rng = random.Random(2026)
    rng.shuffle(pairs)
    cut = int(0.7 * len(pairs))
    train, test = pairs[:cut], pairs[cut:]
    print(f"Pairs total {len(pairs)} → TRAIN {len(train)} / TEST {len(test)}")

    grid = [round(0.05 + 0.10 * k, 3) for k in range(10)]  # 0.05..0.95 step 0.10
    all_node_ids = list(nodes.keys())
    signed_set = set(work_ids)

    def compute_pair_distances(wd, wt, wi):
        adj = build_adj(edges, {"direct": wd, "translation": wt, "indirect": wi})
        d_pair: dict[tuple[str, str], float] = {}
        for src in work_ids:
            res = dijkstra(adj, src, signed_set)
            for tgt, dst in res.items():
                if src < tgt:
                    d_pair[(src, tgt)] = dst
                elif tgt < src:
                    d_pair[(tgt, src)] = dst
        return d_pair

    best = {"R2_train": -1.0}
    n_eval = 0
    for wd in grid:
        for wt in grid:
            if wt > wd:
                continue
            for wi in grid:
                if wi > wt:
                    continue
                d_pair = compute_pair_distances(wd, wt, wi)
                xs, ys = [], []
                for p in train:
                    key = (p["a"], p["b"]) if p["a"] < p["b"] else (p["b"], p["a"])
                    d = d_pair.get(key)
                    if d is None or not math.isfinite(d):
                        continue
                    xs.append(p["d_lex"]); ys.append(d)
                if len(xs) < 30:
                    continue
                r2 = v177.pearson(xs, ys) ** 2
                n_eval += 1
                if r2 > best["R2_train"]:
                    best = {"R2_train": r2, "wd": wd, "wt": wt, "wi": wi,
                            "n_train": len(xs)}
    print(f"Grid évalué : {n_eval} triplets")
    print(f"Best TRAIN : w_d={best['wd']} w_t={best['wt']} w_i={best['wi']} → R²={best['R2_train']:.4f}")

    # TEST
    d_pair_best = compute_pair_distances(best["wd"], best["wt"], best["wi"])
    xs_te, ys_te = [], []
    for p in test:
        key = (p["a"], p["b"]) if p["a"] < p["b"] else (p["b"], p["a"])
        d = d_pair_best.get(key)
        if d is None or not math.isfinite(d):
            continue
        xs_te.append(p["d_lex"]); ys_te.append(d)
    if len(xs_te) >= 10:
        r_te = v177.pearson(xs_te, ys_te)
        r2_te = r_te * r_te
        p_te = v177.perm_test(xs_te, ys_te, n_iter=2000)
    else:
        r_te, r2_te, p_te = 0.0, 0.0, 1.0
    print(f"TEST : R²={r2_te:.4f} p={p_te:.4f} n={len(xs_te)}")

    def eval_full(wd, wt, wi):
        d_pair = compute_pair_distances(wd, wt, wi)
        xs, ys = [], []
        for p in pairs:
            key = (p["a"], p["b"]) if p["a"] < p["b"] else (p["b"], p["a"])
            d = d_pair.get(key)
            if d is None or not math.isfinite(d):
                continue
            xs.append(p["d_lex"]); ys.append(d)
        if len(xs) < 10:
            return 0.0, 1.0, len(xs)
        r2 = v177.pearson(xs, ys) ** 2
        p = v177.perm_test(xs, ys, n_iter=1000)
        return r2, p, len(xs)

    r2_v1, p_v1, n_v1 = eval_full(0.45, 0.15, 0.01)
    r2_v2, p_v2, n_v2 = eval_full(0.80, 0.50, 0.0001)
    r2_v3, p_v3, n_v3 = eval_full(best["wd"], best["wt"], best["wi"])
    print(f"V_OPT v1 (0.45/0.15/0.01)         : R²={r2_v1:.4f} p={p_v1:.4f} n={n_v1}")
    print(f"V_OPT v2 (0.80/0.50/0.0001)       : R²={r2_v2:.4f} p={p_v2:.4f} n={n_v2}")
    print(f"V_OPT v3 ({best['wd']}/{best['wt']}/{best['wi']}) : R²={r2_v3:.4f} p={p_v3:.4f} n={n_v3}")

    out = {
        "version": "v210b",
        "graph_in": str(GRAPH_V12.relative_to(ROOT)),
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "n_signed_v14": len(signed),
        "n_pairs": len(pairs),
        "n_grid_evaluated": n_eval,
        "best_train": best,
        "test": {"R2": r2_te, "pearson_r": r_te, "p_perm": p_te,
                 "n_pairs_connected": len(xs_te)},
        "comparison_full_set": {
            "v_opt_v1": {"weights": [0.45, 0.15, 0.01], "R2": r2_v1, "p": p_v1, "n": n_v1},
            "v_opt_v2": {"weights": [0.80, 0.50, 0.0001], "R2": r2_v2, "p": p_v2, "n": n_v2},
            "v_opt_v3": {"weights": [best["wd"], best["wt"], best["wi"]],
                         "R2": r2_v3, "p": p_v3, "n": n_v3},
        },
        "overfit_gap": round(best["R2_train"] - r2_te, 4),
        "verdict": (
            "PASS — V_OPT v3 calibré, R²(test) significatif"
            if r2_te > 0.05 and p_te < 0.01
            else f"REVUE — R²(test)={r2_te:.4f}, p={p_te:.4f}"
        ),
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    md = f"""# CALIBRATION V_OPT v3 — Graphe densifié + arêtes inférées (NIPADA v0.4.0-α)

**Date :** 2026-04-30  
**Cellule :** §210b  
**Graphe :** `{GRAPH_V12.relative_to(ROOT)}` (v12 post-§210a inférence d'arêtes)

## Configuration

| Métrique | Valeur |
|---|---|
| Nodes | {len(nodes)} |
| Edges (v9 + §210a inferred) | {len(edges)} |
| Nodes signés V14 | {len(signed)} |
| Paires signées | {len(pairs)} |
| Triplets de poids évalués | {n_eval} |
| TRAIN / TEST | {len(train)} / {len(test)} |

## V_OPT v3 calibré (best)

| Paramètre | Valeur |
|---|---|
| `w_direct` | **{best['wd']}** |
| `w_translation` | **{best['wt']}** |
| `w_indirect` | **{best['wi']}** |
| R²(TRAIN) | {best['R2_train']:.4f} |
| R²(TEST) | **{r2_te:.4f}** |
| p_perm(TEST, n=2000) | {p_te:.4f} |
| Overfit gap (TRAIN − TEST) | {out['overfit_gap']} |

## Comparaison plein-set (666 paires)

| Configuration | Poids | R² | p_perm |
|---|---|---|---|
| V_OPT v1 baseline | (0.45 / 0.15 / 0.01) | {r2_v1:.4f} | {p_v1:.4f} |
| V_OPT v2 (rejeté §209) | (0.80 / 0.50 / 0.0001) | {r2_v2:.4f} | {p_v2:.4f} |
| **V_OPT v3** (this) | ({best['wd']} / {best['wt']} / {best['wi']}) | **{r2_v3:.4f}** | {p_v3:.4f} |

## Verdict

**{out['verdict']}**

## Notes

- L'inférence d'arêtes §210a a ajouté {len(edges) - 180} arêtes ({(len(edges)/180):.1f}× v9), augmentant la connectivité du graphe densifié.
- La calibration §210b utilise les 37 nodes signés V14 du PoC §208 (5 vides skippés, 666 paires).
- Étape suivante (§210c) : signer plus de nodes (fetch suttacentral.net + Gutenberg) pour calibration plus robuste sur n>>37.
"""
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"\nVerdict : {out['verdict']}")
    print(f"Sortie  : {OUT_JSON.relative_to(ROOT)}")
    print(f"Rapport : {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

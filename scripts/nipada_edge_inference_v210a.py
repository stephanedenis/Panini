#!/usr/bin/env python3
"""§210a — Inférence d'arêtes pour les 1675 nodes catalog_only (graph v12).

Heuristiques (par ordre de fiabilité) :
  1. **Auteur identique** (même `author`) → channel="auteur_continu", canonisé
     comme `direct` (0.95 baseline).
  2. **Tradition_micro identique + |Δyear| ≤ 50** → channel="tradition_micro_proche",
     canonisé `indirect`.
  3. **Tradition_label macro × epoch identique + |Δyear| ≤ 100** → channel=
     "tradition_macro", canonisé `indirect` (faible).
  4. **Translation explicite** (tag `translation`/lang ≠ original) → defer §210c.

Évite l'explosion combinatoire :
  - Cap par node : max 30 edges sortantes vers les autres règles 2/3.
  - Pas d'arête réflexive.
  - Dé-dup : si une arête (a,b) existe déjà (v9 ou règle 1), on n'écrase pas.

Sortie : `research/nipada/falsification/nipada_v210a_graph_v12.json`
"""
from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_V11 = ROOT / "research/nipada/falsification/nipada_v208_graph_v11.json"
GRAPH_V12 = ROOT / "research/nipada/falsification/nipada_v210a_graph_v12.json"

MAX_EDGES_PER_NODE_RULE2 = 10
MAX_EDGES_PER_NODE_RULE3 = 5
DELTA_YEAR_RULE2 = 50
DELTA_YEAR_RULE3 = 100


def main() -> int:
    graph = json.loads(GRAPH_V11.read_text(encoding="utf-8"))
    nodes: dict = graph["nodes"]
    edges: list = graph["edges"]
    existing = {(e["src"], e["tgt"]) for e in edges} | {(e["tgt"], e["src"]) for e in edges}

    by_author: dict[str, list[str]] = defaultdict(list)
    by_micro: dict[str, list[str]] = defaultdict(list)
    by_macro: dict[str, list[str]] = defaultdict(list)
    for nid, n in nodes.items():
        a = n.get("author")
        if a:
            by_author[a].append(nid)
        m = n.get("tradition_micro")
        if m:
            by_micro[m].append(nid)
        ml = n.get("tradition_label")
        if ml:
            by_macro[ml].append(nid)

    n_added_r1 = 0
    n_added_r2 = 0
    n_added_r3 = 0
    edges_out: list = list(edges)
    deg_out: dict[str, int] = defaultdict(int)
    for e in edges:
        deg_out[e["src"]] += 1

    # Règle 1 — même auteur
    for author, members in by_author.items():
        if len(members) < 2:
            continue
        for a, b in combinations(members, 2):
            if (a, b) in existing:
                continue
            edges_out.append({"src": a, "tgt": b, "weight": 0.95,
                              "channel": "auteur_continu (§210a)"})
            existing.add((a, b)); existing.add((b, a))
            n_added_r1 += 1

    # Règle 2 — même tradition_micro + |Δyear| ≤ 50
    for micro, members in by_micro.items():
        if len(members) < 2:
            continue
        for a, b in combinations(members, 2):
            if (a, b) in existing:
                continue
            ya = nodes[a].get("year")
            yb = nodes[b].get("year")
            if ya is None or yb is None:
                continue
            try:
                if abs(int(ya) - int(yb)) > DELTA_YEAR_RULE2:
                    continue
            except (TypeError, ValueError):
                continue
            if deg_out[a] >= MAX_EDGES_PER_NODE_RULE2 + len(by_author.get(nodes[a].get("author") or "", [])):
                continue
            edges_out.append({"src": a, "tgt": b, "weight": 0.55,
                              "channel": "tradition_micro_proche (§210a)"})
            existing.add((a, b)); existing.add((b, a))
            deg_out[a] += 1
            n_added_r2 += 1

    # Règle 3 — même tradition_label + |Δyear| ≤ 100
    for macro, members in by_macro.items():
        if len(members) < 2:
            continue
        for a, b in combinations(members, 2):
            if (a, b) in existing:
                continue
            ya = nodes[a].get("year")
            yb = nodes[b].get("year")
            if ya is None or yb is None:
                continue
            try:
                if abs(int(ya) - int(yb)) > DELTA_YEAR_RULE3:
                    continue
            except (TypeError, ValueError):
                continue
            if deg_out[a] >= MAX_EDGES_PER_NODE_RULE2 + MAX_EDGES_PER_NODE_RULE3:
                continue
            edges_out.append({"src": a, "tgt": b, "weight": 0.20,
                              "channel": "tradition_macro (§210a indirect)"})
            existing.add((a, b)); existing.add((b, a))
            deg_out[a] += 1
            n_added_r3 += 1

    graph["edges"] = edges_out
    graph["version"] = "v12_post_v210a_edge_inference"
    graph["n_edges"] = len(edges_out)
    graph["n_nodes"] = len(nodes)
    graph.setdefault("meta", {})
    graph["meta"]["v210a_edge_inference"] = {
        "rule1_auteur_continu":     n_added_r1,
        "rule2_tradition_micro":    n_added_r2,
        "rule3_tradition_macro":    n_added_r3,
        "edges_before":             len(edges),
        "edges_after":              len(edges_out),
    }
    GRAPH_V12.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"§210a — Inférence d'arêtes terminée")
    print(f"  Règle 1 (auteur)         : +{n_added_r1}")
    print(f"  Règle 2 (tradition_micro): +{n_added_r2}")
    print(f"  Règle 3 (tradition_macro): +{n_added_r3}")
    print(f"  Edges : {len(edges)} → {len(edges_out)}  (+{n_added_r1 + n_added_r2 + n_added_r3})")
    print(f"  Sortie : {GRAPH_V12.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

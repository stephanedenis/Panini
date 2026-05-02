#!/usr/bin/env python3
"""
§217 — Diagnostic composantes connexes graph v12
Analyse BFS/DFS de la structure de composantes connexes.
Mesure l'isolation BUDDHIST_AXIAL et identifie les nœuds bridge.

Usage:
    python3 scripts/nipada_components_v217.py
"""

import json
import heapq
import time
import sys
from collections import defaultdict, deque
from pathlib import Path

# Chemins
GRAPH_PATH = Path("../Panini-Research/nipada/falsification/nipada_v210a_graph_v12.json")
CORPUS_PATH = Path("../Panini-Research/nipada/corpus/signed_corpus_v212f.json")
OUTPUT_PATH = Path("../Panini-Research/nipada/falsification/nipada_v217_components.json")


def load_graph(path):
    """Charge graph v12, retourne adjacence non-dirigée."""
    g = json.loads(path.read_text())
    adj = defaultdict(set)
    for e in g["edges"]:
        adj[e["src"]].add(e["tgt"])
        adj[e["tgt"]].add(e["src"])
    return g["nodes"], g["edges"], adj


def find_components(adj, all_nodes):
    """BFS pour trouver toutes les composantes connexes."""
    visited = {}
    comp_id = 0
    for node in all_nodes:
        if node in visited:
            continue
        queue = deque([node])
        visited[node] = comp_id
        while queue:
            cur = queue.popleft()
            for nb in adj.get(cur, []):
                if nb not in visited:
                    visited[nb] = comp_id
                    queue.append(nb)
        comp_id += 1
    # Grouper
    components = defaultdict(list)
    for node, cid in visited.items():
        components[cid].append(node)
    return visited, dict(components)


def analyze_signed_connectivity(components_map, signed_nodes):
    """
    Pour chaque tradition, quels composantes contiennent ses nœuds signés ?
    Calculer les paires cross-tradition avec chemin fini.
    """
    # node_id → component_id
    node_to_comp = {}
    for cid, nodes in components_map.items():
        for n in nodes:
            node_to_comp[n] = cid

    # Grouper par tradition
    by_trad = defaultdict(list)
    for sn in signed_nodes:
        by_trad[sn["tradition_label"]].append(sn["graph_node_id"])

    # Par tradition : quels composants ?
    trad_comps = {}
    for trad, nids in by_trad.items():
        comps = set()
        for nid in nids:
            if nid in node_to_comp:
                comps.add(node_to_comp[nid])
        trad_comps[trad] = {"nodes": len(nids), "components": sorted(comps)}

    # Paires cross-tradition avec chemin fini
    traditions = list(by_trad.keys())
    cross_pairs = {}
    for i in range(len(traditions)):
        for j in range(i + 1, len(traditions)):
            ta, tb = traditions[i], traditions[j]
            nodes_a = [n for n in by_trad[ta] if n in node_to_comp]
            nodes_b = [n for n in by_trad[tb] if n in node_to_comp]
            finite_pairs = sum(
                1
                for na in nodes_a
                for nb in nodes_b
                if node_to_comp[na] == node_to_comp[nb]
            )
            total_pairs = len(nodes_a) * len(nodes_b)
            key = f"{ta}→{tb}"
            cross_pairs[key] = {
                "finite": finite_pairs,
                "total": total_pairs,
                "pct": round(100.0 * finite_pairs / total_pairs, 1) if total_pairs else 0.0,
            }

    return trad_comps, cross_pairs


def find_bridge_nodes(adj, comp_map, signed_nodes, top_k=20):
    """
    Nœuds bridge = nœuds présents dans une composante différente de BUDDHIST
    mais avec des voisins dans la composante isolée de BUDDHIST, ou vice versa.
    Plus généralement : nœuds avec voisins dans plusieurs composantes.
    """
    node_to_comp = {}
    for cid, nodes in comp_map.items():
        for n in nodes:
            node_to_comp[n] = cid

    # Composante principale de BUDDHIST
    by_trad = defaultdict(list)
    for sn in signed_nodes:
        by_trad[sn["tradition_label"]].append(sn["graph_node_id"])

    buddhist_nodes = set(by_trad.get("BUDDHIST_AXIAL", []))
    buddhist_comps = set(node_to_comp.get(n) for n in buddhist_nodes if n in node_to_comp)

    # Nœuds bridge : dans composante BUDDHIST avec voisins hors BUDDHIST composante
    # ou hors composante BUDDHIST avec voisins dans composante BUDDHIST
    bridge_candidates = {}
    for node, comp in node_to_comp.items():
        neighbors = adj.get(node, set())
        neighbor_comps = set(node_to_comp.get(nb) for nb in neighbors if nb in node_to_comp)
        neighbor_comps.discard(comp)  # Voisins dans d'autres composantes
        if neighbor_comps and (comp in buddhist_comps or bool(neighbor_comps & buddhist_comps)):
            bridge_candidates[node] = {
                "own_comp": comp,
                "cross_comps": sorted(neighbor_comps),
                "cross_degree": len(neighbor_comps),
            }

    # Top-K par cross_degree
    top = sorted(bridge_candidates.items(), key=lambda x: -x[1]["cross_degree"])[:top_k]
    return [{"node_id": nid, **info} for nid, info in top]


def component_stats(components_map, nodes_dict):
    """Stats par composante."""
    stats = []
    for cid, node_ids in sorted(components_map.items(), key=lambda x: -len(x[1])):
        stats.append({
            "component_id": cid,
            "size": len(node_ids),
            "sample_nodes": node_ids[:3],
        })
    return stats


def main():
    t0 = time.time()
    print("§217 — Diagnostic composantes connexes graph v12")
    print("=" * 55)

    # Charger
    print("Chargement graph v12...", end=" ", flush=True)
    nodes_dict, edges, adj = load_graph(GRAPH_PATH)
    all_nodes = list(nodes_dict.keys())
    print(f"Nodes={len(all_nodes)} Edges={len(edges)}")

    print("Chargement corpus v212f...", end=" ", flush=True)
    corpus = json.loads(CORPUS_PATH.read_text())
    signed = corpus["signed"]
    print(f"Signed={len(signed)}")

    # Composantes connexes
    print("BFS composantes connexes...", end=" ", flush=True)
    visited, comp_map = find_components(adj, all_nodes)
    n_comps = len(comp_map)
    sizes = sorted([len(v) for v in comp_map.values()], reverse=True)
    print(f"N_composantes={n_comps} | Top5={sizes[:5]}")

    # Analyse connectivité signée
    print("Analyse connectivité par tradition...")
    trad_comps, cross_pairs = analyze_signed_connectivity(comp_map, signed)

    for trad, info in trad_comps.items():
        print(f"  {trad}: {info['nodes']} nœuds → composantes {info['components']}")

    print("\nPaires cross-tradition avec chemin fini:")
    for key, info in cross_pairs.items():
        print(f"  {key}: {info['finite']}/{info['total']} ({info['pct']}%)")

    # Bridge nodes
    print("\nRecherche nœuds bridge...", end=" ", flush=True)
    bridges = find_bridge_nodes(adj, comp_map, signed, top_k=20)
    print(f"Candidats trouvés: {len(bridges)}")

    # Stats composantes
    comp_stats = component_stats(comp_map, nodes_dict)
    giant = comp_stats[0] if comp_stats else {}

    elapsed = time.time() - t0

    # Résultat JSON
    result = {
        "section": "§217",
        "description": "Diagnostic composantes connexes graph v12",
        "graph": {
            "nodes": len(all_nodes),
            "edges": len(edges),
            "n_components": n_comps,
            "component_sizes_top10": sizes[:10],
            "giant_component_size": sizes[0] if sizes else 0,
            "giant_component_pct": round(100.0 * sizes[0] / len(all_nodes), 1) if sizes else 0.0,
        },
        "signed_corpus": {
            "total": len(signed),
            "traditions": trad_comps,
        },
        "cross_tradition_reachability": cross_pairs,
        "bridge_node_candidates": bridges[:10],
        "component_stats_top10": comp_stats[:10],
        "elapsed_s": round(elapsed, 1),
    }

    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nSauvegardé → {OUTPUT_PATH}")

    # Verdict
    buddhist_isolated = all(
        info["finite"] == 0
        for key, info in cross_pairs.items()
        if "BUDDHIST" in key
    )
    print("\n--- VERDICT ---")
    print(f"BUDDHIST_AXIAL isolé : {'OUI ⚠️' if buddhist_isolated else 'NON ✓'}")
    print(f"Composante géante : {sizes[0]} nodes ({round(100.0 * sizes[0] / len(all_nodes), 1)}%)")
    print(f"Durée : {elapsed:.1f}s")

    return 0


if __name__ == "__main__":
    sys.exit(main())

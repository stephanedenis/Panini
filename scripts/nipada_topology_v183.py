#!/usr/bin/env python3
"""§183 — Analyse topologique comparée des sous-graphes Ouest vs Est.

§182 a établi que la limite NW×NW est STRUCTURELLE et a proposé l'explication
"transmission critique cumulative occidentale vs lignées de commentaires
orientales". §183 quantifie cette différence par mesures topologiques sur
le graphe v8.

Mesures :
  - Densité (edges / max_edges)
  - Degré moyen, distribution des degrés
  - Coefficient de clustering local moyen (triangles/triplets)
  - Diamètre du sous-graphe (plus long plus court chemin)
  - Variance des distances Floyd-Warshall
  - Centralité de betweenness (% de chemins qui passent par chaque nœud)
  - Nombre de cycles élémentaires (cyclomatic number = E − N + C)
  - Mix entre channels (direct / translation / indirect)

Sous-graphes :
  - WEST = œuvres tradition européenne/gréco-latine
  - EAST = œuvres tradition orientale (chinois, indien, bouddhique, islamique)
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"

EAST_TRADS = {
    "chinese_classics", "daoism", "buddhism_theravada", "hinduism_smriti",
    "hinduism_shruti", "buddhism_modernist", "islamic_canon",
    "islamic_skeptic", "chinese_critic", "chinese_classical",
    "chinese_legalist", "chinese_mohist",
}


def classify_channel(ch: str) -> str:
    s = ch.lower()
    if any(k in s for k in ["traduction", "translation"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "tradition",
        "comparat", "scepticisme", "lecteur", "ascendant", "post-",
        "écho", "reçu", "même école", "succession", "admire", "mentionne",
        "réception", "critique", "synthèse", "commentaire", "compile",
        "milieu",
    ]):
        return "indirect"
    return "direct"


def is_critique(ch: str) -> bool:
    """Détecte si l'arête est de nature 'critique cumulative'
    (citation, réfutation, polémique active)."""
    s = ch.lower()
    return any(k in s for k in [
        "critique", "réfut", "rejett", "rival", "satir", "polém",
        "attaqu", "contre", "oppos", "anti-", "scepti",
    ])


def is_commentary(ch: str) -> bool:
    """Détecte si l'arête est de nature 'commentaire/exégèse'."""
    s = ch.lower()
    return any(k in s for k in [
        "commentaire", "bhāṣya", "bhasya", "compile", "synthèse",
        "scolie", "exég", "kalām", "kalam", "isnād", "tafsir",
    ])


def floyd_warshall_unweighted(nodes_list, adj):
    """Distances en nombre d'arêtes."""
    idx = {n: i for i, n in enumerate(nodes_list)}
    N = len(nodes_list)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0
    for u, ngbs in adj.items():
        if u not in idx:
            continue
        for v in ngbs:
            if v not in idx:
                continue
            D[idx[u]][idx[v]] = 1
    for k in range(N):
        for i in range(N):
            dik = D[i][k]
            if dik == INF:
                continue
            for j in range(N):
                nd = dik + D[k][j]
                if nd < D[i][j]:
                    D[i][j] = nd
    return D, idx


def clustering_coefficient(nodes_list, adj):
    """Coefficient moyen de clustering local."""
    coefs = []
    for u in nodes_list:
        ngbs = list(adj.get(u, set()))
        k = len(ngbs)
        if k < 2:
            continue
        triangles = 0
        for i in range(len(ngbs)):
            for j in range(i + 1, len(ngbs)):
                if ngbs[j] in adj.get(ngbs[i], set()):
                    triangles += 1
        possible = k * (k - 1) / 2
        coefs.append(triangles / possible)
    return sum(coefs) / len(coefs) if coefs else 0.0


def betweenness_simple(nodes_list, adj):
    """Betweenness centrality non-pondérée (BFS pour chaque source)."""
    bc = {n: 0.0 for n in nodes_list}
    nset = set(nodes_list)
    for s in nodes_list:
        # BFS
        dist = {s: 0}
        pred = defaultdict(list)
        queue = [s]
        order = []
        while queue:
            new_q = []
            for u in queue:
                order.append(u)
                for v in adj.get(u, set()):
                    if v not in nset:
                        continue
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        new_q.append(v)
                    if dist[v] == dist[u] + 1:
                        pred[v].append(u)
            queue = new_q
        # Number of shortest paths
        sigma = {n: 0 for n in nodes_list}
        sigma[s] = 1
        for u in order:
            for w in adj.get(u, set()):
                if w not in nset:
                    continue
                if w in dist and dist[w] == dist[u] + 1:
                    sigma[w] += sigma[u]
        # Accumulation
        delta = {n: 0.0 for n in nodes_list}
        for w in reversed(order):
            for v in pred[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    # Normalize (undirected)
    n = len(nodes_list)
    if n > 2:
        scale = 1.0 / ((n - 1) * (n - 2))
        for k in bc:
            bc[k] *= scale
    return bc


def analyze_subgraph(label, node_ids, edges_raw, full_nodes):
    """Analyse topologique d'un sous-graphe."""
    nset = set(node_ids)
    adj = defaultdict(set)
    edges_in = []
    channels = Counter()
    critique_count = 0
    commentary_count = 0
    for e in edges_raw:
        s, t = e.get("src"), e.get("tgt")
        if s in nset and t in nset:
            adj[s].add(t)
            adj[t].add(s)
            edges_in.append(e)
            ch_class = classify_channel(e.get("channel", ""))
            channels[ch_class] += 1
            if is_critique(e.get("channel", "")):
                critique_count += 1
            if is_commentary(e.get("channel", "")):
                commentary_count += 1

    N = len(node_ids)
    E = len(edges_in)
    max_E = N * (N - 1) / 2 if N > 1 else 1
    density = E / max_E if max_E else 0.0

    degrees = [len(adj.get(u, set())) for u in node_ids]
    mean_deg = sum(degrees) / len(degrees) if degrees else 0.0
    max_deg = max(degrees) if degrees else 0
    iso = sum(1 for d in degrees if d == 0)

    cluster = clustering_coefficient(node_ids, adj)

    # Composantes connexes
    seen = set()
    comps = []
    for u in node_ids:
        if u in seen:
            continue
        stack = [u]
        comp = set()
        while stack:
            v = stack.pop()
            if v in comp:
                continue
            comp.add(v)
            stack.extend(adj.get(v, set()))
        comps.append(comp)
        seen |= comp
    n_comps = len(comps)
    largest = max(len(c) for c in comps) if comps else 0

    # Cyclomatic number = E - N + C
    cyclomatic = E - N + n_comps

    # Diamètre + distances (sur plus grosse composante uniquement)
    diameter = 0
    avg_dist = 0.0
    var_dist = 0.0
    if largest > 1:
        big = [u for u in node_ids if len(adj.get(u, set())) > 0]
        big = [u for u in big if u in max(comps, key=len)]
        if len(big) > 1:
            D, _ = floyd_warshall_unweighted(big, adj)
            dists = []
            n = len(D)
            for i in range(n):
                for j in range(i + 1, n):
                    if D[i][j] != float("inf"):
                        dists.append(D[i][j])
            if dists:
                diameter = max(dists)
                avg_dist = sum(dists) / len(dists)
                m = avg_dist
                var_dist = sum((d - m) ** 2 for d in dists) / len(dists)

    bc = betweenness_simple(node_ids, adj)
    bc_top = sorted(bc.items(), key=lambda kv: kv[1], reverse=True)[:5]

    return {
        "label": label,
        "n_nodes": N,
        "n_edges": E,
        "density": round(density, 4),
        "mean_degree": round(mean_deg, 2),
        "max_degree": max_deg,
        "isolated_nodes": iso,
        "n_components": n_comps,
        "largest_component": largest,
        "cyclomatic_number": cyclomatic,
        "clustering_coefficient": round(cluster, 4),
        "diameter": diameter,
        "avg_distance": round(avg_dist, 2),
        "var_distance": round(var_dist, 3),
        "channels": dict(channels),
        "critique_edges": critique_count,
        "commentary_edges": commentary_count,
        "betweenness_top5": [(n, round(v, 4)) for n, v in bc_top],
    }


def main():
    print("=== §183 — Analyse topologique comparée Ouest vs Est ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges\n")

    # Charger traditions des œuvres au corpus
    corpus_dir = ROOT / "corpus" / "protoatheism"
    work_traditions = {}
    for wdir in corpus_dir.iterdir():
        if not wdir.is_dir():
            continue
        prov_p = wdir / "PROVENANCE.json"
        if not prov_p.exists():
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", wdir.name)
        work_traditions[wid] = prov.get("tradition") or "unknown"

    east_works = {w for w, t in work_traditions.items() if t in EAST_TRADS}
    west_works = {w for w, t in work_traditions.items()
                  if t and t not in EAST_TRADS and t != "unknown"}

    # Inclure les pivots philosophiques (non-œuvres) selon affinité
    east_pivots_known = {
        "buddha", "vyāsa", "nāgārjuna", "śaṅkara", "wang_chong",
        "śramaṇa", "mu'tazilites", "ash'arites", "asharites",
        "mu_tazilites", "laozi", "zhuangzi", "confucius", "mencius",
        "khayyam", "han_fei", "ajita_kesakambali", "al_nazzam",
        "ibn_rushd", "averroes", "ibn_sina", "avicenna",
        # traducteurs/orientalistes : classés EAST (porteurs)
        "muller_max", "max_muller", "carus_paul", "arnold_edwin",
        "legge_james", "rodwell_jm", "giles_h_a", "anquetil_duperron",
        "fitzgerald", "fitzgerald_edward",
    }

    east_nodes = (set(east_works) | east_pivots_known) & set(nodes.keys())
    # Règle inverse : tout nœud non-EAST est WEST (incluant les pivots
    # philosophiques européens non listés explicitement)
    west_nodes = set(nodes.keys()) - east_nodes
    other_nodes = set()

    print(f"East nodes: {len(east_nodes)}")
    print(f"West nodes: {len(west_nodes)}")
    print(f"Other (unclassified): {len(other_nodes)}\n")
    if other_nodes:
        print(f"  unclassified sample: {sorted(other_nodes)[:8]}\n")

    west_stats = analyze_subgraph("WEST", sorted(west_nodes), edges, nodes)
    east_stats = analyze_subgraph("EAST", sorted(east_nodes), edges, nodes)
    full_stats = analyze_subgraph("FULL", sorted(nodes.keys()), edges, nodes)

    # Print tableau comparatif
    print("=" * 80)
    print(f"{'Mesure':<32}{'WEST':>14}{'EAST':>14}{'FULL':>14}")
    print("=" * 80)
    keys = [
        ("n_nodes", "Nodes", "{:d}"),
        ("n_edges", "Edges", "{:d}"),
        ("density", "Density", "{:.4f}"),
        ("mean_degree", "Mean degree", "{:.2f}"),
        ("max_degree", "Max degree", "{:d}"),
        ("isolated_nodes", "Isolated", "{:d}"),
        ("n_components", "Components", "{:d}"),
        ("largest_component", "Largest comp", "{:d}"),
        ("cyclomatic_number", "Cyclomatic E-N+C", "{:d}"),
        ("clustering_coefficient", "Clustering coef", "{:.4f}"),
        ("diameter", "Diameter", "{:d}"),
        ("avg_distance", "Avg distance", "{:.2f}"),
        ("var_distance", "Var distance", "{:.3f}"),
        ("critique_edges", "Critique edges", "{:d}"),
        ("commentary_edges", "Commentary edges", "{:d}"),
    ]
    for k, label, fmt in keys:
        w = west_stats.get(k, 0)
        e = east_stats.get(k, 0)
        f = full_stats.get(k, 0)
        try:
            print(f"{label:<32}{fmt.format(w):>14}{fmt.format(e):>14}{fmt.format(f):>14}")
        except Exception:
            print(f"{label:<32}{str(w):>14}{str(e):>14}{str(f):>14}")
    print("=" * 80)

    print("\nChannels distribution:")
    print(f"  WEST: {west_stats['channels']}")
    print(f"  EAST: {east_stats['channels']}")
    print(f"  FULL: {full_stats['channels']}")

    print(f"\nBetweenness top-5:")
    print(f"  WEST: {west_stats['betweenness_top5']}")
    print(f"  EAST: {east_stats['betweenness_top5']}")

    # Diagnostic quantitatif
    print(f"\n=== DIAGNOSTIC QUANTITATIF ===")
    ratio_density = east_stats["density"] / west_stats["density"] if west_stats["density"] else 0
    ratio_cluster = (east_stats["clustering_coefficient"] /
                     west_stats["clustering_coefficient"]
                     if west_stats["clustering_coefficient"] else 0)
    ratio_cycl = (east_stats["cyclomatic_number"] /
                  west_stats["cyclomatic_number"]
                  if west_stats["cyclomatic_number"] else 0)
    print(f"  Density EAST/WEST    = {ratio_density:.2f}")
    print(f"  Clustering EAST/WEST = {ratio_cluster:.2f}")
    print(f"  Cyclomatic EAST/WEST = {ratio_cycl:.2f}")

    crit_w = west_stats["critique_edges"]
    crit_e = east_stats["critique_edges"]
    com_w = west_stats["commentary_edges"]
    com_e = east_stats["commentary_edges"]
    print(f"  Critique edges     WEST={crit_w}, EAST={crit_e}")
    print(f"  Commentary edges   WEST={com_w}, EAST={com_e}")

    # Output
    out = {
        "version": "v183_topology",
        "graph_version": "v8_§182",
        "west": west_stats,
        "east": east_stats,
        "full": full_stats,
        "ratios": {
            "density_east_west": ratio_density,
            "clustering_east_west": ratio_cluster,
            "cyclomatic_east_west": ratio_cycl,
        },
        "interpretation": (
            "Si density EAST << WEST, clustering EAST << WEST, et cyclomatic "
            "EAST << WEST, alors le sous-graphe oriental est topologiquement "
            "ARBORESCENT (peu de cycles), ce qui implique des distances "
            "Floyd-Warshall sur-déterminées par quelques arêtes uniques → "
            "variance faible des distances → R²(NW×NW) mécaniquement nul."
        ),
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    out_path = RES_DIR / "nipada_v183_topology_west_east.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

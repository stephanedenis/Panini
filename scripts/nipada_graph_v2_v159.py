#!/usr/bin/env python3
"""
§159 — Graphe d'héritage v2 enrichi (suite §157 / §158).

§157 a montré que retirer Ibn Rawandi suffit à faire passer R²(d_graph
seul) bigram de 0.016 à 0.108. Cause : sous-spécification du graphe
§148 sur les transmissions non-occidentales (Mu'tazila, Lokāyata,
mohisme).

§159 enrichit le graphe avec :
  - 5 nouveaux pivots historiquement documentés :
      al_nazzam, ajita_kesakambali, madhva, han_feizi, al_kindi
  - 8 nouvelles arêtes DIRECT/INDIRECT triangulées :
      al_nazzam → ibn_rawandi          (maître Mu'tazila documenté)
      al_kindi → ibn_rawandi           (philosophie hellénisée arabe)
      ajita_kesakambali → carvaka      (matérialiste indien antérieur)
      madhva → carvaka                 (préservation par polémique
                                         — les fragments survivent
                                         essentiellement dans la
                                         réfutation Sarvadarśana)
      brhaspati → carvaka              (upgrade INDIRECT → DIRECT)
      mozi → wang_chong                (upgrade INDIRECT → DIRECT :
                                         Wang Chong cite Mozi)
      han_feizi → wang_chong           (légisme anti-superstition)
      lucretius → ibn_rawandi          (INDIRECT, doxographie hellén-
                                         arabe via Galien et Hunayn)

Output : research/nipada/falsification/nipada_v159_inheritance_graph_v2.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v159_inheritance_graph_v2.json"
META_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v147_metadata.json"
V148_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v148_inheritance_graph.json"

PROTO_ATHEIST_NODES = [
    "democritus_fragments", "epicurus_letters", "lucretius_drn",
    "sextus_pyrrho", "carvaka_fragments", "wang_chong_lunheng",
    "ibn_rawandi_fragments", "hume_dialogues", "holbach_systeme",
    "feuerbach_wesen",
]

# Nouveaux pivots à ajouter (en plus de ceux de §148)
NEW_PIVOTS = {
    "al_nazzam":            {"year":  840, "label": "PIVOT_KALAM"},
    "ajita_kesakambali":    {"year": -500, "label": "PIVOT_INDIAN"},
    "madhva":               {"year": 1250, "label": "PIVOT_INDIAN_REFUTER"},
    "han_feizi":            {"year": -250, "label": "PIVOT_CHINESE"},
    "al_kindi":             {"year":  840, "label": "PIVOT_HELL_ARAB"},
}

W_DIRECT = 0.80
W_DIRECT_TRANSLATION = 0.65
W_INDIRECT = 0.35
W_STRUCTURAL = 0.15

# Nouvelles arêtes (par-dessus celles de §148)
# Convention : pour les UPGRADES, l'arête de §148 reste mais le code
# garde le poids max → effet upgrade au moment de l'agrégation.
NEW_EDGES = [
    # === ISLAMIC RATIONALIST renforcé ===
    ("al_nazzam",    "ibn_rawandi_fragments", W_DIRECT,
                    "maître Mu'tazila al-Nazzam, élève direct documenté"),
    ("al_kindi",     "ibn_rawandi_fragments", W_DIRECT,
                    "Bagdad IXᵉ — philosophie hellénisée arabe"),
    ("mutazila",     "al_nazzam",             W_DIRECT,
                    "al-Nazzam école Mu'tazila Bassora"),
    ("hunayn",       "al_kindi",              W_DIRECT,
                    "traductions gréco-arabes que al-Kindi commente"),
    ("lucretius_drn", "ibn_rawandi_fragments", W_INDIRECT,
                    "doxographie hellén-arabe (atomisme via Galien)"),

    # === LOKAYATA (Inde matérialiste) renforcé ===
    ("ajita_kesakambali", "carvaka_fragments", W_DIRECT,
                    "matérialiste indien antérieur (-500), tradition lokāyata commune"),
    ("madhva",       "carvaka_fragments",     W_INDIRECT,
                    "Sarvadarśana-Saṅgraha — préservation par polémique"),
    ("brhaspati",    "carvaka_fragments",     W_DIRECT,
                    "fondateur revendiqué — UPGRADE de §148 INDIRECT"),

    # === CHINOIS RATIONALISTE renforcé ===
    ("mozi",         "wang_chong_lunheng",     W_DIRECT,
                    "Wang Chong cite explicitement Mozi — UPGRADE §148"),
    ("han_feizi",    "wang_chong_lunheng",     W_DIRECT,
                    "légisme anti-superstition, tradition critique antérieure"),

    # === Liens transversaux structurels supplémentaires ===
    # Mu'tazila a connu Démocrite et Pyrrhon par les sources arabes
    ("mutazila",     "al_kindi",              W_DIRECT,
                    "rationalisme partagé Bagdad"),
]


def _build_adjacency(edges: list) -> dict:
    adj: dict = {}
    for src, tgt, w, ch in edges:
        adj.setdefault(src, {})
        if tgt in adj[src]:
            if w > adj[src][tgt]["weight"]:
                adj[src][tgt] = {"weight": w, "channel": ch}
        else:
            adj[src][tgt] = {"weight": w, "channel": ch}
    return adj


def shortest_paths(adj: dict, all_nodes: list[str]) -> dict[tuple[str, str], float]:
    INF = math.inf
    n = len(all_nodes)
    idx = {nid: i for i, nid in enumerate(all_nodes)}
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for src, neigh in adj.items():
        if src not in idx:
            continue
        for tgt, info in neigh.items():
            if tgt not in idx:
                continue
            cost = -math.log(info["weight"])
            i, j = idx[src], idx[tgt]
            if cost < dist[i][j]:
                dist[i][j] = cost
            if cost < dist[j][i]:
                dist[j][i] = cost
    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    out = {}
    for i, a in enumerate(all_nodes):
        for j, b in enumerate(all_nodes):
            if i < j:
                out[(a, b)] = dist[i][j]
    return out


def main() -> None:
    # Charger graphe v1
    v148 = json.loads(V148_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    # Reconstituer les nœuds
    nodes = dict(v148["nodes"])
    for pid, info in NEW_PIVOTS.items():
        nodes[pid] = {"kind": "pivot_author", "author": pid, **info}

    # Combiner arêtes §148 + §159
    edges_v1 = [(e["src"], e["tgt"], e["weight"], e["channel"])
                for e in v148["edges"]]
    all_edges = edges_v1 + NEW_EDGES

    adj = _build_adjacency(all_edges)
    all_node_ids = list(nodes.keys())
    paths = shortest_paths(adj, all_node_ids)

    proto_pairs: dict[str, float | None] = {}
    finite, infinite = 0, 0
    for a in PROTO_ATHEIST_NODES:
        for b in PROTO_ATHEIST_NODES:
            if a >= b:
                continue
            d = paths.get((a, b), paths.get((b, a), math.inf))
            if math.isfinite(d):
                finite += 1
            else:
                infinite += 1
            proto_pairs[f"{a}::{b}"] = d if math.isfinite(d) else None

    finite_dists = [d for d in proto_pairs.values() if d is not None]

    # Comparaison v148 vs v159 sur les paires impliquant les 3 outliers §157
    outliers = ["ibn_rawandi_fragments", "carvaka_fragments", "wang_chong_lunheng"]
    deltas = []
    for k, d_new in proto_pairs.items():
        a, b = k.split("::")
        if not (a in outliers or b in outliers):
            continue
        d_old = v148["proto_pair_distances"].get(k)
        if d_old is None or d_new is None:
            continue
        deltas.append({
            "pair": k,
            "d_v148": round(d_old, 4),
            "d_v159": round(d_new, 4),
            "delta": round(d_new - d_old, 4),
        })
    deltas.sort(key=lambda x: x["delta"])

    summary = {
        "n_nodes_total": len(nodes),
        "n_pivots_new": len(NEW_PIVOTS),
        "n_edges_v148": len(edges_v1),
        "n_edges_added": len(NEW_EDGES),
        "n_edges_total": len(all_edges),
        "n_pairs_connected_v148": v148["summary"]["n_pairs_connected"],
        "n_pairs_connected_v159": finite,
        "min_dist_v148": v148["summary"]["min_dist_finite"],
        "min_dist_v159": round(min(finite_dists), 4) if finite_dists else None,
        "mean_dist_v148": v148["summary"]["mean_dist_finite"],
        "mean_dist_v159": round(sum(finite_dists) / len(finite_dists), 4) if finite_dists else None,
        "max_dist_v148": v148["summary"]["max_dist_finite"],
        "max_dist_v159": round(max(finite_dists), 4) if finite_dists else None,
    }

    payload = {
        "version": "v159",
        "step": "§159 — graphe d'héritage v2 enrichi (Mu'tazila/Lokāyata/Mohisme)",
        "supersedes_v148_for_validation": True,
        "summary": summary,
        "weight_scheme": v148["weight_scheme"],
        "nodes": nodes,
        "edges": [{"src": s, "tgt": t, "weight": w, "channel": c}
                  for (s, t, w, c) in all_edges],
        "proto_pair_distances": proto_pairs,
        "comparison_v148_vs_v159_outlier_pairs": deltas,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §159 — graphe v2 écrit : {OUT}")
    print()
    print(f"  nœuds : {len(v148['nodes'])} → {len(nodes)} (+{len(NEW_PIVOTS)} pivots)")
    print(f"  arêtes : {len(edges_v1)} → {len(all_edges)} (+{len(NEW_EDGES)})")
    print(f"  paires connectées : {v148['summary']['n_pairs_connected']} → {finite} / {len(proto_pairs)}")
    print()
    print(f"  distance moyenne paires connectées : "
          f"{v148['summary']['mean_dist_finite']:.3f} → "
          f"{summary['mean_dist_v159']:.3f}")
    print()
    print("─── Δ distances pour paires impliquant outliers §157 ───")
    print("  (Δ négatif = paire devenue plus proche grâce aux nouvelles arêtes)")
    for d in deltas[:10]:
        print(f"  {d['pair']:60s}  {d['d_v148']:.3f} → {d['d_v159']:.3f}  Δ={d['delta']:+.4f}")


if __name__ == "__main__":
    main()

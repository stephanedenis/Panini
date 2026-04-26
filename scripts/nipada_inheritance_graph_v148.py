#!/usr/bin/env python3
"""
§148 — Construction du graphe d'héritage proto-athéiste.

Nœuds = auteurs (10 œuvres + auteurs-pivots non proto-athéistes mais
nécessaires à la transmission : Cicéron, Bayle, Gassendi, Spinoza,
Diderot, Hunayn ibn Ishaq…).

Arêtes = transmission attestée (du source vers le receveur), pondérée :
  - direct (lecture documentée, citation explicite)        : 0.80
  - direct via traduction                                   : 0.65
  - indirect (via doxographie, intermédiaire, redécouverte) : 0.35
  - structurel (parenté par contexte matériel sans contact) : 0.15

Ce graphe est la **structure causale** que la signature V14 doit
reproduire. La validation §150 mesurera la corrélation entre similarité
de signature et inverse de la distance dans ce graphe.

Output : research/nipada/falsification/nipada_v148_inheritance_graph.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v148_inheritance_graph.json"
META_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v147_metadata.json"

# 10 œuvres canoniques (clés cohérentes avec §141-§147)
PROTO_ATHEIST_NODES = [
    "democritus_fragments",
    "epicurus_letters",
    "lucretius_drn",
    "sextus_pyrrho",
    "carvaka_fragments",
    "wang_chong_lunheng",
    "ibn_rawandi_fragments",
    "hume_dialogues",
    "holbach_systeme",
    "feuerbach_wesen",
]

# Auteurs-pivots intermédiaires (non proto-athéistes mais conduits de transmission)
PIVOT_NODES = {
    "leucippe":              {"year": -440,  "label": "PIVOT_GRECO"},
    "anaxagore":             {"year": -440,  "label": "PIVOT_GRECO"},
    "pyrrhon":               {"year": -310,  "label": "PIVOT_SCEPT"},
    "enesidemus":            {"year":  -50,  "label": "PIVOT_SCEPT"},
    "ciceron":               {"year":  -50,  "label": "PIVOT_GRECO_LAT"},
    "aristote":              {"year": -340,  "label": "PIVOT_GRECO"},
    "galien_ar":             {"year":  170,  "label": "PIVOT_HELL_ARAB"},
    "hunayn":                {"year":  860,  "label": "PIVOT_TRAD_ARAB"},
    "mutazila":              {"year":  830,  "label": "PIVOT_KALAM"},
    "brhaspati":             {"year": -500,  "label": "PIVOT_INDIAN"},
    "vedas":                 {"year": -800,  "label": "PIVOT_INDIAN_REJECTED"},
    "confucius":             {"year": -500,  "label": "PIVOT_CHINESE"},
    "mozi":                  {"year": -430,  "label": "PIVOT_CHINESE"},
    "bayle":                 {"year": 1697,  "label": "PIVOT_MODERN"},
    "spinoza":               {"year": 1670,  "label": "PIVOT_MODERN"},
    "gassendi":              {"year": 1640,  "label": "PIVOT_MODERN"},
    "hobbes":                {"year": 1651,  "label": "PIVOT_MODERN"},
    "locke":                 {"year": 1690,  "label": "PIVOT_MODERN"},
    "diderot":               {"year": 1765,  "label": "PIVOT_MODERN"},
    "lamettrie":             {"year": 1748,  "label": "PIVOT_MODERN"},
    "hegel":                 {"year": 1820,  "label": "PIVOT_MODERN"},
    "strauss_df":            {"year": 1835,  "label": "PIVOT_MODERN"},
}

# Poids canoniques
W_DIRECT = 0.80
W_DIRECT_TRANSLATION = 0.65
W_INDIRECT = 0.35
W_STRUCTURAL = 0.15

# Arêtes (source → cible, poids, type)
# Convention : (source_id, target_id, weight, channel)
EDGES = [
    # === GRECO_LAT_MATERIAL ===
    ("leucippe",     "democritus_fragments",  W_DIRECT,             "maître direct"),
    ("anaxagore",    "democritus_fragments",  W_DIRECT,             "contemporain lu"),
    ("democritus_fragments", "epicurus_letters", W_DIRECT,          "atomisme repris (Nausiphane médiateur)"),
    ("aristote",     "epicurus_letters",      W_INDIRECT,           "critique connue"),
    ("pyrrhon",      "epicurus_letters",      W_INDIRECT,           "ataraxie partagée"),
    ("epicurus_letters", "lucretius_drn",     W_DIRECT,             "transmission systématique en latin"),
    ("democritus_fragments", "lucretius_drn", W_INDIRECT,           "via Épicure"),

    # === SCEPT ===
    ("pyrrhon",      "sextus_pyrrho",       W_DIRECT,             "école pyrrhonienne"),
    ("enesidemus",   "sextus_pyrrho",       W_DIRECT,             "scepticisme néo-pyrrhonien"),
    ("aristote",     "sextus_pyrrho",       W_INDIRECT,           "critique systématique"),
    ("epicurus_letters", "sextus_pyrrho",   W_INDIRECT,           "doxographie matérialiste"),

    # === INDIAN_MATERIAL ===
    ("brhaspati",    "carvaka_fragments",     W_DIRECT,             "fondateur légendaire"),
    ("vedas",        "carvaka_fragments",     W_INDIRECT,           "rejet polémique structurant"),

    # === CHINESE_MATERIAL ===
    ("confucius",    "wang_chong_lunheng",     W_DIRECT,             "critique respectueuse"),
    ("mozi",         "wang_chong_lunheng",     W_INDIRECT,           "rationalisme antérieur"),

    # === ISLAMIC_RATIONALIST (carrefour de transmission gréco-arabe) ===
    ("mutazila",     "ibn_rawandi_fragments", W_DIRECT,           "école de formation puis rupture"),
    ("aristote",     "ibn_rawandi_fragments", W_DIRECT_TRANSLATION, "via traductions Hunayn"),
    ("hunayn",       "ibn_rawandi_fragments", W_DIRECT_TRANSLATION, "traductions arabes"),
    ("galien_ar",    "ibn_rawandi_fragments", W_DIRECT_TRANSLATION, "traductions arabes"),
    ("democritus_fragments", "ibn_rawandi_fragments", W_INDIRECT, "doxographie arabe (atomisme rapporté)"),
    ("sextus_pyrrho", "ibn_rawandi_fragments", W_INDIRECT,      "doxographie arabe (scepticisme rapporté)"),

    # === MODERN_WESTERN — Hume ===
    ("sextus_pyrrho", "hume_dialogues",     W_DIRECT_TRANSLATION, "trad. latines XVIᵉ"),
    ("bayle",        "hume_dialogues",        W_DIRECT,             "Dictionnaire critique"),
    ("ciceron",      "hume_dialogues",        W_DIRECT,             "De natura deorum (modèle direct)"),
    ("lucretius_drn", "hume_dialogues",       W_DIRECT,             "redécouverte humaniste"),
    ("locke",        "hume_dialogues",        W_DIRECT,             "empirisme antérieur"),

    # === MODERN_WESTERN — Holbach ===
    ("lucretius_drn", "holbach_systeme",      W_DIRECT,             "matérialisme antique référence centrale"),
    ("spinoza",      "holbach_systeme",       W_DIRECT,             "déterminisme"),
    ("lamettrie",    "holbach_systeme",       W_DIRECT,             "Homme machine"),
    ("diderot",      "holbach_systeme",       W_DIRECT,             "ami et collaborateur (salon)"),
    ("hume_dialogues", "holbach_systeme",     W_DIRECT,             "empirisme contemporain"),
    ("hobbes",       "holbach_systeme",       W_DIRECT,             "matérialisme politique"),
    ("gassendi",     "holbach_systeme",       W_INDIRECT,           "épicurisme christianisé renversé"),

    # === MODERN_WESTERN — Feuerbach ===
    ("hegel",        "feuerbach_wesen",     W_DIRECT,             "maître renversé"),
    ("spinoza",      "feuerbach_wesen",     W_DIRECT,             "panthéisme"),
    ("holbach_systeme", "feuerbach_wesen",  W_DIRECT,             "matérialisme français"),
    ("hume_dialogues", "feuerbach_wesen",   W_INDIRECT,           "scepticisme religieux"),
    ("strauss_df",   "feuerbach_wesen",     W_DIRECT,             "Vie de Jésus 1835"),

    # === Liens transversaux structurels (VECU partagé sans contact direct) ===
    ("wang_chong_lunheng", "carvaka_fragments", W_STRUCTURAL,        "matérialisme antique sans contact (parenté VECU)"),
    ("carvaka_fragments", "wang_chong_lunheng", W_STRUCTURAL,        "symétrique"),
]


def _all_nodes() -> dict[str, dict]:
    """Construit le dict de tous les nœuds (proto-ath + pivots) avec métadonnées."""
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    nodes: dict[str, dict] = {}
    for wid in PROTO_ATHEIST_NODES:
        w = meta["works"][wid]
        nodes[wid] = {
            "kind": "proto_atheist_work",
            "author": w["author"],
            "year": w["writing_year"],
            "language_original": w["language_original"],
            "tradition_label": w["tradition_label"],
        }
    for pid, info in PIVOT_NODES.items():
        nodes[pid] = {"kind": "pivot_author", "author": pid, **info}
    return nodes


def _build_adjacency(edges: list) -> dict[str, dict[str, dict]]:
    """Adjacency dirigée : src → {tgt: {weight, channel}}. Conserve max si doublon."""
    adj: dict[str, dict[str, dict]] = {}
    for src, tgt, w, ch in edges:
        adj.setdefault(src, {})
        # En cas de double arête src→tgt, garder le poids max (transmission la plus forte)
        if tgt in adj[src]:
            if w > adj[src][tgt]["weight"]:
                adj[src][tgt] = {"weight": w, "channel": ch}
        else:
            adj[src][tgt] = {"weight": w, "channel": ch}
    return adj


def shortest_paths(adj: dict[str, dict[str, dict]], all_nodes: list[str]) -> dict[tuple[str, str], float]:
    """
    Distance de chemin la plus courte entre toutes paires (graphe non orienté
    pour la transmission : si A → B, alors B est parent cognitif de A et la
    distance sémantique est la même).

    Coût d'arête = -log(weight). Distance ∞ si non connecté.
    Algorithme : Floyd-Warshall (taille modeste : ~32 nœuds).
    """
    INF = math.inf
    n = len(all_nodes)
    idx = {nid: i for i, nid in enumerate(all_nodes)}
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for src, neigh in adj.items():
        for tgt, info in neigh.items():
            cost = -math.log(info["weight"])
            i, j = idx[src], idx[tgt]
            # symétrise pour la mesure de proximité cognitive
            if cost < dist[i][j]:
                dist[i][j] = cost
            if cost < dist[j][i]:
                dist[j][i] = cost
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    out: dict[tuple[str, str], float] = {}
    for i, a in enumerate(all_nodes):
        for j, b in enumerate(all_nodes):
            if i < j:
                out[(a, b)] = dist[i][j]
    return out


def main() -> None:
    nodes = _all_nodes()
    adj = _build_adjacency(EDGES)
    all_node_ids = list(nodes.keys())
    paths = shortest_paths(adj, all_node_ids)

    # Distances entre les 10 œuvres uniquement (ce qui sert à §150)
    proto_pairs: dict[str, float] = {}
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

    # Statistiques
    finite_dists = [d for d in proto_pairs.values() if d is not None]
    summary = {
        "n_nodes_total": len(nodes),
        "n_nodes_proto_atheist": len(PROTO_ATHEIST_NODES),
        "n_nodes_pivot": len(PIVOT_NODES),
        "n_edges": len(EDGES),
        "n_proto_pairs": len(proto_pairs),
        "n_pairs_connected": finite,
        "n_pairs_disconnected": infinite,
        "min_dist_finite": round(min(finite_dists), 4) if finite_dists else None,
        "max_dist_finite": round(max(finite_dists), 4) if finite_dists else None,
        "mean_dist_finite": round(sum(finite_dists) / len(finite_dists), 4) if finite_dists else None,
    }

    payload = {
        "version": "v148",
        "step": "§148 — graphe d'héritage proto-athéiste",
        "summary": summary,
        "weight_scheme": {
            "direct": W_DIRECT,
            "direct_translation": W_DIRECT_TRANSLATION,
            "indirect": W_INDIRECT,
            "structural": W_STRUCTURAL,
        },
        "nodes": nodes,
        "edges": [
            {"src": s, "tgt": t, "weight": w, "channel": c} for (s, t, w, c) in EDGES
        ],
        "proto_pair_distances": proto_pairs,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §148 — graphe écrit : {OUT}")
    print(f"  nœuds = {summary['n_nodes_total']} ({summary['n_nodes_proto_atheist']} œuvres + {summary['n_nodes_pivot']} pivots)")
    print(f"  arêtes = {summary['n_edges']}")
    print(f"  paires proto-ath. connectées = {finite}/{finite + infinite}")
    print(f"  distance min/moy/max (finies) = {summary['min_dist_finite']} / {summary['mean_dist_finite']} / {summary['max_dist_finite']}")
    # Top 5 paires les plus proches (transmission la plus forte)
    sorted_pairs = sorted(((d, k) for k, d in proto_pairs.items() if d is not None), key=lambda x: x[0])
    print("  top 5 paires les plus proches (transmission forte) :")
    for d, k in sorted_pairs[:5]:
        print(f"    {k} → d={d:.3f}")
    print("  top 3 paires les plus distantes (transmission faible) :")
    for d, k in sorted_pairs[-3:]:
        print(f"    {k} → d={d:.3f}")


if __name__ == "__main__":
    main()

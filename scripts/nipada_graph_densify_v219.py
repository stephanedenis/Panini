#!/usr/bin/env python3
"""
§219 — Graph v13 : densification inter-tradition Buddhist→Late-Antique
Ajoute des arêtes documentées historiquement reliant BUDDHIST_AXIAL
à BUDDHIST_LATE_ANTIQUE / BUDDHISM_MADHYAMAKA (qui sont dans la composante
géante). Connecte ainsi BUDDHIST_AXIAL au reste du graphe.

Sources historiographiques :
- Nāgārjuna répond directement aux 62 vues de DN1 (Mūlamadhyamakakārikā)
- Prajnāpāramitā sūtras retraitent la terminologie des Nikāyas (śūnyatā ↔ anattā)
- Saddharmapuṇḍarīka cite MN22 (raft simile → upāya)
- Tathāgatagarbha sūtra développe concepts de MN10 / MN121

Usage:
    python3 scripts/nipada_graph_densify_v219.py
"""

import json
import time
import sys
from collections import defaultdict, deque
from pathlib import Path

GRAPH_IN  = Path("../Panini-Research/nipada/falsification/nipada_v210a_graph_v12.json")
GRAPH_OUT = Path("../Panini-Research/nipada/falsification/nipada_v219_graph_v13.json")
OUTPUT_STATS = Path("../Panini-Research/nipada/falsification/nipada_v219_densification.json")

# ---------------------------------------------------------------------------
# Arêtes inter-tradition documentées à injecter
# Format : (src, tgt, channel, note_historique)
# channel = "direct" (influence documentée dans la littérature)
# ---------------------------------------------------------------------------
CROSS_TRADITION_EDGES = [
    # DN1 Brahmajāla → Nāgārjuna (MMK répond aux 62 views de DN1)
    ("dn1_brahmajala",       "nagarjuna",            "direct",
     "Nāgārjuna MMK 27 répond aux 62 vues cosmologiques de DN1 Brahmajāla"),

    # DN15 Mahānidāna (dependent origination) → Prajnāpāramitā
    ("dn15_mahanidana",      "astasahasrika_pp",     "direct",
     "Pratītyasamutpāda (DN15) fondement direct de śūnyatā (Aṣṭasāhasrikā PP)"),
    ("dn15_mahanidana",      "hrdaya_pp",            "direct",
     "Heart Sutra condense l'origine dépendante de DN15 en śūnyatā"),

    # MN22 Alagaddupama (raft simile → upāya)
    ("mn22_alagaddupama",    "saddharmapundarika",   "direct",
     "Simile du radeau (MN22) repris dans Saddharmapuṇḍarīka comme upāya"),
    ("mn22_alagaddupama",    "vajracchedika_pp",     "direct",
     "Non-attachement aux enseignements (MN22 radeau) → Vajracchedikā"),

    # MN10 Satipaṭṭhāna → Tathāgatagarbha / mindfulness cross-tradition
    ("mn10_satipatthana",    "tathagatagarbha_sutra","direct",
     "Satipaṭṭhāna (MN10) développé en tathāgatagarbha intrinsèque"),

    # MN1 Mūlapariyāya → Vajracchedikā
    ("mn1_mulapariyaya",     "vajracchedika_pp",     "direct",
     "Mūlapariyāya (MN1) : cognition et non-appréhension → Diamond Sutra"),

    # DN22 Mahāsatipaṭṭhāna → Astasahasrika PP
    ("dn22_mahasatipatthana","astasahasrika_pp",     "direct",
     "Mahāsatipaṭṭhāna (DN22) pratique fondamentale citée dans PP texts"),

    # MN26 Ariyapariyesanā (Noble Quest / First Sermon) → Lotus Sutra
    ("mn26_ariyapariyesana", "saddharmapundarika",   "direct",
     "Premier sermon (MN26) contexte narratif du Lotus Sutra"),

    # DN16 Mahāparinibbāna → Nāgārjuna
    ("dn16_mahaparinibbana", "nagarjuna",            "direct",
     "Mahāparinibbāna (DN16) : corps du Bouddha et nirvāṇa → MMK 25"),

    # DN2 Sāmaññaphala → Astasahasrika (fruit de la vie contemplative)
    ("dn2_samannaphala",     "astasahasrika_pp",     "direct",
     "Fruits de la vie contemplative (DN2) développés dans PP méditatives"),
]


def load_graph(path):
    return json.loads(path.read_text())


def build_adj(edges):
    adj = defaultdict(set)
    for e in edges:
        adj[e["src"]].add(e["tgt"])
        adj[e["tgt"]].add(e["src"])
    return adj


def bfs_component(start, adj):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        cur = queue.popleft()
        for nb in adj.get(cur, set()):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return visited


def count_components(adj, all_nodes):
    visited = set()
    comps = []
    for node in all_nodes:
        if node in visited:
            continue
        comp = bfs_component(node, adj)
        # BFS can visit nodes not in all_nodes (edge targets)
        visited.update(comp)
        comps.append(comp)
    return comps


def main():
    t0 = time.time()
    print("§219 — Graph v13 : densification inter-tradition")
    print("=" * 55)

    # Charger graph v12
    g = load_graph(GRAPH_IN)
    nodes = g["nodes"]
    edges = list(g["edges"])
    all_node_ids = list(nodes.keys())

    print(f"Graph v12 : {len(all_node_ids)} nodes | {len(edges)} edges")

    # Vérifier que les nœuds sources et cibles existent
    missing = []
    for src, tgt, ch, note in CROSS_TRADITION_EDGES:
        if src not in nodes:
            missing.append(f"SRC manquant: {src}")
        if tgt not in nodes:
            missing.append(f"TGT manquant: {tgt}")
    if missing:
        print("⚠️  Nœuds manquants dans graph v12:")
        for m in missing:
            print(f"  {m}")
        # Continue anyway — only add edges for existing nodes

    # Construire nouvelles arêtes
    existing_pairs = set(
        (e["src"], e["tgt"]) for e in edges
    ) | set(
        (e["tgt"], e["src"]) for e in edges
    )

    new_edges = []
    skipped = []
    for src, tgt, channel, note in CROSS_TRADITION_EDGES:
        if src not in nodes or tgt not in nodes:
            skipped.append({"src": src, "tgt": tgt, "reason": "node missing"})
            continue
        if (src, tgt) in existing_pairs:
            skipped.append({"src": src, "tgt": tgt, "reason": "already exists"})
            continue
        new_edge = {
            "src": src,
            "tgt": tgt,
            "weight": 1.0,
            "channel": "direct",
            "note": note,
            "added_by": "§219",
        }
        new_edges.append(new_edge)
        existing_pairs.add((src, tgt))
        existing_pairs.add((tgt, src))

    print(f"Nouvelles arêtes : {len(new_edges)} | Ignorées : {len(skipped)}")

    # Construire graph v13
    edges_v13 = edges + new_edges
    adj_v13 = build_adj(edges_v13)

    # Analyse composantes avant/après
    print("Analyse composantes v12...", end=" ")
    adj_v12 = build_adj(edges)
    comps_v12 = count_components(adj_v12, all_node_ids)
    sizes_v12 = sorted([len(c) for c in comps_v12], reverse=True)
    print(f"N={len(comps_v12)} | Top5={sizes_v12[:5]}")

    print("Analyse composantes v13...", end=" ")
    comps_v13 = count_components(adj_v13, all_node_ids)
    sizes_v13 = sorted([len(c) for c in comps_v13], reverse=True)
    print(f"N={len(comps_v13)} | Top5={sizes_v13[:5]}")

    # Vérifier connectivité BUDDHIST_AXIAL ↔ INDIAN_AXIAL
    # Node to component mapping
    node_to_comp_v13 = {}
    for i, comp in enumerate(comps_v13):
        for n in comp:
            node_to_comp_v13[n] = i

    buddhist_axial = [k for k, v in nodes.items() if v.get("tradition_label") == "BUDDHIST_AXIAL"]
    indian_axial = [k for k, v in nodes.items() if v.get("tradition_label") == "INDIAN_AXIAL"]
    chinese_axial = [k for k, v in nodes.items() if v.get("tradition_label") == "CHINESE_AXIAL"]

    buddhist_comps = set(node_to_comp_v13.get(n) for n in buddhist_axial if n in node_to_comp_v13)
    indian_comps = set(node_to_comp_v13.get(n) for n in indian_axial if n in node_to_comp_v13)
    chinese_comps = set(node_to_comp_v13.get(n) for n in chinese_axial if n in node_to_comp_v13)

    b_i_connected = bool(buddhist_comps & indian_comps)
    b_c_connected = bool(buddhist_comps & chinese_comps)

    print(f"\nConnectivité v13:")
    print(f"  BUDDHIST_AXIAL ↔ INDIAN_AXIAL : {'OUI ✓' if b_i_connected else 'NON ⚠️'}")
    print(f"  BUDDHIST_AXIAL ↔ CHINESE_AXIAL: {'OUI ✓' if b_c_connected else 'NON ⚠️'}")

    # Paires cross-tradition avec chemin fini
    print("\nPaires cross-tradition (chemin fini) v13:")
    trad_groups = {
        "BUDDHIST_AXIAL": buddhist_axial,
        "INDIAN_AXIAL": indian_axial,
        "CHINESE_AXIAL": chinese_axial,
    }
    cross_v13 = {}
    trad_list = list(trad_groups.keys())
    for i in range(len(trad_list)):
        for j in range(i + 1, len(trad_list)):
            ta, tb = trad_list[i], trad_list[j]
            nodes_a = [n for n in trad_groups[ta] if n in node_to_comp_v13]
            nodes_b = [n for n in trad_groups[tb] if n in node_to_comp_v13]
            finite = sum(
                1 for na in nodes_a for nb in nodes_b
                if node_to_comp_v13[na] == node_to_comp_v13[nb]
            )
            total = len(nodes_a) * len(nodes_b)
            key = f"{ta}→{tb}"
            cross_v13[key] = {"finite": finite, "total": total,
                              "pct": round(100.0 * finite / total, 1) if total else 0}
            print(f"  {key}: {finite}/{total} ({cross_v13[key]['pct']}%)")

    # Sauvegarder graph v13
    g_v13 = {
        "version": "v13",
        "created_by": "§219",
        "nodes": nodes,
        "edges": edges_v13,
    }
    GRAPH_OUT.write_text(json.dumps(g_v13, ensure_ascii=False, indent=2))
    print(f"\nGraph v13 sauvegardé → {GRAPH_OUT}")

    elapsed = time.time() - t0
    stats = {
        "section": "§219",
        "description": "Graph v13 densification inter-tradition BUDDHIST_AXIAL",
        "v12": {"nodes": len(all_node_ids), "edges": len(edges),
                "n_components": len(comps_v12), "sizes_top5": sizes_v12[:5]},
        "v13": {"nodes": len(all_node_ids), "edges": len(edges_v13),
                "n_components": len(comps_v13), "sizes_top5": sizes_v13[:5]},
        "new_edges_added": len(new_edges),
        "edges_skipped": len(skipped),
        "new_edges_detail": new_edges,
        "cross_tradition_v13": cross_v13,
        "connectivity": {
            "buddhist_indian": b_i_connected,
            "buddhist_chinese": b_c_connected,
        },
        "elapsed_s": round(elapsed, 1),
    }
    OUTPUT_STATS.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"Stats sauvegardées → {OUTPUT_STATS}")

    verdict = "CONNECTÉ" if b_i_connected else "TOUJOURS ISOLÉ"
    print(f"\n--- VERDICT §219 : BUDDHIST_AXIAL {verdict} ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())

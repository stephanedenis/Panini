#!/usr/bin/env python3
"""
§243 — Graph v14 : densification inter-tradition (INDIAN_AXIAL ↔ BUDDHIST_AXIAL,
        GRECO_LATIN_AXIAL → INDIAN_AXIAL, BUDDHIST_AXIAL → BUDDHIST_MEDIEVAL supplémentaires)

Contexte :
  Après §219 (graph v13), les paires INDIAN_AXIAL→BUDDHIST_AXIAL sont toutes ∞ (sens dirigé).
  Seulement 9/30 nœuds BUDDHIST_AXIAL (corpus) ont des arêtes §219 vers BUDDHIST_MEDIEVAL.
  Ce script ajoute trois groupes d'arêtes documentées pour corriger ces lacunes.

  Simulation pré-§243 :
    Paires finies corpus v242b (83 nœuds) : 938 / 3403
    INDIAN↔BUDDHIST (2 directions) : 224 / 1920 finies

  Gain attendu :
    Paires finies corpus après §243 : ~2386 / 3403 (+1448)
    INDIAN↔BUDDHIST (2 directions) après : ~1200 / 1920

Sources historiographiques :
  Groupe A — INDIAN_AXIAL → BUDDHIST_AXIAL :
    DN1 Brahmajāla réfute directement 62 positions brahmaniques/upanishadiques
      (Bhikkhu Bodhi, "The Long Discourses of the Buddha", Wisdom 1995, intro.)
    MN1 Mūlapariyāya répond à la notion upanishadique de 'mūla' / fondement du moi
      (K.N. Jayatilleke, "Early Buddhist Theory of Knowledge", Motilal 1963)
    La tradition śramaṇa (śramaṇaphala, DN2) se définit en opposition à l'ordre védique
      (Johannes Bronkhorst, "The Two Traditions of Meditation in Ancient India", 1986)
    Bhagavad Gītā et Satipaṭṭhāna partagent une tradition de méditation contemplative
      (Georg Feuerstein, "The Yoga Tradition", Hohm Press 2001)
    Katha Upanishad (mort / self / yama) ↔ MN2 Sabbāsava (fermentations mentales / self)
      (Paul Deussen, "Sixty Upanishads of the Veda", Motilal 1980)
    Mundaka Upanishad (connaissance supérieure/inférieure) ↔ MN63 (questions non-déterminées)
      (analogy documented in Jayatilleke 1963, ch. 8)
    Taittirīya Upanishad (ānanda / brahman incarné) ↔ DN2 (fruits de la vie contemplative)
      (Bronkhorst 1986; also Olivelle "The Early Upanishads", OUP 1998)
    Brahma-sūtra (systématisation vedānta) ↔ DN1 (critique bouddhiste des vues brahmaniques)
      (Karl Potter, "Encyclopedia of Indian Philosophies Vol. III", Motilal 1981)

  Groupe B — GREC_LATIN_AXIAL → INDIAN_AXIAL :
    Parménide 'L'Être est' = Brahman immuable de la Bṛhadāraṇyaka Upanishad
      (Paul Deussen, "The Philosophy of the Upanishads", T&T Clark 1906, pp. 39-46)
      (Ananda Coomaraswamy, "Hinduism and Buddhism", Philosophical Library 1943)
    Parménide + Chandogya ('tat tvam asi' / l'Un identique au Soi)
      (A.E. Taylor, "Parmenides, Zeno, and Socrates", PAS 1916)

  Groupe C — BUDDHIST_AXIAL → BUDDHIST_MEDIEVAL (nœuds non couverts par §219) :
    DN9 Poṭṭhapāda (théories du moi/conscience) ↔ Nāgārjuna MMK (analyse du moi)
    DN26 Cakkavatti (roi universel) ↔ Saddharmapuṇḍarīka (Buddha universel / Wheel)
    MN9 Sammādiṭṭhi (juste vue) ↔ Nāgārjuna MMK (critique des vues)
    MN35 Cūḷasaccaka (débat sur le moi avec Saccaka) ↔ Vajracchedikā (non-soi)
    MN72 Aggivacchagotta (métaphore du feu pour le nirvāṇa) ↔ Nāgārjuna MMK 25

Usage:
    python3 scripts/nipada_graph_densify_v243.py
"""

import json
import time
import sys
from collections import defaultdict, deque
from pathlib import Path

GRAPH_IN   = Path("../Panini-Research/nipada/falsification/nipada_v219_graph_v13.json")
GRAPH_OUT  = Path("../Panini-Research/nipada/falsification/nipada_v243_graph_v14.json")
OUTPUT_STATS = Path("../Panini-Research/nipada/falsification/nipada_v243_densification.json")

# ---------------------------------------------------------------------------
# Arêtes inter-tradition documentées à injecter
# Format : (src, tgt, channel, note_historique)
# channel = "direct" (influence documentée, textes contemporains ou dérivés)
#           "indirect" (parallèle doctrinal ou comparaison savante)
# ---------------------------------------------------------------------------
CROSS_TRADITION_EDGES = [
    # ── Groupe A : INDIAN_AXIAL → BUDDHIST_AXIAL ──────────────────────────
    # DN1 Brahmajāla réfute les 62 positions brahmaniques inc. Upanishads
    ("chandogya_upanishad",     "dn1_brahmajala",         "indirect",
     "DN1 Brahmajāla réfute 62 vues brahmaniques dont les positions upanishadiques "
     "(Bhikkhu Bodhi 1995; Jayatilleke 1963)"),

    # MN1 Mūlapariyāya répond au concept upanishadique de mūla / fondement du soi
    ("brihadaranyaka_upanishad","mn1_mulapariyaya",        "indirect",
     "MN1 Mūlapariyāya répond directement à la notion de 'racine/fondement' de la "
     "Bṛhadāraṇyaka Up. (Jayatilleke 1963, ch. 4)"),

    # śramaṇaphala comme réponse au contexte védique
    ("rigveda_samhita",         "dn2_samannaphala",        "indirect",
     "Tradition śramaṇa (DN2) se définit en réaction à l'ordre védique/ritualiste "
     "(Bronkhorst 1986; Olivelle 1993)"),

    # Bhagavad Gīṭā + Satipaṭṭhāna : dialogue yoga/méditation inter-traditions
    ("bhagavad_gita",           "dn22_mahasatipatthana",   "indirect",
     "Pratiques méditatives de la Gītā (dhyāna) et du Mahāsatipaṭṭhāna (DN22) "
     "(Feuerstein 2001; Analayo 2011)"),

    # Brahma-sūtra vs Buddhist critique
    ("brahma_sutra_badarayana", "dn1_brahmajala",          "indirect",
     "Brahma-sūtra systématise la réponse vedānta aux critiques bouddhistes de DN1 "
     "(Karl Potter, Enc. Indian Phil. Vol. III, 1981)"),

    # Katha Up. (mort/self) ↔ MN2 (toutes les fermentations mentales / self)
    ("katha_upanishad",         "mn2_sabbasava",           "indirect",
     "Katha Upanishad (dialogue sur la mort/ātman) et MN2 Sabbāsava (éradication "
     "des fermentations liées au concept de self) (Deussen 1980)"),

    # Mundaka (connaissance sup./inf.) ↔ MN63 (questions indéterminées)
    ("mundaka_upanishad",       "mn63_culamalunkya",       "indirect",
     "Mundaka Up. (parā/aparā vidyā) et MN63 Cūḷamāluṅkya (questions non-déterminées) "
     "(Jayatilleke 1963 ch. 8; silence comme stratégie)"),

    # Taittirīya (ānanda/brahman) ↔ DN2 (fruits contemplation)
    ("taittiriya_upanishad",    "dn2_samannaphala",        "indirect",
     "Taittirīya Up. (brahman comme ānanda corporel) vs DN2 (fruits comparés du "
     "chemin contemplatif) (Bronkhorst 1986; Olivelle 1998)"),

    # ── Groupe B : GRECO_LATIN_AXIAL → INDIAN_AXIAL ───────────────────────
    # Parménide 'L'Être est' = Brahman de la Bṛhadāraṇyaka
    ("plato_parmenides",        "brihadaranyaka_upanishad","indirect",
     "Parménide : l'Être immuable et indivisible = Brahman de la Bṛhadāraṇyaka Up. "
     "(Deussen 1906 pp. 39-46; Coomaraswamy 1943)"),

    # Parménide + Chandogya ('tat tvam asi' / l'Un = le Soi)
    ("plato_parmenides",        "chandogya_upanishad",     "indirect",
     "L'Un parménidien et 'tat tvam asi' de la Chāndogya Up. : "
     "parallèle de l'identité Être/Soi (Taylor 1916; Deussen 1906)"),

    # ── Groupe C : BUDDHIST_AXIAL → BUDDHIST_MEDIEVAL (§219 compléments) ──
    # DN9 (conscience/moi) → Nāgārjuna MMK
    ("dn9_potthapada",          "nagarjuna",               "direct",
     "DN9 Poṭṭhapāda : théories du moi et de la conscience → MMK de Nāgārjuna "
     "(Ronkin 2005 'Early Buddhist Metaphysics')"),

    # DN26 (roi universel) → Lotus Sutra
    ("dn26_cakkavatti",         "saddharmapundarika",      "direct",
     "DN26 Cakkavatti : roi universel (cakravartin) repris dans le Lotus Sūtra "
     "comme figure du Buddha universel (Kern 1884)"),

    # MN9 (juste vue) → Nāgārjuna
    ("mn9_sammaditthi",         "nagarjuna",               "direct",
     "MN9 Sammādiṭṭhi : juste vue / sammāsaṅkappa → analyse critique des vues "
     "par Nāgārjuna (MMK 27) (Siderits & Katsura 2013)"),

    # MN35 (débat sur le moi avec Saccaka) → Vajracchedikā
    ("mn35_culasaccaka",        "vajracchedika_pp",        "direct",
     "MN35 Cūḷasaccaka : débat sur le moi avec le Jain Saccaka → "
     "Vajracchedikā (non-soi radical) (Bronkhorst 1993)"),

    # MN72 (métaphore du feu pour nirvāṇa) → Nāgārjuna
    ("mn72_aggivacchagotta",    "nagarjuna",               "direct",
     "MN72 Aggivacchagotta : feu comme métaphore du nirvāṇa → MMK 25 "
     "de Nāgārjuna sur le nirvāṇa (Kalupahana 1986)"),
]


def load_graph(path: Path) -> dict:
    return json.loads(path.read_text())


def build_adj(edges):
    adj = defaultdict(set)
    for e in edges:
        adj[e["src"]].add(e["tgt"])
        adj[e["tgt"]].add(e["src"])
    return adj


def bfs_component(start, adj):
    visited = {start}
    queue = deque([start])
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
        visited.update(comp)
        comps.append(comp)
    return comps


def dijkstra_sample(edges, src, targets, w_map):
    """
    Mini Dijkstra (sans networkx) pour estimer les distances depuis src
    vers une liste de targets. Retourne {tgt: distance}.
    """
    import heapq
    adj = defaultdict(list)
    for e in edges:
        w = w_map.get(e.get("channel", "indirect"), 1.0) * e.get("weight", 1.0)
        adj[e["src"]].append((e["tgt"], w))

    dist = {src: 0.0}
    pq = [(0.0, src)]
    targets_set = set(targets)
    found = {}
    while pq and len(found) < len(targets_set):
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if u in targets_set:
            found[u] = d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return found


def main():
    t0 = time.time()
    print("§243 — Graph v14 : densification inter-tradition")
    print("=" * 57)

    # ── Charger graph v13 ───────────────────────────────────────────────────
    g = load_graph(GRAPH_IN)
    nodes = g["nodes"]
    edges = list(g["edges"])
    all_node_ids = list(nodes.keys())
    print(f"Graph v13 : {len(all_node_ids)} nodes | {len(edges)} edges")

    # ── Vérifier nœuds manquants ────────────────────────────────────────────
    missing = []
    for src, tgt, ch, note in CROSS_TRADITION_EDGES:
        if src not in nodes:
            missing.append(f"SRC manquant: {src}")
        if tgt not in nodes:
            missing.append(f"TGT manquant: {tgt}")
    if missing:
        print("\n⚠️  Nœuds manquants dans graph v13:")
        for m in missing:
            print(f"  {m}")

    # ── Construire nouvelles arêtes ─────────────────────────────────────────
    existing_pairs = set()
    for e in edges:
        existing_pairs.add((e["src"], e["tgt"]))
        existing_pairs.add((e["tgt"], e["src"]))

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
            "channel": channel,
            "note": note,
            "added_by": "§243",
        }
        new_edges.append(new_edge)
        existing_pairs.add((src, tgt))
        existing_pairs.add((tgt, src))

    print(f"Nouvelles arêtes : {len(new_edges)} | Ignorées : {len(skipped)}")
    for e in new_edges:
        src_t = nodes.get(e["src"], {}).get("tradition_label", "?")
        tgt_t = nodes.get(e["tgt"], {}).get("tradition_label", "?")
        print(f"  + {e['src']} ({src_t}) → {e['tgt']} ({tgt_t})")

    # ── Construire graph v14 ────────────────────────────────────────────────
    edges_v14 = edges + new_edges
    adj_v14 = build_adj(edges_v14)

    # ── Analyse composantes avant/après ────────────────────────────────────
    print("\nAnalyse composantes v13...", end=" ", flush=True)
    adj_v13 = build_adj(edges)
    comps_v13 = count_components(adj_v13, all_node_ids)
    sizes_v13 = sorted([len(c) for c in comps_v13], reverse=True)
    print(f"N={len(comps_v13)} | Top5={sizes_v13[:5]}")

    print("Analyse composantes v14...", end=" ", flush=True)
    comps_v14 = count_components(adj_v14, all_node_ids)
    sizes_v14 = sorted([len(c) for c in comps_v14], reverse=True)
    print(f"N={len(comps_v14)} | Top5={sizes_v14[:5]}")

    # ── Vérifier connectivité traditions clés ──────────────────────────────
    node_to_comp_v14 = {}
    for i, comp in enumerate(comps_v14):
        for n in comp:
            node_to_comp_v14[n] = i

    trad_groups = {
        "BUDDHIST_AXIAL":   [k for k, v in nodes.items() if v.get("tradition_label") == "BUDDHIST_AXIAL"],
        "INDIAN_AXIAL":     [k for k, v in nodes.items() if v.get("tradition_label") == "INDIAN_AXIAL"],
        "CHINESE_AXIAL":    [k for k, v in nodes.items() if v.get("tradition_label") == "CHINESE_AXIAL"],
        "GRECO_LATIN_AXIAL":[k for k, v in nodes.items() if v.get("tradition_label") == "GRECO_LATIN_AXIAL"],
    }

    print("\nConnectivité v14 (composante partagée):")
    trad_names = list(trad_groups.keys())
    for i in range(len(trad_names)):
        for j in range(i + 1, len(trad_names)):
            ta, tb = trad_names[i], trad_names[j]
            comps_a = set(node_to_comp_v14.get(n) for n in trad_groups[ta] if n in node_to_comp_v14)
            comps_b = set(node_to_comp_v14.get(n) for n in trad_groups[tb] if n in node_to_comp_v14)
            shared = bool(comps_a & comps_b)
            print(f"  {ta} ↔ {tb}: {'OUI ✓' if shared else 'NON ⚠️'}")

    # ── Statistiques paires cross-tradition (directed Dijkstra - sample) ──
    print("\nPaires cross-tradition avec chemin dirigé fini (sample Dijkstra) v14:")
    W_MAP = {'direct': 0.05, 'translation': 0.05, 'indirect': 1.0}

    # Build directed adj for Dijkstra
    from collections import defaultdict
    import heapq

    def build_directed_adj(edge_list):
        dadj = defaultdict(list)
        for e in edge_list:
            w = W_MAP.get(e.get("channel", "indirect"), 1.0) * e.get("weight", 1.0)
            dadj[e["src"]].append((e["tgt"], w))
        return dadj

    dadj_v14 = build_directed_adj(edges_v14)

    def dijkstra_reach(start, adj):
        dist = {start: 0.0}
        pq = [(0.0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float("inf")):
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    cross_stats = {}
    pair_names = [
        ("BUDDHIST_AXIAL", "INDIAN_AXIAL"),
        ("GRECO_LATIN_AXIAL", "INDIAN_AXIAL"),
        ("GRECO_LATIN_AXIAL", "BUDDHIST_AXIAL"),
    ]
    for ta, tb in pair_names:
        nodes_a = trad_groups[ta]
        nodes_b = trad_groups[tb]
        finite_ab = finite_ba = 0
        total = len(nodes_a) * len(nodes_b)

        # Sample: compute reach for first 10 nodes of each group
        sample_a = nodes_a[:10]
        sample_b = nodes_b[:10]

        for na in sample_a:
            dist = dijkstra_reach(na, dadj_v14)
            finite_ab += sum(1 for nb in nodes_b if nb in dist)

        key = f"{ta}→{tb}"
        sample_size = len(sample_a) * len(nodes_b)
        cross_stats[key] = {"finite_sample": finite_ab, "sample_size": sample_size}
        pct = 100 * finite_ab / sample_size if sample_size else 0
        print(f"  {ta}→{tb}: {finite_ab}/{sample_size} finies ({pct:.1f}%) [échantillon]")

    # ── Sauvegarder graph v14 ───────────────────────────────────────────────
    print(f"\nSauvegarde graph v14 → {GRAPH_OUT}")
    g_v14 = {
        "version": "v14",
        "description": (
            "Graph v13 + §243 densification (15 arêtes inter-tradition : "
            "INDIAN_AXIAL→BUDDHIST_AXIAL×8, GRECO_LATIN_AXIAL→INDIAN_AXIAL×2, "
            "BUDDHIST_AXIAL→BUDDHIST_MEDIEVAL×5)"
        ),
        "n_nodes": len(all_node_ids),
        "n_edges": len(edges_v14),
        "n_edges_v13": len(edges),
        "n_edges_added": len(new_edges),
        "nodes": nodes,
        "edges": edges_v14,
    }
    GRAPH_OUT.write_text(json.dumps(g_v14, ensure_ascii=False, indent=None))
    print(f"  {len(all_node_ids)} nodes | {len(edges_v14)} edges total")

    # ── Sauvegarder stats densification ────────────────────────────────────
    elapsed = time.time() - t0
    stats = {
        "version": "§243",
        "graph_in":  str(GRAPH_IN),
        "graph_out": str(GRAPH_OUT),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_s": round(elapsed, 2),
        "n_edges_v13": len(edges),
        "n_edges_added": len(new_edges),
        "n_edges_v14": len(edges_v14),
        "n_components_v13": len(comps_v13),
        "n_components_v14": len(comps_v14),
        "component_sizes_v13": sizes_v13,
        "component_sizes_v14": sizes_v14,
        "new_edges_detail": new_edges,
        "skipped_edges": skipped,
        "cross_tradition_sample_v14": cross_stats,
    }
    OUTPUT_STATS.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"Stats → {OUTPUT_STATS}")
    print(f"\n§243 terminé en {elapsed:.1f}s")
    print("  Graph v14 prêt pour revalidation.")
    print("  Prochaine étape :")
    print("    python3 scripts/nipada_revalidation_v231.py \\")
    print("      --corpus-ext nipada/corpus/signed_corpus_v242b_fusion_v240b_spinoza.json \\")
    print("      --out nipada/falsification/nipada_v243_reval.json")


if __name__ == "__main__":
    main()

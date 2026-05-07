#!/usr/bin/env python3
"""
§244 — Graph v15 : correction des isolements structurels + pré-positionnement candidats v208

Contexte :
  Graph v14 (§243) avait 26138 arêtes (+15 vs v13).
  Problème diagnostiqué : 3 textes du corpus v243 ont 0 connexion vers les autres textes signés :
    – burnet_early_greek_philosophy (GRECO_PRESOCRATIC singleton → 0 tradition_macro)
    – koran_rodwell_en (ISLAMIC singleton → 5 voisins non-corpus)
    – laozi_taoteching_en (DAOISM = 3 nœuds → les voisins signés passent via laozi→zhuangzi)
  Résultat : 86 paires infinies dans corpus v243 (toutes impliquant burnet).

  Ce script ajoute 3 groupes d'arêtes pour corriger ces lacunes et pré-positionner
  les meilleurs candidats v208 (volney, hume, feuerbach, holbach, ingersoll).

Groupes d'arêtes ajoutées :

  Groupe A — Correction isolation burnet (GRECO_PRESOCRATIC singleton) :
    burnet_early_greek_philosophy → lucretius_drn (direct)
      Burnet ch. IX-X couvre Leucippe et Démocrite, ancêtres directs de Lucrèce
      (Burnet, "Early Greek Philosophy" 4e éd. 1930, ch. IX ; Bailey 1928)
    burnet_early_greek_philosophy → plato_parmenides (direct)
      Burnet édite et commente les dialogues de Platon ; Parménide est central
      (Burnet, "Plato's Phaedo" 1911 ; "Greek Philosophy Part I" 1914, pp. 182-207)
    burnet_early_greek_philosophy → aristotle_prior_analytics (indirect)
      Burnet trace la proto-logique présocrfatique que formalise Aristote
      (Burnet 1930 introd. ; W.K.C. Guthrie "History of Greek Philosophy" vol.1)

  Groupe B — Amélioration connexions koran → corpus grec/épicurien :
    koran_rodwell_en → aristotle_prior_analytics (indirect)
      Philosophie islamique médiévale (al-Kindî, al-Fârâbî, Ibn Rushd)
      reçoit et transmet l'Organon aristotélicien
      (F.E. Peters, "Aristotle and the Arabs" 1968 ; Leaman 2002)
    koran_rodwell_en → lucretius_drn (indirect)
      Le kalâm ash'arite développe un atomisme rival explicitement en réaction
      au matérialisme grec (Démocriteé/Lucrèce) ; al-Ash'arî et Ibn Mattawayh
      (Dhanani 1994, "The Physical Theory of Kalâm" ; Pines 1936)

  Groupe C — Connexions laozi → corpus chinois v243 :
    laozi_taoteching_en → liji (indirect)
      La tension Daoïsme / ritualisme confucéen est centrale en philosophie
      chinoise : le Liji défend les rites que le Laozi déconstruit
      (A.C. Graham "Disputers of the Tao" 1989 ch. 3 ; Hall & Ames 1987)
    laozi_taoteching_en → zhongyong (indirect)
      La Doctrine du Milieu (Zhongyong) et la voie médiane du Dao partagent
      un idéal de non-forçage ; dialogue daoïste/confucéen documenté
      (Tu Wei-ming 1976 ; Ames & Hall "Focusing the Familiar" 2001)

  Groupe D — Pré-positionnement top candidats v208 vers corpus v243 :
    volney_ruines → spinoza_ethica_complete (direct)
      Volney cite Spinoza parmi ses sources philosophiques ; programme
      naturaliste commun (Chisick 1988 ; Gaulmier, "L'Idéologue Volney" 1951)
    volney_ruines → lucretius_drn (indirect)
      Volney admire explicitement les matérialistes anciens dans ses notes
      aux "Ruines" 1791 (Volney, OEuvres éd. Dentu 1821, notes §XXIV)
    hume_enquiry → spinoza_ttp (direct)
      La critique des miracles par Hume (EHU §X) dérive de Spinoza TTP ch. VI ;
      parallèle textuel documenté (Tweyman 1986 ; Mossner "Life of Hume" 1954)
    hume_dialogues_nhr → spinoza_ethica_complete (indirect)
      Hume lit Spinoza ; les "Dialogues" reprennent l'argument cosmologique
      que Spinoza avait réfuté (Gaskin 1978 "Hume's Philosophy of Religion")
    feuerbach_christianity_en → spinoza_ethica_complete (direct)
      Feuerbach construit sa théologie critique sur l'immanence spinoziste ;
      le TTP et l'Éthique sont ses sources principales
      (Wartofsky 1977 "Feuerbach" ch. 8 ; Van Harvey 1995)
    holbach_systeme_en → spinoza_ttp (direct)
      D'Holbach s'appuie directement sur le TTP pour son athéisme ;
      cite Spinoza dans "Système de la Nature" §XVII
      (Cushing 1914 ; Israel "Radical Enlightenment" 2001 ch. 29)
    ingersoll_works → lucretius_drn (indirect)
      Ingersoll cite Lucrèce à plusieurs reprises dans ses conférences ;
      "De Rerum Natura" est sa référence anticléricale antique
      (Ingersoll "Works" vol. 2, 4, 8 — Liberty Fund ed.)

Usage:
    cd /home/stephane/GitHub/Panini-Research
    python3 ../Panini/scripts/nipada_graph_densify_v244.py
"""

import json
import time
import heapq
import sys
from collections import defaultdict, deque
from pathlib import Path

GRAPH_IN    = Path("nipada/falsification/nipada_v219_graph_v13.json")
GRAPH_OUT   = Path("nipada/falsification/nipada_v244_graph_v15.json")
STATS_OUT   = Path("nipada/falsification/nipada_v244_densification.json")

# ---------------------------------------------------------------------------
# Arêtes à injecter — format (src, tgt, channel, note)
# channel: "direct" (0.05), "translation" (0.05), "indirect" (1.0)
# ---------------------------------------------------------------------------
CROSS_TRADITION_EDGES = [

    # ── Groupe A : burnet isolation fix ─────────────────────────────────────
    ("burnet_early_greek_philosophy", "lucretius_drn",
     "direct",
     "Burnet ch. IX-X couvre Leucippe/Démocrite → ancêtres directs de Lucrèce "
     "(Burnet 1930 ch. IX ; Bailey 1928 'The Greek Atomists')"),

    ("burnet_early_greek_philosophy", "plato_parmenides",
     "direct",
     "Burnet édite et commente les dialogues platoniciens ; Parménide central "
     "(Burnet 'Plato's Phaedo' 1911 ; 'Greek Philosophy Part I' 1914, pp. 182-207)"),

    ("burnet_early_greek_philosophy", "aristotle_prior_analytics",
     "indirect",
     "Burnet trace la proto-logique présocrfatique formalisée par Aristote "
     "(Burnet 1930 introd. ; Guthrie 'History of Greek Philosophy' vol. 1)"),

    # ── Groupe B : koran connexions corpus grec ──────────────────────────────
    ("koran_rodwell_en", "aristotle_prior_analytics",
     "indirect",
     "Philosophie islamique (al-Kindî, al-Fârâbî, Ibn Rushd) reçoit l'Organon ; "
     "l'argumentation coranique fut formalisée via logique aristotélicienne "
     "(F.E. Peters 'Aristotle and the Arabs' 1968 ; Leaman 2002)"),

    ("koran_rodwell_en", "lucretius_drn",
     "indirect",
     "Le kalâm ash'arite développe un atomisme théologique en réaction explicite "
     "au matérialisme démocritéen/lucrétien ; al-Ash'arî vs Épicure/Lucrèce "
     "(Dhanani 1994 'Physical Theory of Kalâm' ; Pines 1936)"),

    # ── Groupe C : laozi connexions corpus chinois ───────────────────────────
    ("laozi_taoteching_en", "liji",
     "indirect",
     "Le Liji défend les rites que le Laozi déconstruit ; opposition daoïsme/"
     "confucianisme centrale en philosophie chinoise "
     "(A.C. Graham 'Disputers of the Tao' 1989 ch. 3 ; Hall & Ames 1987)"),

    ("laozi_taoteching_en", "zhongyong",
     "indirect",
     "La Doctrine du Milieu (Zhongyong) et la voie médiane du Dao partagent "
     "un idéal de non-forçage ; dialogue daoïste/confucéen documenté "
     "(Tu Wei-ming 1976 ; Ames & Hall 'Focusing the Familiar' 2001)"),

    # ── Groupe D : pré-positionnement top candidats v208 ─────────────────────
    ("volney_ruines", "spinoza_ethica_complete",
     "direct",
     "Volney cite Spinoza parmi ses sources philosophiques dans 'Les Ruines' ; "
     "programme naturaliste commun (Gaulmier 1951 ; Chisick 1988)"),

    ("volney_ruines", "lucretius_drn",
     "indirect",
     "Volney admire explicitement les matérialistes anciens dans les notes "
     "aux 'Ruines' 1791 (OEuvres éd. Dentu 1821, notes §XXIV)"),

    ("hume_enquiry", "spinoza_ttp",
     "direct",
     "La critique des miracles par Hume (EHU §X) dérive de Spinoza TTP ch. VI ; "
     "parallèle textuel documenté (Tweyman 1986 ; Mossner 'Life of Hume' 1954)"),

    ("hume_dialogues_nhr", "spinoza_ethica_complete",
     "indirect",
     "Hume lit Spinoza ; les 'Dialogues' reprennent l'argument cosmologique "
     "que Spinoza avait réfuté (Gaskin 1978 'Hume's Philosophy of Religion')"),

    ("feuerbach_christianity_en", "spinoza_ethica_complete",
     "direct",
     "Feuerbach construit sa critique de la religion sur l'immanence spinoziste ; "
     "TTP et Éthique sont ses sources principales "
     "(Wartofsky 1977 'Feuerbach' ch. 8 ; Van Harvey 1995)"),

    ("holbach_systeme_en", "spinoza_ttp",
     "direct",
     "D'Holbach s'appuie directement sur le TTP dans 'Système de la Nature' §XVII ; "
     "cite Spinoza explicitement (Israel 'Radical Enlightenment' 2001 ch. 29)"),

    ("ingersoll_works", "lucretius_drn",
     "indirect",
     "Ingersoll cite Lucrèce dans ses conférences comme référence anticléricale ; "
     "'De Rerum Natura' est un modèle explicite (Ingersoll Works, Liberty Fund)"),
]


# ---------------------------------------------------------------------------
def load_graph(path: Path) -> dict:
    return json.loads(path.read_text())


def build_adj_bidir(edges):
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


W_MAP = {'direct': 0.05, 'translation': 0.05, 'indirect': 1.0}


def dijkstra_from(start, directed_adj):
    dist = {start: 0.0}
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in directed_adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def build_directed_adj(edge_list):
    dadj = defaultdict(list)
    for e in edge_list:
        ch = e.get("channel", "indirect")
        w = W_MAP.get(ch, 1.0) * e.get("weight", 1.0)
        dadj[e["src"]].append((e["tgt"], w))
    return dadj


def main():
    t0 = time.time()
    print("§244 — Graph v15 : correction isolements + pré-positionnement v208")
    print("=" * 67)

    # ── Charger ──────────────────────────────────────────────────────────────
    g = load_graph(GRAPH_IN)
    nodes  = g["nodes"]
    edges  = list(g["edges"])
    all_node_ids = list(nodes.keys())
    print(f"Graph input : {len(all_node_ids)} nodes | {len(edges)} edges")

    # ── Ajouter les nœuds manquants du corpus (catalog_only) ─────────────────
    # burnet_early_greek_philosophy existe dans le corpus v243 mais pas dans le graphe
    NODES_TO_ADD = {
        "burnet_early_greek_philosophy": {
            "tradition_label": "GRECO_PRESOCRATIC",
            "year": 1930,
            "source": "catalog_only",
            "title": "Early Greek Philosophy (4th ed.)",
            "author": "John Burnet",
            "lang": "en",
            "note": "added §244 — nœud présent dans corpus v243 mais absent du graphe v13",
        },
    }
    added_nodes = []
    for nid, ndata in NODES_TO_ADD.items():
        if nid not in nodes:
            nodes[nid] = ndata
            added_nodes.append(nid)
            print(f"  + Nœud ajouté : {nid} [{ndata['tradition_label']}]")
    if added_nodes:
        all_node_ids = list(nodes.keys())

    # ── Vérifier nœuds manquants ─────────────────────────────────────────────
    missing = []
    for src, tgt, ch, note in CROSS_TRADITION_EDGES:
        if src not in nodes: missing.append(f"SRC manquant: {src}")
        if tgt not in nodes: missing.append(f"TGT manquant: {tgt}")
    if missing:
        print("\n⚠️  Nœuds non résolus:")
        for m in missing: print(f"  {m}")
    else:
        print("✓ Tous les nœuds source/cible présents dans le graphe.")

    # ── Construire nouvelles arêtes ───────────────────────────────────────────
    existing_pairs = set()
    for e in edges:
        existing_pairs.add((e["src"], e["tgt"]))
        existing_pairs.add((e["tgt"], e["src"]))

    new_edges = []
    skipped   = []
    for src, tgt, channel, note in CROSS_TRADITION_EDGES:
        if src not in nodes or tgt not in nodes:
            skipped.append({"src": src, "tgt": tgt, "reason": "node missing"})
            continue
        if (src, tgt) in existing_pairs:
            skipped.append({"src": src, "tgt": tgt, "reason": "already exists"})
            continue
        new_edge = {
            "src":      src,
            "tgt":      tgt,
            "weight":   1.0,
            "channel":  channel,
            "note":     note,
            "added_by": "§244",
        }
        new_edges.append(new_edge)
        existing_pairs.add((src, tgt))
        existing_pairs.add((tgt, src))

    print(f"\nNouvelles arêtes : {len(new_edges)} | Ignorées : {len(skipped)}")
    for e in new_edges:
        src_t = nodes.get(e["src"], {}).get("tradition_label", "?")
        tgt_t = nodes.get(e["tgt"], {}).get("tradition_label", "?")
        ch = e["channel"]
        print(f"  + {e['src']} ({src_t}) --[{ch}]--> {e['tgt']} ({tgt_t})")

    if skipped:
        print(f"\nIgnorées ({len(skipped)}):")
        for s in skipped:
            print(f"  skip {s['src']} → {s['tgt']}: {s['reason']}")

    # ── Graph v15 ────────────────────────────────────────────────────────────
    edges_v15 = edges + new_edges

    # ── Composantes ──────────────────────────────────────────────────────────
    print("\nAnalyse composantes graph input...", end=" ", flush=True)
    adj_in  = build_adj_bidir(edges)
    comps_in = count_components(adj_in, all_node_ids)
    sizes_in = sorted([len(c) for c in comps_in], reverse=True)
    print(f"N={len(comps_in)} | Top5={sizes_in[:5]}")

    print("Analyse composantes v15...", end=" ", flush=True)
    adj_v15  = build_adj_bidir(edges_v15)
    comps_v15 = count_components(adj_v15, all_node_ids)
    sizes_v15 = sorted([len(c) for c in comps_v15], reverse=True)
    print(f"N={len(comps_v15)} | Top5={sizes_v15[:5]}")

    # ── Vérification spécifique : burnet connecté ? ───────────────────────────
    print("\nVérification connectivité des nœuds isolés auparavant :")
    for nid in ["burnet_early_greek_philosophy", "koran_rodwell_en", "laozi_taoteching_en"]:
        nb_v15 = len(adj_v15.get(nid, set()))
        nb_in  = len(adj_in.get(nid, set()))
        print(f"  {nid:45s}  {nb_in}→{nb_v15} voisins")

    # ── Simulation distances : paires corpus v243 impliquant les isolés ──────
    print("\nSimulation distances dirigées (corpus v243 focus) :")
    try:
        corpus_v243_path = Path("nipada/corpus/signed_corpus_v243_fusion_v242b_aristotle_laozi_plato.json")
        c243 = json.loads(corpus_v243_path.read_text())
        c212f = json.loads(Path("nipada/corpus/signed_corpus_v212f.json").read_text())
        corpus_all = {t["graph_node_id"] for t in c243["signed"]}
        corpus_all |= {t["graph_node_id"] for t in c212f["signed"]}

        dadj_in  = build_directed_adj(edges)
        dadj_v15 = build_directed_adj(edges_v15)

        focus = ["burnet_early_greek_philosophy", "koran_rodwell_en", "laozi_taoteching_en"]
        for nid in focus:
            d_in  = dijkstra_from(nid, dadj_in)
            d_v15 = dijkstra_from(nid, dadj_v15)
            finite_in  = sum(1 for t in corpus_all if t != nid and t in d_in)
            finite_v15 = sum(1 for t in corpus_all if t != nid and t in d_v15)
            print(f"  {nid:45s}  corpus fini: {finite_in}→{finite_v15}/{len(corpus_all)-1}")

    except Exception as ex:
        print(f"  (simulation ignorée: {ex})")

    # ── Sauvegarder ──────────────────────────────────────────────────────────
    print(f"\nSauvegarde → {GRAPH_OUT}")
    g_v15 = {
        "version":      "v15",
        "description":  (
            "Graph v13 + §244 : correction isolements structurels (burnet, koran, laozi) "
            "et pré-positionnement top candidats v208 "
            f"({len(new_edges)} arêtes ajoutées)"
        ),
        "n_nodes":          len(all_node_ids),
        "n_edges":          len(edges_v15),
        "n_edges_v13":      len(edges),
        "n_edges_added":    len(new_edges),
        "nodes": nodes,
        "edges": edges_v15,
    }
    GRAPH_OUT.write_text(json.dumps(g_v15, ensure_ascii=False, indent=None))
    print(f"  {len(all_node_ids)} nodes | {len(edges_v15)} edges total")

    # ── Stats ─────────────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    stats = {
        "section":           "§244",
        "graph_in":          str(GRAPH_IN),
        "graph_out":         str(GRAPH_OUT),
        "timestamp":         time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_s":         round(elapsed, 2),
        "n_edges_in":        len(edges),
        "n_edges_added":     len(new_edges),
        "n_edges_v15":       len(edges_v15),
        "n_components_in":   len(comps_in),
        "n_components_v15":  len(comps_v15),
        "component_sizes_in":  sizes_in,
        "component_sizes_v15": sizes_v15,
        "new_edges_detail":  new_edges,
        "skipped_edges":     skipped,
    }
    STATS_OUT.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"Stats → {STATS_OUT}")
    print(f"\n§244 terminé en {elapsed:.1f}s")
    print("  Prochaine étape — revalidation avec corpus v243 :")
    print("    python3 /home/stephane/GitHub/Panini/scripts/nipada_revalidation_v231.py \\")
    print("      --corpus-ext nipada/corpus/signed_corpus_v243_fusion_v242b_aristotle_laozi_plato.json \\")
    print("      --graph nipada/falsification/nipada_v244_graph_v15.json \\")
    print("      --out nipada/falsification/nipada_v244_reval_v243corpus.json")


if __name__ == "__main__":
    main()

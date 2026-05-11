#!/usr/bin/env python3
"""
nipada_patch_v272_reference_nodes.py
§272 — Intégration des 17 ouvrages de référence NiPaDa dans le graphe v19 → v20

Ajoute 17 nœuds "source scientifique" (fondateurs de la sémantique computationnelle
et cognitive) avec leurs arêtes d'influence documentées.

Usage:
    python3 nipada_patch_v272_reference_nodes.py [--dry-run]

Sortie:
    nipada/falsification/nipada_v272_graph_v20.json
"""
import argparse
import copy
import json
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent / "Panini-Research"
GRAPH_IN  = REPO_ROOT / "nipada" / "falsification" / "nipada_v271_graph_v19.json"
GRAPH_OUT = REPO_ROOT / "nipada" / "falsification" / "nipada_v272_graph_v20.json"

# ---------------------------------------------------------------------------
# Nouveaux nœuds — 17 ouvrages fondateurs NiPaDa
# kind = "reference_scientific" pour les distinguer du corpus signé
# ingestion_status = "planned" jusqu'à ce que les textes soient scorés
# ---------------------------------------------------------------------------
NEW_NODES = {
    # --- Primitives sémantiques / NSM ---
    "wierzbicka_1972": {
        "kind": "reference_scientific",
        "author": "Anna Wierzbicka",
        "year": 1972,
        "language_original": "eng",
        "tradition_label": "SEMANTIC_PRIMITIVES",
        "tradition_micro": "NSM_NATURAL_SEMANTIC_METALANGUAGE",
        "title_original": "Semantic Primitives",
        "title_en": "Semantic Primitives",
        "publisher": "Athenäum Verlag, Frankfurt",
        "relevance_score": 9.5,
        "nipada_relation": "~60 universal primitives ≈ dhātu V14; cross-linguistic validation of atomic decomposition",
        "tags": ["semantic_primitives", "NSM", "universals", "decomposition"],
        "ingestion_status": "planned",
        "url": "https://www.degruyter.com/document/doi/10.1515/9783110876178",
    },

    # --- Fonctions lexicales ---
    "melcuk_1996": {
        "kind": "reference_scientific",
        "author": "Igor Mel'čuk",
        "year": 1996,
        "language_original": "eng",
        "tradition_label": "LEXICAL_FUNCTIONS",
        "tradition_micro": "MEANING_TEXT_THEORY",
        "title_original": "Lexical Functions: A Tool for the Description of Lexical Relations in the Lexicon",
        "title_en": "Lexical Functions: A Tool for the Description of Lexical Relations in the Lexicon",
        "publisher": "in Wanner (ed.), Lexical Functions in Lexicography and Natural Language Processing. Amsterdam: Benjamins",
        "relevance_score": 10.0,
        "nipada_relation": "60+ FL → 7–15 dhātu; FL = direct precursor of n-ary dhātu operators; 42–86% coverage",
        "tags": ["lexical_functions", "MTT", "meaning-text", "paraphrase", "collocations"],
        "ingestion_status": "planned",
        "url": "https://benjamins.com/catalog/llsee.31.04mel",
    },

    # --- Dépendance conceptuelle ---
    "schank_1972": {
        "kind": "reference_scientific",
        "author": "Roger C. Schank",
        "year": 1972,
        "language_original": "eng",
        "tradition_label": "CONCEPTUAL_DEPENDENCY",
        "tradition_micro": "PRIMITIVE_ACTIONS",
        "title_original": "Conceptual Dependency: A Theory of Natural Language Understanding",
        "title_en": "Conceptual Dependency: A Theory of Natural Language Understanding",
        "publisher": "Cognitive Psychology, 3(4), 552–631",
        "relevance_score": 9.0,
        "nipada_relation": "11 primitive actions (PTRANS/ATRANS/MTRANS…) ≈ direct precursor of dhātu OPÉRATION/FONCTION/RAPPORT",
        "tags": ["conceptual_dependency", "primitive_actions", "NLU", "CD_theory"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1016/0010-0285(72)90008-2",
    },

    # --- Limite cognitive 7±2 ---
    "miller_1956": {
        "kind": "reference_scientific",
        "author": "George A. Miller",
        "year": 1956,
        "language_original": "eng",
        "tradition_label": "COGNITIVE_LIMITS",
        "tradition_micro": "WORKING_MEMORY_CAPACITY",
        "title_original": "The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information",
        "title_en": "The Magical Number Seven, Plus or Minus Two",
        "publisher": "Psychological Review, 63(2), 81–97",
        "relevance_score": 9.5,
        "nipada_relation": "7±2 → justification empirique de la limite hexaire sur les opérateurs n-aires dhātu",
        "tags": ["working_memory", "cognitive_load", "chunking", "7_plus_minus_2"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1037/h0043158",
    },

    # --- Sémantique compositionnelle ---
    "jackendoff_1972": {
        "kind": "reference_scientific",
        "author": "Ray Jackendoff",
        "year": 1972,
        "language_original": "eng",
        "tradition_label": "GENERATIVE_SEMANTICS",
        "tradition_micro": "CONCEPTUAL_SEMANTICS",
        "title_original": "Semantic Interpretation in Generative Grammar",
        "title_en": "Semantic Interpretation in Generative Grammar",
        "publisher": "MIT Press, Cambridge MA",
        "relevance_score": 8.5,
        "nipada_relation": "Compositional semantic rules via feature decomposition ≈ dhātu combination rules",
        "tags": ["generative_semantics", "compositionality", "conceptual_structure"],
        "ingestion_status": "planned",
        "url": "https://mitpress.mit.edu/9780262600132/",
    },

    # --- Combinateurs / base formelle ---
    "curry_1930": {
        "kind": "reference_scientific",
        "author": "Haskell B. Curry",
        "year": 1930,
        "language_original": "eng",
        "tradition_label": "COMBINATORY_LOGIC",
        "tradition_micro": "COMBINATORS",
        "title_original": "Grundlagen der Kombinatorischen Logik",
        "title_en": "Foundations of Combinatory Logic",
        "publisher": "American Journal of Mathematics, 52(3), 509–536",
        "relevance_score": 8.5,
        "nipada_relation": "Combinators S/K/I → dhātu = universal semantic combinators; functional composition formalised",
        "tags": ["combinatory_logic", "lambda_calculus", "functional_abstraction"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.2307/2370619",
    },

    # --- Logique floue ---
    "zadeh_1965": {
        "kind": "reference_scientific",
        "author": "Lotfi A. Zadeh",
        "year": 1965,
        "language_original": "eng",
        "tradition_label": "FUZZY_LOGIC",
        "tradition_micro": "MEMBERSHIP_FUNCTIONS",
        "title_original": "Fuzzy Sets",
        "title_en": "Fuzzy Sets",
        "publisher": "Information and Control, 8(3), 338–353",
        "relevance_score": 8.5,
        "nipada_relation": "μ∈[0,1] membership → dhātu intensity = continuous membership degrees (anti-bivalence)",
        "tags": ["fuzzy_sets", "membership", "graded_truth", "vagueness"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1016/S0019-9958(65)90241-X",
    },

    # --- Logique trivalente ---
    "lukasiewicz_1920": {
        "kind": "reference_scientific",
        "author": "Jan Łukasiewicz",
        "year": 1920,
        "language_original": "pol",
        "tradition_label": "MANY_VALUED_LOGIC",
        "tradition_micro": "TRIVALENT_LOGIC",
        "title_original": "O logice trójwartościowej",
        "title_en": "On Three-Valued Logic",
        "publisher": "Ruch Filozoficzny, 5, 170–171",
        "relevance_score": 8.0,
        "nipada_relation": "T/F/indeterminate trivalence → base formelle des opérateurs !/?/+ (affirmé/nié/indéterminé)",
        "tags": ["trivalent_logic", "many_valued_logic", "truth_values"],
        "ingestion_status": "planned",
        "url": "https://scholar.google.com/scholar?q=Lukasiewicz+1920+trivalent+logic",
    },

    # --- Composition récursive ---
    "kleene_1936": {
        "kind": "reference_scientific",
        "author": "Stephen C. Kleene",
        "year": 1936,
        "language_original": "eng",
        "tradition_label": "RECURSIVE_FUNCTIONS",
        "tradition_micro": "LAMBDA_CALCULUS_EXTENSION",
        "title_original": "General Recursive Functions of Natural Numbers",
        "title_en": "General Recursive Functions of Natural Numbers",
        "publisher": "Mathematische Annalen, 112, 727–742",
        "relevance_score": 8.0,
        "nipada_relation": "Recursive composition → formal basis for iterated dhātu composition; Kleene star = unbounded repetition",
        "tags": ["recursive_functions", "computability", "lambda_calculus"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1007/BF01565439",
    },

    # --- Qualia structure ---
    "pustejovsky_1995": {
        "kind": "reference_scientific",
        "author": "James Pustejovsky",
        "year": 1995,
        "language_original": "eng",
        "tradition_label": "GENERATIVE_LEXICON",
        "tradition_micro": "QUALIA_STRUCTURE",
        "title_original": "The Generative Lexicon",
        "title_en": "The Generative Lexicon",
        "publisher": "MIT Press, Cambridge MA",
        "relevance_score": 8.0,
        "nipada_relation": "Qualia structure (FORMAL/CONSTITUTIVE/TELIC/AGENTIVE) ≈ dhātu aspect decomposition",
        "tags": ["generative_lexicon", "qualia", "type_coercion", "cocomposition"],
        "ingestion_status": "planned",
        "url": "https://mitpress.mit.edu/9780262161503/",
    },

    # --- Word embeddings ---
    "mikolov_2013": {
        "kind": "reference_scientific",
        "author": "Tomáš Mikolov",
        "year": 2013,
        "language_original": "eng",
        "tradition_label": "DISTRIBUTIONAL_SEMANTICS",
        "tradition_micro": "WORD2VEC",
        "title_original": "Efficient Estimation of Word Representations in Vector Space",
        "title_en": "Efficient Estimation of Word Representations in Vector Space",
        "publisher": "arXiv:1301.3781",
        "relevance_score": 8.0,
        "nipada_relation": "Word2Vec: dhātu = semantic vector dimensions; king−man+woman=queen validates compositional semantic space",
        "tags": ["word2vec", "word_embeddings", "distributional_semantics", "neural_NLP"],
        "ingestion_status": "planned",
        "url": "https://arxiv.org/abs/1301.3781",
    },

    # --- Frames sémantiques ---
    "minsky_1975": {
        "kind": "reference_scientific",
        "author": "Marvin Minsky",
        "year": 1975,
        "language_original": "eng",
        "tradition_label": "FRAME_SEMANTICS",
        "tradition_micro": "KNOWLEDGE_FRAMES",
        "title_original": "A Framework for Representing Knowledge",
        "title_en": "A Framework for Representing Knowledge",
        "publisher": "in Winston (ed.), The Psychology of Computer Vision. McGraw-Hill",
        "relevance_score": 7.5,
        "nipada_relation": "Frames → dhātu = primitive terminal nodes in semantic frame structures; default inheritance",
        "tags": ["frames", "knowledge_representation", "default_values", "slots"],
        "ingestion_status": "planned",
        "url": "https://dspace.mit.edu/handle/1721.1/6089",
    },

    # --- Neurosémiotique ---
    "pulvermuller_2013": {
        "kind": "reference_scientific",
        "author": "Friedemann Pulvermüller",
        "year": 2013,
        "language_original": "eng",
        "tradition_label": "NEUROSEMIOTICS",
        "tradition_micro": "EMBODIED_SEMANTICS",
        "title_original": "How Neurons Make Meaning: Brain Mechanisms for Embodied and Abstract-Symbolic Semantics",
        "title_en": "How Neurons Make Meaning: Brain Mechanisms for Embodied and Abstract-Symbolic Semantics",
        "publisher": "Trends in Cognitive Sciences, 17(9), 458–470",
        "relevance_score": 7.5,
        "nipada_relation": "Neuronal cell assemblies as semantic primitives → potential neurobiological validation of V14 atoms",
        "tags": ["neurosemiotics", "embodied_semantics", "brain_mechanisms", "cell_assemblies"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1016/j.tics.2013.06.004",
    },

    # --- Réseaux sémantiques ---
    "quillian_1968": {
        "kind": "reference_scientific",
        "author": "M. Ross Quillian",
        "year": 1968,
        "language_original": "eng",
        "tradition_label": "SEMANTIC_NETWORKS",
        "tradition_micro": "SPREADING_ACTIVATION",
        "title_original": "Semantic Memory",
        "title_en": "Semantic Memory",
        "publisher": "in Minsky (ed.), Semantic Information Processing. MIT Press",
        "relevance_score": 7.0,
        "nipada_relation": "Semantic network with type-nodes → dhātu = primitive type-nodes; spreading activation ≈ d_topo",
        "tags": ["semantic_network", "spreading_activation", "associative_memory"],
        "ingestion_status": "planned",
        "url": "https://mitpress.mit.edu/9780262630153/",
    },

    # --- Symboles perceptuels ---
    "barsalou_1999": {
        "kind": "reference_scientific",
        "author": "Lawrence W. Barsalou",
        "year": 1999,
        "language_original": "eng",
        "tradition_label": "EMBODIED_COGNITION",
        "tradition_micro": "PERCEPTUAL_SYMBOL_SYSTEMS",
        "title_original": "Perceptual Symbol Systems",
        "title_en": "Perceptual Symbol Systems",
        "publisher": "Behavioral and Brain Sciences, 22(4), 577–660",
        "relevance_score": 7.0,
        "nipada_relation": "Perceptual symbols as reusable primitives → dhātu = abstract reusable perceptual simulator units",
        "tags": ["perceptual_symbols", "grounded_cognition", "simulation", "embodiment"],
        "ingestion_status": "planned",
        "url": "https://doi.org/10.1017/S0140525X99002149",
    },

    # --- Modèles de langage neuraux ---
    "bengio_2003": {
        "kind": "reference_scientific",
        "author": "Yoshua Bengio",
        "year": 2003,
        "language_original": "eng",
        "tradition_label": "NEURAL_LANGUAGE_MODELS",
        "tradition_micro": "DISTRIBUTED_REPRESENTATIONS",
        "title_original": "A Neural Probabilistic Language Model",
        "title_en": "A Neural Probabilistic Language Model",
        "publisher": "Journal of Machine Learning Research, 3, 1137–1155",
        "relevance_score": 7.0,
        "nipada_relation": "Distributed word representations → dhātu = continuous semantic space components; precursor of Word2Vec",
        "tags": ["neural_LM", "distributed_representations", "word_embeddings", "NNLM"],
        "ingestion_status": "planned",
        "url": "https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf",
    },

    # --- Critique de la décomposition lexicale ---
    "fodor_1970": {
        "kind": "reference_scientific",
        "author": "Jerry A. Fodor",
        "year": 1970,
        "language_original": "eng",
        "tradition_label": "LEXICAL_DECOMPOSITION_CRITIQUE",
        "tradition_micro": "ATOMISM_VS_DECOMPOSITION",
        "title_original": "Three Reasons for Not Deriving 'Kill' from 'Cause to Die'",
        "title_en": "Three Reasons for Not Deriving 'Kill' from 'Cause to Die'",
        "publisher": "Linguistic Inquiry, 1(4), 429–438",
        "relevance_score": 6.5,
        "nipada_relation": "Critique: decomposition loses idiomatic specificity → NiPaDa response: n-ary operators preserve idiomatic nuance",
        "tags": ["lexical_decomposition_critique", "kill_cause_die", "atomism", "Fodor"],
        "ingestion_status": "planned",
        "url": "https://www.jstor.org/stable/4177503",
    },
}

# ---------------------------------------------------------------------------
# Arêtes d'influence documentées entre les 17 référents
# + connexions vers les traditions existantes du graphe v19
# channel = "influence_scientifique (§272)"
# weight = 0.6 (citation directe) ou 0.4 (influence indirecte)
# ---------------------------------------------------------------------------
INFLUENCE_CHANNEL = "influence_scientifique (§272)"
TRADITION_CHANNEL = "héritage_conceptuel (§272)"

NEW_EDGES = [
    # ----------------------------------------------------------------
    # Inter-références : arêtes d'influence entre les 17 ouvrages
    # ----------------------------------------------------------------
    # Łukasiewicz → Kleene (logique → fonctions récursives)
    {"src": "lukasiewicz_1920", "tgt": "kleene_1936",     "weight": 0.6, "channel": INFLUENCE_CHANNEL},
    # Curry → Kleene (combinateurs → récursivité)
    {"src": "curry_1930",       "tgt": "kleene_1936",     "weight": 0.6, "channel": INFLUENCE_CHANNEL},
    # Kleene → Zadeh (logique formelle → logique floue)
    {"src": "kleene_1936",      "tgt": "zadeh_1965",      "weight": 0.4, "channel": INFLUENCE_CHANNEL},
    # Łukasiewicz → Zadeh (trivalence → fuzzy membership)
    {"src": "lukasiewicz_1920", "tgt": "zadeh_1965",      "weight": 0.6, "channel": INFLUENCE_CHANNEL},
    # Quillian → Minsky (réseaux sémantiques → frames)
    {"src": "quillian_1968",    "tgt": "minsky_1975",     "weight": 0.7, "channel": INFLUENCE_CHANNEL},
    # Schank → Wierzbicka (primitive actions → semantic primitives)
    {"src": "schank_1972",      "tgt": "wierzbicka_1972", "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    # Wierzbicka → Mel'čuk (NSM primitives → FL keyword decomposition)
    {"src": "wierzbicka_1972",  "tgt": "melcuk_1996",     "weight": 0.7, "channel": INFLUENCE_CHANNEL},
    # Jackendoff → Mel'čuk (conceptual semantics → MTT)
    {"src": "jackendoff_1972",  "tgt": "melcuk_1996",     "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    # Jackendoff → Pustejovsky (compositional semantics → generative lexicon)
    {"src": "jackendoff_1972",  "tgt": "pustejovsky_1995","weight": 0.6, "channel": INFLUENCE_CHANNEL},
    # Quillian → Pustejovsky (semantic network types → qualia structure)
    {"src": "quillian_1968",    "tgt": "pustejovsky_1995","weight": 0.5, "channel": INFLUENCE_CHANNEL},
    # Minsky → Barsalou (frames → perceptual symbol systems)
    {"src": "minsky_1975",      "tgt": "barsalou_1999",   "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    # Bengio → Mikolov (neural LM → Word2Vec)
    {"src": "bengio_2003",      "tgt": "mikolov_2013",    "weight": 0.8, "channel": INFLUENCE_CHANNEL},
    # Fodor critique ← Wierzbicka (décomposition débattue)
    {"src": "fodor_1970",       "tgt": "wierzbicka_1972", "weight": 0.4, "channel": INFLUENCE_CHANNEL},
    # Wierzbicka → Jackendoff (NSM ↔ conceptual semantics)
    {"src": "wierzbicka_1972",  "tgt": "jackendoff_1972", "weight": 0.4, "channel": INFLUENCE_CHANNEL},
    # Miller → Schank (cognitive limits → primitive action sets)
    {"src": "miller_1956",      "tgt": "schank_1972",     "weight": 0.4, "channel": INFLUENCE_CHANNEL},
    # Kleene → Curry (logique → combinateurs, contemporain)
    {"src": "kleene_1936",      "tgt": "curry_1930",      "weight": 0.4, "channel": INFLUENCE_CHANNEL},
    # Pulvermüller ← Barsalou (neurosémiotique ← perceptual symbols)
    {"src": "barsalou_1999",    "tgt": "pulvermuller_2013","weight": 0.5, "channel": INFLUENCE_CHANNEL},

    # ----------------------------------------------------------------
    # Connexions vers traditions existantes dans le graphe v19
    # (héritage conceptuel documenté — arêtes entrantes dans les refs)
    # ----------------------------------------------------------------
    # Aristote → Lukasiewicz (logique aristotélicienne → logique trivalente)
    {"src": "aristotle_prior_analytics", "tgt": "lukasiewicz_1920", "weight": 0.6, "channel": TRADITION_CHANNEL},
    # Aristote → Fodor (Categories → atomisme lexical)
    {"src": "aristotle_prior_analytics", "tgt": "fodor_1970",       "weight": 0.4, "channel": TRADITION_CHANNEL},
    # Aristote → Jackendoff (hylémorphisme → forme conceptuelle)
    {"src": "aristotle_prior_analytics", "tgt": "jackendoff_1972",  "weight": 0.4, "channel": TRADITION_CHANNEL},
    # Aristote → Quillian (catégories → réseaux sémantiques)
    {"src": "aristotle_prior_analytics", "tgt": "quillian_1968",    "weight": 0.4, "channel": TRADITION_CHANNEL},
    # Platon → Wierzbicka (formes universelles → primitives universelles)
    {"src": "plato_republic",            "tgt": "wierzbicka_1972",  "weight": 0.4, "channel": TRADITION_CHANNEL},
    {"src": "plato_theaetetus",          "tgt": "wierzbicka_1972",  "weight": 0.4, "channel": TRADITION_CHANNEL},
    # Platon → Fodor (idées innées → modules innés)
    {"src": "plato_meno",                "tgt": "fodor_1970",       "weight": 0.3, "channel": TRADITION_CHANNEL},
    # Platon → Quillian (formes comme catégories dans l'âme)
    {"src": "plato_sophist",             "tgt": "quillian_1968",    "weight": 0.3, "channel": TRADITION_CHANNEL},
]

# ---------------------------------------------------------------------------
# Nœuds intermédiaires manquants (pivots) pour fermer certaines chaînes
# ---------------------------------------------------------------------------
NEW_PIVOTS = {
    "turing_1950": {
        "kind": "pivot_author",
        "author": "Alan Turing",
        "year": 1950,
        "label": "PIVOT_COMPUTABILITY",
        "note": "Computing Machinery and Intelligence — pivot entre logique formelle et IA",
    },
    "chomsky_1957": {
        "kind": "pivot_author",
        "author": "Noam Chomsky",
        "year": 1957,
        "label": "PIVOT_GENERATIVE_GRAMMAR",
        "note": "Syntactic Structures — pivot entre logique formelle et sémantique générative",
    },
}

PIVOT_EDGES = [
    {"src": "kleene_1936",     "tgt": "turing_1950",   "weight": 0.7, "channel": INFLUENCE_CHANNEL},
    {"src": "turing_1950",     "tgt": "schank_1972",   "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    {"src": "turing_1950",     "tgt": "minsky_1975",   "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    {"src": "chomsky_1957",    "tgt": "jackendoff_1972","weight": 0.8, "channel": INFLUENCE_CHANNEL},
    {"src": "chomsky_1957",    "tgt": "schank_1972",   "weight": 0.5, "channel": INFLUENCE_CHANNEL},
    {"src": "chomsky_1957",    "tgt": "fodor_1970",    "weight": 0.7, "channel": INFLUENCE_CHANNEL},
    {"src": "chomsky_1957",    "tgt": "wierzbicka_1972","weight": 0.4, "channel": INFLUENCE_CHANNEL},
]


def check_existing_nodes(graph: dict, edge_list: list) -> tuple[list, list]:
    """Vérifie que les src/tgt des arêtes pointant vers des nœuds existants sont bien présents."""
    existing_ids = set(graph["nodes"].keys())
    new_ids = set(NEW_NODES.keys()) | set(NEW_PIVOTS.keys())
    all_ids = existing_ids | new_ids
    missing = []
    ok = []
    for e in edge_list:
        for side in ("src", "tgt"):
            nid = e[side]
            if nid not in all_ids:
                missing.append(nid)
            else:
                ok.append(nid)
    return ok, list(set(missing))


def patch_graph(graph: dict, dry_run: bool = False) -> dict:
    g = copy.deepcopy(graph)
    nodes = g["nodes"]
    edges = g["edges"]

    added_nodes = 0
    added_edges = 0
    skipped_nodes = 0
    skipped_edges = 0
    all_new_edges = NEW_EDGES + PIVOT_EDGES

    # --- Vérification des nœuds sources/cibles ---
    _, missing = check_existing_nodes(graph, all_new_edges)
    if missing:
        print(f"[WARN] Nœuds référencés mais absents du graphe v19: {missing}", file=sys.stderr)
        print("  Ces arêtes seront ignorées.", file=sys.stderr)

    existing_ids = set(nodes.keys())
    new_ids = set(NEW_NODES.keys()) | set(NEW_PIVOTS.keys())
    all_ids = existing_ids | new_ids

    # --- Ajout des nœuds ---
    for nid, ndata in {**NEW_NODES, **NEW_PIVOTS}.items():
        if nid in nodes:
            print(f"  [SKIP node] {nid} (déjà présent)")
            skipped_nodes += 1
        else:
            if not dry_run:
                nodes[nid] = ndata
            added_nodes += 1
            print(f"  [+node] {nid}  ({ndata['author']}, {ndata['year']})")

    # --- Déduplique les arêtes existantes ---
    existing_edge_set = {(e["src"], e["tgt"]) for e in edges}

    # --- Ajout des arêtes ---
    for edge in all_new_edges:
        src, tgt = edge["src"], edge["tgt"]
        # Ignorer si src ou tgt inexistants
        if src not in all_ids or tgt not in all_ids:
            print(f"  [SKIP edge] {src}→{tgt}  (nœud manquant)")
            skipped_edges += 1
            continue
        if (src, tgt) in existing_edge_set:
            print(f"  [SKIP edge] {src}→{tgt}  (déjà présente)")
            skipped_edges += 1
            continue
        if not dry_run:
            edges.append(edge)
            existing_edge_set.add((src, tgt))
        added_edges += 1
        print(f"  [+edge] {src} → {tgt}  w={edge['weight']}  [{edge['channel'][:40]}]")

    # --- Mise à jour des métadonnées ---
    if not dry_run:
        g["version"] = "v20"
        g["section"] = "§272"
        g["date"] = str(date.today())
        g["note"] = (
            f"Graphe v20 — §272 NiPaDa. Basé sur v19 (1781 nœuds, 22971 arêtes). "
            f"Ajout de {added_nodes} nœuds référentiels scientifiques (17 ouvrages fondateurs NiPaDa "
            f"+ {len(NEW_PIVOTS)} pivots Turing/Chomsky) et {added_edges} arêtes d'influence documentées."
        )
        g["patch_info"] = {
            "base_graph": "v19",
            "base_section": "§271",
            "added_nodes": added_nodes,
            "node_type": "reference_scientific + pivot_author",
            "added_edges": added_edges,
            "edge_channels": [INFLUENCE_CHANNEL, TRADITION_CHANNEL],
            "cost_direct": 0.05,
            "cost_indirect": 1.0,
            "motivation": (
                "§272: intégration des 17 ouvrages fondateurs NiPaDa dans le graphe de transmission. "
                "Nœuds 'reference_scientific' avec ingestion_status=planned. "
                "Arêtes d'influence inter-référents documentées (Wierzbicka→Mel'čuk, Bengio→Mikolov, etc.) "
                "et connexions vers traditions existantes (Aristote→Łukasiewicz, Platon→Wierzbicka). "
                "Pivots Turing/Chomsky ajoutés pour fermer les chaînes formelles→NLP."
            ),
        }

    print(f"\n--- Résumé {'(DRY RUN) ' if dry_run else ''}---")
    print(f"  Nœuds ajoutés:   {added_nodes}  (ignorés: {skipped_nodes})")
    print(f"  Arêtes ajoutées: {added_edges}  (ignorées: {skipped_edges})")

    return g


def main():
    parser = argparse.ArgumentParser(description="Patch graphe NiPaDa v19 → v20 (§272)")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans écriture")
    parser.add_argument("--graph-in",  default=str(GRAPH_IN),  help="Graphe source")
    parser.add_argument("--graph-out", default=str(GRAPH_OUT), help="Graphe destination")
    args = parser.parse_args()

    print(f"Lecture: {args.graph_in}")
    g = json.load(open(args.graph_in, encoding="utf-8"))
    print(f"  {len(g['nodes'])} nœuds, {len(g['edges'])} arêtes (v{g.get('version','?')})\n")

    g_new = patch_graph(g, dry_run=args.dry_run)

    if not args.dry_run:
        out = Path(args.graph_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(g_new, f, ensure_ascii=False, indent=2)
        print(f"\nÉcrit: {out}")
        print(f"  {len(g_new['nodes'])} nœuds, {len(g_new['edges'])} arêtes (v{g_new.get('version','?')})")
    else:
        print("\n[DRY RUN] Aucune écriture effectuée.")


if __name__ == "__main__":
    main()

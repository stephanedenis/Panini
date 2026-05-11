#!/usr/bin/env python3
"""
§212-fetch: Harvest multilingual corpus texts and compute V14 signatures.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01
Author: reconstructed for §212

Goal: Sign 100+ graph nodes with V14 signatures (diverse traditions), enabling:
  §213 — V_OPT v4 recalibration with larger/diverse signed set
  §214 — LOO tradition-out validation

Sources:
  1. SuttaCentral bilara API (70 Buddhist axial works, English/Pali)
  2. sacred-texts.com Sacred Books of the East (33 Indian + 17 Chinese)

NOTE on freq_signature:
  The original nipada_calibration_v177.py was created in Colab and never
  committed to git. This script uses a reconstructed V14 keyword lexicon
  (v212f_lexicon) based on content words only. Signatures computed here
  are self-consistent but may not be identical to v208 signatures for
  pre-existing works. This is noted in the output metadata.

Output:
  nipada/corpus/signed_corpus_v212f.json
  nipada/falsification/nipada_v212f_fetch_report.json

Usage:
  python3 nipada_fetch_corpus_v212f.py [--dry-run] [--limit N]

  --dry-run : fetch only first work per catalog, no filesystem write
  --limit N : process at most N works total (for testing)
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Path resolution (dual-repo pattern)
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found; run from Panini or Panini-Research repo")

CORPUS_DIR = _NIPADA / "corpus"
CACHE_DIR = CORPUS_DIR / "_cache"
FALSI_DIR = _NIPADA / "falsification"

CACHE_SUTTACENTRAL = CACHE_DIR / "suttacentral"
CACHE_SACRED_TEXTS = CACHE_DIR / "sacred_texts"

for d in [CACHE_SUTTACENTRAL, CACHE_SACRED_TEXTS, FALSI_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# V14 atom definitions
# ---------------------------------------------------------------------------

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET",
    "TEMPS", "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION",
    "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# V16 extends V14 with two new atoms derived from corpus gap analysis (§272, 2026-05-08)
# CAUSALITÉ : causal relation as such (distinct from action = OPÉRATION)
# ÉVÉNEMENT : event/state distinction (distinct from temporal sequence = TEMPS)
V16_ATOMS = V14_ATOMS + ["CAUSALITÉ", "ÉVÉNEMENT"]

# V17 extends V16 with MENTAL_STATE from §272 corpus gap analysis (2026-05-09)
# MENTAL_STATE : propositional attitudes (know/believe/want/feel/think)
V17_ATOMS = V16_ATOMS + ["MENTAL_STATE"]

# ---------------------------------------------------------------------------
# Reconstructed V14 keyword lexicon for English (v212f_lexicon)
# Uses content words only (no grammatical function words like is/are/not)
# to avoid frequency bias from function-word distribution.
# ---------------------------------------------------------------------------

ATOM_LEXICON_ENG: dict[str, list[str]] = {
    # -----------------------------------------------------------------------
    # Design rationale (v212f_lexicon):
    #   Content words ONLY — no function words (is/are/of/with/was/not).
    #   "one" and ordinals (first/second/...) removed from NOMBRE because
    #   they flood enumerated texts indiscriminately.
    #   "infinite/finite" moved to ESPACE (cosmological extent).
    #   Target tradition fingerprints:
    #     Buddhist: ÊTRE+SUJET dominant (beings/existence, self/mind)
    #     Hindu/Vedic: SUJET+ÊTRE dominant (self/soul/Brahman, reality/truth)
    #     Confucian: STRUCTURE+MODALITÉ dominant (order, rites, duty)
    #     Daoist: ORIENTATION+TEMPS dominant (way, change)
    #     Yijing: ESPACE+SYMÉTRIE dominant (heaven/earth, harmony)
    # -----------------------------------------------------------------------
    "ÊTRE": [
        # Being, existence, reality
        "being", "beings", "existence", "existent", "exist", "exists", "existed",
        "reality", "real", "actual", "actuality", "substance", "essence",
        "nature", "nothing", "nothingness", "something", "everything", "anything",
        "truth", "true", "fact", "facts", "presence", "nonexistent",
        "inexistent", "unreal", "absolute",
    ],
    "DIFFÉRENCE": [
        "different", "difference", "differences", "differ", "differing",
        "distinction", "distinctions", "distinct", "unlike", "contrary",
        "opposite", "opposites", "diversity", "diverse", "various",
        "contrast", "opposition", "opposed", "separate", "separated",
        "division", "divided", "other", "another", "else",
        "negation", "negative",
    ],
    "RAPPORT": [
        # Relation, connection — content words only
        "relation", "relations", "related", "relationship", "relationships",
        "relative", "connection", "connections", "connected", "connect",
        "link", "linked", "links", "bond", "bonds", "bonded",
        "between", "among", "interaction", "interactions", "interdependent",
        "depend", "dependence", "dependent", "together",
        "correspondence", "correspond", "corresponds",
        "association", "associated", "associate",
        "union", "united", "uniting", "unity",
        "contact", "contacts", "attachment", "attached", "binding",
        "involvement", "involved",
    ],
    "ORIENTATION": [
        "toward", "towards", "goal", "goals", "aim", "aims",
        "direction", "aspiration", "aspirations", "aspire",
        "intention", "intentions", "intend", "path", "paths", "way", "ways",
        "seek", "seeking", "sought", "strive", "striving",
        "approach", "progress", "tendency", "incline", "tao", "dao",
    ],
    "SUJET": [
        # Self, person, agent — content words only (no personal pronouns)
        "self", "selves", "soul", "souls", "spirit", "spirits",
        "mind", "minds", "consciousness", "person", "persons",
        "individual", "individuals", "subject", "subjects",
        "agent", "agents", "ego",
    ],
    "TEMPS": [
        "time", "times", "temporal", "impermanence", "impermanent",
        "permanent", "eternally", "eternal", "eternity", "moment", "moments",
        "duration", "period", "age", "era", "past", "future",
        "change", "changing", "changed", "transient", "fleeting",
        "enduring", "arising", "arises", "ceasing", "ceases", "cessation",
        "origination", "transience", "momentary",
    ],
    "MODALITÉ": [
        # Deontic and alethic modality — content words only
        "possible", "possibility", "possibilities", "impossible",
        "necessary", "necessity", "potential", "potentiality",
        "freedom", "free", "able", "ability", "capable", "capacity",
        "constraint", "constraints", "permit", "permission",
        "allowed", "allow", "ought", "duty",
        "obligation", "obliged", "compelled", "unavoidable",
    ],
    "NOMBRE": [
        # Explicit numerals ≥2 only.
        # "one" excluded (ambiguous: "one who" vs. cardinal).
        # Ordinals (first/second/...) excluded (ubiquitous in any listed text).
        # "infinite/finite" moved to ESPACE (cosmological extent).
        "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "hundred", "thousand", "million",
        "number", "numbers", "countless", "manifold", "plural",
    ],
    "ESPACE": [
        "place", "places", "space", "spaces", "world", "worlds",
        "universe", "earth", "heaven", "realm", "realms",
        "region", "field", "ground", "land", "body", "bodies",
        "above", "below", "throughout", "center",
        "boundary", "location", "infinite", "finite",
    ],
    "OPÉRATION": [
        "action", "actions", "act", "acting", "practice", "practices",
        "cause", "causes", "caused", "effect", "effects", "result", "results",
        "transformation", "transform", "transforms",
        "perform", "performed", "creates", "creation", "creating",
        "work", "works", "produce", "produces", "produced",
        "karma", "deed", "deeds",
    ],
    "FONCTION": [
        "function", "functions", "role", "roles", "purpose", "purposes",
        "serve", "serves", "serving", "service",
        "use", "useful", "usefulness", "method", "methods",
        "instrument", "tool", "task", "tasks",
    ],
    "STRUCTURE": [
        "form", "forms", "structure", "structures", "order", "ordered",
        "system", "systems", "element", "elements", "component", "components",
        "category", "categories", "type", "types", "kind", "kinds",
        "pattern", "patterns", "level", "levels", "hierarchy",
        "class", "classes", "organization", "organized", "arrangement",
        "rite", "rites", "ritual", "rituals", "ceremony", "ceremonies",
    ],
    "SYMÉTRIE": [
        "equal", "equality", "equally", "equals",
        "same", "alike", "similar", "similarity",
        "balance", "balanced", "harmony", "harmonious", "harmonize",
        "equivalent", "parallels", "parallel", "mutual", "mutually",
        "reciprocal", "reciprocity", "identical", "mirror",
        "correspond", "corresponds",
    ],
    "ÉQUATION": [
        # Identity, definition — content words only
        "defined", "definition", "definitions", "define", "defines",
        "means", "meaning", "constitute", "constitutes", "constituted",
        "called", "named", "principle", "principles",
        "law", "laws", "rule", "rules", "formula",
        "theorem", "identity", "namely",
    ],
    # -----------------------------------------------------------------------
    # V16 extensions — added 2026-05-08 from §272 corpus gap analysis
    # -----------------------------------------------------------------------
    "CAUSALITÉ": [
        # Causal relation as such — distinct from action (OPÉRATION)
        # Evidence: causative/causation top-50 non-V14 corpus terms
        # Theoretical: Wierzbicka NSM CAUSE, Jackendoff CAUSE(x,BECOME(y))
        # Talmy force dynamics, Levin & Hovav causative alternations
        "causation", "causative", "causatives", "causal", "causally",
        "causality", "anticausative", "anticausatives",
        "resultative", "resultatives",
        "inchoative", "inceptive",
        "volitional", "volition",
        "force", "forces", "forcing",
        "enable", "enables", "enabling",
        "trigger", "triggers", "triggering",
        "induce", "induces", "inducing",
        "prevent", "prevents", "prevention",
        "entail", "entails", "entailment", "entailments",
        "consequence", "consequences", "consequent",
        "compel", "compels", "compelled",
        "allow", "allows", "permit", "permits",
        "enforce", "enforces",
    ],
    "ÉVÉNEMENT": [
        # Event/state distinction — distinct from temporal sequence (TEMPS)
        # Evidence: event/events #1 non-V14 concept (2576 occ, 69 docs)
        # Theoretical: Vendler Aktionsart, Davidson events, aspect theory
        # Pustejovsky telic/agentive qualia, Jackendoff EVENT vs STATE
        "event", "events", "eventuality", "eventualities", "eventive",
        "state", "states", "stative",
        "process", "processes",
        "activity", "activities",
        "accomplishment", "accomplishments",
        "achievement", "achievements",
        "aspect", "aspectual", "aspectuality", "aktionsart",
        "telic", "telicity", "atelic", "atelicity",
        "perfective", "imperfective", "progressive",
        "durative", "punctual", "bounded", "unbounded",
        "dynamic", "dynamicity",
        "happen", "happens", "happening",
        "occur", "occurs", "occurring", "occurrence", "occurrences",
    ],
    # -----------------------------------------------------------------------
    # V17 extension — added 2026-05-09 from §272 corpus gap analysis
    # MENTAL_STATE : propositional attitude verbs (know/believe/want/feel)
    # Distinct from SUJET (self/person), ORIENTATION (goal/intend), MODALITÉ
    # Theoretical: Wierzbicka NSM KNOW/WANT/FEEL, Jackendoff conceptual
    # semantics mental predicates, Vendler propositional attitude verbs
    # Evidence: know/want/think/belief top-50 non-V16 cluster terms (n=62)
    # -----------------------------------------------------------------------
    "MENTAL_STATE": [
        # Epistemic verbs & nouns
        "know", "knows", "knowing", "known", "knowledge",
        "believe", "believes", "believed", "belief", "beliefs",
        "think", "thinks", "thinking", "thought", "thoughts",
        "understand", "understands", "understood", "understanding",
        "realize", "realizes", "realized", "realization",
        "perceive", "perceives", "perceived", "perception", "perceptions",
        "remember", "remembers", "remembered", "memory", "memories",
        "aware", "awareness", "unaware",
        # Conative verbs & nouns
        "want", "wants", "wanting", "wanted",
        "desire", "desires", "desired", "desiring",
        "wish", "wishes", "wishing", "wished",
        "expect", "expects", "expected", "expecting", "expectation", "expectations",
        # Affective states
        "feel", "feels", "feeling", "feelings", "felt",
        "emotion", "emotions", "emotional",
        "sentiment", "sentiments",
        # Cognitive adjectives & nouns
        "cognitive", "cognition", "cognize", "cognizes",
        "mental", "propositional", "attitude", "attitudes",
        "epistemic", "doxastic", "noetic",
        "opinion", "opinions", "view", "views",
        "proposal", "propose", "propose", "proposed",
    ],
}

# Build lookup: word → set of matching atoms  (English)
_WORD_TO_ATOMS: dict[str, list[str]] = {}
for atom, words in ATOM_LEXICON_ENG.items():
    for w in words:
        _WORD_TO_ATOMS.setdefault(w, []).append(atom)

# ===========================================================================
# Multilingual helpers
# ===========================================================================

def _norm(s: str) -> str:
    """Lowercase + strip diacritics → ASCII-only (for multilingual matching)."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )


def _tokenize_multi(text: str) -> list[str]:
    """Tokenize with diacritic normalization (French, Latin, German, etc.)."""
    return re.findall(r"[a-z]+", _norm(text))


# ===========================================================================
# French single-word lexicon (v212f_fra)
# Keys stored with accents; normalized to ASCII at index-build time.
# ===========================================================================

ATOM_LEXICON_FRA: dict[str, list[str]] = {
    "ÊTRE": [
        "être", "étant", "existence", "existant", "exister", "réalité", "réel",
        "actuel", "actualité", "substance", "essence", "nature", "néant", "rien",
        "vérité", "vrai", "fait", "présence", "absolu", "inexistant", "irréel",
    ],
    "DIFFÉRENCE": [
        "différent", "différence", "distinction", "distinct", "contraire",
        "opposé", "diversité", "divers", "contraste", "opposition", "séparé",
        "division", "autre", "autrement", "négation", "négatif",
    ],
    "RAPPORT": [
        "relation", "relatif", "rapport", "connexion", "lien", "entre",
        "interaction", "dépendant", "dépendance", "ensemble", "correspondance",
        "correspondre", "association", "union", "contact", "attachement", "lié",
        "interdépendant",
    ],
    "ORIENTATION": [
        "vers", "but", "objectif", "direction", "aspiration", "aspirer",
        "intention", "chemin", "voie", "chercher", "viser", "tendre",
        "approche", "progrès", "tendance", "tao", "dao",
    ],
    "SUJET": [
        "soi", "âme", "esprit", "conscience", "personne", "personnes",
        "individu", "individus", "sujet", "sujets", "agent", "moi", "ego",
    ],
    "TEMPS": [
        "temps", "temporel", "impermanence", "impermanent", "permanent",
        "éternel", "éternité", "moment", "moments", "durée", "période",
        "âge", "ère", "passé", "futur", "changement", "transitoire",
        "surgissement", "cessation", "origination", "passage", "transitoire",
    ],
    "MODALITÉ": [
        "possible", "possibilité", "impossible", "nécessaire", "nécessité",
        "potentiel", "liberté", "libre", "capacité", "contrainte", "permettre",
        "autoriser", "devoir", "obligation", "obligé", "conditionné",
    ],
    "NOMBRE": [
        "deux", "trois", "quatre", "cinq", "six", "sept", "huit",
        "neuf", "dix", "cent", "mille", "million", "nombre", "nombreux",
        "multiple", "pluriel", "innombrable",
    ],
    "ESPACE": [
        "lieu", "espace", "monde", "univers", "terre", "ciel", "domaine",
        "région", "champ", "sol", "corps", "frontière", "infini", "fini",
    ],
    "OPÉRATION": [
        "action", "acte", "agir", "pratique", "cause", "effet",
        "résultat", "transformation", "transformer", "créer", "création",
        "travail", "produire", "production", "karma", "oeuvre", "réaliser",
    ],
    "FONCTION": [
        "fonction", "rôle", "servir", "service", "utilité",
        "utile", "méthode", "instrument", "outil", "tâche",
    ],
    "STRUCTURE": [
        "forme", "structure", "ordre", "système", "élément", "composant",
        "catégorie", "type", "modèle", "niveau", "hiérarchie",
        "classe", "organisation", "rite", "rituel", "cérémonie",
    ],
    "SYMÉTRIE": [
        "égal", "égalité", "également", "même", "semblable", "similaire",
        "équilibre", "harmonie", "harmonieux", "équivalent", "parallèle",
        "mutuel", "réciproque", "identique", "miroir",
    ],
    "ÉQUATION": [
        "défini", "définition", "définir", "signifie", "signification",
        "constituer", "appeler", "nommer", "principe", "loi", "règle",
        "formule", "identité",
    ],
}

# Build FR lookup: word (ASCII-normalized) → matching atoms
_WORD_TO_ATOMS_FRA: dict[str, list[str]] = {}
for _atom, _words in ATOM_LEXICON_FRA.items():
    for _w in _words:
        _key = _norm(_w)
        _WORD_TO_ATOMS_FRA.setdefault(_key, []).append(_atom)


# ===========================================================================
# Multilingual phraseme lexicons (MWE → atoms)
# Keys are natural-language strings (may include accents / apostrophes).
# They are normalized at index-build time via _norm() + re.findall([a-z]+).
# Phrasemes override their component token lookups (non-compositional meaning).
# ===========================================================================

PHRASEME_LEXICON: dict[str, dict[str, list[str]]] = {
    # -----------------------------------------------------------------------
    # English — Buddhist, Hindu/Vedic, Daoist, Greek, general philosophical
    # -----------------------------------------------------------------------
    "eng": {
        # --- ÊTRE ---
        "come into being":         ["ÊTRE", "TEMPS"],
        "come to be":               ["ÊTRE", "TEMPS"],
        "bring into existence":     ["ÊTRE", "OPÉRATION"],
        "come into existence":      ["ÊTRE", "TEMPS"],
        "cease to be":              ["ÊTRE", "TEMPS"],
        "cease to exist":           ["ÊTRE", "TEMPS"],
        "pass out of existence":    ["ÊTRE", "TEMPS"],
        "human being":              ["ÊTRE", "SUJET"],
        "living being":             ["ÊTRE", "SUJET"],
        "sentient being":           ["ÊTRE", "SUJET"],
        "conscious being":          ["ÊTRE", "SUJET"],
        "in itself":                ["ÊTRE"],
        "by itself":                ["ÊTRE"],
        "as such":                  ["ÊTRE", "ÉQUATION"],
        "true nature":              ["ÊTRE"],
        # --- RAPPORT ---
        "cause and effect":         ["OPÉRATION", "RAPPORT"],
        "dependent origination":    ["RAPPORT", "TEMPS"],
        "in relation to":           ["RAPPORT"],
        "in relation with":         ["RAPPORT"],
        "conditioned by":           ["RAPPORT", "MODALITÉ"],
        "by virtue of":             ["RAPPORT", "ÉQUATION"],
        "by reason of":             ["RAPPORT", "ÉQUATION"],
        # --- ORIENTATION ---
        "middle way":               ["ORIENTATION", "ESPACE"],
        "noble eightfold path":     ["ORIENTATION", "MODALITÉ", "NOMBRE"],
        "eightfold path":           ["ORIENTATION", "MODALITÉ", "NOMBRE"],
        "right path":               ["ORIENTATION", "MODALITÉ"],
        "right way":                ["ORIENTATION", "MODALITÉ"],
        "way of life":              ["ORIENTATION", "OPÉRATION"],
        "way of the tao":           ["ORIENTATION"],
        "great way":                ["ORIENTATION"],
        # --- SUJET ---
        "inner self":               ["SUJET"],
        "true self":                ["SUJET", "ÊTRE"],
        "not self":                 ["SUJET", "DIFFÉRENCE"],
        "no self":                  ["SUJET", "DIFFÉRENCE"],
        "state of mind":            ["SUJET", "MODALITÉ"],
        "peace of mind":            ["SUJET", "MODALITÉ"],
        "frame of mind":            ["SUJET"],
        "one s own nature":         ["SUJET", "ÊTRE"],   # "one's own nature" post-tokenize
        # --- MODALITÉ ---
        "free will":                ["MODALITÉ", "SUJET"],
        "act of will":              ["MODALITÉ", "SUJET", "OPÉRATION"],
        "natural law":              ["MODALITÉ", "ÊTRE"],
        "moral law":                ["MODALITÉ"],
        "divine law":               ["MODALITÉ"],
        "eternal law":              ["MODALITÉ", "TEMPS"],
        "cosmic law":               ["MODALITÉ", "ESPACE"],
        "right conduct":            ["MODALITÉ", "OPÉRATION"],
        "right action":             ["MODALITÉ", "OPÉRATION"],
        "right speech":             ["MODALITÉ"],
        "right livelihood":         ["MODALITÉ"],
        "right effort":             ["MODALITÉ", "OPÉRATION"],
        "right mindfulness":        ["MODALITÉ", "SUJET"],
        "right concentration":      ["MODALITÉ", "SUJET"],
        "right understanding":      ["MODALITÉ"],
        "right intention":          ["MODALITÉ", "ORIENTATION"],
        "right view":               ["MODALITÉ"],
        # --- TEMPS ---
        "arise and cease":          ["TEMPS"],
        "arising and ceasing":      ["TEMPS"],
        "arising and passing":      ["TEMPS"],
        "arising and cessation":    ["TEMPS"],
        "come to pass":             ["TEMPS"],
        "comes to pass":            ["TEMPS"],
        "pass away":                ["TEMPS", "ÊTRE"],
        "at all times":             ["TEMPS"],
        "for all time":             ["TEMPS"],
        # --- STRUCTURE ---
        "five aggregates":          ["STRUCTURE", "NOMBRE"],
        "three marks":              ["STRUCTURE", "NOMBRE"],
        "four noble truths":        ["ÊTRE", "NOMBRE", "STRUCTURE"],
        "three jewels":             ["STRUCTURE", "NOMBRE"],
        "ten commandments":         ["MODALITÉ", "NOMBRE"],
        "natural order":            ["STRUCTURE", "ÊTRE"],
        "social order":             ["STRUCTURE"],
        "cosmic order":             ["STRUCTURE", "ESPACE"],
        "moral order":              ["STRUCTURE", "MODALITÉ"],
        "form and matter":          ["STRUCTURE", "ÊTRE"],
        # --- NOMBRE ---
        "ten thousand things":      ["NOMBRE", "ESPACE"],
        "ten thousand":             ["NOMBRE"],
        "three worlds":             ["NOMBRE", "ESPACE"],
        # --- ESPACE ---
        "heaven and earth":         ["ESPACE"],
        "above and below":          ["ESPACE"],
        "this world":               ["ESPACE"],
        "other world":              ["ESPACE", "DIFFÉRENCE"],
        "other worlds":             ["ESPACE", "DIFFÉRENCE"],
        # --- OPÉRATION ---
        "bring about":              ["OPÉRATION"],
        "set in motion":            ["OPÉRATION"],
        "act upon":                 ["OPÉRATION"],
        "karma yoga":               ["OPÉRATION"],
        "jnana yoga":               ["SUJET"],
        "bhakti yoga":              ["SUJET", "RAPPORT"],
        # --- ÉQUATION ---
        "that is to say":           ["ÉQUATION"],
        "in other words":           ["ÉQUATION"],
        "what is called":           ["ÉQUATION"],
        "so called":                ["ÉQUATION"],
        "is defined as":            ["ÉQUATION"],
        "by which is meant":        ["ÉQUATION"],
        "namely":                   ["ÉQUATION"],   # single word but idiomatic
        "the principle of":         ["ÉQUATION"],
        # --- SYMÉTRIE ---
        "one and the same":         ["SYMÉTRIE", "ÉQUATION"],
        "the same as":              ["SYMÉTRIE", "ÉQUATION"],
        "equal in":                 ["SYMÉTRIE"],
        # --- DIFFÉRENCE ---
        "other than":               ["DIFFÉRENCE"],
        "as opposed to":            ["DIFFÉRENCE"],
        "as distinct from":         ["DIFFÉRENCE"],
        "as against":               ["DIFFÉRENCE"],
        # --- FONCTION ---
        "for the purpose of":       ["FONCTION", "ORIENTATION"],
        "in the service of":        ["FONCTION"],
        "in the capacity of":       ["FONCTION"],
        # --- "less-known" compound expressions ---
        "wu wei":                   ["MODALITÉ", "ÊTRE"],    # Daoist non-action
        "te tao":                   ["ORIENTATION", "ÊTRE"],
        "yin yang":                 ["SYMÉTRIE", "DIFFÉRENCE"],
        "heaven s mandate":         ["MODALITÉ", "ESPACE"],  # 天命
        "mandate of heaven":        ["MODALITÉ", "ESPACE"],
        "original nature":          ["ÊTRE", "SUJET"],
        "returning to the root":    ["ORIENTATION", "ÊTRE"],
        "no action":                ["MODALITÉ", "ÊTRE"],
        "non action":               ["MODALITÉ", "ÊTRE"],
        "self nature":              ["SUJET", "ÊTRE"],
        "buddha nature":            ["SUJET", "ÊTRE"],
        "pure land":                ["ESPACE"],
        "wheel of dharma":          ["OPÉRATION", "MODALITÉ"],
        "turning of the wheel":     ["OPÉRATION", "TEMPS"],
        "noble silence":            ["MODALITÉ"],
        "skillful means":           ["FONCTION", "MODALITÉ"],
        "empty of inherent existence": ["ÊTRE", "DIFFÉRENCE"],
    },
    # -----------------------------------------------------------------------
    # French — phrasèmes philosophiques (Descartes, Bergson, Sartre, traductions)
    # -----------------------------------------------------------------------
    "fra": {
        # --- ÊTRE ---
        "en soi":                   ["ÊTRE"],
        "pour soi":                 ["ÊTRE", "SUJET"],
        "en soi et pour soi":       ["ÊTRE", "SUJET"],
        "en tant que":              ["ÊTRE", "ÉQUATION"],
        "venir à l existence":      ["ÊTRE", "TEMPS"],
        "cesser d exister":         ["ÊTRE", "TEMPS"],
        "prise en existence":       ["ÊTRE", "OPÉRATION"],
        "être humain":              ["ÊTRE", "SUJET"],
        "être vivant":              ["ÊTRE", "SUJET"],
        "être conscient":           ["ÊTRE", "SUJET"],
        "réalité ultime":           ["ÊTRE"],
        "nature véritable":         ["ÊTRE"],
        # --- RAPPORT ---
        "cause et effet":           ["OPÉRATION", "RAPPORT"],
        "en relation avec":         ["RAPPORT"],
        "en rapport avec":          ["RAPPORT"],
        "par l intermédiaire de":   ["RAPPORT"],
        "co-origination dépendante": ["RAPPORT", "TEMPS"],
        "production conditionnée":  ["RAPPORT", "TEMPS"],
        "par le fait de":           ["RAPPORT", "ÉQUATION"],
        # --- ORIENTATION ---
        "voie du milieu":           ["ORIENTATION", "ESPACE"],
        "noble chemin octuple":     ["ORIENTATION", "MODALITÉ", "NOMBRE"],
        "chemin de la vertu":       ["ORIENTATION", "MODALITÉ"],
        "mode de vie":              ["ORIENTATION", "OPÉRATION"],
        "retour à la source":       ["ORIENTATION", "ÊTRE"],
        # --- SUJET ---
        "en soi-même":              ["SUJET"],
        "moi profond":              ["SUJET"],
        "état d esprit":            ["SUJET", "MODALITÉ"],
        "paix de l esprit":         ["SUJET", "MODALITÉ"],
        "nature propre":            ["SUJET", "ÊTRE"],
        "non-soi":                  ["SUJET", "DIFFÉRENCE"],
        "prise de conscience":      ["SUJET", "OPÉRATION"],
        "for-soi":                  ["SUJET", "ÊTRE"],
        # --- MODALITÉ ---
        "libre arbitre":            ["MODALITÉ", "SUJET"],
        "acte de volonté":          ["MODALITÉ", "SUJET", "OPÉRATION"],
        "loi naturelle":            ["MODALITÉ", "ÊTRE"],
        "loi morale":               ["MODALITÉ"],
        "loi divine":               ["MODALITÉ"],
        "loi éternelle":            ["MODALITÉ", "TEMPS"],
        "bonne conduite":           ["MODALITÉ", "OPÉRATION"],
        "juste action":             ["MODALITÉ", "OPÉRATION"],
        "droit chemin":             ["MODALITÉ", "ORIENTATION"],
        # --- TEMPS ---
        "surgissement et disparition": ["TEMPS"],
        "passage du temps":         ["TEMPS"],
        "à tout moment":            ["TEMPS"],
        "de tout temps":            ["TEMPS"],
        "venir à être":             ["ÊTRE", "TEMPS"],
        "cesser d être":            ["ÊTRE", "TEMPS"],
        # --- STRUCTURE ---
        "cinq agrégats":            ["STRUCTURE", "NOMBRE"],
        "trois marques":            ["STRUCTURE", "NOMBRE"],
        "quatre nobles vérités":    ["ÊTRE", "NOMBRE", "STRUCTURE"],
        "triple joyau":             ["STRUCTURE", "NOMBRE"],
        "ordre naturel":            ["STRUCTURE", "ÊTRE"],
        "ordre social":             ["STRUCTURE"],
        "ordre cosmique":           ["STRUCTURE", "ESPACE"],
        "forme et matière":         ["STRUCTURE", "ÊTRE"],
        # --- NOMBRE ---
        "dix mille choses":         ["NOMBRE", "ESPACE"],
        "trois mondes":             ["NOMBRE", "ESPACE"],
        # --- ESPACE ---
        "ciel et terre":            ["ESPACE"],
        "ce monde":                 ["ESPACE"],
        "l autre monde":            ["ESPACE", "DIFFÉRENCE"],
        # --- OPÉRATION ---
        "mettre en mouvement":      ["OPÉRATION"],
        "mettre en oeuvre":         ["OPÉRATION"],
        "wu wei":                   ["MODALITÉ", "ÊTRE"],
        # --- ÉQUATION ---
        "c est-à-dire":             ["ÉQUATION"],
        "autrement dit":            ["ÉQUATION"],
        "par définition":           ["ÉQUATION"],
        "ce que l on entend par":   ["ÉQUATION"],
        "c est à dire":             ["ÉQUATION"],
        # --- SYMÉTRIE ---
        "un seul et même":          ["SYMÉTRIE", "ÉQUATION"],
        "le même que":              ["SYMÉTRIE", "ÉQUATION"],
        "à égalité":                ["SYMÉTRIE"],
        # --- DIFFÉRENCE ---
        "autre que":                ["DIFFÉRENCE"],
        "par opposition à":         ["DIFFÉRENCE"],
        "à la différence de":       ["DIFFÉRENCE"],
        # --- FONCTION ---
        "dans le but de":           ["FONCTION", "ORIENTATION"],
        "au service de":            ["FONCTION"],
        "dans la mesure où":        ["RAPPORT", "MODALITÉ"],
        # --- "less-known" compound expressions ---
        "non-action":               ["MODALITÉ", "ÊTRE"],
        "yin yang":                 ["SYMÉTRIE", "DIFFÉRENCE"],
        "mandat du ciel":           ["MODALITÉ", "ESPACE"],
        "nature de bouddha":        ["SUJET", "ÊTRE"],
        "origination dépendante":   ["RAPPORT", "TEMPS"],
        "vacuité inhérente":        ["ÊTRE", "DIFFÉRENCE"],
    },
}

# Build phraseme index: {lang: {first_word: [(phrase_tuple, atoms), ...]}}
# Keys are ASCII-normalized token tuples (via _norm + [a-z]+).
# Sorted by phrase length (longest first) for greedy matching.
_PHRASEME_INDEX: dict[str, dict[str, list[tuple[tuple[str, ...], list[str]]]]] = {}
for _lang, _phrases in PHRASEME_LEXICON.items():
    _idx: dict[str, list[tuple[tuple[str, ...], list[str]]]] = {}
    for _phrase_str, _atoms in _phrases.items():
        _toks = tuple(re.findall(r"[a-z]+", _norm(_phrase_str)))
        if _toks:
            _idx.setdefault(_toks[0], []).append((_toks, _atoms))
    # Sort each first-word bucket: longest phrase first (greedy)
    for _fw in _idx:
        _idx[_fw].sort(key=lambda x: -len(x[0]))
    _PHRASEME_INDEX[_lang] = _idx


def freq_signature(text: str, lang: str = "eng") -> dict[str, float]:
    """
    Compute V14 signature for text, with multilingual support and MWE detection.

    Algorithm:
      1. Select single-word lexicon by lang (eng / fra; others → uniform)
      2. Tokenize with appropriate normalizer
      3. MWE pass: greedy longest-match phraseme detection (marks consumed)
         Phrasemes override their components — non-compositional interpretation.
      4. Single-token pass on unconsumed positions
      5. Normalize atom counts (L1 = 1.0)

    Supported langs: "eng" (English), "fra" (French).
    Others return uniform 1/14 distribution.

    Note: English tokenizer is kept identical to v212f original (ASCII [a-z]+)
    so existing English signatures remain unchanged. French uses NFD-normalized
    tokenizer to handle diacritics.
    """
    if lang == "eng":
        tokens = re.findall(r"[a-z]+", text.lower())
        word_lexicon = _WORD_TO_ATOMS
    elif lang == "fra":
        tokens = _tokenize_multi(text)
        word_lexicon = _WORD_TO_ATOMS_FRA
    else:
        return {a: 1.0 / 14 for a in V14_ATOMS}

    counts: dict[str, int] = {a: 0 for a in V14_ATOMS}
    total = 0
    n = len(tokens)
    consumed = [False] * n

    # --- MWE / phraseme detection pass (greedy, longest-first) ---
    phraseme_idx = _PHRASEME_INDEX.get(lang, {})
    i = 0
    while i < n:
        candidates = phraseme_idx.get(tokens[i], [])
        matched = False
        for phrase_toks, atoms in candidates:   # already sorted longest-first
            length = len(phrase_toks)
            if i + length <= n and tuple(tokens[i:i + length]) == phrase_toks:
                for atom in atoms:
                    counts[atom] += 1
                total += len(atoms)
                for j in range(i, i + length):
                    consumed[j] = True
                i += length
                matched = True
                break
        if not matched:
            i += 1

    # --- Single-token pass on unconsumed positions ---
    for idx, tok in enumerate(tokens):
        if consumed[idx]:
            continue
        atoms_for_tok = word_lexicon.get(tok)
        if atoms_for_tok:
            for atom in atoms_for_tok:
                counts[atom] += 1
            total += len(atoms_for_tok)

    if total == 0:
        return {a: 1.0 / 14 for a in V14_ATOMS}

    sig = {a: counts[a] / total for a in V14_ATOMS}
    s = sum(sig.values())
    assert abs(s - 1.0) < 1e-9, f"signature sum error: {s}"
    return sig


# ---------------------------------------------------------------------------
# SBE volume URL map (catalog uses wrong sbe/ prefix; corrected here)
# ---------------------------------------------------------------------------

SBE_URL_MAP: dict[str, Optional[str]] = {
    "sbe1":  "https://www.sacred-texts.com/hin/sbe01/",
    "sbe01": "https://www.sacred-texts.com/hin/sbe01/",
    "sbe2":  "https://www.sacred-texts.com/hin/sbe02/",
    "sbe02": "https://www.sacred-texts.com/hin/sbe02/",
    "sbe3":  "https://www.sacred-texts.com/cfu/sbe03/",
    "sbe03": "https://www.sacred-texts.com/cfu/sbe03/",
    "sbe8":  "https://www.sacred-texts.com/hin/sbe08/",
    "sbe08": "https://www.sacred-texts.com/hin/sbe08/",
    "sbe12": "https://www.sacred-texts.com/hin/sbr/sbe12/",
    "sbe14": "https://www.sacred-texts.com/hin/sbe14/",
    "sbe15": "https://www.sacred-texts.com/hin/sbe15/",
    "sbe16": "https://www.sacred-texts.com/ich/",     # Yijing under ich/
    "sbe17": "https://www.sacred-texts.com/bud/sbe17/",
    "sbe22": "https://www.sacred-texts.com/jai/sbe22/",
    "sbe25": None,   # Manu Smriti – not found
    "sbe27": None,   # Li Ki vol 1 – not found
    "sbe28": None,   # Li Ki vol 2 – not found
    "sbe29": "https://www.sacred-texts.com/hin/sbe29/",
    "sbe30": "https://www.sacred-texts.com/hin/sbe30/",
    "sbe32": "https://www.sacred-texts.com/hin/sbe32/",
    "sbe34": "https://www.sacred-texts.com/hin/sbe34/",
    "sbe38": "https://www.sacred-texts.com/hin/sbe38/",
    "sbe39": "https://www.sacred-texts.com/tao/sbe39/",
    "sbe40": "https://www.sacred-texts.com/tao/sbe40/",
    "sbe42": "https://www.sacred-texts.com/hin/sbe42/",
    "sbe44": "https://www.sacred-texts.com/hin/sbr/sbe44/",
    "sbe45": "https://www.sacred-texts.com/jai/sbe45/",
    "sbe49": "https://www.sacred-texts.com/bud/sbe49/",
}

HTTP_HEADERS = {"User-Agent": "NIPADA-Research/0.4.0 (academic, non-commercial)"}
REQUEST_DELAY = 1.2  # seconds between requests


def _get(url: str, timeout: int = 15) -> Optional[requests.Response]:
    """Polite HTTP GET with retry on 429/503."""
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=timeout, headers=HTTP_HEADERS)
            if r.status_code in (429, 503):
                wait = 5 * (attempt + 1)
                print(f"    [rate-limit {r.status_code}] waiting {wait}s …")
                time.sleep(wait)
                continue
            return r
        except requests.RequestException as exc:
            print(f"    [request error] {exc}")
            time.sleep(2)
    return None


# ---------------------------------------------------------------------------
# SuttaCentral fetcher
# ---------------------------------------------------------------------------

def fetch_suttacentral(work_id: str, url: str) -> Optional[str]:
    """
    Fetch English translation from SuttaCentral bilara API.
    URL format: https://suttacentral.net/{uid}/en/{author}
    Returns concatenated segment text, or None on failure.
    """
    # Extract sutta uid and author from URL
    # e.g. https://suttacentral.net/dn1/en/sujato → uid=dn1, author=sujato
    m = re.match(r"https://suttacentral\.net/([^/]+)/en/([^/?]+)", url)
    if not m:
        print(f"    [sc] unexpected URL format: {url}")
        return None
    uid, author = m.group(1), m.group(2)

    cache_file = CACHE_SUTTACENTRAL / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    api_url = f"https://suttacentral.net/api/bilarasuttas/{uid}/en?author={author}"
    print(f"    [sc] GET {api_url}")
    r = _get(api_url)
    time.sleep(REQUEST_DELAY)

    if r is None or r.status_code != 200:
        print(f"    [sc] failed: {r.status_code if r else 'no response'}")
        return None

    try:
        data = r.json()
    except Exception:
        print("    [sc] JSON parse error")
        return None

    tt = data.get("translation_text", {})
    if not tt:
        print("    [sc] no translation_text in response")
        return None

    # Concatenate all segment values (skip headings-only segments if < 5 chars)
    segments = [v.strip() for v in tt.values() if isinstance(v, str) and len(v.strip()) > 4]
    full_text = " ".join(segments)

    if len(full_text) < 100:
        print(f"    [sc] text too short ({len(full_text)} chars), skipping")
        return None

    cache_file.write_text(full_text, encoding="utf-8")
    return full_text


# ---------------------------------------------------------------------------
# sacred-texts.com fetcher
# ---------------------------------------------------------------------------

def _extract_text_from_html(html: str) -> str:
    """Extract readable text from sacred-texts.com HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts, styles, nav
    for tag in soup(["script", "style", "nav", "header", "footer", "a"]):
        tag.decompose()
    # Get main body text
    body = soup.find("body")
    if body is None:
        return soup.get_text(separator=" ", strip=True)
    text = body.get_text(separator=" ", strip=True)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fetch_index_links(index_url: str) -> list[str]:
    """
    Fetch index page and return list of chapter HTML links.
    Returns absolute URLs for .htm/.html files.
    """
    r = _get(index_url)
    time.sleep(REQUEST_DELAY)
    if r is None or r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    from urllib.parse import urljoin

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Keep only local .htm/.html links (not navigation, not external)
        if re.search(r"\.html?$", href, re.IGNORECASE) and not href.startswith(".."):
            abs_url = urljoin(index_url, href)
            if abs_url not in links:
                links.append(abs_url)
    return links


def fetch_sacred_texts(work_id: str, catalog_url: str) -> Optional[str]:
    """
    Fetch text from sacred-texts.com.

    Strategy:
      1. Fix catalog URL (sbe/ prefix → real prefix via SBE_URL_MAP)
      2. Fetch index page
      3. Follow chapter links (skip intro/preface/front-matter)
      4. Extract and concatenate text from chapter pages

    Returns full text or None on failure.
    """
    cache_file = CACHE_SACRED_TEXTS / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    # Fix URL prefix: catalog uses sbe/sbeXX/, we need the real path
    real_url = catalog_url
    sbe_match = re.search(r"sbe/sbe(\d+)/?", catalog_url, re.IGNORECASE)
    if sbe_match:
        sbe_key = f"sbe{sbe_match.group(1)}"
        # Try both zero-padded and non-padded
        real_url_candidate = SBE_URL_MAP.get(sbe_key) or SBE_URL_MAP.get(
            f"sbe{int(sbe_match.group(1)):02d}"
        )
        if real_url_candidate is None:
            print(f"    [st] SBE volume {sbe_key} not mapped – skipping {work_id}")
            return None
        real_url = real_url_candidate
        print(f"    [st] URL remapped: {catalog_url} → {real_url}")

    print(f"    [st] fetching index: {real_url}")
    chapter_links = _fetch_index_links(real_url)

    if not chapter_links:
        print(f"    [st] no chapter links found at {real_url}")
        return None

    # Filter: skip known front-matter files (title, preface, intro, toc, contents)
    _SKIP_PATTERNS = re.compile(
        r"(000|toc|contents?|preface|intro|index|title|copyright|pageidx)", re.IGNORECASE
    )
    content_links = [l for l in chapter_links if not _SKIP_PATTERNS.search(l)]
    if not content_links:
        content_links = chapter_links  # fall back if filter too aggressive

    print(f"    [st] {len(content_links)} chapter links to fetch")

    all_text_parts = []
    for chapter_url in content_links[:30]:  # cap at 30 chapters per work
        r = _get(chapter_url)
        time.sleep(REQUEST_DELAY)
        if r is None or r.status_code != 200:
            continue
        chapter_text = _extract_text_from_html(r.text)
        if len(chapter_text) > 100:
            all_text_parts.append(chapter_text)

    if not all_text_parts:
        print(f"    [st] no chapter text extracted for {work_id}")
        return None

    full_text = " ".join(all_text_parts)
    cache_file.write_text(full_text, encoding="utf-8")
    return full_text


# ---------------------------------------------------------------------------
# Graph node matching
# ---------------------------------------------------------------------------

def _load_graph_nodes() -> dict:
    """Load graph v12 node dict {id: node_data}."""
    graph_path = FALSI_DIR / "nipada_v210a_graph_v12.json"
    if not graph_path.exists():
        print(f"WARNING: graph not found at {graph_path}")
        return {}
    with open(graph_path, encoding="utf-8") as f:
        g = json.load(f)
    return g.get("nodes", {})


def match_to_graph_node(work_id: str, nodes: dict) -> Optional[str]:
    """
    Find graph node matching work_id.
    Tries exact match, then partial match.
    Returns node_id or None.
    """
    if work_id in nodes:
        return work_id
    # Try prefix match
    for node_id in nodes:
        if work_id in node_id or node_id in work_id:
            return node_id
    return None


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_catalogs(dry_run: bool = False, limit: int = 0) -> dict:
    """
    Process all three catalogs, fetch texts, compute V14 signatures.

    Returns:
        {
          "signed": [...],          # list of signed work dicts
          "report": {...},          # fetch report
        }
    """
    # Load catalogs
    catalogs = {
        "buddhist_axial": {
            "file": CORPUS_DIR / "catalog_buddhist_axial_v205.json",
            "source": "suttacentral",
        },
        "indian_axial": {
            "file": CORPUS_DIR / "catalog_indian_axial_v206a.json",
            "source": "sacred_texts",
        },
        "chinese_axial": {
            "file": CORPUS_DIR / "catalog_chinese_axial_v206b.json",
            "source": "sacred_texts",
        },
    }

    nodes = _load_graph_nodes()
    print(f"Loaded {len(nodes)} graph nodes")

    signed_works = []
    report_entries = []
    total_fetched = 0
    total_signed = 0
    total_skipped = 0
    total_failed = 0
    n_processed = 0

    for cat_name, cat_info in catalogs.items():
        cat_path = cat_info["file"]
        if not cat_path.exists():
            print(f"WARNING: catalog not found: {cat_path}")
            continue

        with open(cat_path, encoding="utf-8") as f:
            cat_data = json.load(f)

        works = cat_data.get("works", [])
        source = cat_info["source"]

        print(f"\n=== {cat_name} ({source}) — {len(works)} works ===")

        for w in works:
            if limit > 0 and n_processed >= limit:
                break

            work_id = w.get("id", "")
            url_en = w.get("url_translation_en")

            if not url_en:
                report_entries.append({
                    "work_id": work_id, "catalog": cat_name,
                    "status": "no_url", "reason": "no url_translation_en",
                })
                total_skipped += 1
                continue

            print(f"  [{n_processed+1}] {work_id}")
            n_processed += 1

            # Fetch text
            if source == "suttacentral":
                text = fetch_suttacentral(work_id, url_en)
            else:
                text = fetch_sacred_texts(work_id, url_en)

            if text is None:
                report_entries.append({
                    "work_id": work_id, "catalog": cat_name,
                    "status": "fetch_failed", "url": url_en,
                })
                total_failed += 1
                continue

            total_fetched += 1
            n_chars = len(text)
            n_words = len(text.split())
            print(f"    text: {n_chars} chars, {n_words} words")

            # Compute V14 signature (English)
            sig = freq_signature(text, lang="eng")
            top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]
            print(f"    sig top3: {[(a, round(v, 3)) for a, v in top3]}")

            # Match to graph node
            node_id = match_to_graph_node(work_id, nodes)
            matched = node_id is not None
            if not matched:
                node_id = work_id  # Use work_id as node_id placeholder
                print(f"    WARNING: no graph node match for {work_id}")

            # Build tradition label from catalog metadata
            tradition = nodes.get(node_id, {}).get(
                "tradition_label",
                w.get("tradition_micro", w.get("macro_culture", "UNKNOWN")),
            )

            entry = {
                "local_id": work_id,
                "graph_node_id": node_id,
                "catalog": cat_name,
                "tradition_label": tradition,
                "lang": "eng",
                "n_chars": n_chars,
                "n_words": n_words,
                "v14_signature": sig,
                "v14_top3": [[a, v] for a, v in top3],
                "matched": matched,
                "lexicon_version": "v212f",
                "source": source,
                "url": url_en,
            }
            signed_works.append(entry)
            total_signed += 1

            report_entries.append({
                "work_id": work_id, "catalog": cat_name,
                "status": "signed", "n_chars": n_chars,
                "top3": [[a, round(v, 4)] for a, v in top3],
            })

            if dry_run:
                print("  [dry-run] stopping after first work per catalog")
                break

        if limit > 0 and n_processed >= limit:
            break

    report = {
        "version": "v212f",
        "date": "2026-05-01",
        "lexicon_version": "v212f_lexicon",
        "lexicon_note": (
            "Reconstructed lexicon — original nipada_calibration_v177.py lost (Colab-only). "
            "Uses content-words-only V14 keyword lists. Self-consistent for new works; "
            "may not be numerically identical to v208 signatures for pre-existing works."
        ),
        "n_total_catalog": n_processed + total_skipped,
        "n_fetched": total_fetched,
        "n_signed": total_signed,
        "n_skipped_no_url": total_skipped,
        "n_failed": total_failed,
        "entries": report_entries,
    }

    return {"signed": signed_works, "report": report}


def save_outputs(data: dict, dry_run: bool = False) -> None:
    """Write signed_corpus_v212f.json and fetch_report_v212f.json."""
    signed = data["signed"]
    report = data["report"]

    corpus_out = {
        "version": "v212f",
        "date": "2026-05-01",
        "lexicon_version": "v212f_lexicon",
        "lexicon_note": report["lexicon_note"],
        "n_signed": len(signed),
        "v14_atoms": V14_ATOMS,
        "signed": signed,
    }

    if dry_run:
        print("\n[dry-run] Output preview (first 2 signed works):")
        for entry in signed[:2]:
            print(f"  {entry['work_id'] if 'work_id' in entry else entry['local_id']}")
            print(f"    top3: {entry['v14_top3']}")
        return

    out_corpus = CORPUS_DIR / "signed_corpus_v212f.json"
    out_report = FALSI_DIR / "nipada_v212f_fetch_report.json"

    with open(out_corpus, "w", encoding="utf-8") as f:
        json.dump(corpus_out, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_corpus}")

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote: {out_report}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="§212-fetch: V14 corpus harvester")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch only first work per catalog, no file writes")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process at most N works total (0 = no limit)")
    args = parser.parse_args()

    print("=" * 60)
    print("§212-fetch: NIPADA V14 corpus harvester")
    print(f"  dry_run={args.dry_run}, limit={args.limit}")
    print(f"  nipada dir: {_NIPADA}")
    print(f"  cache dir:  {CACHE_DIR}")
    print("=" * 60)

    import datetime
    t0 = datetime.datetime.now()

    data = process_catalogs(dry_run=args.dry_run, limit=args.limit)
    save_outputs(data, dry_run=args.dry_run)

    elapsed = (datetime.datetime.now() - t0).total_seconds()
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Signed: {data['report']['n_signed']}")
    print(f"Failed: {data['report']['n_failed']}")
    print(f"Skipped (no URL): {data['report']['n_skipped_no_url']}")


if __name__ == "__main__":
    main()

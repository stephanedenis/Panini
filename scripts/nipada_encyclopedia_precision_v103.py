#!/usr/bin/env python3
"""
§103 — Fondations de précision : géographie / temps / individu / événement
===========================================================================

Extension des schémas §101 avec quatre raffinements simultanés :

1. **Géographie à précision variable** — depuis la planète (1e7 m) jusqu'au
   temps de Planck spatial (1.6e-35 m). Toute source vague reste vague,
   toute mesure précise va jusqu'au quantique. Échelle exposée comme
   `precision_class` symbolique + `precision_meters` numérique.

2. **Temps à précision variable** — depuis l'éon géologique (~1e16 s)
   jusqu'au temps de Planck (5.4e-44 s). Inclut `epoque_historique` (déjà
   §101) comme classe parmi d'autres.

3. **Généalogie comme structure de l'individu** — un auteur n'est plus un
   point isolé : il est défini *par* sa lignée et son parcours. On ajoute
   `genealogie.parents` et `genealogie.enfants` à l'auteur.

4. **Événement** comme nouvelle classe d'entité — avec ou sans nom,
   toujours avec cause(s) et effet(s). Signature nipada :
     ÉVÉNEMENT = 2730 = 2·3·5·7·13 (sans sujet)
     ÉVÉNEMENT_INDIVIDUEL = 30030 = 2·3·5·7·11·13 = ω_V6 (avec sujet)
   Note : 30030 est la molécule maximale V6 — un événement avec sujet
   instancie tous les primes V6 simultanément.

Sortie :
  - research/nipada/encyclopedie/precisions.json
  - research/nipada/encyclopedie/evenements_seed.json
  - research/nipada/encyclopedie/auteurs_genealogie.json
  - research/nipada/encyclopedie/molecules_causales.json
"""

from __future__ import annotations

import json
from functools import reduce
from operator import mul
from pathlib import Path
from typing import TypedDict

REPO_ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"


# ══════════════════════════════════════════════════════════════════════════════
# 1. ÉCHELLES DE PRÉCISION
# ══════════════════════════════════════════════════════════════════════════════

# (class, meters, exemple) — du vague au précis
PRECISIONS_GEO: list[tuple[str, float, str]] = [
    ("planete",         1.0e7,    "Terre"),
    ("continent",       5.0e6,    "Eurasie"),
    ("subcontinent",    2.0e6,    "Asie du Sud"),
    ("pays",            5.0e5,    "France"),
    ("region",          1.0e5,    "Toscane"),
    ("departement",     5.0e4,    "Île-de-France"),
    ("ville",           1.0e4,    "Firenze"),
    ("quartier",        1.0e3,    "Trastevere"),
    ("rue",             1.0e2,    "Via Calzaiuoli"),
    ("adresse",         1.0e1,    "Casa di Dante, Florence"),
    ("piece",           1.0e0,    "salle d'étude"),
    ("objet",           1.0e-1,   "boîte de manuscrits"),
    ("centimetre",      1.0e-2,   "tache d'encre"),
    ("millimetre",      1.0e-3,   "trait de lettre"),
    ("micrometre",      1.0e-6,   "fibre"),
    ("nanometre",       1.0e-9,   "molécule"),
    ("angstrom",        1.0e-10,  "atome"),
    ("picometre",       1.0e-12,  "noyau"),
    ("femtometre",      1.0e-15,  "nucléon"),
    ("attometre",       1.0e-18,  "sub-nucléonique"),
    ("planck_length",   1.616e-35, "longueur de Planck"),
]

# (class, secondes, exemple)
PRECISIONS_TEMPS: list[tuple[str, float, str]] = [
    ("eon_geologique",        1.0e16,    "Phanérozoïque"),
    ("ere_geologique",        1.0e14,    "Cénozoïque"),
    ("periode_geologique",    1.0e13,    "Quaternaire"),
    ("epoque_geologique",     1.0e12,    "Holocène"),
    ("epoque_historique",     1.0e10,    "Antiquité classique (≈1300 ans)"),
    ("siecle",                3.156e9,   "XIIe siècle"),
    ("decennie",              3.156e8,   "années 1880"),
    ("annee",                 3.156e7,   "1786"),
    ("mois",                  2.628e6,   "mai 1786"),
    ("jour",                  8.640e4,   "3 septembre 1786"),
    ("heure",                 3.6e3,     "14h"),
    ("minute",                6.0e1,     "14:30"),
    ("seconde",               1.0e0,     "14:30:22"),
    ("milliseconde",          1.0e-3,    "réaction nerveuse"),
    ("microseconde",          1.0e-6,    "switching électronique"),
    ("nanoseconde",           1.0e-9,    "horloge atomique"),
    ("picoseconde",           1.0e-12,   "vibration moléculaire"),
    ("femtoseconde",          1.0e-15,   "rotation électronique"),
    ("attoseconde",           1.0e-18,   "saut électronique"),
    ("zeptoseconde",          1.0e-21,   "désintégration faible"),
    ("yoctoseconde",          1.0e-24,   "interactions nucléaires"),
    ("planck_time",           5.391e-44, "temps de Planck"),
]


def _index_precisions(seq: list[tuple[str, float, str]]) -> dict[str, dict]:
    return {cls: {"value": v, "exemple": ex, "rank": i}
            for i, (cls, v, ex) in enumerate(seq)}


PRECISIONS_GEO_INDEX = _index_precisions(PRECISIONS_GEO)
PRECISIONS_TEMPS_INDEX = _index_precisions(PRECISIONS_TEMPS)


# ══════════════════════════════════════════════════════════════════════════════
# 2. NOUVELLES MOLÉCULES (CAUSALITÉ, ÉVÉNEMENT, GÉNÉALOGIE)
# ══════════════════════════════════════════════════════════════════════════════

PRIMES = {"ÊTRE": 2, "DIFFÉRENCE": 3, "RAPPORT": 5, "ORIENTATION": 7,
          "SUJET": 11, "TEMPS": 13, "MODALITÉ": 17}

MOLECULES_CAUSALES: dict[int, dict] = {
    55: {
        "name": "LIEN_GÉNÉALOGIQUE",
        "atoms": [5, 11],
        "usage": "RAPPORT × SUJET — lien dirigé entre deux sujets (parent → enfant, maître → disciple)",
    },
    195: {
        "name": "CAUSALITÉ",
        "atoms": [3, 5, 13],
        "usage": "DIFFÉRENCE × RAPPORT × TEMPS — cause ≠ effet, en rapport, ordonnés temporellement",
    },
    715: {
        "name": "CAUSALITÉ_INDIVIDUÉE",
        "atoms": [5, 11, 13],
        "usage": "RAPPORT × SUJET × TEMPS — un sujet cause/subit dans le temps (sans DIFFÉRENCE explicite)",
    },
    2145: {
        "name": "CAUSALITÉ_DIFFÉRENCIÉE",
        "atoms": [3, 5, 11, 13],
        "usage": "CAUSALITÉ + SUJET — sujet auteur d'une distinction temporelle (action efficace)",
    },
    2730: {
        "name": "ÉVÉNEMENT",
        "atoms": [2, 3, 5, 7, 13],
        "usage": "ÊTRE × DIFFÉRENCE × RAPPORT × ORIENTATION × TEMPS — événement sans sujet (séisme, éclipse)",
    },
    30030: {
        "name": "ÉVÉNEMENT_INDIVIDUEL",
        "atoms": [2, 3, 5, 7, 11, 13],
        "usage": "ω_V6 — événement avec sujet, instancie tous les 6 primes V6 simultanément",
    },
    510510: {
        "name": "ÉVÉNEMENT_MODAL",
        "atoms": [2, 3, 5, 7, 11, 13, 17],
        "usage": "ω_V7 — événement avec sujet et modalité (planifié, hypothétique, attendu)",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# 3. SCHÉMAS
# ══════════════════════════════════════════════════════════════════════════════

class DateImprecise(TypedDict):
    iso: str                       # "-0399", "1786-09-03", etc.
    precision_class: str           # une clé de PRECISIONS_TEMPS_INDEX
    precision_seconds: float
    uncertain: bool                # True si la valeur ISO elle-même est incertaine
    notes: str


class LieuPrecis(TypedDict):
    place_id: str                  # référence vers lieux_zones.json
    precision_class: str           # une clé de PRECISIONS_GEO_INDEX
    precision_meters: float
    specific_location: str | None  # localisation plus fine (texte libre, optionnel)
    coords_override: list[float] | None  # [lat, lon] ou [lat, lon, alt] si précision le justifie
    uncertain: bool


class LienGenealogique(TypedDict):
    relation: str                  # "pere" / "mere" / "fils" / "fille" / "frere" / "soeur" / "maitre" / "disciple"
    nipada_type: int               # 55 = LIEN_GÉNÉALOGIQUE
    name: str
    name_native_script: str
    dates_iso: list[str] | None    # [naissance, mort] si connu
    auteur_id: str | None          # référence vers auteurs_seed.json si l'individu y est
    notes: str


class Genealogie(TypedDict):
    auteur_id: str
    parents: list[LienGenealogique]
    enfants: list[LienGenealogique]
    fratrie: list[LienGenealogique]
    maitres: list[LienGenealogique]
    notes: str


class Evenement(TypedDict):
    id: str
    nipada_type: int               # 2730 ou 30030 (ou 510510 si modal)
    nipada_atoms: list[int]
    has_sujets: bool
    name: str | None               # NULL si événement sans nom (anonyme)
    name_native: str | None
    description: str
    date: DateImprecise
    duration_seconds: float | None # durée si l'événement n'est pas ponctuel
    lieu: LieuPrecis
    sujets: list[str]              # auteur_ids impliqués (peut être vide)
    causes: list[str]              # event_ids antécédents
    effets: list[str]              # event_ids conséquents
    notes: str


# ══════════════════════════════════════════════════════════════════════════════
# 4. SEED — GÉNÉALOGIES (5 auteurs bien documentés)
# ══════════════════════════════════════════════════════════════════════════════

GENEALOGIES: list[Genealogie] = [
    {
        "auteur_id": "kongzi",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Shū Liánghé", "name_native_script": "叔梁紇",
             "dates_iso": ["-0622", "-0549"], "auteur_id": None,
             "notes": "officier militaire de l'État de Lu"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Yán Zhēngzài", "name_native_script": "顏徵在",
             "dates_iso": None, "auteur_id": None,
             "notes": "concubine, élève selon la tradition"},
        ],
        "enfants": [
            {"relation": "fils", "nipada_type": 55,
             "name": "Kǒng Lǐ", "name_native_script": "孔鯉",
             "dates_iso": ["-0532", "-0481"], "auteur_id": None,
             "notes": "« Bóyú », père du transmetteur Kǒng Jí (Zǐsī)"},
        ],
        "fratrie": [],
        "maitres": [
            {"relation": "maitre", "nipada_type": 55,
             "name": "Lǎozǐ", "name_native_script": "老子",
             "dates_iso": None, "auteur_id": None,
             "notes": "rencontre légendaire (Shǐjì); historicité débattue"},
        ],
        "notes": "Lignée Kǒng documentée sur 80+ générations jusqu'aujourd'hui.",
    },
    {
        "auteur_id": "platon",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Aristōn", "name_native_script": "Ἀρίστων",
             "dates_iso": None, "auteur_id": None,
             "notes": "noble athénien, descendance attribuée au roi Codros"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Periktiónē", "name_native_script": "Περικτιόνη",
             "dates_iso": None, "auteur_id": None,
             "notes": "apparentée au législateur Solon"},
        ],
        "enfants": [],  # Platon n'a pas eu d'enfants attestés
        "fratrie": [
            {"relation": "frere", "nipada_type": 55,
             "name": "Glaúkōn", "name_native_script": "Γλαύκων",
             "dates_iso": None, "auteur_id": None,
             "notes": "personnage majeur de la République"},
            {"relation": "frere", "nipada_type": 55,
             "name": "Adeímantos", "name_native_script": "Ἀδείμαντος",
             "dates_iso": None, "auteur_id": None,
             "notes": "co-interlocuteur dans la République"},
        ],
        "maitres": [
            {"relation": "maitre", "nipada_type": 55,
             "name": "Sōkrátēs", "name_native_script": "Σωκράτης",
             "dates_iso": ["-0470", "-0399"], "auteur_id": None,
             "notes": "maître ; voir événement mort_socrate"},
        ],
        "notes": "Lignée aristocratique, parenté avec Critias et Charmide (oligarques).",
    },
    {
        "auteur_id": "dante",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Alighiero di Bellincione",
             "name_native_script": "Alighiero di Bellincione",
             "dates_iso": [None, "1283"], "auteur_id": None,
             "notes": "notaire ou changeur, mort quand Dante avait ~10 ans"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Bella degli Abati", "name_native_script": "Bella degli Abati",
             "dates_iso": [None, "1270"], "auteur_id": None,
             "notes": "décédée quand Dante était enfant"},
        ],
        "enfants": [
            {"relation": "fils", "nipada_type": 55,
             "name": "Pietro Alighieri", "name_native_script": "Pietro Alighieri",
             "dates_iso": ["1300", "1364"], "auteur_id": None,
             "notes": "juriste, premier commentateur de la Commedia"},
            {"relation": "fils", "nipada_type": 55,
             "name": "Jacopo Alighieri", "name_native_script": "Jacopo Alighieri",
             "dates_iso": ["1289", "1348"], "auteur_id": None,
             "notes": "auteur du Dottrinale en terza rima"},
            {"relation": "fille", "nipada_type": 55,
             "name": "Antonia Alighieri (Suor Beatrice)",
             "name_native_script": "Antonia Alighieri",
             "dates_iso": None, "auteur_id": None,
             "notes": "religieuse à Ravenne ; nom monastique Beatrice"},
        ],
        "fratrie": [],
        "maitres": [
            {"relation": "maitre", "nipada_type": 55,
             "name": "Brunetto Latini", "name_native_script": "Brunetto Latini",
             "dates_iso": ["1220", "1294"], "auteur_id": None,
             "notes": "maître florentin, rencontré dans Inferno XV"},
        ],
        "notes": "Mariage avec Gemma Donati (~1285), promis à 12 ans.",
    },
    {
        "auteur_id": "goethe",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Johann Caspar Goethe",
             "name_native_script": "Johann Caspar Goethe",
             "dates_iso": ["1710", "1782"], "auteur_id": None,
             "notes": "Kaiserlicher Rat, juriste, bibliophile"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Catharina Elisabeth Textor",
             "name_native_script": "Catharina Elisabeth Textor",
             "dates_iso": ["1731", "1808"], "auteur_id": None,
             "notes": "« Frau Aja », fille du Schultheiss de Frankfurt"},
        ],
        "enfants": [
            {"relation": "fils", "nipada_type": 55,
             "name": "Julius August Walther von Goethe",
             "name_native_script": "August von Goethe",
             "dates_iso": ["1789", "1830"], "auteur_id": None,
             "notes": "seul des 5 enfants à atteindre l'âge adulte"},
        ],
        "fratrie": [
            {"relation": "soeur", "nipada_type": 55,
             "name": "Cornelia Friederica Christiana Goethe",
             "name_native_script": "Cornelia Goethe",
             "dates_iso": ["1750", "1777"], "auteur_id": None,
             "notes": "confidente intellectuelle de jeunesse"},
        ],
        "maitres": [],
        "notes": "Christiane Vulpius compagne dès 1788, mariage 1806.",
    },
    {
        "auteur_id": "tagore",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Debendranath Thakur",
             "name_native_script": "দেবেন্দ্রনাথ ঠাকুর",
             "dates_iso": ["1817", "1905"], "auteur_id": None,
             "notes": "réformateur Brahmo Samaj, philosophe"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Sarada Devi", "name_native_script": "সারদা দেবী",
             "dates_iso": [None, "1875"], "auteur_id": None,
             "notes": "morte alors que Rabindranath avait 14 ans"},
        ],
        "enfants": [
            {"relation": "fille", "nipada_type": 55,
             "name": "Madhurilata Devi",
             "name_native_script": "মাধুরীলতা দেবী",
             "dates_iso": ["1886", "1918"], "auteur_id": None,
             "notes": "« Bela », aînée"},
        ],
        "fratrie": [
            {"relation": "frere", "nipada_type": 55,
             "name": "Dwijendranath Thakur",
             "name_native_script": "দ্বিজেন্দ্রনাথ ঠাকুর",
             "dates_iso": ["1840", "1926"], "auteur_id": None,
             "notes": "philosophe, mathématicien, traducteur du Mégha-dūta"},
            {"relation": "frere", "nipada_type": 55,
             "name": "Jyotirindranath Thakur",
             "name_native_script": "জ্যোতিরিন্দ্রনাথ ঠাকুর",
             "dates_iso": ["1849", "1925"], "auteur_id": None,
             "notes": "compositeur, mentor musical de Rabindranath"},
        ],
        "maitres": [],
        "notes": "Famille Thakur (anglicisée Tagore) — 14 frères/sœurs au total. "
                 "Mariage 1883 avec Mrinalini Devi.",
    },
    {
        "auteur_id": "borges",
        "parents": [
            {"relation": "pere", "nipada_type": 55,
             "name": "Jorge Guillermo Borges Haslam",
             "name_native_script": "Jorge Guillermo Borges Haslam",
             "dates_iso": ["1874", "1938"], "auteur_id": None,
             "notes": "avocat, professeur d'anglais, écrivain (El caudillo)"},
            {"relation": "mere", "nipada_type": 55,
             "name": "Leonor Acevedo Suárez",
             "name_native_script": "Leonor Acevedo Suárez",
             "dates_iso": ["1876", "1975"], "auteur_id": None,
             "notes": "lectrice et secrétaire de Borges après sa cécité"},
        ],
        "enfants": [],
        "fratrie": [
            {"relation": "soeur", "nipada_type": 55,
             "name": "Norah Borges Acevedo",
             "name_native_script": "Norah Borges",
             "dates_iso": ["1901", "1998"], "auteur_id": None,
             "notes": "peintre, illustratrice ; vit à Buenos Aires"},
        ],
        "maitres": [],
        "notes": "Bilinguisme es/en transmis par grand-mère paternelle Fanny Haslam (anglaise). "
                 "Mariage tardif avec María Kodama (1986), peu avant sa mort.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# 5. SEED — ÉVÉNEMENTS (graphe causal de 8 entrées)
# ══════════════════════════════════════════════════════════════════════════════

EVENEMENTS: list[Evenement] = [
    {
        "id": "naissance_panini",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Naissance de Pāṇini",
        "name_native": "पाणिनेः जन्म",
        "description": "Naissance du grammairien Pāṇini quelque part en Gandhāra. "
                       "Date traditionnelle conventionnelle : ~500 AEC. "
                       "Précision : époque (incertitude de 50 à 100 ans).",
        "date": {"iso": "-0500", "precision_class": "epoque_historique",
                 "precision_seconds": 1.0e10, "uncertain": True,
                 "notes": "Estimation moderne entre -550 et -450"},
        "duration_seconds": None,
        "lieu": {"place_id": "indus_gandhara", "precision_class": "subcontinent",
                 "precision_meters": 2.0e6, "specific_location": "Śalātura (probablement Lahor, Pakistan)",
                 "coords_override": None, "uncertain": True},
        "sujets": ["panini"],
        "causes": [],
        "effets": ["composition_astadhyayi"],
        "notes": "Précision spatiale faible (subcontinent) malgré localisation traditionnelle "
                 "Śalātura — la village reste contesté.",
    },
    {
        "id": "composition_astadhyayi",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Composition de l'Aṣṭādhyāyī",
        "name_native": "अष्टाध्यायी",
        "description": "Rédaction du traité grammatical en 3959 sūtras "
                       "organisés en 8 chapitres (aṣṭa-adhyāyī).",
        "date": {"iso": "-0460", "precision_class": "decennie",
                 "precision_seconds": 3.156e8, "uncertain": True,
                 "notes": "Période d'activité créatrice présumée"},
        "duration_seconds": 3.156e8,   # ~10 ans
        "lieu": {"place_id": "indus_gandhara", "precision_class": "region",
                 "precision_meters": 1.0e5, "specific_location": None,
                 "coords_override": None, "uncertain": True},
        "sujets": ["panini"],
        "causes": ["naissance_panini"],
        "effets": [],
        "notes": "Texte oral à l'origine ; transmission orale stricte sur des siècles "
                 "avant fixation écrite.",
    },
    {
        "id": "mort_socrate",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Mort de Socrate",
        "name_native": "Σωκράτους θάνατος",
        "description": "Exécution de Socrate par ciguë à Athènes après procès "
                       "pour impiété et corruption de la jeunesse.",
        "date": {"iso": "-0399", "precision_class": "annee",
                 "precision_seconds": 3.156e7, "uncertain": False,
                 "notes": "Mois et jour exact non datables au calendrier moderne"},
        "duration_seconds": None,
        "lieu": {"place_id": "attique", "precision_class": "adresse",
                 "precision_meters": 1.0e1,
                 "specific_location": "prison d'État, Athènes",
                 "coords_override": [37.9710, 23.7240], "uncertain": False},
        "sujets": [],   # Socrate n'est pas dans nos 12 auteurs
        "causes": [],
        "effets": ["exil_platon"],
        "notes": "Précision spatiale élevée (l'enclos de la prison est archéologiquement "
                 "identifié) malgré l'imprécision temporelle (année connue, jour non).",
    },
    {
        "id": "exil_platon",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Voyages de Platon",
        "name_native": "Πλάτωνος ἀποδημίαι",
        "description": "Période d'errance après la mort de Socrate : Mégare, Cyrène, "
                       "Égypte, Italie, Sicile (cour de Denys l'Ancien).",
        "date": {"iso": "-0399", "precision_class": "annee",
                 "precision_seconds": 3.156e7, "uncertain": False,
                 "notes": "Date de départ approximative"},
        "duration_seconds": 12 * 3.156e7,   # ~12 ans
        "lieu": {"place_id": "grece_helleno", "precision_class": "subcontinent",
                 "precision_meters": 2.0e6, "specific_location": "Méditerranée orientale",
                 "coords_override": None, "uncertain": False},
        "sujets": ["platon"],
        "causes": ["mort_socrate"],
        "effets": ["fondation_academie"],
        "notes": "Précision géographique délibérément faible : l'événement "
                 "est multi-localisé par essence.",
    },
    {
        "id": "fondation_academie",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Fondation de l'Académie",
        "name_native": "Ἀκαδημεία",
        "description": "Création par Platon de l'école philosophique dans le bois "
                       "sacré du héros Akadēmos, au nord-ouest d'Athènes.",
        "date": {"iso": "-0387", "precision_class": "annee",
                 "precision_seconds": 3.156e7, "uncertain": True,
                 "notes": "Date traditionnelle ; -388 à -386 selon les sources"},
        "duration_seconds": None,
        "lieu": {"place_id": "attique", "precision_class": "rue",
                 "precision_meters": 1.0e2,
                 "specific_location": "bois d'Akadēmos, banlieue NW d'Athènes",
                 "coords_override": [37.9886, 23.7106], "uncertain": False},
        "sujets": ["platon"],
        "causes": ["exil_platon"],
        "effets": [],
        "notes": "Site archéologique modernement appelé Akadēmia Plátōnos, conservé "
                 "comme parc à Athènes.",
    },
    {
        "id": "exil_dante",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Exil de Dante",
        "name_native": "Esilio di Dante Alighieri",
        "description": "Condamnation à mort par contumace par les Guelfes Noirs "
                       "de Florence, exil perpétuel à partir du 27 janvier 1302.",
        "date": {"iso": "1302-01-27", "precision_class": "jour",
                 "precision_seconds": 8.640e4, "uncertain": False,
                 "notes": "Premier décret ; second décret confirmant la peine de mort 10 mars 1302"},
        "duration_seconds": (1321 - 1302) * 3.156e7,
        "lieu": {"place_id": "toscane_firenze", "precision_class": "ville",
                 "precision_meters": 1.0e4,
                 "specific_location": "Florence (sentence émise) ; Forlì, Vérone, Ravenne (résidences successives)",
                 "coords_override": None, "uncertain": False},
        "sujets": ["dante"],
        "causes": [],
        "effets": ["composition_commedia"],
        "notes": "Précision temporelle au jour ; précision spatiale variable car "
                 "l'exil est multi-localisé (durée ≠ point).",
    },
    {
        "id": "composition_commedia",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Composition de la Commedia",
        "name_native": "La Comedìa",
        "description": "Rédaction des trois cantiques (Inferno, Purgatorio, Paradiso) "
                       "pendant l'exil ; achevée peu avant la mort à Ravenne.",
        "date": {"iso": "1308", "precision_class": "annee",
                 "precision_seconds": 3.156e7, "uncertain": True,
                 "notes": "Inferno commencé vers 1308 ; Paradiso achevé 1320-1321"},
        "duration_seconds": (1321 - 1308) * 3.156e7,
        "lieu": {"place_id": "toscane_firenze", "precision_class": "region",
                 "precision_meters": 1.0e5,
                 "specific_location": "Vérone, Lucques, Ravenne (lieux d'exil successifs)",
                 "coords_override": None, "uncertain": False},
        "sujets": ["dante"],
        "causes": ["exil_dante"],
        "effets": [],
        "notes": "Le titre « Divina » a été ajouté par Boccaccio plus tard.",
    },
    {
        "id": "voyage_italien_goethe",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Italienische Reise",
        "name_native": "Italienische Reise",
        "description": "Voyage incognito de Goethe sous le pseudonyme « Filippo Möller » "
                       "à travers l'Italie : Vérone, Venise, Roma, Napoli, Sicilia.",
        "date": {"iso": "1786-09-03", "precision_class": "jour",
                 "precision_seconds": 8.640e4, "uncertain": False,
                 "notes": "Départ secret de Karlsbad le 3 septembre 1786 à 3h du matin"},
        "duration_seconds": (1788 - 1786) * 3.156e7 + 5 * 2.628e6,   # ~21 mois
        "lieu": {"place_id": "toscane_firenze", "precision_class": "subcontinent",
                 "precision_meters": 2.0e6,
                 "specific_location": "Italie : Vérone → Venezia → Roma → Napoli → Sicilia → Roma",
                 "coords_override": None, "uncertain": False},
        "sujets": ["goethe"],
        "causes": [],
        "effets": [],
        "notes": "Précision temporelle au jour (départ documenté à l'heure) ; "
                 "précision spatiale délibérément faible car événement multi-site.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

def _load_v101() -> tuple[set[str], set[str]]:
    auteurs_path = ENC_DIR / "auteurs_seed.json"
    lieux_path = ENC_DIR / "lieux_zones.json"
    if not auteurs_path.exists() or not lieux_path.exists():
        raise FileNotFoundError(f"§101 manquant — exécuter d'abord nipada_encyclopedia_seed_v101.py")
    with auteurs_path.open(encoding="utf-8") as f:
        auteur_ids = {a["id"] for a in json.load(f)["auteurs"]}
    with lieux_path.open(encoding="utf-8") as f:
        lieu_ids = {l["id"] for l in json.load(f)["lieux"]}
    return auteur_ids, lieu_ids


def _validate() -> list[str]:
    errors = []
    auteur_ids, lieu_ids = _load_v101()

    # 1. Cohérence atomique des nouvelles molécules
    for n, info in MOLECULES_CAUSALES.items():
        prod = reduce(mul, info["atoms"])
        if prod != n:
            errors.append(f"MOLECULES_CAUSALES/{n} ({info['name']}): ∏{info['atoms']}={prod} ≠ {n}")

    # 2. Précisions : valeurs strictement décroissantes
    for label, seq in [("GEO", PRECISIONS_GEO), ("TEMPS", PRECISIONS_TEMPS)]:
        for i in range(len(seq) - 1):
            if seq[i][1] <= seq[i + 1][1]:
                errors.append(f"PRECISIONS_{label}: ordre violé entre {seq[i][0]} et {seq[i+1][0]}")

    # 3. Généalogies : chaque auteur_id doit exister
    seen = set()
    for g in GENEALOGIES:
        if g["auteur_id"] not in auteur_ids:
            errors.append(f"GENEALOGIES/{g['auteur_id']}: auteur inconnu")
        if g["auteur_id"] in seen:
            errors.append(f"GENEALOGIES: doublon pour {g['auteur_id']}")
        seen.add(g["auteur_id"])
        # tous les liens doivent porter nipada_type=55
        for bucket in ("parents", "enfants", "fratrie", "maitres"):
            for lk in g[bucket]:
                if lk["nipada_type"] != 55:
                    errors.append(f"GENEALOGIES/{g['auteur_id']}/{bucket}/{lk['name']}: nipada_type {lk['nipada_type']} ≠ 55")

    # 4. Événements : références et cohérence atomique
    event_ids = {e["id"] for e in EVENEMENTS}
    for e in EVENEMENTS:
        prod = reduce(mul, e["nipada_atoms"])
        if prod != e["nipada_type"]:
            errors.append(f"EVENEMENTS/{e['id']}: ∏{e['nipada_atoms']}={prod} ≠ {e['nipada_type']}")
        # type cohérent avec has_sujets
        if e["has_sujets"] and 11 not in e["nipada_atoms"]:
            errors.append(f"EVENEMENTS/{e['id']}: has_sujets=True mais SUJET(11) absent des atomes")
        if not e["has_sujets"] and 11 in e["nipada_atoms"]:
            errors.append(f"EVENEMENTS/{e['id']}: has_sujets=False mais SUJET(11) présent dans les atomes")
        # sujets connus
        for s in e["sujets"]:
            if s not in auteur_ids:
                errors.append(f"EVENEMENTS/{e['id']}.sujets → '{s}' inconnu dans auteurs_seed")
        # lieu connu
        pid = e["lieu"]["place_id"]
        if pid not in lieu_ids:
            errors.append(f"EVENEMENTS/{e['id']}.lieu → '{pid}' inconnu dans lieux_zones")
        # précisions valides
        if e["lieu"]["precision_class"] not in PRECISIONS_GEO_INDEX:
            errors.append(f"EVENEMENTS/{e['id']}.lieu.precision_class '{e['lieu']['precision_class']}' invalide")
        if e["date"]["precision_class"] not in PRECISIONS_TEMPS_INDEX:
            errors.append(f"EVENEMENTS/{e['id']}.date.precision_class '{e['date']['precision_class']}' invalide")
        # causes/effets référencent des événements existants
        for ref_field in ("causes", "effets"):
            for ref in e[ref_field]:
                if ref not in event_ids:
                    errors.append(f"EVENEMENTS/{e['id']}.{ref_field} → '{ref}' inconnu")

    # 5. Symétrie causes ↔ effets
    by_id = {e["id"]: e for e in EVENEMENTS}
    for e in EVENEMENTS:
        for cause_id in e["causes"]:
            if e["id"] not in by_id[cause_id]["effets"]:
                errors.append(f"EVENEMENTS/{cause_id}.effets manque '{e['id']}' (asymétrie causale)")
        for effet_id in e["effets"]:
            if e["id"] not in by_id[effet_id]["causes"]:
                errors.append(f"EVENEMENTS/{effet_id}.causes manque '{e['id']}' (asymétrie causale)")

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    W = 78
    print("═" * W)
    print("  §103 — Fondations de précision : géo / temps / individu / événement")
    print("═" * W)
    print(f"\n  Précisions GEO     : {len(PRECISIONS_GEO):2d} classes "
          f"({PRECISIONS_GEO[0][1]:.0e} m → {PRECISIONS_GEO[-1][1]:.0e} m)")
    print(f"  Précisions TEMPS   : {len(PRECISIONS_TEMPS):2d} classes "
          f"({PRECISIONS_TEMPS[0][1]:.0e} s → {PRECISIONS_TEMPS[-1][1]:.0e} s)")
    print(f"  Molécules causales : {len(MOLECULES_CAUSALES):2d}")
    print(f"  Généalogies        : {len(GENEALOGIES):2d} auteurs enrichis")
    print(f"  Événements         : {len(EVENEMENTS):2d} (graphe causal)")

    print("\n  ── Validation ──")
    errors = _validate()
    if errors:
        for e in errors:
            print(f"    ✗ {e}")
        raise SystemExit(1)
    print("  ✓ molécules causales : produits primes cohérents")
    print("  ✓ précisions : ordres strictement décroissants")
    print("  ✓ généalogies : auteur_ids existants, liens type 55")
    print("  ✓ événements : ∏atoms == type, has_sujets ↔ SUJET(11)")
    print("  ✓ événements : références sujets/lieux valides")
    print("  ✓ événements : graphe causal symétrique (causes ↔ effets)")

    ENC_DIR.mkdir(parents=True, exist_ok=True)
    out_prec = ENC_DIR / "precisions.json"
    out_mol = ENC_DIR / "molecules_causales.json"
    out_gen = ENC_DIR / "auteurs_genealogie.json"
    out_evt = ENC_DIR / "evenements_seed.json"

    with out_prec.open("w", encoding="utf-8") as f:
        json.dump({
            "version": "§103",
            "geo":   {"index": PRECISIONS_GEO_INDEX,   "ordered": [list(t) for t in PRECISIONS_GEO]},
            "temps": {"index": PRECISIONS_TEMPS_INDEX, "ordered": [list(t) for t in PRECISIONS_TEMPS]},
        }, f, ensure_ascii=False, indent=2)
    with out_mol.open("w", encoding="utf-8") as f:
        json.dump({"version": "§103", "primes": PRIMES,
                   "molecules": MOLECULES_CAUSALES}, f, ensure_ascii=False, indent=2)
    with out_gen.open("w", encoding="utf-8") as f:
        json.dump({"version": "§103", "genealogies": GENEALOGIES},
                  f, ensure_ascii=False, indent=2)
    with out_evt.open("w", encoding="utf-8") as f:
        json.dump({"version": "§103", "evenements": EVENEMENTS},
                  f, ensure_ascii=False, indent=2)

    print("\n  ── Graphe causal ──")
    by_id = {e["id"]: e for e in EVENEMENTS}
    for e in EVENEMENTS:
        causes = ", ".join(e["causes"]) or "—"
        effets = ", ".join(e["effets"]) or "—"
        prec_t = e["date"]["precision_class"]
        prec_g = e["lieu"]["precision_class"]
        print(f"    {e['id']:<28s} t={prec_t:<18s} g={prec_g:<14s}")
        print(f"      cause: {causes}")
        print(f"      effet: {effets}")

    print(f"\n  Sortie :")
    for p in (out_prec, out_mol, out_gen, out_evt):
        print(f"    {p.relative_to(REPO_ROOT)}")
    print("═" * W)


if __name__ == "__main__":
    main()

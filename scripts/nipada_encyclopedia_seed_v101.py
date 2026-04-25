#!/usr/bin/env python3
"""
§101 — Encyclopédie nipada : où / quand / qui (seed initial)
=============================================================
Pivot programme : on quitte la falsification du classifieur pour bâtir
l'encyclopédie qui permettra de **reconstituer fidèlement tout texte**
par le parcours linguistique de son auteur (lieu × temps × langue dominante
à chaque période de sa vie).

Architecture :
  Trois axes fondamentaux, ancrés sur les 6 primes nipada V6.

  ── QUAND (TEMPS=13) ────────────────────────────────────────────────────
  Les époques sont des DURÉE(65) ordonnées par SUCCESSION(273).
  Une date isolée est une PRÉSENCE_T(286 = 2×11×13).

  ── OÙ (ORIENTATION=7) ──────────────────────────────────────────────────
  Un lieu est un ÊTRE localisé : LOCALISATION(14 = 2×7).
  Une zone linguistique-civilisationnelle hérite cette signature, augmentée
  d'attributs : famille de langues, période d'activité, coordonnées.

  ── QUI (SUJET=11) ──────────────────────────────────────────────────────
  Un auteur est ancré en COORDONNÉE_VITALE(2002 = 2×7×11×13) :
  un être localisé en un lieu, individuel, dans le temps.
  Il porte des **variantes nominatives** par script et par traduction,
  et une **trajectoire** = liste de (période × lieu × langue dominante).

Sortie (3 JSON dans research/nipada/encyclopedie/) :
  - temps_epoques.json   — 8 époques fondatrices
  - lieux_zones.json     — 18 zones linguistiques-civilisationnelles
  - auteurs_seed.json    — 12 auteurs ancrés (Pāṇini → Borges)

Cette seed est volontairement parcimonieuse et **typologiquement large** :
chaque entrée illustre un cas de référence (script, famille, époque) qui
servira de prototype pour l'expansion ultérieure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"


# ── Décompositions premières (référence) ─────────────────────────────────────
# Reprend la convention V6 mais étend avec les molécules d'usage encyclopédique.

PRIMES = {"ÊTRE": 2, "DIFFÉRENCE": 3, "RAPPORT": 5, "ORIENTATION": 7,
          "SUJET": 11, "TEMPS": 13}

NIPADA_MOLECULES_GEO_TIME: dict[int, dict] = {
    # Pures
    7:    {"name": "ORIENTATION",     "atoms": [7],            "usage": "axe spatial pur"},
    11:   {"name": "SUJET",           "atoms": [11],           "usage": "identité individuelle"},
    13:   {"name": "TEMPS",           "atoms": [13],           "usage": "instant pur"},
    # Géographiques
    14:   {"name": "LOCALISATION",    "atoms": [2, 7],         "usage": "un être localisé = LIEU"},
    21:   {"name": "DIRECTION",       "atoms": [3, 7],         "usage": "orientation différentielle"},
    35:   {"name": "RELATION_SPATIALE","atoms": [5, 7],        "usage": "deux lieux en rapport"},
    77:   {"name": "LIEU_INDIVIDUEL", "atoms": [7, 11],        "usage": "un sujet localisé"},
    # Temporelles (V6)
    26:   {"name": "ÉVOLUTION",       "atoms": [2, 13],        "usage": "être dans la durée"},
    65:   {"name": "DURÉE",           "atoms": [5, 13],        "usage": "intervalle = ÉPOQUE"},
    273:  {"name": "SUCCESSION",      "atoms": [3, 7, 13],     "usage": "ordonnancement chronologique"},
    286:  {"name": "PRÉSENCE_T",      "atoms": [2, 11, 13],    "usage": "sujet à un instant"},
    1001: {"name": "DÉCISION",        "atoms": [7, 11, 13],    "usage": "sujet localisé temporellement (sans ÊTRE)"},
    # Composées encyclopédiques (nouvelles)
    154:  {"name": "PRÉSENCE_LOC",    "atoms": [2, 7, 11],     "usage": "sujet incarné en un lieu"},
    2002: {"name": "COORDONNÉE_VITALE","atoms": [2, 7, 11, 13],"usage": "ancrage auteur : être × lieu × sujet × temps"},
    182:  {"name": "AVANCEMENT",      "atoms": [2, 7, 13],     "usage": "trajectoire spatio-temporelle (sans SUJET)"},
}


# ══════════════════════════════════════════════════════════════════════════════
# SCHEMAS — TypedDict pour validation interne
# ══════════════════════════════════════════════════════════════════════════════

class Epoque(TypedDict):
    id: str
    nipada_type: int
    nipada_atoms: list[int]
    label_fr: str
    label_en: str
    interval_iso: list[str]      # [start, end] format ISO étendu (négatif = BCE)
    interval_label: str
    centroid_iso: str
    succession_prev: str | None
    succession_next: str | None
    notes: str


class Lieu(TypedDict):
    id: str
    nipada_type: int
    nipada_atoms: list[int]
    label_fr: str
    label_native: str
    label_native_script: str
    coords: list[float]          # [lat, lon] approx capitale ou centroïde
    famille_langues: str
    langues_majeures: list[str]
    epoques_actives: list[str]   # ids dans temps_epoques
    contenant: str | None        # id du lieu plus large


class TrajectoryStep(TypedDict):
    period_iso: list[str]
    place_id: str
    lang_dominant: str
    context: str


class Auteur(TypedDict):
    id: str
    nipada_type: int
    nipada_atoms: list[int]
    names: dict[str, list[str]]
    name_canonical: str
    name_canonical_lang: str
    etymology: str
    birth: dict
    death: dict | None
    epoch_primary: str
    languages: list[str]
    trajectory: list[TrajectoryStep]
    notes: str


# ══════════════════════════════════════════════════════════════════════════════
# SEED — TEMPS / ÉPOQUES (8)
# ══════════════════════════════════════════════════════════════════════════════

EPOQUES: list[Epoque] = [
    {
        "id": "antiquite_preclassique",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Antiquité préclassique",
        "label_en": "Pre-classical antiquity",
        "interval_iso": ["-3000", "-0800"],
        "interval_label": "−III mil. – VIIIe s. AEC",
        "centroid_iso": "-1900",
        "succession_prev": None,
        "succession_next": "antiquite_classique",
        "notes": "Sumer, Égypte ancienne, Indus, Shang, mycéniens, Anatolie hittite. Premières écritures attestées.",
    },
    {
        "id": "antiquite_classique",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Antiquité classique",
        "label_en": "Classical antiquity",
        "interval_iso": ["-0800", "0500"],
        "interval_label": "VIIIe s. AEC – Ve s. EC",
        "centroid_iso": "-0150",
        "succession_prev": "antiquite_preclassique",
        "succession_next": "haut_moyen_age",
        "notes": "Pāṇini, Confucius, présocratiques, Grèce classique, Rome, Han, Maurya, Gupta. Codifications grammaticales.",
    },
    {
        "id": "haut_moyen_age",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Haut Moyen Âge",
        "label_en": "Early Middle Ages",
        "interval_iso": ["0500", "1000"],
        "interval_label": "VIe – Xe s. EC",
        "centroid_iso": "0750",
        "succession_prev": "antiquite_classique",
        "succession_next": "moyen_age_central",
        "notes": "Empire byzantin, califats arabo-musulmans, Tang, Carolingiens, Heian, Vendel.",
    },
    {
        "id": "moyen_age_central",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Moyen Âge central et tardif",
        "label_en": "Central & Late Middle Ages",
        "interval_iso": ["1000", "1500"],
        "interval_label": "XIe – XVe s.",
        "centroid_iso": "1250",
        "succession_prev": "haut_moyen_age",
        "succession_next": "premiere_modernite",
        "notes": "Scolastique, falsafa, Song-Yuan-Ming, Kamakura, Rus de Kiev, premières universités.",
    },
    {
        "id": "premiere_modernite",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Première modernité",
        "label_en": "Early modern period",
        "interval_iso": ["1500", "1800"],
        "interval_label": "XVIe – XVIIIe s.",
        "centroid_iso": "1650",
        "succession_prev": "moyen_age_central",
        "succession_next": "modernite_industrielle",
        "notes": "Renaissance, Réforme, Lumières, Edo, Moghols, Ming-Qing, expansions ibérique-anglaise-russe.",
    },
    {
        "id": "modernite_industrielle",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Modernité industrielle",
        "label_en": "Industrial modernity",
        "interval_iso": ["1800", "1945"],
        "interval_label": "XIXe s. – 1945",
        "centroid_iso": "1880",
        "succession_prev": "premiere_modernite",
        "succession_next": "contemporaine",
        "notes": "Révolutions industrielles, romantisme, nationalismes, colonisations, Meiji, deux guerres mondiales.",
    },
    {
        "id": "contemporaine",
        "nipada_type": 65, "nipada_atoms": [5, 13],
        "label_fr": "Époque contemporaine",
        "label_en": "Contemporary era",
        "interval_iso": ["1945", "2026"],
        "interval_label": "1945 – présent",
        "centroid_iso": "1990",
        "succession_prev": "modernite_industrielle",
        "succession_next": None,
        "notes": "Décolonisations, guerre froide, mondialisation, ère numérique, IA.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SEED — LIEUX / ZONES (18)
# ══════════════════════════════════════════════════════════════════════════════

LIEUX: list[Lieu] = [
    {
        "id": "mesopotamie",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Mésopotamie",
        "label_native": "māt Šumeri u Akkadi",
        "label_native_script": "𒆳𒋗𒈨𒊑 𒌑 𒀝𒅗𒁲",
        "coords": [33.0, 44.0],
        "famille_langues": "isolé (sumérien) / sémitique (akkadien)",
        "langues_majeures": ["sumérien", "akkadien", "araméen"],
        "epoques_actives": ["antiquite_preclassique", "antiquite_classique"],
        "contenant": None,
    },
    {
        "id": "indus_gandhara",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Vallée de l'Indus et Gandhāra",
        "label_native": "Sapta Sindhavaḥ — Gandhāra",
        "label_native_script": "सप्त सिन्धवः — गन्धार",
        "coords": [33.7, 72.9],
        "famille_langues": "indo-aryen",
        "langues_majeures": ["sanskrit védique", "sanskrit classique", "prâkrit"],
        "epoques_actives": ["antiquite_preclassique", "antiquite_classique"],
        "contenant": None,
    },
    {
        "id": "chine_centrale",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Plaine centrale chinoise",
        "label_native": "Zhōngyuán",
        "label_native_script": "中原",
        "coords": [34.7, 113.6],
        "famille_langues": "sino-tibétain",
        "langues_majeures": ["chinois ancien", "chinois moyen", "mandarin"],
        "epoques_actives": ["antiquite_preclassique", "antiquite_classique", "haut_moyen_age",
                            "moyen_age_central", "premiere_modernite"],
        "contenant": None,
    },
    {
        "id": "attique",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Attique",
        "label_native": "Attikḗ",
        "label_native_script": "Ἀττική",
        "coords": [38.0, 23.7],
        "famille_langues": "indo-européen, hellénique",
        "langues_majeures": ["grec attique", "grec koinè"],
        "epoques_actives": ["antiquite_classique"],
        "contenant": "grece_helleno",
    },
    {
        "id": "grece_helleno",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Grèce hellénique et hellénistique",
        "label_native": "Hellás",
        "label_native_script": "Ἑλλάς",
        "coords": [39.0, 22.0],
        "famille_langues": "indo-européen, hellénique",
        "langues_majeures": ["grec ancien", "grec koinè"],
        "epoques_actives": ["antiquite_preclassique", "antiquite_classique"],
        "contenant": None,
    },
    {
        "id": "latium_roma",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Latium et Rome",
        "label_native": "Latium",
        "label_native_script": "Latium",
        "coords": [41.9, 12.5],
        "famille_langues": "indo-européen, italique",
        "langues_majeures": ["latin classique", "latin tardif"],
        "epoques_actives": ["antiquite_classique", "haut_moyen_age"],
        "contenant": None,
    },
    {
        "id": "khorasan_transoxiane",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Khorasan et Transoxiane",
        "label_native": "Ḫurāsān — Mā warāʾ an-nahr",
        "label_native_script": "خراسان — ما وراء النهر",
        "coords": [39.8, 64.4],
        "famille_langues": "indo-iranien / sémitique (arabe savant)",
        "langues_majeures": ["persan classique", "arabe classique", "soghdien"],
        "epoques_actives": ["haut_moyen_age", "moyen_age_central"],
        "contenant": None,
    },
    {
        "id": "al_andalus",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Al-Andalus",
        "label_native": "al-Andalus",
        "label_native_script": "الأندلس",
        "coords": [37.4, -5.0],
        "famille_langues": "sémitique / roman",
        "langues_majeures": ["arabe andalou", "hébreu", "mozarabe"],
        "epoques_actives": ["haut_moyen_age", "moyen_age_central"],
        "contenant": "iberie",
    },
    {
        "id": "iberie",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Péninsule ibérique",
        "label_native": "Hispania — Iberia",
        "label_native_script": "Hispania",
        "coords": [40.0, -4.0],
        "famille_langues": "indo-européen, italique (romanes) / basque (isolat)",
        "langues_majeures": ["castillan", "portugais", "catalan", "basque"],
        "epoques_actives": ["antiquite_classique", "haut_moyen_age", "moyen_age_central",
                            "premiere_modernite", "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "toscane_firenze",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Toscane (Florence)",
        "label_native": "Toscana — Firenze",
        "label_native_script": "Toscana",
        "coords": [43.77, 11.25],
        "famille_langues": "indo-européen, italique",
        "langues_majeures": ["toscan", "italien littéraire"],
        "epoques_actives": ["moyen_age_central", "premiere_modernite"],
        "contenant": None,
    },
    {
        "id": "ile_de_france",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Île-de-France",
        "label_native": "Île-de-France",
        "label_native_script": "Île-de-France",
        "coords": [48.85, 2.35],
        "famille_langues": "indo-européen, italique",
        "langues_majeures": ["ancien français", "moyen français", "français moderne"],
        "epoques_actives": ["moyen_age_central", "premiere_modernite",
                            "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "angleterre_southeast",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Angleterre du Sud-Est",
        "label_native": "England — South East",
        "label_native_script": "England",
        "coords": [52.0, -1.0],
        "famille_langues": "indo-européen, germanique",
        "langues_majeures": ["vieil anglais", "moyen anglais", "anglais moderne"],
        "epoques_actives": ["haut_moyen_age", "moyen_age_central", "premiere_modernite",
                            "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "sachsen_thuringen",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Saxe-Thuringe (Weimar, Frankfurt)",
        "label_native": "Sachsen — Thüringen",
        "label_native_script": "Sachsen — Thüringen",
        "coords": [50.8, 11.0],
        "famille_langues": "indo-européen, germanique",
        "langues_majeures": ["moyen haut-allemand", "haut-allemand"],
        "epoques_actives": ["moyen_age_central", "premiere_modernite",
                            "modernite_industrielle"],
        "contenant": None,
    },
    {
        "id": "rus_moscovie",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Rus' moscovite et Saint-Pétersbourg",
        "label_native": "Moskva — Sankt-Peterburg",
        "label_native_script": "Москва — Санкт-Петербург",
        "coords": [55.75, 37.62],
        "famille_langues": "indo-européen, slave oriental",
        "langues_majeures": ["vieux russe", "russe moderne", "slavon"],
        "epoques_actives": ["moyen_age_central", "premiere_modernite",
                            "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "edo_tokyo",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Edo / Tōkyō",
        "label_native": "Edo — Tōkyō",
        "label_native_script": "江戸 — 東京",
        "coords": [35.68, 139.69],
        "famille_langues": "japonique",
        "langues_majeures": ["japonais classique", "japonais moderne"],
        "epoques_actives": ["premiere_modernite", "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "bengale_kolkata",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Bengale (Kolkata)",
        "label_native": "Bāṅglā — Kolkātā",
        "label_native_script": "বাংলা — কলকাতা",
        "coords": [22.57, 88.36],
        "famille_langues": "indo-aryen",
        "langues_majeures": ["bengali", "anglais (colonial)", "sanskrit savant"],
        "epoques_actives": ["modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "rio_de_la_plata",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Río de la Plata (Buenos Aires)",
        "label_native": "Buenos Aires",
        "label_native_script": "Buenos Aires",
        "coords": [-34.6, -58.4],
        "famille_langues": "indo-européen, italique",
        "langues_majeures": ["espagnol rioplatense", "anglais", "italien (immigration)"],
        "epoques_actives": ["modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
    {
        "id": "geneve",
        "nipada_type": 14, "nipada_atoms": [2, 7],
        "label_fr": "Genève",
        "label_native": "Genève — Genf",
        "label_native_script": "Genève",
        "coords": [46.20, 6.15],
        "famille_langues": "indo-européen, italique / germanique",
        "langues_majeures": ["français", "allemand"],
        "epoques_actives": ["premiere_modernite", "modernite_industrielle", "contemporaine"],
        "contenant": None,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SEED — AUTEURS (12)
# ══════════════════════════════════════════════════════════════════════════════

AUTEURS: list[Auteur] = [
    {
        "id": "panini",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "sa": ["पाणिनि"],
            "fr": ["Pāṇini"],
            "en": ["Pāṇini", "Panini"],
            "ar": ["بانيني"],
            "fa": ["پانینی"],
            "ru": ["Панини"],
            "zh": ["波你尼"],
            "ja": ["パーニニ"],
            "hi": ["पाणिनि"],
        },
        "name_canonical": "पाणिनि",
        "name_canonical_lang": "sa",
        "etymology": "पाणिनि < pāṇi (« main ») + suffixe patronymique -in : « descendant de Pāṇi ».",
        "birth": {"iso": "-0500", "place_id": "indus_gandhara", "uncertain": True},
        "death": {"iso": "-0450", "place_id": "indus_gandhara", "uncertain": True},
        "epoch_primary": "antiquite_classique",
        "languages": ["sanskrit védique", "sanskrit classique"],
        "trajectory": [
            {"period_iso": ["-0500", "-0450"], "place_id": "indus_gandhara",
             "lang_dominant": "sanskrit classique",
             "context": "rédaction de l'Aṣṭādhyāyī, grammaire générative en 3959 sūtras"},
        ],
        "notes": "Père fondateur de la linguistique systématique. Inspirateur direct du projet Panini.",
    },
    {
        "id": "kongzi",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "zh": ["孔子", "孔丘", "仲尼"],
            "fr": ["Confucius", "Kongzi", "Maître Kong"],
            "en": ["Confucius", "Kongzi"],
            "ja": ["孔子", "こうし"],
            "ko": ["공자"],
            "vi": ["Khổng Tử"],
            "ar": ["كونفوشيوس"],
            "ru": ["Конфуций"],
            "hi": ["कन्फ्यूशियस"],
            "sa": ["कुङ्ग्फूत्सी"],
        },
        "name_canonical": "孔子",
        "name_canonical_lang": "zh",
        "etymology": "孔丘 (Kǒng Qiū) — nom personnel ; 孔子 (Kǒngzǐ) « Maître Kong ». Latinisé Confucius par les jésuites du XVIe s.",
        "birth": {"iso": "-0551", "place_id": "chine_centrale"},
        "death": {"iso": "-0479", "place_id": "chine_centrale"},
        "epoch_primary": "antiquite_classique",
        "languages": ["chinois ancien (zhōuyǔ)"],
        "trajectory": [
            {"period_iso": ["-0551", "-0501"], "place_id": "chine_centrale",
             "lang_dominant": "chinois ancien", "context": "État de Lu, formation lettrée"},
            {"period_iso": ["-0497", "-0484"], "place_id": "chine_centrale",
             "lang_dominant": "chinois ancien", "context": "errance entre les royaumes"},
            {"period_iso": ["-0484", "-0479"], "place_id": "chine_centrale",
             "lang_dominant": "chinois ancien", "context": "retour à Lu, enseignement, compilation"},
        ],
        "notes": "Fondateur du courant rú (儒). Œuvre transmise par disciples (Lúnyǔ).",
    },
    {
        "id": "platon",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "grc": ["Πλάτων"],
            "fr": ["Platon"],
            "en": ["Plato"],
            "la": ["Plato"],
            "ar": ["أفلاطون"],
            "fa": ["افلاطون"],
            "ru": ["Платон"],
            "zh": ["柏拉图"],
            "ja": ["プラトン"],
            "hi": ["प्लेटो"],
        },
        "name_canonical": "Πλάτων",
        "name_canonical_lang": "grc",
        "etymology": "Πλάτων < πλατύς « large » — surnom donné, dit-on, à cause de la largeur de ses épaules.",
        "birth": {"iso": "-0428", "place_id": "attique"},
        "death": {"iso": "-0348", "place_id": "attique"},
        "epoch_primary": "antiquite_classique",
        "languages": ["grec attique"],
        "trajectory": [
            {"period_iso": ["-0428", "-0407"], "place_id": "attique",
             "lang_dominant": "grec attique", "context": "jeunesse aristocratique à Athènes"},
            {"period_iso": ["-0407", "-0399"], "place_id": "attique",
             "lang_dominant": "grec attique", "context": "disciple de Socrate"},
            {"period_iso": ["-0399", "-0387"], "place_id": "grece_helleno",
             "lang_dominant": "grec attique", "context": "voyages : Mégare, Égypte, Cyrène, Italie, Sicile"},
            {"period_iso": ["-0387", "-0348"], "place_id": "attique",
             "lang_dominant": "grec attique", "context": "fondation de l'Académie"},
        ],
        "notes": "Variante translittérée vers le persan/arabe via le syriaque (Aflāṭūn).",
    },
    {
        "id": "cicero",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "la": ["Marcus Tullius Cicero"],
            "fr": ["Cicéron"],
            "en": ["Cicero"],
            "it": ["Cicerone"],
            "es": ["Cicerón"],
            "de": ["Cicero", "Tullius"],
            "ar": ["شيشرون"],
            "ru": ["Цицерон"],
            "zh": ["西塞罗"],
            "ja": ["キケロ"],
        },
        "name_canonical": "Marcus Tullius Cicero",
        "name_canonical_lang": "la",
        "etymology": "Cicero < cicer « pois chiche ». Cognomen attribué selon Plutarque à un ancêtre marqué d'une verrue.",
        "birth": {"iso": "-0106", "place_id": "latium_roma"},
        "death": {"iso": "-0043", "place_id": "latium_roma"},
        "epoch_primary": "antiquite_classique",
        "languages": ["latin classique", "grec ancien"],
        "trajectory": [
            {"period_iso": ["-0106", "-0079"], "place_id": "latium_roma",
             "lang_dominant": "latin classique", "context": "formation Arpinum + Roma, étude de la rhétorique grecque"},
            {"period_iso": ["-0079", "-0077"], "place_id": "grece_helleno",
             "lang_dominant": "grec ancien", "context": "Athènes & Rhodes, perfectionnement"},
            {"period_iso": ["-0077", "-0043"], "place_id": "latium_roma",
             "lang_dominant": "latin classique", "context": "carrière politique et œuvre philosophique"},
        ],
        "notes": "Translateur du grec philosophique en latin — forge un vocabulaire conceptuel.",
    },
    {
        "id": "ibn_sina",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "ar": ["ابن سينا", "أبو علي الحسين بن عبد الله بن سينا"],
            "fa": ["ابن سینا", "ابوعلی سینا"],
            "fr": ["Avicenne", "Ibn Sīnā"],
            "en": ["Avicenna", "Ibn Sina"],
            "la": ["Avicenna"],
            "ru": ["Ибн Сина", "Авиценна"],
            "zh": ["伊本·西那", "阿维森纳"],
            "ja": ["イブン・スィーナー"],
            "tr": ["İbn-i Sînâ"],
            "hi": ["इब्न सीना"],
        },
        "name_canonical": "ابن سينا",
        "name_canonical_lang": "ar",
        "etymology": "ابن سينا « fils de Sīnā ». Latinisé Avicenna via l'hébreu Aven Sina au XIIe s. dans Tolède.",
        "birth": {"iso": "0980", "place_id": "khorasan_transoxiane"},
        "death": {"iso": "1037", "place_id": "khorasan_transoxiane"},
        "epoch_primary": "haut_moyen_age",
        "languages": ["persan classique", "arabe classique"],
        "trajectory": [
            {"period_iso": ["0980", "1002"], "place_id": "khorasan_transoxiane",
             "lang_dominant": "persan classique",
             "context": "Boukhara, formation, médecine à la cour samanide"},
            {"period_iso": ["1002", "1015"], "place_id": "khorasan_transoxiane",
             "lang_dominant": "arabe classique", "context": "Gurgāndj, errances post-chute samanide"},
            {"period_iso": ["1015", "1037"], "place_id": "khorasan_transoxiane",
             "lang_dominant": "arabe classique",
             "context": "Hamadan & Ispahan : Qānūn fī al-ṭibb, Kitāb al-šifāʾ"},
        ],
        "notes": "Œuvre principale en arabe ; correspondance et Dānešnāme en persan.",
    },
    {
        "id": "dante",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "it": ["Dante Alighieri", "Durante degli Alighieri"],
            "fr": ["Dante", "Dante Alighieri"],
            "en": ["Dante Alighieri"],
            "la": ["Dantes Alagherius"],
            "ar": ["دانتي أليغييري"],
            "ru": ["Данте Алигьери"],
            "zh": ["但丁·阿利吉耶里"],
            "ja": ["ダンテ・アリギエーリ"],
            "hi": ["दांते अलीगियरी"],
        },
        "name_canonical": "Dante Alighieri",
        "name_canonical_lang": "it",
        "etymology": "Dante hypocoristique de Durante « endurant ». Alighieri possible déformation d'Aldighieri (germanique alt-gēr).",
        "birth": {"iso": "1265", "place_id": "toscane_firenze"},
        "death": {"iso": "1321", "place_id": "toscane_firenze"},
        "epoch_primary": "moyen_age_central",
        "languages": ["toscan", "latin médiéval", "occitan"],
        "trajectory": [
            {"period_iso": ["1265", "1302"], "place_id": "toscane_firenze",
             "lang_dominant": "toscan", "context": "Florence : formation, Vita Nuova, vie politique guelfe"},
            {"period_iso": ["1302", "1321"], "place_id": "toscane_firenze",
             "lang_dominant": "toscan", "context": "exil itinérant : Vérone, Lucques, Ravenne ; Commedia"},
        ],
        "notes": "Fondateur du toscan littéraire qui deviendra italien standard.",
    },
    {
        "id": "shakespeare",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "en": ["William Shakespeare"],
            "fr": ["William Shakespeare", "Shakespeare"],
            "es": ["Guillermo Shakespeare"],
            "ar": ["وليم شكسبير"],
            "ru": ["Уильям Шекспир"],
            "zh": ["威廉·莎士比亚"],
            "ja": ["ウィリアム・シェイクスピア"],
            "hi": ["विलियम शेक्सपियर"],
            "ko": ["윌리엄 셰익스피어"],
        },
        "name_canonical": "William Shakespeare",
        "name_canonical_lang": "en",
        "etymology": "Shakespeare < shake + spear « brandir la lance ». Surnom de guerrier devenu patronyme.",
        "birth": {"iso": "1564", "place_id": "angleterre_southeast"},
        "death": {"iso": "1616", "place_id": "angleterre_southeast"},
        "epoch_primary": "premiere_modernite",
        "languages": ["anglais moderne précoce (Early Modern English)"],
        "trajectory": [
            {"period_iso": ["1564", "1585"], "place_id": "angleterre_southeast",
             "lang_dominant": "early modern english", "context": "Stratford-upon-Avon, formation"},
            {"period_iso": ["1585", "1613"], "place_id": "angleterre_southeast",
             "lang_dominant": "early modern english", "context": "London : théâtre, sonnets, pièces"},
            {"period_iso": ["1613", "1616"], "place_id": "angleterre_southeast",
             "lang_dominant": "early modern english", "context": "retraite à Stratford"},
        ],
        "notes": "Lexique d'environ 17 000 mots — fixe une part majeure de l'anglais littéraire.",
    },
    {
        "id": "goethe",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "de": ["Johann Wolfgang von Goethe"],
            "fr": ["Johann Wolfgang von Goethe", "Goethe"],
            "en": ["Johann Wolfgang von Goethe", "Goethe"],
            "ar": ["يوهان فولفغانغ فون غوته"],
            "ru": ["Иоганн Вольфганг фон Гёте"],
            "zh": ["约翰·沃尔夫冈·冯·歌德"],
            "ja": ["ヨハン・ヴォルフガング・フォン・ゲーテ"],
            "hi": ["योहान वोल्फगांग फ़ोन गेटे"],
        },
        "name_canonical": "Johann Wolfgang von Goethe",
        "name_canonical_lang": "de",
        "etymology": "Goethe < moyen haut-allemand göte « parrain » ou diminutif de Gottfried. « von » = noblesse octroyée en 1782.",
        "birth": {"iso": "1749", "place_id": "sachsen_thuringen"},
        "death": {"iso": "1832", "place_id": "sachsen_thuringen"},
        "epoch_primary": "premiere_modernite",
        "languages": ["haut-allemand", "français", "italien", "latin", "grec"],
        "trajectory": [
            {"period_iso": ["1749", "1775"], "place_id": "sachsen_thuringen",
             "lang_dominant": "haut-allemand", "context": "Frankfurt, Leipzig, Strasbourg : Sturm und Drang, Werther"},
            {"period_iso": ["1775", "1786"], "place_id": "sachsen_thuringen",
             "lang_dominant": "haut-allemand", "context": "Weimar : ministre, sciences, théâtre"},
            {"period_iso": ["1786", "1788"], "place_id": "toscane_firenze",
             "lang_dominant": "italien", "context": "Italienische Reise : Roma, Napoli, Sicilia"},
            {"period_iso": ["1788", "1832"], "place_id": "sachsen_thuringen",
             "lang_dominant": "haut-allemand", "context": "Weimar : Faust I-II, théorie des couleurs"},
        ],
        "notes": "Plurilinguisme savant — modèle d'auteur dont l'œuvre intègre l'italien et la culture classique.",
    },
    {
        "id": "pushkin",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "ru": ["Александр Сергеевич Пушкин"],
            "fr": ["Alexandre Pouchkine", "Pouchkine"],
            "en": ["Alexander Pushkin"],
            "de": ["Alexander Puschkin"],
            "ar": ["ألكسندر بوشكين"],
            "zh": ["亚历山大·普希金"],
            "ja": ["アレクサンドル・プーシキン"],
            "hi": ["अलेक्सान्द्र पुश्किन"],
        },
        "name_canonical": "Александр Сергеевич Пушкин",
        "name_canonical_lang": "ru",
        "etymology": "Пушкин < пушка « canon » : sobriquet d'un ancêtre boyar du XIVe s. Premier prénom Александр < Ἀλέξανδρος « qui repousse l'homme ».",
        "birth": {"iso": "1799", "place_id": "rus_moscovie"},
        "death": {"iso": "1837", "place_id": "rus_moscovie"},
        "epoch_primary": "modernite_industrielle",
        "languages": ["russe", "français"],
        "trajectory": [
            {"period_iso": ["1799", "1811"], "place_id": "rus_moscovie",
             "lang_dominant": "français", "context": "Moscou : éducation aristocratique francophone"},
            {"period_iso": ["1811", "1820"], "place_id": "rus_moscovie",
             "lang_dominant": "russe", "context": "Lycée de Tsarskoïé Sélo, Saint-Pétersbourg"},
            {"period_iso": ["1820", "1826"], "place_id": "rus_moscovie",
             "lang_dominant": "russe", "context": "exils du sud (Kichinev, Odessa) puis Mikhaïlovskoié"},
            {"period_iso": ["1826", "1837"], "place_id": "rus_moscovie",
             "lang_dominant": "russe", "context": "Moscou & Saint-Pétersbourg : Onéguine, La Fille du capitaine"},
        ],
        "notes": "Première éducation francophone, conversion artistique au russe : exemple de bilinguisme à pivot.",
    },
    {
        "id": "natsume_soseki",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "ja": ["夏目 漱石", "夏目 金之助"],
            "fr": ["Natsume Sōseki"],
            "en": ["Natsume Sōseki"],
            "zh": ["夏目漱石"],
            "ko": ["나쓰메 소세키"],
            "ar": ["ناتسوميه سوسيكي"],
            "ru": ["Нацумэ Сосэки"],
            "hi": ["नात्सुमे सोसेकी"],
        },
        "name_canonical": "夏目 漱石",
        "name_canonical_lang": "ja",
        "etymology": "夏目 patronyme (« regard d'été »). 漱石 (sōseki) nom de plume tiré du chinois 漱石枕流 « se rincer la bouche aux pierres » — entêtement.",
        "birth": {"iso": "1867", "place_id": "edo_tokyo"},
        "death": {"iso": "1916", "place_id": "edo_tokyo"},
        "epoch_primary": "modernite_industrielle",
        "languages": ["japonais moderne", "anglais", "chinois classique"],
        "trajectory": [
            {"period_iso": ["1867", "1900"], "place_id": "edo_tokyo",
             "lang_dominant": "japonais moderne", "context": "Tōkyō : université impériale, anglais, chinois classique"},
            {"period_iso": ["1900", "1903"], "place_id": "angleterre_southeast",
             "lang_dominant": "anglais", "context": "bourse au Royaume-Uni : Londres"},
            {"period_iso": ["1903", "1916"], "place_id": "edo_tokyo",
             "lang_dominant": "japonais moderne", "context": "Tōkyō : enseignement puis carrière littéraire"},
        ],
        "notes": "Écrit dans les trois registres : kanbun, japonais Meiji, anglais académique. Né l'année de la restauration.",
    },
    {
        "id": "tagore",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "bn": ["রবীন্দ্রনাথ ঠাকুর"],
            "fr": ["Rabindranath Tagore"],
            "en": ["Rabindranath Tagore"],
            "hi": ["रवीन्द्रनाथ ठाकुर"],
            "sa": ["रवीन्द्रनाथ ठाकुर"],
            "ar": ["رابندرناث طاغور"],
            "ru": ["Рабиндранат Тагор"],
            "zh": ["罗宾德拉纳特·泰戈尔"],
            "ja": ["ラビンドラナート・タゴール"],
            "fa": ["رابیندرانات تاگور"],
        },
        "name_canonical": "রবীন্দ্রনাথ ঠাকুর",
        "name_canonical_lang": "bn",
        "etymology": "রবীন্দ্রনাথ < रवि (soleil) + इन्द्र (Indra) + नाथ (seigneur) — « seigneur du soleil-Indra ». ঠাকুর « seigneur, brahmane », anglicisé en Tagore.",
        "birth": {"iso": "1861", "place_id": "bengale_kolkata"},
        "death": {"iso": "1941", "place_id": "bengale_kolkata"},
        "epoch_primary": "modernite_industrielle",
        "languages": ["bengali", "anglais", "sanskrit"],
        "trajectory": [
            {"period_iso": ["1861", "1878"], "place_id": "bengale_kolkata",
             "lang_dominant": "bengali", "context": "Calcutta : éducation domestique brahmo"},
            {"period_iso": ["1878", "1880"], "place_id": "angleterre_southeast",
             "lang_dominant": "anglais", "context": "Brighton, University College London"},
            {"period_iso": ["1880", "1941"], "place_id": "bengale_kolkata",
             "lang_dominant": "bengali", "context": "Bengale : poésie, fondation de Shantiniketan, voyages mondiaux"},
        ],
        "notes": "Premier non-Européen prix Nobel littérature (1913). Auto-traducteur bengali → anglais.",
    },
    {
        "id": "borges",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "names": {
            "es": ["Jorge Luis Borges"],
            "fr": ["Jorge Luis Borges"],
            "en": ["Jorge Luis Borges"],
            "ar": ["خورخي لويس بورخيس"],
            "ru": ["Хорхе Луис Борхес"],
            "zh": ["豪尔赫·路易斯·博尔赫斯"],
            "ja": ["ホルヘ・ルイス・ボルヘス"],
            "hi": ["जॉर्ज लुइस बोर्खेस"],
        },
        "name_canonical": "Jorge Luis Borges",
        "name_canonical_lang": "es",
        "etymology": "Jorge < Γεώργιος « cultivateur de la terre ». Borges < anglo-normand « bourgeois, citadin » via la lignée portugaise.",
        "birth": {"iso": "1899", "place_id": "rio_de_la_plata"},
        "death": {"iso": "1986", "place_id": "geneve"},
        "epoch_primary": "contemporaine",
        "languages": ["espagnol rioplatense", "anglais", "français", "allemand", "vieux-anglais"],
        "trajectory": [
            {"period_iso": ["1899", "1914"], "place_id": "rio_de_la_plata",
             "lang_dominant": "espagnol rioplatense", "context": "Buenos Aires : éducation bilingue es/en avec grand-mère anglaise"},
            {"period_iso": ["1914", "1921"], "place_id": "geneve",
             "lang_dominant": "français", "context": "Genève (Collège Calvin), Espagne ; latin, allemand"},
            {"period_iso": ["1921", "1986"], "place_id": "rio_de_la_plata",
             "lang_dominant": "espagnol rioplatense", "context": "Buenos Aires : Ficciones, Aleph, bibliothèque, voyages"},
            {"period_iso": ["1986", "1986"], "place_id": "geneve",
             "lang_dominant": "français", "context": "retour final à Genève, mort"},
        ],
        "notes": "Naissance et mort encadrent un parcours quadrilingue. Lecteur de Sōseki, Tagore, anglo-saxon ancien.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Validation et émission
# ══════════════════════════════════════════════════════════════════════════════

def _check_atom_consistency() -> list[str]:
    """Pour chaque entrée, vérifie que ∏(nipada_atoms) == nipada_type."""
    errors = []
    for table_name, table in [("EPOQUES", EPOQUES), ("LIEUX", LIEUX), ("AUTEURS", AUTEURS)]:
        for entry in table:
            prod = 1
            for a in entry["nipada_atoms"]:
                prod *= a
            if prod != entry["nipada_type"]:
                errors.append(f"{table_name}/{entry['id']}: ∏{entry['nipada_atoms']}={prod} ≠ type {entry['nipada_type']}")
    return errors


def _check_id_references() -> list[str]:
    """Vérifie que tous les place_id et epoch_primary référencent une entrée existante."""
    errors = []
    epoque_ids = {e["id"] for e in EPOQUES}
    lieu_ids = {l["id"] for l in LIEUX}
    for e in EPOQUES:
        for ref_field in ("succession_prev", "succession_next"):
            ref = e.get(ref_field)
            if ref is not None and ref not in epoque_ids:
                errors.append(f"EPOQUES/{e['id']}.{ref_field} → '{ref}' inconnu")
    for li in LIEUX:
        c = li.get("contenant")
        if c is not None and c not in lieu_ids:
            errors.append(f"LIEUX/{li['id']}.contenant → '{c}' inconnu")
        for ep in li["epoques_actives"]:
            if ep not in epoque_ids:
                errors.append(f"LIEUX/{li['id']}.epoques_actives → '{ep}' inconnu")
    for au in AUTEURS:
        if au["epoch_primary"] not in epoque_ids:
            errors.append(f"AUTEURS/{au['id']}.epoch_primary → '{au['epoch_primary']}' inconnu")
        for field in ("birth", "death"):
            ref = au.get(field)
            if ref and ref.get("place_id") not in lieu_ids:
                errors.append(f"AUTEURS/{au['id']}.{field}.place_id → '{ref.get('place_id')}' inconnu")
        for step in au["trajectory"]:
            if step["place_id"] not in lieu_ids:
                errors.append(f"AUTEURS/{au['id']}.trajectory → place_id '{step['place_id']}' inconnu")
    return errors


def main() -> None:
    W = 78
    print("═" * W)
    print("  §101 — Encyclopédie nipada : seed initial où / quand / qui")
    print("═" * W)
    print(f"\n  Époques  : {len(EPOQUES)}")
    print(f"  Lieux    : {len(LIEUX)}")
    print(f"  Auteurs  : {len(AUTEURS)}")
    print(f"  Molécules de référence : {len(NIPADA_MOLECULES_GEO_TIME)}")

    errors = _check_atom_consistency() + _check_id_references()
    if errors:
        print("\n  ✗ Erreurs de validation :")
        for e in errors:
            print(f"    - {e}")
        raise SystemExit(1)
    print("\n  ✓ Validation : tous les produits primes et toutes les références sont cohérents.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_temps = OUT_DIR / "temps_epoques.json"
    out_lieux = OUT_DIR / "lieux_zones.json"
    out_auteurs = OUT_DIR / "auteurs_seed.json"
    out_molecules = OUT_DIR / "nipada_molecules_geo_time.json"

    with out_temps.open("w", encoding="utf-8") as f:
        json.dump({"version": "§101 seed", "epoques": EPOQUES}, f, ensure_ascii=False, indent=2)
    with out_lieux.open("w", encoding="utf-8") as f:
        json.dump({"version": "§101 seed", "lieux": LIEUX}, f, ensure_ascii=False, indent=2)
    with out_auteurs.open("w", encoding="utf-8") as f:
        json.dump({"version": "§101 seed", "auteurs": AUTEURS}, f, ensure_ascii=False, indent=2)
    with out_molecules.open("w", encoding="utf-8") as f:
        json.dump({"version": "§101", "primes": PRIMES,
                   "molecules": NIPADA_MOLECULES_GEO_TIME}, f, ensure_ascii=False, indent=2)

    print(f"\n  Sortie :")
    for p in (out_molecules, out_temps, out_lieux, out_auteurs):
        print(f"    {p.relative_to(REPO_ROOT)}")

    # Récapitulatif lisible
    print("\n  ── ÉPOQUES (succession) " + "─" * (W - 24))
    for e in EPOQUES:
        print(f"    {e['id']:<26s} {e['interval_label']:<26s} → {e['label_fr']}")
    print("\n  ── AUTEURS (parcours linguistique) " + "─" * (W - 35))
    for a in AUTEURS:
        n_langs = len(a["languages"])
        n_steps = len(a["trajectory"])
        b = a["birth"]["iso"]
        d = a["death"]["iso"] if a.get("death") else "—"
        print(f"    {a['id']:<18s} {b:>6} → {d:<6}   {n_langs} langue(s), {n_steps} étape(s)   "
              f"[{a['name_canonical']}]")
    print("═" * W)


if __name__ == "__main__":
    main()

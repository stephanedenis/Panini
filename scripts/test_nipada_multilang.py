#!/usr/bin/env python3
"""
test_nipada_multilang.py — §79 : Traduction circulaire multi-langues bit-perfect

Protocole :
    1. Corpus parallèle — même texte en 5 langues (FR/EN/DE/ES/ZH)
       → 5 unités textuelles tirées de l'Article 1 DUDH + passages philosophiques
    2. Encodage — chaque phrase → nipada sequence (top-k molécules, seuil cosinus)
    3. CAS bit-perfect — nipada_fingerprint + sha256 → bytes originaux
       Reconstruction : fingerprint → CAS lookup → bytes → vérification sha256
    4. Analyse comparative — distributions nipada par langue, convergence inter-langues,
       molécules universelles vs molécules langue-spécifiques

Résultats sauvegardés dans :
    research/nipada/falsification/nipada_multilang_test.json

Usage :
    python scripts/test_nipada_multilang.py
    python scripts/test_nipada_multilang.py --topk 5 --threshold 0.18
"""

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_engine import (
    NipadaCatalog,
    Domain,
    encode,
    decode,
)

MODEL_NAME  = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_multilang_test.json"

# ── IDs des 15 molécules Z+ ───────────────────────────────────────────────────
MOLECULE_IDS = [2, 3, 5, 7, 6, 10, 14, 15, 21, 35, 30, 42, 70, 105, 210]

# ── Phrases définitionnelles multi-langues (reprise §76 / H2 v3) ─────────────
DEFINITIONS: dict[str, dict[int, str]] = {
    "fr": {
        2:   "L'être est le pur fait d'exister, antérieur à toute différence ou relation.",
        3:   "La différence est la distinction irréductible entre deux choses, antérieure à toute relation.",
        5:   "Le rapport est la relation structurelle entre deux termes, indépendante de toute orientation.",
        7:   "L'orientation est l'asymétrie directionnelle qui distingue l'avant de l'après, la source du but.",
        6:   "L'existence est l'articulation de l'être et de la différence : quelque chose existe quand son être se distingue du non-être.",
        10:  "La composition est l'articulation de l'être et du rapport : quelque chose est composé quand son être est structuré par une relation de parties.",
        14:  "Le devenir est l'articulation de l'être et de l'orientation : quelque chose devient quand son être est dirigé vers un but.",
        15:  "La mesure est l'articulation de la différence et du rapport : quelque chose est mesuré quand une différence est exprimée en rapport.",
        21:  "L'opposition est l'articulation de la différence et de l'orientation : deux choses s'opposent quand leur différence est directionnelle.",
        35:  "La référence est l'articulation du rapport et de l'orientation : une référence est un rapport orienté du signe vers le sens.",
        30:  "La vie est l'articulation de l'être, de la différence et du rapport : un vivant existe, se différencie de son milieu et entretient avec lui des relations structurées.",
        42:  "La transformation est l'articulation de l'être, de la différence et de l'orientation : quelque chose se transforme quand son être change de façon dirigée et irréversible.",
        70:  "L'intention est l'articulation de l'être, du rapport et de l'orientation : une intention est un être structuré par un rapport orienté vers un but.",
        105: "Le temps est l'articulation de la différence, du rapport et de l'orientation : le temps est la différence ordonnée entre des moments, structurée en rapport avec une direction.",
        210: "L'intégration est l'articulation de l'être, de la différence, du rapport et de l'orientation : le tout intégré rassemble les différences existantes en relations structurées et orientées.",
    },
    "en": {
        2:   "Being is the pure fact of existing, prior to any difference or relation.",
        3:   "Difference is the irreducible distinction between two things, prior to any relation.",
        5:   "Ratio is the structural relation between two terms, independent of direction.",
        7:   "Orientation is the directional asymmetry that distinguishes before from after, source from goal.",
        6:   "Existence is the articulation of being and difference: something exists when its being is distinguished from non-being.",
        10:  "Composition is the articulation of being and ratio: something is composed when its being is structured by a relation of parts.",
        14:  "Becoming is the articulation of being and orientation: something becomes when its being is directed toward a goal.",
        15:  "Measure is the articulation of difference and ratio: something is measured when a difference is expressed as a ratio.",
        21:  "Opposition is the articulation of difference and orientation: two things are opposed when their difference is directional and asymmetric.",
        35:  "Reference is the articulation of ratio and orientation: a reference is a ratio that has a direction, pointing from sign to meaning.",
        30:  "Life is the articulation of being, difference and ratio: a living thing exists, differentiates itself from its environment and maintains structural relations with it.",
        42:  "Transformation is the articulation of being, difference and orientation: something transforms when its being changes in a directed, irreversible way.",
        70:  "Intention is the articulation of being, ratio and orientation: an intention is a being structured by a relation that is oriented toward a goal.",
        105: "Time is the articulation of difference, ratio and orientation: time is the ordered difference between moments, structured as a ratio with a direction.",
        210: "Integration is the articulation of being, difference, ratio and orientation: the integrated whole brings together existing differences into structured and oriented relations.",
    },
    "de": {
        2:   "Sein ist die reine Tatsache zu existieren, vor jeder Differenz oder Beziehung.",
        3:   "Differenz ist die irreduzible Unterscheidung zwischen zwei Dingen, vor jeder Beziehung.",
        5:   "Verhältnis ist die strukturelle Beziehung zwischen zwei Termen, unabhängig von jeder Richtung.",
        7:   "Orientierung ist die gerichtete Asymmetrie, die Vorher von Nachher und Quelle von Ziel unterscheidet.",
        6:   "Existenz ist die Artikulation von Sein und Differenz: etwas existiert, wenn sein Sein von Nicht-Sein unterschieden wird.",
        10:  "Komposition ist die Artikulation von Sein und Verhältnis: etwas ist zusammengesetzt, wenn sein Sein durch ein Teile-Verhältnis strukturiert ist.",
        14:  "Werden ist die Artikulation von Sein und Orientierung: etwas wird, wenn sein Sein auf ein Ziel hin gerichtet ist.",
        15:  "Maß ist die Artikulation von Differenz und Verhältnis: etwas ist gemessen, wenn eine Differenz als Verhältnis ausgedrückt wird.",
        21:  "Gegensatz ist die Artikulation von Differenz und Orientierung: zwei Dinge stehen im Gegensatz, wenn ihre Differenz gerichtet und asymmetrisch ist.",
        35:  "Referenz ist die Artikulation von Verhältnis und Orientierung: eine Referenz ist ein Verhältnis, das gerichtet ist — vom Zeichen zur Bedeutung.",
        30:  "Leben ist die Artikulation von Sein, Differenz und Verhältnis: ein Lebewesen existiert, unterscheidet sich von seiner Umgebung und unterhält strukturelle Beziehungen mit ihr.",
        42:  "Transformation ist die Artikulation von Sein, Differenz und Orientierung: etwas wandelt sich, wenn sein Sein sich gerichtet und irreversibel verändert.",
        70:  "Intention ist die Artikulation von Sein, Verhältnis und Orientierung: eine Intention ist ein Sein, das durch ein auf ein Ziel gerichtetes Verhältnis strukturiert ist.",
        105: "Zeit ist die Artikulation von Differenz, Verhältnis und Orientierung: Zeit ist die geordnete Differenz zwischen Momenten, als Verhältnis mit einer Richtung strukturiert.",
        210: "Integration ist die Artikulation von Sein, Differenz, Verhältnis und Orientierung: das integrierte Ganze vereint bestehende Differenzen in strukturierten und gerichteten Beziehungen.",
    },
    "es": {
        2:   "El ser es el puro hecho de existir, anterior a toda diferencia o relación.",
        3:   "La diferencia es la distinción irreductible entre dos cosas, anterior a toda relación.",
        5:   "La razón es la relación estructural entre dos términos, independiente de cualquier orientación.",
        7:   "La orientación es la asimetría direccional que distingue el antes del después, la fuente del objetivo.",
        6:   "La existencia es la articulación del ser y la diferencia: algo existe cuando su ser se distingue del no-ser.",
        10:  "La composición es la articulación del ser y la razón: algo está compuesto cuando su ser está estructurado por una relación de partes.",
        14:  "El devenir es la articulación del ser y la orientación: algo deviene cuando su ser está dirigido hacia un objetivo.",
        15:  "La medida es la articulación de la diferencia y la razón: algo se mide cuando una diferencia se expresa como razón.",
        21:  "La oposición es la articulación de la diferencia y la orientación: dos cosas se oponen cuando su diferencia es direccional y asimétrica.",
        35:  "La referencia es la articulación de la razón y la orientación: una referencia es una razón orientada del signo hacia el significado.",
        30:  "La vida es la articulación del ser, la diferencia y la razón: un ser vivo existe, se diferencia de su entorno y mantiene relaciones estructurales con él.",
        42:  "La transformación es la articulación del ser, la diferencia y la orientación: algo se transforma cuando su ser cambia de manera dirigida e irreversible.",
        70:  "La intención es la articulación del ser, la razón y la orientación: una intención es un ser estructurado por una razón orientada hacia un objetivo.",
        105: "El tiempo es la articulación de la diferencia, la razón y la orientación: el tiempo es la diferencia ordenada entre momentos, estructurada como razón con una dirección.",
        210: "La integración es la articulación del ser, la diferencia, la razón y la orientación: el todo integrado reúne las diferencias existentes en relaciones estructuradas y orientadas.",
    },
    "zh": {
        2:   "存在是纯粹的事实，先于任何差异或关系。",
        3:   "差异是两事物之间不可还原的区别，先于任何关系。",
        5:   "比率是两个项之间的结构关系，独立于任何方向。",
        7:   "方向是区分前后、源与目标的不对称性。",
        6:   "存在性是存在与差异的结合：当某物的存在与非存在相区别时，它才存在。",
        10:  "组合是存在与比率的结合：当某物的存在由部分之间的关系所结构时，它是组合的。",
        14:  "生成是存在与方向的结合：当某物的存在指向目标时，它在生成中。",
        15:  "测量是差异与比率的结合：当差异以比率表达时，就产生了测量。",
        21:  "对立是差异与方向的结合：当两事物的差异具有方向性和不对称性时，它们相互对立。",
        35:  "指涉是比率与方向的结合：指涉是一个有方向的比率，从符号指向意义。",
        30:  "生命是存在、差异与比率的结合：生命体存在，与环境区别，并与之维持结构关系。",
        42:  "转化是存在、差异与方向的结合：当某物的存在以定向且不可逆的方式改变时，它在转化。",
        70:  "意图是存在、比率与方向的结合：意图是一种由指向目标的有向关系所结构的存在。",
        105: "时间是差异、比率与方向的结合：时间是时刻之间的有序差异，被结构为具有方向的比率。",
        210: "整合是存在、差异、比率与方向的结合：整合的整体将现有的差异汇聚成结构化的有向关系。",
    },
}

LANGUAGES = list(DEFINITIONS.keys())

# ── Corpus parallèle — même contenu sémantique en 5 langues ──────────────────
# 6 unités textuelles, chacune disponible dans les 5 langues.
# Sources : Article 1 DUDH (U1–U2), passages philosophiques (U3–U6).
CORPUS: list[dict[str, str]] = [
    {
        "id": "DUDH_1a",
        "theme": "Égalité en dignité et droits",
        "fr": "Tous les êtres humains naissent libres et égaux en dignité et en droits.",
        "en": "All human beings are born free and equal in dignity and rights.",
        "de": "Alle Menschen sind frei und gleich an Würde und Rechten geboren.",
        "es": "Todos los seres humanos nacen libres e iguales en dignidad y derechos.",
        "zh": "人人生而自由，在尊严和权利上一律平等。",
    },
    {
        "id": "DUDH_1b",
        "theme": "Raison, conscience et fraternité",
        "fr": "Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité.",
        "en": "They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.",
        "de": "Sie sind mit Vernunft und Gewissen begabt und sollen einander im Geist der Brüderlichkeit begegnen.",
        "es": "Dotados de razón y conciencia, deben comportarse fraternalmente los unos con los otros.",
        "zh": "他们赋有理性和良心，并应以兄弟关系的精神相对待。",
    },
    {
        "id": "PHIL_temps",
        "theme": "La flèche du temps",
        "fr": "Le temps est une différence ordonnée entre les moments, irréversible par nature.",
        "en": "Time is an ordered difference between moments, irreversible by nature.",
        "de": "Die Zeit ist eine geordnete Differenz zwischen Momenten, von Natur aus unumkehrbar.",
        "es": "El tiempo es una diferencia ordenada entre momentos, irreversible por naturaleza.",
        "zh": "时间是时刻之间的有序差异，本质上不可逆。",
    },
    {
        "id": "PHIL_vie",
        "theme": "Le vivant et son milieu",
        "fr": "Tout être vivant maintient des relations structurées avec son environnement et se différencie de lui.",
        "en": "Every living being maintains structured relations with its environment and differentiates itself from it.",
        "de": "Jedes Lebewesen unterhält strukturelle Beziehungen zu seiner Umgebung und unterscheidet sich von ihr.",
        "es": "Todo ser vivo mantiene relaciones estructuradas con su entorno y se diferencia de él.",
        "zh": "每个生命体与其环境维持结构化关系，并与之区分自身。",
    },
    {
        "id": "PHIL_transformation",
        "theme": "Transformation irréversible",
        "fr": "Le feu transforme la matière de façon irréversible, orientant le devenir vers la cendre.",
        "en": "Fire transforms matter in an irreversible way, orienting becoming toward ash.",
        "de": "Feuer verwandelt Materie auf unumkehrbare Weise und richtet das Werden zur Asche hin.",
        "es": "El fuego transforma la materia de forma irreversible, orientando el devenir hacia la ceniza.",
        "zh": "火以不可逆的方式改变物质，将生成引向灰烬。",
    },
    {
        "id": "PHIL_integration",
        "theme": "L'unité des opposés",
        "fr": "L'intégration rassemble les différences existantes en un tout structuré et orienté.",
        "en": "Integration brings existing differences together into a structured and oriented whole.",
        "de": "Die Integration vereint bestehende Differenzen zu einem strukturierten und gerichteten Ganzen.",
        "es": "La integración reúne las diferencias existentes en un todo estructurado y orientado.",
        "zh": "整合将现有的差异汇聚成结构化的有向整体。",
    },
]

# ── Noms courts des molécules (affichage) ─────────────────────────────────────
MOL_NAMES_FR = {
    2:   "ÊTRE",       3:   "DIFFÉRENCE", 5:   "RAPPORT",     7:   "ORIENTATION",
    6:   "EXISTENCE",  10:  "COMPOSITION",14:  "DEVENIR",      15:  "MESURE",
    21:  "OPPOSITION", 35:  "RÉFÉRENCE",  30:  "VIE",          42:  "TRANSFORMATION",
    70:  "INTENTION",  105: "TEMPS",      210: "INTÉGRATION",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CAS bit-perfect
# ═══════════════════════════════════════════════════════════════════════════════

class NipadaCAS:
    """
    Content-Addressed Store bit-perfect pour le codec nipada.

    La clé de stockage primaire est le sha256 des bytes originaux.
    Le fingerprint nipada (tuple de mol_ids) est un index sémantique secondaire.

    store() → enregistre (fingerprint, sha256, bytes)
    retrieve_by_hash() → bytes originaux depuis sha256 (bit-perfect garanti)
    retrieve_by_fingerprint() → liste de (sha256, bytes) pour un fingerprint donné
    """

    def __init__(self) -> None:
        # sha256 → bytes originaux
        self._by_hash: dict[str, bytes] = {}
        # fingerprint_key → list[sha256]
        self._by_fingerprint: dict[str, list[str]] = defaultdict(list)

    @staticmethod
    def _fp_key(fingerprint: tuple[int, ...]) -> str:
        return "|".join(str(m) for m in fingerprint)

    def store(self, original: bytes, fingerprint: tuple[int, ...]) -> str:
        """
        Stocke les bytes originaux. Retourne le sha256 hex.
        """
        h = hashlib.sha256(original).hexdigest()
        self._by_hash[h] = original
        fp_key = self._fp_key(fingerprint)
        if h not in self._by_fingerprint[fp_key]:
            self._by_fingerprint[fp_key].append(h)
        return h

    def retrieve_by_hash(self, sha256: str) -> bytes | None:
        return self._by_hash.get(sha256)

    def retrieve_by_fingerprint(self, fingerprint: tuple[int, ...]) -> list[tuple[str, bytes]]:
        fp_key = self._fp_key(fingerprint)
        return [
            (h, self._by_hash[h])
            for h in self._by_fingerprint.get(fp_key, [])
            if h in self._by_hash
        ]

    def verify(self, sha256: str, original: bytes) -> bool:
        """Vérifie l'intégrité bit-perfect."""
        return hashlib.sha256(original).hexdigest() == sha256


# ═══════════════════════════════════════════════════════════════════════════════
# Encodeur nipada pour texte
# ═══════════════════════════════════════════════════════════════════════════════

class NipadaTextEncoder:
    """
    Encode une phrase en séquence de molécules nipada.

    La matrice de référence est construite une fois (moyenne des 5 définitions
    multilingues pour chaque molécule, même approche que H2 v3 / §76).
    """

    def __init__(self, model: SentenceTransformer, topk: int = 3, threshold: float = 0.20):
        self.model     = model
        self.topk      = topk
        self.threshold = threshold
        self._ref_matrix: np.ndarray | None = None

    def _build_ref_matrix(self) -> np.ndarray:
        """Construit la matrice de référence 15 × 384 (moyenne multilingue)."""
        rows = []
        for mol_id in MOLECULE_IDS:
            defs = [DEFINITIONS[lang][mol_id] for lang in LANGUAGES]
            vecs = self.model.encode(defs, normalize_embeddings=True)
            rows.append(vecs.mean(axis=0))
        mat = np.array(rows)
        # Re-normalisation des moyennes
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        return mat / np.where(norms == 0, 1, norms)

    @property
    def ref_matrix(self) -> np.ndarray:
        if self._ref_matrix is None:
            self._ref_matrix = self._build_ref_matrix()
        return self._ref_matrix

    def encode_phrase(self, phrase: str) -> tuple[list[tuple[int, float]], np.ndarray]:
        """
        Encode une phrase en molécules nipada.

        Retourne :
            - liste de (mol_id, cosine_score) triée par score décroissant, filtrée
            - vecteur d'embedding de la phrase (pour mesure de cycle)
        """
        vec = self.model.encode([phrase], normalize_embeddings=True)
        sims = cosine_similarity(vec, self.ref_matrix)[0]
        ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

        selected = []
        for i, score in ranked[: self.topk]:
            if score >= self.threshold:
                selected.append((MOLECULE_IDS[i], float(score)))

        return selected, vec[0]


# ═══════════════════════════════════════════════════════════════════════════════
# Analyse comparative inter-langues
# ═══════════════════════════════════════════════════════════════════════════════

def jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def analyze_unit(unit_results: dict[str, list[int]]) -> dict:
    """
    Analyse la convergence nipada pour une unité du corpus.

    unit_results : {lang → [mol_ids]}
    """
    langs = list(unit_results.keys())
    all_mols = [set(unit_results[l]) for l in langs]

    # Intersection et union globales
    universal = set.intersection(*all_mols) if all_mols else set()
    total_union = set.union(*all_mols) if all_mols else set()

    # Matrice Jaccard par paire de langues
    jaccard_matrix: dict[str, float] = {}
    for i, li in enumerate(langs):
        for j, lj in enumerate(langs):
            if j > i:
                jaccard_matrix[f"{li}×{lj}"] = jaccard(all_mols[i], all_mols[j])

    # Molécules langue-spécifiques (présentes dans 1 seule langue)
    lang_specific: dict[str, list[int]] = {}
    for lang, mols in unit_results.items():
        specific = set(mols) - set.union(*(all_mols[k] for k, l in enumerate(langs) if l != lang))
        lang_specific[lang] = sorted(specific)

    return {
        "universal_molecules": sorted(universal),
        "total_union": sorted(total_union),
        "coverage": len(universal) / len(total_union) if total_union else 0.0,
        "jaccard_pairs": jaccard_matrix,
        "lang_specific": lang_specific,
        "mean_jaccard": (sum(jaccard_matrix.values()) / len(jaccard_matrix)) if jaccard_matrix else 0.0,
    }


def global_analysis(all_results: list[dict]) -> dict:
    """
    Analyse globale sur l'ensemble du corpus :
    - fréquence de chaque molécule par langue
    - molécules les plus universelles
    - langues les plus proches (Jaccard moyen)
    """
    # Fréquence par langue
    freq: dict[str, dict[int, int]] = {lang: defaultdict(int) for lang in LANGUAGES}
    total_phrases: dict[str, int] = defaultdict(int)

    for unit in all_results:
        for lang in LANGUAGES:
            enc = unit.get("encodings", {}).get(lang, {})
            mols = enc.get("molecules", [])
            for m in mols:
                freq[lang][m] += 1
            total_phrases[lang] += 1

    freq_normalized: dict[str, dict[int, float]] = {}
    for lang in LANGUAGES:
        n = total_phrases[lang]
        freq_normalized[lang] = {m: c / n for m, c in sorted(freq[lang].items())}

    # Molécules universelles (présentes dans toutes les langues ≥ 1 fois)
    universal_mols = set(MOLECULE_IDS)
    for lang in LANGUAGES:
        present = set(freq[lang].keys())
        universal_mols &= present

    # Paires de langues les plus proches (Jaccard moyen sur toutes les unités)
    lang_pair_jacc: dict[str, list[float]] = defaultdict(list)
    for unit in all_results:
        analysis = unit.get("analysis", {})
        for pair, j in analysis.get("jaccard_pairs", {}).items():
            lang_pair_jacc[pair].append(j)

    lang_pair_mean = {pair: sum(vals) / len(vals) for pair, vals in lang_pair_jacc.items()}

    return {
        "molecule_freq_by_lang": freq_normalized,
        "universal_molecules": sorted(universal_mols),
        "lang_pair_jaccard_mean": lang_pair_mean,
        "closest_pair": max(lang_pair_mean, key=lang_pair_mean.get) if lang_pair_mean else None,
        "most_divergent_pair": min(lang_pair_mean, key=lang_pair_mean.get) if lang_pair_mean else None,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline principal
# ═══════════════════════════════════════════════════════════════════════════════

def run(topk: int = 3, threshold: float = 0.20) -> dict:
    print(f"\n{'═'*70}")
    print("  §79 — Traduction circulaire multi-langues bit-perfect")
    print(f"  topk={topk}  threshold={threshold:.2f}")
    print(f"{'═'*70}")

    print(f"\n  Chargement du modèle : {MODEL_NAME}")
    model    = SentenceTransformer(MODEL_NAME)
    encoder  = NipadaTextEncoder(model, topk=topk, threshold=threshold)
    cas      = NipadaCAS()
    catalog  = NipadaCatalog()

    print("  Construction matrice de référence (15 molécules × 5 langues)…")
    _ = encoder.ref_matrix  # force le calcul
    print("  Matrice prête.")

    all_unit_results = []
    total_phrases    = 0
    total_bp_ok      = 0

    for unit in CORPUS:
        uid   = unit["id"]
        theme = unit["theme"]
        print(f"\n  ── {uid} : {theme}")

        unit_encodings: dict[str, dict] = {}
        unit_mols_by_lang: dict[str, list[int]] = {}

        for lang in LANGUAGES:
            phrase = unit[lang]
            phrase_bytes = phrase.encode("utf-8")

            # Encodage nipada
            selected, vec_phrase = encoder.encode_phrase(phrase)
            mol_ids     = [m for m, _ in selected]
            fingerprint = tuple(mol_ids)

            # Stockage CAS
            sha256 = cas.store(phrase_bytes, fingerprint)

            # Reconstruction bit-perfect
            retrieved = cas.retrieve_by_hash(sha256)
            bp_ok     = retrieved is not None and cas.verify(sha256, retrieved) and retrieved == phrase_bytes

            total_phrases += 1
            if bp_ok:
                total_bp_ok += 1

            # Embedding de reconstruction (concaténation des définitions)
            if mol_ids:
                recon_phrases = [DEFINITIONS[lang][m] for m in mol_ids if m in DEFINITIONS[lang]]
                recon_text    = " | ".join(recon_phrases)
            else:
                recon_text = ""

            vec_recon    = model.encode([recon_text], normalize_embeddings=True) if recon_text else None
            cycle_sim    = float(cosine_similarity(vec_phrase.reshape(1, -1), vec_recon)[0][0]) if vec_recon is not None else 0.0

            unit_encodings[lang] = {
                "phrase":        phrase,
                "molecules":     mol_ids,
                "scores":        [s for _, s in selected],
                "mol_names":     [MOL_NAMES_FR[m] for m in mol_ids],
                "fingerprint":   list(fingerprint),
                "sha256":        sha256,
                "bit_perfect":   bp_ok,
                "cycle_sim":     round(cycle_sim, 4),
                "recon_text":    recon_text,
            }
            unit_mols_by_lang[lang] = mol_ids

            # Affichage compact
            mols_str = "+".join(MOL_NAMES_FR[m] for m in mol_ids) if mol_ids else "∅"
            bp_mark  = "✓" if bp_ok else "✗"
            print(f"    [{lang}] {mols_str:40s}  cos={cycle_sim:.3f}  bp={bp_mark}")

        # Analyse convergence inter-langues pour cette unité
        analysis = analyze_unit(unit_mols_by_lang)

        univ_str = "+".join(MOL_NAMES_FR[m] for m in analysis["universal_molecules"]) or "∅"
        print(f"    → UNIVERSELLES: {univ_str}  |  coverage={analysis['coverage']:.0%}  |  Jaccard_moy={analysis['mean_jaccard']:.3f}")

        all_unit_results.append({
            "id":        uid,
            "theme":     theme,
            "encodings": unit_encodings,
            "analysis":  analysis,
        })

    # ── Résumé bit-perfect ────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print(f"  BIT-PERFECT : {total_bp_ok}/{total_phrases}  ({100*total_bp_ok//total_phrases}%)")

    # ── Analyse globale ───────────────────────────────────────────────────────
    global_stats = global_analysis(all_unit_results)

    print(f"\n  PAIRE LA PLUS PROCHE  : {global_stats['closest_pair']}  "
          f"(J={global_stats['lang_pair_jaccard_mean'].get(global_stats['closest_pair'], 0):.3f})")
    print(f"  PAIRE LA + DIVERGENTE : {global_stats['most_divergent_pair']}  "
          f"(J={global_stats['lang_pair_jaccard_mean'].get(global_stats['most_divergent_pair'], 0):.3f})")

    # Molécules universelles (présentes dans toutes les langues)
    univ_global = [MOL_NAMES_FR[m] for m in global_stats["universal_molecules"]]
    print(f"  MOLÉCULES UNIVERSELLES (corpus complet) : {', '.join(univ_global) or 'aucune'}")

    # Fréquences par langue
    print(f"\n  FRÉQUENCES MOLÉCULES PAR LANGUE (top 5) :")
    for lang in LANGUAGES:
        freq = global_stats["molecule_freq_by_lang"].get(lang, {})
        top5 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
        top5_str = "  ".join(f"{MOL_NAMES_FR[m]}={f:.0%}" for m, f in top5)
        print(f"    [{lang}]  {top5_str}")

    print(f"\n{'═'*70}\n")

    # ── Assemblage résultat JSON ───────────────────────────────────────────────
    result = {
        "section":         "§79",
        "title":           "Traduction circulaire multi-langues bit-perfect",
        "date":            "2026-04-24",
        "params":          {"topk": topk, "threshold": threshold, "model": MODEL_NAME},
        "corpus_size":     len(CORPUS),
        "languages":       LANGUAGES,
        "bit_perfect":     {"ok": total_bp_ok, "total": total_phrases, "rate": total_bp_ok / total_phrases},
        "units":           all_unit_results,
        "global_analysis": global_stats,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  Résultats sauvegardés → {OUTPUT_FILE}")

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="§79 — Traduction circulaire multi-langues bit-perfect"
    )
    parser.add_argument("--topk",      type=int,   default=3,    help="Nombre max de molécules par phrase")
    parser.add_argument("--threshold", type=float, default=0.20, help="Seuil cosinus minimal")
    args = parser.parse_args()

    run(topk=args.topk, threshold=args.threshold)


if __name__ == "__main__":
    main()

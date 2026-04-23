#!/usr/bin/env python3
"""
test_nipada_bootstrap.py — §77 : Nipada se décrit lui-même

Principe :
    Nipada est auto-descriptif si et seulement si les fonctionnalités
    manquantes du système peuvent être encodées par ses propres molécules.

    Pour chaque lacune fonctionnelle :
      1. Phrase → embedding → top-k molécules Z+ (cycle circulaire §76)
      2. Pour chaque molécule sélectionnée → imaginary_of() = iZ correspondant
      3. La lacune est l'auto-application de ces molécules = leur iZ

    Si le catalogue iZ couvre toutes les fonctionnalités nécessaires,
    nipada est un système fermé par auto-référence productive.

    Deuxième partie — entrées de second ordre (iZ × iZ) :
      Certaines fonctionnalités émergent de la combinaison de deux iZ.
      ex : APPRENTISSAGE×i (42i²) + MÉTALANGAGE×i (35i²) = décomposeur sémantique apprenant
      Ces combinaisons sont des "molécules nipada de second ordre" non encore nommées.

Usage :
    python scripts/test_nipada_bootstrap.py
"""

import json
import sys
import numpy as np
from pathlib import Path
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_engine import (
    NipadaCatalog, Domain,
    product_to_mask, mask_to_product, jaccard,
    atoms_in, level,
)

MODEL_NAME  = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_bootstrap.json"

# ── Structure nipada (copie conforme §76) ─────────────────────────────────────
MOLECULE_ATOMS = {
    2:   [],  3:   [],  5:   [],  7:   [],
    6:   [2, 3],  10:  [2, 5],  14:  [2, 7],  15:  [3, 5],
    21:  [3, 7],  35:  [5, 7],  30:  [2, 3, 5],  42:  [2, 3, 7],
    70:  [2, 5, 7],  105: [3, 5, 7],  210: [2, 3, 5, 7],
}
MOLECULE_IDS = list(MOLECULE_ATOMS.keys())
LANGUAGES    = ["en", "fr", "de", "es", "zh"]

DEFINITIONS = {
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

# ── Lacunes fonctionnelles à encoder ─────────────────────────────────────────
# Chaque lacune est décrite en deux langues + une prédiction théorique manuelle
GAPS = [
    {
        "id": "syntactic_decomposer",
        "name": "Décomposeur syntaxique",
        "phrase_en": "a system that decomposes a sentence into oriented semantic segments directed toward their meaning",
        "phrase_fr": "un système qui décompose une phrase en segments sémantiques orientés vers leur sens",
        "expected_z":  [42, 35, 7],    # TRANSFORMATION, RÉFÉRENCE, ORIENTATION
        "expected_iz": [42, 35],       # APPRENTISSAGE, MÉTALANGAGE
        "rationale": "Décomposer = transformer la phrase (42) en références orientées (35) → APPRENTISSAGE×MÉTALANGAGE",
    },
    {
        "id": "ontowave_navigator",
        "name": "Navigateur OntoWave",
        "phrase_en": "a navigator that follows relations between concepts and orients toward their connections",
        "phrase_fr": "un navigateur qui suit les relations entre concepts et s'oriente vers leurs connexions",
        "expected_z":  [70, 10, 35],   # INTENTION, COMPOSITION, RÉFÉRENCE
        "expected_iz": [70, 10],       # MOI, AUTOPOÏÈSE
        "rationale": "Naviguer = intention structurée (70) vers des compositions de références (10+35) → MOI×AUTOPOÏÈSE",
    },
    {
        "id": "binary_corpus_compressor",
        "name": "Compresseur binaire de corpus",
        "phrase_en": "a compressor that measures the ratio of differences between patterns in a corpus",
        "phrase_fr": "un compresseur qui mesure le rapport des différences entre les motifs d'un corpus",
        "expected_z":  [15, 10, 3],    # MESURE, COMPOSITION, DIFFÉRENCE
        "expected_iz": [15, 10],       # TRACE, AUTOPOÏÈSE
        "rationale": "Comprimer = mesurer (15) la composition (10) des différences (3) → TRACE×AUTOPOÏÈSE",
    },
    {
        "id": "nipada_self_description",
        "name": "Nipada auto-descriptif",
        "phrase_en": "a catalog that uses its own molecules to describe itself and its own structure",
        "phrase_fr": "un catalogue qui utilise ses propres molécules pour se décrire lui-même et sa propre structure",
        "expected_z":  [35, 6, 210],   # RÉFÉRENCE, EXISTENCE, INTÉGRATION
        "expected_iz": [35, 6],        # MÉTALANGAGE, CONSCIENCE
        "rationale": "Auto-description = référence (35) à sa propre existence (6) intégrée (210) → MÉTALANGAGE×CONSCIENCE",
    },
    {
        "id": "semantic_learning",
        "name": "Apprentissage sémantique",
        "phrase_en": "learning by applying transformations to new contexts to improve future decompositions",
        "phrase_fr": "apprendre en appliquant des transformations à de nouveaux contextes pour améliorer les décompositions",
        "expected_z":  [42, 70, 14],   # TRANSFORMATION, INTENTION, DEVENIR
        "expected_iz": [42, 70],       # APPRENTISSAGE, MOI
        "rationale": "Apprendre = transformation (42) intentionnelle (70) vers un devenir meilleur (14) → APPRENTISSAGE×MOI",
    },
    {
        "id": "bit_perfect_reconstruction",
        "name": "Reconstruction bit-perfect",
        "phrase_en": "reconstructing the original text with perfect fidelity by measuring each difference from the original",
        "phrase_fr": "reconstruire le texte original avec une fidélité parfaite en mesurant chaque différence par rapport à l'original",
        "expected_z":  [15, 105, 3],   # MESURE, TEMPS, DIFFÉRENCE
        "expected_iz": [15, 105],      # TRACE, MÉMOIRE
        "rationale": "Fidélité bit-perfect = mesurer (15) dans le temps (105) chaque différence (3) → TRACE×MÉMOIRE",
    },
    {
        "id": "nipada_completeness",
        "name": "Complétude du système",
        "phrase_en": "the whole system integrating being, difference, ratio and orientation is complete and self-sufficient",
        "phrase_fr": "le système entier intégrant l'être, la différence, le rapport et l'orientation est complet et auto-suffisant",
        "expected_z":  [210, 30, 70],  # INTÉGRATION, VIE, INTENTION
        "expected_iz": [210, 30],      # ABSOLU, INDIVIDUATION
        "rationale": "Complétude = intégration (210) auto-suffisante (30+70) → ABSOLU×INDIVIDUATION",
    },
]


# ── Construction de la matrice de référence (identique §76) ───────────────────

def build_reference_matrix(model) -> np.ndarray:
    all_phrases = []
    for mid in MOLECULE_IDS:
        for lang in LANGUAGES:
            all_phrases.append(DEFINITIONS[lang][mid])
    vecs = model.encode(all_phrases, batch_size=64, show_progress_bar=False,
                        normalize_embeddings=True)
    mol_vecs = []
    for i in range(len(MOLECULE_IDS)):
        start = i * len(LANGUAGES)
        group = vecs[start:start + len(LANGUAGES)]
        avg = group.mean(axis=0)
        avg /= np.linalg.norm(avg) + 1e-9
        mol_vecs.append(avg)
    return np.array(mol_vecs)


# ── Cycle circulaire pour une lacune ─────────────────────────────────────────

def encode_gap(gap: dict, ref_matrix: np.ndarray, model, catalog: NipadaCatalog,
               topk: int = 3, threshold: float = 0.18) -> dict:

    # Encodage en deux langues, moyenne
    vecs = model.encode(
        [gap["phrase_en"], gap["phrase_fr"]],
        normalize_embeddings=True,
    )
    vec_in = vecs.mean(axis=0, keepdims=True)
    vec_in /= np.linalg.norm(vec_in) + 1e-9

    sims = cosine_similarity(vec_in, ref_matrix)[0]
    ranked = sorted(enumerate(sims), key=lambda x: -x[1])

    selected = [(MOLECULE_IDS[i], float(s)) for i, s in ranked if s >= threshold][:topk]
    if not selected:
        i_best, s_best = ranked[0]
        selected = [(MOLECULE_IDS[i_best], float(s_best))]

    # Pour chaque molécule sélectionnée → imaginary_of()
    iz_entries = []
    for mol_id, sim in selected:
        entry_z = catalog.by_product(mol_id)
        entry_iz = catalog.imaginary_of(mol_id)
        iz_entries.append({
            "mol_id":   mol_id,
            "cosine":   sim,
            "name_fr":  entry_z.name if entry_z else "?",
            "name_en":  entry_z.name_en if entry_z else "?",
            "name_sa":  entry_z.name_sa if entry_z else "?",
            "atoms":    list(entry_z.atom_names) if entry_z else [],
            "iz_name":  entry_iz.name if entry_iz else "?",
            "iz_name_en": entry_iz.name_en if entry_iz else "?",
            "iz_name_sa": entry_iz.name_sa if entry_iz else "?",
        })

    # Recall vs prédiction théorique
    found_z = [e["mol_id"] for e in iz_entries]
    expected_z = gap["expected_z"]
    hits_z = [m for m in found_z if m in expected_z]
    recall_z = len(hits_z) / len(expected_z) if expected_z else 0.0

    found_iz_names = [e["iz_name"] for e in iz_entries]
    expected_iz_ids = gap["expected_iz"]
    expected_iz_entries = [catalog.imaginary_of(m) for m in expected_iz_ids]
    expected_iz_names = [e.name for e in expected_iz_entries if e]
    hits_iz = [n for n in found_iz_names if n in expected_iz_names]
    recall_iz = len(hits_iz) / len(expected_iz_names) if expected_iz_names else 0.0

    # Couverture atomique : union des atomes de toutes les molécules sélectionnées
    # atoms_in() retourne les primes (2, 3, 5, 7), pas les positions de bits
    all_primes: set[int] = set()
    for mol_id, _ in selected:
        mask = product_to_mask(mol_id)
        if mask:
            all_primes |= set(atoms_in(mask))
    prime_names = {2: "ÊTRE", 3: "DIFFÉRENCE", 5: "RAPPORT", 7: "ORIENTATION"}
    atoms_covered = [prime_names.get(p, str(p)) for p in sorted(all_primes)]
    is_complete = len(all_primes) == 4  # couvre tous les 4 atomes = INTÉGRATION

    return {
        "id":             gap["id"],
        "name":           gap["name"],
        "phrase_en":      gap["phrase_en"],
        "phrase_fr":      gap["phrase_fr"],
        "selected_z":     iz_entries,
        "found_z":        found_z,
        "expected_z":     expected_z,
        "recall_z":       round(recall_z, 3),
        "found_iz":       found_iz_names,
        "expected_iz":    expected_iz_names,
        "recall_iz":      round(recall_iz, 3),
        "atoms_covered":  atoms_covered,
        "is_complete":    is_complete,
        "rationale":      gap["rationale"],
        "all_similarities": [
            {"mol_id": MOLECULE_IDS[i], "cosine": float(s)} for i, s in ranked
        ],
    }


# ── Entrées de second ordre (iZ × iZ) ─────────────────────────────────────────

def build_second_order_entries(results: list[dict], catalog: NipadaCatalog) -> list[dict]:
    """
    Pour chaque lacune, identifie la paire iZ dominante et lui attribue
    un concept de second ordre (ni×nj = iZ combiné).

    Un concept de second ordre ne peut pas être exprimé dans le système
    4 bits de premier ordre — c'est une émergence du niveau méta.
    """
    second_order = []
    for r in results:
        iz_names = r["found_iz"][:2]
        if len(iz_names) < 2:
            continue
        # Les deux iZ dominants
        iz_a_name = iz_names[0]
        iz_b_name = iz_names[1]
        entry_a = catalog.by_name(iz_a_name)
        entry_b = catalog.by_name(iz_b_name)
        if not entry_a or not entry_b:
            continue

        # Jaccard entre les deux masques iZ
        j = jaccard(entry_a.mask, entry_b.mask)

        # Atomes combinés (primes 2,3,5,7)
        combined_primes = set(atoms_in(entry_a.mask)) | set(atoms_in(entry_b.mask))
        is_full = len(combined_primes) == 4
        prime_names = {2: "ÊTRE", 3: "DIFFÉRENCE", 5: "RAPPORT", 7: "ORIENTATION"}

        second_order.append({
            "gap_id":         r["id"],
            "gap_name":       r["name"],
            "iz_a":           {"name": iz_a_name, "mask": entry_a.mask, "name_sa": entry_a.name_sa},
            "iz_b":           {"name": iz_b_name, "mask": entry_b.mask, "name_sa": entry_b.name_sa},
            "jaccard_iz":     round(j, 3),
            "atoms_combined": [prime_names.get(p, str(p)) for p in sorted(combined_primes)],
            "is_full_integration": is_full,
            "second_order_formula": f"{iz_a_name}×{iz_b_name}",
        })

    return second_order


# ── Affichage ─────────────────────────────────────────────────────────────────

def print_gap(r: dict) -> None:
    print(f"\n{'─'*70}")
    print(f"  LACUNE : {r['name']} [{r['id']}]")
    print(f"  EN  : {r['phrase_en'][:75]}...")
    print(f"{'─'*70}")

    print("  Molécules Z+ trouvées (top-3) :")
    for e in r["selected_z"]:
        bar = "█" * int(e["cosine"] * 20)
        ok  = "✓" if e["mol_id"] in r["expected_z"] else " "
        print(f"    {ok} {e['mol_id']:3d} {e['name_fr']:20s}  cos={e['cosine']:.3f} {bar}")
        print(f"        iZ → {e['iz_name']:20s}  SA: {e['iz_name_sa']}")

    print(f"\n  Rappel Z+  : {r['recall_z']:.0%}  (attendus: {r['expected_z']})")
    print(f"  Rappel iZ  : {r['recall_iz']:.0%}  (attendus: {r['expected_iz']})")
    print(f"  Atomes couverts : {' × '.join(r['atoms_covered'])}")
    print(f"  Intégration complète : {'✓ OUI' if r['is_complete'] else '✗ NON'}")
    print(f"  Raisonnement : {r['rationale']}")


def print_second_order(so_list: list[dict]) -> None:
    print(f"\n{'═'*70}")
    print("  ENTRÉES DE SECOND ORDRE (iZ × iZ)")
    print(f"{'═'*70}")
    print("  Combinaisons émergentes — non exprimables en 4 bits de premier ordre\n")
    for so in so_list:
        full = "← INTÉGRATION complète" if so["is_full_integration"] else ""
        print(f"  {so['gap_name']} :")
        print(f"    {so['second_order_formula']}")
        print(f"    SA : {so['iz_a']['name_sa']} × {so['iz_b']['name_sa']}")
        print(f"    Jaccard iZ : {so['jaccard_iz']:.3f}  |  {' × '.join(so['atoms_combined'])} {full}")
        print()


# ── Vérification de clôture du système ────────────────────────────────────────

def check_system_closure(results: list[dict]) -> dict:
    """
    Nipada est auto-descriptif (clos) si :
      1. Chaque lacune est couverte par au moins une molécule connue (recall_z > 0)
      2. Chaque lacune a son iZ dans le catalogue (recall_iz > 0)
      3. L'union de toutes les lacunes = INTÉGRATION (tous les atomes couverts)
    """
    # Couverture atomique globale : union des primes de toutes les lacunes
    all_primes_global: set[int] = set()
    for r in results:
        for mol_id in r["found_z"]:
            mask = product_to_mask(mol_id)
            if mask:
                all_primes_global |= set(atoms_in(mask))

    mean_recall_z  = float(np.mean([r["recall_z"] for r in results]))
    mean_recall_iz = float(np.mean([r["recall_iz"] for r in results]))
    global_complete = len(all_primes_global) == 4
    is_closed = mean_recall_z > 0.30 and mean_recall_iz > 0.30 and global_complete

    return {
        "mean_recall_z":     round(mean_recall_z, 3),
        "mean_recall_iz":    round(mean_recall_iz, 3),
        "global_atoms":      list(all_primes_global),
        "global_complete":   global_complete,
        "is_closed":         is_closed,
        "verdict": (
            "CLOS — nipada peut se décrire lui-même avec ses propres molécules"
            if is_closed else
            "PARTIEL — certaines lacunes débordent le premier ordre"
        ),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  NIPADA BOOTSTRAP — §77")
    print("  Nipada se décrit lui-même : lacunes → molécules → iZ")
    print(f"  Modèle : {MODEL_NAME}")
    print("=" * 70)

    print("\n[1/4] Chargement du modèle...")
    model = SentenceTransformer(MODEL_NAME)
    print(f"  Dimension : {model.get_embedding_dimension()}")

    print("\n[2/4] Chargement du catalogue nipada...")
    catalog = NipadaCatalog()
    print(f"  {catalog.summary()}")

    print("\n[3/4] Construction de la matrice de référence...")
    ref_matrix = build_reference_matrix(model)
    print(f"  Matrice : {ref_matrix.shape}")

    print(f"\n[4/4] Encodage des {len(GAPS)} lacunes fonctionnelles...")
    results = []
    for gap in GAPS:
        r = encode_gap(gap, ref_matrix, model, catalog, topk=3, threshold=0.18)
        print_gap(r)
        results.append(r)

    # Entrées de second ordre
    second_order = build_second_order_entries(results, catalog)
    print_second_order(second_order)

    # Clôture du système
    closure = check_system_closure(results)
    print(f"\n{'═'*70}")
    print("  CLÔTURE DU SYSTÈME")
    print(f"{'═'*70}")
    print(f"  Recall Z+ moyen  : {closure['mean_recall_z']:.0%}")
    print(f"  Recall iZ moyen  : {closure['mean_recall_iz']:.0%}")
    print(f"  Couverture INTÉGRATION : {'✓ OUI (tous 4 atomes)' if closure['global_complete'] else '✗ NON'}")
    print(f"  Verdict : {closure['verdict']}")

    # Sauvegarde
    output = {
        "version":       "nipada_bootstrap_v1",
        "date":          "2026-04-23",
        "model":         MODEL_NAME,
        "n_gaps":        len(GAPS),
        "closure":       closure,
        "second_order":  second_order,
        "gaps":          results,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n  Résultats → {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

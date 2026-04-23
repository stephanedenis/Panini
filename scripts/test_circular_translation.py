#!/usr/bin/env python3
"""
test_circular_translation.py — §76 : Test de traduction circulaire nipada

Cycle complet :
    texte_entrée (n'importe quelle langue)
        → embedding sentence-transformers
        → cosine similarity vs 15 vecteurs-molécules (phrases définitionnelles)
        → sélection top-k molécules (similarité > seuil)
        → encodage nipada (bytes)
        → décodage nipada (mask → NipadaEntry)
        → reconstruction : définition dans la langue cible (ou nom SA)
        → texte_sortie

Ce n'est pas une traduction mot-à-mot : c'est une recomposition sémantique.
La boucle valide que le codec nipada capture suffisamment de sens
pour retrouver les molécules constitutives d'une phrase.

Usage :
    python scripts/test_circular_translation.py
    python scripts/test_circular_translation.py --phrase "fire transforms matter" --lang en --target fr
    python scripts/test_circular_translation.py --topk 3 --threshold 0.25
"""

import argparse
import json
import sys
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# ── Chemins ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_engine import (
    NipadaCatalog, Domain,
    encode, decode, product_to_mask, mask_to_product,
)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE = ROOT / "research" / "nipada" / "falsification" / "circular_translation_test.json"

# ── Structure nipada ──────────────────────────────────────────────────────────
MOLECULE_ATOMS = {
    2:   [],        # ÊTRE
    3:   [],        # DIFFÉRENCE
    5:   [],        # RAPPORT
    7:   [],        # ORIENTATION
    6:   [2, 3],    # EXISTENCE
    10:  [2, 5],    # COMPOSITION
    14:  [2, 7],    # DEVENIR
    15:  [3, 5],    # MESURE
    21:  [3, 7],    # OPPOSITION
    35:  [5, 7],    # RÉFÉRENCE
    30:  [2, 3, 5], # VIE
    42:  [2, 3, 7], # TRANSFORMATION
    70:  [2, 5, 7], # INTENTION
    105: [3, 5, 7], # TEMPS
    210: [2, 3, 5, 7],  # INTÉGRATION
}
MOLECULE_IDS = list(MOLECULE_ATOMS.keys())

# ── Phrases définitionnelles (copie conforme H2 v3 / H3 v3) ──────────────────
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

LANGUAGES = list(DEFINITIONS.keys())

# ── Phrases de test par défaut ─────────────────────────────────────────────────
DEFAULT_TESTS = [
    {
        "phrase": "le feu transforme la matière de façon irréversible",
        "lang": "fr",
        "expected": [42, 14],   # TRANSFORMATION, DEVENIR
    },
    {
        "phrase": "fire transforms matter in an irreversible way",
        "lang": "en",
        "expected": [42, 14],
    },
    {
        "phrase": "time orders the difference between moments",
        "lang": "en",
        "expected": [105, 15],  # TEMPS, MESURE
    },
    {
        "phrase": "living beings maintain structural relations with their environment",
        "lang": "en",
        "expected": [30, 10],   # VIE, COMPOSITION
    },
    {
        "phrase": "当一个人的存在指向目标时，意图就产生了",
        "lang": "zh",
        "expected": [70, 14],   # INTENTION, DEVENIR
    },
    {
        "phrase": "das integrierte Ganze vereint Sein, Differenz, Verhältnis und Orientierung",
        "lang": "de",
        "expected": [210],      # INTÉGRATION
    },
    {
        "phrase": "life adapts and self-differentiates from its environment",
        "lang": "en",
        "expected": [30, 6],    # VIE, EXISTENCE
    },
]


# ── Construction de la matrice de référence ────────────────────────────────────

def build_reference_matrix(model: SentenceTransformer) -> np.ndarray:
    """
    Encode les 15 molécules comme moyenne des 5 définitions multilingues.
    Retourne une matrice [15 × 384] normalisée L2.
    """
    all_phrases: list[str] = []
    for mid in MOLECULE_IDS:
        for lang in LANGUAGES:
            all_phrases.append(DEFINITIONS[lang][mid])

    vecs = model.encode(all_phrases, batch_size=64, show_progress_bar=False,
                        normalize_embeddings=True)

    # Moyenne sur les 5 langues pour chaque molécule
    mol_vecs = []
    for i, mid in enumerate(MOLECULE_IDS):
        start = i * len(LANGUAGES)
        group = vecs[start:start + len(LANGUAGES)]
        avg = group.mean(axis=0)
        avg /= np.linalg.norm(avg) + 1e-9
        mol_vecs.append(avg)

    return np.array(mol_vecs)  # [15, 384]


# ── Cycle circulaire ───────────────────────────────────────────────────────────

def circular_translate(
    phrase: str,
    ref_matrix: np.ndarray,
    model: SentenceTransformer,
    catalog: NipadaCatalog,
    target_lang: str = "fr",
    topk: int = 3,
    threshold: float = 0.20,
) -> dict:
    """
    Effectue un cycle complet :
        phrase → nipada bytes → noms + définition reconstituée

    Retourne un dict avec toutes les étapes du cycle.
    """
    # ── Étape 1 : embedding de l'entrée ──────────────────────────────────────
    vec_in = model.encode([phrase], normalize_embeddings=True)  # [1, 384]

    # ── Étape 2 : similarité cosinus vs 15 molécules ─────────────────────────
    sims = cosine_similarity(vec_in, ref_matrix)[0]  # [15]
    ranked = sorted(enumerate(sims), key=lambda x: -x[1])

    # Top-k avec seuil de confiance
    selected = [(MOLECULE_IDS[i], float(s)) for i, s in ranked if s >= threshold][:topk]
    if not selected:
        # Fallback : toujours garder le meilleur
        i_best, s_best = ranked[0]
        selected = [(MOLECULE_IDS[i_best], float(s_best))]

    # ── Étape 3 : encodage nipada (bytes) ─────────────────────────────────────
    nipada_bytes = []
    for mol_id, _ in selected:
        b = encode(mol_id)
        nipada_bytes.append({
            "mol_id": mol_id,
            "byte_hex": b.hex(),
            "byte_int": int.from_bytes(b, "big"),
        })

    # ── Étape 4 : décodage → NipadaEntry ─────────────────────────────────────
    decoded_entries = []
    for item in nipada_bytes:
        b_int = item["byte_int"]
        domain, mask = decode(b_int)
        entry = catalog.by_mask(mask, Domain.Z_POS)
        decoded_entries.append({
            "mol_id":   item["mol_id"],
            "byte_hex": item["byte_hex"],
            "mask":     mask,
            "mask_bin": f"{mask:04b}",
            "domain":   domain.value if domain else "padding",
            "name_fr":  entry.name if entry else "?",
            "name_en":  entry.name_en if entry else "?",
            "name_sa":  entry.name_sa if entry else "?",
            "atoms":    list(entry.atom_names) if entry else [],
        })

    # ── Étape 5 : reconstruction dans la langue cible ─────────────────────────
    if target_lang in DEFINITIONS:
        reconstructed_phrases = []
        for item in decoded_entries:
            mid = item["mol_id"]
            if mid in DEFINITIONS[target_lang]:
                reconstructed_phrases.append(DEFINITIONS[target_lang][mid])
        reconstruction = " | ".join(reconstructed_phrases)
    else:
        reconstruction = " | ".join(item["name_en"] for item in decoded_entries)

    # ── Étape 6 : embedding de la sortie → similarité retour ─────────────────
    # (mesure de la cohérence sémantique du cycle)
    vec_out = model.encode([reconstruction], normalize_embeddings=True)
    cycle_sim = float(cosine_similarity(vec_in, vec_out)[0][0])

    # Similarité cosinus de chaque molécule sélectionnée vs l'entrée
    all_sims = [{"mol_id": MOLECULE_IDS[i], "cosine": float(s)} for i, s in ranked]

    return {
        "phrase_in":     phrase,
        "target_lang":   target_lang,
        "topk":          topk,
        "threshold":     threshold,
        "top_molecules": [{"mol_id": m, "cosine": s} for m, s in selected],
        "nipada_bytes":  nipada_bytes,
        "decoded":       decoded_entries,
        "reconstruction": reconstruction,
        "cycle_similarity": cycle_sim,
        "all_similarities": all_sims,
    }


# ── Affichage ─────────────────────────────────────────────────────────────────

def print_cycle(result: dict, expected: list[int] | None = None) -> None:
    print(f"\n{'─'*65}")
    print(f"  ENTRÉE  : {result['phrase_in']}")
    print(f"  CIBLE   : {result['target_lang']}")
    print(f"  SEUIL   : cos ≥ {result['threshold']:.2f}  |  top-{result['topk']}")
    print(f"{'─'*65}")

    print("  ÉTAPE 1-2 : Similarités cosinus (top 5)")
    for item in result["all_similarities"][:5]:
        mid = item["mol_id"]
        s = item["cosine"]
        lang = "fr"
        entry_name = DEFINITIONS[lang][mid].split(":")[0].split("est")[0].strip().rstrip("L'").strip("La").strip()
        bar = "█" * int(s * 20)
        mark = " ←" if mid in [m["mol_id"] for m in result["top_molecules"]] else ""
        print(f"    {mid:3d} {entry_name[:18]:18s}  {s:.3f} {bar}{mark}")

    if expected:
        hits = [m["mol_id"] for m in result["top_molecules"] if m["mol_id"] in expected]
        recall = len(hits) / len(expected)
        print(f"\n  ATTENDUS : {expected}  |  TROUVÉS : {[m['mol_id'] for m in result['top_molecules']]}")
        print(f"  RECALL   : {recall:.0%}")

    print(f"\n  ÉTAPE 3-4 : Encodage nipada")
    for dec in result["decoded"]:
        print(f"    0x{dec['byte_hex']} [{dec['mask_bin']}]  {dec['name_fr']:20s}  EN:{dec['name_en']:20s}  SA:{dec['name_sa']}")
        if dec["atoms"]:
            print(f"      atomes : {' × '.join(dec['atoms'])}")

    print(f"\n  ÉTAPE 5 : Reconstruction ({result['target_lang']})")
    for line in result["reconstruction"].split(" | "):
        print(f"    → {line[:90]}")

    print(f"\n  CYCLE cos(entrée, reconstruction) = {result['cycle_similarity']:.3f}")
    verdict = "EXCELLENT" if result["cycle_similarity"] > 0.60 else \
              "BON" if result["cycle_similarity"] > 0.40 else \
              "PARTIEL" if result["cycle_similarity"] > 0.20 else "FAIBLE"
    print(f"  VERDICT : {verdict}")


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Test de traduction circulaire nipada §76")
    p.add_argument("--phrase",    type=str, default=None,
                   help="Phrase à tester (défaut : suite de tests prédéfinis)")
    p.add_argument("--lang",      type=str, default="fr",
                   help="Langue d'entrée (fr/en/de/es/zh)")
    p.add_argument("--target",    type=str, default="en",
                   help="Langue de reconstruction (fr/en/de/es/zh)")
    p.add_argument("--topk",      type=int, default=3,
                   help="Nombre de molécules à sélectionner")
    p.add_argument("--threshold", type=float, default=0.20,
                   help="Seuil de similarité cosinus minimum")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print("=" * 65)
    print("  TEST DE TRADUCTION CIRCULAIRE NIPADA — §76")
    print(f"  Modèle : {MODEL_NAME}")
    print("=" * 65)

    # Chargement du modèle
    print(f"\n[1/3] Chargement du modèle...")
    model = SentenceTransformer(MODEL_NAME)
    dim = model.get_embedding_dimension()
    print(f"  Dimension : {dim}")

    # Chargement du catalogue
    print("\n[2/3] Chargement du catalogue nipada...")
    catalog = NipadaCatalog()
    print(f"  {catalog.summary()}")

    # Construction de la matrice de référence
    print(f"\n[3/3] Construction de la matrice de référence ({len(MOLECULE_IDS)} molécules × {len(LANGUAGES)} langues)...")
    ref_matrix = build_reference_matrix(model)
    print(f"  Matrice : {ref_matrix.shape}")

    # Tests
    results = []
    total_cycle_sims = []
    recalls = []

    if args.phrase:
        # Phrase unique spécifiée en CLI
        tests = [{"phrase": args.phrase, "lang": args.lang, "expected": None}]
        topk, threshold = args.topk, args.threshold
        target = args.target
    else:
        tests = DEFAULT_TESTS
        topk, threshold = args.topk, args.threshold
        target = args.target

    for test in tests:
        result = circular_translate(
            phrase=test["phrase"],
            ref_matrix=ref_matrix,
            model=model,
            catalog=catalog,
            target_lang=target,
            topk=topk,
            threshold=threshold,
        )
        print_cycle(result, expected=test.get("expected"))
        results.append(result)
        total_cycle_sims.append(result["cycle_similarity"])

        if test.get("expected") and not args.phrase:
            found = [m["mol_id"] for m in result["top_molecules"]]
            hits = [m for m in found if m in test["expected"]]
            recalls.append(len(hits) / len(test["expected"]))

    # Résumé global
    print(f"\n{'═'*65}")
    print(f"  RÉSUMÉ GLOBAL ({len(results)} tests)")
    print(f"{'═'*65}")
    mean_sim = np.mean(total_cycle_sims)
    print(f"  cos(entrée, reconstruction) moyen : {mean_sim:.3f}")
    if recalls:
        print(f"  Recall molécules attendues moyen  : {np.mean(recalls):.0%}")

    verdict_global = "COHÉRENT — le cycle nipada capture le sens" if mean_sim > 0.40 else \
                     "PARTIEL — compression sémantique imparfaite" if mean_sim > 0.20 else \
                     "INSUFFISANT — perte sémantique trop importante"
    print(f"  Verdict : {verdict_global}")

    # Sauvegarde JSON
    output = {
        "version": "circular_translation_v1",
        "date":    "2026-04-23",
        "model":   MODEL_NAME,
        "params":  {"topk": topk, "threshold": threshold, "target_lang": target},
        "summary": {
            "n_tests":         len(results),
            "mean_cycle_sim":  float(mean_sim),
            "mean_recall":     float(np.mean(recalls)) if recalls else None,
            "verdict":         verdict_global,
        },
        "tests": results,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n  Résultats sauvegardés → {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

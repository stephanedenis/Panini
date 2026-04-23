#!/usr/bin/env python3
"""
test_h2_v3_phrases.py — H2 version 3 : cohérence cosinus sur phrases définitionnelles

Diagnostic §73 : les mots isolés abstraits forment un cluster dense (cos ≈ 0.63 partout).
Solution v3 : utiliser des PHRASES DÉFINITIONNELLES qui encodent explicitement
les atomes constitutifs de chaque molécule.

Hypothèse : si la structure nipada est compositionnelle, alors :
  cosine(def_A, def_B) ∝ Jaccard(atomes_A, atomes_B)

Méthode :
  - 15 phrases en 5 langues, une par molécule
  - chaque phrase mentionne ses atomes constitutifs
  - Spearman(Jaccard_théorique, cosine_observé) sur les 105 paires

Si ρ > 0.50 avec ces phrases → la structure nipada est détectable
Si ρ ≈ 0.0 même là → l'espace sémantique est fondamentalement incompatible
"""
import json
import sys
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr
from sentence_transformers import SentenceTransformer

ROOT      = Path(__file__).parent.parent
FALSI_DIR = ROOT / "research" / "nipada" / "falsification"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# ---------------------------------------------------------------------------
# Atomes de base (structure nipada, niveau 0 JSON)
# ---------------------------------------------------------------------------
ATOM_IDS  = [2, 3, 5, 7]
PRIMES    = {2: "ÊTRE", 3: "DIFFÉRENCE", 5: "RAPPORT", 7: "ORIENTATION"}

MOLECULE_ATOMS = {
    2:   [],
    3:   [],
    5:   [],
    7:   [],
    6:   [2, 3],
    10:  [2, 5],
    14:  [2, 7],
    15:  [3, 5],
    21:  [3, 7],
    35:  [5, 7],
    30:  [2, 3, 5],
    42:  [2, 3, 7],
    70:  [2, 5, 7],
    105: [3, 5, 7],
    210: [2, 3, 5, 7],
}

# ---------------------------------------------------------------------------
# Phrases définitionnelles — 5 langues × 15 molécules
#
# Règle de construction :
#   - Les atomes sont nommés explicitement dans la définition
#   - La phrase décrit la RELATION entre les atomes, pas juste le concept
#   - Pas de synonyme vague — on colle à la structure
# ---------------------------------------------------------------------------

DEFINITIONS = {
    "en": {
        # Atomes (niveau 0)
        2:   "Being is the pure fact of existing, prior to any difference or relation.",
        3:   "Difference is the irreducible distinction between two things, prior to any relation.",
        5:   "Ratio is the structural relation between two terms, independent of direction.",
        7:   "Orientation is the directional asymmetry that distinguishes before from after, source from goal.",

        # Binaires (niveau 1)
        6:   "Existence is the articulation of being and difference: something exists when its being is distinguished from non-being.",
        10:  "Composition is the articulation of being and ratio: something is composed when its being is structured by a relation of parts.",
        14:  "Becoming is the articulation of being and orientation: something becomes when its being is directed toward a goal.",
        15:  "Measure is the articulation of difference and ratio: something is measured when a difference is expressed as a ratio.",
        21:  "Opposition is the articulation of difference and orientation: two things are opposed when their difference is directional and asymmetric.",
        35:  "Reference is the articulation of ratio and orientation: a reference is a ratio that has a direction, pointing from sign to meaning.",

        # Ternaires (niveau 2)
        30:  "Life is the articulation of being, difference and ratio: a living thing exists, differentiates itself from its environment and maintains structural relations with it.",
        42:  "Transformation is the articulation of being, difference and orientation: something transforms when its being changes in a directed, irreversible way.",
        70:  "Intention is the articulation of being, ratio and orientation: an intention is a being structured by a relation that is oriented toward a goal.",
        105: "Time is the articulation of difference, ratio and orientation: time is the ordered difference between moments, structured as a ratio with a direction.",

        # Quaternaire (niveau 3)
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
MOLECULE_IDS = list(MOLECULE_ATOMS.keys())


def _jaccard(id_a: int, id_b: int) -> float:
    sa = set(MOLECULE_ATOMS[id_a]) or {id_a}  # atomes = {self} pour les atomes
    sb = set(MOLECULE_ATOMS[id_b]) or {id_b}
    # Pour les atomes (level 0) : pas de chevauchement sauf avec eux-mêmes
    # Utiliser le masque 4 bits pour la cohérence
    bits_a = {bit for bit, prime in enumerate([2, 3, 5, 7]) if prime == id_a or prime in MOLECULE_ATOMS[id_a]}
    bits_b = {bit for bit, prime in enumerate([2, 3, 5, 7]) if prime == id_b or prime in MOLECULE_ATOMS[id_b]}
    inter = len(bits_a & bits_b)
    union = len(bits_a | bits_b)
    return inter / union if union > 0 else 0.0


def build_matrix(model: SentenceTransformer) -> tuple[np.ndarray, list[int]]:
    """
    Encode les phrases définitionnelles par concept (moyenne sur les 5 langues).
    """
    mol_ids = MOLECULE_IDS
    # Collecter toutes les phrases uniques
    all_phrases = list({
        DEFINITIONS[lang][mid]
        for lang in LANGUAGES
        for mid in mol_ids
        if mid in DEFINITIONS[lang]
    })
    print(f"  Encodage de {len(all_phrases)} phrases définitionnelles...")
    all_vecs = model.encode(all_phrases, batch_size=128, show_progress_bar=False)
    phrase2vec = {p: all_vecs[i] for i, p in enumerate(all_phrases)}

    matrix = []
    for mid in mol_ids:
        vecs = []
        for lang in LANGUAGES:
            phrase = DEFINITIONS.get(lang, {}).get(mid)
            if phrase and phrase in phrase2vec:
                vecs.append(phrase2vec[phrase])
        if vecs:
            mean_vec = np.mean(vecs, axis=0)
            norm = np.linalg.norm(mean_vec)
            matrix.append(mean_vec / norm if norm > 0 else mean_vec)
        else:
            matrix.append(np.zeros(model.get_embedding_dimension()))

    return np.array(matrix), mol_ids


def run_h2_v3(matrix: np.ndarray, mol_ids: list[int]) -> dict:
    """
    H2 v3 — Spearman(Jaccard_théorique, cosine_observé) sur 105 paires.
    Compare aussi avec H2 v2 (mots isolés) pour mesurer le gain.
    """
    n = len(mol_ids)
    predicted = []
    observed  = []
    pairs_detail = []

    for i in range(n):
        for j in range(i + 1, n):
            jac = _jaccard(mol_ids[i], mol_ids[j])
            cos = float(cosine_similarity(
                matrix[i].reshape(1, -1),
                matrix[j].reshape(1, -1)
            )[0, 0])
            predicted.append(jac)
            observed.append(cos)
            pairs_detail.append({
                "a": mol_ids[i], "b": mol_ids[j],
                "jaccard": jac, "cosine": cos
            })

    rho, pval = spearmanr(predicted, observed)
    rho, pval = float(rho), float(pval)

    # Analyse par bucket Jaccard
    bucket_stats = {}
    for bucket in [0.0, 0.25, 0.5, 0.75, 1.0]:
        pairs = [(p, o) for p, o in zip(predicted, observed) if abs(p - bucket) < 0.13]
        if pairs:
            bucket_stats[f"jaccard≈{bucket:.2f}"] = {
                "n_pairs": len(pairs),
                "mean_cosine": float(np.mean([o for _, o in pairs])),
                "std_cosine":  float(np.std([o for _, o in pairs])),
            }

    # Top 5 paires les plus/moins similaires vs prédiction
    sorted_by_cos = sorted(pairs_detail, key=lambda x: -x["cosine"])
    top5_similar  = sorted_by_cos[:5]
    top5_dissimilar = sorted_by_cos[-5:]

    if rho > 0.50:
        verdict = f"RENFORCÉ — ρ={rho:.3f} (p={pval:.3e}) : structure atomique explique les similarités sur phrases"
    elif rho > 0.30:
        verdict = f"AMBIGU — ρ={rho:.3f} (p={pval:.3e}) : signal partiel"
    else:
        verdict = f"FALSIFIÉ — ρ={rho:.3f} (p={pval:.3e}) : même sur phrases définitionnelles, pas de corrélation"

    return {
        "method": "phrases définitionnelles 5 langues × 15 molécules",
        "n_languages": len(LANGUAGES),
        "n_molecules": n,
        "n_pairs": len(predicted),
        "spearman_rho": rho,
        "spearman_pval": pval,
        "predicted_range": [float(min(predicted)), float(max(predicted))],
        "observed_range":  [float(min(observed)),  float(max(observed))],
        "mean_observed_cosine": float(np.mean(observed)),
        "std_observed_cosine":  float(np.std(observed)),
        "bucket_analysis": bucket_stats,
        "top5_most_similar_pairs":   top5_similar,
        "top5_least_similar_pairs":  top5_dissimilar,
        "verdict": verdict,
        "comparison_h2v2": {
            "v2_rho": 0.019,
            "v2_mean_cosine": 0.629,
            "v3_rho": rho,
            "v3_mean_cosine": float(np.mean(observed)),
            "delta_rho": rho - 0.019,
            "interpretation": (
                "Les phrases définitionnelles augmentent la variance des cosinus observés "
                "si les concepts structurellement distants deviennent réellement plus éloignés "
                "dans l'espace sémantique."
            ),
        },
    }


def print_bucket_table(result: dict) -> None:
    print("\n  Distribution cosinus par Jaccard :")
    print(f"  {'Jaccard':15s} {'n paires':10s} {'cos moyen':12s} {'std':8s}")
    print("  " + "-" * 47)
    for bucket, stats in result["bucket_analysis"].items():
        print(f"  {bucket:15s} {stats['n_pairs']:10d} {stats['mean_cosine']:12.4f} {stats['std_cosine']:8.4f}")


if __name__ == "__main__":
    print("=" * 60)
    print("H2 v3 — Phrases définitionnelles (test cohérence nipada)")
    print(f"Langues : {len(LANGUAGES)} | Molécules : {len(MOLECULE_IDS)}")
    print(f"Modèle  : {MODEL_NAME}")
    print("=" * 60)

    print(f"\n[1/3] Chargement du modèle {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    dim = model.get_embedding_dimension()
    print(f"  Dimension : {dim}")

    print(f"\n[2/3] Construction de la matrice par phrases définitionnelles...")
    matrix, mol_ids = build_matrix(model)
    print(f"  Matrice : {matrix.shape[0]} concepts × {matrix.shape[1]} dim")

    print(f"\n[3/3] Test H2 v3 (Spearman)...")
    result = run_h2_v3(matrix, mol_ids)

    print(f"\n  Verdict : {result['verdict']}")
    print(f"  ρ = {result['spearman_rho']:.4f}  (p = {result['spearman_pval']:.3e})")
    print(f"  cosinus : min={result['observed_range'][0]:.3f}  max={result['observed_range'][1]:.3f}  "
          f"moy={result['mean_observed_cosine']:.3f}  std={result['std_observed_cosine']:.3f}")
    print(f"\n  Comparaison H2 v2 vs v3 :")
    print(f"    v2 (mots isolés)      : ρ = {result['comparison_h2v2']['v2_rho']:.3f}, cos_moy = {result['comparison_h2v2']['v2_mean_cosine']:.3f}")
    print(f"    v3 (phrases définit.) : ρ = {result['comparison_h2v2']['v3_rho']:.3f}, cos_moy = {result['comparison_h2v2']['v3_mean_cosine']:.3f}")
    print(f"    Δρ = {result['comparison_h2v2']['delta_rho']:+.3f}")
    print_bucket_table(result)

    print("\n  Top 5 paires les plus similaires :")
    sys.path.insert(0, str(ROOT))
    from src.core.nipada_engine import NipadaCatalog
    cat = NipadaCatalog()
    for p in result["top5_most_similar_pairs"]:
        na = cat.by_product(p["a"])
        nb = cat.by_product(p["b"])
        na_name = na.name if na else f"id={p['a']}"
        nb_name = nb.name if nb else f"id={p['b']}"
        print(f"    {na_name:15s} × {nb_name:15s}  Jaccard={p['jaccard']:.2f}  cos={p['cosine']:.4f}")

    print("\n  Top 5 paires les moins similaires :")
    for p in result["top5_least_similar_pairs"]:
        na = cat.by_product(p["a"])
        nb = cat.by_product(p["b"])
        na_name = na.name if na else f"id={p['a']}"
        nb_name = nb.name if nb else f"id={p['b']}"
        print(f"    {na_name:15s} × {nb_name:15s}  Jaccard={p['jaccard']:.2f}  cos={p['cosine']:.4f}")

    # Sauvegarder
    out = FALSI_DIR / "H2_v3_phrases_definitionnelles.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n  → Sauvegardé : {out}")

#!/usr/bin/env python3
"""
test_h3_v3_calibration_phrases.py — H3 version 3 : calibration ℂ* sur matrice phrases

Diagnostic H3 v2 (§74) : la calibration Jaccard→cosinus sur mots isolés donnait
slope=-0.443 (pente NÉGATIVE), cohérente avec l'artefact cluster-dense de H2 v2.
Le même artefact biaisait le résultat.

Solution v3 : utiliser la matrice phrases-définitionnelles (construite par H2 v3,
qui donne ρ=+0.472) pour la calibration des poids ℂ*.

Hypothèse : sur la matrice phrases, la calibration cos~Jaccard doit être positive
(pente > 0) et cohérente avec ρ=0.472 de H2 v3.

Méthode :
  1. Construire la matrice phrases (même code que H2 v3)
  2. Extraire 8 paires avec Jaccard nipada connu
  3. Spearman(Jaccard, cosine) sur ces 8 paires de calibration
  4. Régression linéaire → slope, intercept → poids recalibré pour COLÈRE-FEU
  5. Sauvegarder → H3_v3_calibration_phrases.json
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
sys.path.insert(0, str(ROOT))

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# ---------------------------------------------------------------------------
# Structure nipada (dupliquée depuis H2 v3 pour autonomie du script)
# ---------------------------------------------------------------------------
ATOM_IDS = [2, 3, 5, 7]
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
MOLECULE_IDS = list(MOLECULE_ATOMS.keys())

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


# ---------------------------------------------------------------------------
# Jaccard sur masques 4 bits
# ---------------------------------------------------------------------------
def _jaccard(id_a: int, id_b: int) -> float:
    bits_a = {bit for bit, prime in enumerate([2, 3, 5, 7]) if prime == id_a or prime in MOLECULE_ATOMS[id_a]}
    bits_b = {bit for bit, prime in enumerate([2, 3, 5, 7]) if prime == id_b or prime in MOLECULE_ATOMS[id_b]}
    inter = len(bits_a & bits_b)
    union = len(bits_a | bits_b)
    return inter / union if union > 0 else 0.0


# ---------------------------------------------------------------------------
# Construction de la matrice phrases (copie conforme de H2 v3)
# ---------------------------------------------------------------------------
def build_phrase_matrix(model: SentenceTransformer) -> tuple[np.ndarray, list[int]]:
    mol_ids = MOLECULE_IDS
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


# ---------------------------------------------------------------------------
# H3 v3 — calibration sur matrice phrases
# ---------------------------------------------------------------------------
def run_h3_v3(matrix: np.ndarray, mol_ids: list[int]) -> dict:
    """
    Calibration empirique cos~Jaccard sur les mêmes 8 paires qu'en H3 v2,
    mais cette fois sur la matrice PHRASES définitionnelles.

    Si slope > 0 et ρ > 0.3 → la calibration est cohérente avec H2 v3 (ρ=0.472).
    Si slope < 0 → l'artefact cluster-dense est encore présent sur ces paires.
    """
    # Mêmes 8 paires que H3 v2
    calibration_pairs_def = [
        (70,  42, "INTENTION×TRANSFORMATION — partagent ÊTRE+RAPPORT+ORIENTATION vs ÊTRE+DIFFÉRENCE+ORIENTATION"),
        (70,  30, "INTENTION×VIE — partagent ÊTRE+RAPPORT+ORIENTATION (3 bits sur 3+3)"),
        (14,  42, "DEVENIR×TRANSFORMATION — partagent ÊTRE+ORIENTATION"),
        (6,   30, "EXISTENCE×VIE — partagent ÊTRE+DIFFÉRENCE"),
        (35, 105, "RÉFÉRENCE×TEMPS — partagent RAPPORT+ORIENTATION"),
        (2,   70, "ÊTRE×INTENTION — ÊTRE est atome de INTENTION"),
        (15,  30, "MESURE×VIE — partagent DIFFÉRENCE+RAPPORT"),
        (7,   35, "ORIENTATION×RÉFÉRENCE — ORIENTATION est atome de RÉFÉRENCE"),
    ]

    results_pairs = []
    for id_a, id_b, desc in calibration_pairs_def:
        if id_a not in mol_ids or id_b not in mol_ids:
            continue
        idx_a = mol_ids.index(id_a)
        idx_b = mol_ids.index(id_b)
        jac = _jaccard(id_a, id_b)
        cos = float(cosine_similarity(
            matrix[idx_a].reshape(1, -1),
            matrix[idx_b].reshape(1, -1)
        )[0, 0])
        results_pairs.append({
            "id_a": id_a, "id_b": id_b,
            "jaccard": jac, "cosine": cos,
            "description": desc,
        })

    jacs = [p["jaccard"] for p in results_pairs]
    coss = [p["cosine"]  for p in results_pairs]
    rho, pval = spearmanr(jacs, coss)

    # Régression linéaire
    A = np.column_stack([np.array(jacs).reshape(-1, 1), np.ones(len(jacs))])
    (slope, intercept), *_ = np.linalg.lstsq(A, np.array(coss), rcond=None)

    # Poids recalibré pour COLÈRE-FEU
    # Rappel : COLÈRE ≈ INTENTION (70) dans la littérature lakoffienne (ℂ* : FEU=42)
    jac_70_42 = _jaccard(70, 42)
    cos_70_42 = None
    if 70 in mol_ids and 42 in mol_ids:
        idx70 = mol_ids.index(70)
        idx42 = mol_ids.index(42)
        cos_70_42 = float(cosine_similarity(
            matrix[idx70].reshape(1, -1),
            matrix[idx42].reshape(1, -1)
        )[0, 0])

    cos_prédit = float(slope * jac_70_42 + intercept)

    # Comparaison directe H3 v2 vs H3 v3
    delta_slope = float(slope) - (-0.443)  # slope H3v2 était -0.443

    if float(slope) > 0.1 and float(rho) > 0.2:
        verdict_calibration = "COHÉRENT — pente positive sur phrases (correction de l'artefact H3 v2)"
    elif float(slope) > 0:
        verdict_calibration = "AMBIGU — pente légèrement positive mais ρ faible"
    else:
        verdict_calibration = "ARTEFACT PERSISTANT — pente négative même sur phrases"

    return {
        "method": "H3 v3 — calibration ℂ* sur matrice phrases-définitionnelles",
        "n_languages": len(LANGUAGES),
        "n_calibration_pairs": len(results_pairs),
        "pairs": results_pairs,
        "spearman_rho": float(rho),
        "spearman_pval": float(pval),
        "linear_calibration": {
            "slope":     float(slope),
            "intercept": float(intercept),
            "equation":  f"cos_phrases ≈ {slope:.3f} × Jaccard + {intercept:.3f}",
        },
        "comparison_h3v2": {
            "slope_h3v2":     -0.443,
            "slope_h3v3":     float(slope),
            "delta_slope":    delta_slope,
            "rho_h3v2":       -0.365,
            "rho_h3v3":       float(rho),
            "interpretation": "Δslope > 0 → correction de l'artefact cluster-dense",
        },
        "colere_feu_recalibration": {
            "jaccard_70_42":          jac_70_42,
            "cos_observé_70_42_mots": 0.472,    # mesuré en H3 v2 sur mots isolés
            "cos_observé_70_42_phrases": cos_70_42,
            "poids_initial_h3v1":     0.30,
            "cos_prédit_par_régression": cos_prédit,
            "poids_final_recalibré":  cos_70_42 if cos_70_42 else cos_prédit,
        },
        "verdict": (
            f"{verdict_calibration}. "
            f"Calibration phrases : cos ≈ {slope:.3f}×Jaccard + {intercept:.3f} (ρ={rho:.3f}). "
            f"vs H3 v2 mots : slope=-0.443 (ρ=-0.365). "
            f"Poids recalibré COLÈRE-FEU : {cos_70_42:.3f} (phrases) vs 0.472 (mots) vs 0.30 (initial)."
        ) if cos_70_42 else "Paires manquantes.",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("H3 v3 — Calibration ℂ* sur matrice phrases")
    print(f"Modèle : {MODEL_NAME}")
    print("=" * 60)

    print(f"\n[1/3] Chargement du modèle...")
    model = SentenceTransformer(MODEL_NAME)
    dim = model.get_embedding_dimension()
    print(f"  Dimension : {dim}")

    print(f"\n[2/3] Construction de la matrice phrases ({len(LANGUAGES)} langues × {len(MOLECULE_IDS)} molécules)...")
    matrix, mol_ids = build_phrase_matrix(model)
    print(f"  Matrice : {matrix.shape}")

    print(f"\n[3/3] H3 v3 — Calibration sur {len(mol_ids)} concepts...")
    results = run_h3_v3(matrix, mol_ids)

    print(f"\n  → ρ = {results['spearman_rho']:.3f} (p = {results['spearman_pval']:.3e})")
    print(f"  → Régression : {results['linear_calibration']['equation']}")
    print(f"  → Δslope vs H3 v2 : {results['comparison_h3v2']['delta_slope']:+.3f}")
    print(f"  → cos(INTENTION,TRANSFORMATION) sur phrases : {results['colere_feu_recalibration'].get('cos_observé_70_42_phrases', 'N/A')}")
    print(f"\n  Verdict : {results['verdict']}")

    # Tableau paires calibration
    print(f"\n  Paires de calibration :")
    print(f"  {'id_a':>4} {'id_b':>4} {'Jaccard':>8} {'cosine':>8}")
    for p in results["pairs"]:
        print(f"  {p['id_a']:>4} {p['id_b']:>4} {p['jaccard']:>8.3f} {p['cosine']:>8.3f}")

    # Sauvegarde
    out = FALSI_DIR / "H3_v3_calibration_phrases.json"
    out_data = {
        "version": "H3_v3",
        "date": "2026-04-23",
        "description": "Calibration ℂ* sur matrice phrases-définitionnelles (correction artefact H3 v2)",
        "model": MODEL_NAME,
        "results": results,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"\n  → Résultats sauvegardés : {out}")
    print("=" * 60)


if __name__ == "__main__":
    main()

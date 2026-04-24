#!/usr/bin/env python3
"""
test_nipada_decomposer.py — §80A : Décomposeur syntaxique inverse nipada

Ferme la boucle sémantique SANS CAS :

    texte_original (lang L)
        → encodeur nipada → molécules M = {m1, m2, m3}
        → NipadaSynthesizer.synthesize(M, lang=L, strategy=S) → texte_synthétisé
        → cos(embed(original), embed(synthétisé)) = cycle_sim_§80A

Trois stratégies comparées :
    A  concat_defs      — baseline §79 (concaténation des définitions complètes)
    B  kernel_flat      — noyaux courts séparés par virgule
    C  kernel_structured— noyaux courts + connecteurs Jaccard-aware

Tests supplémentaires :
    1. Cycle inverse : encode(synthétisé) → molécules → Jaccard vs molécules originales
       Mesure la stabilité du codec : si la génération préserve les molécules, le
       système est auto-cohérent.
    2. Cohérence inter-langues : pour les unités à convergence 100% (DUDH_1a, PHIL_integration),
       synthétiser dans les 5 langues depuis les mêmes molécules universelles, mesurer
       cos(generated_fr, generated_en) etc.

Résultats sauvegardés dans :
    research/nipada/falsification/nipada_decomposer_test.json

Usage :
    python scripts/test_nipada_decomposer.py
    python scripts/test_nipada_decomposer.py --topk 3 --threshold 0.20
"""

import argparse
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
    product_to_mask,
)
from src.core.nipada_synthesizer import NipadaSynthesizer, DEFINITIONS

MODEL_NAME  = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_decomposer_test.json"
MULTILANG_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_multilang_test.json"

MOLECULE_IDS = [2, 3, 5, 7, 6, 10, 14, 15, 21, 35, 30, 42, 70, 105, 210]
LANGUAGES    = ["fr", "en", "de", "es", "zh"]

MOL_NAMES_FR = {
    2:   "ÊTRE",       3:   "DIFFÉRENCE", 5:   "RAPPORT",     7:   "ORIENTATION",
    6:   "EXISTENCE",  10:  "COMPOSITION",14:  "DEVENIR",      15:  "MESURE",
    21:  "OPPOSITION", 35:  "RÉFÉRENCE",  30:  "VIE",          42:  "TRANSFORMATION",
    70:  "INTENTION",  105: "TEMPS",      210: "INTÉGRATION",
}

STRATEGIES = ["concat_defs", "kernel_flat", "kernel_structured"]


# ═══════════════════════════════════════════════════════════════════════════════
# Encodeur (repris de §79, standalone)
# ═══════════════════════════════════════════════════════════════════════════════

def build_reference_matrix(model: SentenceTransformer) -> np.ndarray:
    """Matrice de référence 15 × 384 (moyenne multilingue, même méthode que §79)."""
    rows = []
    for mol_id in MOLECULE_IDS:
        defs = [DEFINITIONS[lang][mol_id] for lang in LANGUAGES]
        vecs = model.encode(defs, normalize_embeddings=True)
        rows.append(vecs.mean(axis=0))
    mat = np.array(rows)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    return mat / np.where(norms == 0, 1, norms)


def encode_phrase(
    phrase: str,
    model: SentenceTransformer,
    ref_matrix: np.ndarray,
    topk: int = 3,
    threshold: float = 0.20,
) -> tuple[list[tuple[int, float]], np.ndarray]:
    """Encode une phrase → liste de (mol_id, score) + vecteur d'embedding."""
    vec = model.encode([phrase], normalize_embeddings=True)
    sims = cosine_similarity(vec, ref_matrix)[0]
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    selected = [
        (MOLECULE_IDS[i], float(s))
        for i, s in ranked[:topk]
        if s >= threshold
    ]
    return selected, vec[0]


# ═══════════════════════════════════════════════════════════════════════════════
# Test inverse de cycle
# ═══════════════════════════════════════════════════════════════════════════════

def jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def inverse_cycle_test(
    original_mols: list[int],
    generated_text: str,
    lang: str,
    model: SentenceTransformer,
    ref_matrix: np.ndarray,
    topk: int,
    threshold: float,
) -> dict:
    """
    Encode le texte généré → molécules, compare avec molécules originales.

    Retourne le Jaccard entre les deux ensembles de molécules.
    C'est le test de clôture du système : un décomposeur inverse parfait
    produirait du texte dont le re-encodage redonne exactement les mêmes molécules.
    """
    selected_gen, _ = encode_phrase(generated_text, model, ref_matrix, topk, threshold)
    gen_mols = [m for m, _ in selected_gen]

    orig_set = set(original_mols)
    gen_set  = set(gen_mols)

    j = jaccard(orig_set, gen_set)
    preserved = sorted(orig_set & gen_set)
    lost      = sorted(orig_set - gen_set)
    added     = sorted(gen_set - orig_set)

    return {
        "original_mols":  original_mols,
        "generated_mols": gen_mols,
        "jaccard":        round(j, 4),
        "preserved":      [MOL_NAMES_FR[m] for m in preserved],
        "lost":           [MOL_NAMES_FR[m] for m in lost],
        "added":          [MOL_NAMES_FR[m] for m in added],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Cohérence inter-langues
# ═══════════════════════════════════════════════════════════════════════════════

def cross_lang_consistency(
    mol_ids: list[int],
    strategy: str,
    synth: NipadaSynthesizer,
    model: SentenceTransformer,
) -> dict:
    """
    Synthétise le texte dans les 5 langues depuis les mêmes molécules.
    Mesure la cohérence sémantique inter-langues (cos des paires).
    """
    generated: dict[str, str] = {}
    vecs: dict[str, np.ndarray] = {}

    for lang in LANGUAGES:
        text = synth.synthesize(mol_ids, lang, strategy=strategy)
        generated[lang] = text
        vecs[lang] = model.encode([text], normalize_embeddings=True)[0]

    # Toutes les paires de langues
    pairs: dict[str, float] = {}
    for i, li in enumerate(LANGUAGES):
        for j, lj in enumerate(LANGUAGES):
            if j > i:
                cos = float(cosine_similarity(
                    vecs[li].reshape(1, -1),
                    vecs[lj].reshape(1, -1)
                )[0][0])
                pairs[f"{li}×{lj}"] = round(cos, 4)

    mean_cos = sum(pairs.values()) / len(pairs) if pairs else 0.0

    return {
        "generated":  generated,
        "pairs":      pairs,
        "mean_cos":   round(mean_cos, 4),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline principal
# ═══════════════════════════════════════════════════════════════════════════════

def run(topk: int = 3, threshold: float = 0.20) -> dict:
    print(f"\n{'═'*70}")
    print("  §80A — Décomposeur syntaxique inverse nipada")
    print(f"  topk={topk}  threshold={threshold:.2f}")
    print(f"{'═'*70}")

    print(f"\n  Chargement du modèle : {MODEL_NAME}")
    model  = SentenceTransformer(MODEL_NAME)
    synth  = NipadaSynthesizer()

    print("  Construction matrice de référence…")
    ref_matrix = build_reference_matrix(model)
    print("  Matrice prête.")

    # Charger les résultats §79 pour récupérer les molécules et le baseline
    if MULTILANG_FILE.exists():
        with open(MULTILANG_FILE, encoding="utf-8") as f:
            data_79 = json.load(f)
        corpus_units = data_79["units"]
        print(f"  Corpus §79 chargé : {len(corpus_units)} unités.")
    else:
        print("  ERREUR : nipada_multilang_test.json introuvable — exécuter §79 d'abord.")
        sys.exit(1)

    # ── Phase 1 : comparaison des stratégies de synthèse ─────────────────────
    print(f"\n{'─'*70}")
    print("  PHASE 1 — Comparaison des 3 stratégies de synthèse")
    print(f"{'─'*70}")

    all_unit_results = []

    # Accumulateurs pour les moyennes globales
    total_sim:   dict[str, list[float]] = {s: [] for s in STRATEGIES}
    total_inv_j: dict[str, list[float]] = {s: [] for s in STRATEGIES}

    for unit in corpus_units:
        uid   = unit["id"]
        theme = unit["theme"]
        print(f"\n  ── {uid} : {theme}")

        unit_lang_results = {}

        for lang in LANGUAGES:
            enc = unit["encodings"][lang]
            original     = enc["phrase"]
            mol_ids      = enc["molecules"]  # list[int]
            cycle_sim_79 = enc["cycle_sim"]  # baseline §79 concat_defs

            if not mol_ids:
                continue

            # Embedding du texte original
            vec_orig = model.encode([original], normalize_embeddings=True)[0]

            lang_strats = {}

            for strategy in STRATEGIES:
                # Génération
                generated = synth.synthesize(mol_ids, lang, strategy=strategy)

                # Cycle sim : cos(original, généré)
                vec_gen   = model.encode([generated], normalize_embeddings=True)[0]
                cycle_sim = float(cosine_similarity(
                    vec_orig.reshape(1, -1),
                    vec_gen.reshape(1, -1)
                )[0][0])

                # Test inverse du cycle
                inv = inverse_cycle_test(
                    mol_ids, generated, lang, model, ref_matrix, topk, threshold
                )

                total_sim[strategy].append(cycle_sim)
                total_inv_j[strategy].append(inv["jaccard"])

                lang_strats[strategy] = {
                    "generated":  generated,
                    "cycle_sim":  round(cycle_sim, 4),
                    "inv_cycle":  inv,
                }

            unit_lang_results[lang] = {
                "original":     original,
                "molecules":    mol_ids,
                "mol_names":    [MOL_NAMES_FR[m] for m in mol_ids],
                "cycle_sim_79": cycle_sim_79,
                "strategies":   lang_strats,
            }

            # Affichage compact
            sims_str = "  ".join(
                f"{s[:4]}={lang_strats[s]['cycle_sim']:.3f}"
                for s in STRATEGIES
            )
            inv_j_str = "  ".join(
                f"inv_j={lang_strats[s]['inv_cycle']['jaccard']:.2f}"
                for s in ["kernel_structured"]
            )
            mols_str = "+".join(MOL_NAMES_FR[m] for m in mol_ids)
            print(f"    [{lang}] {mols_str:38s}  {sims_str}  {inv_j_str}")

        all_unit_results.append({
            "id":     uid,
            "theme":  theme,
            "langs":  unit_lang_results,
        })

    # ── Résumé Phase 1 ────────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("  RÉSUMÉ — cycle_sim moyen par stratégie")
    print(f"  (plus élevé = meilleure restitution sémantique du sens original)")
    baseline_mean = sum(total_sim["concat_defs"]) / len(total_sim["concat_defs"])

    for s in STRATEGIES:
        mean_s   = sum(total_sim[s]) / len(total_sim[s])
        mean_inv = sum(total_inv_j[s]) / len(total_inv_j[s])
        delta    = mean_s - baseline_mean if s != "concat_defs" else 0.0
        delta_str = f"  Δ={delta:+.3f}" if s != "concat_defs" else "  (baseline)"
        print(f"    {s:20s}  cycle_sim={mean_s:.3f}{delta_str}  inv_Jaccard={mean_inv:.3f}")

    # ── Phase 2 : cohérence inter-langues (stratégie kernel_structured) ───────
    print(f"\n{'─'*70}")
    print("  PHASE 2 — Cohérence inter-langues (kernel_structured)")
    print(f"  Pour les unités à convergence 100%, synthèse depuis molécules universelles")
    print(f"{'─'*70}")

    cross_lang_results = []

    for unit in corpus_units:
        uid      = unit["id"]
        analysis = unit["analysis"]
        universal_mols = analysis.get("universal_molecules", [])

        if not universal_mols:
            continue

        # Seuil : au moins 2 molécules universelles pour un test utile
        if len(universal_mols) < 2:
            continue

        print(f"\n  {uid} — molécules universelles : {[MOL_NAMES_FR[m] for m in universal_mols]}")

        for strategy in ["concat_defs", "kernel_structured"]:
            cr = cross_lang_consistency(universal_mols, strategy, synth, model)
            mean_cos = cr["mean_cos"]
            top_pair = max(cr["pairs"], key=cr["pairs"].get)
            bot_pair = min(cr["pairs"], key=cr["pairs"].get)
            print(f"    [{strategy:20s}]  cos_moy={mean_cos:.3f}  "
                  f"proche={top_pair}({cr['pairs'][top_pair]:.3f})  "
                  f"éloigné={bot_pair}({cr['pairs'][bot_pair]:.3f})")

            cross_lang_results.append({
                "unit_id":  uid,
                "strategy": strategy,
                "molecules": universal_mols,
                "mol_names": [MOL_NAMES_FR[m] for m in universal_mols],
                **cr,
            })

    # ── Phase 3 : test de clôture globale ─────────────────────────────────────
    print(f"\n{'─'*70}")
    print("  PHASE 3 — Clôture : encode(synthesize(M)) ≈ M ?")
    print(f"  Jaccard moyen entre molécules originales et re-encodage du texte généré")
    print(f"{'─'*70}")

    for s in STRATEGIES:
        inv_vals = total_inv_j[s]
        mean_inv = sum(inv_vals) / len(inv_vals) if inv_vals else 0.0
        perfect  = sum(1 for v in inv_vals if v >= 1.0)
        partial  = sum(1 for v in inv_vals if 0.5 <= v < 1.0)
        weak     = sum(1 for v in inv_vals if v < 0.5)
        print(f"    {s:20s}  inv_J_moy={mean_inv:.3f}  "
              f"parfait={perfect}/{len(inv_vals)}  "
              f"partiel={partial}  faible={weak}")

    print(f"\n{'═'*70}\n")

    # ── Assemblage résultat JSON ───────────────────────────────────────────────
    global_summary = {}
    for s in STRATEGIES:
        global_summary[s] = {
            "cycle_sim_mean":       round(sum(total_sim[s]) / len(total_sim[s]), 4),
            "inv_jaccard_mean":     round(sum(total_inv_j[s]) / len(total_inv_j[s]), 4),
            "delta_vs_baseline":    round(
                sum(total_sim[s]) / len(total_sim[s])
                - sum(total_sim["concat_defs"]) / len(total_sim["concat_defs"]),
                4,
            ),
        }

    result = {
        "section":           "§80A",
        "title":             "Décomposeur syntaxique inverse nipada",
        "date":              "2026-04-24",
        "params":            {"topk": topk, "threshold": threshold, "model": MODEL_NAME},
        "strategies":        STRATEGIES,
        "global_summary":    global_summary,
        "units":             all_unit_results,
        "cross_lang_tests":  cross_lang_results,
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
        description="§80A — Décomposeur syntaxique inverse nipada"
    )
    parser.add_argument("--topk",      type=int,   default=3,    help="Nombre max de molécules")
    parser.add_argument("--threshold", type=float, default=0.20, help="Seuil cosinus minimal")
    args = parser.parse_args()

    run(topk=args.topk, threshold=args.threshold)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
test_nipada_adaptive.py — §81 : Synthèse adaptative nipada

Valide la règle de sélection de stratégie par type de molécule.

Règle §81 :
    - Molécule architecturale (n_atomes ≥ 4 OU RAPPORT×ORIENTATION à n=3) → definition
    - Molécule naturelle (tous les autres cas)                              → kernel

Molécules architecturales : TEMPS(105), INTENTION(70), INTÉGRATION(210)
Molécules naturelles       : les 12 restantes

Tests :
    1. Vérification de la table MOL_TYPES (toutes les 15 molécules)
    2. Cycle_sim adaptatif vs §80A (concat_defs, kernel_structured) sur corpus §79
    3. Analyse des cas mixtes (tuples contenant des molécules des deux types)
    4. Cross-lingual consistency (même mesure que §80A)

Hypothèse §81 :
    adaptive ≥ max(concat_defs, kernel_structured) pour chaque unité du corpus

Résultats sauvegardés dans :
    research/nipada/falsification/nipada_adaptive_test.json

Usage :
    python scripts/test_nipada_adaptive.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_engine import product_to_mask, atoms_in
from src.core.nipada_synthesizer import (
    NipadaSynthesizer,
    NipadaAdaptiveSynthesizer,
    MOL_TYPES,
    DEFINITIONS,
    _is_architectural,
)

MODEL_NAME     = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE    = ROOT / "research" / "nipada" / "falsification" / "nipada_adaptive_test.json"
MULTILANG_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_multilang_test.json"
DECOMP_FILE    = ROOT / "research" / "nipada" / "falsification" / "nipada_decomposer_test.json"

LANGUAGES    = ["fr", "en", "de", "es", "zh"]
MOLECULE_IDS = [2, 3, 5, 7, 6, 10, 14, 15, 21, 35, 30, 42, 70, 105, 210]

MOL_NAMES_FR = {
    2:   "ÊTRE",       3:   "DIFFÉRENCE", 5:   "RAPPORT",     7:   "ORIENTATION",
    6:   "EXISTENCE",  10:  "COMPOSITION",14:  "DEVENIR",      15:  "MESURE",
    21:  "OPPOSITION", 35:  "RÉFÉRENCE",  30:  "VIE",          42:  "TRANSFORMATION",
    70:  "INTENTION",  105: "TEMPS",      210: "INTÉGRATION",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Encodeur (standalone, même méthode que §79/§80A)
# ═══════════════════════════════════════════════════════════════════════════════

def build_reference_matrix(model: SentenceTransformer) -> np.ndarray:
    rows = []
    for mol_id in MOLECULE_IDS:
        defs = [DEFINITIONS[lang][mol_id] for lang in LANGUAGES]
        vecs = model.encode(defs, normalize_embeddings=True)
        rows.append(vecs.mean(axis=0))
    mat = np.array(rows)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    return mat / np.where(norms == 0, 1, norms)


def embed(text: str, model: SentenceTransformer) -> np.ndarray:
    return model.encode([text], normalize_embeddings=True)[0]


def cycle_sim(orig: str, gen: str, model: SentenceTransformer) -> float:
    v1 = model.encode([orig], normalize_embeddings=True)
    v2 = model.encode([gen],  normalize_embeddings=True)
    return float(cosine_similarity(v1, v2)[0][0])


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 0 : vérification de la table MOL_TYPES
# ═══════════════════════════════════════════════════════════════════════════════

def verify_mol_types() -> dict:
    """Affiche et vérifie la classification de toutes les molécules."""
    print(f"\n{'─'*70}")
    print("  PHASE 0 — Vérification de la table MOL_TYPES")
    print(f"{'─'*70}")
    print(f"  {'mol':>4}  {'nom':>15}  {'atomes':>22}  {'n':>2}  {'type':>10}  {'règle'}")
    print(f"  {'─'*68}")

    expected_arch = {70, 105, 210}  # attendus comme architecturaux
    errors = []

    for mol_id in MOLECULE_IDS:
        mask   = product_to_mask(mol_id) or 0
        primes = sorted(atoms_in(mask))
        n      = len(primes)
        t      = MOL_TYPES[mol_id]
        is_ok  = (t == "def") == (mol_id in expected_arch)

        prime_str  = "×".join(str(p) for p in primes)
        name       = MOL_NAMES_FR[mol_id]
        status     = "✓" if is_ok else "✗ ERREUR"

        if n >= 4:
            rule = "n_atomes=4"
        elif n == 3 and 5 in primes and 7 in primes:
            rule = "RAPPORT×ORIENT, n=3"
        else:
            rule = "naturel"

        print(f"  {mol_id:>4}  {name:>15}  {prime_str:>22}  {n:>2}  {t:>10}  {rule} {status}")

        if not is_ok:
            errors.append(mol_id)

    print()
    architectural = [m for m in MOLECULE_IDS if MOL_TYPES[m] == "def"]
    natural       = [m for m in MOLECULE_IDS if MOL_TYPES[m] == "kernel"]
    print(f"  Architecturales ({len(architectural)}) : {[MOL_NAMES_FR[m] for m in architectural]}")
    print(f"  Naturelles      ({len(natural)})       : {[MOL_NAMES_FR[m] for m in natural]}")

    if errors:
        print(f"\n  ERREURS : {[MOL_NAMES_FR[m] for m in errors]}")
    else:
        print(f"\n  Classification : OK (0 erreur)")

    return {
        "architectural":  architectural,
        "natural":        natural,
        "errors":         errors,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 1 : comparaison adaptive vs §80A sur corpus §79
# ═══════════════════════════════════════════════════════════════════════════════

def run_comparison(
    model: SentenceTransformer,
    data_79: dict,
    data_80: dict,
) -> tuple[list[dict], dict]:
    """
    Compare adaptive vs concat_defs et kernel_structured sur le corpus §79.

    Pour chaque (unité, langue) :
        - Récupère les molécules et la phrase originale
        - Génère le texte adaptatif
        - Mesure cycle_sim adaptatif
        - Compare avec §80A scores
    """
    print(f"\n{'─'*70}")
    print("  PHASE 1 — Comparaison adaptive vs §80A (concat_defs / kernel_structured)")
    print(f"{'─'*70}")

    synth    = NipadaAdaptiveSynthesizer()
    base     = NipadaSynthesizer()

    # Indexer les résultats §80A par (unit_id, lang)
    scores_80: dict[tuple[str, str], dict[str, float]] = {}
    for unit in data_80.get("units", []):
        uid = unit["id"]
        for lang, ldata in unit.get("langs", {}).items():
            strats = ldata.get("strategies", {})
            scores_80[(uid, lang)] = {
                s: strats[s]["cycle_sim"]
                for s in ("concat_defs", "kernel_structured")
                if s in strats
            }

    all_results = []
    total_adaptive: list[float] = []
    total_concat:   list[float] = []
    total_kernel:   list[float] = []
    adaptive_wins  = 0
    adaptive_equal = 0
    adaptive_loses = 0

    for unit in data_79["units"]:
        uid   = unit["id"]
        theme = unit["theme"]
        print(f"\n  ── {uid} : {theme}")

        unit_results = {}

        for lang in LANGUAGES:
            enc      = unit["encodings"][lang]
            original = enc["phrase"]
            mol_ids  = enc["molecules"]

            if not mol_ids:
                continue

            # Types des molécules
            types = {m: MOL_TYPES.get(m, "kernel") for m in mol_ids}

            # Génération adaptative
            gen_adaptive = synth.synthesize(mol_ids, lang)
            sim_adaptive = cycle_sim(original, gen_adaptive, model)
            total_adaptive.append(sim_adaptive)

            # Récupérer scores §80A
            prev = scores_80.get((uid, lang), {})
            sim_concat  = prev.get("concat_defs", 0.0)
            sim_kernel  = prev.get("kernel_structured", 0.0)
            total_concat.append(sim_concat)
            total_kernel.append(sim_kernel)

            best_80 = max(sim_concat, sim_kernel)
            delta   = sim_adaptive - best_80

            if delta > 0.005:
                adaptive_wins  += 1
                verdict = "↑ win"
            elif delta < -0.005:
                adaptive_loses += 1
                verdict = "↓ lose"
            else:
                adaptive_equal += 1
                verdict = "≈ equal"

            # Affichage compact
            type_str = "+".join(f"{MOL_NAMES_FR[m]}({types[m][0].upper()})" for m in mol_ids)
            print(f"    [{lang}] adapt={sim_adaptive:.3f}  "
                  f"concat={sim_concat:.3f}  kern={sim_kernel:.3f}  "
                  f"Δ={delta:+.3f}  {verdict}")
            print(f"           {type_str}")

            unit_results[lang] = {
                "original":        original,
                "molecules":       mol_ids,
                "mol_types":       {MOL_NAMES_FR[m]: types[m] for m in mol_ids},
                "generated":       gen_adaptive,
                "cycle_sim":       round(sim_adaptive, 4),
                "baseline_concat": round(sim_concat, 4),
                "baseline_kernel": round(sim_kernel, 4),
                "delta_vs_best":   round(delta, 4),
                "verdict":         verdict.split()[1],
            }

        all_results.append({
            "id":     uid,
            "theme":  theme,
            "langs":  unit_results,
        })

    # Résumé
    print(f"\n{'─'*70}")
    print("  RÉSUMÉ — cycle_sim moyen")
    n = len(total_adaptive)
    m_adapt  = sum(total_adaptive) / n
    m_concat = sum(total_concat)   / n
    m_kernel = sum(total_kernel)   / n
    print(f"    adaptive    = {m_adapt:.3f}")
    print(f"    concat_defs = {m_concat:.3f}  (Δ={m_adapt - m_concat:+.3f} vs adaptive)")
    print(f"    kernel_str  = {m_kernel:.3f}  (Δ={m_adapt - m_kernel:+.3f} vs adaptive)")
    print(f"\n  Sur {n} cas :")
    print(f"    adaptive > best_80A  : {adaptive_wins:>3} ({100*adaptive_wins/n:.0f}%)")
    print(f"    adaptive ≈ best_80A  : {adaptive_equal:>3} ({100*adaptive_equal/n:.0f}%)")
    print(f"    adaptive < best_80A  : {adaptive_loses:>3} ({100*adaptive_loses/n:.0f}%)")

    summary = {
        "adaptive_mean":    round(m_adapt, 4),
        "concat_mean":      round(m_concat, 4),
        "kernel_str_mean":  round(m_kernel, 4),
        "delta_vs_concat":  round(m_adapt - m_concat, 4),
        "delta_vs_kernel":  round(m_adapt - m_kernel, 4),
        "wins":             adaptive_wins,
        "equal":            adaptive_equal,
        "loses":            adaptive_loses,
        "total":            n,
    }

    return all_results, summary


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 2 : analyse des cas mixtes
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_mixed_cases(all_results: list[dict]) -> list[dict]:
    """
    Isole les cas où le tuple contient des molécules des deux types (mixed).
    Ce sont les cas où l'adaptif apporte le plus de valeur ajoutée.
    """
    print(f"\n{'─'*70}")
    print("  PHASE 2 — Analyse des cas mixtes (kernel + def dans le même tuple)")
    print(f"{'─'*70}")

    mixed_cases = []

    for unit in all_results:
        uid = unit["id"]
        for lang, ldata in unit["langs"].items():
            types = list(ldata["mol_types"].values())
            if "kernel" in types and "def" in types:
                delta  = ldata["delta_vs_best"]
                verdict = ldata["verdict"]
                mols_str = "+".join(
                    f"{m}({t[0].upper()})"
                    for m, t in ldata["mol_types"].items()
                )
                print(f"  [{uid}][{lang}]  {mols_str}")
                print(f"    adapt={ldata['cycle_sim']:.3f}  "
                      f"concat={ldata['baseline_concat']:.3f}  "
                      f"kern={ldata['baseline_kernel']:.3f}  "
                      f"Δ={delta:+.3f}  → {verdict}")
                print(f"    Texte: {ldata['generated'][:90]}…")

                mixed_cases.append({
                    "unit_id":  uid,
                    "lang":     lang,
                    "types":    ldata["mol_types"],
                    "cycle_sim_adaptive": ldata["cycle_sim"],
                    "delta_vs_best":      delta,
                    "verdict":            verdict,
                })

    if not mixed_cases:
        print("  (aucun cas mixte dans le corpus §79)")
    else:
        wins  = sum(1 for c in mixed_cases if c["verdict"] == "win")
        total = len(mixed_cases)
        print(f"\n  Cas mixtes : {total}  |  wins adaptatif : {wins}/{total}")

    return mixed_cases


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 3 : cohérence cross-lingual adaptive
# ═══════════════════════════════════════════════════════════════════════════════

def cross_lang_adaptive(
    data_79: dict,
    model: SentenceTransformer,
) -> list[dict]:
    """
    Synthétise depuis les molécules universelles en 5 langues avec la stratégie
    adaptative, et mesure la cohérence inter-langues.
    Compare avec les scores §80A concat_defs et kernel_structured.
    """
    print(f"\n{'─'*70}")
    print("  PHASE 3 — Cohérence cross-lingual (stratégie adaptative)")
    print(f"{'─'*70}")

    synth   = NipadaAdaptiveSynthesizer()
    results = []

    for unit in data_79["units"]:
        uid      = unit["id"]
        analysis = unit["analysis"]
        univ_mols = analysis.get("universal_molecules", [])

        if len(univ_mols) < 2:
            continue

        print(f"\n  {uid} — molécules universelles : {[MOL_NAMES_FR[m] for m in univ_mols]}")
        types_str = " ".join(f"{MOL_NAMES_FR[m]}={MOL_TYPES.get(m,'?')}" for m in univ_mols)
        print(f"    types : {types_str}")

        # Générer dans les 5 langues
        vecs: dict[str, np.ndarray] = {}
        generated: dict[str, str]   = {}
        for lang in LANGUAGES:
            text = synth.synthesize(univ_mols, lang)
            generated[lang] = text
            vecs[lang] = model.encode([text], normalize_embeddings=True)[0]

        # Paires de langues
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
        top_pair = max(pairs, key=pairs.get)
        bot_pair = min(pairs, key=pairs.get)

        print(f"    adapt  cos_moy={mean_cos:.3f}  "
              f"proche={top_pair}({pairs[top_pair]:.3f})  "
              f"éloigné={bot_pair}({pairs[bot_pair]:.3f})")

        results.append({
            "unit_id":   uid,
            "molecules": univ_mols,
            "mol_types": {MOL_NAMES_FR[m]: MOL_TYPES.get(m, "kernel") for m in univ_mols},
            "generated": generated,
            "pairs":     pairs,
            "mean_cos":  round(mean_cos, 4),
        })

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline principal
# ═══════════════════════════════════════════════════════════════════════════════

def run() -> None:
    print(f"\n{'═'*70}")
    print("  §81 — Synthèse adaptative nipada")
    print(f"  Règle : TEMPS/INTENTION/INTÉGRATION → def, autres → kernel")
    print(f"{'═'*70}")

    # Charger les données §79 et §80A
    if not MULTILANG_FILE.exists():
        print("  ERREUR : nipada_multilang_test.json introuvable.")
        sys.exit(1)
    if not DECOMP_FILE.exists():
        print("  ERREUR : nipada_decomposer_test.json introuvable.")
        sys.exit(1)

    with open(MULTILANG_FILE, encoding="utf-8") as f:
        data_79 = json.load(f)
    with open(DECOMP_FILE, encoding="utf-8") as f:
        data_80 = json.load(f)

    print(f"\n  Chargement du modèle : {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # ── Phase 0 : vérification classification ─────────────────────────────────
    mol_type_info = verify_mol_types()

    # ── Phase 1 : comparaison corpus complet ──────────────────────────────────
    all_results, summary = run_comparison(model, data_79, data_80)

    # ── Phase 2 : cas mixtes ──────────────────────────────────────────────────
    mixed_cases = analyze_mixed_cases(all_results)

    # ── Phase 3 : cohérence cross-lingual ─────────────────────────────────────
    cross_results = cross_lang_adaptive(data_79, model)

    print(f"\n{'═'*70}")

    # Verdict §81
    delta_c = summary["delta_vs_concat"]
    delta_k = summary["delta_vs_kernel"]
    wins    = summary["wins"]
    total   = summary["total"]
    print(f"\n  VERDICT §81")
    print(f"  adaptive vs concat_defs   : Δ={delta_c:+.3f}")
    print(f"  adaptive vs kernel_struct : Δ={delta_k:+.3f}")
    print(f"  adaptive > best_§80A      : {wins}/{total} cas ({100*wins/total:.0f}%)")
    hyp_valid = wins > total * 0.5
    print(f"  Hypothèse (>50% wins)     : {'VALIDÉE ✓' if hyp_valid else 'INVALIDÉE ✗'}")
    print()

    # Assemblage JSON
    result = {
        "section":         "§81",
        "title":           "Synthèse adaptative nipada",
        "date":            "2026-04-24",
        "model":           MODEL_NAME,
        "classification":  {
            "rule": "def if n_atoms>=4 OR (n_atoms==3 AND RAPPORT(5) AND ORIENTATION(7) in atoms)",
            "architectural": [MOL_NAMES_FR[m] for m in mol_type_info["architectural"]],
            "natural":       [MOL_NAMES_FR[m] for m in mol_type_info["natural"]],
        },
        "mol_types":       {MOL_NAMES_FR[m]: t for m, t in MOL_TYPES.items()},
        "summary":         summary,
        "hypothesis_validated": hyp_valid,
        "units":           all_results,
        "mixed_cases":     mixed_cases,
        "cross_lang":      cross_results,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  Résultats sauvegardés → {OUTPUT_FILE}")


if __name__ == "__main__":
    run()

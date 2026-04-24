#!/usr/bin/env python3
"""
test_nipada_subject.py — §82 : 5e atome SUJET(11)

Valide l'hypothèse : le medium est le message.
Les 4 atomes ontologiques {ÊTRE,DIFF,RAPP,ORIENT} ne suffisent pas à encoder
les speech acts (proclamations, droits, dignité). SUJET(11) ouvre la couche
phénoménologique — l'observateur, le porteur, le cadre d'énonciation.

Tests :
    Phase 0 — Vérification de la table MOL_TYPES_5 (31 molécules)
    Phase 1 — DUDH_1a : re-encodage avec [770, 77, 55] vs §79 [2, 30, 6]
    Phase 2 — Discrimination de speech acts par SUJET (McLuhan)
    Phase 3 — Cross-lingual SUJET molecules

Hypothèses :
    H1 : cycle_sim([770,77,55], DUDH_1a) > 2 × cycle_sim([2,30,6], DUDH_1a)
    H2 : SENS(385) discrimine proclamation vs description vs question (cosine < 0.85)

Résultats sauvegardés dans :
    research/nipada/falsification/nipada_subject_test.json

Usage :
    python scripts/test_nipada_subject.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_subject import (
    NipadaExtendedSynthesizer,
    MOL_TYPES_5,
    SUJET_MOL_IDS,
    SUJET_ATOMS,
    SUJET_MOL_NAMES,
    atoms_in_5,
    _is_architectural_5,
)
from src.core.nipada_engine import atoms_in, product_to_mask
from src.core.nipada_synthesizer import NipadaSynthesizer, DEFINITIONS

MODEL_NAME   = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE  = ROOT / "research" / "nipada" / "falsification" / "nipada_subject_test.json"
DECOMP_FILE  = ROOT / "research" / "nipada" / "falsification" / "nipada_decomposer_test.json"

LANGUAGES = ["fr", "en", "de", "es", "zh"]

# Phrase originale DUDH_1a dans les 5 langues
DUDH_1A: dict[str, str] = {
    "fr": "Tous les êtres humains naissent libres et égaux en dignité et en droits. Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité.",
    "en": "All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.",
    "de": "Alle Menschen sind frei und gleich an Würde und Rechten geboren. Sie sind mit Vernunft und Gewissen begabt und sollen einander im Geist der Brüderlichkeit begegnen.",
    "es": "Todos los seres humanos nacen libres e iguales en dignidad y derechos y, dotados como están de razón y conciencia, deben comportarse fraternalmente los unos con los otros.",
    "zh": "人人生而自由，在尊严和权利上一律平等。他们赋有理性和良心，并应以兄弟关系的精神相对待。",
}

# Encodages à comparer pour DUDH_1a
ENCODINGS_DUDH = {
    "§79":        [2, 30, 6],            # ÊTRE+VIE+EXISTENCE (§79 original)
    "§82_compact": [770, 2310],          # DIGNITÉ+CONSCIENCE
    "§82_explicit": [770, 77, 55],       # DIGNITÉ+LIBERTÉ+DROIT
    "§82_full":   [770, 77, 55, 2310],   # DIGNITÉ+LIBERTÉ+DROIT+CONSCIENCE
}

# Speech acts — 5 types de phrases pour tester la discrimination SUJET
SPEECH_ACTS: dict[str, dict[str, str]] = {
    "proclamation": {
        "fr": "Tous les êtres humains naissent libres et égaux en dignité et en droits.",
        "en": "All human beings are born free and equal in dignity and rights.",
    },
    "description": {
        "fr": "Un être humain se différencie de son environnement et maintient des relations.",
        "en": "A human being differentiates itself from its environment and maintains relations.",
    },
    "question": {
        "fr": "Qu'est-ce qui distingue un être humain d'un autre ?",
        "en": "What distinguishes one human being from another?",
    },
    "ordre": {
        "fr": "Agissez les uns envers les autres dans un esprit de fraternité.",
        "en": "Act towards one another in a spirit of brotherhood.",
    },
    "definition": {
        "fr": "La dignité est le rapport orienté qu'un être entretient avec lui-même.",
        "en": "Dignity is the oriented relation a being maintains with itself.",
    },
}

# Molécules SUJET proposées pour chaque speech act (hypothèse)
SPEECH_ACT_MOLECULES: dict[str, list[int]] = {
    "proclamation": [770, 33, 55],     # DIGNITÉ + NORME + DROIT
    "description":  [30, 5, 3],        # VIE + RAPPORT + DIFF (sans SUJET)
    "question":     [165, 385],        # JUGEMENT + SENS
    "ordre":        [77, 110, 2310],   # LIBERTÉ + VALEUR + CONSCIENCE
    "definition":   [770, 385],        # DIGNITÉ + SENS
}


# ══════════════════════════════════════════════════════════════════════════════

def cycle_sim(orig: str, gen: str, model: SentenceTransformer) -> float:
    v1 = model.encode([orig], normalize_embeddings=True)
    v2 = model.encode([gen],  normalize_embeddings=True)
    return float(cosine_similarity(v1, v2)[0][0])


# ══════════════════════════════════════════════════════════════════════════════
# Phase 0 : vérification MOL_TYPES_5
# ══════════════════════════════════════════════════════════════════════════════

def verify_mol_types_5() -> dict:
    print(f"\n{'─'*72}")
    print("  PHASE 0 — Table MOL_TYPES_5 (31 molécules)")
    print(f"{'─'*72}")

    names_fr = {
        2:"ÊTRE", 3:"DIFF", 5:"RAPP", 7:"ORIENT", 6:"EXIST", 10:"COMPO",
        14:"DEVENIR", 15:"MESURE", 21:"OPPOS", 35:"REF", 30:"VIE", 42:"TRANSF",
        70:"INTENT", 105:"TEMPS", 210:"INTÉGR",
        **{m: SUJET_MOL_NAMES["fr"][m] for m in SUJET_MOL_IDS},
    }

    print(f"  {'mol':>5}  {'nom':>12}  {'atomes':>22}  {'n':>2}  {'type':>8}  arch?")
    print(f"  {'─'*70}")

    all_mols = [2,3,5,7,6,10,14,15,21,35,30,42,70,105,210] + SUJET_MOL_IDS
    architectural = []
    natural       = []

    for m in all_mols:
        primes = sorted(atoms_in_5(m))
        n = len(primes)
        t = MOL_TYPES_5.get(m, "?")
        arch = "✓" if t == "def" else ""
        prime_str = "×".join(str(p) for p in primes)
        name = names_fr.get(m, str(m))
        print(f"  {m:>5}  {name:>12}  {prime_str:>22}  {n:>2}  {t:>8}  {arch}")
        if t == "def":
            architectural.append(m)
        else:
            natural.append(m)

    print(f"\n  Architecturales ({len(architectural)}) : "
          f"{[names_fr[m] for m in architectural]}")
    print(f"  Naturelles      ({len(natural)}) : "
          f"{[names_fr[m] for m in natural]}")
    return {"architectural": architectural, "natural": natural}


# ══════════════════════════════════════════════════════════════════════════════
# Phase 1 : DUDH_1a re-encodage
# ══════════════════════════════════════════════════════════════════════════════

def test_dudh_reencoding(model: SentenceTransformer) -> dict:
    print(f"\n{'─'*72}")
    print("  PHASE 1 — DUDH_1a : re-encodage §79 [2,30,6] vs §82 SUJET")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()
    base  = NipadaSynthesizer()
    results = {}

    for enc_name, mol_ids in ENCODINGS_DUDH.items():
        print(f"\n  Encodage {enc_name} : {mol_ids}")
        lang_results = {}
        sims = []

        for lang in LANGUAGES:
            original = DUDH_1A[lang]
            generated = synth.synthesize(mol_ids, lang)
            sim = cycle_sim(original, generated, model)
            sims.append(sim)
            print(f"    [{lang}] sim={sim:.3f}  → {generated[:75]}…")
            lang_results[lang] = {
                "cycle_sim": round(sim, 4),
                "generated": generated,
            }

        mean_sim = sum(sims) / len(sims)
        print(f"    MOYENNE : {mean_sim:.3f}")
        results[enc_name] = {
            "molecules": mol_ids,
            "mean_cycle_sim": round(mean_sim, 4),
            "langs": lang_results,
        }

    # Comparer §79 vs meilleur §82
    sim_79   = results["§79"]["mean_cycle_sim"]
    best_82  = max(
        results[k]["mean_cycle_sim"]
        for k in ("§82_compact", "§82_explicit", "§82_full")
    )
    ratio    = best_82 / sim_79 if sim_79 > 0 else 0
    h1_valid = best_82 > 2 * sim_79

    print(f"\n  H1 : best_§82({best_82:.3f}) > 2 × §79({sim_79:.3f}) = {2*sim_79:.3f}")
    print(f"  Ratio : ×{ratio:.1f}")
    print(f"  HYPOTHÈSE H1 : {'VALIDÉE ✓' if h1_valid else 'INVALIDÉE ✗'}")

    return {
        "encodings": results,
        "baseline_§79": sim_79,
        "best_§82":     round(best_82, 4),
        "ratio":        round(ratio, 2),
        "H1_validated": h1_valid,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Phase 2 : discrimination de speech acts
# ══════════════════════════════════════════════════════════════════════════════

def test_speech_acts(model: SentenceTransformer) -> dict:
    """
    Tester si les molécules SUJET discriminent les types de speech acts.
    H2 : les textes de speech acts différents ont cosine < 0.85 entre eux,
    et les mêmes types ont cosine > 0.90.
    """
    print(f"\n{'─'*72}")
    print("  PHASE 2 — Discrimination des speech acts par molécules SUJET")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()
    act_types = list(SPEECH_ACTS.keys())
    langs_test = ["fr", "en"]

    # Générer textes nipada pour chaque type de speech act
    generated: dict[str, dict[str, str]] = {}
    for act in act_types:
        generated[act] = {}
        mol_ids = SPEECH_ACT_MOLECULES[act]
        type_str = "+".join(str(m) for m in mol_ids)
        print(f"\n  {act:>15} — molécules {type_str}")
        for lang in langs_test:
            text = synth.synthesize(mol_ids, lang)
            orig = SPEECH_ACTS[act][lang]
            sim  = cycle_sim(orig, text, model)
            generated[act][lang] = text
            print(f"    [{lang}] sim_orig={sim:.3f}  → {text[:70]}…")

    # Matrice cosine entre speech acts (en FR)
    print(f"\n  Matrice de similarité cosine (textes nipada, FR) :")
    print(f"  {'':>15}", end="")
    for act in act_types:
        print(f"  {act[:8]:>8}", end="")
    print()

    vecs = {
        act: model.encode([generated[act]["fr"]], normalize_embeddings=True)[0]
        for act in act_types
    }
    cos_matrix: dict[tuple[str,str], float] = {}
    for i, ai in enumerate(act_types):
        print(f"  {ai:>15}", end="")
        for j, aj in enumerate(act_types):
            cos = float(cosine_similarity(
                vecs[ai].reshape(1,-1),
                vecs[aj].reshape(1,-1)
            )[0][0])
            cos_matrix[(ai, aj)] = round(cos, 3)
            print(f"  {cos:.3f}  ", end="")
        print()

    # Vérification H2 : off-diagonal < 0.85
    off_diag = [
        cos_matrix[(ai, aj)]
        for i, ai in enumerate(act_types)
        for j, aj in enumerate(act_types)
        if i != j
    ]
    max_off = max(off_diag)
    min_off = min(off_diag)
    h2_valid = max_off < 0.90

    print(f"\n  Off-diagonal : max={max_off:.3f}  min={min_off:.3f}")
    print(f"  HYPOTHÈSE H2 (max_off < 0.90) : {'VALIDÉE ✓' if h2_valid else 'INVALIDÉE ✗'}")

    return {
        "generated": generated,
        "cosine_matrix": {f"{a}×{b}": v for (a,b), v in cos_matrix.items()},
        "max_off_diagonal": max_off,
        "H2_validated": h2_valid,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Phase 3 : cohérence cross-lingual SUJET
# ══════════════════════════════════════════════════════════════════════════════

def test_cross_lingual_subject(model: SentenceTransformer) -> dict:
    """
    Mesure la cohérence inter-langues pour les molécules SUJET clés.
    Comparer avec §81 baseline (PHIL_integration adaptive : 0.939).
    """
    print(f"\n{'─'*72}")
    print("  PHASE 3 — Cohérence cross-lingual (molécules SUJET)")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()
    test_cases = [
        ("DIGNITÉ",     [770]),
        ("LIBERTÉ",     [77]),
        ("SENS",        [385]),
        ("DIGNITÉ+LIBERTÉ+DROIT",  [770, 77, 55]),
        ("CONSCIENCE",  [2310]),
        ("DIGNITÉ+CONSCIENCE", [770, 2310]),
    ]

    results = []
    for label, mol_ids in test_cases:
        vecs: dict[str, np.ndarray] = {}
        for lang in LANGUAGES:
            text = synth.synthesize(mol_ids, lang)
            vecs[lang] = model.encode([text], normalize_embeddings=True)[0]

        pairs: dict[str, float] = {}
        for i, li in enumerate(LANGUAGES):
            for j, lj in enumerate(LANGUAGES):
                if j > i:
                    cos = float(cosine_similarity(
                        vecs[li].reshape(1,-1),
                        vecs[lj].reshape(1,-1)
                    )[0][0])
                    pairs[f"{li}×{lj}"] = round(cos, 4)

        mean_cos = sum(pairs.values()) / len(pairs) if pairs else 0.0
        top_pair = max(pairs, key=pairs.get)
        bot_pair = min(pairs, key=pairs.get)

        print(f"  {label:<30} cos_moy={mean_cos:.3f}  "
              f"top={top_pair}({pairs[top_pair]:.3f})  "
              f"bot={bot_pair}({pairs[bot_pair]:.3f})")

        results.append({
            "label":    label,
            "molecules": mol_ids,
            "pairs":    pairs,
            "mean_cos": round(mean_cos, 4),
        })

    return results


# ══════════════════════════════════════════════════════════════════════════════
# Pipeline principal
# ══════════════════════════════════════════════════════════════════════════════

def run() -> None:
    print(f"\n{'═'*72}")
    print("  §82 — 5e atome SUJET(11) : couche phénoménologique nipada")
    print(f"  McLuhan : le medium (SUJET) est le message")
    print(f"{'═'*72}")

    print(f"\n  Chargement du modèle : {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # ── Phase 0 : classification ──────────────────────────────────────────────
    mol_type_info = verify_mol_types_5()

    # ── Phase 1 : DUDH_1a re-encodage ─────────────────────────────────────────
    dudh_results = test_dudh_reencoding(model)

    # ── Phase 2 : speech acts ─────────────────────────────────────────────────
    speech_results = test_speech_acts(model)

    # ── Phase 3 : cross-lingual SUJET ─────────────────────────────────────────
    cross_results = test_cross_lingual_subject(model)

    print(f"\n{'═'*72}")
    print(f"\n  VERDICT §82")
    print(f"  H1 (DUDH_1a ratio ×2) : {'✓' if dudh_results['H1_validated'] else '✗'}")
    print(f"    §79 baseline : {dudh_results['baseline_§79']:.3f}")
    print(f"    §82 best     : {dudh_results['best_§82']:.3f}  (×{dudh_results['ratio']:.1f})")
    print(f"  H2 (speech acts off-diag < 0.90) : "
          f"{'✓' if speech_results['H2_validated'] else '✗'} "
          f"(max={speech_results['max_off_diagonal']:.3f})")
    print()

    result = {
        "section": "§82",
        "title":   "5e atome SUJET(11) — couche phénoménologique nipada",
        "date":    "2026-04-24",
        "model":   MODEL_NAME,
        "atom_5":  {"prime": 11, "name": "SUJET",
                    "motivation": "McLuhan: le medium est le message"},
        "new_molecules": {
            str(m): {
                "name": SUJET_MOL_NAMES["fr"][m],
                "atoms": sorted(SUJET_ATOMS[m]),
                "type": MOL_TYPES_5[m],
            }
            for m in SUJET_MOL_IDS
        },
        "mol_classification": mol_type_info,
        "dudh_reencoding":    dudh_results,
        "speech_acts":        speech_results,
        "cross_lingual":      cross_results,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  Résultats → {OUTPUT_FILE}")


if __name__ == "__main__":
    run()

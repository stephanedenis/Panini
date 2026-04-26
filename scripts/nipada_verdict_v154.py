#!/usr/bin/env python3
"""
§154 — Verdict synthétique Phase B² + Phase C, et formulation du pivot
Phase D (bigrammes atomiques).

Synthèse :
  Phase B² (lex)        : R²(d_graph seul) = 0.0073, p = 0.66 → falsifié
  Phase C  (dense)      : R²(d_graph seul) = 0.0003          → falsifié
  Mix lex×dense (λ=0.3) : R²(d_graph seul) = 0.046           → faible
  → conclusion : la **fréquence** des 14 atomes est insuffisante pour
    capter une filiation intellectuelle.

Hypothèse Phase D :
  Si chaque pensée est un MOTIF combinatoire d'atomes (ex. RAPPORT—MODALITÉ
  pour la conditionnalité, ÊTRE—DIFFÉRENCE—ÉQUATION pour l'identité), alors
  la **co-occurrence** d'atomes au sein d'un même fragment porte plus
  d'information que leur fréquence marginale.

Output : research/nipada/falsification/nipada_v154_verdict_pivot.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v154_verdict_pivot.json"

V150 = json.loads((RES_DIR / "nipada_v150_validation.json").read_text(encoding="utf-8"))
V152 = json.loads((RES_DIR / "nipada_v152_dense_validation.json").read_text(encoding="utf-8"))
V153 = json.loads((RES_DIR / "nipada_v153_diagnostic.json").read_text(encoding="utf-8"))


def main() -> None:
    a_lex = V153["summary"]["A_r2_d_graph_only"]["lex"]
    a_dense = V153["summary"]["A_r2_d_graph_only"]["dense"]
    interp = V153["summary"]["B_interpolation_lex_dense"]
    perm = V153["summary"]["C_permutation_test_lex_r2_d_graph_only"]

    # OLS complet de §150 et §152 pour rappel
    lex_full = V150["H3_ols_regression"]["ols_dsig"]
    dense_full = V152["H3_ols_regression_dense"]["ols_dense"]

    verdict = {
        "phase_b2_lex": {
            "R2_full_4var": lex_full["r2"],
            "R2_d_graph_only": a_lex["r2"],
            "beta_d_graph_only": a_lex["beta"][1],
            "permutation_p_one_tailed": perm["p_value_one_tailed"],
            "diagnosis": (
                "Le R²=0.30 du §150 venait de Δyear (β=+0.138), pas de d_graph. "
                "Hors confound, R²=0.007 et p=0.66 → aucun signal généalogique."
            ),
        },
        "phase_c_dense": {
            "R2_full_4var": dense_full["r2"],
            "R2_d_graph_only": a_dense["r2"],
            "beta_d_graph_only": a_dense["beta"][1],
            "diagnosis": (
                "L'embedding multilingue projette toutes les œuvres "
                "philosophiques dans une bande étroite ; la signature 14-dim "
                "obtenue par cosinus avec prototypes ne discrimine pas plus."
            ),
        },
        "interpolation_lex_x_dense": {
            "best_lambda": interp["best_lambda"],
            "best_R2_d_graph_only": interp["best_r2_d_graph_only"],
            "diagnosis": (
                f"Meilleur mix à λ={interp['best_lambda']} mais R² reste à "
                f"{interp['best_r2_d_graph_only']:.3f} — sous le seuil de "
                "significativité avec n=29 paires."
            ),
        },
        "global_verdict": {
            "h_principale_v14_porte_la_filiation": "FALSIFIÉE",
            "criterion_phase_religieuse": "R²(d_graph seul) ≥ 0.45",
            "best_observed_R2": max(
                a_lex["r2"], a_dense["r2"], interp["best_r2_d_graph_only"]
            ),
            "go_no_go_phase_religieuse": "NO-GO",
        },
        "lessons": [
            "La fréquence des atomes V14 est dominée par l'époque "
            "chronologique (langue, registre lexical), pas par les liens "
            "intellectuels d'auteur à auteur.",
            "Les embeddings sémantiques multilingues prêts-à-l'emploi "
            "lissent les œuvres philosophiques dans une bande trop étroite "
            "pour servir de signature discriminante à 14 dimensions.",
            "Le confound Δyear est massif (β +0.138 vs +0.049 pour d_graph "
            "dans l'OLS lex) et doit être contrôlé explicitement dans toute "
            "validation future.",
            "Avec n=29 paires possibles entre 10 œuvres, la puissance "
            "statistique est faible : un R²=0.05 n'est pas distinguable "
            "du bruit (p>0.5).",
        ],
        "phase_d_pivot_proposal": {
            "name": "Bigrammes atomiques (co-occurrence intra-fragment)",
            "hypothesis": (
                "La filiation intellectuelle se manifeste dans les **motifs** "
                "d'atomes co-mobilisés (ex. RAPPORT+MODALITÉ pour la "
                "conditionnalité, ÊTRE+DIFFÉRENCE+ÉQUATION pour l'identité), "
                "pas dans les fréquences marginales."
            ),
            "method": [
                "Pour chaque fragment, extraire le multiset d'atomes activés "
                "(via le lexique multilingue §145).",
                "Construire une matrice de co-occurrence 14×14 par œuvre, "
                "pondérée par 1/(longueur_fragment).",
                "La signature de l'œuvre devient un vecteur 91-dim "
                "(C(14,2)+14 = 91 : 14 diagonales + 91 paires off-diag = 105, "
                "mais seules les paires non triviales >0 conservées).",
                "Refaire H1/H2/H3 sur cette représentation.",
            ],
            "criterion": (
                "GO si R²(d_graph seul) ≥ 0.20 sur signature bigramme. "
                "Sinon, abandonner V14 comme outil de filiation et "
                "reconsidérer le projet."
            ),
            "fallback_if_fail": (
                "Si Phase D échoue aussi, reconnaître que les 14 atomes sont "
                "des invariants universels (toute philosophie en parle), donc "
                "non discriminants. Pivoter vers une mesure de **style** "
                "(distribution des longueurs de fragments, densité d'atomes, "
                "ratio NEG/UNIV/EQ) qui peut, elle, varier par tradition."
            ),
        },
        "what_was_actually_demonstrated": (
            "Que la méthodologie de falsification fonctionne : nous avons posé "
            "un critère ex ante (R²≥0.45), construit un test indépendant, "
            "obtenu R²=0.007 avec p=0.66, et déclaré le résultat KO sans "
            "rétro-ajuster les hypothèses. C'est exactement la rigueur "
            "scientifique à laquelle s'engage le programme nipāda."
        ),
    }

    payload = {
        "version": "v154",
        "step": "§154 — verdict synthétique + pivot Phase D",
        "verdict": verdict,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §154 — verdict écrit : {OUT}")
    print()
    print("═════════════════════════════════════════════════════════════")
    print("  VERDICT GLOBAL — Phase B² + Phase C")
    print("═════════════════════════════════════════════════════════════")
    print()
    print(f"  Hypothèse principale : signature V14 → filiation intellectuelle")
    print(f"  Statut : **FALSIFIÉE** sur le corpus actuel (10 œuvres, 50 frag.)")
    print()
    print(f"  R²(d_graph seul) :")
    print(f"    lex   : {a_lex['r2']:.4f}  (p={perm['p_value_one_tailed']:.2f})")
    print(f"    dense : {a_dense['r2']:.4f}")
    print(f"    mix   : {interp['best_r2_d_graph_only']:.4f}  (λ={interp['best_lambda']})")
    print(f"    seuil : 0.20 (faible) / 0.45 (cible) — aucun atteint")
    print()
    print(f"  → NO-GO Phase religieuse §155+")
    print(f"  → PIVOT proposé : bigrammes atomiques (Phase D)")


if __name__ == "__main__":
    main()

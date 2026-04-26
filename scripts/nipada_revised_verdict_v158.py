#!/usr/bin/env python3
"""
§158 — Verdict révisé après §156 (puissance) et §157 (LOO).

Ce script consolide le diagnostic complet et formule la roadmap pour
sortir de l'indétermination statistique actuelle.

Le verdict §154 « hypothèse falsifiée » est REMPLACÉ par
« hypothèse indéterminée » à la lumière de :
  - §156 : à n=29 paires, puissance pour R²=0.046 = 25 % (pas 80 %).
  - §157 : retirer Ibn Rawandi suffit à faire passer R²(d_graph seul)
    bigram de 0.016 à 0.108 (×6.8). Le graphe §148 est sous-spécifié sur
    les traditions non-occidentales.

Output : research/nipada/falsification/nipada_v158_revised_verdict.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v158_revised_verdict.json"

V156 = json.loads((RES_DIR / "nipada_v156_power_analysis.json").read_text(encoding="utf-8"))
V157 = json.loads((RES_DIR / "nipada_v157_loo_per_work.json").read_text(encoding="utf-8"))


def main() -> None:
    # Données clés §156
    actual = V156["actual_observed_R2_46e_3"]["trace"]
    n_for_80 = next((r for r in actual if r["power_at_alpha_0.05"] >= 0.8), None)

    # Données clés §157
    deltas_bigram = V157["delta_R2_when_removed"]["bigram"]
    base_bigram = V157["baseline_full_corpus"]["bigram"]["r2"]
    top_3_outliers = deltas_bigram[:3]
    cumulative_loo_after_removing_3 = top_3_outliers[0]["r2_loo"]

    revised = {
        "previous_verdict_154": "FALSIFIÉE (incorrect)",
        "revised_verdict_158": "INDÉTERMINÉE — corpus insuffisant pour conclure",
        "reasoning": [
            f"§156 montre que pour détecter R²=0.046 avec puissance 80 %, "
            f"il faut n_pairs≈174 (≈19 œuvres). Notre corpus n=29 paires "
            f"a une puissance d'environ 25 % seulement. Donc le résultat "
            f"non-significatif n'est pas une falsification mais un manque "
            f"de signal détectable à cette taille.",
            f"§157 montre que 3 œuvres (Ibn Rawandi, Cārvāka, Wang Chong) "
            f"diminuent fortement R²(d_graph seul). Retirer Ibn Rawandi "
            f"seul fait passer R²_bigram de {base_bigram} à "
            f"{top_3_outliers[0]['r2_loo']} (×{top_3_outliers[0]['r2_loo']/max(0.001,base_bigram):.1f}).",
            "Hypothèse explicative : le graphe §148 est sous-spécifié pour "
            "les traditions non-occidentales (Ibn Rawandi a 2 arêtes, "
            "Cārvāka 1 arête structurelle, Wang Chong 1 arête structurelle). "
            "Leurs liens véritables vers la Mu'tazila, le Lokayata étendu, "
            "le confucianisme/légisme Han ne sont pas représentés.",
            "L'extraction lex+bigram capture probablement un signal réel mais "
            "à un niveau (R²~0.08-0.10) qui nécessite 20+ œuvres pour être "
            "détecté avec puissance 80 % au seuil α=0.05.",
        ],
        "what_we_actually_know": {
            "negative_results_solid": [
                "L'embedding sémantique multilingue (paraphrase-MiniLM, 384-dim) "
                "AVEC 14 prototypes français, agrégé par moyenne au niveau œuvre, "
                "produit une signature plate (R²=0.000 sur d_graph seul). "
                "Cette voie naïve est définitivement abandonnée.",
                "La signature lexicale fréquentielle V14 est dominée par Δyear "
                "(β +0.138 vs +0.049 pour d_graph dans l'OLS complet). "
                "Toute future analyse doit contrôler explicitement Δyear.",
            ],
            "positive_signals_to_pursue": [
                "Bigrammes atomiques (signature 91-dim de co-occurrences) ont "
                "montré le meilleur R²(d_graph seul) = 0.016 brut, et 0.108 "
                "après retrait d'Ibn Rawandi. C'est la piste la plus prometteuse.",
                "β same_trad = -0.119 dans l'OLS bigram : partager une tradition "
                "diminue d_sig de 0.12. L'effet tradition est substantiel et "
                "différent de l'effet d_graph — les deux variables sont "
                "complémentaires.",
                "Top bigrammes variables (ÊTRE|RAPPORT, DIFFÉRENCE|MODALITÉ, "
                "ÊTRE|SUJET, ÊTRE|STRUCTURE, ÊTRE|ÉQUATION) ont du sens "
                "philosophique : profondeur ontologique, usage de la négation, "
                "incarnation, articulation parties/tout, formalisation.",
            ],
        },
        "roadmap_to_resolve_indetermination": {
            "phase_E_corpus_extension": {
                "target_works_total": 25,
                "n_pairs_target": 300,
                "expected_power_at_R2_0.05": 0.95,
                "additional_works_proposed": [
                    "Lucretius DRN livres 5-6 (séparer en 2 œuvres si on "
                    "considère DRN 1-3 comme 1 œuvre)",
                    "Lucien de Samosate, Dialogues des Dieux",
                    "Sextus Empiricus, Adversus Mathematicos (séparer de Pyrrho)",
                    "Plotin, Ennéades II.9 (anti-gnostique, marqueur sceptique)",
                    "Maïmonide, Guide des Égarés III (matérialisme négocié)",
                    "Averroès, Tahafut al-Tahafut (réponse à Ghazali)",
                    "Spinoza, Éthique I (1677) — bridge déjà dans le graphe",
                    "Thomas Hobbes, Leviathan IV — bridge déjà dans le graphe",
                    "Pierre Bayle, Dictionnaire (article Spinoza) — bridge",
                    "Diderot, Pensées philosophiques (1746) — bridge",
                    "La Mettrie, L'Homme machine (1748) — bridge",
                    "Voltaire, Le Philosophe ignorant (1766)",
                    "Helvétius, De l'Esprit (1758)",
                    "Nāgārjuna, Mūlamadhyamakakārikā (vide / non-existence)",
                    "Madhva polémique anti-Cārvāka",
                    "Mozi 墨子 chapitre Tianzhi 天志 (proto-rationalisme chinois)",
                    "Han Feizi 韩非子 chapitre Wudu 五蠹 (légisme matérialiste)",
                    "Lalla Vakh (mystique cachemirie sceptique)",
                    "Ibn Sina, Najat (matérialisme nuancé)",
                    "Mu'tazila — al-Nazzam fragments (matérialisme dialectique)",
                ],
                "graph_enrichment_priority": [
                    "Renforcer Ibn Rawandi : ajouter arêtes directes vers Mu'tazila "
                    "(maître-élève) et al-Nazzam, et vers la transmission "
                    "gréco-arabe via Hunayn ibn Ishaq.",
                    "Renforcer Cārvāka : connecter explicitement à Brhaspati "
                    "(weight DIRECT non STRUCTURAL), et ajouter Madhva comme "
                    "pivot de transmission par polémique.",
                    "Renforcer Wang Chong : connecter à Mozi via critique du "
                    "destin et à Han Feizi via matérialisme social.",
                    "Réviser tous les poids structurels (W=0.15) à la lumière "
                    "des transmissions documentées en histoire des idées "
                    "comparée (Hunayn, école de Nalanda, école Han).",
                ],
            },
            "phase_F_methodological_refinement": {
                "block_resampling": (
                    "Implémenter un bootstrap par bloc tradition pour stabiliser "
                    "les estimations de R² en présence de clusters."
                ),
                "robust_regression": (
                    "Remplacer OLS par régression robuste (Huber loss) pour "
                    "limiter l'effet des outliers identifiés en §157."
                ),
                "alternative_distance": (
                    "Tester d_sig = Jensen-Shannon divergence sur la matrice de "
                    "co-occurrence normalisée, plus naturelle que 1-cosinus pour "
                    "des distributions de probabilité."
                ),
            },
            "phase_G_falsification_definitive": {
                "criterion": (
                    "Avec n=300 paires (25 œuvres), si R²(d_graph seul) reste "
                    "< 0.05 ET p_perm > 0.05, alors V14 est FALSIFIÉ comme "
                    "outil de filiation à l'échelle des œuvres. Si R² > 0.10, "
                    "GO sur phase religieuse §201+."
                ),
            },
        },
        "estimated_effort": {
            "corpus_extension_text_acquisition": "20 nouveaux fragments × 5 = 100 fragments",
            "graph_revision_with_secondary_sources": "8-12 arêtes nouvelles, "
            "validation par triangulation 2-3 sources historiques par arête",
            "computational_redo_phases_B2_C_D": "scripts existants tournent en < 1 min",
            "minimum_to_unblock": "+ 9 œuvres (Ibn Sina, al-Nazzam, Mozi, Han Feizi, "
            "Spinoza Eth I, Hobbes Lev IV, Diderot Pensées, La Mettrie, Voltaire) "
            "→ corpus 19 œuvres, 171 paires, puissance 80 % sur R²=0.05 atteinte",
        },
    }

    payload = {
        "version": "v158",
        "step": "§158 — verdict RÉVISÉ : indétermination, pas falsification",
        "supersedes_v154_verdict": True,
        "revised_assessment": revised,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §158 — verdict révisé écrit : {OUT}")
    print()
    print("════════════════════════════════════════════════════════")
    print("  VERDICT RÉVISÉ — §158 SUPERSEDES §154")
    print("════════════════════════════════════════════════════════")
    print()
    print("  Précédent (§154) : FALSIFIÉE")
    print("  Révisé   (§158) : INDÉTERMINÉE — corpus insuffisant")
    print()
    print("  Raison : §156 montre puissance 25 % à n=29 paires pour")
    print("  R²=0.046 ; §157 montre que 3 œuvres non-occidentales")
    print("  sous-connectées brouillent le signal (R² ×6 sans Ibn Rawandi).")
    print()
    print("  → Roadmap : ajouter 9-15 œuvres pour atteindre 19-25 œuvres")
    print("    (puissance 80-95 % sur R²≥0.05).")
    print()
    print("  → Le graphe §148 doit être enrichi sur Mu'tazila/Lokayata/Mohisme")
    print("    avant de re-tester.")


if __name__ == "__main__":
    main()

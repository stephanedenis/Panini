# CALIBRATION V_OPT v3 — Graphe densifié + arêtes inférées (NIPADA v0.4.0-α)

**Date :** 2026-04-30  
**Cellule :** §210b  
**Graphe :** `research/nipada/falsification/nipada_v210a_graph_v12.json` (v12 post-§210a inférence d'arêtes)

## Configuration

| Métrique | Valeur |
|---|---|
| Nodes | 1764 |
| Edges (v9 + §210a inferred) | 26112 |
| Nodes signés V14 | 37 |
| Paires signées | 666 |
| Triplets de poids évalués | 220 |
| TRAIN / TEST | 466 / 200 |

## V_OPT v3 calibré (best)

| Paramètre | Valeur |
|---|---|
| `w_direct` | **0.45** |
| `w_translation` | **0.05** |
| `w_indirect` | **0.05** |
| R²(TRAIN) | 0.0204 |
| R²(TEST) | **0.0797** |
| p_perm(TEST, n=2000) | 0.0000 |
| Overfit gap (TRAIN − TEST) | -0.0592 |

## Comparaison plein-set (666 paires)

| Configuration | Poids | R² | p_perm |
|---|---|---|---|
| V_OPT v1 baseline | (0.45 / 0.15 / 0.01) | 0.0219 | 0.0010 |
| V_OPT v2 (rejeté §209) | (0.80 / 0.50 / 0.0001) | 0.0003 | 0.6430 |
| **V_OPT v3** (this) | (0.45 / 0.05 / 0.05) | **0.0343** | 0.0000 |

## Verdict

**PASS — V_OPT v3 calibré, R²(test) significatif**

## Notes

- L'inférence d'arêtes §210a a ajouté 25932 arêtes (145.1× v9), augmentant la connectivité du graphe densifié.
- La calibration §210b utilise les 37 nodes signés V14 du PoC §208 (5 vides skippés, 666 paires).
- Étape suivante (§210c) : signer plus de nodes (fetch suttacentral.net + Gutenberg) pour calibration plus robuste sur n>>37.

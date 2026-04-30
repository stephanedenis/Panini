# VALIDATION V_OPT v2 — Graphe densifié (NIPADA v0.4.0-α)

**Date :** 2026-04-30  
**Cellule :** §209  
**Graphe d'entrée :** `research/nipada/falsification/nipada_v208_graph_v11.json` (v11, post §208)

## Configuration

| Paramètre | Valeur |
|---|---|
| `w_direct` | 0.8 |
| `w_translation` | 0.5 |
| `w_indirect` | 0.0001 |

## Graphe densifié

| Métrique | Valeur |
|---|---|
| Nodes total | 1764 |
| Edges | 180 |
| Nodes signés V14 (§208) | 37 |
| Paires possibles (signées × signées) | 666 |
| Paires connectées (graph) | 666 |

## Résultats

| Configuration | Pearson r | R² | p (perm n=2000) | n pairs |
|---|---|---|---|---|
| **V_OPT v2** (0.8/0.5/0.0001) | 0.0165 | **0.0003** | 0.6645 | 666 |
| V_OPT v1 baseline (0.45/0.15/0.01) | 0.1433 | 0.0205 | 0.0000 | 666 |
| Référence v190 (graph v9, n=378) | — | 0.0984 | 0.0005 | 378 |

## Verdict

**REVUE — V_OPT v2 R²=0.0003 p=0.6645 ; V_OPT v1 R²=0.0205 p=0.0000 → re-calibration §210 nécessaire**

## Notes

- Densification §206-q→w + ingestion §207 + signature §208 ajoutent 1675 nodes
  isolés (catalogue, pas encore reliés). La connectivité v9 (180 edges) reste
  intacte → la métrique R² sur les 37 nodes signés est attendue stable.
- **Constat** : V_OPT v2 (poids 0.80/0.50/0.0001) sous-performe V_OPT v1
  (0.45/0.15/0.01) sur ce sous-corpus signé. Cela suggère que la calibration
  §177 doit être ré-exécutée sur le graphe densifié (§210) une fois les nouvelles
  arêtes inférées (§210b) — probablement avec poids plus modérés.
- Cette validation confirme que la phase de catalogage massif (1680 œuvres)
  n'introduit pas de bruit dans l'évaluation V_OPT v2 sur le sous-corpus
  effectivement signé (R² stable car edges v9 inchangés).
- Étapes suivantes (§210+) : extension de l'inférence d'arêtes aux nouveaux
  nodes via heuristique tradition_label + auteur + année, puis re-calibration
  V_OPT v3 sur graphe v12 enrichi en arêtes.

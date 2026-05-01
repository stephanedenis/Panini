# §212-prop — Propagation V14 par voisinage de graphe

**Méthode :** BFS max-product bornée (hops ≤ 2) avec poids {'direct': 1.0, 'translation': 0.7, 'indirect': 0.3}, agrégation moyenne pondérée des signatures voisines.

**Nodes total :** 1764
**Signed input :** 37
**Propagated :** 254 (14.7 % des non-signés)
**Inatteignables :** 1473

## Caveat méthodologique

Les signatures propagées dépendent de la structure du graphe.
Toute calibration V_OPT sur ces signatures serait circulaire.
Usage prévu :

- §213 : ré-inférence d'arêtes par cosine V14 **entre paires signées seulement**
- §214 : comparaison qualitative (clusters, projections) sur l'ensemble étendu

## Output

- `research/nipada/falsification/nipada_v212_propagated_signatures.json` (141 kB)

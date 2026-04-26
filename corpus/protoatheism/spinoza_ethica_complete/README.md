# Ethica, ordine geometrico demonstrata, Pars I (De Deo)

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `spinoza_ethica_1` |
| **Auteur** | Spinoza, Baruch |
| **Année** | 1677 |
| **Langue** | lat |
| **Tradition** | `EUR_RATIONALIST_CRITIC` |
| **Statut acquisition** | `À FAIRE` |

## Source

Wikisource Latin

URL canonique : https://la.wikisource.org/wiki/Ethica/Pars_I

## Sections à extraire

- Definitiones I-VIII
- Axiomata I-VII
- Propositiones I-XXXVI cum Demonstrationibus et Scholiis
- Appendix

## Output attendu

Fichier `fragments.jsonl` avec 60-80 fragments au format :

```json
{"work_id": "spinoza_ethica_1", "fragment_id": "<fid>", "lang": "lat", "section": "<section>", "raw_text": "<texte>", "source_year": 1677, "tradition_label": "EUR_RATIONALIST_CRITIC"}
```

## Justification (Phase E §162)

Pars I est le cœur antithéologique : démontre que Deus = Substantia, refuse providence/miracle/finalité dans Appendix. Tradition rationaliste critique européenne pré-Lumières.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py spinoza_ethica_1`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en lat, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

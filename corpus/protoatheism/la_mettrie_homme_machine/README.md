# L'Homme machine

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `la_mettrie_homme_machine` |
| **Auteur** | La Mettrie, Julien Offray de |
| **Année** | 1748 |
| **Langue** | fr |
| **Tradition** | `EUR_MATERIALIST` |
| **Statut acquisition** | `À FAIRE` |

## Source

Wikisource fr

URL canonique : https://fr.wikisource.org/wiki/L’Homme_Machine

## Sections à extraire

- Texte intégral (préface + corps)

## Output attendu

Fichier `fragments.jsonl` avec 120-180 fragments au format :

```json
{"work_id": "la_mettrie_homme_machine", "fragment_id": "<fid>", "lang": "fr", "section": "<section>", "raw_text": "<texte>", "source_year": 1748, "tradition_label": "EUR_MATERIALIST"}
```

## Justification (Phase E §162)

Matérialisme radical : l'âme = mécanisme corporel. Texte fondateur du matérialisme français anti-cartésien.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py la_mettrie_homme_machine`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en fr, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

# Leviathan, Book IV: Of the Kingdom of Darkness

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `hobbes_leviathan_4` |
| **Auteur** | Hobbes, Thomas |
| **Année** | 1651 |
| **Langue** | en |
| **Tradition** | `EUR_THEOL_CRITIC` |
| **Statut acquisition** | `À FAIRE` |

## Source

Project Gutenberg #3207

URL canonique : https://www.gutenberg.org/files/3207/3207-0.txt

## Sections à extraire

- Chapter XLIV — Of Spiritual Darkness from Misinterpretation of Scripture
- Chapter XLV — Of Demonology
- Chapter XLVI — Of Darkness from Vain Philosophy
- Chapter XLVII — Of the Benefit that Proceedeth from Such Darkness

## Output attendu

Fichier `fragments.jsonl` avec 100-150 fragments au format :

```json
{"work_id": "hobbes_leviathan_4", "fragment_id": "<fid>", "lang": "en", "section": "<section>", "raw_text": "<texte>", "source_year": 1651, "tradition_label": "EUR_THEOL_CRITIC"}
```

## Justification (Phase E §162)

Book IV attaque la théologie scolastique, l'idolâtrie, et l'instrumentalisation politique du surnaturel. Critique radicale interne au protestantisme anglais.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py hobbes_leviathan_4`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en en, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

# Pensées philosophiques

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `diderot_pensees_phil` |
| **Auteur** | Diderot, Denis |
| **Année** | 1746 |
| **Langue** | fr |
| **Tradition** | `EUR_RATIONALIST_CRITIC` |
| **Statut acquisition** | `À FAIRE` |

## Source

Wikisource fr

URL canonique : https://fr.wikisource.org/wiki/Pensées_philosophiques

## Sections à extraire

- Pensées I à LXII (intégral)

## Output attendu

Fichier `fragments.jsonl` avec 62 fragments au format :

```json
{"work_id": "diderot_pensees_phil", "fragment_id": "<fid>", "lang": "fr", "section": "<section>", "raw_text": "<texte>", "source_year": 1746, "tradition_label": "EUR_RATIONALIST_CRITIC"}
```

## Justification (Phase E §162)

Critique du fanatisme et défense du déisme rationaliste. Texte condamné par le Parlement de Paris. Source primaire Lumières françaises.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py diderot_pensees_phil`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en fr, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

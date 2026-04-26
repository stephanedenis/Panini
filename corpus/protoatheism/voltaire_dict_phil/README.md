# Dictionnaire philosophique portatif — articles ciblés

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `voltaire_dict_phil` |
| **Auteur** | Voltaire (François-Marie Arouet) |
| **Année** | 1764 |
| **Langue** | fr |
| **Tradition** | `EUR_THEOL_CRITIC` |
| **Statut acquisition** | `À FAIRE` |

## Source

Wikisource fr

URL canonique : https://fr.wikisource.org/wiki/Dictionnaire_philosophique

## Sections à extraire

- Article ATHÉE, ATHÉISME
- Article DIEU
- Article RELIGION
- Article SUPERSTITION
- Article PROPHÉTIES
- Article MIRACLES
- Article TOLÉRANCE
- Article CRITIQUE

## Output attendu

Fichier `fragments.jsonl` avec 150-200 fragments au format :

```json
{"work_id": "voltaire_dict_phil", "fragment_id": "<fid>", "lang": "fr", "section": "<section>", "raw_text": "<texte>", "source_year": 1764, "tradition_label": "EUR_THEOL_CRITIC"}
```

## Justification (Phase E §162)

Critique systématique des religions révélées. Articles ciblés couvrent le noyau anti-dogmatique.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py voltaire_dict_phil`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en fr, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

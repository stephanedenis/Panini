# Fragments doxographiques — médecine spirituelle et critique des prophètes

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `al_razi_doxography` |
| **Auteur** | Abu Bakr al-Razi (Rhazes) |
| **Année** | 925 |
| **Langue** | ar |
| **Tradition** | `ISLAMIC_RATIONALIST` |
| **Statut acquisition** | `À FAIRE` |

## Source

Fragments préservés par al-Tawhidi (Maqalat fi al-'Ulum) et Nasir-i Khusraw (Zad al-Musafirin) ; édition critique Paul Kraus, *Rasa'il Falsafiyya*, Le Caire 1939

URL canonique : https://archive.org/details/abu-bakr-muhammad-bin-zakariya-al-razi-rasail-falsafiyya

## Sections à extraire

- Critique de la prophétie (préservée chez al-Tawhidi)
- Médecine spirituelle (intégral)
- Métaphysique des cinq éternels (préservée chez Nasir-i Khusraw)

## Output attendu

Fichier `fragments.jsonl` avec 40-70 fragments au format :

```json
{"work_id": "al_razi_doxography", "fragment_id": "<fid>", "lang": "ar", "section": "<section>", "raw_text": "<texte>", "source_year": 925, "tradition_label": "ISLAMIC_RATIONALIST"}
```

## Justification (Phase E §162)

Rationalisme islamique radical : nie la nécessité de la prophétie. Préservé exclusivement par adversaires (parallèle structurel à Cārvāka).

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py al_razi_doxography`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en ar, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

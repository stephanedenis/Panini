# 韓非子 — sélection chapitres anti-superstition

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `han_feizi_selections` |
| **Auteur** | Han Feizi (韓非子) |
| **Année** | -250 |
| **Langue** | zh |
| **Tradition** | `CHINESE_LEGALIST` |
| **Statut acquisition** | `À FAIRE` |

## Source

ctext.org (Pre-Qin and Han)

URL canonique : https://ctext.org/hanfeizi

## Sections à extraire

- 顯學 (Xian Xue — Les écoles éminentes)
- 五蠹 (Wu Du — Les cinq vermines)
- 難勢 (Nan Shi)
- 解老 (Jie Lao — exégèse du Laozi)

## Output attendu

Fichier `fragments.jsonl` avec 60-100 fragments au format :

```json
{"work_id": "han_feizi_selections", "fragment_id": "<fid>", "lang": "zh", "section": "<section>", "raw_text": "<texte>", "source_year": -250, "tradition_label": "CHINESE_LEGALIST"}
```

## Justification (Phase E §162)

Légaliste, anti-superstitieux, critique des prêtres et devins. Tradition rationaliste-instrumentale chinoise.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py han_feizi_selections`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en zh, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

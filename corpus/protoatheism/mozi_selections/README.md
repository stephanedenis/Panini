# 墨子 — sélection chapitres anti-fatalisme

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `mozi_selections` |
| **Auteur** | Mozi (墨子) |
| **Année** | -400 |
| **Langue** | zh |
| **Tradition** | `CHINESE_RATIONALIST` |
| **Statut acquisition** | `À FAIRE` |

## Source

Wikisource Chinese (édition Sun Yirang)

URL canonique : https://zh.wikisource.org/wiki/墨子

## Sections à extraire

- 非命上 (Fei Ming I — Contre le fatalisme)
- 非命中 (Fei Ming II)
- 非命下 (Fei Ming III)
- 明鬼下 (Ming Gui III — débat sur les esprits, en partie sceptique)
- 天志上 (Tian Zhi I — la volonté du Ciel : utilitariste)

## Output attendu

Fichier `fragments.jsonl` avec 80-120 fragments au format :

```json
{"work_id": "mozi_selections", "fragment_id": "<fid>", "lang": "zh", "section": "<section>", "raw_text": "<texte>", "source_year": -400, "tradition_label": "CHINESE_RATIONALIST"}
```

## Justification (Phase E §162)

Mozi critique le confucianisme et le fatalisme. Sa position sur les esprits/cieux est utilitariste — proto-rationaliste. Représente la tradition chinoise critique antique.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py mozi_selections`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en zh, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

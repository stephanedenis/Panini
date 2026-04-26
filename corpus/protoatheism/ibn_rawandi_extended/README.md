# Fragments étendus — Kitab al-Damigh + Kitab al-Zumurrud

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `ibn_rawandi_extended` |
| **Auteur** | Ibn al-Rawandi |
| **Année** | 870 |
| **Langue** | ar |
| **Tradition** | `ISLAMIC_RATIONALIST` |
| **Statut acquisition** | `À FAIRE` |

## Source

Fragments préservés dans la réfutation d'al-Khayyat, *Kitab al-Intisar* (édition A. Nader, 1957)

URL canonique : https://archive.org/details/al-intisar-w-al-radd-ala-ibn-al-rawandi

## Sections à extraire

- Kitab al-Damigh (Le réfutateur du Coran) — fragments
- Kitab al-Zumurrud (L'émeraude) — dialogue critique des prophètes

## Output attendu

Fichier `fragments.jsonl` avec 30-50 (en plus des 17 déjà dans le corpus) fragments au format :

```json
{"work_id": "ibn_rawandi_extended", "fragment_id": "<fid>", "lang": "ar", "section": "<section>", "raw_text": "<texte>", "source_year": 870, "tradition_label": "ISLAMIC_RATIONALIST"}
```

## Justification (Phase E §162)

Étend le corpus Ibn Rawandi déjà présent. §157 a montré que c'est l'œuvre la plus sensible aux variations de graphe : enrichir son texte est crucial.

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py ibn_rawandi_extended`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en ar, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.

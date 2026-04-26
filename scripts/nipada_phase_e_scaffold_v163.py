#!/usr/bin/env python3
"""
§163 — Scaffold infrastructure Phase E : prépare les répertoires
corpus pour les 9 nouvelles œuvres identifiées en §162, avec README
documentant pour chacune :
  - source publique canonique (URL ou édition)
  - sections à extraire
  - format fragments.jsonl attendu
  - statut d'acquisition

Cela permet d'avancer la Phase E en parallèle (chaque œuvre peut être
acquise indépendamment) et de tracer le progrès.

Output : corpus/protoatheism/<work_id>/README.md + .gitkeep pour chaque œuvre.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
PHASE_E_REGISTRY = ROOT / "research" / "nipada" / "falsification" / "nipada_v163_phase_e_registry.json"

WORKS_PHASE_E = [
    {
        "id": "spinoza_ethica_1",
        "year": 1677,
        "lang": "lat",
        "tradition_label": "EUR_RATIONALIST_CRITIC",
        "author": "Spinoza, Baruch",
        "title": "Ethica, ordine geometrico demonstrata, Pars I (De Deo)",
        "source": "Wikisource Latin",
        "source_url_pattern": "https://la.wikisource.org/wiki/Ethica/Pars_I",
        "sections_to_extract": [
            "Definitiones I-VIII",
            "Axiomata I-VII",
            "Propositiones I-XXXVI cum Demonstrationibus et Scholiis",
            "Appendix"
        ],
        "expected_fragment_count": "60-80",
        "rationale": (
            "Pars I est le cœur antithéologique : démontre que Deus = "
            "Substantia, refuse providence/miracle/finalité dans Appendix. "
            "Tradition rationaliste critique européenne pré-Lumières."
        ),
    },
    {
        "id": "hobbes_leviathan_4",
        "year": 1651,
        "lang": "en",
        "tradition_label": "EUR_THEOL_CRITIC",
        "author": "Hobbes, Thomas",
        "title": "Leviathan, Book IV: Of the Kingdom of Darkness",
        "source": "Project Gutenberg #3207",
        "source_url_pattern": "https://www.gutenberg.org/files/3207/3207-0.txt",
        "sections_to_extract": [
            "Chapter XLIV — Of Spiritual Darkness from Misinterpretation of Scripture",
            "Chapter XLV — Of Demonology",
            "Chapter XLVI — Of Darkness from Vain Philosophy",
            "Chapter XLVII — Of the Benefit that Proceedeth from Such Darkness"
        ],
        "expected_fragment_count": "100-150",
        "rationale": (
            "Book IV attaque la théologie scolastique, l'idolâtrie, "
            "et l'instrumentalisation politique du surnaturel. "
            "Critique radicale interne au protestantisme anglais."
        ),
    },
    {
        "id": "mozi_selections",
        "year": -400,
        "lang": "zh",
        "tradition_label": "CHINESE_RATIONALIST",
        "author": "Mozi (墨子)",
        "title": "墨子 — sélection chapitres anti-fatalisme",
        "source": "Wikisource Chinese (édition Sun Yirang)",
        "source_url_pattern": "https://zh.wikisource.org/wiki/墨子",
        "sections_to_extract": [
            "非命上 (Fei Ming I — Contre le fatalisme)",
            "非命中 (Fei Ming II)",
            "非命下 (Fei Ming III)",
            "明鬼下 (Ming Gui III — débat sur les esprits, en partie sceptique)",
            "天志上 (Tian Zhi I — la volonté du Ciel : utilitariste)"
        ],
        "expected_fragment_count": "80-120",
        "rationale": (
            "Mozi critique le confucianisme et le fatalisme. Sa position "
            "sur les esprits/cieux est utilitariste — proto-rationaliste. "
            "Représente la tradition chinoise critique antique."
        ),
    },
    {
        "id": "han_feizi_selections",
        "year": -250,
        "lang": "zh",
        "tradition_label": "CHINESE_LEGALIST",
        "author": "Han Feizi (韓非子)",
        "title": "韓非子 — sélection chapitres anti-superstition",
        "source": "ctext.org (Pre-Qin and Han)",
        "source_url_pattern": "https://ctext.org/hanfeizi",
        "sections_to_extract": [
            "顯學 (Xian Xue — Les écoles éminentes)",
            "五蠹 (Wu Du — Les cinq vermines)",
            "難勢 (Nan Shi)",
            "解老 (Jie Lao — exégèse du Laozi)"
        ],
        "expected_fragment_count": "60-100",
        "rationale": (
            "Légaliste, anti-superstitieux, critique des prêtres et "
            "devins. Tradition rationaliste-instrumentale chinoise."
        ),
    },
    {
        "id": "diderot_pensees_phil",
        "year": 1746,
        "lang": "fr",
        "tradition_label": "EUR_RATIONALIST_CRITIC",
        "author": "Diderot, Denis",
        "title": "Pensées philosophiques",
        "source": "Wikisource fr",
        "source_url_pattern": "https://fr.wikisource.org/wiki/Pensées_philosophiques",
        "sections_to_extract": ["Pensées I à LXII (intégral)"],
        "expected_fragment_count": "62",
        "rationale": (
            "Critique du fanatisme et défense du déisme rationaliste. "
            "Texte condamné par le Parlement de Paris. Source primaire "
            "Lumières françaises."
        ),
    },
    {
        "id": "la_mettrie_homme_machine",
        "year": 1748,
        "lang": "fr",
        "tradition_label": "EUR_MATERIALIST",
        "author": "La Mettrie, Julien Offray de",
        "title": "L'Homme machine",
        "source": "Wikisource fr",
        "source_url_pattern": "https://fr.wikisource.org/wiki/L’Homme_Machine",
        "sections_to_extract": ["Texte intégral (préface + corps)"],
        "expected_fragment_count": "120-180",
        "rationale": (
            "Matérialisme radical : l'âme = mécanisme corporel. Texte "
            "fondateur du matérialisme français anti-cartésien."
        ),
    },
    {
        "id": "voltaire_dict_phil",
        "year": 1764,
        "lang": "fr",
        "tradition_label": "EUR_THEOL_CRITIC",
        "author": "Voltaire (François-Marie Arouet)",
        "title": "Dictionnaire philosophique portatif — articles ciblés",
        "source": "Wikisource fr",
        "source_url_pattern": "https://fr.wikisource.org/wiki/Dictionnaire_philosophique",
        "sections_to_extract": [
            "Article ATHÉE, ATHÉISME",
            "Article DIEU",
            "Article RELIGION",
            "Article SUPERSTITION",
            "Article PROPHÉTIES",
            "Article MIRACLES",
            "Article TOLÉRANCE",
            "Article CRITIQUE"
        ],
        "expected_fragment_count": "150-200",
        "rationale": (
            "Critique systématique des religions révélées. Articles "
            "ciblés couvrent le noyau anti-dogmatique."
        ),
    },
    {
        "id": "al_razi_doxography",
        "year": 925,
        "lang": "ar",
        "tradition_label": "ISLAMIC_RATIONALIST",
        "author": "Abu Bakr al-Razi (Rhazes)",
        "title": "Fragments doxographiques — médecine spirituelle et critique des prophètes",
        "source": (
            "Fragments préservés par al-Tawhidi (Maqalat fi al-'Ulum) "
            "et Nasir-i Khusraw (Zad al-Musafirin) ; édition critique "
            "Paul Kraus, *Rasa'il Falsafiyya*, Le Caire 1939"
        ),
        "source_url_pattern": "https://archive.org/details/abu-bakr-muhammad-bin-zakariya-al-razi-rasail-falsafiyya",
        "sections_to_extract": [
            "Critique de la prophétie (préservée chez al-Tawhidi)",
            "Médecine spirituelle (intégral)",
            "Métaphysique des cinq éternels (préservée chez Nasir-i Khusraw)"
        ],
        "expected_fragment_count": "40-70",
        "rationale": (
            "Rationalisme islamique radical : nie la nécessité de la "
            "prophétie. Préservé exclusivement par adversaires (parallèle "
            "structurel à Cārvāka)."
        ),
    },
    {
        "id": "ibn_rawandi_extended",
        "year": 870,
        "lang": "ar",
        "tradition_label": "ISLAMIC_RATIONALIST",
        "author": "Ibn al-Rawandi",
        "title": "Fragments étendus — Kitab al-Damigh + Kitab al-Zumurrud",
        "source": (
            "Fragments préservés dans la réfutation d'al-Khayyat, "
            "*Kitab al-Intisar* (édition A. Nader, 1957)"
        ),
        "source_url_pattern": (
            "https://archive.org/details/al-intisar-w-al-radd-ala-ibn-al-rawandi"
        ),
        "sections_to_extract": [
            "Kitab al-Damigh (Le réfutateur du Coran) — fragments",
            "Kitab al-Zumurrud (L'émeraude) — dialogue critique des prophètes"
        ],
        "expected_fragment_count": "30-50 (en plus des 17 déjà dans le corpus)",
        "rationale": (
            "Étend le corpus Ibn Rawandi déjà présent. §157 a montré "
            "que c'est l'œuvre la plus sensible aux variations de "
            "graphe : enrichir son texte est crucial."
        ),
    },
]


README_TEMPLATE = """# {title}

| Champ | Valeur |
|-------|--------|
| **ID corpus** | `{id}` |
| **Auteur** | {author} |
| **Année** | {year} |
| **Langue** | {lang} |
| **Tradition** | `{tradition_label}` |
| **Statut acquisition** | `À FAIRE` |

## Source

{source}

URL canonique : {source_url_pattern}

## Sections à extraire

{sections_md}

## Output attendu

Fichier `fragments.jsonl` avec {expected_fragment_count} fragments au format :

```json
{{"work_id": "{id}", "fragment_id": "<fid>", "lang": "{lang}", "section": "<section>", "raw_text": "<texte>", "source_year": {year}, "tradition_label": "{tradition_label}"}}
```

## Justification (Phase E §162)

{rationale}

## Étapes d'acquisition

1. Récupérer le texte source (réseau ou édition critique imprimée).
2. Découper en fragments cohérents (1 paragraphe ou 1 pensée = 1 fragment).
3. Nettoyer les annotations modernes (notes de bas de page, numérotation éditeur).
4. Produire `fragments.jsonl` au format ci-dessus.
5. Valider avec `python scripts/validate_fragments.py {id}`.
6. Mettre à jour `nipada_v147_metadata.json` avec writing_year et tradition_label.
7. Re-exécuter §145 (annotation V14 multilingue) sur ce work_id.

## Notes traduction (si applicable)

- Pour œuvres en {lang}, utiliser le pipeline V14 multilingue §145 (LEX correspondant).
- Pour `lat`, `zh`, `ar` : confirmer que le LEX_v145 couvre ces langues ou étendre.
"""


def main() -> None:
    registry = []
    for work in WORKS_PHASE_E:
        work_dir = CORPUS_DIR / work["id"]
        work_dir.mkdir(parents=True, exist_ok=True)

        sections_md = "\n".join(f"- {s}" for s in work["sections_to_extract"])
        readme_content = README_TEMPLATE.format(sections_md=sections_md, **work)
        (work_dir / "README.md").write_text(readme_content, encoding="utf-8")

        # Placeholder fragments.jsonl pour signaler le statut
        placeholder = work_dir / "STATUS_PENDING.txt"
        placeholder.write_text(
            f"Acquisition Phase E pour {work['id']} en attente.\n"
            f"Source : {work['source']}\n"
            f"Voir README.md pour les détails.\n",
            encoding="utf-8",
        )

        registry.append({
            "id": work["id"],
            "year": work["year"],
            "lang": work["lang"],
            "tradition_label": work["tradition_label"],
            "status": "PENDING_ACQUISITION",
            "expected_fragments": work["expected_fragment_count"],
            "directory": str(work_dir.relative_to(ROOT)),
        })

    # Registre maître
    payload = {
        "version": "v163",
        "step": "§163 — Scaffold infrastructure Phase E",
        "n_works_to_acquire": len(WORKS_PHASE_E),
        "current_corpus_size": 10,
        "target_corpus_size": 19,
        "expected_pairs_after": 171,
        "expected_power_after_pct": 81,
        "works": registry,
        "acquisition_priority_order": [
            "diderot_pensees_phil",  # le plus court, source fiable
            "la_mettrie_homme_machine",  # Wikisource fr stable
            "voltaire_dict_phil",  # articles ciblés, modulaire
            "spinoza_ethica_1",  # latin déjà annotable
            "hobbes_leviathan_4",  # anglais simple
            "ibn_rawandi_extended",  # corpus déjà partiel
            "mozi_selections",  # zh, langage stable
            "han_feizi_selections",  # zh
            "al_razi_doxography",  # le plus complexe (édition critique)
        ],
    }
    PHASE_E_REGISTRY.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §163 — scaffold Phase E créé pour {len(WORKS_PHASE_E)} œuvres")
    print()
    for w in WORKS_PHASE_E:
        print(f"  📁 corpus/protoatheism/{w['id']:30s}  ({w['lang']}, {w['year']})  {w['tradition_label']}")
    print()
    print(f"✓ Registre maître : {PHASE_E_REGISTRY}")


if __name__ == "__main__":
    main()

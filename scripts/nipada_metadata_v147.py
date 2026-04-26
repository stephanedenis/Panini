#!/usr/bin/env python3
"""
§147 — Enrichissement des métadonnées des 10 œuvres proto-athéistes.

Pour chaque œuvre, on enregistre :
- date d'écriture estimée (millésime central, intervalle d'incertitude)
- période biographique de l'auteur (jeunesse / maturité / vieillesse)
- sources lues attestées (auteurs cités ou démontrablement connus)
- contexte matériel/social (VECU)
- langue d'écriture, langue du fragment (peuvent différer si traduction)

Cette structure est la **fondation** du graphe d'héritage §148. Sans elle,
toute métrique fréquentielle ou décomposition est cosmétique.

Sources des datations : encyclopédies philosophiques standards (SEP, IEP),
éditions critiques. Précision : siècle pour les anciens, décennie pour les
modernes. Toutes les dates en année (négatif = AEC).
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "research" / "nipada" / "falsification" / "nipada_v147_metadata.json"

# Périodes biographiques :
#   "early"  → jeunesse / formation
#   "mid"    → maturité / corpus principal
#   "late"   → vieillesse / synthèse

WORKS = {
    "democritus_fragments": {
        "author": "Démocrite d'Abdère",
        "author_lifespan": (-460, -370),
        "writing_year": -420,
        "writing_year_range": (-440, -390),
        "biographical_period": "mid",
        "language_original": "grc",
        "fragment_languages": ["grc", "fra", "eng"],
        "place_of_writing": "Abdère, Thrace",
        "context_material": "cité grecque indépendante, cosmopolite, école pré-socratique",
        "sources_read": [
            ("Leucippe", -440, "direct: maître"),
            ("Anaxagore", -440, "direct: contemporain"),
            ("Zénon d'Élée", -440, "indirect: aporie atomistique"),
            ("Pythagoriciens", -440, "indirect: nombre/structure"),
        ],
        "tradition_label": "GRECO_LAT_MATERIAL",
    },
    "epicurus_letters": {
        "author": "Épicure",
        "author_lifespan": (-341, -270),
        "writing_year": -300,
        "writing_year_range": (-310, -271),
        "biographical_period": "mid",
        "language_original": "grc",
        "fragment_languages": ["grc", "fra", "eng"],
        "place_of_writing": "Athènes, Jardin",
        "context_material": "post-Alexandre, hellénisme, école communautaire",
        "sources_read": [
            ("Démocrite", -300, "direct: atomisme repris et réformé"),
            ("Nausiphane", -310, "direct: maître démocritéen"),
            ("Aristote", -300, "indirect: critique"),
            ("Pyrrhon", -310, "indirect: ataraxie partagée"),
        ],
        "tradition_label": "GRECO_LAT_MATERIAL",
    },
    "lucretius_drn": {
        "author": "Titus Lucretius Carus",
        "author_lifespan": (-99, -55),
        "writing_year": -58,
        "writing_year_range": (-60, -55),
        "biographical_period": "mid",
        "language_original": "lat",
        "fragment_languages": ["lat", "fra", "eng"],
        "place_of_writing": "Rome",
        "context_material": "fin République romaine, guerres civiles, Cicéron contemporain",
        "sources_read": [
            ("Épicure", -58, "direct: maître absolu, transmission systématique"),
            ("Démocrite", -58, "indirect via Épicure"),
            ("Empédocle", -58, "direct: cité dans DRN I"),
            ("Ennius", -58, "direct: poète latin précurseur"),
        ],
        "tradition_label": "GRECO_LAT_MATERIAL",
    },
    "sextus_pyrrho": {
        "author": "Sextus Empiricus",
        "author_lifespan": (160, 210),
        "writing_year": 190,
        "writing_year_range": (180, 200),
        "biographical_period": "mid",
        "language_original": "grc",
        "fragment_languages": ["grc", "fra", "eng"],
        "place_of_writing": "Alexandrie ou Rome",
        "context_material": "Empire romain, koiné gréco-romaine, scepticisme tardif",
        "sources_read": [
            ("Pyrrhon", 190, "direct: école pyrrhonienne"),
            ("Énésidème", 190, "direct: scepticisme néo-pyrrhonien"),
            ("Agrippa", 190, "direct: 5 tropes"),
            ("Aristote", 190, "indirect: critique systématique"),
            ("Épicure", 190, "indirect: source matérialiste connue"),
        ],
        "tradition_label": "SCEPT",
    },
    "carvaka_fragments": {
        "author": "Cārvāka / Lokāyata (école)",
        "author_lifespan": (-600, 1200),  # tradition longue
        "writing_year": -300,
        "writing_year_range": (-600, 800),
        "biographical_period": "mid",
        "language_original": "san",
        "fragment_languages": ["san", "fra", "eng"],
        "place_of_writing": "Inde du Nord",
        "context_material": "Inde brahmanique, contre-tradition matérialiste anti-védique",
        "sources_read": [
            ("Tradition védique", -400, "indirect: rejet polémique"),
            ("Brhaspati", -500, "direct: fondateur légendaire"),
            ("Upaniṣads", -400, "indirect: critique"),
        ],
        "tradition_label": "INDIAN_MATERIAL",
    },
    "wang_chong_lunheng": {
        "author": "Wang Chong",
        "author_lifespan": (27, 100),
        "writing_year": 80,
        "writing_year_range": (70, 97),
        "biographical_period": "late",
        "language_original": "zho",
        "fragment_languages": ["zho", "fra", "eng"],
        "place_of_writing": "Han postérieur, Kuaiji",
        "context_material": "Chine Han, Confucéens dominants, taoïsme populaire, prophéties weishu",
        "sources_read": [
            ("Confucius", 80, "direct: critique respectueuse"),
            ("Mozi", 80, "indirect: rationalisme"),
            ("Sima Qian", 80, "direct: historiographie"),
            ("Han Fei", 80, "indirect: légisme"),
        ],
        "tradition_label": "CHINESE_MATERIAL",
    },
    "ibn_rawandi_fragments": {
        "author": "Ibn al-Rāwandī",
        "author_lifespan": (827, 911),
        "writing_year": 870,
        "writing_year_range": (860, 900),
        "biographical_period": "mid",
        "language_original": "ara",
        "fragment_languages": ["ara", "fra", "eng"],
        "place_of_writing": "Bagdad / Khurasan",
        "context_material": "Califat abbasside, Mu'tazila, falsifa naissante, transmission gréco-arabe",
        "sources_read": [
            ("Mu'tazilites", 870, "direct: école de formation puis rupture"),
            ("Aristote (ar.)", 870, "direct: traductions Hunayn"),
            ("Galien (ar.)", 870, "direct: traductions"),
            ("Démocrite (via doxographie ar.)", 870, "indirect: atomisme rapporté"),
            ("Sextus (via doxographie ar.)", 870, "indirect: scepticisme rapporté"),
        ],
        "tradition_label": "ISLAMIC_RATIONALIST",
    },
    "hume_dialogues": {
        "author": "David Hume",
        "author_lifespan": (1711, 1776),
        "writing_year": 1751,
        "writing_year_range": (1750, 1776),  # publication posthume
        "biographical_period": "mid",
        "language_original": "eng",
        "fragment_languages": ["eng", "fra"],
        "place_of_writing": "Édimbourg",
        "context_material": "Écosse presbytérienne, Lumières écossaises, Bayle/Spinoza diffusés",
        "sources_read": [
            ("Sextus Empiricus", 1751, "direct: traductions latines XVIᵉ"),
            ("Bayle (Pierre)", 1751, "direct: Dictionnaire critique"),
            ("Cicéron (De natura deorum)", 1751, "direct: scepticisme académicien"),
            ("Lucrèce", 1751, "direct: redécouverte humaniste"),
            ("Locke", 1751, "direct: empirisme"),
            ("Newton", 1751, "indirect: physique"),
        ],
        "tradition_label": "MODERN_WESTERN",
    },
    "holbach_systeme": {
        "author": "Paul-Henri Thiry, baron d'Holbach",
        "author_lifespan": (1723, 1789),
        "writing_year": 1770,
        "writing_year_range": (1768, 1772),
        "biographical_period": "mid",
        "language_original": "fra",
        "fragment_languages": ["fra", "eng"],
        "place_of_writing": "Paris",
        "context_material": "France pré-révolutionnaire, salon d'Holbach, Encyclopédie",
        "sources_read": [
            ("Lucrèce", 1770, "direct: matérialisme antique"),
            ("Spinoza", 1770, "direct: déterminisme"),
            ("La Mettrie", 1770, "direct: Homme machine"),
            ("Diderot", 1770, "direct: ami et collaborateur"),
            ("Hume", 1770, "direct: empirisme"),
            ("Hobbes", 1770, "direct: matérialisme politique"),
            ("Gassendi", 1770, "indirect: épicurisme christianisé renversé"),
        ],
        "tradition_label": "MODERN_WESTERN",
    },
    "feuerbach_wesen": {
        "author": "Ludwig Feuerbach",
        "author_lifespan": (1804, 1872),
        "writing_year": 1841,
        "writing_year_range": (1839, 1843),
        "biographical_period": "mid",
        "language_original": "deu",
        "fragment_languages": ["deu", "fra", "eng"],
        "place_of_writing": "Bruckberg, Bavière",
        "context_material": "Allemagne post-hégélienne, jeunes hégéliens, anthropologie nouvelle",
        "sources_read": [
            ("Hegel", 1841, "direct: maître renversé"),
            ("Spinoza", 1841, "direct: panthéisme"),
            ("Holbach", 1841, "direct: matérialisme français"),
            ("Hume", 1841, "indirect: scepticisme religieux"),
            ("Strauss (D.F.)", 1841, "direct: Vie de Jésus 1835"),
            ("Bauer (B.)", 1841, "direct: critique évangélique"),
        ],
        "tradition_label": "MODERN_WESTERN",
    },
}


def stat_summary(meta: dict) -> dict:
    """Statistiques globales."""
    n_works = len(meta)
    centuries = sorted({w["writing_year"] // 100 for w in meta.values()})
    langs = sorted({w["language_original"] for w in meta.values()})
    traditions = sorted({w["tradition_label"] for w in meta.values()})
    n_sources_total = sum(len(w["sources_read"]) for w in meta.values())
    avg_sources = n_sources_total / n_works
    span_years = max(w["writing_year"] for w in meta.values()) - min(w["writing_year"] for w in meta.values())
    return {
        "n_works": n_works,
        "writing_centuries": centuries,
        "languages": langs,
        "traditions": traditions,
        "n_sources_attested": n_sources_total,
        "avg_sources_per_work": round(avg_sources, 2),
        "span_years": span_years,
    }


def write_metadata(meta: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "v147",
        "step": "§147 — métadonnées œuvres + sources attestées",
        "summary": stat_summary(meta),
        "works": {
            wid: {
                **w,
                # tuples non sérialisables → listes
                "author_lifespan": list(w["author_lifespan"]),
                "writing_year_range": list(w["writing_year_range"]),
                "sources_read": [
                    {"name": n, "year_when_read": y, "channel": c}
                    for (n, y, c) in w["sources_read"]
                ],
            }
            for wid, w in meta.items()
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    write_metadata(WORKS)
    summary = stat_summary(WORKS)
    print(f"✓ §147 — métadonnées écrites : {OUT}")
    print(f"  œuvres = {summary['n_works']}")
    print(f"  langues originales = {summary['languages']}")
    print(f"  traditions = {summary['traditions']}")
    print(f"  sources attestées (total) = {summary['n_sources_attested']}  (moy {summary['avg_sources_per_work']}/œuvre)")
    print(f"  écart temporel = {summary['span_years']} ans (siècles {summary['writing_centuries']})")


if __name__ == "__main__":
    main()

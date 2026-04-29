#!/usr/bin/env python3
"""
§206o — Catalogue WESTERN_RATIONAL × modern (1789 → 1914), 70 œuvres.

Cellule contemporaine des orientalistes du canal §206c : Kant post-1789,
Idéalisme allemand (Fichte, Schelling, Hegel), Schopenhauer (premier pont
philosophique avec l'Inde via Upaniṣad d'Anquetil-Duperron), Marx (matérialisme
historique), Mill (utilitarisme), Comte (positivisme), Nietzsche (généalogie),
Frege (logicisme), Husserl (phénoménologie), pragmatistes américains.

Note : Marx, Mill, Comte, Bentham classés WESTERN_RATIONAL (rationalisme
critique-immanent) plutôt que WESTERN_RADICAL réservé aux ruptures plus
radicales du XXe siècle (école de Francfort, post-structuralisme).

Sources : Project Gutenberg, Wikisource, archive.org, Bennett Early Modern Texts.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_western_rational_modern_v206o.json"

WORKS = [
    # ── Kant post-1789
    ("kant_kritik_praktischen_vernunft", "Kritik der praktischen Vernunft", "Critique of Practical Reason", "deu", 1788, ["kantian"], "kant"),
    ("kant_kritik_urteilskraft", "Kritik der Urteilskraft", "Critique of Judgment", "deu", 1790, ["kantian", "aesthetics"], "kant"),
    ("kant_religion_grenzen", "Die Religion innerhalb der Grenzen der bloßen Vernunft", "Religion within the Bounds of Bare Reason", "deu", 1793, ["kantian", "religion"], "kant"),
    ("kant_zum_ewigen_frieden", "Zum ewigen Frieden", "Perpetual Peace", "deu", 1795, ["kantian", "politics"], "kant"),
    ("kant_metaphysik_sitten", "Die Metaphysik der Sitten", "The Metaphysics of Morals", "deu", 1797, ["kantian", "ethics"], "kant"),

    # ── Idéalisme allemand
    ("fichte_wissenschaftslehre", "Grundlage der gesamten Wissenschaftslehre", "Foundations of the Science of Knowledge", "deu", 1794, ["german_idealism"], "fichte"),
    ("fichte_bestimmung_menschen", "Die Bestimmung des Menschen", "The Vocation of Man", "deu", 1800, ["german_idealism"], "fichte"),
    ("fichte_reden_deutsche_nation", "Reden an die deutsche Nation", "Addresses to the German Nation", "deu", 1808, ["german_idealism", "politics"], "fichte"),
    ("schelling_system_transzendental", "System des transzendentalen Idealismus", "System of Transcendental Idealism", "deu", 1800, ["german_idealism"], "schelling"),
    ("schelling_ideen_philosophie_natur", "Ideen zu einer Philosophie der Natur", "Ideas for a Philosophy of Nature", "deu", 1797, ["german_idealism", "naturphilosophie"], "schelling"),
    ("schelling_freiheitsschrift", "Philosophische Untersuchungen über das Wesen der menschlichen Freiheit", "Of Human Freedom", "deu", 1809, ["german_idealism"], "schelling"),
    ("hegel_phaenomenologie_geistes", "Phänomenologie des Geistes", "Phenomenology of Spirit", "deu", 1807, ["german_idealism", "hegelian"], "hegel"),
    ("hegel_wissenschaft_logik", "Wissenschaft der Logik", "Science of Logic", "deu", 1816, ["german_idealism", "hegelian"], "hegel"),
    ("hegel_enzyklopaedie", "Enzyklopädie der philosophischen Wissenschaften im Grundrisse", "Encyclopedia of the Philosophical Sciences", "deu", 1830, ["german_idealism", "hegelian"], "hegel"),
    ("hegel_grundlinien_rechts", "Grundlinien der Philosophie des Rechts", "Elements of the Philosophy of Right", "deu", 1820, ["german_idealism", "hegelian", "politics"], "hegel"),
    ("hegel_vorlesungen_geschichte_philosophie", "Vorlesungen über die Geschichte der Philosophie", "Lectures on the History of Philosophy", "deu", 1837, ["german_idealism", "hegelian"], "hegel"),

    # ── Schopenhauer (pont vers l'Inde)
    ("schopenhauer_welt_als_wille", "Die Welt als Wille und Vorstellung", "The World as Will and Representation", "deu", 1819, ["pessimist", "indophile"], "schopenhauer"),
    ("schopenhauer_parerga", "Parerga und Paralipomena", "Parerga and Paralipomena", "deu", 1851, ["pessimist", "indophile"], "schopenhauer"),
    ("schopenhauer_ueber_grundlage_moral", "Über die Grundlage der Moral", "On the Basis of Morality", "deu", 1840, ["pessimist", "ethics"], "schopenhauer"),
    ("schopenhauer_vierfache_wurzel", "Über die vierfache Wurzel des Satzes vom zureichenden Grunde", "On the Fourfold Root", "deu", 1813, ["pessimist", "epistemology"], "schopenhauer"),

    # ── Empirisme et utilitarisme
    ("bentham_introduction_morals", "An Introduction to the Principles of Morals and Legislation", "Introduction to the Principles of Morals and Legislation", "eng", 1789, ["utilitarian"], "bentham"),
    ("mill_system_logic", "A System of Logic, Ratiocinative and Inductive", "A System of Logic", "eng", 1843, ["utilitarian", "empiricist", "logic"], "john_stuart_mill"),
    ("mill_principles_political_economy", "Principles of Political Economy", "Principles of Political Economy", "eng", 1848, ["utilitarian", "economics"], "john_stuart_mill"),
    ("mill_on_liberty", "On Liberty", "On Liberty", "eng", 1859, ["utilitarian", "politics"], "john_stuart_mill"),
    ("mill_utilitarianism", "Utilitarianism", "Utilitarianism", "eng", 1863, ["utilitarian", "ethics"], "john_stuart_mill"),
    ("mill_subjection_women", "The Subjection of Women", "The Subjection of Women", "eng", 1869, ["utilitarian", "feminism"], "john_stuart_mill"),
    ("spencer_principles_psychology", "The Principles of Psychology", "Principles of Psychology", "eng", 1855, ["evolutionist"], "herbert_spencer"),

    # ── Positivisme et sciences sociales
    ("comte_cours_philosophie_positive", "Cours de philosophie positive", "Course of Positive Philosophy", "frm", 1842, ["positivist"], "auguste_comte"),
    ("comte_systeme_politique_positive", "Système de politique positive", "System of Positive Polity", "frm", 1854, ["positivist", "politics"], "auguste_comte"),
    ("durkheim_division_travail", "De la division du travail social", "The Division of Labor in Society", "frm", 1893, ["positivist", "sociology"], "durkheim"),
    ("durkheim_regles_methode", "Les Règles de la méthode sociologique", "Rules of Sociological Method", "frm", 1895, ["positivist", "sociology"], "durkheim"),
    ("durkheim_suicide", "Le Suicide", "Suicide", "frm", 1897, ["positivist", "sociology"], "durkheim"),
    ("durkheim_formes_elementaires", "Les Formes élémentaires de la vie religieuse", "Elementary Forms of Religious Life", "frm", 1912, ["positivist", "sociology", "religion"], "durkheim"),
    ("weber_protestant_ethic", "Die protestantische Ethik und der Geist des Kapitalismus", "The Protestant Ethic and the Spirit of Capitalism", "deu", 1905, ["sociology"], "max_weber"),

    # ── Marx & socialisme critique
    ("marx_manifest", "Manifest der Kommunistischen Partei", "The Communist Manifesto", "deu", 1848, ["materialist_dialectical", "politics"], "marx_engels"),
    ("marx_kapital", "Das Kapital, Kritik der politischen Ökonomie", "Capital, Critique of Political Economy", "deu", 1867, ["materialist_dialectical", "economics"], "marx"),
    ("marx_grundrisse", "Grundrisse der Kritik der politischen Ökonomie", "Grundrisse", "deu", 1858, ["materialist_dialectical", "economics"], "marx"),
    ("marx_pariser_manuskripte", "Ökonomisch-philosophische Manuskripte aus dem Jahre 1844", "Economic and Philosophic Manuscripts of 1844", "deu", 1844, ["materialist_dialectical"], "marx"),
    ("marx_thesen_feuerbach", "Thesen über Feuerbach", "Theses on Feuerbach", "deu", 1845, ["materialist_dialectical"], "marx"),
    ("marx_deutsche_ideologie", "Die deutsche Ideologie", "The German Ideology", "deu", 1846, ["materialist_dialectical"], "marx_engels"),
    ("engels_anti_duehring", "Herrn Eugen Dührings Umwälzung der Wissenschaft", "Anti-Dühring", "deu", 1878, ["materialist_dialectical"], "engels"),

    # ── Nietzsche & critique de la moralité
    ("nietzsche_geburt_tragoedie", "Die Geburt der Tragödie", "The Birth of Tragedy", "deu", 1872, ["genealogical"], "nietzsche"),
    ("nietzsche_unzeitgemaesse", "Unzeitgemäße Betrachtungen", "Untimely Meditations", "deu", 1876, ["genealogical"], "nietzsche"),
    ("nietzsche_menschliches", "Menschliches, Allzumenschliches", "Human, All Too Human", "deu", 1878, ["genealogical"], "nietzsche"),
    ("nietzsche_morgenroete", "Morgenröte", "Daybreak", "deu", 1881, ["genealogical"], "nietzsche"),
    ("nietzsche_froehliche_wissenschaft", "Die fröhliche Wissenschaft", "The Gay Science", "deu", 1882, ["genealogical"], "nietzsche"),
    ("nietzsche_zarathustra", "Also sprach Zarathustra", "Thus Spoke Zarathustra", "deu", 1885, ["genealogical"], "nietzsche"),
    ("nietzsche_jenseits_gut_boese", "Jenseits von Gut und Böse", "Beyond Good and Evil", "deu", 1886, ["genealogical"], "nietzsche"),
    ("nietzsche_genealogie", "Zur Genealogie der Moral", "On the Genealogy of Morals", "deu", 1887, ["genealogical"], "nietzsche"),

    # ── Kierkegaard & existence (proto-existentialiste)
    ("kierkegaard_entweder_oder", "Enten-Eller", "Either/Or", "dan", 1843, ["existentialist_proto"], "kierkegaard"),
    ("kierkegaard_furcht_zittern", "Frygt og Bæven", "Fear and Trembling", "dan", 1843, ["existentialist_proto"], "kierkegaard"),
    ("kierkegaard_unwissenschaftliche_nachschrift", "Afsluttende uvidenskabelig Efterskrift", "Concluding Unscientific Postscript", "dan", 1846, ["existentialist_proto"], "kierkegaard"),
    ("kierkegaard_krankheit_zum_tode", "Sygdommen til Døden", "The Sickness Unto Death", "dan", 1849, ["existentialist_proto"], "kierkegaard"),

    # ── Logique et philosophie analytique précoce
    ("frege_begriffsschrift", "Begriffsschrift", "Begriffsschrift", "deu", 1879, ["analytic_proto", "logic"], "frege"),
    ("frege_grundlagen_arithmetik", "Die Grundlagen der Arithmetik", "Foundations of Arithmetic", "deu", 1884, ["analytic_proto", "logic"], "frege"),
    ("frege_grundgesetze", "Grundgesetze der Arithmetik", "Basic Laws of Arithmetic", "deu", 1903, ["analytic_proto", "logic"], "frege"),
    ("russell_principles_mathematics", "The Principles of Mathematics", "The Principles of Mathematics", "eng", 1903, ["analytic_proto", "logic"], "russell"),
    ("whitehead_russell_principia", "Principia Mathematica", "Principia Mathematica", "eng", 1913, ["analytic_proto", "logic"], "whitehead_russell"),
    ("moore_principia_ethica", "Principia Ethica", "Principia Ethica", "eng", 1903, ["analytic_proto", "ethics"], "george_edward_moore"),

    # ── Phénoménologie
    ("husserl_logische_untersuchungen", "Logische Untersuchungen", "Logical Investigations", "deu", 1900, ["phenomenology"], "husserl"),
    ("husserl_ideen_phaenomenologie", "Ideen zu einer reinen Phänomenologie", "Ideas Pertaining to a Pure Phenomenology", "deu", 1913, ["phenomenology"], "husserl"),
    ("brentano_psychologie_empirischen", "Psychologie vom empirischen Standpunkte", "Psychology from an Empirical Standpoint", "deu", 1874, ["phenomenology", "psychology"], "brentano"),

    # ── Vitalisme & process
    ("bergson_essai_donnees", "Essai sur les données immédiates de la conscience", "Time and Free Will", "frm", 1889, ["vitalism"], "bergson"),
    ("bergson_evolution_creatrice", "L'Évolution créatrice", "Creative Evolution", "frm", 1907, ["vitalism"], "bergson"),
    ("bergson_matiere_memoire", "Matière et mémoire", "Matter and Memory", "frm", 1896, ["vitalism", "psychology"], "bergson"),

    # ── Pragmatistes américains
    ("peirce_collected_papers", "How to Make Our Ideas Clear", "How to Make Our Ideas Clear (1878 + Collected Papers)", "eng", 1878, ["pragmatist"], "peirce"),
    ("james_principles_psychology", "The Principles of Psychology", "Principles of Psychology", "eng", 1890, ["pragmatist", "psychology"], "william_james"),
    ("james_varieties_religious_experience", "The Varieties of Religious Experience", "Varieties of Religious Experience", "eng", 1902, ["pragmatist", "religion"], "william_james"),
    ("james_pragmatism", "Pragmatism: A New Name for Some Old Ways of Thinking", "Pragmatism", "eng", 1907, ["pragmatist"], "william_james"),
    ("dewey_school_society", "The School and Society", "The School and Society", "eng", 1899, ["pragmatist", "education"], "john_dewey"),
]

assert len(WORKS) == 70, f"WESTERN_RATIONAL×modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "kantian" in tags:
        return "KANTIAN_LATE"
    if "german_idealism" in tags:
        return "GERMAN_IDEALISM"
    if "pessimist" in tags and "indophile" in tags:
        return "SCHOPENHAUERIAN_INDOPHILE"
    if "pessimist" in tags:
        return "SCHOPENHAUERIAN"
    if "utilitarian" in tags:
        return "UTILITARIAN"
    if "evolutionist" in tags:
        return "EVOLUTIONIST"
    if "positivist" in tags and "sociology" in tags:
        return "POSITIVIST_SOCIOLOGY"
    if "positivist" in tags:
        return "POSITIVIST"
    if "sociology" in tags:
        return "SOCIOLOGY"
    if "materialist_dialectical" in tags:
        return "MARXIST"
    if "genealogical" in tags:
        return "NIETZSCHEAN"
    if "existentialist_proto" in tags:
        return "EXISTENTIALIST_PROTO"
    if "analytic_proto" in tags:
        return "ANALYTIC_PROTO"
    if "phenomenology" in tags:
        return "PHENOMENOLOGY"
    if "vitalism" in tags:
        return "VITALIST_PROCESS"
    if "pragmatist" in tags:
        return "PRAGMATIST"
    return "MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "WESTERN_RATIONAL",
            "epoch": "modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 3,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206o_western_rational_modern",
        "generated": "2026-04-29",
        "macro_culture": "WESTERN_RATIONAL",
        "epoch": "modern",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["Project Gutenberg", "Wikisource (de/fr/en/da)", "archive.org", "MEW (Marx-Engels-Werke)", "Husserliana"],
        "language_original_dominant": "deu + eng + frm + dan",
        "schools_covered": [
            "Kant post-1789 (KprV+KU+Religion+Frieden+Metaphysik Sitten)",
            "Idéalisme allemand (Fichte ×3, Schelling ×3, Hegel ×5)",
            "Schopenhauer ×4 (premier pont indien-occidental)",
            "Bentham + Mill ×5 + Spencer ×2 (utilitarisme + évolutionnisme)",
            "Comte ×2 + Durkheim ×4 + Weber (positivisme + sociologie)",
            "Marx ×5 + Engels ×2 (matérialisme dialectique)",
            "Nietzsche ×8 (corpus complet pré-effondrement)",
            "Kierkegaard ×4 (existentialisme proto)",
            "Frege ×3 + Russell + Whitehead-Russell + Moore (analytique proto)",
            "Husserl ×2 + Brentano (phénoménologie)",
            "Bergson ×3 (vitalisme/durée)",
            "Peirce + James ×3 + Dewey (pragmatisme américain)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue WESTERN_RATIONAL × modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

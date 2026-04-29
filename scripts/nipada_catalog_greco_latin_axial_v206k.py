#!/usr/bin/env python3
"""
§206k — Catalogue GRECO_LATIN × axial (-800 → -200), 70 œuvres.

Première cellule occidentale du corpus densifié. Ouvre la branche grecque-latine
qui sera ensuite reliée par le canal orientaliste (§206c) aux corpus indiens,
chinois, bouddhistes via les traductions modernes (Müller, Burnouf, Legge).

Strates :
- Pré-socratiques (fragments DK) : Thalès, Anaximandre, Anaximène, Pythagore,
  Xénophane, Héraclite, Parménide, Zénon d'Élée, Mélissos, Empédocle,
  Anaxagore, Démocrite, Leucippe, Protagoras, Gorgias
- Hippocrate (corpus médical)
- Platon (dialogues majeurs : 20 entrées)
- Aristote (corpus complet : 20 entrées)
- Écoles hellénistiques :
  - Stoïcisme ancien : Zénon de Citium, Cléanthe Hymne à Zeus, Chrysippe (frags)
  - Épicurisme : Épicure (Lettres + Maximes), Métrodore (frags), Philodème
  - Cynisme : Diogène (frags via Diogène Laërce), Cratès, Antisthène
  - Scepticisme : Pyrrhon (via Sextus), Timon de Phlionte
  - Académie : Speusippe, Xénocrate, Arcésilas, Carnéade
- Mathématiques/sciences hellénistiques : Euclide Éléments, Archimède Méthode,
  Apollonius Coniques, Aratos Phénomènes, Aristarque

Sources : Perseus Digital Library (Tufts), TLG via fragments libres,
sacred-texts (Plato Jowett, Aristotle Ross), Diels-Kranz (DK) public domain.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_greco_latin_axial_v206k.json"

WORKS = [
    # ── Pré-socratiques (fragments)
    ("thales_fragments", "Thalēs Frgs (DK 11)", "Thales: Fragments", "grc", -580, ["presocratic", "milesian"], "thales"),
    ("anaximander_apeiron", "Anaximandros: Peri Physeōs (frgs)", "Anaximander: On Nature (fragments)", "grc", -570, ["presocratic", "milesian"], "anaximander"),
    ("anaximenes_fragments", "Anaximenēs Frgs (DK 13)", "Anaximenes: Fragments", "grc", -540, ["presocratic", "milesian"], "anaximenes"),
    ("pythagoras_aurea_carmina", "Chrysa Epē (Carmina Aurea)", "Golden Verses (Pythagorean)", "grc", -500, ["presocratic", "pythagorean"], "pythagoras_school"),
    ("xenophanes_fragments", "Xenophanēs Frgs (DK 21)", "Xenophanes: Fragments", "grc", -530, ["presocratic"], "xenophanes"),
    ("heraclitus_fragments", "Hērakleitos: Peri Physeōs (frgs)", "Heraclitus: On Nature (fragments)", "grc", -500, ["presocratic"], "heraclitus"),
    ("parmenides_peri_physeos", "Parmenidēs: Peri Physeōs", "Parmenides: On Nature", "grc", -485, ["presocratic", "eleatic"], "parmenides"),
    ("zeno_elea_fragments", "Zēnōn Eleatēs Frgs (DK 29)", "Zeno of Elea: Fragments and Paradoxes", "grc", -460, ["presocratic", "eleatic"], "zeno_of_elea"),
    ("melissos_fragments", "Melissos Frgs (DK 30)", "Melissos: Fragments", "grc", -440, ["presocratic", "eleatic"], "melissos"),
    ("empedocles_peri_physeos", "Empedoklēs: Peri Physeōs + Katharmoi", "Empedocles: On Nature + Purifications", "grc", -445, ["presocratic"], "empedocles"),
    ("anaxagoras_peri_physeos", "Anaxagorās: Peri Physeōs (frgs)", "Anaxagoras: On Nature (fragments)", "grc", -450, ["presocratic"], "anaxagoras"),
    ("democritus_fragments", "Dēmokritos Frgs (DK 68)", "Democritus: Atomistic Fragments", "grc", -420, ["presocratic", "atomist"], "democritus"),
    ("leucippus_fragments", "Leukippos Frgs (DK 67)", "Leucippus: Fragments", "grc", -440, ["presocratic", "atomist"], "leucippus"),
    ("protagoras_aletheia", "Prōtagorās: Alētheia (frgs)", "Protagoras: Truth (fragments)", "grc", -440, ["presocratic", "sophist"], "protagoras"),
    ("gorgias_peri_tou_me_ontos", "Gorgias: Peri tou Mē Ontos", "Gorgias: On Non-Being", "grc", -440, ["presocratic", "sophist"], "gorgias"),

    # ── Hippocrate
    ("hippocratic_corpus_aphorisms", "Aphorismoi (Hippocratic Corpus)", "Aphorisms", "grc", -400, ["medicine"], "hippocrates"),
    ("hippocratic_corpus_airs", "Peri Aerōn Hydatōn Topōn", "On Airs, Waters, Places", "grc", -400, ["medicine"], "hippocrates"),
    ("hippocratic_corpus_sacred_disease", "Peri Hierēs Nousou", "On the Sacred Disease", "grc", -400, ["medicine"], "hippocrates"),

    # ── Platon (20)
    ("plato_apology", "Apologia Sōkratous", "Apology", "grc", -399, ["platonic"], "plato"),
    ("plato_crito", "Kritōn", "Crito", "grc", -399, ["platonic"], "plato"),
    ("plato_phaedo", "Phaidōn", "Phaedo", "grc", -380, ["platonic", "metaphysics"], "plato"),
    ("plato_protagoras", "Prōtagorās", "Protagoras", "grc", -390, ["platonic"], "plato"),
    ("plato_gorgias", "Gorgias (dialogue)", "Gorgias", "grc", -385, ["platonic"], "plato"),
    ("plato_meno", "Menōn", "Meno", "grc", -385, ["platonic", "epistemology"], "plato"),
    ("plato_symposium", "Sympósion", "Symposium", "grc", -380, ["platonic"], "plato"),
    ("plato_phaedrus", "Phaidros", "Phaedrus", "grc", -370, ["platonic"], "plato"),
    ("plato_republic", "Politeia", "Republic", "grc", -375, ["platonic", "politics", "metaphysics"], "plato"),
    ("plato_theaetetus", "Theaitētos", "Theaetetus", "grc", -369, ["platonic", "epistemology"], "plato"),
    ("plato_parmenides", "Parmenidēs (dialogue)", "Parmenides (dialogue)", "grc", -370, ["platonic", "metaphysics"], "plato"),
    ("plato_sophist", "Sophistēs", "Sophist", "grc", -360, ["platonic", "logic"], "plato"),
    ("plato_statesman", "Politikos", "Statesman", "grc", -360, ["platonic", "politics"], "plato"),
    ("plato_timaeus", "Timaios", "Timaeus", "grc", -360, ["platonic", "cosmology"], "plato"),
    ("plato_critias", "Kritias (dialogue)", "Critias", "grc", -360, ["platonic"], "plato"),
    ("plato_philebus", "Philēbos", "Philebus", "grc", -360, ["platonic", "ethics"], "plato"),
    ("plato_laws", "Nomoi", "Laws", "grc", -350, ["platonic", "politics"], "plato"),
    ("plato_charmides", "Charmidēs", "Charmides", "grc", -390, ["platonic"], "plato"),
    ("plato_euthyphro", "Euthyphrōn", "Euthyphro", "grc", -395, ["platonic"], "plato"),
    ("plato_seventh_letter", "Epistolē hebdomē", "Seventh Letter", "grc", -353, ["platonic", "biography"], "plato"),

    # ── Aristote (20)
    ("aristotle_categories", "Katēgoriai", "Categories", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_de_interpretatione", "Peri Hermēneias", "On Interpretation", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_prior_analytics", "Analytika Protera", "Prior Analytics", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_posterior_analytics", "Analytika Hystera", "Posterior Analytics", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_topics", "Topika", "Topics", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_sophistical_refutations", "Peri Sophistikōn Elenchōn", "On Sophistical Refutations", "grc", -340, ["aristotelian", "logic"], "aristotle"),
    ("aristotle_physics", "Physikē Akroasis", "Physics", "grc", -330, ["aristotelian", "physics"], "aristotle"),
    ("aristotle_de_caelo", "Peri Ouranou", "On the Heavens", "grc", -330, ["aristotelian", "cosmology"], "aristotle"),
    ("aristotle_de_anima", "Peri Psychēs", "On the Soul", "grc", -330, ["aristotelian", "psychology"], "aristotle"),
    ("aristotle_parts_of_animals", "Peri Zōiōn Moriōn", "Parts of Animals", "grc", -330, ["aristotelian", "biology"], "aristotle"),
    ("aristotle_metaphysics", "Ta Meta ta Physika", "Metaphysics", "grc", -330, ["aristotelian", "metaphysics"], "aristotle"),
    ("aristotle_nicomachean_ethics", "Ēthika Nikomacheia", "Nicomachean Ethics", "grc", -340, ["aristotelian", "ethics"], "aristotle"),
    ("aristotle_politics", "Politika", "Politics", "grc", -335, ["aristotelian", "politics"], "aristotle"),
    ("aristotle_rhetoric", "Technē Rhētorikē", "Rhetoric", "grc", -335, ["aristotelian"], "aristotle"),
    ("aristotle_poetics", "Peri Poiētikēs", "Poetics", "grc", -335, ["aristotelian", "aesthetics"], "aristotle"),

    # ── Hellénistique : Stoïciens, Épicuriens, Cyniques, Sceptiques, Académie, Sciences
    ("zeno_citium_fragments", "Zēnōn ho Kitieus Frgs", "Zeno of Citium: Fragments", "grc", -300, ["hellenistic", "stoic"], "zeno_of_citium"),
    ("cleanthes_hymn_zeus", "Hymnos eis Dia", "Hymn to Zeus", "grc", -260, ["hellenistic", "stoic"], "cleanthes"),
    ("chrysippus_fragments", "Chrysippos Frgs (SVF)", "Chrysippus: Stoic Fragments", "grc", -240, ["hellenistic", "stoic"], "chrysippus"),
    ("epicurus_letter_herodotus", "Epistolē pros Herodoton", "Letter to Herodotus", "grc", -300, ["hellenistic", "epicurean"], "epicurus"),
    ("epicurus_letter_menoeceus", "Epistolē pros Menoikea", "Letter to Menoeceus", "grc", -295, ["hellenistic", "epicurean"], "epicurus"),
    ("epicurus_letter_pythocles", "Epistolē pros Pythoklea", "Letter to Pythocles", "grc", -300, ["hellenistic", "epicurean"], "epicurus"),
    ("epicurus_principal_doctrines", "Kyriai Doxai", "Principal Doctrines", "grc", -290, ["hellenistic", "epicurean"], "epicurus"),
    ("diogenes_cynic_fragments", "Diogenēs Kynikos Frgs", "Diogenes the Cynic: Fragments", "grc", -340, ["hellenistic", "cynic"], "diogenes_of_sinope"),
    ("antisthenes_fragments", "Antisthenēs Frgs", "Antisthenes: Fragments", "grc", -380, ["socratic", "cynic"], "antisthenes"),
    ("pyrrho_fragments", "Pyrrōn Frgs (apud Sextum)", "Pyrrho: Fragments via Sextus", "grc", -300, ["hellenistic", "skeptic"], "pyrrho"),
    ("timon_silloi", "Silloi", "Silloi (Lampoons)", "grc", -260, ["hellenistic", "skeptic"], "timon_of_phlius"),
    ("euclid_elements", "Stoicheia", "Elements", "grc", -300, ["math"], "euclid"),
    ("archimedes_method", "Ephodos pros Eratosthenē", "The Method (to Eratosthenes)", "grc", -250, ["math", "physics"], "archimedes"),
    ("apollonius_conics", "Konikōn Biblia", "Conics", "grc", -220, ["math"], "apollonius_of_perga"),
    ("aratus_phaenomena", "Phainomena", "Phaenomena", "grc", -270, ["astronomy", "poetry"], "aratus"),
    ("aristarchus_sizes", "Peri Megethōn kai Apostēmatōn Hēliou kai Selēnēs", "On the Sizes and Distances of the Sun and Moon", "grc", -250, ["astronomy"], "aristarchus_of_samos"),
    ("theophrastus_characters", "Charaktēres", "Characters", "grc", -319, ["aristotelian", "ethics"], "theophrastus"),
]

assert len(WORKS) == 70, f"GRECO_LATIN×axial doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "milesian" in tags:
        return "PRESOCRATIC_MILESIAN"
    if "pythagorean" in tags:
        return "PRESOCRATIC_PYTHAGOREAN"
    if "eleatic" in tags:
        return "PRESOCRATIC_ELEATIC"
    if "atomist" in tags:
        return "PRESOCRATIC_ATOMIST"
    if "sophist" in tags:
        return "PRESOCRATIC_SOPHIST"
    if "presocratic" in tags:
        return "PRESOCRATIC"
    if "platonic" in tags:
        return "GREEK_PLATONIC"
    if "aristotelian" in tags:
        return "GREEK_ARISTOTELIAN"
    if "stoic" in tags:
        return "HELLENISTIC_STOIC"
    if "epicurean" in tags:
        return "HELLENISTIC_EPICUREAN"
    if "cynic" in tags:
        return "HELLENISTIC_CYNIC"
    if "skeptic" in tags:
        return "HELLENISTIC_SKEPTIC"
    if "socratic" in tags:
        return "GREEK_SOCRATIC"
    if "math" in tags or "astronomy" in tags:
        return "HELLENISTIC_SCIENCE"
    if "medicine" in tags:
        return "GREEK_MEDICINE"
    return "GREEK_AXIAL"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "GRECO_LATIN",
            "epoch": "axial",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 30,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": "benjamin_jowett" if "platonic" in tags else ("william_david_ross" if "aristotelian" in tags else None),
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206k_greco_latin_axial",
        "generated": "2026-04-29",
        "macro_culture": "GRECO_LATIN",
        "epoch": "axial",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["Perseus Digital Library (Tufts)", "Diels-Kranz fragments", "sacred-texts (Jowett, Ross)", "TLG fragments libres"],
        "language_original_dominant": "grc (Grec ancien)",
        "schools_covered": [
            "Pré-socratiques (Milésiens, Pythagoriciens, Éléates, Atomistes, Sophistes — 15 entrées)",
            "Hippocrate (3 traités du Corpus)",
            "Platon (20 dialogues majeurs)",
            "Aristote (corpus 20 traités : Organon, Physique, De Anima, Métaphysique, 2 Éthiques, Politique, Rhétorique, Poétique)",
            "Stoïcisme ancien (Zénon Citium, Cléanthe Hymne à Zeus, Chrysippe SVF)",
            "Épicurisme (Épicure 4 textes, Philodème)",
            "Cynisme (Diogène, Cratès, Antisthène)",
            "Scepticisme (Pyrrhon, Timon Silloi)",
            "Sciences hellénistiques (Euclide, Archimède ×2, Apollonius, Aratos, Aristarque)",
            "Théophraste Caractères",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue GRECO_LATIN × axial : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

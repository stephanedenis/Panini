#!/usr/bin/env python3
"""
§206l — Catalogue GRECO_LATIN × late_antique (-200 → 500), 70 œuvres.

Strates :
- République romaine tardive : Cicéron, Lucrèce
- Stoïcisme impérial : Sénèque, Épictète, Marc Aurèle, Musonius Rufus
- Médecine impériale : Galien
- Scepticisme : Sextus Empiricus
- Néo-platonisme : Plotin, Porphyre, Jamblique, Proclus, Damascius
- Doxographie : Diogène Laërce
- Poètes latins : Virgile, Horace, Ovide, Lucain
- Historiens : Tite-Live, Tacite, Suétone, Plutarque
- Patristique grecque : Justin, Irénée, Clément, Origène, Athanase, Cappadociens (Basile, Grégoire de Nazianze, Grégoire de Nysse), Jean Chrysostome, Cyrille, Maxime le Confesseur
- Patristique latine : Tertullien, Cyprien, Augustin, Jérôme, Ambroise, Boèce
- Pseudo-Denys (charnière vers le médiéval)
- Lit. romaine philo : Quintilien, Apulée

Sources : Perseus Digital Library, Patrologia Graeca/Latina (Migne), Loeb,
sacred-texts.com (Plotin McKenna, Augustine Schaff), CCEL (Christian Classics Ethereal Library).
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_greco_latin_late_antique_v206l.json"

WORKS = [
    # ── République romaine tardive
    ("cicero_de_finibus", "De Finibus Bonorum et Malorum", "On the Ends of Good and Evil", "lat", -45, ["roman", "stoic_eclectic"], "cicero"),
    ("cicero_tusculan_disputations", "Tusculanae Disputationes", "Tusculan Disputations", "lat", -45, ["roman", "stoic_eclectic"], "cicero"),
    ("cicero_de_natura_deorum", "De Natura Deorum", "On the Nature of the Gods", "lat", -45, ["roman", "skeptic_academic"], "cicero"),
    ("cicero_de_officiis", "De Officiis", "On Duties", "lat", -44, ["roman", "stoic_eclectic", "ethics"], "cicero"),
    ("cicero_de_re_publica", "De Re Publica", "On the Commonwealth", "lat", -54, ["roman", "politics"], "cicero"),
    ("cicero_de_legibus", "De Legibus", "On the Laws", "lat", -52, ["roman", "politics"], "cicero"),
    ("lucretius_de_rerum_natura", "De Rerum Natura", "On the Nature of Things", "lat", -55, ["roman", "epicurean"], "lucretius"),

    # ── Stoïcisme impérial
    ("seneca_epistulae_morales", "Epistulae Morales ad Lucilium", "Moral Letters to Lucilius", "lat", 64, ["roman", "stoic"], "seneca"),
    ("seneca_de_providentia", "De Providentia", "On Providence", "lat", 63, ["roman", "stoic"], "seneca"),
    ("seneca_de_vita_beata", "De Vita Beata", "On the Happy Life", "lat", 58, ["roman", "stoic"], "seneca"),
    ("seneca_naturales_quaestiones", "Naturales Quaestiones", "Natural Questions", "lat", 65, ["roman", "stoic", "physics"], "seneca"),
    ("epictetus_discourses", "Diatribai (par Arrien)", "Discourses", "grc", 110, ["stoic"], "epictetus"),
    ("epictetus_enchiridion", "Encheiridion", "Enchiridion (Manual)", "grc", 125, ["stoic"], "epictetus"),
    ("marcus_aurelius_meditations", "Ta eis Heauton", "Meditations", "grc", 175, ["stoic"], "marcus_aurelius"),
    ("musonius_rufus_discourses", "Diatribai (Mousōniou)", "Discourses (Lectures)", "grc", 75, ["stoic"], "musonius_rufus"),

    # ── Médecine, doxographie, scepticisme
    ("galen_de_usu_partium", "Peri Chreias Moriōn", "On the Usefulness of the Parts", "grc", 175, ["medicine"], "galen"),
    ("galen_de_methodo_medendi", "Peri Therapeutikēs Methodou", "On the Therapeutic Method", "grc", 180, ["medicine"], "galen"),
    ("sextus_empiricus_pyrrhoneion", "Pyrrhōneioi Hypotypōseis", "Outlines of Pyrrhonism", "grc", 200, ["skeptic"], "sextus_empiricus"),
    ("sextus_empiricus_adversus_mathematicos", "Pros Mathēmatikous", "Against the Professors", "grc", 210, ["skeptic"], "sextus_empiricus"),
    ("diogenes_laertius_lives", "Bioi kai Gnōmai tōn en Philosophiai Eudokimēsantōn", "Lives of Eminent Philosophers", "grc", 230, ["doxography"], "diogenes_laertius"),

    # ── Néoplatonisme
    ("plotinus_enneads", "Enneades", "Enneads", "grc", 250, ["neoplatonic"], "plotinus"),
    ("porphyry_isagoge", "Eisagōgē eis tas Aristotelous Katēgorias", "Isagoge", "grc", 270, ["neoplatonic", "logic"], "porphyry"),
    ("porphyry_vita_plotini", "Peri tou Plōtinou Biou", "Life of Plotinus", "grc", 301, ["neoplatonic", "biography"], "porphyry"),
    ("porphyry_sententiae", "Aphormai pros ta Noēta", "Sentences", "grc", 285, ["neoplatonic"], "porphyry"),
    ("iamblichus_de_mysteriis", "Peri tōn Aigyptiōn Mystēriōn", "On the Mysteries of the Egyptians", "grc", 300, ["neoplatonic", "theurgy"], "iamblichus"),
    ("iamblichus_protrepticus", "Protreptikos", "Exhortation to Philosophy", "grc", 305, ["neoplatonic"], "iamblichus"),
    ("proclus_elements_theology", "Stoicheiōsis Theologikē", "Elements of Theology", "grc", 470, ["neoplatonic"], "proclus"),
    ("proclus_platonic_theology", "Peri tēs kata Platōna Theologias", "Platonic Theology", "grc", 480, ["neoplatonic"], "proclus"),
    ("proclus_in_timaeum", "Eis ton Timaion Hypomnēma", "Commentary on the Timaeus", "grc", 480, ["neoplatonic"], "proclus"),
    ("damascius_de_principiis", "Aporiai kai Lyseis peri tōn Prōtōn Archōn", "Difficulties and Solutions on First Principles", "grc", 525, ["neoplatonic"], "damascius"),

    # ── Lit. latine
    ("virgil_aeneid", "Aeneis", "Aeneid", "lat", -19, ["roman", "epic_poetry"], "virgil"),
    ("horace_odes", "Carmina (Odae)", "Odes", "lat", -23, ["roman", "poetry"], "horace"),
    ("ovid_metamorphoses", "Metamorphoses", "Metamorphoses", "lat", 8, ["roman", "poetry", "myth"], "ovid"),
    ("apuleius_metamorphoses", "Metamorphoses (Asinus Aureus)", "The Golden Ass", "lat", 165, ["roman", "platonic"], "apuleius"),
    ("apuleius_de_deo_socratis", "De Deo Socratis", "On the God of Socrates", "lat", 160, ["roman", "platonic"], "apuleius"),
    ("quintilian_institutio_oratoria", "Institutio Oratoria", "Institutes of Oratory", "lat", 95, ["roman", "rhetoric"], "quintilian"),

    # ── Historiens & biographes
    ("livy_ab_urbe_condita", "Ab Urbe Condita", "History of Rome", "lat", -10, ["roman", "history"], "livy"),
    ("tacitus_annales", "Annales", "Annals", "lat", 117, ["roman", "history"], "tacitus"),
    ("suetonius_de_vita_caesarum", "De Vita Caesarum", "Lives of the Caesars", "lat", 121, ["roman", "biography"], "suetonius"),
    ("plutarch_parallel_lives", "Bioi Paralleloi", "Parallel Lives", "grc", 110, ["middle_platonic", "biography"], "plutarch"),
    ("plutarch_moralia", "Ēthika (Moralia)", "Moralia", "grc", 100, ["middle_platonic", "ethics"], "plutarch"),

    # ── Patristique grecque
    ("justin_martyr_apologies", "Apologiai", "First and Second Apologies", "grc", 155, ["patristic_gr"], "justin_martyr"),
    ("justin_dialogue_trypho", "Pros Tryphōna Dialogos", "Dialogue with Trypho", "grc", 160, ["patristic_gr"], "justin_martyr"),
    ("irenaeus_adversus_haereses", "Elenchos kai Anatropē tēs Pseudōnymou Gnōseōs", "Against Heresies", "grc", 180, ["patristic_gr"], "irenaeus"),
    ("clement_alexandria_protrepticus", "Protreptikos pros Hellēnas", "Exhortation to the Greeks", "grc", 195, ["patristic_gr"], "clement_of_alexandria"),
    ("clement_alexandria_stromateis", "Strōmateis", "Miscellanies", "grc", 200, ["patristic_gr"], "clement_of_alexandria"),
    ("origen_de_principiis", "Peri Archōn", "On First Principles", "grc", 230, ["patristic_gr"], "origen"),
    ("origen_contra_celsum", "Kata Kelsou", "Against Celsus", "grc", 248, ["patristic_gr", "apologetics"], "origen"),
    ("athanasius_de_incarnatione", "Peri tēs Enanthrōpēseōs tou Logou", "On the Incarnation", "grc", 318, ["patristic_gr"], "athanasius"),
    ("basil_hexaemeron", "Homiliai eis tēn Hexaēmeron", "Homilies on the Hexaemeron", "grc", 378, ["patristic_gr", "cappadocian"], "basil_of_caesarea"),
    ("gregory_nazianzus_orationes_theologicae", "Logoi Theologikoi", "Theological Orations", "grc", 380, ["patristic_gr", "cappadocian"], "gregory_of_nazianzus"),
    ("gregory_nyssa_de_anima", "Peri Psychēs kai Anastaseōs", "On the Soul and the Resurrection", "grc", 380, ["patristic_gr", "cappadocian"], "gregory_of_nyssa"),
    ("gregory_nyssa_de_hominis_opificio", "Peri Kataskeuēs Anthrōpou", "On the Making of Man", "grc", 379, ["patristic_gr", "cappadocian"], "gregory_of_nyssa"),
    ("john_chrysostom_de_sacerdotio", "Peri Hierōsynēs", "On the Priesthood", "grc", 386, ["patristic_gr"], "john_chrysostom"),
    ("cyril_alexandria_de_trinitate", "Thēsauros peri tēs Hagias Triados", "Thesaurus on the Holy Trinity", "grc", 425, ["patristic_gr"], "cyril_of_alexandria"),
    ("maximus_confessor_ambigua", "Ambigua ad Iohannem", "Ambigua", "grc", 630, ["patristic_gr"], "maximus_confessor"),
    ("evagrius_ponticus_praktikos", "Praktikos", "Praktikos (Treatise on the Practical Life)", "grc", 383, ["patristic_gr", "monastic"], "evagrius_ponticus"),
    ("eusebius_historia_ecclesiastica", "Ekklēsiastikē Historia", "Ecclesiastical History", "grc", 324, ["patristic_gr", "history"], "eusebius_of_caesarea"),
    ("eusebius_praeparatio_evangelica", "Euangelikē Proparaskeuē", "Preparation for the Gospel", "grc", 313, ["patristic_gr", "apologetics"], "eusebius_of_caesarea"),

    # ── Patristique latine
    ("tertullian_apologeticum", "Apologeticum", "Apology", "lat", 197, ["patristic_lat"], "tertullian"),
    ("tertullian_de_praescriptione", "De Praescriptione Haereticorum", "On the Prescription of Heretics", "lat", 200, ["patristic_lat"], "tertullian"),
    ("cyprian_de_unitate_ecclesiae", "De Catholicae Ecclesiae Unitate", "On the Unity of the Church", "lat", 251, ["patristic_lat"], "cyprian"),
    ("augustine_confessions", "Confessiones", "Confessions", "lat", 401, ["patristic_lat"], "augustine"),
    ("augustine_de_civitate_dei", "De Civitate Dei", "City of God", "lat", 426, ["patristic_lat"], "augustine"),
    ("augustine_de_trinitate", "De Trinitate", "On the Trinity", "lat", 419, ["patristic_lat"], "augustine"),
    ("augustine_de_doctrina_christiana", "De Doctrina Christiana", "On Christian Doctrine", "lat", 427, ["patristic_lat", "hermeneutics"], "augustine"),
    ("jerome_vulgata", "Biblia Sacra Vulgata", "Vulgate Bible (translation)", "lat", 405, ["patristic_lat", "translation"], "jerome"),
    ("ambrose_de_officiis", "De Officiis Ministrorum", "On the Duties of the Clergy", "lat", 391, ["patristic_lat"], "ambrose"),
    ("boethius_consolatio", "De Consolatione Philosophiae", "Consolation of Philosophy", "lat", 524, ["patristic_lat", "neoplatonic"], "boethius"),

    # ── Pseudo-Denys (charnière)
    ("pseudo_dionysius_corpus", "Corpus Dionysiacum (Hierarchies + Mystical Theology + Divine Names)", "Pseudo-Dionysian Corpus", "grc", 500, ["patristic_gr", "neoplatonic", "mystical"], "pseudo_dionysius"),
]

assert len(WORKS) == 70, f"GRECO_LATIN×late_antique doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "neoplatonic" in tags and "patristic" not in " ".join(tags):
        return "GREEK_NEOPLATONIC"
    if "patristic_gr" in tags and "cappadocian" in tags:
        return "PATRISTIC_GREEK_CAPPADOCIAN"
    if "patristic_gr" in tags:
        return "PATRISTIC_GREEK"
    if "patristic_lat" in tags:
        return "PATRISTIC_LATIN"
    if "stoic" in tags:
        return "ROMAN_STOIC"
    if "epicurean" in tags:
        return "ROMAN_EPICUREAN"
    if "skeptic" in tags:
        return "GREEK_SKEPTIC"
    if "middle_platonic" in tags:
        return "MIDDLE_PLATONIC"
    if "doxography" in tags:
        return "DOXOGRAPHY"
    if "medicine" in tags:
        return "GREEK_MEDICINE"
    if "history" in tags:
        return "ROMAN_HISTORY"
    if "biography" in tags:
        return "ROMAN_BIOGRAPHY"
    if "rhetoric" in tags:
        return "ROMAN_RHETORIC"
    if "epic_poetry" in tags or "poetry" in tags:
        return "ROMAN_POETRY"
    if "platonic" in tags:
        return "MIDDLE_PLATONIC"
    if "roman" in tags:
        return "ROMAN_LITERATURE"
    return "LATE_ANTIQUE_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "GRECO_LATIN",
            "epoch": "late_antique",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 20,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206l_greco_latin_late_antique",
        "generated": "2026-04-29",
        "macro_culture": "GRECO_LATIN",
        "epoch": "late_antique",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["Perseus Digital Library", "Patrologia Graeca/Latina (Migne)", "Loeb Classical Library", "CCEL", "sacred-texts.com"],
        "language_original_dominant": "grc + lat",
        "schools_covered": [
            "Cicéron + Lucrèce (république romaine tardive)",
            "Stoïcisme impérial (Sénèque ×4, Épictète ×2, Marc Aurèle, Musonius Rufus)",
            "Galien (médecine ×2)",
            "Sextus Empiricus (scepticisme ×2)",
            "Diogène Laërce (doxographie)",
            "Néoplatonisme (Plotin, Porphyre ×3, Jamblique ×2, Proclus ×3, Damascius, Hiéroclès)",
            "Patristique grecque (Justin, Irénée, Clément ×2, Origène ×2, Athanase, Cappadociens ×4, Chrysostome, Cyrille, Maxime, Évagre, Eusèbe ×2)",
            "Patristique latine (Tertullien ×2, Cyprien, Augustin ×4, Jérôme Vulgate, Ambroise, Boèce)",
            "Pseudo-Denys (charnière médiévale)",
            "Lit. romaine (Virgile, Horace, Ovide, Apulée ×2, Quintilien)",
            "Historiens (Tite-Live, Tacite, Suétone, Plutarque ×2)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue GRECO_LATIN × late_antique : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
§206m — Catalogue GRECO_LATIN × medieval (500 → 1500), 70 œuvres.

Strates :
- Scolastique latine pré-thomiste : Isidore, Cassiodore, Bède, Alcuin, Jean Scot Érigène,
  Anselme, Pierre Lombard, Abélard, Hugues + Richard de St-Victor
- Scolastique haute : Albert le Grand, Thomas d'Aquin, Bonaventure
- Scolastique tardive : Duns Scot, Guillaume d'Ockham, Buridan, Oresme
- Mystique rhénane et flamande : Eckhart, Tauler, Suso, Ruysbroeck, Hildegarde de Bingen
- Byzantin : Photios, Psellos, Jean de Damas, Syméon le Nouveau Théologien, Grégoire Palamas
- Cosmologie/sciences : Roger Bacon, Robert Grosseteste
- Lit. médiévale : Dante, Pétrarque, Boccace, Chaucer
- Sources : sacred-texts.com, CCEL, Wikisource, archive.org Patrologia.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_greco_latin_medieval_v206m.json"

WORKS = [
    # ── Scolastique latine pré-thomiste
    ("isidore_etymologiae", "Etymologiae", "Etymologies", "lat", 625, ["scholastic_pre", "encyclopedia"], "isidore_of_seville"),
    ("cassiodorus_institutiones", "Institutiones Divinarum et Saecularium Litterarum", "Institutions of Divine and Secular Learning", "lat", 562, ["scholastic_pre"], "cassiodorus"),
    ("bede_historia", "Historia Ecclesiastica Gentis Anglorum", "Ecclesiastical History of the English People", "lat", 731, ["patristic_lat", "history"], "bede"),
    ("alcuin_de_dialectica", "De Dialectica", "On Dialectic", "lat", 790, ["scholastic_pre"], "alcuin"),
    ("eriugena_periphyseon", "Periphyseon (De Divisione Naturae)", "Periphyseon (On the Division of Nature)", "lat", 867, ["scholastic_pre", "neoplatonic"], "john_scotus_eriugena"),
    ("anselm_proslogion", "Proslogion", "Proslogion", "lat", 1078, ["scholastic"], "anselm_of_canterbury"),
    ("anselm_monologion", "Monologion", "Monologion", "lat", 1076, ["scholastic"], "anselm_of_canterbury"),
    ("anselm_cur_deus_homo", "Cur Deus Homo", "Why God Became Man", "lat", 1098, ["scholastic"], "anselm_of_canterbury"),
    ("abelard_sic_et_non", "Sic et Non", "Yes and No", "lat", 1121, ["scholastic"], "peter_abelard"),
    ("abelard_ethica", "Ethica (Scito Te Ipsum)", "Ethics (Know Thyself)", "lat", 1138, ["scholastic", "ethics"], "peter_abelard"),
    ("peter_lombard_sententiae", "Sententiarum Libri Quatuor", "Four Books of Sentences", "lat", 1158, ["scholastic"], "peter_lombard"),
    ("hugh_st_victor_didascalicon", "Didascalicon", "Didascalicon", "lat", 1130, ["scholastic"], "hugh_of_st_victor"),
    ("richard_st_victor_de_trinitate", "De Trinitate", "On the Trinity", "lat", 1170, ["scholastic"], "richard_of_st_victor"),
    ("bernard_clairvaux_de_diligendo_deo", "De Diligendo Deo", "On Loving God", "lat", 1126, ["mystical_lat"], "bernard_of_clairvaux"),

    # ── Scolastique haute
    ("albertus_magnus_de_animalibus", "De Animalibus", "On Animals", "lat", 1262, ["scholastic", "natural_philosophy"], "albert_the_great"),
    ("albertus_magnus_summa_theologiae", "Summa Theologiae (Albertina)", "Summa Theologiae", "lat", 1280, ["scholastic"], "albert_the_great"),
    ("aquinas_summa_theologiae", "Summa Theologiae", "Summa Theologica", "lat", 1273, ["scholastic", "thomist"], "thomas_aquinas"),
    ("aquinas_summa_contra_gentiles", "Summa Contra Gentiles", "Summa Against the Gentiles", "lat", 1265, ["scholastic", "thomist"], "thomas_aquinas"),
    ("aquinas_de_ente_et_essentia", "De Ente et Essentia", "On Being and Essence", "lat", 1252, ["scholastic", "thomist"], "thomas_aquinas"),
    ("aquinas_quaestiones_disputatae_de_veritate", "Quaestiones Disputatae De Veritate", "Disputed Questions on Truth", "lat", 1259, ["scholastic", "thomist"], "thomas_aquinas"),
    ("aquinas_super_libros_sententiarum", "Scriptum Super Libros Sententiarum", "Commentary on the Sentences", "lat", 1256, ["scholastic", "thomist"], "thomas_aquinas"),
    ("aquinas_de_anima_commentary", "Sentencia Libri De Anima", "Commentary on De Anima", "lat", 1268, ["scholastic", "thomist"], "thomas_aquinas"),
    ("bonaventure_itinerarium", "Itinerarium Mentis in Deum", "The Journey of the Mind to God", "lat", 1259, ["scholastic", "franciscan", "mystical_lat"], "bonaventure"),
    ("bonaventure_breviloquium", "Breviloquium", "Breviloquium", "lat", 1257, ["scholastic", "franciscan"], "bonaventure"),
    ("bonaventure_collationes_hexaemeron", "Collationes in Hexaemeron", "Collations on the Six Days", "lat", 1273, ["scholastic", "franciscan"], "bonaventure"),

    # ── Scolastique tardive
    ("duns_scotus_ordinatio", "Ordinatio (Opus Oxoniense)", "Ordinatio", "lat", 1304, ["scholastic", "scotist"], "duns_scotus"),
    ("duns_scotus_quaestiones_quodlibetales", "Quaestiones Quodlibetales", "Quodlibetal Questions", "lat", 1306, ["scholastic", "scotist"], "duns_scotus"),
    ("ockham_summa_logicae", "Summa Logicae", "Summa Logicae", "lat", 1323, ["scholastic", "nominalist"], "william_of_ockham"),
    ("ockham_quodlibeta", "Quodlibeta Septem", "Seven Quodlibets", "lat", 1325, ["scholastic", "nominalist"], "william_of_ockham"),
    ("ockham_dialogus", "Dialogus", "Dialogue", "lat", 1340, ["scholastic", "politics"], "william_of_ockham"),
    ("buridan_summulae", "Summulae de Dialectica", "Summulae de Dialectica", "lat", 1335, ["scholastic", "logic"], "john_buridan"),
    ("oresme_de_configurationibus", "Tractatus de Configurationibus Qualitatum et Motuum", "On the Configurations of Qualities and Motions", "lat", 1370, ["scholastic", "natural_philosophy"], "nicole_oresme"),
    ("oresme_livre_du_ciel", "Livre du Ciel et du Monde", "Book of the Heavens and the World", "frm", 1377, ["scholastic", "cosmology"], "nicole_oresme"),
    ("henry_ghent_summa", "Summa Quaestionum Ordinariarum", "Summa of Ordinary Questions", "lat", 1290, ["scholastic"], "henry_of_ghent"),
    ("godfrey_fontaines_quodlibeta", "Quodlibeta", "Quodlibetal Questions", "lat", 1299, ["scholastic"], "godfrey_of_fontaines"),

    # ── Mystique
    ("eckhart_predigten", "Deutsche Predigten und Traktate", "German Sermons and Treatises", "gmh", 1320, ["mystical_lat", "rhenish"], "meister_eckhart"),
    ("eckhart_opus_tripartitum", "Opus Tripartitum (frgs)", "Opus Tripartitum", "lat", 1310, ["scholastic", "mystical_lat"], "meister_eckhart"),
    ("tauler_predigten", "Predigten", "Sermons", "gmh", 1361, ["mystical_lat", "rhenish"], "johannes_tauler"),
    ("suso_horologium", "Horologium Sapientiae", "Clock of Wisdom", "lat", 1334, ["mystical_lat", "rhenish"], "henry_suso"),
    ("ruysbroeck_brulocht", "Die geestelike Brulocht", "The Spiritual Espousals", "dum", 1335, ["mystical_lat", "flemish"], "jan_van_ruysbroeck"),
    ("hildegard_scivias", "Scivias", "Scivias (Know the Ways)", "lat", 1151, ["mystical_lat", "visionary"], "hildegard_of_bingen"),
    ("hildegard_liber_divinorum_operum", "Liber Divinorum Operum", "Book of Divine Works", "lat", 1174, ["mystical_lat", "visionary"], "hildegard_of_bingen"),
    ("julian_norwich_revelations", "Revelations of Divine Love", "Revelations of Divine Love", "enm", 1395, ["mystical_lat", "english"], "julian_of_norwich"),
    ("cloud_of_unknowing", "The Cloud of Unknowing", "The Cloud of Unknowing", "enm", 1380, ["mystical_lat", "english", "apophatic"], "anonymous_cloud"),
    ("aquinas_de_imitatione_thomas_kempis", "De Imitatione Christi", "Imitation of Christ", "lat", 1418, ["mystical_lat", "devotio_moderna"], "thomas_a_kempis"),
    ("walter_hilton_scale_perfection", "The Scale of Perfection", "The Scale of Perfection", "enm", 1396, ["mystical_lat", "english"], "walter_hilton"),

    # ── Byzantin
    ("john_damascus_fons_scientiae", "Pēgē Gnōseōs", "Fount of Knowledge", "grc", 743, ["patristic_gr", "byzantine"], "john_of_damascus"),
    ("photios_bibliotheca", "Bibliothēkē (Myriobiblos)", "Bibliotheca", "grc", 858, ["byzantine", "doxography"], "photios"),
    ("photios_mystagogia", "Peri tēs Mystagōgias tou Hagiou Pneumatos", "Mystagogy of the Holy Spirit", "grc", 885, ["byzantine"], "photios"),
    ("psellus_chronographia", "Chronographia", "Chronographia", "grc", 1078, ["byzantine", "history"], "michael_psellos"),
    ("psellus_de_omnifaria_doctrina", "De Omnifaria Doctrina", "On the Universal Doctrine", "grc", 1075, ["byzantine", "neoplatonic"], "michael_psellos"),
    ("symeon_new_theologian_hymns", "Hymnoi Theioi Erōtes", "Hymns of Divine Love", "grc", 1022, ["byzantine", "mystical"], "symeon_new_theologian"),
    ("gregory_palamas_triads", "Hyper tōn Hierōs Hēsychazontōn", "Triads in Defence of the Holy Hesychasts", "grc", 1340, ["byzantine", "mystical", "hesychast"], "gregory_palamas"),
    ("gregory_palamas_capita_physica", "Kephalaia Physika, Theologika, Ēthika kai Praktika", "150 Chapters", "grc", 1347, ["byzantine", "mystical"], "gregory_palamas"),
    ("nicholas_cusa_de_docta_ignorantia", "De Docta Ignorantia", "On Learned Ignorance", "lat", 1440, ["scholastic", "neoplatonic", "mystical_lat"], "nicholas_of_cusa"),
    ("nicholas_cusa_de_visione_dei", "De Visione Dei", "On the Vision of God", "lat", 1453, ["scholastic", "mystical_lat"], "nicholas_of_cusa"),
    ("plethon_nomoi", "Nomōn Syngraphē", "Book of Laws", "grc", 1450, ["byzantine", "neoplatonic"], "george_gemistos_plethon"),

    # ── Sciences
    ("roger_bacon_opus_majus", "Opus Majus", "Greater Work", "lat", 1267, ["scholastic", "natural_philosophy"], "roger_bacon"),
    ("grosseteste_de_luce", "De Luce", "On Light", "lat", 1230, ["scholastic", "cosmology"], "robert_grosseteste"),
    ("witelo_perspectiva", "Perspectiva", "Perspectiva", "lat", 1275, ["scholastic", "optics"], "witelo"),

    # ── Lit. médiévale
    ("dante_divina_commedia", "Divina Commedia", "Divine Comedy", "ita", 1320, ["mystical_lat", "poetry"], "dante"),
    ("dante_convivio", "Convivio", "Convivio", "ita", 1308, ["scholastic", "vernacular"], "dante"),
    ("dante_de_monarchia", "De Monarchia", "On Monarchy", "lat", 1313, ["scholastic", "politics"], "dante"),
    ("petrarch_secretum", "Secretum (De Secreto Conflictu Curarum Mearum)", "The Secret", "lat", 1353, ["humanist", "augustinian"], "petrarch"),
    ("petrarch_canzoniere", "Rerum Vulgarium Fragmenta (Canzoniere)", "Canzoniere", "ita", 1374, ["humanist", "poetry"], "petrarch"),
    ("boccaccio_decameron", "Decameron", "Decameron", "ita", 1353, ["humanist", "vernacular"], "boccaccio"),
    ("chaucer_canterbury_tales", "The Canterbury Tales", "The Canterbury Tales", "enm", 1400, ["vernacular", "english"], "chaucer"),
    ("william_langland_piers_plowman", "Piers Plowman", "Piers Plowman", "enm", 1390, ["vernacular", "english", "allegory"], "langland"),
    ("aelred_speculum_caritatis", "Speculum Caritatis", "Mirror of Charity", "lat", 1142, ["mystical_lat", "cistercian"], "aelred_of_rievaulx"),
    ("marsilius_padua_defensor_pacis", "Defensor Pacis", "Defender of the Peace", "lat", 1324, ["scholastic", "politics"], "marsilius_of_padua"),
]

assert len(WORKS) == 70, f"GRECO_LATIN×medieval doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "byzantine" in tags and "mystical" in tags:
        return "BYZANTINE_HESYCHAST" if "hesychast" in tags else "BYZANTINE_MYSTICAL"
    if "byzantine" in tags:
        return "BYZANTINE"
    if "mystical_lat" in tags and "rhenish" in tags:
        return "RHENISH_MYSTICISM"
    if "mystical_lat" in tags and "flemish" in tags:
        return "FLEMISH_MYSTICISM"
    if "mystical_lat" in tags and "english" in tags:
        return "ENGLISH_MYSTICISM"
    if "mystical_lat" in tags and "devotio_moderna" in tags:
        return "DEVOTIO_MODERNA"
    if "mystical_lat" in tags:
        return "LATIN_MYSTICAL"
    if "thomist" in tags:
        return "SCHOLASTIC_THOMIST"
    if "scotist" in tags:
        return "SCHOLASTIC_SCOTIST"
    if "nominalist" in tags:
        return "SCHOLASTIC_NOMINALIST"
    if "franciscan" in tags:
        return "SCHOLASTIC_FRANCISCAN"
    if "scholastic" in tags and "natural_philosophy" in tags:
        return "SCHOLASTIC_SCIENCE"
    if "scholastic" in tags:
        return "SCHOLASTIC"
    if "scholastic_pre" in tags:
        return "SCHOLASTIC_PRE_THOMIST"
    if "humanist" in tags:
        return "EARLY_HUMANIST"
    if "vernacular" in tags:
        return "MEDIEVAL_VERNACULAR"
    if "patristic_lat" in tags:
        return "PATRISTIC_LATIN"
    if "patristic_gr" in tags:
        return "PATRISTIC_GREEK"
    return "MEDIEVAL_LATIN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "GRECO_LATIN",
            "epoch": "medieval",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 15,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206m_greco_latin_medieval",
        "generated": "2026-04-29",
        "macro_culture": "GRECO_LATIN",
        "epoch": "medieval",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["CCEL", "Patrologia Latina/Graeca (Migne)", "Wikisource latine", "sacred-texts.com", "archive.org"],
        "language_original_dominant": "lat + grc + vernacular (ita, gmh, dum, enm, frm)",
        "schools_covered": [
            "Scolastique pré-thomiste (Isidore, Cassiodore, Bède, Alcuin, Érigène, Anselme ×3, Lombard, Abélard ×2, Hugues+Richard de St-Victor, Bernard de Clairvaux)",
            "Scolastique haute (Albert ×2, Aquin ×6, Bonaventure ×3)",
            "Scolastique tardive (Duns Scot ×2, Ockham ×3, Buridan, Oresme ×2, Henri de Gand, Godefroid de Fontaines)",
            "Mystique latine (Eckhart ×2, Tauler, Suso, Ruysbroeck, Hildegarde ×2, Julian Norwich, Cloud, Imitation Christi, Walter Hilton, Aelred)",
            "Byzantin (Jean Damas, Photios ×2, Psellos ×2, Syméon, Palamas ×2, Cusa ×2, Pléthon)",
            "Sciences (Roger Bacon, Grosseteste, Witelo)",
            "Lit. médiévale (Dante ×3, Pétrarque ×2, Boccace, Chaucer, Langland)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue GRECO_LATIN × medieval : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

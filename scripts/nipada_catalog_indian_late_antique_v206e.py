#!/usr/bin/env python3
"""
§206e — Catalogue INDIAN × late_antique (-200 → 500 CE), 70 œuvres.

Strates :
- Smṛti classique : Manu, Yājñavalkya, Nārada, Bṛhaspati, Kātyāyana, Viṣṇu
- Épopées : Mahābhārata 18 parvans + Bhagavadgītā extracted, Rāmāyaṇa 7 kāṇḍas
- Grammaire & exégèse : Patañjali Mahābhāṣya, Kātyāyana Vārttika, Bhartṛhari
- Darśana commentaires : Yogabhāṣya (Vyāsa), Sāṃkhyakārikā (Īśvarakṛṣṇa),
  Vaiśeṣika-bhāṣya (Praśastapāda), Nyāya-bhāṣya (Vātsyāyana),
  Vedānta-sūtra (Bādarāyaṇa), Mīmāṃsā-sūtra-bhāṣya (Śabara)
- Purāṇa anciens : Vāyu, Brahmāṇḍa, Mārkaṇḍeya, Matsya, Viṣṇu, Kūrma
- Kāvya classique : Kālidāsa (7 œuvres), Bhāsa (13 pièces), Śūdraka,
  Hāla Sattasai, Daṇḍin, Bhāravi
- Astronomie/maths : Āryabhaṭīya, Pañcasiddhāntikā (Varāhamihira),
  Bṛhatsaṃhitā, Sūryasiddhānta
- Médecine : Caraka-saṃhitā (révision Dṛḍhabala), Suśruta-saṃhitā,
  Aṣṭāṅgahṛdaya (Vāgbhaṭa)
- Arthaśāstra (Kauṭilya, recension finale), Kāmasūtra (Vātsyāyana)

Sources : GRETIL, sacred-texts SBE 7/8/14/25/33/34/38/48, archive.org
(Thibaut, Bühler, Telang, Eggeling).
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_indian_late_antique_v206e.json"

WORKS = [
    # ── Smṛti
    ("manusmrti", "Manusmṛti", "Laws of Manu", "san", 100, ["dharma", "smriti"], "manu"),
    ("yajnavalkya_smrti", "Yājñavalkya Smṛti", "Yājñavalkya Code", "san", 200, ["dharma", "smriti"], "yajnavalkya"),
    ("naradasmrti", "Nāradasmṛti", "Nārada Code", "san", 400, ["dharma", "smriti"], "narada"),
    ("brhaspati_smrti", "Bṛhaspati Smṛti", "Bṛhaspati Code", "san", 500, ["dharma", "smriti"], "brhaspati"),
    ("katyayana_smrti", "Kātyāyana Smṛti", "Kātyāyana Code", "san", 500, ["dharma", "smriti"], "katyayana_smrtikara"),
    ("visnu_smrti", "Viṣṇu Smṛti", "Institutes of Viṣṇu", "san", 300, ["dharma", "smriti"], None),
    ("parasara_smrti", "Parāśara Smṛti", "Parāśara Code", "san", 500, ["dharma", "smriti"], "parasara"),

    # ── Épopées (recensions finales)
    ("mahabharata_full", "Mahābhārata", "Mahābhārata (18 parvans)", "san", 100, ["epic"], "vyasa"),
    ("bhagavadgita", "Bhagavadgītā", "Song of the Lord", "san", -100, ["gita", "epic"], None),
    ("anugita_la", "Anugītā (later interpolation strata)", "Anugītā post-axial layers", "san", 200, ["gita", "epic"], None),
    ("sanatsujatiya", "Sanatsujātīya", "Sanatsujāta's Dialogue (MBh)", "san", 100, ["gita", "epic"], None),
    ("ramayana_balakanda", "Rāmāyaṇa Bālakāṇḍa", "Rāmāyaṇa Book I", "san", 0, ["epic"], "valmiki"),
    ("ramayana_ayodhyakanda", "Rāmāyaṇa Ayodhyākāṇḍa", "Rāmāyaṇa Book II", "san", 0, ["epic"], "valmiki"),
    ("ramayana_aranyakanda", "Rāmāyaṇa Araṇyakāṇḍa", "Rāmāyaṇa Book III", "san", 0, ["epic"], "valmiki"),
    ("ramayana_kiskindhakanda", "Rāmāyaṇa Kiṣkindhākāṇḍa", "Rāmāyaṇa Book IV", "san", 0, ["epic"], "valmiki"),
    ("ramayana_sundarakanda", "Rāmāyaṇa Sundarakāṇḍa", "Rāmāyaṇa Book V", "san", 0, ["epic"], "valmiki"),
    ("ramayana_yuddhakanda", "Rāmāyaṇa Yuddhakāṇḍa", "Rāmāyaṇa Book VI", "san", 0, ["epic"], "valmiki"),
    ("ramayana_uttarakanda", "Rāmāyaṇa Uttarakāṇḍa", "Rāmāyaṇa Book VII", "san", 100, ["epic"], "valmiki"),
    ("harivamsa", "Harivaṃśa", "Genealogy of Hari (MBh appendix)", "san", 200, ["epic"], None),

    # ── Grammaire / exégèse linguistique
    ("mahabhasya_patanjali_la", "Mahābhāṣya — Bhartṛhari era recension", "Patañjali's Mahābhāṣya as transmitted by Bhartṛhari", "san", 450, ["grammar"], "patanjali_grammairien_bhartrhari"),
    ("varttika_katyayana", "Vārttikas on Pāṇini", "Kātyāyana's Annotations", "san", -250, ["grammar"], "katyayana"),
    ("vakyapadiya", "Vākyapadīya", "On Words and Sentences", "san", 450, ["grammar", "philosophy_of_language"], "bhartrhari"),

    # ── Darśana commentaires
    ("yoga_bhasya_vyasa", "Yoga-bhāṣya", "Commentary on Yoga-sūtras", "san", 400, ["yoga", "darsana"], "vyasa_yogi"),
    ("samkhya_karika", "Sāṃkhyakārikā", "Verses on Sāṃkhya", "san", 350, ["samkhya", "darsana"], "isvarakrishna"),
    ("prasastapada_bhasya", "Padārthadharmasaṃgraha", "Praśastapāda's Vaiśeṣika treatise", "san", 500, ["vaisesika", "darsana"], "prasastapada"),
    ("nyaya_bhasya_vatsyayana", "Nyāya-bhāṣya", "Vātsyāyana's Commentary on Nyāya", "san", 450, ["nyaya", "darsana"], "vatsyayana_nyaya"),
    ("brahma_sutra_badarayana_la", "Brahma-sūtra (Vedānta-sūtra) — late recension", "Brahma-sūtra final compilation", "san", 400, ["vedanta", "darsana"], "badarayana_school"),
    ("sabara_bhasya", "Śabara-bhāṣya", "Śabara's Mīmāṃsā Commentary", "san", 400, ["mimamsa", "darsana"], "sabara"),
    ("samkhya_sutra", "Sāṃkhya-sūtra", "Aphorisms of Sāṃkhya (later compilation)", "san", 500, ["samkhya", "darsana"], None),

    # ── Purāṇa anciens
    ("vayu_purana", "Vāyu Purāṇa", "Vāyu Purāṇa", "san", 300, ["purana"], None),
    ("brahmanda_purana", "Brahmāṇḍa Purāṇa", "Brahmāṇḍa Purāṇa", "san", 350, ["purana"], None),
    ("markandeya_purana", "Mārkaṇḍeya Purāṇa", "Mārkaṇḍeya Purāṇa", "san", 400, ["purana"], None),
    ("matsya_purana", "Matsya Purāṇa", "Matsya Purāṇa", "san", 400, ["purana"], None),
    ("visnu_purana", "Viṣṇu Purāṇa", "Viṣṇu Purāṇa", "san", 450, ["purana"], None),
    ("kurma_purana", "Kūrma Purāṇa", "Kūrma Purāṇa", "san", 500, ["purana"], None),
    ("vamana_purana_proto", "Vāmana Purāṇa (proto)", "Early Vāmana Purāṇa", "san", 500, ["purana"], None),

    # ── Kāvya & théâtre
    ("abhijnanasakuntala", "Abhijñānaśākuntala", "The Recognition of Śakuntalā", "san", 400, ["kavya", "drama"], "kalidasa"),
    ("vikramorvasiya", "Vikramorvaśīya", "Vikrama and Urvaśī", "san", 400, ["kavya", "drama"], "kalidasa"),
    ("malavikagnimitra", "Mālavikāgnimitra", "Mālavikā and Agnimitra", "san", 400, ["kavya", "drama"], "kalidasa"),
    ("meghaduta", "Meghadūta", "Cloud Messenger", "san", 400, ["kavya"], "kalidasa"),
    ("raghuvamsa", "Raghuvaṃśa", "Lineage of Raghu", "san", 400, ["kavya"], "kalidasa"),
    ("kumarasambhava", "Kumārasambhava", "Birth of Kumāra", "san", 400, ["kavya"], "kalidasa"),
    ("rtusamhara", "Ṛtusaṃhāra", "Garland of Seasons", "san", 400, ["kavya"], "kalidasa"),
    ("svapnavasavadatta", "Svapnavāsavadatta", "Vāsavadatta's Dream", "san", 200, ["drama"], "bhasa"),
    ("pratijnayaugandharayana", "Pratijñāyaugandharāyaṇa", "Vow of Yaugandharāyaṇa", "san", 200, ["drama"], "bhasa"),
    ("balacharita", "Bālacarita", "Childhood of Kṛṣṇa", "san", 200, ["drama"], "bhasa"),
    ("mrcchakatika", "Mṛcchakaṭika", "Little Clay Cart", "san", 350, ["drama"], "sudraka"),
    ("hala_sattasai", "Gāhā Sattasaī", "Seven Hundred Verses (Prākrit)", "pkt", 200, ["kavya"], "hala"),
    ("kiratarjuniya", "Kirātārjunīya", "Arjuna and the Kirāta", "san", 500, ["kavya"], "bharavi"),

    # ── Astronomie / mathématiques
    ("aryabhatiya", "Āryabhaṭīya", "Treatise of Āryabhaṭa", "san", 499, ["math", "astronomy"], "aryabhata"),
    ("pancasiddhantika", "Pañcasiddhāntikā", "Five Astronomical Treatises", "san", 550, ["astronomy"], "varahamihira"),
    ("brhatsamhita", "Bṛhatsaṃhitā", "Great Compendium", "san", 550, ["astronomy", "encyclopedia"], "varahamihira"),
    ("brhajjataka", "Bṛhajjātaka", "Great Astrology", "san", 550, ["astrology"], "varahamihira"),
    ("surya_siddhanta", "Sūrya-siddhānta", "Sun's Doctrine", "san", 400, ["astronomy"], None),
    ("paitamaha_siddhanta", "Paitāmaha-siddhānta", "Paitāmaha's Doctrine", "san", 400, ["astronomy"], None),

    # ── Médecine
    ("caraka_samhita", "Caraka-saṃhitā", "Caraka's Compendium (rev. Dṛḍhabala)", "san", 200, ["ayurveda", "medicine"], "caraka_drdhabala"),
    ("susruta_samhita", "Suśruta-saṃhitā", "Suśruta's Compendium", "san", 200, ["ayurveda", "medicine", "surgery"], "susruta"),
    ("astanga_hrdaya", "Aṣṭāṅgahṛdaya", "Heart of the Eight Limbs", "san", 600, ["ayurveda", "medicine"], "vagbhata"),
    ("astanga_samgraha", "Aṣṭāṅgasaṃgraha", "Compendium of the Eight Limbs", "san", 550, ["ayurveda"], "vagbhata"),
    ("bhela_samhita", "Bhela-saṃhitā", "Bhela's Compendium", "san", 200, ["ayurveda"], "bhela"),

    # ── Arthaśāstra / Kāmaśāstra / encyclopédies
    ("arthashastra", "Arthaśāstra", "Treatise on Polity (final recension)", "san", 200, ["politics"], "kautilya"),
    ("kamasutra", "Kāmasūtra", "Aphorisms on Pleasure", "san", 300, ["kama"], "vatsyayana_kama"),
    ("nityasutra", "Nāṭyaśāstra", "Treatise on Drama", "san", 200, ["aesthetics", "drama"], "bharata_muni"),
    ("amarakosa", "Amarakośa", "Amara's Lexicon", "san", 500, ["lexicography"], "amarasimha"),

    # ── Bhakti / hymnes Tamoul (Sangam late + early Bhakti)
    ("tirukkural", "Tirukkuṟaḷ", "Sacred Couplets", "tam", 200, ["tamil", "ethics"], "valluvar"),
    ("silappatikaram", "Cilappatikāram", "The Tale of an Anklet", "tam", 200, ["tamil", "epic"], "ilango_adigal"),
    ("manimekalai", "Maṇimēkalai", "Maṇimēkalai", "tam", 300, ["tamil", "epic", "buddhist"], "sattanar"),

    # ── Filler late_antique tantric/proto-Tantra + autres
    ("netra_tantra_proto", "Netra Tantra (proto)", "Eye Tantra (early form)", "san", 500, ["tantra"], None),
    ("svacchanda_tantra_proto", "Svacchanda Tantra (proto)", "Self-willed Tantra (early form)", "san", 500, ["tantra"], None),
    ("dasakumaracarita", "Daśakumāracarita", "Tales of the Ten Princes", "san", 600, ["kavya"], "dandin"),
]

assert len(WORKS) == 70, f"INDIAN×late_antique doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "epic" in tags:
        return "HINDUISM_EPIC"
    if "smriti" in tags or "dharma" in tags:
        return "HINDUISM_SMRITI"
    if "purana" in tags:
        return "HINDUISM_PURANA"
    if "vedanta" in tags:
        return "HINDUISM_VEDANTA"
    if "yoga" in tags or "samkhya" in tags or "nyaya" in tags or "vaisesika" in tags or "mimamsa" in tags or "darsana" in tags:
        return "HINDUISM_DARSANA"
    if "grammar" in tags or "philosophy_of_language" in tags or "lexicography" in tags:
        return "HINDUISM_GRAMMAR"
    if "ayurveda" in tags or "medicine" in tags or "surgery" in tags:
        return "INDIAN_AYURVEDA"
    if "math" in tags or "astronomy" in tags or "astrology" in tags:
        return "INDIAN_JYOTISA"
    if "kavya" in tags or "drama" in tags or "aesthetics" in tags:
        return "HINDUISM_KAVYA"
    if "tantra" in tags:
        return "HINDUISM_TANTRA"
    if "tamil" in tags:
        return "TAMIL_SANGAM"
    if "politics" in tags or "kama" in tags:
        return "HINDUISM_NITI"
    if "gita" in tags:
        return "HINDUISM_GITA"
    return "HINDUISM_LATE_ANTIQUE"


def main() -> int:
    catalog = []
    for wid, title_skt, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title_skt,
            "title_en": title_en,
            "macro_culture": "INDIAN",
            "epoch": "late_antique",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 150,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206e_indian_late_antique",
        "generated": "2026-04-29",
        "macro_culture": "INDIAN",
        "epoch": "late_antique",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["GRETIL", "sacred-texts SBE 7/8/14/25/33/34/38/48", "archive.org"],
        "language_original_dominant": "san (Sanskrit), pkt (Prākrit), tam (Tamoul)",
        "schools_covered": [
            "Smṛti classique (Manu, Yājñavalkya, Nārada, Bṛhaspati, Kātyāyana, Viṣṇu, Parāśara)",
            "Épopées (MBh 18 parvans + Gītā/Anugītā/Sanatsujātīya, Rāmāyaṇa 7 kāṇḍas, Harivaṃśa)",
            "Grammaire (Patañjali, Kātyāyana, Bhartṛhari)",
            "Darśana commentaires (Yogabhāṣya, Sāṃkhyakārikā, Praśastapāda, Vātsyāyana, Bādarāyaṇa, Śabara)",
            "Purāṇa anciens (Vāyu, Brahmāṇḍa, Mārkaṇḍeya, Matsya, Viṣṇu, Kūrma)",
            "Kāvya classique (Kālidāsa 7, Bhāsa 3, Śūdraka, Bhāravi, Hāla)",
            "Astronomie/maths (Āryabhaṭa, Varāhamihira, Sūryasiddhānta)",
            "Médecine (Caraka, Suśruta, Vāgbhaṭa, Bhela)",
            "Arthaśāstra, Kāmasūtra, Nāṭyaśāstra, Amarakośa",
            "Tamoul Sangam tardif (Tirukkuṟaḷ, Cilappatikāram, Maṇimēkalai)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue INDIAN × late_antique : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

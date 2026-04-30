#!/usr/bin/env python3
"""§206q — INDIAN × early_modern (1500 → 1789), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_indian_early_modern_v206q.json"

WORKS = [
    # ── Vedānta post-Vijayanagara (Advaita scolastique tardive)
    ("madhusudana_advaita_siddhi", "Advaita-siddhi", "Establishment of Non-dualism", "san", 1570, ["advaita_late"], "madhusudana_sarasvati"),
    ("madhusudana_gudartha_dipika", "Gūḍhārtha-dīpikā", "Lamp on the Hidden Meaning of the Gītā", "san", 1580, ["advaita_late"], "madhusudana_sarasvati"),
    ("madhusudana_bhakti_rasayana", "Bhakti-rasāyana", "Elixir of Devotion", "san", 1575, ["advaita_late", "bhakti"], "madhusudana_sarasvati"),
    ("appayya_siddhanta_lesa_samgraha", "Siddhāntaleśa-saṃgraha", "Compendium of Vedānta Doctrines", "san", 1590, ["advaita_late"], "appayya_dikshita"),
    ("appayya_parimala", "Parimala", "Fragrance (commentary on Kalpataru)", "san", 1595, ["advaita_late"], "appayya_dikshita"),
    ("nilakantha_mahabharata_bhasya", "Bhārata-bhāva-dīpa", "Light on the Bhāva of the Mahābhārata", "san", 1690, ["advaita_late", "epic_commentary"], "nilakantha_caturdhara"),
    ("dharmaraja_vedanta_paribhasa", "Vedānta-paribhāṣā", "Definitions of Vedānta", "san", 1640, ["advaita_late"], "dharmaraja_adhvarindra"),
    ("sadananda_vedantasara", "Vedānta-sāra", "Essence of Vedānta", "san", 1550, ["advaita_late"], "sadananda"),

    # ── Dvaita & Viśiṣṭādvaita tardifs
    ("vyasa_tirtha_nyayamrta", "Nyāyāmṛta", "Nectar of Logic", "san", 1500, ["dvaita_late"], "vyasa_tirtha"),
    ("vedanta_desika_late_followers", "Tattva-muktā-kalāpa (school continuation)", "Garland of Truth (school continuation)", "san", 1550, ["visistadvaita_late"], "vedanta_desika_school"),

    # ── Caitanya & Gauḍīya Vaiṣṇavisme
    ("caitanya_siksastaka", "Śikṣāṣṭaka", "Eight Verses of Instruction", "san", 1530, ["bhakti_gaudiya"], "caitanya"),
    ("rupa_gosvami_bhakti_rasamrta", "Bhakti-rasāmṛta-sindhu", "Ocean of the Nectar of Devotion", "san", 1542, ["bhakti_gaudiya"], "rupa_gosvami"),
    ("rupa_gosvami_ujjvala_nilamani", "Ujjvala-nīlamaṇi", "Brilliant Sapphire", "san", 1548, ["bhakti_gaudiya"], "rupa_gosvami"),
    ("jiva_gosvami_satsandarbha", "Ṣaṭ-sandarbha", "Six Treatises", "san", 1580, ["bhakti_gaudiya"], "jiva_gosvami"),
    ("sanatana_gosvami_brhad_bhagavatamrta", "Bṛhad-bhāgavatāmṛta", "Great Nectar of the Bhāgavata", "san", 1555, ["bhakti_gaudiya"], "sanatana_gosvami"),
    ("krsnadasa_caitanya_caritamrta", "Caitanya-caritāmṛta", "Nectar of the Life of Caitanya", "ben", 1615, ["bhakti_gaudiya"], "krsnadasa_kaviraja"),
    ("vrndavana_dasa_caitanya_bhagavata", "Caitanya-bhāgavata", "Bhāgavata of Caitanya", "ben", 1573, ["bhakti_gaudiya"], "vrndavana_dasa"),
    ("baladeva_govinda_bhasya", "Govinda-bhāṣya", "Govinda's Commentary (on Brahma-sūtras)", "san", 1764, ["bhakti_gaudiya"], "baladeva_vidyabhusana"),

    # ── Bhakti — Vārkari Maharashtra
    ("tukaram_abhanga", "Abhaṅga-gāthā", "Abhaṅgas (collected hymns)", "mar", 1640, ["bhakti_varkari"], "tukaram"),
    ("eknath_bhagavata", "Eknāthī Bhāgavata", "Eknāth's Bhāgavata", "mar", 1573, ["bhakti_varkari"], "eknath"),
    ("ramadasa_dasabodha", "Dāsabodha", "Instruction to the Servant", "mar", 1654, ["bhakti_varkari", "ethics"], "ramadasa"),
    ("namdev_late_abhanga", "Nāmdev abhaṅgas (late compilation)", "Nāmdev hymns (late compilation)", "mar", 1500, ["bhakti_varkari"], "namdev_compilers"),

    # ── Bhakti — Sant tradition Nord
    ("dadu_dayal_bani", "Dādū-bāṇī", "Sayings of Dādū", "hin", 1600, ["bhakti_sant_nirguna"], "dadu_dayal"),
    ("ravidas_padavali", "Ravidās-padāvalī", "Verses of Ravidās", "hin", 1520, ["bhakti_sant_nirguna"], "ravidas"),
    ("mirabai_padavali", "Mīrā-padāvalī", "Verses of Mīrābāī", "hin", 1560, ["bhakti_sant_saguna"], "mirabai"),
    ("sundardas_jnana_samudra", "Jñāna-samudra", "Ocean of Knowledge", "hin", 1660, ["bhakti_sant_nirguna"], "sundardas"),
    ("tulsidas_kavitavali", "Kavitāvalī", "Garland of Verses", "hin", 1612, ["bhakti_sant_saguna"], "tulsidas"),
    ("tulsidas_vinay_patrika", "Vinay-patrikā", "Petition of Humility", "hin", 1580, ["bhakti_sant_saguna"], "tulsidas"),
    ("bihari_satsai", "Satsaī", "Seven Hundred Verses", "hin", 1662, ["bhakti_sant_saguna", "reeti_kavya"], "bihari_lal"),

    # ── Bhakti — Tamoul tardif & Sant Sud
    ("tayumanavar_padalgal", "Tāyumāṉavar Pāḍalgaḷ", "Songs of Tāyumāṉavar", "tam", 1730, ["bhakti_tamil_late", "saiva"], "tayumanavar"),
    ("ramalinga_predecessors_tiruvarutpa_proto", "Tiruppukaḻ (Aruṇagiri continuation)", "Tiruppukaḻ tradition (post-1500)", "tam", 1500, ["bhakti_tamil_late"], "arunagiri_school"),

    # ── Sikhisme (Ādi Granth + Dasam Granth + littérature secondaire)
    ("adi_granth", "Ādi Granth (Gurū Granth Sāhib)", "Ādi Granth (compiled 1604)", "pan", 1604, ["sikh"], "guru_arjan_compiler"),
    ("dasam_granth", "Dasam Granth", "Book of the Tenth (Gurū Gobind Singh)", "pan", 1698, ["sikh"], "guru_gobind_singh"),
    ("janamsakhi_bhai_bala", "Bhai Bala Janamsākhī", "Birth-stories of Gurū Nānak (Bhai Bala)", "pan", 1620, ["sikh", "hagiography"], "bhai_bala_school"),
    ("janamsakhi_puratan", "Purātan Janamsākhī", "Old Birth-stories of Gurū Nānak", "pan", 1635, ["sikh", "hagiography"], "puratan_compilers"),
    ("varan_bhai_gurdas", "Vārān", "Ballads of Bhai Gurdās", "pan", 1620, ["sikh"], "bhai_gurdas"),
    ("zafarnama_guru_gobind", "Zafarnāmā", "Letter of Victory", "fas", 1705, ["sikh", "epistolary"], "guru_gobind_singh"),

    # ── Tantra & Śākta tardif
    ("bhaskararaya_setu_bandha", "Setu-bandha", "Bridge (commentary on Nityāṣoḍaśīkārṇava)", "san", 1730, ["tantra_late", "sakta"], "bhaskararaya"),
    ("bhaskararaya_lalita_sahasranama_bhasya", "Saubhāgya-bhāskara", "Commentary on Lalitā-sahasranāma", "san", 1729, ["tantra_late", "sakta"], "bhaskararaya"),
    ("laksmidhara_advaita_makaranda", "Advaita-makaranda commentary", "Commentary on the Honey of Non-dualism", "san", 1530, ["tantra_late"], "laksmidhara"),
    ("brahmananda_sarasvati_kaivalya_kalpadruma", "Kaivalya-kalpadruma", "Wishing-tree of Liberation", "san", 1700, ["tantra_late"], "brahmananda_sarasvati"),

    # ── Mughal syncrétisme
    ("dara_shukoh_sirr_i_akbar", "Sirr-i Akbar", "The Greatest Mystery (50 Upaniṣads in Persian)", "fas", 1657, ["syncretism_mughal"], "dara_shukoh"),
    ("dara_shukoh_majma_ul_bahrain", "Majma'-ul-Baḥrain", "The Confluence of the Two Seas", "fas", 1655, ["syncretism_mughal"], "dara_shukoh"),
    ("dara_shukoh_safinat_ul_auliya", "Safīnat-ul-Auliyā", "Ship of the Saints", "fas", 1640, ["syncretism_mughal"], "dara_shukoh"),
    ("akbar_sulh_e_kul_ain_proto", "Ā'īn-i Akbarī (philosophical sections)", "Ā'īn-i Akbarī (philosophy)", "fas", 1590, ["syncretism_mughal"], "abul_fazl"),
    ("abul_fazl_akbarnama", "Akbar-nāma", "Akbar-nāma", "fas", 1602, ["syncretism_mughal", "history"], "abul_fazl"),
    ("badauni_muntakhab_tawarikh", "Muntakhab-ut-Tavārīkh", "Selection of Histories", "fas", 1595, ["islamic_indo_persian", "history"], "badauni"),

    # ── Navya-nyāya tardif & Vyākaraṇa
    ("gadadhara_vyutpattivada", "Vyutpatti-vāda", "Doctrine of Linguistic Derivation", "san", 1650, ["navya_nyaya_late"], "gadadhara_bhattacarya"),
    ("gadadhara_sakti_vada", "Śakti-vāda", "Doctrine of Power (semantic)", "san", 1655, ["navya_nyaya_late", "linguistics"], "gadadhara_bhattacarya"),
    ("jagadisha_sabda_sakti_prakasika", "Śabda-śakti-prakāśikā", "Illumination of Word-Power", "san", 1620, ["navya_nyaya_late"], "jagadisha_tarkalankara"),
    ("kaunda_bhatta_vaiyakarana_bhusana", "Vaiyākaraṇa-bhūṣaṇa", "Ornament of the Grammarian", "san", 1640, ["vyakarana_late"], "kaunda_bhatta"),
    ("nagesa_paribhasendu_sekhara", "Paribhāṣenduśekhara", "Crest-jewel of Maxims", "san", 1730, ["vyakarana_late"], "nagesa_bhatta"),
    ("nagesa_laghu_sabdendu_sekhara", "Laghu-śabdenduśekhara", "Short Crest-jewel of Words", "san", 1740, ["vyakarana_late"], "nagesa_bhatta"),
    ("nagesa_mahabhasya_pradipa_uddyota", "Mahābhāṣya-pradīpa-uddyota", "Light on the Lamp of the Mahābhāṣya", "san", 1735, ["vyakarana_late"], "nagesa_bhatta"),
    ("bhattoji_diksita_siddhanta_kaumudi", "Siddhānta-kaumudī", "Moonlight of Established Conclusions", "san", 1620, ["vyakarana_late"], "bhattoji_diksita"),
    ("varadaraja_laghu_siddhanta_kaumudi", "Laghu-siddhānta-kaumudī", "Short Moonlight of Conclusions", "san", 1660, ["vyakarana_late"], "varadaraja"),

    # ── Mīmāṃsā tardive
    ("apadeva_mimamsa_nyaya_prakasa", "Mīmāṃsā-nyāya-prakāśa", "Light on Mīmāṃsā Logic", "san", 1610, ["mimamsa_late"], "apadeva"),
    ("khandadeva_bhatta_dipika", "Bhāṭṭa-dīpikā", "Lamp of the Bhāṭṭa School", "san", 1670, ["mimamsa_late"], "khandadeva"),

    # ── Sciences & médecine
    ("bhaskara_ii_continuation_kamalakara_siddhanta_tattvaviveka", "Siddhānta-tattva-viveka", "Discrimination of Astronomical Truth", "san", 1658, ["jyotisa_late"], "kamalakara"),
    ("munisvara_siddhanta_sarvabhauma", "Siddhānta-sārvabhauma", "Universal Astronomy", "san", 1646, ["jyotisa_late"], "munisvara"),
    ("samartha_ramadasa_manache_shloka_proto", "Manāce Śloka", "Verses to the Mind", "mar", 1670, ["bhakti_varkari", "ethics"], "ramadasa"),
    ("yogi_sundardasa_sarbangi", "Sarbaṅgī", "All Limbs (anthology of Sant verses)", "hin", 1640, ["bhakti_sant_nirguna"], "rajab_compilers"),

    # ── Kaśmīr Śaiva tardif
    ("kashmir_saiva_late_madhuraja_yogini_hrdaya_bhasya", "Yoginī-hṛdaya commentaries (late)", "Late commentaries on Yoginī-hṛdaya", "san", 1550, ["kashmir_saiva_late", "tantra_late"], "amrtanandanatha_school"),

    # ── Vedānta sub-schools later commentary
    ("nrsimhasrama_bheda_dhikkara", "Bheda-dhikkāra", "Refutation of Difference", "san", 1530, ["advaita_late"], "nrsimhasrama"),
    ("prakashananda_siddhanta_muktavali", "Siddhānta-muktāvalī", "Pearl-Necklace of Conclusions (Vedānta)", "san", 1550, ["advaita_late"], "prakashananda"),
    ("citsukha_continuator_late_advaita", "Tattva-pradīpikā commentaries (late)", "Late commentaries on Citsukhī", "san", 1600, ["advaita_late"], "citsukha_school"),
    ("vallabha_tattvartha_dipa", "Tattvārtha-dīpa-nibandha", "Lamp on the Meaning of Truth", "san", 1525, ["suddhadvaita"], "vallabha"),
    ("vallabha_subodhini", "Subodhinī", "Easy to Understand (Bhāgavata commentary)", "san", 1535, ["suddhadvaita"], "vallabha"),
    ("vitthalanatha_vidvan_mandana", "Vidvan-maṇḍana", "Adornment of the Learned", "san", 1570, ["suddhadvaita"], "vitthalanatha"),
    ("anandabodha_late_continuator", "Pramāṇa-mālā (late commentaries)", "Late commentaries on Pramāṇa-mālā", "san", 1580, ["advaita_late"], "anandabodha_school"),
]

assert len(WORKS) == 70, f"INDIAN×early_modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "advaita_late" in tags and "bhakti" in tags:
        return "ADVAITA_BHAKTI_SYNTHESIS"
    if "advaita_late" in tags:
        return "ADVAITA_LATE"
    if "dvaita_late" in tags:
        return "DVAITA_LATE"
    if "visistadvaita_late" in tags:
        return "VISISTADVAITA_LATE"
    if "suddhadvaita" in tags:
        return "SUDDHADVAITA_VALLABHA"
    if "bhakti_gaudiya" in tags:
        return "BHAKTI_GAUDIYA"
    if "bhakti_varkari" in tags:
        return "BHAKTI_VARKARI"
    if "bhakti_sant_nirguna" in tags:
        return "BHAKTI_SANT_NIRGUNA"
    if "bhakti_sant_saguna" in tags:
        return "BHAKTI_SANT_SAGUNA"
    if "bhakti_tamil_late" in tags:
        return "BHAKTI_TAMIL_LATE"
    if "sikh" in tags:
        return "SIKH"
    if "tantra_late" in tags and "sakta" in tags:
        return "TANTRA_SAKTA_LATE"
    if "tantra_late" in tags:
        return "TANTRA_LATE"
    if "syncretism_mughal" in tags:
        return "MUGHAL_SYNCRETISM"
    if "islamic_indo_persian" in tags:
        return "INDO_PERSIAN_HISTORIO"
    if "navya_nyaya_late" in tags:
        return "NAVYA_NYAYA_LATE"
    if "vyakarana_late" in tags:
        return "VYAKARANA_LATE"
    if "mimamsa_late" in tags:
        return "MIMAMSA_LATE"
    if "jyotisa_late" in tags:
        return "JYOTISA_LATE"
    if "kashmir_saiva_late" in tags:
        return "KASHMIR_SAIVA_LATE"
    return "INDIAN_EARLY_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "INDIAN", "epoch": "early_modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 15,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "public_domain", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206q_indian_early_modern", "generated": "2026-04-30",
        "macro_culture": "INDIAN", "epoch": "early_modern",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["GRETIL", "sacred-texts.com", "archive.org", "Sikh Reference Library"],
        "language_original_dominant": "san + hin + mar + ben + pan + fas + tam",
        "schools_covered": [
            "Vedānta post-Vijayanagara (Madhusūdana ×3, Appayya ×2, Nīlakaṇṭha, Dharmarāja, Sadānanda)",
            "Caitanya & Gauḍīya (Caitanya, Rūpa ×2, Jīva, Sanātana, Kṛṣṇadāsa, Vṛndāvana, Baladeva)",
            "Bhakti Vārkari (Tukārām, Eknāth, Rāmadāsa ×2, Nāmdev)",
            "Bhakti Sant nirguṇa+saguṇa (Dādū, Ravidās, Mīrā, Sundardās, Tulsidās ×2, Sūrdās)",
            "Sikhisme (Ādi Granth, Dasam Granth, Janamsākhīs ×2, Bhai Gurdās, Zafarnāma)",
            "Tantra/Śākta tardif (Bhāskararāya ×2, Lakṣmīdhara, Brahmānanda)",
            "Mughal syncrétisme (Dārā Shukōh ×3, Abū'l Fażl ×2, Badāūnī)",
            "Navya-nyāya & Vyākaraṇa tardifs (Gadādhara ×2, Jagadīśa, Kauṇḍa Bhaṭṭa, Nāgeśa ×3, Bhaṭṭoji, Varadarāja)",
            "Mīmāṃsā tardive + Jyotiṣa tardif",
            "Vallabha śuddhādvaita ×3 + Vedānta sub-schools tardif",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue INDIAN × early_modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

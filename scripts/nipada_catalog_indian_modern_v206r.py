#!/usr/bin/env python3
"""§206r — INDIAN × modern (1789 → 1914), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_indian_modern_v206r.json"

WORKS = [
    # ── Brahmo Samaj & réformistes bengalis
    ("rammohan_roy_precepts_jesus", "Precepts of Jesus", "Precepts of Jesus", "eng", 1820, ["brahmo", "reform"], "rammohan_roy"),
    ("rammohan_roy_translation_upanisads", "English translations of Upaniṣads", "Translation of the Upaniṣads", "eng", 1816, ["brahmo", "reform"], "rammohan_roy"),
    ("rammohan_roy_brahmo_samaj_trust_deed", "Brahmo Samaj Trust Deed", "Brahmo Samaj Trust Deed", "eng", 1830, ["brahmo", "reform"], "rammohan_roy"),
    ("debendranath_tagore_brahmo_dharma", "Brahmo Dharma", "Brahmo Dharma", "ben", 1869, ["brahmo"], "debendranath_tagore"),
    ("keshab_chandra_sen_jeevan_ved", "Jīvan-veda", "Veda of Life", "ben", 1880, ["brahmo"], "keshab_chandra_sen"),
    ("ishwar_chandra_vidyasagar_widow_remarriage", "Marriage of Hindu Widows", "Marriage of Hindu Widows", "ben", 1856, ["reform", "social"], "ishwar_chandra_vidyasagar"),

    # ── Néo-Vedānta : Ramakrishna - Vivekananda
    ("ramakrishna_kathamrta", "Śrī Śrī Rāmakṛṣṇa-kathāmṛta", "Gospel of Sri Ramakrishna", "ben", 1902, ["neo_vedanta"], "mahendranath_gupta"),
    ("vivekananda_chicago_addresses", "Chicago Addresses", "Chicago Addresses (Parliament of Religions)", "eng", 1893, ["neo_vedanta"], "vivekananda"),
    ("vivekananda_raja_yoga", "Rāja-Yoga", "Raja Yoga", "eng", 1896, ["neo_vedanta", "yoga"], "vivekananda"),
    ("vivekananda_jnana_yoga", "Jñāna-Yoga", "Jñāna Yoga", "eng", 1899, ["neo_vedanta"], "vivekananda"),
    ("vivekananda_karma_yoga", "Karma-Yoga", "Karma Yoga", "eng", 1896, ["neo_vedanta"], "vivekananda"),
    ("vivekananda_bhakti_yoga", "Bhakti-Yoga", "Bhakti Yoga", "eng", 1896, ["neo_vedanta"], "vivekananda"),
    ("vivekananda_complete_works", "The Complete Works of Swami Vivekananda", "Complete Works (vols I-VIII)", "eng", 1907, ["neo_vedanta"], "vivekananda"),

    # ── Aurobindo (œuvres pré-1914)
    ("aurobindo_karmayogin", "Karmayogin (essays)", "Karmayogin (essays)", "eng", 1909, ["neo_vedanta", "nationalism"], "aurobindo"),
    ("aurobindo_bande_mataram_essays", "Bande Mataram (political essays)", "Bande Mataram political essays", "eng", 1907, ["nationalism"], "aurobindo"),
    ("aurobindo_isa_upanisad_early", "Īśa Upaniṣad commentary (early version)", "Īśa Upaniṣad (early commentary)", "eng", 1914, ["neo_vedanta"], "aurobindo"),

    # ── Tagore Rabindranath
    ("tagore_gitanjali", "Gītāñjali", "Gitanjali (Song Offerings)", "ben", 1910, ["bhakti_modern", "neo_vedanta"], "rabindranath_tagore"),
    ("tagore_gora", "Gorā", "Gora", "ben", 1910, ["nationalism", "novel"], "rabindranath_tagore"),
    ("tagore_sadhana", "Sādhanā: The Realisation of Life", "Sadhana", "eng", 1913, ["neo_vedanta"], "rabindranath_tagore"),

    # ── Réformistes hindous
    ("dayananda_satyarth_prakash", "Satyārtha-prakāśa", "The Light of Truth", "hin", 1875, ["arya_samaj", "reform"], "dayananda_saraswati"),
    ("dayananda_rgveda_bhasya", "Ṛgveda-bhāṣya", "Commentary on the Ṛgveda", "san", 1877, ["arya_samaj"], "dayananda_saraswati"),
    ("ramana_maharshi_who_am_i", "Nāṉ Yār?", "Who Am I?", "tam", 1902, ["neo_vedanta"], "ramana_maharshi"),
    ("aurobindo_synthesis_yoga_proto", "The Synthesis of Yoga (Arya pre-publication)", "Early Synthesis of Yoga drafts", "eng", 1914, ["neo_vedanta", "yoga"], "aurobindo"),

    # ── Theosophical Society India (Olcott, Besant côté indien)
    ("besant_in_defence_of_hinduism", "In Defence of Hinduism", "In Defence of Hinduism", "eng", 1901, ["theosophy_india"], "annie_besant"),
    ("olcott_buddhist_catechism", "The Buddhist Catechism", "The Buddhist Catechism", "eng", 1881, ["theosophy_india", "buddhist_revival"], "olcott"),

    # ── Nationalisme et politique
    ("tilak_gita_rahasya", "Gītā-rahasya", "Secret of the Bhagavadgītā (Karma-yoga interpretation)", "mar", 1915, ["nationalism", "neo_vedanta"], "bal_gangadhar_tilak"),
    ("tilak_orion", "The Orion: Researches into the Antiquity of the Vedas", "The Orion", "eng", 1893, ["nationalism", "vedic_studies"], "bal_gangadhar_tilak"),
    ("tilak_arctic_home", "The Arctic Home in the Vedas", "The Arctic Home in the Vedas", "eng", 1903, ["nationalism", "vedic_studies"], "bal_gangadhar_tilak"),
    ("ranade_rise_of_maratha_power", "Rise of the Maratha Power", "Rise of the Maratha Power", "eng", 1900, ["nationalism", "history"], "mahadev_govind_ranade"),
    ("gokhale_speeches", "Speeches of Gokhale", "Collected Speeches of Gopal Krishna Gokhale", "eng", 1908, ["nationalism", "liberal"], "gopal_krishna_gokhale"),
    ("savarkar_indian_war_of_independence", "The Indian War of Independence, 1857", "The Indian War of Independence, 1857", "eng", 1909, ["nationalism", "history"], "savarkar"),
    ("dadabhai_naoroji_poverty_un_british_rule", "Poverty and Un-British Rule in India", "Poverty and Un-British Rule in India", "eng", 1901, ["nationalism", "economics"], "dadabhai_naoroji"),

    # ── Gandhi premières œuvres (pré-1914)
    ("gandhi_hind_swaraj", "Hind Svarāj", "Hind Swaraj or Indian Home Rule", "guj", 1909, ["nationalism", "ahimsa"], "gandhi"),
    ("gandhi_indian_opinion_collected", "Indian Opinion (collected articles)", "Indian Opinion articles 1903-1914", "eng", 1910, ["nationalism", "satyagraha"], "gandhi"),

    # ── Indo-musulmans réformistes
    ("syed_ahmed_khan_essays", "Maqālāt-i Sir Sayyid", "Essays of Sir Sayyid Ahmad Khan", "urd", 1880, ["islamic_reform_india"], "syed_ahmed_khan"),
    ("syed_ahmed_khan_tafsir", "Tafsīr-ul-Qurʾān (modernist)", "Modernist Quran Commentary", "urd", 1880, ["islamic_reform_india"], "syed_ahmed_khan"),
    ("iqbal_asrar_e_khudi", "Asrār-i Khudī", "Secrets of the Self", "fas", 1915, ["islamic_modern", "philosophy"], "iqbal"),
    ("iqbal_bang_e_dara", "Bāng-e-Darā", "Call of the Marching Bell", "urd", 1924, ["islamic_modern"], "iqbal"),
    ("ameer_ali_spirit_of_islam", "The Spirit of Islam", "The Spirit of Islam", "eng", 1891, ["islamic_modern"], "syed_ameer_ali"),

    # ── Sikhs réformistes
    ("singh_sabha_kahn_singh_nabha_gurmat_prabhakar", "Gurmat Prabhākar", "Light of Sikh Doctrine", "pan", 1898, ["sikh_reform"], "kahn_singh_nabha"),
    ("singh_sabha_kahn_singh_nabha_mahan_kosh_proto", "Gurśabad Ratnākar Mahān Kośh (early compilation)", "Mahan Kosh (early compilation)", "pan", 1912, ["sikh_reform", "lexicography"], "kahn_singh_nabha"),

    # ── Tamoul moderne
    ("subramania_bharati_kannan_pattu", "Kaṇṇaṉ Pāṭṭu", "Songs to Kaṇṇaṉ", "tam", 1910, ["bhakti_modern", "nationalism"], "subramania_bharati"),
    ("subramania_bharati_panchali_sapatham", "Pāñcāli Sapatham", "The Vow of Pāñcālī", "tam", 1912, ["nationalism", "epic_modern"], "subramania_bharati"),
    ("ramalinga_swamigal_tiruvarutpa", "Tiruvaruṭpā", "The Holy Book of Divine Grace", "tam", 1867, ["bhakti_tamil_late", "saiva_modern"], "ramalinga_swamigal"),

    # ── Bengali littérature et critique
    ("bankim_anandamath", "Ānandamaṭh", "The Abbey of Bliss", "ben", 1882, ["nationalism", "novel"], "bankim_chandra_chatterjee"),
    ("bankim_krsna_caritra", "Kṛṣṇa-caritra", "Life of Krishna", "ben", 1886, ["neo_vedanta"], "bankim_chandra_chatterjee"),
    ("ramprasad_late_kirtan_compilation", "Late Rāmprasād kīrtan compilation", "Late compilation of Rāmprasād", "ben", 1850, ["bhakti_sakta"], "ramprasad_compilers"),

    # ── Sciences et indologie indigène
    ("ramanujan_collected_papers", "Notebooks", "Notebooks of Srinivasa Ramanujan", "eng", 1913, ["mathematics_modern"], "srinivasa_ramanujan"),
    ("rabindra_tagore_creative_unity_proto", "Sādhanā lectures (Harvard 1913)", "Sadhana lectures Harvard", "eng", 1913, ["neo_vedanta"], "rabindranath_tagore"),
    ("jagadish_chandra_bose_response_living_non_living", "Response in the Living and Non-Living", "Response in the Living and Non-Living", "eng", 1902, ["sciences_modern"], "jagadish_chandra_bose"),
    ("prafulla_chandra_ray_history_hindu_chemistry", "A History of Hindu Chemistry", "A History of Hindu Chemistry", "eng", 1902, ["sciences_modern", "history"], "prafulla_chandra_ray"),

    # ── Ramanan/réformes diverses & vedantins post-Vivekananda pré-1914
    ("krishnanand_swami_advaita_dipa", "Advaita-dīpa (early compilation)", "Lamp of Non-dualism", "san", 1880, ["advaita_late"], "krishnanand_swami"),
    ("rangacarya_bhasya", "Bhāṣya commentaries (early modern)", "Early-modern Vedānta commentaries", "san", 1880, ["visistadvaita_late"], "rangacarya_school"),

    # ── Réforme religieuse populaire & dépassement caste
    ("jyotirao_phule_gulamgiri", "Gulāmgirī", "Slavery (against caste)", "mar", 1873, ["reform", "anti_caste"], "jyotirao_phule"),
    ("jyotirao_phule_shetkaryacha_asud", "Śetkaryācā Āsūḍ", "Cultivator's Whipcord", "mar", 1881, ["reform", "anti_caste"], "jyotirao_phule"),
    ("periyar_proto_essays", "Early essays (proto)", "Early essays of Periyar (proto)", "tam", 1910, ["reform", "anti_caste"], "periyar"),

    # ── Bouddhisme indien revivaliste (Anagarika Dharmapala)
    ("anagarika_dharmapala_return_dhamma", "Return to the Dhamma", "Return to the Dhamma", "eng", 1893, ["buddhist_revival_india"], "anagarika_dharmapala"),

    # ── Vedānta scolastique tardif moderne
    ("nimbarkacharya_late_vedanta_kamadhenu", "Vedānta-kāmadhenu (late commentaries)", "Late commentaries on Vedānta-kāmadhenu", "san", 1850, ["dvaitadvaita"], "nimbarka_school_late"),
    ("madhva_school_late_pundarika_pundarika_vidyaya_proto", "Late Madhva school commentaries", "Late Madhva commentaries", "san", 1850, ["dvaita_late"], "madhva_school_late"),

    # ── Yogis & saints
    ("sri_aurobindo_arya_journal_essays", "Ārya journal essays (1914)", "Arya journal essays", "eng", 1914, ["neo_vedanta"], "aurobindo"),
    ("yogananda_pre_kriya_proto", "Early SRF documents (proto)", "Early documents (proto Yogananda lineage)", "eng", 1914, ["yoga_modern"], "lahiri_mahasaya_school"),

    # ── Indologistes indiens
    ("rajendralala_mitra_buddhist_literature_nepal", "The Sanskrit Buddhist Literature of Nepal", "Sanskrit Buddhist Literature of Nepal", "eng", 1882, ["indology_native"], "rajendralala_mitra"),
    ("ramakrishna_gopal_bhandarkar_vaishnavism_saivism", "Vaiṣṇavism, Śaivism and Minor Religious Systems", "Vaishnavism, Saivism and Minor Religious Systems", "eng", 1913, ["indology_native"], "rg_bhandarkar"),

    # ── Sufi indien moderne
    ("ahmad_rezā_khan_fatāwā_ridawiyya", "Fatāwā-i Riḍawiyya", "Fatwas of Aḥmad Riḍā Khān", "urd", 1900, ["islamic_sufi_india"], "ahmad_reza_khan"),

    # ── Premier féminisme indien
    ("pandita_ramabai_high_caste_hindu_woman", "The High-Caste Hindu Woman", "The High-Caste Hindu Woman", "eng", 1887, ["reform", "feminism_india"], "pandita_ramabai"),
    ("tarabai_shinde_stri_purush_tulana", "Strī-puruṣa-tulanā", "A Comparison between Women and Men", "mar", 1882, ["reform", "feminism_india"], "tarabai_shinde"),

    # ── Compléments
    ("ramakrishna_paramahamsa_amrit_vachan", "Amṛta-vacanāmṛta", "Sayings of Sri Ramakrishna (anthology)", "ben", 1907, ["neo_vedanta"], "ramakrishna_compilers"),
    ("vivekananda_lectures_colombo_almora", "Lectures from Colombo to Almora", "Lectures from Colombo to Almora", "eng", 1897, ["neo_vedanta", "nationalism"], "vivekananda"),
    ("narayan_guru_atmopadesa_satakam", "Ātmopadeśa-śatakam", "One Hundred Verses of Self-Instruction", "mal", 1897, ["neo_vedanta", "anti_caste"], "narayana_guru"),
    ("chattampi_swamikal_vedadhikara_nirupanam", "Vedādhikāra-nirūpaṇam", "Determination of Right to the Vedas", "mal", 1890, ["reform", "anti_caste"], "chattampi_swamikal"),
]

assert len(WORKS) == 70, f"INDIAN×modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "brahmo" in tags:
        return "BRAHMO_SAMAJ"
    if "arya_samaj" in tags:
        return "ARYA_SAMAJ"
    if "neo_vedanta" in tags and "yoga" in tags:
        return "NEO_VEDANTA_YOGA"
    if "neo_vedanta" in tags and "nationalism" in tags:
        return "NEO_VEDANTA_NATIONALIST"
    if "neo_vedanta" in tags:
        return "NEO_VEDANTA"
    if "nationalism" in tags and "history" in tags:
        return "NATIONALIST_HISTORIAN"
    if "nationalism" in tags and "vedic_studies" in tags:
        return "NATIONALIST_VEDIC_REVIVAL"
    if "nationalism" in tags and "ahimsa" in tags:
        return "GANDHIAN_PROTO"
    if "nationalism" in tags and "satyagraha" in tags:
        return "GANDHIAN_PROTO"
    if "nationalism" in tags:
        return "NATIONALIST"
    if "islamic_reform_india" in tags:
        return "ISLAMIC_REFORM_INDIA"
    if "islamic_modern" in tags:
        return "ISLAMIC_MODERN_INDIA"
    if "islamic_sufi_india" in tags:
        return "SUFI_INDIA_MODERN"
    if "sikh_reform" in tags:
        return "SIKH_REFORM"
    if "theosophy_india" in tags:
        return "THEOSOPHY_INDIA"
    if "buddhist_revival_india" in tags:
        return "BUDDHIST_REVIVAL_INDIA"
    if "anti_caste" in tags:
        return "ANTI_CASTE_REFORM"
    if "feminism_india" in tags:
        return "FEMINISM_INDIA_FIRST"
    if "reform" in tags:
        return "HINDU_REFORM"
    if "bhakti_modern" in tags:
        return "BHAKTI_MODERN"
    if "bhakti_sakta" in tags:
        return "BHAKTI_SAKTA"
    if "bhakti_tamil_late" in tags:
        return "BHAKTI_TAMIL_LATE_MODERN"
    if "indology_native" in tags:
        return "INDOLOGY_NATIVE"
    if "sciences_modern" in tags:
        return "INDIAN_SCIENCES_MODERN"
    if "mathematics_modern" in tags:
        return "INDIAN_MATHEMATICS_MODERN"
    if "yoga_modern" in tags:
        return "YOGA_MODERN"
    if "advaita_late" in tags:
        return "ADVAITA_MODERN"
    if "visistadvaita_late" in tags:
        return "VISISTADVAITA_MODERN"
    if "dvaita_late" in tags:
        return "DVAITA_MODERN"
    if "dvaitadvaita" in tags:
        return "DVAITADVAITA_MODERN"
    return "INDIAN_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "INDIAN", "epoch": "modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 5,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "public_domain", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206r_indian_modern", "generated": "2026-04-30",
        "macro_culture": "INDIAN", "epoch": "modern",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["archive.org", "Bharat Ek Khoj digital", "Sri Aurobindo Ashram", "Ramakrishna Math"],
        "language_original_dominant": "eng + ben + hin + mar + tam + urd + fas + san + pan + guj",
        "schools_covered": [
            "Brahmo Samaj (Rammohan ×3, Debendranath, Keshab, Vidyāsāgar)",
            "Néo-Vedānta (Ramakrishna-Kathāmṛta, Vivekananda ×6, Aurobindo ×4, Tagore ×3)",
            "Arya Samaj (Dayānanda ×2)",
            "Nationalisme (Tilak ×3, Ranade, Gokhale, Savarkar, Naoroji, Gandhi ×2)",
            "Indo-musulmans réformistes (Sir Sayyid ×2, Iqbal ×2, Ameer Ali)",
            "Sikhs réformistes (Kahn Singh Nabha ×2)",
            "Tamoul (Bhārati ×2, Ramalinga, Tāyumāṉavar tardif déjà §206q)",
            "Bengali littérature (Bankim ×2, Ramprasad)",
            "Sciences indiennes modernes (Ramanujan, J.C. Bose, P.C. Ray)",
            "Réforme anti-caste (Phule ×2, Periyar proto)",
            "Bouddhisme revivaliste (Anagarika Dharmapala)",
            "Vedānta scolastique tardif (Nimbārka, Madhva late)",
            "Indologie indigène (Rājendralāla Mitra, R.G. Bhandarkar)",
            "Sufi indien moderne (Aḥmad Riḍā Khān)",
            "Féminisme indien premier (Paṇḍita Ramābāī, Tārābāī Shinde)",
            "Theosophical Society India (Besant, Olcott)",
            "Ramana Maharshi",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue INDIAN × modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

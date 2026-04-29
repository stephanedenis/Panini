#!/usr/bin/env python3
"""
§206j — Catalogue ISLAMIC × medieval (600 → 1500 CE), 70 œuvres.

Strates :
- Sources fondatrices VIIᵉ siècle : Qurʾān (texte canonique uthmanien),
  Ḥadīth majeurs (al-Bukhārī, Muslim, Abū Dāwūd, al-Tirmidhī, al-Nasāʾī, Ibn Māja)
- Tafsīr classique : al-Ṭabarī, al-Zamakhsharī, al-Rāzī Mafātīḥ al-Ghayb,
  al-Qurṭubī, Ibn Kathīr
- Fiqh / uṣūl : al-Shāfiʿī Risāla, Mālik Muwaṭṭaʾ, Ibn Ḥanbal Musnad,
  al-Sarakhsī Mabsūṭ, Ibn Qudāma Mughnī
- Kalām : al-Ashʿarī, al-Bāqillānī, al-Juwaynī, al-Shahrastānī, al-Māturīdī
- Falsafa : al-Kindī, al-Fārābī, Ibn Sīnā, Ibn Rushd, al-Rāzī (médecin),
  Ibn Ṭufayl, Ibn Bājja, Ibn Ḥazm, Suhrawardī, Ibn ʿArabī, Mullā Ṣadrā début
- Soufisme : al-Muḥāsibī, al-Junayd (Rasāʾil), al-Sarrāj, al-Qushayrī,
  al-Hujwīrī, al-Ghazālī Iḥyāʾ + connexes, Rūmī, ʿAṭṭār, Saʿdī, Ḥāfiẓ,
  Ibn ʿAṭāʾ Allāh
- Histoire/sociologie/geographie : al-Masʿūdī, Ibn al-Athīr, Ibn Khaldūn,
  Yāqūt, al-Bīrūnī Hind, Rashīd al-Dīn Jāmiʿ al-Tawārīkh
- Sciences : al-Khwārizmī Algèbre, Ibn al-Haytham Manāẓir, al-Bīrūnī Tafhīm,
  ʿUmar Khayyām Algèbre, al-Tūsī Tadhkira

Sources : al-mostafa.com, shamela.ws, sacred-texts (Sale Coran, Whinfield,
Khayyam), archive.org (G.A.L.).
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_islamic_medieval_v206j.json"

WORKS = [
    # ── Sources fondatrices
    ("quran", "al-Qurʾān al-Karīm", "The Noble Qurʾān (Uthmanic recension)", "ara", 650, ["quran"], None),
    ("bukhari_sahih", "al-Jāmiʿ al-Ṣaḥīḥ (al-Bukhārī)", "Ṣaḥīḥ al-Bukhārī", "ara", 870, ["hadith"], "al_bukhari"),
    ("muslim_sahih", "Ṣaḥīḥ Muslim", "Ṣaḥīḥ Muslim", "ara", 875, ["hadith"], "muslim_ibn_hajjaj"),
    ("abu_dawud_sunan", "Sunan Abī Dāwūd", "Sunan of Abū Dāwūd", "ara", 888, ["hadith"], "abu_dawud"),
    ("tirmidhi_jami", "Jāmiʿ al-Tirmidhī", "Sunan al-Tirmidhī", "ara", 884, ["hadith"], "al_tirmidhi"),
    ("nasai_sunan", "Sunan al-Nasāʾī", "Sunan al-Nasāʾī", "ara", 905, ["hadith"], "al_nasai"),
    ("ibn_maja_sunan", "Sunan Ibn Māja", "Sunan Ibn Māja", "ara", 887, ["hadith"], "ibn_maja"),
    ("malik_muwatta", "al-Muwaṭṭaʾ", "Mālik's Muwaṭṭaʾ", "ara", 795, ["hadith", "fiqh"], "malik_ibn_anas"),
    ("ahmad_musnad", "Musnad Aḥmad", "Musnad of Ibn Ḥanbal", "ara", 855, ["hadith"], "ibn_hanbal"),

    # ── Tafsīr
    ("tabari_tafsir", "Jāmiʿ al-Bayān (Tafsīr al-Ṭabarī)", "al-Ṭabarī's Comprehensive Exegesis", "ara", 920, ["tafsir"], "al_tabari"),
    ("zamakhshari_kashshaf", "al-Kashshāf", "The Unveiler", "ara", 1144, ["tafsir", "mutazila"], "al_zamakhshari"),
    ("razi_mafatih_ghayb", "Mafātīḥ al-Ghayb", "Keys to the Unseen", "ara", 1210, ["tafsir", "kalam"], "fakhr_al_din_razi"),
    ("qurtubi_jami_ahkam", "al-Jāmiʿ li-Aḥkām al-Qurʾān", "Compendium of Qurʾānic Rulings", "ara", 1273, ["tafsir", "fiqh"], "al_qurtubi"),
    ("ibn_kathir_tafsir", "Tafsīr Ibn Kathīr", "Ibn Kathīr's Exegesis", "ara", 1373, ["tafsir"], "ibn_kathir"),

    # ── Histoire / Sīra
    ("ibn_ishaq_sira", "Sīrat Rasūl Allāh", "Life of the Messenger of God", "ara", 770, ["sira", "history"], "ibn_ishaq"),
    ("tabari_tarikh", "Tārīkh al-Rusul wa-l-Mulūk", "History of Prophets and Kings", "ara", 915, ["history"], "al_tabari"),
    ("masudi_muruj_dhahab", "Murūj al-Dhahab", "Meadows of Gold", "ara", 947, ["history", "geography"], "al_masudi"),
    ("ibn_athir_kamil", "al-Kāmil fī al-Tārīkh", "The Complete History", "ara", 1231, ["history"], "ibn_al_athir"),
    ("ibn_khaldun_muqaddima", "al-Muqaddima", "Prolegomena", "ara", 1377, ["history", "sociology"], "ibn_khaldun"),
    ("rashid_al_din_jami_tawarikh", "Jāmiʿ al-Tawārīkh", "Compendium of Chronicles", "fas", 1310, ["history"], "rashid_al_din"),

    # ── Fiqh / Uṣūl
    ("shafii_risala", "al-Risāla", "al-Shāfiʿī's Epistle on Legal Theory", "ara", 815, ["fiqh", "usul"], "al_shafii"),
    ("sarakhsi_mabsut", "al-Mabsūṭ", "The Extensive (Hanafi)", "ara", 1090, ["fiqh", "hanafi"], "al_sarakhsi"),
    ("ibn_qudama_mughni", "al-Mughnī", "The Sufficient (Hanbali)", "ara", 1223, ["fiqh", "hanbali"], "ibn_qudama"),
    ("ghazali_mustasfa", "al-Mustaṣfā min ʿIlm al-Uṣūl", "The Distilled Essence of Legal Theory", "ara", 1109, ["usul", "fiqh"], "al_ghazali"),
    ("ibn_taymiyya_majmu_fatawa", "Majmūʿ al-Fatāwā", "Collected Fatwas", "ara", 1320, ["fiqh", "salafi"], "ibn_taymiyya"),

    # ── Kalām
    ("ashari_ibana", "al-Ibāna ʿan Uṣūl al-Diyāna", "Elucidation of the Foundations of Religion", "ara", 935, ["kalam", "ashari"], "al_ashari"),
    ("ashari_maqalat", "Maqālāt al-Islāmiyyīn", "Discourses of the Muslims", "ara", 935, ["kalam"], "al_ashari"),
    ("baqillani_tamhid", "al-Tamhīd", "The Introduction (Ash'arī)", "ara", 1010, ["kalam", "ashari"], "al_baqillani"),
    ("juwayni_irshad", "Kitāb al-Irshād", "Book of Guidance", "ara", 1080, ["kalam", "ashari"], "al_juwayni"),
    ("shahrastani_milal", "al-Milal wa-l-Niḥal", "Religions and Sects", "ara", 1127, ["kalam", "doxography"], "al_shahrastani"),
    ("maturidi_tawhid", "Kitāb al-Tawḥīd", "Book of Divine Unity", "ara", 940, ["kalam", "maturidi"], "al_maturidi"),
    ("abd_al_jabbar_mughni", "al-Mughnī fī Abwāb al-Tawḥīd", "The Sufficient on Topics of Unity (Mu'tazilī)", "ara", 1020, ["kalam", "mutazila"], "abd_al_jabbar"),

    # ── Falsafa (philosophie hellénisée)
    ("kindi_falsafa_ula", "Risāla fī al-Falsafa al-Ūlā", "On First Philosophy", "ara", 860, ["falsafa"], "al_kindi"),
    ("farabi_madina_fadila", "Ārāʾ Ahl al-Madīna al-Fāḍila", "Opinions of the People of the Virtuous City", "ara", 942, ["falsafa", "politics"], "al_farabi"),
    ("farabi_ihsa_ulum", "Iḥṣāʾ al-ʿUlūm", "Enumeration of the Sciences", "ara", 945, ["falsafa"], "al_farabi"),
    ("farabi_kitab_huruf", "Kitāb al-Ḥurūf", "Book of Letters", "ara", 940, ["falsafa", "logic"], "al_farabi"),
    ("ibn_sina_shifa_metaphysics", "al-Shifāʾ (al-Ilāhiyyāt)", "The Healing — Metaphysics", "ara", 1027, ["falsafa", "metaphysics"], "ibn_sina"),
    ("ibn_sina_najat", "Kitāb al-Najāt", "Book of Salvation", "ara", 1027, ["falsafa"], "ibn_sina"),
    ("ibn_sina_isharat", "al-Ishārāt wa-l-Tanbīhāt", "Pointers and Reminders", "ara", 1030, ["falsafa", "mysticism"], "ibn_sina"),
    ("ibn_sina_qanun", "al-Qānūn fī al-Ṭibb", "Canon of Medicine", "ara", 1025, ["medicine"], "ibn_sina"),
    ("razi_medicus_hawi", "al-Ḥāwī fī al-Ṭibb", "The Comprehensive Book of Medicine", "ara", 920, ["medicine"], "abu_bakr_al_razi"),
    ("razi_medicus_shukuk", "al-Shukūk ʿalā Jālīnūs", "Doubts about Galen", "ara", 920, ["medicine", "falsafa"], "abu_bakr_al_razi"),
    ("ghazali_tahafut_falasifa", "Tahāfut al-Falāsifa", "Incoherence of the Philosophers", "ara", 1095, ["kalam", "falsafa_critique"], "al_ghazali"),
    ("ghazali_munqidh", "al-Munqidh min al-Ḍalāl", "Deliverer from Error", "ara", 1108, ["sufism", "autobiography"], "al_ghazali"),
    ("ghazali_iqtisad", "al-Iqtiṣād fī al-Iʿtiqād", "Moderation in Belief", "ara", 1095, ["kalam"], "al_ghazali"),
    ("ibn_rushd_tahafut_tahafut", "Tahāfut al-Tahāfut", "Incoherence of the Incoherence", "ara", 1180, ["falsafa"], "ibn_rushd"),
    ("ibn_rushd_fasl_maqal", "Faṣl al-Maqāl", "Decisive Treatise", "ara", 1180, ["falsafa", "fiqh"], "ibn_rushd"),
    ("ibn_rushd_bidayat_mujtahid", "Bidāyat al-Mujtahid", "Beginning of the Independent Jurist", "ara", 1180, ["fiqh"], "ibn_rushd"),
    ("ibn_tufayl_hayy", "Ḥayy ibn Yaqẓān", "Living Son of the Vigilant", "ara", 1170, ["falsafa", "mysticism"], "ibn_tufayl"),
    ("ibn_bajja_tadbir", "Tadbīr al-Mutawaḥḥid", "Governance of the Solitary", "ara", 1135, ["falsafa", "politics"], "ibn_bajja"),
    ("ibn_hazm_fisal", "al-Fiṣal fī al-Milal", "Detailed Examination of Religions and Sects", "ara", 1060, ["kalam", "doxography"], "ibn_hazm"),
    ("suhrawardi_hikmat_ishraq", "Ḥikmat al-Ishrāq", "Philosophy of Illumination", "ara", 1186, ["falsafa", "ishraqi"], "suhrawardi"),

    # ── Soufisme
    ("muhasibi_riaya", "al-Riʿāya li-Ḥuqūq Allāh", "Observance of the Rights of God", "ara", 850, ["sufism"], "al_muhasibi"),
    ("junayd_rasail", "Rasāʾil al-Junayd", "Epistles of al-Junayd", "ara", 905, ["sufism"], "al_junayd"),
    ("sarraj_luma", "Kitāb al-Lumaʿ", "Book of Flashes", "ara", 988, ["sufism"], "al_sarraj"),
    ("qushayri_risala", "al-Risāla al-Qushayriyya", "Qushayrī's Epistle on Sufism", "ara", 1045, ["sufism"], "al_qushayri"),
    ("hujwiri_kashf_mahjub", "Kashf al-Maḥjūb", "Unveiling of the Veiled", "fas", 1075, ["sufism", "persian"], "al_hujwiri"),
    ("ghazali_ihya", "Iḥyāʾ ʿUlūm al-Dīn", "Revival of the Religious Sciences", "ara", 1105, ["sufism", "ethics"], "al_ghazali"),
    ("ibn_arabi_futuhat", "al-Futūḥāt al-Makkiyya", "The Meccan Openings", "ara", 1230, ["sufism", "metaphysics"], "ibn_arabi"),
    ("ibn_arabi_fusus", "Fuṣūṣ al-Ḥikam", "Bezels of Wisdom", "ara", 1229, ["sufism", "metaphysics"], "ibn_arabi"),
    ("ibn_ata_allah_hikam", "al-Ḥikam al-ʿAṭāʾiyya", "Aphorisms of Ibn ʿAṭāʾ Allāh", "ara", 1290, ["sufism", "shadhili"], "ibn_ata_allah"),
    ("rumi_mathnawi", "Mathnawī-i Maʿnawī", "Spiritual Couplets", "fas", 1273, ["sufism", "persian", "poetry"], "rumi"),
    ("attar_mantiq_tayr", "Manṭiq al-Ṭayr", "Conference of the Birds", "fas", 1177, ["sufism", "persian", "poetry"], "attar"),
    ("saadi_gulistan", "Gulistān", "The Rose Garden", "fas", 1258, ["literature", "ethics", "persian"], "saadi"),
    ("hafez_divan", "Dīwān-e Ḥāfeẓ", "Dīvān of Ḥāfeẓ", "fas", 1390, ["sufism", "persian", "poetry"], "hafez"),

    # ── Sciences
    ("khwarizmi_jabr", "al-Kitāb al-Mukhtaṣar fī Ḥisāb al-Jabr", "Compendious Book on Algebra", "ara", 825, ["math"], "al_khwarizmi"),
    ("ibn_haytham_manazir", "Kitāb al-Manāẓir", "Book of Optics", "ara", 1021, ["optics", "math"], "ibn_al_haytham"),
    ("biruni_hind", "Taḥqīq mā li-l-Hind", "India (Verification of What India Says)", "ara", 1030, ["history", "comparative"], "al_biruni"),
    ("biruni_tafhim", "al-Tafhīm", "Elements of Astrology", "ara", 1029, ["astronomy"], "al_biruni"),
    ("khayyam_jabr", "Risāla fī al-Barāhīn ʿalā Masāʾil al-Jabr", "Treatise on Demonstration of Algebra Problems", "ara", 1075, ["math"], "umar_khayyam"),
]

assert len(WORKS) == 70, f"ISLAMIC×medieval doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "quran" in tags:
        return "ISLAM_QURAN"
    if "hadith" in tags:
        return "ISLAM_HADITH"
    if "tafsir" in tags:
        return "ISLAM_TAFSIR"
    if "sira" in tags:
        return "ISLAM_SIRA"
    if "salafi" in tags:
        return "ISLAM_SALAFI"
    if "fiqh" in tags or "usul" in tags:
        return "ISLAM_FIQH"
    if "kalam" in tags:
        if "mutazila" in tags:
            return "ISLAM_MUTAZILA"
        if "ashari" in tags:
            return "ISLAM_ASHARI"
        if "maturidi" in tags:
            return "ISLAM_MATURIDI"
        return "ISLAM_KALAM"
    if "falsafa" in tags or "ishraqi" in tags or "falsafa_critique" in tags:
        return "ISLAM_FALSAFA"
    if "sufism" in tags:
        if "shadhili" in tags:
            return "ISLAM_SUFISM_SHADHILI"
        if "persian" in tags:
            return "ISLAM_SUFISM_PERSIAN"
        return "ISLAM_SUFISM"
    if "history" in tags or "sociology" in tags or "geography" in tags:
        return "ISLAM_HISTORY"
    if "math" in tags or "astronomy" in tags or "optics" in tags:
        return "ISLAM_SCIENCE"
    if "medicine" in tags:
        return "ISLAM_MEDICINE"
    if "doxography" in tags:
        return "ISLAM_DOXOGRAPHY"
    if "persian" in tags and "poetry" in tags:
        return "ISLAM_PERSIAN_LITERATURE"
    if "literature" in tags:
        return "ISLAM_LITERATURE"
    return "ISLAM_MEDIEVAL"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "ISLAMIC",
            "epoch": "medieval",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 30,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206j_islamic_medieval",
        "generated": "2026-04-29",
        "macro_culture": "ISLAMIC",
        "epoch": "medieval",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["al-mostafa.com", "shamela.ws", "sacred-texts (Sale Coran, Whinfield, Khayyam)", "archive.org (G.A.L.)"],
        "language_original_dominant": "ara (Arabe classique), fas (Persan)",
        "schools_covered": [
            "Sources fondatrices (Qurʾān, 6 Sunan canoniques, Muwaṭṭaʾ, Musnad)",
            "Tafsīr classique (Ṭabarī, Zamakhsharī, Rāzī, Qurṭubī, Ibn Kathīr)",
            "Histoire/Sīra (Ibn Isḥāq, Ṭabarī, Masʿūdī, Ibn al-Athīr, Ibn Khaldūn, Rashīd al-Dīn)",
            "Fiqh/Uṣūl (al-Shāfiʿī, Sarakhsī, Ibn Qudāma, Ghazālī Mustaṣfā, Ibn Taymiyya)",
            "Kalām (Ashʿarī, Bāqillānī, Juwaynī, Shahrastānī, Māturīdī, ʿAbd al-Jabbār)",
            "Falsafa (Kindī, Fārābī, Ibn Sīnā corpus, Ibn Rushd corpus, Ibn Ṭufayl, Ibn Bājja, Ibn Ḥazm, Suhrawardī)",
            "Soufisme arabophone (Muḥāsibī, Junayd, Sarrāj, Qushayrī, Ghazālī Iḥyāʾ, Ibn ʿArabī, Ibn ʿAṭāʾ Allāh)",
            "Soufisme persan & littérature (Hujwīrī, Rūmī, ʿAṭṭār, Saʿdī, Ḥāfeẓ)",
            "Sciences (Khwārizmī, Ibn al-Haytham, Bīrūnī, Khayyām)",
            "Médecine (Ibn Sīnā Qānūn, Abū Bakr al-Rāzī)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue ISLAMIC × medieval : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

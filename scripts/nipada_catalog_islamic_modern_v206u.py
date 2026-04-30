#!/usr/bin/env python3
"""§206u — ISLAMIC × modern (1789 → 1914), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_islamic_modern_v206u.json"

WORKS = [
    # ── Réforme arabe « Nahda » : Égypte, Levant, Tunisie
    ("rifa_al_tahtawi_takhlis_al_ibriz", "تخليص الإبريز في تلخيص باريز / Takhlīṣ al-ibrīz fī talkhīṣ Bārīz", "The Extraction of Pure Gold in Summarizing Paris", "ara", 1834, ["nahda", "reform"], "rifa_al_tahtawi"),
    ("rifa_al_tahtawi_manahij_al_albab", "مناهج الألباب المصرية / Manāhij al-albāb al-miṣriyya", "Egyptian Methods for Modern Education", "ara", 1869, ["nahda", "reform"], "rifa_al_tahtawi"),
    ("khayr_al_din_al_tunisi_aqwam_al_masalik", "أقوم المسالك في معرفة أحوال الممالك / Aqwam al-masālik fī maʿrifat aḥwāl al-mamālik", "The Surest Path to Knowledge of the Conditions of Kingdoms", "ara", 1867, ["nahda", "reform"], "khayr_al_din_al_tunisi"),
    ("butrus_al_bustani_da_irat_al_maarif", "دائرة المعارف / Dāʾirat al-maʿārif", "Encyclopedia (Arabic)", "ara", 1876, ["nahda", "encyclopedia"], "butrus_al_bustani"),
    ("ahmad_faris_al_shidyaq_saq_ala_l_saq", "الساق على الساق / Al-Sāq ʿalā al-sāq", "Leg over Leg", "ara", 1855, ["nahda", "literature"], "ahmad_faris_al_shidyaq"),
    ("nasif_al_yaziji_majma_al_bahrayn", "مجمع البحرين / Majmaʿ al-baḥrayn", "Confluence of the Two Seas (rhetoric)", "ara", 1856, ["nahda", "rhetoric"], "nasif_al_yaziji"),
    ("ibrahim_al_yaziji_essays", "العقد / Al-ʿIqd (selected essays)", "The Necklace (essays)", "ara", 1899, ["nahda", "literature"], "ibrahim_al_yaziji"),
    ("francis_marrash_ghabat_al_haqq", "غابة الحق / Ghābat al-ḥaqq", "The Forest of Truth", "ara", 1865, ["nahda", "utopian"], "francis_marrash"),
    ("jurji_zaydan_tarikh_al_tamaddun_al_islami", "تاريخ التمدن الإسلامي / Tārīkh al-tamaddun al-islāmī", "History of Islamic Civilization", "ara", 1903, ["nahda", "history"], "jurji_zaydan"),

    # ── Salafiyya réformiste — al-Afghānī, ʿAbduh, Riḍā
    ("jamal_al_din_al_afghani_al_radd_ala_al_dahriyyin", "الرد على الدهريين / Al-Radd ʿalā al-dahriyyīn", "Refutation of the Materialists", "ara", 1881, ["islamic_modernism", "anti_materialism"], "jamal_al_din_al_afghani"),
    ("al_afghani_al_urwa_al_wuthqa", "العروة الوثقى / Al-ʿUrwa al-wuthqā", "The Indissoluble Bond (journal articles)", "ara", 1884, ["islamic_modernism", "pan_islamism"], "jamal_al_din_al_afghani_muhammad_abduh"),
    ("muhammad_abduh_risalat_al_tawhid", "رسالة التوحيد / Risālat al-tawḥīd", "The Theology of Unity", "ara", 1897, ["islamic_modernism"], "muhammad_abduh"),
    ("muhammad_abduh_al_islam_wa_l_nasraniyya", "الإسلام والنصرانية مع العلم والمدنية / Al-Islām wa al-naṣrāniyya maʿa al-ʿilm wa al-madaniyya", "Islam and Christianity with Science and Civilization", "ara", 1902, ["islamic_modernism"], "muhammad_abduh"),
    ("muhammad_abduh_tafsir_al_manar_proto", "تفسير المنار (الجزء الأول) / Tafsīr al-Manār (vol. I)", "Tafsīr al-Manār vol. I", "ara", 1900, ["islamic_modernism", "tafsir"], "muhammad_abduh_rashid_rida"),
    ("rashid_rida_tafsir_al_manar_full", "تفسير المنار / Tafsīr al-Manār", "Tafsīr al-Manār (full)", "ara", 1927, ["islamic_modernism", "tafsir"], "rashid_rida"),
    ("rashid_rida_al_khilafa_aw_al_imama_al_uzma", "الخلافة أو الإمامة العظمى / Al-Khilāfa aw al-imāma al-ʿuẓmā", "The Caliphate or the Great Imamate", "ara", 1923, ["islamic_modernism", "political_theology"], "rashid_rida"),
    ("rashid_rida_al_wahy_al_muhammadi", "الوحي المحمدي / Al-Waḥy al-Muḥammadī", "The Muhammadan Revelation", "ara", 1933, ["islamic_modernism"], "rashid_rida"),
    ("jamal_al_din_al_qasimi_mahasin_al_tawil", "محاسن التأويل / Maḥāsin al-taʾwīl", "The Beauties of Interpretation", "ara", 1909, ["islamic_modernism", "salafi_proto"], "jamal_al_din_al_qasimi"),
    ("abd_al_rahman_al_kawakibi_taba_i_al_istibdad", "طبائع الاستبداد / Ṭabāʾiʿ al-istibdād", "The Nature of Despotism", "ara", 1900, ["islamic_modernism", "political_critique"], "abd_al_rahman_al_kawakibi"),
    ("al_kawakibi_umm_al_qura", "أم القرى / Umm al-qurā", "The Mother of Villages", "ara", 1899, ["islamic_modernism", "pan_arab_proto"], "abd_al_rahman_al_kawakibi"),
    ("shakib_arslan_li_madha_taakhkhara_al_muslimun", "لماذا تأخر المسلمون / Li-mādhā taʾakhkhara al-muslimūn", "Why Have the Muslims Lagged Behind?", "ara", 1939, ["islamic_modernism", "decline_thesis"], "shakib_arslan"),

    # ── Tanzimat ottoman & Jeunes Ottomans
    ("namik_kemal_vatan_yahut_silistre", "Vatan yahut Silistre", "Fatherland or Silistre", "ota", 1873, ["young_ottoman", "ottoman_constitutionalism"], "namik_kemal"),
    ("namik_kemal_renan_mudafaanamesi", "Renan Müdafaanamesi", "Defense Against Renan", "ota", 1883, ["young_ottoman", "islamic_modernism"], "namik_kemal"),
    ("ziya_pasha_terci_i_bend", "Terci-i Bend", "Strophic Poem (with philosophical commentary)", "ota", 1870, ["young_ottoman"], "ziya_pasha"),
    ("ahmed_cevdet_pasha_mecelle", "مجلة الأحكام العدلية / Mecelle-i Aḥkām-ı ʿAdliye", "The Mecelle (Ottoman Civil Code)", "ota", 1877, ["ottoman_legal_reform"], "ahmed_cevdet_pasha"),
    ("ahmed_cevdet_pasha_tarih", "Tarih-i Cevdet", "Cevdet's History", "ota", 1884, ["ottoman_history", "reform"], "ahmed_cevdet_pasha"),
    ("said_halim_pasa_islamlasmak", "İslâmlaşmak", "Becoming Muslim", "ota", 1918, ["young_ottoman", "islamic_modernism"], "said_halim_pasa"),
    ("musa_kazim_efendi_kulliyat", "Külliyat-ı Şeyhülislâm Musa Kâzım", "Collected Works of Şeyhülislâm Musa Kâzım", "ota", 1920, ["ottoman_legal_reform", "islamic_modernism"], "musa_kazim_efendi"),
    ("ismail_gasprinski_terjuman", "Terjuman / Tercüman", "The Interpreter (newspaper essays)", "tat", 1903, ["jadid", "pan_turkic_proto"], "ismail_gasprinski"),
    ("ismail_gasprinski_russkoye_musulmanstvo", "Русское мусульманство / Russkoye musulmanstvo", "Russian Muslims", "rus", 1881, ["jadid", "reform"], "ismail_gasprinski"),

    # ── Réforme indienne : Aligarh, Deobandi, Barelvi
    ("syed_ahmad_khan_asbab_baghawat", "أسباب بغاوة الهند / Asbāb-i baghāwat-i Hind", "The Causes of the Indian Mutiny", "urd", 1858, ["islamic_reform_india", "aligarh"], "sayyid_ahmad_khan"),
    ("syed_ahmad_khan_tahdhib_al_akhlaq", "Tahdhīb al-akhlāq", "The Refinement of Morals (journal)", "urd", 1872, ["islamic_reform_india", "aligarh"], "sayyid_ahmad_khan"),
    ("altaf_husain_hali_musaddas_madd_o_jazr_e_islam", "مسدس مد و جزر اسلام / Musaddas Madd-o-jazr-e-Islām", "The Flow and Ebb of Islam", "urd", 1879, ["islamic_reform_india", "aligarh"], "altaf_husain_hali"),
    ("shibli_numani_al_kalam", "الكلام / Al-Kalām", "Theology (in Urdu)", "urd", 1903, ["islamic_reform_india", "aligarh"], "shibli_numani"),
    ("shibli_numani_al_farooq", "الفاروق / Al-Fārūq", "Biography of ʿUmar al-Fārūq", "urd", 1899, ["islamic_reform_india", "history"], "shibli_numani"),
    ("rashid_ahmad_gangohi_fatawa_rashidiyya", "فتاوی رشیدیہ / Fatāwā Rashīdiyya", "The Rashidi Legal Verdicts", "urd", 1880, ["deobandi"], "rashid_ahmad_gangohi"),
    ("qasim_nanautawi_taqrir_dilpazir", "تقریر دل پذیر / Taqrīr dil-pazīr", "Pleasing Discourse", "urd", 1875, ["deobandi"], "muhammad_qasim_nanautawi"),
    ("ashraf_ali_thanwi_bahishti_zewar", "بہشتی زیور / Bihishtī Zewar", "Heavenly Ornaments", "urd", 1905, ["deobandi"], "ashraf_ali_thanwi"),
    ("mahmud_hasan_deobandi_translations", "Translations and Commentaries", "Translations and Commentaries (Deobandi)", "urd", 1911, ["deobandi"], "mahmud_hasan_deobandi"),
    ("ahmad_raza_khan_fatawa_ridawiyya", "فتاوی رضویہ / Fatāwā Riḍawiyya", "The Ridawi Legal Verdicts", "urd", 1900, ["barelvi"], "ahmad_raza_khan"),
    ("ahmad_raza_khan_husam_al_haramayn", "حسام الحرمین / Ḥusām al-Ḥaramayn", "The Sword of the Two Sanctuaries", "ara", 1906, ["barelvi"], "ahmad_raza_khan"),

    # ── Iqbal philosophique
    ("iqbal_development_metaphysics_persia", "The Development of Metaphysics in Persia", "The Development of Metaphysics in Persia", "eng", 1908, ["islamic_modern", "philosophy_iqbal"], "muhammad_iqbal"),
    ("iqbal_secrets_of_self_proto", "Asrār-i khudī (early drafts)", "Secrets of the Self (early drafts)", "fas", 1915, ["islamic_modern", "philosophy_iqbal"], "muhammad_iqbal"),

    # ── Soufisme tardif & Naqshbandī Mujaddidī
    ("khalid_al_baghdadi_majmuat_rasail", "مجموعة رسائل / Majmūʿat rasāʾil", "Collected Treatises (Naqshbandī Khālidī)", "ara", 1820, ["naqshbandi_khalidi", "sufism_late"], "khalid_al_baghdadi"),
    ("ahmad_zarruq_late_school_compilations", "Late Zarrūqī school anthologies", "Late Zarrūqī school anthologies", "ara", 1850, ["sufism_maliki_morocco"], "zarruqi_school_late"),
    ("muhammad_b_ali_al_sanusi_al_masail_al_ashr", "المسائل العشر / Al-Masāʾil al-ʿashr", "The Ten Questions", "ara", 1849, ["sanusiyya"], "muhammad_b_ali_al_sanusi"),
    ("ahmad_b_idris_collected_treatises", "مجموعة رسائل / Majmūʿat rasāʾil al-Aḥmadiyya", "Collected Treatises of Aḥmad b. Idrīs", "ara", 1837, ["sufism_neo"], "ahmad_b_idris"),
    ("ahmad_al_tijani_jawahir_al_maani", "جواهر المعاني / Jawāhir al-maʿānī", "Jewels of Meanings", "ara", 1817, ["tijaniyya"], "ali_harazim"),
    ("amir_abd_al_qadir_kitab_al_mawaqif", "كتاب المواقف / Kitāb al-mawāqif", "Book of Halts", "ara", 1860, ["sufism_akbarian", "anti_colonial_proto"], "abd_al_qadir_al_jazairi"),
    ("amir_abd_al_qadir_dhikra_al_aqil", "ذكرى العاقل وتنبيه الغافل / Dhikrā al-ʿāqil", "Reminder to the Intelligent", "ara", 1855, ["sufism_akbarian"], "abd_al_qadir_al_jazairi"),

    # ── Iran qajar et néo-platonisme tardif
    ("hadi_sabzawari_sharh_al_manzuma", "شرح المنظومة / Sharḥ al-Manẓūma", "Commentary on the Versified Treatise", "ara", 1845, ["sadrian_late", "philosophy_iran_qajar"], "hadi_sabzawari"),
    ("hadi_sabzawari_asrar_al_hikam", "أسرار الحكم / Asrār al-ḥikam", "Secrets of Wisdom", "fas", 1860, ["sadrian_late"], "hadi_sabzawari"),
    ("agha_ali_modarres_zunuzi_badayi", "بدائع الحكم / Badāyiʿ al-ḥikam", "Marvels of Wisdom", "ara", 1881, ["sadrian_late"], "agha_ali_modarres_zunuzi"),

    # ── Bābī-Bahāʾī
    ("bab_al_bayan_al_arabi", "البيان العربي / Al-Bayān al-ʿarabī", "The Arabic Bayan", "ara", 1848, ["babi"], "the_bab"),
    ("bab_al_bayan_al_farsi", "بيان فارسي / Bayān-i Fārsī", "The Persian Bayan", "fas", 1848, ["babi"], "the_bab"),
    ("bahaullah_kitab_i_aqdas", "كتاب الأقدس / Kitāb-i-Aqdas", "The Most Holy Book", "ara", 1873, ["bahai"], "bahaullah"),
    ("bahaullah_kitab_i_iqan", "كتاب الإيقان / Kitāb-i-Īqān", "The Book of Certitude", "fas", 1862, ["bahai"], "bahaullah"),
    ("bahaullah_seven_valleys", "هفت وادی / Haft Vādī", "The Seven Valleys", "fas", 1856, ["bahai", "sufism_neo"], "bahaullah"),
    ("abdul_baha_some_answered_questions", "مفاوضات / Mufāwaḍāt", "Some Answered Questions", "fas", 1908, ["bahai"], "abdul_baha"),

    # ── Ahmadiyya
    ("mirza_ghulam_ahmad_barahin_i_ahmadiyya", "براہین احمدیہ / Barāhīn-i Aḥmadiyya", "The Proofs of Ahmadiyya", "urd", 1880, ["ahmadiyya"], "mirza_ghulam_ahmad"),
    ("mirza_ghulam_ahmad_haqiqat_al_wahi", "حقیقت الوحی / Ḥaqīqat al-waḥy", "The Reality of Revelation", "urd", 1907, ["ahmadiyya"], "mirza_ghulam_ahmad"),

    # ── Wahhabite seconde génération + Salafi
    ("ibn_uthaymin_predecessors_late_najdi", "Late Najdi school treatises (al-Saʿdī al-ʿAṣimī predecessors)", "Late Najdi school treatises", "ara", 1880, ["wahhabi_najdi_late"], "najdi_late_school"),

    # ── Africain ouest-saharien
    ("usman_dan_fodio_bayan_wujub_al_hijra", "بيان وجوب الهجرة / Bayān wujūb al-hijra", "Statement on the Obligation of Hijra", "ara", 1806, ["sufism_qadiri", "sokoto_jihad"], "usman_dan_fodio"),
    ("muhammad_bello_infaq_al_maysur", "إنفاق الميسور / Infāq al-maysūr", "The Easy Expenditure", "ara", 1812, ["sokoto_caliphate", "history"], "muhammad_bello"),

    # ── Christianisme arabe & traduction biblique
    ("smith_van_dyck_bible_translation", "الكتاب المقدس (ترجمة فاندايك) / Smith-Van Dyck Bible", "Smith-Van Dyck Arabic Bible", "ara", 1865, ["nahda", "translation"], "eli_smith_cornelius_van_dyck"),

    # ── Asie centrale
    ("ahmad_donish_navadir_al_waqai", "نوادر الوقایع / Nawādir al-waqāʾiʿ", "Curious Events", "fas", 1885, ["central_asian_modern", "reform"], "ahmad_donish"),
    ("munavvar_qari_jadid_pedagogy", "Jadidist pedagogical treatises", "Jadidist pedagogical treatises", "uzb", 1908, ["jadid"], "munavvar_qari_abdurashidkhonov"),

    # ── Penseurs ottomans tardifs
    ("ahmet_riza_la_faillite_morale", "La faillite morale de la politique occidentale", "The Moral Bankruptcy of Western Policy", "fra", 1922, ["young_ottoman", "anti_colonial_proto"], "ahmet_riza"),
    ("ziya_gokalp_turklesmek_islamlasmak_muasirlasmak", "Türkleşmek, İslâmlaşmak, Muasırlaşmak", "Turkification, Islamization, Modernization", "ota", 1918, ["young_ottoman", "turkish_proto_nationalism"], "ziya_gokalp"),
    ("musa_jarullah_bigiyev_rahmat_i_ilahiyya_burhanlari", "Раҳмәт-и Илаҳия бурhанлары / Raḥmat-i ilāhiyya burhānları", "Proofs of Divine Mercy", "tat", 1911, ["jadid", "islamic_modernism"], "musa_jarullah_bigiyev"),
]

assert len(WORKS) == 70, f"ISLAMIC×modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "babi" in tags:
        return "BABI"
    if "bahai" in tags:
        return "BAHAI"
    if "ahmadiyya" in tags:
        return "AHMADIYYA"
    if "nahda" in tags and "encyclopedia" in tags:
        return "NAHDA_ENCYCLOPEDIA"
    if "nahda" in tags and "literature" in tags:
        return "NAHDA_LITERATURE"
    if "nahda" in tags and "history" in tags:
        return "NAHDA_HISTORIOGRAPHY"
    if "nahda" in tags and "rhetoric" in tags:
        return "NAHDA_RHETORIC"
    if "nahda" in tags and "utopian" in tags:
        return "NAHDA_UTOPIAN"
    if "nahda" in tags and "translation" in tags:
        return "NAHDA_BIBLE_TRANSLATION"
    if "nahda" in tags:
        return "NAHDA_REFORM"
    if "islamic_modernism" in tags and "salafi_proto" in tags:
        return "SALAFIYYA_PROTO"
    if "islamic_modernism" in tags and "tafsir" in tags:
        return "ISLAMIC_MODERNISM_TAFSIR"
    if "islamic_modernism" in tags and "political_theology" in tags:
        return "ISLAMIC_MODERNISM_POLITICAL"
    if "islamic_modernism" in tags and "political_critique" in tags:
        return "ISLAMIC_MODERNISM_POLITICAL"
    if "islamic_modernism" in tags and "decline_thesis" in tags:
        return "ISLAMIC_MODERNISM_DECLINE"
    if "islamic_modernism" in tags and "anti_materialism" in tags:
        return "ISLAMIC_MODERNISM_ANTI_MATERIALISM"
    if "islamic_modernism" in tags and "pan_islamism" in tags:
        return "PAN_ISLAMISM"
    if "islamic_modernism" in tags and "pan_arab_proto" in tags:
        return "PAN_ARAB_PROTO"
    if "islamic_modernism" in tags:
        return "ISLAMIC_MODERNISM"
    if "young_ottoman" in tags:
        return "YOUNG_OTTOMAN"
    if "ottoman_legal_reform" in tags:
        return "OTTOMAN_LEGAL_REFORM"
    if "ottoman_history" in tags:
        return "OTTOMAN_HISTORIOGRAPHY"
    if "jadid" in tags:
        return "JADID"
    if "deobandi" in tags:
        return "DEOBANDI"
    if "barelvi" in tags:
        return "BARELVI"
    if "aligarh" in tags:
        return "ALIGARH"
    if "islamic_reform_india" in tags:
        return "ISLAMIC_REFORM_INDIA"
    if "philosophy_iqbal" in tags:
        return "IQBAL_PHILOSOPHY"
    if "naqshbandi_khalidi" in tags:
        return "NAQSHBANDI_KHALIDI"
    if "tijaniyya" in tags:
        return "TIJANIYYA"
    if "sanusiyya" in tags:
        return "SANUSIYYA"
    if "sufism_akbarian" in tags:
        return "SUFISM_AKBARIAN_LATE"
    if "sufism_qadiri" in tags or "sokoto_jihad" in tags:
        return "SOKOTO_QADIRI"
    if "sokoto_caliphate" in tags:
        return "SOKOTO_HISTORIO"
    if "sufism_maliki_morocco" in tags:
        return "SUFISM_MAGHREB_LATE"
    if "sufism_late" in tags:
        return "SUFISM_LATE"
    if "sufism_neo" in tags:
        return "SUFI_NEO"
    if "sadrian_late" in tags:
        return "SADRIAN_LATE_QAJAR"
    if "wahhabi_najdi_late" in tags:
        return "WAHHABI_NAJDI_LATE"
    if "central_asian_modern" in tags:
        return "CENTRAL_ASIAN_MODERN"
    return "ISLAMIC_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "ISLAMIC", "epoch": "modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 5,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "public_domain", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206u_islamic_modern", "generated": "2026-04-30",
        "macro_culture": "ISLAMIC", "epoch": "modern",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["al-maktaba.org", "shamela.ws", "archive.org", "Bahai Reference Library"],
        "language_original_dominant": "ara + ota + urd + fas + tat + uzb + eng + fra",
        "schools_covered": [
            "Nahda arabe (Ṭahṭāwī ×2, Khayr al-Dīn, al-Bustānī, al-Shidyāq, al-Yāzijī ×2, Marrāsh, Zaydān)",
            "Salafiyya réformiste (al-Afghānī ×2, ʿAbduh ×3, Riḍā ×3, al-Qāsimī, al-Kawākibī ×2, Arslān)",
            "Tanzimat-Jeunes Ottomans (Namık Kemal ×2, Ziya Paşa, Cevdet ×2, Said Halim, Musa Kâzım, Ahmet Rıza)",
            "Jadid (Gasprinski ×2, Munavvar Qari)",
            "Réforme indienne Aligarh (Sayyid Aḥmad Khan ×2, Ḥālī, Shiblī ×2)",
            "Deobandi (Gangohī, Nānautawī, Thānwī, Maḥmūd Ḥasan)",
            "Barelvi (Aḥmad Riḍā Khān ×2)",
            "Iqbal philosophique ×2",
            "Sufisme tardif & Naqshbandī (al-Baghdādī, ʿAbd al-Qādir ×2, Aḥmad b. Idrīs, Tijāniyya, Sanūsiyya)",
            "Iran qajar (Sabzawārī ×2, Zunūzī)",
            "Bābī-Bahāʾī (Bāb ×2, Bahā'ullāh ×3, ʿAbdu'l-Bahā')",
            "Ahmadiyya (Ghulām Aḥmad ×2)",
            "Wahhabi-Salafi tardif (école najdi)",
            "Sokoto/Afrique de l'Ouest (Usman dan Fodio, Muḥammad Bello)",
            "Christianisme arabe (Smith-Van Dyck Bible)",
            "Asie centrale moderne (Ahmad Donish)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue ISLAMIC × modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

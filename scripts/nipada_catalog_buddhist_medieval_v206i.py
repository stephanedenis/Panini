#!/usr/bin/env python3
"""
§206i — Catalogue BUDDHIST × medieval (500 → 1500 CE), 70 œuvres.

Cellule complémentaire à CHINESE×medieval (qui couvre Tiantai/Huayan/Chan/Faxiang
chinois). Ici on cible :
- Theravāda médiéval (Buddhaghosa Visuddhimagga + commentaires + Anuruddha)
- Tibetan canon translations (Atiśa, Sakya Paṇḍita, Tsongkhapa, Longchenpa,
  Gampopa, Mi-la-ras-pa, Dol-po-pa, Karma-pa)
- Vajrayāna sūtra-tantra : Guhyasamāja, Hevajra, Cakrasaṃvara, Kālacakra,
  Mahāvairocana, Sarvatathāgata-tattvasaṃgraha, Kriyāsaṃgraha
- Korean Sŏn (Wonhyo, Chinul, Uisang)
- Japanese : Saichō, Kūkai, Hōnen, Shinran, Dōgen, Nichiren, Eisai
- Burmese / Sri Lankan Pāli : Buddhadatta, Dhammapāla, Mahānāma
- Late Mahāyāna sūtras canonized in Tibet
- Bka' brgyud / rNying ma terma
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_buddhist_medieval_v206i.json"

WORKS = [
    # ── Theravāda médiéval (Pāli)
    ("buddhaghosa_visuddhimagga", "Visuddhimagga", "Path of Purification", "pli", 430, ["theravada", "abhidhamma"], "buddhaghosa"),
    ("buddhaghosa_samantapasadika", "Samantapāsādikā", "Commentary on Vinaya", "pli", 430, ["theravada", "vinaya"], "buddhaghosa"),
    ("buddhaghosa_sumangalavilasini", "Sumaṅgalavilāsinī", "Commentary on Dīgha Nikāya", "pli", 430, ["theravada", "atthakatha"], "buddhaghosa"),
    ("buddhaghosa_papancasudani", "Papañcasūdanī", "Commentary on Majjhima Nikāya", "pli", 430, ["theravada", "atthakatha"], "buddhaghosa"),
    ("buddhaghosa_saratthappakasini", "Sāratthappakāsinī", "Commentary on Saṃyutta Nikāya", "pli", 430, ["theravada", "atthakatha"], "buddhaghosa"),
    ("buddhaghosa_manorathapurani", "Manorathapūraṇī", "Commentary on Aṅguttara Nikāya", "pli", 430, ["theravada", "atthakatha"], "buddhaghosa"),
    ("buddhaghosa_atthasalini", "Atthasālinī", "Commentary on Dhammasaṅgaṇī", "pli", 430, ["theravada", "abhidhamma"], "buddhaghosa"),
    ("buddhadatta_abhidhammavatara", "Abhidhammāvatāra", "Introduction to Abhidhamma", "pli", 450, ["theravada", "abhidhamma"], "buddhadatta"),
    ("dhammapala_paramatthadipani", "Paramatthadīpanī", "Commentaries on Khuddaka", "pli", 550, ["theravada", "atthakatha"], "dhammapala"),
    ("anuruddha_abhidhammatthasangaha", "Abhidhammatthasaṅgaha", "Manual of Abhidhamma", "pli", 1000, ["theravada", "abhidhamma"], "anuruddha"),
    ("mahanama_mahavamsa", "Mahāvaṃsa", "Great Chronicle of Sri Lanka", "pli", 500, ["theravada", "history"], "mahanama"),
    ("buddhaghosa_dhammapada_atthakatha", "Dhammapada-aṭṭhakathā", "Commentary on Dhammapada", "pli", 430, ["theravada", "atthakatha"], "buddhaghosa"),

    # ── Tibetan early translation period (snga dar) + later (phyi dar)
    ("atisa_bodhipathapradipa_tib", "Byang chub lam gyi sgron ma", "Lamp on the Path to Awakening (Tibetan)", "bod", 1042, ["tibetan", "kadam"], "atisa"),
    ("atisa_carya_samgraha", "spyod pa bsdus pa", "Compendium of Conduct", "bod", 1045, ["tibetan", "kadam"], "atisa"),
    ("dromton_kadam_thorbu", "bka' gdams thor bu", "Kadam Miscellaneous Sayings", "bod", 1060, ["tibetan", "kadam"], "dromton"),
    ("milarepa_mgur_bum", "mgur 'bum", "Hundred Thousand Songs of Milarepa", "bod", 1110, ["tibetan", "kagyu"], "milarepa"),
    ("gampopa_thar_rgyan", "thar pa rin po che'i rgyan", "Jewel Ornament of Liberation", "bod", 1130, ["tibetan", "kagyu"], "gampopa"),
    ("sakya_pandita_sdom_gsum", "sdom gsum rab dbye", "Distinguishing the Three Vows", "bod", 1232, ["tibetan", "sakya"], "sakya_pandita"),
    ("sakya_pandita_legs_bshad", "sa skya legs bshad", "Sakya Pandita's Treasury of Sayings", "bod", 1245, ["tibetan", "sakya"], "sakya_pandita"),
    ("longchenpa_klong_chen_mdzod_bdun", "klong chen mdzod bdun", "Longchenpa's Seven Treasuries (1)", "bod", 1340, ["tibetan", "nyingma", "dzogchen"], "longchenpa"),
    ("longchenpa_ngal_gso_skor_gsum", "ngal gso skor gsum", "Trilogy of Rest", "bod", 1340, ["tibetan", "nyingma", "dzogchen"], "longchenpa"),
    ("longchenpa_chos_dbyings_mdzod", "chos dbyings mdzod", "Treasury of the Dharmadhātu", "bod", 1345, ["tibetan", "nyingma", "dzogchen"], "longchenpa"),
    ("dolpopa_ri_chos_nges_don", "ri chos nges don rgya mtsho", "Mountain Doctrine: Ocean of Definitive Meaning", "bod", 1330, ["tibetan", "jonang", "shentong"], "dolpopa"),
    ("buton_chos_byung", "bu ston chos 'byung", "History of Buddhism in India and Tibet", "bod", 1322, ["tibetan", "history"], "buton"),
    ("tsongkhapa_lamrim_chenmo", "lam rim chen mo", "Great Treatise on the Stages of the Path", "bod", 1402, ["tibetan", "gelug"], "tsongkhapa"),
    ("tsongkhapa_lamrim_chungba", "lam rim chung ba", "Middle-Length Lamrim", "bod", 1415, ["tibetan", "gelug"], "tsongkhapa"),
    ("tsongkhapa_sngags_rim_chenmo", "sngags rim chen mo", "Great Treatise on Mantra", "bod", 1405, ["tibetan", "gelug", "vajrayana"], "tsongkhapa"),
    ("tsongkhapa_drang_nges_legs_bshad", "drang nges legs bshad snying po", "Essence of True Eloquence", "bod", 1407, ["tibetan", "gelug", "madhyamaka"], "tsongkhapa"),
    ("rendawa_madhyamaka_commentary", "dbu ma 'jug pa'i rnam bshad", "Rendawa's Madhyamaka Commentary", "bod", 1380, ["tibetan", "sakya", "madhyamaka"], "rendawa"),
    ("milarepa_namthar", "mi la'i rnam thar", "Life of Milarepa", "bod", 1488, ["tibetan", "kagyu", "biography"], "tsangnyon_heruka"),

    # ── Vajrayāna tantra textes (sūtra-class translations into Tibetan medieval)
    ("guhyasamaja_tantra", "Guhyasamāja Tantra", "Secret Assembly Tantra", "san", 700, ["vajrayana", "tantra"], None),
    ("hevajra_tantra", "Hevajra Tantra", "Hevajra Tantra", "san", 800, ["vajrayana", "tantra"], None),
    ("cakrasamvara_tantra", "Cakrasaṃvara Tantra", "Cakrasaṃvara Tantra", "san", 800, ["vajrayana", "tantra"], None),
    ("kalacakra_tantra", "Kālacakra Tantra", "Wheel of Time Tantra", "san", 1025, ["vajrayana", "tantra"], None),
    ("vimalaprabha", "Vimalaprabhā", "Stainless Light Commentary on Kālacakra", "san", 1030, ["vajrayana", "tantra"], "pundarika"),
    ("mahavairocana_tantra", "Mahāvairocana Tantra", "Great Vairocana Tantra", "san", 670, ["vajrayana", "tantra"], None),
    ("sarvatathagata_tattvasamgraha", "Sarvatathāgata-tattvasaṃgraha", "Compendium of the Truth of All Tathāgatas", "san", 700, ["vajrayana", "tantra"], None),
    ("manjusrinamasamgiti", "Mañjuśrī-nāma-saṃgīti", "Concert of Names of Mañjuśrī", "san", 750, ["vajrayana"], None),
    ("naropa_six_yogas", "Nā ro chos drug", "Six Yogas of Nāropa", "bod", 1050, ["vajrayana", "kagyu"], "naropa"),
    ("tilopa_dohas", "Mahāmudrā-upadeśa (Tilopa)", "Tilopa's Mahāmudrā Instructions", "san", 1010, ["vajrayana", "mahamudra"], "tilopa"),
    ("saraha_dohakosa", "Dohākośa-gīti", "Saraha's Treasury of Couplets", "san", 800, ["vajrayana", "mahamudra"], "saraha"),

    # ── Korean Sŏn / Hwaŏm
    ("wonhyo_taeseung_kisillon_so", "Daeseung gisillon so 大乘起信論疏", "Wonhyo's Commentary on Awakening of Faith", "lzh", 670, ["buddhist", "korean", "huayan"], "wonhyo"),
    ("wonhyo_simmun_hwajaeng_non", "Simmun hwajaeng non 十門和諍論", "Treatise on Reconciling the Ten Approaches", "lzh", 680, ["buddhist", "korean"], "wonhyo"),
    ("uisang_hwaom_ilseung_popgye_do", "Hwaeom ilseung beopgye do 華嚴一乘法界圖", "Diagram of the Hwaom Dharma-realm", "lzh", 670, ["buddhist", "korean", "huayan"], "uisang"),
    ("chinul_susim_gyol", "Susim gyol 修心訣", "Secrets on Cultivating the Mind", "lzh", 1205, ["buddhist", "korean", "son"], "chinul"),
    ("chinul_chinsim_chiksol", "Jinsim jikseol 真心直說", "Direct Discourse on the True Mind", "lzh", 1205, ["buddhist", "korean", "son"], "chinul"),

    # ── Japanese Buddhism
    ("kukai_sanjugohakke", "Sango Shīki 三教指帰", "Indications of the Goals of the Three Teachings", "ja-classical", 797, ["buddhist", "japanese", "shingon"], "kukai"),
    ("kukai_jujushinron", "Jūjūshin-ron 十住心論", "Treatise on the Ten Stages of Mind", "ja-classical", 830, ["buddhist", "japanese", "shingon"], "kukai"),
    ("saicho_sange_gakushoshiki", "Sange Gakushōshiki 山家學生式", "Tendai Monastic Rules", "ja-classical", 819, ["buddhist", "japanese", "tendai"], "saicho"),
    ("honen_senchakushu", "Senchakushū 選擇集", "Passages on the Selection of the Nembutsu", "ja-classical", 1198, ["buddhist", "japanese", "pureland"], "honen"),
    ("shinran_kyogyoshinsho", "Kyōgyōshinshō 教行信証", "Teaching, Practice, Faith and Realization", "ja-classical", 1224, ["buddhist", "japanese", "pureland"], "shinran"),
    ("shinran_tannisho", "Tannishō 歎異抄", "Lamenting the Deviations", "ja-classical", 1290, ["buddhist", "japanese", "pureland"], "yuien"),
    ("dogen_shobogenzo", "Shōbōgenzō 正法眼藏", "Treasury of the True Dharma Eye", "ja-classical", 1253, ["buddhist", "japanese", "zen", "soto"], "dogen"),
    ("dogen_fukan_zazengi", "Fukan Zazengi 普勧坐禪儀", "Universal Recommendation for Zazen", "ja-classical", 1227, ["buddhist", "japanese", "zen", "soto"], "dogen"),
    ("dogen_eihei_koroku", "Eihei Kōroku 永平廣錄", "Eihei Recorded Sayings", "ja-classical", 1253, ["buddhist", "japanese", "zen"], "dogen"),
    ("eisai_kozen_gokokuron", "Kōzen Gokokuron 興禪護國論", "Treatise on Promoting Zen for the Protection of the Country", "ja-classical", 1198, ["buddhist", "japanese", "zen", "rinzai"], "eisai"),
    ("nichiren_rissho_ankoku_ron", "Risshō Ankoku Ron 立正安國論", "On Establishing the Correct Teaching for the Peace of the Land", "ja-classical", 1260, ["buddhist", "japanese", "nichiren"], "nichiren"),
    ("nichiren_kaimokusho", "Kaimokushō 開目抄", "On the Opening of the Eyes", "ja-classical", 1272, ["buddhist", "japanese", "nichiren"], "nichiren"),
    ("ippen_shonin_goroku", "Ippen Shōnin Goroku 一遍上人語錄", "Recorded Sayings of Ippen", "ja-classical", 1289, ["buddhist", "japanese", "pureland"], "ippen"),
    ("musō_soseki_muchū_mondō", "Muchū Mondōshū 夢中問答集", "Dream Conversations", "ja-classical", 1342, ["buddhist", "japanese", "zen"], "muso_soseki"),
    ("ikkyu_kyounshu", "Kyōunshū 狂雲集", "Crazy Cloud Anthology", "ja-classical", 1470, ["buddhist", "japanese", "zen"], "ikkyu"),

    # ── Vietnamese Thiền (Lý-Trần dynasty)
    ("vinitaruci_lineage_records", "Thiền Uyển Tập Anh", "Outstanding Figures of the Zen Garden (Vietnam)", "lzh", 1337, ["buddhist", "vietnamese", "thien"], None),
    ("tran_nhan_tong_truc_lam", "Cư Trần Lạc Đạo Phú", "Living in the Dust, Joy in the Way", "lzh", 1295, ["buddhist", "vietnamese", "thien"], "tran_nhan_tong"),

    # ── Late Mahāyāna sūtra-class compilations (Tibetan canon)
    ("kalacakra_laghutantra", "Laghu-Kālacakra Tantra", "Abridged Kālacakra", "san", 1027, ["vajrayana", "tantra"], None),
    ("ratnamala_bodhipathapradipa_panjika", "Bodhipathapradīpa-pañjikā", "Atiśa's Auto-commentary", "san", 1050, ["tibetan", "kadam"], "atisa"),
    ("maitripa_tattvadasaka", "Tattvadaśaka", "Ten Verses on Reality", "san", 1060, ["vajrayana", "mahamudra"], "maitripa"),
    ("santaraksita_tattvasamgraha", "Tattvasaṃgraha", "Compendium of Reality", "san", 760, ["buddhist", "madhyamaka", "yogacara"], "santaraksita"),
    ("kamalasila_bhavanakrama", "Bhāvanākrama", "Stages of Meditation", "san", 790, ["buddhist", "madhyamaka"], "kamalasila"),
    ("haribhadra_abhisamayalankaraloka", "Abhisamayālaṅkārāloka", "Light of the Ornament of Realization", "san", 800, ["buddhist", "yogacara"], "haribhadra"),
    ("ratnakarasanti_madhyamakalankaravarttika", "Madhyamakālaṅkāra-vārttika", "Sub-commentary on the Ornament of the Middle Way", "san", 1020, ["buddhist", "yogacara"], "ratnakarasanti"),
]

assert len(WORKS) == 70, f"BUDDHIST×medieval doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "theravada" in tags:
        return "BUDDHISM_THERAVADA_MEDIEVAL"
    if "dzogchen" in tags:
        return "BUDDHISM_NYINGMA_DZOGCHEN"
    if "mahamudra" in tags:
        return "BUDDHISM_MAHAMUDRA"
    if "shentong" in tags or "jonang" in tags:
        return "BUDDHISM_JONANG"
    if "kagyu" in tags:
        return "BUDDHISM_KAGYU"
    if "sakya" in tags:
        return "BUDDHISM_SAKYA"
    if "kadam" in tags:
        return "BUDDHISM_KADAM"
    if "gelug" in tags:
        return "BUDDHISM_GELUG"
    if "nyingma" in tags:
        return "BUDDHISM_NYINGMA"
    if "tibetan" in tags:
        return "BUDDHISM_TIBETAN"
    if "vajrayana" in tags or "tantra" in tags:
        return "BUDDHISM_VAJRAYANA"
    if "korean" in tags:
        return "BUDDHISM_KOREAN"
    if "vietnamese" in tags:
        return "BUDDHISM_VIETNAMESE"
    if "japanese" in tags:
        if "shingon" in tags:
            return "BUDDHISM_SHINGON"
        if "tendai" in tags:
            return "BUDDHISM_TENDAI"
        if "pureland" in tags:
            return "BUDDHISM_JODO"
        if "zen" in tags:
            return "BUDDHISM_ZEN"
        if "nichiren" in tags:
            return "BUDDHISM_NICHIREN"
        return "BUDDHISM_JAPANESE"
    return "BUDDHISM_MEDIEVAL"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "BUDDHIST",
            "epoch": "medieval",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 50,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206i_buddhist_medieval",
        "generated": "2026-04-29",
        "macro_culture": "BUDDHIST",
        "epoch": "medieval",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["84000.co", "CBETA", "BDRC (Buddhist Digital Resource Center)", "SuttaCentral atthakatha", "archive.org"],
        "language_original_dominant": "pli (Theravāda), san (Sanskrit Vajrayāna), bod (Tibetan), lzh (Chinese-Korean), ja-classical (kanbun)",
        "schools_covered": [
            "Theravāda médiéval (Buddhaghosa Visuddhimagga + 6 Aṭṭhakathās, Buddhadatta, Dhammapāla, Anuruddha, Mahānāma)",
            "Tibetan Kadam/Sakya/Kagyu/Gelug/Nyingma/Jonang (Atiśa, Sakya Paṇḍita, Tsongkhapa corpus, Longchenpa, Dolpopa, Milarepa, Gampopa)",
            "Vajrayāna sūtra-tantra (Guhyasamāja, Hevajra, Cakrasaṃvara, Kālacakra, Mahāvairocana, Tattvasaṃgraha, Mañjuśrīnāmasaṃgīti)",
            "Mahāmudrā (Saraha, Tilopa, Maitrīpa)",
            "Korean Sŏn/Hwaŏm (Wonhyo, Uisang, Chinul)",
            "Japanese (Saichō Tendai, Kūkai Shingon, Hōnen+Shinran Pure Land, Dōgen+Eisai Zen, Nichiren, Ippen, Musō, Ikkyū)",
            "Vietnamese Thiền (Trần Nhân Tông Trúc Lâm)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue BUDDHIST × medieval : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

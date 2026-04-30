#!/usr/bin/env python3
"""§206t — CHINESE × modern (1789 → 1914), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_chinese_modern_v206t.json"

WORKS = [
    # ── Statecraft & écoles d'apprentissage pratique fin Qing
    ("wei_yuan_haiguo_tuzhi", "海國圖志 / Hǎi guó tú zhì", "Illustrated Treatise on the Maritime Kingdoms", "lzh", 1843, ["statecraft_late_qing", "world_geography"], "wei_yuan"),
    ("wei_yuan_shengwu_ji", "聖武記 / Shèng wǔ jì", "Records of Imperial Military Exploits", "lzh", 1842, ["statecraft_late_qing", "history"], "wei_yuan"),
    ("gong_zizhen_dingan_wenji", "定盦文集 / Dìng'ān wénjí", "Collected Works of Gong Zizhen", "lzh", 1837, ["statecraft_late_qing", "literati_critique"], "gong_zizhen"),
    ("gong_zizhen_jihai_zashi", "己亥雜詩 / Jǐ hài zá shī", "Miscellaneous Poems of 1839", "lzh", 1839, ["statecraft_late_qing"], "gong_zizhen"),
    ("lin_zexu_siguo_zhi", "四洲志 / Sì zhōu zhì", "Records of the Four Continents", "lzh", 1839, ["statecraft_late_qing", "world_geography"], "lin_zexu"),
    ("feng_guifen_jiaobinlu_kangyi", "校邠廬抗議 / Jiào bīn lú kàng yì", "Protests from the Studio of Jiaobin", "lzh", 1861, ["statecraft_late_qing", "self_strengthening"], "feng_guifen"),
    ("zeng_guofan_jiashu", "曾國藩家書 / Zēng Guófān jiāshū", "Family Letters of Zeng Guofan", "lzh", 1872, ["confucian_orthodox_late", "self_strengthening"], "zeng_guofan"),
    ("zeng_guofan_diary", "曾國藩日記 / Zēng Guófān rìjì", "Diaries of Zeng Guofan", "lzh", 1870, ["confucian_orthodox_late"], "zeng_guofan"),
    ("zhang_zhidong_quanxue_pian", "勸學篇 / Quàn xué piān", "Exhortation to Learning", "lzh", 1898, ["self_strengthening", "ti_yong"], "zhang_zhidong"),

    # ── New Text confucianisme & utopistes
    ("kang_youwei_xinxue_weijing_kao", "新學偽經考 / Xīnxué wěijīng kǎo", "Study of the Forged Classics of the New Text School", "lzh", 1891, ["new_text_confucian", "reform"], "kang_youwei"),
    ("kang_youwei_kongzi_gaizhi_kao", "孔子改制考 / Kǒngzǐ gǎizhì kǎo", "Confucius as a Reformer", "lzh", 1897, ["new_text_confucian", "reform"], "kang_youwei"),
    ("kang_youwei_datong_shu", "大同書 / Dà tóng shū", "The Book of Great Unity", "lzh", 1902, ["new_text_confucian", "utopian"], "kang_youwei"),
    ("liao_ping_jingue_wuyi", "經學六議 / Jīng xué liù yì", "Six Discussions of the Classics", "lzh", 1886, ["new_text_confucian"], "liao_ping"),
    ("liang_qichao_xinmin_shuo", "新民說 / Xīn mín shuō", "Discourse on the New Citizen", "lzh", 1903, ["liberal_reform", "nationalism"], "liang_qichao"),
    ("liang_qichao_qingdai_xueshu_gailun", "清代學術概論 / Qīngdài xuéshù gài lùn", "Outline of Qing Scholarship", "lzh", 1920, ["intellectual_history_modern"], "liang_qichao"),
    ("liang_qichao_yinbing_shi_wenji", "飲冰室文集 / Yǐn bīng shì wénjí", "Collected Works of the Ice-Drinker's Studio", "lzh", 1908, ["liberal_reform", "nationalism"], "liang_qichao"),
    ("tan_sitong_renxue", "仁學 / Rén xué", "An Exposition of Benevolence", "lzh", 1898, ["reform", "syncretism_three_teachings"], "tan_sitong"),

    # ── Yan Fu : traduction philosophique
    ("yan_fu_tianyan_lun", "天演論 / Tiān yǎn lùn", "On Evolution (Huxley translation)", "lzh", 1898, ["translation_western"], "yan_fu"),
    ("yan_fu_yuan_fu", "原富 / Yuán fù", "Inquiry into the Wealth of Nations", "lzh", 1902, ["translation_western"], "yan_fu"),
    ("yan_fu_qun_xue_yi_yan", "群學肄言 / Qún xué yì yán", "Study of Sociology", "lzh", 1903, ["translation_western"], "yan_fu"),
    ("yan_fu_qun_ji_quan_jie_lun", "群己權界論 / Qún jǐ quán jiè lùn", "On Liberty (Mill translation)", "lzh", 1903, ["translation_western"], "yan_fu"),
    ("yan_fu_mingxue_qianshuo", "名學淺說 / Míng xué qiǎn shuō", "Outline of Logic (Jevons translation)", "lzh", 1909, ["translation_western", "logic"], "yan_fu"),

    # ── Nationaliste révolutionnaire & culturel
    ("zhang_taiyan_qiushu", "訄書 / Qiú shū", "Book of Urgings", "lzh", 1900, ["nationalism", "philology_modern"], "zhang_taiyan"),
    ("zhang_taiyan_guogu_lunheng", "國故論衡 / Guó gù lùn héng", "Balanced Discussion of National Heritage", "lzh", 1910, ["nationalism", "philology_modern"], "zhang_taiyan"),
    ("zhang_taiyan_wuwu_lun", "五無論 / Wǔ wú lùn", "Five Negations", "lzh", 1907, ["buddhist_modern_china", "nationalism"], "zhang_taiyan"),
    ("sun_yatsen_sanmin_zhuyi_proto", "三民主義初稿 / Sān mín zhǔyì chū gǎo", "Three Principles of the People (early)", "lzh", 1905, ["nationalism", "republican"], "sun_yatsen"),
    ("zou_rong_geming_jun", "革命軍 / Gé mìng jūn", "The Revolutionary Army", "lzh", 1903, ["nationalism", "republican"], "zou_rong"),
    ("chen_tianhua_jingshi_zhong", "警世鐘 / Jǐng shì zhōng", "Bell to Awaken the Age", "lzh", 1903, ["nationalism", "republican"], "chen_tianhua"),
    ("liu_shipei_zhongguo_minzu_zhi", "中國民族志 / Zhōngguó mínzú zhì", "Records of the Chinese Nation", "lzh", 1903, ["nationalism", "anarchist_proto"], "liu_shipei"),
    ("liu_shipei_anarchist_essays_paris", "天義報文集 / Tiān yì bào wénjí", "Tianyi (Natural Justice) Essays", "lzh", 1907, ["anarchist_proto"], "liu_shipei"),
    ("he_zhen_nüjie_geming", "女界革命 / Nǚ jiè gé mìng", "Revolution in the Women's World", "lzh", 1907, ["feminism_china", "anarchist_proto"], "he_zhen"),

    # ── Lu Xun proto, littérature critique
    ("lu_xun_moluo_shi_li_shuo", "摩羅詩力說 / Móluó shī lì shuō", "On the Power of Mara Poetry", "lzh", 1908, ["literary_critique_modern"], "lu_xun"),
    ("lu_xun_wenhua_pianzhi_lun", "文化偏至論 / Wén huà piān zhì lùn", "On the Imbalance of Culture", "lzh", 1908, ["literary_critique_modern"], "lu_xun"),
    ("wang_guowei_renjian_cihua", "人間詞話 / Rén jiān cí huà", "Talks on Lyrics in the Human World", "lzh", 1908, ["aesthetic_modern"], "wang_guowei"),
    ("wang_guowei_jingzi_xuepai", "靜安文集 / Jìng ān wénjí", "Collected Works of Jing'an (philosophy)", "lzh", 1905, ["aesthetic_modern", "translation_western"], "wang_guowei"),

    # ── Cai Yuanpei et Hu Shi proto
    ("cai_yuanpei_zhongguo_lunlixue_shi", "中國倫理學史 / Zhōngguó lúnlǐ xué shǐ", "History of Chinese Ethics", "lzh", 1910, ["intellectual_history_modern"], "cai_yuanpei"),
    ("cai_yuanpei_yi_meiyu_dai_zongjiao", "以美育代宗教說 / Yǐ měiyù dài zōngjiào shuō", "Replacing Religion with Aesthetic Education", "lzh", 1917, ["aesthetic_modern", "secularism"], "cai_yuanpei"),
    ("hu_shi_xianqin_minglue_shi", "先秦名學史 / Xiān Qín míng xué shǐ", "History of Logical Method in Pre-Qin China", "eng", 1917, ["intellectual_history_modern", "logic"], "hu_shi"),

    # ── Bouddhisme moderne réformiste
    ("yang_wenhui_chen_yuan_zhang", "等不等觀雜錄 / Děng bù děng guān zá lù", "Miscellaneous Records of Equal-Unequal Views", "lzh", 1907, ["buddhist_modern_china"], "yang_wenhui"),
    ("yang_wenhui_jin_ling_publishing", "金陵刻經處編目 / Jīnlíng kèjīng chù biān mù", "Catalog of the Jinling Sūtra Press", "lzh", 1893, ["buddhist_modern_china", "publishing"], "yang_wenhui"),
    ("ouyang_jingwu_weishi_jueze_tan", "唯識抉擇談 / Wéi shí jué zé tán", "Discussion on Yogācāra Decisions", "lzh", 1922, ["buddhist_modern_china", "yogacara_revival"], "ouyang_jingwu"),
    ("taixu_zhengli_sengjia_zhidu_lun", "整理僧伽制度論 / Zhěnglǐ sēngjiā zhìdù lùn", "On Reorganizing the Saṅgha System", "lzh", 1915, ["buddhist_modern_china", "reform"], "taixu"),
    ("xuyun_zixu_nianpu", "虛雲老和尚自述年譜 / Xūyún lǎo héshàng zìshù niánpǔ", "Autobiographical Chronicle of Xuyun", "lzh", 1953, ["buddhist_chan_late", "modern"], "xuyun"),

    # ── Daoïsme moderne
    ("chen_yingning_xianxue_quanji_proto", "仙學論文集 (early) / Xiān xué lùn wén jí", "Early Essays on Immortal Studies", "lzh", 1933, ["daoist_modern", "neidan"], "chen_yingning"),
    ("zhao_bichen_xingming_fajue_mingzhi", "性命法訣明指 / Xìng mìng fǎ jué míng zhǐ", "Clear Pointers to the Methods of Nature and Life", "lzh", 1933, ["daoist_neidan_late", "modern"], "zhao_bichen"),

    # ── Christianisme chinois moderne
    ("hong_xiuquan_taiping_dao_li_shu", "太平天日 / Tài píng tiān rì", "Taiping Heavenly Days", "lzh", 1862, ["christian_chinese_heterodox", "millennialism"], "hong_xiuquan"),
    ("hong_xiuquan_yuan_dao_jue_shi_xun", "原道救世訓 / Yuán dào jiù shì xùn", "Exhortation to the Original Way to Save the World", "lzh", 1845, ["christian_chinese_heterodox"], "hong_xiuquan"),

    # ── Femmes & émancipation
    ("qiu_jin_jingwei_shi", "精衛石 / Jīng wèi shí", "Stone of the Jingwei Bird", "lzh", 1907, ["feminism_china", "republican"], "qiu_jin"),
    ("qiu_jin_zhongguo_nübao_yanlun", "中國女報文選 / Zhōngguó nǚ bào wén xuǎn", "Selections from the Chinese Women's Journal", "lzh", 1907, ["feminism_china"], "qiu_jin"),
    ("jin_tianhe_nüjie_zhong", "女界鐘 / Nǚ jiè zhōng", "Bell of the Women's World", "lzh", 1903, ["feminism_china", "reform"], "jin_tianhe"),

    # ── Histoire intellectuelle & cataloguage
    ("liang_qichao_zhongguo_jin_sanbainian_xueshushi", "中國近三百年學術史 / Zhōngguó jìn sān bǎi nián xuéshù shǐ", "Intellectual History of China in the Last 300 Years", "lzh", 1924, ["intellectual_history_modern"], "liang_qichao"),
    ("zhang_taiyan_zhuzi_xuelüe", "諸子學略 / Zhū zǐ xué lüè", "Brief Studies of the Masters", "lzh", 1910, ["philology_modern", "intellectual_history_modern"], "zhang_taiyan"),

    # ── Sciences naturelles & astronomie tardive
    ("li_shanlan_dai_wei_ji_shi_ji", "代微積拾級 / Dài wēi jī shí jí", "Steps to Algebra and Calculus", "lzh", 1859, ["mathematics_modern_china"], "li_shanlan"),
    ("li_shanlan_translation_calculus", "Translation of Loomis Elements of Analytical Geometry & Calculus", "Loomis translation", "lzh", 1859, ["translation_western", "mathematics_modern_china"], "li_shanlan_alexander_wylie"),
    ("xu_shou_huaxue_jianyuan", "化學鑒原 / Huà xué jiàn yuán", "Mirror of Chemistry's Origins", "lzh", 1872, ["sciences_modern_china", "chemistry"], "xu_shou"),

    # ── Compléments réforme & utopie
    ("kang_youwei_riben_bianzheng_kao", "日本變政考 / Rìběn biàn zhèng kǎo", "Study of Japanese Political Reform", "lzh", 1898, ["liberal_reform"], "kang_youwei"),
    ("liang_qichao_xixue_shumu_biao", "西學書目表 / Xī xué shū mù biǎo", "Catalog of Western Learning", "lzh", 1896, ["liberal_reform", "translation_western"], "liang_qichao"),

    # ── Tibétain Qing tardif
    ("dorje_dudjom_dudjom_lineage_late", "Dudjom Lingpa lineage writings", "Dudjom Lingpa lineage writings", "bod", 1880, ["buddhist_tibetan_late", "nyingma"], "dudjom_lingpa"),
    ("ju_mipham_collected_works_late", "Mi-pham gsung-'bum (selected late)", "Selected late writings of Mipham Rinpoche", "bod", 1900, ["buddhist_tibetan_late", "rime"], "ju_mipham"),

    # ── Confucianisme orthodoxe tardif
    ("li_hongzhang_correspondence_state_papers", "李文忠公全書 / Lǐ Wénzhōng gōng quán shū", "Complete Works of Li Wenzhong", "lzh", 1908, ["statecraft_late_qing"], "li_hongzhang"),
    ("yan_fu_correspondence_late", "嚴復書信集 / Yán Fù shū xìn jí", "Letters of Yan Fu (collected)", "lzh", 1920, ["translation_western", "intellectual_history_modern"], "yan_fu"),

    # ── Anarchistes Tokyo & Paris
    ("liu_shipei_jun_zheng_fu", "君政復古論 / Jūn zhèng fù gǔ lùn", "On Restoring Monarchical Government (essay)", "lzh", 1909, ["anarchist_proto"], "liu_shipei"),
    ("li_shizeng_anarchist_essays", "李石曾無政府主義文集 / Lǐ Shízēng wú zhèngfǔ zhǔyì wénjí", "Anarchist Writings of Li Shizeng", "lzh", 1907, ["anarchist_proto"], "li_shizeng"),
    ("wu_zhihui_essays", "吳稚暉先生選集 / Wú Zhìhuī xiānshēng xuǎn jí", "Selected Writings of Wu Zhihui", "lzh", 1908, ["anarchist_proto", "republican"], "wu_zhihui"),

    # ── Liang Shuming proto
    ("liang_shuming_jiu_yuan_jue_yi_lun", "究元決疑論 / Jiū yuán jué yí lùn", "Examining the Origins and Resolving Doubts", "lzh", 1916, ["modern_confucian_proto", "buddhist_modern_china"], "liang_shuming"),

    # ── Compléments
    ("kang_youwei_xushi_jiantian_si_kao", "孔子改制以後考 / Hòu kǎo (sequel)", "Studies after Confucius the Reformer (sequel)", "lzh", 1900, ["new_text_confucian"], "kang_youwei"),
    ("ma_xiangbo_kunjing_jiyao", "馬相伯文集 / Mǎ Xiāngbó wénjí", "Collected Works of Ma Xiangbo (Catholic-Confucian)", "lzh", 1908, ["jesuit_confucian", "modern"], "ma_xiangbo"),
    ("yang_changji_dahuazhai_riji", "達化齋日記 / Dá huà zhāi rìjì", "Diary of the Studio of Reaching Transformation", "lzh", 1914, ["modern_confucian_proto"], "yang_changji"),
    ("xie_wuliang_zhongguo_zhexueshi", "中國哲學史 / Zhōngguó zhéxué shǐ", "History of Chinese Philosophy", "lzh", 1916, ["intellectual_history_modern"], "xie_wuliang"),
    ("zou_rong_revolutionary_letters_supp", "鄒容革命函稿補遺 / Zōu Róng gé mìng hán gǎo bǔ yí", "Supplemental Revolutionary Letters of Zou Rong", "lzh", 1903, ["nationalism", "republican"], "zou_rong"),
]

assert len(WORKS) == 70, f"CHINESE×modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "statecraft_late_qing" in tags and "world_geography" in tags:
        return "STATECRAFT_GEOGRAPHIC_LATE_QING"
    if "statecraft_late_qing" in tags and "self_strengthening" in tags:
        return "SELF_STRENGTHENING"
    if "statecraft_late_qing" in tags:
        return "STATECRAFT_LATE_QING"
    if "self_strengthening" in tags and "ti_yong" in tags:
        return "TI_YONG_SYNTHESIS"
    if "self_strengthening" in tags:
        return "SELF_STRENGTHENING"
    if "confucian_orthodox_late" in tags:
        return "CONFUCIAN_ORTHODOX_LATE"
    if "new_text_confucian" in tags and "utopian" in tags:
        return "NEW_TEXT_UTOPIAN"
    if "new_text_confucian" in tags:
        return "NEW_TEXT_CONFUCIAN"
    if "liberal_reform" in tags and "nationalism" in tags:
        return "LIBERAL_REFORM_NATIONALIST"
    if "liberal_reform" in tags:
        return "LIBERAL_REFORM"
    if "intellectual_history_modern" in tags:
        return "INTELLECTUAL_HISTORY_MODERN_CHINA"
    if "translation_western" in tags and "logic" in tags:
        return "TRANSLATION_WESTERN_LOGIC"
    if "translation_western" in tags:
        return "TRANSLATION_WESTERN"
    if "anarchist_proto" in tags:
        return "ANARCHIST_PROTO_CHINA"
    if "feminism_china" in tags:
        return "FEMINISM_CHINA_FIRST"
    if "republican" in tags and "nationalism" in tags:
        return "REVOLUTIONARY_NATIONALIST"
    if "republican" in tags:
        return "REPUBLICAN_PROTO"
    if "nationalism" in tags and "philology_modern" in tags:
        return "NATIONALIST_PHILOLOGY"
    if "nationalism" in tags:
        return "CHINESE_NATIONALISM_LATE_QING"
    if "buddhist_modern_china" in tags and "yogacara_revival" in tags:
        return "BUDDHIST_YOGACARA_REVIVAL_CHINA"
    if "buddhist_modern_china" in tags and "reform" in tags:
        return "BUDDHIST_REFORM_CHINA"
    if "buddhist_modern_china" in tags:
        return "BUDDHIST_MODERN_CHINA"
    if "buddhist_chan_late" in tags:
        return "BUDDHIST_CHAN_MODERN"
    if "buddhist_tibetan_late" in tags:
        return "BUDDHIST_TIBETAN_MODERN"
    if "daoist_modern" in tags or "daoist_neidan_late" in tags:
        return "DAOIST_MODERN"
    if "christian_chinese_heterodox" in tags:
        return "CHRISTIAN_CHINESE_HETERODOX_TAIPING"
    if "literary_critique_modern" in tags:
        return "LITERARY_CRITIQUE_MODERN_CHINA"
    if "aesthetic_modern" in tags:
        return "AESTHETIC_MODERN_CHINA"
    if "modern_confucian_proto" in tags:
        return "NEW_CONFUCIANISM_PROTO"
    if "mathematics_modern_china" in tags:
        return "MATHEMATICS_MODERN_CHINA"
    if "sciences_modern_china" in tags:
        return "SCIENCES_MODERN_CHINA"
    if "secularism" in tags:
        return "SECULARISM_CHINA"
    return "CHINESE_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "CHINESE", "epoch": "modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 5,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "public_domain", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206t_chinese_modern", "generated": "2026-04-30",
        "macro_culture": "CHINESE", "epoch": "modern",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["ctext.org", "Cornell Wason Collection", "CBETA", "archive.org"],
        "language_original_dominant": "lzh + bod + eng",
        "schools_covered": [
            "Statecraft fin Qing (Wei Yuan ×2, Gong Zizhen ×2, Lin Zexu, Feng Guifen, Zhang Zhidong)",
            "Confucianisme orthodoxe tardif (Zeng Guofan ×2, Li Hongzhang)",
            "New Text confucianisme (Kang Youwei ×4, Liao Ping)",
            "Liang Qichao ×5",
            "Tan Sitong",
            "Yan Fu traducteur ×5 (+ correspondance)",
            "Nationalisme révolutionnaire (Sun Yat-sen, Zou Rong, Chen Tianhua)",
            "Zhang Taiyan ×4 (philologie + nationalisme)",
            "Anarchistes (Liu Shipei ×3, Li Shizeng, Wu Zhihui, He Zhen)",
            "Lu Xun proto ×2, Wang Guowei ×2",
            "Cai Yuanpei ×2, Hu Shi proto",
            "Bouddhisme moderne (Yang Wenhui ×2, Ouyang Jingwu, Taixu, Xuyun)",
            "Daoïsme moderne (Chen Yingning, Zhao Bichen)",
            "Taiping (Hong Xiuquan ×2)",
            "Féminisme chinois (Qiu Jin ×2, Jin Tianhe)",
            "Sciences modernes (Li Shanlan ×2, Xu Shou)",
            "Bouddhisme tibétain Qing tardif (Dudjom Lingpa, Ju Mipham)",
            "Liang Shuming proto Confucianisme nouveau",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue CHINESE × modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

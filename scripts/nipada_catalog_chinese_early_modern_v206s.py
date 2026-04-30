#!/usr/bin/env python3
"""§206s — CHINESE × early_modern (1500 → 1789), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_chinese_early_modern_v206s.json"

WORKS = [
    # ── École Wang Yangming tardive et école de Taizhou
    ("wang_yangming_da_xue_wen", "大學問 / Dà xué wèn", "Inquiry on the Great Learning", "lzh", 1527, ["neoconfucian_xinxue"], "wang_yangming"),
    ("wang_yangming_yangming_quanshu", "陽明全書 / Yángmíng quánshū", "Complete Works of Wang Yangming", "lzh", 1572, ["neoconfucian_xinxue"], "wang_yangming"),
    ("wang_yangming_late_correspondence", "陸澄並書 / Yú Lu Chéng bì shū", "Late Letters to Lu Cheng and Others", "lzh", 1525, ["neoconfucian_xinxue"], "wang_yangming"),
    ("wang_ji_longxi_wenji", "龍溪王先生全集 / Lóngxī Wáng xiānshēng quánjí", "Complete Works of Wang Longxi", "lzh", 1583, ["neoconfucian_xinxue"], "wang_ji"),
    ("wang_gen_xinzhai_wenji", "心齋先生全集 / Xīnzhāi xiānshēng quánjí", "Complete Works of Wang Xinzhai", "lzh", 1631, ["neoconfucian_taizhou"], "wang_gen"),
    ("li_zhi_xu_fenshu", "續焚書 / Xù fén shū", "A Sequel to A Book to Burn", "lzh", 1602, ["neoconfucian_taizhou", "iconoclast"], "li_zhi"),
    ("li_zhi_cangshu", "藏書 / Cáng shū", "A Book to Hide", "lzh", 1599, ["neoconfucian_taizhou", "history"], "li_zhi"),
    ("luo_rufang_jinxi_zilu", "近溪子錄 / Jìnxī zǐ lù", "Records of Master Jinxi", "lzh", 1593, ["neoconfucian_taizhou"], "luo_rufang"),
    ("liu_zongzhou_renpu", "人譜 / Rén pǔ", "Manual on Becoming Human", "lzh", 1634, ["neoconfucian_dongling"], "liu_zongzhou"),

    # ── Donglin Academy & critique politique
    ("gu_xiancheng_donglin_huiyu", "東林會語 / Dōnglín huì yǔ", "Donglin Academy Conversations", "lzh", 1604, ["neoconfucian_dongling", "political_critique"], "gu_xiancheng"),
    ("gao_panlong_gaozi_yishu", "高子遺書 / Gāo zǐ yíshū", "Bequeathed Writings of Master Gao", "lzh", 1632, ["neoconfucian_dongling"], "gao_panlong"),

    # ── Qing initial : Trois grands penseurs critiques
    ("wang_fuzhi_zhuangzi_jie", "莊子解 / Zhuāngzǐ jiě", "Explication of the Zhuangzi", "lzh", 1670, ["confucian_qing", "daoist_critique"], "wang_fuzhi"),
    ("wang_fuzhi_du_tongjian_lun", "讀通鑑論 / Dú tōngjiàn lùn", "Discourses on Reading the Comprehensive Mirror", "lzh", 1687, ["confucian_qing", "history"], "wang_fuzhi"),
    ("wang_fuzhi_zhang_zi_zheng_meng_zhu", "張子正蒙注 / Zhāng zǐ Zhèng méng zhù", "Commentary on Zhang Zai's Correcting Youthful Ignorance", "lzh", 1685, ["confucian_qing", "neoconfucian_revival"], "wang_fuzhi"),
    ("wang_fuzhi_si_jie", "思問錄 / Sī wèn lù", "Records of Reflective Inquiry", "lzh", 1675, ["confucian_qing"], "wang_fuzhi"),
    ("wang_fuzhi_song_lun", "宋論 / Sòng lùn", "Discourses on the Song Dynasty", "lzh", 1691, ["confucian_qing", "history"], "wang_fuzhi"),
    ("gu_yanwu_rizhi_lu", "日知錄 / Rì zhī lù", "Record of Daily Knowledge", "lzh", 1670, ["confucian_qing", "kaozheng"], "gu_yanwu"),
    ("gu_yanwu_tianxia_junguo_libingshu", "天下郡國利病書 / Tiānxià jùn guó lì bìng shū", "Strengths and Weaknesses of the Empire's Regions", "lzh", 1662, ["confucian_qing", "statecraft"], "gu_yanwu"),
    ("gu_yanwu_yinxue_wushu", "音學五書 / Yīnxué wǔ shū", "Five Books on Phonology", "lzh", 1667, ["kaozheng", "philology"], "gu_yanwu"),
    ("huang_zongxi_mingyi_daifang_lu", "明夷待訪錄 / Míngyí dàifǎng lù", "Waiting for the Dawn: A Plan for the Prince", "lzh", 1663, ["confucian_qing", "political_critique"], "huang_zongxi"),
    ("huang_zongxi_mingru_xuean", "明儒學案 / Míng rú xué àn", "Scholarly Cases of Ming Confucians", "lzh", 1676, ["confucian_qing", "intellectual_history"], "huang_zongxi"),
    ("huang_zongxi_song_yuan_xuean", "宋元學案 / Sòng Yuán xué àn", "Scholarly Cases of Song-Yuan Confucians", "lzh", 1701, ["confucian_qing", "intellectual_history"], "huang_zongxi"),

    # ── Yan Yuan / Li Gong : pragmatisme confucéen
    ("yan_yuan_sicun_bian", "四存編 / Sì cún biān", "Four Treatises on Preservation", "lzh", 1700, ["confucian_qing", "pragmatist_school"], "yan_yuan"),
    ("yan_yuan_cunxue_bian", "存學編 / Cún xué biān", "On Preserving Learning", "lzh", 1696, ["confucian_qing", "pragmatist_school"], "yan_yuan"),
    ("li_gong_zhouyi_zhuan_zhu", "周易傳註 / Zhōu yì zhuàn zhù", "Commentary on the Book of Changes", "lzh", 1719, ["confucian_qing", "yijing"], "li_gong"),

    # ── Évidentialisme (kaozheng) Qing
    ("dai_zhen_mengzi_ziyi_shuzheng", "孟子字義疏證 / Mèngzǐ zì yì shū zhèng", "Evidential Study of the Meaning of Mencius's Terms", "lzh", 1777, ["kaozheng", "neoconfucian_critique"], "dai_zhen"),
    ("dai_zhen_yuan_shan", "原善 / Yuán shàn", "On the Origin of Goodness", "lzh", 1769, ["kaozheng", "ethics"], "dai_zhen"),
    ("dai_zhen_xugian_lu", "緒言 / Xù yán", "Preliminary Words", "lzh", 1775, ["kaozheng"], "dai_zhen"),
    ("hui_dong_jiu_jing_guyi", "九經古義 / Jiǔ jīng gǔ yì", "Ancient Meanings of the Nine Classics", "lzh", 1758, ["kaozheng", "philology"], "hui_dong"),
    ("ruan_yuan_jingji_zhuanlue", "經籍纂詁 / Jīng jí zuǎn gǔ", "Compiled Glosses on the Classics", "lzh", 1798, ["kaozheng", "philology"], "ruan_yuan"),
    ("duan_yucai_shuowen_jiezi_zhu", "說文解字注 / Shuōwén jiězì zhù", "Commentary on the Shuowen Jiezi", "lzh", 1815, ["kaozheng", "philology"], "duan_yucai"),
    ("wang_niansun_dushu_zazhi", "讀書雜志 / Dú shū zá zhì", "Miscellaneous Records of Reading", "lzh", 1812, ["kaozheng", "philology"], "wang_niansun"),
    ("ji_yun_yuewei_caotang_biji", "閱微草堂筆記 / Yuèwēi cǎotáng bǐjì", "Notes from the Thatched Abode of Close Observations", "lzh", 1798, ["kaozheng", "literati_notes"], "ji_yun"),
    ("siku_quanshu_general_catalog", "四庫全書總目提要 / Sìkù quánshū zǒngmù tíyào", "Annotated Catalog of the Complete Library", "lzh", 1782, ["kaozheng", "encyclopedia"], "ji_yun"),

    # ── Néo-confucianisme orthodoxe Qing (Zhu Xi school continuation)
    ("zhang_lüxiang_yangzhe_quanshu", "楊園先生全集 / Yángyuán xiānshēng quánjí", "Complete Works of Master Yangyuan", "lzh", 1671, ["neoconfucian_orthodox_qing"], "zhang_lüxiang"),
    ("li_guangdi_zhuzi_quanshu", "朱子全書 / Zhū zǐ quánshū", "Complete Works of Master Zhu (imperial edition)", "lzh", 1714, ["neoconfucian_orthodox_qing"], "li_guangdi"),
    ("xingli_jingyi", "性理精義 / Xìnglǐ jīngyì", "Essential Meaning of Nature and Principle", "lzh", 1715, ["neoconfucian_orthodox_qing"], "li_guangdi"),

    # ── Bouddhisme Ming tardif : "Quatre maîtres éminents"
    ("yunqi_zhuhong_zhu_chuang_sanbi", "竹窗三筆 / Zhú chuāng sān bǐ", "Three Notes from the Bamboo Window", "lzh", 1600, ["buddhist_chan_late"], "yunqi_zhuhong"),
    ("yunqi_zhuhong_amitabha_jing_shuchao", "阿彌陀經疏鈔 / Āmítuó jīng shū chāo", "Subcommentary on the Amitābha Sūtra", "lzh", 1584, ["buddhist_pure_land_late"], "yunqi_zhuhong"),
    ("hanshan_deqing_mengyou_ji", "夢遊集 / Mèng yóu jí", "Dream Wanderings Collection", "lzh", 1622, ["buddhist_chan_late"], "hanshan_deqing"),
    ("hanshan_deqing_laozi_zhuangzi_zhu", "老子莊子註 / Lǎozǐ Zhuāngzǐ zhù", "Commentary on Laozi and Zhuangzi", "lzh", 1610, ["buddhist_chan_late", "syncretism_three_teachings"], "hanshan_deqing"),
    ("zibo_zhenke_zibo_zunzhe_quanji", "紫柏尊者全集 / Zǐbǎi zūn zhě quánjí", "Complete Works of Reverend Zibai", "lzh", 1607, ["buddhist_chan_late"], "zibo_zhenke"),
    ("ouyi_zhixu_jiaoguan_gangzong", "教觀綱宗 / Jiào guān gāng zōng", "Outline of Tiantai Doctrine and Contemplation", "lzh", 1635, ["buddhist_tiantai_late"], "ouyi_zhixu"),
    ("ouyi_zhixu_zhouyi_chanjie", "周易禪解 / Zhōu yì chán jiě", "Chan Interpretation of the Yijing", "lzh", 1641, ["buddhist_chan_late", "yijing"], "ouyi_zhixu"),

    # ── Daoïsme Ming-Qing
    ("wu_chengen_xiyou_ji", "西遊記 / Xī yóu jì", "Journey to the West", "lzh", 1592, ["daoist_buddhist_syncretism", "novel"], "wu_chengen"),
    ("zhang_sanfeng_quanji", "張三丰全集 / Zhāng Sānfēng quánjí", "Complete Works of Zhang Sanfeng (Ming compilation)", "lzh", 1723, ["daoist_neidan_late"], "zhang_sanfeng_compilers"),
    ("wu_shouyang_xianfo_hezong", "仙佛合宗 / Xiān fó hé zōng", "Combined Tradition of Immortals and Buddhas", "lzh", 1640, ["daoist_neidan_late"], "wu_shouyang"),
    ("liu_yiming_dao_shu_shi'er_zhong", "道書十二種 / Dào shū shí'èr zhǒng", "Twelve Categories of Daoist Books", "lzh", 1788, ["daoist_neidan_late"], "liu_yiming"),
    ("liu_yiming_xiyou_yuanzhi", "西遊原旨 / Xī yóu yuán zhǐ", "Original Meaning of Journey to the West", "lzh", 1778, ["daoist_neidan_late"], "liu_yiming"),

    # ── Christianisme jésuite-confucéen
    ("ricci_tianzhu_shiyi", "天主實義 / Tiānzhǔ shíyì", "True Meaning of the Lord of Heaven", "lzh", 1603, ["jesuit_confucian"], "matteo_ricci"),
    ("xu_guangqi_nongzheng_quanshu", "農政全書 / Nóng zhèng quán shū", "Complete Treatise on Agriculture", "lzh", 1639, ["jesuit_confucian", "sciences"], "xu_guangqi"),
    ("xu_guangqi_jihe_yuanben", "幾何原本 / Jǐhé yuán běn", "Elements of Geometry (Euclid translation)", "lzh", 1607, ["jesuit_confucian", "mathematics"], "xu_guangqi"),
    ("li_zhizao_tongwen_suanzhi", "同文算指 / Tóngwén suànzhǐ", "Rules of Calculation Common to Cultures", "lzh", 1614, ["jesuit_confucian", "mathematics"], "li_zhizao"),
    ("yang_tingyun_dai_yi_pian", "代疑篇 / Dài yí piān", "Replies to Doubts (on Christianity)", "lzh", 1621, ["jesuit_confucian"], "yang_tingyun"),

    # ── Romans philosophiques
    ("cao_xueqin_honglou_meng", "紅樓夢 / Hóng lóu mèng", "Dream of the Red Chamber", "lzh", 1763, ["novel_philosophical", "buddhist_daoist_imagery"], "cao_xueqin"),
    ("wu_jingzi_rulin_waishi", "儒林外史 / Rúlín wàishǐ", "The Scholars (Unofficial History of the Forest of Scholars)", "lzh", 1750, ["novel_philosophical", "confucian_critique"], "wu_jingzi"),
    ("pu_songling_liaozhai_zhiyi", "聊齋誌異 / Liáo zhāi zhì yì", "Strange Stories from a Chinese Studio", "lzh", 1740, ["novel_philosophical", "literati_notes"], "pu_songling"),
    ("ming_jin_ping_mei", "金瓶梅 / Jīn píng méi", "The Plum in the Golden Vase", "lzh", 1610, ["novel_philosophical"], "lanling_xiaoxiaosheng"),

    # ── Statecraft & gouvernement Qing
    ("kangxi_shengxun", "聖訓 / Shèngxùn (Kāngxī)", "Sacred Edicts of the Kangxi Emperor", "lzh", 1700, ["statecraft", "imperial_doctrine"], "kangxi_emperor"),
    ("yongzheng_dayi_juemi_lu", "大義覺迷錄 / Dà yì jué mí lù", "Record of Awakening to the Great Righteousness", "lzh", 1730, ["statecraft", "imperial_doctrine"], "yongzheng_emperor"),
    ("qianlong_yuzhi_shi_wen", "御製詩文 / Yùzhì shī wén", "Imperial Poems and Prose of Qianlong", "lzh", 1780, ["statecraft", "imperial_doctrine"], "qianlong_emperor"),

    # ── Esthétique et critique
    ("ye_xie_yuan_shi", "原詩 / Yuán shī", "Origins of Poetry", "lzh", 1690, ["aesthetic_criticism"], "ye_xie"),
    ("li_yu_xianqing_ouji", "閒情偶寄 / Xián qíng ǒu jì", "Casual Expressions of Idle Feeling", "lzh", 1671, ["aesthetic_criticism", "literati_notes"], "li_yu"),
    ("yuan_mei_suiyuan_shihua", "隨園詩話 / Suíyuán shī huà", "Suiyuan's Poetry Talks", "lzh", 1788, ["aesthetic_criticism"], "yuan_mei"),

    # ── Études classiques tardives
    ("wang_fuzhi_yi_wai_zhuan", "周易外傳 / Zhōu yì wài zhuàn", "Outer Commentary on the Yijing", "lzh", 1655, ["confucian_qing", "yijing"], "wang_fuzhi"),
    ("hui_shiqi_yili_shuo", "易例 / Yì lì", "Models for the Yijing", "lzh", 1730, ["kaozheng", "yijing"], "hui_shiqi"),

    # ── Tibétan-Chinese late tantric (côté Pékin officiel)
    ("changkya_rolpe_dorje_doctrines_compendium", "Grub mtha' thub bstan lhun po'i mdzes rgyan", "Beautiful Ornament of Tenets", "bod", 1750, ["buddhist_tibetan_qing"], "changkya_rolpe_dorje"),

    # ── Compléments école Wang Yangming + Buddhist Ming
    ("luo_qinshun_late_correspondence", "整庵先生存稿 / Zhěngān xiānshēng cúng gǎo", "Surviving Drafts of Master Zheng'an", "lzh", 1545, ["neoconfucian_qixue"], "luo_qinshun"),
    ("zhanruoshui_ganquan_wenji", "甘泉文集 / Gānquán wénjí", "Collected Works of Zhanruoshui", "lzh", 1560, ["neoconfucian_xinxue"], "zhan_ruoshui"),
    ("buddhist_yongjue_yuanxian_yongjue_yulu", "永覺元賢禪師廣錄 / Yǒngjué Yuánxián chánshī guǎng lù", "Extensive Records of Chan Master Yongjue Yuanxian", "lzh", 1657, ["buddhist_chan_late"], "yongjue_yuanxian"),
]

assert len(WORKS) == 70, f"CHINESE×early_modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "neoconfucian_xinxue" in tags:
        return "NEOCONFUCIAN_XINXUE"
    if "neoconfucian_taizhou" in tags:
        return "NEOCONFUCIAN_TAIZHOU"
    if "neoconfucian_dongling" in tags:
        return "NEOCONFUCIAN_DONGLIN"
    if "neoconfucian_qixue" in tags:
        return "NEOCONFUCIAN_QIXUE"
    if "neoconfucian_orthodox_qing" in tags:
        return "NEOCONFUCIAN_ORTHODOX_QING"
    if "neoconfucian_revival" in tags:
        return "NEOCONFUCIAN_REVIVAL_QING"
    if "confucian_qing" in tags and "history" in tags:
        return "CONFUCIAN_QING_HISTORIAN"
    if "confucian_qing" in tags and "political_critique" in tags:
        return "CONFUCIAN_QING_POLITICAL"
    if "confucian_qing" in tags and "pragmatist_school" in tags:
        return "CONFUCIAN_QING_PRAGMATIST"
    if "confucian_qing" in tags and "kaozheng" in tags:
        return "CONFUCIAN_QING_KAOZHENG"
    if "confucian_qing" in tags and "intellectual_history" in tags:
        return "CONFUCIAN_QING_INTELLECTUAL_HISTORY"
    if "confucian_qing" in tags:
        return "CONFUCIAN_QING_GENERAL"
    if "kaozheng" in tags and "philology" in tags:
        return "KAOZHENG_PHILOLOGY"
    if "kaozheng" in tags and "yijing" in tags:
        return "KAOZHENG_YIJING"
    if "kaozheng" in tags:
        return "KAOZHENG_EVIDENTIAL"
    if "buddhist_pure_land_late" in tags:
        return "BUDDHIST_PURE_LAND_LATE"
    if "buddhist_tiantai_late" in tags:
        return "BUDDHIST_TIANTAI_LATE"
    if "buddhist_chan_late" in tags:
        return "BUDDHIST_CHAN_LATE"
    if "buddhist_tibetan_qing" in tags:
        return "BUDDHIST_TIBETAN_QING"
    if "daoist_neidan_late" in tags:
        return "DAOIST_NEIDAN_LATE"
    if "daoist_buddhist_syncretism" in tags:
        return "DAOIST_BUDDHIST_NOVEL"
    if "jesuit_confucian" in tags:
        return "JESUIT_CONFUCIAN"
    if "novel_philosophical" in tags:
        return "NOVEL_PHILOSOPHICAL"
    if "statecraft" in tags:
        return "STATECRAFT_IMPERIAL"
    if "aesthetic_criticism" in tags:
        return "AESTHETIC_CRITICISM"
    return "CHINESE_EARLY_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "CHINESE", "epoch": "early_modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 10,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "public_domain", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206s_chinese_early_modern", "generated": "2026-04-30",
        "macro_culture": "CHINESE", "epoch": "early_modern",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["ctext.org", "Chinese Buddhist Electronic Text Association (CBETA)", "Daoist Canon"],
        "language_original_dominant": "lzh + bod",
        "schools_covered": [
            "École Wang Yangming tardive (Wang Yangming ×3, Wang Ji, Zhanruoshui, Luo Qinshun)",
            "École Taizhou (Wang Gen, Li Zhi ×2, Luo Rufang)",
            "Académie Donglin & Liu Zongzhou (Gu Xiancheng, Gao Panlong, Liu Zongzhou)",
            "Trois grands penseurs Qing (Wang Fuzhi ×6, Gu Yanwu ×3, Huang Zongxi ×3)",
            "Yan-Li school pragmatiste (Yan Yuan ×2, Li Gong)",
            "Évidentialisme (Dai Zhen ×3, Hui Dong, Ruan Yuan, Duan Yucai, Wang Niansun, Ji Yun ×2)",
            "Néo-confucianisme orthodoxe Qing (Zhang Lüxiang, Li Guangdi ×2)",
            "Bouddhisme Ming tardif Quatre maîtres (Yunqi Zhuhong ×2, Hanshan Deqing ×2, Zibo, Ouyi ×2, Yongjue)",
            "Daoïsme Ming-Qing (Wu Chengen, Zhang Sanfeng comp., Wu Shouyang, Liu Yiming ×2)",
            "Christianisme jésuite-confucéen (Ricci, Xu Guangqi ×2, Li Zhizao, Yang Tingyun)",
            "Romans philosophiques (Cao Xueqin, Wu Jingzi, Pu Songling, Jin Ping Mei)",
            "Statecraft impérial (Kangxi, Yongzheng, Qianlong)",
            "Esthétique & critique (Ye Xie, Li Yu, Yuan Mei)",
            "Études classiques tardives (Hui Shiqi)",
            "Bouddhisme tibétain Qing (Changkya Rolpe Dorje)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue CHINESE × early_modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

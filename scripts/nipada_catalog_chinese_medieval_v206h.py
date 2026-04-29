#!/usr/bin/env python3
"""
§206h — Catalogue CHINESE × medieval (500 → 1500 CE), 70 œuvres.

Strates :
- Sui-Tang Buddhism : Tiantai (Zhiyi), Huayan (Fazang), Faxiang (Xuanzang),
  Chan (Bodhidharma → 6 patriarches), Pure Land (Tanluan, Daochuo, Shandao)
- Tang poetry & cosmopolitanism (réf. Daoist + Buddhist canon)
- Tang-Song Daoism : Sima Chengzhen, Zhang Boduan
- Song neo-Confucianism : Zhou Dunyi, Shao Yong, Zhang Zai, Cheng Hao,
  Cheng Yi, Zhu Xi (Sì Shū Jí Zhù), Lu Jiuyuan, Chen Liang
- Song-Yuan Buddhism : Linji Yulu, Wumenguan, Bi Yan Lu, Platform Sūtra,
  Tan Luan canonized, Zongmi
- Tao Tsang medieval : Wuzhen Pian, Yunji Qiqian
- Ming neo-Confucianism : Wang Yangming, Luo Qinshun
- Histoire & encyclopedies : Tang Liu Dian, Tongdian, Zizhi Tongjian,
  Yongle Dadian
- Médecine : Sun Simiao Beiji Qianjin Yaofang, Wang Tao Waitai Miyao,
  Bencao Gangmu (Li Shizhen, late Ming charnière)
- Xuanzang Cheng Weishi Lun (Faxiang)

Sources : ctext.org, CBETA, sacred-texts.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_chinese_medieval_v206h.json"

WORKS = [
    # ── Tang Buddhism — Tiantai
    ("zhiyi_mohe_zhiguan", "Móhē Zhǐguān 摩訶止觀", "Great Calming and Contemplation", "lzh", 594, ["buddhist", "tiantai"], "zhiyi"),
    ("zhiyi_fahua_xuanyi", "Fǎhuá Xuányì 法華玄義", "Profound Meaning of the Lotus", "lzh", 593, ["buddhist", "tiantai", "lotus"], "zhiyi"),
    ("zhiyi_fahua_wenju", "Fǎhuá Wénjù 法華文句", "Words and Phrases of the Lotus", "lzh", 587, ["buddhist", "tiantai", "lotus"], "zhiyi"),
    ("zhiyi_xiao_zhiguan", "Xiǎo Zhǐguān 小止觀", "Small Calming and Contemplation", "lzh", 590, ["buddhist", "tiantai"], "zhiyi"),

    # ── Huayan
    ("fazang_huayan_jing_tanxuan", "Huāyán Jīng Tànxuán Jì 華嚴經探玄記", "Searching the Profundities of Avataṃsaka", "lzh", 700, ["buddhist", "huayan"], "fazang"),
    ("fazang_jin_shizi_zhang", "Jīn Shīzi Zhāng 金師子章", "Treatise on the Golden Lion", "lzh", 700, ["buddhist", "huayan"], "fazang"),
    ("fazang_wujiao_zhang", "Wǔjiào Zhāng 五教章", "Treatise on the Five Teachings", "lzh", 700, ["buddhist", "huayan"], "fazang"),
    ("chengguan_huayan_shu", "Huāyán Shū 華嚴疏", "Commentary on Avataṃsaka", "lzh", 800, ["buddhist", "huayan"], "chengguan"),

    # ── Faxiang (Yogācāra chinois)
    ("xuanzang_cheng_weishi_lun", "Chéng Wéishí Lùn 成唯識論", "Demonstration of Consciousness-only", "lzh", 659, ["buddhist", "yogacara"], "xuanzang"),
    ("xuanzang_da_tang_xiyu_ji", "Dà Táng Xīyù Jì 大唐西域記", "Great Tang Records on Western Regions", "lzh", 646, ["buddhist", "travel"], "xuanzang"),
    ("kuiji_cheng_weishi_shu", "Chéng Wéishí Lùn Shù Jì 成唯識論述記", "Notes on the Cheng Weishi Lun", "lzh", 680, ["buddhist", "yogacara"], "kuiji"),

    # ── Chan/Zen
    ("liuzu_tanjing", "Liùzǔ Tánjīng 六祖壇經", "Platform Sutra of the Sixth Patriarch", "lzh", 780, ["buddhist", "chan"], "huineng"),
    ("xinxin_ming", "Xìnxīn Míng 信心銘", "Faith in Mind Inscription", "lzh", 600, ["buddhist", "chan"], "sengcan"),
    ("zhengdao_ge", "Zhèngdào Gē 證道歌", "Song of Enlightenment", "lzh", 700, ["buddhist", "chan"], "yongjia"),
    ("linji_yulu", "Línjì Yǔlù 臨濟錄", "Recorded Sayings of Linji", "lzh", 866, ["buddhist", "chan"], "linji_yixuan"),
    ("dongshan_yulu", "Dòngshān Yǔlù 洞山錄", "Recorded Sayings of Dongshan", "lzh", 869, ["buddhist", "chan"], "dongshan_liangjie"),
    ("baoji_jing", "Bǎojì Jīng 寶積經 (Caodong)", "Caodong Treasure Mirror Samādhi", "lzh", 850, ["buddhist", "chan"], "dongshan_liangjie"),
    ("wumenguan", "Wúménguān 無門關", "Gateless Barrier", "lzh", 1228, ["buddhist", "chan", "koan"], "wumen_huikai"),
    ("bi_yan_lu", "Bì Yán Lù 碧巖錄", "Blue Cliff Record", "lzh", 1125, ["buddhist", "chan", "koan"], "yuanwu_keqin"),
    ("congrong_lu", "Cóngróng Lù 從容錄", "Book of Serenity", "lzh", 1224, ["buddhist", "chan", "koan"], "wansong_xingxiu"),
    ("dahui_yulu", "Dàhuì Yǔlù 大慧語錄", "Recorded Sayings of Dahui", "lzh", 1163, ["buddhist", "chan"], "dahui_zonggao"),
    ("hongzhi_yulu", "Hóngzhì Yǔlù 宏智錄", "Recorded Sayings of Hongzhi", "lzh", 1157, ["buddhist", "chan", "silent_illumination"], "hongzhi_zhengjue"),

    # ── Pure Land
    ("tanluan_wangsheng_lunzhu", "Wǎngshēng Lùnzhù 往生論註", "Commentary on the Rebirth Treatise", "lzh", 542, ["buddhist", "pureland"], "tanluan"),
    ("daochuo_anle_ji", "Ānlè Jí 安樂集", "Collection on Peace and Bliss", "lzh", 645, ["buddhist", "pureland"], "daochuo"),
    ("shandao_guannianfa", "Guānniàn Fǎmén 觀念法門", "Methods of Contemplation", "lzh", 650, ["buddhist", "pureland"], "shandao"),
    ("shandao_wangsheng_lizan", "Wǎngshēng Lǐzàn 往生禮讚", "Hymns of Rebirth", "lzh", 670, ["buddhist", "pureland"], "shandao"),

    # ── Zongmi (Chan-Huayan synthesis)
    ("zongmi_chan_yuan_zhuxu", "Chán Yuán Zhū Xù 禪源諸詮集都序", "Preface to the Collected Writings on the Source of Chan", "lzh", 833, ["buddhist", "chan", "huayan"], "zongmi"),
    ("zongmi_yuanren_lun", "Yuánrén Lùn 原人論", "Inquiry into Human Nature", "lzh", 830, ["buddhist", "huayan"], "zongmi"),

    # ── Daoism Tang-Song
    ("zuowanglun", "Zuòwàng Lùn 坐忘論", "On Sitting and Forgetting", "lzh", 720, ["daoism"], "sima_chengzhen"),
    ("yunji_qiqian", "Yúnjí Qīqiān 雲笈七籤", "Seven Slips of the Cloudy Satchel", "lzh", 1029, ["daoism", "encyclopedia"], "zhang_junfang"),
    ("wuzhen_pian", "Wùzhēn Piān 悟真篇", "Folios on Awakening to the Real", "lzh", 1075, ["daoism", "alchemy"], "zhang_boduan"),
    ("baopuzi_song_recension", "Bàopǔzǐ (Song recension)", "Bàopǔzǐ in Tao Tsang", "lzh", 1100, ["daoism", "alchemy"], None),

    # ── Song neo-Confucianism
    ("zhou_dunyi_taiji_tushuo", "Tàijí Túshuō 太極圖說", "Explanation of the Diagram of the Supreme Polarity", "lzh", 1060, ["neoconfucian", "song"], "zhou_dunyi"),
    ("zhou_dunyi_tongshu", "Tōngshū 通書", "Penetrating the Yi", "lzh", 1060, ["neoconfucian", "song"], "zhou_dunyi"),
    ("shao_yong_huangji_jingshi", "Huángjí Jīngshì 皇極經世", "Supreme Principles Governing the World", "lzh", 1070, ["neoconfucian", "yijing"], "shao_yong"),
    ("zhang_zai_zhengmeng", "Zhèng Méng 正蒙", "Correcting Youthful Ignorance", "lzh", 1076, ["neoconfucian", "song"], "zhang_zai"),
    ("zhang_zai_ximing", "Xī Míng 西銘", "Western Inscription", "lzh", 1076, ["neoconfucian"], "zhang_zai"),
    ("cheng_yi_yichuan_yizhuan", "Yīchuān Yìzhuàn 伊川易傳", "Cheng Yi's Yijing Commentary", "lzh", 1099, ["neoconfucian", "yijing"], "cheng_yi"),
    ("ercheng_yishu", "Èrchéng Yíshū 二程遺書", "Surviving Works of the Two Chengs", "lzh", 1100, ["neoconfucian"], "cheng_brothers"),
    ("zhu_xi_sishu_jizhu", "Sì Shū Jí Zhù 四書集注", "Collected Commentaries on the Four Books", "lzh", 1190, ["neoconfucian", "song"], "zhu_xi"),
    ("zhu_xi_zhouyi_benyi", "Zhōuyì Běnyì 周易本義", "Original Meaning of the Yi", "lzh", 1188, ["neoconfucian", "yijing"], "zhu_xi"),
    ("zhu_xi_jinsi_lu", "Jìnsī Lù 近思錄", "Reflections on Things at Hand", "lzh", 1175, ["neoconfucian", "song"], "zhu_xi_lu_zuqian"),
    ("zhu_xi_yulei", "Zhūzǐ Yǔlèi 朱子語類", "Classified Sayings of Master Zhu", "lzh", 1270, ["neoconfucian"], "zhu_xi"),
    ("zhu_xi_xiaoxue", "Xiǎoxué 小學", "Elementary Learning", "lzh", 1187, ["neoconfucian"], "zhu_xi"),
    ("lu_jiuyuan_xiangshan_quanji", "Xiàngshān Quánjí 象山全集", "Complete Works of Lu Xiangshan", "lzh", 1190, ["neoconfucian", "song", "xinxue"], "lu_jiuyuan"),
    ("chen_liang_longchuan_wenji", "Lóngchuān Wénjí 龍川文集", "Chen Liang's Collected Works", "lzh", 1193, ["neoconfucian", "utilitarian"], "chen_liang"),
    ("ye_shi_xixue_jiyan", "Xíxué Jìyán 習學記言", "Notes on Learning", "lzh", 1220, ["neoconfucian", "yongjia"], "ye_shi"),

    # ── Ming neo-Confucianism
    ("wang_yangming_chuanxi_lu", "Chuánxí Lù 傳習錄", "Instructions for Practical Living", "lzh", 1518, ["neoconfucian", "ming", "xinxue"], "wang_yangming"),
    ("wang_yangming_daxue_wen", "Dàxué Wèn 大學問", "Inquiry on the Great Learning", "lzh", 1527, ["neoconfucian", "ming"], "wang_yangming"),
    ("luo_qinshun_kunzhi_ji", "Kùnzhī Jì 困知記", "Knowledge Painfully Acquired", "lzh", 1528, ["neoconfucian", "ming"], "luo_qinshun"),
    ("wang_ji_longxi_huiyu", "Lóngxī Huìyǔ 龍溪會語", "Wang Ji's Discussions", "lzh", 1570, ["neoconfucian", "ming", "xinxue"], "wang_ji"),
    ("li_zhi_fenshu", "Fénshū 焚書", "A Book to Burn", "lzh", 1590, ["heterodox", "ming"], "li_zhi"),

    # ── History / encyclopedies
    ("tang_liu_dian", "Táng Liù Diǎn 唐六典", "Six Statutes of the Tang", "lzh", 738, ["history", "law"], None),
    ("tongdian", "Tōngdiǎn 通典", "Comprehensive Statutes", "lzh", 801, ["history", "encyclopedia"], "du_you"),
    ("zizhi_tongjian", "Zīzhì Tōngjiàn 資治通鑑", "Comprehensive Mirror in Aid of Governance", "lzh", 1084, ["history"], "sima_guang"),
    ("zizhi_tongjian_gangmu", "Tōngjiàn Gāngmù 通鑑綱目", "Outline of the Comprehensive Mirror", "lzh", 1172, ["history"], "zhu_xi"),
    ("yongle_dadian_summary", "Yǒnglè Dàdiǎn 永樂大典 (extant fragments)", "Yongle Encyclopedia (surviving)", "lzh", 1408, ["encyclopedia"], None),
    ("tongzhi", "Tōngzhì 通志", "Comprehensive Records", "lzh", 1161, ["history"], "zheng_qiao"),

    # ── Médecine
    ("beiji_qianjin_yaofang", "Bèijí Qiānjīn Yàofāng 備急千金要方", "Essential Prescriptions for Every Emergency", "lzh", 652, ["medicine"], "sun_simiao"),
    ("qianjin_yifang", "Qiānjīn Yìfāng 千金翼方", "Supplement to Thousand-Gold Prescriptions", "lzh", 682, ["medicine"], "sun_simiao"),
    ("waitai_miyao", "Wàitái Mìyào 外臺秘要", "Arcane Essentials from the Imperial Library", "lzh", 752, ["medicine"], "wang_tao"),
    ("taiping_huimin_hejiju_fang", "Tàipíng Huìmín Héjìjú Fāng 太平惠民和劑局方", "Imperial Pharmacy Formulary", "lzh", 1078, ["medicine", "pharmacy"], None),
    ("pi_wei_lun", "Pí Wèi Lùn 脾胃論", "Treatise on the Spleen and Stomach", "lzh", 1249, ["medicine"], "li_dongyuan"),

    # ── Tang lit / aesthetics
    ("zhu_xi_chuci_jizhu", "Chǔcí Jí Zhù 楚辭集注", "Collected Commentaries on the Songs of Chu", "lzh", 1199, ["literature", "neoconfucian"], "zhu_xi"),
    ("yan_yu_canglang_shihua", "Cānglàng Shīhuà 滄浪詩話", "Canglang's Talks on Poetry", "lzh", 1244, ["aesthetics", "literature"], "yan_yu"),
    ("liu_zongyuan_essays", "Liǔ Zōngyuán Wénjí 柳宗元文集", "Liu Zongyuan's Collected Prose", "lzh", 815, ["literature", "neoconfucian_proto"], "liu_zongyuan"),
    ("han_yu_essays", "Hán Yù Wénjí 韓愈文集", "Han Yu's Collected Prose (Daotong)", "lzh", 820, ["literature", "neoconfucian_proto"], "han_yu"),
    ("li_ao_fuxing_shu", "Fùxìng Shū 復性書", "Book of Returning to the Nature", "lzh", 800, ["literature", "neoconfucian_proto"], "li_ao"),
    ("ouyang_xiu_xin_tangshu", "Xīn Tángshū 新唐書", "New History of Tang", "lzh", 1060, ["history"], "ouyang_xiu_song_qi"),
    ("ouyang_xiu_xin_wudai_shi", "Xīn Wǔdài Shǐ 新五代史", "New History of Five Dynasties", "lzh", 1073, ["history"], "ouyang_xiu"),
]

assert len(WORKS) == 70, f"CHINESE×medieval doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "tiantai" in tags:
        return "BUDDHISM_TIANTAI"
    if "huayan" in tags:
        return "BUDDHISM_HUAYAN"
    if "yogacara" in tags:
        return "BUDDHISM_FAXIANG"
    if "chan" in tags:
        return "BUDDHISM_CHAN"
    if "pureland" in tags:
        return "BUDDHISM_PURELAND_CHINESE"
    if "buddhist" in tags:
        return "BUDDHISM_CHINESE"
    if "daoism" in tags:
        return "DAOISM_MEDIEVAL"
    if "neoconfucian" in tags:
        if "xinxue" in tags:
            return "NEOCONFUCIAN_XINXUE"
        return "NEOCONFUCIAN_LIXUE"
    if "history" in tags or "encyclopedia" in tags:
        return "CHINESE_HISTORIOGRAPHY"
    if "medicine" in tags or "pharmacy" in tags:
        return "CHINESE_MEDICINE"
    if "law" in tags:
        return "CHINESE_LAW"
    if "aesthetics" in tags or "literature" in tags:
        return "CHINESE_LITERATURE"
    if "heterodox" in tags:
        return "CHINESE_HETERODOX"
    return "CHINESE_MEDIEVAL"


def main() -> int:
    catalog = []
    for wid, title_zh, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title_zh,
            "title_en": title_en,
            "macro_culture": "CHINESE",
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
        "version": "v206h_chinese_medieval",
        "generated": "2026-04-29",
        "macro_culture": "CHINESE",
        "epoch": "medieval",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["ctext.org", "CBETA Online", "sacred-texts", "archive.org"],
        "language_original_dominant": "lzh (Literary Chinese)",
        "schools_covered": [
            "Tiantai (Zhiyi)",
            "Huayan (Fazang, Chengguan)",
            "Faxiang/Yogācāra chinois (Xuanzang, Kuiji)",
            "Chan (Huineng, Sengcan, Linji, Dongshan, Wumen, Yuanwu, Dahui, Hongzhi)",
            "Pure Land chinois (Tanluan, Daochuo, Shandao)",
            "Zongmi (synthèse Chan-Huayan)",
            "Daoisme Tang-Song (Sima Chengzhen, Zhang Boduan, Yunji Qiqian)",
            "Néo-confucianisme Song (Zhou Dunyi, Shao Yong, Zhang Zai, Cheng frères, Zhu Xi corpus, Lu Jiuyuan, Chen Liang, Ye Shi)",
            "Néo-confucianisme Ming (Wang Yangming, Luo Qinshun, Wang Ji, Li Zhi)",
            "Histoire/encyclopédies (Tongdian, Zizhi Tongjian, Yongle Dadian, Tongzhi)",
            "Médecine (Sun Simiao, Wang Tao, Li Dongyuan)",
            "Aesthetics/Tang lit (Han Yu, Liu Zongyuan, Yan Yu)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue CHINESE × medieval : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

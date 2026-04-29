#!/usr/bin/env python3
"""
§206f — Catalogue CHINESE × late_antique (-200 → 500 CE), 70 œuvres.

Strates :
- Han Confucianism : Lu Jia, Jia Yi, Dong Zhongshu, Liu Xiang, Yang Xiong,
  Wang Chong (CRITICAL — déjà nœud du graphe), Huan Tan
- Han Daoism / proto-religious : Huangdi Neijing, Taipingjing, Laozi
  Xiang'er Zhu, Cantong Qi (Wei Boyang), Zhang Lu Tianshi corpus
- Han historiographie : Shǐjì (Sima Qian), Hànshū (Ban Gu), Hòu Hànshū,
  Sānguózhì
- Han classics commentary : Mao Heng, Zheng Xuan, He Xiu, Du Yu
- Six Dynasties Xuanxue : He Yan, Wang Bi, Guo Xiang, Pei Wei, Xi Kang,
  Ruan Ji
- Bouddhisme chinois (canal) : An Shigao trad., Dharmarakṣa trad.,
  Kumārajīva trad., Sengzhao Zhào Lùn, Dao'an, Huiyuan, Daosheng
- Pensée militaire/political tardive : Zhuge Liang, Cao Cao
- Astronomie/maths : Jiǔzhāng Suànshù, Zhōubì Suànjīng, Hǎidǎo Suànjīng,
  Sūnzǐ Suànjīng
- Médecine : Huángdì Nèijīng (Sùwèn + Língshū), Shénnóng Běncǎo Jīng,
  Shānghán Lùn (Zhang Zhongjing), Jīnguì Yàolüè
- Lexicographie : Shuōwén Jiězì (Xu Shen), Fāngyán (Yang Xiong), Shìmíng

Sources : ctext.org, sacred-texts SBE 39/40 (Legge), CBETA, archive.org.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_chinese_late_antique_v206f.json"

WORKS = [
    # ── Han Confucianism / political-philosophical
    ("xinyu_lujia", "Xīn Yǔ 新語", "New Discourses", "lzh", -195, ["confucian", "han"], "lu_jia"),
    ("xinshu_jiayi", "Xīn Shū 新書", "New Writings", "lzh", -170, ["confucian", "han"], "jia_yi"),
    ("chunqiu_fanlu_la", "Chūnqiū Fánlù 春秋繁露 (post-Dong commentary)", "Later Han additions to Luxuriant Dew", "lzh", -50, ["confucian", "han"], "dong_zhongshu_school"),
    ("shuoyuan", "Shuōyuàn 說苑", "Garden of Persuasions", "lzh", -20, ["confucian", "han"], "liu_xiang"),
    ("xinxu", "Xīnxù 新序", "New Prefaces", "lzh", -20, ["confucian", "han"], "liu_xiang"),
    ("liexian_zhuan", "Lièxiān Zhuàn 列仙傳", "Biographies of Immortals", "lzh", 0, ["daoism", "hagiography"], "liu_xiang_attr"),
    ("lienü_zhuan", "Liènǚ Zhuàn 列女傳", "Biographies of Exemplary Women", "lzh", -20, ["confucian"], "liu_xiang"),
    ("fayan", "Fǎ Yán 法言", "Exemplary Sayings", "lzh", 5, ["confucian", "han"], "yang_xiong"),
    ("taixuan_jing", "Tài Xuán Jīng 太玄經", "Canon of Supreme Mystery", "lzh", 0, ["confucian", "yinyang"], "yang_xiong"),
    ("fangyan", "Fāngyán 方言", "Dialects", "lzh", 10, ["lexicography"], "yang_xiong"),
    ("lunheng_full", "Lùnhéng (full) 論衡", "Balanced Discourses (full corpus)", "lzh", 80, ["skeptic", "han"], "wang_chong"),
    ("xinlun_huantan", "Xīn Lùn 新論", "New Discussions", "lzh", 30, ["skeptic", "han"], "huan_tan"),
    ("qianfu_lun", "Qiánfū Lùn 潛夫論", "Comments of a Recluse", "lzh", 150, ["confucian"], "wang_fu"),
    ("changyan", "Chāng Yán 昌言", "Bold Words", "lzh", 200, ["skeptic"], "zhongchang_tong"),
    ("zhonglun_xugan", "Zhōng Lùn 中論", "Treatise on the Mean", "lzh", 215, ["confucian"], "xu_gan"),

    # ── Han historiographie
    ("shiji", "Shǐjì 史記", "Records of the Grand Historian", "lzh", -91, ["history"], "sima_qian"),
    ("hanshu", "Hànshū 漢書", "Book of Han", "lzh", 100, ["history"], "ban_gu"),
    ("hou_hanshu", "Hòu Hànshū 後漢書", "Book of Later Han", "lzh", 445, ["history"], "fan_ye"),
    ("sanguozhi", "Sānguózhì 三國志", "Records of the Three Kingdoms", "lzh", 285, ["history"], "chen_shou"),
    ("zhushu_jinian", "Zhúshū Jìnián 竹書紀年", "Bamboo Annals", "lzh", -300, ["history"], None),

    # ── Classical commentaries
    ("maoshi_zhuan", "Máo Shī Zhuàn 毛詩傳", "Mao Tradition of the Odes", "lzh", -100, ["confucian", "classics_comm"], "mao_heng"),
    ("zhengxuan_sanli", "Zhèng Xuán Sānlǐ Zhù 鄭玄三禮注", "Zheng Xuan's Three Rites Commentary", "lzh", 180, ["confucian", "classics_comm"], "zheng_xuan"),
    ("hexiu_gongyang", "Hé Xiū Gōngyáng Zhuàn Jiěgǔ 何休公羊解詁", "He Xiu's Gongyang Commentary", "lzh", 180, ["confucian", "classics_comm"], "he_xiu"),
    ("duyu_zuozhuan", "Dù Yù Zuǒ Zhuàn Jí Jiě 杜預左傳集解", "Du Yu's Zuo Zhuan Commentary", "lzh", 280, ["confucian", "classics_comm"], "du_yu"),

    # ── Xuanxue (mystery learning) — Six Dynasties
    ("wangbi_laozi", "Wáng Bì Lǎozǐ Zhù 王弼老子注", "Wang Bi's Daodejing Commentary", "lzh", 245, ["xuanxue", "daoism"], "wang_bi"),
    ("wangbi_yijing", "Wáng Bì Zhōu Yì Zhù 王弼周易注", "Wang Bi's Yijing Commentary", "lzh", 245, ["xuanxue", "yijing"], "wang_bi"),
    ("heyan_lunyu", "Hé Yàn Lúnyǔ Jíjiě 何晏論語集解", "He Yan's Analects Compendium", "lzh", 240, ["xuanxue", "confucian"], "he_yan"),
    ("guoxiang_zhuangzi", "Guō Xiàng Zhuāngzǐ Zhù 郭象莊子注", "Guo Xiang's Zhuangzi Commentary", "lzh", 300, ["xuanxue", "daoism"], "guo_xiang"),
    ("xikang_yangsheng", "Xī Kāng Yǎngshēng Lùn 嵇康養生論", "Xi Kang on Nourishing Life", "lzh", 260, ["xuanxue", "daoism"], "xi_kang"),
    ("ruanji_dazhuanlun", "Ruǎn Jí Dà Rén Xiānshēng Zhuàn 阮籍大人先生傳", "Biography of Master Great Man", "lzh", 250, ["xuanxue"], "ruan_ji"),
    ("baopuzi_neipian", "Bàopǔzǐ Nèipiān 抱朴子內篇", "Master Embracing Simplicity (Inner)", "lzh", 320, ["daoism", "alchemy"], "ge_hong"),
    ("baopuzi_waipian", "Bàopǔzǐ Wàipiān 抱朴子外篇", "Master Embracing Simplicity (Outer)", "lzh", 320, ["confucian", "social"], "ge_hong"),
    ("shenxian_zhuan", "Shénxiān Zhuàn 神仙傳", "Biographies of Divine Immortals", "lzh", 320, ["daoism", "hagiography"], "ge_hong"),

    # ── Daoist religious texts (early)
    ("taiping_jing", "Tàipíng Jīng 太平經", "Scripture of Great Peace", "lzh", 150, ["daoism", "religious"], None),
    ("xianger_zhu", "Lǎozǐ Xiǎng'ěr Zhù 老子想爾注", "Xiang'er Commentary on Laozi", "lzh", 200, ["daoism", "religious"], "zhang_lu"),
    ("cantong_qi", "Zhōuyì Cāntóng Qì 周易參同契", "Kinship of Three", "lzh", 142, ["daoism", "alchemy", "yijing"], "wei_boyang"),
    ("huangting_jing", "Huángtíng Jīng 黃庭經", "Yellow Court Scripture", "lzh", 300, ["daoism", "religious"], None),
    ("dadao_jia_lingjie", "Dàdào Jiā Lìngjiè 大道家令誡", "Commands and Admonitions", "lzh", 255, ["daoism", "religious"], None),

    # ── Buddhist Chinese (channel late_antique)
    ("an_shigao_anban", "Ānbān Shǒuyì Jīng 安般守意經", "Sutra on Mindfulness of Breathing (trans. An Shigao)", "lzh", 150, ["buddhist", "translation"], "an_shigao"),
    ("zhi_qian_corpus", "Zhī Qiān Translation Corpus 支謙譯經", "Translations of Zhi Qian", "lzh", 240, ["buddhist", "translation"], "zhi_qian"),
    ("dharmaraksa_corpus", "Dharmarakṣa Corpus 竺法護譯經", "Translations of Dharmarakṣa", "lzh", 290, ["buddhist", "translation"], "dharmaraksa"),
    ("kumarajiva_corpus", "Kumārajīva Translation Corpus 鳩摩羅什譯經", "Translations of Kumārajīva", "lzh", 410, ["buddhist", "translation"], "kumarajiva"),
    ("zhao_lun", "Zhào Lùn 肇論", "Treatises of Sengzhao", "lzh", 410, ["buddhist", "madhyamaka"], "sengzhao"),
    ("dao_an_zongli", "Dào'ān Zōnglǐ Zhòngjīng Mùlù 道安綜理眾經目錄", "Dao'an's Catalog of Sutras", "lzh", 374, ["buddhist", "catalog"], "dao_an"),
    ("huiyuan_shamen", "Huìyuǎn Shāmén Bù Jìng Wángzhě Lùn 慧遠沙門不敬王者論", "On Monks Not Bowing to Kings", "lzh", 404, ["buddhist", "ethics"], "huiyuan"),
    ("daosheng_fragments", "Dàoshēng Fragments 道生遺教", "Fragments of Daosheng", "lzh", 430, ["buddhist", "lotus"], "daosheng"),
    ("mouzi_lihuolun", "Móuzǐ Lǐhuò Lùn 牟子理惑論", "Mouzi's Resolution of Doubts", "lzh", 200, ["buddhist", "apologetics"], "mouzi"),
    ("gaoseng_zhuan", "Gāosēng Zhuàn 高僧傳", "Biographies of Eminent Monks", "lzh", 519, ["buddhist", "hagiography"], "huijiao"),

    # ── Math / astronomy
    ("jiuzhang_suanshu_la", "Jiǔzhāng Suànshù 九章算術 (Liu Hui ed.)", "Nine Chapters with Liu Hui's Commentary", "lzh", 263, ["math"], "liu_hui"),
    ("zhoubi_suanjing_la", "Zhōubì Suànjīng 周髀算經 (Zhao Shuang ed.)", "Zhou Gnomon with Zhao Shuang's Notes", "lzh", 250, ["math", "astronomy"], "zhao_shuang"),
    ("haidao_suanjing", "Hǎidǎo Suànjīng 海島算經", "Sea Island Mathematical Classic", "lzh", 263, ["math"], "liu_hui"),
    ("sunzi_suanjing", "Sūnzǐ Suànjīng 孫子算經", "Sunzi's Mathematical Classic", "lzh", 400, ["math"], None),
    ("zhang_heng_lingxian", "Líng Xiàn 靈憲", "Spiritual Constitution of the Universe", "lzh", 120, ["astronomy"], "zhang_heng"),

    # ── Medicine
    ("huangdi_neijing_suwen_la", "Huángdì Nèijīng Sùwèn 黃帝內經素問 (Wang Bing ed.)", "Plain Questions, Wang Bing's recension", "lzh", 762, ["medicine"], "wang_bing"),
    ("huangdi_neijing_lingshu_la", "Huángdì Nèijīng Língshū 黃帝內經靈樞 (Tang ed.)", "Spiritual Pivot, Tang recension", "lzh", 762, ["medicine", "acupuncture"], None),
    ("shennong_bencao_full", "Shénnóng Běncǎo Jīng 神農本草經", "Divine Husbandman's Materia Medica", "lzh", 0, ["medicine", "pharmacology"], None),
    ("shanghan_lun", "Shānghán Lùn 傷寒論", "Treatise on Cold Damage", "lzh", 220, ["medicine"], "zhang_zhongjing"),
    ("jingui_yaolue", "Jīnguì Yàolüè 金匱要略", "Essential Prescriptions of the Golden Cabinet", "lzh", 220, ["medicine"], "zhang_zhongjing"),
    ("nanjing_classic", "Nán Jīng 難經", "Classic of Difficult Issues", "lzh", 100, ["medicine"], None),
    ("zhouhou_beijifang", "Zhǒuhòu Bèijí Fāng 肘後備急方", "Handy Therapy for Emergencies", "lzh", 320, ["medicine"], "ge_hong"),

    # ── Lexicography & encyclopedia
    ("shuowen_jiezi", "Shuōwén Jiězì 說文解字", "Explanation of Characters", "lzh", 100, ["lexicography"], "xu_shen"),
    ("shiming", "Shìmíng 釋名", "Explanations of Names", "lzh", 200, ["lexicography"], "liu_xi"),
    ("guangya", "Guǎngyǎ 廣雅", "Expanded Erya", "lzh", 230, ["lexicography"], "zhang_yi"),

    # ── Military / strategic Han-Three Kingdoms
    ("zhugeliang_chushi", "Chū Shī Biǎo 出師表", "Memorial on Sending Out the Army", "lzh", 227, ["military", "political"], "zhuge_liang"),
    ("caocao_sunzi_zhu", "Cáo Cāo Sūnzǐ Zhù 曹操孫子注", "Cao Cao's Commentary on Sunzi", "lzh", 200, ["military"], "cao_cao"),

    # ── Filler late_antique (poésie, divers)
    ("wenxin_diaolong", "Wénxīn Diāolóng 文心雕龍", "Literary Mind & Carving of Dragons", "lzh", 501, ["aesthetics", "literature"], "liu_xie"),
    ("shipin_zhongrong", "Shī Pǐn 詩品", "Grades of the Poets", "lzh", 513, ["aesthetics", "literature"], "zhong_rong"),
    ("yutai_xinyong", "Yùtái Xīnyǒng 玉臺新詠", "New Songs from Jade Terrace", "lzh", 545, ["literature"], "xu_ling"),
    ("wenxuan", "Wénxuǎn 文選", "Selections of Refined Literature", "lzh", 530, ["literature", "anthology"], "xiao_tong"),
    ("yanshi_jiaxun", "Yán Shì Jiāxùn 顏氏家訓", "Family Instructions of Master Yan", "lzh", 590, ["confucian", "social"], "yan_zhitui"),
]

assert len(WORKS) == 70, f"CHINESE×late_antique doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "buddhist" in tags:
        return "BUDDHISM_CHINESE"
    if "xuanxue" in tags:
        return "CHINESE_XUANXUE"
    if "daoism" in tags:
        return "DAOISM"
    if "history" in tags:
        return "CHINESE_HISTORIOGRAPHY"
    if "medicine" in tags or "acupuncture" in tags or "pharmacology" in tags:
        return "CHINESE_MEDICINE"
    if "math" in tags or "astronomy" in tags:
        return "CHINESE_SCIENCE"
    if "lexicography" in tags:
        return "CHINESE_PHILOLOGY"
    if "military" in tags:
        return "CHINESE_MILITARY"
    if "skeptic" in tags:
        return "CHINESE_SKEPTIC"
    if "yinyang" in tags:
        return "CHINESE_YINYANG"
    if "classics_comm" in tags:
        return "CHINESE_CLASSICS_COMM"
    if "confucian" in tags:
        return "CHINESE_CLASSICS"
    return "CHINESE_LATE_ANTIQUE"


def main() -> int:
    catalog = []
    for wid, title_zh, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title_zh,
            "title_en": title_en,
            "macro_culture": "CHINESE",
            "epoch": "late_antique",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 50,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": "james_legge" if "confucian" in tags or "daoism" in tags else None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206f_chinese_late_antique",
        "generated": "2026-04-29",
        "macro_culture": "CHINESE",
        "epoch": "late_antique",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["ctext.org", "sacred-texts SBE 39/40 (Legge)", "CBETA Online", "archive.org"],
        "language_original_dominant": "lzh (Literary Chinese)",
        "schools_covered": [
            "Han Confucianism (Lu Jia, Jia Yi, Dong Zhongshu, Liu Xiang, Yang Xiong, Wang Chong, Huan Tan)",
            "Han historiographie (Shǐjì, Hànshū, Hòu Hànshū, Sānguózhì)",
            "Han classics commentary (Mao, Zheng Xuan, He Xiu, Du Yu)",
            "Xuanxue (He Yan, Wang Bi, Guo Xiang, Xi Kang, Ruan Ji, Ge Hong)",
            "Daoism religieux (Taipingjing, Xiang'er, Cantong Qi)",
            "Bouddhisme chinois (canal — An Shigao, Kumārajīva, Sengzhao, Dao'an, Huiyuan, Mouzi)",
            "Math (Jiuzhang, Zhoubi, Liu Hui, Sunzi)",
            "Médecine (Huangdi Neijing complet, Shennong, Shanghan Lun, Jingui)",
            "Lexicographie (Shuowen, Shiming, Guangya)",
            "Militaire (Zhuge Liang, Cao Cao)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue CHINESE × late_antique : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

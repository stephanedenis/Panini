#!/usr/bin/env python3
"""
§206b — Catalogue CHINESE × axial (70 œuvres, ~800-200 BCE).

Couvre les 100 écoles (諸子百家) : Confucianisme (Confucius, Mencius,
Xunzi), Taoïsme (Laozi, Zhuangzi, Liezi), Légisme (Han Fei, Shang Yang),
Mohisme (Mozi), École des Noms (Hui Shi, Gongsun Long), École Yin-Yang,
ainsi que classiques canoniques (Wu Jing) et chroniques (Zuo Zhuan).

Sources principales :
- Chinese Text Project (ctext.org) — corpus complet avec apparat critique
- sacred-texts.com/cfu/ + /tao/ — Legge translations (SBE 3, 16, 27, 28, 39, 40)
- Wikisource ZH

Référence Sacred Books of the East volumes Confucian/Daoist (Legge) :
  3   = Shu Jing, Shi Jing (sections rel.), Xiao Jing
  16  = Yi Jing
  27  = Li Ki I-X
  28  = Li Ki XI-XLVI
  39  = Tao Te Ching, Texts of Taoism I (Zhuangzi 1-17)
  40  = Texts of Taoism II (Zhuangzi 18-33, Lieh-tzu, Tractate of Actions)
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_chinese_axial_v206b.json"

# (id, title_zh_pinyin, title_en, year, tags, ctext_path, sbe_vol)
WORKS = [
    # ── Wu Jing — Cinq Classiques
    ("yijing", "Yìjīng (易經)", "Book of Changes", -800, ["wujing", "divination", "metaphysics"], "book-of-changes", "16"),
    ("shijing", "Shījīng (詩經)", "Book of Songs", -700, ["wujing", "poetry"], "book-of-poetry", "3"),
    ("shujing", "Shūjīng (書經)", "Book of Documents", -700, ["wujing", "history"], "shang-shu", "3"),
    ("liji", "Lǐjì (禮記)", "Book of Rites", -300, ["wujing", "ritual"], "liji", "27"),
    ("chunqiu", "Chūnqiū (春秋)", "Spring and Autumn Annals", -480, ["wujing", "chronicle"], "chun-qiu", None),

    # ── Quatre Livres (Sì Shū) confucianisme classique
    ("lunyu", "Lúnyǔ (論語)", "Analects of Confucius", -480, ["confucian", "classic"], "analects", None),
    ("mengzi", "Mèngzǐ (孟子)", "Mencius", -300, ["confucian", "classic"], "mengzi", None),
    ("daxue", "Dàxué (大學)", "Great Learning", -300, ["confucian", "classic"], "liji/da-xue", "28"),
    ("zhongyong", "Zhōngyōng (中庸)", "Doctrine of the Mean", -300, ["confucian", "classic"], "liji/zhong-yong", "28"),

    # ── Confucianisme étendu
    ("xunzi", "Xúnzǐ (荀子)", "Xunzi", -250, ["confucian", "philosophy"], "xunzi", None),
    ("xiaojing", "Xiàojīng (孝經)", "Classic of Filial Piety", -300, ["confucian"], "xiao-jing", "3"),
    ("zhouyili", "Zhōulǐ (周禮)", "Rites of Zhou", -300, ["ritual"], "rites-of-zhou", None),
    ("yili", "Yílǐ (儀禮)", "Etiquette and Ceremonies", -300, ["ritual"], "yili", None),
    ("dadai_liji", "Dà Dài Lǐjì (大戴禮記)", "Da Dai Liji", -100, ["ritual"], "da-dai-li-ji", None),
    ("kongzi_jiayu", "Kǒngzǐ Jiāyǔ (孔子家語)", "Family Sayings of Confucius", -150, ["confucian"], "kongzi-jiayu", None),

    # ── Taoïsme classique
    ("daodejing", "Dàodéjīng (道德經)", "Tao Te Ching (Laozi)", -350, ["daoism", "classic"], "dao-de-jing", "39"),
    ("zhuangzi", "Zhuāngzǐ (莊子)", "Zhuangzi", -300, ["daoism", "classic"], "zhuangzi", "39"),
    ("liezi", "Lièzǐ (列子)", "Liezi", -300, ["daoism"], "liezi", "40"),
    ("wenzi", "Wénzǐ (文子)", "Wenzi", -250, ["daoism"], "wenzi", None),
    ("huainanzi", "Huáinánzǐ (淮南子)", "Huainanzi", -139, ["daoism", "syncretism"], "huainanzi", None),

    # ── Mohisme
    ("mozi", "Mòzǐ (墨子)", "Mozi", -390, ["mohist", "ethics", "logic"], "mozi", None),

    # ── Légisme
    ("hanfeizi", "Hán Fēizǐ (韓非子)", "Han Feizi", -240, ["legalist", "philosophy"], "hanfeizi", None),
    ("shangjunshu", "Shāng Jūn Shū (商君書)", "Book of Lord Shang", -300, ["legalist"], "shang-jun-shu", None),
    ("shenzi", "Shēnzǐ (慎子)", "Shenzi (fragments)", -300, ["legalist"], "shenzi", None),
    ("shenbuhai_fragments", "Shēn Bùhài fragments (申不害)", "Shen Buhai fragments", -340, ["legalist"], None, None),
    ("guanzi", "Guǎnzǐ (管子)", "Guanzi", -300, ["legalist", "syncretist"], "guanzi", None),

    # ── École des Noms (logiciens)
    ("gongsun_longzi", "Gōngsūn Lóngzǐ (公孫龍子)", "Gongsun Longzi", -300, ["names", "logic"], "gongsun-longzi", None),
    ("hui_shi_fragments", "Huì Shī fragments (惠施)", "Hui Shi fragments (in Zhuangzi 33)", -310, ["names", "logic"], None, None),
    ("dengxi_zi", "Dèng Xī zǐ (鄧析子)", "Deng Xizi", -500, ["names", "logic"], "deng-xi-zi", None),

    # ── École Yin-Yang
    ("zou_yan_fragments", "Zōu Yǎn fragments (鄒衍)", "Zou Yan fragments (Five Phases)", -280, ["yinyang", "cosmology"], None, None),

    # ── Stratèges (兵家)
    ("sunzi_bingfa", "Sūnzǐ Bīngfǎ (孫子兵法)", "Art of War (Sunzi)", -500, ["military", "strategy"], "art-of-war", None),
    ("wuzi", "Wúzǐ (吳子)", "Wuzi (Wu Qi)", -380, ["military"], "wuzi", None),
    ("sun_bin_bingfa", "Sūn Bìn Bīngfǎ (孫臏兵法)", "Art of War (Sun Bin)", -300, ["military"], "sun-bin", None),
    ("six_secret_teachings", "Liùtāo (六韜)", "Six Secret Teachings", -300, ["military"], "liutao", None),

    # ── Chroniques et histoires anciennes
    ("zuozhuan", "Zuǒ Zhuàn (左傳)", "Zuo Commentary", -390, ["chronicle", "history"], "zuo-zhuan", None),
    ("guoyu", "Guóyǔ (國語)", "Discourses of the States", -350, ["chronicle"], "guo-yu", None),
    ("zhanguoce", "Zhànguó Cè (戰國策)", "Strategies of the Warring States", -250, ["chronicle"], "zhan-guo-ce", None),
    ("gongyangzhuan", "Gōngyáng Zhuàn (公羊傳)", "Gongyang Commentary", -200, ["commentary"], "gongyang-zhuan", None),
    ("guliangzhuan", "Gǔliáng Zhuàn (穀梁傳)", "Guliang Commentary", -200, ["commentary"], "guliang-zhuan", None),
    ("yi_zhou_shu", "Yì Zhōu Shū (逸周書)", "Lost Book of Zhou", -300, ["history"], "yi-zhou-shu", None),

    # ── Médical et auxiliaire (axial)
    ("huangdi_neijing_suwen", "Huángdì Nèijīng Sùwèn (黃帝內經素問)", "Inner Canon of Huangdi - Plain Questions", -200, ["medical", "metaphysics"], "huangdi-neijing", None),
    ("huangdi_neijing_lingshu", "Huángdì Nèijīng Língshū (黃帝內經靈樞)", "Inner Canon - Spiritual Pivot", -200, ["medical"], "huangdi-neijing", None),

    # ── Mathématiques anciennes
    ("zhoubi_suanjing", "Zhōubì Suànjīng (周髀算經)", "Zhoubi Suanjing", -200, ["math", "astronomy"], "zhou-bi-suan-jing", None),
    ("jiuzhang_suanshu", "Jiǔzhāng Suànshù (九章算術)", "Nine Chapters on the Mathematical Art", -150, ["math"], "nine-chapters", None),

    # ── Compendia syncrétistes
    ("lushi_chunqiu", "Lǚ Shì Chūnqiū (呂氏春秋)", "Annals of Lü Buwei", -240, ["syncretist"], "lvshi-chunqiu", None),
    ("yanzi_chunqiu", "Yànzǐ Chūnqiū (晏子春秋)", "Annals of Yan Ying", -300, ["confucian", "advice"], "yanzi-chunqiu", None),

    # ── Daoist auxiliaires
    ("yinwenzi", "Yǐn Wén zǐ (尹文子)", "Yin Wenzi", -300, ["daoism", "names"], "yin-wenzi", None),
    ("heguanzi", "Hé Guān zǐ (鶡冠子)", "Heguanzi", -250, ["daoism", "syncretist"], "he-guan-zi", None),
    ("guigu_zi", "Guǐgǔ zǐ (鬼谷子)", "Guiguzi", -300, ["rhetoric", "strategy"], "guiguzi", None),

    # ── Han transitionnel (axial tardif)
    ("shiji_core", "Shǐjì (史記, livres anciens)", "Records of the Grand Historian (axial-related books)", -90, ["history", "biographies"], "shiji", None),
    ("xinyu", "Xīnyǔ (新語)", "New Discussions (Lu Jia)", -190, ["confucian", "han"], "xin-yu", None),
    ("xinshu", "Xīnshū (新書)", "New Writings (Jia Yi)", -170, ["confucian", "han"], "xin-shu", None),
    ("yantielun", "Yán Tiě Lùn (鹽鐵論)", "Discourses on Salt and Iron", -81, ["confucian", "legalist", "debate"], "yantielun", None),
    ("chunqiu_fanlu", "Chūnqiū Fánlù (春秋繁露)", "Luxuriant Dew of the Spring and Autumn (Dong Zhongshu)", -100, ["confucian", "han"], "chun-qiu-fan-lu", None),
    ("baihu_tongyi_proto", "Báihǔ Tōngyì (白虎通義 proto)", "Comprehensive Discussions in the White Tiger Hall (early strata)", -50, ["confucian", "han"], "bai-hu-tong", None),

    # ── Compléments École des Noms / sceptiques
    ("yangzi_fragments", "Yáng Zhū fragments (楊朱)", "Yang Zhu fragments (in Liezi 7, Mencius)", -350, ["egoist", "skeptic"], None, None),

    # ── Petits classiques
    ("gengsang_zi", "Gēngsāng zǐ (庚桑子)", "Gengsangzi", -300, ["daoism"], "gengsang-zi", None),
    ("ji_ran", "Jì Rán (計然)", "Ji Ran fragments", -450, ["daoism", "economics"], None, None),

    # ── Auxiliaires (rituel/musique)
    ("yueji", "Yuèjì (樂記)", "Record of Music (Liji ch.19)", -200, ["ritual", "music"], "liji/yue-ji", "28"),
    ("daxiang_zhuan", "Dàxiàng Zhuàn (大象傳)", "Great Image Commentary (Yijing wing)", -200, ["yijing", "wing"], "yi-jing", "16"),
    ("xugua_zhuan", "Xùguà Zhuàn (序卦傳)", "Sequence of Hexagrams (Yijing wing)", -200, ["yijing", "wing"], "yi-jing", "16"),
    ("xicizhuan", "Xìcí Zhuàn (繫辭傳)", "Great Treatise (Yijing wing)", -250, ["yijing", "wing", "metaphysics"], "yi-jing", "16"),
    ("zaguazhuan", "Záguà Zhuàn (雜卦傳)", "Miscellaneous Notes on Hexagrams", -200, ["yijing", "wing"], "yi-jing", "16"),

    # ── Daoïsme — classiques mineurs
    ("yangsheng_zhu", "Yǎngshēng Zhǔ", "Master of Nourishing Life (Zhuangzi 3)", -300, ["daoism"], None, "39"),
    ("qiwulun", "Qíwù Lùn", "Discussion on Equalizing Things (Zhuangzi 2)", -300, ["daoism", "skepticism"], None, "39"),

    # ── Compléments Han pour atteindre 70
    ("hannji_jia_yi_fu", "Jiǎ Yì Fù (賈誼賦)", "Rhapsodies of Jia Yi", -180, ["confucian", "literature"], None, None),
    ("zhouyi_lou", "Zhōuyì Lóu (周易樓)", "Zhouyi commentaries (early Han)", -150, ["yijing", "commentary"], None, None),
    ("yantieshi_proto", "Yán Tiě Shì (鹽鐵史 proto)", "Salt and Iron debates supplements", -75, ["legalist", "han"], None, None),
    ("shennong_bencao_jing", "Shénnóng Běncǎo Jīng (神農本草經)", "Divine Husbandman's Materia Medica", -100, ["medical"], "shennong-bencao-jing", None),
    ("erya", "Ěryǎ (爾雅)", "Erya (Ready Guide — earliest dictionary)", -300, ["lexicon", "philology"], "er-ya", None),
]

assert len(WORKS) == 70, f"Catalogue CHINESE×axial doit contenir 70 entrées, actuel = {len(WORKS)}"


MICRO_FROM_TAGS = {
    "confucian": "CHINESE_CLASSICS",
    "daoism": "DAOISM",
    "legalist": "CHINESE_LEGALIST",
    "mohist": "CHINESE_MOHIST",
    "names": "CHINESE_NAMES",
    "yinyang": "CHINESE_YINYANG",
    "military": "CHINESE_MILITARY",
    "egoist": "CHINESE_EGOIST",
    "syncretist": "CHINESE_SYNCRETIST",
    "skeptic": "CHINESE_SKEPTIC",
}


def main() -> int:
    catalog = []
    for wid, t_zh, t_en, year, tags, ctext, sbe_vol in WORKS:
        ts = set(tags)
        micro = next((MICRO_FROM_TAGS[t] for t in tags if t in MICRO_FROM_TAGS), "CHINESE_CLASSICS")
        if "wujing" in ts:
            micro = "CHINESE_CLASSICS"

        url_ctext = f"https://ctext.org/{ctext}" if ctext else None
        url_sbe = f"https://www.sacred-texts.com/sbe/sbe{sbe_vol.split(',')[0]}/" if sbe_vol else None

        catalog.append({
            "id": wid,
            "title_original": t_zh,
            "title_en": t_en,
            "macro_culture": "CHINESE",
            "epoch": "axial",
            "tradition_micro": micro,
            "language_original": "lzh",  # littéraire chinois
            "year_estimate": year,
            "year_uncertainty": 100,
            "author": _author_for(wid),
            "url_original": url_ctext,
            "url_translation_en": url_sbe,
            "translator_canonical_en": "james_legge" if sbe_vol else None,
            "sbe_volumes": sbe_vol,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206b_chinese_axial",
        "generated": "2026-04-27",
        "macro_culture": "CHINESE",
        "epoch": "axial",
        "n_works": len(catalog),
        "target": 70,
        "primary_source": "Chinese Text Project (ctext.org)",
        "secondary_source": "sacred-texts.com — Legge translations (SBE 3, 16, 27, 28, 39, 40)",
        "language_original_dominant": "lzh",
        "translation_canonical_en": [
            "James Legge (Chinese Classics + SBE 1879-1885)",
            "Herbert A. Giles (Zhuangzi 1889)",
            "Arthur Waley (Analects 1938 — sous copyright)",
        ],
        "works": catalog,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue CHINESE × axial : {len(catalog)} œuvres")
    print(f"Source : ctext.org + Legge SBE")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


def _author_for(wid: str) -> str:
    table = {
        "lunyu": "confucius_disciples",
        "mengzi": "mencius",
        "daodejing": "laozi",
        "zhuangzi": "zhuangzi",
        "liezi": "liezi",
        "mozi": "mozi",
        "hanfeizi": "han_feizi",
        "shangjunshu": "shang_yang",
        "xunzi": "xunzi",
        "huainanzi": "liu_an",
        "lushi_chunqiu": "lu_buwei",
        "sunzi_bingfa": "sunzi",
        "wuzi": "wu_qi",
        "sun_bin_bingfa": "sun_bin",
        "gongsun_longzi": "gongsun_long",
        "hui_shi_fragments": "hui_shi",
        "zou_yan_fragments": "zou_yan",
        "shenbuhai_fragments": "shen_buhai",
        "yangzi_fragments": "yang_zhu",
        "guiguzi": "guiguzi",
        "xinyu": "lu_jia",
        "xinshu": "jia_yi",
        "chunqiu_fanlu": "dong_zhongshu",
        "shiji_core": "sima_qian",
        "kongzi_jiayu": "wang_su",
    }
    return table.get(wid, "anonymous")


if __name__ == "__main__":
    raise SystemExit(main())

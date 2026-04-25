#!/usr/bin/env python3
"""
§100 — Extension corpus ciblée sur les lacunes §99 + réentraînement
====================================================================
Plan §99 : 30 erreurs résiduelles dont
  - 9 sur définition cross-famille (ar/ja/hi/ru/zh sans copule IE)
  - 5 description→narration (verbes d'action)
  - 9/30 erreurs concentrées en arabe (sur 7.7 % du corpus)
  - 7/30 ambiguïtés intrinsèques irréductibles

Stratégie §100 :
  1. **Étendre corpus** ciblant les lacunes :
     - +6 défin × {ar, ja, hi, ru, zh} avec marqueurs copulaires natifs
     - +5 description factuelle × {fr, en, ru, hi, ar} (état, pas action)
     - +3 par type ar (description/proclamation/question/ordre/narration/introspection)
       pour réduire la concentration d'erreurs
     Total nouveau : ~73 phrases → 983 phrases
  2. **Features natives** : 5 nouveaux marqueurs définitoires
     - ar : هو / هي (copule pronominale en phrase nominale)
     - ja : とは…である / である
     - hi : होता है (postposé)
     - ru : является / — (tiret prédicatif) / это
     - zh : 是 / 即 / 称为 / 指
     → dim totale : 384 (emb) + 4 (syn §97) + 5 (def natifs §100) + 11 (lang) = 404
  3. **Réentraîner** logreg et comparer :
     [A] CV 5-fold sur 983 phrases vs §98 96.7 %
     [B] Hold-out cross-fam: train sur 7 langues §94, test sur 4 nouvelles vs §98 76.4 %
     [C] Per-langue/per-type breakdown pour vérifier fermeture lacune définition

Output → research/nipada/falsification/nipada_v100_retrain_report.json
"""

from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

warnings.filterwarnings("ignore", category=FutureWarning)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import importlib.util  # noqa: E402

# Charger §98
_spec = importlib.util.spec_from_file_location(
    "v98", REPO_ROOT / "scripts" / "nipada_crosslingual_v98.py"
)
_v98 = importlib.util.module_from_spec(_spec)
_v98.__name__ = "v98"
_spec.loader.exec_module(_v98)  # type: ignore[attr-defined]

merge_corpus_98 = _v98.merge_corpus
TYPES = _v98.TYPES
TYPE2IDX = _v98.TYPE2IDX
IDX2TYPE = _v98.IDX2TYPE
ALL_LANGS = _v98.ALL_LANGS  # 11 langues
LANG2IDX = _v98.LANG2IDX
syntactic_features_v98 = _v98.syntactic_features
lang_onehot = _v98.lang_onehot
LANGS_94 = _v98.LANGS_94
NEW_LANGS = _v98.NEW_LANGS
_NpEncoder = _v98._NpEncoder
_to_native = _v98._to_native

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v100_retrain_report.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


# ── Corpus §100 — extensions ciblées ─────────────────────────────────────────
# A. Définitions natives (copule explicite dans la langue cible)
DEFINITIONS_100: dict[str, list[str]] = {
    "ar": [
        "العدد الأولي هو عدد طبيعي أكبر من واحد لا يقبل القسمة إلا على نفسه وعلى الواحد.",
        "الجبر هو فرع من الرياضيات يدرس البنى المجردة والعلاقات بينها.",
        "الديمقراطية هي نظام سياسي تكون فيه السيادة للشعب.",
        "الذاكرة هي القدرة العقلية على تخزين المعلومات واسترجاعها.",
        "العدالة هي إعطاء كل ذي حق حقه دون تمييز.",
        "القانون هو مجموعة قواعد ملزمة تنظم سلوك الأفراد في المجتمع.",
    ],
    "ja": [
        "素数とは、一より大きい自然数で、一と自分自身以外に約数を持たないものである。",
        "代数学とは、抽象的構造とその関係を研究する数学の一分野である。",
        "民主主義とは、主権が国民に属する政治体制のことである。",
        "記憶とは、情報を保存し再生する精神的能力のことである。",
        "正義とは、各人にその当然の権利を差別なく与えることである。",
        "法とは、社会における個人の行動を規律する強制的な規則の総体である。",
    ],
    "hi": [
        "अभाज्य संख्या वह प्राकृत संख्या होती है जो एक से बड़ी हो और केवल एक तथा स्वयं से विभाज्य हो।",
        "बीजगणित गणित की वह शाखा है जो अमूर्त संरचनाओं और उनके संबंधों का अध्ययन करती है।",
        "लोकतंत्र वह राजनीतिक व्यवस्था है जिसमें संप्रभुता जनता में निहित होती है।",
        "स्मृति वह मानसिक क्षमता है जिससे सूचनाएँ संचित और पुनः प्राप्त की जाती हैं।",
        "न्याय वह सिद्धांत है जो प्रत्येक व्यक्ति को बिना भेदभाव के उसका अधिकार देता है।",
        "क़ानून समाज में व्यक्तियों के आचरण को विनियमित करने वाले बाध्यकारी नियमों का समूह होता है।",
    ],
    "ru": [
        "Простое число — это натуральное число, большее единицы, делящееся только на единицу и само на себя.",
        "Алгебра — это раздел математики, изучающий абстрактные структуры и отношения между ними.",
        "Демократия — это политическая система, в которой суверенитет принадлежит народу.",
        "Память — это умственная способность сохранять и извлекать информацию.",
        "Справедливость — это принцип воздаяния каждому по его праву без различия.",
        "Закон — это совокупность обязательных норм, регулирующих поведение людей в обществе.",
    ],
    "zh": [
        "素数是指大于一且只能被一和自身整除的自然数。",
        "代数是研究抽象结构及其相互关系的数学分支。",
        "民主是指主权属于人民的政治制度。",
        "记忆是指存储和提取信息的心理能力。",
        "正义即给予每个人其应得权利而不加区别的原则。",
        "法律是规范社会成员行为的强制性规则的总和。",
    ],
}

# B. Descriptions factuelles non-narratives (état d'affaires, pas séquence d'actions)
DESCRIPTIONS_100: dict[str, list[str]] = {
    "fr": [
        "Le mont Everest culmine à huit mille huit cent quarante-huit mètres au-dessus du niveau de la mer.",
        "L'atmosphère terrestre est composée principalement d'azote et d'oxygène.",
        "Le génome humain comporte environ trois milliards de paires de bases.",
        "La capitale de l'Australie est Canberra, située dans le Territoire de la capitale.",
        "Une année lumière équivaut à environ neuf mille milliards de kilomètres.",
    ],
    "en": [
        "Mount Everest stands at eight thousand eight hundred and forty-eight metres above sea level.",
        "Earth's atmosphere is composed primarily of nitrogen and oxygen.",
        "The human genome contains roughly three billion base pairs.",
        "The capital of Australia is Canberra, located in the Capital Territory.",
        "One light-year equals approximately nine trillion kilometres.",
    ],
    "ru": [
        "Гора Эверест возвышается на восемь тысяч восемьсот сорок восемь метров над уровнем моря.",
        "Атмосфера Земли состоит главным образом из азота и кислорода.",
        "Геном человека содержит около трёх миллиардов пар оснований.",
        "Столицей Австралии является Канберра, расположенная на Столичной территории.",
        "Один световой год равен примерно девяти триллионам километров.",
    ],
    "hi": [
        "माउंट एवरेस्ट समुद्र तल से आठ हज़ार आठ सौ अड़तालीस मीटर ऊँचा है।",
        "पृथ्वी का वायुमंडल मुख्यतः नाइट्रोजन और ऑक्सीजन से बना है।",
        "मानव जीनोम में लगभग तीन अरब क्षार-युग्म होते हैं।",
        "ऑस्ट्रेलिया की राजधानी कैनबरा है, जो राजधानी क्षेत्र में स्थित है।",
        "एक प्रकाश वर्ष लगभग नौ खरब किलोमीटर के बराबर होता है।",
    ],
    "ar": [
        "يبلغ ارتفاع جبل إيفرست ثمانية آلاف وثمانمائة وثمانية وأربعين متراً فوق سطح البحر.",
        "يتكون الغلاف الجوي للأرض أساساً من النيتروجين والأكسجين.",
        "يحتوي الجينوم البشري على حوالي ثلاثة مليارات زوج من القواعد.",
        "عاصمة أستراليا هي كانبيرا الواقعة في إقليم العاصمة.",
        "تعادل السنة الضوئية حوالي تسعة تريليونات كيلومتر.",
    ],
}

# C. Diversification arabe (3 nouvelles phrases par autre type)
ARABIC_100: dict[str, list[str]] = {
    "proclamation": [
        "لكل إنسان الحق في حرية الفكر والوجدان والدين دون تمييز.",
        "لا يجوز إخضاع أحد للتعذيب ولا للمعاملة القاسية أو المهينة.",
        "تضمن الدولة المساواة بين المواطنين أمام القانون.",
    ],
    "question": [
        "هل يمكن الجمع بين الحرية الفردية والعدالة الجماعية؟",
        "ماذا يحدث للوقت داخل الثقب الأسود؟",
        "كيف نشأت الحياة على كوكب الأرض؟",
    ],
    "ordre": [
        "ضع حزام الأمان قبل تشغيل المحرك.",
        "احفظ كلمة المرور في مكان آمن ولا تشاركها مع أحد.",
        "ادفع الفاتورة قبل نهاية الشهر لتجنب الغرامات.",
    ],
    "narration": [
        "في صباح ذلك اليوم، خرج التاجر من بيته متجهاً إلى السوق حاملاً بضاعته.",
        "غامر الأمير بحياته لإنقاذ مملكته من الغزاة، فعاد منتصراً بعد سنوات.",
        "وُلد ابن سينا في بخارى ثم انتقل إلى أصفهان حيث ألّف معظم مؤلفاته.",
    ],
    "introspection": [
        "أشعر أحياناً بأنني غريب حتى عن نفسي، وكأن أفكاري ليست لي.",
        "أتساءل في أعماقي إن كنت قد اخترت طريقي حقاً أم أن الظروف اختارته لي.",
        "يلازمني شعور بالذنب كلما تذكرت ما لم أقله في الوقت المناسب.",
    ],
}


# ── Détecteurs de copule définitoire native (§100) ───────────────────────────
# AR : pronom-copule هو/هي précédé d'un nom défini (article ال) en début/clause
_DEF_NATIVE_AR = re.compile(r"\bال\S+\s+(هو|هي)\s+")
# JA : « とは … である » ou simple « である » à la fin
_DEF_NATIVE_JA = re.compile(r"とは|である(?:[。.]?$)")
# HI : « होता है » / « होती है » (postposé, marqueur définitionnel typique)
_DEF_NATIVE_HI = re.compile(r"होता\s*है|होती\s*है|होते\s*हैं")
# RU : tiret prédicatif « X — это Y » ou « является »
_DEF_NATIVE_RU = re.compile(r"\s—\s+это\s+|являет(ся|ся)|\bесть\b")
# ZH : « 是…的 » classique, « 即 » formel, « 称为 » / « 指 »
_DEF_NATIVE_ZH = re.compile(r"是.+的|即.|称为|是指|指的是")


def has_native_def(text: str, lang: str) -> bool:
    if lang == "ar":
        return bool(_DEF_NATIVE_AR.search(text))
    if lang == "ja":
        return bool(_DEF_NATIVE_JA.search(text))
    if lang == "hi":
        return bool(_DEF_NATIVE_HI.search(text))
    if lang == "ru":
        return bool(_DEF_NATIVE_RU.search(text))
    if lang == "zh":
        return bool(_DEF_NATIVE_ZH.search(text))
    return False


def native_def_features(text: str, lang: str) -> np.ndarray:
    """5-dim one-hot : (ar, ja, hi, ru, zh) si copule native définitoire détectée."""
    v = np.zeros(5, dtype=np.float32)
    if not has_native_def(text, lang):
        return v
    idx = {"ar": 0, "ja": 1, "hi": 2, "ru": 3, "zh": 4}.get(lang)
    if idx is not None:
        v[idx] = 1.0
    return v


def syntactic_features_v100(text: str, lang: str) -> np.ndarray:
    """4 (syntactic §97) + 5 (native def §100) = 9 dim."""
    base = syntactic_features_v98(text, lang)
    nat = native_def_features(text, lang)
    return np.concatenate([base, nat])


def merge_corpus_v100() -> dict[str, dict[str, list[str]]]:
    base = merge_corpus_98()
    merged: dict[str, dict[str, list[str]]] = {t: {la: list(ph) for la, ph in by_lang.items()}
                                                 for t, by_lang in base.items()}
    # A. Définitions
    for la, phrases in DEFINITIONS_100.items():
        merged["définition"][la].extend(phrases)
    # B. Descriptions factuelles
    for la, phrases in DESCRIPTIONS_100.items():
        merged["description"][la].extend(phrases)
    # C. Diversification arabe
    for t, phrases in ARABIC_100.items():
        merged[t]["ar"].extend(phrases)
    return merged


def build_dataset_v100(model: SentenceTransformer, corpus: dict):
    texts: list[str] = []
    langs: list[str] = []
    y: list[int] = []
    for t, by_lang in corpus.items():
        for la, phrases in by_lang.items():
            for p in phrases:
                texts.append(p)
                langs.append(la)
                y.append(TYPE2IDX[t])
    print(f"  Encoding {len(texts)} phrases…", flush=True)
    X = np.asarray(model.encode(texts, batch_size=64, show_progress_bar=False, normalize_embeddings=True))
    feats_syn = np.stack([syntactic_features_v100(t, la) for t, la in zip(texts, langs)])
    feats_lang = np.stack([lang_onehot(la) for la in langs])
    y_arr = np.asarray(y, dtype=np.int64)
    strata = np.asarray([y[i] * len(ALL_LANGS) + LANG2IDX[langs[i]] for i in range(len(y))])
    return X, feats_syn, feats_lang, y_arr, np.asarray(langs), strata, texts


def cv_score(Xc, y, strata, n_splits=5, seed=42):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    accs, per_type, per_lang_dummy = [], {t: [] for t in TYPES}, None
    for tr, te in skf.split(Xc, strata):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(Xc[tr], y[tr])
        pred = clf.predict(Xc[te])
        accs.append(float((pred == y[te]).mean()))
        for ti, t in enumerate(TYPES):
            mask = y[te] == ti
            if mask.sum() > 0:
                per_type[t].append(float((pred[mask] == y[te][mask]).mean()))
    return float(np.mean(accs)), float(np.std(accs)), {t: float(np.mean(v)) for t, v in per_type.items()}


def per_lang_acc(Xc, y, langs, strata, n_splits=5, seed=42):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    correct = {la: 0 for la in ALL_LANGS}
    total = {la: 0 for la in ALL_LANGS}
    for tr, te in skf.split(Xc, strata):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(Xc[tr], y[tr])
        pred = clf.predict(Xc[te])
        for i, idx in enumerate(te):
            la = langs[idx]
            total[la] += 1
            if pred[i] == y[idx]:
                correct[la] += 1
    return {la: (correct[la] / total[la] if total[la] > 0 else None) for la in ALL_LANGS}


def holdout_train_94_test_new(Xc, y, langs):
    """Train on phrases from LANGS_94 only, test on NEW_LANGS."""
    train_mask = np.isin(langs, list(LANGS_94))
    test_mask = np.isin(langs, list(NEW_LANGS))
    clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf.fit(Xc[train_mask], y[train_mask])
    pred = clf.predict(Xc[test_mask])
    acc = float((pred == y[test_mask]).mean())
    # Per-type / per-lang
    per_type = {}
    per_lang = {}
    y_test = y[test_mask]
    langs_test = langs[test_mask]
    for ti, t in enumerate(TYPES):
        mask = y_test == ti
        if mask.sum() > 0:
            per_type[t] = float((pred[mask] == y_test[mask]).mean())
    for la in NEW_LANGS:
        mask = langs_test == la
        if mask.sum() > 0:
            per_lang[la] = float((pred[mask] == y_test[mask]).mean())
    return acc, per_type, per_lang, int(train_mask.sum()), int(test_mask.sum())


def main() -> None:
    W = 78
    print("═" * W)
    print("  §100 — Corpus étendu + features natives + réentraînement")
    print("═" * W)

    corpus = merge_corpus_v100()
    n_total = sum(len(p) for by_l in corpus.values() for p in by_l.values())
    print(f"\n  Corpus §100 : {n_total} phrases (vs §98 : 910)")

    # Détail nouveau corpus
    add_def = sum(len(v) for v in DEFINITIONS_100.values())
    add_desc = sum(len(v) for v in DESCRIPTIONS_100.values())
    add_ar = sum(len(v) for v in ARABIC_100.values())
    print(f"    +{add_def} définitions natives (ar/ja/hi/ru/zh)")
    print(f"    +{add_desc} descriptions factuelles (fr/en/ru/hi/ar)")
    print(f"    +{add_ar} arabe diversifié (autres types)")

    model = SentenceTransformer(MODEL_NAME)
    X, feats_syn, feats_lang, y, langs, strata, texts = build_dataset_v100(model, corpus)
    Xc = np.hstack([X, feats_syn, feats_lang])
    print(f"  Feature dim : {Xc.shape[1]} (384 emb + 9 syn+def_natifs + 11 lang)")

    # Compter les marqueurs natifs détectés
    nat_hits = {la: 0 for la in {"ar", "ja", "hi", "ru", "zh"}}
    for t, la in zip(texts, langs):
        if has_native_def(t, la):
            nat_hits[la] = nat_hits.get(la, 0) + 1
    print("\n  Détection marqueurs définitoires natifs :")
    for la, n in nat_hits.items():
        print(f"    {la} : {n}")

    # [A] CV 5-fold sur tout le corpus §100
    print("\n  [A] CV 5-fold sur les 983 phrases…")
    acc_a, std_a, per_type_a = cv_score(Xc, y, strata)
    print(f"      Accuracy : {acc_a:.1%} (±{std_a:.1%}) — §98 [A] : 96.7 %")
    for t in TYPES:
        print(f"        {t:<14s}{per_type_a[t]:.1%}")
    plang_a = per_lang_acc(Xc, y, langs, strata)
    print("\n      Par langue :")
    for la in ALL_LANGS:
        print(f"        {la:<6s}{plang_a[la]:.1%}")

    # [B] Hold-out cross-famille
    print("\n  [B] Hold-out : train sur LANGS_94 (7 langues §94), test sur NEW_LANGS (4)…")
    acc_b, ptype_b, plang_b, n_train, n_test = holdout_train_94_test_new(Xc, y, langs)
    print(f"      Train : {n_train}   Test : {n_test}")
    print(f"      Accuracy : {acc_b:.1%} — §98 [B] : 76.4 %")
    print("      Par type :")
    for t in TYPES:
        v = ptype_b.get(t)
        print(f"        {t:<14s}{v:.1%}" if v is not None else f"        {t:<14s}—")
    print("      Par langue (NEW) :")
    for la in NEW_LANGS:
        v = plang_b.get(la)
        print(f"        {la:<6s}{v:.1%}" if v is not None else f"        {la:<6s}—")

    out = {
        "benchmark": "§100 corpus étendu (983) + features natives définitoires + réentraînement",
        "model": MODEL_NAME,
        "n_total": n_total,
        "feature_dim": int(Xc.shape[1]),
        "additions": {
            "definitions_natives": add_def,
            "descriptions_factuelles": add_desc,
            "arabic_diversification": add_ar,
        },
        "native_def_marker_hits": nat_hits,
        "experiment_A_cv5_on_all": {
            "accuracy_mean": acc_a, "accuracy_std": std_a,
            "per_type": per_type_a, "per_lang": plang_a,
            "vs_v98": 0.967,
        },
        "experiment_B_holdout_train94_test_new": {
            "accuracy": acc_b, "per_type": ptype_b, "per_lang": plang_b,
            "n_train": n_train, "n_test": n_test,
            "vs_v98": 0.764,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(_to_native(out), f, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"\n  Résultats → {OUTPUT}")
    print("═" * W)


if __name__ == "__main__":
    main()

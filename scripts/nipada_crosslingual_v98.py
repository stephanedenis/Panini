#!/usr/bin/env python3
"""
§98 — Extension cross-lingual : ar/ru/ja/hi
============================================
Plan §97 : valider que le classifieur logreg-395 généralise au-delà des 7
langues d'entraînement (fr/en/de/es/zh/it/pt). Ajoute 4 langues structurellement
distinctes :
  - ar (arabe)   — sémitique RTL, racines triconsonantiques
  - ru (russe)   — slave, cas grammaticaux, cyrillique
  - ja (japonais) — agglutinant, particules, SOV, scripts mixtes
  - hi (hindi)   — indo-aryen, devanagari, postpositions

Protocole :
  10 phrases × 7 types × 4 langues = **280 nouvelles phrases**
  Total cumulé : 630 (§94) + 280 = **910 phrases × 11 langues**

Tests :
  [A] CV 5-fold stratifié sur les 910 phrases (intra-distribution)
  [B] **Hold-out cross-lingual** : train sur 7 langues §94 (630),
      test sur 4 langues §98 (280) — généralisation pure
  [C] Comparaison vs §97 sur les 7 langues originales (sanity check)

Output → research/nipada/falsification/nipada_v98_crosslingual_report.json
"""

from __future__ import annotations

import json
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

_spec = importlib.util.spec_from_file_location(
    "lacunes", REPO_ROOT / "scripts" / "test_nipada_lacunes.py"
)
_mod = importlib.util.module_from_spec(_spec)
_mod.__name__ = "lacunes"
_spec.loader.exec_module(_mod)  # type: ignore[attr-defined]

CORPUS_94 = _mod.CORPUS
LANGS_94 = _mod.LANGS  # 7 langues
SYNTACTIC_BONUS = _mod.SYNTACTIC_BONUS
_has_question_marker = _mod._has_question_marker
_has_introspection_marker = _mod._has_introspection_marker
_has_definition_marker = _mod._has_definition_marker
_NpEncoder = _mod._NpEncoder
_to_native = _mod._to_native

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v98_crosslingual_report.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


# ── Corpus §98 — 4 nouvelles langues × 7 types × 10 phrases ──────────────────
# Critères : phrases naturelles, registre varié, syntaxe propre à chaque langue.
# Pas de translittération, scripts natifs.

CORPUS_98: dict[str, dict[str, list[str]]] = {
    "description": {
        "ar": [
            "الماء جزيء يتكون من ذرتي هيدروجين وذرة أكسجين.",
            "برج إيفل يبلغ ارتفاعه ثلاثمائة وثلاثين متراً.",
            "القلب البشري ينبض حوالي سبعين مرة في الدقيقة.",
            "تتكون الذرة من نواة محاطة بإلكترونات.",
            "الفيل أكبر حيوان بري على وجه الأرض.",
            "نهر النيل يتدفق من الجنوب إلى الشمال.",
            "الجلد البشري يحتوي على ملايين المسامات.",
            "تحتوي شجرة الخوخ على ألف زهرة في الموسم.",
            "النحلة تمتلك خمس عيون وستة أرجل.",
            "تتكون الأرض من قشرة ووشاح ولب.",
        ],
        "ru": [
            "Вода — молекула, состоящая из двух атомов водорода и одного атома кислорода.",
            "Эйфелева башня достигает высоты триста тридцать метров.",
            "Сердце человека бьётся примерно семьдесят раз в минуту.",
            "Атом состоит из ядра, окружённого электронами.",
            "Слон — самое крупное наземное животное на Земле.",
            "Река Волга впадает в Каспийское море.",
            "Человеческая кожа содержит миллионы пор.",
            "Берёза имеет белую кору с чёрными отметинами.",
            "Пчела обладает пятью глазами и шестью ногами.",
            "Земля состоит из коры, мантии и ядра.",
        ],
        "ja": [
            "水は水素二つと酸素一つからなる分子である。",
            "エッフェル塔の高さは三百三十メートルに達する。",
            "人間の心臓は一分間に約七十回鼓動する。",
            "原子は核と核を取り巻く電子から構成されている。",
            "象は地球上最大の陸生動物である。",
            "信濃川は新潟県を流れて日本海に注ぐ。",
            "人間の皮膚には数百万の毛穴が含まれている。",
            "桜の木は春に淡紅色の花を咲かせる。",
            "蜂は五つの目と六本の脚を持っている。",
            "地球は地殻、マントル、核から成り立っている。",
        ],
        "hi": [
            "पानी एक अणु है जो दो हाइड्रोजन और एक ऑक्सीजन परमाणु से बना है।",
            "एफिल टॉवर की ऊँचाई तीन सौ तीस मीटर है।",
            "मानव हृदय प्रति मिनट लगभग सत्तर बार धड़कता है।",
            "परमाणु एक नाभिक और उसके चारों ओर इलेक्ट्रॉनों से बना होता है।",
            "हाथी पृथ्वी पर सबसे बड़ा भूमि जानवर है।",
            "गंगा नदी हिमालय से निकलकर बंगाल की खाड़ी में मिलती है।",
            "मानव त्वचा में लाखों छिद्र होते हैं।",
            "नीम का पेड़ भारत में बहुत आम है।",
            "मधुमक्खी की पाँच आँखें और छह पैर होते हैं।",
            "पृथ्वी क्रस्ट, मेंटल और कोर से बनी है।",
        ],
    },
    "définition": {
        "ar": [
            "الحرية هي القدرة على التصرف وفقاً لإرادة المرء دون إكراه خارجي.",
            "العدالة هي إعطاء كل ذي حق حقه.",
            "المثلث هو شكل هندسي ذو ثلاثة أضلاع وثلاث زوايا.",
            "الديمقراطية هي نظام حكم يستمد سلطته من الشعب.",
            "الذاكرة هي قدرة العقل على تخزين المعلومات واستعادتها.",
            "الفلسفة هي البحث عن الحكمة من خلال التفكير العقلاني.",
            "الفعل الجيد هو الذي يحقق الخير للجميع.",
            "العدد الأولي هو عدد طبيعي أكبر من واحد لا يقبل القسمة إلا على نفسه وعلى الواحد.",
            "السيادة هي السلطة العليا التي لا تخضع لسلطة أخرى.",
            "التعليم هو عملية اكتساب المعرفة والمهارات.",
        ],
        "ru": [
            "Свобода — это способность действовать по собственной воле без внешнего принуждения.",
            "Справедливость — это давать каждому то, что ему причитается.",
            "Треугольник — это геометрическая фигура с тремя сторонами и тремя углами.",
            "Демократия — это форма правления, при которой власть исходит от народа.",
            "Память — это способность ума хранить и воспроизводить информацию.",
            "Философия — это поиск мудрости посредством рационального мышления.",
            "Добрый поступок — это тот, который приносит благо всем.",
            "Простое число — это натуральное число больше единицы, делящееся только на себя и на единицу.",
            "Суверенитет — это высшая власть, не подчинённая никакой другой.",
            "Образование — это процесс приобретения знаний и навыков.",
        ],
        "ja": [
            "自由とは、外部からの強制なしに自分の意志に従って行動できる能力である。",
            "正義とは、各人に当然受け取るべきものを与えることである。",
            "三角形とは、三つの辺と三つの角を持つ幾何学的図形である。",
            "民主主義とは、権力が人民に由来する政治体制である。",
            "記憶とは、心が情報を蓄え、再生する能力である。",
            "哲学とは、理性的思考を通じて知恵を探求することである。",
            "善い行いとは、すべての人に利益をもたらす行いである。",
            "素数とは、一より大きく、一と自分自身でしか割り切れない自然数である。",
            "主権とは、他のいかなる権威にも従属しない最高の権力である。",
            "教育とは、知識と技能を獲得する過程である。",
        ],
        "hi": [
            "स्वतंत्रता बाहरी दबाव के बिना अपनी इच्छा के अनुसार कार्य करने की क्षमता है।",
            "न्याय वह है जो प्रत्येक को उसका हक देता है।",
            "त्रिभुज एक ज्यामितीय आकृति है जिसमें तीन भुजाएँ और तीन कोण होते हैं।",
            "लोकतंत्र वह शासन व्यवस्था है जिसमें सत्ता जनता से प्राप्त होती है।",
            "स्मृति मन की वह क्षमता है जिसके द्वारा सूचनाओं को संग्रहीत और पुनः प्राप्त किया जाता है।",
            "दर्शन तार्किक चिंतन के माध्यम से ज्ञान की खोज है।",
            "अच्छा कर्म वह है जो सभी का हित करता है।",
            "अभाज्य संख्या एक से बड़ी प्राकृतिक संख्या है जो केवल स्वयं और एक से विभाज्य होती है।",
            "संप्रभुता वह सर्वोच्च सत्ता है जो किसी अन्य के अधीन नहीं है।",
            "शिक्षा ज्ञान और कौशल अर्जित करने की प्रक्रिया है।",
        ],
    },
    "proclamation": {
        "ar": [
            "يولد جميع الناس أحراراً ومتساوين في الكرامة والحقوق.",
            "لكل فرد الحق في الحياة والحرية وسلامة شخصه.",
            "لا يجوز استرقاق أحد أو استعباده.",
            "لا يعرض أحد للتعذيب ولا للمعاملة القاسية أو المهينة.",
            "لكل إنسان أينما وجد الحق في الاعتراف بشخصيته القانونية.",
            "الناس جميعاً سواء أمام القانون.",
            "لا يجوز القبض على أي إنسان أو حجزه أو نفيه تعسفاً.",
            "لكل شخص حق التمتع بالأمن الاجتماعي.",
            "لكل فرد حق في حرية التفكير والضمير والدين.",
            "للأمة سيادة كاملة على ثرواتها الطبيعية.",
        ],
        "ru": [
            "Все люди рождаются свободными и равными в своём достоинстве и правах.",
            "Каждый имеет право на жизнь, свободу и личную неприкосновенность.",
            "Никто не должен содержаться в рабстве или подневольном состоянии.",
            "Никто не должен подвергаться пыткам или жестокому обращению.",
            "Каждый человек, где бы он ни находился, имеет право на признание его правосубъектности.",
            "Все люди равны перед законом.",
            "Никто не может быть подвергнут произвольному аресту или изгнанию.",
            "Каждый имеет право на социальное обеспечение.",
            "Каждый имеет право на свободу мысли, совести и религии.",
            "Народ обладает полным суверенитетом над своими природными ресурсами.",
        ],
        "ja": [
            "すべての人間は、生まれながらにして自由であり、かつ尊厳と権利において平等である。",
            "すべて人は、生命、自由及び身体の安全に対する権利を有する。",
            "何人も、奴隷状態に置かれることはない。",
            "何人も、拷問または残虐な取扱いを受けることはない。",
            "すべて人は、いかなる場所においても、法の下において人として認められる権利を有する。",
            "すべての人は、法の前に平等である。",
            "何人も、ほしいままに逮捕、拘禁または追放されることはない。",
            "すべて人は、社会保障を受ける権利を有する。",
            "すべて人は、思想、良心及び宗教の自由に対する権利を有する。",
            "国民は、自国の天然資源に対し完全な主権を有する。",
        ],
        "hi": [
            "सभी मनुष्य जन्म से स्वतंत्र और गरिमा एवं अधिकारों में समान हैं।",
            "प्रत्येक व्यक्ति को जीवन, स्वतंत्रता और व्यक्तिगत सुरक्षा का अधिकार है।",
            "किसी को भी दासता या बंधन में नहीं रखा जाएगा।",
            "किसी को भी यातना या क्रूर व्यवहार के अधीन नहीं किया जाएगा।",
            "प्रत्येक व्यक्ति को कानून के समक्ष व्यक्ति के रूप में मान्यता पाने का अधिकार है।",
            "सभी व्यक्ति कानून के समक्ष समान हैं।",
            "किसी को मनमाने ढंग से गिरफ्तार या निर्वासित नहीं किया जाएगा।",
            "प्रत्येक व्यक्ति को सामाजिक सुरक्षा का अधिकार है।",
            "प्रत्येक व्यक्ति को विचार, अंतःकरण और धर्म की स्वतंत्रता का अधिकार है।",
            "राष्ट्र अपने प्राकृतिक संसाधनों पर पूर्ण संप्रभुता रखता है।",
        ],
    },
    "question": {
        "ar": [
            "ما معنى الحياة؟",
            "هل توجد حقيقة موضوعية مستقلة عن الإدراك؟",
            "كيف نعرف ما نعرفه؟",
            "متى يصل القطار التالي إلى المحطة؟",
            "أين يقع أقرب مستشفى من هنا؟",
            "من اخترع المحرك البخاري؟",
            "لماذا تتحول أوراق الأشجار إلى اللون الأصفر في الخريف؟",
            "كم عدد كواكب المجموعة الشمسية؟",
            "هل يمكنك أن تخبرني عن الطريق إلى المتحف؟",
            "أي طريق يجب أن أسلكه للوصول إلى المطار؟",
        ],
        "ru": [
            "В чём смысл жизни?",
            "Существует ли объективная истина, независимая от восприятия?",
            "Как мы узнаём то, что знаем?",
            "Когда прибывает следующий поезд?",
            "Где находится ближайшая больница?",
            "Кто изобрёл паровой двигатель?",
            "Почему листья желтеют осенью?",
            "Сколько планет в Солнечной системе?",
            "Не могли бы вы подсказать дорогу к музею?",
            "Каким путём мне ехать в аэропорт?",
        ],
        "ja": [
            "人生の意味とは何か?",
            "知覚から独立した客観的真理は存在するのか?",
            "私たちは知っていることをどのようにして知るのか?",
            "次の電車はいつ到着しますか?",
            "最寄りの病院はどこですか?",
            "蒸気機関を発明したのは誰ですか?",
            "なぜ木の葉は秋に黄色くなるのですか?",
            "太陽系には惑星はいくつありますか?",
            "博物館への道を教えてくださいませんか?",
            "空港に行くにはどの道を通ればよいですか?",
        ],
        "hi": [
            "जीवन का अर्थ क्या है?",
            "क्या धारणा से स्वतंत्र कोई वस्तुनिष्ठ सत्य मौजूद है?",
            "हम जो जानते हैं वह कैसे जानते हैं?",
            "अगली ट्रेन कब आएगी?",
            "यहाँ से सबसे नज़दीक अस्पताल कहाँ है?",
            "भाप के इंजन का आविष्कार किसने किया?",
            "पतझड़ में पत्ते पीले क्यों हो जाते हैं?",
            "सौरमंडल में कितने ग्रह हैं?",
            "क्या आप मुझे संग्रहालय का रास्ता बता सकते हैं?",
            "हवाई अड्डे जाने के लिए मुझे कौन सा रास्ता लेना चाहिए?",
        ],
    },
    "ordre": {
        "ar": [
            "أغلق الباب بالمفتاح قبل أن تغادر.",
            "أزل الغطاء قبل تشغيل الجهاز.",
            "أرسل التقرير إلى الإدارة قبل الجمعة.",
            "اقرأ التعليمات بعناية قبل الاستخدام.",
            "افتح النافذة للسماح بدخول الهواء.",
            "اتبع الإشارات حتى المخرج الرئيسي.",
            "تجنب الاقتراب من الحافة.",
            "حافظ على هدوئك في حالة الطوارئ.",
            "افصل الجهاز عن مصدر الطاقة قبل التنظيف.",
            "احترم الآخرين كما تحب أن يحترموك.",
        ],
        "ru": [
            "Запри дверь на ключ перед уходом.",
            "Снимите крышку перед включением прибора.",
            "Отправьте отчёт руководству до пятницы.",
            "Внимательно прочитайте инструкцию перед использованием.",
            "Откройте окно, чтобы впустить воздух.",
            "Следуйте указателям к главному выходу.",
            "Не приближайтесь к краю.",
            "Сохраняйте спокойствие в случае чрезвычайной ситуации.",
            "Отключите прибор от сети перед чисткой.",
            "Уважайте других, как хотите, чтобы уважали вас.",
        ],
        "ja": [
            "出かける前に鍵をかけてドアを閉めなさい。",
            "装置を起動する前にカバーを外してください。",
            "金曜日までに経営陣に報告書を送ってください。",
            "使用前に説明書をよく読んでください。",
            "空気を入れるために窓を開けなさい。",
            "正面出口まで標識に従ってください。",
            "縁に近づかないでください。",
            "緊急時には冷静を保ちなさい。",
            "清掃の前に装置を電源から外してください。",
            "他人にされたいように他人を尊重しなさい。",
        ],
        "hi": [
            "जाने से पहले दरवाज़े को ताला लगाकर बंद कर दो।",
            "उपकरण चालू करने से पहले ढक्कन हटा दीजिए।",
            "शुक्रवार से पहले प्रबंधन को रिपोर्ट भेज दीजिए।",
            "उपयोग से पहले निर्देश ध्यान से पढ़िए।",
            "हवा आने के लिए खिड़की खोलिए।",
            "मुख्य निकास तक संकेतों का पालन कीजिए।",
            "किनारे के पास मत जाइए।",
            "आपातकाल में शांत रहिए।",
            "सफाई से पहले उपकरण को बिजली से अलग कर दीजिए।",
            "जैसा तुम चाहते हो दूसरों से व्यवहार वैसा ही उनसे करो।",
        ],
    },
    "narration": {
        "ar": [
            "في صباح أحد أيام الخريف، خرج الطفل من البيت لقطف التفاح.",
            "ثم سار في الغابة حتى وصل إلى نهر صغير.",
            "في عام 1492 أبحر كولومبوس غرباً واكتشف أرضاً جديدة.",
            "بعد ذلك، عبر الجيش الجبال خلال ثلاثة أيام.",
            "كانت الأم تطبخ الحساء بينما يلعب الأطفال في الحديقة.",
            "ذات يوم سقط ملك من على ظهر حصانه أثناء الصيد.",
            "غابت الشمس وأشعلت العائلة النار حول الخيمة.",
            "بدأ المهندس بناء الجسر في الربيع وأكمله في الخريف.",
            "كل صباح كان الخباز يخبز الخبز قبل شروق الشمس.",
            "في النهاية وصل المسافرون إلى المدينة بعد ثلاثة أشهر من السفر.",
        ],
        "ru": [
            "Однажды осенним утром мальчик вышел из дома собирать яблоки.",
            "Затем он шёл по лесу, пока не дошёл до маленькой речки.",
            "В тысяча четыреста девяносто втором году Колумб поплыл на запад и открыл новые земли.",
            "Потом армия пересекла горы за три дня.",
            "Мать варила суп, пока дети играли в саду.",
            "Однажды король упал с лошади во время охоты.",
            "Солнце село, и семья развела костёр возле палатки.",
            "Инженер начал строить мост весной и закончил его осенью.",
            "Каждое утро пекарь пёк хлеб до восхода солнца.",
            "В конце концов путники достигли города после трёх месяцев пути.",
        ],
        "ja": [
            "ある秋の朝、少年はリンゴを摘みに家を出た。",
            "それから森を歩き、小さな川にたどり着いた。",
            "千四百九十二年、コロンブスは西へ航海し新しい大陸を発見した。",
            "その後、軍は三日間で山を越えた。",
            "母はスープを作り、子供たちは庭で遊んでいた。",
            "ある日、王は狩りの最中に馬から落ちた。",
            "日が沈み、家族はテントの周りで火を焚いた。",
            "技師は春に橋の建設を始め、秋に完成させた。",
            "毎朝パン屋は日の出前にパンを焼いていた。",
            "ついに旅人たちは三か月の旅の末に都に着いた。",
        ],
        "hi": [
            "एक पतझड़ की सुबह लड़का सेब तोड़ने के लिए घर से निकला।",
            "फिर वह जंगल में चलते हुए एक छोटी नदी तक पहुँचा।",
            "सन् चौदह सौ बानवे में कोलंबस पश्चिम की ओर रवाना हुआ और नई धरती खोजी।",
            "इसके बाद सेना ने तीन दिनों में पहाड़ पार किए।",
            "माँ सूप पका रही थी जबकि बच्चे बगीचे में खेल रहे थे।",
            "एक दिन शिकार के दौरान राजा घोड़े से गिर पड़ा।",
            "सूरज डूब गया और परिवार ने तंबू के पास आग जलाई।",
            "इंजीनियर ने वसंत में पुल बनाना शुरू किया और पतझड़ में पूरा किया।",
            "हर सुबह नानबाई सूरज उगने से पहले रोटी पकाता था।",
            "अंततः यात्री तीन महीने की यात्रा के बाद नगर पहुँचे।",
        ],
    },
    "introspection": {
        "ar": [
            "أشعر بالحزن دون أن أعرف السبب.",
            "أتساءل أحياناً عن جدوى ما أفعله.",
            "أعتقد أنني قد أكون مخطئاً في حكمي السابق.",
            "أتذكر طفولتي بحنين عميق.",
            "أحس بضياع داخلي يصعب وصفه.",
            "أفكر كثيراً في معنى وجودي.",
            "أخشى من أن أفقد من أحب.",
            "أشعر بالامتنان لكل ما عشته حتى اليوم.",
            "أتأمل أفكاري وكأنها أمواج تأتي وتذهب.",
            "أدرك الآن أنني تغيرت كثيراً منذ سنوات.",
        ],
        "ru": [
            "Я чувствую грусть, не зная её причины.",
            "Иногда я задаюсь вопросом, имеет ли смысл то, что я делаю.",
            "Думаю, что я мог ошибаться в своём прежнем суждении.",
            "Я вспоминаю своё детство с глубокой ностальгией.",
            "Я ощущаю внутреннюю потерянность, которую трудно описать.",
            "Я часто размышляю о смысле своего существования.",
            "Я боюсь потерять тех, кого люблю.",
            "Я благодарен за всё, что я пережил до сегодняшнего дня.",
            "Я наблюдаю за своими мыслями, словно они волны, приходящие и уходящие.",
            "Теперь я понимаю, что сильно изменился за эти годы.",
        ],
        "ja": [
            "なぜか分からないが悲しみを感じる。",
            "自分のしていることに意味があるのかと時々問う。",
            "以前の判断が間違っていたかもしれないと思う。",
            "深い郷愁とともに子供時代を思い出す。",
            "言葉にしがたい内なる迷いを感じる。",
            "自分の存在の意味についてよく考える。",
            "愛する人を失うことを恐れている。",
            "今日までに経験したすべてに感謝している。",
            "自分の思考を、寄せては返す波のように見つめている。",
            "ここ数年で自分は大きく変わったと今気づいている。",
        ],
        "hi": [
            "मुझे बिना कारण जाने उदासी महसूस होती है।",
            "मैं कभी-कभी सोचता हूँ कि जो मैं कर रहा हूँ उसका कोई अर्थ है या नहीं।",
            "मुझे लगता है कि मेरा पिछला निर्णय ग़लत हो सकता था।",
            "मैं अपने बचपन को गहरी याद के साथ याद करता हूँ।",
            "मैं भीतर एक खोयापन महसूस करता हूँ जिसे शब्दों में बताना कठिन है।",
            "मैं अक्सर अपने अस्तित्व के अर्थ के बारे में सोचता हूँ।",
            "मुझे डर है कि मैं अपने प्रियजनों को खो दूँगा।",
            "मैं आज तक के अपने हर अनुभव के लिए कृतज्ञ हूँ।",
            "मैं अपने विचारों को आती-जाती लहरों की तरह देखता हूँ।",
            "अब मुझे एहसास होता है कि मैं इन वर्षों में बहुत बदल गया हूँ।",
        ],
    },
}

NEW_LANGS = ["ar", "ru", "ja", "hi"]
ALL_LANGS = LANGS_94 + NEW_LANGS  # 11 langues
LANG2IDX = {la: i for i, la in enumerate(ALL_LANGS)}

TYPES = list(CORPUS_94.keys())
TYPE2IDX = {t: i for i, t in enumerate(TYPES)}
IDX2TYPE = {i: t for t, i in TYPE2IDX.items()}


def merge_corpus() -> dict[str, dict[str, list[str]]]:
    merged: dict[str, dict[str, list[str]]] = {}
    for t in TYPES:
        merged[t] = dict(CORPUS_94[t])
        for la in NEW_LANGS:
            merged[t][la] = CORPUS_98[t][la]
    return merged


def syntactic_features(text: str, lang: str) -> np.ndarray:
    has_q = _has_question_marker(text)
    has_1p = _has_introspection_marker(text)
    has_def = _has_definition_marker(text)
    pro_drop = 1.0 if lang in {"it", "pt", "es", "ja"} else 0.0  # ja aussi pro-drop
    return np.array([float(has_q), float(has_1p), float(has_def), pro_drop], dtype=np.float32)


def lang_onehot(lang: str) -> np.ndarray:
    v = np.zeros(len(ALL_LANGS), dtype=np.float32)
    v[LANG2IDX[lang]] = 1.0
    return v


def build_dataset(model: SentenceTransformer, corpus: dict):
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
    feats_syn = np.stack([syntactic_features(t, la) for t, la in zip(texts, langs)])
    feats_lang = np.stack([lang_onehot(la) for la in langs])
    y_arr = np.asarray(y, dtype=np.int64)
    strata = np.asarray([TYPE2IDX[TYPES[yi]] * len(ALL_LANGS) + LANG2IDX[la] for yi, la in zip(y, langs)])
    return X, feats_syn, feats_lang, y_arr, np.asarray(langs), strata, texts


def train_logreg(X: np.ndarray, y: np.ndarray, C: float = 1.0) -> LogisticRegression:
    clf = LogisticRegression(C=C, max_iter=2000, solver="lbfgs", random_state=42)
    clf.fit(X, y)
    return clf


def evaluate(clf, X, y, langs):
    preds = clf.predict(X)
    correct = (preds == y).sum()
    total = len(y)
    confusion = np.zeros((len(TYPES), len(TYPES)), dtype=np.int64)
    per_lang = {la: [0, 0] for la in ALL_LANGS}
    per_type = {t: [0, 0] for t in TYPES}
    for true_i, pred_i, la in zip(y, preds, langs):
        confusion[true_i, pred_i] += 1
        per_lang[la][1] += 1
        per_type[TYPES[true_i]][1] += 1
        if pred_i == true_i:
            per_lang[la][0] += 1
            per_type[TYPES[true_i]][0] += 1
    return {
        "global": float(correct / total),
        "n": int(total),
        "lang_accuracy": {la: per_lang[la][0] / max(per_lang[la][1], 1) for la in ALL_LANGS},
        "type_accuracy": {t: per_type[t][0] / max(per_type[t][1], 1) for t in TYPES},
        "confusion_matrix": {TYPES[i]: {TYPES[j]: int(confusion[i, j]) for j in range(len(TYPES))}
                              for i in range(len(TYPES))},
    }


def cv_score(X, y, langs, strata, n_splits: int = 5):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    splits = list(skf.split(X, strata))
    confusion = np.zeros((len(TYPES), len(TYPES)), dtype=np.int64)
    per_lang = {la: [0, 0] for la in ALL_LANGS}
    fold_acc = []
    for tr, te in splits:
        clf = train_logreg(X[tr], y[tr])
        preds = clf.predict(X[te])
        fold_acc.append(float((preds == y[te]).sum() / len(te)))
        for true_i, pred_i, la in zip(y[te], preds, langs[te]):
            confusion[true_i, pred_i] += 1
            per_lang[la][1] += 1
            if pred_i == true_i:
                per_lang[la][0] += 1
    return {
        "global_micro": float(confusion.trace() / max(confusion.sum(), 1)),
        "fold_mean": float(np.mean(fold_acc)),
        "fold_std": float(np.std(fold_acc)),
        "fold_accuracies": fold_acc,
        "lang_accuracy": {la: per_lang[la][0] / max(per_lang[la][1], 1) for la in ALL_LANGS},
        "type_accuracy": {TYPES[i]: float(confusion[i, i]) / max(confusion[i].sum(), 1)
                           for i in range(len(TYPES))},
        "confusion_matrix": {TYPES[i]: {TYPES[j]: int(confusion[i, j]) for j in range(len(TYPES))}
                              for i in range(len(TYPES))},
    }


def main() -> None:
    W = 78
    print("═" * W)
    print("  §98 — Extension cross-lingual : ar/ru/ja/hi (910 phrases × 11 langues)")
    print("═" * W)

    model = SentenceTransformer(MODEL_NAME)
    corpus_full = merge_corpus()

    print("\n  [1] Encodage du corpus complet (910 phrases)…")
    X, feats_syn, feats_lang, y, langs, strata, texts = build_dataset(model, corpus_full)
    print(f"  X.shape = {X.shape}  |  langues = {ALL_LANGS}")

    extra = np.hstack([feats_syn, feats_lang])
    Xc = np.hstack([X, extra])

    # ── [A] CV 5-fold sur les 910 phrases ────────────────────────────────────
    print("\n  [A] Validation croisée 5-fold stratifiée sur 910 phrases…")
    cv_all = cv_score(Xc, y, langs, strata, n_splits=5)
    print(f"      global  = {cv_all['global_micro']:.1%}  (±{cv_all['fold_std']:.1%})")

    # ── [B] Hold-out cross-lingual : train sur 7 langues §94, test sur 4 §98 ──
    print("\n  [B] Hold-out cross-lingual : train 7 langues (630), test 4 langues (280)…")
    train_mask = np.isin(langs, LANGS_94)
    test_mask = np.isin(langs, NEW_LANGS)
    clf = train_logreg(Xc[train_mask], y[train_mask])
    holdout = evaluate(clf, Xc[test_mask], y[test_mask], langs[test_mask])
    print(f"      global  = {holdout['global']:.1%}  ({holdout['n']} phrases)")

    # ── [C] Sanity check : test sur les 7 langues d'origine après ré-entraînement
    print("\n  [C] Sanity check : ré-entraîne logreg-395 sur 7 langues §94 → CV interne…")
    sub_X = Xc[train_mask]
    sub_y = y[train_mask]
    sub_langs = langs[train_mask]
    sub_strata = np.asarray([TYPE2IDX[TYPES[yi]] * len(ALL_LANGS) + LANG2IDX[la]
                              for yi, la in zip(sub_y, sub_langs)])
    cv_94 = cv_score(sub_X, sub_y, sub_langs, sub_strata, n_splits=5)
    print(f"      global  = {cv_94['global_micro']:.1%}  (rappel §97 = 97.6%)")

    # ── Affichage ────────────────────────────────────────────────────────────
    print("\n" + "═" * W)
    print("  RÉSULTATS §98")
    print("═" * W)
    print(f"  {'expérience':<48s} {'global':>8s}")
    print(f"  {'[A] CV 5-fold sur 910 phrases (11 langues)':<48s} {cv_all['global_micro']:>8.1%}")
    print(f"  {'[B] hold-out 4 nouvelles langues (ar/ru/ja/hi)':<48s} {holdout['global']:>8.1%}")
    print(f"  {'[C] CV 5-fold sur 630 phrases §94 (rappel)':<48s} {cv_94['global_micro']:>8.1%}")

    print("\n  ── Hold-out [B] : accuracy par langue ──")
    print(f"  {'lang':<6s}{'acc':>10s}")
    for la in NEW_LANGS:
        print(f"  {la:<6s}{holdout['lang_accuracy'][la]:>10.1%}")

    print("\n  ── Hold-out [B] : accuracy par type ──")
    print(f"  {'type':<16s}{'acc':>10s}")
    for t in TYPES:
        print(f"  {t:<16s}{holdout['type_accuracy'][t]:>10.1%}")

    print("\n  ── CV [A] : accuracy par langue (toutes 11) ──")
    print(f"  {'lang':<6s}{'acc':>10s}")
    for la in ALL_LANGS:
        print(f"  {la:<6s}{cv_all['lang_accuracy'][la]:>10.1%}")

    out = {
        "benchmark": "§98 extension cross-lingual ar/ru/ja/hi (910 phrases × 11 langues)",
        "model": MODEL_NAME,
        "n_total": int(len(y)),
        "langs_train_94": LANGS_94,
        "langs_holdout_98": NEW_LANGS,
        "all_langs": ALL_LANGS,
        "types": TYPES,
        "experiment_A_cv5_on_910": cv_all,
        "experiment_B_holdout_new_langs": holdout,
        "experiment_C_cv5_on_630": cv_94,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(_to_native(out), f, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"\n  Résultats → {OUTPUT}")
    print("═" * W)


if __name__ == "__main__":
    main()

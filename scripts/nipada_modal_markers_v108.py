#!/usr/bin/env python3
"""
§108 — Détecteur multilingue de marqueurs modaux
==================================================

Pour chaque langue du corpus §100, on liste les marqueurs des 7 modalités
nipada_v7 (DEVOIR, POUVOIR, VOULOIR, DOUTE, ORDONNER, SAVOIR, PROBABILITÉ_T)
identifiées en §102. Le détecteur retourne un vecteur 7-dim de comptages
par phrase.

Les marqueurs ont été collectés dans la littérature de typologie modale :
- IE-occidentale : modaux verbaux (devoir, must, dovere, deber, müssen…)
- arabe : يجب / يمكن / ينبغي + particules
- chinois : 应/应该/必须/能/会/可能/想/要 etc.
- russe : должен / надо / можно / надо бы / возможно
- japonais : べき / なければならない / られる / かもしれない / たい / だろう
- hindi : चाहिए / सकता / होगा / शायद / पड़ेगा

Ce module est consommé par §107 (ré-annotation) et §111 (profil auteur).

Sortie :
  - research/nipada/modal/markers_v108.json     — table complète
  - research/nipada/modal/coverage_v108.json    — couverture sur corpus §100
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

OUT_DIR = REPO_ROOT / "research" / "nipada" / "modal"


# ══════════════════════════════════════════════════════════════════════════════
# 7 modalités V7 = MOLECULES_MODALES restreintes aux 7 atomiques (sans
# combinaisons SAVOIR/ESPÉRER/DESTINÉE qui sont des composées).
# Indices : 0=DEVOIR 1=POUVOIR 2=VOULOIR 3=DOUTE 4=ORDONNER 5=SAVOIR 6=PROBABILITÉ_T
# ══════════════════════════════════════════════════════════════════════════════

MODALITES = ["DEVOIR", "POUVOIR", "VOULOIR", "DOUTE", "ORDONNER", "SAVOIR", "PROBABILITÉ_T"]
MOD2IDX = {m: i for i, m in enumerate(MODALITES)}
N_MOD = len(MODALITES)

# Atomes V7 associés (cf. §102)
MODALITE_ATOMS = {
    "DEVOIR":         [2, 17],          # 34
    "POUVOIR":        [5, 17],          # 85
    "VOULOIR":        [11, 17],         # 187
    "DOUTE":          [3, 17],          # 51
    "ORDONNER":       [2, 11, 17],      # 374
    "SAVOIR":         [2, 3, 17],       # 102
    "PROBABILITÉ_T":  [13, 17],         # 221
}


# ══════════════════════════════════════════════════════════════════════════════
# Marqueurs par langue × modalité
# Sources : grammaires de référence, typologie modale (Palmer 2001, Bybee 1994).
# Format : liste de patterns regex (avec frontières mot adaptées à chaque script).
# ══════════════════════════════════════════════════════════════════════════════

# Helpers de frontière pour scripts non-latins (CJK, devanāgarī, arabe) :
# pas de \b utilisable → on cherche le motif tel quel (les caractères Han et
# devanāgarī délimitent leurs propres mots dans le contexte).

def _word_bounded(words: list[str]) -> list[re.Pattern]:
    return [re.compile(r"(?<![A-Za-zÀ-ÿ])" + re.escape(w) + r"(?![A-Za-zÀ-ÿ])", re.IGNORECASE)
            for w in words]


def _substring(words: list[str]) -> list[re.Pattern]:
    return [re.compile(re.escape(w)) for w in words]


MARKERS: dict[str, dict[str, list[re.Pattern]]] = {
    # ── Français ──────────────────────────────────────────────────────────
    "fr": {
        "DEVOIR": _word_bounded(["doit", "doivent", "doive", "dois", "devra", "devrait",
                                 "devraient", "il faut", "faudra", "faudrait", "il est nécessaire",
                                 "nécessairement"]),
        "POUVOIR": _word_bounded(["peut", "peuvent", "puisse", "pourra", "pourrait",
                                  "pouvait", "il est possible"]),
        "VOULOIR": _word_bounded(["veut", "veulent", "veuille", "voudra", "voudrait",
                                  "souhaite", "souhaitent", "désire", "désirent"]),
        "DOUTE": _word_bounded(["est-ce", "peut-être", "douteux", "douter", "incertain",
                                "probablement"]) + [re.compile(r"\?"), re.compile(r"\bsi\s+\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["faut", "doit", "exige", "ordonne", "obligé"]),
        "SAVOIR": _word_bounded(["sait", "savent", "savait", "il est connu", "selon", "d'après"]),
        "PROBABILITÉ_T": _word_bounded(["sera", "seront", "deviendra", "demain", "plus tard"])
                          + [re.compile(r"\b(?:au\s+futur|dans\s+le\s+futur)\b", re.IGNORECASE)],
    },
    # ── Anglais ───────────────────────────────────────────────────────────
    "en": {
        "DEVOIR": _word_bounded(["must", "shall", "ought", "have to", "has to", "had to",
                                 "should", "needs to", "necessarily"]),
        "POUVOIR": _word_bounded(["can", "could", "may", "might", "able to"]),
        "VOULOIR": _word_bounded(["want", "wants", "wanted", "wish", "wishes", "would like",
                                  "desire"]),
        "DOUTE": _word_bounded(["maybe", "perhaps", "doubt", "doubtful", "uncertain",
                                "probably"]) + [re.compile(r"\?"), re.compile(r"\bif\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["must", "shall", "have to", "obliged", "command", "order"]),
        "SAVOIR": _word_bounded(["knows", "known", "known to", "according"]),
        "PROBABILITÉ_T": _word_bounded(["will", "shall", "going to", "tomorrow", "future",
                                         "soon"]),
    },
    # ── Italien ───────────────────────────────────────────────────────────
    "it": {
        "DEVOIR": _word_bounded(["deve", "devono", "dovrà", "dovrebbe", "occorre", "bisogna"]),
        "POUVOIR": _word_bounded(["può", "possono", "potrà", "potrebbe", "è possibile"]),
        "VOULOIR": _word_bounded(["vuole", "vogliono", "vorrebbe", "desidera"]),
        "DOUTE": _word_bounded(["forse", "probabilmente", "incerto", "dubbio"])
                  + [re.compile(r"\?"), re.compile(r"\bse\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["deve", "occorre", "bisogna", "ordina", "obbligato"]),
        "SAVOIR": _word_bounded(["sa", "sanno", "secondo"]),
        "PROBABILITÉ_T": _word_bounded(["sarà", "saranno", "domani", "futuro"]),
    },
    # ── Espagnol ──────────────────────────────────────────────────────────
    "es": {
        "DEVOIR": _word_bounded(["debe", "deben", "deberá", "debería", "hay que", "tiene que"]),
        "POUVOIR": _word_bounded(["puede", "pueden", "podrá", "podría", "es posible"]),
        "VOULOIR": _word_bounded(["quiere", "quieren", "querría", "desea"]),
        "DOUTE": _word_bounded(["quizás", "tal vez", "probablemente", "duda", "incierto"])
                  + [re.compile(r"\?"), re.compile(r"\bsi\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["debe", "hay que", "ordena", "obligado"]),
        "SAVOIR": _word_bounded(["sabe", "saben", "según"]),
        "PROBABILITÉ_T": _word_bounded(["será", "serán", "mañana", "futuro"]),
    },
    # ── Portugais ─────────────────────────────────────────────────────────
    "pt": {
        "DEVOIR": _word_bounded(["deve", "devem", "deverá", "deveria", "é preciso", "tem que"]),
        "POUVOIR": _word_bounded(["pode", "podem", "poderá", "poderia", "é possível"]),
        "VOULOIR": _word_bounded(["quer", "querem", "queria", "deseja"]),
        "DOUTE": _word_bounded(["talvez", "provavelmente", "dúvida", "incerto"])
                  + [re.compile(r"\?"), re.compile(r"\bse\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["deve", "é preciso", "ordena", "obrigado"]),
        "SAVOIR": _word_bounded(["sabe", "sabem", "segundo"]),
        "PROBABILITÉ_T": _word_bounded(["será", "serão", "amanhã", "futuro"]),
    },
    # ── Allemand ──────────────────────────────────────────────────────────
    "de": {
        "DEVOIR": _word_bounded(["muss", "müssen", "musste", "sollte", "sollen", "sollten",
                                 "notwendig"]),
        "POUVOIR": _word_bounded(["kann", "können", "könnte", "konnte", "möglich"]),
        "VOULOIR": _word_bounded(["will", "wollen", "möchte", "wünscht"]),
        "DOUTE": _word_bounded(["vielleicht", "wahrscheinlich", "Zweifel", "ungewiss"])
                  + [re.compile(r"\?"), re.compile(r"\bob\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["muss", "soll", "befiehlt", "verpflichtet"]),
        "SAVOIR": _word_bounded(["weiß", "wissen", "bekannt", "laut"]),
        "PROBABILITÉ_T": _word_bounded(["wird", "werden", "morgen", "Zukunft"]),
    },
    # ── Russe (cyrillique, frontières mot OK) ────────────────────────────
    "ru": {
        "DEVOIR": _word_bounded(["должен", "должна", "должны", "надо", "необходимо",
                                  "следует"]),
        "POUVOIR": _word_bounded(["может", "можно", "смог", "сможет", "возможно"]),
        "VOULOIR": _word_bounded(["хочет", "хочу", "желает", "хотел"]),
        "DOUTE": _word_bounded(["возможно", "вероятно", "может быть", "сомнение",
                                  "неуверен"])
                  + [re.compile(r"\?"), re.compile(r"\bли\b", re.IGNORECASE)],
        "ORDONNER": _word_bounded(["должен", "приказ", "обязан"]),
        "SAVOIR": _word_bounded(["знает", "известно", "согласно"]),
        "PROBABILITÉ_T": _word_bounded(["будет", "будут", "завтра", "будущее"]),
    },
    # ── Arabe ─────────────────────────────────────────────────────────────
    "ar": {
        "DEVOIR": _substring(["يجب", "ينبغي", "لا بد", "ضروري", "لزاما"]),
        "POUVOIR": _substring(["يمكن", "قد", "ربما", "بالإمكان", "قادر"]),
        "VOULOIR": _substring(["يريد", "يرغب", "يود"]),
        "DOUTE": _substring(["ربما", "لعل", "محتمل", "شك"]) + [re.compile(r"\?"), re.compile(r"؟")],
        "ORDONNER": _substring(["يجب", "أمر", "يأمر", "ملزم"]),
        "SAVOIR": _substring(["يعرف", "معروف", "وفقا", "بحسب"]),
        "PROBABILITÉ_T": _substring(["سوف", "سيكون", "غدا", "المستقبل"]),
    },
    # ── Chinois ───────────────────────────────────────────────────────────
    "zh": {
        "DEVOIR": _substring(["应当", "应该", "必须", "得", "需要"]),
        "POUVOIR": _substring(["能", "可以", "可", "会", "能够"]),
        "VOULOIR": _substring(["想", "要", "希望", "愿意", "欲"]),
        "DOUTE": _substring(["可能", "也许", "或许", "大概", "怀疑"]) + [re.compile(r"吗"),
                                                                          re.compile(r"\?"),
                                                                          re.compile(r"？")],
        "ORDONNER": _substring(["必须", "命令", "得", "应"]),
        "SAVOIR": _substring(["知道", "据说", "根据"]),
        "PROBABILITÉ_T": _substring(["将", "会", "明天", "未来"]),
    },
    # ── Japonais ──────────────────────────────────────────────────────────
    "ja": {
        "DEVOIR": _substring(["べき", "なければならない", "ねばならない", "必要", "しなければ"]),
        "POUVOIR": _substring(["できる", "られる", "可能", "得る"]),
        "VOULOIR": _substring(["たい", "ほしい", "望む", "願う"]),
        "DOUTE": _substring(["かもしれない", "だろう", "おそらく", "疑"]) + [re.compile(r"か。"),
                                                                                  re.compile(r"\?"),
                                                                                  re.compile(r"？")],
        "ORDONNER": _substring(["べき", "なさい", "せよ", "命じる"]),
        "SAVOIR": _substring(["知る", "周知", "によれば"]),
        "PROBABILITÉ_T": _substring(["でしょう", "明日", "未来", "将来"]),
    },
    # ── Hindi ─────────────────────────────────────────────────────────────
    "hi": {
        "DEVOIR": _substring(["चाहिए", "ज़रूरी", "ज़रूर", "पड़ेगा", "करना है"]),
        "POUVOIR": _substring(["सकता", "सकती", "सकते", "सकना", "मुमकिन"]),
        "VOULOIR": _substring(["चाहता", "चाहती", "चाहते", "इच्छा"]),
        "DOUTE": _substring(["शायद", "संभवतः", "संदेह", "अनिश्चित"])
                  + [re.compile(r"\?"), re.compile(r"क्या")],
        "ORDONNER": _substring(["चाहिए", "आदेश", "बाध्य"]),
        "SAVOIR": _substring(["जानता", "ज्ञात", "के अनुसार"]),
        "PROBABILITÉ_T": _substring(["गा", "गी", "गे", "कल", "भविष्य"]),
    },
}


def detect_modalities(text: str, lang: str) -> dict[str, int]:
    """Retourne {modalité: nb d'occurrences} pour la langue donnée."""
    counts = {m: 0 for m in MODALITES}
    if lang not in MARKERS:
        return counts
    for mod, patterns in MARKERS[lang].items():
        for p in patterns:
            counts[mod] += len(p.findall(text))
    return counts


def detect_modalities_vec(text: str, lang: str) -> list[int]:
    c = detect_modalities(text, lang)
    return [c[m] for m in MODALITES]


def has_any_modality(text: str, lang: str) -> bool:
    return sum(detect_modalities_vec(text, lang)) > 0


def dominant_modality(text: str, lang: str) -> str | None:
    """Retourne la modalité dominante (par count) ou None."""
    c = detect_modalities(text, lang)
    best = None
    best_n = 0
    for m, n in c.items():
        if n > best_n:
            best = m
            best_n = n
    return best


# ══════════════════════════════════════════════════════════════════════════════
# Validation : couverture sur corpus §100
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 78)
    print("  §108 — Détecteur multilingue de marqueurs modaux")
    print("═" * 78)

    n_lang = len(MARKERS)
    n_patterns_total = sum(sum(len(ps) for ps in mods.values()) for mods in MARKERS.values())
    print(f"\n  Langues couvertes  : {n_lang} ({', '.join(sorted(MARKERS.keys()))})")
    print(f"  Modalités          : {N_MOD} ({', '.join(MODALITES)})")
    print(f"  Patterns totaux    : {n_patterns_total}")

    # Mesure de couverture sur corpus §100
    print("\n  ── Couverture sur corpus §100 (980 phrases) ──")
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py"
    )
    _v100 = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_v100)  # type: ignore[attr-defined]

    corpus = _v100.merge_corpus_v100()
    cov_per_type: dict[str, dict[str, int]] = {t: {m: 0 for m in MODALITES + ["ANY"]}
                                                for t in _v100.TYPES}
    counts_per_type: dict[str, int] = {t: 0 for t in _v100.TYPES}
    for t, by_lang in corpus.items():
        for la, phrases in by_lang.items():
            for p in phrases:
                counts_per_type[t] += 1
                vec = detect_modalities(p, la)
                if any(v > 0 for v in vec.values()):
                    cov_per_type[t]["ANY"] += 1
                for m, n in vec.items():
                    if n > 0:
                        cov_per_type[t][m] += 1

    print(f"  {'type':<14s}|  ANY |", " | ".join(f"{m[:7]:>7s}" for m in MODALITES), "|  N")
    for t in _v100.TYPES:
        N = counts_per_type[t]
        any_pct = 100.0 * cov_per_type[t]["ANY"] / max(1, N)
        cells = " | ".join(f"{100.0 * cov_per_type[t][m] / max(1,N):6.1f}" for m in MODALITES)
        print(f"  {t:<14s}|{any_pct:5.1f} | {cells} | {N}")

    # Sortie
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    markers_serializable = {
        la: {m: [p.pattern for p in ps] for m, ps in mods.items()}
        for la, mods in MARKERS.items()
    }
    (OUT_DIR / "markers_v108.json").write_text(json.dumps({
        "version": "§108",
        "modalites": MODALITES,
        "modalite_atoms": MODALITE_ATOMS,
        "languages": sorted(MARKERS.keys()),
        "n_patterns_total": n_patterns_total,
        "markers": markers_serializable,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    (OUT_DIR / "coverage_v108.json").write_text(json.dumps({
        "version": "§108",
        "corpus": "§100 (980 phrases × 11 langues)",
        "coverage_per_type": {t: {**cov_per_type[t], "TOTAL_PHRASES": counts_per_type[t]}
                               for t in _v100.TYPES},
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n  Sortie : {(OUT_DIR / 'markers_v108.json').relative_to(REPO_ROOT)}")
    print(f"           {(OUT_DIR / 'coverage_v108.json').relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

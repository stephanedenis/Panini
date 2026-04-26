"""
§142 — Pipeline de tokenisation/lemmatisation multilingue.

Contraintes :
- Zéro téléchargement de modèles lourds.
- Couvre 8 langues (lat, grc, san, lzh, ara, eng, fra, deu).
- Si un lemmatiseur tiers est disponible (CLTK, Stanza), on l'utilise ;
  sinon fallback déterministe (regex + casefold + heuristiques par langue).

Format unifié de sortie (JSONL) :
  {frag_id, work_id, lang, sentence_id, token_id, surface, lemma, pos}

Le but n'est pas la lemmatisation parfaite mais un substrat normalisé
qui permet à §143 (alignement) et §144+ (annotation) de travailler sur
des unités comparables.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
OUT_DIR = ROOT / "corpus" / "protoatheism_tokens"


# ----------------------------------------------------------------------------
# Sentence splitters par langue
# ----------------------------------------------------------------------------

SENT_SPLIT_LATIN = re.compile(r"(?<=[\.\!\?])\s+|(?<=[\.\!\?])$")
SENT_SPLIT_GREEK = re.compile(r"(?<=[\.\;\!\·])\s+|(?<=[\.\;\!\·])$")
SENT_SPLIT_DEVA = re.compile(r"(?<=[।॥])\s*")  # daṇḍa, double daṇḍa
SENT_SPLIT_CJK = re.compile(r"(?<=[。！？；])")
SENT_SPLIT_ARABIC = re.compile(r"(?<=[\.\!\?؟])\s+")


def split_sentences(text: str, lang: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if lang == "lat":
        parts = SENT_SPLIT_LATIN.split(text)
    elif lang == "grc":
        parts = SENT_SPLIT_GREEK.split(text)
    elif lang == "san":
        parts = SENT_SPLIT_DEVA.split(text)
    elif lang == "lzh":
        parts = SENT_SPLIT_CJK.split(text)
    elif lang == "ara":
        parts = SENT_SPLIT_ARABIC.split(text)
    else:  # eng/fra/deu
        parts = re.split(r"(?<=[\.\!\?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


# ----------------------------------------------------------------------------
# Tokenizers par langue
# ----------------------------------------------------------------------------

WORD_LATIN = re.compile(r"[A-Za-zĀ-žœæ]+", re.UNICODE)
WORD_GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]+")
WORD_DEVA = re.compile(r"[\u0900-\u097F]+|[a-zāīūṛṝḷḹṅñṭḍṇśṣḥṃ]+")
WORD_ARABIC = re.compile(r"[\u0600-\u06FF\u0750-\u077F]+")


def tokenize(sentence: str, lang: str) -> list[str]:
    if lang == "lat":
        return WORD_LATIN.findall(sentence)
    if lang == "grc":
        return WORD_GREEK.findall(sentence)
    if lang == "san":
        return WORD_DEVA.findall(sentence)
    if lang == "lzh":
        # Chinois classique : un caractère ≈ un token
        return [c for c in sentence if "\u4e00" <= c <= "\u9fff"]
    if lang == "ara":
        return WORD_ARABIC.findall(sentence)
    # Latin script européen
    return re.findall(r"[A-Za-zÀ-ÿ]+", sentence)


# ----------------------------------------------------------------------------
# Lemmatisation : fallback déterministe par langue
# ----------------------------------------------------------------------------

LATIN_SUFFIXES = ["ibus", "arum", "orum", "tur", "mus", "tis", "que",
                  "us", "um", "is", "es", "as", "os", "am", "im",
                  "em", "ae", "ei", "ui", "i", "o", "a", "e", "u"]

GREEK_SUFFIXES = ["εται", "εσθαι", "ονται", "ομεν", "ετε",
                  "ων", "ος", "ου", "ῳ", "ον", "οι", "οις",
                  "ης", "ας", "ες", "α", "η", "ω", "ε", "ι"]

FRENCH_SUFFIXES = ["ements", "ement", "ions", "tions", "aient",
                   "iers", "ères", "tion", "ique", "isme", "iste",
                   "iste", "es", "er", "ir", "re", "s", "e"]

ENG_SUFFIXES = ["ingly", "tion", "ness", "ment", "able",
                "ed", "es", "er", "ly", "ing", "s"]

GERMAN_SUFFIXES = ["lichkeit", "ungen", "keit", "lich", "schaft",
                    "ungen", "ung", "heit", "haft", "lich", "isch",
                    "en", "es", "er", "et", "em", "et", "e", "n", "s"]

ARABIC_PREFIXES = ["وال", "بال", "كال", "فال", "ال", "و", "ف", "ب", "ك", "ل"]
ARABIC_SUFFIXES = ["تموهن", "تموها", "تكما", "كما", "هما", "هم",
                    "هن", "كم", "كن", "نا", "ها", "ون", "ين", "ات",
                    "وا", "تي", "تم", "تن", "ك", "ه", "ت", "ا", "ي", "ن"]


def _strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if not unicodedata.combining(c))


def lemmatize(token: str, lang: str) -> str:
    t = token.casefold() if lang != "lzh" else token
    if lang == "lat":
        bare = _strip_diacritics(t)
        for suf in LATIN_SUFFIXES:
            if bare.endswith(suf) and len(bare) > len(suf) + 2:
                return bare[: -len(suf)]
        return bare
    if lang == "grc":
        for suf in GREEK_SUFFIXES:
            if t.endswith(suf) and len(t) > len(suf) + 2:
                return t[: -len(suf)]
        return t
    if lang == "san":
        # devanagari ou IAST
        bare = _strip_diacritics(t)
        return bare.rstrip("aāḥṃ")
    if lang == "lzh":
        return t  # caractère-token : pas de lemmatisation
    if lang == "ara":
        # supprime un préfixe et un suffixe les plus longs
        for pre in ARABIC_PREFIXES:
            if t.startswith(pre) and len(t) > len(pre) + 2:
                t = t[len(pre):]
                break
        for suf in ARABIC_SUFFIXES:
            if t.endswith(suf) and len(t) > len(suf) + 2:
                t = t[: -len(suf)]
                break
        return t
    if lang == "fra":
        bare = _strip_diacritics(t)
        for suf in FRENCH_SUFFIXES:
            if bare.endswith(suf) and len(bare) > len(suf) + 2:
                return bare[: -len(suf)]
        return bare
    if lang == "deu":
        for suf in GERMAN_SUFFIXES:
            if t.endswith(suf) and len(t) > len(suf) + 2:
                return t[: -len(suf)]
        return t
    if lang == "eng":
        for suf in ENG_SUFFIXES:
            if t.endswith(suf) and len(t) > len(suf) + 2:
                return t[: -len(suf)]
        return t
    return t


# ----------------------------------------------------------------------------
# POS tagging très naïf (par classes lexicales)
# ----------------------------------------------------------------------------

CONJ = {"et", "ac", "que", "atque", "vel", "aut", "sed", "nam", "enim",
         "καί", "δέ", "ἀλλά", "γάρ", "οὖν",
         "and", "but", "or", "for", "nor", "so", "yet",
         "et", "mais", "ou", "donc", "or", "ni", "car",
         "und", "aber", "oder", "denn", "doch", "sondern",
         "च", "वा", "तु", "हि",
         "و", "أو", "لكن", "بل"}
PREP = {"in", "ad", "de", "ex", "cum", "per", "sine", "sub", "ante",
         "ἐν", "εἰς", "ἐκ", "πρός", "παρά", "διά", "ἐπί",
         "in", "of", "to", "from", "by", "with", "without", "for",
         "dans", "de", "à", "par", "pour", "avec", "sans",
         "in", "von", "zu", "bei", "mit", "ohne", "für", "auf",
         "في", "من", "إلى", "عن", "على", "ب", "ل"}
DET = {"is", "ea", "id", "hic", "haec", "hoc", "ille", "illa", "illud",
        "ὁ", "ἡ", "τό", "οἱ", "αἱ", "τά",
        "the", "a", "an", "this", "that", "these", "those",
        "le", "la", "les", "un", "une", "des",
        "der", "die", "das", "ein", "eine"}


def pos_tag(token: str, lemma: str, lang: str) -> str:
    t = token.casefold() if lang != "lzh" else token
    bare = _strip_diacritics(t)
    if bare in CONJ or t in CONJ:
        return "CONJ"
    if bare in PREP or t in PREP:
        return "PREP"
    if bare in DET or t in DET:
        return "DET"
    if lang == "lzh":
        return "CHAR"
    if t and t[0].isupper():
        return "PROPN"
    if any(ch.isdigit() for ch in t):
        return "NUM"
    return "X"  # unknown / content


# ----------------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------------

def process_fragment(frag: dict) -> list[dict]:
    lang = frag["lang"]
    sents = split_sentences(frag["text"], lang)
    out = []
    for si, sent in enumerate(sents):
        toks = tokenize(sent, lang)
        for ti, tok in enumerate(toks):
            lemma = lemmatize(tok, lang)
            pos = pos_tag(tok, lemma, lang)
            out.append({
                "frag_id": frag["frag_id"],
                "work_id": frag["work_id"],
                "lang": lang,
                "sentence_id": si,
                "token_id": ti,
                "surface": tok,
                "lemma": lemma,
                "pos": pos,
            })
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not CORPUS_DIR.exists():
        print(f"Corpus introuvable: {CORPUS_DIR}")
        return

    by_corpus = []
    total_sentences = 0
    total_tokens = 0
    total_unique_lemmas: set[str] = set()
    pos_counts: dict[str, int] = {}
    lang_stats: dict[str, dict] = {}

    for work_dir in sorted(CORPUS_DIR.iterdir()):
        if not work_dir.is_dir():
            continue
        frag_path = work_dir / "fragments.jsonl"
        if not frag_path.exists():
            continue

        all_tokens = []
        sentences = set()
        for line in frag_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            frag = json.loads(line)
            tokens = process_fragment(frag)
            all_tokens.extend(tokens)
            for t in tokens:
                sentences.add((t["frag_id"], t["sentence_id"]))

        out_path = OUT_DIR / f"{work_dir.name}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for t in all_tokens:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")

        n_sents = len(sentences)
        n_tokens = len(all_tokens)
        unique_lemmas = {t["lemma"] for t in all_tokens}
        total_sentences += n_sents
        total_tokens += n_tokens
        total_unique_lemmas |= unique_lemmas

        for t in all_tokens:
            pos_counts[t["pos"]] = pos_counts.get(t["pos"], 0) + 1

        lang = all_tokens[0]["lang"] if all_tokens else "?"
        lang_stats.setdefault(lang, {"works": 0, "sentences": 0, "tokens": 0,
                                       "unique_lemmas": set()})
        lang_stats[lang]["works"] += 1
        lang_stats[lang]["sentences"] += n_sents
        lang_stats[lang]["tokens"] += n_tokens
        lang_stats[lang]["unique_lemmas"] |= unique_lemmas

        by_corpus.append({
            "work_id": work_dir.name,
            "lang": lang,
            "n_sentences": n_sents,
            "n_tokens": n_tokens,
            "n_unique_lemmas": len(unique_lemmas),
            "ttr": round(len(unique_lemmas) / n_tokens, 3) if n_tokens else 0.0,
            "output": str(out_path.relative_to(ROOT)),
        })

    lang_summary = {}
    for lg, s in lang_stats.items():
        lang_summary[lg] = {
            "works": s["works"],
            "sentences": s["sentences"],
            "tokens": s["tokens"],
            "unique_lemmas": len(s["unique_lemmas"]),
            "ttr": round(len(s["unique_lemmas"]) / s["tokens"], 3)
                    if s["tokens"] else 0.0,
        }

    summary = {
        "version": "v142",
        "context": ("§142 — Pipeline tokenisation/lemmatisation multilingue "
                    "(8 langues, fallback déterministe sans dépendance lourde)"),
        "n_works": len(by_corpus),
        "n_sentences_total": total_sentences,
        "n_tokens_total": total_tokens,
        "n_unique_lemmas_total": len(total_unique_lemmas),
        "ttr_global": round(len(total_unique_lemmas) / total_tokens, 3)
                       if total_tokens else 0.0,
        "pos_distribution": dict(sorted(pos_counts.items(),
                                          key=lambda x: -x[1])),
        "by_language": lang_summary,
        "by_corpus": by_corpus,
        "approche": ("split phrases par regex spécifiques par langue "
                     "(point latin, point haut grec, daṇḍa sanskrit, "
                     "句号 chinois, etc.) ; tokenisation par classes "
                     "Unicode ; lemmatisation par stripping de suffixes/"
                     "préfixes spécifiques ; POS heuristique sur listes "
                     "fermées (CONJ/PREP/DET/PROPN/NUM/X)"),
        "limitations": [
            "Lemmatisation = stripping naïf — pas de désambiguïsation morpho",
            "POS tag X (content) ne distingue pas N/V/ADJ",
            "Sandhi sanskrit non décomposé (mots agglutinés gardés tels quels)",
            "Pas de gestion de l'ambiguïté graphique grec ↔ latin pour les "
            "translittérations (acceptable car corpus gardé en script natif)",
        ],
    }
    out_summary = ROOT / "research" / "nipada" / "falsification" / "nipada_v142_tokenize.json"
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(f"§142 — Tokenisation/lemmatisation multilingue")
    print(f"  Œuvres            : {len(by_corpus)}")
    print(f"  Phrases           : {total_sentences}")
    print(f"  Tokens            : {total_tokens}")
    print(f"  Lemmes uniques    : {len(total_unique_lemmas)}")
    print(f"  TTR global        : {summary['ttr_global']}")
    print(f"  Langues couvertes : {sorted(lang_summary.keys())}")
    print(f"→ {out_summary.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

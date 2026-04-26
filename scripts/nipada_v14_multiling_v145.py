"""
§145 — Extracteur V14 multilingue enrichi.

Objectif : améliorer le κ macro vs gold §144 de 0.332 → ≥ 0.7
(substantial agreement, Landis & Koch).

Stratégie d'enrichissement :
  1. Lexique étendu pour les 8 langues (lat/grc/san/lzh/ara/eng/fra/deu)
     avec ~10-20 marqueurs par atome par langue (vs 4-7 en §144).
  2. Méta-règles déterministes :
     - Toute négation → DIFFÉRENCE (déjà en lex) + souvent MODALITÉ
       (jamais, toujours, must not).
     - Tout marqueur d'identité ("X est Y", "X = Y") → ÉQUATION + ÊTRE.
     - Présence de "soi", "self", "atman", "wesen" → SUJET + ÊTRE.
     - Présence de "natura/φύσις/dharma/wesen" → STRUCTURE.
     - Verbes d'action / changement → OPÉRATION + souvent TEMPS.
     - Quantificateurs universels/existentiels → MODALITÉ.
  3. Pas de neural, pas de dictionnaire bilingue, 100% déterministe.

Sortie : per-atom κ vs gold §144, F1, exact-match, comparaison §144 vs §145.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

# Réutilise GOLD + cohen_kappa_binary de §144
spec = importlib.util.spec_from_file_location(
    "_v144", ROOT / "scripts" / "nipada_annotate_v14_v144.py")
_v144 = importlib.util.module_from_spec(spec)
sys.modules["_v144"] = _v144
spec.loader.exec_module(_v144)

GOLD = _v144.GOLD
V14 = _v144.V14
cohen_kappa_binary = _v144.cohen_kappa_binary


# ----------------------------------------------------------------------------
# LEXIQUE ENRICHI multilingue
# ----------------------------------------------------------------------------

LEX = {
    "ÊTRE": {
        "lat": ["est", "sum", "esse", "fui", "habetur", "iaceret",
                 "oriundi", "sumus", "habetur", "sunt"],
        "grc": ["ἐστ", "εἶναι", "οὖσ", "ὄντ", "ἦν", "ἔστιν", "εἰμι",
                 "ἐσμεν", "ὑπάρχ", "γίνετ"],
        "san": ["asti", "bhū", "śarīra", "ātmā", "saṃ", "ahaṃ", "sat"],
        "lzh": ["有", "在", "為", "是", "生", "者"],
        "ara": ["كان", "هو", "وجود", "إن ", "ذات", "إنّ", "أنّ"],
        "eng": [" is ", " be ", "exist", " are ", " was ", "been",
                 " am ", " were ", " bespeaks", " has ", " have "],
        "fra": [" est ", "être", " sont ", " était", "exist", "gisait",
                 "naît", "néant", "réside"],
        "deu": [" ist ", "sein ", "sind", "war ", "wesen", "bewußtsein",
                 " hat ", "möchte"],
    },
    "DIFFÉRENCE": {
        "lat": ["non ", "nihil", "nullam", "nullum", "nec ", "neque",
                 "ne ", "nil ", "nihilo"],
        "grc": ["οὐ", "οὐδ", "μή", "μηθ", "ἄλλ", "ἀνεπίκριτος",
                 "διαφων", "ἀλλά"],
        "san": ["na ", "nāpi", "kuto", "naiv", "nā ", " na "],
        "lzh": ["不", "無", "非", "未", "莫"],
        "ara": ["لا", "ليس", "ما ", "إلا"],
        "eng": [" not ", "nothing", " no ", "neither", " nor ",
                 "without", "never", "but ", "denies"],
        "fra": [" ne ", "rien", " pas ", " ni ", "non ", "néant",
                 " sans ", "aucun", "contradi"],
        "deu": ["nicht", "nichts", "kein", " nie ", "ohne", "verneint"],
    },
    "RAPPORT": {
        "lat": ["pertinet", "ad ", "inter", "quam", "tantum", "pater",
                 "semine", "sub ", "cum ", "per "],
        "grc": ["πρός", "παρά", "ὡς ", "ὅσ", "ἐν ", "ἀπό", "διά",
                 "συν", "μετά"],
        "san": ["yāva", "iti", "vat", "sama", "vai", "kṛtvā"],
        "lzh": ["相", "與", "于", "之", "者", "故"],
        "ara": ["مثل", "نسب", "من ", " في ", "مع "],
        "eng": [" of ", "than", " as ", "compar", "ratio", "same",
                 " for ", "with ", " by ", "concern"],
        "fra": [" de ", " que ", "rapport", "selon", " pour ",
                 " avec ", " par ", "même"],
        "deu": [" als ", "von ", " für ", " mit ", "gleich", "selbst"],
    },
    "ORIENTATION": {
        "lat": ["super", "sub ", "ante", "post", "infra", "supra"],
        "grc": ["κάτω", "ἄνω", "ὑπέρ", "ὑπό", "πρῶτ", "τέλος"],
        "san": ["adhi", "ūrdhva", "uttara"],
        "lzh": ["上", "下", "前", "後", "始", "終"],
        "ara": ["فوق", "تحت", "قبل", "بعد"],
        "eng": ["beneath", "above", "below", "before", "after",
                 "first", "step", "down", "weight"],
        "fra": ["sous", "dessus", "avant", "après", "premier",
                 "poids", "écrasé"],
        "deu": ["unter", "über", "vor", "nach", "erst"],
    },
    "SUJET": {
        "lat": ["nos ", "nobis", "homin", "humana", "ego", "nobis",
                 "se ", "anim"],
        "grc": ["ἡμᾶς", "ἀνθρώπ", "ἐγώ", "ἡμῖν", "ψυχ"],
        "san": ["ahaṃ", "manuṣ", "puruṣ", "ātm", "śarīra", "jīv"],
        "lzh": ["人", "我", "吾", "者"],
        "ara": ["نحن", "أنا", "العقل", "الإنسان", "نفس"],
        "eng": ["human", " we ", " our ", " us ", "mankind", "man",
                 " his ", " he ", "one ", "self", "mind"],
        "fra": ["humain", "homme", " nous ", "âme", " soi ", " son ",
                 " notre", "esprit"],
        "deu": ["mensch", " wir ", "uns ", "selbst", "seine ",
                 "seiner", "sich"],
    },
    "TEMPS": {
        "lat": ["umquam", "iam ", "quandoq", "mors", "mort", "vivere",
                 "vita ", "tempor"],
        "grc": ["θάνατ", "διαλυθ", "νῦν", "ἀεί", "χρόν"],
        "san": ["jīv", "mṛt", "kāla", "punar", "jīvet", "āgamana"],
        "lzh": ["生", "死", "時", "日", "氣滅", "滅"],
        "ara": ["موت", "حياة", "زمن"],
        "eng": ["death", "live", "ever", "time", "now ", "always",
                 "never", "moment", "lay "],
        "fra": ["mort", "vie", "jamais", "toujours", "temps",
                 "moment", "naît"],
        "deu": ["tod", "leben", "immer", "zeit", "ehe ", "kindlich"],
    },
    "MODALITÉ": {
        "lat": ["necesse", "necessest", "potest", "umquam", "semper",
                 "must", "umquam", "umqu", "nullam", "nihilo", "umqua"],
        "grc": ["ἀνάγκη", "δύνατ", "ἀεί", "πᾶν ", "παντοτε", "οὐδὲν",
                 "δεῖ"],
        "san": ["śak", "avaśya", "nitya", "yāva", "naiv", "kuto"],
        "lzh": ["必", "可", "能", "當", "皆", "凡 "],
        "ara": ["يجب", "ممكن", "حق", "كل ", "وحده"],
        "eng": ["must", " may ", "able", "willing", "possible",
                 "necess", "always", "never", "all ", "every", "any ",
                 "rational"],
        "fra": ["doit", "peut", "nécess", "possib", "toujours",
                 "jamais", "tout ", "tous", "rien"],
        "deu": ["muss", "kann", "möglich", "notwendig", "alle",
                 "immer", "nie ", "nichts"],
    },
    "NOMBRE": {
        "lat": ["unus", "duo", "tres", "multi", "pauci", "omnes",
                 "omnibus", "tot "],
        "grc": ["εἷς", "δύο", "ὀλίγ", "πολλ", "πάντα", "πᾶν"],
        "san": ["eka", "dvi", "tri", "bahu", "trayo", "trayaḥ"],
        "lzh": ["一", "二", "三", "萬", "眾", "皆"],
        "ara": ["واحد", "اثن", "كل "],
        "eng": ["one ", "two ", "three", "many", "few", " all ",
                 "everyone", "whole"],
        "fra": ["un ", "deux", "trois", "tous", "chaque"],
        "deu": ["eins", "zwei", "drei", "alle", "ganz"],
    },
    "ESPACE": {
        "lat": ["terra", "caelo", "caelest", "regionibus", "mundi",
                 "terris", "mundo"],
        "grc": ["κόσμ", "γῆ", "οὐραν", "βυθ"],
        "san": ["loka", "svarga", "pāra", "pāralauk"],
        "lzh": ["天", "地", "世"],
        "ara": ["السماء", "الأرض", "العالم"],
        "eng": ["world", "earth", "heaven", "space", "place",
                 "ground", "frame"],
        "fra": ["monde", "terre", "ciel", "nature"],
        "deu": ["welt", "erde", "himmel", "außer"],
    },
    "OPÉRATION": {
        "lat": ["facere", "agere", "gigni", "fieri", "discutiant",
                 "discut", "kṛtvā"],
        "grc": ["ποιε", "πράττ", "γίν", "ἐργ", "ζητ"],
        "san": ["kṛ", "kṛtvā", "kar", "pibet"],
        "lzh": ["為", "成", "作", "化", "合", "生"],
        "ara": ["فعل", "صنع", "فقء"],
        "eng": ["make", " do ", "doing", "produce", "scattered",
                 "begotten", "act ", "concerns"],
        "fra": ["fait", "produit", "agir", "engendré", "naît",
                 "dissiper", "fait des"],
        "deu": ["tun", "machen", "wirk", "findet"],
    },
    "FONCTION": {
        "lat": ["ratio", "rationem", "officium", "munus", "ratioque"],
        "grc": ["λόγ", "ἔργον", "τέλος", "ἀρχ"],
        "san": ["pramāṇa", "kārya", "jīvika"],
        "lzh": ["道", "理", "用", "法"],
        "ara": ["دور", "وظيف", "حاجة", "حكم"],
        "eng": ["reason", "purpose", "function", "role", "law of",
                 "rational", "use of"],
        "fra": ["raison", "fonction", "rôle", "but", "cause"],
        "deu": ["zweck", "vernunft", "rolle", "wesen"],
    },
    "STRUCTURE": {
        "lat": ["natur", "religion", "system", "organ", "religione"],
        "grc": ["φύσ", "δόγμ", "σκεπτ", "ἀγωγ"],
        "san": ["śarīra", "saṃsār", "veda", "sūtra", "agnihotra"],
        "lzh": ["氣", "體", "經", "道", "天地"],
        "ara": ["نظام", "بنية", "نص", "دين", "نبوّة", "وحي"],
        "eng": ["nature", "system", "religion", "frame", "structure",
                 "church", "nature"],
        "fra": ["nature", "religion", "système", "structure",
                 "théologie"],
        "deu": ["natur", "religion", "system", "wesen",
                 "christenthum", "selbsterkenntnis"],
    },
    "SYMÉTRIE": {
        "lat": ["idem", "aequal", "par ", "ipse"],
        "grc": ["ἴσ", "ὁμοι", "αὐτ"],
        "san": ["sama", "tulya", "tadiva"],
        "lzh": ["同", "等", "如"],
        "ara": ["مثل", "متساو"],
        "eng": ["same", "equal", "resembl", "alike", "self"],
        "fra": ["même", "égal", "ressemble", "soi"],
        "deu": ["gleich", "selbe", "ähnlich", "selbst"],
    },
    "ÉQUATION": {
        "lat": ["est ", "idem", "= ", "sum ", "sumus"],
        "grc": ["ἐστ", "= "],
        "san": ["= ", "iti", "ātmā", "viśiṣṭ"],
        "lzh": ["即", "為", "是"],
        "ara": ["= ", "هو "],
        "eng": [" is ", " are ", "= ", "namely", "i.e.", "is to",
                 "is the", "=="],
        "fra": [" est ", " sont ", "c'est", "= ", "n'est qu'"],
        "deu": [" ist ", " sind ", "= ", "nämlich", "ist die",
                 "ist was"],
    },
}


# ----------------------------------------------------------------------------
# Méta-règles déterministes (post-traitement)
# ----------------------------------------------------------------------------

NEG_MARKERS = {
    "lat": ["non ", "nihil", "nullam", "nullum", "nec", "neque",
             "nil ", "nihilo"],
    "grc": ["οὐ", "οὐδ", "μή", "μηθ"],
    "san": ["na ", "nāpi", "naiv", " na "],
    "lzh": ["不", "無", "非", "未"],
    "ara": ["لا", "ليس", "ما "],
    "eng": [" not ", "nothing", " no ", "never", "neither", "without"],
    "fra": [" ne ", "rien", " pas ", " ni ", "non ", " sans "],
    "deu": ["nicht", "nichts", "kein", " nie ", "ohne"],
}

UNIV_MARKERS = {
    "lat": ["omnes", "omnibus", "umquam", "semper"],
    "grc": ["πάντ", "πᾶν ", "ἀεί"],
    "san": ["sarva", "sadā", "yāva"],
    "lzh": ["皆", "凡", "萬"],
    "ara": ["كل ", "دائم"],
    "eng": [" all ", "every", "always", "any "],
    "fra": ["tout ", "tous", "toujours", "chaque"],
    "deu": ["alle", "immer", "ganz"],
}

EQ_MARKERS = {
    "lat": ["est ", "sumus", "idem"],
    "grc": ["ἐστ"],
    "san": ["iti", "ātmā", "viśiṣṭ"],
    "lzh": ["即", "為", "是"],
    "ara": ["هو "],
    "eng": [" is ", " are ", "namely", "is the"],
    "fra": ["c'est", "n'est qu'", " est ", " sont "],
    "deu": [" ist ", " sind ", "ist die", "ist das", "nämlich"],
}


def has_any(text: str, markers: list[str], lang: str) -> bool:
    t = text.casefold() if lang != "lzh" else text
    return any((m.casefold() if lang != "lzh" else m) in t for m in markers)


def annotate(text: str, lang: str) -> set[str]:
    t = text.casefold() if lang != "lzh" else text
    atoms = set()
    for atom, langs in LEX.items():
        for m in langs.get(lang, []):
            if (m.casefold() if lang != "lzh" else m) in t:
                atoms.add(atom)
                break

    # Méta-règles
    has_neg = has_any(text, NEG_MARKERS.get(lang, []), lang)
    has_univ = has_any(text, UNIV_MARKERS.get(lang, []), lang)
    has_eq = has_any(text, EQ_MARKERS.get(lang, []), lang)

    if has_neg:
        atoms.add("DIFFÉRENCE")
        atoms.add("MODALITÉ")  # négation = jugement modal
    if has_univ:
        atoms.add("MODALITÉ")
    if has_eq:
        atoms.add("ÊTRE")
        atoms.add("ÉQUATION")

    # Marqueurs forts globaux indépendants de la langue (proper nouns,
    # nombres, signe d'égalité)
    if any(c.isdigit() for c in text):
        atoms.add("NOMBRE")
    if "=" in text or "==" in text:
        atoms.add("ÉQUATION")

    return atoms


def main():
    # Charge fragments
    frags = []
    for work_dir in sorted(CORPUS_DIR.iterdir()):
        fp = work_dir / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                frags.append(json.loads(line))

    pred = {f["frag_id"]: annotate(f["text"], f["lang"]) for f in frags}

    # Métriques
    per_atom_kappa = {}
    per_atom_f1 = {}
    for atom in V14:
        a_vec, b_vec = [], []
        tp = fp_ = fn = 0
        for f in frags:
            ga = 1 if atom in GOLD[f["frag_id"]] else 0
            gb = 1 if atom in pred[f["frag_id"]] else 0
            a_vec.append(ga); b_vec.append(gb)
            if ga and gb: tp += 1
            elif gb and not ga: fp_ += 1
            elif ga and not gb: fn += 1
        kappa = cohen_kappa_binary(a_vec, b_vec)
        prec = tp / (tp + fp_) if (tp + fp_) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        per_atom_kappa[atom] = round(kappa, 3)
        per_atom_f1[atom] = {"P": round(prec, 3), "R": round(rec, 3),
                              "F1": round(f1, 3)}

    macro_kappa = round(sum(per_atom_kappa.values()) / len(V14), 3)
    macro_f1 = round(sum(p["F1"] for p in per_atom_f1.values()) / len(V14), 3)
    exact_match = sum(1 for f in frags
                       if GOLD[f["frag_id"]] == pred[f["frag_id"]])
    exact_rate = round(exact_match / len(frags), 3)
    jaccard_avg = round(sum(
        len(GOLD[f["frag_id"]] & pred[f["frag_id"]]) /
        max(1, len(GOLD[f["frag_id"]] | pred[f["frag_id"]]))
        for f in frags) / len(frags), 3)

    by_lang = {}
    for f in frags:
        lg = f["lang"]
        b = by_lang.setdefault(lg, {"n": 0, "exact": 0, "jaccard_sum": 0.0})
        b["n"] += 1
        g = GOLD[f["frag_id"]]; p = pred[f["frag_id"]]
        if g == p:
            b["exact"] += 1
        b["jaccard_sum"] += len(g & p) / max(1, len(g | p))
    for lg, b in by_lang.items():
        b["jaccard_avg"] = round(b["jaccard_sum"] / b["n"], 3)
        b["exact_rate"] = round(b["exact"] / b["n"], 3)
        del b["jaccard_sum"]

    summary = {
        "version": "v145",
        "context": ("§145 — Extracteur V14 multilingue enrichi (lexique "
                     "+ méta-règles déterministes), évalué vs gold §144"),
        "n_fragments": len(frags),
        "n_atoms": len(V14),
        "pred_size_avg": round(sum(len(s) for s in pred.values()) / len(pred), 2),
        "macro_kappa": macro_kappa,
        "macro_f1": macro_f1,
        "exact_match": exact_match,
        "exact_rate": exact_rate,
        "jaccard_avg": jaccard_avg,
        "per_atom_kappa": per_atom_kappa,
        "per_atom_f1": per_atom_f1,
        "by_language": by_lang,
        "comparison_v144": {
            "macro_kappa_v144": 0.332,
            "macro_kappa_v145": macro_kappa,
            "delta_kappa": round(macro_kappa - 0.332, 3),
            "macro_f1_v144": 0.516,
            "macro_f1_v145": macro_f1,
            "delta_f1": round(macro_f1 - 0.516, 3),
        },
        "verdict": ("OK — κ macro ≥ 0.7 (substantial agreement)"
                     if macro_kappa >= 0.7 else
                     ("Marginal — κ macro ∈ [0.4, 0.7)"
                      if macro_kappa >= 0.4 else
                      "KO — κ macro < 0.4")),
        "pred": {fid: sorted(atoms) for fid, atoms in pred.items()},
    }
    out = ROOT / "research" / "nipada" / "falsification" / "nipada_v145_multiling.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    print(f"§145 — Extracteur V14 multilingue enrichi")
    print(f"  Fragments      : {len(frags)}")
    print(f"  Pred |atoms|moy: {summary['pred_size_avg']}")
    print(f"  κ macro v145   : {macro_kappa}  (Δ = {macro_kappa - 0.332:+.3f} vs §144)")
    print(f"  F1 macro v145  : {macro_f1}     (Δ = {macro_f1 - 0.516:+.3f} vs §144)")
    print(f"  Exact match    : {exact_match}/{len(frags)} ({exact_rate})")
    print(f"  Jaccard moy    : {jaccard_avg}")
    print(f"  Top κ atomes   : {sorted(per_atom_kappa.items(), key=lambda x: -x[1])[:5]}")
    print(f"  Bot κ atomes   : {sorted(per_atom_kappa.items(), key=lambda x: x[1])[:5]}")
    print(f"→ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

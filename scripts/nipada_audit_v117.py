#!/usr/bin/env python3
"""
§117 — Bug-fix regex IT et audit des labels du corpus §94/§100
================================================================

1. Bug-fix : `_Q_WH_IT` et `_Q_WH_PT` matchent partiellement les mots
   `qualità`, `chiamare`, `comefare`, etc. (pas de frontière mot \b).
   On corrige en ajoutant `\b` après chaque mot-clé interrogatif.

2. Audit : pour chaque (texte, label) du corpus §100, on demande
   au classifier baseline + regex de prédire ; on liste les phrases dont
   la prédiction n'est pas le label, classées par sévérité.

Sortie : research/nipada/falsification/nipada_v117_audit_report.json
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _import(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__name__ = name
    spec.loader.exec_module(mod)
    return mod


_v100 = _import("v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py")


# ══════════════════════════════════════════════════════════════════════════════
# 1. Regex corrigées avec \b
# ══════════════════════════════════════════════════════════════════════════════

_Q_WH_IT_BUG     = re.compile(r'^\s*(che\s+cosa|cosa\s|perché|come\s|quando\s|dove\s|chi\s|quale|quali|esiste|è\s+possibile|puoi\s|può\s)', re.IGNORECASE)
_Q_WH_IT_FIXED   = re.compile(r'^\s*(che\s+cosa\b|cosa\b|perché\b|come\b|quando\b|dove\b|chi\b|quale\b|quali\b|esiste\b|è\s+possibile|puoi\b|può\b)', re.IGNORECASE)
_Q_WH_PT_BUG     = re.compile(r'^\s*(o\s+que|porque|por\s+que|como\s|quando\s|onde\s|quem\s|qual|quais|existe|é\s+possível|pode\s)', re.IGNORECASE)
_Q_WH_PT_FIXED   = re.compile(r'^\s*(o\s+que\b|porque\b|por\s+que\b|como\b|quando\b|onde\b|quem\b|qual\b|quais\b|existe\b|é\s+possível|pode\b)', re.IGNORECASE)


def _measure_bug_impact(corpus: dict) -> dict:
    """Pour chaque langue, compte les phrases où la regex matche par erreur (false-positive
    sur un type non-question)."""
    impact = {"it": {"bug_only": [], "fixed_only": [], "both": [], "neither_unchanged": 0},
              "pt": {"bug_only": [], "fixed_only": [], "both": [], "neither_unchanged": 0}}
    for t, by_lang in corpus.items():
        for la in ("it", "pt"):
            phrases = by_lang.get(la, [])
            for p in phrases:
                if la == "it":
                    bug   = bool(_Q_WH_IT_BUG.search(p))
                    fixed = bool(_Q_WH_IT_FIXED.search(p))
                else:
                    bug   = bool(_Q_WH_PT_BUG.search(p))
                    fixed = bool(_Q_WH_PT_FIXED.search(p))
                if bug and not fixed:
                    impact[la]["bug_only"].append({"text": p, "type": t})
                elif fixed and not bug:
                    impact[la]["fixed_only"].append({"text": p, "type": t})
                elif bug and fixed:
                    impact[la]["both"].append({"text": p, "type": t})
                else:
                    impact[la]["neither_unchanged"] += 1
    return impact


def main() -> None:
    print("═" * 78)
    print("  §117 — Bug-fix regex IT/PT + audit labels corpus §100")
    print("═" * 78)

    corpus = _v100.merge_corpus_v100()

    # 1. Mesure de l'impact du bug
    print("\n  ── Impact bug regex IT/PT ──")
    impact = _measure_bug_impact(corpus)
    for la in ("it", "pt"):
        n_bug_only = len(impact[la]["bug_only"])
        n_fixed_only = len(impact[la]["fixed_only"])
        print(f"  {la} : bug_FP={n_bug_only}  bug_FN_evite={n_fixed_only}  identiques={len(impact[la]['both'])}  inchanges={impact[la]['neither_unchanged']}")
        if n_bug_only:
            print(f"    Faux-positifs supprimés par le fix :")
            for ex in impact[la]["bug_only"][:5]:
                print(f"      [{ex['type']:<14s}] « {ex['text'][:70]} »")

    # 2. Audit : entraîner classifieur §100 et lister erreurs
    print("\n  ── Audit erreurs classifieur §100 ──")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    X, feats_syn, feats_lang, y, langs, strata, texts = _v100.build_dataset_v100(model, corpus)

    # Train sur tout, prédire sur tout : audit IN-SAMPLE des labels suspects.
    # (on cherche les phrases dont la marge est faible OU la pred ≠ label)
    clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf.fit(X, y)
    proba = clf.predict_proba(X)
    pred = proba.argmax(axis=1)
    margin = np.sort(proba, axis=1)[:, -1] - np.sort(proba, axis=1)[:, -2]

    errors = []
    for i in range(len(texts)):
        if pred[i] != y[i]:
            errors.append({
                "text":      texts[i],
                "lang":      langs[i],
                "label":     _v100.IDX2TYPE[int(y[i])],
                "predicted": _v100.IDX2TYPE[int(pred[i])],
                "margin":    float(margin[i]),
                "p_label":   float(proba[i, y[i]]),
                "p_pred":    float(proba[i, pred[i]]),
            })
    errors.sort(key=lambda e: -e["margin"])
    print(f"    Erreurs in-sample (potentielles erreurs de label) : {len(errors)}")
    for e in errors[:10]:
        print(f"      [{e['lang']}] {e['label']:<14s} → {e['predicted']:<14s}  "
              f"margin={e['margin']:.2f}  « {e['text'][:60]} »")

    # 3. Suspects de label (margin > 0.4 → forte confiance que le label est faux)
    suspects = [e for e in errors if e["margin"] > 0.4]
    print(f"\n  ── Suspects forts (margin>0.4) : {len(suspects)} ──")

    out = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v117_audit_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version": "§117",
        "regex_bug_impact": {
            "it": {"bug_FP_supprimes": len(impact["it"]["bug_only"]),
                   "fixed_only":         len(impact["it"]["fixed_only"]),
                   "exemples_FP":        impact["it"]["bug_only"][:10]},
            "pt": {"bug_FP_supprimes": len(impact["pt"]["bug_only"]),
                   "fixed_only":         len(impact["pt"]["fixed_only"]),
                   "exemples_FP":        impact["pt"]["bug_only"][:10]},
        },
        "regex_fixed_patterns": {
            "_Q_WH_IT_FIXED": _Q_WH_IT_FIXED.pattern,
            "_Q_WH_PT_FIXED": _Q_WH_PT_FIXED.pattern,
        },
        "audit_labels": {
            "n_errors_in_sample": len(errors),
            "n_suspects_strong":  len(suspects),
            "errors_top20":       errors[:20],
        },
    }, ensure_ascii=False, indent=2, cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

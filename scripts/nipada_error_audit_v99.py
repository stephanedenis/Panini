#!/usr/bin/env python3
"""
§99 — Audit qualitatif des erreurs résiduelles [A]
====================================================
Plan §98 : la CV 5-fold sur 910 phrases atteint 96.7 % → ~30 erreurs.
Question : ces erreurs sont-elles des **vraies erreurs du modèle** (limites
empiriques) ou des **ambiguïtés intrinsèques** (le label nipada lui-même
est discutable) ?

Méthode :
  1. Reproduire CV 5-fold du §98 expérience [A] avec le même seed
  2. Extraire chaque phrase mal classée :
     - texte original
     - langue
     - label vrai
     - label prédit
     - probabilités top-3 (pour mesurer la confiance)
     - marge = p(vrai) - p(prédit)
  3. Classer en 3 catégories selon la marge :
     - HARD ERROR (marge < -0.3) : modèle confiant dans la mauvaise classe
     - SOFT ERROR (-0.3 ≤ marge < 0)  : modèle hésitant
     - AMBIGUOUS  (|p_top1 - p_top2| < 0.1) : multi-classe plausible

Output → research/nipada/falsification/nipada_v99_error_audit.json
        + tableau imprimé des 30 erreurs classées
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

# Charger §98 (qui charge §94)
_spec98 = importlib.util.spec_from_file_location(
    "v98", REPO_ROOT / "scripts" / "nipada_crosslingual_v98.py"
)
_v98 = importlib.util.module_from_spec(_spec98)
_v98.__name__ = "v98"
_spec98.loader.exec_module(_v98)  # type: ignore[attr-defined]

merge_corpus = _v98.merge_corpus
build_dataset = _v98.build_dataset
TYPES = _v98.TYPES
ALL_LANGS = _v98.ALL_LANGS
TYPE2IDX = _v98.TYPE2IDX
IDX2TYPE = _v98.IDX2TYPE
LANG2IDX = _v98.LANG2IDX
_NpEncoder = _v98._NpEncoder
_to_native = _v98._to_native

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v99_error_audit.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def main() -> None:
    W = 78
    print("═" * W)
    print("  §99 — Audit qualitatif des erreurs résiduelles (CV 5-fold sur 910)")
    print("═" * W)

    model = SentenceTransformer(MODEL_NAME)
    corpus = merge_corpus()
    X, feats_syn, feats_lang, y, langs, strata, texts = build_dataset(model, corpus)
    Xc = np.hstack([X, feats_syn, feats_lang])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    splits = list(skf.split(Xc, strata))

    errors = []  # liste de dicts
    n_total = 0
    n_correct = 0

    for fold_idx, (tr, te) in enumerate(splits):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(Xc[tr], y[tr])
        proba = clf.predict_proba(Xc[te])
        preds = proba.argmax(axis=1)

        for i_local, i_global in enumerate(te):
            n_total += 1
            true_i = int(y[i_global])
            pred_i = int(preds[i_local])
            if pred_i == true_i:
                n_correct += 1
                continue
            p_sorted_idx = proba[i_local].argsort()[::-1]
            top3 = [(IDX2TYPE[int(j)], float(proba[i_local, j])) for j in p_sorted_idx[:3]]
            p_true = float(proba[i_local, true_i])
            p_pred = float(proba[i_local, pred_i])
            margin = p_true - p_pred  # négatif puisqu'on s'est trompé
            top1_top2_gap = top3[0][1] - top3[1][1]

            # Catégorisation
            if top1_top2_gap < 0.1:
                category = "AMBIGUOUS"
            elif margin < -0.3:
                category = "HARD"
            else:
                category = "SOFT"

            errors.append({
                "fold": fold_idx,
                "lang": str(langs[i_global]),
                "true": IDX2TYPE[true_i],
                "pred": IDX2TYPE[pred_i],
                "text": texts[i_global],
                "p_true": p_true,
                "p_pred": p_pred,
                "margin": margin,
                "top1_top2_gap": top1_top2_gap,
                "top3": top3,
                "category": category,
            })

    accuracy = n_correct / n_total
    print(f"\n  CV 5-fold accuracy globale : {accuracy:.1%}  ({n_correct}/{n_total})")
    print(f"  Erreurs résiduelles : {len(errors)}")

    # Statistiques par catégorie
    cats = {"HARD": 0, "SOFT": 0, "AMBIGUOUS": 0}
    for e in errors:
        cats[e["category"]] += 1
    print(f"\n  Catégorisation des {len(errors)} erreurs :")
    for c, n in cats.items():
        print(f"    {c:<10s}{n:>4d}  ({n/len(errors)*100:.1f}%)")

    # Statistiques par paire (true → pred)
    print("\n  Top confusions (true → pred) :")
    pairs: dict[tuple[str, str], int] = {}
    for e in errors:
        k = (e["true"], e["pred"])
        pairs[k] = pairs.get(k, 0) + 1
    for (t, p), n in sorted(pairs.items(), key=lambda x: -x[1])[:8]:
        print(f"    {t:<14s} → {p:<14s}  ×{n}")

    # Statistiques par langue
    print("\n  Erreurs par langue :")
    by_lang: dict[str, int] = {}
    for e in errors:
        by_lang[e["lang"]] = by_lang.get(e["lang"], 0) + 1
    for la in ALL_LANGS:
        n = by_lang.get(la, 0)
        if n > 0:
            print(f"    {la:<6s}{n:>4d}")

    # Tableau détaillé des erreurs (triées par catégorie puis margin)
    cat_order = {"HARD": 0, "AMBIGUOUS": 1, "SOFT": 2}
    errors_sorted = sorted(errors, key=lambda e: (cat_order[e["category"]], e["margin"]))

    print("\n" + "═" * W)
    print(f"  TABLEAU DES {len(errors)} ERREURS (triées par sévérité)")
    print("═" * W)
    for i, e in enumerate(errors_sorted, 1):
        text = e["text"]
        if len(text) > 70:
            text = text[:67] + "…"
        print(f"\n  [{i:2d}] {e['category']:<10s} {e['lang']}  "
              f"{e['true']:<14s} → {e['pred']:<14s}  "
              f"p_true={e['p_true']:.2f}  p_pred={e['p_pred']:.2f}  margin={e['margin']:+.2f}")
        print(f"       \"{text}\"")
        top3_str = "  ".join(f"{t}={p:.2f}" for t, p in e["top3"])
        print(f"       top3: {top3_str}")

    out = {
        "benchmark": "§99 audit qualitatif des erreurs résiduelles CV 5-fold sur 910 phrases",
        "model": MODEL_NAME,
        "n_total": n_total,
        "n_correct": n_correct,
        "accuracy": accuracy,
        "n_errors": len(errors),
        "categorization": cats,
        "top_confusions": [{"true": t, "pred": p, "count": n}
                           for (t, p), n in sorted(pairs.items(), key=lambda x: -x[1])],
        "errors_by_lang": by_lang,
        "errors": errors_sorted,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(_to_native(out), f, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"\n  Résultats → {OUTPUT}")
    print("═" * W)


if __name__ == "__main__":
    main()

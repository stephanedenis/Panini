#!/usr/bin/env python3
"""
§119 — Borne supérieure empirique
==================================================

Hypothèse : les 16 erreurs in-sample identifiées en §117 sont des cas
intrinsèquement ambigus (margin<0.4) qui plafonnent le classifier.
En les retirant, on devrait converger vers ≥99 % CV-5.

Méthode
-------
1. Refaire l'audit §117 (in-sample erreurs).
2. Retirer ces phrases du corpus.
3. CV-5 stratifié sur le corpus nettoyé.
4. Comparer au baseline §100 (96.63 %).

Sortie : research/nipada/falsification/nipada_v119_upper_bound_report.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _import(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_v100 = _import("v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py")


def main() -> None:
    print("═" * 78)
    print("  §119 — Borne supérieure empirique (retrait cas ambigus)")
    print("═" * 78)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    corpus = _v100.merge_corpus_v100()
    X, feats_syn, feats_lang, y, langs, strata, texts = _v100.build_dataset_v100(model, corpus)
    n = len(texts)

    # 1. CV-5 baseline
    print("\n  ── Baseline §100 (CV-5) ──")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    accs_full = []
    for tr, te in skf.split(X, y):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(X[tr], y[tr])
        accs_full.append(accuracy_score(y[te], clf.predict(X[te])))
    base_mean = float(np.mean(accs_full))
    base_std = float(np.std(accs_full))
    print(f"    {base_mean*100:.2f} ± {base_std*100:.2f} %  (n={n})")

    # 2. Trouver les ambigus : in-sample erreurs avec confiance non-écrasante
    clf_full = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf_full.fit(X, y)
    proba = clf_full.predict_proba(X)
    pred = proba.argmax(axis=1)
    margin = np.sort(proba, axis=1)[:, -1] - np.sort(proba, axis=1)[:, -2]

    # Critère "ambigu" : margin < 0.40 (cohérent avec §117)
    ambigu_idx = np.where((pred != y) | (margin < 0.20))[0]
    # On retire seulement les vrais ambigus (à la fois mal prédits ET bas-margin)
    strict_amb = np.where((pred != y) & (margin < 0.40))[0]
    print(f"\n  Cas mal prédits in-sample : {(pred != y).sum()}  (= 16 attendus)")
    print(f"  Cas low-margin (<0.40)    : {(margin < 0.40).sum()}")
    print(f"  Intersection (ambigus retirés §119) : {len(strict_amb)}")

    # 3. Corpus nettoyé
    keep = np.setdiff1d(np.arange(n), strict_amb)
    Xk, yk, langsk = X[keep], y[keep], langs[keep]
    n_keep = len(keep)

    accs_clean = []
    for tr, te in skf.split(Xk, yk):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(Xk[tr], yk[tr])
        accs_clean.append(accuracy_score(yk[te], clf.predict(Xk[te])))
    clean_mean = float(np.mean(accs_clean))
    clean_std = float(np.std(accs_clean))
    print(f"\n  Corpus nettoyé (n={n_keep}, retiré={n - n_keep}) :")
    print(f"    CV-5 = {clean_mean*100:.2f} ± {clean_std*100:.2f} %")
    print(f"    Δ vs baseline = {(clean_mean - base_mean)*100:+.2f} pp")

    converge_99 = clean_mean >= 0.99
    print("\n  ── Verdict §119 ──")
    if converge_99:
        print(f"  ✓ Borne supérieure empirique atteinte : ≥ 99 % avec retrait de {n - n_keep} cas ambigus")
    else:
        print(f"  ↗ Borne supérieure approchée mais < 99 % : reste {(1-clean_mean)*100:.1f} % d'incertitude")
        print(f"    (peut nécessiter retrait d'ambigus low-margin supplémentaires)")

    # 4. Variantes : retrait progressif
    print("\n  ── Sensibilité au seuil de margin ──")
    sensitivity = {}
    for thr in [0.10, 0.20, 0.30, 0.40]:
        amb = np.where((pred != y) & (margin < thr))[0]
        keep_t = np.setdiff1d(np.arange(n), amb)
        if len(keep_t) < 50:
            continue
        Xt, yt = X[keep_t], y[keep_t]
        accs_t = []
        for tr, te in skf.split(Xt, yt):
            clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
            clf.fit(Xt[tr], yt[tr])
            accs_t.append(accuracy_score(yt[te], clf.predict(Xt[te])))
        m = float(np.mean(accs_t))
        sensitivity[thr] = {"n_removed": int(len(amb)), "n_kept": int(len(keep_t)), "cv5_mean": m}
        print(f"    margin<{thr} : retirés={len(amb):3d}  n_kept={len(keep_t):3d}  CV-5={m*100:.2f}%")

    out = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v119_upper_bound_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version":            "§119",
        "n_total":            int(n),
        "n_removed":          int(n - n_keep),
        "baseline_cv5_mean":  base_mean,
        "cleaned_cv5_mean":   clean_mean,
        "delta_pp":           (clean_mean - base_mean) * 100,
        "convergence_99":     converge_99,
        "sensitivity":        sensitivity,
    }, ensure_ascii=False, indent=2, cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

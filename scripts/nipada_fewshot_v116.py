#!/usr/bin/env python3
"""
§116 — Few-shot k=2-5 par (type × langue) sur ar/ru/ja/hi
============================================================

Hypothèse : avec très peu d'exemples par (type × nouvelle langue), on peut
faire monter le rappel hold-out de §98 (76.4 %) sans annoter massivement.

Méthode
-------
- Pour chaque k ∈ {2, 3, 5}, on construit un train ne contenant pour les
  4 nouvelles langues (ar, ru, ja, hi) que k phrases par type.
- Pour les 7 langues anciennes (LANGS_94), on garde tout le corpus §100.
- On évalue : test = phrases restantes des 4 nouvelles langues.

Sortie : research/nipada/falsification/nipada_v116_fewshot_report.json
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

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
    print("  §116 — Few-shot k=2-5 par (type × nouvelle langue)")
    print("═" * 78)

    from sentence_transformers import SentenceTransformer
    print("\n  Modèle…")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    corpus = _v100.merge_corpus_v100()
    X, feats_syn, feats_lang, y, langs, strata, texts = _v100.build_dataset_v100(model, corpus)
    n = len(texts)

    NEW = set(_v100.NEW_LANGS)  # ar, ru, ja, hi

    # Indices par (type, langue) pour les nouvelles langues
    by_tl: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, (t_idx, la) in enumerate(zip(y, langs)):
        if la in NEW:
            by_tl[(_v100.IDX2TYPE[t_idx], la)].append(i)

    # Indices ancienne_langue (toujours train)
    old_idx = [i for i, la in enumerate(langs) if la not in NEW]

    results: dict[int, dict] = {}
    rng = random.Random(42)

    for k in [2, 3, 5]:
        print(f"\n  ── k={k} few-shot ──")
        # 5 splits stochastiques pour réduire variance
        accs = []
        per_lang_accs: dict[str, list[float]] = {la: [] for la in _v100.NEW_LANGS}
        for seed in range(5):
            rng2 = random.Random(seed)
            train_new = []
            test_new = []
            for (t, la), idxs in by_tl.items():
                rng2.shuffle(idxs)
                train_new.extend(idxs[:k])
                test_new.extend(idxs[k:])
            tr = old_idx + train_new
            te = test_new
            if not te:
                continue
            clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
            clf.fit(X[tr], y[tr])
            pred = clf.predict(X[te])
            acc = float(accuracy_score(y[te], pred))
            accs.append(acc)
            for la in _v100.NEW_LANGS:
                mask = [i for i, idx in enumerate(te) if langs[idx] == la]
                if mask:
                    per_lang_accs[la].append(float((pred[mask] == y[te][mask]).mean()))
        m = float(np.mean(accs))
        s = float(np.std(accs))
        print(f"    overall (5 seeds) : {m*100:.2f} ± {s*100:.2f} %  (n_train_new={k*7*4}, n_test_new≈{(89-k)*7*4})")
        per_lang_summary = {}
        for la in _v100.NEW_LANGS:
            if per_lang_accs[la]:
                pl_m = float(np.mean(per_lang_accs[la]))
                pl_s = float(np.std(per_lang_accs[la]))
                per_lang_summary[la] = {"mean": pl_m, "std": pl_s}
                print(f"      {la} : {pl_m*100:.2f} ± {pl_s*100:.2f} %")
        results[k] = {"overall_mean": m, "overall_std": s, "per_lang": per_lang_summary}

    # Comparaison référence : §98 hold-out 76.4 % sans aucun exemple new-lang en train
    print("\n  ── Référence §98 (zéro-shot sur 4 nouvelles) : 76.4% ──")
    print(f"  ↑ Few-shot k=2 : +{(results[2]['overall_mean']-0.764)*100:+.2f} pp")
    print(f"  ↑ Few-shot k=3 : +{(results[3]['overall_mean']-0.764)*100:+.2f} pp")
    print(f"  ↑ Few-shot k=5 : +{(results[5]['overall_mean']-0.764)*100:+.2f} pp")

    out = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v116_fewshot_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version":   "§116",
        "baseline_98_zeroshot_4newlangs": 0.764,
        "results_by_k": results,
        "n_phrases_total": int(n),
        "new_langs": list(_v100.NEW_LANGS),
    }, ensure_ascii=False, indent=2, cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

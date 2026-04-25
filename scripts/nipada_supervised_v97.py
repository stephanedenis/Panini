#!/usr/bin/env python3
"""
§97 — Pivot supervisé : régression logistique sur embeddings MiniLM
====================================================================
Plan §96 : abandonner le bricolage `cosinus + SYNTACTIC_BONUS` (plafond 53.2 %)
au profit d'un classifieur supervisé léger.

Approche :
- Réutilise CORPUS, LANGS, MODES, SYNTACTIC_BONUS et les regex de
  scripts/test_nipada_lacunes.py (corpus §94, 630 phrases × 7 types × 7 langues).
- Encode chaque phrase avec paraphrase-multilingual-MiniLM-L12-v2 (384-dim).
- Compare 4 stratégies sur exactement les mêmes splits :
    1. baseline §96 — cosinus + bonus syntaxique (référence)
    2. logistic regression sur embeddings purs (384 features)
    3. logistic regression + 4 features syntaxiques (388 features)
    4. logistic regression + 4 features syntaxiques + one-hot langue (395 feats)
- Validation croisée k=5 stratifiée par (type × langue) pour préserver
  l'équilibre.
- Hold-out final : test sur les 30 cas adversariaux (jamais vus en train).

Output → research/nipada/falsification/nipada_supervised_report.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Réutilise tout ce qui est défini dans test_nipada_lacunes.py
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "lacunes", REPO_ROOT / "scripts" / "test_nipada_lacunes.py"
)
_mod = importlib.util.module_from_spec(_spec)
# Patch __name__ pour empêcher l'exécution de main()
_mod.__name__ = "lacunes"
_spec.loader.exec_module(_mod)  # type: ignore[attr-defined]

CORPUS = _mod.CORPUS
LANGS = _mod.LANGS
MODES_V6 = _mod.MODES_V6
SYNTACTIC_BONUS = _mod.SYNTACTIC_BONUS
ADVERSARIAL = _mod.ADVERSARIAL
classify_with_syntax = _mod.classify_with_syntax
_has_question_marker = _mod._has_question_marker
_has_introspection_marker = _mod._has_introspection_marker
_has_definition_marker = _mod._has_definition_marker
_NpEncoder = _mod._NpEncoder
_to_native = _mod._to_native

from src.core.nipada_v6 import NipadaV6Synthesizer  # noqa: E402

CENTROID_LANGS = ["fr", "en", "de", "es", "zh"]

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_supervised_report.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

TYPES = list(CORPUS.keys())  # 7 types dans l'ordre canonique
TYPE2IDX = {t: i for i, t in enumerate(TYPES)}
IDX2TYPE = {i: t for t, i in TYPE2IDX.items()}
LANG2IDX = {la: i for i, la in enumerate(LANGS)}


def syntactic_features(text: str, lang: str) -> np.ndarray:
    """4 features binaires : has_question, has_intro_1p, has_def, lang_is_pro_drop."""
    has_q = _has_question_marker(text)
    has_1p = _has_introspection_marker(text)
    has_def = _has_definition_marker(text)
    pro_drop = 1.0 if lang in {"it", "pt", "es"} else 0.0
    return np.array([float(has_q), float(has_1p), float(has_def), pro_drop], dtype=np.float32)


def lang_onehot(lang: str) -> np.ndarray:
    v = np.zeros(len(LANGS), dtype=np.float32)
    v[LANG2IDX[lang]] = 1.0
    return v


def build_dataset(model: SentenceTransformer):
    """Retourne X (n×384), feats_syn (n×4), feats_lang (n×7), y (n,), strata (n,)."""
    texts: list[str] = []
    langs: list[str] = []
    y: list[int] = []
    for t, by_lang in CORPUS.items():
        for la, phrases in by_lang.items():
            for p in phrases:
                texts.append(p)
                langs.append(la)
                y.append(TYPE2IDX[t])
    print(f"  Encoding {len(texts)} phrases avec {MODEL_NAME}…", flush=True)
    X = np.asarray(model.encode(texts, batch_size=64, show_progress_bar=False, normalize_embeddings=True))
    feats_syn = np.stack([syntactic_features(t, la) for t, la in zip(texts, langs)])
    feats_lang = np.stack([lang_onehot(la) for la in langs])
    y_arr = np.asarray(y, dtype=np.int64)
    # strata = type * len(langs) + lang_idx → garantit ≥1 sample/(type,lang) par fold si possible
    strata = np.asarray([TYPE2IDX[TYPES[yi]] * len(LANGS) + LANG2IDX[la] for yi, la in zip(y, langs)])
    return X, feats_syn, feats_lang, y_arr, np.asarray(langs), strata, texts


def baseline_centroid_with_bonus(X_train: np.ndarray, y_train: np.ndarray,
                                 X_test: np.ndarray, texts_test: list[str]) -> np.ndarray:
    """Baseline §96 : centroïdes par type (entraînés sur train), cosinus + SYNTACTIC_BONUS."""
    centroids = {}
    for ti, t in enumerate(TYPES):
        mask = y_train == ti
        if mask.sum() == 0:
            centroids[t] = np.zeros_like(X_train[0])
        else:
            c = X_train[mask].mean(axis=0)
            n = np.linalg.norm(c)
            centroids[t] = c / n if n > 1e-10 else c
    preds = np.empty(len(X_test), dtype=np.int64)
    for i, (emb, txt) in enumerate(zip(X_test, texts_test)):
        # cosinus (X_test déjà normalisé → produit scalaire)
        sims = {t: float(np.dot(emb, centroids[t])) for t in TYPES}
        # bonus syntaxique
        has_q = _has_question_marker(txt)
        has_1p = _has_introspection_marker(txt)
        if has_q:
            sims["question"] += SYNTACTIC_BONUS["question"]
            if has_1p:
                sims["introspection"] += SYNTACTIC_BONUS["introspection_wq"]
        elif has_1p:
            sims["introspection"] += SYNTACTIC_BONUS["introspection_1p"]
        if _has_definition_marker(txt):
            sims["définition"] += SYNTACTIC_BONUS["définition"]
        preds[i] = TYPE2IDX[max(sims, key=sims.__getitem__)]
    return preds


def train_logreg(X_train: np.ndarray, y_train: np.ndarray, C: float = 1.0) -> LogisticRegression:
    # sklearn ≥ 1.5 : multi_class param retiré, multinomial est par défaut pour lbfgs
    clf = LogisticRegression(
        C=C, max_iter=2000, solver="lbfgs",
        random_state=42,
    )
    clf.fit(X_train, y_train)
    return clf


def cv_score(X_full: np.ndarray, y: np.ndarray, langs: np.ndarray,
             texts: list[str], strata: np.ndarray, n_splits: int = 5,
             extra_features: np.ndarray | None = None,
             use_logreg: bool = True, label: str = "") -> dict:
    """Validation croisée stratifiée."""
    # Combine embeddings + extra features si présent
    if extra_features is not None and use_logreg:
        Xc = np.hstack([X_full, extra_features])
    else:
        Xc = X_full

    # Stratification par strata combiné (type × lang) — fallback sur y si trop peu de samples
    try:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        splits = list(skf.split(Xc, strata))
    except ValueError:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        splits = list(skf.split(Xc, y))

    confusion = np.zeros((len(TYPES), len(TYPES)), dtype=np.int64)
    per_lang_correct: dict[str, int] = {la: 0 for la in LANGS}
    per_lang_total: dict[str, int] = {la: 0 for la in LANGS}
    fold_accuracies = []

    for fold, (tr, te) in enumerate(splits):
        if use_logreg:
            clf = train_logreg(Xc[tr], y[tr])
            preds = clf.predict(Xc[te])
        else:
            # baseline cosinus + bonus, centroïdes appris sur tr
            preds = baseline_centroid_with_bonus(
                X_full[tr], y[tr], X_full[te], [texts[i] for i in te]
            )
        correct = (preds == y[te]).sum()
        fold_accuracies.append(correct / len(te))
        for true_i, pred_i in zip(y[te], preds):
            confusion[true_i, pred_i] += 1
        for i, la in zip(te, langs[te]):
            per_lang_total[la] += 1
        for i, la, p, t in zip(te, langs[te], preds, y[te]):
            if p == t:
                per_lang_correct[la] += 1

    type_accuracy = {}
    for ti, t in enumerate(TYPES):
        n_t = confusion[ti].sum()
        type_accuracy[t] = float(confusion[ti, ti]) / float(n_t) if n_t > 0 else 0.0

    lang_accuracy = {
        la: per_lang_correct[la] / per_lang_total[la] if per_lang_total[la] > 0 else 0.0
        for la in LANGS
    }

    cm_dict = {TYPES[i]: {TYPES[j]: int(confusion[i, j]) for j in range(len(TYPES))}
               for i in range(len(TYPES))}

    return {
        "label": label,
        "global_accuracy": float(np.mean([(confusion[i, i]) / max(confusion[i].sum(), 1)
                                          for i in range(len(TYPES))]).mean()),
        "global_accuracy_micro": float(confusion.trace() / max(confusion.sum(), 1)),
        "fold_accuracies": [float(a) for a in fold_accuracies],
        "fold_mean": float(np.mean(fold_accuracies)),
        "fold_std": float(np.std(fold_accuracies)),
        "type_accuracy": type_accuracy,
        "lang_accuracy": lang_accuracy,
        "confusion_matrix": cm_dict,
    }


def adversarial_eval(model_clf: LogisticRegression, model_st: SentenceTransformer,
                     extra_n: int) -> dict:
    """Évalue les 30 cas adversariaux (toujours testés en FR puis EN)."""
    correct_fr = correct_en = 0
    details = []
    for adv in ADVERSARIAL:
        for lang_key in ("fr", "en"):
            txt = adv[lang_key]
            emb = model_st.encode([txt], normalize_embeddings=True)[0]
            feats = []
            if extra_n >= 4:
                feats.append(syntactic_features(txt, lang_key))
            if extra_n >= 11:
                feats.append(lang_onehot(lang_key))
            if feats:
                x = np.hstack([emb, *feats]).reshape(1, -1)
            else:
                x = emb.reshape(1, -1)
            pred_idx = int(model_clf.predict(x)[0])
            pred = IDX2TYPE[pred_idx]
            ok = (pred == adv["expected"])
            if lang_key == "fr" and ok:
                correct_fr += 1
            if lang_key == "en" and ok:
                correct_en += 1
            details.append({
                "lang": lang_key, "text": txt, "expected": adv["expected"],
                "predicted": pred, "confusible_with": adv.get("confusible_with"),
                "correct": bool(ok),
            })
    return {
        "correct_fr": correct_fr, "correct_en": correct_en,
        "n": len(ADVERSARIAL),
        "details": details,
    }


def main() -> None:
    W = 78
    print("═" * W)
    print(f"  §97 — Classifieur supervisé sur embeddings MiniLM (corpus §94)")
    print("═" * W)
    print(f"  Modèle : {MODEL_NAME}  |  {len(TYPES)} types  |  {len(LANGS)} langues")

    model = SentenceTransformer(MODEL_NAME)
    X, feats_syn, feats_lang, y, langs, strata, texts = build_dataset(model)
    print(f"  X.shape = {X.shape}  |  y bins = {np.bincount(y).tolist()}")

    print("\n  ── Validation croisée stratifiée k=5 ──")

    results = {}

    # ── Vrai baseline §96 : centroïdes fixes synthétisés depuis MODES_V6 (kernels nipada) ──
    print("  [0/5] vrai baseline §96 (centroïdes nipada fixes, classify_with_syntax)…", flush=True)
    synth = NipadaV6Synthesizer()
    fixed_centroids: dict[str, np.ndarray] = {}
    for mode_name, mol_ids in MODES_V6.items():
        vecs = [model.encode(synth.synthesize(mol_ids, la), show_progress_bar=False)
                for la in CENTROID_LANGS]
        c = np.mean(vecs, axis=0)
        n = np.linalg.norm(c)
        fixed_centroids[mode_name] = c / n if n > 1e-10 else c
    # évalue sur l'intégralité du corpus (pas de train/test split, les centroïdes sont fixes)
    confusion_fix = np.zeros((len(TYPES), len(TYPES)), dtype=np.int64)
    per_lang_fix = {la: [0, 0] for la in LANGS}  # [correct, total]
    for emb, txt, true_i, la in zip(X, texts, y, langs):
        sims = {t: float(np.dot(emb, fixed_centroids[t])) for t in TYPES}
        has_q = _has_question_marker(txt)
        has_1p = _has_introspection_marker(txt)
        if has_q:
            sims["question"] += SYNTACTIC_BONUS["question"]
            if has_1p:
                sims["introspection"] += SYNTACTIC_BONUS["introspection_wq"]
        elif has_1p:
            sims["introspection"] += SYNTACTIC_BONUS["introspection_1p"]
        if _has_definition_marker(txt):
            sims["définition"] += SYNTACTIC_BONUS["définition"]
        pred_i = TYPE2IDX[max(sims, key=sims.__getitem__)]
        confusion_fix[true_i, pred_i] += 1
        per_lang_fix[la][1] += 1
        if pred_i == true_i:
            per_lang_fix[la][0] += 1
    type_acc_fix = {t: float(confusion_fix[i, i]) / max(confusion_fix[i].sum(), 1)
                    for i, t in enumerate(TYPES)}
    lang_acc_fix = {la: per_lang_fix[la][0] / max(per_lang_fix[la][1], 1) for la in LANGS}
    results["baseline_96_true"] = {
        "label": "§96 vrai (kernels nipada fixes)",
        "global_accuracy_micro": float(confusion_fix.trace() / max(confusion_fix.sum(), 1)),
        "fold_mean": float(confusion_fix.trace() / max(confusion_fix.sum(), 1)),
        "fold_std": 0.0,
        "fold_accuracies": [],
        "type_accuracy": type_acc_fix,
        "lang_accuracy": lang_acc_fix,
        "confusion_matrix": {TYPES[i]: {TYPES[j]: int(confusion_fix[i, j]) for j in range(len(TYPES))}
                              for i in range(len(TYPES))},
    }

    print("  [1/5] centroïde-corpus (centroïdes appris sur train fold + bonus, k=5)…", flush=True)
    results["centroid_corpus"] = cv_score(X, y, langs, texts, strata,
                                           use_logreg=False, label="centroïdes corpus + bonus")

    print("  [2/5] logreg sur embeddings 384-dim purs…", flush=True)
    results["logreg_384"] = cv_score(X, y, langs, texts, strata,
                                      extra_features=None, label="logreg 384-dim")

    print("  [3/5] logreg + 4 features syntaxiques (388-dim)…", flush=True)
    results["logreg_388"] = cv_score(X, y, langs, texts, strata,
                                      extra_features=feats_syn,
                                      label="logreg 384 + 4 syntaxiques")

    print("  [4/5] logreg + 4 syntax + 7 lang one-hot (395-dim)…", flush=True)
    extra = np.hstack([feats_syn, feats_lang])
    results["logreg_395"] = cv_score(X, y, langs, texts, strata,
                                      extra_features=extra,
                                      label="logreg 384 + 4 syntax + 7 lang")

    print("\n" + "═" * W)
    print("  RÉSULTATS COMPARATIFS")
    print("═" * W)
    print(f"  {'stratégie':<36s} {'global':>8s} {'fold_mean':>10s} {'fold_std':>9s}")
    for k, r in results.items():
        print(f"  {r['label']:<36s} {r['global_accuracy_micro']:>8.1%} "
              f"{r['fold_mean']:>10.1%} {r['fold_std']:>9.1%}")

    print("\n  ── Détail par type (vrai §96 → logreg_395) ──")
    best = results["logreg_395"]
    base = results["baseline_96_true"]
    print(f"  {'type':<16s}{'§96 vrai':>10s}{'395-dim':>10s}{'Δ':>9s}")
    for t in TYPES:
        a0 = base["type_accuracy"][t]
        a1 = best["type_accuracy"][t]
        print(f"  {t:<16s}{a0:>10.1%}{a1:>10.1%}{(a1-a0)*100:>+8.1f}pp")

    print("\n  ── Détail par langue (vrai §96 → logreg_395) ──")
    print(f"  {'lang':<6s}{'§96 vrai':>10s}{'395-dim':>10s}{'Δ':>9s}")
    for la in LANGS:
        a0 = base["lang_accuracy"][la]
        a1 = best["lang_accuracy"][la]
        print(f"  {la:<6s}{a0:>10.1%}{a1:>10.1%}{(a1-a0)*100:>+8.1f}pp")

    # Adversarial : on entraîne le meilleur classifieur sur tout le corpus
    print("\n  ── Évaluation adversariale (30 cas × FR/EN, hors corpus) ──")
    extra_full = np.hstack([feats_syn, feats_lang])
    X_full = np.hstack([X, extra_full])
    final_clf = train_logreg(X_full, y)
    adv = adversarial_eval(final_clf, model, extra_n=11)
    print(f"  Adversarial : {adv['correct_fr']}/{adv['n']} FR  +  {adv['correct_en']}/{adv['n']} EN")

    out = {
        "benchmark": "§97 classifieur supervisé sur MiniLM (corpus §94, 630 phrases, k=5 cv stratifié)",
        "model": MODEL_NAME,
        "n_sentences": int(len(y)),
        "n_types": len(TYPES),
        "n_langs": len(LANGS),
        "types": TYPES,
        "langs": LANGS,
        "results": results,
        "adversarial": adv,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(_to_native(out), f, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"\n  Résultats → {OUTPUT}")
    print("═" * W)


if __name__ == "__main__":
    main()

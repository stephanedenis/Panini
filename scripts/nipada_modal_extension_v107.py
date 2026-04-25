#!/usr/bin/env python3
"""
§107 — Ré-annotation modale du corpus §100 (7 → 11 sous-types)
==================================================================

Hypothèse §102 :  V7 + MODALITÉ ⇒ séparabilité supplémentaire des types
                  qui se distinguent par la *modalité* plutôt que par le
                  contenu sémantique.

Méthode
-------
1. On charge le corpus §100 (980 phrases × 11 langues).
2. Pour chaque phrase, on détecte les modalités via §108.
3. On crée la taxonomie étendue T_E_v107 :
   - description           (mol [30])             — non-modal
   - narration             (mol [13, 78, 273])    — non-modal
   - définition            (non-modal pure)       — sans marqueur DEVOIR
   - définition_normative  (modale)               — avec marqueur DEVOIR
   - proclamation          (sans modal)
   - proclamation_modale   (avec marqueur)
   - question              (DOUTE forcé par '?')
   - ordre                 (sans modal explicite — impératif)
   - ordre_modal           (avec DEVOIR/ORDONNER)
   - introspection         (sans modal)
   - introspection_modale  (avec marqueur DOUTE/SAVOIR/VOULOIR)
4. On entraîne logreg sur (404 dim §100 + 7 dim modal) avec ces sous-types.
5. CV-5 stratifiée par (sous-type × langue), comparée au baseline §100.

Sortie : research/nipada/falsification/nipada_v107_modal_subtypes_report.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _import(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


_v100 = _import("v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py")
_v108 = _import("v108", REPO_ROOT / "scripts" / "nipada_modal_markers_v108.py")


# ══════════════════════════════════════════════════════════════════════════════
# Taxonomie étendue v107
# ══════════════════════════════════════════════════════════════════════════════

# Pour chaque type V7, on définit la règle de splitting :
#   - "modal_kind"=None       → pas de split (description, narration)
#   - "modal_kind"="DOUTE"    → split en X / X_modale selon présence DOUTE
#   - "modal_kind"=*          → split en X / X_modale selon présence du marqueur
SPLIT_RULES = {
    "description":   {"split": False},
    "narration":     {"split": False},
    "définition":    {"split": True,  "marker": "DEVOIR",     "suffix": "_normative"},
    "proclamation":  {"split": True,  "marker": None,         "suffix": "_modale"},  # any modal
    "question":      {"split": False},  # toujours DOUTE par '?'
    "ordre":         {"split": True,  "marker": "ORDONNER+DEVOIR", "suffix": "_modale"},
    "introspection": {"split": True,  "marker": "DOUTE+VOULOIR+SAVOIR", "suffix": "_modale"},
}


def _matches_marker(modvec: list[int], marker_spec: str | None) -> bool:
    """Retourne True si la phrase contient au moins un marqueur de la spec."""
    if marker_spec is None:
        return sum(modvec) > 0
    wanted = marker_spec.split("+")
    for m in wanted:
        if modvec[_v108.MOD2IDX[m]] > 0:
            return True
    return False


def relabel_v107(text: str, lang: str, type_v7: str) -> str:
    """Retourne le sous-type étendu pour une phrase."""
    rule = SPLIT_RULES[type_v7]
    if not rule["split"]:
        return type_v7
    modvec = _v108.detect_modalities_vec(text, lang)
    if _matches_marker(modvec, rule["marker"]):
        return type_v7 + rule["suffix"]
    return type_v7


# ══════════════════════════════════════════════════════════════════════════════
# Pipeline
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 78)
    print("  §107 — Ré-annotation modale corpus §100 (7 → 11 sous-types)")
    print("═" * 78)

    # 1. Embeddings + features §100
    from sentence_transformers import SentenceTransformer
    print("\n  Chargement modèle paraphrase-multilingual-MiniLM-L12-v2...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    print("  Construction dataset §100 (404 dim)...")
    corpus = _v100.merge_corpus_v100()
    X100, feats_syn, feats_lang, y_arr, langs_arr, strata, texts = \
        _v100.build_dataset_v100(model, corpus)

    n = len(texts)
    print(f"    n = {n} phrases  X100.shape = {X100.shape}")

    # 2. Vecteur modal 7-dim par phrase
    print("\n  Détection modalités §108 (7 dim)...")
    mod_vecs = np.array([_v108.detect_modalities_vec(t, la)
                          for t, la in zip(texts, langs_arr)], dtype=np.float32)
    print(f"    mod_vecs.shape = {mod_vecs.shape}  total markers = {int(mod_vecs.sum())}")

    # 3. Ré-annotation v107
    print("\n  Ré-annotation v107...")
    types_v7 = [_v100.IDX2TYPE[i] for i in y_arr]
    labels_v107 = [relabel_v107(t, la, ty) for t, la, ty in zip(texts, langs_arr, types_v7)]
    cnt = Counter(labels_v107)
    print(f"    Sous-types observés : {len(cnt)}")
    for label, n_label in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"      {label:<28s} {n_label:4d}")

    # Filtrer sous-types trop rares pour CV-5 (n<5)
    min_samples = 5
    rare = [k for k, v in cnt.items() if v < min_samples]
    if rare:
        print(f"\n    /!\\  Sous-types <{min_samples} regroupés au type parent : {rare}")
        labels_v107 = [(l if cnt[l] >= min_samples else l.split("_")[0]) for l in labels_v107]
        cnt = Counter(labels_v107)
        print(f"    Sous-types finaux : {len(cnt)}")

    LBL = sorted(cnt.keys())
    LBL2IDX = {l: i for i, l in enumerate(LBL)}
    y_v107 = np.array([LBL2IDX[l] for l in labels_v107], dtype=np.int32)

    # 4. Construction features étendues
    X_v107 = np.hstack([X100, mod_vecs])
    print(f"\n  X_v107.shape = {X_v107.shape}  ({X100.shape[1]}+{mod_vecs.shape[1]})")

    # 5. Stratification par (sous-type × langue), classes rares regroupées
    new_strata = [f"{l}|{la}" for l, la in zip(labels_v107, langs_arr)]
    s_cnt = Counter(new_strata)
    new_strata = [(s if s_cnt[s] >= 5 else l) for s, l in zip(new_strata, labels_v107)]

    # 6. CV-5 : baseline V7 (7 classes) vs v107 étendu
    print("\n  ── CV-5 stratifiée ──")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 6a. Baseline V7 sur X100
    accs_v7 = []
    for tr, te in skf.split(X100, y_arr):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(X100[tr], y_arr[tr])
        accs_v7.append(accuracy_score(y_arr[te], clf.predict(X100[te])))
    cv_v7_mean = float(np.mean(accs_v7))
    cv_v7_std = float(np.std(accs_v7))
    print(f"    V7 (7 classes,  X100=404d)        : {cv_v7_mean*100:.2f} ± {cv_v7_std*100:.2f} %")

    # 6b. v107 sur X100 (sans modal — borne basse)
    accs_v107_x100 = []
    for tr, te in skf.split(X100, y_v107):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(X100[tr], y_v107[tr])
        accs_v107_x100.append(accuracy_score(y_v107[te], clf.predict(X100[te])))
    cv_v107_x100_mean = float(np.mean(accs_v107_x100))
    cv_v107_x100_std = float(np.std(accs_v107_x100))
    print(f"    v107 ({len(LBL)} classes, X100=404d)        : "
          f"{cv_v107_x100_mean*100:.2f} ± {cv_v107_x100_std*100:.2f} %")

    # 6c. v107 sur X_v107 (avec modal — borne haute)
    accs_v107 = []
    per_class_acc: dict[str, list[float]] = {l: [] for l in LBL}
    for tr, te in skf.split(X_v107, y_v107):
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
        clf.fit(X_v107[tr], y_v107[tr])
        y_pred = clf.predict(X_v107[te])
        accs_v107.append(accuracy_score(y_v107[te], y_pred))
        for l in LBL:
            mask = y_v107[te] == LBL2IDX[l]
            if mask.sum() > 0:
                per_class_acc[l].append(float((y_pred[mask] == LBL2IDX[l]).mean()))
    cv_v107_mean = float(np.mean(accs_v107))
    cv_v107_std = float(np.std(accs_v107))
    print(f"    v107 ({len(LBL)} classes, X_v107={X_v107.shape[1]}d): "
          f"{cv_v107_mean*100:.2f} ± {cv_v107_std*100:.2f} %")

    print("\n  ── Accuracy par sous-type (X_v107) ──")
    per_class_summary = {}
    for l in LBL:
        m = float(np.mean(per_class_acc[l])) if per_class_acc[l] else 0.0
        per_class_summary[l] = {"mean_acc": m, "n_total": int(cnt[l])}
        print(f"    {l:<28s}  acc={m*100:5.1f}%  (n={cnt[l]})")

    # 7. Verdict §102
    delta = (cv_v107_mean - cv_v107_x100_mean) * 100
    print("\n" + "═" * 78)
    print("  VERDICT §102 (V7 + MODALITÉ apporte-t-il une séparabilité supplémentaire ?)")
    print("═" * 78)
    print(f"  Sans modal : {cv_v107_x100_mean*100:.2f} %")
    print(f"  Avec modal : {cv_v107_mean*100:.2f} %")
    print(f"  Δ          : {delta:+.2f} pp sur la taxonomie étendue ({len(LBL)} classes)")
    if delta > 1.0:
        print("  → SIGNAL : les marqueurs modaux discriminent les sous-types modaux/non-modaux.")
    elif delta > 0.0:
        print("  → Léger signal positif (sub-pp).")
    else:
        print("  → Pas de gain : les embeddings encodent déjà la modalité (cohérent §106).")

    # 8. Sortie
    out = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v107_modal_subtypes_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version": "§107",
        "n_phrases": int(n),
        "labels_v107": LBL,
        "label_counts": dict(cnt),
        "split_rules": SPLIT_RULES,
        "cv5_v7_baseline":      {"mean": cv_v7_mean,        "std": cv_v7_std,        "n_classes": 7,        "feat_dim": int(X100.shape[1])},
        "cv5_v107_no_modal":    {"mean": cv_v107_x100_mean, "std": cv_v107_x100_std, "n_classes": len(LBL), "feat_dim": int(X100.shape[1])},
        "cv5_v107_with_modal":  {"mean": cv_v107_mean,      "std": cv_v107_std,      "n_classes": len(LBL), "feat_dim": int(X_v107.shape[1])},
        "delta_modal_pp":       delta,
        "per_class_acc": per_class_summary,
    }, ensure_ascii=False, indent=2, cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

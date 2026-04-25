#!/usr/bin/env python3
"""
§118 — Adversarial automatisé multi-langues
==================================================

Objectif : générer un corpus de phrases borderline en appliquant 5 transformations
procédurales connues pour brouiller la frontière entre 2 types V7, et mesurer
la dégradation du classifier §100.

Transformations (T1-T5)
-----------------------
T1. Définition → Question rhétorique   ("X est Y." → "Qu'est-ce que X, sinon Y ?")
T2. Description → Narration            ("Le X fait Y." → "Hier, le X fit Y.")
T3. Proclamation → Définition normative ("Tout X est Y." identique mais on le donne comme un fait)
T4. Ordre → Description impersonnelle   ("Faites X !" → "Il convient de faire X.")
T5. Introspection → Narration 3e        ("Je doute." → "Il douta.")

Sortie : research/nipada/falsification/nipada_v118_adversarial_report.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _import(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_v100 = _import("v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py")


# ══════════════════════════════════════════════════════════════════════════════
# Corpus adversarial
# Format : (texte, label_intention_initiale, label_brouille_hypothese, lang, transformation)
# ══════════════════════════════════════════════════════════════════════════════

ADV = [
    # T1 — définition → question rhétorique (label cible reste DÉFINITION)
    ("Qu'est-ce que la liberté, sinon l'absence de contrainte ?", "définition", "question", "fr", "T1"),
    ("What is justice, if not the proper proportion?",            "définition", "question", "en", "T1"),
    ("Cos'è il tempo, se non la misura del cambiamento?",          "définition", "question", "it", "T1"),
    ("¿Qué es la verdad, sino la conformidad de pensamiento y cosa?", "définition", "question", "es", "T1"),
    ("Was ist Sein, wenn nicht das Anwesende?",                    "définition", "question", "de", "T1"),

    # T2 — description → narration (présent → passé simple/composé)
    ("Hier, le boulanger pétrit la pâte, la laissa lever, puis la cuisit à 250°C.", "description", "narration", "fr", "T2"),
    ("Yesterday the baker kneaded the dough, let it rise, and then baked it.",      "description", "narration", "en", "T2"),
    ("Ieri il fornaio impastò, lasciò lievitare, poi cosse il pane.",                "description", "narration", "it", "T2"),

    # T3 — proclamation → définition normative
    ("Tout être humain est libre et égal en droits ; cela définit la condition humaine.", "proclamation", "définition", "fr", "T3"),
    ("All citizens are by definition equal before the law.",                                "proclamation", "définition", "en", "T3"),
    ("Ogni essere umano è, per definizione, dotato di dignità.",                            "proclamation", "définition", "it", "T3"),

    # T4 — ordre → description impersonnelle
    ("Il convient de fermer la porte avant de partir.",                                  "ordre", "description", "fr", "T4"),
    ("It is appropriate to close the door before leaving.",                              "ordre", "description", "en", "T4"),
    ("È opportuno chiudere la porta prima di uscire.",                                   "ordre", "description", "it", "T4"),

    # T5 — introspection → narration 3e personne
    ("Il douta longtemps puis se résolut à partir.",                                     "introspection", "narration", "fr", "T5"),
    ("He doubted long, then resolved to leave.",                                         "introspection", "narration", "en", "T5"),
    ("Dubitò a lungo, poi decise di partire.",                                           "introspection", "narration", "it", "T5"),

    # Bonus arabe / russe / japonais / hindi
    ("ما هو العدل، إن لم يكن التناسب الصحيح؟",                                          "définition", "question", "ar", "T1"),
    ("Что есть свобода, если не отсутствие принуждения?",                                "définition", "question", "ru", "T1"),
    ("正義とは何か、適切な均衡でなければ何なのか？",                                     "définition", "question", "ja", "T1"),
    ("स्वतंत्रता क्या है, यदि बाधा का अभाव नहीं?",                                            "définition", "question", "hi", "T1"),
    ("彼は長く疑い、ついに去ることを決意した。",                                          "introspection", "narration", "ja", "T5"),
    ("Он долго сомневался, потом решил уйти.",                                           "introspection", "narration", "ru", "T5"),
]


def main() -> None:
    print("═" * 78)
    print("  §118 — Adversarial automatisé multi-langues")
    print("═" * 78)
    print(f"\n  Corpus adversarial : {len(ADV)} phrases (5 transformations T1-T5)")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    corpus = _v100.merge_corpus_v100()
    X, feats_syn, feats_lang, y, langs, strata, texts = _v100.build_dataset_v100(model, corpus)

    clf = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf.fit(X, y)

    adv_texts = [t for t, *_ in ADV]
    adv_labels = [_v100.TYPE2IDX[l] for _, l, *_ in ADV]
    adv_brouilles = [_v100.TYPE2IDX[lb] for _, _, lb, *_ in ADV]
    adv_langs = [la for _, _, _, la, _ in ADV]

    Xa = np.asarray(model.encode(adv_texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True))
    proba = clf.predict_proba(Xa)
    pred = proba.argmax(axis=1)

    print("\n  ── Résultats ──")
    correct_target = 0
    fooled_to_brouille = 0
    other = 0
    per_T: dict[str, list[int]] = {f"T{i}": [0, 0, 0] for i in range(1, 6)}  # [target, brouille, other]
    rows = []
    for i, (t, intent, brouille, la, T) in enumerate(ADV):
        p = pred[i]
        is_target = (p == adv_labels[i])
        is_brouille = (p == adv_brouilles[i])
        if is_target:
            correct_target += 1
            per_T[T][0] += 1
            verdict = "✓"
        elif is_brouille:
            fooled_to_brouille += 1
            per_T[T][1] += 1
            verdict = "✗ brouillé"
        else:
            other += 1
            per_T[T][2] += 1
            verdict = "✗ autre"
        pred_label = _v100.IDX2TYPE[int(p)]
        margin = float(np.sort(proba[i])[-1] - np.sort(proba[i])[-2])
        rows.append({"text": t, "lang": la, "T": T, "intent": intent, "brouille": brouille,
                     "predicted": pred_label, "verdict": verdict, "margin": margin,
                     "p_intent": float(proba[i, adv_labels[i]]),
                     "p_brouille": float(proba[i, adv_brouilles[i]])})
        print(f"  [{T} {la}] {intent:<14s} → pred={pred_label:<14s}  m={margin:.2f}  {verdict}")

    n = len(ADV)
    print("\n  ── Synthèse ──")
    print(f"  Accuracy intent (label robuste) : {correct_target}/{n} = {correct_target/n*100:.1f}%")
    print(f"  Brouillage (T réussit)          : {fooled_to_brouille}/{n} = {fooled_to_brouille/n*100:.1f}%")
    print(f"  Autre erreur                    : {other}/{n} = {other/n*100:.1f}%")
    print("\n  Par transformation :")
    for T in ["T1", "T2", "T3", "T4", "T5"]:
        a, b, c = per_T[T]
        tot = a + b + c
        print(f"    {T} : intent={a}/{tot} brouille={b}/{tot} autre={c}/{tot}")

    out = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_v118_adversarial_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version":      "§118",
        "n_adversarial": n,
        "accuracy_intent":   correct_target / n,
        "brouillage_rate":   fooled_to_brouille / n,
        "other_error_rate":  other / n,
        "per_transformation": {T: {"intent": v[0], "brouille": v[1], "other": v[2]} for T, v in per_T.items()},
        "details": rows,
    }, ensure_ascii=False, indent=2, cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

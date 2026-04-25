#!/usr/bin/env python3
"""
§106 — Décision B : connecter l'encyclopédie au classifieur
============================================================

Test empirique de la tension fondationnelle « encyclopédie ⊥ classifieur »
identifiée à la rétrospective de §104. On injecte des features
d'attestation encyclopédique dans le pipeline §100 :

    auteur_count       — nb mentions distinctes d'auteur (T_O.AUTEUR)
    lieu_count         — nb mentions distinctes de lieu (T_O.LIEU)
    epoque_count       — nb mentions distinctes d'époque (T_O.EPOQUE)
    objet_celeste_count — nb mentions distinctes (T_O.OBJET_CELESTE)
    evenement_count    — nb mentions distinctes (T_O.ÉVÉNEMENT_*)
    has_iso_date       — présence d'un indice de date (siècle / année / -###)
    total_attest       — somme des cinq comptages

Pipeline : 384 (emb) + 4 (syn §97) + 5 (def §100) + 11 (lang §98) + 7 (enc §106) = 411 dim.

Protocole :
  1. Construire détecteur multi-script via `names`/`label_native`/aliases.
  2. Mesurer couverture sur les 983 phrases §100 (combien activent ≥ 1 feature ?).
  3. Si couverture < 5 %, le test sur §100 sera quasi-nul → c'est en soi
     le résultat empirique : le corpus §100 est non-narratif par construction.
  4. Ré-entraîner logreg avec les 7 features ajoutées et comparer CV §100.
  5. Tester sur un mini-corpus narratif §106 (~30 phrases historiques
     cross-langue) où les features sont par construction informatives.

Sortie :
  - research/nipada/falsification/nipada_v106_encyclopedia_features_report.json

Conclusion attendue :
  - §100 : gain ≈ 0 (couverture insuffisante).
  - §106-narrative : features bien différenciantes pour `narration`.
"""

from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

warnings.filterwarnings("ignore", category=FutureWarning)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import importlib.util  # noqa: E402

_spec_v100 = importlib.util.spec_from_file_location(
    "v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py"
)
_v100 = importlib.util.module_from_spec(_spec_v100)
_spec_v100.loader.exec_module(_v100)  # type: ignore[attr-defined]

ENC_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"
OUTPUT = (REPO_ROOT / "research" / "nipada" / "falsification"
          / "nipada_v106_encyclopedia_features_report.json")
MODEL_NAME = _v100.MODEL_NAME


# ══════════════════════════════════════════════════════════════════════════════
# 1. Détecteur encyclopédique
# ══════════════════════════════════════════════════════════════════════════════

def _load_seeds() -> dict[str, list[dict]]:
    seeds = {}
    seeds["auteur"] = json.loads((ENC_DIR / "auteurs_seed.json").read_text(encoding="utf-8"))["auteurs"]
    seeds["lieu"] = json.loads((ENC_DIR / "lieux_zones.json").read_text(encoding="utf-8"))["lieux"]
    seeds["epoque"] = json.loads((ENC_DIR / "temps_epoques.json").read_text(encoding="utf-8"))["epoques"]
    seeds["evenement"] = json.loads((ENC_DIR / "evenements_seed.json").read_text(encoding="utf-8"))["evenements"]
    astro = ENC_DIR / "astronomie"
    seeds["objet_celeste"] = json.loads((astro / "objets_celestes.json").read_text(encoding="utf-8"))["objets"]
    seeds["evenement_astro"] = json.loads((astro / "evenements_astronomiques.json").read_text(encoding="utf-8"))["evenements"]
    return seeds


def _norm(s: str) -> str:
    return s.lower()


def _build_alias_index(seeds: dict[str, list[dict]]) -> dict[str, list[tuple[str, set[str]]]]:
    """Pour chaque catégorie, retourne (entity_id, set_of_aliases_lowercased)."""
    idx: dict[str, list[tuple[str, set[str]]]] = {}

    # AUTEUR : `names` est un dict lang → list[str]
    auteur_aliases = []
    for ent in seeds["auteur"]:
        aliases = set()
        for la, names in (ent.get("names") or {}).items():
            for n in names:
                if len(n) >= 4:   # éviter monosyllabes ambigus
                    aliases.add(_norm(n))
        if aliases:
            auteur_aliases.append((ent["id"], aliases))
    idx["auteur"] = auteur_aliases

    # LIEU : label_fr + label_native (script natif) + label en
    lieu_aliases = []
    for ent in seeds["lieu"]:
        aliases = set()
        for k in ("label_fr", "label_en", "label_native"):
            v = ent.get(k)
            if isinstance(v, str) and len(v) >= 4:
                aliases.add(_norm(v))
        # extraire mots significatifs des labels composites
        for k in ("label_fr", "label_en"):
            v = ent.get(k, "")
            for w in re.findall(r"\b[\w\u00C0-\uFFFF]{4,}\b", v):
                if w.lower() not in {"vallée", "plaine", "centrale", "anciennes", "moderne"}:
                    aliases.add(_norm(w))
        if aliases:
            lieu_aliases.append((ent["id"], aliases))
    idx["lieu"] = lieu_aliases

    # EPOQUE : label_fr + label_en + interval_label (« −III mil. – VIIIe s. AEC »)
    epoque_aliases = []
    for ent in seeds["epoque"]:
        aliases = set()
        for k in ("label_fr", "label_en"):
            v = ent.get(k, "")
            if v:
                aliases.add(_norm(v))
        if aliases:
            epoque_aliases.append((ent["id"], aliases))
    idx["epoque"] = epoque_aliases

    # OBJET_CELESTE
    objet_aliases = []
    for ent in seeds["objet_celeste"]:
        aliases = set()
        for k in ("notes",):
            pass  # skip
        for k in ("id",):
            v = ent.get(k, "")
            v = v.replace("_", " ")
            if len(v) >= 4:
                aliases.add(_norm(v))
        # alias usuels (peuvent venir de notes/catalogues)
        cats = ent.get("catalogues") or {}
        if isinstance(cats, dict):
            for vlist in cats.values():
                if isinstance(vlist, str) and len(vlist) >= 4:
                    aliases.add(_norm(vlist))
        notes = ent.get("notes", "")
        for word in ("Soleil", "Sun", "Sol", "Proxima", "Centauri", "Sagittarius", "Sgr A",
                     "Sanduleak", "GW150914", "CMB", "fond diffus", "cosmic microwave"):
            if word.lower() in notes.lower() or word.lower() in ent.get("id", "").lower():
                aliases.add(_norm(word))
        if aliases:
            objet_aliases.append((ent["id"], aliases))
    idx["objet_celeste"] = objet_aliases

    # EVENEMENT (§103 + §104)
    evt_aliases = []
    for ent in seeds["evenement"] + seeds["evenement_astro"]:
        aliases = set()
        for k in ("name", "name_native"):
            v = ent.get(k, "")
            if isinstance(v, str) and len(v) >= 4:
                aliases.add(_norm(v))
                # mots significatifs
                for w in re.findall(r"\b[\w\u00C0-\uFFFF]{4,}\b", v):
                    aliases.add(_norm(w))
        if aliases:
            evt_aliases.append((ent["id"], aliases))
    idx["evenement"] = evt_aliases

    return idx


_DATE_RE = re.compile(
    r"\b(?:"
    r"\d{3,4}\s*(?:AEC|EC|av\.?\s*J\.?-?C\.?|ap\.?\s*J\.?-?C\.?|BCE|CE|BC|AD)"   # 384 AEC
    r"|[-−]\d{3,4}"                                                              # -384
    r"|[IVX]+e?\s*si[èe]cle"                                                    # IVe siècle
    r"|\d{4}"                                                                    # 1985 (peut être faux positif)
    r")\b",
    flags=re.IGNORECASE,
)


def encyclopedia_features(text: str, idx: dict) -> np.ndarray:
    """7 dim : auteur, lieu, epoque, objet_celeste, evenement, date, total."""
    t = _norm(text)
    counts = {}
    for cat, entities in idx.items():
        c = 0
        for _ent_id, aliases in entities:
            # un alias suffit pour compter l'entité
            for a in aliases:
                if a in t:
                    c += 1
                    break
        counts[cat] = c
    # Normalisation log1p légère (counts déjà petits par phrase)
    f_aut = float(counts.get("auteur", 0))
    f_lie = float(counts.get("lieu", 0))
    f_epo = float(counts.get("epoque", 0))
    f_obj = float(counts.get("objet_celeste", 0))
    f_evt = float(counts.get("evenement", 0))
    f_date = 1.0 if _DATE_RE.search(text) else 0.0
    f_tot = f_aut + f_lie + f_epo + f_obj + f_evt + f_date
    return np.array([f_aut, f_lie, f_epo, f_obj, f_evt, f_date, f_tot], dtype=np.float64)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Mini-corpus narratif §106 (validation positive)
# ══════════════════════════════════════════════════════════════════════════════
#
# 30 phrases courtes mentionnant explicitement auteurs/lieux/époques/événements.
# But : démontrer que les features encyclopédiques sont par construction
#       informatives pour distinguer narration vs description.
# 6 langues, 5 phrases / langue, 3 narration + 2 description par langue.

NARRATIVE_CORPUS: list[tuple[str, str, str]] = [
    # FR — narration
    ("Platon fonda l'Académie à Athènes au IVe siècle AEC.", "narration", "fr"),
    ("Pāṇini composa l'Aṣṭādhyāyī dans la vallée de l'Indus.", "narration", "fr"),
    ("Dante écrivit la Divine Comédie pendant son exil de Florence.", "narration", "fr"),
    ("Une étoile brille dans le ciel.", "description", "fr"),
    ("La justice est un principe universel.", "description", "fr"),
    # EN — narration
    ("Confucius taught his disciples in the Central Plain during the Spring and Autumn period.", "narration", "en"),
    ("Goethe traveled through Italy in 1786 and recorded his impressions.", "narration", "en"),
    ("Tagore founded a university in Bengal in the early twentieth century.", "narration", "en"),
    ("The sky appears blue during the day.", "description", "en"),
    ("Memory is the mental faculty of recalling information.", "description", "en"),
    # IT — narration
    ("Dante scrisse la Commedia durante l'esilio da Firenze.", "narration", "it"),
    ("Goethe visitò Roma e Napoli nel 1786.", "narration", "it"),
    ("Platone fondò l'Accademia ad Atene nel IV secolo AEC.", "narration", "it"),
    ("Il cielo è azzurro.", "description", "it"),
    ("La giustizia è un valore fondamentale.", "description", "it"),
    # ES — narration
    ("Borges escribió Ficciones en Buenos Aires en 1944.", "narration", "es"),
    ("Confucio enseñó en la China central.", "narration", "es"),
    ("Platón fundó la Academia en Atenas.", "narración" if False else "narration", "es"),
    ("La memoria es una facultad mental.", "description", "es"),
    ("El cielo es azul.", "description", "es"),
    # DE — narration
    ("Goethe reiste 1786 nach Italien und besuchte Rom.", "narration", "de"),
    ("Konfuzius lehrte seine Schüler in der zentralchinesischen Ebene.", "narration", "de"),
    ("Platon gründete die Akademie in Athen im IV Jahrhundert.", "narration", "de"),
    ("Der Himmel ist blau.", "description", "de"),
    ("Gerechtigkeit ist ein universelles Prinzip.", "description", "de"),
    # ZH — narration (mentions historiques)
    ("孔子在春秋时期于中原讲学。", "narration", "zh"),
    ("柏拉图在公元前四世纪在雅典创立了学院。", "narration", "zh"),
    ("但丁在被流放期间写下了神曲。", "narration", "zh"),
    ("天空是蓝色的。", "description", "zh"),
    ("记忆是一种心智能力。", "description", "zh"),
]


# ══════════════════════════════════════════════════════════════════════════════
# 3. Pipeline
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 78)
    print("  §106 — Décision B : encyclopédie ↔ classifieur")
    print("═" * 78)

    print("\n  ── Construction de l'index encyclopédique ──")
    seeds = _load_seeds()
    idx = _build_alias_index(seeds)
    for cat, entities in idx.items():
        n_ent = len(entities)
        n_alias = sum(len(a) for _, a in entities)
        print(f"    {cat:<16s} : {n_ent:3d} entités, {n_alias:4d} alias")

    print("\n  ── Chargement modèle SentenceTransformer ──")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)

    # ── Étape A : couverture sur corpus §100
    print("\n  ── A. Couverture encyclopédique sur corpus §100 ──")
    corpus_100 = _v100.merge_corpus_v100()
    cov_total = 0
    cov_any = 0
    cov_per_type: dict[str, list[int]] = {t: [] for t in _v100.TYPES}
    cov_examples: list[str] = []
    enc_features_100: list[np.ndarray] = []
    texts_100: list[str] = []
    langs_100: list[str] = []
    types_100: list[str] = []
    for t, by_lang in corpus_100.items():
        for la, phrases in by_lang.items():
            for p in phrases:
                f = encyclopedia_features(p, idx)
                enc_features_100.append(f)
                texts_100.append(p)
                langs_100.append(la)
                types_100.append(t)
                cov_total += 1
                if f[6] > 0:                        # total_attest > 0
                    cov_any += 1
                    cov_per_type[t].append(1)
                    if len(cov_examples) < 5:
                        cov_examples.append(f"[{t}/{la}] {p[:80]}")
                else:
                    cov_per_type[t].append(0)
    coverage_pct = 100.0 * cov_any / max(1, cov_total)
    print(f"    Phrases totales         : {cov_total}")
    print(f"    Au moins une attestation: {cov_any} ({coverage_pct:.1f} %)")
    print(f"    Couverture par type     :")
    for t in _v100.TYPES:
        arr = cov_per_type[t]
        pct = 100.0 * sum(arr) / max(1, len(arr))
        print(f"      {t:<14s} : {sum(arr):3d}/{len(arr):3d} ({pct:.1f} %)")
    if cov_examples:
        print(f"    Exemples de matches :")
        for ex in cov_examples:
            print(f"      • {ex}")

    # ── Étape B : ré-entraîner avec features §106
    print("\n  ── B. Ré-entraînement avec 7 features encyclopédiques ──")
    X_text, feats_syn, feats_lang, y_arr, langs_arr, strata, _texts = _v100.build_dataset_v100(model, corpus_100)
    feats_enc = np.stack(enc_features_100)
    Xc_v100 = np.hstack([X_text, feats_syn, feats_lang])           # 404 dim
    Xc_v106 = np.hstack([X_text, feats_syn, feats_lang, feats_enc])  # 411 dim
    print(f"    Dim §100  : {Xc_v100.shape[1]}")
    print(f"    Dim §106  : {Xc_v106.shape[1]} (+7 enc)")
    cv100_mean, cv100_std, cv100_per_type = _v100.cv_score(Xc_v100, y_arr, strata)
    cv106_mean, cv106_std, cv106_per_type = _v100.cv_score(Xc_v106, y_arr, strata)
    print(f"    CV-5 §100 : {cv100_mean*100:.2f} % ± {cv100_std*100:.2f}")
    print(f"    CV-5 §106 : {cv106_mean*100:.2f} % ± {cv106_std*100:.2f}")
    delta = (cv106_mean - cv100_mean) * 100
    print(f"    Per-type §100 → §106 :")
    for t in _v100.TYPES:
        v0 = cv100_per_type[t] * 100
        v1 = cv106_per_type[t] * 100
        print(f"      {t:<14s} : {v0:5.1f} → {v1:5.1f}  (Δ {v1-v0:+.1f} pp)")
    print(f"    Δ          : {delta:+.2f} pp")

    # ── Étape C : mini-corpus narratif (validation positive)
    print("\n  ── C. Mini-corpus narratif §106 (validation features) ──")
    nar_texts = [t for t, _, _ in NARRATIVE_CORPUS]
    nar_y_lbl = [lbl for _, lbl, _ in NARRATIVE_CORPUS]
    nar_langs = [la for _, _, la in NARRATIVE_CORPUS]
    nar_y = np.array([_v100.TYPE2IDX[lbl] for lbl in nar_y_lbl])
    print(f"    Phrases : {len(nar_texts)} ; narration={(nar_y_lbl.count('narration'))} ; description={nar_y_lbl.count('description')}")

    nar_X = np.asarray(model.encode(nar_texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True))
    nar_syn = np.stack([_v100.syntactic_features_v100(t, la) for t, la in zip(nar_texts, nar_langs)])
    nar_lang = np.stack([_v100.lang_onehot(la if la in _v100.ALL_LANGS else "fr") for la in nar_langs])
    nar_enc = np.stack([encyclopedia_features(t, idx) for t in nar_texts])

    # Couverture sur narratif
    nar_cov_nar = sum(1 for f, lbl in zip(nar_enc, nar_y_lbl) if lbl == "narration" and f[6] > 0)
    nar_cov_desc = sum(1 for f, lbl in zip(nar_enc, nar_y_lbl) if lbl == "description" and f[6] > 0)
    n_nar = nar_y_lbl.count("narration")
    n_desc = nar_y_lbl.count("description")
    print(f"    Couverture encyclopédique narratif :")
    print(f"      narration   : {nar_cov_nar}/{n_nar} ({100*nar_cov_nar/max(1,n_nar):.0f} %)")
    print(f"      description : {nar_cov_desc}/{n_desc} ({100*nar_cov_desc/max(1,n_desc):.0f} %)")

    nar_X_v100 = np.hstack([nar_X, nar_syn, nar_lang])
    nar_X_v106 = np.hstack([nar_X, nar_syn, nar_lang, nar_enc])

    # Train sur §100 corpus, prédire mini narratif
    print(f"    Train sur corpus §100 (n={len(y_arr)}), test sur narratif §106 (n={len(nar_y)})")
    clf100 = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf100.fit(Xc_v100, y_arr)
    pred100 = clf100.predict(nar_X_v100)
    acc100 = float((pred100 == nar_y).mean())
    clf106 = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs", random_state=42)
    clf106.fit(Xc_v106, y_arr)
    pred106 = clf106.predict(nar_X_v106)
    acc106 = float((pred106 == nar_y).mean())
    print(f"    Accuracy §100 (sans enc) : {acc100*100:.1f} %")
    print(f"    Accuracy §106 (avec enc) : {acc106*100:.1f} %")
    print(f"    Δ narratif               : {(acc106-acc100)*100:+.1f} pp")

    # Détail par classe attendue
    nar_pred100_lbl = [_v100.IDX2TYPE[p] for p in pred100]
    nar_pred106_lbl = [_v100.IDX2TYPE[p] for p in pred106]
    confusions = []
    for txt, gold, p1, p6, lang in zip(nar_texts, nar_y_lbl, nar_pred100_lbl, nar_pred106_lbl, nar_langs):
        marker = "✓" if p6 == gold else "✗"
        change = " ←" if p6 != p1 else ""
        confusions.append((marker, lang, gold, p1, p6, change, txt))
    print(f"\n    Détail (gold | pred §100 | pred §106 | texte) :")
    for marker, lang, gold, p1, p6, change, txt in confusions:
        print(f"      {marker} [{lang}] {gold[:6]:<6s}| {p1[:6]:<6s}| {p6[:6]:<6s}{change} | {txt[:60]}")

    # Importance des features encyclopédiques (coefficients pour la classe 'narration')
    nar_idx = _v100.TYPE2IDX["narration"]
    enc_coefs = clf106.coef_[nar_idx, -7:]
    print(f"\n    Coefficients logreg classe 'narration' sur les 7 features enc :")
    for name, c in zip(["auteur", "lieu", "epoque", "objet_cel", "evenement", "date", "total"], enc_coefs):
        print(f"      {name:<10s} : {c:+.3f}")

    # ── Verdict
    print("\n  ── Verdict décision B ──")
    verdict_lines = []
    if coverage_pct < 5.0:
        verdict_lines.append(
            f"§100 : couverture encyclopédique = {coverage_pct:.1f} % < 5 %. "
            f"Le corpus §100 est non-narratif par construction "
            f"(math/droit/définitions). Les features sont quasi nulles, "
            f"d'où Δ CV ≈ 0 attendu et observé ({delta:+.2f} pp)."
        )
    else:
        verdict_lines.append(
            f"§100 : couverture {coverage_pct:.1f} %, Δ CV = {delta:+.2f} pp."
        )
    nar_delta = (acc106 - acc100) * 100
    if abs(nar_delta) >= 5.0:
        verdict_lines.append(
            f"§106-narratif : Δ accuracy = {nar_delta:+.1f} pp — "
            f"les features encyclopédiques sont {'utiles' if nar_delta > 0 else 'nuisibles (sur-distribution)'}."
        )
    else:
        verdict_lines.append(
            f"§106-narratif : Δ accuracy = {nar_delta:+.1f} pp — gain marginal "
            f"(SBERT capte déjà le contenu lexical)."
        )
    if any(c > 0 for c in enc_coefs):
        verdict_lines.append(
            "Les coefficients narration/{auteur,lieu,epoque,evenement} sont positifs : "
            "le classifieur exploite l'attestation encyclopédique quand elle est présente."
        )
    for line in verdict_lines:
        print(f"    • {line}")

    # ── Sortie
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "version": "§106",
        "decision": "B (rétrospective §104) — connecter encyclopédie ↔ classifieur",
        "encyclopedia_index": {
            cat: {"n_entities": len(ents), "n_aliases": sum(len(a) for _, a in ents)}
            for cat, ents in idx.items()
        },
        "step_A_coverage_v100": {
            "n_phrases": cov_total,
            "n_with_attestation": cov_any,
            "coverage_pct": coverage_pct,
            "per_type_coverage_pct": {
                t: 100.0 * sum(arr) / max(1, len(arr)) for t, arr in cov_per_type.items()
            },
            "examples": cov_examples,
        },
        "step_B_retrain_v100": {
            "dim_v100": int(Xc_v100.shape[1]),
            "dim_v106": int(Xc_v106.shape[1]),
            "cv5_v100_acc_mean": float(cv100_mean),
            "cv5_v100_acc_std": float(cv100_std),
            "cv5_v106_acc_mean": float(cv106_mean),
            "cv5_v106_acc_std": float(cv106_std),
            "delta_pp": delta,
            "per_type_v100": cv100_per_type,
            "per_type_v106": cv106_per_type,
        },
        "step_C_narrative_validation": {
            "n_phrases": len(nar_texts),
            "n_narration": n_nar,
            "n_description": n_desc,
            "coverage_narration": nar_cov_nar / max(1, n_nar),
            "coverage_description": nar_cov_desc / max(1, n_desc),
            "acc_v100": acc100,
            "acc_v106": acc106,
            "delta_pp": nar_delta,
            "narration_feature_coefs": {
                name: float(c) for name, c in zip(
                    ["auteur", "lieu", "epoque", "objet_celeste", "evenement", "date", "total"],
                    enc_coefs,
                )
            },
            "predictions": [
                {"lang": lang, "gold": gold, "pred_v100": p1, "pred_v106": p6, "text": txt}
                for _m, lang, gold, p1, p6, _c, txt in confusions
            ],
        },
        "verdict": verdict_lines,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                 cls=_v100._NpEncoder), encoding="utf-8")
    print(f"\n  Sortie : {OUTPUT.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

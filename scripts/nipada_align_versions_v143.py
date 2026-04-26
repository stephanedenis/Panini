"""
§143 — Alignement multi-versions phrase-à-phrase (cross-lingual).

Approche : char-3gram TF-IDF + cosinus (réutilisé de §139). Les n-grammes
caractères capturent les cognats latins/romans/germaniques + noms propres,
même à travers le grec/arabe via translittération.

Cas de test : 5 fragments de Lucrèce DRN (latin) avec leurs traductions
canoniques alignées en français et en anglais. Pour chaque paire de
langues (lat↔fra, lat↔eng, fra↔eng), on calcule la matrice cosinus 5×5
et on mesure le taux de correspondance argmax-diagonale.

Métrique principale : alignment_accuracy = (# argmax correct) / (# total).
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Réutilise §139 char-3gram TF-IDF
SPEC_V139 = importlib.util.spec_from_file_location(
    "nipada_v139", ROOT / "scripts" / "nipada_lightclf_v139.py")
v139 = importlib.util.module_from_spec(SPEC_V139)
sys.modules["nipada_v139"] = v139
SPEC_V139.loader.exec_module(v139)


# ----------------------------------------------------------------------------
# Corpus aligné : 5 passages canoniques de Lucrèce DRN, en 3 langues
# ----------------------------------------------------------------------------
# Chaque clé = passage_id ; chaque valeur = {lat, fra, eng}

ALIGNED = {
    "DRN_I_62": {
        "lat": ("Humana ante oculos foede cum vita iaceret in terris "
                "oppressa gravi sub religione."),
        "fra": ("La vie humaine gisait honteusement sur la terre, "
                "écrasée sous le poids de la religion."),
        "eng": ("Human life lay foully grovelling upon the earth, "
                "crushed beneath the heavy weight of religion."),
    },
    "DRN_I_146": {
        "lat": ("Hunc terrorem animi tenebrasque necessest non radii "
                "solis discutiant, sed naturae species ratioque."),
        "fra": ("Cette terreur de l'âme et ces ténèbres, ce ne sont pas "
                "les rayons du soleil qui peuvent les dissiper, mais "
                "l'aspect et la raison de la nature."),
        "eng": ("This terror of the mind and these shadows must be "
                "scattered not by the rays of the sun but by the aspect "
                "and the law of nature."),
    },
    "DRN_I_215": {
        "lat": "Nullam rem e nihilo gigni divinitus umquam.",
        "fra": "Rien ne naît jamais de rien par une volonté divine.",
        "eng": "Nothing is ever begotten of nothing by divine power.",
    },
    "DRN_II_991": {
        "lat": ("Caelesti sumus omnes semine oriundi; omnibus ille idem "
                "pater est."),
        "fra": ("Nous sommes tous issus d'une semence céleste ; pour "
                "tous, le même est le père."),
        "eng": ("We are all sprung from a celestial seed; for all there "
                "is the same father."),
    },
    "DRN_III_830": {
        "lat": ("Nil igitur mors est ad nos neque pertinet hilum, "
                "quandoquidem natura animi mortalis habetur."),
        "fra": ("La mort donc n'est rien pour nous et ne nous touche en "
                "rien, puisque la nature de l'âme est tenue pour mortelle."),
        "eng": ("Therefore death is nothing to us nor concerns us at all, "
                "since the nature of the mind is held to be mortal."),
    },
}


# ----------------------------------------------------------------------------
# Alignement par cosinus de char-3grams TF-IDF
# ----------------------------------------------------------------------------

def build_tfidf_vectors(texts: list[str]):
    """Construit les vecteurs TF-IDF (dict) pour une liste de textes."""
    ngrams_per_doc = [v139.char_ngrams(t, n=3) for t in texts]
    idf = v139.build_idf(ngrams_per_doc)
    vecs = [v139.tfidf(ng, idf) for ng in ngrams_per_doc]
    return vecs, idf


def align(src_texts: list[str], tgt_texts: list[str]) -> tuple[list[int], list[list[float]]]:
    """Retourne (assignments, matrice_cosinus). assignments[i] = j tq tgt[j]
    correspond le mieux à src[i] (argmax cosinus)."""
    # On construit un IDF commun aux deux côtés pour rester comparable
    all_texts = src_texts + tgt_texts
    vecs, _ = build_tfidf_vectors(all_texts)
    src_vecs = vecs[: len(src_texts)]
    tgt_vecs = vecs[len(src_texts):]

    matrix = []
    assignments = []
    for sv in src_vecs:
        row = [v139.cosine(sv, tv) for tv in tgt_vecs]
        matrix.append(row)
        assignments.append(int(max(range(len(row)), key=lambda j: row[j])))
    return assignments, matrix


def evaluate_pair(lang_a: str, lang_b: str) -> dict:
    pids = list(ALIGNED.keys())
    src = [ALIGNED[p][lang_a] for p in pids]
    tgt = [ALIGNED[p][lang_b] for p in pids]
    # Vérité terrain : i↔i (ordre identique)
    assignments, matrix = align(src, tgt)
    correct = sum(1 for i, j in enumerate(assignments) if i == j)
    diag = [matrix[i][i] for i in range(len(pids))]
    off_diag = [matrix[i][j] for i in range(len(pids))
                 for j in range(len(pids)) if i != j]
    return {
        "pair": f"{lang_a}↔{lang_b}",
        "n_pairs": len(pids),
        "correct": correct,
        "accuracy": round(correct / len(pids), 3),
        "mean_diagonal_cos": round(sum(diag) / len(diag), 4),
        "mean_offdiag_cos": round(sum(off_diag) / len(off_diag), 4)
                              if off_diag else 0.0,
        "separation": round(sum(diag) / len(diag) - (sum(off_diag) / len(off_diag) if off_diag else 0.0), 4),
        "assignments": dict(zip(pids, [pids[a] for a in assignments])),
        "matrix": [[round(v, 3) for v in row] for row in matrix],
    }


def main():
    pairs = [("lat", "fra"), ("lat", "eng"), ("fra", "eng")]
    results = [evaluate_pair(a, b) for a, b in pairs]

    n_pairs_total = sum(r["n_pairs"] for r in results)
    n_correct_total = sum(r["correct"] for r in results)
    accuracy_global = round(n_correct_total / n_pairs_total, 3)

    summary = {
        "version": "v143",
        "context": ("§143 — Alignement multi-versions phrase-à-phrase via "
                     "char-3gram TF-IDF + cosinus (réutilise §139)"),
        "test_corpus": "Lucrèce DRN — 5 passages canoniques en {lat, fra, eng}",
        "n_passages": len(ALIGNED),
        "n_languages": 3,
        "pairs": [r["pair"] for r in results],
        "accuracy_global": accuracy_global,
        "results_per_pair": results,
        "verdict": ("OK — alignement déterministe sans modèle neural ni "
                     "dictionnaire bilingue ; les n-grammes caractères "
                     "capturent les cognats lat→fra/eng et les noms propres."
                     if accuracy_global >= 0.8 else
                     "KO — alignement char-3gram insuffisant entre langues "
                     "trop éloignées ; envisager un alignement par lemmes "
                     "ou par dictionnaire bilingue minimal."),
        "limitations": [
            "Couvre uniquement scripts latins (lat/fra/eng) ; "
            "alignement grc/san/lzh/ara exigerait translittération préalable.",
            "5 passages = échantillon minimal ; valider à 80+ passages "
            "lors de §144 (annotation gold).",
            "Pas de pondération sémantique : un passage très court "
            "(DRN I.215) peut être confondu avec un voisin court.",
        ],
    }
    out = ROOT / "research" / "nipada" / "falsification" / "nipada_v143_alignment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    print(f"§143 — Alignement multi-versions phrase-à-phrase")
    print(f"  Passages          : {len(ALIGNED)}")
    print(f"  Paires de langues : {len(pairs)}")
    for r in results:
        print(f"  {r['pair']}  acc={r['accuracy']}  "
              f"diag={r['mean_diagonal_cos']}  off={r['mean_offdiag_cos']}  "
              f"sep={r['separation']}")
    print(f"  Global accuracy   : {accuracy_global}")
    print(f"→ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

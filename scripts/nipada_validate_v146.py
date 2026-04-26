"""
§146 — Validation prédictive : stabilité de la signature V14 et
classification par tradition.

Objectifs :
  1. **Cohérence intra-œuvre** : pour chaque œuvre (5 fragments),
     mesurer la variance de la signature V14 vs la variance moyenne
     entre œuvres. Hypothèse : intra < inter (signature stable
     par auteur).
  2. **Discriminabilité par tradition** : grouper les 10 œuvres
     en 4 traditions philosophiques :
       - GRECO_LAT_MATERIAL   = {Lucrèce, Épicure, Démocrite}
       - SCEPT                = {Sextus}
       - INDIAN_MATERIAL      = {Cārvāka}
       - CHINESE_MATERIAL     = {Wang Chong}
       - ISLAMIC_RATIONALIST  = {Ibn al-Rāwandī}
       - MODERN_WESTERN       = {Hume, Holbach, Feuerbach}
     → moyenner les signatures par tradition, mesurer la séparation.
  3. **Hold-out prédictif** : LOOCV — pour chaque œuvre, retirer
     ses 5 fragments, entraîner le centroïde de chaque tradition
     sur les fragments restants, prédire la tradition de chaque
     fragment hold-out. Comparer à la baseline (majoritaire = MODERN
     puisque 3 œuvres : 15/50 = 30 %).

Définition signature V14 d'une phrase : vecteur binaire 14-dim
(présence/absence de chaque atome) produit par §145.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

spec_v145 = importlib.util.spec_from_file_location(
    "_v145", ROOT / "scripts" / "nipada_v14_multiling_v145.py")
_v145 = importlib.util.module_from_spec(spec_v145)
sys.modules["_v145"] = _v145
spec_v145.loader.exec_module(_v145)

V14 = _v145.V14
annotate = _v145.annotate

# Mapping œuvre → tradition
TRADITIONS = {
    "lucretius_drn":          "GRECO_LAT_MATERIAL",
    "epicurus_letters":       "GRECO_LAT_MATERIAL",
    "democritus_fragments":   "GRECO_LAT_MATERIAL",
    "sextus_pyrrho":          "SCEPT",
    "carvaka_fragments":      "INDIAN_MATERIAL",
    "wang_chong_lunheng":     "CHINESE_MATERIAL",
    "ibn_rawandi_fragments":  "ISLAMIC_RATIONALIST",
    "hume_dialogues":         "MODERN_WESTERN",
    "holbach_systeme":        "MODERN_WESTERN",
    "feuerbach_wesen":        "MODERN_WESTERN",
}


def signature_vec(atoms: set[str]) -> list[float]:
    return [1.0 if a in atoms else 0.0 for a in V14]


def vec_mean(vecs: list[list[float]]) -> list[float]:
    n = len(vecs)
    if n == 0:
        return [0.0] * len(V14)
    return [sum(v[i] for v in vecs) / n for i in range(len(V14))]


def cosine(a: list[float], b: list[float]) -> float:
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def euclid(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def main():
    # Charge tous les fragments + signatures
    by_work: dict[str, list[dict]] = {}
    for work_dir in sorted(CORPUS_DIR.iterdir()):
        fp = work_dir / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                f = json.loads(line)
                atoms = annotate(f["text"], f["lang"])
                f["sig"] = signature_vec(atoms)
                f["atoms"] = sorted(atoms)
                by_work.setdefault(f["work_id"], []).append(f)

    # 1. Cohérence intra-œuvre vs inter-œuvre
    work_centroids = {w: vec_mean([f["sig"] for f in fs])
                       for w, fs in by_work.items()}

    intra_dist = {}  # œuvre → distance moyenne fragment ↔ centroïde de l'œuvre
    for w, fs in by_work.items():
        c = work_centroids[w]
        intra_dist[w] = round(sum(euclid(f["sig"], c) for f in fs) / len(fs), 3)

    inter_dist_avg = []
    works = sorted(by_work.keys())
    for i, w1 in enumerate(works):
        for w2 in works[i + 1:]:
            inter_dist_avg.append(euclid(work_centroids[w1], work_centroids[w2]))
    inter_mean = round(sum(inter_dist_avg) / len(inter_dist_avg), 3)
    intra_mean = round(sum(intra_dist.values()) / len(intra_dist), 3)
    separation_ratio = round(inter_mean / max(intra_mean, 1e-9), 3)

    # 2. Discriminabilité par tradition
    by_trad: dict[str, list[list[float]]] = {}
    for w, fs in by_work.items():
        trad = TRADITIONS[w]
        by_trad.setdefault(trad, []).extend(f["sig"] for f in fs)
    trad_centroids = {t: vec_mean(vs) for t, vs in by_trad.items()}

    trad_pairs = sorted(trad_centroids.keys())
    trad_dist_matrix = {}
    for t1 in trad_pairs:
        trad_dist_matrix[t1] = {}
        for t2 in trad_pairs:
            trad_dist_matrix[t1][t2] = round(
                cosine(trad_centroids[t1], trad_centroids[t2]), 3)

    # 3. Hold-out LOOCV par œuvre → prédiction tradition par centroïde
    n_correct = 0
    n_total = 0
    confusion: dict[str, dict[str, int]] = {}
    per_work_acc = {}
    for held_work in works:
        held_trad = TRADITIONS[held_work]
        # Recalcule centroïdes traditionnels SANS l'œuvre tenue
        trad_train = {}
        for w, fs in by_work.items():
            if w == held_work:
                continue
            trad_train.setdefault(TRADITIONS[w], []).extend(f["sig"] for f in fs)
        trad_train_centroids = {t: vec_mean(vs) for t, vs in trad_train.items()}

        # Prédit chaque fragment hold-out
        n_w_correct = 0
        for f in by_work[held_work]:
            best_t = max(trad_train_centroids.keys(),
                          key=lambda t: cosine(f["sig"], trad_train_centroids[t]))
            confusion.setdefault(held_trad, {}).setdefault(best_t, 0)
            confusion[held_trad][best_t] += 1
            if best_t == held_trad:
                n_correct += 1
                n_w_correct += 1
            n_total += 1
        per_work_acc[held_work] = {
            "tradition": held_trad,
            "correct": n_w_correct,
            "n": len(by_work[held_work]),
            "accuracy": round(n_w_correct / len(by_work[held_work]), 3),
        }

    accuracy = round(n_correct / n_total, 3)

    # Baseline = classe majoritaire (MODERN_WESTERN, 15 frag / 50)
    trad_counts = {t: sum(len(by_work[w]) for w in works
                            if TRADITIONS[w] == t)
                    for t in trad_pairs}
    baseline_majority_class = max(trad_counts, key=trad_counts.get)
    baseline_acc = round(trad_counts[baseline_majority_class] / n_total, 3)

    summary = {
        "version": "v146",
        "context": ("§146 — Validation prédictive : stabilité signature V14 "
                     "+ hold-out LOOCV par œuvre + classification par tradition"),
        "n_fragments": n_total,
        "n_works": len(works),
        "n_traditions": len(trad_pairs),
        "atoms_v14": V14,
        "stability": {
            "intra_work_distance_avg": intra_mean,
            "inter_work_distance_avg": inter_mean,
            "separation_ratio": separation_ratio,
            "interpretation": ("OK — signature plus stable intra-œuvre "
                                "qu'inter-œuvre"
                                if separation_ratio > 1.0 else
                                "KO — pas de discriminabilité par œuvre"),
            "per_work_intra_distance": intra_dist,
        },
        "tradition_centroids": {t: [round(x, 3) for x in v]
                                  for t, v in trad_centroids.items()},
        "tradition_pairwise_cosine": trad_dist_matrix,
        "hold_out_loocv": {
            "n_total": n_total,
            "n_correct": n_correct,
            "accuracy": accuracy,
            "baseline_majority_class": baseline_majority_class,
            "baseline_accuracy": baseline_acc,
            "delta_vs_baseline": round(accuracy - baseline_acc, 3),
            "per_work": per_work_acc,
            "confusion_matrix": confusion,
        },
        "verdict": {
            "stability": ("OK" if separation_ratio > 1.0 else "KO"),
            "predictive": ("OK — accuracy > baseline + 15 pts"
                            if accuracy >= baseline_acc + 0.15 else
                            ("Marginal — accuracy > baseline mais Δ < 15 pts"
                             if accuracy > baseline_acc else
                             "KO — accuracy ≤ baseline majoritaire")),
        },
    }
    out = ROOT / "research" / "nipada" / "falsification" / "nipada_v146_validation.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    print(f"§146 — Validation prédictive")
    print(f"  Fragments        : {n_total}")
    print(f"  Œuvres / Trad.   : {len(works)} / {len(trad_pairs)}")
    print(f"  Intra-work dist  : {intra_mean}")
    print(f"  Inter-work dist  : {inter_mean}")
    print(f"  Sep ratio        : {separation_ratio}× ({'OK' if separation_ratio > 1.0 else 'KO'})")
    print(f"  Hold-out LOOCV   : {n_correct}/{n_total} = {accuracy}")
    print(f"  Baseline (maj.)  : {baseline_acc}  Δ = {accuracy - baseline_acc:+.3f}")
    print(f"  Per-work acc     :")
    for w, info in per_work_acc.items():
        print(f"    {w:30s} {info['tradition']:25s} {info['correct']}/{info['n']} = {info['accuracy']}")
    print(f"→ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

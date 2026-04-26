#!/usr/bin/env python3
"""
§155 — Phase D : signatures par bigrammes atomiques (co-occurrence
intra-fragment) + validation H1/H2/H3.

Hypothèse Phase D :
  Si chaque pensée philosophique est un MOTIF combinatoire d'atomes
  (RAPPORT+MODALITÉ → conditionnalité, ÊTRE+DIFFÉRENCE+ÉQUATION → identité,
  NOMBRE+ESPACE+OPÉRATION → mathématique, etc.), alors les **co-occurrences**
  d'atomes au sein d'un même fragment portent plus d'information que leurs
  fréquences marginales.

Méthode :
  1. Pour chaque fragment, extraire le SET d'atomes activés via §145.annotate.
  2. Pour chaque œuvre, agréger une matrice de co-occurrence 14×14
     symétrique : C[a][b] = nombre de fragments où a ET b co-apparaissent,
     normalisé par le nombre de fragments de l'œuvre.
  3. La signature d'œuvre = vecteur des C(14,2)=91 valeurs hors diagonale.
     (On stocke aussi la diagonale 14 pour comparaison avec §149.)
  4. Refaire H1 (Mann-Whitney), H2 (LOOCV tradition), H3 (OLS) +
     R²(d_graph seul) + permutation test.

Output : research/nipada/falsification/nipada_v155_bigrams.json
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v155_bigrams.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v145 = _load("nipada_v14_multiling_v145", SCRIPTS / "nipada_v14_multiling_v145.py")
_v150 = _load("nipada_validation_v150", SCRIPTS / "nipada_validation_v150.py")

annotate = _v145.annotate
V14 = _v150.V14
mann_whitney_u = _v150.mann_whitney_u
ols = _v150.ols
mean = _v150.mean
median = _v150.median


def _all_fragments() -> list[dict]:
    base = ROOT / "corpus" / "protoatheism"
    out = []
    for d in sorted(base.iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


# Index canonique des paires (i<j) → 91 paires
PAIR_KEYS = [(V14[i], V14[j]) for i in range(len(V14)) for j in range(i + 1, len(V14))]
PAIR_INDEX = {p: idx for idx, p in enumerate(PAIR_KEYS)}


def cooccurrence_signature(atoms_per_fragment: list[set[str]]) -> dict[str, float]:
    """Pour chaque paire (a<b), proportion de fragments où a ET b sont activés."""
    n = len(atoms_per_fragment)
    if n == 0:
        return {f"{a}|{b}": 0.0 for (a, b) in PAIR_KEYS}
    counts = {f"{a}|{b}": 0 for (a, b) in PAIR_KEYS}
    for atoms in atoms_per_fragment:
        ordered = [a for a in V14 if a in atoms]
        for a, b in itertools.combinations(ordered, 2):
            counts[f"{a}|{b}"] += 1
    return {k: v / n for k, v in counts.items()}


def cosine_dict(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return num / (na * nb)


def loocv_by_work_bigram(sigs: dict, traditions: dict) -> dict:
    """LOOCV : pour chaque œuvre, classifier par tradition selon le centroïde
    le plus proche (moyenne des autres œuvres de chaque tradition)."""
    works = list(sigs.keys())
    correct = 0
    confusion = []
    for held_out in works:
        true_trad = traditions[held_out]
        # Centroïdes par tradition (moyenne des sigs des œuvres restantes)
        centroids = {}
        members = {}
        for w in works:
            if w == held_out:
                continue
            t = traditions[w]
            members.setdefault(t, []).append(w)
        for t, ws in members.items():
            cent = {}
            for k in sigs[ws[0]].keys():
                cent[k] = sum(sigs[w][k] for w in ws) / len(ws)
            centroids[t] = cent
        # Argmax cosinus
        best_t = max(centroids.keys(), key=lambda t: cosine_dict(sigs[held_out], centroids[t]))
        ok = (best_t == true_trad)
        confusion.append({"work": held_out, "true": true_trad, "pred": best_t, "ok": ok})
        if ok:
            correct += 1
    return {"accuracy": round(correct / len(works), 4), "confusion": confusion}


def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}
    works_traditions = {wid: meta["works"][wid]["tradition_label"] for wid in proto_ids}

    # 1. Annoter tous les fragments
    frags = _all_fragments()
    atoms_by_work: dict[str, list[set[str]]] = {}
    for f in frags:
        atoms = annotate(f["text"], f["lang"])
        atoms_by_work.setdefault(f["work_id"], []).append(atoms)

    # 2. Signatures de co-occurrence par œuvre
    sigs_bigram: dict[str, dict[str, float]] = {}
    activation_rate: dict[str, dict[str, float]] = {}  # diagonale = fréquence d'activation
    for wid in proto_ids:
        afs = atoms_by_work.get(wid, [])
        sigs_bigram[wid] = cooccurrence_signature(afs)
        # taux d'activation par atome (singleton)
        activation_rate[wid] = {
            atom: (sum(1 for s in afs if atom in s) / max(1, len(afs)))
            for atom in V14
        }

    # 3. Construire les paires
    pairs = []
    for i, a in enumerate(proto_ids):
        for b in proto_ids[i + 1:]:
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_sig = 1.0 - cosine_dict(sigs_bigram[a], sigs_bigram[b])
            dyear = abs(works_year[a] - works_year[b])
            same_trad = 1.0 if works_traditions[a] == works_traditions[b] else 0.0
            pairs.append((a, b, d_graph, d_sig, dyear, same_trad))

    # 4. H1
    cutoff = median([p[2] for p in pairs])
    strong = [p[3] for p in pairs if p[2] <= cutoff]
    weak = [p[3] for p in pairs if p[2] > cutoff]
    u, p_val = mann_whitney_u(strong, weak)
    h1 = {
        "median_d_graph": round(cutoff, 4),
        "n_strong": len(strong),
        "n_weak": len(weak),
        "mean_dsig_strong": round(mean(strong), 4),
        "mean_dsig_weak": round(mean(weak), 4),
        "u": round(u, 4),
        "p_value_two_tailed": round(p_val, 4),
        "verdict": "OK" if (mean(strong) < mean(weak) and p_val < 0.05) else "KO",
    }

    # 5. H2 LOOCV
    loo = loocv_by_work_bigram(sigs_bigram, works_traditions)
    from collections import Counter
    trad_counts = Counter(works_traditions.values())
    baseline = max(trad_counts.values()) / sum(trad_counts.values())
    h2 = {
        "baseline_majority_acc": round(baseline, 4),
        "acc_bigram": loo["accuracy"],
        "delta_vs_baseline": round(loo["accuracy"] - baseline, 4),
        "verdict": "OK" if loo["accuracy"] >= baseline + 0.15 else "KO",
        "loocv": loo,
    }

    # 6. H3 OLS complet
    X4 = [[1.0, p[2], p[4] / 1000.0, p[5]] for p in pairs]
    y = [p[3] for p in pairs]
    beta4, r2_4 = ols(X4, y)
    # OLS d_graph seul (test crucial)
    X1 = [[1.0, p[2]] for p in pairs]
    beta1, r2_1 = ols(X1, y)
    h3 = {
        "ols_full": {
            "features": ["intercept", "d_graph", "dyear/1000", "same_trad"],
            "beta": [round(b, 4) for b in beta4],
            "r2": round(r2_4, 4),
        },
        "ols_d_graph_only": {
            "features": ["intercept", "d_graph"],
            "beta": [round(b, 4) for b in beta1],
            "r2": round(r2_1, 4),
        },
        "verdict_full": "OK" if r2_4 >= 0.30 else "KO",
        "verdict_d_graph_only": "OK" if r2_1 >= 0.20 else "KO",
    }

    # 7. Permutation test sur R²(d_graph seul)
    rng = random.Random(42)
    n_perm = 2000
    ge = 0
    for _ in range(n_perm):
        y_shuf = y[:]
        rng.shuffle(y_shuf)
        _, r2_p = ols(X1, y_shuf)
        if r2_p >= r2_1:
            ge += 1
    p_perm = (ge + 1) / (n_perm + 1)

    # 8. Top bigrammes les plus discriminants (var entre œuvres)
    top_bigrams = []
    for key in PAIR_KEYS:
        k = f"{key[0]}|{key[1]}"
        vals = [sigs_bigram[w][k] for w in proto_ids]
        if not vals:
            continue
        m = sum(vals) / len(vals)
        var = sum((v - m) ** 2 for v in vals) / len(vals)
        top_bigrams.append((k, round(m, 4), round(var, 6)))
    top_bigrams.sort(key=lambda x: x[2], reverse=True)

    # Verdict final
    h1_ok = h1["verdict"] == "OK"
    h2_ok = h2["verdict"] == "OK"
    h3a_ok = h3["verdict_d_graph_only"] == "OK"
    go = (h1_ok or h2_ok) and h3a_ok
    verdict = {
        "H1": h1["verdict"],
        "H2": h2["verdict"],
        "H3_full": h3["verdict_full"],
        "H3_d_graph_only": h3["verdict_d_graph_only"],
        "permutation_p_one_tailed": round(p_perm, 4),
        "go_phase_religieuse_revised": "GO" if go else "NO-GO",
    }

    payload = {
        "version": "v155",
        "step": "§155 — Phase D : bigrammes atomiques (co-occurrence intra-fragment)",
        "n_pair_keys": len(PAIR_KEYS),
        "activation_rate_per_work": activation_rate,
        "bigram_signatures": sigs_bigram,
        "H1": h1,
        "H2": h2,
        "H3": h3,
        "permutation_test": {
            "observed_R2_d_graph_only": round(r2_1, 4),
            "n_permutations": n_perm,
            "p_value_one_tailed": round(p_perm, 4),
        },
        "top_10_most_variable_bigrams": [
            {"pair": k, "mean": m, "variance": v} for k, m, v in top_bigrams[:10]
        ],
        "verdict": verdict,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §155 — bigrammes écrits : {OUT}")
    print()
    print("─── H1 stratification (Mann-Whitney) ───")
    print(f"  d_sig forte = {h1['mean_dsig_strong']:.4f}  vs  faible = {h1['mean_dsig_weak']:.4f}")
    print(f"  p two-tailed = {h1['p_value_two_tailed']}  → {h1['verdict']}")
    print()
    print("─── H2 LOOCV par tradition ───")
    print(f"  baseline = {baseline:.2f}  acc = {h2['acc_bigram']}  Δ = {h2['delta_vs_baseline']:+}  → {h2['verdict']}")
    print()
    print("─── H3 OLS ───")
    print(f"  full (4 var) : β = {h3['ols_full']['beta']}  R² = {h3['ols_full']['r2']}")
    print(f"  d_graph seul : β = {h3['ols_d_graph_only']['beta']}  R² = {h3['ols_d_graph_only']['r2']}")
    print(f"  permutation p (one-tailed) = {p_perm:.4f}")
    print()
    print("─── Top 5 bigrammes les plus variables ───")
    for k, m, v in top_bigrams[:5]:
        print(f"  {k:40s}  mean={m:.4f}  var={v}")
    print()
    print(f"═══ VERDICT §155 ═══")
    print(f"  H1={h1['verdict']}  H2={h2['verdict']}  H3_full={h3['verdict_full']}  H3_d_graph_seul={h3['verdict_d_graph_only']}")
    print(f"  → Phase religieuse : **{verdict['go_phase_religieuse_revised']}**")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
§160 — Refaire H1/H2/H3 sur le graphe v159 (enrichi) avec les 3 signatures
disponibles (lex §149, dense §151, bigram §155).

Test crucial : R²(d_graph SEUL) sur le nouveau graphe, avec permutation.

Output : research/nipada/falsification/nipada_v160_validation_graph_v2.json
"""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v160_validation_graph_v2.json"

GRAPH_V2_PATH = RES_DIR / "nipada_v159_inheritance_graph_v2.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"
DECOMP_PATH = RES_DIR / "nipada_v149_decomposition.json"
DENSE_PATH = RES_DIR / "nipada_v151_dense_signatures.json"
BIGRAM_PATH = RES_DIR / "nipada_v155_bigrams.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v150 = _load("nipada_validation_v150", SCRIPTS / "nipada_validation_v150.py")
V14 = _v150.V14
cosine = _v150.cosine
mann_whitney_u = _v150.mann_whitney_u
ols = _v150.ols
loocv_by_work = _v150.loocv_by_work
mean = _v150.mean
median = _v150.median


def cosine_dict(a: dict, b: dict) -> float:
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if (na > 0 and nb > 0) else 0.0


def evaluate(name: str, sigs: dict, proto_ids: list, graph: dict,
             works_year: dict, works_trad: dict, cos_func) -> dict:
    """Évalue H1/H2/H3 d'une représentation contre le graphe."""
    pairs = []
    for i, a in enumerate(proto_ids):
        for b in proto_ids[i + 1:]:
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_sig = 1.0 - cos_func(sigs[a], sigs[b])
            dyear = abs(works_year[a] - works_year[b])
            same_trad = 1.0 if works_trad[a] == works_trad[b] else 0.0
            pairs.append((a, b, d_graph, d_sig, dyear, same_trad))

    # H1
    cutoff = median([p[2] for p in pairs])
    strong = [p[3] for p in pairs if p[2] <= cutoff]
    weak = [p[3] for p in pairs if p[2] > cutoff]
    u, p_h1 = mann_whitney_u(strong, weak)

    # H3 OLS complet
    X4 = [[1.0, p[2], p[4] / 1000.0, p[5]] for p in pairs]
    y = [p[3] for p in pairs]
    beta4, r2_4 = ols(X4, y)

    # H3 OLS d_graph seul
    X1 = [[1.0, p[2]] for p in pairs]
    beta1, r2_1 = ols(X1, y)

    # Permutation test sur R²(d_graph seul)
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

    return {
        "name": name,
        "n_pairs": len(pairs),
        "H1_mann_whitney": {
            "median_d_graph": round(cutoff, 4),
            "mean_dsig_strong": round(mean(strong), 4),
            "mean_dsig_weak": round(mean(weak), 4),
            "p_two_tailed": round(p_h1, 4),
            "verdict": "OK" if (mean(strong) < mean(weak) and p_h1 < 0.05) else "KO",
        },
        "H3_full": {
            "beta": [round(b, 4) for b in beta4],
            "r2": round(r2_4, 4),
        },
        "H3_d_graph_only": {
            "beta": [round(b, 4) for b in beta1],
            "r2": round(r2_1, 4),
            "permutation_p_one_tailed": round(p_perm, 4),
            "verdict": "OK" if r2_1 >= 0.20 and p_perm < 0.05 else "KO",
        },
    }


def main() -> None:
    graph_v2 = json.loads(GRAPH_V2_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    decomp = json.loads(DECOMP_PATH.read_text(encoding="utf-8"))
    dense = json.loads(DENSE_PATH.read_text(encoding="utf-8"))
    bigram = json.loads(BIGRAM_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph_v2["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}
    works_trad = {wid: meta["works"][wid]["tradition_label"] for wid in proto_ids}

    sigs_lex = decomp["signatures_aggregated"]
    sigs_dense = dense["work_signatures_aggregated"]
    sigs_bigram = bigram["bigram_signatures"]

    # H2 LOOCV (indépendant du graphe — réutilise §150 logic)
    from collections import Counter
    trad_counts = Counter(works_trad.values())
    baseline = max(trad_counts.values()) / sum(trad_counts.values())

    loo_lex = loocv_by_work(sigs_lex, works_trad)
    # H2 sur dense et bigram nécessite cosine_dict
    def loocv_dict(sigs, traditions):
        works = list(sigs.keys())
        correct = 0
        for held_out in works:
            true_trad = traditions[held_out]
            members: dict = {}
            for w in works:
                if w == held_out:
                    continue
                members.setdefault(traditions[w], []).append(w)
            centroids = {}
            for t, ws in members.items():
                cent = {k: sum(sigs[w][k] for w in ws) / len(ws) for k in sigs[ws[0]].keys()}
                centroids[t] = cent
            best_t = max(centroids.keys(), key=lambda t: cosine_dict(sigs[held_out], centroids[t]))
            if best_t == true_trad:
                correct += 1
        return round(correct / len(works), 4)

    acc_lex = loo_lex["accuracy"]
    acc_dense = loocv_dict(sigs_dense, works_trad)
    acc_bigram = loocv_dict(sigs_bigram, works_trad)

    # Évaluations
    results = {
        "lex":    evaluate("lex", sigs_lex, proto_ids, graph_v2, works_year, works_trad, cosine),
        "dense":  evaluate("dense", sigs_dense, proto_ids, graph_v2, works_year, works_trad, cosine_dict),
        "bigram": evaluate("bigram", sigs_bigram, proto_ids, graph_v2, works_year, works_trad, cosine_dict),
    }

    # Comparaison v148 vs v159
    # (Reload §150 et §155 pour les R² baseline)
    v150 = json.loads((RES_DIR / "nipada_v150_validation.json").read_text(encoding="utf-8"))
    v152 = json.loads((RES_DIR / "nipada_v152_dense_validation.json").read_text(encoding="utf-8"))
    v155 = json.loads((RES_DIR / "nipada_v155_bigrams.json").read_text(encoding="utf-8"))
    v153 = json.loads((RES_DIR / "nipada_v153_diagnostic.json").read_text(encoding="utf-8"))

    comparison = {
        "R2_d_graph_only": {
            "lex_v148":    v153["summary"]["A_r2_d_graph_only"]["lex"]["r2"],
            "lex_v159":    results["lex"]["H3_d_graph_only"]["r2"],
            "dense_v148":  v153["summary"]["A_r2_d_graph_only"]["dense"]["r2"],
            "dense_v159":  results["dense"]["H3_d_graph_only"]["r2"],
            "bigram_v148": v155["H3"]["ols_d_graph_only"]["r2"],
            "bigram_v159": results["bigram"]["H3_d_graph_only"]["r2"],
        },
        "R2_full_4var": {
            "lex_v148":    v150["H3_ols_regression"]["ols_dsig"]["r2"],
            "lex_v159":    results["lex"]["H3_full"]["r2"],
            "dense_v148":  v152["H3_ols_regression_dense"]["ols_dense"]["r2"],
            "dense_v159":  results["dense"]["H3_full"]["r2"],
            "bigram_v148": v155["H3"]["ols_full"]["r2"],
            "bigram_v159": results["bigram"]["H3_full"]["r2"],
        },
    }

    payload = {
        "version": "v160",
        "step": "§160 — H1/H2/H3 sur graphe v2 (lex, dense, bigram)",
        "graph_used": "v159 (enrichi)",
        "n_pairs": results["lex"]["n_pairs"],
        "results_per_signature": results,
        "H2_loocv_summary": {
            "baseline_majority_acc": round(baseline, 4),
            "acc_lex": acc_lex,
            "acc_dense": acc_dense,
            "acc_bigram": acc_bigram,
        },
        "comparison_v148_vs_v159": comparison,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §160 — validation graphe v2 écrite : {OUT}")
    print()
    print("─── Comparaison R²(d_graph SEUL) v148 → v159 ───")
    for rep in ["lex", "dense", "bigram"]:
        old = comparison["R2_d_graph_only"][f"{rep}_v148"]
        new = comparison["R2_d_graph_only"][f"{rep}_v159"]
        delta = new - old
        marker = "↑" if delta > 0.005 else ("↓" if delta < -0.005 else "·")
        print(f"  {rep:7s}  {old:.4f} → {new:.4f}  Δ={delta:+.4f}  {marker}")
    print()
    print("─── R²(d_graph SEUL) v159 + permutation ───")
    for rep in ["lex", "dense", "bigram"]:
        r = results[rep]["H3_d_graph_only"]
        print(f"  {rep:7s}  R²={r['r2']:.4f}  p_perm={r['permutation_p_one_tailed']:.4f}  → {r['verdict']}")
    print()
    print("─── R²(modèle complet 4-var) v148 → v159 ───")
    for rep in ["lex", "dense", "bigram"]:
        old = comparison["R2_full_4var"][f"{rep}_v148"]
        new = comparison["R2_full_4var"][f"{rep}_v159"]
        delta = new - old
        print(f"  {rep:7s}  {old:.4f} → {new:.4f}  Δ={delta:+.4f}")


if __name__ == "__main__":
    main()

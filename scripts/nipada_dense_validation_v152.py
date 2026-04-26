#!/usr/bin/env python3
"""
§152 — Validation des signatures denses §151 sur le triplet H1/H2/H3.

Recopie la logique §150 mais en remplaçant les signatures lexicales-
fréquentielles par les signatures denses (cosinus vs prototypes V14).

But : voir si l'embedding sémantique multilingue lève la limitation lexicale
identifiée en §150 (où Δyear dominait d_graph).

Hypothèse à vérifier : si V14 capture le concept (pas le signifiant), la
signature dense devrait corréler plus fortement avec d_graph et moins avec
Δyear que la signature lexicale.

Output : research/nipada/falsification/nipada_v152_dense_validation.json
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v152_dense_validation.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"
DENSE_PATH = RES_DIR / "nipada_v151_dense_signatures.json"
LEX_PATH = RES_DIR / "nipada_v149_decomposition.json"
LEX_VAL_PATH = RES_DIR / "nipada_v150_validation.json"


# Réutilise les utilitaires de §150 par import dynamique
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


def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    dense = json.loads(DENSE_PATH.read_text(encoding="utf-8"))
    lex_val = json.loads(LEX_VAL_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    sigs_dense = dense["work_signatures_aggregated"]
    works_traditions = {wid: meta["works"][wid]["tradition_label"] for wid in proto_ids}
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}

    # Construire les paires
    pairs = []
    for i, a in enumerate(proto_ids):
        for b in proto_ids[i + 1:]:
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_sig = 1.0 - cosine(sigs_dense[a], sigs_dense[b])
            dyear = abs(works_year[a] - works_year[b])
            same_trad = 1.0 if works_traditions[a] == works_traditions[b] else 0.0
            pairs.append((a, b, d_graph, d_sig, dyear, same_trad))

    # H1
    d_graphs = [p[2] for p in pairs]
    cutoff = median(d_graphs)
    strong = [p[3] for p in pairs if p[2] <= cutoff]
    weak = [p[3] for p in pairs if p[2] > cutoff]
    u, p_val = mann_whitney_u(strong, weak)
    h1 = {
        "median_d_graph": round(cutoff, 4),
        "n_strong_transmission": len(strong),
        "n_weak_transmission": len(weak),
        "mean_dsig_strong_dense": round(mean(strong), 4),
        "mean_dsig_weak_dense": round(mean(weak), 4),
        "u_stat": round(u, 4),
        "p_value_two_tailed": round(p_val, 4),
        "verdict": "OK" if (mean(strong) < mean(weak) and p_val < 0.05) else "KO",
    }

    # H2 LOOCV par tradition
    loo_dense = loocv_by_work(sigs_dense, works_traditions)
    from collections import Counter
    trad_counts = Counter(works_traditions.values())
    majority_acc = max(trad_counts.values()) / sum(trad_counts.values())
    h2 = {
        "baseline_majority_acc": round(majority_acc, 4),
        "acc_dense_signature": loo_dense["accuracy"],
        "delta_dense_vs_baseline": round(loo_dense["accuracy"] - majority_acc, 4),
        "verdict": "OK" if loo_dense["accuracy"] >= majority_acc + 0.15 else "KO",
        "loocv_dense": loo_dense,
    }

    # H3 OLS
    X = [[1.0, p[2], p[4] / 1000.0, p[5]] for p in pairs]
    y_dense = [p[3] for p in pairs]
    beta, r2 = ols(X, y_dense)
    h3 = {
        "features": ["intercept", "d_graph", "dyear_per_1000y", "same_tradition"],
        "ols_dense": {"beta": [round(b, 4) for b in beta], "r2": round(r2, 4)},
        "interpretation": (
            f"d_dense ≈ {beta[0]:+.3f} {beta[1]:+.3f}·d_graph "
            f"{beta[2]:+.3f}·(Δyear/1000) {beta[3]:+.3f}·same_trad  "
            f"(R²={r2:.3f})"
        ),
        "verdict": "OK" if r2 >= 0.20 else "KO",
    }

    # OLS avec d_graph SEUL (sans Δyear) — test crucial
    X_graph_only = [[1.0, p[2]] for p in pairs]
    beta_go, r2_go = ols(X_graph_only, y_dense)
    h3_graph_only = {
        "features": ["intercept", "d_graph"],
        "beta": [round(b, 4) for b in beta_go],
        "r2": round(r2_go, 4),
        "interpretation": f"d_dense ≈ {beta_go[0]:+.3f} {beta_go[1]:+.3f}·d_graph  (R²={r2_go:.3f})",
    }

    # Comparaison vs §150 (lexical)
    lex_h1 = lex_val["H1_stratification"]
    lex_h2 = lex_val["H2_loocv_tradition"]
    lex_h3 = lex_val["H3_ols_regression"]

    comparison = {
        "H1_strong_vs_weak": {
            "lex": {
                "mean_strong": lex_h1["mean_dsig_strong"],
                "mean_weak": lex_h1["mean_dsig_weak"],
                "p": lex_h1["p_value_two_tailed"],
                "verdict": lex_h1["verdict"],
            },
            "dense": {
                "mean_strong": h1["mean_dsig_strong_dense"],
                "mean_weak": h1["mean_dsig_weak_dense"],
                "p": h1["p_value_two_tailed"],
                "verdict": h1["verdict"],
            },
        },
        "H2_loocv": {
            "lex_full": lex_h2["acc_full_signature"],
            "lex_refl": lex_h2["acc_reflexion_signature"],
            "dense": h2["acc_dense_signature"],
            "baseline": majority_acc,
        },
        "H3_ols_R2": {
            "lex": lex_h3["ols_dsig"]["r2"],
            "dense": h3["ols_dense"]["r2"],
            "dense_d_graph_only": r2_go,
        },
        "H3_beta_d_graph": {
            "lex": lex_h3["ols_dsig"]["beta"][1],
            "dense": h3["ols_dense"]["beta"][1],
        },
        "H3_beta_dyear": {
            "lex": lex_h3["ols_dsig"]["beta"][2],
            "dense": h3["ols_dense"]["beta"][2],
        },
    }

    # Verdict
    h1_ok = h1["verdict"] == "OK"
    h2_ok = h2["verdict"] == "OK"
    h3_ok = h3["verdict"] == "OK"
    go = h1_ok and (h2_ok or (r2_go >= 0.20))
    verdict = {
        "H1_dense": h1["verdict"],
        "H2_dense": h2["verdict"],
        "H3_dense": h3["verdict"],
        "R2_d_graph_only": round(r2_go, 4),
        "go_no_go_phase_religieuse_revised": "GO" if go else "NO-GO",
        "delta_R2_dense_vs_lex": round(r2 - lex_h3["ols_dsig"]["r2"], 4),
    }

    payload = {
        "version": "v152",
        "step": "§152 — validation signatures denses (sentence-transformers)",
        "H1_stratification_dense": h1,
        "H2_loocv_tradition_dense": h2,
        "H3_ols_regression_dense": h3,
        "H3_d_graph_only": h3_graph_only,
        "comparison_lex_vs_dense": comparison,
        "verdict": verdict,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §152 — validation dense écrite : {OUT}")
    print()
    print("─── Comparaison lex (§150) vs dense (§152) ───")
    print(f"  H1 d_sig forte vs faible :")
    print(f"    lex   : {lex_h1['mean_dsig_strong']:.3f} vs {lex_h1['mean_dsig_weak']:.3f}  p={lex_h1['p_value_two_tailed']}  → {lex_h1['verdict']}")
    print(f"    dense : {h1['mean_dsig_strong_dense']:.3f} vs {h1['mean_dsig_weak_dense']:.3f}  p={h1['p_value_two_tailed']}  → {h1['verdict']}")
    print(f"  H2 LOOCV par tradition (baseline {majority_acc:.2f}) :")
    print(f"    lex full      : acc {lex_h2['acc_full_signature']}  Δ {lex_h2['delta_full_vs_baseline']:+}")
    print(f"    lex reflexion : acc {lex_h2['acc_reflexion_signature']}  Δ {lex_h2['delta_refl_vs_baseline']:+}")
    print(f"    dense         : acc {h2['acc_dense_signature']}  Δ {h2['delta_dense_vs_baseline']:+}")
    print(f"  H3 OLS R² :")
    print(f"    lex            : R²={lex_h3['ols_dsig']['r2']}")
    print(f"    dense (4 var)  : R²={h3['ols_dense']['r2']}")
    print(f"    dense (d_graph seul) : R²={r2_go:.4f}  ←  test crucial")
    print(f"  β coefficients (signature dense) :")
    print(f"    {h3['interpretation']}")
    print()
    print(f"═══ VERDICT §152 ═══")
    print(f"  H1={h1['verdict']}  H2={h2['verdict']}  H3={h3['verdict']}")
    print(f"  R²(d_graph seul) sur signature dense = {r2_go:.4f}")
    print(f"  go/no-go phase religieuse révisé : **{verdict['go_no_go_phase_religieuse_revised']}**")


if __name__ == "__main__":
    main()

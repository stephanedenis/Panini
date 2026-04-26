#!/usr/bin/env python3
"""
§153 — Analyse approfondie : pourquoi dense fait pire que lex ?

Tests :

A. **R²(d_graph seul) lex vs dense** : isoler la contribution réelle de
   d_graph hors confound Δyear pour les deux signatures.
B. **Interpolation lex × dense** : tester si une combinaison λ·sig_lex +
   (1-λ)·sig_dense bat l'une des deux. Balayer λ ∈ [0,1] par pas de 0.1.
C. **Permutation test** sur le R² OLS d_graph seul (signature lex) : la
   valeur observée est-elle significativement différente de 0 sous H0 ?
D. **Variance par œuvre** : la signature dense est-elle pathologiquement
   plate (toutes les œuvres tombent dans une même bande étroite, expliquant
   l'absence de discrimination) ?

Output : research/nipada/falsification/nipada_v153_diagnostic.json
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
OUT = RES_DIR / "nipada_v153_diagnostic.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"
DENSE_PATH = RES_DIR / "nipada_v151_dense_signatures.json"
DECOMP_PATH = RES_DIR / "nipada_v149_decomposition.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v150 = _load("nipada_validation_v150", SCRIPTS / "nipada_validation_v150.py")
V14 = _v150.V14
cosine = _v150.cosine
ols = _v150.ols
mean = _v150.mean
stddev = _v150.stddev


def interpolate(lex: dict[str, float], dense: dict[str, float], lam: float) -> dict[str, float]:
    """Interpolation pondérée. Les deux signatures sont déjà dans des
    échelles différentes (lex L1-normalisée, dense cosinus brut). On
    normalise d'abord les deux à norme L2 = 1 pour les rendre comparables."""
    def l2_norm(d):
        n = math.sqrt(sum(v * v for v in d.values()))
        return {k: (v / n if n > 0 else 0.0) for k, v in d.items()}
    a = l2_norm(lex)
    b = l2_norm(dense)
    return {k: lam * a[k] + (1 - lam) * b[k] for k in V14}


def variance_per_atom(sigs: dict[str, dict[str, float]]) -> dict[str, float]:
    """Pour chaque atome, calcule la variance des valeurs entre les œuvres."""
    out = {}
    for atom in V14:
        vals = [sigs[w][atom] for w in sigs]
        out[atom] = round(stddev(vals) ** 2, 6)
    return out


def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    dense = json.loads(DENSE_PATH.read_text(encoding="utf-8"))
    decomp = json.loads(DECOMP_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    sigs_lex = decomp["signatures_aggregated"]
    sigs_dense = dense["work_signatures_aggregated"]
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}

    # Construire les paires
    def build_pairs(sigs: dict[str, dict[str, float]]):
        out = []
        for i, a in enumerate(proto_ids):
            for b in proto_ids[i + 1:]:
                ka, kb = (a, b) if a < b else (b, a)
                d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
                if d_graph is None:
                    continue
                d_sig = 1.0 - cosine(sigs[a], sigs[b])
                dyear = abs(works_year[a] - works_year[b])
                out.append((a, b, d_graph, d_sig, dyear))
        return out

    pairs_lex = build_pairs(sigs_lex)
    pairs_dense = build_pairs(sigs_dense)

    # ===== A. R²(d_graph seul) =====
    def r2_graph_only(pairs):
        X = [[1.0, p[2]] for p in pairs]
        y = [p[3] for p in pairs]
        beta, r2 = ols(X, y)
        return {"beta": [round(b, 4) for b in beta], "r2": round(r2, 4)}

    a_lex = r2_graph_only(pairs_lex)
    a_dense = r2_graph_only(pairs_dense)

    # ===== B. Interpolation =====
    interp_results = []
    for lam_int in range(0, 11):
        lam = lam_int / 10.0
        sigs_mix = {wid: interpolate(sigs_lex[wid], sigs_dense[wid], lam) for wid in proto_ids}
        pairs_mix = build_pairs(sigs_mix)
        # R² d_graph seul
        ro = r2_graph_only(pairs_mix)
        # R² complet (intercept, d_graph, dyear/1000)
        X = [[1.0, p[2], p[4] / 1000.0] for p in pairs_mix]
        y = [p[3] for p in pairs_mix]
        _, r2_full = ols(X, y)
        interp_results.append({
            "lambda": round(lam, 2),
            "r2_d_graph_only": ro["r2"],
            "r2_d_graph_plus_dyear": round(r2_full, 4),
            "beta_d_graph": ro["beta"][1],
        })

    best = max(interp_results, key=lambda r: r["r2_d_graph_only"])

    # ===== C. Permutation test sur R²(d_graph seul) lex =====
    rng = random.Random(42)
    observed = a_lex["r2"]
    y = [p[3] for p in pairs_lex]
    n_perm = 2000
    ge_count = 0
    for _ in range(n_perm):
        y_shuf = y[:]
        rng.shuffle(y_shuf)
        X = [[1.0, p[2]] for p in pairs_lex]
        _, r2_p = ols(X, y_shuf)
        if r2_p >= observed:
            ge_count += 1
    p_perm = (ge_count + 1) / (n_perm + 1)

    # ===== D. Variance par atome (signature plate ?) =====
    var_lex = variance_per_atom(sigs_lex)
    var_dense = variance_per_atom(sigs_dense)
    var_lex_total = round(sum(var_lex.values()), 6)
    var_dense_total = round(sum(var_dense.values()), 6)

    # ===== Synthèse =====
    summary = {
        "A_r2_d_graph_only": {
            "lex": a_lex,
            "dense": a_dense,
            "diagnosis": (
                "lex légèrement positif, dense quasi nul → la signature dense "
                "ne capture aucun signal de transmission une fois Δyear retiré"
                if a_lex["r2"] > a_dense["r2"] else "dense > lex (résultat inverse)"
            ),
        },
        "B_interpolation_lex_dense": {
            "best_lambda": best["lambda"],
            "best_r2_d_graph_only": best["r2_d_graph_only"],
            "trace": interp_results,
        },
        "C_permutation_test_lex_r2_d_graph_only": {
            "observed_r2": observed,
            "n_permutations": n_perm,
            "n_perm_R2_geq_observed": ge_count,
            "p_value_one_tailed": round(p_perm, 4),
            "verdict": (
                "significatif (p<0.05)" if p_perm < 0.05 else
                "non significatif (R² indistinguable de 0)"
            ),
        },
        "D_variance_per_atom": {
            "var_total_lex": var_lex_total,
            "var_total_dense": var_dense_total,
            "ratio_lex_over_dense": (
                round(var_lex_total / var_dense_total, 2)
                if var_dense_total > 0 else None
            ),
            "lex_per_atom": var_lex,
            "dense_per_atom": var_dense,
            "diagnosis": (
                "signature dense est plate (toutes œuvres dans une même bande "
                "étroite) → manque de pouvoir discriminant"
                if var_dense_total < var_lex_total else
                "signature dense est plus dispersée"
            ),
        },
    }

    payload = {
        "version": "v153",
        "step": "§153 — diagnostic approfondi lex vs dense + interpolation + permutation",
        "summary": summary,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §153 — diagnostic écrit : {OUT}")
    print()
    print("─── A. R²(d_graph seul) — confound Δyear retiré ───")
    print(f"  lex   : R² = {a_lex['r2']:.4f}  β_d_graph = {a_lex['beta'][1]:+.4f}")
    print(f"  dense : R² = {a_dense['r2']:.4f}  β_d_graph = {a_dense['beta'][1]:+.4f}")
    print()
    print("─── B. Interpolation lex (λ=1) ↔ dense (λ=0) ───")
    print("   λ    R²(d_graph seul)   R²(d_graph + Δyear)   β_d_graph")
    for r in interp_results:
        marker = " ←" if r["lambda"] == best["lambda"] else ""
        print(f"   {r['lambda']:.1f}   {r['r2_d_graph_only']:>+.4f}              "
              f"{r['r2_d_graph_plus_dyear']:>+.4f}             "
              f"{r['beta_d_graph']:>+.4f}{marker}")
    print()
    print("─── C. Permutation test (2000 perm) sur R²(d_graph seul, lex) ───")
    print(f"  observé = {observed:.4f}  |  p one-tailed = {p_perm:.4f}")
    print(f"  → {'significatif' if p_perm < 0.05 else 'NON significatif (R² lex compatible avec H0)'}")
    print()
    print("─── D. Variance totale par atome (somme σ²) ───")
    print(f"  lex   : σ²_total = {var_lex_total:.6f}")
    print(f"  dense : σ²_total = {var_dense_total:.6f}")
    if var_dense_total > 0:
        print(f"  ratio lex/dense = {var_lex_total / var_dense_total:.2f}×")


if __name__ == "__main__":
    main()

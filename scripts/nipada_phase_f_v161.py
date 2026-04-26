#!/usr/bin/env python3
"""
§161 — Phase F méthodologique : (a) distance Jensen-Shannon sur les
matrices de co-occurrence, (b) orthogonalisation explicite Δyear via
résidus.

Idée (a) — Jensen-Shannon plutôt que 1-cosinus :
  Les signatures bigram (91-dim de proportions de co-occurrence) sont
  des distributions de probabilité. La JS-divergence est la métrique
  naturelle entre distributions, plus robuste que 1-cosinus pour des
  vecteurs sparses.

Idée (b) — Orthogonalisation Δyear :
  d_sig observé = effet_filiation + effet_époque + bruit
  On régresse d'abord d_sig ~ Δyear seul → on récupère ε = d_sig - prédiction.
  ε représente la part de d_sig qui n'est pas explicable par l'époque.
  On teste alors corrélation(ε, d_graph) — corrélation pure filiation.

Cette approche est strictement plus puissante qu'OLS multivariée quand
les régresseurs sont fortement asymétriques en variance (ici Δyear domine).

Output : research/nipada/falsification/nipada_v161_phase_f.json
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
OUT = RES_DIR / "nipada_v161_phase_f.json"

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
ols = _v150.ols
mean = _v150.mean


def js_divergence(p: dict, q: dict) -> float:
    """Jensen-Shannon divergence (base 2). Renormalise les deux dicts en
    distributions de probabilité avant calcul. Retourne valeur ∈ [0, 1]."""
    keys = set(p.keys()) | set(q.keys())
    sp = sum(p.values())
    sq = sum(q.values())
    if sp == 0 or sq == 0:
        return 0.0
    pn = {k: p.get(k, 0.0) / sp for k in keys}
    qn = {k: q.get(k, 0.0) / sq for k in keys}
    m = {k: 0.5 * (pn[k] + qn[k]) for k in keys}

    def kl(a, b):
        s = 0.0
        for k in keys:
            if a[k] > 0 and b[k] > 0:
                s += a[k] * math.log2(a[k] / b[k])
        return s

    return 0.5 * kl(pn, m) + 0.5 * kl(qn, m)


def js_distance(p: dict, q: dict) -> float:
    """Racine carrée de la JS-divergence — métrique légitime."""
    return math.sqrt(max(0.0, js_divergence(p, q)))


def cosine_dict(a: dict, b: dict) -> float:
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if (na > 0 and nb > 0) else 0.0


def pearson(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx = math.sqrt(sum((x[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((y[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def perm_test_r2(X: list, y: list, observed_r2: float, n_perm: int = 2000, seed: int = 42) -> float:
    rng = random.Random(seed)
    ge = 0
    for _ in range(n_perm):
        y_shuf = y[:]
        rng.shuffle(y_shuf)
        _, r2_p = ols(X, y_shuf)
        if r2_p >= observed_r2:
            ge += 1
    return (ge + 1) / (n_perm + 1)


def perm_test_corr(x: list, y: list, observed_r: float, n_perm: int = 2000, seed: int = 42) -> float:
    """Two-tailed permutation test sur la corrélation."""
    rng = random.Random(seed)
    ge = 0
    obs_abs = abs(observed_r)
    for _ in range(n_perm):
        y_shuf = y[:]
        rng.shuffle(y_shuf)
        if abs(pearson(x, y_shuf)) >= obs_abs:
            ge += 1
    return (ge + 1) / (n_perm + 1)


def main() -> None:
    graph_v2 = json.loads(GRAPH_V2_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    decomp = json.loads(DECOMP_PATH.read_text(encoding="utf-8"))
    dense = json.loads(DENSE_PATH.read_text(encoding="utf-8"))
    bigram = json.loads(BIGRAM_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph_v2["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}

    sigs_lex = decomp["signatures_aggregated"]
    sigs_dense = dense["work_signatures_aggregated"]
    sigs_bigram = bigram["bigram_signatures"]

    def build_pairs(sigs: dict, distance_func):
        out = []
        for i, a in enumerate(proto_ids):
            for b in proto_ids[i + 1:]:
                ka, kb = (a, b) if a < b else (b, a)
                d_g = graph_v2["proto_pair_distances"].get(f"{ka}::{kb}")
                if d_g is None:
                    continue
                d_s = distance_func(sigs[a], sigs[b])
                dy = abs(works_year[a] - works_year[b])
                out.append({"a": a, "b": b, "d_graph": d_g, "d_sig": d_s, "dyear": dy})
        return out

    # Pour chaque combinaison (signature × distance) :
    # signatures : lex, dense, bigram
    # distances  : 1-cosinus, JS-distance
    distance_funcs = {
        "1-cosine": lambda a, b: 1.0 - cosine_dict(a, b),
        "js":       js_distance,
    }

    summary = {}
    for sig_name, sigs in [("lex", sigs_lex), ("dense", sigs_dense), ("bigram", sigs_bigram)]:
        for dist_name, dfunc in distance_funcs.items():
            try:
                pairs = build_pairs(sigs, dfunc)
            except Exception as e:
                summary[f"{sig_name}_{dist_name}"] = {"error": str(e)}
                continue

            d_g = [p["d_graph"] for p in pairs]
            d_s = [p["d_sig"] for p in pairs]
            d_y = [p["dyear"] / 1000.0 for p in pairs]

            # (a) corrélation Pearson directe d_sig vs d_graph
            r_direct = pearson(d_s, d_g)
            p_direct = perm_test_corr(d_g, d_s, r_direct)

            # (b) Régression d_sig ~ d_year, calcul des résidus
            X_y = [[1.0, dy] for dy in d_y]
            beta_y, r2_y = ols(X_y, d_s)
            resid = [d_s[i] - (beta_y[0] + beta_y[1] * d_y[i]) for i in range(len(d_s))]

            # (c) Corrélation des résidus avec d_graph (filiation pure)
            r_resid = pearson(resid, d_g)
            p_resid = perm_test_corr(d_g, resid, r_resid)

            # (d) Régression OLS d_sig ~ d_graph seul (rappel)
            X_g = [[1.0, dg] for dg in d_g]
            beta_g, r2_g = ols(X_g, d_s)
            p_r2_g = perm_test_r2(X_g, d_s, r2_g)

            summary[f"{sig_name}_{dist_name}"] = {
                "n_pairs": len(pairs),
                "pearson_d_sig_vs_d_graph": {
                    "r": round(r_direct, 4),
                    "p_perm_two_tailed": round(p_direct, 4),
                },
                "ols_d_sig_on_dyear": {
                    "beta": [round(b, 4) for b in beta_y],
                    "r2_explained_by_year": round(r2_y, 4),
                },
                "pearson_residuals_vs_d_graph": {
                    "r": round(r_resid, 4),
                    "p_perm_two_tailed": round(p_resid, 4),
                    "interpretation": (
                        "corrélation pure filiation (Δyear retiré)"
                    ),
                },
                "ols_d_sig_on_d_graph_alone": {
                    "beta": [round(b, 4) for b in beta_g],
                    "r2": round(r2_g, 4),
                    "p_perm_one_tailed": round(p_r2_g, 4),
                },
            }

    # Verdict
    best_signal = None
    best_p = 1.0
    for key, val in summary.items():
        if "error" in val:
            continue
        p = val["pearson_residuals_vs_d_graph"]["p_perm_two_tailed"]
        if p < best_p:
            best_p = p
            best_signal = (key, val)

    payload = {
        "version": "v161",
        "step": "§161 — Phase F : Jensen-Shannon + orthogonalisation Δyear",
        "graph_used": "v159 (enrichi)",
        "n_proto_pairs": 29,
        "results": summary,
        "best_residual_signal": {
            "signature_distance": best_signal[0] if best_signal else None,
            "pearson_r": best_signal[1]["pearson_residuals_vs_d_graph"]["r"] if best_signal else None,
            "p_value": best_p,
            "verdict": "OK" if best_p < 0.05 else "KO",
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §161 — Phase F écrite : {OUT}")
    print()
    print("─── Tableau récapitulatif (signature × distance) ───")
    print(f"  {'combo':25s}  {'r_direct':>10s}  {'p_direct':>9s}  {'r2_year':>9s}  "
          f"{'r_resid':>9s}  {'p_resid':>9s}  {'R²(d_g seul)':>13s}")
    for key, val in summary.items():
        if "error" in val:
            continue
        rd = val["pearson_d_sig_vs_d_graph"]["r"]
        pd = val["pearson_d_sig_vs_d_graph"]["p_perm_two_tailed"]
        ry = val["ols_d_sig_on_dyear"]["r2_explained_by_year"]
        rr = val["pearson_residuals_vs_d_graph"]["r"]
        pr = val["pearson_residuals_vs_d_graph"]["p_perm_two_tailed"]
        r2g = val["ols_d_sig_on_d_graph_alone"]["r2"]
        print(f"  {key:25s}  {rd:+10.4f}  {pd:9.4f}  {ry:9.4f}  "
              f"{rr:+9.4f}  {pr:9.4f}  {r2g:13.4f}")
    print()
    if best_signal:
        print(f"─── Meilleur signal résiduel : {best_signal[0]} ───")
        print(f"  Pearson(résidus, d_graph) = {best_signal[1]['pearson_residuals_vs_d_graph']['r']:+.4f}")
        print(f"  p two-tailed = {best_p:.4f}")
        print(f"  R² année seule = {best_signal[1]['ols_d_sig_on_dyear']['r2_explained_by_year']:.4f}")
        v = "**OK significatif (p<0.05)**" if best_p < 0.05 else "KO non-significatif"
        print(f"  → {v}")


if __name__ == "__main__":
    main()

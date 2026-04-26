#!/usr/bin/env python3
"""
§150 — Validation prédictive Phase B révisée (architecture composite).

Trois tests indépendants :

H1 — **Stratification par distance d'héritage** :
     les paires d'œuvres avec transmission forte (d_graph < median)
     ont-elles une similarité de signature significativement supérieure
     aux paires de transmission faible (d_graph > median) ?
     Test de Mann-Whitney implémentation simple (sum-of-ranks).

H2 — **Classification par tradition via REFLEXION** :
     le résiduel propre §149 discrimine-t-il mieux les 6 traditions
     qu'la signature complète ? Hold-out LOOCV par œuvre, classifieur
     centroïde nearest-tradition, comparaison sig vs reflexion.

H3 — **Régression multi-facteurs** :
     d_sig ≈ β₀ + β₁·d_graph + β₂·|Δyear|/1000 + β₃·same_tradition + ε
     Quels facteurs prédisent la similarité de signature, et avec quel
     poids ? OLS scalaire (4-dim, fermé).

Critère go/no-go §150 (révisé) :
- GO si H1 montre Mann-Whitney p < 0.05 (stratification réelle)
  ET au moins un de {H2, H3} apporte un signal non-trivial.
- NO-GO sinon → revoir l'extracteur V14 (passer aux embeddings denses ?
  passer à un sous-stratum argumentatif §149 alternatif ?).

Output : research/nipada/falsification/nipada_v150_validation.json
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
OUT = RES_DIR / "nipada_v150_validation.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
DECOMP_PATH = RES_DIR / "nipada_v149_decomposition.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v149 = _load("nipada_decomposition_v149", SCRIPTS / "nipada_decomposition_v149.py")
V14 = _v149.V14


# ---------- utilitaires ----------
def _vec(d: dict[str, float]) -> list[float]:
    return [d[a] for a in V14]


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    va, vb = _vec(a), _vec(b)
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(va, vb)) / (na * nb)


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def stddev(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def median(xs: list[float]) -> float:
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


# ---------- H1 : Mann-Whitney U ----------
def mann_whitney_u(group_a: list[float], group_b: list[float]) -> tuple[float, float]:
    """U statistic + approximation normale pour p (two-tailed).
    Implémentation directe (pas de scipy)."""
    combined = [(v, "a") for v in group_a] + [(v, "b") for v in group_b]
    combined.sort(key=lambda x: x[0])
    # Ranks moyens en cas d'égalité
    ranks: list[float] = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i
        while j + 1 < len(combined) and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0  # rangs 1-indexés
        for k in range(i, j + 1):
            ranks[k] = avg_rank
        i = j + 1
    rank_a = sum(ranks[k] for k in range(len(combined)) if combined[k][1] == "a")
    n_a = len(group_a)
    n_b = len(group_b)
    u_a = rank_a - n_a * (n_a + 1) / 2.0
    u = min(u_a, n_a * n_b - u_a)
    # Approximation normale (correction continuité)
    mu = n_a * n_b / 2.0
    sigma = math.sqrt(n_a * n_b * (n_a + n_b + 1) / 12.0)
    if sigma == 0:
        return u, 1.0
    z = (u - mu) / sigma
    # p two-tailed via approximation erfc
    p = math.erfc(abs(z) / math.sqrt(2))
    return u, p


# ---------- H3 : OLS multi-facteurs (4 régresseurs + intercept) ----------
def ols(X: list[list[float]], y: list[float]) -> tuple[list[float], float]:
    """OLS sur petite matrice (jusqu'à ~30 lignes, 5 colonnes).
    Résolution par équations normales : β = (XᵀX)⁻¹ Xᵀy."""
    n = len(X)
    p = len(X[0])
    # XᵀX (p×p)
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(p)] for a in range(p)]
    # Xᵀy
    Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(p)]
    # Inversion par Gauss-Jordan
    A = [row[:] + [Xty[a]] for a, row in enumerate(XtX)]
    for i in range(p):
        # pivot
        piv = A[i][i]
        if abs(piv) < 1e-12:
            for r in range(i + 1, p):
                if abs(A[r][i]) > 1e-12:
                    A[i], A[r] = A[r], A[i]
                    piv = A[i][i]
                    break
        if abs(piv) < 1e-12:
            return [0.0] * p, 0.0  # singulier
        for j in range(p + 1):
            A[i][j] /= piv
        for r in range(p):
            if r != i:
                f = A[r][i]
                for j in range(p + 1):
                    A[r][j] -= f * A[i][j]
    beta = [A[i][p] for i in range(p)]
    # R²
    y_hat = [sum(X[i][a] * beta[a] for a in range(p)) for i in range(n)]
    ss_res = sum((y[i] - y_hat[i]) ** 2 for i in range(n))
    ym = mean(y)
    ss_tot = sum((y[i] - ym) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return beta, r2


# ---------- H2 : LOOCV par tradition (centroïde) ----------
def loocv_by_work(sigs: dict[str, dict[str, float]],
                  works_traditions: dict[str, str]) -> dict:
    """Hold-out chaque œuvre, recalcule centroïdes traditions sur les autres,
    classifie par cosinus argmax. Retourne accuracy + matrice confusion."""
    proto_ids = list(sigs.keys())
    correct = 0
    confusion: dict[str, dict[str, int]] = {}
    detail = []
    traditions = sorted(set(works_traditions.values()))
    for held in proto_ids:
        true_t = works_traditions[held]
        # Centroïdes sur les 9 autres
        centroids: dict[str, dict[str, float]] = {}
        for t in traditions:
            members = [w for w in proto_ids if w != held and works_traditions[w] == t]
            if not members:
                continue
            cent = {a: 0.0 for a in V14}
            for m in members:
                for a in V14:
                    cent[a] += sigs[m][a]
            for a in V14:
                cent[a] /= len(members)
            centroids[t] = cent
        # Classifier le held
        scores = {t: cosine(sigs[held], c) for t, c in centroids.items()}
        pred_t = max(scores, key=scores.get)
        ok = (pred_t == true_t)
        correct += int(ok)
        confusion.setdefault(true_t, {}).setdefault(pred_t, 0)
        confusion[true_t][pred_t] += 1
        detail.append({"work": held, "true": true_t, "pred": pred_t, "ok": ok,
                       "scores": {t: round(s, 4) for t, s in scores.items()}})
    acc = correct / len(proto_ids)
    return {"accuracy": round(acc, 4), "n": len(proto_ids), "n_correct": correct,
            "confusion": confusion, "detail": detail}


# ---------- main ----------
def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    decomp = json.loads(DECOMP_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    sigs_full = decomp["signatures_aggregated"]   # signature SIG complète
    sigs_refl = {wid: decomp["decomposition"][wid]["reflexion"] for wid in proto_ids}
    works_traditions = {wid: meta["works"][wid]["tradition_label"] for wid in proto_ids}
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}

    # ----- Construire le tableau de paires connectées -----
    pairs = []  # (a, b, d_graph, d_sig, d_refl, dyear, same_trad)
    for i, a in enumerate(proto_ids):
        for b in proto_ids[i + 1:]:
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_sig = 1.0 - cosine(sigs_full[a], sigs_full[b])
            d_refl = 1.0 - cosine(sigs_refl[a], sigs_refl[b])
            dyear = abs(works_year[a] - works_year[b])
            same_trad = 1.0 if works_traditions[a] == works_traditions[b] else 0.0
            pairs.append((a, b, d_graph, d_sig, d_refl, dyear, same_trad))

    # ===== H1 : stratification par distance graphe =====
    d_graphs = [p[2] for p in pairs]
    cutoff = median(d_graphs)
    strong = [p[3] for p in pairs if p[2] <= cutoff]   # d_sig pour transmission forte
    weak = [p[3] for p in pairs if p[2] > cutoff]
    u, p_val = mann_whitney_u(strong, weak)
    h1 = {
        "median_d_graph": round(cutoff, 4),
        "n_strong_transmission": len(strong),
        "n_weak_transmission": len(weak),
        "mean_dsig_strong": round(mean(strong), 4),
        "mean_dsig_weak": round(mean(weak), 4),
        "expected": "mean_dsig_strong < mean_dsig_weak (signature plus proche si héritage fort)",
        "u_stat": round(u, 4),
        "p_value_two_tailed": round(p_val, 4),
        "verdict": "OK" if (mean(strong) < mean(weak) and p_val < 0.05) else "KO",
    }

    # ===== H2 : LOOCV par tradition (sig complète vs REFLEXION) =====
    loo_full = loocv_by_work(sigs_full, works_traditions)
    loo_refl = loocv_by_work(sigs_refl, works_traditions)
    # baseline majoritaire
    from collections import Counter
    trad_counts = Counter(works_traditions.values())
    majority_acc = max(trad_counts.values()) / sum(trad_counts.values())
    h2 = {
        "baseline_majority_acc": round(majority_acc, 4),
        "acc_full_signature": loo_full["accuracy"],
        "acc_reflexion_signature": loo_refl["accuracy"],
        "delta_full_vs_baseline": round(loo_full["accuracy"] - majority_acc, 4),
        "delta_refl_vs_baseline": round(loo_refl["accuracy"] - majority_acc, 4),
        "delta_refl_vs_full": round(loo_refl["accuracy"] - loo_full["accuracy"], 4),
        "verdict": "OK" if max(loo_full["accuracy"], loo_refl["accuracy"]) >= majority_acc + 0.15 else "KO",
        "loocv_full": loo_full,
        "loocv_reflexion": loo_refl,
    }

    # ===== H3 : régression OLS multi-facteurs =====
    # X = [1, d_graph, dyear/1000, same_trad]   y = d_sig
    X = [[1.0, p[2], p[5] / 1000.0, p[6]] for p in pairs]
    y_sig = [p[3] for p in pairs]
    y_refl = [p[4] for p in pairs]
    beta_sig, r2_sig = ols(X, y_sig)
    beta_refl, r2_refl = ols(X, y_refl)
    feature_names = ["intercept", "d_graph", "dyear_per_1000y", "same_tradition"]
    h3 = {
        "features": feature_names,
        "ols_dsig": {"beta": [round(b, 4) for b in beta_sig], "r2": round(r2_sig, 4)},
        "ols_drefl": {"beta": [round(b, 4) for b in beta_refl], "r2": round(r2_refl, 4)},
        "interpretation_dsig": (
            f"d_sig ≈ {beta_sig[0]:+.3f} {beta_sig[1]:+.3f}·d_graph "
            f"{beta_sig[2]:+.3f}·(Δyear/1000) {beta_sig[3]:+.3f}·same_trad  "
            f"(R²={r2_sig:.3f})"
        ),
        "verdict": "OK" if r2_sig >= 0.20 else "KO",
    }

    # ===== Verdict global =====
    h1_ok = h1["verdict"] == "OK"
    h2_ok = h2["verdict"] == "OK"
    h3_ok = h3["verdict"] == "OK"
    go = h1_ok and (h2_ok or h3_ok)
    overall_verdict = {
        "H1_strong_vs_weak_transmission": h1["verdict"],
        "H2_loocv_tradition": h2["verdict"],
        "H3_ols_regression": h3["verdict"],
        "go_no_go_phase_religieuse": "GO" if go else "NO-GO",
        "rationale": (
            "Phase religieuse §151+ AUTORISÉE — V14 + héritage discrimine."
            if go else
            "Phase religieuse §151+ SUSPENDUE — la signature V14 (binaire ou "
            "fréquentielle) ne reproduit pas suffisamment le graphe d'héritage. "
            "Cela ne réfute pas V14 en soi, mais exige soit (a) un extracteur "
            "sémantique au-delà du lexical (embeddings, parseurs philosophiques), "
            "soit (b) un corpus avec ≥ 20 fragments par auteur."
        ),
    }

    payload = {
        "version": "v150",
        "step": "§150 — validation prédictive Phase B révisée (composite)",
        "H1_stratification": h1,
        "H2_loocv_tradition": h2,
        "H3_ols_regression": h3,
        "verdict": overall_verdict,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §150 — validation écrite : {OUT}")
    print()
    print("─── H1 : transmission forte vs faible (Mann-Whitney) ───")
    print(f"  cutoff médian d_graph = {h1['median_d_graph']}")
    print(f"  d_sig moyen (forte transmission) = {h1['mean_dsig_strong']}")
    print(f"  d_sig moyen (faible transmission) = {h1['mean_dsig_weak']}")
    print(f"  U = {h1['u_stat']}, p = {h1['p_value_two_tailed']}")
    print(f"  → verdict H1 : {h1['verdict']}")
    print()
    print("─── H2 : LOOCV par tradition ───")
    print(f"  baseline majoritaire = {h2['baseline_majority_acc']}")
    print(f"  acc(SIG complète)    = {h2['acc_full_signature']}  (Δ vs baseline {h2['delta_full_vs_baseline']:+})")
    print(f"  acc(REFLEXION propre)= {h2['acc_reflexion_signature']}  (Δ vs baseline {h2['delta_refl_vs_baseline']:+})")
    print(f"  → verdict H2 : {h2['verdict']}")
    print()
    print("─── H3 : régression OLS d_sig ~ d_graph + Δyear + same_tradition ───")
    print(f"  {h3['interpretation_dsig']}")
    print(f"  → verdict H3 : {h3['verdict']}  (R²={h3['ols_dsig']['r2']})")
    print()
    print("═══ VERDICT GLOBAL §150 ═══")
    print(f"  H1={h1['verdict']}  H2={h2['verdict']}  H3={h3['verdict']}")
    print(f"  go/no-go phase religieuse §151+ : **{overall_verdict['go_no_go_phase_religieuse']}**")
    print(f"  rationale : {overall_verdict['rationale']}")


if __name__ == "__main__":
    main()

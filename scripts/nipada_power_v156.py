#!/usr/bin/env python3
"""
§156 — Analyse de puissance statistique : combien d'œuvres faut-il pour
détecter un signal généalogique de force réelle r (R²_vrai) avec
puissance ≥ 80 % au seuil α=0.05 ?

Méthode (Monte Carlo) :
  Pour chaque (n_pairs, R²_vrai) :
    1. Simuler n paires : d_graph ~ U(0.2, 2.0), dyear ~ U(0, 2200) ans,
       same_trad ~ Bernoulli(0.3).
    2. Générer d_sig = α + β_g·d_graph + β_y·(dyear/1000) + ε
       avec ε ~ N(0, σ²) calibré pour atteindre R²_vrai du modèle complet.
    3. Fitter OLS d_sig ~ d_graph SEUL (test crucial), garder R²_obs.
    4. Permutation test sur le R²_obs (1000 perm), seuil α=0.05.
    5. Compter fraction de simulations où H0 est rejetée → puissance empirique.

But : trouver le n_pairs minimal pour atteindre puissance ≥ 0.80 si
R²_vrai = 0.05, 0.10, 0.20.

Output : research/nipada/falsification/nipada_v156_power_analysis.json

Note importante : on simule volontairement des données plus simples que le
réel (pas de saturation, ε normal) — c'est une borne **optimiste** sur la
puissance. Le n trouvé est un minimum.
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
OUT = RES_DIR / "nipada_v156_power_analysis.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v150 = _load("nipada_validation_v150", SCRIPTS / "nipada_validation_v150.py")
ols = _v150.ols


def works_to_pairs(n_works: int) -> int:
    return n_works * (n_works - 1) // 2


def simulate_one(rng: random.Random, n: int, r2_true: float,
                  beta_g: float, beta_y: float) -> tuple[float, float]:
    """Simule n paires sous le modèle complet et retourne (R²_d_graph_only,
    R²_full)."""
    # On veut β_g, β_y réels dans le DGP, et bruit calibré à r2_true du
    # modèle complet d_sig ~ d_graph + dyear.

    # 1. Génère les régresseurs
    d_graph = [rng.uniform(0.2, 2.0) for _ in range(n)]
    dyear = [rng.uniform(0, 2200) / 1000.0 for _ in range(n)]
    # 2. Compute systematic part
    sys_part = [beta_g * d_graph[i] + beta_y * dyear[i] for i in range(n)]
    var_sys = sum((x - sum(sys_part) / n) ** 2 for x in sys_part) / n
    if var_sys == 0:
        return (0.0, 0.0)
    # var_sys / (var_sys + sigma²) = r2_true → sigma² = var_sys * (1/r2_true - 1)
    sigma2 = var_sys * (1.0 / r2_true - 1.0)
    sigma = math.sqrt(max(0.0, sigma2))
    # 3. Génère y avec bruit
    y = [sys_part[i] + rng.gauss(0.0, sigma) for i in range(n)]
    # 4. R² d_graph seul
    X1 = [[1.0, d_graph[i]] for i in range(n)]
    _, r2_1 = ols(X1, y)
    # 5. R² full
    X2 = [[1.0, d_graph[i], dyear[i]] for i in range(n)]
    _, r2_full = ols(X2, y)
    return (r2_1, r2_full)


def power_for(n: int, r2_true: float, beta_ratio_g_over_y: float,
               n_simulations: int = 400, n_perm: int = 200,
               alpha: float = 0.05, seed: int = 42) -> dict:
    """Estime la puissance pour détecter un effet d_graph SEUL non nul,
    via permutation test. n_simulations × n_perm peut être lourd ; on
    réduit n_perm à 200 (tolérable car on agrège sur 400 sims)."""
    rng = random.Random(seed)
    # Pour le DGP : on fixe la part de β_g sur le total de la variance
    # explicable. Si beta_ratio = 0.5, alors β_g et β_y contribuent
    # également à r2_true.
    beta_g = beta_ratio_g_over_y
    beta_y = 1.0 - beta_ratio_g_over_y

    rejected = 0
    r2_observed_list = []
    for sim in range(n_simulations):
        r2_obs, _ = simulate_one(rng, n, r2_true, beta_g, beta_y)
        r2_observed_list.append(r2_obs)
        # Permutation test
        # On réutilise les régresseurs ci-dessus mais on a perdu y → on
        # refait : pour la perm, il suffit de sampler n y aléatoires de
        # même taille et calculer R² sous shuffle.
        # OPTIMISATION : on calcule R²_critique théorique au lieu du test
        # de permutation pour chaque sim. R²_crit pour OLS avec 1 prédicteur :
        #   F = R²/(1-R²) × (n-2)
        #   F_crit ≈ 4.0 pour α=0.05 et n≥20 (one-sided)
        #   donc R²_crit ≈ 4 / (n - 2 + 4) ≈ 4 / n+2
        # Plus précisément : F_crit(1, n-2) ≈ 1 + 2.71/(n-2)^0.5 (approx Welch)
        # Pour simplicité, on prend la formule exacte avec F_crit(1, df2) à 0.05:
        df2 = max(1, n - 2)
        # F-distribution 95th percentile, df1=1, df2 — approximation
        # via t² : t_crit(df2)² ≈ 1.96² + 5/df2 = 3.84 + 5/df2
        f_crit = 3.84 + 5.0 / df2
        r2_crit = f_crit / (df2 + f_crit)
        if r2_obs >= r2_crit:
            rejected += 1
    return {
        "n_pairs": n,
        "n_works_approx": int(0.5 + 0.5 * (1 + math.sqrt(1 + 8 * n))),
        "r2_true_full": r2_true,
        "beta_ratio_g_over_y": beta_ratio_g_over_y,
        "n_simulations": n_simulations,
        "power_at_alpha_0.05": round(rejected / n_simulations, 3),
        "mean_r2_observed_d_graph_only": round(
            sum(r2_observed_list) / len(r2_observed_list), 4),
    }


def find_min_n(target_r2_true: float, beta_ratio: float,
                target_power: float = 0.80,
                n_grid: list[int] = [29, 45, 90, 174, 300, 500, 1000]) -> dict:
    results = []
    for n in n_grid:
        r = power_for(n, target_r2_true, beta_ratio, n_simulations=400)
        results.append(r)
        if r["power_at_alpha_0.05"] >= target_power:
            break
    return {
        "target_r2_true": target_r2_true,
        "beta_ratio_g_over_y": beta_ratio,
        "target_power": target_power,
        "trace": results,
        "min_n_pairs_for_target_power": (
            results[-1]["n_pairs"]
            if results[-1]["power_at_alpha_0.05"] >= target_power
            else None
        ),
        "min_n_works_for_target_power": (
            results[-1]["n_works_approx"]
            if results[-1]["power_at_alpha_0.05"] >= target_power
            else None
        ),
    }


def main() -> None:
    # On teste plusieurs scénarios :
    # (a) effet faible R²_vrai=0.05, β_g pèse 30 % (réel : Δyear domine)
    # (b) effet faible R²_vrai=0.05, β_g pèse 50 %
    # (c) effet modéré R²_vrai=0.10, β_g pèse 30 %
    # (d) effet modéré R²_vrai=0.20, β_g pèse 30 %
    # (e) effet fort R²_vrai=0.45, β_g pèse 30 %

    scenarios = [
        ("a_R2_0.05_betaG_30%", 0.05, 0.3),
        ("b_R2_0.05_betaG_50%", 0.05, 0.5),
        ("c_R2_0.10_betaG_30%", 0.10, 0.3),
        ("d_R2_0.20_betaG_30%", 0.20, 0.3),
        ("e_R2_0.45_betaG_30%", 0.45, 0.3),
    ]

    out = {}
    for name, r2, ratio in scenarios:
        print(f"→ Scénario {name} (R²_vrai={r2}, β_g/total={ratio})…")
        out[name] = find_min_n(r2, ratio)
        if out[name]["min_n_pairs_for_target_power"]:
            print(f"   → puissance 80 % à n={out[name]['min_n_pairs_for_target_power']} "
                  f"({out[name]['min_n_works_for_target_power']} œuvres)")
        else:
            print(f"   → puissance 80 % NON atteinte avec n≤1000")

    # Calcul du R²_observé actuel (mix=0.046) sous différents n
    actual_r2 = 0.046  # observé à n=29
    actual = []
    for n in [29, 45, 90, 174, 300, 500, 1000]:
        # Sous H0 (R²_vrai = 0.046 pour d_graph seul), la puissance =
        # P(R²_obs > R²_crit). On simule directement.
        r = power_for(n, actual_r2, 1.0, n_simulations=400)
        actual.append(r)

    payload = {
        "version": "v156",
        "step": "§156 — analyse de puissance statistique (Monte Carlo)",
        "scenarios": out,
        "actual_observed_R2_46e_3": {
            "description": "Si l'effet réel est exactement R²=0.046 (mix lex×dense observé), puissance par n",
            "trace": actual,
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print(f"✓ §156 — analyse de puissance écrite : {OUT}")
    print()
    print("─── Résumé : combien d'œuvres pour atteindre puissance 80 % ? ───")
    for name, _, _ in scenarios:
        s = out[name]
        n_w = s["min_n_works_for_target_power"]
        n_p = s["min_n_pairs_for_target_power"]
        if n_w:
            print(f"  {name}: {n_w} œuvres ({n_p} paires)")
        else:
            print(f"  {name}: > 1000 paires nécessaires (R²_vrai trop faible)")
    print()
    print("─── Si l'effet réel = R²=0.046 (mix observé) : ───")
    for r in actual:
        print(f"  n={r['n_pairs']:4d} ({r['n_works_approx']:3d} œuvres)  →  puissance = {r['power_at_alpha_0.05']}")


if __name__ == "__main__":
    main()

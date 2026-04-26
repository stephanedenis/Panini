#!/usr/bin/env python3
"""
§170 — Revalidation NIPADA sur corpus étendu (graphe v168).

Pipeline :
  1. Charger v168 graph (41 nodes, 91 paires) + métadonnées v168.
  2. Annoter tous les fragments (V14 §145) sur 14 œuvres :
     - 10 œuvres §141-§148 originales
     - 4 nouvelles œuvres §166-§167 (Spinoza, Hobbes, Mozi, Han Feizi).
  3. Calculer :
     - sig_lex (fréquence atomique normalisée, dim 14)
     - sig_bigram (co-occurrence intra-fragment, dim 91)
  4. Pour chaque paire (a, b) connectée dans v168 :
     - d_graph = -log(produit poids) [Floyd-Warshall, déjà calculé]
     - d_lex = 1 - cos(sig_lex_a, sig_lex_b)
     - d_bigram = 1 - cos(sig_bigram_a, sig_bigram_b)
  5. Tester :
     - Pearson r(d_lex, d_graph), r(d_bigram, d_graph)
     - OLS R²(d_graph alone) régressant d_sig sur d_graph
     - Permutation test (2000 itérations) → p_perm
     - Comparaison v159 (n_pairs=29) vs v168
  6. Power analysis :
     - Détectabilité d'un effet R²=0.05 à α=0.05 avec n_pairs courant.

Output : research/nipada/falsification/nipada_v170_revalidation.json
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
OUT = RES_DIR / "nipada_v170_revalidation.json"

GRAPH_V168 = RES_DIR / "nipada_v168_inheritance_graph_v3.json"
META_V168 = RES_DIR / "nipada_v168_metadata_extended.json"
GRAPH_V159 = RES_DIR / "nipada_v159_inheritance_graph_v2.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v145 = _load("nipada_v14_multiling_v145", SCRIPTS / "nipada_v14_multiling_v145.py")
V14 = _v145.V14
LEX = _v145.LEX
NEG_MARKERS = _v145.NEG_MARKERS
UNIV_MARKERS = _v145.UNIV_MARKERS
EQ_MARKERS = _v145.EQ_MARKERS
annotate = _v145.annotate

PAIR_KEYS = [(V14[i], V14[j]) for i in range(len(V14)) for j in range(i + 1, len(V14))]


def freq_signature(text: str, lang: str) -> dict[str, float]:
    counts = {a: 0 for a in V14}
    text_lc = text.lower() if lang != "lzh" else text
    for atom in V14:
        for m in LEX.get(atom, {}).get(lang, []):
            mlc = m.lower() if lang != "lzh" else m
            counts[atom] += text_lc.count(mlc)
    for m in NEG_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["DIFFÉRENCE"] += 1
            counts["MODALITÉ"] += 1
    for m in UNIV_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["MODALITÉ"] += 1
    for m in EQ_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["ÊTRE"] += 1
            counts["ÉQUATION"] += 1
    if any(c.isdigit() for c in text):
        counts["NOMBRE"] += 1
    return counts


def aggregate_lex_sig(work_id: str, frags: list[dict]) -> dict[str, float]:
    sig = {a: 0.0 for a in V14}
    for f in frags:
        if f["work_id"] != work_id:
            continue
        c = freq_signature(f["text"], f["lang"])
        for a in V14:
            sig[a] += c[a]
    total = sum(sig.values())
    if total > 0:
        return {a: sig[a] / total for a in V14}
    return {a: 1.0 / len(V14) for a in V14}


def cooccurrence_sig(work_id: str, frags: list[dict]) -> dict[str, float]:
    counts = {f"{a}|{b}": 0 for (a, b) in PAIR_KEYS}
    n = 0
    for f in frags:
        if f["work_id"] != work_id:
            continue
        atoms = annotate(f["text"], f["lang"])
        ordered = [a for a in V14 if a in atoms]
        for a, b in itertools.combinations(ordered, 2):
            counts[f"{a}|{b}"] += 1
        n += 1
    if n == 0:
        return {k: 0.0 for k in counts}
    return {k: v / n for k, v in counts.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na > 0 and nb > 0 else 0.0


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0.0


def ols_r2(xs: list[float], ys: list[float]) -> float:
    """R² de la régression OLS univariée ys ~ a + b·xs."""
    r = pearson(xs, ys)
    return r * r


def perm_test_r2(xs: list[float], ys: list[float], n_iter: int = 2000,
                 seed: int = 42) -> float:
    obs = ols_r2(xs, ys)
    rng = random.Random(seed)
    ys_shuf = list(ys)
    cnt = 0
    for _ in range(n_iter):
        rng.shuffle(ys_shuf)
        if ols_r2(xs, ys_shuf) >= obs:
            cnt += 1
    return cnt / n_iter


def power_estimate(n: int, r_target: float = 0.224, alpha: float = 0.05) -> dict:
    """Estimation simplifiée de la puissance pour détecter un r=r_target.
    r=0.224 ≈ R²=0.05. Utilise approximation z de Fisher.
    n_min = ((z_{α/2}+z_{1-β})/atanh(r))² + 3.
    Ici on calcule la puissance pour n donné."""
    if n < 4:
        return {"n_required_for_R2_0.05_at_pow_0.80": None,
                "current_power_estimate": 0.0}
    z_alpha = 1.96  # two-sided 0.05
    fisher_z = math.atanh(r_target)
    se = 1.0 / math.sqrt(n - 3)
    z = fisher_z / se
    # power ≈ 1 - Φ(z_alpha - z) (one-sided approximation)
    def phi(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    pw = 1.0 - phi(z_alpha - z) + phi(-z_alpha - z)
    # n required for power 0.80
    z_beta = 0.84
    n_req = int(math.ceil(((z_alpha + z_beta) / fisher_z) ** 2 + 3))
    return {
        "r_target": r_target,
        "n_pairs_current": n,
        "current_power_at_alpha_0.05": round(pw, 4),
        "n_required_for_power_0.80": n_req,
    }


def main() -> None:
    graph = json.loads(GRAPH_V168.read_text(encoding="utf-8"))
    meta = json.loads(META_V168.read_text(encoding="utf-8"))

    # PROTO_ATHEIST_NODES = œuvres avec fragments (les nodes "proto_atheist_work"
    # + les 4 nouveaux ajoutés en v168)
    works = sorted([n for n, info in graph["nodes"].items()
                    if info.get("kind") == "proto_atheist_work"])

    # Filtrer aux œuvres ayant des fragments réels
    frags = []
    for d in sorted((ROOT / "corpus" / "protoatheism").iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                frags.append(json.loads(line))

    works_with_frags = sorted({f["work_id"] for f in frags})
    works_eligible = [w for w in works if w in works_with_frags]
    print(f"Œuvres éligibles (proto-athéistes avec fragments) : {len(works_eligible)}")

    # Calculer signatures
    lex_sigs = {w: aggregate_lex_sig(w, frags) for w in works_eligible}
    bigr_sigs = {w: cooccurrence_sig(w, frags) for w in works_eligible}

    # Calculer paires (lex et bigram)
    pairs_lex, pairs_bigr, pairs_dgr = [], [], []
    pair_details = []
    for i, a in enumerate(works_eligible):
        for b in works_eligible[i + 1:]:
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_lex = 1.0 - cosine(lex_sigs[a], lex_sigs[b])
            d_bigr = 1.0 - cosine(bigr_sigs[a], bigr_sigs[b])
            pairs_lex.append(d_lex)
            pairs_bigr.append(d_bigr)
            pairs_dgr.append(d_graph)
            pair_details.append({
                "a": ka, "b": kb,
                "d_graph": round(d_graph, 4),
                "d_lex": round(d_lex, 4),
                "d_bigram": round(d_bigr, 4),
            })

    n_pairs = len(pairs_dgr)
    r_lex = pearson(pairs_lex, pairs_dgr)
    r_bigr = pearson(pairs_bigr, pairs_dgr)
    r2_lex = ols_r2(pairs_lex, pairs_dgr)
    r2_bigr = ols_r2(pairs_bigr, pairs_dgr)
    p_lex = perm_test_r2(pairs_lex, pairs_dgr)
    p_bigr = perm_test_r2(pairs_bigr, pairs_dgr)

    power_lex = power_estimate(n_pairs)

    # Comparaison v159 (lecture du fichier de validation §160)
    v159_graph = json.loads(GRAPH_V159.read_text(encoding="utf-8"))
    v159_n = sum(1 for v in v159_graph["proto_pair_distances"].values() if v is not None)

    summary = {
        "n_works_eligible": len(works_eligible),
        "n_pairs_v168": n_pairs,
        "n_pairs_v159": v159_n,
        "lex_R2": round(r2_lex, 4),
        "lex_pearson_r": round(r_lex, 4),
        "lex_p_perm": round(p_lex, 4),
        "bigram_R2": round(r2_bigr, 4),
        "bigram_pearson_r": round(r_bigr, 4),
        "bigram_p_perm": round(p_bigr, 4),
        "power_analysis": power_lex,
        "verdict": (
            "REJET H0 (signal robuste détecté)" if (p_bigr < 0.05 or p_lex < 0.05)
            else "INDÉTERMINÉ (sous-puissance ou absence d'effet)"
        ),
    }

    payload = {
        "version": "v170",
        "step": "§170 — revalidation corpus étendu sur graphe v168",
        "summary": summary,
        "lex_signatures": lex_sigs,
        "pair_details": pair_details,
        "works_eligible": works_eligible,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== VERDICT §170 ===")
    print(f"Œuvres : {summary['n_works_eligible']}  Paires : {n_pairs} (vs v159 : {v159_n})")
    print(f"  LEX     R²={r2_lex:.4f}  r={r_lex:+.4f}  p_perm={p_lex:.4f}")
    print(f"  BIGRAM  R²={r2_bigr:.4f}  r={r_bigr:+.4f}  p_perm={p_bigr:.4f}")
    print(f"  Puissance courante (à r=0.224) = {power_lex['current_power_at_alpha_0.05']}")
    print(f"  n requis pour puissance 0.80    = {power_lex['n_required_for_power_0.80']}")
    print(f"  VERDICT : {summary['verdict']}")
    print(f"\n✓ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

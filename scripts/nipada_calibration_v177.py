#!/usr/bin/env python3
"""
§177 — Calibration empirique des poids du graphe (passer §175 placebo).

Idée :
  Au lieu de poser a priori W_DIRECT=0.80 / W_INDIRECT=0.35 / W_TRANSLATION=0.65,
  on cherche les valeurs (w_direct, w_indirect, w_translation) qui maximisent
  R²(d_lex_distance, d_graph_distance) sur l'ensemble des paires connectées.

Méthode (grid search 3D, séparée train/test) :
  1. Split paires connectées (graph v5) en TRAIN (70%) / TEST (30%) — split
     stratifié par tradition pour éviter biais.
  2. Sur TRAIN : grid 3D sur (w_d, w_t, w_i) ∈ [0.10, 0.99]³ pas 0.05.
     Pour chaque triplet, recalculer Floyd-Warshall, mesurer R²(LEX) sur TRAIN.
  3. Conserver le triplet maximisant R²(LEX_train).
  4. Appliquer ce triplet à TEST : mesurer R² + p_perm.
  5. Si R²(test) > 95ᵉ pct du R²(test) sous poids randomisés (placebo §175 sur
     le SET de test), §177 passe.

Anti-overfitting : on rapporte aussi R²(train) - R²(test). S'il y a un large
gap, c'est de l'overfit ; on vise gap < 0.03.

Output :
  research/nipada/falsification/nipada_v177_weight_calibration.json
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
GRAPH_V5 = RES_DIR / "nipada_v176_graph_v5.json"


def _load(name, path):
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


def freq_signature(text, lang):
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


def cosine(a, b):
    keys = set(a) | set(b)
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na > 0 and nb > 0 else 0.0


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0.0


def perm_test(xs, ys, n_iter=2000):
    obs = pearson(xs, ys) ** 2
    rng = random.Random(42)
    yshuf = list(ys)
    cnt = 0
    for _ in range(n_iter):
        rng.shuffle(yshuf)
        if pearson(xs, yshuf) ** 2 >= obs:
            cnt += 1
    return cnt / n_iter


def floyd_warshall_weighted(edges_with_channels, weight_map, all_nodes):
    """edges_with_channels = list of (src, tgt, channel_str)
       weight_map: dict {direct/indirect/translation/structural: float}"""
    INF = math.inf
    n = len(all_nodes)
    idx = {nid: i for i, nid in enumerate(all_nodes)}
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0.0
    # Build adj with category-derived weights
    adj = {}
    for src, tgt, ch in edges_with_channels:
        cat = classify_channel(ch)
        w = weight_map[cat]
        if src not in adj:
            adj[src] = {}
        if tgt in adj[src]:
            if w > adj[src][tgt]:
                adj[src][tgt] = w
        else:
            adj[src][tgt] = w
    for src, neigh in adj.items():
        if src not in idx:
            continue
        for tgt, w in neigh.items():
            if tgt not in idx:
                continue
            cost = -math.log(w)
            i, j = idx[src], idx[tgt]
            d[i][j] = min(d[i][j], cost)
            d[j][i] = min(d[j][i], cost)
    for k in range(n):
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + d[k][j]
                if nd < d[i][j]:
                    d[i][j] = nd
    out = {}
    for i, a in enumerate(all_nodes):
        for j, b in enumerate(all_nodes):
            if i < j:
                out[(a, b)] = d[i][j]
    return out


def classify_channel(channel_text):
    """Catégorise un libellé d'arête en {direct, translation, indirect, structural}."""
    t = channel_text.lower()
    if "traduction" in t or "translation" in t:
        return "translation"
    if "indirect" in t or "héritier" in t or "transmission" in t or "héritage" in t \
            or "lit " in t or "connaît" in t or "tradition" in t or "comparat" in t \
            or "scepticisme" in t or "lecteur" in t or "ascendant" in t \
            or "ami " in t or "post-" in t or "même transmission" in t \
            or "écho" in t or "reçu" in t or "même école" in t \
            or "succession" in t:
        return "indirect"
    return "direct"


def main():
    graph = json.loads(GRAPH_V5.read_text(encoding="utf-8"))
    nodes = graph["nodes"]
    edges = [(e["src"], e["tgt"], e["channel"]) for e in graph["edges"]]
    proto_works = sorted([n for n, info in nodes.items() if info.get("kind") == "proto_atheist_work"])

    # Vérifier la classification des canaux
    cat_counts = {"direct": 0, "translation": 0, "indirect": 0}
    for _, _, ch in edges:
        cat_counts[classify_channel(ch)] += 1
    print(f"Catégories : {cat_counts}")

    # Charger fragments + signatures
    frags_all = []
    for d in sorted((ROOT / "corpus" / "protoatheism").iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                frags_all.append(json.loads(line))

    lex_sigs = {}
    for w in proto_works:
        wfrags = [f for f in frags_all if f["work_id"] == w]
        if not wfrags:
            continue
        lex = {a: 0.0 for a in V14}
        for f in wfrags:
            c = freq_signature(f["text"], f["lang"])
            for a in V14:
                lex[a] += c[a]
        tot = sum(lex.values())
        lex_sigs[w] = {a: lex[a] / tot if tot > 0 else 1.0 / 14 for a in V14}

    works = sorted(lex_sigs.keys())
    traditions = {w: nodes[w].get("tradition_label", "?") for w in works}
    all_nodes_ids = list(nodes.keys())

    # Construire toutes les paires possibles + leurs distances LEX (fixes)
    pair_records = []
    for i, a in enumerate(works):
        for b in works[i + 1:]:
            d_lex = 1.0 - cosine(lex_sigs[a], lex_sigs[b])
            same_trad = traditions[a] == traditions[b]
            pair_records.append({
                "a": a, "b": b, "d_lex": d_lex, "same_trad": same_trad,
                "trad_a": traditions[a], "trad_b": traditions[b],
            })
    print(f"Paires totales possibles : {len(pair_records)}")

    # Split TRAIN/TEST stratifié par appartenance "même tradition"
    rng = random.Random(2026)
    intra = [p for p in pair_records if p["same_trad"]]
    inter = [p for p in pair_records if not p["same_trad"]]
    rng.shuffle(intra)
    rng.shuffle(inter)
    cut_intra = int(0.7 * len(intra))
    cut_inter = int(0.7 * len(inter))
    train = intra[:cut_intra] + inter[:cut_inter]
    test = intra[cut_intra:] + inter[cut_inter:]
    print(f"Split: TRAIN={len(train)} (intra={cut_intra}, inter={cut_inter}) "
          f"TEST={len(test)} (intra={len(intra)-cut_intra}, inter={len(inter)-cut_inter})")

    # Grid 3D — pas 0.05 pour rester rapide
    print("\n=== §177 grid search 3D ===")
    grid = [round(0.10 + 0.05 * k, 3) for k in range(18)]  # 0.10 → 0.95
    best = {"R2_train": -1.0, "wd": None, "wt": None, "wi": None}
    n_evaluated = 0
    for wd in grid:
        for wt in grid:
            for wi in grid:
                if not (wi <= wt <= wd):  # contrainte : indirect ≤ translation ≤ direct
                    continue
                paths = floyd_warshall_weighted(
                    edges, {"direct": wd, "translation": wt, "indirect": wi}, all_nodes_ids)
                xs, ys = [], []
                for p in train:
                    d = paths.get((p["a"], p["b"])) or paths.get((p["b"], p["a"]))
                    if d is None or not math.isfinite(d):
                        continue
                    xs.append(p["d_lex"])
                    ys.append(d)
                if len(xs) < 10:
                    continue
                r2 = pearson(xs, ys) ** 2
                n_evaluated += 1
                if r2 > best["R2_train"]:
                    best = {"R2_train": r2, "wd": wd, "wt": wt, "wi": wi,
                            "n_train_connected": len(xs)}
    print(f"  Évalué {n_evaluated} triplets (contrainte wi ≤ wt ≤ wd)")
    print(f"  Best: w_direct={best['wd']} w_translation={best['wt']} w_indirect={best['wi']}")
    print(f"  R²(TRAIN) = {best['R2_train']:.4f}")

    # Apply best to TEST
    paths_best = floyd_warshall_weighted(
        edges, {"direct": best["wd"], "translation": best["wt"], "indirect": best["wi"]},
        all_nodes_ids)
    xs_test, ys_test = [], []
    for p in test:
        d = paths_best.get((p["a"], p["b"])) or paths_best.get((p["b"], p["a"]))
        if d is None or not math.isfinite(d):
            continue
        xs_test.append(p["d_lex"])
        ys_test.append(d)
    r_test = pearson(xs_test, ys_test)
    p_test = perm_test(xs_test, ys_test, n_iter=2000)
    print(f"\n  TEST n={len(xs_test)}: r={r_test:+.4f} R²={r_test**2:.4f} p_perm={p_test:.4f}")

    # Placebo sur TEST avec le même nombre d'arêtes/canaux mais poids randomisés
    print("\n=== §177 placebo TEST sous poids randomisés ===")
    rng2 = random.Random(7)
    n_placebo = 200
    null_r2 = []
    for _ in range(n_placebo):
        # poids aléatoires dans la même plage avec même contrainte d'ordre
        ws = sorted([rng2.uniform(0.10, 0.99), rng2.uniform(0.10, 0.99), rng2.uniform(0.10, 0.99)])
        wi_r, wt_r, wd_r = ws
        paths_r = floyd_warshall_weighted(
            edges, {"direct": wd_r, "translation": wt_r, "indirect": wi_r}, all_nodes_ids)
        xs_r, ys_r = [], []
        for p in test:
            d = paths_r.get((p["a"], p["b"])) or paths_r.get((p["b"], p["a"]))
            if d is None or not math.isfinite(d):
                continue
            xs_r.append(p["d_lex"])
            ys_r.append(d)
        if len(xs_r) >= 10:
            null_r2.append(pearson(xs_r, ys_r) ** 2)
    null_r2.sort()
    p95 = null_r2[int(0.95 * len(null_r2)) - 1] if null_r2 else None
    p_placebo = sum(1 for v in null_r2 if v >= r_test ** 2) / max(1, len(null_r2))
    print(f"  Placebo TEST p₉₅ = {p95:.4f} (n={len(null_r2)})")
    print(f"  Observed TEST R² = {r_test**2:.4f}")
    print(f"  p vs placebo TEST = {p_placebo:.4f}")

    # Comparison vs original weights (0.80/0.65/0.35)
    print("\n=== §177 comparaison vs poids a priori (§172) ===")
    paths_apriori = floyd_warshall_weighted(
        edges, {"direct": 0.80, "translation": 0.65, "indirect": 0.35},
        all_nodes_ids)
    xs_ap, ys_ap = [], []
    for p in test:
        d = paths_apriori.get((p["a"], p["b"])) or paths_apriori.get((p["b"], p["a"]))
        if d is None or not math.isfinite(d):
            continue
        xs_ap.append(p["d_lex"])
        ys_ap.append(d)
    r_ap = pearson(xs_ap, ys_ap)
    print(f"  A priori (0.80/0.65/0.35) sur TEST: r={r_ap:+.4f} R²={r_ap**2:.4f}")
    print(f"  Calibrés sur TEST                : r={r_test:+.4f} R²={r_test**2:.4f}")
    gap = best["R2_train"] - r_test ** 2
    print(f"  Overfitting gap (R²_train − R²_test) = {gap:+.4f}")

    summary = {
        "best_weights": {"direct": best["wd"], "translation": best["wt"], "indirect": best["wi"]},
        "channel_categories": cat_counts,
        "n_train": len(train), "n_test": len(test),
        "R2_train": round(best["R2_train"], 4),
        "R2_test_calibrated": round(r_test ** 2, 4),
        "r_test_calibrated": round(r_test, 4),
        "p_perm_test": round(p_test, 4),
        "R2_test_apriori": round(r_ap ** 2, 4),
        "r_test_apriori": round(r_ap, 4),
        "overfitting_gap": round(gap, 4),
        "placebo_p95_R2": round(p95, 4) if p95 else None,
        "p_vs_placebo_test": round(p_placebo, 4),
        "verdict": (
            "Calibration améliore signal sur TEST avec p_placebo<0.05"
            if p_placebo < 0.05 and r_test ** 2 > r_ap ** 2
            else "Calibration n'améliore pas significativement (overfit ou plateau)"
            if gap > 0.05
            else "Signal stable, calibration marginale"
        ),
    }
    (RES_DIR / "nipada_v177_weight_calibration.json").write_text(
        json.dumps({"version": "v177", "summary": summary}, indent=2),
        encoding="utf-8")
    print(f"\n  VERDICT : {summary['verdict']}")


if __name__ == "__main__":
    main()

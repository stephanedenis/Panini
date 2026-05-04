#!/usr/bin/env python3
"""
§231 — Revalidation après extension Greco-Latin v225.

Compare R² topo-lex pour:
- corpus v212f (base)
- corpus v225 seul
- corpus fusionné v212f + v225 (dédup par graph_node_id)

Ajoute un permutation test (d_topo fixe, d_lex permuté) sur le corpus fusionné.
Sortie: Panini-Research/nipada/falsification/nipada_v231_revalidation_v225.json
"""

from __future__ import annotations

import heapq
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

GRAPH_PATH = _NIPADA / "falsification/nipada_v219_graph_v13.json"
V220_PATH = _NIPADA / "falsification/nipada_v220_vopt_calibration.json"
C212_PATH = _NIPADA / "corpus/signed_corpus_v212f.json"
C225_PATH = _NIPADA / "corpus/signed_corpus_v225_greco_latin.json"
C225B_PATH = _NIPADA / "corpus/signed_corpus_v225b_greco_latin.json"
OUT_PATH = _NIPADA / "falsification/nipada_v231_revalidation_v225.json"
OUT_B_PATH = _NIPADA / "falsification/nipada_v231b_revalidation_v225b.json"

V_OPT_FALLBACK = {"direct": 0.1, "translation": 0.1, "indirect": 1.0}
V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

_DTOPO_GLOBAL = None
_DLEX_GLOBAL = None


def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(edges: list[dict[str, Any]], weights: dict[str, float]) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = weights[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(source: str, adj: dict[str, list[tuple[str, float]]], targets: set[str]) -> dict[str, float]:
    dist = {source: 0.0}
    pq = [(0.0, source)]
    remaining = set(targets) - {source}
    found: dict[str, float] = {}
    while pq and remaining:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        if u in remaining:
            remaining.discard(u)
            found[u] = d
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return {t: found.get(t, dist.get(t, math.inf)) for t in targets}


def v14_vector(sig: dict[str, float]) -> list[float]:
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1: list[float], v2: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r2(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return (num / (sx * sy)) ** 2


def build_pairs(adj: dict[str, list[tuple[str, float]]], signed: list[dict[str, Any]]) -> tuple[list[float], list[float], int]:
    ids = [s["graph_node_id"] for s in signed]
    sigs = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    d_topo: list[float] = []
    d_lex: list[float] = []
    inf_count = 0

    for i in range(len(ids)):
        dists = dijkstra_from(ids[i], adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = dists[ids[j]]
            if math.isinf(dt):
                inf_count += 1
                continue
            dl = l2_distance(sigs[ids[i]], sigs[ids[j]])
            d_topo.append(dt)
            d_lex.append(dl)

    return d_topo, d_lex, inf_count


def _init_worker_perm(dtopo: list[float], dlex: list[float]) -> None:
    global _DTOPO_GLOBAL, _DLEX_GLOBAL
    _DTOPO_GLOBAL = dtopo
    _DLEX_GLOBAL = dlex


def _worker_perm(seed: int) -> float:
    rng = random.Random(seed)
    shuffled = list(_DLEX_GLOBAL)
    rng.shuffle(shuffled)
    return pearson_r2(_DTOPO_GLOBAL, shuffled)


def merge_corpora(c212: list[dict[str, Any]], c225: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for s in c212:
        out[s["graph_node_id"]] = s
    # v225 remplace en cas de collision (aucune attendue)
    for s in c225:
        out[s["graph_node_id"]] = s
    return list(out.values())


def eval_corpus(adj: dict[str, list[tuple[str, float]]], signed: list[dict[str, Any]]) -> dict[str, Any]:
    d_topo, d_lex, inf_count = build_pairs(adj, signed)
    r2 = pearson_r2(d_topo, d_lex)
    return {
        "n_signed": len(signed),
        "n_pairs_finite": len(d_topo),
        "n_pairs_infinite": inf_count,
        "r2": round(r2, 4),
        "d_topo": d_topo,
        "d_lex": d_lex,
    }


def main() -> int:
    t0 = time.time()
    n_perm = 1000
    if "--perms" in sys.argv:
        i = sys.argv.index("--perms")
        if i + 1 < len(sys.argv):
            n_perm = int(sys.argv[i + 1])

    # Allow pointing at a different extension corpus (e.g. v225b)
    ext_path = C225_PATH
    out_path  = OUT_PATH
    label_ext = "v225"
    if "--corpus-ext" in sys.argv:
        idx = sys.argv.index("--corpus-ext")
        if idx + 1 < len(sys.argv):
            p = Path(sys.argv[idx + 1])
            if not p.is_absolute():
                p = _NIPADA / "corpus" / p
            ext_path = p
            stem = p.stem  # e.g. signed_corpus_v225b_greco_latin
            tag = stem.replace("signed_corpus_", "").replace("_greco_latin", "").replace("_", "-")
            label_ext = tag
            out_path = FALSI_DIR / f"nipada_v231_revalidation_{tag}.json" if "FALSI_DIR" in dir() else \
                        _NIPADA / "falsification" / f"nipada_v231_revalidation_{tag}.json"
    if "--out" in sys.argv:
        idx2 = sys.argv.index("--out")
        if idx2 + 1 < len(sys.argv):
            out_path = Path(sys.argv[idx2 + 1])

    graph = json.loads(GRAPH_PATH.read_text())
    c212 = json.loads(C212_PATH.read_text())
    c225 = json.loads(ext_path.read_text())

    if V220_PATH.exists():
        v220 = json.loads(V220_PATH.read_text())
        vopt = v220.get("v_opt_v5_best_cv", {}).get("weights", V_OPT_FALLBACK)
    else:
        vopt = V_OPT_FALLBACK

    edges = graph["edges"]
    adj = build_adjacency(edges, vopt)

    s212 = c212.get("signed", [])
    s225 = c225.get("signed", [])
    smerge = merge_corpora(s212, s225)

    print(f"§231 — Revalidation {label_ext}")
    print(f"  n212={len(s212)} n_ext={len(s225)} nmerge={len(smerge)}")

    m212 = eval_corpus(adj, s212)
    m225 = eval_corpus(adj, s225)
    mmerge = eval_corpus(adj, smerge)

    print(f"  R² v212f        = {m212['r2']:.4f} ({m212['n_pairs_finite']} paires)")
    print(f"  R² {label_ext:12s} = {m225['r2']:.4f} ({m225['n_pairs_finite']} paires)")
    print(f"  R² merged       = {mmerge['r2']:.4f} ({mmerge['n_pairs_finite']} paires)")

    # Permutation sur merged
    n_cpu = os.cpu_count() or 4
    n_workers = max(1, n_cpu - 2)
    mp.set_start_method("fork", force=True)
    seeds = list(range(23100, 23100 + n_perm))
    chunk = max(1, n_perm // (n_workers * 4))

    print(f"  Permutation merged: n_perm={n_perm}, workers={n_workers}")
    t_perm = time.time()
    r2_perms: list[float] = []
    with mp.Pool(
        processes=n_workers,
        initializer=_init_worker_perm,
        initargs=(mmerge["d_topo"], mmerge["d_lex"]),
    ) as pool:
        for i, r in enumerate(pool.imap_unordered(_worker_perm, seeds, chunksize=chunk), start=1):
            r2_perms.append(r)
            if i % max(1, n_perm // 10) == 0:
                print(f"    {int(i / n_perm * 100)}%")

    mean_p = sum(r2_perms) / len(r2_perms)
    std_p = math.sqrt(sum((x - mean_p) ** 2 for x in r2_perms) / len(r2_perms))
    p_value = sum(1 for r in r2_perms if r >= mmerge["r2"]) / len(r2_perms)
    z_score = (mmerge["r2"] - mean_p) / std_p if std_p > 0 else float("inf")
    rs = sorted(r2_perms)
    ci_lo = rs[int(0.025 * len(rs))]
    ci_hi = rs[int(0.975 * len(rs))]

    out = {
        "section": "§231",
        "description": f"Revalidation après extension Greco-Latin {label_ext}",
        "corpus_ext": str(ext_path),
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "graph": GRAPH_PATH.name,
        "vopt_weights": vopt,
        "corpora": {
            "v212f": {
                "n_signed": m212["n_signed"],
                "n_pairs_finite": m212["n_pairs_finite"],
                "n_pairs_infinite": m212["n_pairs_infinite"],
                "r2": m212["r2"],
            },
            f"{label_ext}_only": {
                "n_signed": m225["n_signed"],
                "n_pairs_finite": m225["n_pairs_finite"],
                "n_pairs_infinite": m225["n_pairs_infinite"],
                "r2": m225["r2"],
            },
            f"merged_v212f_{label_ext}": {
                "n_signed": mmerge["n_signed"],
                "n_pairs_finite": mmerge["n_pairs_finite"],
                "n_pairs_infinite": mmerge["n_pairs_infinite"],
                "r2": mmerge["r2"],
                "delta_vs_v212f": round(mmerge["r2"] - m212["r2"], 4),
            },
        },
        "permutation_test_merged": {
            "n_perm": n_perm,
            "mean_r2_perm": round(mean_p, 4),
            "std_r2_perm": round(std_p, 4),
            "ci_95_null": [round(ci_lo, 4), round(ci_hi, 4)],
            "p_value": round(p_value, 4),
            "z_score": round(z_score, 3),
            "significant_p01": p_value < 0.01,
            "elapsed_s": round(time.time() - t_perm, 1),
        },
        "elapsed_total_s": round(time.time() - t0, 1),
    }

    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Écrit: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

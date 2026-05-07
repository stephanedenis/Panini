#!/usr/bin/env python3
"""
§266 — Revalidation après densification prophétique (graphe v18p).

Charge :
  - signed_corpus_v263_clean.json    (100 textes, base §263 dédupl.)
  - signed_corpus_v264_prophetic.json (16 textes prophétiques §264)
  - nipada_v266_graph_v18p.json      (graphe densifié §266)

Calcule :
  - R² sur v263_clean seul (100 textes, graphe v18p) — baseline propre
  - R² sur v264_prophetic seul (16 textes)
  - R² sur merged (116 textes, 1056+ paires)
  - Permutation test (1000 shuffles) sur merged

Sortie :
  nipada/falsification/nipada_v266_revalidation.json

Usage :
  python3 nipada_revalidation_v266.py [--perms N]
"""

from __future__ import annotations

import json
import math
import multiprocessing as mp
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Localisation du répertoire nipada ────────────────────────────────────────
_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

FALSI_DIR  = _NIPADA / "falsification"
CORPUS_DIR = _NIPADA / "corpus"

GRAPH_PATH   = FALSI_DIR / "nipada_v266_graph_v18p.json"
V220_PATH    = FALSI_DIR / "nipada_v220_vopt_calibration.json"
C263_PATH    = CORPUS_DIR / "signed_corpus_v263_clean.json"
C264_PATH    = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
OUT_PATH     = FALSI_DIR / "nipada_v266_revalidation.json"

VOPT_DEFAULT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# ── Globals pour multiprocessing ─────────────────────────────────────────────
_DTOPO_GLOBAL = None
_DLEX_GLOBAL  = None


# ── Fonctions core ────────────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(
    edges: list[dict], weights: dict[str, float]
) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = weights[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(
    source: str,
    adj: dict[str, list[tuple[str, float]]],
    targets: set[str],
) -> dict[str, float]:
    import heapq
    dist = {source: 0.0}
    pq   = [(0.0, source)]
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
    sx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return (num / (sx * sy)) ** 2


def merge_corpora(c1: list[dict], c2: list[dict]) -> list[dict]:
    out: dict[str, dict] = {}
    for s in c1:
        out[s["graph_node_id"]] = s
    for s in c2:
        out[s["graph_node_id"]] = s
    return list(out.values())


def eval_corpus(
    adj: dict[str, list[tuple[str, float]]],
    signed: list[dict],
) -> dict:
    ids    = [s["graph_node_id"] for s in signed]
    sigs   = {s["graph_node_id"]: v14_vector(s["v14_signature"]) for s in signed}
    id_set = set(ids)
    d_topo: list[float] = []
    d_lex:  list[float] = []
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

    return {
        "n_signed": len(signed),
        "n_pairs_finite": len(d_topo),
        "n_pairs_infinite": inf_count,
        "r2": round(pearson_r2(d_topo, d_lex), 4),
        "d_topo": d_topo,
        "d_lex": d_lex,
    }


def _init_worker_perm(dtopo: list[float], dlex: list[float]) -> None:
    global _DTOPO_GLOBAL, _DLEX_GLOBAL
    _DTOPO_GLOBAL = dtopo
    _DLEX_GLOBAL  = dlex


def _worker_perm(seed: int) -> float:
    rng = random.Random(seed)
    shuffled = list(_DLEX_GLOBAL)
    rng.shuffle(shuffled)
    return pearson_r2(_DTOPO_GLOBAL, shuffled)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    t0 = time.time()
    n_perm = 1000
    if "--perms" in sys.argv:
        idx = sys.argv.index("--perms")
        if idx + 1 < len(sys.argv):
            n_perm = int(sys.argv[idx + 1])

    print("=" * 65)
    print("§266 — Revalidation densification prophétique (v18p)")
    print("=" * 65)

    # ── Vérification des fichiers ────────────────────────────────────────────
    for p in [GRAPH_PATH, C263_PATH, C264_PATH]:
        if not p.exists():
            sys.exit(f"ERROR: fichier manquant: {p}")

    # ── Chargement ───────────────────────────────────────────────────────────
    print(f"\nGraphe  : {GRAPH_PATH.name}")
    graph  = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    n_nodes = len(graph["nodes"])
    n_edges = len(graph["edges"])
    graph_version = graph.get("version", "?")
    print(f"  {n_nodes} nœuds, {n_edges} arêtes, version={graph_version}")

    print(f"\nVOPT : chargement depuis {V220_PATH.name if V220_PATH.exists() else 'fallback'}...")
    if V220_PATH.exists():
        v220 = json.loads(V220_PATH.read_text(encoding="utf-8"))
        vopt = v220.get("v_opt_v5_best_cv", {}).get("weights", VOPT_DEFAULT)
    else:
        vopt = VOPT_DEFAULT
    print(f"  {vopt}")

    print(f"\nCorpus base  : {C263_PATH.name}")
    c263_data = json.loads(C263_PATH.read_text(encoding="utf-8"))
    s263 = c263_data.get("signed", [])
    print(f"  {len(s263)} textes signés")

    print(f"\nCorpus ext   : {C264_PATH.name}")
    c264_data = json.loads(C264_PATH.read_text(encoding="utf-8"))
    s264 = c264_data.get("signed", [])
    print(f"  {len(s264)} textes signés")

    smerge = merge_corpora(s263, s264)
    print(f"\nMergé        : {len(smerge)} textes ({len(s263)} + {len(s264)})")

    # ── Construction adjacence ───────────────────────────────────────────────
    print("\nConstruction de l'adjacence...")
    adj = build_adjacency(graph["edges"], vopt)
    print(f"  {len(adj)} nœuds dans l'adjacence")

    # ── Évaluation R² ────────────────────────────────────────────────────────
    print("\nCalcul R² corpus v263_clean (100 textes, graphe v18p)...")
    t1 = time.time()
    m263 = eval_corpus(adj, s263)
    print(f"  R² = {m263['r2']:.4f} ({m263['n_pairs_finite']} paires, "
          f"{m263['n_pairs_infinite']} inf | {time.time()-t1:.1f}s)")

    print("\nCalcul R² corpus v264_prophetic (16 textes)...")
    t1 = time.time()
    m264 = eval_corpus(adj, s264)
    print(f"  R² = {m264['r2']:.4f} ({m264['n_pairs_finite']} paires, "
          f"{m264['n_pairs_infinite']} inf | {time.time()-t1:.1f}s)")

    print("\nCalcul R² corpus merged (116 textes)...")
    t1 = time.time()
    mmerge = eval_corpus(adj, smerge)
    print(f"  R² = {mmerge['r2']:.4f} ({mmerge['n_pairs_finite']} paires, "
          f"{mmerge['n_pairs_infinite']} inf | {time.time()-t1:.1f}s)")

    # ── Permutation test (multiprocessing) ───────────────────────────────────
    n_cpu     = mp.cpu_count() or 4
    n_workers = max(1, n_cpu - 2)
    seeds     = list(range(26500, 26500 + n_perm))
    chunk     = max(1, n_perm // (n_workers * 4))

    print(f"\nPermutation test (merged, n_perm={n_perm}, workers={n_workers})...")
    t1 = time.time()
    try:
        mp.set_start_method("fork", force=True)
    except RuntimeError:
        pass
    r2_perms: list[float] = []
    with mp.Pool(
        processes=n_workers,
        initializer=_init_worker_perm,
        initargs=(mmerge["d_topo"], mmerge["d_lex"]),
    ) as pool:
        for i, r in enumerate(
            pool.imap_unordered(_worker_perm, seeds, chunksize=chunk), start=1
        ):
            r2_perms.append(r)
            if n_perm >= 10 and i % max(1, n_perm // 10) == 0:
                print(f"  {int(i / n_perm * 100)}%")

    print(f"  Permutations calculées en {time.time()-t1:.1f}s")

    mean_p  = sum(r2_perms) / len(r2_perms)
    std_p   = math.sqrt(sum((x - mean_p) ** 2 for x in r2_perms) / len(r2_perms))
    p_value = sum(1 for r in r2_perms if r >= mmerge["r2"]) / len(r2_perms)
    z_score = (mmerge["r2"] - mean_p) / std_p if std_p > 0 else float("inf")
    rs      = sorted(r2_perms)
    ci_lo   = rs[max(0, int(0.025 * len(rs)))]
    ci_hi   = rs[min(len(rs) - 1, int(0.975 * len(rs)))]

    # ── Résumé ────────────────────────────────────────────────────────────────
    delta = mmerge["r2"] - 0.5980  # comparaison §264 baseline
    print(f"\n── Résultats §266 ────────────────────────────────────────────────")
    print(f"  R² v263_clean (100 textes, v18p) = {m263['r2']:.4f}")
    print(f"  R² v264_prophetic seul (16 textes)= {m264['r2']:.4f}")
    print(f"  R² merged (116 textes)            = {mmerge['r2']:.4f}")
    print(f"  Δ vs §264 baseline (0.5980)       = {delta:+.4f}")
    print(f"  z = {z_score:.2f}, p = {p_value:.4f}")
    print(f"  Permutation 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"  Paires inf. (excluded): {mmerge['n_pairs_infinite']}")
    print(f"  Durée totale: {time.time()-t0:.1f}s")

    # ── Écriture résultats ────────────────────────────────────────────────────
    out = {
        "section": "§266",
        "graph": graph_version,
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        "r2_v263_clean": m263["r2"],
        "r2_v264_prophetic_only": m264["r2"],
        "r2_merged": mmerge["r2"],
        "delta_vs_v264": round(delta, 4),
        "n_v263": len(s263),
        "n_v264": len(s264),
        "n_merged": len(smerge),
        "n_pairs_v263": m263["n_pairs_finite"],
        "n_pairs_merged": mmerge["n_pairs_finite"],
        "n_pairs_infinite_merged": mmerge["n_pairs_infinite"],
        "vopt": vopt,
        "permutation": {
            "n_perms": n_perm,
            "z_score": round(z_score, 4),
            "p_value": round(p_value, 4),
            "ci_95": [round(ci_lo, 4), round(ci_hi, 4)],
            "mean_null": round(mean_p, 4),
            "std_null": round(std_p, 4),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", ""),
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRésultats écrits : {OUT_PATH}")


if __name__ == "__main__":
    main()

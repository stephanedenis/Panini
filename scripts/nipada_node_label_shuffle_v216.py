#!/usr/bin/env python3
"""
§216 — Node-Label Shuffle Falsification Test
=============================================
Test de falsification complémentaire à §215 :
  - §215 : shuffle des *canaux* d'arêtes  → V_OPT capture la sémantique
           des canaux, pas seulement la topologie
  - §216 : shuffle des *étiquettes nœuds* (V14 signatures) → la disposition
           spatiale des œuvres dans le graphe est sémantiquement cohérente,
           pas aléatoire

Protocole :
  1. Charger graphe v12 + corpus signé (37 nœuds)
  2. Construire adj (non-dirigé, V_OPT v3) — une seule fois
  3. Calculer la matrice d_topo (37 Dijkstra) — une seule fois
  4. Calculer R²_real avec les vraies affectations nœud→V14
  5. N=100 shuffles : permuter aléatoirement les signatures V14 entre les
     37 nœuds, recalculer R²(d_topo, d_lex_permuted) sans Dijkstra
  6. Verdict PASS si R²_real > p95(R²_shuffled)

Hypothèse :
  Si PASS → les œuvres sémantiquement proches sont spatialement proches
            dans le graphe d'influence (non-aléatoire)
  Sinon   → la correspondance d_topo/d_lex est fortuite

V_OPT v3 : (w_direct=0.45, w_translation=0.05, w_indirect=0.05)
Graphe    : nipada_v210a_graph_v12.json  (1764 nodes / 26112 edges)
Signed    : signed_corpus_v208.json      (37 nœuds avec V14 signatures)

Usage : python3 scripts/nipada_node_label_shuffle_v216.py
Sortie : research/nipada/falsification/nipada_v216_node_label_shuffle.json
"""

import json
import heapq
import random
import math
import time
from pathlib import Path

# ─── Chemins ───────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_CANDIDATES = [
    _SCRIPT_DIR.parent / "research" / "nipada",
    _SCRIPT_DIR.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

GRAPH_PATH  = _NIPADA / "falsification/nipada_v210a_graph_v12.json"
SIGNED_PATH = _NIPADA / "corpus/signed_corpus_v208.json"
OUT_PATH    = _NIPADA / "falsification/nipada_v216_node_label_shuffle.json"

# ─── V_OPT v3 ──────────────────────────────────────────────────────────────
V_OPT_V3 = {"direct": 0.45, "translation": 0.05, "indirect": 0.05}

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

N_SHUFFLE = 100
SEED      = 2026


# ─── Primitives ────────────────────────────────────────────────────────────

def classify_channel(ch: str) -> str:
    ch_low = ch.lower()
    if "traduction" in ch_low or ch_low == "idem traduction":
        return "translation"
    if "direct" in ch_low:
        return "direct"
    return "indirect"


def build_adjacency(edges: list) -> dict:
    """Adjacence non-dirigée, V_OPT v3."""
    adj: dict = {}
    for e in edges:
        src, tgt = e["src"], e["tgt"]
        cost = V_OPT_V3[classify_channel(e["channel"])]
        adj.setdefault(src, []).append((tgt, cost))
        adj.setdefault(tgt, []).append((src, cost))
    return adj


def dijkstra_from(source: str, adj: dict, targets: set) -> dict:
    """Dijkstra avec early-stop quand tous les targets sont trouvés."""
    dist      = {source: 0.0}
    pq        = [(0.0, source)]
    remaining = set(targets) - {source}
    found: dict = {}
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


def v14_vector(sig: dict) -> list:
    return [sig.get(a, 0.0) for a in V14_ATOMS]


def l2_distance(v1: list, v2: list) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def pearson_r(xs: list, ys: list) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return num / (sx * sy)


def build_dtopo_matrix(ids: list, adj: dict) -> dict:
    """
    Calcule d_topo entre toutes les paires de nœuds signés.
    Retourne un dict {(i,j): d_topo} pour i < j (indices dans `ids`).
    """
    id_set  = set(ids)
    dtopo   = {}
    for i, src in enumerate(ids):
        distances = dijkstra_from(src, adj, id_set)
        for j in range(i + 1, len(ids)):
            dt = distances[ids[j]]
            if not math.isinf(dt):
                dtopo[(i, j)] = dt
    return dtopo


def compute_r2_from_matrix(
    dtopo: dict, sigs_vec: list, perm: list | None = None
) -> tuple:
    """
    Calcule R²(d_topo, d_lex) à partir de la matrice précalculée.

    Args:
        dtopo    : {(i,j): d_topo} pour i < j
        sigs_vec : liste ordonnée des vecteurs V14 (dans l'ordre des ids)
        perm     : permutation des indices de signatures (None = identité)

    Returns:
        (r2, n_pairs)
    """
    if perm is None:
        perm = list(range(len(sigs_vec)))

    d_topo_list = []
    d_lex_list  = []
    for (i, j), dt in dtopo.items():
        dl = l2_distance(sigs_vec[perm[i]], sigs_vec[perm[j]])
        d_topo_list.append(dt)
        d_lex_list.append(dl)

    if len(d_topo_list) < 2:
        return 0.0, 0
    r = pearson_r(d_topo_list, d_lex_list)
    return r * r, len(d_topo_list)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("§216 — Node-Label Shuffle Falsification Test")
    print(f"  graph  : {GRAPH_PATH}")
    print(f"  signed : {SIGNED_PATH}")
    print()

    graph  = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    corpus = json.loads(SIGNED_PATH.read_text(encoding="utf-8"))

    edges  = graph["edges"]
    signed = [s for s in corpus["signed"] if s["matched"]]
    n      = len(signed)

    print(f"  edges  : {len(edges)}")
    print(f"  signed : {n}")
    print(f"  pairs  : {n * (n - 1) // 2}")
    print()

    # ── Adjacence (calculée une seule fois) ──────────────────────────────
    adj  = build_adjacency(edges)
    ids  = [s["graph_node_id"] for s in signed]
    sigs_vec = [v14_vector(s["v14_signature"]) for s in signed]

    # ── Matrice d_topo (calculée une seule fois — 37 Dijkstra) ───────────
    print("  Calcul matrice d_topo (37 Dijkstra) ...", flush=True)
    t_dijkstra = time.time()
    dtopo = build_dtopo_matrix(ids, adj)
    print(f"  Matrice d_topo : {len(dtopo)} paires connectées  "
          f"({time.time() - t_dijkstra:.1f}s)")
    print()

    # ── R² réel ──────────────────────────────────────────────────────────
    r2_real, n_pairs_used = compute_r2_from_matrix(dtopo, sigs_vec)
    print(f"  R²_real = {r2_real:.6f}  (n_pairs = {n_pairs_used})")
    print()

    # ── Node-label shuffle ───────────────────────────────────────────────
    rng = random.Random(SEED)
    indices = list(range(n))
    r2_shuffled = []
    for k in range(N_SHUFFLE):
        perm = indices[:]
        rng.shuffle(perm)
        r2_s, _ = compute_r2_from_matrix(dtopo, sigs_vec, perm=perm)
        r2_shuffled.append(r2_s)
        if (k + 1) % 10 == 0:
            print(f"  shuffle {k+1:3d}/{N_SHUFFLE} | running mean R²_shuf = "
                  f"{sum(r2_shuffled) / len(r2_shuffled):.6f}", flush=True)

    mean_shuf = sum(r2_shuffled) / N_SHUFFLE
    std_shuf  = math.sqrt(sum((x - mean_shuf) ** 2 for x in r2_shuffled) / N_SHUFFLE)
    p95_shuf  = sorted(r2_shuffled)[int(0.95 * N_SHUFFLE) - 1]
    verdict   = "PASS" if r2_real > p95_shuf else "FAIL"

    elapsed = time.time() - t0
    print()
    print(f"  R²_real              = {r2_real:.6f}")
    print(f"  R²_shuffled mean±σ   = {mean_shuf:.6f} ± {std_shuf:.6f}")
    print(f"  R²_shuffled p95      = {p95_shuf:.6f}")
    print(f"  Verdict              : {verdict}")
    print(f"  Elapsed              : {elapsed:.1f}s")
    print()
    if verdict == "PASS":
        ratio = r2_real / p95_shuf if p95_shuf > 0 else float("inf")
        print(f"  ✓ Disposition spatiale non-aléatoire : R²_real = {ratio:.1f}× p95")
        print("  → Les œuvres sémantiquement proches sont spatialement proches")
    else:
        print("  ✗ FAIL : R²_real ≤ p95 (disposition possiblement fortuite)")

    # ── Résultats JSON ───────────────────────────────────────────────────
    result = {
        "section": "§216",
        "test":    "node_label_shuffle",
        "description": (
            "Permutation aléatoire des V14 signatures entre les 37 nœuds signés. "
            "d_topo calculée une seule fois (graphe intact). "
            "PASS si R²_real > p95(R²_shuffled)."
        ),
        "params": {
            "n_shuffle": N_SHUFFLE,
            "seed":      SEED,
            "v_opt_v3":  V_OPT_V3,
        },
        "data": {
            "n_edges":      len(edges),
            "n_signed":     n,
            "n_pairs_used": n_pairs_used,
        },
        "results": {
            "r2_real":           round(r2_real, 6),
            "r2_shuffled_mean":  round(mean_shuf, 6),
            "r2_shuffled_std":   round(std_shuf, 6),
            "r2_shuffled_p95":   round(p95_shuf, 6),
            "ratio_real_over_p95": round(r2_real / p95_shuf, 2) if p95_shuf > 0 else None,
            "verdict":           verdict,
            "elapsed_s":         round(elapsed, 1),
        },
        "interpretation": (
            "La disposition spatiale des œuvres dans le graphe d'influence "
            "est sémantiquement cohérente (non-aléatoire)."
            if verdict == "PASS" else
            "La correspondance d_topo/d_lex ne dépasse pas le seuil de "
            "signification pour ce test de disposition spatiale."
        ),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"  → Résultat écrit : {OUT_PATH}")


if __name__ == "__main__":
    main()

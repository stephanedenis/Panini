"""§211 — Validation croisée k-fold (k=5) de V_OPT v3 sur graph v12.

Objectif : confirmer absence d'overfit du triplet (0.45, 0.05, 0.05) calibré en §210b
sur la totalité des paires signées (n=666). Stratégie : 5-fold sur les 666 paires,
on calcule R² sur chaque fold-test puis on vérifie cohérence.

Output :
- research/nipada/falsification/nipada_v211_kfold_cv.json
- docs/rapports/KFOLD_CV_VOPT_V3_v0.4.0.md
"""
from __future__ import annotations
import json
import math
import random
import sys
import heapq
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import nipada_calibration_v177 as v177  # type: ignore

GRAPH_V12 = ROOT / "research" / "nipada" / "falsification" / "nipada_v210a_graph_v12.json"
SIGNED_CORPUS = ROOT / "research" / "nipada" / "corpus" / "signed_corpus_v208.json"
OUT_JSON = ROOT / "research" / "nipada" / "falsification" / "nipada_v211_kfold_cv.json"
OUT_MD = ROOT / "docs" / "rapports" / "KFOLD_CV_VOPT_V3_v0.4.0.md"

V_OPT_V3 = (0.45, 0.05, 0.05)
V_OPT_V1 = (0.45, 0.15, 0.01)
N_FOLDS = 5
SEED = 2026


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def build_adj(edges, weight_map):
    adj: dict[str, dict[str, float]] = defaultdict(dict)
    for e in edges:
        ch = v177.classify_channel(e.get("channel", ""))
        w = weight_map.get(ch, 0.01)
        if w <= 0:
            continue
        cost = -math.log(w)
        s, t = e["src"], e["tgt"]
        if t not in adj[s] or cost < adj[s][t]:
            adj[s][t] = cost
        if s not in adj[t] or cost < adj[t][s]:
            adj[t][s] = cost
    return adj


def dijkstra(adj, source, targets):
    dist = {source: 0.0}
    pq = [(0.0, source)]
    found: dict[str, float] = {}
    targets_set = set(targets)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        if u in targets_set:
            found[u] = d
            if len(found) == len(targets_set):
                break
        for v, w in adj[u].items():
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return found


def compute_pair_distances(edges, work_ids, wd, wt, wi):
    adj = build_adj(edges, {"direct": wd, "translation": wt, "indirect": wi})
    signed_set = set(work_ids)
    d_pair: dict[tuple[str, str], float] = {}
    for src in work_ids:
        res = dijkstra(adj, src, signed_set)
        for tgt, dst in res.items():
            key = (src, tgt) if src < tgt else (tgt, src)
            d_pair[key] = dst
    return d_pair


def main() -> int:
    g = json.loads(GRAPH_V12.read_text())
    nodes = g["nodes"] if isinstance(g["nodes"], dict) else {n["id"]: n for n in g["nodes"]}
    edges = g["edges"]
    corpus = json.loads(SIGNED_CORPUS.read_text())
    work_ids = [w["graph_node_id"] for w in corpus["signed"] if w["graph_node_id"] in nodes]
    sig = {w["graph_node_id"]: w["v14_signature"] for w in corpus["signed"]}

    # construire toutes les paires
    pairs = []
    for i, a in enumerate(work_ids):
        for b in work_ids[i + 1:]:
            d_lex = 1 - cosine(sig[a], sig[b])
            pairs.append({"a": a, "b": b, "d_lex": d_lex})
    print(f"Pairs total : {len(pairs)}")

    rng = random.Random(SEED)
    indices = list(range(len(pairs)))
    rng.shuffle(indices)
    fold_size = len(indices) // N_FOLDS
    folds = [indices[i * fold_size:(i + 1) * fold_size] for i in range(N_FOLDS)]
    # last fold takes remainder
    folds[-1].extend(indices[N_FOLDS * fold_size:])

    # Précalcul des distances pour V_OPT v3 et v1
    print("Calcul Dijkstra pour V_OPT v3...")
    d_v3 = compute_pair_distances(edges, work_ids, *V_OPT_V3)
    print("Calcul Dijkstra pour V_OPT v1...")
    d_v1 = compute_pair_distances(edges, work_ids, *V_OPT_V1)

    def eval_fold(fold_indices, d_pair):
        xs, ys = [], []
        for i in fold_indices:
            p = pairs[i]
            key = (p["a"], p["b"]) if p["a"] < p["b"] else (p["b"], p["a"])
            d = d_pair.get(key)
            if d is None or not math.isfinite(d):
                continue
            xs.append(p["d_lex"]); ys.append(d)
        if len(xs) < 10:
            return 0.0, 1.0, len(xs)
        r2 = v177.pearson(xs, ys) ** 2
        p = v177.perm_test(xs, ys, n_iter=1000)
        return r2, p, len(xs)

    results_v3 = []
    results_v1 = []
    for k in range(N_FOLDS):
        test_idx = folds[k]
        r2_v3, p_v3, n_v3 = eval_fold(test_idx, d_v3)
        r2_v1, p_v1, n_v1 = eval_fold(test_idx, d_v1)
        results_v3.append({"fold": k, "R2": r2_v3, "p": p_v3, "n": n_v3})
        results_v1.append({"fold": k, "R2": r2_v1, "p": p_v1, "n": n_v1})
        print(f"Fold {k}: V_OPT v3 R²={r2_v3:.4f} p={p_v3:.4f} n={n_v3} | V_OPT v1 R²={r2_v1:.4f} p={p_v1:.4f}")

    mean_v3 = sum(r["R2"] for r in results_v3) / N_FOLDS
    mean_v1 = sum(r["R2"] for r in results_v1) / N_FOLDS
    var_v3 = sum((r["R2"] - mean_v3) ** 2 for r in results_v3) / N_FOLDS
    var_v1 = sum((r["R2"] - mean_v1) ** 2 for r in results_v1) / N_FOLDS
    std_v3 = math.sqrt(var_v3)
    std_v1 = math.sqrt(var_v1)

    sig_count_v3 = sum(1 for r in results_v3 if r["p"] < 0.05)
    sig_count_v1 = sum(1 for r in results_v1 if r["p"] < 0.05)

    verdict = "PASS" if (mean_v3 > 0 and sig_count_v3 >= 3) else "REVUE"

    out = {
        "version": "v211",
        "k_folds": N_FOLDS,
        "seed": SEED,
        "n_pairs": len(pairs),
        "v_opt_v3": list(V_OPT_V3),
        "v_opt_v1": list(V_OPT_V1),
        "results_v3": results_v3,
        "results_v1": results_v1,
        "mean_R2_v3": mean_v3,
        "std_R2_v3": std_v3,
        "mean_R2_v1": mean_v1,
        "std_R2_v1": std_v1,
        "sig_folds_v3": sig_count_v3,
        "sig_folds_v1": sig_count_v1,
        "verdict": verdict,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    md_lines = [
        "# §211 — Validation croisée k-fold (k=5) sur V_OPT v3",
        "",
        f"**Verdict :** {verdict}",
        f"**Paires :** {len(pairs)} | **Folds :** {N_FOLDS} | **Seed :** {SEED}",
        "",
        "## Résultats par fold",
        "",
        "| Fold | n | V_OPT v3 R² | v3 p | V_OPT v1 R² | v1 p |",
        "|---|---|---|---|---|---|",
    ]
    for k in range(N_FOLDS):
        r3 = results_v3[k]; r1 = results_v1[k]
        md_lines.append(f"| {k} | {r3['n']} | {r3['R2']:.4f} | {r3['p']:.4f} | {r1['R2']:.4f} | {r1['p']:.4f} |")
    md_lines += [
        "",
        f"**V_OPT v3 :** mean R² = {mean_v3:.4f} (σ={std_v3:.4f}), folds significatifs = {sig_count_v3}/{N_FOLDS}",
        f"**V_OPT v1 :** mean R² = {mean_v1:.4f} (σ={std_v1:.4f}), folds significatifs = {sig_count_v1}/{N_FOLDS}",
        "",
        f"**Conclusion :** {verdict}.",
    ]
    OUT_MD.write_text("\n".join(md_lines) + "\n")

    print(f"\nMean R² v3 = {mean_v3:.4f} ± {std_v3:.4f} | sig={sig_count_v3}/{N_FOLDS}")
    print(f"Mean R² v1 = {mean_v1:.4f} ± {std_v1:.4f} | sig={sig_count_v1}/{N_FOLDS}")
    print(f"Verdict : {verdict}")
    print(f"Sortie  : {OUT_JSON.relative_to(ROOT)}")
    print(f"Rapport : {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

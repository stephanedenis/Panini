#!/usr/bin/env python3
"""§187 — Grid 2D calibration fine sur w_indirect × w_translation.

§186 a établi w_indirect=0.05 comme sweet spot (R² 0.030→0.042).
§187 raffine : grille 2D pour confirmer optimum et identifier zone stable.

Métrique objective composite :
  score = R²_GLOBAL × √R²_WEST × LOO_min

Privilégie :
- Signal global fort
- Signal occidental significatif (révélé par §186)
- Robustesse worst-case (LOO minimum)
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

EAST_TRADS = {
    "chinese_classics", "daoism", "buddhism_theravada", "hinduism_smriti",
    "hinduism_shruti", "buddhism_modernist", "islamic_canon",
    "islamic_skeptic", "chinese_critic", "chinese_classical",
    "chinese_legalist", "chinese_mohist",
}


def classify_channel(ch: str) -> str:
    s = ch.lower()
    if any(k in s for k in ["traduction", "translation"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "tradition",
        "comparat", "scepticisme", "lecteur", "ascendant", "post-",
        "écho", "reçu", "même école", "succession", "admire", "mentionne",
        "réception", "critique", "synthèse", "commentaire", "compile",
        "milieu",
    ]):
        return "indirect"
    return "direct"


def floyd_warshall(node_ids, edges_with_weight):
    idx = {n: i for i, n in enumerate(node_ids)}
    N = len(node_ids)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0.0
    for s, t, w in edges_with_weight:
        if s not in idx or t not in idx:
            continue
        cost = -math.log(w)
        i, j = idx[s], idx[t]
        if cost < D[i][j]:
            D[i][j] = cost
            D[j][i] = cost
    for k in range(N):
        for i in range(N):
            dik = D[i][k]
            if dik == INF:
                continue
            for j in range(N):
                nd = dik + D[k][j]
                if nd < D[i][j]:
                    D[i][j] = nd
    return D, idx


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx and dy else 0.0


def perm_test(xs, ys, n_iter=1000, seed=2026):
    rnd = random.Random(seed)
    obs = abs(pearson(xs, ys))
    ge = 0
    yl = list(ys)
    for _ in range(n_iter):
        rnd.shuffle(yl)
        if abs(pearson(xs, yl)) >= obs:
            ge += 1
    return (ge + 1) / (n_iter + 1)


def cosine_dict(a, b):
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def load_v14_lex():
    spec = importlib.util.spec_from_file_location(
        "v14lex", ROOT / "scripts" / "nipada_v14_multiling_v145.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


def freq_signature(text, lex, lang="eng"):
    txt_l = text.lower()
    sig = {}
    for atom, langs in lex.items():
        terms = list(set(langs.get(lang, []) + langs.get("eng", []) + langs.get("fra", [])))
        c = sum(txt_l.count(t.lower()) for t in terms if t)
        sig[atom] = c
    s = sum(sig.values()) or 1
    return {a: v / s for a, v in sig.items()}


def build_pairs(node_ids, edges_w, sigs):
    D, idx = floyd_warshall(node_ids, edges_w)
    work_ids = [w for w in sigs if w in idx]
    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            d_lex = 1.0 - cosine_dict(sigs[a], sigs[b])
            pairs.append((a, b, d_g, d_lex))
    return pairs


def stratify(pairs, trads):
    nw_ids = {w for w, t in trads.items() if t in EAST_TRADS}
    west = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
    inter = [p for p in pairs if (p[0] in nw_ids) != (p[1] in nw_ids)]
    nw = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]
    return west, inter, nw


def stat(pp):
    if len(pp) < 3:
        return 0.0, 1.0
    xs = [x[2] for x in pp]
    ys = [x[3] for x in pp]
    r = pearson(xs, ys)
    return r * r, perm_test(xs, ys, n_iter=500)


def loo_min(node_ids, edges_w, sigs, trads):
    """Min R² across LOO by tradition."""
    all_trads = sorted(set(trads.values()) - {"unknown"})
    r2s = []
    for held in all_trads:
        kept = {w for w, t in trads.items() if t != held}
        sigs_kept = {k: v for k, v in sigs.items() if k in kept}
        if len(sigs_kept) < 4:
            continue
        pairs = build_pairs(node_ids, edges_w, sigs_kept)
        if len(pairs) < 5:
            continue
        xs = [p[2] for p in pairs]
        ys = [p[3] for p in pairs]
        r = pearson(xs, ys)
        r2s.append(r * r)
    return (min(r2s), max(r2s), sum(r2s) / len(r2s)) if r2s else (0.0, 0.0, 0.0)


def main():
    print("=== §187 — Grid 2D calibration w_indirect × w_translation ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges")

    edges_typed = []
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        cat = classify_channel(e.get("channel", ""))
        edges_typed.append((s, t, cat))

    node_ids = list(nodes.keys())

    # Charger signatures
    lex = load_v14_lex()
    sigs, trads = {}, {}
    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        prov_p = wdir / "PROVENANCE.json"
        frags_p = wdir / "fragments.jsonl"
        if not (prov_p.exists() and frags_p.exists()):
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", wdir.name)
        text = ""
        with frags_p.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                text += (rec.get("text") or rec.get("raw_text", "")) + "\n"
        if not text.strip():
            continue
        lang = prov.get("text_language", "eng")
        if lang in ("en", "english"):
            lang = "eng"
        elif lang == "zh":
            lang = "lzh"
        sigs[wid] = freq_signature(text, lex, lang)
        trads[wid] = prov.get("tradition") or "unknown"
    print(f"Signatures: {len(sigs)} œuvres")

    # Grille 2D
    w_indirect_grid = [0.01, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30]
    w_translation_grid = [0.05, 0.15, 0.30, 0.45, 0.60]
    w_direct = 0.45  # fixé (§177 confirmé optimal pour direct)

    print(f"\nGrille : w_indirect ({len(w_indirect_grid)}) × "
          f"w_translation ({len(w_translation_grid)}) "
          f"= {len(w_indirect_grid) * len(w_translation_grid)} cellules\n")

    results = []
    print(f"{'w_ind':>7}{'w_trn':>7}{'n_p':>5}"
          f"{'GLOB R²':>10}{'WEST R²':>9}{'INTER R²':>10}"
          f"{'LOO_min':>9}{'LOO_med':>9}{'score':>10}")
    print("-" * 80)

    for w_i in w_indirect_grid:
        for w_t in w_translation_grid:
            wm = {"direct": w_direct, "translation": w_t, "indirect": w_i}
            edges_w = [(s, t, wm[c]) for s, t, c in edges_typed]
            pairs = build_pairs(node_ids, edges_w, sigs)
            r2_glob, p_glob = stat(pairs)
            west, inter, nw = stratify(pairs, trads)
            r2_w, _ = stat(west)
            r2_i, _ = stat(inter)
            r2_n, _ = stat(nw)
            loo_lo, loo_hi, loo_avg = loo_min(node_ids, edges_w, sigs, trads)
            score = r2_glob * math.sqrt(max(r2_w, 0)) * max(loo_lo, 1e-6)

            row = {
                "w_indirect": w_i, "w_translation": w_t, "w_direct": w_direct,
                "n_pairs": len(pairs),
                "global": {"R2": round(r2_glob, 4), "p": round(p_glob, 4)},
                "west": {"R2": round(r2_w, 4)},
                "inter": {"R2": round(r2_i, 4)},
                "nw": {"R2": round(r2_n, 4)},
                "loo": {"min": round(loo_lo, 4), "max": round(loo_hi, 4),
                        "avg": round(loo_avg, 4)},
                "score": round(score, 6),
            }
            results.append(row)
            print(f"{w_i:>7.3f}{w_t:>7.3f}{len(pairs):>5}"
                  f"{r2_glob:>10.4f}{r2_w:>9.4f}{r2_i:>10.4f}"
                  f"{loo_lo:>9.4f}{loo_avg:>9.4f}{score:>10.6f}")

    # Top 5 par score
    results_sorted = sorted(results, key=lambda r: r["score"], reverse=True)
    print("\n=== TOP 5 par score composite ===")
    print(f"{'rank':<5}{'w_ind':>7}{'w_trn':>7}{'GLOB':>9}{'WEST':>9}"
          f"{'LOO_min':>9}{'score':>10}")
    for i, r in enumerate(results_sorted[:5]):
        print(f"{i+1:<5}{r['w_indirect']:>7.3f}{r['w_translation']:>7.3f}"
              f"{r['global']['R2']:>9.4f}{r['west']['R2']:>9.4f}"
              f"{r['loo']['min']:>9.4f}{r['score']:>10.6f}")

    best = results_sorted[0]
    print(f"\n=== OPTIMUM ===")
    print(f"  w_indirect    = {best['w_indirect']}")
    print(f"  w_translation = {best['w_translation']}")
    print(f"  w_direct      = {best['w_direct']}")
    print(f"  GLOBAL R²     = {best['global']['R2']}")
    print(f"  WEST R²       = {best['west']['R2']}")
    print(f"  LOO min       = {best['loo']['min']}")

    out = {
        "version": "0.2.7",
        "iteration": "v187_grid2d",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v182_graph_v8.json",
        "n_signatures": len(sigs),
        "w_direct_fixed": w_direct,
        "w_indirect_grid": w_indirect_grid,
        "w_translation_grid": w_translation_grid,
        "score_formula": "R²_global × √R²_west × LOO_min",
        "all_cells": results,
        "top5": results_sorted[:5],
        "optimum": best,
    }
    out_p = RES_DIR / "nipada_v187_grid2d.json"
    out_p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

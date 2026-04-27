#!/usr/bin/env python3
"""§186 — Revalidation complète du pipeline NIPADA sans/avec indirects atténués.

§185 a montré que les arêtes indirectes (w=0.30) MASQUENT le signal NIPADA
au lieu de le porter (R² INTER passe de 0.022 à 0.240 sans elles).

§186 reconstruit le pipeline complet (Bootstrap + Permutation + LOO inter-trad)
avec deux variantes pour ancrer le résultat :
  - V_NOIND  : indirects exclus (binarisation : direct=0.45, translation=0.45)
  - V_W005   : indirects à w=0.05 (×6 plus faibles que original §177)

Pour chaque variante, on évalue :
  1. R² global + p (permutation 2000)
  2. Bootstrap n=2000 → IC₉₅
  3. Stratification : INTER, NW×NW, WEST×WEST
  4. LOO par tradition (croise §174)

Comparaison vs ORIGINAL §178 (w=0.30) : la reconstruction confirme-t-elle §185 ?
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
from collections import defaultdict
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


def perm_test(xs, ys, n_iter=2000, seed=2026):
    rnd = random.Random(seed)
    obs = abs(pearson(xs, ys))
    ge = 0
    yl = list(ys)
    for _ in range(n_iter):
        rnd.shuffle(yl)
        if abs(pearson(xs, yl)) >= obs:
            ge += 1
    return (ge + 1) / (n_iter + 1)


def bootstrap_r2(xs, ys, n_iter=2000, seed=2026):
    rnd = random.Random(seed)
    n = len(xs)
    if n < 5:
        return 0.0, 0.0, 0.0
    rs = []
    for _ in range(n_iter):
        idx = [rnd.randrange(n) for _ in range(n)]
        bx = [xs[i] for i in idx]
        by = [ys[i] for i in idx]
        r = pearson(bx, by)
        rs.append(r * r)
    rs.sort()
    return rs[n_iter // 2], rs[int(n_iter * 0.025)], rs[int(n_iter * 0.975)]


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
    west_pairs = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
    inter_pairs = [p for p in pairs if (p[0] in nw_ids) != (p[1] in nw_ids)]
    nw_pairs = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]
    return {"WEST×WEST": west_pairs, "INTER (W×E)": inter_pairs,
            "NW×NW (E×E)": nw_pairs}


def stat_block(label, pairs, do_bootstrap=True):
    if len(pairs) < 3:
        return {"label": label, "n": len(pairs), "R2": 0.0, "p": 1.0,
                "ci95": [0.0, 0.0]}
    xs = [p[2] for p in pairs]
    ys = [p[3] for p in pairs]
    r = pearson(xs, ys)
    pv = perm_test(xs, ys)
    if do_bootstrap and len(pairs) >= 5:
        med, lo, hi = bootstrap_r2(xs, ys)
    else:
        med, lo, hi = r * r, 0.0, 0.0
    return {"label": label, "n": len(pairs),
            "R2": round(r * r, 4), "p": round(pv, 4),
            "R2_median": round(med, 4),
            "ci95": [round(lo, 4), round(hi, 4)]}


def loo_inter_trad(node_ids, edges_w, sigs, trads, weight_map):
    """LOO par tradition : retire toutes les œuvres d'une tradition,
    mesure R² global sur le reste."""
    all_trads = sorted(set(trads.values()) - {"unknown"})
    results = {}
    for held in all_trads:
        kept_works = {w for w, t in trads.items() if t != held}
        sigs_kept = {k: v for k, v in sigs.items() if k in kept_works}
        if len(sigs_kept) < 4:
            continue
        pairs = build_pairs(node_ids, edges_w, sigs_kept)
        if len(pairs) < 5:
            continue
        xs = [p[2] for p in pairs]
        ys = [p[3] for p in pairs]
        r = pearson(xs, ys)
        results[held] = {"n_works_held": sum(1 for t in trads.values() if t == held),
                         "n_pairs": len(pairs),
                         "R2": round(r * r, 4),
                         "p": round(perm_test(xs, ys, n_iter=1000), 4)}
    return results


def evaluate_variant(label, weight_map, edges_typed, node_ids, sigs, trads):
    edges_w = [(s, t, weight_map.get(c, 0))
               for s, t, _, c in edges_typed
               if weight_map.get(c, 0) > 0]
    pairs = build_pairs(node_ids, edges_w, sigs)

    glob = stat_block("GLOBAL", pairs)
    strata = {k: stat_block(k, v) for k, v in stratify(pairs, trads).items()}
    loo = loo_inter_trad(node_ids, edges_w, sigs, trads, weight_map)

    return {
        "variant": label,
        "weight_map": weight_map,
        "n_edges_used": len(edges_w),
        "n_pairs": glob["n"],
        "global": glob,
        "strata": strata,
        "loo_inter_trad": loo,
    }


def main():
    print("=== §186 — Revalidation pipeline sans/avec indirects atténués ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges")

    edges_typed = []
    counts = {"direct": 0, "translation": 0, "indirect": 0}
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        cat = classify_channel(e.get("channel", ""))
        edges_typed.append((s, t, None, cat))
        counts[cat] += 1
    print(f"  direct={counts['direct']} translation={counts['translation']} indirect={counts['indirect']}")

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

    print(f"  Signatures chargées: {len(sigs)} œuvres")

    variants = [
        ("ORIGINAL §177", {"direct": 0.45, "translation": 0.45, "indirect": 0.30}),
        ("V_W005 (indirects atténués)", {"direct": 0.45, "translation": 0.45, "indirect": 0.05}),
        ("V_NOIND (indirects exclus)", {"direct": 0.45, "translation": 0.45}),
    ]

    print("\n=== Évaluations ===")
    results = []
    for label, wm in variants:
        print(f"\n→ {label}  weights={wm}")
        r = evaluate_variant(label, wm, edges_typed, node_ids, sigs, trads)
        results.append(r)
        g = r["global"]
        print(f"  GLOBAL    : n={g['n']:>3} R²={g['R2']:.4f} p={g['p']:.4f} "
              f"CI95=[{g['ci95'][0]:.4f}, {g['ci95'][1]:.4f}]")
        for sname, s in r["strata"].items():
            print(f"  {sname:<13}: n={s['n']:>3} R²={s['R2']:.4f} p={s['p']:.4f} "
                  f"CI95=[{s['ci95'][0]:.4f}, {s['ci95'][1]:.4f}]")
        loo = r["loo_inter_trad"]
        if loo:
            r2_vals = [v["R2"] for v in loo.values()]
            print(f"  LOO       : {len(loo)} traditions, R² range "
                  f"[{min(r2_vals):.4f}, {max(r2_vals):.4f}], "
                  f"médiane {sorted(r2_vals)[len(r2_vals)//2]:.4f}")

    out = {
        "version": "0.2.6",
        "iteration": "v186_revalidation_no_indirect",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v182_graph_v8.json",
        "edge_counts": counts,
        "n_signatures": len(sigs),
        "variants": results,
    }
    out_p = RES_DIR / "nipada_v186_revalidation.json"
    out_p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""§197 — LOO par arête : sensibilité du signal à chaque arête individuelle.

Pour chaque arête e du graph v9, retirer cette arête seule, recalculer
R² stratifié, mesurer Δ R² = R²(v9 \ {e}) - R²(v9).

Δ négatif = retirer e diminue R² → e est porteuse de signal.
Δ positif = retirer e augmente R² → e est nuisible.
Δ ~ 0 = e neutre (chemin alternatif compense).

Calibration V_OPT.
"""
from __future__ import annotations

import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "research" / "nipada" / "falsification"
CORPUS = ROOT / "corpus" / "protoatheism"

EAST_TRADS = {
    "chinese_classics", "daoism", "buddhism_theravada", "hinduism_smriti",
    "hinduism_shruti", "buddhism_modernist", "islamic_canon",
    "islamic_skeptic", "chinese_critic", "chinese_classical",
    "chinese_legalist", "chinese_mohist",
}
W_OPT = {"direct": 0.45, "translation": 0.15, "indirect": 0.01}


def classify(ch):
    s = (ch or "").lower()
    if any(k in s for k in ["traduction", "translation"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "tradition",
        "comparat", "scepticisme", "lecteur", "ascendant", "post-",
        "écho", "reçu", "même école", "succession", "admire", "mentionne",
        "réception", "critique", "synthèse", "commentaire", "compile",
        "milieu", "contemplative",
    ]):
        return "indirect"
    return "direct"


def floyd(node_ids, edges_w):
    idx = {n: i for i, n in enumerate(node_ids)}
    N = len(node_ids)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0.0
    for s, t, w in edges_w:
        if s not in idx or t not in idx:
            continue
        c = -math.log(w)
        i, j = idx[s], idx[t]
        if c < D[i][j]:
            D[i][j] = c
            D[j][i] = c
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
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx and dy else 0.0


def cosine(a, b):
    keys = set(a) | set(b)
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def load_lex():
    spec = importlib.util.spec_from_file_location(
        "v14lex", ROOT / "scripts" / "nipada_v14_multiling_v145.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


def freq_sig(text, lex, lang="eng"):
    txt = text.lower()
    sig = {}
    for atom, langs in lex.items():
        terms = list(set(
            langs.get(lang, []) + langs.get("eng", []) + langs.get("fra", [])
        ))
        sig[atom] = sum(txt.count(t.lower()) for t in terms if t)
    s = sum(sig.values()) or 1
    return {a: v / s for a, v in sig.items()}


def compute_strata(node_ids, edges_w, sigs, east_set):
    D, idx = floyd(node_ids, edges_w)
    work_ids = sorted(w for w in sigs if w in idx)
    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            d_lex = 1.0 - cosine(sigs[a], sigs[b])
            pairs.append((a, b, d_g, d_lex))
    west = [p for p in pairs if p[0] not in east_set and p[1] not in east_set]
    inter = [p for p in pairs if (p[0] in east_set) != (p[1] in east_set)]
    nw = [p for p in pairs if p[0] in east_set and p[1] in east_set]
    out = {}
    for label, sub in [("GLOBAL", pairs), ("WEST", west),
                       ("INTER", inter), ("NW", nw)]:
        if len(sub) < 3:
            out[label] = (0.0, len(sub))
            continue
        xs = [p[2] for p in sub]
        ys = [p[3] for p in sub]
        out[label] = (pearson(xs, ys) ** 2, len(sub))
    return out


def main():
    print("=== §197 — LOO par arête (V_OPT, graph v9) ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]
    print(f"Graph v9: {len(nodes)} nodes, {len(edges)} edges")

    lex = load_lex()
    sigs, trads = {}, {}
    for d in sorted(CORPUS.iterdir()):
        prov_p = d / "PROVENANCE.json"
        frags_p = d / "fragments.jsonl"
        if not (prov_p.exists() and frags_p.exists()):
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", d.name)
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
        sigs[wid] = freq_sig(text, lex, lang)
        trads[wid] = prov.get("tradition") or "unknown"
    east_set = {w for w, t in trads.items() if t in EAST_TRADS}
    print(f"Signatures: {len(sigs)}, EAST: {len(east_set)}")

    # R² complet
    edges_w = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
               for e in edges]
    base = compute_strata(node_ids, edges_w, sigs, east_set)
    print("\n=== Baseline R² (graph v9 complet) ===")
    for k, (r, n) in base.items():
        print(f"  {k:<6}: {r:.4f}  n={n}")

    # LOO par arête
    deltas = []
    for i, e in enumerate(edges):
        edges_w_loo = [edges_w[j] for j in range(len(edges_w)) if j != i]
        r = compute_strata(node_ids, edges_w_loo, sigs, east_set)
        delta = {k: r[k][0] - base[k][0] for k in base}
        deltas.append({
            "src": e["src"],
            "tgt": e["tgt"],
            "channel": e.get("channel", "")[:50],
            "category": classify(e.get("channel", "")),
            "delta": delta,
        })
        if (i + 1) % 30 == 0:
            print(f"  ... {i+1}/{len(edges)}")

    print(f"  done {len(edges)}/{len(edges)}")

    # Top 10 arêtes les plus IMPACTANTES (Δ négatif = retirer baisse R²)
    print("\n=== TOP 15 arêtes les plus PORTEUSES sur GLOBAL "
          "(Δ négatif = leur retrait baisse R²) ===")
    sorted_global = sorted(deltas, key=lambda d: d["delta"]["GLOBAL"])
    for d in sorted_global[:15]:
        print(f"  Δ={d['delta']['GLOBAL']:>+7.4f} [{d['category']:<11}] "
              f"{d['src']:<35s} → {d['tgt']:<35s}")

    print("\n=== TOP 10 arêtes les plus NUISIBLES sur GLOBAL "
          "(Δ positif = leur retrait augmente R²) ===")
    for d in sorted_global[-10:][::-1]:
        print(f"  Δ={d['delta']['GLOBAL']:>+7.4f} [{d['category']:<11}] "
              f"{d['src']:<35s} → {d['tgt']:<35s}")

    # Stats par catégorie
    print("\n=== Δ moyen par catégorie d'arête ===")
    by_cat = {"direct": [], "translation": [], "indirect": []}
    for d in deltas:
        if d["category"] in by_cat:
            by_cat[d["category"]].append(d["delta"]["GLOBAL"])
    for cat, vals in by_cat.items():
        if vals:
            m = sum(vals) / len(vals)
            print(f"  {cat:<12}: μΔ={m:+.5f}  n={len(vals)}  "
                  f"min={min(vals):+.4f}  max={max(vals):+.4f}")

    # Stats sur les 9 arêtes documentées v189
    v189_deltas = [d for d in deltas
                   if any(d["src"] == e["src"] and d["tgt"] == e["tgt"]
                          for e in edges if e.get("added_in") == "v189")]
    print(f"\n=== Δ moyen sur les 9 arêtes documentées §189 ===")
    if v189_deltas:
        for k in ("GLOBAL", "WEST", "INTER", "NW"):
            vals = [d["delta"][k] for d in v189_deltas]
            m = sum(vals) / len(vals)
            print(f"  {k:<6}: μΔ={m:+.5f}  min={min(vals):+.4f}  max={max(vals):+.4f}")

    out = {
        "version": "0.3.2",
        "iteration": "v197_loo_per_edge",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "calibration": W_OPT,
        "baseline_R2": {k: round(v[0], 4) for k, v in base.items()},
        "n_edges": len(edges),
        "deltas_all": [
            {**d, "delta": {k: round(v, 5) for k, v in d["delta"].items()}}
            for d in deltas
        ],
        "top_15_porteuses_GLOBAL": [
            {"src": d["src"], "tgt": d["tgt"], "category": d["category"],
             "channel": d["channel"],
             "delta_GLOBAL": round(d["delta"]["GLOBAL"], 5)}
            for d in sorted_global[:15]
        ],
        "top_10_nuisibles_GLOBAL": [
            {"src": d["src"], "tgt": d["tgt"], "category": d["category"],
             "channel": d["channel"],
             "delta_GLOBAL": round(d["delta"]["GLOBAL"], 5)}
            for d in sorted_global[-10:][::-1]
        ],
        "by_category": {
            cat: {
                "n": len(vals),
                "mean": round(sum(vals) / len(vals), 5) if vals else 0,
                "min": round(min(vals), 4) if vals else 0,
                "max": round(max(vals), 4) if vals else 0,
            }
            for cat, vals in by_cat.items()
        },
    }
    p = RES / "nipada_v197_loo_per_edge.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

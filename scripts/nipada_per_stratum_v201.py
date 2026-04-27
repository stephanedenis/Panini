#!/usr/bin/env python3
"""§201 — Per-stratum recalibration.

V_OPT (0.45/0.15/0.01) optimise un composite GLOBAL+WEST. La stratégie
NW (East-East, n=55) reste à 0.0575 — possiblement parce que les
transmissions Est-Est sont majoritairement *indirectes* (transmission
silencieuse, milieux contemplatifs, traditions orales) plutôt que des
filiations directes documentées.

Méthode : sur graph v9 (180 arêtes), grid 2D fine sur (w_direct, w_indirect)
en maintenant w_translation=0.15 ; choisir le maximum R²_NW au lieu d'un
composite. Comparer avec V_OPT global.

Hypothèse : argmax NW déplacera w_indirect plus haut (≥0.05) au détriment
de WEST.
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


def compute_strata(node_ids, edges, sigs, east_set, w_d, w_t, w_i):
    weights = {"direct": w_d, "translation": w_t, "indirect": w_i}
    edges_w = [(e["src"], e["tgt"], weights[classify(e.get("channel", ""))])
               for e in edges]
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
            out[label] = 0.0
            continue
        xs = [p[2] for p in sub]
        ys = [p[3] for p in sub]
        out[label] = pearson(xs, ys) ** 2
    return out


def main():
    print("=== §201 — Per-stratum recalibration ===\n")
    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]

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

    # Grid 3D
    grid_d = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
    grid_t = [0.001, 0.01, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
    grid_i = [0.0001, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
    print(f"Grid 3D : w_d × w_t × w_i = "
          f"{len(grid_d)}×{len(grid_t)}×{len(grid_i)} = "
          f"{len(grid_d)*len(grid_t)*len(grid_i)} points\n")

    results = []
    for wd in grid_d:
        for wt in grid_t:
            for wi in grid_i:
                r = compute_strata(node_ids, edges, sigs, east_set, wd, wt, wi)
                results.append({"w_d": wd, "w_t": wt, "w_i": wi, "R2": r})

    # argmax par stratum
    print("=== argmax par stratum ===")
    bests = {}
    for stratum in ("GLOBAL", "WEST", "INTER", "NW"):
        best = max(results, key=lambda r: r["R2"][stratum])
        bests[stratum] = best
        print(f"  {stratum:<6}: w_d={best['w_d']:.2f}  w_t={best['w_t']:<6}"
              f"  w_i={best['w_i']:<7}"
              f"  R²={best['R2'][stratum]:.4f}  "
              f"(GLOBAL={best['R2']['GLOBAL']:.3f} WEST={best['R2']['WEST']:.3f} "
              f"INTER={best['R2']['INTER']:.3f} NW={best['R2']['NW']:.3f})")

    # Référence V_OPT
    r_vopt = compute_strata(node_ids, edges, sigs, east_set, 0.45, 0.15, 0.01)
    print(f"\n=== V_OPT référence (0.45/0.15/0.01) ===")
    for k, v in r_vopt.items():
        print(f"  {k:<6}: R²={v:.4f}")

    # Sauvegarde
    out = {
        "version": "0.3.3",
        "iteration": "v201_per_stratum_recalibration",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "grid": {"w_direct": grid_d, "w_translation": grid_t,
                 "w_indirect": grid_i},
        "v_opt_reference": {"params": [0.45, 0.15, 0.01],
                            "R2": {k: round(v, 4) for k, v in r_vopt.items()}},
        "argmax_per_stratum": {
            k: {"w_d": v["w_d"], "w_t": v["w_t"], "w_i": v["w_i"],
                "R2": {kk: round(vv, 4) for kk, vv in v["R2"].items()}}
            for k, v in bests.items()
        },
        "all_results": [
            {"w_d": r["w_d"], "w_t": r["w_t"], "w_i": r["w_i"],
             "R2": {k: round(v, 4) for k, v in r["R2"].items()}}
            for r in results
        ],
    }
    p = RES / "nipada_v201_per_stratum.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

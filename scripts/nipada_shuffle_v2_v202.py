#!/usr/bin/env python3
"""§202 — Validation V_OPT v2 par channel-shuffle.

V_OPT v2 = (0.80 / 0.50 / 0.0001) découverte §201 domine V_OPT (0.45/
0.15/0.01) sur tous les strata. Mais cette domination est-elle due à la
*classification* documentaire des canaux, ou simplement à l'écart
direct/indirect plus extrême (×8000 vs ×45) qui rend la topologie plus
sensible aux raccourcis ?

Méthode : 500 shuffles aléatoires des channels (préservant la structure
topologique). Si V_OPT v2 R² ne dépend que de l'écart de poids, le
shuffle ne devrait pas casser le signal autant qu'il l'a cassé pour V_OPT
en §193 (NW p=0.013).

Si shuffle casse encore le signal → V_OPT v2 capture davantage la
classification. Si shuffle ne le casse plus → V_OPT v2 surexploite la
structure et est moins fiable que V_OPT.
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
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
W_V2 = {"direct": 0.80, "translation": 0.50, "indirect": 0.0001}
W_V1 = {"direct": 0.45, "translation": 0.15, "indirect": 0.01}
N_SHUFFLE = 500
SEED = 20260427


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
            out[label] = 0.0
            continue
        xs = [p[2] for p in sub]
        ys = [p[3] for p in sub]
        out[label] = pearson(xs, ys) ** 2
    return out


def shuffle_test(node_ids, edges, sigs, east_set, weights, n_shuffle, seed):
    rnd = random.Random(seed)
    cats = [classify(e.get("channel", "")) for e in edges]
    base_w = [(e["src"], e["tgt"], weights[c]) for e, c in zip(edges, cats)]
    base_R2 = compute_strata(node_ids, base_w, sigs, east_set)
    print(f"  baseline : {base_R2}")

    shuffled = {k: [] for k in ("GLOBAL", "WEST", "INTER", "NW")}
    for it in range(n_shuffle):
        rnd.shuffle(cats)
        ew = [(e["src"], e["tgt"], weights[c]) for e, c in zip(edges, cats)]
        r = compute_strata(node_ids, ew, sigs, east_set)
        for k in shuffled:
            shuffled[k].append(r[k])
        if (it + 1) % 100 == 0:
            print(f"    shuffle {it+1}/{n_shuffle}")

    # p-value : fraction shuffles ≥ baseline
    pvals = {}
    means = {}
    for k in shuffled:
        vals = shuffled[k]
        n_ge = sum(1 for v in vals if v >= base_R2[k])
        pvals[k] = (n_ge + 1) / (n_shuffle + 1)
        means[k] = sum(vals) / len(vals)
    return base_R2, means, pvals


def main():
    print("=== §202 — Validation V_OPT v2 par channel-shuffle ===\n")
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

    print(f"\n--- V_OPT v1 ({W_V1}) ---")
    b1, m1, p1 = shuffle_test(node_ids, edges, sigs, east_set, W_V1,
                               N_SHUFFLE, SEED)
    print(f"\n--- V_OPT v2 ({W_V2}) ---")
    b2, m2, p2 = shuffle_test(node_ids, edges, sigs, east_set, W_V2,
                               N_SHUFFLE, SEED + 1)

    print("\n=== Récapitulatif p-values ===")
    print(f"{'stratum':<8} {'baseline_v1':>11} {'p_v1':>7} "
          f"{'baseline_v2':>11} {'p_v2':>7}")
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        print(f"{k:<8} {b1[k]:>11.4f} {p1[k]:>7.4f} "
              f"{b2[k]:>11.4f} {p2[k]:>7.4f}")

    out = {
        "version": "0.3.3",
        "iteration": "v202_shuffle_validation_vopt_v2",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_shuffle": N_SHUFFLE,
        "seed": SEED,
        "v_opt_v1": {
            "params": W_V1,
            "baseline": {k: round(v, 4) for k, v in b1.items()},
            "shuffle_mean": {k: round(v, 4) for k, v in m1.items()},
            "p_value": {k: round(v, 4) for k, v in p1.items()},
        },
        "v_opt_v2": {
            "params": W_V2,
            "baseline": {k: round(v, 4) for k, v in b2.items()},
            "shuffle_mean": {k: round(v, 4) for k, v in m2.items()},
            "p_value": {k: round(v, 4) for k, v in p2.items()},
        },
    }
    p = RES / "nipada_v202_shuffle_v2.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

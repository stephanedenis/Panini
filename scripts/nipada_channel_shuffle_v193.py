#!/usr/bin/env python3
"""§193 — Test H1 channel-shuffle.

Question : V_OPT (w_dir=0.45, w_trn=0.15, w_ind=0.01) attribue des poids
très différents selon le type de canal (direct/translation/indirect). Si
ces différences exploitent vraiment l'information sémantique du canal,
alors permuter aléatoirement les channels de toutes les arêtes (sans
toucher la structure topologique) doit casser le R².

Si R² reste stable malgré le shuffle → V_OPT n'exploite que la structure
du graphe, pas la classification des canaux. Le signal NIPADA serait alors
un effet de connectivité, pas de contenu.

Si R² chute significativement → la classification (direct/translation/
indirect) porte une information mesurable.

Méthode : 1000 shuffles. Pour chacun, mélange aléatoire des channels parmi
les arêtes du graphe v9. Recalcul R² stratifié.

Calibration V_OPT.
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


def compute_r2(node_ids, edges_w, sigs, east_set):
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
    print("=== §193 — Test H1 channel-shuffle (V_OPT, graph v9) ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]
    print(f"Graph v9: {len(nodes)} nodes, {len(edges)} edges")

    # Compter channels par catégorie
    cats = [classify(e.get("channel", "")) for e in edges]
    from collections import Counter
    cnt = Counter(cats)
    print(f"Channels: {dict(cnt)}")

    # Signatures
    lex = load_lex()
    sigs = {}
    trads = {}
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
    print(f"Signatures: {len(sigs)}")

    east_set = {w for w, t in trads.items() if t in EAST_TRADS}

    # OBSERVATION
    edges_w_obs = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                   for e in edges]
    obs = compute_r2(node_ids, edges_w_obs, sigs, east_set)
    print("\n=== Observation (V_OPT graph v9) ===")
    for k, (r2, n) in obs.items():
        print(f"  {k:<6}: R²={r2:.4f}  n={n}")

    # SHUFFLE: shuffler les catégories entre arêtes
    n_iter = 1000
    rnd = random.Random(2026)
    shuffle_results = {"GLOBAL": [], "WEST": [], "INTER": [], "NW": []}
    print(f"\n=== Channel-shuffle n={n_iter} ===")
    for it in range(n_iter):
        cats_shuf = list(cats)
        rnd.shuffle(cats_shuf)
        edges_w_sh = [
            (edges[i]["src"], edges[i]["tgt"], W_OPT[cats_shuf[i]])
            for i in range(len(edges))
        ]
        r = compute_r2(node_ids, edges_w_sh, sigs, east_set)
        for k in shuffle_results:
            shuffle_results[k].append(r[k][0])
        if (it + 1) % 200 == 0:
            print(f"  ... {it+1}/{n_iter}")

    # CONTRÔLE EXTRÊME : tous w=0.45 (uniforme)
    edges_w_uni = [(e["src"], e["tgt"], 0.45) for e in edges]
    uni = compute_r2(node_ids, edges_w_uni, sigs, east_set)

    # CONTRÔLE EXTRÊME : tous w=0.01 (uniforme bas)
    edges_w_low = [(e["src"], e["tgt"], 0.01) for e in edges]
    low = compute_r2(node_ids, edges_w_low, sigs, east_set)

    print("\n=== Comparaison observé vs shuffle vs uniformes ===")
    print(f"{'Strate':<8}{'obs R²':>10}{'shuf μ':>10}{'shuf σ':>10}"
          f"{'p (obs ≥)':>12}{'unif=0.45':>11}{'unif=0.01':>11}")
    res = {}
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        obs_r2 = obs[k][0]
        vals = shuffle_results[k]
        m = sum(vals) / len(vals)
        v = sum((x - m) ** 2 for x in vals) / len(vals)
        s = math.sqrt(v)
        ge = sum(1 for x in vals if x >= obs_r2)
        p = (ge + 1) / (n_iter + 1)
        print(f"{k:<8}{obs_r2:>10.4f}{m:>10.4f}{s:>10.4f}{p:>12.4f}"
              f"{uni[k][0]:>11.4f}{low[k][0]:>11.4f}")
        res[k] = {
            "observed_R2": round(obs_r2, 4),
            "shuffle_mean": round(m, 4),
            "shuffle_std": round(s, 4),
            "p_obs_ge_shuffle": round(p, 4),
            "uniform_045_R2": round(uni[k][0], 4),
            "uniform_001_R2": round(low[k][0], 4),
        }

    print("\n=== DIAGNOSTIC ===")
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        r = res[k]
        diff = r["observed_R2"] - r["shuffle_mean"]
        if r["p_obs_ge_shuffle"] < 0.05:
            verdict = (
                f"✓ CLASSIFICATION CHANNELS PORTE INFO — V_OPT > shuffle "
                f"(p={r['p_obs_ge_shuffle']:.4f}, +{diff:.4f})"
            )
        elif r["p_obs_ge_shuffle"] > 0.95:
            verdict = (
                f"✗ ANTI-info — shuffle bat V_OPT (p={r['p_obs_ge_shuffle']:.4f})"
            )
        else:
            verdict = (
                f"= V_OPT n'exploite pas la classification (p={r['p_obs_ge_shuffle']:.4f}, Δ={diff:+.4f})"
            )
        print(f"  {k:<6} : {verdict}")

    out = {
        "version": "0.3.0",
        "iteration": "v193_channel_shuffle",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "n_iter": n_iter,
        "calibration": W_OPT,
        "channels_distribution": dict(cnt),
        "results": res,
    }
    p = RES / "nipada_v193_channel_shuffle.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

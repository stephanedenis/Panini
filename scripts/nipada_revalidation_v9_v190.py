#!/usr/bin/env python3
"""§190 — Revalidation NIPADA sur graph v9 avec calibration V_OPT.

Mesure l'effet des 9 arêtes East-East ajoutées par §189 sur les R²
stratifiés. Hypothèse : NW×NW devrait passer de R²=0.005 vers une valeur
significative si la transmission est documentaire.

Utilise V_OPT (0.45/0.15/0.01) et permutation test n=2000 stratifié.
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


def classify(ch: str) -> str:
    s = ch.lower()
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


def floyd(node_ids, edges):
    idx = {n: i for i, n in enumerate(node_ids)}
    N = len(node_ids)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0.0
    for s, t, w in edges:
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
    mx, my = sum(xs) / n, sum(ys) / n
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


def perm_test(pairs, n_iter=2000, seed=2026):
    xs = [p[2] for p in pairs]
    ys = [p[3] for p in pairs]
    obs_r2 = pearson(xs, ys) ** 2
    rnd = random.Random(seed)
    ge = 0
    for _ in range(n_iter):
        ys2 = ys[:]
        rnd.shuffle(ys2)
        if pearson(xs, ys2) ** 2 >= obs_r2:
            ge += 1
    return obs_r2, (ge + 1) / (n_iter + 1)


def main():
    print("=== §190 — Revalidation graph v9 (V_OPT) ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    edges_raw = g9["edges"]

    edges_w = []
    for e in edges_raw:
        cat = classify(e.get("channel", ""))
        edges_w.append((e["src"], e["tgt"], W_OPT[cat]))

    node_ids = list(nodes.keys())
    print(f"Graph v9: {len(nodes)} nodes, {len(edges_raw)} edges")

    lex = load_lex()
    sigs, trads = {}, {}
    for d in sorted(CORPUS.iterdir()):
        if not d.is_dir():
            continue
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
    print(f"Pairs connectées: {len(pairs)}\n")

    nw_ids = {w for w, t in trads.items() if t in EAST_TRADS}
    print(f"Œuvres EAST signées: {len(nw_ids)}")
    print(f"  {sorted(nw_ids)}\n")

    west = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
    inter = [p for p in pairs if (p[0] in nw_ids) != (p[1] in nw_ids)]
    nw = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]

    results = {}
    for label, sub in [("GLOBAL", pairs), ("WEST", west),
                       ("INTER", inter), ("NW", nw)]:
        if len(sub) < 3:
            print(f"  {label:<6}: n={len(sub)} (insuffisant)")
            results[label] = {"n": len(sub), "R2": None, "p": None}
            continue
        r2, p = perm_test(sub, n_iter=2000)
        print(f"  {label:<6}: R²={r2:.4f}  n={len(sub)}  p_perm={p:.4f}")
        results[label] = {"n": len(sub), "R2": round(r2, 4), "p": round(p, 4)}

    # Comparaison avec graph v8
    print("\n=== Comparaison v8 → v9 ===")
    v8_ref = {  # depuis §188
        "GLOBAL": (0.0474, 378),
        "WEST":   (0.0890, 136),
        "INTER":  (0.0290, 187),
        "NW":     (0.0050,  55),
    }
    print(f"{'Strate':<8}{'v8 R²':>10}{'v9 R²':>10}{'Δ R²':>10}"
          f"{'v8 n':>8}{'v9 n':>8}")
    for label in ("GLOBAL", "WEST", "INTER", "NW"):
        r8, n8 = v8_ref[label]
        r = results[label]
        if r["R2"] is None:
            continue
        delta = r["R2"] - r8
        print(f"{label:<8}{r8:>10.4f}{r['R2']:>10.4f}{delta:>+10.4f}"
              f"{n8:>8}{r['n']:>8}")

    out = {
        "version": "0.2.7",
        "iteration": "v190_revalidation_v9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "calibration": W_OPT,
        "n_signatures": len(sigs),
        "n_pairs": len(pairs),
        "n_east_signed": len(nw_ids),
        "east_signed_ids": sorted(nw_ids),
        "results": results,
        "comparison_v8": {k: {"R2": v[0], "n": v[1]} for k, v in v8_ref.items()},
    }
    p = RES / "nipada_v190_revalidation_v9.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

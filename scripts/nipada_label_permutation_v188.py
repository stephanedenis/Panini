#!/usr/bin/env python3
"""§188 — Permutation des labels de tradition (test confondant).

Test rigoureux : si le signal NIPADA est causé par l'appartenance
co-traditionnelle (œuvres de même école se ressemblent ⇒ d_lex faible
indépendamment du graphe), alors permuter les labels de tradition entre
les œuvres devrait :
  - Détruire la structure stratifiée (WEST×WEST, INTER, NW×NW deviennent
    aléatoires)
  - Conserver le R² global (les arêtes du graphe restent)

À l'inverse, si le signal vient de la transmission documentaire :
  - Stratification reste cohérente (WEST×WEST conserve R² élevé)
  - Permutation casse la structure stratifiée mais pas le signal global

Pipeline : V_OPT (w_dir=0.45, w_trn=0.15, w_ind=0.01) sur graph v8,
permutation labels 1000 fois, mesure R² par strate.
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

W_OPT = {"direct": 0.45, "translation": 0.15, "indirect": 0.01}


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


def stratified_r2(pairs, trads_map, east_set):
    nw_ids = {w for w, t in trads_map.items() if t in east_set}
    west = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
    inter = [p for p in pairs if (p[0] in nw_ids) != (p[1] in nw_ids)]
    nw = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]

    def r2(pp):
        if len(pp) < 3:
            return 0.0, len(pp)
        xs = [p[2] for p in pp]
        ys = [p[3] for p in pp]
        return pearson(xs, ys) ** 2, len(pp)

    return {
        "west": r2(west),
        "inter": r2(inter),
        "nw": r2(nw),
    }


def main():
    print("=== §188 — Permutation labels traditions (V_OPT) ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]

    edges_w = []
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        cat = classify_channel(e.get("channel", ""))
        edges_w.append((s, t, W_OPT[cat]))

    node_ids = list(nodes.keys())
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges")
    print(f"V_OPT: {W_OPT}")

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

    # Construire pairs (une fois)
    D, idx = floyd_warshall(node_ids, edges_w)
    work_ids = sorted(w for w in sigs if w in idx)
    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            d_lex = 1.0 - cosine_dict(sigs[a], sigs[b])
            pairs.append((a, b, d_g, d_lex))
    print(f"Signatures: {len(sigs)}, Pairs connectées: {len(pairs)}")

    # Observation
    obs = stratified_r2(pairs, trads, EAST_TRADS)
    print("\n=== Observation (vrais labels) ===")
    for k, (r2, n) in obs.items():
        print(f"  {k:<6}: R²={r2:.4f}  n={n}")

    # GLOBAL
    xs = [p[2] for p in pairs]
    ys = [p[3] for p in pairs]
    r2_glob = pearson(xs, ys) ** 2
    print(f"  GLOBAL: R²={r2_glob:.4f}  n={len(pairs)}")

    # Permutation labels: shuffle labels parmi les œuvres signées
    n_iter = 1000
    rnd = random.Random(2026)
    work_list = list(trads.keys())
    label_list = list(trads.values())

    print(f"\n=== Permutation labels (n={n_iter}) ===")
    perm_results = {"west": [], "inter": [], "nw": []}
    perm_global = []  # devrait rester constant (labels n'affectent pas global)

    for it in range(n_iter):
        rnd.shuffle(label_list)
        perm_trads = dict(zip(work_list, label_list))
        strat = stratified_r2(pairs, perm_trads, EAST_TRADS)
        for k in ("west", "inter", "nw"):
            perm_results[k].append(strat[k][0])
        # global n'est pas affecté par labels (mêmes pairs)

    print(f"{'Strate':<8}{'obs R²':>10}{'perm μ':>10}{'perm σ':>10}"
          f"{'p (obs ≥ perm)':>16}{'percentile':>12}")

    out_perm = {}
    for k in ("west", "inter", "nw"):
        obs_r2 = obs[k][0]
        perm_vals = perm_results[k]
        m = sum(perm_vals) / len(perm_vals)
        v = sum((x - m) ** 2 for x in perm_vals) / len(perm_vals)
        s = math.sqrt(v)
        p = (sum(1 for x in perm_vals if x >= obs_r2) + 1) / (n_iter + 1)
        # Percentile observé dans la distribution
        sorted_p = sorted(perm_vals)
        pct = sum(1 for x in sorted_p if x <= obs_r2) / len(sorted_p) * 100
        print(f"{k:<8}{obs_r2:>10.4f}{m:>10.4f}{s:>10.4f}"
              f"{p:>16.4f}{pct:>11.1f}%")
        out_perm[k] = {
            "observed_R2": round(obs_r2, 4),
            "perm_mean": round(m, 4),
            "perm_std": round(s, 4),
            "p_value": round(p, 4),
            "percentile": round(pct, 1),
            "n_pairs_observed": obs[k][1],
        }

    # Diagnostic
    print("\n=== DIAGNOSTIC ===")
    for k in ("west", "inter", "nw"):
        r = out_perm[k]
        if r["p_value"] < 0.05:
            verdict = (
                f"✓ STRATIFICATION SIGNIFICATIVE — observé > 95% des "
                f"permutations (p={r['p_value']:.4f})"
            )
        elif r["p_value"] > 0.95:
            verdict = (
                f"✗ ANTI-stratification — observé < 5% des permutations"
                f" (signal opposé attendu, p={r['p_value']:.4f})"
            )
        else:
            verdict = (
                f"= aléatoire — observé n'est pas distinguable des "
                f"permutations (p={r['p_value']:.4f})"
            )
        print(f"  {k.upper():<6} : {verdict}")

    out = {
        "version": "0.2.7",
        "iteration": "v188_label_permutation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v182_graph_v8.json",
        "calibration": W_OPT,
        "n_signatures": len(sigs),
        "n_pairs_connected": len(pairs),
        "global_R2": round(r2_glob, 4),
        "observed_strata": {k: {"R2": round(v[0], 4), "n": v[1]}
                            for k, v in obs.items()},
        "permutation_n_iter": n_iter,
        "permutation_results": out_perm,
    }
    out_p = RES_DIR / "nipada_v188_label_permutation.json"
    out_p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

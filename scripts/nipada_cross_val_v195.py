#!/usr/bin/env python3
"""§195 — H5 Cross-validation 5-fold stratifiée par tradition.

Test de robustesse statistique indépendant de la permutation : partitionne
les œuvres en 5 plis stratifiés par tradition (préserve proportions
EAST/WEST), entraîne sur 4 plis (calcule la régression d_lex ~ d_g),
prédit sur le pli sortant.

Métrique : R² out-of-fold (OOF), différent du R² in-sample. Si R² OOF reste
significatif, le signal généralise hors corpus d'entraînement.

Calibration V_OPT, graph v9.
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


def linreg(xs, ys):
    """Fit y = a + b*x. Return (a, b)."""
    n = len(xs)
    if n < 2:
        return 0.0, 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((x - mx) ** 2 for x in xs)
    b = num / den if den else 0.0
    a = my - b * mx
    return a, b


def r2_oof(test_xs, test_ys, a, b):
    """R² out-of-fold avec modèle (a,b) entraîné ailleurs."""
    if len(test_xs) < 2:
        return 0.0
    preds = [a + b * x for x in test_xs]
    my = sum(test_ys) / len(test_ys)
    ss_res = sum((test_ys[i] - preds[i]) ** 2 for i in range(len(test_ys)))
    ss_tot = sum((y - my) ** 2 for y in test_ys)
    if ss_tot < 1e-12:
        return 0.0
    return 1.0 - ss_res / ss_tot


def stratified_kfold(works_with_trad, k=5, seed=2026):
    """Partitionne en k plis stratifiés par tradition."""
    rnd = random.Random(seed)
    by_trad = {}
    for w, t in works_with_trad:
        by_trad.setdefault(t, []).append(w)
    folds = [[] for _ in range(k)]
    for trad, ws in by_trad.items():
        ws_shuf = ws[:]
        rnd.shuffle(ws_shuf)
        for i, w in enumerate(ws_shuf):
            folds[i % k].append(w)
    return folds


def main():
    print("=== §195 — H5 Cross-validation 5-fold (V_OPT graph v9) ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]

    edges_w = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
               for e in edges]
    print(f"Graph v9: {len(nodes)} nodes, {len(edges)} edges")

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

    # Construire toutes les paires
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
    print(f"Pairs connectées: {len(pairs)}")

    # Stratification par tradition (regrouper EAST hétérogènes en 'east')
    works_with_trad = []
    for w in work_ids:
        t = trads[w]
        meta_t = "east" if t in EAST_TRADS else (
            "west" if t != "unknown" else "west")
        works_with_trad.append((w, meta_t))

    east_n = sum(1 for _, t in works_with_trad if t == "east")
    west_n = sum(1 for _, t in works_with_trad if t == "west")
    print(f"Stratification: east={east_n}, west={west_n}")

    # 5-fold
    K = 5
    N_REPEATS = 20
    print(f"\n=== {N_REPEATS} répétitions × {K}-fold stratifié ===")

    east_set = {w for w, t in works_with_trad if t == "east"}

    rep_results = {"GLOBAL": [], "WEST": [], "INTER": [], "NW": []}

    for rep in range(N_REPEATS):
        folds = stratified_kfold(works_with_trad, k=K, seed=2026 + rep)
        # OOF predictions
        oof = {}  # pair_key -> (true, pred)
        for fold_idx in range(K):
            test_works = set(folds[fold_idx])
            train_works = set()
            for fi in range(K):
                if fi != fold_idx:
                    train_works.update(folds[fi])
            train_pairs = [p for p in pairs
                           if p[0] in train_works and p[1] in train_works]
            if len(train_pairs) < 5:
                continue
            xs_tr = [p[2] for p in train_pairs]
            ys_tr = [p[3] for p in train_pairs]
            a, b = linreg(xs_tr, ys_tr)
            # Test pairs : au moins une œuvre dans test_works
            test_pairs = [p for p in pairs
                          if (p[0] in test_works) or (p[1] in test_works)]
            for p in test_pairs:
                pred = a + b * p[2]
                key = (p[0], p[1])
                if key not in oof:
                    oof[key] = (p[3], pred, p[0], p[1])

        # Calculer R² OOF par strate
        all_pairs = list(oof.values())
        west_pairs = [v for v in all_pairs
                      if v[2] not in east_set and v[3] not in east_set]
        inter_pairs = [v for v in all_pairs
                       if (v[2] in east_set) != (v[3] in east_set)]
        nw_pairs = [v for v in all_pairs
                    if v[2] in east_set and v[3] in east_set]

        for label, sub in [("GLOBAL", all_pairs), ("WEST", west_pairs),
                           ("INTER", inter_pairs), ("NW", nw_pairs)]:
            if len(sub) < 3:
                continue
            ys_true = [v[0] for v in sub]
            ys_pred = [v[1] for v in sub]
            my = sum(ys_true) / len(ys_true)
            ss_res = sum((ys_true[i] - ys_pred[i]) ** 2
                         for i in range(len(ys_true)))
            ss_tot = sum((y - my) ** 2 for y in ys_true)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
            rep_results[label].append(r2)

    print(f"\n{'Strate':<8}{'R² OOF μ':>12}{'R² OOF σ':>12}"
          f"{'min':>10}{'max':>10}{'CI95':>20}")
    print("-" * 75)
    res = {}
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        vals = rep_results[k]
        if not vals:
            print(f"{k:<8}  (insuffisant)")
            res[k] = None
            continue
        m = sum(vals) / len(vals)
        v = sum((x - m) ** 2 for x in vals) / len(vals)
        s = math.sqrt(v)
        sv = sorted(vals)
        lo = sv[int(len(sv) * 0.025)]
        hi = sv[int(len(sv) * 0.975)] if len(sv) > 1 else sv[0]
        print(f"{k:<8}{m:>12.4f}{s:>12.4f}{min(vals):>10.4f}{max(vals):>10.4f}"
              f"  [{lo:.4f},{hi:.4f}]")
        res[k] = {
            "R2_OOF_mean": round(m, 4),
            "R2_OOF_std": round(s, 4),
            "R2_OOF_min": round(min(vals), 4),
            "R2_OOF_max": round(max(vals), 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "n_repeats": len(vals),
        }

    # Comparaison rappel R² in-sample
    print("\n=== Comparaison R² in-sample (§190) vs R² OOF (§195) ===")
    in_sample = {"GLOBAL": 0.0984, "WEST": 0.0890, "INTER": 0.0782, "NW": 0.0575}
    print(f"{'Strate':<8}{'in-sample':>12}{'OOF μ':>12}{'gap':>10}")
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        if res.get(k):
            gap = in_sample[k] - res[k]["R2_OOF_mean"]
            print(f"{k:<8}{in_sample[k]:>12.4f}"
                  f"{res[k]['R2_OOF_mean']:>12.4f}{gap:>+10.4f}")

    out = {
        "version": "0.3.2",
        "iteration": "v195_cross_validation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "calibration": W_OPT,
        "k_folds": K,
        "n_repeats": N_REPEATS,
        "n_signatures": len(sigs),
        "n_pairs_connected": len(pairs),
        "stratification": {"east": east_n, "west": west_n},
        "results": res,
        "in_sample_reference": in_sample,
    }
    p = RES / "nipada_v195_cross_validation.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

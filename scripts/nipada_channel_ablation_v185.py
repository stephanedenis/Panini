#!/usr/bin/env python3
"""§185 — Ablation par canal : test de la conjecture §184.

§184 a montré:
  - Acycliser détruit le signal (chute 94% global)
  - MSF_max (arêtes fortes w=0.45) PIRE que random
  - MSF_min (arêtes indirectes w=0.30) booste INTER ×2.5

Hypothèse §184 raffinée: le signal NIPADA est porté par la combinatoire
des chemins indirects multi-saut redondants, PAS par les arêtes
individuellement fortes.

Test §185: ablation directe par canal. On supprime sélectivement chaque
type d'arête et on mesure l'effet:
  - SANS direct       : seul indirect + translation restent
  - SANS translation  : seul direct + indirect restent
  - SANS indirect     : seul direct + translation restent
  - SEUL direct       : ablation des deux autres (control)
  - SEUL indirect     : ablation des deux autres (test crucial)
  - SEUL translation  : ablation des deux autres

Prédictions §184 :
  - SANS indirect → R² INTER s'effondre   (les indirects sont les ponts longs)
  - SEUL indirect → R² INTER reste élevé  (suffisant pour la transmission)
  - SANS direct   → R² INTER inchangé     (les directs sont locaux)
  - SEUL direct   → R² INTER faible       (locaux uniquement, pas de transmission)
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


def main():
    print("=== §185 — Ablation par canal ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges")

    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    edges_typed = []
    counts = {"direct": 0, "translation": 0, "indirect": 0}
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        cat = classify_channel(e.get("channel", ""))
        edges_typed.append((s, t, weight_map[cat], cat))
        counts[cat] += 1

    print(f"  direct      : {counts['direct']:>3}")
    print(f"  translation : {counts['translation']:>3}")
    print(f"  indirect    : {counts['indirect']:>3}")

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

    def evaluate(label, kept_categories):
        edges_used = [(s, t, w) for s, t, w, c in edges_typed
                      if c in kept_categories]
        D, idx = floyd_warshall(node_ids, edges_used)
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

        xs = [p[2] for p in pairs]
        ys = [p[3] for p in pairs]
        r = pearson(xs, ys)
        pv = perm_test(xs, ys)

        nw_ids = {w for w, t in trads.items() if t in EAST_TRADS}
        west_pairs = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
        inter_pairs = [p for p in pairs
                       if (p[0] in nw_ids) != (p[1] in nw_ids)]
        nw_pairs = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]

        def stat(pp):
            if len(pp) < 3:
                return {"n": len(pp), "R2": 0.0, "p": 1.0}
            xs = [x[2] for x in pp]
            ys = [x[3] for x in pp]
            rr = pearson(xs, ys)
            return {"n": len(pp), "R2": round(rr * rr, 4),
                    "p": round(perm_test(xs, ys), 4)}

        return {
            "label": label,
            "kept": sorted(kept_categories),
            "n_edges_used": len(edges_used),
            "n_pairs_connected": len(pairs),
            "global": {"n": len(pairs), "R2": round(r * r, 4),
                       "p": round(pv, 4)},
            "west_west": stat(west_pairs),
            "inter": stat(inter_pairs),
            "nw_nw": stat(nw_pairs),
        }

    scenarios = [
        ("ORIGINAL", {"direct", "translation", "indirect"}),
        ("SANS direct", {"translation", "indirect"}),
        ("SANS translation", {"direct", "indirect"}),
        ("SANS indirect", {"direct", "translation"}),
        ("SEUL direct", {"direct"}),
        ("SEUL translation", {"translation"}),
        ("SEUL indirect", {"indirect"}),
    ]

    print("\n=== Résultats ===")
    print(f"{'Scénario':<20}{'n_edges':>9}{'n_pairs':>9}"
          f"{'GLOBAL R²':>12}{'p':>8}{'WEST R²':>10}{'INTER R²':>10}{'NW R²':>9}")
    print("-" * 87)

    results = []
    for label, cats in scenarios:
        r = evaluate(label, cats)
        results.append(r)
        print(f"{label:<20}{r['n_edges_used']:>9}{r['n_pairs_connected']:>9}"
              f"{r['global']['R2']:>12.4f}{r['global']['p']:>8.3f}"
              f"{r['west_west']['R2']:>10.4f}{r['inter']['R2']:>10.4f}"
              f"{r['nw_nw']['R2']:>9.4f}")

    # Diagnostic
    orig = results[0]
    print("\n=== DIAGNOSTIC ===")
    print(f"  ORIGINAL    : GLOBAL R²={orig['global']['R2']:.4f}  "
          f"INTER R²={orig['inter']['R2']:.4f}")

    for r in results[1:]:
        delta_g = (orig["global"]["R2"] - r["global"]["R2"]) / max(orig["global"]["R2"], 1e-9)
        delta_i = (orig["inter"]["R2"] - r["inter"]["R2"]) / max(orig["inter"]["R2"], 1e-9)
        print(f"  {r['label']:<18} ΔGLOBAL={delta_g*100:+6.1f}%  "
              f"ΔINTER={delta_i*100:+6.1f}%")

    out = {
        "version": "0.2.5",
        "iteration": "v185_channel_ablation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v182_graph_v8.json",
        "edge_counts": counts,
        "weights": weight_map,
        "scenarios": results,
    }
    out_p = RES_DIR / "nipada_v185_channel_ablation.json"
    out_p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

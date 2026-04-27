#!/usr/bin/env python3
"""§199 — Author-only nodes cleanup → graph v10.

§197 LOO révèle que les arêtes œuvre→auteur (confucius_analects_en→confucius,
schopenhauer→buddha, dhammapada→buddha, voltaire→voltaire_candide…) sont
les plus NUISIBLES : elles dégradent R² parce que le nœud auteur n'a pas
de signature V14 (pas de corpus PROVENANCE) et agit comme un pivot court-
circuitant les distances.

Stratégies testées :
  v10a — REMOVE : retirer toutes arêtes incidentes à un nœud sans signature
  v10b — DOWNWEIGHT : pondérer ces arêtes à W_AUTHOR=0.001 (≃ indirect floor)

Pour chaque variante, recalcul R² stratifié avec V_OPT (0.45/0.15/0.01).

Hypothèse : v10a doit faire grimper GLOBAL R² au-delà du baseline 0.0984
en supprimant 4-5 arêtes nuisibles top-§197.
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
W_AUTHOR_FLOOR = 0.001  # v10b downweight


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
        out[label] = (round(pearson(xs, ys) ** 2, 4), len(sub))
    return out


def main():
    print("=== §199 — Author-only nodes cleanup → graph v10 ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]
    print(f"Graph v9: {len(nodes)} nœuds, {len(edges)} arêtes")

    # corpus signatures
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
    print(f"Signatures: {len(sigs)} œuvres, EAST: {len(east_set)}")

    # critère "auteur seul" : pas de signature V14 disponible
    AUTHOR_KINDS = {
        "pivot_author", "philosopher_proto", "religious_figure",
        "philosopher_modern", "translator",
    }
    author_only = set()
    for nid, ndata in nodes.items():
        if nid in sigs:
            continue
        kind = ndata.get("kind", "?")
        # candidat author-only : kind explicite OU absent du corpus signé
        if kind in AUTHOR_KINDS or nid not in sigs:
            author_only.add(nid)
    # ne jamais retirer un nœud avec signature
    author_only -= set(sigs.keys())
    print(f"Nœuds author-only (sans signature V14) : {len(author_only)}")
    print("  exemples :", sorted(author_only)[:10])

    # === Baseline v9 ===
    edges_w_v9 = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                  for e in edges]
    base = compute_strata(node_ids, edges_w_v9, sigs, east_set)
    print("\n=== Baseline v9 ===")
    for k, (r, n) in base.items():
        print(f"  {k:<6}: R²={r:.4f}  n={n}")

    # === v10a : REMOVE arêtes incidentes à author-only ===
    edges_v10a = [e for e in edges
                  if e["src"] not in author_only and e["tgt"] not in author_only]
    nodes_v10a = [n for n in node_ids if n not in author_only]
    edges_w_v10a = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                    for e in edges_v10a]
    print(f"\n=== v10a — REMOVE author-only ===")
    print(f"  nœuds : {len(nodes_v10a)} (−{len(author_only)})")
    print(f"  arêtes : {len(edges_v10a)} (−{len(edges) - len(edges_v10a)})")
    r10a = compute_strata(nodes_v10a, edges_w_v10a, sigs, east_set)
    for k, (r, n) in r10a.items():
        d = r - base[k][0]
        print(f"  {k:<6}: R²={r:.4f}  n={n}  Δ={d:+.4f}")

    # === v10b : DOWNWEIGHT W_AUTHOR_FLOOR sur arêtes incidentes à author-only ===
    def weight_v10b(e):
        cat = classify(e.get("channel", ""))
        w = W_OPT[cat]
        if e["src"] in author_only or e["tgt"] in author_only:
            return min(w, W_AUTHOR_FLOOR)
        return w
    edges_w_v10b = [(e["src"], e["tgt"], weight_v10b(e)) for e in edges]
    n_downweighted = sum(1 for e in edges
                         if e["src"] in author_only or e["tgt"] in author_only)
    print(f"\n=== v10b — DOWNWEIGHT (W_AUTHOR={W_AUTHOR_FLOOR}) ===")
    print(f"  arêtes : {len(edges)} ({n_downweighted} pondérées floor)")
    r10b = compute_strata(node_ids, edges_w_v10b, sigs, east_set)
    for k, (r, n) in r10b.items():
        d = r - base[k][0]
        print(f"  {k:<6}: R²={r:.4f}  n={n}  Δ={d:+.4f}")

    # === Save ===
    out = {
        "version": "0.3.3",
        "iteration": "v199_author_cleanup",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "calibration": W_OPT,
        "n_author_only": len(author_only),
        "author_only_nodes": sorted(author_only),
        "baseline_v9": {k: {"R2": v[0], "n": v[1]} for k, v in base.items()},
        "v10a_remove": {
            "n_nodes": len(nodes_v10a),
            "n_edges": len(edges_v10a),
            "R2": {k: {"R2": v[0], "n": v[1], "delta": round(v[0] - base[k][0], 4)}
                   for k, v in r10a.items()},
        },
        "v10b_downweight": {
            "W_AUTHOR_FLOOR": W_AUTHOR_FLOOR,
            "n_downweighted": n_downweighted,
            "R2": {k: {"R2": v[0], "n": v[1], "delta": round(v[0] - base[k][0], 4)}
                   for k, v in r10b.items()},
        },
    }
    p = RES / "nipada_v199_graph_v10.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

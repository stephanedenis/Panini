#!/usr/bin/env python3
"""§200 — Surgical edge cleanup (raffinement §199).

§199 montre que retirer TOUS les nœuds author-only effondre R² : les
auteurs sont des PIVOTS de transit indispensables. La conclusion v0.3.2
selon laquelle § 197 identifiait des arêtes "nuisibles" doit être nuancée :
ce ne sont pas les *nœuds* qui nuisent mais des *arêtes spécifiques* dont
le poids ou la classification est probablement mal réglé.

Stratégies :
  v10c — REMOVE TOP-N : retirer uniquement les N arêtes les plus
         nuisibles (Δ_GLOBAL > 0) selon §197
  v10d — RECLASSIFY auteur→œuvre : ré-étiqueter les arêtes
         work→author (compilation, parole rapportée…) en "indirect"
         w=0.01 au lieu de "direct" w=0.45

V_OPT (0.45/0.15/0.01) inchangé.
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

# Top arêtes nuisibles GLOBAL d'après §197 (Δ>0 = leur retrait améliore)
TOP_NUISIBLES = [
    ("confucius_analects_en", "confucius"),
    ("holbach_systeme", "volney_ruines"),
    ("schopenhauer", "buddha"),
    ("dhammapada_muller_en", "buddha"),
    ("feuerbach_christianity_en", "marx_critique"),
    ("hume_dialogues", "volney_ruines"),
    ("lucretius_drn", "voltaire_candide"),
    ("voltaire", "voltaire_candide"),
    ("lucretius_drn", "marx_critique"),
    ("voltaire", "confucius"),
]


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
    print("=== §200 — Surgical edge cleanup ===\n")

    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())
    edges = g9["edges"]
    print(f"Graph v9: {len(nodes)} nœuds, {len(edges)} arêtes")

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
    print(f"Signatures: {len(sigs)}")

    # Baseline
    edges_w_v9 = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                  for e in edges]
    base = compute_strata(node_ids, edges_w_v9, sigs, east_set)
    print("\n=== Baseline v9 ===")
    for k, (r, n) in base.items():
        print(f"  {k:<6}: R²={r:.4f}  n={n}")

    # v10c — REMOVE TOP-N nuisibles, sweep N=1..10
    print("\n=== v10c — REMOVE top-N nuisibles (sweep) ===")
    nuisibles_set = set(TOP_NUISIBLES)
    sweep_results = {}
    for N in [1, 2, 3, 5, 8, 10]:
        target = set(TOP_NUISIBLES[:N])
        edges_keep = [e for e in edges
                      if (e["src"], e["tgt"]) not in target]
        ew = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
              for e in edges_keep]
        r = compute_strata(node_ids, ew, sigs, east_set)
        sweep_results[N] = {k: v[0] for k, v in r.items()}
        print(f"  N={N:>2}  GLOBAL={r['GLOBAL'][0]:.4f}  "
              f"WEST={r['WEST'][0]:.4f}  INTER={r['INTER'][0]:.4f}  "
              f"NW={r['NW'][0]:.4f}")

    # v10d — RECLASSIFY work→pivot_author edges as indirect
    print("\n=== v10d — RECLASSIFY work→author en 'indirect' ===")
    AUTHOR_KINDS = {
        "pivot_author", "philosopher_proto", "religious_figure",
        "philosopher_modern",
    }
    n_reclass = 0

    def w_v10d(e):
        cat = classify(e.get("channel", ""))
        # Si arête œuvre→auteur (target est un nœud auteur), force "indirect"
        tgt_kind = nodes.get(e["tgt"], {}).get("kind", "")
        src_kind = nodes.get(e["src"], {}).get("kind", "")
        if cat == "direct" and (tgt_kind in AUTHOR_KINDS or
                                src_kind in AUTHOR_KINDS):
            # Cas où l'œuvre pointe vers un auteur (compilation, parole
            # rapportée) ou inversement
            if e["src"] in sigs and tgt_kind in AUTHOR_KINDS:
                return W_OPT["indirect"]
            if e["tgt"] in sigs and src_kind in AUTHOR_KINDS:
                # l'auteur est source vers l'œuvre — c'est pertinent (filiation)
                return W_OPT[cat]
        return W_OPT[cat]

    ew_v10d = []
    for e in edges:
        cat = classify(e.get("channel", ""))
        tgt_kind = nodes.get(e["tgt"], {}).get("kind", "")
        src_kind = nodes.get(e["src"], {}).get("kind", "")
        if cat == "direct" and e["src"] in sigs and tgt_kind in AUTHOR_KINDS:
            ew_v10d.append((e["src"], e["tgt"], W_OPT["indirect"]))
            n_reclass += 1
        else:
            ew_v10d.append((e["src"], e["tgt"], W_OPT[cat]))
    print(f"  {n_reclass} arêtes work→author reclassifiées 'direct'→'indirect'")
    r10d = compute_strata(node_ids, ew_v10d, sigs, east_set)
    for k, (r, n) in r10d.items():
        d = r - base[k][0]
        print(f"  {k:<6}: R²={r:.4f}  Δ={d:+.4f}")

    # Save
    out = {
        "version": "0.3.3",
        "iteration": "v200_surgical_cleanup",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "calibration": W_OPT,
        "baseline_v9": {k: {"R2": v[0], "n": v[1]} for k, v in base.items()},
        "v10c_remove_top_N": sweep_results,
        "v10d_reclassify_work_author": {
            "n_reclassified": n_reclass,
            "R2": {k: {"R2": v[0], "n": v[1],
                       "delta": round(v[0] - base[k][0], 4)}
                   for k, v in r10d.items()},
        },
        "top_nuisibles_targeted": [
            {"src": s, "tgt": t} for s, t in TOP_NUISIBLES
        ],
    }
    p = RES / "nipada_v200_surgical_cleanup.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

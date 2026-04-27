#!/usr/bin/env python3
"""§191 — Test placebo des arêtes East-East ajoutées en §189.

Hypothèse à tester : les 9 arêtes ajoutées en §189 portent-elles un signal
spécifique (transmission documentée) ou n'ont-elles fait qu'augmenter la
connectivité aléatoire entre œuvres EAST ?

Méthode : 1000 placebos. Pour chacun, on remplace les 9 arêtes documentées
par 9 arêtes East-East tirées au hasard (parmi C(11,2)=55 paires possibles
EAST×EAST), avec poids et channels arbitrairement "direct". On recalcule R²
sur graph v9-placebo.

Si R²_obs(NW) >> R²_perm(NW), les arêtes documentées portent du signal.
Si distributions chevauchent, signal est purement structural (densité).

Calibration V_OPT (0.45/0.15/0.01).
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
from datetime import datetime, timezone
from itertools import combinations
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

EAST_SIGNED = [
    "bhagavad_gita_arnold_en", "carus_gospel_buddha_en",
    "confucius_analects_en", "dhammapada_muller_en",
    "han_feizi_selections", "khayyam_rubaiyat_fitzgerald_en",
    "koran_rodwell_en", "laozi_taoteching_en", "mozi_selections",
    "upanishads_muller_en", "zhuangzi_giles_en",
]


def classify(ch):
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


def compute_r2(node_ids, edges_w, sigs, idx_corpus, mengzi_handle):
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
    nw_set = set(EAST_SIGNED)
    west = [p for p in pairs if p[0] not in nw_set and p[1] not in nw_set]
    inter = [p for p in pairs if (p[0] in nw_set) != (p[1] in nw_set)]
    nw = [p for p in pairs if p[0] in nw_set and p[1] in nw_set]
    out = {}
    for label, sub in [("GLOBAL", pairs), ("WEST", west),
                       ("INTER", inter), ("NW", nw)]:
        if len(sub) < 3:
            out[label] = (0.0, len(sub))
        else:
            xs = [p[2] for p in sub]
            ys = [p[3] for p in sub]
            out[label] = (pearson(xs, ys) ** 2, len(sub))
    return out


def main():
    print("=== §191 — Test placebo arêtes East-East ajoutées (V_OPT) ===\n")

    g8 = json.loads((RES / "nipada_v182_graph_v8.json").read_text())
    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())

    # Charger signatures
    lex = load_lex()
    sigs = {}
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
    print(f"Signatures: {len(sigs)}")

    # Identifier les 9 arêtes ajoutées en v189
    g9_added = [e for e in g9["edges"] if e.get("added_in") == "v189"]
    print(f"Arêtes v189 (à remplacer en placebo): {len(g9_added)}")

    # Base = g9 sans les arêtes added_in="v189"
    base_edges = [e for e in g9["edges"] if e.get("added_in") != "v189"]
    print(f"Edges de base (v8 + annotations): {len(base_edges)}")

    # Nodes (g9 inclut "mengzi")
    nodes = g9["nodes"]
    node_ids = list(nodes.keys())

    # Pool de paires East-East possibles (parmi 11 EAST signed + mengzi)
    east_universe = list(EAST_SIGNED) + (
        ["mengzi"] if "mengzi" in nodes else []
    )
    all_ee_pairs = list(combinations(east_universe, 2))
    print(f"Univers paires East-East: {len(all_ee_pairs)}")

    # === OBSERVATION : R² avec g9 réel ===
    edges_w_real = [
        (e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
        for e in g9["edges"]
    ]
    obs = compute_r2(node_ids, edges_w_real, sigs, None, None)
    print("\n=== Observation (graph v9 réel) ===")
    for k, (r2, n) in obs.items():
        print(f"  {k:<6}: R²={r2:.4f}  n={n}")

    # === BASE : R² avec g9 sans les 9 arêtes ===
    edges_w_base = [
        (e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
        for e in base_edges
    ]
    base = compute_r2(node_ids, edges_w_base, sigs, None, None)
    print("\n=== Base (g9 sans v189 = ~v8 + mengzi/annotations) ===")
    for k, (r2, n) in base.items():
        print(f"  {k:<6}: R²={r2:.4f}  n={n}")

    # === PLACEBOS : tirer 9 arêtes E-E aléatoires ===
    n_iter = 1000
    rnd = random.Random(2026)
    pool = [p for p in all_ee_pairs]
    placebo_results = {"GLOBAL": [], "WEST": [], "INTER": [], "NW": []}
    print(f"\n=== Placebo n={n_iter} (9 arêtes East-East aléatoires direct) ===")
    for it in range(n_iter):
        sample = rnd.sample(pool, 9)
        placebo_edges = list(edges_w_base)
        for s, t in sample:
            placebo_edges.append((s, t, W_OPT["direct"]))
        r = compute_r2(node_ids, placebo_edges, sigs, None, None)
        for k in placebo_results:
            placebo_results[k].append(r[k][0])
        if (it + 1) % 200 == 0:
            print(f"  ... {it+1}/{n_iter}")

    print("\n=== Comparaison observé vs placebo ===")
    print(f"{'Strate':<8}{'obs R²':>10}{'placebo μ':>11}{'placebo σ':>11}"
          f"{'p (obs ≥ pl)':>14}{'percentile':>12}")
    res = {}
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        obs_r2 = obs[k][0]
        vals = placebo_results[k]
        m = sum(vals) / len(vals)
        v = sum((x - m) ** 2 for x in vals) / len(vals)
        s = math.sqrt(v)
        ge = sum(1 for x in vals if x >= obs_r2)
        p = (ge + 1) / (n_iter + 1)
        sorted_v = sorted(vals)
        pct = sum(1 for x in sorted_v if x <= obs_r2) / len(sorted_v) * 100
        print(f"{k:<8}{obs_r2:>10.4f}{m:>11.4f}{s:>11.4f}"
              f"{p:>14.4f}{pct:>11.1f}%")
        res[k] = {
            "observed_R2": round(obs_r2, 4),
            "base_R2": round(base[k][0], 4),
            "placebo_mean": round(m, 4),
            "placebo_std": round(s, 4),
            "p_obs_ge_placebo": round(p, 4),
            "percentile": round(pct, 1),
        }

    print("\n=== DIAGNOSTIC ===")
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        r = res[k]
        if r["p_obs_ge_placebo"] < 0.05:
            verdict = (
                f"✓ ARÊTES DOCUMENTÉES PORTENT SIGNAL — observé > 95% "
                f"placebos (p={r['p_obs_ge_placebo']:.4f})"
            )
        elif r["p_obs_ge_placebo"] > 0.95:
            verdict = (
                f"✗ ANTI-signal — placebos battent observé (p={r['p_obs_ge_placebo']:.4f})"
            )
        else:
            verdict = (
                f"= signal essentiellement structural (densité) "
                f"(p={r['p_obs_ge_placebo']:.4f}, percentile {r['percentile']:.0f}%)"
            )
        print(f"  {k:<6} : {verdict}")

    out = {
        "version": "0.2.8",
        "iteration": "v191_placebo_east_edges",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_source": "nipada_v189_graph_v9.json",
        "n_iter": n_iter,
        "calibration": W_OPT,
        "n_signatures": len(sigs),
        "n_added_edges_tested": len(g9_added),
        "results": res,
    }
    out_p = RES / "nipada_v191_placebo_east_edges.json"
    out_p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

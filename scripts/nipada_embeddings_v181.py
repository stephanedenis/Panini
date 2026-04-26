#!/usr/bin/env python3
"""§181 — Falsification du diagnostic §179 par embeddings multilingues.

Hypothèse §179 : la limite NW×NW (R²≈0) vient de V14-LEX (cadre gréco-latin),
pas du graphe.

Test : remplacer V14-LEX par embeddings multilingues
(paraphrase-multilingual-MiniLM-L12-v2, 50+ langues incl. zh, ar, hi).

Décision :
  - Si NW×NW avec embeddings devient significatif (p < 0.05) → V14 confirmé bottleneck.
  - Sinon → la limite est dans le graphe ou intrinsèque au corpus.

Usage:
    .venv/bin/python scripts/nipada_embeddings_v181.py
"""
from __future__ import annotations

import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MAX_FRAGS_PER_WORK = 30  # plafond pour limiter le coût
FRAG_MAX_CHARS = 1500    # tronquer chaque fragment


# ────────────── Stat helpers ──────────────

def cosine(a, b):
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(y * y for y in b))
    return num / (da * db) if da and db else 0.0


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


def classify_channel(ch: str) -> str:
    s = ch.lower()
    if any(k in s for k in ["traduction", "translation", "transl"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "lit ", "connaît",
        "connais", "tradition", "comparat", "scepticisme", "lecteur",
        "ascendant", "ami ", "post-", "écho", "reçu", "même école",
        "succession", "admire", "mentionne", "réception", "critique",
        "synthèse", "héritage critique", "commentaire", "compile", "milieu",
    ]):
        return "indirect"
    return "direct"


def floyd_warshall(nodes, edges, weight_map):
    node_ids = list(nodes.keys())
    idx = {n: i for i, n in enumerate(node_ids)}
    N = len(node_ids)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0.0
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        if s not in idx or t not in idx:
            continue
        cat = classify_channel(e.get("channel", ""))
        cost = -math.log(weight_map[cat])
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


# ────────────── Pipeline §181 ──────────────

def main():
    print("=== §181 — Embeddings multilingues (test diagnostic) ===\n")

    print(f"Chargement modèle {MODEL_NAME} ...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    print(f"  dim = {model.get_sentence_embedding_dimension()}\n")

    # 1. Collecte fragments (tronqués) par œuvre
    print("Collecte fragments :")
    work_fragments = {}
    work_traditions = {}
    rnd = random.Random(2026)
    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        frags_p = wdir / "fragments.jsonl"
        prov_p = wdir / "PROVENANCE.json"
        if not frags_p.exists() or not prov_p.exists():
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", wdir.name)
        all_frags = []
        with frags_p.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                txt = rec.get("text") or rec.get("raw_text", "")
                if len(txt) >= 200:
                    all_frags.append(txt[:FRAG_MAX_CHARS])
        if not all_frags:
            continue
        if len(all_frags) > MAX_FRAGS_PER_WORK:
            sampled = rnd.sample(all_frags, MAX_FRAGS_PER_WORK)
        else:
            sampled = all_frags
        work_fragments[wid] = sampled
        work_traditions[wid] = prov.get("tradition", "unknown")
        print(f"  {wid:35s} : {len(sampled)} frags (sur {len(all_frags)})")

    print(f"\nTotal œuvres : {len(work_fragments)}")
    total_frags = sum(len(v) for v in work_fragments.values())
    print(f"Total fragments à encoder : {total_frags}\n")

    # 2. Encodage par lots
    print("Encodage embeddings ...")
    work_embeddings = {}
    for wid, frags in work_fragments.items():
        embs = model.encode(frags, show_progress_bar=False, normalize_embeddings=True)
        # moyenne (puis renormalisation)
        avg = [0.0] * len(embs[0])
        for e in embs:
            for i, v in enumerate(e):
                avg[i] += float(v)
        for i in range(len(avg)):
            avg[i] /= len(embs)
        norm = math.sqrt(sum(v * v for v in avg)) or 1.0
        avg = [v / norm for v in avg]
        work_embeddings[wid] = avg
        print(f"  ✓ {wid}")

    # 3. Charger graphe v6 (poids §177)
    g6 = json.loads((RES_DIR / "nipada_v178_graph_v6.json").read_text())
    print(f"\nGraphe v6 : {len(g6['nodes'])} nodes, {len(g6['edges'])} edges")

    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    D, idx = floyd_warshall(g6["nodes"], g6["edges"], weight_map)

    work_ids = [w for w in work_embeddings if w in idx]
    print(f"Œuvres présentes dans graphe : {len(work_ids)}")

    # 4. Paires connectées
    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            sim = cosine(work_embeddings[a], work_embeddings[b])
            d_emb = 1.0 - sim
            pairs.append({
                "a": a, "b": b,
                "d_graph": d_g,
                "d_emb": d_emb,
                "trad_a": work_traditions[a],
                "trad_b": work_traditions[b],
                "same_trad": work_traditions[a] == work_traditions[b],
            })

    print(f"Paires connectées : {len(pairs)}\n")

    # 5. Stats globales
    xs = [p["d_graph"] for p in pairs]
    ys = [p["d_emb"] for p in pairs]
    r = pearson(xs, ys)
    pv = perm_test(xs, ys)
    print(f"=== §181 GLOBAL  n={len(pairs)} (embeddings) ===")
    print(f"  r={r:+.4f}  R²={r*r:.4f}  p_perm={pv:.4f}")

    inter = [pp for pp in pairs if not pp["same_trad"]]
    intra = [pp for pp in pairs if pp["same_trad"]]
    if inter:
        ri = pearson([pp["d_graph"] for pp in inter], [pp["d_emb"] for pp in inter])
        pi = perm_test([pp["d_graph"] for pp in inter], [pp["d_emb"] for pp in inter])
        print(f"  INTER n={len(inter)} : r={ri:+.4f} R²={ri*ri:.4f} p={pi:.4f}")
    else:
        ri, pi = 0.0, 1.0
    if intra:
        ra = pearson([pp["d_graph"] for pp in intra], [pp["d_emb"] for pp in intra])
        pa = perm_test([pp["d_graph"] for pp in intra], [pp["d_emb"] for pp in intra])
        print(f"  INTRA n={len(intra)} : r={ra:+.4f} R²={ra*ra:.4f} p={pa:.4f}")
    else:
        ra, pa = 0.0, 1.0

    # 6. Sous-corpus NW×NW (test diagnostique critique)
    nw_trads = {
        "chinese_classics", "daoism", "buddhism_theravada",
        "hinduism_smriti", "buddhism_modernist", "islamic_canon",
        "chinese_critic", "chinese_classical", "chinese_legalist",
    }
    nw_ids = {w for w, t in work_traditions.items() if t in nw_trads}
    nw_only = [pp for pp in pairs if pp["a"] in nw_ids and pp["b"] in nw_ids]

    print(f"\n=== §181 NW×NW EXCLUSIF (test diagnostique critique) ===")
    print(f"  œuvres NW : {len(nw_ids)} | paires : {len(nw_only)}")
    if nw_only:
        ro = pearson([pp["d_graph"] for pp in nw_only], [pp["d_emb"] for pp in nw_only])
        po = perm_test([pp["d_graph"] for pp in nw_only], [pp["d_emb"] for pp in nw_only])
        print(f"  EMBEDDINGS NW×NW : r={ro:+.4f} R²={ro*ro:.4f} p={po:.4f}")
        print(f"  vs §178 LEX-V14 : R²=0.0019 p=0.87")
        print(f"  vs §179 LEX-V14+densif : R²=0.0002 p=0.96")
        delta_lex = ro * ro - 0.0019
        print(f"  Δ R²(EMB − LEX) = {delta_lex:+.4f}")
    else:
        ro, po, delta_lex = 0.0, 1.0, 0.0

    # 7. Verdict diagnostic
    print(f"\n=== VERDICT DIAGNOSTIC ===")
    if po < 0.05 and delta_lex > 0.05:
        verdict = "V14-LEX confirmé comme bottleneck — embeddings restaurent signal NW×NW"
    elif po < 0.10 and delta_lex > 0.02:
        verdict = "V14-LEX partiellement bottleneck — amélioration modérée avec embeddings"
    else:
        verdict = ("La limite NW×NW persiste avec embeddings — "
                   "ce n'est pas seulement V14, c'est le graphe ou le corpus oriental")
    print(f"  → {verdict}")

    # 8. Output
    out = {
        "version": "v181_embeddings",
        "model": MODEL_NAME,
        "n_works": len(work_ids),
        "n_pairs": len(pairs),
        "max_frags_per_work": MAX_FRAGS_PER_WORK,
        "weight_map": weight_map,
        "global": {"n": len(pairs), "r": r, "R2": r * r, "p_perm": pv},
        "inter": {"n": len(inter), "r": ri, "R2": ri * ri, "p": pi},
        "intra": {"n": len(intra), "r": ra, "R2": ra * ra, "p": pa},
        "nw_exclusive_emb": {"n": len(nw_only), "r": ro, "R2": ro * ro, "p": po},
        "nw_exclusive_lex_v178": {"R2": 0.0019, "p": 0.87},
        "nw_exclusive_lex_v179": {"R2": 0.0002, "p": 0.96},
        "delta_R2_emb_minus_lex": delta_lex,
        "verdict": verdict,
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    out_path = RES_DIR / "nipada_v181_embeddings_diagnostic.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
§176 — Extension corpus iter4 (22 → 29 œuvres).

7 nouvelles œuvres anglophones acquises via Project Gutenberg :
  - lucretius_drn          (#785, ~55 BCE / Munro 1894 trans, eng)
  - hume_dialogues_nhr     (#4583, 1779, eng)
  - hume_enquiry           (#9662, 1748, eng)
  - spinoza_ttp            (#989, 1670, eng — Elwes trans)
  - ingersoll_works        (#38802, 1879+, eng)
  - paine_age_of_reason    (#3743, 1794, eng)
  - marx_critique          (#46423, 1859, eng — Critique of Political Economy)

Ajout d'un node pivot manquant : lucretius (auteur, ~55 BCE).
Refit complet : graphe v5 + LEX/BIGRAM revalidation + bootstrap rapide.

Output :
  corpus/protoatheism/<work_id>/{raw_text.txt, PROVENANCE.json, fragments.jsonl}
  research/nipada/falsification/nipada_v176_graph_v5.json
  research/nipada/falsification/nipada_v176_revalidation.json
"""

from __future__ import annotations

import datetime
import hashlib
import importlib.util
import itertools
import json
import math
import random
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
RES_DIR = ROOT / "research" / "nipada" / "falsification"

UA = "PaniniResearch/1.0 (academic; +https://github.com/stephanedenis/Panini)"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v145 = _load("nipada_v14_multiling_v145", SCRIPTS / "nipada_v14_multiling_v145.py")
V14 = _v145.V14
LEX = _v145.LEX
NEG_MARKERS = _v145.NEG_MARKERS
UNIV_MARKERS = _v145.UNIV_MARKERS
EQ_MARKERS = _v145.EQ_MARKERS
annotate = _v145.annotate

PAIR_KEYS = [(V14[i], V14[j]) for i in range(len(V14)) for j in range(i + 1, len(V14))]


def fetch_gutenberg(book_id):
    for url in [
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-8.txt",
    ]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = urllib.request.urlopen(req, timeout=30)
            txt = r.read().decode("utf-8", errors="replace")
            if len(txt) > 5000:
                s = re.search(r"\*\*\*\s*START OF .* PROJECT GUTENBERG.*?\*\*\*", txt, re.IGNORECASE)
                e = re.search(r"\*\*\*\s*END OF .* PROJECT GUTENBERG.*?\*\*\*", txt, re.IGNORECASE)
                if s and e:
                    return txt[s.end():e.start()].strip(), url
                return txt, url
        except Exception:
            continue
    raise RuntimeError(f"Gutenberg #{book_id} unreachable")


def split_paragraphs(text, min_words=25, max_words=800):
    raw = re.split(r"\n{2,}", text)
    out = []
    for p in raw:
        p = re.sub(r"\s+", " ", p).strip()
        wc = len(p.split())
        if wc < min_words:
            continue
        if wc <= max_words:
            out.append(p)
            continue
        sentences = re.split(r"(?<=[.!?])\s+", p)
        cur, cur_wc = "", 0
        for s in sentences:
            sw = len(s.split())
            if cur_wc + sw > max_words and cur:
                out.append(cur.strip())
                cur, cur_wc = s, sw
            else:
                cur = (cur + " " + s).strip() if cur else s
                cur_wc += sw
        if cur and cur_wc >= min_words:
            out.append(cur.strip())
    return out


WORKS = [
    {"work_id": "lucretius_drn", "gid": 785, "year": -55, "lang": "eng",
     "tradition": "ANCIENT_EPICUREAN", "author": "lucretius",
     "edition": "De Rerum Natura, Munro trans 1894"},
    {"work_id": "hume_dialogues_nhr", "gid": 4583, "year": 1779, "lang": "eng",
     "tradition": "EUR_SCEPTICAL_EMPIRICIST", "author": "hume",
     "edition": "Dialogues Concerning Natural Religion, posthumous 1779"},
    {"work_id": "hume_enquiry", "gid": 9662, "year": 1748, "lang": "eng",
     "tradition": "EUR_SCEPTICAL_EMPIRICIST", "author": "hume",
     "edition": "Enquiry Concerning Human Understanding, 1748"},
    {"work_id": "spinoza_ttp", "gid": 989, "year": 1670, "lang": "eng",
     "tradition": "EUR_RATIONALIST_NATURAL_RELIGION", "author": "spinoza",
     "edition": "Theologico-Political Treatise, Elwes trans 1883"},
    {"work_id": "ingersoll_works", "gid": 38802, "year": 1879, "lang": "eng",
     "tradition": "AMERICAN_FREETHINKER", "author": "ingersoll",
     "edition": "Works of Robert G. Ingersoll Vol. 02 (Mistakes of Moses+)"},
    {"work_id": "paine_age_of_reason", "gid": 3743, "year": 1794, "lang": "eng",
     "tradition": "EUR_DEIST_ANTICLERICAL", "author": "paine",
     "edition": "The Age of Reason, 1794-1796"},
    {"work_id": "marx_critique", "gid": 46423, "year": 1859, "lang": "eng",
     "tradition": "EUR_MATERIALIST_HISTORICAL", "author": "marx",
     "edition": "A Contribution to the Critique of Political Economy, 1859"},
]


# Nouveaux pivots auteur
NEW_PIVOTS = {
    "lucretius": {"year": -55, "label": "PIVOT_EPICUREAN"},
    "hume":      {"year": 1750, "label": "PIVOT_SCEPTICAL_EMPIRICIST"},
    "paine":     {"year": 1794, "label": "PIVOT_DEIST"},
    "ingersoll": {"year": 1879, "label": "PIVOT_FREETHINKER"},
    "marx":      {"year": 1859, "label": "PIVOT_MATERIALIST_HISTORICAL"},
}

W_DIRECT = 0.80
W_DIRECT_TRANSLATION = 0.65
W_INDIRECT = 0.35

# Arêtes documentées historiquement
NEW_EDGES = [
    # Lucretius racine ancienne
    ("epicurus", "lucretius", W_DIRECT, "filiation directe ; Lucrèce élève d'Epicure via Philodème"),
    ("lucretius", "lucretius_drn", W_DIRECT, "identité auteur"),
    ("lucretius_drn", "hobbes_leviathan_complete", W_INDIRECT, "Hobbes lit Lucrèce"),
    ("lucretius_drn", "spinoza_ethica_complete", W_INDIRECT, "Spinoza connaît Lucrèce"),
    ("lucretius_drn", "holbach_systeme", W_DIRECT, "Holbach cite explicitement Lucrèce"),
    ("lucretius_drn", "holbach_systeme_en", W_DIRECT, "idem traduction"),
    ("lucretius_drn", "voltaire_candide", W_INDIRECT, "Voltaire connaissance classique"),
    ("lucretius_drn", "marx_critique", W_DIRECT, "Marx thèse doctorale sur Démocrite/Epicure ; lit Lucrèce"),

    # Hume Dialogues = même node existant ; on relie l'œuvre acquise
    ("hume_dialogues", "hume_dialogues_nhr", W_DIRECT, "même œuvre, édition Gutenberg"),
    ("hume_dialogues", "hume_enquiry", W_DIRECT, "même auteur"),
    ("hume_dialogues_nhr", "hume_enquiry", W_DIRECT, "même auteur, projet philosophique commun"),
    ("hume", "hume_dialogues_nhr", W_DIRECT, "identité auteur"),
    ("hume", "hume_enquiry", W_DIRECT, "identité auteur"),

    # Spinoza TTP frère cadet de l'Ethica
    ("spinoza_ethica_complete", "spinoza_ttp", W_DIRECT, "même auteur, programme commun"),
    ("hobbes_leviathan_complete", "spinoza_ttp", W_DIRECT, "Hobbes lu par Spinoza, similitudes critique des Écritures"),
    ("spinoza_ttp", "voltaire_candide", W_INDIRECT, "Voltaire lit Spinoza"),
    ("spinoza_ttp", "holbach_systeme", W_INDIRECT, "Holbach descendant TTP"),

    # Ingersoll
    ("paine", "ingersoll_works", W_DIRECT, "Ingersoll héritier du free-thought de Paine"),
    ("paine_age_of_reason", "ingersoll_works", W_DIRECT, "filiation directe revendiquée"),
    ("voltaire", "ingersoll_works", W_INDIRECT, "Ingersoll cite Voltaire"),
    ("hume_dialogues_nhr", "ingersoll_works", W_INDIRECT, "héritage sceptique"),
    ("feuerbach_christianity_en", "ingersoll_works", W_INDIRECT, "critique de l'anthropologie chrétienne"),

    # Paine Age of Reason
    ("paine", "paine_age_of_reason", W_DIRECT, "identité auteur"),
    ("voltaire", "paine_age_of_reason", W_DIRECT, "Paine lit Voltaire (déisme français)"),
    ("hume_dialogues_nhr", "paine_age_of_reason", W_INDIRECT, "héritage sceptique commun"),
    ("holbach_systeme_en", "paine_age_of_reason", W_INDIRECT, "tradition matérialiste lue par Paine"),

    # Marx Critique
    ("marx", "marx_critique", W_DIRECT, "identité auteur"),
    ("hegel", "marx_critique", W_DIRECT, "Marx héritier critique de Hegel"),
    ("feuerbach_wesen", "marx_critique", W_DIRECT, "Marx critique Feuerbach explicitement"),
    ("feuerbach_christianity_en", "marx_critique", W_DIRECT, "version anglaise lue par cercle marxien"),
    ("holbach_systeme", "marx_critique", W_INDIRECT, "matérialisme français → matérialisme historique"),

    # Pivots auteurs reliés au réseau existant
    ("epicurus", "hume", W_INDIRECT, "Hume formé sur la philosophie ancienne"),
    ("hume", "voltaire", W_DIRECT, "Voltaire admire Hume"),
    ("hume", "holbach_systeme", W_DIRECT, "Holbach hôte de Hume à Paris"),
    ("voltaire", "paine", W_DIRECT, "Paine francophile lecteur de Voltaire"),
    ("hume", "paine", W_INDIRECT, "Paine connaît Hume"),
    ("ingersoll", "ingersoll_works", W_DIRECT, "identité"),
]


def build_adj(edges):
    adj = {}
    for src, tgt, w, ch in edges:
        adj.setdefault(src, {})
        if tgt in adj[src]:
            if w > adj[src][tgt]["weight"]:
                adj[src][tgt] = {"weight": w, "channel": ch}
        else:
            adj[src][tgt] = {"weight": w, "channel": ch}
    return adj


def floyd_warshall(adj, all_nodes):
    INF = math.inf
    n = len(all_nodes)
    idx = {nid: i for i, nid in enumerate(all_nodes)}
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0.0
    for src, neigh in adj.items():
        if src not in idx:
            continue
        for tgt, info in neigh.items():
            if tgt not in idx:
                continue
            cost = -math.log(info["weight"])
            i, j = idx[src], idx[tgt]
            d[i][j] = min(d[i][j], cost)
            d[j][i] = min(d[j][i], cost)
    for k in range(n):
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + d[k][j]
                if nd < d[i][j]:
                    d[i][j] = nd
    out = {}
    for i, a in enumerate(all_nodes):
        for j, b in enumerate(all_nodes):
            if i < j:
                out[(a, b)] = d[i][j]
    return out


def freq_signature(text, lang):
    counts = {a: 0 for a in V14}
    text_lc = text.lower() if lang != "lzh" else text
    for atom in V14:
        for m in LEX.get(atom, {}).get(lang, []):
            mlc = m.lower() if lang != "lzh" else m
            counts[atom] += text_lc.count(mlc)
    for m in NEG_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["DIFFÉRENCE"] += 1
            counts["MODALITÉ"] += 1
    for m in UNIV_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["MODALITÉ"] += 1
    for m in EQ_MARKERS.get(lang, []):
        ml = m.lower() if lang != "lzh" else m
        if ml in text_lc:
            counts["ÊTRE"] += 1
            counts["ÉQUATION"] += 1
    if any(c.isdigit() for c in text):
        counts["NOMBRE"] += 1
    return counts


def cosine(a, b):
    keys = set(a) | set(b)
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na > 0 and nb > 0 else 0.0


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0.0


def perm_test(xs, ys, n_iter=2000):
    obs = pearson(xs, ys) ** 2
    rng = random.Random(42)
    yshuf = list(ys)
    cnt = 0
    for _ in range(n_iter):
        rng.shuffle(yshuf)
        if pearson(xs, yshuf) ** 2 >= obs:
            cnt += 1
    return cnt / n_iter


def main():
    # PHASE 1 — Acquisition
    print("=== §176 PHASE 1 : Acquisition ===")
    acq = []
    for w in WORKS:
        print(f"\n→ {w['work_id']} (#{w['gid']})")
        try:
            text, url = fetch_gutenberg(w["gid"])
        except Exception as e:
            print(f"  ✗ {e}")
            acq.append({"work_id": w["work_id"], "status": "FAILED", "error": str(e)})
            continue
        wd = CORPUS_DIR / w["work_id"]
        wd.mkdir(parents=True, exist_ok=True)
        (wd / "raw_text.txt").write_text(text, encoding="utf-8")
        prov = {
            "source_type": "Project Gutenberg",
            "source_url": url,
            "gutenberg_id": w["gid"],
            "edition": w["edition"],
            "original_language": w["lang"],
            "text_language": w["lang"],
            "license": "Public Domain (Gutenberg)",
            "retrieval_date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "byte_length": len(text.encode("utf-8")),
            "completeness": "Complete (Gutenberg edition)",
        }
        (wd / "PROVENANCE.json").write_text(
            json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
        paras = split_paragraphs(text)
        with (wd / "fragments.jsonl").open("w", encoding="utf-8") as f:
            for i, p in enumerate(paras, start=1):
                fr = {
                    "work_id": w["work_id"],
                    "frag_id": f"{w['work_id'][:8]}_{i:04d}",
                    "fragment_id": f"{w['work_id'][:8]}_{i:04d}",
                    "lang": w["lang"], "section": "BODY",
                    "text": p, "raw_text": p,
                    "source_year": w["year"],
                    "tradition_label": w["tradition"],
                }
                f.write(json.dumps(fr, ensure_ascii=False) + "\n")
        print(f"  ✓ {len(text)} bytes, {len(paras)} fragments")
        acq.append({"work_id": w["work_id"], "status": "ACQUIRED",
                    "n_fragments": len(paras), "byte_length": prov["byte_length"]})

    # PHASE 2 — Graphe v5
    print("\n=== §176 PHASE 2 : Graphe v5 ===")
    v172 = json.loads((RES_DIR / "nipada_v172_graph_v4.json").read_text(encoding="utf-8"))
    nodes = dict(v172["nodes"])
    for pid, info in NEW_PIVOTS.items():
        if pid not in nodes:
            nodes[pid] = {"kind": "pivot_author", "author": pid, **info}
    acquired_ids = {a["work_id"] for a in acq if a["status"] == "ACQUIRED"}
    for w in WORKS:
        if w["work_id"] in acquired_ids:
            nodes[w["work_id"]] = {
                "kind": "proto_atheist_work",
                "year": w["year"], "lang": w["lang"],
                "tradition_label": w["tradition"], "author": w["author"],
            }
    edges_v4 = [(e["src"], e["tgt"], e["weight"], e["channel"]) for e in v172["edges"]]
    edges_v5 = edges_v4 + [e for e in NEW_EDGES if e[0] in nodes and e[1] in nodes]
    adj = build_adj(edges_v5)
    all_nodes = list(nodes.keys())
    paths = floyd_warshall(adj, all_nodes)
    proto_works = sorted([n for n, info in nodes.items() if info.get("kind") == "proto_atheist_work"])
    proto_pairs = {}
    for i, a in enumerate(proto_works):
        for b in proto_works[i + 1:]:
            d = paths.get((a, b)) or paths.get((b, a))
            proto_pairs[f"{a}::{b}"] = d if (d is not None and math.isfinite(d)) else None
    n_total = len(proto_pairs)
    n_conn = sum(1 for v in proto_pairs.values() if v is not None)
    graph_payload = {
        "version": "v176_v5",
        "step": "§176 — graphe v5 (corpus 22→29 œuvres)",
        "n_nodes": len(nodes), "n_edges": len(edges_v5),
        "n_proto_works": len(proto_works),
        "n_pairs_total": n_total, "n_pairs_connected": n_conn,
        "nodes": nodes,
        "edges": [{"src": s, "tgt": t, "weight": w, "channel": c}
                  for (s, t, w, c) in edges_v5],
        "proto_pair_distances": proto_pairs,
    }
    (RES_DIR / "nipada_v176_graph_v5.json").write_text(
        json.dumps(graph_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ {len(nodes)} nodes, {len(edges_v5)} edges, {n_total} paires, {n_conn} connectées")

    # PHASE 3 — Revalidation
    print("\n=== §176 PHASE 3 : Revalidation ===")
    frags_all = []
    for d in sorted(CORPUS_DIR.iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                frags_all.append(json.loads(line))

    lex_sigs, bigr_sigs = {}, {}
    for w in proto_works:
        wfrags = [f for f in frags_all if f["work_id"] == w]
        if not wfrags:
            continue
        lex = {a: 0.0 for a in V14}
        for f in wfrags:
            c = freq_signature(f["text"], f["lang"])
            for a in V14:
                lex[a] += c[a]
        tot = sum(lex.values())
        lex_sigs[w] = {a: lex[a] / tot if tot > 0 else 1.0 / 14 for a in V14}
        bcounts = {f"{a}|{b}": 0 for (a, b) in PAIR_KEYS}
        n = 0
        for f in wfrags:
            atoms = annotate(f["text"], f["lang"])
            ordered = [a for a in V14 if a in atoms]
            for a, b in itertools.combinations(ordered, 2):
                bcounts[f"{a}|{b}"] += 1
            n += 1
        bigr_sigs[w] = {k: v / n if n > 0 else 0.0 for k, v in bcounts.items()}

    pairs_lex, pairs_bigr, pairs_dgr = [], [], []
    intra_idx, inter_idx = [], []
    traditions = {w: nodes[w].get("tradition_label", "?") for w in proto_works}
    for i, a in enumerate(proto_works):
        for b in proto_works[i + 1:]:
            d_graph = proto_pairs.get(f"{a}::{b}") or proto_pairs.get(f"{b}::{a}")
            if d_graph is None or a not in lex_sigs or b not in lex_sigs:
                continue
            pairs_lex.append(1.0 - cosine(lex_sigs[a], lex_sigs[b]))
            pairs_bigr.append(1.0 - cosine(bigr_sigs[a], bigr_sigs[b]))
            pairs_dgr.append(d_graph)
            (intra_idx if traditions[a] == traditions[b] else inter_idx).append(len(pairs_dgr) - 1)

    n_p = len(pairs_dgr)
    r_lex = pearson(pairs_lex, pairs_dgr)
    r_bigr = pearson(pairs_bigr, pairs_dgr)
    p_lex = perm_test(pairs_lex, pairs_dgr)
    p_bigr = perm_test(pairs_bigr, pairs_dgr)

    # LOO inter
    inter_lex = [pairs_lex[i] for i in inter_idx]
    inter_bigr = [pairs_bigr[i] for i in inter_idx]
    inter_dgr = [pairs_dgr[i] for i in inter_idx]
    intra_lex = [pairs_lex[i] for i in intra_idx]
    intra_bigr = [pairs_bigr[i] for i in intra_idx]
    intra_dgr = [pairs_dgr[i] for i in intra_idx]

    r_inter_lex = pearson(inter_lex, inter_dgr)
    r_inter_bigr = pearson(inter_bigr, inter_dgr)
    p_inter_lex = perm_test(inter_lex, inter_dgr, n_iter=1000) if len(inter_dgr) >= 4 else None
    p_inter_bigr = perm_test(inter_bigr, inter_dgr, n_iter=1000) if len(inter_dgr) >= 4 else None
    r_intra_lex = pearson(intra_lex, intra_dgr) if len(intra_dgr) >= 4 else None

    # Power
    z_alpha = 1.96
    z_beta = 0.84
    fz = math.atanh(0.224)
    pw = None
    if n_p > 4:
        z = fz / (1.0 / math.sqrt(n_p - 3))
        from math import erf
        def phi(x): return 0.5 * (1 + erf(x / math.sqrt(2)))
        pw = {
            "current_power": round(1 - phi(z_alpha - z) + phi(-z_alpha - z), 4),
            "n_required_pow_0.80": int(math.ceil(((z_alpha + z_beta) / fz) ** 2 + 3)),
        }

    summary = {
        "n_works_eligible": len(lex_sigs),
        "n_pairs_total": n_p,
        "n_pairs_intra": len(intra_idx),
        "n_pairs_inter": len(inter_idx),
        "lex_R2": round(r_lex ** 2, 4),
        "lex_pearson_r": round(r_lex, 4),
        "lex_p_perm": round(p_lex, 4),
        "bigram_R2": round(r_bigr ** 2, 4),
        "bigram_pearson_r": round(r_bigr, 4),
        "bigram_p_perm": round(p_bigr, 4),
        "inter_lex_R2": round(r_inter_lex ** 2, 4) if inter_idx else None,
        "inter_lex_p_perm": round(p_inter_lex, 4) if p_inter_lex is not None else None,
        "inter_bigram_R2": round(r_inter_bigr ** 2, 4) if inter_idx else None,
        "inter_bigram_p_perm": round(p_inter_bigr, 4) if p_inter_bigr is not None else None,
        "intra_lex_R2": round(r_intra_lex ** 2, 4) if r_intra_lex is not None else None,
        "power": pw,
    }
    payload = {"version": "v176", "summary": summary, "acquisition": acq,
               "lex_signatures": lex_sigs}
    (RES_DIR / "nipada_v176_revalidation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== VERDICT §176 ===")
    print(f"Œuvres : {summary['n_works_eligible']}  Paires totales : {n_p} (intra={len(intra_idx)} inter={len(inter_idx)})")
    print(f"  GLOBAL  LEX R²={summary['lex_R2']:.4f} r={r_lex:+.4f} p={p_lex:.4f}")
    print(f"  GLOBAL  BIGRAM R²={summary['bigram_R2']:.4f} r={r_bigr:+.4f} p={p_bigr:.4f}")
    if inter_idx:
        print(f"  INTER   LEX R²={summary['inter_lex_R2']:.4f} p={summary['inter_lex_p_perm']}")
        print(f"  INTER   BIGRAM R²={summary['inter_bigram_R2']:.4f} p={summary['inter_bigram_p_perm']}")
    if pw:
        print(f"  Puissance courante = {pw['current_power']}  n requis = {pw['n_required_pow_0.80']}")


if __name__ == "__main__":
    main()

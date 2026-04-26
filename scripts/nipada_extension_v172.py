#!/usr/bin/env python3
"""
§172 — Extension corpus iteration 3 (boost vers n=154).

Acquiert 8 œuvres supplémentaires Gutenberg, fragmente, intègre au graphe,
refit. Vise à passer de 14 → 22 œuvres et de 51 → ~120 paires connectées.

Œuvres cibles :
  - holbach_systeme_en       (#8909, EN — complément du fr existant)
  - voltaire_candide         (#4650, fr)
  - feuerbach_christianity_en (#47025, EN — complément du deu existant)
  - nietzsche_antichrist     (#19322, EN)
  - nietzsche_genealogy      (#52319, EN)
  - nietzsche_twilight       (#52263, EN)
  - volney_ruines            (#27931, fr)
  - schopenhauer_pessimism   (#10732, EN)

Pipeline en une passe :
  1. Fetch + provenance + raw_text
  2. Fragmentation (paragraphes 25-800 mots, sections détectées si possible)
  3. Annotation V14 + signatures lex+bigram
  4. Update graph v4 (nouvelles arêtes documentées)
  5. Refit OLS + Pearson + perm + power

Output :
  - corpus/protoatheism/<work_id>/{raw_text.txt, PROVENANCE.json, fragments.jsonl}
  - research/nipada/falsification/nipada_v172_extension.json (récap acquisition)
  - research/nipada/falsification/nipada_v172_graph_v4.json
  - research/nipada/falsification/nipada_v172_revalidation.json
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
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
RES_DIR = ROOT / "research" / "nipada" / "falsification"

USER_AGENT = "PaniniResearch/1.0 (academic; +https://github.com/stephanedenis/Panini)"


def _load(name: str, path: Path):
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


# ────────── Acquisition ──────────


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def gutenberg_strip(text: str) -> str:
    s = re.search(r"\*\*\*\s*START OF .* PROJECT GUTENBERG.*?\*\*\*", text, re.IGNORECASE)
    e = re.search(r"\*\*\*\s*END OF .* PROJECT GUTENBERG.*?\*\*\*", text, re.IGNORECASE)
    if s and e:
        return text[s.end():e.start()].strip()
    return text


def fetch_gutenberg(book_id: int) -> tuple[str, str]:
    for url in [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-8.txt",
    ]:
        try:
            txt = fetch(url)
            if len(txt) > 5000:
                return gutenberg_strip(txt), url
        except Exception:
            continue
    raise RuntimeError(f"Gutenberg #{book_id} unreachable")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


WORKS_PLAN = [
    {"work_id": "holbach_systeme_en", "gid": 8909, "year": 1770, "lang": "eng",
     "tradition": "EUR_MATERIALIST_ATHEIST", "author": "holbach",
     "edition": "Système de la nature, English translation H.D. Robinson 1868"},
    {"work_id": "voltaire_candide", "gid": 4650, "year": 1759, "lang": "fra",
     "tradition": "EUR_DEIST_ANTICLERICAL", "author": "voltaire",
     "edition": "Candide ou l'optimisme, French original 1759"},
    {"work_id": "feuerbach_christianity_en", "gid": 47025, "year": 1841, "lang": "eng",
     "tradition": "EUR_RATIONALIST_CRITIC", "author": "feuerbach",
     "edition": "Essence of Christianity, trans. George Eliot 1854"},
    {"work_id": "nietzsche_antichrist", "gid": 19322, "year": 1888, "lang": "eng",
     "tradition": "EUR_ANTI_CHRISTIAN", "author": "nietzsche",
     "edition": "The Antichrist, trans. H.L. Mencken 1920"},
    {"work_id": "nietzsche_genealogy", "gid": 52319, "year": 1887, "lang": "eng",
     "tradition": "EUR_ANTI_CHRISTIAN", "author": "nietzsche",
     "edition": "Genealogy of Morals, trans. Horace B. Samuel 1913"},
    {"work_id": "nietzsche_twilight", "gid": 52263, "year": 1888, "lang": "eng",
     "tradition": "EUR_ANTI_CHRISTIAN", "author": "nietzsche",
     "edition": "Twilight of the Idols, trans. Anthony Ludovici 1911"},
    {"work_id": "volney_ruines", "gid": 27931, "year": 1791, "lang": "fra",
     "tradition": "EUR_DEIST_ANTICLERICAL", "author": "volney",
     "edition": "Les Ruines, French original 1791"},
    {"work_id": "schopenhauer_pessimism", "gid": 10732, "year": 1851, "lang": "eng",
     "tradition": "EUR_PESSIMIST_CRITIC", "author": "schopenhauer",
     "edition": "Studies in Pessimism, trans. T. Bailey Saunders 1890"},
]


# ────────── Fragmentation ──────────


def split_paragraphs(text: str, min_words: int = 25, max_words: int = 800) -> list[str]:
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


def fragmentize(work_meta: dict, text: str) -> list[dict]:
    paras = split_paragraphs(text)
    out = []
    for i, p in enumerate(paras, start=1):
        out.append({
            "work_id": work_meta["work_id"],
            "frag_id": f"{work_meta['work_id'][:6]}_{i:04d}",
            "fragment_id": f"{work_meta['work_id'][:6]}_{i:04d}",
            "lang": work_meta["lang"],
            "section": "BODY",
            "text": p,
            "raw_text": p,
            "source_year": work_meta["year"],
            "tradition_label": work_meta["tradition"],
        })
    return out


# ────────── Graph v4 (extension) ──────────


W_DIRECT = 0.80
W_DIRECT_TRANSLATION = 0.65
W_INDIRECT = 0.35

# Arêtes documentées historiquement pour les 8 nouvelles œuvres
NEW_EDGES_V4 = [
    # === Holbach EN — traduction de l'œuvre fr existante ===
    ("holbach_systeme", "holbach_systeme_en", W_DIRECT_TRANSLATION,
     "traduction H.D. Robinson 1868 du Système 1770"),
    # Holbach EN connecté aux mêmes ascendants que la version fr
    ("hobbes_leviathan_complete", "holbach_systeme_en", W_INDIRECT,
     "même transmission que vers holbach fr"),

    # === Voltaire Candide ===
    ("voltaire", "voltaire_candide", W_DIRECT,
     "identité auteur"),
    ("bayle", "voltaire_candide", W_INDIRECT,
     "scepticisme baylien"),
    ("hobbes_leviathan_complete", "voltaire_candide", W_INDIRECT,
     "tradition critique anglaise reçue par Voltaire"),

    # === Feuerbach EN — traduction du Wesen ===
    ("feuerbach_wesen", "feuerbach_christianity_en", W_DIRECT_TRANSLATION,
     "traduction George Eliot 1854 du Wesen 1841"),

    # === Nietzsche — école anti-chrétienne ===
    ("schopenhauer", "nietzsche_antichrist", W_DIRECT,
     "Nietzsche disciple critique de Schopenhauer"),
    ("schopenhauer", "nietzsche_genealogy", W_DIRECT,
     "filiation directe"),
    ("schopenhauer", "nietzsche_twilight", W_DIRECT,
     "filiation directe"),
    ("feuerbach_wesen", "nietzsche_antichrist", W_DIRECT,
     "Nietzsche lit Feuerbach explicitement"),
    ("feuerbach_wesen", "nietzsche_genealogy", W_INDIRECT,
     "généalogie de la morale chrétienne"),
    ("feuerbach_wesen", "nietzsche_twilight", W_INDIRECT,
     "critique de l'idéal moral"),
    ("nietzsche_genealogy", "nietzsche_antichrist", W_DIRECT,
     "même auteur, même période 1887-1888"),
    ("nietzsche_twilight", "nietzsche_antichrist", W_DIRECT,
     "même auteur, 1888"),
    ("nietzsche_genealogy", "nietzsche_twilight", W_DIRECT,
     "même auteur"),

    # === Volney Ruines ===
    ("volney", "volney_ruines", W_DIRECT,
     "identité auteur"),
    ("holbach_systeme", "volney_ruines", W_DIRECT,
     "Volney héritier des Lumières matérialistes françaises"),
    ("hume_dialogues", "volney_ruines", W_INDIRECT,
     "comparatisme religieux 18ᵉ s."),

    # === Schopenhauer ===
    ("schopenhauer", "schopenhauer_pessimism", W_DIRECT,
     "identité auteur"),
    ("hume_dialogues", "schopenhauer_pessimism", W_INDIRECT,
     "Hume cité par Schopenhauer"),
    ("feuerbach_wesen", "schopenhauer_pessimism", W_INDIRECT,
     "post-hégélianisme allemand commun"),
    ("spinoza_ethica_complete", "schopenhauer_pessimism", W_DIRECT,
     "Schopenhauer cite Spinoza"),

    # === Auteurs comme nodes ===
    # voltaire et schopenhauer doivent être des nodes pivot
]

NEW_PIVOTS_V4 = {
    "voltaire":      {"year": 1750, "label": "PIVOT_DEIST_FRENCH"},
    "schopenhauer":  {"year": 1850, "label": "PIVOT_GERMAN_PESSIMIST"},
    "volney":        {"year": 1791, "label": "PIVOT_DEIST_FRENCH"},
    "bayle":         {"year": 1697, "label": "PIVOT_SCEPTIC_FRENCH"},
}

NEW_PIVOT_EDGES_V4 = [
    # bayle → existing nodes (rétro-ajout)
    ("bayle", "holbach_systeme", W_INDIRECT,
     "Holbach lit Bayle"),
    ("bayle", "hume_dialogues", W_DIRECT,
     "Hume connaît Bayle"),
    ("bayle", "voltaire", W_DIRECT,
     "Voltaire admire Bayle"),
    # voltaire → autres
    ("voltaire", "holbach_systeme", W_DIRECT,
     "ami et collègue de Holbach"),
    # schopenhauer dans le réseau
    ("hume_dialogues", "schopenhauer", W_DIRECT,
     "Schopenhauer cite Hume"),
    ("spinoza_ethica_complete", "schopenhauer", W_DIRECT,
     "Schopenhauer cite Spinoza"),
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


# ────────── Annotation + signatures ──────────


def freq_signature(text: str, lang: str) -> dict[str, float]:
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


def perm_test_r2(xs, ys, n_iter=2000, seed=42):
    obs = pearson(xs, ys) ** 2
    rng = random.Random(seed)
    yshuf = list(ys)
    cnt = 0
    for _ in range(n_iter):
        rng.shuffle(yshuf)
        if pearson(xs, yshuf) ** 2 >= obs:
            cnt += 1
    return cnt / n_iter


def power_estimate(n, r_target=0.224):
    if n < 4:
        return None
    z_alpha = 1.96
    fz = math.atanh(r_target)
    se = 1.0 / math.sqrt(n - 3)
    z = fz / se
    def phi(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    pw = 1.0 - phi(z_alpha - z) + phi(-z_alpha - z)
    z_beta = 0.84
    n_req = int(math.ceil(((z_alpha + z_beta) / fz) ** 2 + 3))
    return {"current_power": round(pw, 4), "n_required_pow_0.80": n_req}


# ────────── Main ──────────


def main():
    # Step 1: Acquisition
    print("=== §172 PHASE 1 : Acquisition ===")
    acq_summary = []
    for w in WORKS_PLAN:
        print(f"\n→ {w['work_id']} (#{w['gid']})")
        try:
            text, url = fetch_gutenberg(w["gid"])
        except Exception as e:
            print(f"  ✗ {e}")
            acq_summary.append({"work_id": w["work_id"], "status": "FAILED", "error": str(e)})
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
            "sha256": sha256_text(text),
            "byte_length": len(text.encode("utf-8")),
            "completeness": "Complete (Gutenberg edition)",
        }
        (wd / "PROVENANCE.json").write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
        # Step 2: fragment
        frags = fragmentize(w, text)
        with (wd / "fragments.jsonl").open("w", encoding="utf-8") as f:
            for fr in frags:
                f.write(json.dumps(fr, ensure_ascii=False) + "\n")
        print(f"  ✓ {len(text)} bytes, {len(frags)} fragments, sha={prov['sha256'][:12]}")
        acq_summary.append({
            "work_id": w["work_id"], "status": "ACQUIRED",
            "byte_length": prov["byte_length"], "n_fragments": len(frags),
            "sha256": prov["sha256"], "url": url,
        })

    # Step 3: Graph v4
    print("\n=== §172 PHASE 2 : Graph v4 ===")
    v168 = json.loads((RES_DIR / "nipada_v168_inheritance_graph_v3.json").read_text(encoding="utf-8"))
    nodes = dict(v168["nodes"])
    for pid, info in NEW_PIVOTS_V4.items():
        if pid not in nodes:
            nodes[pid] = {"kind": "pivot_author", "author": pid, **info}
    acquired_ids = [s["work_id"] for s in acq_summary if s["status"] == "ACQUIRED"]
    v172_meta = {}
    for w in WORKS_PLAN:
        if w["work_id"] in acquired_ids:
            nodes[w["work_id"]] = {
                "kind": "proto_atheist_work",
                "year": w["year"], "lang": w["lang"],
                "tradition_label": w["tradition"], "author": w["author"],
            }
    edges_v3 = [(e["src"], e["tgt"], e["weight"], e["channel"]) for e in v168["edges"]]
    edges_v4 = edges_v3 + [
        e for e in NEW_EDGES_V4
        if e[0] in nodes and e[1] in nodes
    ] + [
        e for e in NEW_PIVOT_EDGES_V4
        if e[0] in nodes and e[1] in nodes
    ]
    adj = build_adj(edges_v4)
    all_node_ids = list(nodes.keys())
    paths = floyd_warshall(adj, all_node_ids)

    proto_works = sorted([n for n, info in nodes.items() if info.get("kind") == "proto_atheist_work"])
    proto_pairs = {}
    for i, a in enumerate(proto_works):
        for b in proto_works[i + 1:]:
            d = paths.get((a, b), paths.get((b, a), math.inf))
            proto_pairs[f"{a}::{b}"] = d if math.isfinite(d) else None

    n_pairs_total = len(proto_pairs)
    n_connected = sum(1 for v in proto_pairs.values() if v is not None)
    graph_payload = {
        "version": "v172_v4",
        "step": "§172 — graphe v4 (corpus +8 œuvres)",
        "n_nodes": len(nodes),
        "n_edges": len(edges_v4),
        "n_proto_works": len(proto_works),
        "n_pairs_total": n_pairs_total,
        "n_pairs_connected": n_connected,
        "nodes": nodes,
        "edges": [{"src": s, "tgt": t, "weight": w, "channel": c} for (s, t, w, c) in edges_v4],
        "proto_pair_distances": proto_pairs,
    }
    (RES_DIR / "nipada_v172_graph_v4.json").write_text(
        json.dumps(graph_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ {len(nodes)} nodes, {len(edges_v4)} edges, {n_pairs_total} paires, {n_connected} connectées")

    # Step 4: Revalidation
    print("\n=== §172 PHASE 3 : Revalidation ===")
    frags_all = []
    for d in sorted(CORPUS_DIR.iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                frags_all.append(json.loads(line))

    # Signatures par œuvre
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
        # Bigram
        bcounts = {f"{a}|{b}": 0 for (a, b) in PAIR_KEYS}
        n = 0
        for f in wfrags:
            atoms = annotate(f["text"], f["lang"])
            ordered = [a for a in V14 if a in atoms]
            for a, b in itertools.combinations(ordered, 2):
                bcounts[f"{a}|{b}"] += 1
            n += 1
        bigr_sigs[w] = {k: v / n if n > 0 else 0.0 for k, v in bcounts.items()}

    # Paires
    pairs_lex, pairs_bigr, pairs_dgr = [], [], []
    for i, a in enumerate(proto_works):
        for b in proto_works[i + 1:]:
            d_graph = proto_pairs.get(f"{a}::{b}") or proto_pairs.get(f"{b}::{a}")
            if d_graph is None:
                continue
            if a not in lex_sigs or b not in lex_sigs:
                continue
            pairs_lex.append(1.0 - cosine(lex_sigs[a], lex_sigs[b]))
            pairs_bigr.append(1.0 - cosine(bigr_sigs[a], bigr_sigs[b]))
            pairs_dgr.append(d_graph)

    n_p = len(pairs_dgr)
    r_lex = pearson(pairs_lex, pairs_dgr)
    r_bigr = pearson(pairs_bigr, pairs_dgr)
    p_lex = perm_test_r2(pairs_lex, pairs_dgr)
    p_bigr = perm_test_r2(pairs_bigr, pairs_dgr)
    pw = power_estimate(n_p)

    summary = {
        "n_works_eligible": len(lex_sigs),
        "n_pairs": n_p,
        "lex_R2": round(r_lex ** 2, 4),
        "lex_pearson_r": round(r_lex, 4),
        "lex_p_perm": round(p_lex, 4),
        "bigram_R2": round(r_bigr ** 2, 4),
        "bigram_pearson_r": round(r_bigr, 4),
        "bigram_p_perm": round(p_bigr, 4),
        "power": pw,
        "verdict": (
            "REJET H0 (signal robuste détecté)" if (p_lex < 0.05 or p_bigr < 0.05)
            else "INDÉTERMINÉ tendanciellement positif" if (r_lex > 0.20 or r_bigr > 0.20)
            else "INDÉTERMINÉ"
        ),
    }
    payload = {
        "version": "v172",
        "step": "§172 — extension corpus +8 œuvres + refit",
        "summary": summary,
        "acquisition": acq_summary,
        "lex_signatures": lex_sigs,
    }
    (RES_DIR / "nipada_v172_revalidation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== VERDICT §172 ===")
    print(f"Œuvres éligibles : {summary['n_works_eligible']}  Paires : {n_p}")
    print(f"  LEX     R²={summary['lex_R2']:.4f}  r={r_lex:+.4f}  p_perm={p_lex:.4f}")
    print(f"  BIGRAM  R²={summary['bigram_R2']:.4f}  r={r_bigr:+.4f}  p_perm={p_bigr:.4f}")
    if pw:
        print(f"  Puissance courante = {pw['current_power']}  n requis = {pw['n_required_pow_0.80']}")
    print(f"  VERDICT : {summary['verdict']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""§178 — Extension hors-occidentale du corpus NIPADA.

Ajoute 6 œuvres non-européennes (Confucius, Laozi, Dhammapada, Bhagavad-Gita,
Gospel of Buddha, Koran) pour réduire le biais eurocentrique du graphe v5.
Construit graphe v6 et revalide LEX/BIGRAM.

Usage:
    .venv/bin/python scripts/nipada_extension_v178.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
SCRIPTS = ROOT / "scripts"
LEX_PATH = SCRIPTS / "nipada_v14_multiling_v145.py"

UA = "PaniniResearch/1.0 (academic; +https://github.com/stephanedenis/Panini)"


def load_lex():
    spec = importlib.util.spec_from_file_location("nipada_v145", LEX_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


LEX = load_lex()


# ───────────────────────── 1. Acquisition ─────────────────────────

WORKS_NEW = [
    {
        "id": "confucius_analects_en",
        "gid": 3330,
        "title": "The Analects of Confucius",
        "author": "Confucius",
        "translator": "James Legge",
        "lang": "eng",
        "tradition": "chinese_classics",
        "edition": "Legge 1893 — Project Gutenberg #3330",
    },
    {
        "id": "laozi_taoteching_en",
        "gid": 216,
        "title": "The Tao Teh King",
        "author": "Laozi",
        "translator": "James Legge",
        "lang": "eng",
        "tradition": "daoism",
        "edition": "Legge 1891 — Project Gutenberg #216",
    },
    {
        "id": "dhammapada_muller_en",
        "gid": 2017,
        "title": "Dhammapada",
        "author": "Buddhist canon (Pali)",
        "translator": "Friedrich Max Müller",
        "lang": "eng",
        "tradition": "buddhism_theravada",
        "edition": "Müller 1881 — Project Gutenberg #2017",
    },
    {
        "id": "bhagavad_gita_arnold_en",
        "gid": 2388,
        "title": "The Song Celestial; Or, Bhagavad-Gîtâ",
        "author": "Vyasa (attributed)",
        "translator": "Edwin Arnold",
        "lang": "eng",
        "tradition": "hinduism_smriti",
        "edition": "Arnold 1885 — Project Gutenberg #2388",
    },
    {
        "id": "carus_gospel_buddha_en",
        "gid": 35895,
        "title": "The Gospel of Buddha",
        "author": "Paul Carus",
        "translator": None,
        "lang": "eng",
        "tradition": "buddhism_modernist",
        "edition": "Carus 1894 — Project Gutenberg #35895",
    },
    {
        "id": "koran_rodwell_en",
        "gid": 3434,
        "title": "The Koran (Al-Qur'an)",
        "author": "Quranic canon",
        "translator": "John Medows Rodwell",
        "lang": "eng",
        "tradition": "islamic_canon",
        "edition": "Rodwell 1861 — Project Gutenberg #3434",
    },
]


def fetch_gutenberg(gid: int) -> tuple[str, str]:
    url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return raw, url


def strip_gutenberg_boilerplate(text: str) -> str:
    start = re.search(r"\*\*\* START OF (?:THE |THIS )?PROJECT GUTENBERG[^*]+\*\*\*", text)
    end = re.search(r"\*\*\* END OF (?:THE |THIS )?PROJECT GUTENBERG[^*]+\*\*\*", text)
    if start:
        text = text[start.end():]
    if end:
        text = text[:end.start()]
    return text.strip()


def acquire_all() -> list[dict]:
    acquired = []
    for w in WORKS_NEW:
        wdir = CORPUS_DIR / w["id"]
        wdir.mkdir(parents=True, exist_ok=True)
        raw_path = wdir / "raw_text.txt"
        prov_path = wdir / "PROVENANCE.json"

        if raw_path.exists() and prov_path.exists():
            raw = raw_path.read_text(encoding="utf-8", errors="replace")
            prov = json.loads(prov_path.read_text())
            print(f"  ↻ {w['id']} (cache, {len(raw):,} chars)")
        else:
            print(f"  ↓ {w['id']} #{w['gid']} ...", end=" ", flush=True)
            raw_full, url = fetch_gutenberg(w["gid"])
            raw = strip_gutenberg_boilerplate(raw_full)
            sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            raw_path.write_text(raw, encoding="utf-8")
            prov = {
                "work_id": w["id"],
                "title": w["title"],
                "author": w["author"],
                "translator": w["translator"],
                "language": w["lang"],
                "tradition": w["tradition"],
                "edition": w["edition"],
                "source_url": url,
                "sha256": sha,
                "char_count": len(raw),
                "retrieval_date_utc": datetime.now(timezone.utc).isoformat(),
            }
            prov_path.write_text(json.dumps(prov, ensure_ascii=False, indent=2))
            print(f"{len(raw):,} chars")
            time.sleep(1.0)
        acquired.append({**w, "text": raw, "provenance": prov})
    return acquired


# ───────────────────────── 2. Fragmentation ─────────────────────────

def fragment(text: str, target_chars: int = 1800) -> list[str]:
    paras = re.split(r"\n\s*\n", text)
    frags, buf = [], []
    cur = 0
    for p in paras:
        p = p.strip()
        if not p:
            continue
        buf.append(p)
        cur += len(p)
        if cur >= target_chars:
            frags.append("\n\n".join(buf))
            buf, cur = [], 0
    if buf:
        frags.append("\n\n".join(buf))
    return [f for f in frags if len(f) >= 400]


def write_fragments(work: dict) -> int:
    wdir = CORPUS_DIR / work["id"]
    frags_path = wdir / "fragments.jsonl"
    if frags_path.exists():
        n = sum(1 for _ in frags_path.open("r", encoding="utf-8"))
        return n
    frags = fragment(work["text"])
    with frags_path.open("w", encoding="utf-8") as fh:
        for i, ftext in enumerate(frags, 1):
            rec = {
                "fragment_id": f"{work['id']}_f{i:04d}",
                "text": ftext,
                "raw_text": ftext,
                "frag_id": f"{work['id']}_f{i:04d}",
                "lang": work["lang"],
                "language": work["lang"],
                "work_id": work["id"],
                "tradition": work["tradition"],
                "char_count": len(ftext),
            }
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(frags)


# ───────────────────────── 3. Signature & distances ─────────────────────────

def freq_signature(text: str, lang: str) -> dict[str, float]:
    """LEX[atom][lang] = list of terms."""
    text_low = text.lower()
    counts = {}
    total = 0
    for atom, lang_dict in LEX.items():
        terms = lang_dict.get(lang, [])
        if not terms:
            continue
        c = 0
        for t in terms:
            c += len(re.findall(r"\b" + re.escape(t.lower()) + r"\b", text_low))
        counts[atom] = c
        total += c
    if total == 0:
        return {}
    return {a: c / total for a, c in counts.items()}


def cosine(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def pearson(xs: list[float], ys: list[float]) -> float:
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
    ys_list = list(ys)
    for _ in range(n_iter):
        rnd.shuffle(ys_list)
        if abs(pearson(xs, ys_list)) >= obs:
            ge += 1
    return (ge + 1) / (n_iter + 1)


# ───────────────────────── 4. Charge graphe v5 + extension v6 ─────────────────────────

def load_graph_v5():
    p = RES_DIR / "nipada_v176_graph_v5.json"
    return json.loads(p.read_text())


def build_graph_v6(g5: dict) -> dict:
    """Etend v5 avec les 6 nouvelles œuvres + arêtes vers leurs auteurs/traditions.

    Schéma v5: nodes = dict {id: {kind,...}}, edges = list [{src,tgt,weight,channel},...]
    """
    nodes = dict(g5["nodes"])
    edges = list(g5["edges"])

    # Nouveaux pivots auteurs / écoles si absents
    pivots_new = {
        "confucius": {"kind": "philosopher_proto", "tradition_label": "CHINESE_CLASSICS"},
        "laozi": {"kind": "philosopher_proto", "tradition_label": "DAOISM"},
        "buddha": {"kind": "philosopher_proto", "tradition_label": "BUDDHISM"},
        "vyasa": {"kind": "philosopher_proto", "tradition_label": "HINDUISM"},
        "muhammad": {"kind": "religious_figure", "tradition_label": "ISLAMIC"},
        "carus": {"kind": "philosopher_modern", "tradition_label": "BUDDHISM_MODERNIST"},
    }
    for p, meta in pivots_new.items():
        if p not in nodes:
            nodes[p] = meta

    # Translators-pivots
    trans_new = ["legge_translator", "muller_translator", "arnold_translator", "rodwell_translator"]
    for t in trans_new:
        if t not in nodes:
            nodes[t] = {"kind": "translator", "tradition_label": "ORIENTALIST_19C"}

    # Nouvelles œuvres comme nodes
    new_works_nodes = {
        "confucius_analects_en":   {"kind": "proto_text_work", "author": "Confucius", "language_original": "lzh", "tradition_label": "CHINESE_CLASSICS"},
        "laozi_taoteching_en":     {"kind": "proto_text_work", "author": "Laozi", "language_original": "lzh", "tradition_label": "DAOISM"},
        "dhammapada_muller_en":    {"kind": "proto_text_work", "author": "Buddhist canon", "language_original": "pli", "tradition_label": "BUDDHISM"},
        "bhagavad_gita_arnold_en": {"kind": "proto_text_work", "author": "Vyasa", "language_original": "san", "tradition_label": "HINDUISM"},
        "carus_gospel_buddha_en":  {"kind": "proto_text_work", "author": "Paul Carus", "language_original": "eng", "tradition_label": "BUDDHISM_MODERNIST"},
        "koran_rodwell_en":        {"kind": "proto_text_work", "author": "Quranic canon", "language_original": "ara", "tradition_label": "ISLAMIC"},
    }
    for k, v in new_works_nodes.items():
        if k not in nodes:
            nodes[k] = v

    works_edges = [
        ("confucius_analects_en", "confucius", "auteur ⟶ œuvre (compilation par disciples)", 0.8),
        ("confucius_analects_en", "legge_translator", "traduction Legge 1893", 0.65),
        ("laozi_taoteching_en", "laozi", "auteur attribué (traditionnellement)", 0.7),
        ("laozi_taoteching_en", "legge_translator", "traduction Legge 1891", 0.65),
        ("dhammapada_muller_en", "buddha", "tradition canonique pali (parole rapportée)", 0.6),
        ("dhammapada_muller_en", "muller_translator", "traduction Müller 1881", 0.65),
        ("bhagavad_gita_arnold_en", "vyasa", "auteur mythique (Mahabharata)", 0.5),
        ("bhagavad_gita_arnold_en", "arnold_translator", "traduction Arnold 1885", 0.65),
        ("carus_gospel_buddha_en", "carus", "auteur compilateur", 0.8),
        ("carus_gospel_buddha_en", "buddha", "synthèse de sources canoniques", 0.4),
        ("koran_rodwell_en", "muhammad", "tradition prophétique (canon)", 0.6),
        ("koran_rodwell_en", "rodwell_translator", "traduction Rodwell 1861", 0.65),
    ]
    for src, tgt, ch, w in works_edges:
        edges.append({"src": src, "tgt": tgt, "weight": w, "channel": ch})

    # Liens transversaux documentés
    cross_edges = [
        ("laozi", "zhuangzi", "école taoïste — Zhuangzi développe Laozi", 0.7),
        ("confucius", "mencius", "école confucéenne — Mencius commente Confucius", 0.7),
        ("confucius", "han_feizi", "école légiste critique du confucianisme", 0.4),
        ("schopenhauer", "buddha", "Schopenhauer lit les Upaniṣads et le bouddhisme", 0.4),
        ("schopenhauer", "vyasa", "Schopenhauer cite la Bhagavad-Gîtâ", 0.4),
        ("nietzsche", "buddha", "Nietzsche, Antichrist §20-23 (Buddha vs. christianisme)", 0.4),
        ("voltaire", "confucius", "Voltaire admire Confucius (Dictionnaire philosophique)", 0.35),
        ("hume", "confucius", "Hume mentionne le confucianisme (Of Superstition)", 0.3),
        ("muhammad", "voltaire", "Voltaire écrit Mahomet — réception critique", 0.35),
        ("ingersoll", "muhammad", "Ingersoll critique l'islam comme le christianisme", 0.35),
    ]
    for src, tgt, ch, w in cross_edges:
        if src in nodes and tgt in nodes:
            edges.append({"src": src, "tgt": tgt, "weight": w, "channel": ch})

    # Suppression doublons (paire non-orientée par (src,tgt))
    seen = set()
    uniq = []
    for e in edges:
        if "src" not in e or "tgt" not in e:
            continue
        a, b = e["src"], e["tgt"]
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(e)

    return {"nodes": nodes, "edges": uniq, "version": "v6"}


# ───────────────────────── 5. Floyd-Warshall ─────────────────────────

def classify_channel(ch: str) -> str:
    s = ch.lower()
    if "traduction" in s or "translation" in s or "transl" in s:
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "heritage", "héritage", "transmission",
        "lit ", "connaît", "connais", "tradition", "comparat", "scepticisme",
        "lecteur", "ascendant", "ami ", "post-", "même transmission",
        "écho", "reçu", "même école", "succession", "admire", "mentionne",
        "réception", "critique", "synthèse", "héritage critique",
    ]):
        return "indirect"
    return "direct"


def floyd_warshall(nodes, edges, weight_map):
    """nodes: dict {id: meta}; edges: list of {src,tgt,weight,channel}."""
    node_ids = list(nodes.keys()) if isinstance(nodes, dict) else list(nodes)
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
        w = weight_map[cat]
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


# ───────────────────────── 6. Pipeline principal ─────────────────────────

def pair_key(a, b):
    return f"{min(a,b)}::{max(a,b)}"


def main():
    print("=== §178 — Extension hors-occidentale ===\n")
    print("Acquisition Gutenberg :")
    works = acquire_all()

    print("\nFragmentation :")
    n_frags_total = 0
    for w in works:
        n = write_fragments(w)
        n_frags_total += n
        print(f"  {w['id']}: {n} fragments")

    print(f"\nTotal nouveaux fragments : {n_frags_total}")

    # Charger graphe v5 et étendre
    g5 = load_graph_v5()
    print(f"\nGraphe v5 : {len(g5['nodes'])} nodes, {len(g5['edges'])} edges")
    g6 = build_graph_v6(g5)
    print(f"Graphe v6 : {len(g6['nodes'])} nodes, {len(g6['edges'])} edges")
    g6_path = RES_DIR / "nipada_v178_graph_v6.json"
    g6_path.write_text(json.dumps(g6, ensure_ascii=False, indent=2))
    print(f"  → {g6_path.relative_to(ROOT)}")

    # Charger TOUS les fragments du corpus
    print("\nChargement signatures fragments (corpus complet) :")
    work_signatures = {}  # work_id → {atom: freq moyen}
    work_traditions = {}
    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        frags_path = wdir / "fragments.jsonl"
        prov_path = wdir / "PROVENANCE.json"
        if not frags_path.exists() or not prov_path.exists():
            continue
        prov = json.loads(prov_path.read_text())
        wid = prov.get("work_id", wdir.name)
        sigs = []
        with frags_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                lang = rec.get("language") or rec.get("lang") or prov.get("language", "eng")
                # normaliser 2-letter → 3-letter
                lang_map = {"en": "eng", "fr": "fra", "de": "deu", "la": "lat", "el": "grc", "ar": "ara", "zh": "lzh", "sa": "san"}
                lang = lang_map.get(lang, lang)
                txt = rec.get("text") or rec.get("raw_text", "")
                sig = freq_signature(txt, lang)
                if sig:
                    sigs.append(sig)
        if sigs:
            avg = {}
            for s in sigs:
                for k, v in s.items():
                    avg[k] = avg.get(k, 0.0) + v
            for k in avg:
                avg[k] /= len(sigs)
            work_signatures[wid] = avg
            work_traditions[wid] = prov.get("tradition", "unknown")

    print(f"  {len(work_signatures)} œuvres avec signatures non-vides")

    # Floyd-Warshall avec poids calibrés §177
    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    D, idx = floyd_warshall(g6["nodes"], g6["edges"], weight_map)

    # Calculer paires connectées entre œuvres ayant signature
    work_ids = [w for w in work_signatures.keys() if w in idx]
    print(f"  {len(work_ids)} œuvres présentes dans graphe v6")

    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_graph = D[idx[a]][idx[b]]
            if d_graph == float("inf"):
                continue
            sim = cosine(work_signatures[a], work_signatures[b])
            d_lex = 1.0 - sim
            pairs.append({
                "a": a, "b": b,
                "d_graph": d_graph,
                "d_lex": d_lex,
                "trad_a": work_traditions.get(a, "?"),
                "trad_b": work_traditions.get(b, "?"),
                "same_trad": work_traditions.get(a) == work_traditions.get(b),
            })

    print(f"\n  {len(pairs)} paires connectées (sur {len(work_ids)*(len(work_ids)-1)//2} possibles)")

    # Statistiques globales
    xs = [p["d_graph"] for p in pairs]
    ys = [p["d_lex"] for p in pairs]
    r = pearson(xs, ys)
    p = perm_test(xs, ys)
    R2 = r * r
    print(f"\n=== §178 GLOBAL  n={len(pairs)} ===")
    print(f"  r = {r:+.4f}   R² = {R2:.4f}   p_perm = {p:.4f}")

    # Sous-groupes
    inter = [p for p in pairs if not p["same_trad"]]
    intra = [p for p in pairs if p["same_trad"]]
    if inter:
        xi = [p["d_graph"] for p in inter]
        yi = [p["d_lex"] for p in inter]
        ri = pearson(xi, yi)
        pi = perm_test(xi, yi)
        print(f"  INTER-trad n={len(inter)} : r={ri:+.4f} R²={ri*ri:.4f} p={pi:.4f}")
    if intra:
        xa = [p["d_graph"] for p in intra]
        ya = [p["d_lex"] for p in intra]
        ra = pearson(xa, ya)
        pa = perm_test(xa, ya)
        print(f"  INTRA-trad n={len(intra)} : r={ra:+.4f} R²={ra*ra:.4f} p={pa:.4f}")

    # Sous-corpus hors-occidental
    nonwest_trads = {
        "chinese_classics", "daoism", "buddhism_theravada",
        "hinduism_smriti", "buddhism_modernist", "islamic_canon",
        "chinese_critic", "chinese_classical", "chinese_legalist",
    }
    nw_ids = {w for w, t in work_traditions.items() if t in nonwest_trads}
    nw_pairs = [p for p in pairs if p["a"] in nw_ids or p["b"] in nw_ids]
    nw_only = [p for p in pairs if p["a"] in nw_ids and p["b"] in nw_ids]

    print(f"\n=== §178 SOUS-CORPUS HORS-OCCIDENT ===")
    print(f"  œuvres non-occidentales : {len(nw_ids)}")
    print(f"  paires impliquant ≥1 non-occidentale : {len(nw_pairs)}")
    print(f"  paires NW×NW exclusives : {len(nw_only)}")
    if len(nw_pairs) >= 5:
        xp = [p["d_graph"] for p in nw_pairs]
        yp = [p["d_lex"] for p in nw_pairs]
        rp = pearson(xp, yp)
        pp = perm_test(xp, yp)
        print(f"  ≥1 NW   : r={rp:+.4f} R²={rp*rp:.4f} p={pp:.4f}")
    if len(nw_only) >= 5:
        xo = [p["d_graph"] for p in nw_only]
        yo = [p["d_lex"] for p in nw_only]
        ro = pearson(xo, yo)
        po = perm_test(xo, yo)
        print(f"  NW×NW   : r={ro:+.4f} R²={ro*ro:.4f} p={po:.4f}")

    # Output JSON
    out = {
        "version": "v178",
        "n_works": len(work_ids),
        "n_pairs_connected": len(pairs),
        "n_works_nonwest": len(nw_ids),
        "n_pairs_nonwest_inclusive": len(nw_pairs),
        "n_pairs_nonwest_exclusive": len(nw_only),
        "weight_map": weight_map,
        "global": {"n": len(pairs), "r": r, "R2": R2, "p_perm": p},
        "inter": {"n": len(inter), "r": pearson([p["d_graph"] for p in inter], [p["d_lex"] for p in inter]) if inter else None},
        "intra": {"n": len(intra)},
        "nonwest_inclusive": {"n": len(nw_pairs)},
        "nonwest_exclusive": {"n": len(nw_only)},
        "graph_v6": {"nodes": len(g6["nodes"]), "edges": len(g6["edges"])},
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    out_path = RES_DIR / "nipada_v178_extension_nonwest.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

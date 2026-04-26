#!/usr/bin/env python3
"""§182 — Élargissement corpus NW pour résoudre puissance statistique.

§181 a révélé que la limite NW×NW (R²~0) vient probablement de la TAILLE
du sous-corpus (6 œuvres = 15 paires) plutôt que de V14 ou de la méthode.

§182 :
  1. Annoter Mozi/Han Feizi avec tradition explicite (chinois, déjà au corpus)
  2. Acquérir 4 œuvres orientales supplémentaires Gutenberg
  3. Construire graphe v8 + Floyd-Warshall + revalidation
  4. Test diagnostic critique : signal NW×NW émerge-t-il avec n>>15 ?
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

USER_AGENT = "PaniniResearch/1.0 (academic; +https://github.com/stephanedenis/Panini)"


# ────────────── Acquisition ──────────────

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def gutenberg_clean(raw: str) -> str:
    """Strip Gutenberg header/footer."""
    start_pat = re.compile(r"\*\*\*\s*START OF (THE|THIS).*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pat = re.compile(r"\*\*\*\s*END OF (THE|THIS).*?\*\*\*", re.IGNORECASE | re.DOTALL)
    m1 = start_pat.search(raw)
    m2 = end_pat.search(raw)
    if m1:
        raw = raw[m1.end():]
    if m2:
        raw = raw[:m2.start()]
    return raw.strip()


def fragmentize(text: str, target_chars: int = 1200) -> list[str]:
    """Découpe en fragments de ~target_chars sur frontières paragraphe."""
    paras = re.split(r"\n\s*\n", text)
    frags = []
    buf = ""
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(buf) + len(p) + 2 > target_chars and buf:
            frags.append(buf)
            buf = p
        else:
            buf = (buf + "\n\n" + p) if buf else p
    if buf:
        frags.append(buf)
    return [f for f in frags if len(f) >= 200]


# Œuvres orientales additionnelles à acquérir
NEW_WORKS = [
    {
        "work_id": "khayyam_rubaiyat_fitzgerald_en",
        "gutenberg_id": 246,
        "url": "https://www.gutenberg.org/cache/epub/246/pg246.txt",
        "edition": "Edward FitzGerald translation, 5th ed. (1889)",
        "original_language": "fa",
        "text_language": "en",
        "tradition": "islamic_skeptic",
        "completeness": "Rubaiyat complets (101 quatrains, 5e éd.)",
    },
    {
        "work_id": "zhuangzi_giles_en",
        "gutenberg_id": 9774,
        "url": "https://www.gutenberg.org/cache/epub/9774/pg9774.txt",
        "edition": "Herbert A. Giles, 'Chuang Tzŭ: Mystic, Moralist, and Social Reformer' (1889)",
        "original_language": "lzh",
        "text_language": "en",
        "tradition": "daoism",
        "completeness": "Chuang Tzŭ traduit sélections importantes",
    },
    {
        "work_id": "upanishads_muller_en",
        "gutenberg_id": 17369,
        "url": "https://www.gutenberg.org/cache/epub/17369/pg17369.txt",
        "edition": "Max Müller, 'The Upanishads' (Sacred Books of the East vol. 1)",
        "original_language": "san",
        "text_language": "en",
        "tradition": "hinduism_shruti",
        "completeness": "Chāndogya, Talavakāra, Aitareya, Kauṣītaki, Vājasaneyi",
    },
    {
        "work_id": "mencius_legge_en",
        "gutenberg_id": 3330,  # Chinese Classics vol cited (différent du #3330 Confucius? vérifions)
        "url": "https://www.gutenberg.org/cache/epub/3330/pg3330.txt",
        "edition": "Legge - need verification (already used for confucius)",
        "skip": True,  # already covered
        "original_language": "lzh",
        "text_language": "en",
        "tradition": "chinese_classical",
        "completeness": "n/a",
    },
]


def acquire(work_meta: dict) -> bool:
    """Télécharge et fragmente une œuvre. Retourne True si succès."""
    if work_meta.get("skip"):
        return False
    wid = work_meta["work_id"]
    wdir = CORPUS_DIR / wid
    if wdir.exists() and (wdir / "fragments.jsonl").exists():
        print(f"  ⊙ {wid} (déjà présent)")
        return True
    wdir.mkdir(parents=True, exist_ok=True)
    print(f"  ↓ {wid} ({work_meta['url']})")
    try:
        raw = fetch(work_meta["url"]).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    ❌ {e}")
        return False
    cleaned = gutenberg_clean(raw)
    sha = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
    (wdir / "raw_text.txt").write_text(cleaned, encoding="utf-8")
    frags = fragmentize(cleaned)
    with (wdir / "fragments.jsonl").open("w", encoding="utf-8") as fh:
        for i, t in enumerate(frags):
            fh.write(json.dumps({"frag_id": i, "text": t}, ensure_ascii=False) + "\n")
    prov = {
        "work_id": wid,
        "source_type": "Project Gutenberg",
        "source_url": work_meta["url"],
        "gutenberg_id": work_meta["gutenberg_id"],
        "edition": work_meta["edition"],
        "transcriber": "Project Gutenberg / Distributed Proofreaders",
        "original_language": work_meta["original_language"],
        "text_language": work_meta["text_language"],
        "tradition": work_meta["tradition"],
        "license": "Public Domain (PG)",
        "retrieval_date_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": sha,
        "byte_length": len(cleaned.encode("utf-8")),
        "fragment_count": len(frags),
        "completeness": work_meta["completeness"],
    }
    (wdir / "PROVENANCE.json").write_text(json.dumps(prov, ensure_ascii=False, indent=2))
    print(f"    ✓ {len(frags)} fragments, sha {sha[:12]}")
    return True


# ────────────── Annotation Mozi / Han Feizi ──────────────

def annotate_existing():
    """Ajoute tradition explicite à Mozi (mohist) et Han Feizi (legalist)."""
    updates = {
        "mozi_selections": "chinese_mohist",
        "han_feizi_selections": "chinese_legalist",
    }
    for wid, trad in updates.items():
        p = CORPUS_DIR / wid / "PROVENANCE.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        if d.get("tradition") in (None, "", "unknown"):
            d["tradition"] = trad
            d["annotation_date_utc"] = datetime.now(timezone.utc).isoformat()
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
            print(f"  ✎ {wid}: tradition='{trad}'")


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
    if any(k in s for k in ["traduction", "translation"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "lit ", "connaît",
        "tradition", "comparat", "scepticisme", "lecteur", "ascendant",
        "post-", "écho", "reçu", "même école", "succession", "admire",
        "mentionne", "réception", "critique", "synthèse", "commentaire",
        "compile", "milieu",
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


# ────────────── Build graphe v8 ──────────────

def build_graph_v8(g7: dict, new_works: list) -> dict:
    nodes = dict(g7["nodes"])
    edges = list(g7["edges"])

    # Ajout des nouveaux nœuds
    for w in new_works:
        if w.get("skip"):
            continue
        wid = w["work_id"]
        if wid not in nodes:
            nodes[wid] = {
                "label": wid,
                "lang": w["text_language"],
                "tradition": w["tradition"],
                "added_in": "v8_§182",
            }

    # Arêtes additionnelles philologiquement documentées
    new_edges = [
        # Khayyam (Persan, ~1100) — sceptique épicurien
        {"src": "khayyam_rubaiyat_fitzgerald_en", "tgt": "epicurus_quotes",
         "channel": "indirect — héritage hellénistique via Bagdad (école aristotélicienne arabe), thèmes hédonistes/sceptiques",
         "weight_hint": "indirect"},
        {"src": "khayyam_rubaiyat_fitzgerald_en", "tgt": "lucretius_drn",
         "channel": "indirect — parallèle thématique vanité/temps/mort, transmission via FitzGerald (lecteur de Lucrèce)",
         "weight_hint": "indirect"},
        {"src": "voltaire_candide", "tgt": "khayyam_rubaiyat_fitzgerald_en",
         "channel": "indirect — Voltaire connaît Khayyam via traductions latines/françaises, scepticisme religieux partagé",
         "weight_hint": "indirect"},

        # Zhuangzi (Chine, ~3e s. av.) — école taoïste
        {"src": "zhuangzi_giles_en", "tgt": "laozi_taoteching_en",
         "channel": "direct — Zhuangzi disciple de la tradition Laozi (deux pôles du Daodejing)",
         "weight_hint": "direct"},
        {"src": "zhuangzi_giles_en", "tgt": "confucius_analects_en",
         "channel": "indirect — critique satirique du confucianisme (chapitres internes)",
         "weight_hint": "indirect"},
        {"src": "zhuangzi_giles_en", "tgt": "wang_chong",
         "channel": "indirect — Wang Chong influencé par scepticisme taoïste de Zhuangzi",
         "weight_hint": "indirect"},

        # Upanishads (Inde, ~800-500 av.) — Vedanta foundationnal
        {"src": "upanishads_muller_en", "tgt": "bhagavad_gita_arnold_en",
         "channel": "direct — Bhagavad-Gîtâ cite/synthétise Upanishads (chap. 8, 13, 15)",
         "weight_hint": "direct"},
        {"src": "upanishads_muller_en", "tgt": "śaṅkara",
         "channel": "direct — Śaṅkara écrit Bhāṣya commentaire des Upanishads",
         "weight_hint": "direct"},
        {"src": "upanishads_muller_en", "tgt": "schopenhauer_pessimism",
         "channel": "indirect — Schopenhauer considère Upanishads (Anquetil-Duperron) comme révélation de sa philosophie",
         "weight_hint": "indirect"},
        {"src": "upanishads_muller_en", "tgt": "carus_gospel_buddha_en",
         "channel": "indirect — Müller traduit aussi Dhammapada et inspire orientalisme victorien (Carus)",
         "weight_hint": "indirect"},

        # Annotation Mozi/Han Feizi (déjà nœuds, juste nouvelles arêtes intra-chinoises)
        {"src": "mozi_selections", "tgt": "confucius_analects_en",
         "channel": "indirect — Mozi critique le ritualisme confucéen (école rivale)",
         "weight_hint": "indirect"},
        {"src": "han_feizi_selections", "tgt": "confucius_analects_en",
         "channel": "indirect — Han Fei rejette confucianisme (école Fa-jia)",
         "weight_hint": "indirect"},
        {"src": "han_feizi_selections", "tgt": "mozi_selections",
         "channel": "indirect — Han Fei lit Mozi (scolastique pré-Qin)",
         "weight_hint": "indirect"},
        {"src": "wang_chong", "tgt": "han_feizi_selections",
         "channel": "indirect — Wang Chong écrit Han, fréquente courants Fa-jia",
         "weight_hint": "indirect"},
    ]

    # Filtrer arêtes dont les nœuds existent
    valid = []
    for e in new_edges:
        if e["src"] in nodes and e["tgt"] in nodes:
            valid.append({
                "src": e["src"], "tgt": e["tgt"],
                "channel": e["channel"],
                "added_in": "v8_§182",
            })

    edges.extend(valid)

    return {
        "version": "v8_§182",
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "nodes": nodes,
        "edges": edges,
        "edges_added_in_v8": len(valid),
    }


# ────────────── V14-LEX signature (réutilise §178) ──────────────

def load_v14_lex():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "v14lex", ROOT / "scripts" / "nipada_v14_multiling_v145.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


def freq_signature(text: str, lex, lang: str = "eng") -> dict:
    """LEX[atom][lang] = list of terms. Returns frequency vector by atom."""
    txt_l = text.lower()
    sig = {}
    for atom, langs in lex.items():
        terms = langs.get(lang, []) + langs.get("eng", []) + langs.get("fra", [])
        terms = list(set(terms))
        c = 0
        for t in terms:
            if not t:
                continue
            c += txt_l.count(t.lower())
        sig[atom] = c
    s = sum(sig.values()) or 1
    return {a: v / s for a, v in sig.items()}


def cosine_dict(a: dict, b: dict) -> float:
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


# ────────────── Pipeline §182 ──────────────

def main():
    print("=== §182 — Élargissement corpus NW ===\n")

    # Étape 1
    print("Étape 1 — Annotation Mozi/Han Feizi:")
    annotate_existing()

    # Étape 2 — acquisition
    print("\nÉtape 2 — Acquisition œuvres orientales additionnelles:")
    acquired = []
    for w in NEW_WORKS:
        if acquire(w):
            acquired.append(w)
    print(f"\n  → {len(acquired)} œuvres acquises ou déjà présentes")

    # Étape 3 — graphe v8
    print("\nÉtape 3 — Construction graphe v8:")
    g7 = json.loads((RES_DIR / "nipada_v179_graph_v7.json").read_text())
    g8 = build_graph_v8(g7, acquired)
    n_v7_nodes = len(g7.get("nodes", {}))
    n_v7_edges = len(g7.get("edges", []))
    print(f"  v7 : {n_v7_nodes} nodes, {n_v7_edges} edges")
    print(f"  v8 : {g8['n_nodes']} nodes, {g8['n_edges']} edges (+{g8['edges_added_in_v8']} arêtes)")

    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    D, idx = floyd_warshall(g8["nodes"], g8["edges"], weight_map)

    # Étape 4 — signatures V14-LEX
    print("\nÉtape 4 — Signatures V14-LEX du corpus complet:")
    lex = load_v14_lex()
    work_signatures = {}
    work_traditions = {}
    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        frags_p = wdir / "fragments.jsonl"
        prov_p = wdir / "PROVENANCE.json"
        if not frags_p.exists() or not prov_p.exists():
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", wdir.name)
        text = ""
        with frags_p.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                t = rec.get("text") or rec.get("raw_text", "")
                text += t + "\n"
        if not text.strip():
            continue
        lang = prov.get("text_language", "eng")
        if lang in ("en", "english"):
            lang = "eng"
        elif lang in ("fr", "french"):
            lang = "fra"
        elif lang == "zh":
            lang = "lzh"
        sig = freq_signature(text, lex, lang)
        work_signatures[wid] = sig
        work_traditions[wid] = prov.get("tradition") or "unknown"

    print(f"  {len(work_signatures)} œuvres avec signatures")

    # Étape 5 — paires connectées
    work_ids = [w for w in work_signatures if w in idx]
    print(f"  {len(work_ids)} dans graphe v8")

    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            d_lex = 1.0 - cosine_dict(work_signatures[a], work_signatures[b])
            pairs.append({
                "a": a, "b": b,
                "d_graph": d_g,
                "d_lex": d_lex,
                "trad_a": work_traditions[a],
                "trad_b": work_traditions[b],
                "same_trad": work_traditions[a] == work_traditions[b],
            })

    print(f"  {len(pairs)} paires connectées")

    # Étape 6 — stats
    xs = [p["d_graph"] for p in pairs]
    ys = [p["d_lex"] for p in pairs]
    r = pearson(xs, ys)
    pv = perm_test(xs, ys)
    print(f"\n=== §182 GLOBAL  n={len(pairs)} ===")
    print(f"  r={r:+.4f}  R²={r*r:.4f}  p_perm={pv:.4f}")

    inter = [pp for pp in pairs if not pp["same_trad"]]
    intra = [pp for pp in pairs if pp["same_trad"]]
    if inter:
        ri = pearson([pp["d_graph"] for pp in inter], [pp["d_lex"] for pp in inter])
        pi = perm_test([pp["d_graph"] for pp in inter], [pp["d_lex"] for pp in inter])
        print(f"  INTER n={len(inter)} : r={ri:+.4f} R²={ri*ri:.4f} p={pi:.4f}")
    else:
        ri, pi = 0.0, 1.0
    if intra:
        ra = pearson([pp["d_graph"] for pp in intra], [pp["d_lex"] for pp in intra])
        pa = perm_test([pp["d_graph"] for pp in intra], [pp["d_lex"] for pp in intra])
        print(f"  INTRA n={len(intra)} : r={ra:+.4f} R²={ra*ra:.4f} p={pa:.4f}")
    else:
        ra, pa = 0.0, 1.0

    # Sous-corpus NW (corrigé : inclut maintenant Mozi, Han Feizi, Zhuangzi, Upanishads, Khayyam)
    nw_trads = {
        "chinese_classics", "daoism", "buddhism_theravada",
        "hinduism_smriti", "hinduism_shruti", "buddhism_modernist",
        "islamic_canon", "islamic_skeptic", "chinese_critic",
        "chinese_classical", "chinese_legalist", "chinese_mohist",
    }
    nw_ids = {w for w, t in work_traditions.items() if t in nw_trads}
    nw_only = [pp for pp in pairs if pp["a"] in nw_ids and pp["b"] in nw_ids]

    print(f"\n=== §182 NW×NW EXCLUSIF (test puissance) ===")
    print(f"  œuvres NW : {len(nw_ids)} → paires NW×NW : {len(nw_only)}")
    print(f"  (vs §181 : 6 œuvres, 15 paires)")

    if nw_only:
        ro = pearson([pp["d_graph"] for pp in nw_only], [pp["d_lex"] for pp in nw_only])
        po = perm_test([pp["d_graph"] for pp in nw_only], [pp["d_lex"] for pp in nw_only])
        print(f"  NW×NW V14-LEX : r={ro:+.4f} R²={ro*ro:.4f} p={po:.4f}")
        print(f"  vs §178 : R²=0.0019 p=0.87  (n=15)")
        print(f"  vs §179 : R²=0.0002 p=0.96  (n=15)")
    else:
        ro, po = 0.0, 1.0

    # Verdict
    print(f"\n=== VERDICT §182 ===")
    if po < 0.05 and ro > 0:
        verdict = ("Signal NW×NW émerge avec corpus élargi — "
                   "puissance statistique confirmée comme cause principale")
    elif po < 0.10:
        verdict = "Signal NW×NW marginal — la limite était partiellement la puissance"
    else:
        verdict = ("Signal NW×NW persiste à zéro — la limite n'est PAS la taille du corpus, "
                   "elle est dans le graphe ou dans le concept même de transmission orientale modélisable")
    print(f"  → {verdict}")

    # Output
    out = {
        "version": "v182_corpus_extension",
        "n_works_corpus": len(work_signatures),
        "n_works_graph": len(work_ids),
        "n_pairs": len(pairs),
        "n_works_nw": len(nw_ids),
        "n_pairs_nw_nw": len(nw_only),
        "weight_map": weight_map,
        "global": {"n": len(pairs), "r": r, "R2": r * r, "p_perm": pv},
        "inter": {"n": len(inter), "r": ri, "R2": ri * ri, "p": pi},
        "intra": {"n": len(intra), "r": ra, "R2": ra * ra, "p": pa},
        "nw_exclusive": {"n": len(nw_only), "r": ro, "R2": ro * ro, "p": po},
        "comparison": {
            "v178_nw_nw": {"n": 15, "R2": 0.0019, "p": 0.87},
            "v179_nw_nw": {"n": 15, "R2": 0.0002, "p": 0.96},
            "v181_nw_nw_emb": {"n": 15, "R2": 0.0295, "p": 0.55},
            "v182_nw_nw_lex": {"n": len(nw_only), "R2": ro * ro, "p": po},
        },
        "verdict": verdict,
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    out_path = RES_DIR / "nipada_v182_corpus_extension.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  → {out_path.relative_to(ROOT)}")

    g8_path = RES_DIR / "nipada_v182_graph_v8.json"
    g8_path.write_text(json.dumps(g8, ensure_ascii=False, indent=2))
    print(f"  → {g8_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

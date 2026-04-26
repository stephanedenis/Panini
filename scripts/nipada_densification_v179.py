#!/usr/bin/env python3
"""§179 — Densification intra-orientale du graphe v6 → v7.

Teste si l'enrichissement des arêtes entre œuvres et auteurs orientaux
permet au sous-corpus NW×NW de produire un signal indépendant des ponts
européens.

Ajoute des arêtes philologiquement documentées :
- Carus → Dhammapada (compilation explicite des sources Pali)
- Laozi ↔ Confucius (contemporains, critique mutuelle école taoïste/confucéenne)
- Bhagavad-Gîtâ → Dhammapada (milieu shramana commun, ascétisme indien)
- Mencius → Confucius (école, déjà), Han Feizi (héritage critique)
- Nāgārjuna (nœud nouveau) commentaire de Buddha → Dhammapada
- Śaṅkara (nœud nouveau) commentaire des Upaniṣads → Bhagavad-Gîtâ
- Mu'tazilites (nœud) théologie rationnelle → Koran
- Wang Chong → Confucius (critique skeptique)
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
SCRIPTS = ROOT / "scripts"
LEX_PATH = SCRIPTS / "nipada_v14_multiling_v145.py"


def load_lex():
    spec = importlib.util.spec_from_file_location("v145", LEX_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


LEX = load_lex()


# ────────────── Pipeline réutilisé de v178 ──────────────

def freq_signature(text: str, lang: str) -> dict[str, float]:
    text_low = text.lower()
    counts, total = {}, 0
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


def cosine(a, b):
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
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


# ────────────── Densification §179 ──────────────

def build_graph_v7(g6: dict) -> dict:
    nodes = dict(g6["nodes"])
    edges = list(g6["edges"])

    # Nouveaux pivots (commentateurs, écoles)
    new_pivots = {
        "nagarjuna": {"kind": "philosopher_proto", "tradition_label": "BUDDHISM_MADHYAMAKA",
                      "note": "fondateur Madhyamaka, 2-3e s., commentateur du Bouddha"},
        "sankara": {"kind": "philosopher_proto", "tradition_label": "HINDUISM_ADVAITA",
                    "note": "8e s., commentateur des Upaniṣads et Bhagavad-Gîtâ"},
        "mutazilites": {"kind": "school", "tradition_label": "ISLAMIC_KALAM",
                        "note": "théologie rationaliste 8-10e s. (Abd al-Jabbar, al-Nazzam)"},
        "asharites": {"kind": "school", "tradition_label": "ISLAMIC_KALAM",
                      "note": "théologie ash'arite 10e s., réplique aux Mu'tazilites"},
        "wang_chong": {"kind": "philosopher_proto", "tradition_label": "CHINESE_CRITIC",
                       "note": "Lunheng, 1er s., critique skeptique du confucianisme/divination"},
        "zhuangzi": nodes.get("zhuangzi", {"kind": "philosopher_proto", "tradition_label": "DAOISM"}),
        "shramana": {"kind": "milieu", "tradition_label": "INDIAN_HETERODOX",
                     "note": "ascétisme hétérodoxe pré-bouddhique commun (Cārvāka, Jaïna, bouddhisme)"},
    }
    for k, v in new_pivots.items():
        if k not in nodes:
            nodes[k] = v

    # Arêtes intra-orientales philologiquement documentées
    new_edges = [
        # Bouddhisme : Carus compile explicitement le Dhammapada parmi ses sources
        ("carus_gospel_buddha_en", "dhammapada_muller_en", 0.7,
         "compilation directe : Carus 1894 cite et compile le Dhammapada parmi ses sources"),
        # Nāgārjuna commente Buddha → arête vers Dhammapada
        ("nagarjuna", "buddha", 0.65, "commentaire indirect : Mūlamadhyamakakārikā développe l'enseignement du Bouddha"),
        ("nagarjuna", "dhammapada_muller_en", 0.4, "tradition canonique commune (héritage critique)"),
        # Śaṅkara commente Upaniṣads et Bhagavad-Gîtâ
        ("sankara", "vyasa", 0.5, "commentaire : Bhāṣya sur la Bhagavad-Gîtâ attribuée à Vyāsa"),
        ("sankara", "bhagavad_gita_arnold_en", 0.5, "commentaire direct de la Bhagavad-Gîtâ (advaita)"),
        # Daoisme/Confucianisme : contemporains et critique mutuelle
        ("laozi", "confucius", 0.4,
         "contemporains 6e-5e s. avant J.-C., pôles philosophiques opposés (Sima Qian, Shiji)"),
        ("laozi_taoteching_en", "confucius_analects_en", 0.4,
         "dialogue daoïsme/confucianisme — Zhuangzi développe la critique du Lunyu"),
        ("zhuangzi", "confucius", 0.35, "critique satirique du confucianisme dans Zhuangzi"),
        ("zhuangzi", "laozi", 0.7, "école taoïste — Zhuangzi développe Laozi"),
        # Wang Chong critique skeptique du confucianisme
        ("wang_chong", "confucius", 0.4,
         "critique skeptique : Lunheng 論衡 (Discussions critiques) attaque la divination confucéenne"),
        ("wang_chong", "confucius_analects_en", 0.35, "Wang Chong cite et critique le Lunyu"),
        # Mu'tazilites/Asharites au Coran
        ("mutazilites", "koran_rodwell_en", 0.5,
         "exégèse rationaliste : Abd al-Jabbar interprète le Coran via la raison ('aql)"),
        ("asharites", "koran_rodwell_en", 0.4,
         "exégèse traditionaliste : al-Ash'ari fonde un kalām en réponse aux Mu'tazilites"),
        ("asharites", "mutazilites", 0.5, "héritage critique : ash'arites en débat avec mu'tazilites"),
        # Milieu shramana commun (Bhagavad-Gîtâ ↔ Dhammapada)
        ("shramana", "buddha", 0.4, "milieu hétérodoxe indien (śramaṇa) commun — Cārvāka, Jaïna, bouddhisme"),
        ("shramana", "vyasa", 0.3, "milieu indien commun — la BG répond aux śramaṇas hétérodoxes"),
        ("shramana", "dhammapada_muller_en", 0.4, "tradition ascétique partagée"),
        ("shramana", "bhagavad_gita_arnold_en", 0.3, "réception critique des śramaṇas dans la Gîtâ"),
        # Cross orientaux : transmission Confucius → Mahayana via École de Yan
        ("buddha", "confucius", 0.2,
         "transmission bouddhique vers la Chine au 1er s. — réception confucéenne via Han Ming"),
    ]

    for src, tgt, w, ch in new_edges:
        if src not in nodes:
            nodes[src] = {"kind": "philosopher_proto", "tradition_label": "ORIENTAL_NEW"}
        edges.append({"src": src, "tgt": tgt, "weight": w, "channel": ch})

    # Suppression doublons (paire non-orientée)
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

    return {"nodes": nodes, "edges": uniq, "version": "v7"}


def main():
    print("=== §179 — Densification intra-orientale ===\n")
    g6 = json.loads((RES_DIR / "nipada_v178_graph_v6.json").read_text())
    print(f"Graphe v6 : {len(g6['nodes'])} nodes, {len(g6['edges'])} edges")

    g7 = build_graph_v7(g6)
    print(f"Graphe v7 : {len(g7['nodes'])} nodes, {len(g7['edges'])} edges")
    (RES_DIR / "nipada_v179_graph_v7.json").write_text(json.dumps(g7, ensure_ascii=False, indent=2))

    # Charger signatures fragments (corpus complet — déjà acquis)
    work_signatures = {}
    work_traditions = {}
    lang_map = {"en": "eng", "fr": "fra", "de": "deu", "la": "lat", "el": "grc",
                "ar": "ara", "zh": "lzh", "sa": "san"}

    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        frags = wdir / "fragments.jsonl"
        prov = wdir / "PROVENANCE.json"
        if not frags.exists() or not prov.exists():
            continue
        p = json.loads(prov.read_text())
        wid = p.get("work_id", wdir.name)
        sigs = []
        with frags.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                lang = rec.get("language") or rec.get("lang") or p.get("language", "eng")
                lang = lang_map.get(lang, lang)
                txt = rec.get("text") or rec.get("raw_text", "")
                s = freq_signature(txt, lang)
                if s:
                    sigs.append(s)
        if sigs:
            avg = {}
            for s in sigs:
                for k, v in s.items():
                    avg[k] = avg.get(k, 0.0) + v
            for k in avg:
                avg[k] /= len(sigs)
            work_signatures[wid] = avg
            work_traditions[wid] = p.get("tradition", "unknown")

    # Floyd-Warshall avec poids §177
    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    D, idx = floyd_warshall(g7["nodes"], g7["edges"], weight_map)

    work_ids = [w for w in work_signatures.keys() if w in idx]
    pairs = []
    for i in range(len(work_ids)):
        for j in range(i + 1, len(work_ids)):
            a, b = work_ids[i], work_ids[j]
            d_g = D[idx[a]][idx[b]]
            if d_g == float("inf"):
                continue
            sim = cosine(work_signatures[a], work_signatures[b])
            pairs.append({
                "a": a, "b": b,
                "d_graph": d_g,
                "d_lex": 1.0 - sim,
                "trad_a": work_traditions[a],
                "trad_b": work_traditions[b],
                "same_trad": work_traditions[a] == work_traditions[b],
            })

    print(f"\n  {len(work_ids)} œuvres, {len(pairs)} paires connectées")

    xs = [p["d_graph"] for p in pairs]
    ys = [p["d_lex"] for p in pairs]
    r = pearson(xs, ys)
    p = perm_test(xs, ys)
    print(f"\n=== §179 GLOBAL  n={len(pairs)} ===")
    print(f"  r={r:+.4f}  R²={r*r:.4f}  p_perm={p:.4f}")

    inter = [pp for pp in pairs if not pp["same_trad"]]
    intra = [pp for pp in pairs if pp["same_trad"]]
    if inter:
        ri = pearson([pp["d_graph"] for pp in inter], [pp["d_lex"] for pp in inter])
        pi = perm_test([pp["d_graph"] for pp in inter], [pp["d_lex"] for pp in inter])
        print(f"  INTER n={len(inter)} : r={ri:+.4f} R²={ri*ri:.4f} p={pi:.4f}")
    if intra:
        ra = pearson([pp["d_graph"] for pp in intra], [pp["d_lex"] for pp in intra])
        pa = perm_test([pp["d_graph"] for pp in intra], [pp["d_lex"] for pp in intra])
        print(f"  INTRA n={len(intra)} : r={ra:+.4f} R²={ra*ra:.4f} p={pa:.4f}")

    nw_trads = {
        "chinese_classics", "daoism", "buddhism_theravada",
        "hinduism_smriti", "buddhism_modernist", "islamic_canon",
        "chinese_critic", "chinese_classical", "chinese_legalist",
    }
    nw_ids = {w for w, t in work_traditions.items() if t in nw_trads}
    nw_only = [pp for pp in pairs if pp["a"] in nw_ids and pp["b"] in nw_ids]
    nw_inc = [pp for pp in pairs if pp["a"] in nw_ids or pp["b"] in nw_ids]

    print(f"\n=== §179 SOUS-CORPUS NON-OCCIDENTAL ===")
    print(f"  œuvres NW : {len(nw_ids)}")
    if nw_inc:
        rp = pearson([pp["d_graph"] for pp in nw_inc], [pp["d_lex"] for pp in nw_inc])
        pp1 = perm_test([pp["d_graph"] for pp in nw_inc], [pp["d_lex"] for pp in nw_inc])
        print(f"  ≥1 NW   n={len(nw_inc)} : r={rp:+.4f} R²={rp*rp:.4f} p={pp1:.4f}")
    if nw_only:
        ro = pearson([pp["d_graph"] for pp in nw_only], [pp["d_lex"] for pp in nw_only])
        po = perm_test([pp["d_graph"] for pp in nw_only], [pp["d_lex"] for pp in nw_only])
        print(f"  NW×NW   n={len(nw_only)} : r={ro:+.4f} R²={ro*ro:.4f} p={po:.4f}")
    else:
        ro, po = 0.0, 1.0

    # Comparaison vs §178 (NW×NW p=0.87)
    print(f"\n  §178 NW×NW : R²=0.0019 p=0.87")
    print(f"  §179 NW×NW : R²={ro*ro:.4f} p={po:.4f}")
    delta = ro * ro - 0.0019
    print(f"  Δ R² = {delta:+.4f}")

    out = {
        "version": "v179",
        "n_works": len(work_ids),
        "n_pairs": len(pairs),
        "graph_v7": {"nodes": len(g7["nodes"]), "edges": len(g7["edges"])},
        "weight_map": weight_map,
        "global": {"n": len(pairs), "r": r, "R2": r * r, "p_perm": p},
        "inter": {"n": len(inter)},
        "intra": {"n": len(intra)},
        "nw_inclusive": {"n": len(nw_inc)},
        "nw_exclusive": {"n": len(nw_only), "r": ro, "R2": ro * ro, "p": po},
        "delta_NWxNW_vs_v178": delta,
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    (RES_DIR / "nipada_v179_densification_oriental.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2)
    )
    print(f"\n  → research/nipada/falsification/nipada_v179_*.json")


if __name__ == "__main__":
    main()

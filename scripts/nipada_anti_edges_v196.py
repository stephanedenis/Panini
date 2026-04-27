#!/usr/bin/env python3
"""§196 — H2 Arêtes anti-documentées.

Test discriminant : ajouter 9 arêtes "anti-documentées" (paires historiquement
sans contact direct) au graph v8, comparer aux 9 arêtes documentées de v9.

Si R²(v8 + anti) ≈ R²(v9 documentées), le signal est purement structural.
Si R²(v8 + anti) < R²(v9 documentées), le contenu documentaire compte.

Anti-arêtes choisies (paires sans contact direct attesté avant XIXe s.) :
- Khayyam ↔ Confucius (perse XIe ↔ chinois VIe av. J.-C., aucun pont)
- Lucrèce ↔ Coran (latin Ie av. J.-C. ↔ arabe VIIe, gap >700 ans absence)
- Spinoza ↔ Dhammapada (NL XVIIe ↔ pali Ier, premières trad. occ. fin XIXe)
- Han Feizi ↔ Bhagavad Gita (chinois IIIe av. J.-C. ↔ indien IVe av. J.-C.,
  écoles et langues étrangères, aucun contact attesté)
- Hobbes ↔ Coran (anglais XVIIe, Hobbes ne lit pas l'arabe, pas de contact)
- Voltaire ↔ Han Feizi (français XVIIIe ↔ chinois IIIe av. J.-C., Voltaire
  ne mentionne ni Han Feizi ni légisme)
- Mozi ↔ Upanishads (chinois Ve av. J.-C. ↔ sanskrit, aucun contact attesté)
- Hume ↔ Confucius (Hume ne mentionne pas Confucius dans ses œuvres
  philosophiques principales)
- Marx ↔ Laozi (Marx allemand XIXe, ne cite pas Laozi)

Ces "anti-arêtes" sont ajoutées avec channel="direct" (poids 0.45) pour
maximiser leur effet structural. Si R² monte autant qu'avec les arêtes
documentées, on peut conclure que le gain §190 est purement structural.

Calibration V_OPT.
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

ANTI_EDGES = [
    ("khayyam_rubaiyat_fitzgerald_en", "confucius_analects_en",
     "ANTI: persan XIe ↔ chinois VIe av. J.-C. (aucun contact)"),
    ("lucretius_drn", "koran_rodwell_en",
     "ANTI: latin Ie av. J.-C. ↔ arabe VIIe (gap >700 ans)"),
    ("spinoza_ethica_complete", "dhammapada_muller_en",
     "ANTI: NL XVIIe ↔ pali Ier (1ère trad. occ. fin XIXe)"),
    ("han_feizi_selections", "bhagavad_gita_arnold_en",
     "ANTI: chinois IIIe av. J.-C. ↔ indien (aucun contact)"),
    ("hobbes_leviathan_complete", "koran_rodwell_en",
     "ANTI: Hobbes ne lit pas l'arabe (aucun pont)"),
    ("voltaire_candide", "han_feizi_selections",
     "ANTI: Voltaire ne mentionne pas le légisme"),
    ("mozi_selections", "upanishads_muller_en",
     "ANTI: chinois ↔ sanskrit (aucun contact attesté)"),
    ("hume_enquiry", "confucius_analects_en",
     "ANTI: Hume ne mentionne pas Confucius"),
    ("marx_critique", "laozi_taoteching_en",
     "ANTI: Marx ne cite pas Laozi"),
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
        out[label] = (pearson(xs, ys) ** 2, len(sub))
    return out


def main():
    print("=== §196 — H2 Anti-arêtes (V_OPT) ===\n")

    g8 = json.loads((RES / "nipada_v182_graph_v8.json").read_text())
    g9 = json.loads((RES / "nipada_v189_graph_v9.json").read_text())

    # Signatures
    lex = load_lex()
    sigs = {}
    trads = {}
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
    print(f"Signatures: {len(sigs)}, EAST: {len(east_set)}")

    # Annotations EAST sur g8 nodes
    east_traditions_map = {
        "bhagavad_gita_arnold_en": "hinduism_smriti",
        "carus_gospel_buddha_en": "buddhism_modernist",
        "confucius_analects_en": "chinese_classics",
        "dhammapada_muller_en": "buddhism_theravada",
        "han_feizi_selections": "chinese_legalist",
        "khayyam_rubaiyat_fitzgerald_en": "islamic_skeptic",
        "koran_rodwell_en": "islamic_canon",
        "laozi_taoteching_en": "daoism",
        "mozi_selections": "chinese_mohist",
        "upanishads_muller_en": "hinduism_shruti",
        "zhuangzi_giles_en": "daoism",
    }
    g8_nodes = dict(g8["nodes"])
    for nid, t in east_traditions_map.items():
        if nid in g8_nodes:
            g8_nodes[nid] = {**g8_nodes[nid], "tradition": t}

    # Vérifier que les nodes existent
    print("\nValidation anti-arêtes :")
    valid_anti = []
    for s, t, ev in ANTI_EDGES:
        s_in = s in g8_nodes
        t_in = t in g8_nodes
        s_sig = s in sigs
        t_sig = t in sigs
        status = "✓" if (s_in and t_in and s_sig and t_sig) else "✗"
        print(f"  {status} {s:35s} ↔ {t:35s}")
        if s_in and t_in and s_sig and t_sig:
            valid_anti.append((s, t, ev))

    if len(valid_anti) < len(ANTI_EDGES):
        print(f"\n⚠ Seulement {len(valid_anti)}/{len(ANTI_EDGES)} anti-arêtes valides")
    # Construire v9-anti edges = g8 + valid_anti
    v9_anti = {
        "nodes": g8_nodes,
        "edges": list(g8["edges"]) + [
            {"src": s, "tgt": t, "channel": "direct " + ev,
             "is_anti_edge": True, "added_in": "v196"}
            for s, t, ev in valid_anti
        ],
    }

    # === 3 graphes à comparer ===
    # 1. v8 baseline (g8 + annotations, sans arêtes v189)
    v8_edges = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                for e in g8["edges"]]

    # 2. v9 réel (avec les 9 arêtes documentées)
    v9_edges = [(e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
                for e in g9["edges"]]
    # Note: g9.nodes inclut "mengzi", v8.nodes ne l'a pas
    v9_node_ids = list(g9["nodes"].keys())

    # 3. v9-anti (g8 + 9 anti-arêtes)
    v9_anti_edges = [
        (e["src"], e["tgt"], W_OPT[classify(e.get("channel", ""))])
        for e in v9_anti["edges"]
    ]
    v9_anti_node_ids = list(g8_nodes.keys())

    # v8 ne doit PAS contenir mengzi (cohérent avec g8)
    v8_node_ids = list(g8["nodes"].keys())

    print(f"\nGraph v8 base    : {len(v8_node_ids)} nodes, {len(v8_edges)} edges")
    print(f"Graph v9 docu    : {len(v9_node_ids)} nodes, {len(v9_edges)} edges")
    print(f"Graph v9-anti    : {len(v9_anti_node_ids)} nodes, "
          f"{len(v9_anti_edges)} edges (+{len(valid_anti)} anti)")

    # Calcul R² par graphe
    print("\n=== R² par graphe (V_OPT) ===")
    print(f"{'Strate':<8}{'v8 base':>10}{'v9 docu':>10}{'v9 anti':>10}"
          f"{'Δ docu':>10}{'Δ anti':>10}{'docu−anti':>11}")
    print("-" * 73)

    r_v8 = compute_strata(v8_node_ids, v8_edges, sigs, east_set)
    r_v9 = compute_strata(v9_node_ids, v9_edges, sigs, east_set)
    r_anti = compute_strata(v9_anti_node_ids, v9_anti_edges, sigs, east_set)

    out_compare = {}
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        b8 = r_v8[k][0]
        b9 = r_v9[k][0]
        ba = r_anti[k][0]
        d_doc = b9 - b8
        d_anti = ba - b8
        diff = b9 - ba
        print(f"{k:<8}{b8:>10.4f}{b9:>10.4f}{ba:>10.4f}"
              f"{d_doc:>+10.4f}{d_anti:>+10.4f}{diff:>+11.4f}")
        out_compare[k] = {
            "v8_base": round(b8, 4),
            "v9_documented": round(b9, 4),
            "v9_anti": round(ba, 4),
            "delta_documented": round(d_doc, 4),
            "delta_anti": round(d_anti, 4),
            "documented_minus_anti": round(diff, 4),
            "n_pairs_v9_doc": r_v9[k][1],
            "n_pairs_v9_anti": r_anti[k][1],
        }

    print("\n=== DIAGNOSTIC ===")
    for k in ("GLOBAL", "WEST", "INTER", "NW"):
        c = out_compare[k]
        diff = c["documented_minus_anti"]
        if diff > 0.01:
            verdict = (f"✓ DOCUMENTÉ > ANTI (+{diff:.4f}) — "
                       f"contenu sémantique compte")
        elif diff < -0.01:
            verdict = (f"✗ ANTI > DOCUMENTÉ ({diff:+.4f}) — "
                       f"signal artefactuel")
        else:
            verdict = (f"= équivalent ({diff:+.4f}) — "
                       f"signal essentiellement structural")
        print(f"  {k:<6} : {verdict}")

    out = {
        "version": "0.3.2",
        "iteration": "v196_anti_edges",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "calibration": W_OPT,
        "anti_edges": [
            {"src": s, "tgt": t, "evidence": ev}
            for s, t, ev in valid_anti
        ],
        "n_signatures": len(sigs),
        "n_east_signed": len(east_set),
        "comparison": out_compare,
    }
    p = RES / "nipada_v196_anti_edges.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n  → {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

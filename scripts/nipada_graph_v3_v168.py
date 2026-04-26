#!/usr/bin/env python3
"""
§168 — Graphe d'héritage v3 + extension métadonnées (suite §166-§167).

Ajoute les œuvres nouvellement acquises au corpus PROTO_ATHEIST :
  - spinoza_ethica_complete  (1677, NL/EN, Public Domain Gutenberg)
  - hobbes_leviathan_complete (1651, EN, Public Domain Gutenberg)
  - mozi_selections (-400, lzh, Wikisource)
  - han_feizi_selections (-250, lzh, Wikisource)

Et ajoute les arêtes documentées historiquement :
  hobbes → spinoza               DIRECT (Spinoza lecteur attesté)
  epicurus / lucretius → hobbes  INDIRECT (revival atomiste 17ᵉ s.)
  hobbes → hume                  INDIRECT (tradition empiriste anglaise)
  hobbes → holbach               INDIRECT (matérialisme)
  spinoza → feuerbach            DIRECT (Feuerbach cite Spinoza)
  spinoza → holbach              INDIRECT (panthéisme → matérialisme)
  mozi pivot → mozi_selections   DIRECT (identité auteur)
  han_feizi pivot → han_feizi_selections DIRECT (identité)
  mozi_selections / han_feizi_selections → wang_chong_lunheng
                                  DIRECT (héritage chinois critique)

Output :
  - research/nipada/falsification/nipada_v168_inheritance_graph_v3.json
  - research/nipada/falsification/nipada_v168_metadata_extended.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v168_inheritance_graph_v3.json"
META_OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v168_metadata_extended.json"

V159_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v159_inheritance_graph_v2.json"
V147_META_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v147_metadata.json"
V166_SUMMARY = ROOT / "research" / "nipada" / "falsification" / "nipada_v166_phase_e_iter2.json"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

W_DIRECT = 0.80
W_INDIRECT = 0.35

# Nouveaux PROTO_ATHEIST_NODES (œuvres ajoutées au corpus §166-§167)
NEW_WORKS = {
    "spinoza_ethica_complete": {
        "year": 1677,
        "lang": "eng",
        "tradition_label": "EUR_RATIONALIST_CRITIC",
        "author": "spinoza",
    },
    "hobbes_leviathan_complete": {
        "year": 1651,
        "lang": "eng",
        "tradition_label": "EUR_THEOL_CRITIC",
        "author": "hobbes",
    },
    "mozi_selections": {
        "year": -400,
        "lang": "lzh",
        "tradition_label": "CHINESE_RATIONALIST",
        "author": "mozi",
    },
    "han_feizi_selections": {
        "year": -250,
        "lang": "lzh",
        "tradition_label": "CHINESE_LEGALIST",
        "author": "han_feizi",
    },
}

# Arêtes historiquement documentées
NEW_EDGES = [
    # Hobbes axis
    ("hobbes_leviathan_complete", "spinoza_ethica_complete", W_DIRECT,
     "Spinoza lecteur direct du Leviathan (correspondance avec Oldenburg)"),
    ("epicurus_letters", "hobbes_leviathan_complete", W_INDIRECT,
     "revival atomiste 17ᵉ s. (Hobbes connaît Gassendi)"),
    ("lucretius_drn", "hobbes_leviathan_complete", W_INDIRECT,
     "DRN largement diffusé en Angleterre 17ᵉ s."),
    ("hobbes_leviathan_complete", "hume_dialogues", W_INDIRECT,
     "tradition empiriste / sceptique anglaise"),
    ("hobbes_leviathan_complete", "holbach_systeme", W_INDIRECT,
     "Holbach cite Hobbes parmi les précurseurs"),
    # Spinoza axis
    ("spinoza_ethica_complete", "feuerbach_wesen", W_DIRECT,
     "Feuerbach cite explicitement Spinoza dans Wesen"),
    ("spinoza_ethica_complete", "holbach_systeme", W_INDIRECT,
     "panthéisme → matérialisme français 18ᵉ s."),
    # Identités auteur → corpus
    ("mozi", "mozi_selections", W_DIRECT,
     "identité auteur (Mozi → corpus extrait)"),
    ("han_feizi", "han_feizi_selections", W_DIRECT,
     "identité auteur (Han Feizi → corpus extrait)"),
    # Filiations chinoises sur les nouveaux corpus
    ("mozi_selections", "wang_chong_lunheng", W_DIRECT,
     "Wang Chong cite Mozi explicitement"),
    ("han_feizi_selections", "wang_chong_lunheng", W_DIRECT,
     "héritage légiste anti-superstition"),
    # Croisements
    ("democritus_fragments", "hobbes_leviathan_complete", W_INDIRECT,
     "atomisme antique transmis via Diogène Laërce et Bacon"),
    ("sextus_pyrrho", "hobbes_leviathan_complete", W_INDIRECT,
     "Hobbes lit la doxographie sceptique"),
]


def _build_adjacency(edges: list) -> dict:
    adj: dict = {}
    for src, tgt, w, ch in edges:
        adj.setdefault(src, {})
        if tgt in adj[src]:
            if w > adj[src][tgt]["weight"]:
                adj[src][tgt] = {"weight": w, "channel": ch}
        else:
            adj[src][tgt] = {"weight": w, "channel": ch}
    return adj


def shortest_paths(adj: dict, all_nodes: list[str]) -> dict[tuple[str, str], float]:
    INF = math.inf
    n = len(all_nodes)
    idx = {nid: i for i, nid in enumerate(all_nodes)}
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for src, neigh in adj.items():
        if src not in idx:
            continue
        for tgt, info in neigh.items():
            if tgt not in idx:
                continue
            cost = -math.log(info["weight"])
            i, j = idx[src], idx[tgt]
            if cost < dist[i][j]:
                dist[i][j] = cost
            if cost < dist[j][i]:
                dist[j][i] = cost
    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    out = {}
    for i, a in enumerate(all_nodes):
        for j, b in enumerate(all_nodes):
            if i < j:
                out[(a, b)] = dist[i][j]
    return out


def count_fragments(work_id: str) -> int:
    p = CORPUS_DIR / work_id / "fragments.jsonl"
    if not p.exists():
        return 0
    return sum(1 for _ in p.open(encoding="utf-8"))


def main() -> None:
    v159 = json.loads(V159_PATH.read_text(encoding="utf-8"))
    v147_meta = json.loads(V147_META_PATH.read_text(encoding="utf-8"))
    v166 = json.loads(V166_SUMMARY.read_text(encoding="utf-8"))

    # Construire la liste complète des PROTO_ATHEIST_NODES
    proto_nodes_v3 = list(v159["proto_pair_distances"].keys())
    # Extraire les nœuds uniques
    base_proto_set = set()
    for pair in proto_nodes_v3:
        a, b = pair.split("::")
        base_proto_set.update([a, b])
    proto_nodes_full = sorted(base_proto_set | set(NEW_WORKS.keys()))

    # Étendre les nodes (ajouter les nouvelles œuvres)
    nodes = dict(v159["nodes"])
    for wid, info in NEW_WORKS.items():
        nodes[wid] = {
            "kind": "proto_atheist_work",
            **info,
        }

    # Combiner arêtes v159 + v168
    edges_v2 = [(e["src"], e["tgt"], e["weight"], e["channel"])
                for e in v159["edges"]]
    all_edges = edges_v2 + NEW_EDGES
    adj = _build_adjacency(all_edges)
    all_node_ids = list(nodes.keys())
    paths = shortest_paths(adj, all_node_ids)

    # Calculer les distances pour TOUS les couples PROTO
    proto_pairs: dict[str, float | None] = {}
    finite = 0
    for i, a in enumerate(proto_nodes_full):
        for b in proto_nodes_full[i + 1:]:
            d = paths.get((a, b), paths.get((b, a), math.inf))
            if math.isfinite(d):
                finite += 1
            proto_pairs[f"{a}::{b}"] = d if math.isfinite(d) else None

    finite_dists = [d for d in proto_pairs.values() if d is not None]
    n_total_pairs = len(proto_pairs)

    # Comparaison v159 vs v168 sur les paires existantes
    deltas = []
    for k, d_v3 in proto_pairs.items():
        d_v2 = v159["proto_pair_distances"].get(k)
        if d_v2 is None or d_v3 is None:
            continue
        if abs(d_v3 - d_v2) > 1e-6:
            deltas.append({
                "pair": k,
                "d_v159": round(d_v2, 4),
                "d_v168": round(d_v3, 4),
                "delta": round(d_v3 - d_v2, 4),
            })
    deltas.sort(key=lambda x: x["delta"])

    summary = {
        "n_nodes_total": len(nodes),
        "n_proto_works_v2": len(base_proto_set),
        "n_proto_works_v3": len(proto_nodes_full),
        "n_works_added": len(NEW_WORKS),
        "n_edges_v159": len(edges_v2),
        "n_edges_added": len(NEW_EDGES),
        "n_edges_total": len(all_edges),
        "n_pairs_total": n_total_pairs,
        "n_pairs_connected": finite,
        "n_pairs_unconnected": n_total_pairs - finite,
        "min_dist_v168": round(min(finite_dists), 4) if finite_dists else None,
        "mean_dist_v168": round(sum(finite_dists) / len(finite_dists), 4) if finite_dists else None,
        "max_dist_v168": round(max(finite_dists), 4) if finite_dists else None,
    }

    payload = {
        "version": "v168",
        "step": "§168 — graphe d'héritage v3 (extension Spinoza/Hobbes/Mozi/HanFeizi)",
        "supersedes": "v159",
        "summary": summary,
        "weight_scheme": v159.get("weight_scheme"),
        "nodes": nodes,
        "edges": [{"src": s, "tgt": t, "weight": w, "channel": c}
                  for (s, t, w, c) in all_edges],
        "proto_pair_distances": proto_pairs,
        "deltas_v159_vs_v168": deltas[:30],  # top 30 changes
    }
    GRAPH_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Graphe v3 écrit : {GRAPH_OUT.relative_to(ROOT)}")
    print(f"  nodes={len(nodes)}  edges={len(all_edges)}  pairs={n_total_pairs}  "
          f"connected={finite}")
    print(f"  mean dist = {summary['mean_dist_v168']}")

    # ─── Métadonnées étendues ────────────────────────────────────────
    works_meta = dict(v147_meta.get("works", {}))
    v166_results = {r["work_id"]: r for r in v166.get("results", [])}
    for wid, info in NEW_WORKS.items():
        prov_path = CORPUS_DIR / wid / "PROVENANCE.json"
        prov = json.loads(prov_path.read_text(encoding="utf-8")) if prov_path.exists() else {}
        nfrag = count_fragments(wid)
        works_meta[wid] = {
            "writing_year": info["year"],
            "lang": info["lang"],
            "tradition_label": info["tradition_label"],
            "author": info["author"],
            "n_fragments": nfrag,
            "source_url": prov.get("source_url"),
            "sha256": prov.get("sha256"),
            "edition": prov.get("edition"),
            "license": prov.get("license"),
            "completeness": prov.get("completeness"),
            "retrieval_date_utc": prov.get("retrieval_date_utc"),
        }

    meta_payload = {
        "version": "v168",
        "step": "§168 — métadonnées étendues (4 nouvelles œuvres avec traçabilité)",
        "n_works_total": len(works_meta),
        "n_works_new_v168": len(NEW_WORKS),
        "works": works_meta,
    }
    META_OUT.write_text(json.dumps(meta_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Métadonnées v168 écrites : {META_OUT.relative_to(ROOT)}")
    print(f"  n_works = {len(works_meta)} (4 nouvelles avec traçabilité)")


if __name__ == "__main__":
    main()

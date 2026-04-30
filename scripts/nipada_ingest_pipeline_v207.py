#!/usr/bin/env python3
"""§207 — Pipeline auto-ingestion : 24 catalogues × 70 → graphe v10.

Étapes :
  1. Charger graphe v9 (89 nodes, 180 edges).
  2. Charger les 24 catalogues `research/nipada/corpus/catalog_*_v206?.json`.
  3. Pour chaque œuvre catalog_only, produire un node graph v10.
  4. Préserver les nodes existants v9 (89 → enrichis si overlap par ID).
  5. Conserver les edges v9 telles quelles (pas de nouvelle inférence ici).
  6. Stubs pour `fetch_url`, `normalize_text`, `v14_signature`
     (seront utilisés par §208 sur sous-ensemble PoC).

Sortie : `research/nipada/falsification/nipada_v207_graph_v10.json`
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRAPH_V9 = REPO / "research/nipada/falsification/nipada_v189_graph_v9.json"
CATALOG_DIR = REPO / "research/nipada/corpus"
GRAPH_V10 = REPO / "research/nipada/falsification/nipada_v207_graph_v10.json"
CACHE_DIR = REPO / "data/references_cache/corpus_text"


# --------------------------------------------------------------------- stubs
def fetch_url(url: str, cache_dir: Path = CACHE_DIR) -> str | None:
    """Récupère un texte distant, met en cache local. Stub §207 (§208 actif).

    En §207, retourne None systématiquement : la phase ingestion réelle
    démarre en §208. La cache_dir est créée pour la PoC suivante.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    if url is None:
        return None
    cache_file = cache_dir / hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")
    return None


def normalize_text(text: str) -> str:
    """Normalisation Unicode NFC + collapse whitespace."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def v14_signature(text: str, lang: str) -> dict[str, float]:
    """Signature V14 baseline (§145-light heuristique).

    Retourne {atom: score 0..1} pour 14 atomes. Stub §207 — sera enrichi en §208.
    Implémentation v0 : marqueurs lexicaux multilingues minimaux.
    """
    if not text:
        return {a: 0.0 for a in V14}
    text_l = text.lower()
    sig: dict[str, float] = {a: 0.0 for a in V14}
    for atom, markers in V14_MARKERS.items():
        hits = sum(text_l.count(m) for m in markers)
        sig[atom] = min(1.0, hits / 5.0)
    return sig


V14 = ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
       "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
       "STRUCTURE", "SYMÉTRIE", "ÉQUATION"]

V14_MARKERS: dict[str, list[str]] = {
    "ÊTRE":        ["est ", " is ", "sein", "esse", "ens", "to be", "बत"],
    "DIFFÉRENCE":  ["non ", " not ", "ne pas", "nicht", "anyatva", "差", "ال "],
    "RAPPORT":     [" rapport", " relation", " ratio", "sambandha", "關係"],
    "ORIENTATION": [" vers ", " toward", " richtung", " ad ", "इसी"],
    "SUJET":       [" je ", " moi ", " self ", " ich ", "ātman", " atman", "我"],
    "TEMPS":       [" temps", " time", " zeit", " kāla", "तदा", "時"],
    "MODALITÉ":    [" peut ", " may ", " kann ", " ne pas ", " not ", " forse"],
    "NOMBRE":      [" un ", " one ", " ein ", " eka ", " duo ", "數"],
    "ESPACE":      [" lieu", " place", " ākāśa", " akasa", "空間"],
    "OPÉRATION":   [" produit", " génère", " engendr", "kriyā", "kriya"],
    "FONCTION":    [" fonction", " function", " upakar", " purpose"],
    "STRUCTURE":   [" structure", " corps ", " body ", "deha", "śarīra"],
    "SYMÉTRIE":    [" symét", " symmet", " ardha", "сим"],
    "ÉQUATION":    [" égal", " equal", " sama ", "मिथः"],
}


def upsert_graph_node(graph: dict, work: dict) -> bool:
    """Insère/met à jour un node dans `graph`.

    Retourne True si insertion (id absent), False si update.
    """
    wid = work["id"]
    nodes: dict = graph["nodes"]
    new = wid not in nodes
    node_payload = {
        "kind": "canon_work",
        "author": work.get("author"),
        "year": work.get("year_estimate"),
        "language_original": work.get("language_original"),
        "tradition_label": f"{work['macro_culture']}_{work['epoch']}".upper(),
        "tradition_micro": work.get("tradition_micro"),
        "title_original": work.get("title_original"),
        "title_en": work.get("title_en"),
        "tags": work.get("tags", []),
        "ingestion_status": work.get("ingestion_status", "catalog_only"),
        "v14_signature": None,
    }
    if new:
        nodes[wid] = node_payload
    else:
        # préserve les champs existants v9, ajoute les manquants
        existing = nodes[wid]
        for k, v in node_payload.items():
            if k not in existing or existing.get(k) is None:
                existing[k] = v
    return new


def main() -> int:
    graph = json.loads(GRAPH_V9.read_text(encoding="utf-8"))
    n_v9_nodes = len(graph["nodes"])
    n_v9_edges = len(graph["edges"])

    catalogs = sorted(CATALOG_DIR.glob("catalog_*.json"))
    catalogs = [c for c in catalogs if c.name != "INDEX_catalogs_v206z.json"]

    n_inserted = 0
    n_updated = 0
    n_total_works = 0

    for cat_path in catalogs:
        data = json.loads(cat_path.read_text(encoding="utf-8"))
        for work in data["works"]:
            n_total_works += 1
            if upsert_graph_node(graph, work):
                n_inserted += 1
            else:
                n_updated += 1

    graph["version"] = "v10_post_v207_ingestion"
    graph["n_nodes"] = len(graph["nodes"])
    graph["n_edges"] = len(graph["edges"])
    graph.setdefault("meta", {})
    graph["meta"]["v207_ingestion"] = {
        "catalogs_loaded": len(catalogs),
        "works_total": n_total_works,
        "nodes_inserted": n_inserted,
        "nodes_updated": n_updated,
        "n_v9_nodes_before": n_v9_nodes,
        "n_v9_edges_before": n_v9_edges,
        "n_v10_nodes_after": graph["n_nodes"],
        "n_v10_edges_after": graph["n_edges"],
    }

    GRAPH_V10.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"§207 — Pipeline ingestion terminé")
    print(f"  Catalogues chargés      : {len(catalogs)}")
    print(f"  Œuvres parcourues       : {n_total_works}")
    print(f"  Nodes insérés (nouveau) : {n_inserted}")
    print(f"  Nodes mis à jour        : {n_updated}")
    print(f"  Graph v9  : {n_v9_nodes} nodes, {n_v9_edges} edges")
    print(f"  Graph v10 : {graph['n_nodes']} nodes, {graph['n_edges']} edges")
    print(f"  Sortie : {GRAPH_V10.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

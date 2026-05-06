#!/usr/bin/env python3
"""
§264 — Patch graph v15s → v16p : ajout du catalogue prophétique.

Ajoute au graphe nipada_v258_graph_v15s.json :
  - Nœuds pour les textes prophétiques et leurs interprètes (source_type metadata)
  - Arêtes intra-tradition (tradition_macro §264 indirect) pour chaque tradition prophétique
  - Arêtes d'interprétation directe (direct interprétation §264) : commentary → source

Nouvelles traditions:
  ABRAHAMIC_PROPHETIC_AXIAL        : Isaïe, Jérémie, Ézéchiel, Daniel, Zacharie, Osée
  JUDEAN_APOCALYPTIC_LATE          : 1 Hénoch, 2 Esdras
  CHRISTIAN_APOCALYPTIC_EARLY      : Apocalypse de Jean
  CLASSICAL_ORACULAR               : Oracles sibyllins
  ZOROASTRIAN_AXIAL                : Gathas de Zarathoustra
  NORSE_EDDIC_MEDIEVAL             : Völuspá
  MESOAMERICAN_COLONIAL            : Chilam Balam
  RENAISSANCE_OCCULT_EARLY_MODERN  : Nostradamus
  MILLENARIAN_MODERN_PROTESTANT    : Russell (1878), Miller (1836)

Canaux d'arêtes:
  'tradition_macro (§264 prophétique)' → classify_channel → 'indirect' (coût 1.0)
  'direct interprétation critique (§264)' → classify_channel → 'direct' (coût 0.05)

Produit:
  nipada/falsification/nipada_v264_graph_v16p.json
  nipada/falsification/nipada_v264_graph_patch_report.json
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

FALSI_DIR   = _NIPADA / "falsification"
IN_GRAPH    = FALSI_DIR / "nipada_v258_graph_v15s.json"
OUT_GRAPH   = FALSI_DIR / "nipada_v264_graph_v16p.json"
OUT_REPORT  = FALSI_DIR / "nipada_v264_graph_patch_report.json"

# ── New prophetic nodes ──────────────────────────────────────────────────────
# Each entry becomes a graph node. v14_signature is null until §264 fetch runs.
# Fields match the graph node convention (see other entries in v15s).

NEW_NODES: dict[str, dict] = {
    # ── ABRAHAMIC_PROPHETIC_AXIAL ────────────────────────────────────────────
    "isaiah_book": {
        "kind": "prophetic_text",
        "author": "Isaiah ben Amoz (attributed)",
        "year": -700,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "title_en": "Isaiah (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "jeremiah_book": {
        "kind": "prophetic_text",
        "author": "Jeremiah ben Hilkiah (attributed)",
        "year": -600,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "title_en": "Jeremiah (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "ezekiel_book": {
        "kind": "prophetic_text",
        "author": "Ezekiel ben Buzi (attributed)",
        "year": -590,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "title_en": "Ezekiel (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "daniel_book": {
        "kind": "prophetic_text",
        "author": "anonymous (Daniel tradition)",
        "year": -165,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_APOCALYPTIC",
        "title_en": "Daniel (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "zechariah_book": {
        "kind": "prophetic_text",
        "author": "Zechariah ben Berechiah (attributed)",
        "year": -520,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "title_en": "Zechariah (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "hosea_book": {
        "kind": "prophetic_text",
        "author": "Hosea ben Beeri (attributed)",
        "year": -750,
        "lang": "eng",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "title_en": "Hosea (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── JUDEAN_APOCALYPTIC_LATE ──────────────────────────────────────────────
    "book_of_enoch": {
        "kind": "apocalyptic_text",
        "author": "anonymous (R.H. Charles trans. 1913)",
        "year": -200,
        "lang": "eng",
        "tradition_label": "JUDEAN_APOCALYPTIC_LATE",
        "tradition_micro": "JEWISH_APOCALYPTIC",
        "title_en": "The Book of Enoch (1 Enoch)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "2_esdras": {
        "kind": "apocalyptic_text",
        "author": "anonymous (Ezra apocalypse tradition)",
        "year": 100,
        "lang": "eng",
        "tradition_label": "JUDEAN_APOCALYPTIC_LATE",
        "tradition_micro": "JEWISH_APOCALYPTIC",
        "title_en": "2 Esdras / 4 Ezra (Polyglot Bible)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── CHRISTIAN_APOCALYPTIC_EARLY ──────────────────────────────────────────
    "revelation_john": {
        "kind": "apocalyptic_text",
        "author": "John of Patmos (attributed)",
        "year": 95,
        "lang": "eng",
        "tradition_label": "CHRISTIAN_APOCALYPTIC_EARLY",
        "tradition_micro": "CHRISTIAN_PROPHETIC",
        "title_en": "Revelation of John (KJV)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── CLASSICAL_ORACULAR ───────────────────────────────────────────────────
    "sibylline_oracles": {
        "kind": "oracular_text",
        "author": "anonymous (Milton S. Terry trans. 1899)",
        "year": -200,
        "lang": "eng",
        "tradition_label": "CLASSICAL_ORACULAR",
        "tradition_micro": "GRECO_ROMAN_ORACULAR",
        "title_en": "Sibylline Oracles",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── ZOROASTRIAN_AXIAL ────────────────────────────────────────────────────
    "avesta_gathas": {
        "kind": "sacred_hymn",
        "author": "Zarathustra (attributed, L.H. Mills trans. 1887, SBE vol.31)",
        "year": -1000,
        "lang": "eng",
        "tradition_label": "ZOROASTRIAN_AXIAL",
        "tradition_micro": "ZOROASTRIAN_PROPHETIC",
        "title_en": "Avesta: The Gathas (SBE 31)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── NORSE_EDDIC_MEDIEVAL ─────────────────────────────────────────────────
    "voluspa": {
        "kind": "eddic_poem",
        "author": "anonymous (Bellows trans. 1936)",
        "year": 1000,
        "lang": "eng",
        "tradition_label": "NORSE_EDDIC_MEDIEVAL",
        "tradition_micro": "NORSE_EDDIC_PROPHETIC",
        "title_en": "Völuspá — The Sibyl's Prophecy (Poetic Edda)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── MESOAMERICAN_COLONIAL ────────────────────────────────────────────────
    "chilam_balam": {
        "kind": "prophetic_text",
        "author": "anonymous Maya scribes (Roys trans. 1933)",
        "year": 1650,
        "lang": "eng",
        "tradition_label": "MESOAMERICAN_COLONIAL",
        "tradition_micro": "MAYAN_PROPHETIC",
        "title_en": "The Book of Chilam Balam of Chumayel",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── RENAISSANCE_OCCULT_EARLY_MODERN ─────────────────────────────────────
    "nostradamus_centuries": {
        "kind": "prophetic_text",
        "author": "Michel de Nostredame (Nostradamus)",
        "year": 1555,
        "lang": "fra",
        "tradition_label": "RENAISSANCE_OCCULT_EARLY_MODERN",
        "tradition_micro": "FRENCH_PROPHETIC_RENAISSANCE",
        "title_en": "Les Prophéties (Centuries)",
        "source_type": "primary_prophetic",
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },

    # ── MILLENARIAN_MODERN_PROTESTANT ────────────────────────────────────────
    "russell_parousia_1878": {
        "kind": "interpretive_work",
        "author": "James Stuart Russell",
        "year": 1878,
        "lang": "eng",
        "tradition_label": "MILLENARIAN_MODERN_PROTESTANT",
        "tradition_micro": "PRETERIST_INTERPRETATION",
        "title_en": "The Parousia (1878)",
        "source_type": "interpretive_commentary",
        "interprets_ref": ["revelation_john", "daniel_book", "2_esdras"],
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
    "miller_evidence_prophecy": {
        "kind": "interpretive_work",
        "author": "William Miller",
        "year": 1836,
        "lang": "eng",
        "tradition_label": "MILLENARIAN_MODERN_PROTESTANT",
        "tradition_micro": "ADVENTIST_INTERPRETATION",
        "title_en": "Evidence from Scripture and History of the Second Coming (1836)",
        "source_type": "interpretive_commentary",
        "interprets_ref": ["daniel_book", "revelation_john", "2_esdras"],
        "ingestion_status": "catalog_only",
        "v14_signature": None,
    },
}

# ── Tradition clusters for intra-tradition indirect edges ────────────────────
# These are the groups within which all texts are connected via indirect edges.

TRADITION_CLUSTERS: dict[str, list[str]] = {
    # Prophètes hébreux et apocalyptique juif : tradition commune
    "abrahamic_prophetic": [
        "isaiah_book", "jeremiah_book", "ezekiel_book", "daniel_book",
        "zechariah_book", "hosea_book", "book_of_enoch", "2_esdras",
    ],
    # Christianisme apocalyptique : Révélation + lien judéo-chrétien
    "christian_judean_apocalyptic": [
        "revelation_john", "daniel_book", "book_of_enoch", "2_esdras",
    ],
    # Tradition oraculaire classique (sibylline) : peut avoir subi influence judéo-chrétienne
    "classical_and_judean_oracular": [
        "sibylline_oracles", "book_of_enoch",
    ],
    # Tradition millénariste moderne : lit tous les textes apocalyptiques
    "millenarian_modern": [
        "russell_parousia_1878", "miller_evidence_prophecy",
        "revelation_john", "daniel_book", "2_esdras",
    ],
}

# ── Interprets edges (direct) ────────────────────────────────────────────────
# channel contains "direct" → classify_channel → "direct" (coût 0.05)

INTERPRETS_EDGES: list[tuple[str, str, str]] = [
    # Russell → sources qu'il interprète
    ("russell_parousia_1878", "revelation_john",
     "direct interprétation critique (§264) — Russell prétériste sur l'Apocalypse"),
    ("russell_parousia_1878", "daniel_book",
     "direct interprétation critique (§264) — Russell sur Daniel"),
    ("russell_parousia_1878", "2_esdras",
     "direct interprétation critique (§264) — Russell sur 4 Esdras"),
    # Miller → sources qu'il interprète
    ("miller_evidence_prophecy", "daniel_book",
     "direct interprétation critique (§264) — Miller millénariste sur Daniel"),
    ("miller_evidence_prophecy", "revelation_john",
     "direct interprétation critique (§264) — Miller sur l'Apocalypse"),
    ("miller_evidence_prophecy", "2_esdras",
     "direct interprétation critique (§264) — Miller sur 4 Esdras"),
]

# ── Fix carus_gospel_buddha_en (already in graph, needs interprets edges) ────
# Paul Carus 1894 : interprète/compile Dhammapada, Jataka, divers suttas
CARUS_FIX_EDGES: list[tuple[str, str, str]] = [
    ("carus_gospel_buddha_en", "dhammapada_muller_en",
     "direct compilation (§264) — Carus 1894 compile le Dhammapada parmi ses sources"),
]


def main() -> None:
    print("=" * 65)
    print("§264 — Graph patch v15s → v16p : catalogue prophétique")
    print(f"  input : {IN_GRAPH}")
    print(f"  output: {OUT_GRAPH}")
    print("=" * 65)

    # ── Charger graphe de base ────────────────────────────────────────────────
    print(f"\nChargement {IN_GRAPH.name}...")
    g = json.loads(IN_GRAPH.read_text(encoding="utf-8"))
    nodes: dict = g["nodes"]
    edges: list  = g["edges"]
    n_nodes_before = len(nodes)
    n_edges_before  = len(edges)
    print(f"  {n_nodes_before} nœuds, {n_edges_before} arêtes")

    # ── Ajouter nœuds ─────────────────────────────────────────────────────────
    print(f"\nAjout de {len(NEW_NODES)} nœuds prophétiques...")
    already_exists = []
    added_nodes = []
    for nid, meta in NEW_NODES.items():
        if nid in nodes:
            print(f"  [SKIP] {nid} — déjà présent")
            already_exists.append(nid)
        else:
            nodes[nid] = meta
            added_nodes.append(nid)
            print(f"  [+] {nid} ({meta['tradition_label']})")

    # ── Ajouter arêtes intra-tradition ────────────────────────────────────────
    print(f"\nAjout arêtes tradition_macro (§264 prophétique)...")
    added_indirect: list[dict] = []
    for cluster_name, members in TRADITION_CLUSTERS.items():
        # Only include members that are actually in the graph
        present = [m for m in members if m in nodes]
        if len(present) < 2:
            continue
        for a, b in combinations(sorted(present), 2):
            edge = {
                "src": a,
                "tgt": b,
                "weight": 1.0,
                "channel": f"tradition_macro (§264 prophétique — {cluster_name})",
            }
            edges.append(edge)
            added_indirect.append(edge)
        print(f"  [{cluster_name}] {len(present)} membres → "
              f"{len(list(combinations(present, 2)))} arêtes intra-tradition")

    # ── Ajouter arêtes d'interprétation directe ───────────────────────────────
    print(f"\nAjout arêtes d'interprétation directe (§264)...")
    added_direct: list[dict] = []
    for src, tgt, channel in INTERPRETS_EDGES:
        if src not in nodes:
            print(f"  [SKIP] {src} — nœud absent")
            continue
        if tgt not in nodes:
            print(f"  [SKIP] {tgt} — nœud cible absent")
            continue
        edge = {"src": src, "tgt": tgt, "weight": 0.05, "channel": channel}
        edges.append(edge)
        added_direct.append(edge)
        print(f"  [+] {src} → {tgt}")

    # ── Fix carus_gospel_buddha_en si présent ─────────────────────────────────
    print(f"\nFix carus_gospel_buddha_en (arêtes manquantes)...")
    added_carus: list[dict] = []
    for src, tgt, channel in CARUS_FIX_EDGES:
        if src in nodes and tgt in nodes:
            edge = {"src": src, "tgt": tgt, "weight": 0.05, "channel": channel}
            edges.append(edge)
            added_carus.append(edge)
            print(f"  [+] {src} → {tgt}")
        else:
            missing = [x for x in [src, tgt] if x not in nodes]
            print(f"  [SKIP] nœuds absents: {missing}")

    # ── Mettre à jour métadonnées du graphe ────────────────────────────────────
    g["nodes"] = nodes
    g["edges"] = edges
    g["version"] = "v16p"
    g["section"] = "§264"
    g["note"] = (
        "§264 — Patch prophétique sur v15s: "
        f"{len(added_nodes)} nouveaux nœuds, "
        f"{len(added_indirect)} arêtes intra-tradition, "
        f"{len(added_direct)} arêtes interprétation directe, "
        f"{len(added_carus)} arêtes fix carus."
    )

    # ── Résumé ────────────────────────────────────────────────────────────────
    n_nodes_after = len(nodes)
    n_edges_after  = len(edges)
    print(f"\n── Résultats ────────────────────────────────────────────────")
    print(f"  Nœuds: {n_nodes_before} → {n_nodes_after} (+{n_nodes_after - n_nodes_before})")
    print(f"  Arêtes: {n_edges_before} → {n_edges_after} (+{n_edges_after - n_edges_before})")
    print(f"    intra-tradition : {len(added_indirect)}")
    print(f"    interprétation  : {len(added_direct)}")
    print(f"    carus fix       : {len(added_carus)}")

    # ── Écriture ──────────────────────────────────────────────────────────────
    OUT_GRAPH.write_text(json.dumps(g, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"\nGraphe écrit : {OUT_GRAPH}")

    report = {
        "section": "§264",
        "graph_version": "v16p",
        "base_graph": "nipada_v258_graph_v15s.json",
        "n_nodes_before": n_nodes_before,
        "n_nodes_after":  n_nodes_after,
        "n_edges_before": n_edges_before,
        "n_edges_after":  n_edges_after,
        "added_nodes": added_nodes,
        "skipped_nodes_already_present": already_exists,
        "added_indirect_edges": len(added_indirect),
        "added_direct_edges": len(added_direct),
        "added_carus_fix_edges": len(added_carus),
        "tradition_clusters": {k: v for k, v in TRADITION_CLUSTERS.items()},
    }
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print(f"Rapport écrit: {OUT_REPORT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
nipada_patch_graph_v19.py  — §271 NiPaDa
═══════════════════════════════════════════════════════════════════════════════
Construit le graphe v19 à partir de v18p en ajoutant 15 arêtes inter-traditions
(grec ↔ inde/chine) de type tradition_macro (§271 inter-axial direct), coût 0.05.

Ces arêtes sont DIRIGÉES (grec → tradition_cible) pour éviter les raccourcis
«fantômes» Indian↔Chinese via le hub grec tradition_macro.

Contexte §271:
  - §270a officiel : 120 textes, R²=0.5866, graphe v18p
  - §271 objectif : intégrer 29 textes grecs (Platon + Aristote) dans le corpus
  - Problème v18p : Platon/Aristote isolés, seul aristotle_prior_analytics
    connecté au corpus signé (via tradition_macro 0.05)
  - Solution v19 : 15 arêtes directes vers textes inde/chine sémantiquement
    proches ET documentés historiquement (Axial Age parallels)

Sortie: nipada/falsification/nipada_v271_graph_v19.json

Usage:
  cd /home/stephane/GitHub/Panini-Research
  python3 /home/stephane/GitHub/Panini/scripts/nipada_patch_graph_v19.py
"""

import json
import sys
import pathlib
from datetime import datetime

# ─── Chemins ──────────────────────────────────────────────────────────────────
REPO_ROOT = pathlib.Path("/home/stephane/GitHub/Panini-Research")
GRAPH_V18P = REPO_ROOT / "nipada/falsification/nipada_v266_graph_v18p.json"
OUT_DIR    = REPO_ROOT / "nipada/falsification"
OUT_GRAPH  = OUT_DIR / "nipada_v271_graph_v19.json"

# ─── Arêtes inter-traditions §271 ─────────────────────────────────────────────
# Format: (src_grec, tgt_signé, justification_courte)
# Toutes avec channel "tradition_macro (§271 inter-axial direct)" → coût 0.05
# Arêtes DIRIGÉES: src→tgt uniquement (pas de reverse edge)
# Sélectionnées sur deux critères:
#   1) d_lex (L2 en V14) ≤ 0.15 → proximité sémantique réelle
#   2) Connexion documentée par scholarship comparée (Axial Age)

EDGES_V19 = [
    # ── Platon ↔ Chine ──────────────────────────────────────────────────────
    (
        "plato_timaeus", "zhuangzi",
        "Timée ↔ Zhuangzi — cosmologie primordiale, force créatrice (Scharfstein 1998, d_lex=0.078)",
    ),
    (
        "plato_timaeus", "liezi",
        "Timée ↔ Liezi — naturalisme cosmologique, transformation (d_lex=0.083)",
    ),
    (
        "plato_timaeus", "daodejing",
        "Timée ↔ Dào — ordre cosmique primordial (Needham 1954, Scharfstein 1998, d_lex=0.102)",
    ),
    (
        "plato_laws", "mengzi",
        "Lois ↔ Mengzi — éthique politique, vertu civique (MacIntyre 1988, Hall & Ames 1987, d_lex=0.085)",
    ),
    # ── Platon ↔ Inde ───────────────────────────────────────────────────────
    (
        "plato_laws", "apastamba_dharmasutra",
        "Lois ↔ Āpastamba-Dharmasūtra — normativité légale, devoir social (d_lex=0.106)",
    ),
    (
        "plato_phaedo", "brahma_sutra_badarayana",
        "Phédon ↔ Brahma-Sūtra — âme immortelle, libération (Deussen 1907, d_lex=0.115)",
    ),
    (
        "plato_phaedo", "katha_upanishad",
        "Phédon ↔ Kaṭha-Upaniṣad — mort/immortalité de l'âme (Deussen 1907, Schopenhauer, d_lex=0.120)",
    ),
    (
        "plato_republic", "bhagavad_gita",
        "République ↔ Bhagavad-Gītā — vertu/devoir/guerre juste (Aurobindo, Zaehner 1969, d_lex=0.125)",
    ),
    (
        "plato_republic", "brahma_sutra_badarayana",
        "République ↔ Brahma-Sūtra — ordre cosmique/social, idéal (d_lex=0.116)",
    ),
    (
        "plato_phaedo", "qiwulun",
        "Phédon ↔ Qí wù lùn (Zhuangzi ch.2) — apparence/réalité, éphémère (Scharfstein 1998, d_lex=0.102)",
    ),
    # ── Aristote ↔ Inde/Chine ────────────────────────────────────────────────
    (
        "aristotle_de_anima", "brahma_sutra_badarayana",
        "De Anima ↔ Brahma-Sūtra — théorie âme/conscience (Larson, Matilal 1986, d_lex=0.081)",
    ),
    (
        "aristotle_nicomachean_ethics", "mengzi",
        "Éthique Nicomaque ↔ Mengzi — vertu/bonheur (MacIntyre 1988 'Whose Justice?', d_lex=0.150)",
    ),
    (
        "aristotle_nicomachean_ethics", "bhagavad_gita",
        "Éthique ↔ Gītā — vertu et devoir (Leidecker 1933, Matilal 1986, d_lex=0.153)",
    ),
    (
        "aristotle_politics", "apastamba_dharmasutra",
        "Politique ↔ Dharmasūtra — philosophie normative société (d_lex=0.109)",
    ),
    (
        "aristotle_metaphysics", "brahma_sutra_badarayana",
        "Métaphysique ↔ Brahma-Sūtra — ontologie être/Brahman (Halbfass 1988, d_lex=0.081)",
    ),
]

CHANNEL_V19 = "tradition_macro (§271 inter-axial direct)"


def main() -> None:
    if not GRAPH_V18P.exists():
        sys.exit(f"ERREUR: graphe v18p introuvable: {GRAPH_V18P}")

    print(f"Chargement graphe v18p: {GRAPH_V18P}")
    with GRAPH_V18P.open(encoding="utf-8") as f:
        g18p = json.load(f)

    n_nodes_before = len(g18p["nodes"])
    n_edges_before = len(g18p["edges"])
    print(f"v18p: {n_nodes_before} nœuds, {n_edges_before} arêtes")

    # ── Vérification que les nœuds existent ──────────────────────────────────
    all_nodes = set(g18p["nodes"].keys())
    missing = []
    for src, tgt, _ in EDGES_V19:
        for nid in (src, tgt):
            if nid not in all_nodes:
                missing.append(nid)
    if missing:
        sys.exit(f"ERREUR: nœuds introuvables dans v18p: {missing}")
    print(f"✓ Tous les nœuds source/cible présents dans v18p")

    # ── Construire v19 ────────────────────────────────────────────────────────
    g19 = dict(g18p)  # shallow copy
    g19["nodes"]   = dict(g18p["nodes"])   # copie des nœuds (inchangés)
    g19["edges"]   = list(g18p["edges"])   # copie des arêtes existantes

    new_edges = []
    for src, tgt, justif in EDGES_V19:
        edge = {
            "src":      src,
            "tgt":      tgt,
            "channel":  CHANNEL_V19,
            "weight":   0.05,
            "directed": True,   # Arête DIRIGÉE src→tgt (pas de reverse)
            "note":     justif,
            "section":  "§271",
        }
        g19["edges"].append(edge)
        new_edges.append(edge)

    # ── Métadonnées v19 ───────────────────────────────────────────────────────
    g19["version"] = "v19"
    g19["section"] = "§271"
    g19["date"]    = datetime.now().strftime("%Y-%m-%d")
    g19["note"]    = (
        f"Graphe v19 — §271 NiPaDa. "
        f"Basé sur v18p ({n_nodes_before} nœuds, {n_edges_before} arêtes). "
        f"Ajout de {len(EDGES_V19)} arêtes DIRIGÉES inter-traditions "
        f"(grec→inde/chine, channel='{CHANNEL_V19}', coût=0.05). "
        f"Arêtes dirigées pour éviter raccourcis Indian↔Chinese via hub grec."
    )
    g19["patch_info"] = {
        "base_graph":   "v18p",
        "base_section": g18p.get("section", "§266-§270"),
        "added_edges":  len(EDGES_V19),
        "edge_type":    "directed (src→tgt uniquement)",
        "channel":      CHANNEL_V19,
        "cost":         0.05,
        "motivation":   (
            "§271: intégration textes grecs (Platon/Aristote) dans corpus NiPaDa. "
            "Connexions Axial Age documentées (Scharfstein, MacIntyre, Deussen, Matilal, Halbfass). "
            "Arêtes DIRIGÉES pour préserver R²(intra-signé)=0.5866 (§270a)."
        ),
    }

    # ── Résumé ────────────────────────────────────────────────────────────────
    n_edges_after = len(g19["edges"])
    print(f"\nv19 résumé:")
    print(f"  Nœuds: {len(g19['nodes'])} (inchangé)")
    print(f"  Arêtes: {n_edges_before} + {len(EDGES_V19)} = {n_edges_after}")
    print(f"\nNouvelles arêtes inter-traditions §271:")
    for src, tgt, justif in EDGES_V19:
        print(f"  {src} → {tgt}  [{justif[:60]}...]")

    # ── Sauvegarde ────────────────────────────────────────────────────────────
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_GRAPH.open("w", encoding="utf-8") as f:
        json.dump(g19, f, ensure_ascii=False, indent=2)

    size_kb = OUT_GRAPH.stat().st_size // 1024
    print(f"\n✓ Graphe v19 sauvegardé: {OUT_GRAPH} ({size_kb} Ko)")
    print(f"\nÉtape suivante: python3 nipada_revalidation_v271.py")


if __name__ == "__main__":
    main()

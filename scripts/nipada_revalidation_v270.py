#!/usr/bin/env python3
"""
§270 — Extension corpus + diagnostic Platon/Aristote.

§270a (officiel) : +3 suttas pāli individuels → 117 → 120 textes
§270b (diagnostic) : 25 textes Platon/Aristote → R² effondré (0.266)
                     cause : arêtes "auteur_continu" (coût=1.0) créent clusters d_topo dégénérés

Sources :
  Base §268c  : v263 (100) + v264 (16) + v268c (1) = 117 textes
  v235 (§235) : 3 suttas pāli acceptés (≥900 mots, 6 voisins signés chacun)
    an3_65_kalama (1517 mots), an7_64_kodhana (941 mots), an10_60_girimananda (1213 mots)

Filtrages §270 :
  - an5_159_udayi          : 164 mots → EXCLU
  - diogenes_laertius_lives : NOMBRE=0.950 (artefact liste), matched=False → EXCLU
  - confucius_analects_en  : degré graphique = 0 → EXCLU
  - 25 Platon/Aristote     : R²(vs base)=0.10, bottleneck indirect → §270b diagnostic

Résultat §270a :
  n_texts = 120, n_pairs = 1211, R² = 0.587 (−0.039 vs §268c = 0.626)
  Cause de la légère baisse : clusters d_topo=1.000 (arêtes indirectes)

Usage :
    python3 nipada_revalidation_v270.py [--full]
    --full : inclut aussi le diagnostic §270b (Platon/Aristote, +28 textes)

Produit :
    Panini-Research/nipada/corpus/signed_corpus_v270_merged.json
    Panini-Research/nipada/falsification/nipada_v270_revalidation_v18p.json
"""

from __future__ import annotations

import heapq
import json
import math
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

FALSI_DIR  = _NIPADA / "falsification"
CORPUS_DIR = _NIPADA / "corpus"

GRAPH_FILE     = FALSI_DIR / "nipada_v266_graph_v18p.json"
CORPUS_V263    = CORPUS_DIR / "signed_corpus_v263_clean.json"
CORPUS_V264    = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
CORPUS_V268C   = CORPUS_DIR / "signed_corpus_v268c_mengzi.json"
CORPUS_V234C   = CORPUS_DIR / "signed_corpus_v234_curated.json"
CORPUS_V235    = CORPUS_DIR / "signed_corpus_v235_individual_suttas.json"

OUT_CORPUS     = CORPUS_DIR / "signed_corpus_v270_merged.json"
OUT_REPORT     = FALSI_DIR  / "nipada_v270_revalidation_v18p.json"

# Baseline §268c
R2_BASELINE     = 0.6261
N_PAIRS_BASELINE = 1070
N_TEXTS_BASELINE = 117

VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}
V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION",
    "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# Exclusions explicites §270
EXCLUDED_IDS = {
    "diogenes_laertius_lives",  # NOMBRE=0.950 artefact, matched=False
    "confucius_analects_en",    # nœud isolé dans le graphe (degré=0)
    "an5_159_udayi",            # 164 mots — trop court
}

# Suttas v235 acceptables (≥ 900 mots)
SUTTAS_ACCEPTED = {"an3_65_kalama", "an7_64_kodhana", "an10_60_girimananda"}


# ---------------------------------------------------------------------------
# Utilitaires graphe
# ---------------------------------------------------------------------------
def classify_channel(ch: str) -> str:
    low = ch.lower()
    if "traduction" in low or low == "idem traduction":
        return "translation"
    if "direct" in low:
        return "direct"
    return "indirect"


def build_adj(edges: list[dict]) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        s, t = e["src"], e["tgt"]
        w = VOPT[classify_channel(e.get("channel", ""))]
        adj.setdefault(s, []).append((t, w))
        adj.setdefault(t, []).append((s, w))
    return adj


def dijkstra(src: str, adj: dict) -> dict[str, float]:
    dist: dict[str, float] = {src: 0.0}
    heap: list = [(0.0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, math.inf):
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def l2(sa: dict, sb: dict) -> float:
    return math.sqrt(sum((sa.get(a, 0.0) - sb.get(a, 0.0)) ** 2 for a in V14_ATOMS))


def pearson_r2(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return float("nan")
    return (num / (dx * dy)) ** 2


# ---------------------------------------------------------------------------
# Chargement corpus
# ---------------------------------------------------------------------------
def get_id(t: dict) -> str:
    return t.get("graph_node_id") or t.get("local_id") or ""


def load_base_corpus() -> list[dict[str, Any]]:
    """Charge les 117 textes officiels (v263 + v264 + v268c)."""
    texts: list[dict[str, Any]] = []
    for p in [CORPUS_V263, CORPUS_V264, CORPUS_V268C]:
        d = json.loads(p.read_text(encoding="utf-8"))
        texts.extend(d.get("signed", []))
    return texts


def normalise_item(t: dict, source: str) -> dict[str, Any]:
    """Normalise un item vers le schéma minimal requis par compute_pairs."""
    nid = get_id(t)
    return {
        "graph_node_id": nid,
        "local_id": t.get("local_id") or nid,
        "v14_signature": t["v14_signature"],
        "v14_top3": t.get("v14_top3", []),
        "n_words": t.get("n_words") or t.get("n_words_total") or 0,
        "tradition_label": t.get("tradition_label", ""),
        "source_270": source,
    }


def load_suttas(existing_ids: set[str]) -> list[dict[str, Any]]:
    """§270a officiel : 3 suttas pāli acceptés (≥900 mots, 6 voisins signés)."""
    d235 = json.loads(CORPUS_V235.read_text(encoding="utf-8"))
    return [
        normalise_item(t, "v235_suttas")
        for t in d235.get("signed", [])
        if get_id(t) in SUTTAS_ACCEPTED and get_id(t) not in existing_ids
    ]


def load_greek(existing_ids: set[str]) -> list[dict[str, Any]]:
    """§270b diagnostic : 25 textes Platon + Aristote de v234_curated."""
    d234c = json.loads(CORPUS_V234C.read_text(encoding="utf-8"))
    return [
        normalise_item(t, "v234_curated")
        for t in d234c.get("signed", [])
        if get_id(t) not in existing_ids and get_id(t) not in EXCLUDED_IDS
    ]


# ---------------------------------------------------------------------------
# Calcul des paires
# ---------------------------------------------------------------------------
def compute_pairs(
    texts: list[dict[str, Any]],
    adj: dict[str, list[tuple[str, float]]],
) -> tuple[list[float], list[float]]:
    ids = [t["graph_node_id"] for t in texts]
    sigs = {t["graph_node_id"]: t["v14_signature"] for t in texts}
    dtopo_list: list[float] = []
    dlex_list: list[float] = []
    for i, src in enumerate(ids):
        dist = dijkstra(src, adj)
        for tgt in ids[i + 1:]:
            d = dist.get(tgt, math.inf)
            if math.isfinite(d):
                dtopo_list.append(d)
                dlex_list.append(l2(sigs[src], sigs[tgt]))
    return dtopo_list, dlex_list


# ---------------------------------------------------------------------------
# Sauvegarde corpus fusionné
# ---------------------------------------------------------------------------
def save_merged_corpus(
    base_texts: list[dict[str, Any]],
    suttas: list[dict[str, Any]],
    greek: list[dict[str, Any]],
    include_greek: bool,
) -> None:
    import datetime

    d263 = json.loads(CORPUS_V263.read_text(encoding="utf-8"))
    d264 = json.loads(CORPUS_V264.read_text(encoding="utf-8"))
    d268c = json.loads(CORPUS_V268C.read_text(encoding="utf-8"))

    all_items: list[dict[str, Any]] = []
    all_items.extend(d263.get("signed", []))
    all_items.extend(d264.get("signed", []))
    all_items.extend(d268c.get("signed", []))

    # Suttas v235
    d235 = json.loads(CORPUS_V235.read_text(encoding="utf-8"))
    sutta_ids = {t["graph_node_id"] for t in suttas}
    for t in d235.get("signed", []):
        if get_id(t) in sutta_ids:
            item = dict(t); item["corpus_source"] = "v235_individual_suttas"
            all_items.append(item)

    # Platon/Aristote v234_curated (§270b seulement)
    greek_ids: set[str] = set()
    if include_greek:
        d234c = json.loads(CORPUS_V234C.read_text(encoding="utf-8"))
        greek_ids = {t["graph_node_id"] for t in greek}
        for t in d234c.get("signed", []):
            if get_id(t) in greek_ids:
                item = dict(t); item["corpus_source"] = "v234_curated"
                all_items.append(item)

    n_sutta = len(d263.get("signed",[])) + len(d264.get("signed",[])) + len(d268c.get("signed",[]))
    mode_note = "§270a+§270b (145 textes)" if include_greek else "§270a (120 textes, officiel)"
    payload = {
        "version": "v270",
        "description": (
            f"Corpus §270 — {mode_note}. "
            "§270a : +3 suttas pāli (an3_65_kalama, an7_64_kodhana, an10_60_girimananda). "
            + ("§270b : +25 Platon/Aristote (diagnostic, R² dégradé)." if include_greek else "")
        ),
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_texts": len(all_items),
        "sources": {
            "v263_clean": len(d263.get("signed", [])),
            "v264_prophetic": len(d264.get("signed", [])),
            "v268c_mengzi": len(d268c.get("signed", [])),
            "v235_suttas_270a": len(sutta_ids),
            "v234_curated_270b": len(greek_ids),
        },
        "exclusions": sorted(EXCLUDED_IDS),
        "graph_version": "v18p",
        "vopt": VOPT,
        "signed": all_items,
    }
    OUT_CORPUS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Corpus fusionné → {OUT_CORPUS}  ({len(all_items)} textes)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    include_greek = "--full" in sys.argv
    if include_greek:
        print("§270 — Mode COMPLET (§270a + §270b diagnostic Platon/Aristote)")
    else:
        print("§270a — Extension officielle : 117 → 120 textes (suttas pāli)")
    print("=" * 60)

    # 1. Chargement base
    print("\n[1] Chargement corpus base (117 textes)…")
    base_texts = load_base_corpus()
    base_ids = {get_id(t) for t in base_texts}
    print(f"  Base §268c : {len(base_texts)} textes")

    # 2. Nouveaux textes
    print("\n[2] Chargement nouveaux textes…")
    suttas = load_suttas(base_ids)
    print(f"  §270a suttas pāli : {len(suttas)} textes")
    greek = load_greek(base_ids)
    print(f"  §270b Platon/Aristote : {len(greek)} textes (diagnostic)")

    new_texts = suttas + (greek if include_greek else [])
    all_texts = base_texts + new_texts
    all_ids = {t["graph_node_id"] for t in all_texts}
    print(f"  TOTAL §270{'+b' if include_greek else 'a'} : {len(all_texts)} textes")

    # 3. Graphe
    print("\n[3] Chargement graphe v18p…")
    gd = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
    adj = build_adj(gd["edges"])
    print(f"  {len(gd['nodes'])} nœuds, {len(gd['edges'])} arêtes")

    missing = [t["graph_node_id"] for t in new_texts if t["graph_node_id"] not in gd["nodes"]]
    if missing:
        print(f"  ⚠  Nœuds ABSENTS du graphe : {missing}")

    # 4. Paires §270a (officiel)
    print(f"\n[4] R² §270a ({len(base_texts) + len(suttas)} textes)…")
    import time
    t0 = time.time()
    xs_a, ys_a = compute_pairs(base_texts + suttas, adj)
    r2_a = pearson_r2(xs_a, ys_a)
    print(f"  n_texts={len(base_texts)+len(suttas)}, n_pairs={len(xs_a):,d}, R²={r2_a:.6f}  "
          f"(Δ={r2_a - R2_BASELINE:+.6f} vs §268c={R2_BASELINE})")

    # 5. Paires §270b (si --full)
    r2_b, xs_b, ys_b = float("nan"), [], []
    if include_greek:
        print(f"\n[5] R² §270b ({len(all_texts)} textes, diagnostic Platon/Aristote)…")
        xs_b, ys_b = compute_pairs(all_texts, adj)
        r2_b = pearson_r2(xs_b, ys_b)
        print(f"  n_texts={len(all_texts)}, n_pairs={len(xs_b):,d}, R²={r2_b:.6f}  "
              f"(Δ={r2_b - R2_BASELINE:+.6f} vs §268c)")

    elapsed = time.time() - t0
    print(f"  Durée totale calcul : {elapsed:.1f}s")

    # 6. Voisins signés nouveaux textes
    print("\n[6] Voisins signés dans la base (117 textes)…")
    from collections import defaultdict
    adj_raw: dict[str, set[str]] = defaultdict(set)
    for e in gd["edges"]:
        adj_raw[e["src"]].add(e["tgt"])
        adj_raw[e["tgt"]].add(e["src"])
    for t in sorted(suttas + (greek if include_greek else []), key=lambda x: x["graph_node_id"]):
        nid = t["graph_node_id"]
        nb_signed = sum(1 for nb in adj_raw[nid] if nb in base_ids)
        top1 = sorted(t["v14_signature"].items(), key=lambda x: -x[1])[0]
        label = "[270a]" if t.get("source_270") == "v235_suttas" else "[270b]"
        print(f"  {label} {nid:<42} signed_nb={nb_signed:>2}  top1={top1[0]}:{top1[1]:.3f}")

    # 7. LOO §270a par sutta
    print("\n[7] LOO §270a (contribution de chaque sutta)…")
    loo_a: list[dict] = []
    base_plus_suttas = base_texts + suttas
    xs_full_a, ys_full_a = xs_a, ys_a
    r2_full_a = r2_a
    for s in suttas:
        sid = s["graph_node_id"]
        subset = [t for t in base_plus_suttas if t["graph_node_id"] != sid]
        xs2, ys2 = compute_pairs(subset, adj)
        r2_wo = pearson_r2(xs2, ys2)
        delta = r2_full_a - r2_wo
        role = "contributor" if delta > 0.001 else ("outlier" if delta < -0.001 else "neutral")
        loo_a.append({"text": sid, "r2_without": round(r2_wo, 6), "delta_r2": round(delta, 6), "role": role})
        print(f"  {sid:<42} ΔR²={delta:+.6f}  [{role}]")

    # 8. LOO §270b groupé (si --full)
    loo_b: list[dict] = []
    if include_greek:
        print("\n[8] LOO §270b groupé (Platon, Aristote, suttas)…")
        greek_ids_by_tradition = {
            "platon": [t["graph_node_id"] for t in greek if t["graph_node_id"].startswith("plato_")],
            "aristote": [t["graph_node_id"] for t in greek if t["graph_node_id"].startswith("aristotle_")],
            "suttas_pali": [t["graph_node_id"] for t in suttas],
        }
        for gname, gids in greek_ids_by_tradition.items():
            subset = [t for t in all_texts if t["graph_node_id"] not in set(gids)]
            xs2, ys2 = compute_pairs(subset, adj)
            r2_wo = pearson_r2(xs2, ys2)
            delta = r2_b - r2_wo
            role = "contributor" if delta > 0.001 else ("outlier" if delta < -0.001 else "neutral")
            loo_b.append({"group": gname, "n": len(gids), "r2_without": round(r2_wo, 6),
                          "delta_r2": round(delta, 6), "role": role})
            print(f"  {gname:<15} (n={len(gids):>2})  ΔR²={delta:+.6f}  [{role}]  R²_sans={r2_wo:.6f}")

    # 9. Sauvegarde
    print("\n[9] Sauvegarde rapport et corpus…")
    import datetime
    report: dict[str, Any] = {
        "section": "§270",
        "description": "Extension corpus NiPaDa §270a (suttas pāli) + §270b diagnostic (Platon/Aristote)",
        "graph_version": "v18p",
        "vopt": VOPT,
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "section_270a": {
            "description": "Officiel — 117 → 120 textes (+3 suttas pāli)",
            "n_texts": len(base_texts) + len(suttas),
            "n_pairs": len(xs_a),
            "r2": round(r2_a, 6),
            "r2_baseline": R2_BASELINE,
            "delta_r2": round(r2_a - R2_BASELINE, 6),
            "verdict": "STABLE" if r2_a >= R2_BASELINE - 0.05 else "DÉGRADÉ",
            "new_texts": [t["graph_node_id"] for t in suttas],
            "loo_per_sutta": loo_a,
        },
        "section_270b_diagnostic": {
            "description": "Diagnostic — +25 Platon/Aristote → R² effondré",
            "n_texts_total": len(all_texts) if include_greek else None,
            "n_pairs": len(xs_b) if include_greek else None,
            "r2": round(r2_b, 6) if include_greek else None,
            "delta_r2": round(r2_b - R2_BASELINE, 6) if include_greek else None,
            "root_cause": (
                "Textes Platon/Aristote connectés au corpus signé UNIQUEMENT via arêtes "
                "'auteur_continu' (coût=1.0) vers aristotle_prior_analytics (seul voisin signé). "
                "Crée des clusters d_topo dégénérés (40+ paires à d_topo≈3.5–5.0 uniforme). "
                "Recommandation §271 : enrichir graphe v19 avec arêtes directes inter-traditions."
            ),
            "greek_added_would_be": [t["graph_node_id"] for t in greek],
            "loo_grouped": loo_b,
            "plato_protagoras_note": (
                "plato_protagoras est dans le corpus §263 mais ISOLÉ dans le graphe (degré=0). "
                "Génère 0 paires, n'affecte pas R²."
            ),
        },
        "exclusions": sorted(EXCLUDED_IDS),
    }
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Rapport §270 → {OUT_REPORT}")

    save_merged_corpus(base_texts, suttas, greek, include_greek=False)  # toujours §270a officiel

    print("\n" + "=" * 60)
    print(f"§270a officiel : {len(base_texts)+len(suttas)} textes, R²={r2_a:.6f} "
          f"({r2_a - R2_BASELINE:+.6f} vs §268c)")
    if include_greek:
        print(f"§270b diagnostic : {len(all_texts)} textes, R²={r2_b:.6f} "
              f"({r2_b - R2_BASELINE:+.6f}) — NE PAS ADOPTER sans enrichissement graphe")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
nipada_resign_evaluate_v272_v17.py  — §272 NiPaDa
═══════════════════════════════════════════════════════════════════════════════
Axes A+B+C : Corpus étendu V16/V17 + évaluation R² + test de permutation

AXE A  — Fix 45 nœuds SuttaCentral
  Intègre signed_corpus_v235_suttacentral_collections.json (27 textes récupérés)
  en les re-signant avec V16 et V17 depuis le cache suttacentral/{work_id}.txt.
  Corpus étendu (disque) : 102 textes (75 + 27).
  Corpus R² (calcul)     :  79 textes (75 + 4 suttas individuels)
  → Les 23 textes de type «collection» (concaténations de dizaines de suttas)
    ont des profils lexicaux dilués qui détruisent la corrélation ; ils sont
    sauvegardés mais exclus du calcul de R².

AXE B  — V17 = V16 + MENTAL_STATE
  Importe V17_ATOMS + MENTAL_STATE du lexique de nipada_fetch_corpus_v212f.py
  Re-signe les 75 textes du corpus principal.
  R² calculé sur 75 docs V16 (baseline) et 75 docs V17 (effet pur Axe B).
  R² calculé aussi sur 79 docs V16/V17 (Axe A+B).

AXE C  — Test de permutation R²
  1000 shuffles de l'assignation nœud→signature dans le corpus.
  Pour chaque shuffle : recalcule R²(d_lex, d_topo).
  p-value = P(R²_shuffled ≥ R²_observé).
  z-score = (R²_obs − μ_shuffled) / σ_shuffled.

Sorties :
  nipada/corpus/signed_corpus_v272_v16_extended.json   (102 docs, 16 atoms)
  nipada/corpus/signed_corpus_v272_v17_extended.json   (102 docs, 17 atoms)
  nipada/falsification/r2_v16v17_extended_graph_v20.json
  nipada/falsification/permutation_test_v272_v17.json

Graphe : nipada_v272_graph_v20.json (1800 nœuds, 23003 arêtes)
VOPT   : {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

Usage :
  cd /home/stephane/GitHub/Panini-Research
  python3 /home/stephane/GitHub/Panini/scripts/nipada_resign_evaluate_v272_v17.py
"""

import heapq
import json
import math
import random
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT    = Path("/home/stephane/GitHub/Panini-Research")
SCRIPTS_DIR  = Path("/home/stephane/GitHub/Panini/scripts")

CORPUS_V14       = REPO_ROOT / "nipada/corpus/signed_corpus_v212f.json"
CORPUS_V16_MAIN  = REPO_ROOT / "nipada/corpus/signed_corpus_v272_v16.json"
CORPUS_V235      = REPO_ROOT / "nipada/corpus/signed_corpus_v235_suttacentral_collections.json"
GRAPH_V20        = REPO_ROOT / "nipada/falsification/nipada_v272_graph_v20.json"

CACHE_SC         = REPO_ROOT / "nipada/corpus/_cache/suttacentral"
CACHE_ST         = REPO_ROOT / "nipada/corpus/_cache/sacred_texts"

CORPUS_V16_EXT   = REPO_ROOT / "nipada/corpus/signed_corpus_v272_v16_extended.json"
CORPUS_V17_EXT   = REPO_ROOT / "nipada/corpus/signed_corpus_v272_v17_extended.json"
R2_REPORT        = REPO_ROOT / "nipada/falsification/r2_v16v17_extended_graph_v20.json"
PERM_REPORT      = REPO_ROOT / "nipada/falsification/permutation_test_v272_v17.json"

# ─── Import lexicon from v212f ────────────────────────────────────────────────
sys.path.insert(0, str(SCRIPTS_DIR))
from nipada_fetch_corpus_v212f import (  # noqa: E402
    ATOM_LEXICON_ENG,
    V14_ATOMS,
    V16_ATOMS,
    V17_ATOMS,
)

# ─── VOPT weights ─────────────────────────────────────────────────────────────
VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

N_PERMUTATIONS = 1000

# ═══════════════════════════════════════════════════════════════════════════════
# Part 0 — V16/V17 frequency signature
# ═══════════════════════════════════════════════════════════════════════════════

# Build lookup  word → list of atoms  (using the full V17 lexicon)
_WORD_TO_ATOMS: dict[str, list[str]] = {}
for _atom, _words in ATOM_LEXICON_ENG.items():
    for _w in _words:
        _WORD_TO_ATOMS.setdefault(_w, []).append(_atom)


def freq_signature(text: str, atoms: list[str]) -> dict[str, float]:
    """
    Compute signature for *atoms* (V16 or V17) from plain text.
    Only counts hits for atoms in the given list (subset of lexicon).
    Normalises to L1 = 1.0 ; uniform fallback if no hits.
    """
    tokens = re.findall(r"[a-z]+", text.lower())
    counts: Counter = Counter()
    total = 0
    atom_set = set(atoms)
    for tok in tokens:
        for atom in _WORD_TO_ATOMS.get(tok, []):
            if atom in atom_set:
                counts[atom] += 1
                total += 1
    n = len(atoms)
    if total == 0:
        return {a: 1.0 / n for a in atoms}
    sig = {a: counts.get(a, 0) / total for a in atoms}
    return sig


# ═══════════════════════════════════════════════════════════════════════════════
# Part 1 — Text loader from cache
# ═══════════════════════════════════════════════════════════════════════════════

def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def load_text(local_id: str, source: str) -> str | None:
    """Load cached text for a document (v212f convention)."""
    # 1. Direct cache file
    if source == "suttacentral":
        f = CACHE_SC / f"{local_id}.txt"
    else:
        f = CACHE_ST / f"{local_id}.txt"

    if f.exists():
        raw = f.read_text(encoding="utf-8", errors="replace")
        return _strip_html(raw)

    # 2. Sacred-texts: try v237_* fragment files (Upanishads)
    if source == "sacred_texts":
        frags = sorted(CACHE_ST.glob(f"v237_{local_id}_*.htm"))
        if frags:
            parts = []
            for frag in frags:
                parts.append(_strip_html(frag.read_text(encoding="utf-8", errors="replace")))
            return " ".join(parts) if parts else None

    return None


# ═══════════════════════════════════════════════════════════════════════════════
# Part 2 — Build extended corpus (75 main + 27 SC collections)
# ═══════════════════════════════════════════════════════════════════════════════

def build_extended_corpus() -> tuple[list[dict], list[dict]]:
    """
    Returns (entries_v16, entries_v17) — parallel lists with same order.
    Each entry is a dict ready for saving in signed_corpus format.
    """
    # --- Load main V16 corpus (75 docs, pre-signed with V16) ---
    raw_v16 = json.loads(CORPUS_V16_MAIN.read_text(encoding="utf-8"))
    main_entries = raw_v16["signed"]

    # --- Load v235 SC collections (27 docs, pre-signed with V14 only) ---
    raw_v235 = json.loads(CORPUS_V235.read_text(encoding="utf-8"))
    sc_entries = raw_v235["signed"]  # keys: local_id, v14_signature, …

    entries_v16: list[dict] = []
    entries_v17: list[dict] = []
    missing_text = []

    # ── Process main corpus ─────────────────────────────────────────────────
    print(f"\n[main corpus] {len(main_entries)} documents")
    for e in main_entries:
        local_id = e["local_id"]
        source   = e.get("source", "suttacentral")

        # Load raw text from cache to recompute V17
        text = load_text(local_id, source)
        if text is None:
            # V16 is pre-computed; for V17 we need the text — flag and skip
            missing_text.append(local_id)
            print(f"  WARN: no cache for {local_id} (source={source})")
            # Fallback: project V16 sig (MENTAL_STATE=0) for this doc
            v16_sig = e["v16_signature"]
            v17_sig = {a: v16_sig.get(a, 0.0) for a in V16_ATOMS}
            total_v16 = sum(v16_sig.values())
            # Renormalise V17 (add MENTAL_STATE=0 → renorm stays identical)
            v17_sig["MENTAL_STATE"] = 0.0
            v17_total = sum(v17_sig.values())
            v17_sig = {a: v17_sig[a] / v17_total if v17_total else 1.0/17 for a in V17_ATOMS}
        else:
            v16_sig = freq_signature(text, V16_ATOMS)
            v17_sig = freq_signature(text, V17_ATOMS)

        base = {k: v for k, v in e.items() if k not in ("v16_signature", "v16_top3")}

        entry_v16 = {**base,
                     "v16_signature": v16_sig,
                     "v16_top3": sorted(v16_sig.items(), key=lambda x: -x[1])[:3]}
        entry_v17 = {**base,
                     "v17_signature": v17_sig,
                     "v17_top3": sorted(v17_sig.items(), key=lambda x: -x[1])[:3]}

        entries_v16.append(entry_v16)
        entries_v17.append(entry_v17)

    # ── Process v235 SC collections ─────────────────────────────────────────
    print(f"\n[v235 SC collections] {len(sc_entries)} documents")
    for e in sc_entries:
        local_id = e["local_id"]

        text = load_text(local_id, "suttacentral")
        if text is None:
            missing_text.append(local_id)
            print(f"  WARN: no cache for SC collection {local_id}")
            continue  # Skip — no text means no reliable signature

        v16_sig = freq_signature(text, V16_ATOMS)
        v17_sig = freq_signature(text, V17_ATOMS)

        base = {
            "local_id":      local_id,
            "graph_node_id": e.get("graph_node_id", local_id),
            "catalog":       e.get("catalog", "buddhist_axial"),
            "tradition_label": e.get("tradition_label", "Buddhist"),
            "lang":          "eng",
            "n_chars":       e.get("n_chars", 0),
            "n_words":       e.get("n_words", 0),
            "matched":       e.get("matched", True),
            "lexicon_version": "v212f",
            "source":        "suttacentral",
            "sc_uid":        e.get("sc_uid", ""),
            "corpus_origin": "v235_sc_collections",
        }

        entry_v16 = {**base,
                     "v16_signature": v16_sig,
                     "v16_top3": sorted(v16_sig.items(), key=lambda x: -x[1])[:3]}
        entry_v17 = {**base,
                     "v17_signature": v17_sig,
                     "v17_top3": sorted(v17_sig.items(), key=lambda x: -x[1])[:3]}

        entries_v16.append(entry_v16)
        entries_v17.append(entry_v17)
        print(f"  ✓ {local_id:40s}  V17 top1 = {entry_v17['v17_top3'][0]}")

    if missing_text:
        print(f"\n  WARN: {len(missing_text)} docs without cached text: {missing_text[:5]}")

    print(f"\nExtended corpus: {len(entries_v16)} docs (V16), {len(entries_v17)} docs (V17)")
    return entries_v16, entries_v17


# ═══════════════════════════════════════════════════════════════════════════════
# Part 3 — Graph (Dijkstra)
# ═══════════════════════════════════════════════════════════════════════════════

def classify_edge(edge: dict) -> str:
    """Classify edge type → VOPT key."""
    etype = edge.get("type", "indirect").lower()
    if etype == "translation":
        return "translation"
    if etype == "direct":
        return "direct"
    return "indirect"


def build_adj(edges: list[dict]) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        u = e.get("src") or e.get("source")
        v = e.get("tgt") or e.get("target")
        if not u or not v:
            continue
        w = VOPT[classify_edge(e)]
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def dijkstra(adj: dict, source: str) -> dict[str, float]:
    dist = {source: 0.0}
    heap = [(0.0, source)]
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


def load_graph() -> dict[str, list[tuple[str, float]]]:
    g = json.loads(GRAPH_V20.read_text(encoding="utf-8"))
    edges = g["edges"]
    print(f"[graph] {len(g.get('nodes', {}))} nodes, {len(edges)} edges (v20)")
    return build_adj(edges)


# ═══════════════════════════════════════════════════════════════════════════════
# Part 4 — R² computation
# ═══════════════════════════════════════════════════════════════════════════════

def l2_distance(sig1: dict, sig2: dict, atoms: list[str]) -> float:
    return math.sqrt(sum((sig1.get(a, 0) - sig2.get(a, 0)) ** 2 for a in atoms))


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
    r = num / (dx * dy)
    return r * r


def compute_r2(entries: list[dict], sig_key: str, atoms: list[str],
               adj: dict) -> dict:
    """
    Compute R²(d_lex, d_topo) for all reachable pairs in *entries*.

    Returns dict with r2, n_pairs, and auxiliary arrays.
    """
    # Build node→signature index
    node_sig: dict[str, dict] = {}
    for e in entries:
        nid = e["graph_node_id"]
        sig = e.get(sig_key)
        if sig:
            node_sig[nid] = sig

    node_ids = list(node_sig.keys())
    n = len(node_ids)

    # Compute Dijkstra from each node
    print(f"  [dijkstra] {n} nodes …")
    d_topo_full: dict[str, dict[str, float]] = {}
    for nid in node_ids:
        d_topo_full[nid] = dijkstra(adj, nid)

    d_lex_list: list[float] = []
    d_topo_list: list[float] = []
    pairs_list: list[tuple[str, str]] = []

    for i in range(n):
        for j in range(i + 1, n):
            u = node_ids[i]
            v = node_ids[j]
            d_t = d_topo_full[u].get(v, math.inf)
            if not math.isfinite(d_t):
                continue
            d_l = l2_distance(node_sig[u], node_sig[v], atoms)
            d_lex_list.append(d_l)
            d_topo_list.append(d_t)
            pairs_list.append((u, v))

    r2 = pearson_r2(d_lex_list, d_topo_list)
    print(f"  R² = {r2:.6f}  ({len(d_lex_list)} pairs)")
    return {
        "r2": round(r2, 6),
        "n_pairs": len(d_lex_list),
        "n_nodes": n,
        "d_lex":   d_lex_list,
        "d_topo":  d_topo_list,
        "pairs":   pairs_list,      # (u,v) in same order as d_lex/d_topo
        "node_ids": node_ids,
        "node_sig": node_sig,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Part 5 — Permutation test
# ═══════════════════════════════════════════════════════════════════════════════

def permutation_test(
    node_ids: list[str],
    node_sig: dict[str, dict],
    adj: dict,
    atoms: list[str],
    d_topo: list[float],
    pairs: list[tuple[str, str]],
    n_perm: int = N_PERMUTATIONS,
    rng_seed: int = 42,
) -> dict:
    """
    Permutation test on R²:
    - Shuffle the assignment node→signature *n_perm* times.
    - Recompute R² for each shuffle using the same pairs and topo distances.
    Returns dict with r2_shuffled list, p_value, z_score.
    """
    rng = random.Random(rng_seed)
    sigs = list(node_sig.values())
    r2_shuffled = []

    # Pre-build (u,v)→topo_idx
    pair_topo = dict(zip([(u, v) for u, v in pairs], d_topo))

    print(f"\n[permutation] {n_perm} shuffles …")
    for k in range(n_perm):
        if (k + 1) % 200 == 0:
            print(f"  … {k+1}/{n_perm}")
        # Shuffle: reassign signatures to node IDs randomly
        shuffled_sigs = sigs[:]
        rng.shuffle(shuffled_sigs)
        perm_node_sig = dict(zip(node_ids, shuffled_sigs))

        d_lex_perm: list[float] = []
        d_topo_perm: list[float] = []
        for (u, v), dt in pair_topo.items():
            dl = l2_distance(perm_node_sig.get(u, {}), perm_node_sig.get(v, {}), atoms)
            d_lex_perm.append(dl)
            d_topo_perm.append(dt)

        r2_shuffled.append(pearson_r2(d_lex_perm, d_topo_perm))

    return r2_shuffled


def summarize_permutation(r2_obs: float, r2_shuffled: list[float]) -> dict:
    valid = [x for x in r2_shuffled if not math.isnan(x)]
    mu = sum(valid) / len(valid)
    var = sum((x - mu) ** 2 for x in valid) / len(valid)
    sigma = math.sqrt(var) if var > 0 else 0.0
    p_value = sum(1 for x in valid if x >= r2_obs) / len(valid)
    z_score = (r2_obs - mu) / sigma if sigma > 0 else float("inf")
    pct95 = sorted(valid)[int(0.95 * len(valid))]
    pct99 = sorted(valid)[int(0.99 * len(valid))]
    return {
        "r2_observed": round(r2_obs, 6),
        "n_permutations": len(r2_shuffled),
        "p_value": round(p_value, 4),
        "z_score": round(z_score, 3),
        "mu_shuffled": round(mu, 6),
        "sigma_shuffled": round(sigma, 6),
        "pct95": round(pct95, 6),
        "pct99": round(pct99, 6),
        "r2_shuffled_min": round(min(valid), 6),
        "r2_shuffled_max": round(max(valid), 6),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    t0 = datetime.now()
    print("=" * 70)
    print("§272 NiPaDa — Axes A+B+C : V17 extended corpus + R² + permutation")
    print(f"Date : {t0.isoformat(timespec='seconds')}")
    print("=" * 70)

    # ── PHASE 1 : Build extended corpus ──────────────────────────────────────
    print("\n─── PHASE 1 : Re-signing corpus ─────────────────────────────────────")
    entries_v16, entries_v17 = build_extended_corpus()

    # ── Save V16 extended corpus ──────────────────────────────────────────────
    corpus_v16_out = {
        "version": "v272_v16_extended",
        "date": t0.strftime("%Y-%m-%d"),
        "description": "V16 extended: 75 main docs + 27 SC collections (Axe A)",
        "atoms": V16_ATOMS,
        "n_atoms": len(V16_ATOMS),
        "n_signed": len(entries_v16),
        "signed": entries_v16,
    }
    CORPUS_V16_EXT.write_text(
        json.dumps(corpus_v16_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote: {CORPUS_V16_EXT.name}  ({len(entries_v16)} docs)")

    # ── Save V17 extended corpus ──────────────────────────────────────────────
    corpus_v17_out = {
        "version": "v272_v17_extended",
        "date": t0.strftime("%Y-%m-%d"),
        "description": "V17 extended: 75 main docs + 27 SC collections (Axe A+B)",
        "atoms": V17_ATOMS,
        "n_atoms": len(V17_ATOMS),
        "n_signed": len(entries_v17),
        "signed": entries_v17,
    }
    CORPUS_V17_EXT.write_text(
        json.dumps(corpus_v17_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote: {CORPUS_V17_EXT.name}  ({len(entries_v17)} docs)")

    # ── PHASE 2 : Load graph ──────────────────────────────────────────────────
    print("\n─── PHASE 2 : Load graph v20 ────────────────────────────────────────")
    adj = load_graph()

    # ── PHASE 3 : R² evaluation ───────────────────────────────────────────────
    print("\n─── PHASE 3 : R² evaluation ─────────────────────────────────────────")

    # A) Baseline: V16 main (75 docs)
    print("\n[V16 main, 75 docs — baseline]")
    raw_v16_main = json.loads(CORPUS_V16_MAIN.read_text(encoding="utf-8"))
    r2_v16_main = compute_r2(raw_v16_main["signed"], "v16_signature", V16_ATOMS, adj)

    # B) V17 main (75 docs) — isolates Axe B effect on the same nodes
    print("\n[V17 main, 75 docs — Axe B effet pur]")
    # Re-sign the 75 main entries with V17 from in-memory entries_v17
    entries_v17_main = [e for e in entries_v17
                        if e.get("corpus_origin") != "v235_sc_collections"]
    r2_v17_main = compute_r2(entries_v17_main, "v17_signature", V17_ATOMS, adj)

    # C) V16 + 4 individual SC suttas (79 docs) — Axe A minimal extension
    #    Only include fetch_type="individual" from v235 (not large collections)
    raw_v235 = json.loads(CORPUS_V235.read_text(encoding="utf-8"))
    individual_ids = {e["local_id"]
                      for e in raw_v235["signed"]
                      if e.get("fetch_type") == "individual"}
    entries_v16_ext79 = [e for e in entries_v16
                         if e.get("corpus_origin") != "v235_sc_collections"
                         or e["local_id"] in individual_ids]
    entries_v17_ext79 = [e for e in entries_v17
                         if e.get("corpus_origin") != "v235_sc_collections"
                         or e["local_id"] in individual_ids]
    n_ext79 = len(entries_v16_ext79)
    print(f"\n[V16 extended-79, {n_ext79} docs — Axe A: 75 + 4 individual suttas]")
    r2_v16_ext79 = compute_r2(entries_v16_ext79, "v16_signature", V16_ATOMS, adj)

    print(f"\n[V17 extended-79, {n_ext79} docs — Axe A+B]")
    r2_v17_ext79 = compute_r2(entries_v17_ext79, "v17_signature", V17_ATOMS, adj)

    # ── PHASE 4 : Permutation tests ───────────────────────────────────────────
    print("\n─── PHASE 4 : Permutation test ──────────────────────────────────────")

    # Test on V17_main (75 docs, cleanest test of Axe B statistical significance)
    print("[Permutation on V17 main, 75 docs]")
    r2_shuf_v17_main = permutation_test(
        node_ids=r2_v17_main["node_ids"],
        node_sig=r2_v17_main["node_sig"],
        adj=adj,
        atoms=V17_ATOMS,
        d_topo=r2_v17_main["d_topo"],
        pairs=r2_v17_main["pairs"],          # pairs returned by compute_r2 ✓
        n_perm=N_PERMUTATIONS,
        rng_seed=42,
    )
    perm_v17_main = summarize_permutation(r2_v17_main["r2"], r2_shuf_v17_main)
    print(f"  p-value = {perm_v17_main['p_value']}  z = {perm_v17_main['z_score']}")

    # Test on V16_main (baseline, for comparison with V17)
    print("[Permutation on V16 main, 75 docs]")
    r2_shuf_v16_main = permutation_test(
        node_ids=r2_v16_main["node_ids"],
        node_sig=r2_v16_main["node_sig"],
        adj=adj,
        atoms=V16_ATOMS,
        d_topo=r2_v16_main["d_topo"],
        pairs=r2_v16_main["pairs"],
        n_perm=N_PERMUTATIONS,
        rng_seed=42,
    )
    perm_v16_main = summarize_permutation(r2_v16_main["r2"], r2_shuf_v16_main)
    print(f"  p-value = {perm_v16_main['p_value']}  z = {perm_v16_main['z_score']}")

    # ── PHASE 5 : Save reports ────────────────────────────────────────────────
    print("\n─── PHASE 5 : Saving reports ────────────────────────────────────────")

    elapsed = (datetime.now() - t0).total_seconds()

    r2_report = {
        "version": "v272_v16v17_extended",
        "date": t0.strftime("%Y-%m-%d"),
        "graph": "nipada_v272_graph_v20.json",
        "vopt": VOPT,
        "elapsed_s": round(elapsed, 1),
        "note_axe_a": (
            "27 SC texts saved in extended corpus (102 docs). "
            "23 large collections excluded from R² (diluted signatures). "
            "ext79 = 75 main + 4 individual suttas."
        ),
        # ── Baseline V16 (75 docs) ──
        "r2_v16_main_75": {
            "r2": r2_v16_main["r2"],
            "n_pairs": r2_v16_main["n_pairs"],
            "n_nodes": r2_v16_main["n_nodes"],
            "note": "baseline V16 (75 docs)",
        },
        # ── Axe B : V17 on same 75 docs ──
        "r2_v17_main_75": {
            "r2": r2_v17_main["r2"],
            "n_pairs": r2_v17_main["n_pairs"],
            "n_nodes": r2_v17_main["n_nodes"],
            "delta_vs_v16_main": round(r2_v17_main["r2"] - r2_v16_main["r2"], 6),
            "note": "V17 + MENTAL_STATE on 75 docs (Axe B isolé)",
        },
        # ── Axe A : V16 + 4 individual suttas (79 docs) ──
        "r2_v16_ext79": {
            "r2": r2_v16_ext79["r2"],
            "n_pairs": r2_v16_ext79["n_pairs"],
            "n_nodes": r2_v16_ext79["n_nodes"],
            "delta_vs_v16_main": round(r2_v16_ext79["r2"] - r2_v16_main["r2"], 6),
            "note": "V16 + 4 individual SC suttas (Axe A minimal)",
        },
        # ── Axe A+B : V17 + 4 individual suttas (79 docs) ──
        "r2_v17_ext79": {
            "r2": r2_v17_ext79["r2"],
            "n_pairs": r2_v17_ext79["n_pairs"],
            "n_nodes": r2_v17_ext79["n_nodes"],
            "delta_vs_v16_main": round(r2_v17_ext79["r2"] - r2_v16_main["r2"], 6),
            "delta_vs_v17_main": round(r2_v17_ext79["r2"] - r2_v17_main["r2"], 6),
            "note": "V17 + 4 individual SC suttas (Axe A+B)",
        },
        # ── Axe C : permutation results ──
        "permutation_v17_main": perm_v17_main,
        "permutation_v16_main": perm_v16_main,
    }

    R2_REPORT.write_text(
        json.dumps(r2_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote: {R2_REPORT.name}")

    perm_report = {
        "version": "v272_permutation_v17",
        "date": t0.strftime("%Y-%m-%d"),
        "n_permutations": N_PERMUTATIONS,
        "rng_seed": 42,
        "V17_main_75": perm_v17_main,
        "V16_main_75": perm_v16_main,
        "r2_shuffled_v17_main": [round(x, 6) for x in r2_shuf_v17_main],
        "r2_shuffled_v16_main": [round(x, 6) for x in r2_shuf_v16_main],
    }
    PERM_REPORT.write_text(
        json.dumps(perm_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote: {PERM_REPORT.name}")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("RÉSULTATS §272 NiPaDa — H₀ = d_lex ∝ d_topo")
    print("=" * 70)
    print(f"  V16 main  (75 docs)   R² = {r2_v16_main['r2']:.6f}"
          f"  ({r2_v16_main['n_pairs']} paires)")
    print(f"  V17 main  (75 docs)   R² = {r2_v17_main['r2']:.6f}"
          f"  ({r2_v17_main['n_pairs']} paires)"
          f"  Δ(V17−V16) = {r2_v17_main['r2'] - r2_v16_main['r2']:+.6f}")
    print(f"  V16 ext79 (79 docs)   R² = {r2_v16_ext79['r2']:.6f}"
          f"  ({r2_v16_ext79['n_pairs']} paires)"
          f"  Δ(A)      = {r2_v16_ext79['r2'] - r2_v16_main['r2']:+.6f}")
    print(f"  V17 ext79 (79 docs)   R² = {r2_v17_ext79['r2']:.6f}"
          f"  ({r2_v17_ext79['n_pairs']} paires)"
          f"  Δ(A+B)    = {r2_v17_ext79['r2'] - r2_v16_main['r2']:+.6f}")
    print(f"\n  Permutation V17 main: p = {perm_v17_main['p_value']}"
          f"  z = {perm_v17_main['z_score']}"
          f"  μ_null = {perm_v17_main['mu_shuffled']:.4f}")
    print(f"  Permutation V16 main: p = {perm_v16_main['p_value']}"
          f"  z = {perm_v16_main['z_score']}")
    print(f"\n  Corpus disque : {len(entries_v16)} docs (V16 étendu / 102 total)")
    print(f"  Durée totale  : {elapsed:.1f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()

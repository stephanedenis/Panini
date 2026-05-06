#!/usr/bin/env python3
"""
nipada_tradition_out_cv.py  —  §261 / Chantier #4
Tradition-out cross-validation for the NiPaDa v260 corpus.

For each tradition fold, ALL texts belonging to that tradition are excluded
from the signed corpus, then R² is re-evaluated on the remaining texts.
A strong R² on each fold proves the signal is not an artefact of any single
tradition dominating the corpus.

Output: nipada/falsification/tradition_out_cv_v260.json
        (also prints a Markdown table for direct insertion into §10/§11)

Usage:
    python3 nipada_tradition_out_cv.py [--output PATH]
"""

import json
import sys
import argparse
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent.parent / "Panini-Research"
SCRIPTS = Path(__file__).resolve().parent

GRAPH_FILE    = REPO / "nipada/falsification/nipada_v258_graph_v15s.json"
# The §260 R²=0.8231 baseline uses the merged c212+c245 corpus
# (v260 fusion contains 13 re-signed texts with a newer lexicon that gives R²=0.6718)
CORPUS_V212F  = REPO / "nipada/corpus/signed_corpus_v212f.json"
CORPUS_V245   = REPO / "nipada/corpus/signed_corpus_v245_100textes.json"
# v260 fusion used for tradition_label and metadata lookup only
CORPUS_V260   = REPO / "nipada/corpus/signed_corpus_v260_fusion.json"
DEFAULT_OUT   = REPO / "nipada/falsification/tradition_out_cv_v260.json"

VOPT = {"direct": 0.05, "translation": 0.05, "indirect": 1.0}

# Western rationalist/materialist texts have tradition_label = None in v260
WESTERN_MATERIALIST_IDS = {
    "plato_protagoras", "aristotle_prior_analytics", "ibn_rawandi_fragments",
    "epicurus_letters", "marx_critique", "sextus_pyrrho", "volney_ruines",
    "voltaire_candide", "democritus_fragments", "spinoza_ttp",
    "paine_age_of_reason", "hume_enquiry", "hume_dialogues_nhr",
    "holbach_systeme_en", "ingersoll_works",
}

# ---------------------------------------------------------------------------
# Re-use existing revalidation primitives
# ---------------------------------------------------------------------------
sys.path.insert(0, str(SCRIPTS))
from nipada_revalidation_v231 import build_adjacency, eval_corpus


def load_data():
    graph   = json.loads(GRAPH_FILE.read_text())
    c212    = json.loads(CORPUS_V212F.read_text())["signed"]
    c245    = json.loads(CORPUS_V245.read_text())["signed"]
    c260    = json.loads(CORPUS_V260.read_text())["signed"]

    # Build merged corpus (c245 wins collisions) — reproduces R²=0.8231 baseline
    merged_map: dict = {}
    for e in c212:
        merged_map[e["graph_node_id"]] = e
    for e in c245:
        merged_map[e["graph_node_id"]] = e

    # Graft v260 tradition_labels onto merged entries (some entries lacked them)
    trad_from_v260 = {e["graph_node_id"]: e.get("tradition_label") for e in c260}
    for nid, entry in merged_map.items():
        if not entry.get("tradition_label") and trad_from_v260.get(nid):
            entry["tradition_label"] = trad_from_v260[nid]

    return graph["edges"], list(merged_map.values())


def tradition_label(entry):
    """Return a canonical tradition string for a corpus entry."""
    tl = entry.get("tradition_label") or ""
    if not tl:
        nid = entry.get("graph_node_id", "")
        if nid in WESTERN_MATERIALIST_IDS:
            return "WESTERN_MATERIALIST"
        return "UNKNOWN"
    return tl


def group_by_tradition(signed):
    groups = {}
    for entry in signed:
        t = tradition_label(entry)
        groups.setdefault(t, []).append(entry)
    return groups


def run_fold(edges, signed_all, excluded_ids, label):
    """Compute R² after removing texts in excluded_ids from signed corpus."""
    remaining = [e for e in signed_all if e["graph_node_id"] not in excluded_ids]
    adj = build_adjacency(edges, VOPT)
    result = eval_corpus(adj, remaining)
    return {
        "fold": label,
        "n_excluded": len(excluded_ids),
        "n_remaining": len(remaining),
        "r2": result["r2"],
        "n_pairs": result["n_pairs_finite"],
        "excluded_ids": sorted(excluded_ids),
    }


def run_baseline(edges, signed_all):
    adj = build_adjacency(edges, VOPT)
    result = eval_corpus(adj, signed_all)
    return {
        "fold": "BASELINE (all 100)",
        "n_excluded": 0,
        "n_remaining": len(signed_all),
        "r2": result["r2"],
        "n_pairs": result["n_pairs_finite"],
        "excluded_ids": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Tradition-out cross-validation §261")
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print("Loading graph and corpus…")
    edges, signed = load_data()
    print(f"  {len(edges)} edges, {len(signed)} signed texts")

    groups = group_by_tradition(signed)
    print(f"\nTradition groups:")
    for t, entries in sorted(groups.items()):
        print(f"  {t:40s}  n={len(entries)}")

    # Only fold traditions with ≥ 2 texts (singleton folds are noise)
    foldable = {t: entries for t, entries in groups.items() if len(entries) >= 2}
    # Also test: all non-Buddhist (the biggest possible bias check)
    non_buddhist_ids = {
        e["graph_node_id"] for e in signed
        if tradition_label(e) != "BUDDHIST_AXIAL"
    }

    print(f"\nRunning {len(foldable) + 2} folds…")
    results = []

    # Baseline
    bl = run_baseline(edges, signed)
    results.append(bl)
    print(f"  {'BASELINE':42s}  R²={bl['r2']:.4f}  n={bl['n_pairs']}")

    # Per-tradition folds (exclude one tradition at a time)
    for t in sorted(foldable.keys()):
        excluded_ids = {e["graph_node_id"] for e in foldable[t]}
        fold = run_fold(edges, signed, excluded_ids, f"exclude_{t}")
        results.append(fold)
        delta = fold["r2"] - bl["r2"]
        print(f"  {'exclude ' + t:42s}  R²={fold['r2']:.4f}  Δ={delta:+.4f}  n={fold['n_pairs']}")

    # Special: exclude all non-Buddhist (stress-test for Buddhist dominance)
    fold_nb = run_fold(edges, signed, non_buddhist_ids, "BUDDHIST_ONLY")
    results.append(fold_nb)
    delta_nb = fold_nb["r2"] - bl["r2"]
    print(f"  {'BUDDHIST_ONLY (excl. all non-Buddhist)':42s}  R²={fold_nb['r2']:.4f}  Δ={delta_nb:+.4f}  n={fold_nb['n_pairs']}")

    elapsed = time.time() - t0

    output = {
        "meta": {
            "script": "nipada_tradition_out_cv.py",
            "section": "§261",
            "corpus_file": f"{CORPUS_V212F} + {CORPUS_V245}",
            "graph_file": str(GRAPH_FILE),
            "n_texts_total": len(signed),
            "n_edges": len(edges),
            "v_opt": VOPT,
            "elapsed_s": round(elapsed, 1),
        },
        "folds": results,
    }

    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nOutput: {out_path}")
    print(f"Elapsed: {elapsed:.1f}s")

    # Markdown summary table
    print("\n---")
    print("| Fold | n_textes_restants | n_paires | R² | Δ vs baseline |")
    print("|------|------------------|----------|----|---------------|")
    baseline_r2 = results[0]["r2"]
    for r in results:
        delta_str = "" if r["fold"].startswith("BASELINE") else f"{r['r2'] - baseline_r2:+.4f}"
        print(f"| {r['fold']} | {r['n_remaining']} | {r['n_pairs']} | {r['r2']:.4f} | {delta_str} |")


if __name__ == "__main__":
    main()

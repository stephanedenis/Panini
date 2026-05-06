#!/usr/bin/env python3
"""
§260-build: Fusion corpus v260 — v245 (100 textes) with §237 upanishad corrections.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01

Problem:
  signed_corpus_v245_100textes.json inherits 13 buggy upanishad signatures from
  signed_corpus_v212f.json (the volume-collision bug: all SBE01 upanishads got
  the same text, and all SBE15 upanishads got the same text).

Fix:
  Replace the 13 buggy upanishad entries in the v212f base with the correctly
  fetched entries from signed_corpus_v237_upanishads.json (per-chapter fetch).

Output corpus:
  nipada/corpus/signed_corpus_v260_fusion.json
  - 75 base texts (v212f) with 13 upanishads corrected by v237
  - 25 extension texts (from v245)
  - Total: 100 texts, all with valid distinct V14 signatures

Usage:
  python3 nipada_build_corpus_v260_fusion.py [--verify]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_NIPADA = _HERE.parent.parent / "Panini-Research" / "nipada"
CORPUS_DIR = _NIPADA / "corpus"

V212F_FILE = CORPUS_DIR / "signed_corpus_v212f.json"
V237_FILE = CORPUS_DIR / "signed_corpus_v237_upanishads.json"
V245_FILE = CORPUS_DIR / "signed_corpus_v245_100textes.json"
OUT_FILE = CORPUS_DIR / "signed_corpus_v260_fusion.json"

# The 13 upanishads that must be replaced (v212f's buggy entries)
UPANISHAD_NODE_IDS = {
    # SBE01 group (all had same text = first 30 pages of sbe01/)
    "chandogya_upanishad",
    "kena_upanishad",
    "aitareya_upanishad",
    "kausitaki_upanishad",
    "isa_upanishad",
    # SBE15 group (all had same text = first 30 pages of sbe15/)
    "katha_upanishad",
    "mundaka_upanishad",
    "taittiriya_upanishad",
    "brihadaranyaka_upanishad",
    "svetasvatara_upanishad",
    "prashna_upanishad",
    "maitri_upanishad",
    "mandukya_upanishad",
}


def _v237_to_v212f_schema(entry: dict) -> dict:
    """
    Normalize a v237 upanishad entry to the v212f schema so that the fused
    corpus is schema-consistent throughout.

    v212f schema: {local_id, graph_node_id, catalog, tradition_label, lang,
                   n_chars, n_words, v14_signature, v14_top3, matched,
                   lexicon_version, source, url}
    v237 schema: {graph_node_id, title_en, tradition_label, tradition_micro,
                  language_original, author, year, source_volumes, tags,
                  v14_signature, signed_n_chars, n_chapters_fetched,
                  ingestion_status, script_version, signed_at}
    """
    sig = entry["v14_signature"]
    top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]

    node_id = entry["graph_node_id"]
    n_chars = entry.get("signed_n_chars", 0)
    # Rough word estimate: English prose ≈ 5 chars per word
    n_words = n_chars // 5 if n_chars else 0

    # Source URL from the chapter files (we reconstruct the base URL)
    source_vol = entry.get("source_volumes", "")
    if source_vol == "SBE01":
        url = "https://www.sacred-texts.com/hin/sbe01/index.htm"
    elif source_vol == "SBE15":
        url = "https://www.sacred-texts.com/hin/sbe15/index.htm"
    elif source_vol == "HUME1921":
        url = "https://www.sacred-texts.com/hin/upan/"
    else:
        url = ""

    url_wayback = (f"https://web.archive.org/web/*/" + url) if url else None

    return {
        "local_id": node_id,
        "graph_node_id": node_id,
        "catalog": "indian_axial",
        "tradition_label": entry.get("tradition_label", "INDIAN_AXIAL"),
        "lang": "eng",
        "n_chars": n_chars,
        "n_words": n_words,
        "v14_signature": sig,
        "v14_top3": [[a, v] for a, v in top3],
        "matched": True,
        "lexicon_version": "v14",
        "source": f"sacred-texts.com {source_vol} (§237 per-chapter fix)",
        "url": url,
        "url_original": url or None,
        "url_wayback": url_wayback,
        # Extra provenance fields (not in v212f but harmless to include)
        "title_en": entry.get("title_en", ""),
        "author": entry.get("author", ""),
        "year": entry.get("year"),
        "n_chapters_fetched": entry.get("n_chapters_fetched"),
        "v260_fix": "§212f_volume_collision",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build v260 fusion corpus (v245 + §237 upanishad fix)")
    parser.add_argument("--verify", action="store_true", help="Run verification checks only (no write)")
    args = parser.parse_args()

    # ---- Load source files -------------------------------------------------
    print(f"Loading v212f: {V212F_FILE}")
    with open(V212F_FILE, encoding="utf-8") as f:
        v212f = json.load(f)

    print(f"Loading v237: {V237_FILE}")
    if not V237_FILE.exists():
        print(f"ERROR: {V237_FILE} not found. Run nipada_fetch_corpus_v237_upanishads.py first.")
        sys.exit(1)
    with open(V237_FILE, encoding="utf-8") as f:
        v237 = json.load(f)

    print(f"Loading v245: {V245_FILE}")
    with open(V245_FILE, encoding="utf-8") as f:
        v245 = json.load(f)

    # ---- Build v237 lookup table -------------------------------------------
    v237_by_id = {w["graph_node_id"]: w for w in v237["signed"]}
    print(f"\nv237 upanishads available: {sorted(v237_by_id.keys())}")
    missing_from_v237 = UPANISHAD_NODE_IDS - set(v237_by_id.keys())
    if missing_from_v237:
        print(f"WARNING: {len(missing_from_v237)} upanishads not in v237 (will keep v212f version): {missing_from_v237}")

    # ---- Process v212f base ------------------------------------------------
    corrected_count = 0
    kept_count = 0
    base_texts = []
    for entry in v212f["signed"]:
        node_id = entry["graph_node_id"]
        if node_id in UPANISHAD_NODE_IDS and node_id in v237_by_id:
            # Replace with corrected v237 entry
            corrected = _v237_to_v212f_schema(v237_by_id[node_id])
            base_texts.append(corrected)
            corrected_count += 1
        else:
            base_texts.append(entry)
            kept_count += 1

    print(f"\nv212f base: {kept_count} kept + {corrected_count} corrected = {len(base_texts)} total")

    # ---- Add v245 extensions -----------------------------------------------
    # Check for collisions (v245 extensions should not duplicate v212f base)
    base_ids = {w["graph_node_id"] for w in base_texts}
    extensions = []
    extension_dups = []
    for entry in v245["signed"]:
        if entry["graph_node_id"] in base_ids:
            extension_dups.append(entry["graph_node_id"])
        else:
            extensions.append(entry)

    if extension_dups:
        print(f"WARNING: {len(extension_dups)} v245 extensions already in base (skipped): {extension_dups}")

    all_texts = base_texts + extensions
    print(f"v245 extensions added: {len(extensions)}")
    print(f"Total v260 texts: {len(all_texts)}")

    # ---- Verification ------------------------------------------------------
    # Check signatures are distinct for the upanishads
    print("\n--- Upanishad signature check ---")
    upanishad_sigs = {}
    for w in all_texts:
        if w["graph_node_id"] in UPANISHAD_NODE_IDS:
            sig = w["v14_signature"]
            top1 = max(sig, key=lambda k: sig[k]) if sig else "?"
            n_chars = w.get("n_chars", w.get("signed_n_chars", 0))
            print(f"  {w['graph_node_id']:45s} {n_chars:10,} chars  top: {top1}={sig.get(top1, 0):.3f}")
            sig_key = str(sorted(sig.items()))
            if sig_key in upanishad_sigs:
                print(f"  !! COLLISION with {upanishad_sigs[sig_key]}")
            else:
                upanishad_sigs[sig_key] = w["graph_node_id"]

    n_distinct = len(upanishad_sigs)
    n_total = sum(1 for w in all_texts if w["graph_node_id"] in UPANISHAD_NODE_IDS)
    print(f"\nDistinct signatures: {n_distinct}/{n_total}")
    if n_distinct < n_total:
        print("WARNING: some signatures are still colliding!")
    else:
        print("OK: all upanishad signatures are distinct")

    # ---- Overall uniqueness check ------------------------------------------
    all_sigs = [str(sorted(w["v14_signature"].items())) for w in all_texts]
    n_unique = len(set(all_sigs))
    print(f"\nOverall uniqueness: {n_unique}/{len(all_texts)} distinct signatures")
    if n_unique < len(all_texts):
        # Find which ones collide
        from collections import Counter
        sig_counter = Counter(all_sigs)
        dups = {s: c for s, c in sig_counter.items() if c > 1}
        print(f"  {len(dups)} collision groups:")
        for s, c in list(dups.items())[:5]:
            colliders = [w["graph_node_id"] for w in all_texts if str(sorted(w["v14_signature"].items())) == s]
            print(f"  × {colliders}")

    if args.verify:
        print("\n[--verify mode] No files written.")
        return

    # ---- Write output ------------------------------------------------------
    out = {
        "version": "v260",
        "description": (
            "Corpus v260: v245 (100 textes) with §237 upanishad corrections. "
            "Fixes the §212f SBE01/SBE15 volume-collision bug: all 13 upanishads "
            "now have individually-fetched per-chapter signatures. "
            f"Sources: v212f ({kept_count} base), v237 ({corrected_count} upanishad fixes), "
            f"v245 ({len(extensions)} extensions)."
        ),
        "generated": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "base": "signed_corpus_v212f.json",
            "upanishad_fix": "signed_corpus_v237_upanishads.json",
            "extensions": "signed_corpus_v245_100textes.json",
        },
        "n_texts": len(all_texts),
        "n_corrected_upanishads": corrected_count,
        "n_extensions": len(extensions),
        "bug_fixed": "§212f_sbe01_sbe15_volume_collision",
        "lexicon_version": "v14",
        "signed": all_texts,
    }

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    size_kb = OUT_FILE.stat().st_size // 1024
    print(f"\nSaved: {OUT_FILE} ({len(all_texts)} texts, {size_kb} KB)")
    print("\nNext steps:")
    print("  1. Run R² analysis: python3 nipada_analyse_rsquared.py signed_corpus_v260_fusion.json")
    print("  2. Compare R² v245 vs v260 to quantify the fix")
    print("  3. Update graph embeddings if needed")


if __name__ == "__main__":
    main()

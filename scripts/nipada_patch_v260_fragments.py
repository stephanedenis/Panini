#!/usr/bin/env python3
"""
nipada_patch_v260_fragments.py — Chantier #1

Adds `fragments` and `fragments_hash` fields to every entry in
signed_corpus_v260_fusion.json by reading cached source texts from
nipada/corpus/_cache/.

Schema:
  fragments: [
    {"seq": 0, "n_words": N, "hash": "sha256..."},
    ...
  ]
  fragments_hash: sha256(full_text_concatenated)

Fragment text is NOT stored inline; it stays in nipada/corpus/_cache/.
To retrieve fragment k: split cached text by FRAGMENT_WORDS, take index k.

Entries without a resolvable cache file get:
  fragments: null
  fragments_hash: null

Usage:
  python3 nipada_patch_v260_fragments.py [--dry-run]
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_RESEARCH = Path(__file__).resolve().parent.parent.parent / "Panini-Research"
CORPUS_JSON   = REPO_RESEARCH / "nipada/corpus/signed_corpus_v260_fusion.json"
CACHE_ROOT    = REPO_RESEARCH / "nipada/corpus/_cache"
CACHE_ST      = CACHE_ROOT / "sacred_texts"
CACHE_SC      = CACHE_ROOT / "suttacentral"

FRAGMENT_WORDS = 500   # target fragment size in words

# ---------------------------------------------------------------------------
# Manual overrides: corpus local_id → cache path(s) relative to CACHE_ROOT
# ---------------------------------------------------------------------------

MANUAL_CACHE = {
    # Gutenberg – Plato
    "plato_protagoras":         ["pg_1591.txt"],

    # MIT Classics – Aristotle (multiple sections concatenated)
    "aristotle_prior_analytics": [
        "mit_aristotle_prior_analytics_s001.txt",
        "mit_aristotle_prior_analytics_s002.txt",
    ],

    # Upanishads (v237 cache, in sacred_texts/)
    "aitareya_upanishad":      ["sacred_texts/v237_aitareya_upanishad.txt"],
    "brihadaranyaka_upanishad":["sacred_texts/v237_brihadaranyaka_upanishad.txt"],
    "chandogya_upanishad":     ["sacred_texts/v237_chandogya_upanishad.txt"],
    "isa_upanishad":           ["sacred_texts/v237_isa_upanishad.txt"],
    "katha_upanishad":         ["sacred_texts/v237_katha_upanishad.txt"],
    "kausitaki_upanishad":     ["sacred_texts/v237_kausitaki_upanishad.txt"],
    "kena_upanishad":          ["sacred_texts/v237_kena_upanishad.txt"],
    "maitri_upanishad":        ["sacred_texts/v237_maitri_upanishad.txt"],
    "mandukya_upanishad":      ["sacred_texts/v237_mandukya_upanishad.txt"],
    "mundaka_upanishad":       ["sacred_texts/v237_mundaka_upanishad.txt"],
    "prashna_upanishad":       ["sacred_texts/v237_prashna_upanishad.txt"],
    "svetasvatara_upanishad":  ["sacred_texts/v237_svetasvatara_upanishad.txt"],
    "taittiriya_upanishad":    ["sacred_texts/v237_taittiriya_upanishad.txt"],

    # Chinese classics (v236 cache, in sacred_texts/)
    "daxue":     ["sacred_texts/v236_daxue.txt"],
    "liji":      ["sacred_texts/v236_liji.txt"],
    "yueji":     ["sacred_texts/v236_yueji.txt"],
    "zhongyong": ["sacred_texts/v236_zhongyong.txt"],

    # Alias: Laozi / Tao Te Ching
    "laozi_taoteching_en": ["sacred_texts/daodejing.txt"],

    # §261 Chantier #5 — Gutenberg plain-text fetches (nipada_gutenberg_fetcher.py)
    "burnet_early_greek_philosophy": ["pg_31649.txt"],
    "plato_parmenides":              ["pg_1687.txt"],
    "spinoza_ttp":                   ["pg_989.txt"],
    "paine_age_of_reason":           ["pg_3743.txt"],
    "hume_enquiry":                  ["pg_9662.txt"],
    "hume_dialogues_nhr":            ["pg_4583.txt"],
    "holbach_systeme_en":            ["pg_8909.txt"],
    "ingersoll_works":               ["pg_38802.txt"],
    "volney_ruines":                 ["pg_27931.txt"],
    "voltaire_candide":              ["pg_4650.txt"],
    "marx_critique":                 ["pg_46423.txt"],
    "koran_rodwell_en":              ["pg_16955.txt"],
    "lucretius_drn":                 ["pg_785.txt"],
    "spinoza_ethica_complete":       ["pg_3800.txt"],
    "epicurus_letters":              ["pg_32.txt"],       # Diogenes Laertius X (Bailey)
    "sextus_pyrrho":                 ["pg_sextus_pyrrho.txt"],   # Against the Professors #14417
    "democritus_fragments":          ["pg_democritus.txt"],      # Presocratic anthology #38172
    # ibn_rawandi_fragments: no free plain-text source — remains null
}

# ---------------------------------------------------------------------------
# HTML strip helper (for MIT cache files)
# ---------------------------------------------------------------------------

def _strip_html(raw: str) -> str:
    """Remove HTML tags and decode common entities."""
    text = re.sub(r"<!--.*?-->", " ", raw, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    entities = {"&amp;": "&", "&lt;": "<", "&gt;": ">",
                "&quot;": '"', "&apos;": "'", "&nbsp;": " "}
    for ent, ch in entities.items():
        text = text.replace(ent, ch)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------------------------------------------------------------------
# Cache file resolution
# ---------------------------------------------------------------------------

def _resolve_cache_files(local_id: str) -> list[Path] | None:
    """Return list of cache file Paths for a given corpus local_id, or None."""

    # 1. Manual overrides
    if local_id in MANUAL_CACHE:
        paths = [CACHE_ROOT / rel for rel in MANUAL_CACHE[local_id]]
        existing = [p for p in paths if p.exists()]
        return existing if existing else None

    # 2. Direct match: sacred_texts/{local_id}.txt
    p_st = CACHE_ST / f"{local_id}.txt"
    if p_st.exists():
        return [p_st]

    # 3. Direct match: suttacentral/{local_id}.txt
    p_sc = CACHE_SC / f"{local_id}.txt"
    if p_sc.exists():
        return [p_sc]

    return None

# ---------------------------------------------------------------------------
# Text loading
# ---------------------------------------------------------------------------

def _load_text(paths: list[Path]) -> str:
    """Load and concatenate text from cache paths, stripping HTML if needed."""
    parts = []
    for p in paths:
        raw = p.read_text(encoding="utf-8", errors="replace")
        if raw.lstrip().startswith("<") or "<HTML" in raw[:200].upper():
            raw = _strip_html(raw)
        parts.append(raw)
    return "\n\n".join(parts)

# ---------------------------------------------------------------------------
# Fragment splitting
# ---------------------------------------------------------------------------

def _split_fragments(text: str, target_words: int = FRAGMENT_WORDS) -> list[dict]:
    """Split text into non-overlapping ~target_words fragments."""
    words = text.split()
    if not words:
        return []

    fragments = []
    start = 0
    seq = 0
    while start < len(words):
        end = min(start + target_words, len(words))
        chunk = " ".join(words[start:end])
        h = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
        fragments.append({
            "seq":    seq,
            "n_words": end - start,
            "hash":  h,
            # text NOT stored inline — stays in _cache/
        })
        start = end
        seq += 1
    return fragments

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Add fragments/fragments_hash to v260 corpus")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print stats without writing the file")
    args = parser.parse_args()

    corpus = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
    entries = corpus["signed"]

    n_total   = len(entries)
    n_resolved = 0
    n_null     = 0
    null_ids   = []

    for entry in entries:
        local_id = entry.get("local_id") or entry.get("graph_node_id", "")

        cache_files = _resolve_cache_files(local_id)

        if cache_files:
            text = _load_text(cache_files)
            frags = _split_fragments(text)
            fhash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            entry["fragments"]      = frags
            entry["fragments_hash"] = fhash
            n_resolved += 1
        else:
            entry["fragments"]      = None
            entry["fragments_hash"] = None
            n_null += 1
            null_ids.append(local_id)

    print(f"Corpus entries  : {n_total}")
    print(f"  with fragments: {n_resolved}")
    print(f"  null (no cache): {n_null}")
    if null_ids:
        print("  null IDs:", sorted(null_ids))

    if args.dry_run:
        print("[dry-run] no file written.")
        return

    out = json.dumps(corpus, ensure_ascii=False, indent=2)
    CORPUS_JSON.write_text(out, encoding="utf-8")
    size_kb = CORPUS_JSON.stat().st_size // 1024
    print(f"Written: {CORPUS_JSON}  ({size_kb} KB)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
§260-patch: Add url_original, url_wayback, normalize lexicon_version in v260 corpus.

Chantier #4 + URL fields:
  - Normalize lexicon_version → "v14" for all 100 entries (model version, not corpus script)
  - Add url_original: canonical source URL for the text
  - Add url_wayback:  https://web.archive.org/web/*/[url_original] for archival citation
  - Entries without source URL get null (to be filled manually)

Two entry schemas coexist in v260:
  Type1 (local_id):      'url' field (string)
  Type2 (graph_node_id): 'source_url' field (list of chapter URLs) or absent

Usage:
    python3 nipada_patch_v260_url_fields.py [--dry-run]
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

_HERE = Path(__file__).resolve().parent
_NIPADA = _HERE.parent.parent / "Panini-Research" / "nipada"
CORPUS_DIR = _NIPADA / "corpus"
V260_FILE = CORPUS_DIR / "signed_corpus_v260_fusion.json"

WAYBACK_PREFIX = "https://web.archive.org/web/*/"

# Manual URL overrides for entries that have no URL in the JSON
# (sourced from v208 / internal sign — we know their origin)
MANUAL_URLS: dict[str, str] = {
    # v208 sacred-texts sources
    "koran_rodwell_en":         "https://www.sacred-texts.com/isl/quran/index.htm",
    "lucretius_drn":            "https://www.sacred-texts.com/cla/luc/index.htm",
    "spinoza_ethica_complete":  "https://www.sacred-texts.com/phi/spinoza/index.htm",
    "laozi_taoteching_en":      "https://www.sacred-texts.com/tao/taote.htm",
    # Project Gutenberg sources (v172/v176/v208 batches)
    "plato_protagoras":         "https://www.gutenberg.org/ebooks/1591",
    "marx_critique":            "https://www.gutenberg.org/ebooks/46423",
    "volney_ruines":            "https://www.gutenberg.org/ebooks/27931",
    "voltaire_candide":         "https://www.gutenberg.org/ebooks/4650",
    "spinoza_ttp":              "https://www.gutenberg.org/ebooks/989",
    "paine_age_of_reason":      "https://www.gutenberg.org/ebooks/3743",
    "hume_enquiry":             "https://www.gutenberg.org/ebooks/9662",
    "hume_dialogues_nhr":       "https://www.gutenberg.org/ebooks/4583",
    "holbach_systeme_en":       "https://www.gutenberg.org/ebooks/8909",
    "ingersoll_works":          "https://www.gutenberg.org/ebooks/38802",
    # MIT Classics
    "aristotle_prior_analytics": "https://classics.mit.edu/Aristotle/prior.html",
    # epicurus.net
    "epicurus_letters":         "https://www.epicurus.net/en/letters.html",
    # No stable open source (remain null):
    #   ibn_rawandi_fragments  (Stroumsa 1999, academic only)
    #   democritus_fragments   (Diels-Kranz B, no open stable text)
    #   sextus_pyrrho          (embedded, no original fetch URL)
}


def _derive_url_original(entry: dict) -> str | None:
    """Return the canonical source URL for an entry, or None if unknown."""
    node_id = entry.get("graph_node_id") or entry.get("local_id") or ""

    # Check manual overrides first
    if node_id in MANUAL_URLS:
        return MANUAL_URLS[node_id]

    # Type1 entries have a 'url' field (string)
    url_str = entry.get("url", "")
    if isinstance(url_str, str) and url_str.strip():
        return url_str.strip()

    # Type2 entries may have 'source_url' as a list → use base of first item
    source_url = entry.get("source_url")
    if isinstance(source_url, list) and source_url:
        first = source_url[0]
        # Derive the directory index URL from the first chapter URL
        parsed = urlparse(first)
        # e.g. https://www.sacred-texts.com/cfu/liki/liki01.htm → /cfu/liki/
        base_path = "/".join(parsed.path.split("/")[:-1]) + "/"
        return f"{parsed.scheme}://{parsed.netloc}{base_path}"
    if isinstance(source_url, str) and source_url.strip():
        return source_url.strip()

    return None


def patch_entry(entry: dict) -> dict:
    """Return a new entry dict with normalized lexicon_version + url fields added."""
    patched = dict(entry)

    # 1. Normalize lexicon_version → the actual V14 model (not corpus script version)
    patched["lexicon_version"] = "v14"

    # 2. Derive canonical source URL
    url_original = _derive_url_original(entry)
    patched["url_original"] = url_original

    # 3. WaybackMachine archival URL
    patched["url_wayback"] = (WAYBACK_PREFIX + url_original) if url_original else None

    return patched


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch v260 corpus: url_original, url_wayback, lexicon_version")
    parser.add_argument("--dry-run", action="store_true", help="Print stats only, don't write")
    args = parser.parse_args()

    with open(V260_FILE, encoding="utf-8") as f:
        data = json.load(f)

    original_entries = data["signed"]
    patched_entries = [patch_entry(e) for e in original_entries]

    # Stats
    with_url = sum(1 for e in patched_entries if e["url_original"])
    without_url = sum(1 for e in patched_entries if not e["url_original"])
    lv_dist: dict[str, int] = {}
    for e in original_entries:
        lv = e.get("lexicon_version", "MISSING")
        lv_dist[lv] = lv_dist.get(lv, 0) + 1

    print(f"Entries: {len(patched_entries)}")
    print(f"  url_original resolved: {with_url}")
    print(f"  url_original null    : {without_url}")
    print(f"  lexicon_version before: {lv_dist}")
    print(f"  lexicon_version after : all → 'v14'")

    if without_url:
        print("\n  Entries still without url_original:")
        for e in patched_entries:
            if not e["url_original"]:
                node_id = e.get("graph_node_id") or e.get("local_id", "?")
                print(f"    {node_id}")

    if args.dry_run:
        print("\n[--dry-run] No file written.")
        return

    data["signed"] = patched_entries
    data["patch_v260_urls"] = {
        "applied": datetime.now(timezone.utc).isoformat(),
        "fields_added": ["url_original", "url_wayback"],
        "lexicon_version_normalized": "v14",
        "entries_with_url": with_url,
        "entries_without_url": without_url,
    }

    with open(V260_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    size_kb = V260_FILE.stat().st_size // 1024
    print(f"\nPatched: {V260_FILE} ({size_kb} KB)")


if __name__ == "__main__":
    main()

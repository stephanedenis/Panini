#!/usr/bin/env python3
"""
nipada_gutenberg_fetcher.py  —  §261 / Chantier #5

Downloads plain-text sources for the 18 null-fragment entries in
signed_corpus_v260_fusion.json, saves them to nipada/corpus/_cache/,
and prints the MANUAL_CACHE snippet to add to nipada_patch_v260_fragments.py.

Texts that cannot be resolved are skipped with a warning.

Usage:
    python3 nipada_gutenberg_fetcher.py [--dry-run]
"""

import argparse
import hashlib
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("requests not installed — run: pip install requests")

CACHE_ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "Panini-Research/nipada/corpus/_cache"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NiPaDa-Research/1.0; "
        "+https://github.com/stephanedenis/Panini-Research)"
    )
}

# ---------------------------------------------------------------------------
# Fetch targets
# Each entry: (local_id, cache_filename, url, post_fn)
#   post_fn: None (keep raw) or a callable(str)->str to post-process the text
# ---------------------------------------------------------------------------

def _strip_gutenberg_header(text: str) -> str:
    """Remove Project Gutenberg front- and back-matter."""
    # Try to find start marker
    for marker in [
        "*** START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
        "*END*THE SMALL PRINT",
        "END OF THE PROJECT GUTENBERG",
    ]:
        idx = text.find(marker)
        if idx != -1:
            # Move past the marker line
            rest = text[idx:]
            newline = rest.find("\n")
            if newline != -1:
                text = rest[newline + 1:]
            break
    # Remove back-matter
    for marker in [
        "*** END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "End of Project Gutenberg",
    ]:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    return text.strip()


def _to_pg_url(pg_id: int) -> list[str]:
    """Generate candidate plain-text URLs for a Gutenberg ID."""
    return [
        f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt",
        f"https://www.gutenberg.org/files/{pg_id}/{pg_id}-0.txt",
        f"https://www.gutenberg.org/files/{pg_id}/{pg_id}.txt",
    ]


FETCH_TARGETS: list[dict] = [
    # -- Direct Gutenberg plain text --
    {
        "local_id": "burnet_early_greek_philosophy",
        "cache_file": "pg_31649.txt",
        "urls": _to_pg_url(31649),
    },
    {
        "local_id": "plato_parmenides",
        "cache_file": "pg_1687.txt",
        "urls": _to_pg_url(1687),
    },
    {
        "local_id": "spinoza_ttp",
        "cache_file": "pg_989.txt",
        "urls": _to_pg_url(989),
    },
    {
        "local_id": "paine_age_of_reason",
        "cache_file": "pg_3743.txt",
        "urls": _to_pg_url(3743),
    },
    {
        "local_id": "hume_enquiry",
        "cache_file": "pg_9662.txt",
        "urls": _to_pg_url(9662),
    },
    {
        "local_id": "hume_dialogues_nhr",
        "cache_file": "pg_4583.txt",
        "urls": _to_pg_url(4583),
    },
    {
        "local_id": "holbach_systeme_en",
        "cache_file": "pg_8909.txt",
        "urls": _to_pg_url(8909),
    },
    {
        "local_id": "ingersoll_works",
        "cache_file": "pg_38802.txt",
        "urls": _to_pg_url(38802),
    },
    {
        "local_id": "volney_ruines",
        "cache_file": "pg_27931.txt",
        "urls": _to_pg_url(27931),
    },
    {
        "local_id": "voltaire_candide",
        "cache_file": "pg_4650.txt",
        "urls": _to_pg_url(4650),
    },
    {
        "local_id": "marx_critique",
        "cache_file": "pg_46423.txt",
        "urls": _to_pg_url(46423),
    },
    # -- Koran: Rodwell translation (Sacred Texts index → try Gutenberg #16955 Palmer as fallback) --
    {
        "local_id": "koran_rodwell_en",
        "cache_file": "pg_16955.txt",
        "urls": _to_pg_url(16955),
    },
    # -- Lucretius De Rerum Natura: Munro translation (Gutenberg #785) --
    {
        "local_id": "lucretius_drn",
        "cache_file": "pg_785.txt",
        "urls": _to_pg_url(785),
    },
    # -- Spinoza Ethics: Elwes translation (Gutenberg #3800) --
    {
        "local_id": "spinoza_ethica_complete",
        "cache_file": "pg_3800.txt",
        "urls": _to_pg_url(3800),
    },
    # -- Epicurus Letters: in Diogenes Laertius Book X (Gutenberg #32) --
    {
        "local_id": "epicurus_letters",
        "cache_file": "pg_32.txt",
        "urls": _to_pg_url(32),
    },
    # -- Sextus Empiricus: Outlines of Pyrrhonism (Wikisource / Sacred Texts) --
    {
        "local_id": "sextus_pyrrho",
        "cache_file": "pg_sextus_pyrrho.txt",
        "urls": [
            # Sacred texts has it
            "https://www.gutenberg.org/cache/epub/14417/pg14417.txt",  # Sextus: Against the Professors
            "https://www.gutenberg.org/files/14417/14417-0.txt",
        ],
    },
    # -- Democritus fragments: no Gutenberg; use Bailey via a plain-text mirror --
    {
        "local_id": "democritus_fragments",
        "cache_file": "pg_democritus.txt",
        "urls": [
            # Anaxagoras + Presocratic fragments collection (Burnet overlaps, but this has Democritus)
            "https://www.gutenberg.org/cache/epub/38172/pg38172.txt",
        ],
    },
    # -- Ibn Rawandi: no publicly available plain-text source; skip --
    # {
    #     "local_id": "ibn_rawandi_fragments",
    #     "cache_file": "ibn_rawandi_fragments.txt",
    #     "urls": [],
    # },
]


def fetch_first_successful(urls: list[str], dry_run: bool = False) -> tuple[str | None, str | None]:
    """Try each URL in order; return (content, url_used) or (None, None)."""
    if dry_run:
        return f"[DRY-RUN placeholder for {urls[0]}]", urls[0]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                # Detect encoding
                text = resp.content.decode(resp.apparent_encoding or "utf-8", errors="replace")
                return text, url
            print(f"    HTTP {resp.status_code} for {url}")
        except Exception as exc:
            print(f"    Error fetching {url}: {exc}")
        time.sleep(0.5)
    return None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    successful = []
    failed = []

    for target in FETCH_TARGETS:
        local_id = target["local_id"]
        cache_file = target["cache_file"]
        urls = target["urls"]
        dest = CACHE_ROOT / cache_file

        if dest.exists():
            print(f"[SKIP]    {local_id:45s}  {cache_file} (already cached)")
            successful.append((local_id, cache_file))
            continue

        print(f"[FETCH]   {local_id:45s}  → {cache_file}")
        text, url_used = fetch_first_successful(urls, dry_run=args.dry_run)

        if text is None:
            print(f"  ✗ FAILED — no URL returned content")
            failed.append(local_id)
            continue

        cleaned = _strip_gutenberg_header(text)
        if len(cleaned.split()) < 500:
            print(f"  ✗ Text too short ({len(cleaned.split())} words) — skipping")
            failed.append(local_id)
            continue

        if not args.dry_run:
            dest.write_text(cleaned, encoding="utf-8")
        sha = hashlib.sha256(cleaned.encode()).hexdigest()[:12]
        print(f"  ✓ {len(cleaned.split()):,} words — sha256={sha}… — from {url_used}")
        successful.append((local_id, cache_file))
        time.sleep(1.0)  # polite crawl delay

    print(f"\n{'='*60}")
    print(f"Fetched: {len(successful)}  Failed: {len(failed)}")
    if failed:
        print(f"Still null: {failed}")

    print("\n# --- Add to MANUAL_CACHE in nipada_patch_v260_fragments.py ---")
    for local_id, cache_file in successful:
        print(f'    "{local_id}": ["{cache_file}"],')


if __name__ == "__main__":
    main()

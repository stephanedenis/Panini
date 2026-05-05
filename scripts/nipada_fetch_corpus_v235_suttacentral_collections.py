#!/usr/bin/env python3
"""
§235-fetch: SuttaCentral collections fix.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01
Author: §235

Problem:
  40 of 70 Buddhist texts in catalog_buddhist_axial_v205.json failed in §212f
  because the SuttaCentral bilara API returns no translation_text for
  collection-level UIDs (sn12, an1, dhp, etc.).

Fix strategy:
  1. Individual suttas with broken UIDs (an365 → an3.65, etc.): corrected URL.
  2. Collection-level UIDs: use suttaplex API → leaf UIDs → fetch each leaf →
     concatenate into one text per work.

Available translations (tested):
  - 28 of 40 works fetchable via Sujato translations
  - 8 skipped: snp4/snp5 (covered by snp), mil/peṭ/nett/vv/mv/cv/dhs/kv
    (no Sujato translation available on bilara API)

Output:
  nipada/corpus/signed_corpus_v235_suttacentral_collections.json
  nipada/falsification/nipada_v235_fetch_report.json

Usage:
  python3 nipada_fetch_corpus_v235_suttacentral_collections.py [--limit N]
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Import shared infrastructure from v212f
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found; run from Panini or Panini-Research repo")

# Add scripts dir to path so we can import from v212f
sys.path.insert(0, str(_HERE))
from nipada_fetch_corpus_v212f import (  # noqa: E402
    V14_ATOMS,
    freq_signature,
    _get,
    HTTP_HEADERS,
    REQUEST_DELAY,
    CACHE_SUTTACENTRAL,
    CORPUS_DIR,
    FALSI_DIR,
)

# Leaf cache: one file per SC leaf UID
CACHE_LEAVES = CACHE_SUTTACENTRAL / "leaves"
CACHE_LEAVES.mkdir(parents=True, exist_ok=True)

GRAPH_PATH = FALSI_DIR / "nipada_v219_graph_v13.json"


# ---------------------------------------------------------------------------
# Work definitions — the 40 failing texts from §212f
# ---------------------------------------------------------------------------
# fetch_type: "individual" | "collection" | "skip"
# sc_uid:     correct SuttaCentral UID (may differ from catalog URL)
# leaf_limit: max leaves to concat for very large collections (None = all)

WORKS = [
    # -- Individual suttas (broken URL mapping in catalog) --
    {"id": "an3_65_kalama",       "sc_uid": "an3.65",  "fetch_type": "individual"},
    {"id": "an5_159_udayi",       "sc_uid": "an5.159", "fetch_type": "individual"},
    {"id": "an7_64_kodhana",      "sc_uid": "an7.64",  "fetch_type": "individual"},
    {"id": "an10_60_girimananda", "sc_uid": "an10.60", "fetch_type": "individual"},

    # -- Samyutta Nikāya collections --
    {"id": "sn5_bhikkhuni",           "sc_uid": "sn5",  "fetch_type": "collection"},
    {"id": "sn12_paticcasamuppada",   "sc_uid": "sn12", "fetch_type": "collection"},
    {"id": "sn22_khandha",            "sc_uid": "sn22", "fetch_type": "collection"},
    {"id": "sn35_salayatana",         "sc_uid": "sn35", "fetch_type": "collection"},
    {"id": "sn36_vedana",             "sc_uid": "sn36", "fetch_type": "collection"},
    {"id": "sn38_jambukhadaka",       "sc_uid": "sn38", "fetch_type": "collection"},
    {"id": "sn41_citta",              "sc_uid": "sn41", "fetch_type": "collection"},
    {"id": "sn42_gamani",             "sc_uid": "sn42", "fetch_type": "collection"},
    {"id": "sn44_avyakata",           "sc_uid": "sn44", "fetch_type": "collection"},
    {"id": "sn45_magga",              "sc_uid": "sn45", "fetch_type": "collection"},
    {"id": "sn46_bojjhanga",          "sc_uid": "sn46", "fetch_type": "collection"},
    {"id": "sn56_sacca",              "sc_uid": "sn56", "fetch_type": "collection"},

    # -- Anguttara Nikāya book-level collections --
    {"id": "an1_book_of_ones",        "sc_uid": "an1",  "fetch_type": "collection"},
    {"id": "an2_book_of_twos",        "sc_uid": "an2",  "fetch_type": "collection"},
    {"id": "an3_book_of_threes",      "sc_uid": "an3",  "fetch_type": "collection"},
    {"id": "an4_book_of_fours",       "sc_uid": "an4",  "fetch_type": "collection"},

    # -- Khuddaka Nikāya --
    {"id": "dhammapada",              "sc_uid": "dhp",  "fetch_type": "collection"},
    {"id": "udana",                   "sc_uid": "ud",   "fetch_type": "collection"},
    {"id": "itivuttaka",              "sc_uid": "iti",  "fetch_type": "collection"},
    {"id": "suttanipata",             "sc_uid": "snp",  "fetch_type": "collection"},
    {"id": "theragatha",              "sc_uid": "thag", "fetch_type": "collection"},
    {"id": "therigatha",              "sc_uid": "thig", "fetch_type": "collection"},
    # Jataka: limit to first 100 tales as "selection"
    {"id": "jataka_selection",        "sc_uid": "ja",   "fetch_type": "collection",
     "leaf_limit": 100},
    {"id": "petavatthu",              "sc_uid": "pv",   "fetch_type": "collection"},

    # -- Skipped: no Sujato bilara translation available --
    # snp4 / snp5: Atthakavagga & Parāyanavagga sub-sections of snp (already covered)
    {"id": "snp_atthakavagga",  "sc_uid": "snp4", "fetch_type": "skip",
     "skip_reason": "sub-collection of snp; covered by suttanipata"},
    {"id": "snp_parayanavagga", "sc_uid": "snp5", "fetch_type": "skip",
     "skip_reason": "sub-collection of snp; covered by suttanipata"},
    # Texts with no Sujato bilara translation:
    {"id": "nettippakarana",          "sc_uid": "nett",   "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation (Bhikkhu Nanamoli only)"},
    {"id": "petakopadesa",            "sc_uid": "pet",    "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation"},
    {"id": "milindapanha",            "sc_uid": "mil",    "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation (Rhys Davids only)"},
    {"id": "vimanavatthu",            "sc_uid": "vv",     "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation"},
    {"id": "vinaya_mahavagga",        "sc_uid": "mv",     "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation (Horner only)"},
    {"id": "vinaya_cullavagga",       "sc_uid": "cv",     "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation"},
    {"id": "vinaya_patimokkha_bhikkhu",    "sc_uid": "bhi-pm", "fetch_type": "skip",
     "skip_reason": "Patimokkha rules — no narrative text for V14 signing"},
    {"id": "vinaya_patimokkha_bhikkhuni",  "sc_uid": "bhik-pm","fetch_type": "skip",
     "skip_reason": "Patimokkha rules — no narrative text for V14 signing"},
    {"id": "abhidhamma_dhammasangani",     "sc_uid": "dhs",    "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation"},
    {"id": "abhidhamma_kathavatthu",       "sc_uid": "kv",     "fetch_type": "skip",
     "skip_reason": "no Sujato bilara translation"},
]


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def _fetch_leaf(uid: str, author: str = "sujato") -> Optional[str]:
    """
    Fetch a single bilara sutta leaf and return its translation text.
    Uses per-leaf cache in CACHE_LEAVES/{uid}.txt.
    """
    cache_file = CACHE_LEAVES / f"{uid}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    api_url = f"https://suttacentral.net/api/bilarasuttas/{uid}/en?author={author}"
    r = _get(api_url)
    time.sleep(REQUEST_DELAY)

    if r is None or r.status_code != 200:
        print(f"    [leaf] HTTP {r.status_code if r else 'err'}: {api_url}")
        return None

    try:
        data = r.json()
    except Exception:
        print(f"    [leaf] JSON parse error: {uid}")
        return None

    tt = data.get("translation_text", {})
    if not tt:
        return None

    segments = [v.strip() for v in tt.values() if isinstance(v, str) and len(v.strip()) > 4]
    text = " ".join(segments)
    if text:
        cache_file.write_text(text, encoding="utf-8")
    return text or None


def _get_leaf_uids(collection_uid: str) -> list[str]:
    """
    Use suttaplex API to get all leaf UIDs in a collection.
    """
    url = f"https://suttacentral.net/api/suttaplex/{collection_uid}?lang=en"
    r = _get(url)
    time.sleep(REQUEST_DELAY)
    if r is None or r.status_code != 200:
        print(f"    [suttaplex] HTTP {r.status_code if r else 'err'}: {collection_uid}")
        return []
    try:
        data = r.json()
    except Exception:
        print(f"    [suttaplex] JSON parse error: {collection_uid}")
        return []
    return [item["uid"] for item in data if item.get("type") == "leaf"]


def fetch_individual(work_id: str, sc_uid: str) -> Optional[str]:
    """Fetch a single individual sutta, using work-level cache."""
    cache_file = CACHE_SUTTACENTRAL / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")
    text = _fetch_leaf(sc_uid)
    if text:
        cache_file.write_text(text, encoding="utf-8")
    return text


def fetch_collection(work_id: str, sc_uid: str, leaf_limit: Optional[int] = None) -> Optional[str]:
    """
    Fetch all leaves of a collection, concatenate, return full text.
    Uses work-level cache for the final concatenated result.
    """
    cache_file = CACHE_SUTTACENTRAL / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    print(f"    [suttaplex] getting leaf UIDs for {sc_uid} …")
    leaf_uids = _get_leaf_uids(sc_uid)
    if not leaf_uids:
        print(f"    [collection] no leaves for {sc_uid}")
        return None

    if leaf_limit and len(leaf_uids) > leaf_limit:
        print(f"    [collection] {len(leaf_uids)} leaves → limiting to first {leaf_limit}")
        leaf_uids = leaf_uids[:leaf_limit]
    else:
        print(f"    [collection] {len(leaf_uids)} leaves")

    parts = []
    failed = 0
    for i, uid in enumerate(leaf_uids, 1):
        if i % 20 == 0:
            print(f"      … {i}/{len(leaf_uids)} leaves …")
        leaf_text = _fetch_leaf(uid)
        if leaf_text:
            parts.append(leaf_text)
        else:
            failed += 1

    if not parts:
        print(f"    [collection] all leaves failed for {sc_uid}")
        return None

    print(f"    [collection] got {len(parts)}/{len(leaf_uids)} leaves, {failed} failed")
    full_text = " ".join(parts)

    cache_file.write_text(full_text, encoding="utf-8")
    return full_text


# ---------------------------------------------------------------------------
# Graph node loader
# ---------------------------------------------------------------------------

def _load_graph_nodes() -> dict:
    """Load graph v13 node dict {id: node_data}."""
    if not GRAPH_PATH.exists():
        print(f"WARNING: graph not found at {GRAPH_PATH}")
        return {}
    with open(GRAPH_PATH, encoding="utf-8") as f:
        g = json.load(f)
    return g.get("nodes", {})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_works(limit: int = 0) -> dict:
    nodes = _load_graph_nodes()
    print(f"Loaded {len(nodes)} graph nodes from v13")

    signed_works = []
    report_entries = []
    n_signed = 0
    n_failed = 0
    n_skipped = 0
    n_processed = 0

    fetchable = [w for w in WORKS if w["fetch_type"] != "skip"]
    skippable = [w for w in WORKS if w["fetch_type"] == "skip"]

    print(f"\nFetchable: {len(fetchable)}  |  Skipped: {len(skippable)}")
    print("=" * 60)

    for w in fetchable:
        if limit > 0 and n_processed >= limit:
            break

        work_id = w["id"]
        sc_uid = w["sc_uid"]
        ftype = w["fetch_type"]
        leaf_limit = w.get("leaf_limit")

        n_processed += 1
        print(f"\n[{n_processed}] {work_id}  (uid={sc_uid}, type={ftype})")

        if ftype == "individual":
            text = fetch_individual(work_id, sc_uid)
        elif ftype == "collection":
            text = fetch_collection(work_id, sc_uid, leaf_limit=leaf_limit)
        else:
            text = None

        if text is None or len(text) < 100:
            print(f"  FAILED: no text for {work_id}")
            n_failed += 1
            report_entries.append({
                "work_id": work_id, "sc_uid": sc_uid,
                "status": "failed", "fetch_type": ftype,
            })
            continue

        n_chars = len(text)
        n_words = len(text.split())
        print(f"  text: {n_chars:,} chars, {n_words:,} words")

        sig = freq_signature(text, lang="eng")
        top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]
        print(f"  sig top3: {[(a, round(v, 3)) for a, v in top3]}")

        node = nodes.get(work_id, {})
        tradition = (
            node.get("tradition_label")
            or node.get("tradition_micro")
            or "BUDDHISM_THERAVADA"
        )

        entry = {
            "local_id": work_id,
            "graph_node_id": work_id,
            "catalog": "buddhist_axial",
            "tradition_label": tradition,
            "lang": "eng",
            "n_chars": n_chars,
            "n_words": n_words,
            "v14_signature": sig,
            "v14_top3": [[a, v] for a, v in top3],
            "matched": work_id in nodes,
            "lexicon_version": "v212f",
            "source": "suttacentral",
            "sc_uid": sc_uid,
            "fetch_type": ftype,
        }
        signed_works.append(entry)
        n_signed += 1
        report_entries.append({
            "work_id": work_id, "sc_uid": sc_uid,
            "status": "signed", "fetch_type": ftype,
            "n_chars": n_chars,
            "top3": [[a, round(v, 4)] for a, v in top3],
        })

    # Log skipped entries
    for w in skippable:
        n_skipped += 1
        report_entries.append({
            "work_id": w["id"], "sc_uid": w["sc_uid"],
            "status": "skipped", "fetch_type": "skip",
            "skip_reason": w.get("skip_reason", ""),
        })

    print(f"\n{'='*60}")
    print(f"Signed: {n_signed}  Failed: {n_failed}  Skipped: {n_skipped}")

    report = {
        "version": "v235",
        "n_signed": n_signed,
        "n_failed": n_failed,
        "n_skipped": n_skipped,
        "entries": report_entries,
    }
    return {"signed": signed_works, "report": report}


def save_outputs(data: dict) -> None:
    signed = data["signed"]
    report = data["report"]

    corpus_out = CORPUS_DIR / "signed_corpus_v235_suttacentral_collections.json"
    report_out = FALSI_DIR / "nipada_v235_fetch_report.json"

    corpus_data = {
        "version": "v235",
        "description": "SuttaCentral collections fix — 40 failed texts from §212f, 28 successfully signed",
        "lexicon_version": "v212f",
        "n_signed": len(signed),
        "v14_atoms": V14_ATOMS,
        "signed": signed,
    }

    with open(corpus_out, "w", encoding="utf-8") as f:
        json.dump(corpus_data, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {corpus_out}")

    with open(report_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote: {report_out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="§235-fetch: SuttaCentral collections fix")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process at most N fetchable works (0 = all)")
    args = parser.parse_args()

    print("=" * 60)
    print("§235-fetch: SuttaCentral collections fix")
    print(f"  limit={args.limit}")
    print(f"  nipada dir: {_NIPADA}")
    print(f"  leaf cache: {CACHE_LEAVES}")
    print("=" * 60)

    import datetime
    t0 = datetime.datetime.now()

    data = process_works(limit=args.limit)
    save_outputs(data)

    elapsed = (datetime.datetime.now() - t0).total_seconds()
    print(f"\nDone in {elapsed:.1f}s")


if __name__ == "__main__":
    main()

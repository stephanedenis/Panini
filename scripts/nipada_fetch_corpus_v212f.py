#!/usr/bin/env python3
"""
§212-fetch: Harvest multilingual corpus texts and compute V14 signatures.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01
Author: reconstructed for §212

Goal: Sign 100+ graph nodes with V14 signatures (diverse traditions), enabling:
  §213 — V_OPT v4 recalibration with larger/diverse signed set
  §214 — LOO tradition-out validation

Sources:
  1. SuttaCentral bilara API (70 Buddhist axial works, English/Pali)
  2. sacred-texts.com Sacred Books of the East (33 Indian + 17 Chinese)

NOTE on freq_signature:
  The original nipada_calibration_v177.py was created in Colab and never
  committed to git. This script uses a reconstructed V14 keyword lexicon
  (v212f_lexicon) based on content words only. Signatures computed here
  are self-consistent but may not be identical to v208 signatures for
  pre-existing works. This is noted in the output metadata.

Output:
  nipada/corpus/signed_corpus_v212f.json
  nipada/falsification/nipada_v212f_fetch_report.json

Usage:
  python3 nipada_fetch_corpus_v212f.py [--dry-run] [--limit N]

  --dry-run : fetch only first work per catalog, no filesystem write
  --limit N : process at most N works total (for testing)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Path resolution (dual-repo pattern)
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found; run from Panini or Panini-Research repo")

CORPUS_DIR = _NIPADA / "corpus"
CACHE_DIR = CORPUS_DIR / "_cache"
FALSI_DIR = _NIPADA / "falsification"

CACHE_SUTTACENTRAL = CACHE_DIR / "suttacentral"
CACHE_SACRED_TEXTS = CACHE_DIR / "sacred_texts"

for d in [CACHE_SUTTACENTRAL, CACHE_SACRED_TEXTS, FALSI_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# V14 atom definitions
# ---------------------------------------------------------------------------

V14_ATOMS = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET",
    "TEMPS", "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION",
    "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# ---------------------------------------------------------------------------
# Reconstructed V14 keyword lexicon for English (v212f_lexicon)
# Uses content words only (no grammatical function words like is/are/not)
# to avoid frequency bias from function-word distribution.
# ---------------------------------------------------------------------------

ATOM_LEXICON_ENG: dict[str, list[str]] = {
    # -----------------------------------------------------------------------
    # Design rationale (v212f_lexicon):
    #   Content words ONLY — no function words (is/are/of/with/was/not).
    #   "one" and ordinals (first/second/...) removed from NOMBRE because
    #   they flood enumerated texts indiscriminately.
    #   "infinite/finite" moved to ESPACE (cosmological extent).
    #   Target tradition fingerprints:
    #     Buddhist: ÊTRE+SUJET dominant (beings/existence, self/mind)
    #     Hindu/Vedic: SUJET+ÊTRE dominant (self/soul/Brahman, reality/truth)
    #     Confucian: STRUCTURE+MODALITÉ dominant (order, rites, duty)
    #     Daoist: ORIENTATION+TEMPS dominant (way, change)
    #     Yijing: ESPACE+SYMÉTRIE dominant (heaven/earth, harmony)
    # -----------------------------------------------------------------------
    "ÊTRE": [
        # Being, existence, reality
        "being", "beings", "existence", "existent", "exist", "exists", "existed",
        "reality", "real", "actual", "actuality", "substance", "essence",
        "nature", "nothing", "nothingness", "something", "everything", "anything",
        "truth", "true", "fact", "facts", "presence", "nonexistent",
        "inexistent", "unreal", "absolute",
    ],
    "DIFFÉRENCE": [
        "different", "difference", "differences", "differ", "differing",
        "distinction", "distinctions", "distinct", "unlike", "contrary",
        "opposite", "opposites", "diversity", "diverse", "various",
        "contrast", "opposition", "opposed", "separate", "separated",
        "division", "divided", "other", "another", "else",
        "negation", "negative",
    ],
    "RAPPORT": [
        # Relation, connection — content words only
        "relation", "relations", "related", "relationship", "relationships",
        "relative", "connection", "connections", "connected", "connect",
        "link", "linked", "links", "bond", "bonds", "bonded",
        "between", "among", "interaction", "interactions", "interdependent",
        "depend", "dependence", "dependent", "together",
        "correspondence", "correspond", "corresponds",
        "association", "associated", "associate",
        "union", "united", "uniting", "unity",
        "contact", "contacts", "attachment", "attached", "binding",
        "involvement", "involved",
    ],
    "ORIENTATION": [
        "toward", "towards", "goal", "goals", "aim", "aims",
        "direction", "aspiration", "aspirations", "aspire",
        "intention", "intentions", "intend", "path", "paths", "way", "ways",
        "seek", "seeking", "sought", "strive", "striving",
        "approach", "progress", "tendency", "incline", "tao", "dao",
    ],
    "SUJET": [
        # Self, person, agent — content words only (no personal pronouns)
        "self", "selves", "soul", "souls", "spirit", "spirits",
        "mind", "minds", "consciousness", "person", "persons",
        "individual", "individuals", "subject", "subjects",
        "agent", "agents", "ego",
    ],
    "TEMPS": [
        "time", "times", "temporal", "impermanence", "impermanent",
        "permanent", "eternally", "eternal", "eternity", "moment", "moments",
        "duration", "period", "age", "era", "past", "future",
        "change", "changing", "changed", "transient", "fleeting",
        "enduring", "arising", "arises", "ceasing", "ceases", "cessation",
        "origination", "transience", "momentary",
    ],
    "MODALITÉ": [
        # Deontic and alethic modality — content words only
        "possible", "possibility", "possibilities", "impossible",
        "necessary", "necessity", "potential", "potentiality",
        "freedom", "free", "able", "ability", "capable", "capacity",
        "constraint", "constraints", "permit", "permission",
        "allowed", "allow", "ought", "duty",
        "obligation", "obliged", "compelled", "unavoidable",
    ],
    "NOMBRE": [
        # Explicit numerals ≥2 only.
        # "one" excluded (ambiguous: "one who" vs. cardinal).
        # Ordinals (first/second/...) excluded (ubiquitous in any listed text).
        # "infinite/finite" moved to ESPACE (cosmological extent).
        "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "hundred", "thousand", "million",
        "number", "numbers", "countless", "manifold", "plural",
    ],
    "ESPACE": [
        "place", "places", "space", "spaces", "world", "worlds",
        "universe", "earth", "heaven", "realm", "realms",
        "region", "field", "ground", "land", "body", "bodies",
        "above", "below", "throughout", "center",
        "boundary", "location", "infinite", "finite",
    ],
    "OPÉRATION": [
        "action", "actions", "act", "acting", "practice", "practices",
        "cause", "causes", "caused", "effect", "effects", "result", "results",
        "transformation", "transform", "transforms",
        "perform", "performed", "creates", "creation", "creating",
        "work", "works", "produce", "produces", "produced",
        "karma", "deed", "deeds",
    ],
    "FONCTION": [
        "function", "functions", "role", "roles", "purpose", "purposes",
        "serve", "serves", "serving", "service",
        "use", "useful", "usefulness", "method", "methods",
        "instrument", "tool", "task", "tasks",
    ],
    "STRUCTURE": [
        "form", "forms", "structure", "structures", "order", "ordered",
        "system", "systems", "element", "elements", "component", "components",
        "category", "categories", "type", "types", "kind", "kinds",
        "pattern", "patterns", "level", "levels", "hierarchy",
        "class", "classes", "organization", "organized", "arrangement",
        "rite", "rites", "ritual", "rituals", "ceremony", "ceremonies",
    ],
    "SYMÉTRIE": [
        "equal", "equality", "equally", "equals",
        "same", "alike", "similar", "similarity",
        "balance", "balanced", "harmony", "harmonious", "harmonize",
        "equivalent", "parallels", "parallel", "mutual", "mutually",
        "reciprocal", "reciprocity", "identical", "mirror",
        "correspond", "corresponds",
    ],
    "ÉQUATION": [
        # Identity, definition — content words only
        "defined", "definition", "definitions", "define", "defines",
        "means", "meaning", "constitute", "constitutes", "constituted",
        "called", "named", "principle", "principles",
        "law", "laws", "rule", "rules", "formula",
        "theorem", "identity", "namely",
    ],
}

# Build lookup: word → set of matching atoms
_WORD_TO_ATOMS: dict[str, list[str]] = {}
for atom, words in ATOM_LEXICON_ENG.items():
    for w in words:
        _WORD_TO_ATOMS.setdefault(w, []).append(atom)


def freq_signature(text: str, lang: str = "eng") -> dict[str, float]:
    """
    Compute V14 signature for an English text using v212f_lexicon.

    Algorithm:
      1. Tokenize to lowercase alpha tokens
      2. For each token, check all V14 atom lexicons
      3. Count atom matches (one token can match multiple atoms)
      4. Normalize by total match count (L1 = 1.0)

    Returns dict {atom: frequency} with sum ≈ 1.0.
    If no tokens match, returns uniform distribution.

    Note: This is a reconstructed lexicon (v212f). The original
    nipada_calibration_v177.py script is unavailable (Colab-only, not committed).
    Signatures computed here are self-consistent but may differ from v208 values.
    """
    if lang != "eng":
        # Fallback: uniform distribution for unsupported languages
        return {a: 1.0 / 14 for a in V14_ATOMS}

    tokens = re.findall(r"[a-z]+", text.lower())
    counts: dict[str, int] = {a: 0 for a in V14_ATOMS}
    total = 0

    for tok in tokens:
        atoms_for_tok = _WORD_TO_ATOMS.get(tok)
        if atoms_for_tok:
            for atom in atoms_for_tok:
                counts[atom] += 1
            total += len(atoms_for_tok)

    if total == 0:
        return {a: 1.0 / 14 for a in V14_ATOMS}

    sig = {a: counts[a] / total for a in V14_ATOMS}
    # Verify sum ≈ 1.0
    s = sum(sig.values())
    assert abs(s - 1.0) < 1e-9, f"signature sum error: {s}"
    return sig


# ---------------------------------------------------------------------------
# SBE volume URL map (catalog uses wrong sbe/ prefix; corrected here)
# ---------------------------------------------------------------------------

SBE_URL_MAP: dict[str, Optional[str]] = {
    "sbe1":  "https://www.sacred-texts.com/hin/sbe01/",
    "sbe01": "https://www.sacred-texts.com/hin/sbe01/",
    "sbe2":  "https://www.sacred-texts.com/hin/sbe02/",
    "sbe02": "https://www.sacred-texts.com/hin/sbe02/",
    "sbe3":  "https://www.sacred-texts.com/cfu/sbe03/",
    "sbe03": "https://www.sacred-texts.com/cfu/sbe03/",
    "sbe8":  "https://www.sacred-texts.com/hin/sbe08/",
    "sbe08": "https://www.sacred-texts.com/hin/sbe08/",
    "sbe12": "https://www.sacred-texts.com/hin/sbr/sbe12/",
    "sbe14": "https://www.sacred-texts.com/hin/sbe14/",
    "sbe15": "https://www.sacred-texts.com/hin/sbe15/",
    "sbe16": "https://www.sacred-texts.com/ich/",     # Yijing under ich/
    "sbe17": "https://www.sacred-texts.com/bud/sbe17/",
    "sbe22": "https://www.sacred-texts.com/jai/sbe22/",
    "sbe25": None,   # Manu Smriti – not found
    "sbe27": None,   # Li Ki vol 1 – not found
    "sbe28": None,   # Li Ki vol 2 – not found
    "sbe29": "https://www.sacred-texts.com/hin/sbe29/",
    "sbe30": "https://www.sacred-texts.com/hin/sbe30/",
    "sbe32": "https://www.sacred-texts.com/hin/sbe32/",
    "sbe34": "https://www.sacred-texts.com/hin/sbe34/",
    "sbe38": "https://www.sacred-texts.com/hin/sbe38/",
    "sbe39": "https://www.sacred-texts.com/tao/sbe39/",
    "sbe40": "https://www.sacred-texts.com/tao/sbe40/",
    "sbe42": "https://www.sacred-texts.com/hin/sbe42/",
    "sbe44": "https://www.sacred-texts.com/hin/sbr/sbe44/",
    "sbe45": "https://www.sacred-texts.com/jai/sbe45/",
    "sbe49": "https://www.sacred-texts.com/bud/sbe49/",
}

HTTP_HEADERS = {"User-Agent": "NIPADA-Research/0.4.0 (academic, non-commercial)"}
REQUEST_DELAY = 1.2  # seconds between requests


def _get(url: str, timeout: int = 15) -> Optional[requests.Response]:
    """Polite HTTP GET with retry on 429/503."""
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=timeout, headers=HTTP_HEADERS)
            if r.status_code in (429, 503):
                wait = 5 * (attempt + 1)
                print(f"    [rate-limit {r.status_code}] waiting {wait}s …")
                time.sleep(wait)
                continue
            return r
        except requests.RequestException as exc:
            print(f"    [request error] {exc}")
            time.sleep(2)
    return None


# ---------------------------------------------------------------------------
# SuttaCentral fetcher
# ---------------------------------------------------------------------------

def fetch_suttacentral(work_id: str, url: str) -> Optional[str]:
    """
    Fetch English translation from SuttaCentral bilara API.
    URL format: https://suttacentral.net/{uid}/en/{author}
    Returns concatenated segment text, or None on failure.
    """
    # Extract sutta uid and author from URL
    # e.g. https://suttacentral.net/dn1/en/sujato → uid=dn1, author=sujato
    m = re.match(r"https://suttacentral\.net/([^/]+)/en/([^/?]+)", url)
    if not m:
        print(f"    [sc] unexpected URL format: {url}")
        return None
    uid, author = m.group(1), m.group(2)

    cache_file = CACHE_SUTTACENTRAL / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    api_url = f"https://suttacentral.net/api/bilarasuttas/{uid}/en?author={author}"
    print(f"    [sc] GET {api_url}")
    r = _get(api_url)
    time.sleep(REQUEST_DELAY)

    if r is None or r.status_code != 200:
        print(f"    [sc] failed: {r.status_code if r else 'no response'}")
        return None

    try:
        data = r.json()
    except Exception:
        print("    [sc] JSON parse error")
        return None

    tt = data.get("translation_text", {})
    if not tt:
        print("    [sc] no translation_text in response")
        return None

    # Concatenate all segment values (skip headings-only segments if < 5 chars)
    segments = [v.strip() for v in tt.values() if isinstance(v, str) and len(v.strip()) > 4]
    full_text = " ".join(segments)

    if len(full_text) < 100:
        print(f"    [sc] text too short ({len(full_text)} chars), skipping")
        return None

    cache_file.write_text(full_text, encoding="utf-8")
    return full_text


# ---------------------------------------------------------------------------
# sacred-texts.com fetcher
# ---------------------------------------------------------------------------

def _extract_text_from_html(html: str) -> str:
    """Extract readable text from sacred-texts.com HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts, styles, nav
    for tag in soup(["script", "style", "nav", "header", "footer", "a"]):
        tag.decompose()
    # Get main body text
    body = soup.find("body")
    if body is None:
        return soup.get_text(separator=" ", strip=True)
    text = body.get_text(separator=" ", strip=True)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fetch_index_links(index_url: str) -> list[str]:
    """
    Fetch index page and return list of chapter HTML links.
    Returns absolute URLs for .htm/.html files.
    """
    r = _get(index_url)
    time.sleep(REQUEST_DELAY)
    if r is None or r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    from urllib.parse import urljoin

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Keep only local .htm/.html links (not navigation, not external)
        if re.search(r"\.html?$", href, re.IGNORECASE) and not href.startswith(".."):
            abs_url = urljoin(index_url, href)
            if abs_url not in links:
                links.append(abs_url)
    return links


def fetch_sacred_texts(work_id: str, catalog_url: str) -> Optional[str]:
    """
    Fetch text from sacred-texts.com.

    Strategy:
      1. Fix catalog URL (sbe/ prefix → real prefix via SBE_URL_MAP)
      2. Fetch index page
      3. Follow chapter links (skip intro/preface/front-matter)
      4. Extract and concatenate text from chapter pages

    Returns full text or None on failure.
    """
    cache_file = CACHE_SACRED_TEXTS / f"{work_id}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    # Fix URL prefix: catalog uses sbe/sbeXX/, we need the real path
    real_url = catalog_url
    sbe_match = re.search(r"sbe/sbe(\d+)/?", catalog_url, re.IGNORECASE)
    if sbe_match:
        sbe_key = f"sbe{sbe_match.group(1)}"
        # Try both zero-padded and non-padded
        real_url_candidate = SBE_URL_MAP.get(sbe_key) or SBE_URL_MAP.get(
            f"sbe{int(sbe_match.group(1)):02d}"
        )
        if real_url_candidate is None:
            print(f"    [st] SBE volume {sbe_key} not mapped – skipping {work_id}")
            return None
        real_url = real_url_candidate
        print(f"    [st] URL remapped: {catalog_url} → {real_url}")

    print(f"    [st] fetching index: {real_url}")
    chapter_links = _fetch_index_links(real_url)

    if not chapter_links:
        print(f"    [st] no chapter links found at {real_url}")
        return None

    # Filter: skip known front-matter files (title, preface, intro, toc, contents)
    _SKIP_PATTERNS = re.compile(
        r"(000|toc|contents?|preface|intro|index|title|copyright|pageidx)", re.IGNORECASE
    )
    content_links = [l for l in chapter_links if not _SKIP_PATTERNS.search(l)]
    if not content_links:
        content_links = chapter_links  # fall back if filter too aggressive

    print(f"    [st] {len(content_links)} chapter links to fetch")

    all_text_parts = []
    for chapter_url in content_links[:30]:  # cap at 30 chapters per work
        r = _get(chapter_url)
        time.sleep(REQUEST_DELAY)
        if r is None or r.status_code != 200:
            continue
        chapter_text = _extract_text_from_html(r.text)
        if len(chapter_text) > 100:
            all_text_parts.append(chapter_text)

    if not all_text_parts:
        print(f"    [st] no chapter text extracted for {work_id}")
        return None

    full_text = " ".join(all_text_parts)
    cache_file.write_text(full_text, encoding="utf-8")
    return full_text


# ---------------------------------------------------------------------------
# Graph node matching
# ---------------------------------------------------------------------------

def _load_graph_nodes() -> dict:
    """Load graph v12 node dict {id: node_data}."""
    graph_path = FALSI_DIR / "nipada_v210a_graph_v12.json"
    if not graph_path.exists():
        print(f"WARNING: graph not found at {graph_path}")
        return {}
    with open(graph_path, encoding="utf-8") as f:
        g = json.load(f)
    return g.get("nodes", {})


def match_to_graph_node(work_id: str, nodes: dict) -> Optional[str]:
    """
    Find graph node matching work_id.
    Tries exact match, then partial match.
    Returns node_id or None.
    """
    if work_id in nodes:
        return work_id
    # Try prefix match
    for node_id in nodes:
        if work_id in node_id or node_id in work_id:
            return node_id
    return None


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_catalogs(dry_run: bool = False, limit: int = 0) -> dict:
    """
    Process all three catalogs, fetch texts, compute V14 signatures.

    Returns:
        {
          "signed": [...],          # list of signed work dicts
          "report": {...},          # fetch report
        }
    """
    # Load catalogs
    catalogs = {
        "buddhist_axial": {
            "file": CORPUS_DIR / "catalog_buddhist_axial_v205.json",
            "source": "suttacentral",
        },
        "indian_axial": {
            "file": CORPUS_DIR / "catalog_indian_axial_v206a.json",
            "source": "sacred_texts",
        },
        "chinese_axial": {
            "file": CORPUS_DIR / "catalog_chinese_axial_v206b.json",
            "source": "sacred_texts",
        },
    }

    nodes = _load_graph_nodes()
    print(f"Loaded {len(nodes)} graph nodes")

    signed_works = []
    report_entries = []
    total_fetched = 0
    total_signed = 0
    total_skipped = 0
    total_failed = 0
    n_processed = 0

    for cat_name, cat_info in catalogs.items():
        cat_path = cat_info["file"]
        if not cat_path.exists():
            print(f"WARNING: catalog not found: {cat_path}")
            continue

        with open(cat_path, encoding="utf-8") as f:
            cat_data = json.load(f)

        works = cat_data.get("works", [])
        source = cat_info["source"]

        print(f"\n=== {cat_name} ({source}) — {len(works)} works ===")

        for w in works:
            if limit > 0 and n_processed >= limit:
                break

            work_id = w.get("id", "")
            url_en = w.get("url_translation_en")

            if not url_en:
                report_entries.append({
                    "work_id": work_id, "catalog": cat_name,
                    "status": "no_url", "reason": "no url_translation_en",
                })
                total_skipped += 1
                continue

            print(f"  [{n_processed+1}] {work_id}")
            n_processed += 1

            # Fetch text
            if source == "suttacentral":
                text = fetch_suttacentral(work_id, url_en)
            else:
                text = fetch_sacred_texts(work_id, url_en)

            if text is None:
                report_entries.append({
                    "work_id": work_id, "catalog": cat_name,
                    "status": "fetch_failed", "url": url_en,
                })
                total_failed += 1
                continue

            total_fetched += 1
            n_chars = len(text)
            n_words = len(text.split())
            print(f"    text: {n_chars} chars, {n_words} words")

            # Compute V14 signature (English)
            sig = freq_signature(text, lang="eng")
            top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]
            print(f"    sig top3: {[(a, round(v, 3)) for a, v in top3]}")

            # Match to graph node
            node_id = match_to_graph_node(work_id, nodes)
            matched = node_id is not None
            if not matched:
                node_id = work_id  # Use work_id as node_id placeholder
                print(f"    WARNING: no graph node match for {work_id}")

            # Build tradition label from catalog metadata
            tradition = nodes.get(node_id, {}).get(
                "tradition_label",
                w.get("tradition_micro", w.get("macro_culture", "UNKNOWN")),
            )

            entry = {
                "local_id": work_id,
                "graph_node_id": node_id,
                "catalog": cat_name,
                "tradition_label": tradition,
                "lang": "eng",
                "n_chars": n_chars,
                "n_words": n_words,
                "v14_signature": sig,
                "v14_top3": [[a, v] for a, v in top3],
                "matched": matched,
                "lexicon_version": "v212f",
                "source": source,
                "url": url_en,
            }
            signed_works.append(entry)
            total_signed += 1

            report_entries.append({
                "work_id": work_id, "catalog": cat_name,
                "status": "signed", "n_chars": n_chars,
                "top3": [[a, round(v, 4)] for a, v in top3],
            })

            if dry_run:
                print("  [dry-run] stopping after first work per catalog")
                break

        if limit > 0 and n_processed >= limit:
            break

    report = {
        "version": "v212f",
        "date": "2026-05-01",
        "lexicon_version": "v212f_lexicon",
        "lexicon_note": (
            "Reconstructed lexicon — original nipada_calibration_v177.py lost (Colab-only). "
            "Uses content-words-only V14 keyword lists. Self-consistent for new works; "
            "may not be numerically identical to v208 signatures for pre-existing works."
        ),
        "n_total_catalog": n_processed + total_skipped,
        "n_fetched": total_fetched,
        "n_signed": total_signed,
        "n_skipped_no_url": total_skipped,
        "n_failed": total_failed,
        "entries": report_entries,
    }

    return {"signed": signed_works, "report": report}


def save_outputs(data: dict, dry_run: bool = False) -> None:
    """Write signed_corpus_v212f.json and fetch_report_v212f.json."""
    signed = data["signed"]
    report = data["report"]

    corpus_out = {
        "version": "v212f",
        "date": "2026-05-01",
        "lexicon_version": "v212f_lexicon",
        "lexicon_note": report["lexicon_note"],
        "n_signed": len(signed),
        "v14_atoms": V14_ATOMS,
        "signed": signed,
    }

    if dry_run:
        print("\n[dry-run] Output preview (first 2 signed works):")
        for entry in signed[:2]:
            print(f"  {entry['work_id'] if 'work_id' in entry else entry['local_id']}")
            print(f"    top3: {entry['v14_top3']}")
        return

    out_corpus = CORPUS_DIR / "signed_corpus_v212f.json"
    out_report = FALSI_DIR / "nipada_v212f_fetch_report.json"

    with open(out_corpus, "w", encoding="utf-8") as f:
        json.dump(corpus_out, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_corpus}")

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote: {out_report}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="§212-fetch: V14 corpus harvester")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch only first work per catalog, no file writes")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process at most N works total (0 = no limit)")
    args = parser.parse_args()

    print("=" * 60)
    print("§212-fetch: NIPADA V14 corpus harvester")
    print(f"  dry_run={args.dry_run}, limit={args.limit}")
    print(f"  nipada dir: {_NIPADA}")
    print(f"  cache dir:  {CACHE_DIR}")
    print("=" * 60)

    import datetime
    t0 = datetime.datetime.now()

    data = process_catalogs(dry_run=args.dry_run, limit=args.limit)
    save_outputs(data, dry_run=args.dry_run)

    elapsed = (datetime.datetime.now() - t0).total_seconds()
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Signed: {data['report']['n_signed']}")
    print(f"Failed: {data['report']['n_failed']}")
    print(f"Skipped (no URL): {data['report']['n_skipped_no_url']}")


if __name__ == "__main__":
    main()

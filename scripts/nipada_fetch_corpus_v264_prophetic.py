#!/usr/bin/env python3
"""
§264 — Extension prophétique : textes oraculaires, prophétiques et leurs interprètes.

Stratégie:
  Les textes prophétiques forment une classe distincte dans le corpus NIPADA :
  ils possèdent une δ_min > 0 structurelle (intentionnellement polysémiques).
  Nous les traitons comme des textes primaires à part entière.

  De plus, les œuvres des interprètes (Russell, Miller, etc.) sont elles-mêmes
  des textes originaux — avec `source_type: "interpretive_commentary"` et
  `interprets_ref` pointant vers leurs sources.

  Schema extensions ajoutées aux entrées corpus:
    - source_type: "primary_prophetic" | "interpretive_commentary" | "primary"
    - interprets_ref: [id, ...] | null

  Nouveaux catalogues de traditions:
    - ABRAHAMIC_PROPHETIC_AXIAL  (-800 à -400): Isaïe, Jérémie, Ézéchiel, Daniel, Zacharie
    - JUDEAN_APOCALYPTIC_LATE    (-300 à +100): 1 Hénoch, 2 Esdras (4 Esdras)
    - CHRISTIAN_APOCALYPTIC_EARLY (+50 à +100): Apocalypse de Jean
    - CLASSICAL_ORACULAR         (-300 à +200): Oracles sibyllins
    - ZOROASTRIAN_AXIAL          (-1000 à -600): Gathas de Zarathoustra
    - NORSE_EDDIC_MEDIEVAL       (+900 à +1200): Völuspá
    - MESOAMERICAN_COLONIAL      (+1500 à +1700): Chilam Balam
    - RENAISSANCE_OCCULT_EARLY_MODERN (+1550): Nostradamus
    - MILLENARIAN_MODERN_PROTESTANT (+1830 à +1880): Russell, Miller

Sources:
  - KJV via sacred-texts.com/bib/kjv/  (Isaïe, Jérémie, Ézéchiel, Daniel, Zacharie, Révélation)
  - Polyglot Bible via sacred-texts.com/bib/poly/  (2 Esdras = 4 Esdras)
  - 1 Hénoch via sacred-texts.com/bib/boe/  (R.H. Charles trans.)
  - Oracles sibyllins via sacred-texts.com/cla/sib/  (Milton S. Terry trans.)
  - Völuspá via sacred-texts.com/neu/poe/  (Henry Adams Bellows trans.)
  - Gathas via sacred-texts.com/zor/sbe31/  (L.H. Mills trans., SBE vol. 31)
  - Chilam Balam via sacred-texts.com/nam/maya/cbc/  (Ralph Roys trans.)
  - Nostradamus via Project Gutenberg #3814  (Les Prophéties, french)
  - J.S. Russell "The Parousia" via Project Gutenberg #35423
  - William Miller "Evidence from Scripture and History" via PG #23893

Produits:
  nipada/corpus/signed_corpus_v264_prophetic.json
  nipada/falsification/nipada_v264_fetch_report.json
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

# ── Path resolution ──────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

try:
    from nipada_fetch_corpus_v212f import freq_signature, V14_ATOMS
except Exception as e:
    sys.exit(f"ERROR: cannot import freq_signature from v212f script: {e}")

CORPUS_DIR = _NIPADA / "corpus"
FALSI_DIR  = _NIPADA / "falsification"
CACHE_DIR  = CORPUS_DIR / "_cache"
CACHE_DIR.mkdir(exist_ok=True)

OUT_CORPUS = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
OUT_REPORT = FALSI_DIR  / "nipada_v264_fetch_report.json"

HEADERS     = {"User-Agent": "NIPADA-Research/0.4.0 (academic, non-commercial)"}
REQ_TIMEOUT = 45
REQ_DELAY   = 1.2   # seconds between requests

# ── Catalog: primary prophetic texts ────────────────────────────────────────
# source_type = "primary_prophetic"
# Völuspá is a true single HTML page; KJV books are index pages → multi-page below.

KJV_SINGLE_PAGE_TEXTS: list[dict[str, Any]] = [
    {
        "id": "voluspa",
        "url": "https://www.sacred-texts.com/neu/poe/poe03.htm",
        "title": "Völuspá (The Sibyl's Prophecy)",
        "tradition_label": "NORSE_EDDIC_MEDIEVAL",
        "tradition_micro": "NORSE_EDDIC_PROPHETIC",
        "year": 1000,
        "lang": "eng",
        "author": "anonymous (Eddic tradition, trans. Bellows 1936)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
]

# ── KJV Bible books and Polyglot apocrypha: index + chapter pages ────────────
# sacred-texts.com KJV: book index (e.g. isa.htm) + chapter pages (isa001.htm…)
# These go through process_multi_page but with a book-specific chapter pattern.

KJV_MULTI_PAGE_TEXTS: list[dict[str, Any]] = [
    {
        "id": "isaiah_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/isa.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"isa\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_isa",
        "title": "Isaiah (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "year": -700,
        "lang": "eng",
        "author": "Isaiah ben Amoz (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "jeremiah_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/jer.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"jer\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_jer",
        "title": "Jeremiah (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "year": -600,
        "lang": "eng",
        "author": "Jeremiah ben Hilkiah (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "ezekiel_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/eze.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"eze\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_eze",
        "title": "Ezekiel (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "year": -590,
        "lang": "eng",
        "author": "Ezekiel ben Buzi (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "daniel_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/dan.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"dan\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_dan",
        "title": "Daniel (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_APOCALYPTIC",
        "year": -165,
        "lang": "eng",
        "author": "anonymous (Daniel tradition)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "zechariah_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/zac.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"zac\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_zac",
        "title": "Zechariah (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "year": -520,
        "lang": "eng",
        "author": "Zechariah ben Berechiah (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "hosea_book",
        "index_url": "https://www.sacred-texts.com/bib/kjv/hos.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"hos\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_hos",
        "title": "Hosea (KJV)",
        "tradition_label": "ABRAHAMIC_PROPHETIC_AXIAL",
        "tradition_micro": "HEBREW_PROPHETIC",
        "year": -750,
        "lang": "eng",
        "author": "Hosea ben Beeri (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "revelation_john",
        "index_url": "https://www.sacred-texts.com/bib/kjv/rev.htm",
        "base_url": "https://www.sacred-texts.com/bib/kjv/",
        "link_pattern": r"rev\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "kjv_rev",
        "title": "Revelation of John (KJV)",
        "tradition_label": "CHRISTIAN_APOCALYPTIC_EARLY",
        "tradition_micro": "CHRISTIAN_PROPHETIC",
        "year": 95,
        "lang": "eng",
        "author": "John of Patmos (attributed)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "2_esdras",
        "index_url": "https://www.sacred-texts.com/bib/poly/es2.htm",
        "base_url": "https://www.sacred-texts.com/bib/poly/",
        "link_pattern": r"es2\d+\.htm",
        "exclude_patterns": [],
        "cache_prefix": "poly_es2",
        "title": "2 Esdras / 4 Ezra (Polyglot Bible)",
        "tradition_label": "JUDEAN_APOCALYPTIC_LATE",
        "tradition_micro": "JEWISH_APOCALYPTIC",
        "year": 100,
        "lang": "eng",
        "author": "anonymous (Ezra apocalypse tradition)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
]

# ── Catalog: multi-page sacred-texts.com texts ──────────────────────────────
# Require fetching index + individual chapter pages.

MULTI_PAGE_TEXTS: list[dict[str, Any]] = [
    {
        "id": "book_of_enoch",
        "index_url": "https://www.sacred-texts.com/bib/boe/index.htm",
        "base_url": "https://www.sacred-texts.com/bib/boe/",
        "link_pattern": r"boe\d+\.htm",
        "exclude_patterns": ["index", "boe001.htm"],  # skip cover page
        "cache_prefix": "boe",
        "title": "The Book of Enoch (1 Enoch)",
        "tradition_label": "JUDEAN_APOCALYPTIC_LATE",
        "tradition_micro": "JEWISH_APOCALYPTIC",
        "year": -200,
        "lang": "eng",
        "author": "anonymous (R.H. Charles trans. 1913)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "sibylline_oracles",
        "index_url": "https://www.sacred-texts.com/cla/sib/index.htm",
        "base_url": "https://www.sacred-texts.com/cla/sib/",
        "link_pattern": r"sib\d+\.htm",
        "exclude_patterns": ["index", "sib01.htm", "sib02.htm", "sib03.htm"],  # intro pages
        "cache_prefix": "sib",
        "title": "Sibylline Oracles",
        "tradition_label": "CLASSICAL_ORACULAR",
        "tradition_micro": "GRECO_ROMAN_ORACULAR",
        "year": -200,
        "lang": "eng",
        "author": "anonymous (Milton S. Terry trans. 1899)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "avesta_gathas",
        "index_url": "https://www.sacred-texts.com/zor/sbe31/index.htm",
        "base_url": "https://www.sacred-texts.com/zor/sbe31/",
        "link_pattern": r"sbe31\d+\.htm",
        "exclude_patterns": ["index", "sbe31000.htm"],  # skip intro/frontmatter
        "cache_prefix": "sbe31",
        "title": "Avesta: The Gathas of Zarathustra (SBE vol.31)",
        "tradition_label": "ZOROASTRIAN_AXIAL",
        "tradition_micro": "ZOROASTRIAN_PROPHETIC",
        "year": -1000,
        "lang": "eng",
        "author": "Zarathustra (attributed, L.H. Mills trans. 1887, SBE vol.31)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "chilam_balam",
        "index_url": "https://www.sacred-texts.com/nam/maya/cbc/index.htm",
        "base_url": "https://www.sacred-texts.com/nam/maya/cbc/",
        "link_pattern": r"cbc\d+\.htm",
        "exclude_patterns": ["index", "cbc01.htm", "cbc02.htm"],  # intro pages
        "cache_prefix": "cbc",
        "title": "The Book of Chilam Balam of Chumayel",
        "tradition_label": "MESOAMERICAN_COLONIAL",
        "tradition_micro": "MAYAN_PROPHETIC",
        "year": 1650,
        "lang": "eng",
        "author": "anonymous Maya scribes (Ralph L. Roys trans. 1933)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
]

# ── Catalog: Project Gutenberg texts ────────────────────────────────────────
# Mix of primary prophetic (Nostradamus) and interpretive commentaries (Russell, Miller).

GUTENBERG_TEXTS: list[dict[str, Any]] = [
    {
        "id": "nostradamus_centuries",
        "pg_ids": [3814],
        "title": "Les Prophéties de Michel Nostradamus",
        "tradition_label": "RENAISSANCE_OCCULT_EARLY_MODERN",
        "tradition_micro": "FRENCH_PROPHETIC_RENAISSANCE",
        "year": 1555,
        "lang": "fra",
        "author": "Michel de Nostredame (Nostradamus)",
        "source_type": "primary_prophetic",
        "interprets_ref": None,
    },
    {
        "id": "russell_parousia_1878",
        "pg_ids": [35423],
        "title": "The Parousia: A Critical Inquiry into the New Testament Doctrine of Our Lord's Second Coming",
        "tradition_label": "MILLENARIAN_MODERN_PROTESTANT",
        "tradition_micro": "PRETERIST_INTERPRETATION",
        "year": 1878,
        "lang": "eng",
        "author": "James Stuart Russell",
        "source_type": "interpretive_commentary",
        "interprets_ref": ["revelation_john", "daniel_book", "2_esdras"],
    },
    {
        "id": "miller_evidence_prophecy",
        "pg_ids": [23893],
        "title": "Evidence from Scripture and History of the Second Coming of Christ",
        "tradition_label": "MILLENARIAN_MODERN_PROTESTANT",
        "tradition_micro": "ADVENTIST_INTERPRETATION",
        "year": 1836,
        "lang": "eng",
        "author": "William Miller",
        "source_type": "interpretive_commentary",
        "interprets_ref": ["daniel_book", "revelation_john", "2_esdras"],
    },
]


# ── HTTP cache + fetch helpers ───────────────────────────────────────────────

def _get(url: str, cache_key: str) -> str | None:
    cache_file = CACHE_DIR / f"v264_{cache_key}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8", errors="replace")
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQ_TIMEOUT, verify=False)
        time.sleep(REQ_DELAY)
        if r.status_code == 200:
            cache_file.write_text(r.text, encoding="utf-8")
            return r.text
        print(f"    [HTTP {r.status_code}] {url}")
        return None
    except Exception as e:
        print(f"    [ERR] {url}: {e}")
        return None


def _html_to_text(html: str) -> str:
    """Extract clean text from sacred-texts.com HTML."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove navigation, header, footer divs if present
    for tag in soup.find_all(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    # Prefer body text
    body = soup.find("body")
    if body:
        return body.get_text(" ", strip=True)
    return soup.get_text(" ", strip=True)


def _tokenize_words(text: str) -> list[str]:
    """Extract English words (and common French/Latin) for V14 signature."""
    return re.findall(r"[A-Za-zÀ-ÿ]+", text)


def _strip_gutenberg(text: str) -> str:
    """Remove Project Gutenberg header/footer boilerplate."""
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "*END*THE SMALL PRINT!",
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "End of the Project Gutenberg EBook",
        "End of Project Gutenberg",
    ]
    best_start = 0
    for m in start_markers:
        idx = text.find(m)
        if idx != -1:
            eol = text.find("\n", idx)
            best_start = max(best_start, eol + 1 if eol != -1 else idx + len(m))
    best_end = len(text)
    for m in end_markers:
        idx = text.rfind(m)
        if idx != -1:
            best_end = min(best_end, idx)
    return text[best_start:best_end]


def _sign_text(
    text: str,
    local_id: str,
    min_words: int = 1500,
    win: int = 200,
    step: int = 100,
) -> dict[str, Any] | None:
    """
    Segment text into sliding windows, compute V14 signature.
    Returns None if text is too short or has zero signal.
    """
    words = _tokenize_words(text)
    if len(words) < min_words:
        print(f"    [SKIP] {local_id}: only {len(words)} words (min {min_words})")
        return None

    segments = [words[i: i + win] for i in range(0, len(words) - win + 1, step)]
    if not segments:
        return None

    agg_sig: dict[str, float] = {a: 0.0 for a in V14_ATOMS}
    for seg in segments:
        sig = freq_signature(" ".join(seg))
        for a in V14_ATOMS:
            agg_sig[a] += sig.get(a, 0.0)

    total = sum(agg_sig.values())
    if total < 1e-9:
        return None

    norm_sig = {a: round(agg_sig[a] / total, 6) for a in V14_ATOMS}
    top3 = sorted(norm_sig.items(), key=lambda x: -x[1])[:3]

    return {
        "n_segments": len(segments),
        "n_words": len(words),
        "v14_signature": norm_sig,
        "v14_top3": top3,
    }


# ── Corpus entry builder ─────────────────────────────────────────────────────

def _make_entry(meta: dict, sig_data: dict, source_url: str, source_label: str) -> dict:
    """Merge catalog metadata with signature data into a corpus entry."""
    return {
        "local_id": meta["id"],
        "graph_node_id": meta["id"],
        "catalog": meta["tradition_label"].lower(),
        "tradition_label": meta["tradition_label"],
        "tradition_micro": meta["tradition_micro"],
        "lang": meta["lang"],
        "title": meta["title"],
        "author": meta["author"],
        "year": meta["year"],
        "source_type": meta["source_type"],
        "interprets_ref": meta["interprets_ref"],
        "n_chars": sig_data.get("n_chars", 0),
        "n_words": sig_data["n_words"],
        "v14_signature": sig_data["v14_signature"],
        "v14_top3": sig_data["v14_top3"],
        "matched": True,
        "lexicon_version": "v14",
        "source": source_label,
        "url": source_url,
    }


# ── Fetch: single-page KJV / sacred-texts ───────────────────────────────────

def process_single_page(entry: dict) -> dict[str, Any]:
    tid  = entry["id"]
    url  = entry["url"]
    print(f"  [{tid}]  {url}")

    raw_html = _get(url, tid)
    if not raw_html:
        return {"local_id": tid, "status": "failed", "reason": "fetch_error"}

    text = _html_to_text(raw_html)
    n_chars = len(text)

    signed = _sign_text(text, tid)
    if signed is None:
        return {"local_id": tid, "status": "failed", "reason": "sign_error_or_short"}

    signed["n_chars"] = n_chars
    top3_str = ", ".join(f"{a}({v:.3f})" for a, v in signed["v14_top3"])
    print(f"    {signed['n_words']:,}w  top3: {top3_str}")

    corp = _make_entry(entry, signed, url, "sacred_texts_kjv")
    return {**corp, "status": "ok"}


# ── Fetch: multi-page sacred-texts.com ──────────────────────────────────────

def process_multi_page(entry: dict) -> dict[str, Any]:
    tid        = entry["id"]
    index_url  = entry["index_url"]
    base_url   = entry["base_url"]
    link_pat   = re.compile(entry["link_pattern"], re.IGNORECASE)
    excludes   = entry.get("exclude_patterns", [])
    prefix     = entry["cache_prefix"]

    print(f"  [{tid}]  index: {index_url}")

    idx_html = _get(index_url, f"{tid}_idx")
    if not idx_html:
        return {"local_id": tid, "status": "failed", "reason": "index_fetch_error"}

    soup = BeautifulSoup(idx_html, "html.parser")
    chapter_urls: list[str] = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]  # strip verse/section anchors
        if not href:
            continue
        if link_pat.search(href):
            # Skip excluded pages
            skip = any(ex in href for ex in excludes)
            if not skip and href not in seen:
                seen.add(href)
                full_url = base_url + href if not href.startswith("http") else href
                chapter_urls.append(full_url)

    if not chapter_urls:
        return {"local_id": tid, "status": "failed", "reason": "no_chapters_found"}

    print(f"    {len(chapter_urls)} chapter pages to fetch")

    parts: list[str] = []
    for i, url in enumerate(chapter_urls, 1):
        ckey = f"{prefix}_ch{i:03d}"
        html = _get(url, ckey)
        if html:
            parts.append(_html_to_text(html))

    if not parts:
        return {"local_id": tid, "status": "failed", "reason": "all_chapters_failed"}

    full_text = "\n\n".join(parts)
    n_chars = len(full_text)
    print(f"    concatenated: {n_chars:,} chars")

    signed = _sign_text(full_text, tid)
    if signed is None:
        return {"local_id": tid, "status": "failed", "reason": "sign_error_or_short"}

    signed["n_chars"] = n_chars
    top3_str = ", ".join(f"{a}({v:.3f})" for a, v in signed["v14_top3"])
    print(f"    {signed['n_words']:,}w  top3: {top3_str}")

    corp = _make_entry(entry, signed, index_url, "sacred_texts_html")
    return {**corp, "status": "ok"}


# ── Fetch: Project Gutenberg ─────────────────────────────────────────────────

def _fetch_gutenberg_text(pg_ids: list[int], text_id: str) -> str | None:
    for pg_id in pg_ids:
        urls = [
            f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt",
            f"https://www.gutenberg.org/files/{pg_id}/{pg_id}-0.txt",
            f"https://www.gutenberg.org/files/{pg_id}/{pg_id}.txt",
        ]
        for url in urls:
            raw = _get(url, f"pg_{pg_id}")
            if raw and len(raw) > 5000:
                return _strip_gutenberg(raw)
    return None


def process_gutenberg(entry: dict) -> dict[str, Any]:
    tid    = entry["id"]
    pg_ids = entry["pg_ids"]
    print(f"  [{tid}]  PG {pg_ids}")

    raw = _fetch_gutenberg_text(pg_ids, tid)
    if not raw:
        return {"local_id": tid, "status": "failed", "reason": "gutenberg_fetch_error"}

    n_chars = len(raw)
    signed = _sign_text(raw, tid)
    if signed is None:
        return {"local_id": tid, "status": "failed", "reason": "sign_error_or_short"}

    signed["n_chars"] = n_chars
    top3_str = ", ".join(f"{a}({v:.3f})" for a, v in signed["v14_top3"])
    print(f"    {signed['n_words']:,}w  top3: {top3_str}")

    pg_url = f"https://www.gutenberg.org/ebooks/{pg_ids[0]}"
    corp = _make_entry(entry, signed, pg_url, "project_gutenberg")
    return {**corp, "status": "ok"}


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    import urllib3
    urllib3.disable_warnings()

    print("=" * 70)
    print("§264 — Corpus prophétique : oracles, prophètes et interprètes")
    print(f"  nipada: {_NIPADA}")
    n_total = (len(KJV_SINGLE_PAGE_TEXTS) + len(KJV_MULTI_PAGE_TEXTS)
               + len(MULTI_PAGE_TEXTS) + len(GUTENBERG_TEXTS))
    print(f"  textes à traiter: {n_total}")
    print("=" * 70)

    signed: list[dict] = []
    failed: list[dict] = []
    t0 = time.time()

    # ── Völuspá (vraie page unique) ───────────────────────────────────────────
    print(f"\n=== PAGE UNIQUE [{len(KJV_SINGLE_PAGE_TEXTS)} textes] ===")
    for entry in KJV_SINGLE_PAGE_TEXTS:
        result = process_single_page(entry)
        (signed if result.get("status") == "ok" else failed).append(result)

    # ── KJV Bible + Polyglot (index → chapitres) ──────────────────────────────
    print(f"\n=== KJV / POLYGLOT (multi-pages) [{len(KJV_MULTI_PAGE_TEXTS)} textes] ===")
    for entry in KJV_MULTI_PAGE_TEXTS:
        result = process_multi_page(entry)
        (signed if result.get("status") == "ok" else failed).append(result)

    # ── Textes multi-pages sacred-texts ──────────────────────────────────────
    print(f"\n=== SACRED-TEXTS (multi-pages) [{len(MULTI_PAGE_TEXTS)} textes] ===")
    for entry in MULTI_PAGE_TEXTS:
        result = process_multi_page(entry)
        (signed if result.get("status") == "ok" else failed).append(result)

    # ── Textes Project Gutenberg ──────────────────────────────────────────────
    print(f"\n=== PROJECT GUTENBERG [{len(GUTENBERG_TEXTS)} textes] ===")
    for entry in GUTENBERG_TEXTS:
        result = process_gutenberg(entry)
        (signed if result.get("status") == "ok" else failed).append(result)

    elapsed = time.time() - t0

    print(f"\n── Résultats ──────────────────────────────────────────────────────────")
    print(f"  Signés   : {len(signed)} / {n_total}")
    print(f"  Échoués  : {len(failed)}")
    print(f"  Durée    : {elapsed:.1f}s")

    print("\n── Signatures V14 (source_type | tradition) ───────────────────────────")
    for t in signed:
        top = t.get("v14_top3", [])
        top_str = ", ".join(f"{a}({v:.3f})" for a, v in top[:3])
        st = t.get("source_type", "?")
        trad = t.get("tradition_label", "?")[:30]
        print(f"  {t['local_id']:35s} [{st[:10]}]  {trad:30s}  {top_str}")

    # ── Écriture corpus ───────────────────────────────────────────────────────
    def _clean(t: dict) -> dict:
        return {k: v for k, v in t.items() if k != "status"}

    # Count by source_type
    n_primary = sum(1 for t in signed if t.get("source_type") == "primary_prophetic")
    n_interp  = sum(1 for t in signed if t.get("source_type") == "interpretive_commentary")

    corpus_out = {
        "version": "v264",
        "description": (
            "§264 Corpus prophétique : textes oraculaires et interprètes. "
            "Nouveaux champs: source_type, interprets_ref. "
            "Nouveaux catalogues: ABRAHAMIC_PROPHETIC_AXIAL, JUDEAN_APOCALYPTIC_LATE, "
            "CHRISTIAN_APOCALYPTIC_EARLY, CLASSICAL_ORACULAR, ZOROASTRIAN_AXIAL, "
            "NORSE_EDDIC_MEDIEVAL, MESOAMERICAN_COLONIAL, "
            "RENAISSANCE_OCCULT_EARLY_MODERN, MILLENARIAN_MODERN_PROTESTANT."
        ),
        "section": "§264",
        "schema_extensions": {
            "source_type": "primary_prophetic | interpretive_commentary | primary",
            "interprets_ref": "list of local_ids that this text interprets, or null",
        },
        "n_signed": len(signed),
        "n_primary_prophetic": n_primary,
        "n_interpretive_commentary": n_interp,
        "n_failed": len(failed),
        "lexicon_version": "v14",
        "signed": [_clean(t) for t in signed],
        "failed": failed,
    }

    OUT_CORPUS.write_text(json.dumps(corpus_out, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print(f"\nCorpus écrit : {OUT_CORPUS}")
    print(f"  {len(signed)} entrées signées "
          f"({n_primary} primary_prophetic + {n_interp} interpretive_commentary)")

    # ── Rapport fetch ─────────────────────────────────────────────────────────
    report = {
        "section": "§264",
        "elapsed_s": round(elapsed, 1),
        "n_signed": len(signed),
        "n_primary_prophetic": n_primary,
        "n_interpretive_commentary": n_interp,
        "n_failed": len(failed),
        "signed_ids": [t["local_id"] for t in signed],
        "failed_details": failed,
        "traditions_added": [
            "ABRAHAMIC_PROPHETIC_AXIAL",
            "JUDEAN_APOCALYPTIC_LATE",
            "CHRISTIAN_APOCALYPTIC_EARLY",
            "CLASSICAL_ORACULAR",
            "ZOROASTRIAN_AXIAL",
            "NORSE_EDDIC_MEDIEVAL",
            "MESOAMERICAN_COLONIAL",
            "RENAISSANCE_OCCULT_EARLY_MODERN",
            "MILLENARIAN_MODERN_PROTESTANT",
        ],
    }
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print(f"Rapport écrit: {OUT_REPORT}")


if __name__ == "__main__":
    main()

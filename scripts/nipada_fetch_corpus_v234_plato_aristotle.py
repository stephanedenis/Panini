#!/usr/bin/env python3
"""
§234 — Extension Platon + Aristote: fetch + signature V14.

Stratégie:
  Les dialogues de Platon et les œuvres d'Aristote sont déjà dans graph v13
  comme nœuds UNSIGNED (signed_n_chars=0). Les signer générera des milliers
  de cross-pairs avec le corpus v212f (textes indiens/bouddhistes/chinois).

  - Platon (deg=34-45): 18 dialogues via Project Gutenberg (Jowett trans.)
  - Aristote (deg=49): 15 œuvres via MIT Internet Classics Archive HTML

Produit:
  nipada/corpus/signed_corpus_v234_plato_aristotle.json
  nipada/falsification/nipada_v234_fetch_report.json
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

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

OUT_CORPUS = CORPUS_DIR / "signed_corpus_v234_plato_aristotle.json"
OUT_REPORT = FALSI_DIR  / "nipada_v234_fetch_report.json"

HEADERS = {"User-Agent": "NIPADA-Research/0.4.0 (academic, non-commercial)"}
REQ_TIMEOUT = 45
REQ_DELAY   = 1.2   # seconds between requests

# ── Platon — dialogues Jowett, Project Gutenberg ────────────────────────────
# Tous sont déjà dans graph v13 (tradition_label=GRECO_LATIN_AXIAL,
# tradition_micro=GREEK_PLATONIC) avec deg=34-45.
# NB: plato_parmenides (PG 1687) déjà signé en §233 — exclus ici.

PLATO_PG_TEXTS: list[dict[str, Any]] = [
    # deg=45 group
    {"id": "plato_apology",     "pg": 1656, "deg": 45},
    {"id": "plato_crito",       "pg": 1657, "deg": 45},
    {"id": "plato_gorgias",     "pg": 1672, "deg": 45},
    {"id": "plato_protagoras",  "pg": 1591, "deg": 45},
    {"id": "plato_meno",        "pg": 1643, "deg": 45},
    # deg=44
    {"id": "plato_phaedo",      "pg": 1658, "deg": 44},
    # deg=43
    {"id": "plato_symposium",   "pg": 1600, "deg": 43},
    # deg=42
    {"id": "plato_phaedrus",    "pg": 1636, "deg": 42},
    # deg=41
    {"id": "plato_republic",    "pg": 1497, "deg": 41},
    # deg=40
    {"id": "plato_theaetetus",  "pg": 1726, "deg": 40},
    # deg=38
    {"id": "plato_sophist",     "pg": 1735, "deg": 38},
    # deg=37
    {"id": "plato_timaeus",     "pg": 1572, "deg": 37},
    {"id": "plato_statesman",   "pg": 1744, "deg": 37},
    {"id": "plato_critias",     "pg": 1571, "deg": 37},
    # deg=34
    {"id": "plato_laws",        "pg": 1750, "deg": 34},
    {"id": "plato_euthyphro",   "pg": 1642, "deg": 34},
    {"id": "plato_charmides",   "pg": 1580, "deg": 34},
    {"id": "plato_philebus",    "pg": 1746, "deg": 34},
]

# ── Aristote — MIT Internet Classics Archive ─────────────────────────────────
# Tous deg=49 dans graph v13.
# Structure MIT Classics: index page + section pages avec <pre> text.

ARISTOTLE_MIT_TEXTS: list[dict[str, Any]] = [
    {"id": "aristotle_metaphysics",            "mit": "Aristotle/metaphysics"},
    {"id": "aristotle_nicomachean_ethics",     "mit": "Aristotle/nicomachaen"},
    {"id": "aristotle_de_anima",               "mit": "Aristotle/soul"},
    {"id": "aristotle_physics",                "mit": "Aristotle/physics"},
    {"id": "aristotle_categories",             "mit": "Aristotle/categories"},
    {"id": "aristotle_de_interpretatione",     "mit": "Aristotle/interpretation"},
    {"id": "aristotle_prior_analytics",        "mit": "Aristotle/prior"},
    {"id": "aristotle_posterior_analytics",    "mit": "Aristotle/posterior"},
    {"id": "aristotle_topics",                 "mit": "Aristotle/topics"},
    {"id": "aristotle_sophistical_refutations","mit": "Aristotle/sophistical_refut"},
    {"id": "aristotle_de_caelo",               "mit": "Aristotle/heavens"},
    {"id": "aristotle_parts_of_animals",       "mit": "Aristotle/parts_animals"},
    {"id": "aristotle_politics",               "mit": "Aristotle/politics"},
    {"id": "aristotle_rhetoric",               "mit": "Aristotle/rhetoric"},
    {"id": "aristotle_poetics",                "mit": "Aristotle/poetics"},
]

MIT_BASE = "https://classics.mit.edu/"


# ── Fetch helpers ─────────────────────────────────────────────────────────────

def _get(url: str, cache_key: str) -> str | None:
    cache_file = CACHE_DIR / f"{cache_key}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8", errors="replace")
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQ_TIMEOUT,
                         verify=False)  # some servers have cert issues
        time.sleep(REQ_DELAY)
        if r.status_code == 200:
            text = r.text
            cache_file.write_text(text, encoding="utf-8")
            return text
        print(f"    [HTTP {r.status_code}] {url}")
        return None
    except Exception as e:
        print(f"    [ERR] {url}: {e}")
        return None


def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


def _strip_gutenberg(text: str) -> str:
    """Remove PG header/footer."""
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


def _sign_text(text: str, local_id: str) -> dict[str, Any] | None:
    """Segment text into ~200-word windows, compute V14 signature."""
    words = _tokenize_words(text)
    if len(words) < 1500:
        print(f"    [SKIP] {local_id}: too short ({len(words)} words)")
        return None

    WIN = 200
    STEP = 100
    segments = []
    for i in range(0, len(words) - WIN + 1, STEP):
        segments.append(words[i:i + WIN])

    if not segments:
        return None

    # Aggregate V14 across all segments
    agg_sig: dict[str, float] = {a: 0.0 for a in V14_ATOMS}
    for seg in segments:
        sig = freq_signature(" ".join(seg))
        for a in V14_ATOMS:
            agg_sig[a] += sig.get(a, 0.0)

    total = sum(agg_sig.values())
    if total < 1e-9:
        return None
    norm_sig = {a: round(agg_sig[a] / total, 6) for a in V14_ATOMS}

    return {
        "local_id": local_id,
        "graph_node_id": local_id,     # matches graph v13 node IDs
        "n_segments": len(segments),
        "n_words_total": len(words),
        "v14_signature": norm_sig,
        "v14_top3": sorted(norm_sig.items(), key=lambda x: -x[1])[:3],
        "source": "fetch_v234",
    }


# ── Project Gutenberg fetch ───────────────────────────────────────────────────

def fetch_pg_text(pg_id: int, text_id: str) -> str | None:
    """Try multiple PG URL patterns for a given ID."""
    urls = [
        f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt",
        f"https://www.gutenberg.org/files/{pg_id}/{pg_id}-0.txt",
        f"https://www.gutenberg.org/files/{pg_id}/{pg_id}.txt",
    ]
    for url in urls:
        text = _get(url, f"pg_{pg_id}")
        if text and len(text) > 5000:
            return _strip_gutenberg(text)
    return None


def process_plato(entry: dict) -> dict[str, Any]:
    tid = entry["id"]
    pg  = entry["pg"]
    print(f"  [{tid}] PG {pg}")
    raw = fetch_pg_text(pg, tid)
    if not raw:
        print(f"    [FAIL] PG {pg} not fetched")
        return {"local_id": tid, "status": "failed", "reason": "fetch_error"}

    words = _tokenize_words(raw)
    print(f"    {len(words)} words")

    # Verify content — check first 500 words for expected Greek philosophy keywords
    preview = " ".join(words[:500]).lower()
    if any(k in preview for k in ["london", "alaska", "yukon", "klondike"]):
        return {"local_id": tid, "status": "failed", "reason": "wrong_content_detected"}

    signed = _sign_text(raw, tid)
    if signed is None:
        return {"local_id": tid, "status": "failed", "reason": "sign_error"}

    top3 = signed["v14_top3"]
    print(f"    sig top3: {top3[:3]}")
    return {**signed, "status": "ok", "pg_id": pg}


# ── MIT Classics fetch ────────────────────────────────────────────────────────

def fetch_mit_classic(mit_path: str, text_id: str) -> str | None:
    """
    Fetch all section pages from MIT Classics.
    Pattern: https://classics.mit.edu/Author/work.N.N.html
    """
    index_url = MIT_BASE + mit_path + ".html"
    raw_idx = _get(index_url, f"mit_{text_id}_idx")
    if not raw_idx:
        return None

    soup = BeautifulSoup(raw_idx, "html.parser")
    # Find links to section pages
    work_name = mit_path.split("/")[-1]
    section_urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Section pages: work.N.N.html or work.N.html
        if re.match(rf"{re.escape(work_name)}\.\d", href):
            section_urls.append(urljoin(index_url, href))

    if not section_urls:
        print(f"    [WARN] No section links found on {index_url}")
        return None

    section_urls = sorted(dict.fromkeys(section_urls))
    print(f"    {len(section_urls)} section pages to fetch")

    full_parts: list[str] = []
    for i, url in enumerate(section_urls, 1):
        key = f"mit_{text_id}_s{i:03d}"
        html = _get(url, key)
        if not html:
            continue
        s = BeautifulSoup(html, "html.parser")
        # MIT Classics stores text in <pre> tags
        pre = s.find("pre")
        if pre:
            full_parts.append(pre.get_text())
        else:
            # Fallback: get all paragraph text
            body = s.find("body")
            if body:
                full_parts.append(body.get_text(" ", strip=True))

    return "\n\n".join(full_parts) if full_parts else None


def process_aristotle(entry: dict) -> dict[str, Any]:
    tid = entry["id"]
    mit = entry["mit"]
    print(f"  [{tid}] MIT Classics /{mit}")
    raw = fetch_mit_classic(mit, tid)
    if not raw or len(_tokenize_words(raw)) < 1500:
        # Fallback: try PG if available
        PG_FALLBACK = {
            "aristotle_politics": 6762,
            "aristotle_poetics": 2412,
        }
        pg_id = PG_FALLBACK.get(tid)
        if pg_id:
            print(f"    [FALLBACK] trying PG {pg_id}")
            raw = fetch_pg_text(pg_id, tid)
        if not raw:
            print(f"    [FAIL] {tid}")
            return {"local_id": tid, "status": "failed", "reason": "fetch_error"}

    words = _tokenize_words(raw)
    print(f"    {len(words)} words")

    signed = _sign_text(raw, tid)
    if signed is None:
        return {"local_id": tid, "status": "failed", "reason": "sign_error"}

    top3 = signed["v14_top3"]
    print(f"    sig top3: {top3[:3]}")
    return {**signed, "status": "ok"}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    import urllib3
    urllib3.disable_warnings()

    print("=" * 60)
    print("§234 — fetch Platon (18 dialogues) + Aristote (15 œuvres)")
    print(f"  nipada: {_NIPADA}")
    print("=" * 60)

    signed: list[dict] = []
    failed: list[dict] = []
    t0 = time.time()

    # ── Platon ────────────────────────────────────────────────────────────────
    print(f"\n=== PLATON ({len(PLATO_PG_TEXTS)} dialogues) ===")
    for entry in PLATO_PG_TEXTS:
        result = process_plato(entry)
        if result.get("status") == "ok":
            signed.append(result)
        else:
            failed.append(result)

    # ── Aristote ──────────────────────────────────────────────────────────────
    print(f"\n=== ARISTOTE ({len(ARISTOTLE_MIT_TEXTS)} œuvres) ===")
    for entry in ARISTOTLE_MIT_TEXTS:
        result = process_aristotle(entry)
        if result.get("status") == "ok":
            signed.append(result)
        else:
            failed.append(result)

    elapsed = time.time() - t0
    print(f"\n── Résultats ──────────────────────────────────────────────")
    print(f"  Signés   : {len(signed)}")
    print(f"  Échoués  : {len(failed)}")
    print(f"  Durée    : {elapsed:.1f}s")

    # Résumé signatures
    print("\n── Signatures V14 ─────────────────────────────────────────")
    for t in signed:
        top = t.get("v14_top3", [])
        top_str = ", ".join(f"{a}({v:.3f})" for a, v in top[:3])
        print(f"  {t['local_id']:45s}  {t['n_words_total']:>8}w  {top_str}")

    # ── Écriture corpus ───────────────────────────────────────────────────────
    # Nettoyage: enlever champs internes avant sauvegarde
    def _clean(t: dict) -> dict:
        return {k: v for k, v in t.items()
                if k not in ("status", "pg_id")}

    corpus_out = {
        "version": "v234",
        "description": "§234 Platon + Aristote — traduits Jowett/MIT Classics",
        "n_signed": len(signed),
        "n_failed": len(failed),
        "signed": [_clean(t) for t in signed],
        "failed": failed,
    }
    OUT_CORPUS.write_text(json.dumps(corpus_out, ensure_ascii=False, indent=2))
    print(f"\nÉcrit: {OUT_CORPUS}")

    # ── Rapport fetch ─────────────────────────────────────────────────────────
    report = {
        "section": "§234",
        "elapsed_s": round(elapsed, 1),
        "n_signed": len(signed),
        "n_failed": len(failed),
        "signed_ids": [t["local_id"] for t in signed],
        "failed_ids": [t["local_id"] for t in failed],
    }
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Écrit: {OUT_REPORT}")


if __name__ == "__main__":
    main()

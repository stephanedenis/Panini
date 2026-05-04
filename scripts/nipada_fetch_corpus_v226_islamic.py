#!/usr/bin/env python3
"""
§226 — Extension islamique: fetch + signature V14 pour textes philosophiques islamiques.

Stratégie:
  - Textes cibles: graph_node_ids déjà présents dans nipada_v219_graph_v13.json
  - Sources: Internet Archive (IA) textes en domaine public, traductions anglaises
  - Cible: 4–6 textes signés V14

Textes prioritaires (dans le graph):
  ghazali_munqidh         → IA: TheDelivererFromError
  ibn_rushd_tahafut_tahafut → IA: averroes-tahafut-al-tahafut (Averroes reply)
  ibn_rushd_fasl_maqal    → IA: ibn-rushd-averroes-the-decisive-treatise
  ghazali_ihya            → IA: Revival of Religious Sciences (partial)
  ghazali_tahafut_falasifa → IA: al-ghazali-incoherence (via Sacred Texts)

Produit:
  Panini-Research/nipada/corpus/signed_corpus_v226_islamic.json
  Panini-Research/nipada/falsification/nipada_v226_fetch_report.json
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

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

OUT_CORPUS = CORPUS_DIR / "signed_corpus_v226_islamic.json"
OUT_REPORT = FALSI_DIR  / "nipada_v226_fetch_report.json"

# ---------------------------------------------------------------------------
# Textes islamiques à fetcher
# Chaque entrée a:
#   - id: graph_node_id (doit correspondre à nipada_v219_graph_v13.json)
#   - urls: liste d'URLs à essayer dans l'ordre
#   - ia_identifier: identifiant Internet Archive (pour construire fallback URLs)
# ---------------------------------------------------------------------------
ISLAMIC_TEXTS: list[dict[str, Any]] = [
    # ── Ibn Rushd (Averroes) — Tahafut al-Tahafut (Incoherence of the Incoherence) ──
    # Source: IA identifier averroes-tahafut-al-tahafut-the-incoherence-of-the-incoherence-volumes-i-and-ii
    # File confirmed: 1.7MB djvu.txt, Simon Van den Bergh translation
    {
        "id": "ibn_rushd_tahafut_tahafut",
        "author": "ibn_rushd",
        "title_en": "The Incoherence of the Incoherence (Tahafut al-Tahafut) — Van den Bergh trans.",
        "tradition": "ISLAM_FALSAFA",
        "graph_node_id": "ibn_rushd_tahafut_tahafut",
        "urls": [
            "https://archive.org/download/averroes-tahafut-al-tahafut-the-incoherence-of-the-incoherence-volumes-i-and-ii/"
            "Averroes%2C%20Tahafut%20Al-Tahafut%20The%20Incoherence%20of%20the%20Incoherence%20Volumes%20I%20and%20II_djvu.txt",
        ],
    },
    # ── Ibn Rushd — Fasl al-Maqal (Decisive Treatise) ───────────────────────
    # Source: IA identifier ibn-rushd-averroes-the-decisive-treatise-rafiabadi-2
    # File confirmed: 144KB djvu.txt
    {
        "id": "ibn_rushd_fasl_maqal",
        "author": "ibn_rushd",
        "title_en": "The Decisive Treatise (Fasl al-Maqal) — Averroes",
        "tradition": "ISLAM_FALSAFA",
        "graph_node_id": "ibn_rushd_fasl_maqal",
        "urls": [
            "https://archive.org/download/ibn-rushd-averroes-the-decisive-treatise-rafiabadi-2/"
            "Averroes%20-%20THE%20DECISIVE%20TREATISE_djvu.txt",
        ],
    },
    # ── al-Ghazali — Alchemy of Happiness (Kimiya-yi Sa'adat) ───────────────
    # Close abridgment of the Ihya; used for ghazali_ihya node
    # Source: IA identifier alchemy-of-happiness (Claud Field trans., public domain)
    # File confirmed: 141KB djvu.txt
    {
        "id": "ghazali_ihya",
        "author": "al_ghazali",
        "title_en": "The Alchemy of Happiness (Kimiya-yi Sa'adat) — Field trans.",
        "tradition": "ISLAM_SUFISM",
        "graph_node_id": "ghazali_ihya",
        "urls": [
            "https://archive.org/download/alchemy-of-happiness/alchemy-of-happiness_djvu.txt",
        ],
    },
    # ── Rumi — Masnavi Book I (Whinfield abridged, public domain) ───────────
    # Source: IA Masnavi-English collection, file 131_masnavi_b1_djvu.txt
    # File confirmed: 131KB djvu.txt, E.H. Whinfield translation
    {
        "id": "rumi_mathnawi",
        "author": "rumi",
        "title_en": "Masnavi i Ma'navi Book I (Whinfield abridged translation)",
        "tradition": "ISLAM_SUFISM",
        "graph_node_id": "rumi_mathnawi",
        "urls": [
            "https://archive.org/download/Masnavi-English/131_masnavi_b1_djvu.txt",
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers (same as v225d pattern)
# ---------------------------------------------------------------------------

def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


def _strip_boilerplate(text: str) -> str:
    """Remove Project Gutenberg and common IA OCR boilerplate."""
    # Gutenberg header/footer
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "End of the Project Gutenberg EBook",
        "End of Project Gutenberg's",
    ]
    best_start = 0
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            eol = text.find("\n", idx)
            if eol != -1:
                best_start = max(best_start, eol + 1)
    best_end = len(text)
    for marker in end_markers:
        idx = text.rfind(marker)
        if idx != -1:
            best_end = min(best_end, idx)
    return text[best_start:best_end]


def _segments_700(words: list[str], min_words: int = 500, max_words: int = 1000) -> list[str]:
    if not words:
        return []
    seg_len = 700
    segments = []
    i = 0
    n = len(words)
    while i < n:
        j = min(i + seg_len, n)
        chunk = words[i:j]
        if len(chunk) < min_words:
            break
        segments.append(" ".join(chunk))
        i = j
    if not segments and len(words) >= min_words:
        segments.append(" ".join(words[:max_words]))
    return segments


def _download_first_ok(urls: list[str], timeout: int = 30) -> tuple[str, str]:
    last_err: Exception = RuntimeError("no URLs provided")
    for url in urls:
        try:
            r = requests.get(url, timeout=timeout,
                             headers={"User-Agent": "Mozilla/5.0 (compatible; NIPADA-research/1.0)"})
            r.raise_for_status()
            text = r.content.decode("utf-8", errors="replace").replace("\r\n", "\n")
            if len(text) < 1000:
                last_err = RuntimeError(f"Response too short ({len(text)} chars) from {url}")
                continue
            return text, url
        except Exception as e:
            last_err = e
            time.sleep(1.0)
    raise last_err


def _top3(sig: dict[str, float]) -> list[list[Any]]:
    return [[k, v] for k, v in sorted(sig.items(), key=lambda kv: kv[1], reverse=True)[:3]]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    signed_list: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []

    print(f"§226 — Fetch Islamic corpus ({len(ISLAMIC_TEXTS)} textes cibles)")

    for entry in ISLAMIC_TEXTS:
        tid = entry["id"]
        print(f"\n  [{tid}] fetching…")
        row: dict[str, Any] = {"id": tid, "status": "ERROR", "url_used": None, "error": None}

        try:
            raw_text, url_used = _download_first_ok(entry["urls"])
            row["url_used"] = url_used
        except Exception as exc:
            row["error"] = str(exc)
            print(f"    ERROR fetch: {exc}")
            report_rows.append(row)
            continue

        # Clean and tokenize
        cleaned = _strip_boilerplate(raw_text)
        words = _tokenize_words(cleaned)
        if len(words) < 2000:
            row["error"] = f"Too few words after cleaning: {len(words)}"
            print(f"    ERROR: {row['error']}")
            report_rows.append(row)
            continue

        segments = _segments_700(words)
        if not segments:
            row["error"] = "No segments generated"
            print(f"    ERROR: {row['error']}")
            report_rows.append(row)
            continue

        # Sign (freq_signature expects a single string)
        try:
            sig = freq_signature("\n\n".join(segments), lang="eng")
        except Exception as exc:
            row["error"] = f"freq_signature failed: {exc}"
            print(f"    ERROR signing: {exc}")
            report_rows.append(row)
            continue

        signed_obj: dict[str, Any] = {
            "local_id": tid,
            "graph_node_id": entry["graph_node_id"],
            "catalog": "nipada_v226_islamic",
            "tradition_label": entry["tradition"],
            "lang": "en",
            "n_chars": len(cleaned),
            "n_words": len(words),
            "n_segments": len(segments),
            "v14_signature": sig,
            "v14_top3": _top3(sig),
            "matched": True,
            "lexicon_version": "v14",
            "source": "internet_archive",
            "url": url_used,
            "title_en": entry["title_en"],
            "author": entry["author"],
        }
        signed_list.append(signed_obj)

        top3_str = ", ".join(f"{a}({v:.3f})" for a, v in sig.items()
                             if [a, v] in _top3(sig))
        print(f"    OK: {len(segments)} segs, {len(words):,} words — top3: {_top3(sig)}")
        row["status"] = "OK"
        row["n_segments"] = len(segments)
        row["n_words"] = len(words)
        row["v14_top3"] = _top3(sig)
        report_rows.append(row)
        time.sleep(0.5)

    # Output
    corpus_out = {
        "version": "v226",
        "description": "§226 Islamic extension: public domain EN translations, signed V14",
        "n_signed": len(signed_list),
        "n_failed": len([r for r in report_rows if r["status"] != "OK"]),
        "signed": signed_list,
    }

    OUT_CORPUS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CORPUS, "w", encoding="utf-8") as fh:
        json.dump(corpus_out, fh, ensure_ascii=False, indent=2)

    report_out = {
        "version": "nipada_v226_fetch_report",
        "n_texts_attempted": len(ISLAMIC_TEXTS),
        "n_ok": len([r for r in report_rows if r["status"] == "OK"]),
        "n_failed": len([r for r in report_rows if r["status"] != "OK"]),
        "rows": report_rows,
    }
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        json.dump(report_out, fh, ensure_ascii=False, indent=2)

    print(f"\n§226 terminé: {len(signed_list)}/{len(ISLAMIC_TEXTS)} signés")
    print(f"  Corpus: {OUT_CORPUS}")
    print(f"  Report: {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

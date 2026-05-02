#!/usr/bin/env python3
"""
§225 — Fetch + segmentation + signature V14 (Greco-Latin shortlist v224).

Lit la sortie §224 et télécharge jusqu'à 10 textes depuis Gutendex.
Produit:
- Panini-Research/nipada/corpus/signed_corpus_v225_greco_latin.json
- Panini-Research/nipada/falsification/nipada_v225_fetch_report.json
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
FALSI_DIR = _NIPADA / "falsification"
IN_PATH = CORPUS_DIR / "nipada_v224_greco_latin_catalog.json"
OUT_CORPUS = CORPUS_DIR / "signed_corpus_v225_greco_latin.json"
OUT_REPORT = FALSI_DIR / "nipada_v225_fetch_report.json"


def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


def _segments_700(words: list[str], min_words: int = 500, max_words: int = 1000) -> list[str]:
    if not words:
        return []
    seg_len = min(700, max_words)
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


def _download_text(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    txt = r.text
    txt = txt.replace("\r\n", "\n")
    return txt


def _top3(sig: dict[str, float]) -> list[list[Any]]:
    return [[k, v] for k, v in sorted(sig.items(), key=lambda kv: kv[1], reverse=True)[:3]]


def main() -> int:
    if not IN_PATH.exists():
        sys.exit(f"ERROR: missing input {IN_PATH}; run §224 first")

    with IN_PATH.open("r", encoding="utf-8") as f:
        v224 = json.load(f)

    rows = [r for r in v224.get("rows", []) if r.get("status") == "OK" and (r.get("gutendex") or {}).get("best")]
    rows = rows[:10]

    signed: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []

    print("§225 — Fetch + signature Greco-Latin")
    print(f"  Entrées exploitables depuis §224: {len(rows)}")

    for idx, row in enumerate(rows, start=1):
        best = row["gutendex"]["best"]
        url = best["url_text"]
        local_id = str(row["id"])
        tradition = str(row.get("macro_culture") or "GRECO_LATIN") + "_" + str(row.get("epoch") or "UNKNOWN").upper()

        print(f"  [{idx:02d}] {local_id} — download")
        try:
            raw = _download_text(url)
            words = _tokenize_words(raw)
            segments = _segments_700(words)

            if not segments:
                raise RuntimeError("insufficient text length for 500-word segment")

            text_all = "\n\n".join(segments)
            sig = freq_signature(text_all, lang="eng")

            signed.append(
                {
                    "local_id": local_id,
                    "graph_node_id": local_id,
                    "catalog": "greco_latin_v225",
                    "tradition_label": tradition,
                    "lang": "eng",
                    "n_chars": len(text_all),
                    "n_words": sum(len(_tokenize_words(s)) for s in segments),
                    "n_segments": len(segments),
                    "v14_signature": sig,
                    "v14_top3": _top3(sig),
                    "matched": True,
                    "lexicon_version": "v212f",
                    "source": "gutendex",
                    "url": url,
                    "title_en": row.get("title_en"),
                    "author": row.get("author"),
                }
            )

            report_rows.append(
                {
                    "id": local_id,
                    "status": "OK",
                    "url": url,
                    "n_words_raw": len(words),
                    "n_segments": len(segments),
                    "n_words_signed": sum(len(_tokenize_words(s)) for s in segments),
                }
            )
        except Exception as e:
            report_rows.append(
                {
                    "id": local_id,
                    "status": "ERR",
                    "url": url,
                    "error": str(e),
                }
            )
        time.sleep(0.2)

    out_corpus = {
        "version": "v225_greco_latin",
        "date": time.strftime("%Y-%m-%d"),
        "base": "v224_greco_latin_catalog",
        "n_signed": len(signed),
        "v14_atoms": V14_ATOMS,
        "signed": signed,
    }

    out_report = {
        "version": "v225_fetch_report",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_input_ok": len(rows),
        "n_signed": len(signed),
        "n_errors": sum(1 for r in report_rows if r["status"] != "OK"),
        "rows": report_rows,
    }

    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    FALSI_DIR.mkdir(parents=True, exist_ok=True)

    with OUT_CORPUS.open("w", encoding="utf-8") as f:
        json.dump(out_corpus, f, ensure_ascii=False, indent=2)
    with OUT_REPORT.open("w", encoding="utf-8") as f:
        json.dump(out_report, f, ensure_ascii=False, indent=2)

    print(f"\nÉcrit: {OUT_CORPUS}")
    print(f"Écrit: {OUT_REPORT}")
    print(f"  n_signed={len(signed)} / {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

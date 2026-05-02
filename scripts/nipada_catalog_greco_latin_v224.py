#!/usr/bin/env python3
"""
§224 — Catalogue Greco-Latin prioritaire + validation URLs.

Produit une short-list de 10 textes et teste des URLs candidates via Gutendex.
Sortie: Panini-Research/nipada/corpus/nipada_v224_greco_latin_catalog.json
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

CORPUS_DIR = _NIPADA / "corpus"
OUT_PATH = CORPUS_DIR / "nipada_v224_greco_latin_catalog.json"

SRC_GRECO_AXIAL = CORPUS_DIR / "catalog_greco_latin_axial_v206k.json"
SRC_GRECO_LATE = CORPUS_DIR / "catalog_greco_latin_late_antique_v206l.json"
SRC_WESTERN = CORPUS_DIR / "catalog_western_rational_early_modern_v206n.json"

TARGET_AUTHORS = [
    "plato",
    "aristotle",
    "plotinus",
    "epictetus",
    "marcus_aurelius",
    "lucretius",
    "cicero",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _pick_priorities(works: list[dict[str, Any]], k: int = 10) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for author in TARGET_AUTHORS:
        for w in works:
            wid = str(w.get("id", ""))
            wa = str(w.get("author", "")).lower()
            if wid in seen_ids:
                continue
            if author in wa:
                selected.append(w)
                seen_ids.add(wid)
                break
        if len(selected) >= k:
            return selected

    for w in works:
        wid = str(w.get("id", ""))
        if wid in seen_ids:
            continue
        selected.append(w)
        seen_ids.add(wid)
        if len(selected) >= k:
            break
    return selected


def _query_gutendex(title: str, author: str) -> dict[str, Any]:
    q = f"{title} {author}".strip()
    url = "https://gutendex.com/books"
    r = requests.get(url, params={"search": q}, timeout=20)
    r.raise_for_status()
    payload = r.json()
    results = payload.get("results", [])

    best = None
    for item in results:
        formats = item.get("formats", {}) or {}
        txt_url = (
            formats.get("text/plain; charset=utf-8")
            or formats.get("text/plain")
            or formats.get("text/html; charset=utf-8")
            or formats.get("text/html")
        )
        if txt_url:
            best = {
                "gutendex_id": item.get("id"),
                "title": item.get("title"),
                "authors": [a.get("name") for a in item.get("authors", [])],
                "download_count": item.get("download_count", 0),
                "url_text": txt_url,
            }
            break

    return {
        "query": q,
        "num_results": len(results),
        "best": best,
    }


def main() -> int:
    src_axial = _load_json(SRC_GRECO_AXIAL)
    src_late = _load_json(SRC_GRECO_LATE)
    src_west = _load_json(SRC_WESTERN)

    all_works = (
        src_axial.get("works", [])
        + src_late.get("works", [])
        + src_west.get("works", [])
    )

    shortlist = _pick_priorities(all_works, k=10)

    rows = []
    print("§224 — Catalogue Greco-Latin prioritaire")
    print(f"  Sources: {len(all_works)} oeuvres cataloguées")
    print(f"  Shortlist: {len(shortlist)}")

    for i, w in enumerate(shortlist, start=1):
        title = _safe(str(w.get("title_en") or w.get("title_original") or w.get("id")))
        author = _safe(str(w.get("author") or "unknown"))
        print(f"  [{i:02d}] {w.get('id')} :: {title} :: {author}")
        try:
            hit = _query_gutendex(title=title, author=author)
            status = "OK" if hit.get("best") else "MISS"
        except Exception as e:
            hit = {"query": f"{title} {author}", "error": str(e), "best": None}
            status = "ERR"

        rows.append(
            {
                "id": w.get("id"),
                "title_en": w.get("title_en"),
                "title_original": w.get("title_original"),
                "author": w.get("author"),
                "macro_culture": w.get("macro_culture"),
                "epoch": w.get("epoch"),
                "tradition_micro": w.get("tradition_micro"),
                "gutendex": hit,
                "status": status,
            }
        )
        time.sleep(0.2)

    n_ok = sum(1 for r in rows if r["status"] == "OK")
    out = {
        "version": "v224_greco_latin_catalog",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": [
            SRC_GRECO_AXIAL.name,
            SRC_GRECO_LATE.name,
            SRC_WESTERN.name,
        ],
        "n_catalog_works": len(all_works),
        "n_shortlist": len(rows),
        "n_gutendex_ok": n_ok,
        "rows": rows,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\nÉcrit: {OUT_PATH}")
    print(f"  Gutendex OK: {n_ok}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

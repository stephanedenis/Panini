#!/usr/bin/env python3
"""
§226 — Catalogue Islamic medieval: shortlist prioritaire + URLs validées.

Valide des ressources Open Library / Internet Archive pour al-Ghazali,
Ibn Rushd, Ibn Sina et génère une shortlist exploitable.
Sortie: Panini-Research/nipada/corpus/nipada_v226_islamic_catalog.json
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
SRC_ISLAMIC = CORPUS_DIR / "catalog_islamic_medieval_v206j.json"
OUT_PATH = CORPUS_DIR / "nipada_v226_islamic_catalog.json"

TARGET_AUTHORS = [
    "al_ghazali",
    "ibn_rushd",
    "ibn_sina",
    "al_farabi",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _search_openlibrary(q: str) -> dict[str, Any]:
    r = requests.get("https://openlibrary.org/search.json", params={"q": q}, timeout=20)
    r.raise_for_status()
    d = r.json()
    docs = d.get("docs", [])
    top = []
    for doc in docs[:3]:
        top.append(
            {
                "title": doc.get("title"),
                "author_name": doc.get("author_name", [])[:3],
                "first_publish_year": doc.get("first_publish_year"),
                "edition_key": doc.get("cover_edition_key"),
                "key": doc.get("key"),
            }
        )
    return {"query": q, "num_found": d.get("numFound", 0), "top3": top}


def _search_archive(q: str) -> dict[str, Any]:
    params = {
        "q": q,
        "fl[]": "identifier,title,creator,year",
        "rows": "3",
        "output": "json",
    }
    r = requests.get("https://archive.org/advancedsearch.php", params=params, timeout=20)
    r.raise_for_status()
    d = r.json()
    docs = (((d or {}).get("response") or {}).get("docs") or [])[:3]
    top = []
    for doc in docs:
        top.append(
            {
                "identifier": doc.get("identifier"),
                "title": doc.get("title"),
                "creator": doc.get("creator"),
                "year": doc.get("year"),
                "url": f"https://archive.org/details/{doc.get('identifier')}" if doc.get("identifier") else None,
            }
        )
    return {"query": q, "num_found": (((d or {}).get("response") or {}).get("numFound", 0)), "top3": top}


def main() -> int:
    src = _load_json(SRC_ISLAMIC)
    works = src.get("works", [])

    shortlist = []
    for author in TARGET_AUTHORS:
        for w in works:
            wa = str(w.get("author") or "")
            if author in wa:
                shortlist.append(w)
        if len(shortlist) >= 8:
            break

    # complete if needed
    seen = {str(w.get("id")) for w in shortlist}
    for w in works:
        wid = str(w.get("id"))
        if wid in seen:
            continue
        if len(shortlist) >= 8:
            break
        shortlist.append(w)
        seen.add(wid)

    print("§226 — Catalogue Islamic medieval")
    print(f"  shortlist={len(shortlist)}")

    rows = []
    for i, w in enumerate(shortlist, start=1):
        title = _norm(str(w.get("title_en") or w.get("title_original") or w.get("id")))
        author = _norm(str(w.get("author") or "unknown"))
        q = f"{title} {author}".strip()
        print(f"  [{i:02d}] {w.get('id')} :: {author}")

        ol = None
        ia = None
        err = None
        try:
            ol = _search_openlibrary(q)
            ia = _search_archive(q)
        except Exception as e:
            err = str(e)

        rows.append(
            {
                "id": w.get("id"),
                "title_en": w.get("title_en"),
                "title_original": w.get("title_original"),
                "author": w.get("author"),
                "tradition_micro": w.get("tradition_micro"),
                "openlibrary": ol,
                "internet_archive": ia,
                "status": "OK" if (ol and ia) else "ERR",
                "error": err,
            }
        )
        time.sleep(0.2)

    out = {
        "version": "v226_islamic_catalog",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_catalog": SRC_ISLAMIC.name,
        "n_shortlist": len(rows),
        "n_ok": sum(1 for r in rows if r["status"] == "OK"),
        "rows": rows,
    }

    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\nÉcrit: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

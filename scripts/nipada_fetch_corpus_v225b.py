#!/usr/bin/env python3
"""
§225b — Fetch + segmentation + signature V14 (Greco-Latin diversifié).

Catalogue codé en dur avec IDs Project Gutenberg directs pour 8 auteurs
distincts — contourne le biais Platon de §225/Gutendex.

Cible: 14 textes, max 2 par auteur, ≥7 auteurs différents.

Produit:
- Panini-Research/nipada/corpus/signed_corpus_v225b_greco_latin.json
- Panini-Research/nipada/falsification/nipada_v225b_fetch_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from collections import Counter

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
OUT_CORPUS = CORPUS_DIR / "signed_corpus_v225b_greco_latin.json"
OUT_REPORT = FALSI_DIR  / "nipada_v225b_fetch_report.json"

# ---------------------------------------------------------------------------
# Catalogue codé en dur — IDs Project Gutenberg + URLs alternatives
# Format: pg_ids = liste prioritaire d'URLs à tenter dans l'ordre
# ---------------------------------------------------------------------------
CATALOG: list[dict[str, Any]] = [
    # ── Marcus Aurelius ─────────────────────────────────────────────────────
    {
        "id": "marcus_aurelius_meditations",
        "author": "marcus_aurelius",
        "title_en": "Meditations",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 2680,
        "urls": [
            "https://www.gutenberg.org/cache/epub/2680/pg2680.txt",
            "https://www.gutenberg.org/files/2680/2680-0.txt",
            "https://www.gutenberg.org/files/2680/2680.txt",
        ],
    },
    # ── Epictetus ───────────────────────────────────────────────────────────
    {
        "id": "epictetus_discourses",
        "author": "epictetus",
        "title_en": "Discourses",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 4135,
        "urls": [
            "https://www.gutenberg.org/cache/epub/4135/pg4135.txt",
            "https://www.gutenberg.org/files/4135/4135-0.txt",
            "https://www.gutenberg.org/files/4135/4135.txt",
        ],
    },
    {
        "id": "epictetus_enchiridion",
        "author": "epictetus",
        "title_en": "Enchiridion",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 45898,
        "urls": [
            "https://www.gutenberg.org/cache/epub/45898/pg45898.txt",
            "https://www.gutenberg.org/files/45898/45898-0.txt",
        ],
    },
    # ── Aristotle ───────────────────────────────────────────────────────────
    {
        "id": "aristotle_nicomachean_ethics",
        "author": "aristotle",
        "title_en": "Nicomachean Ethics",
        "tradition": "GRECO_LATIN_ARISTOTELIAN",
        "pg_id": 2412,
        "urls": [
            "https://www.gutenberg.org/cache/epub/2412/pg2412.txt",
            "https://www.gutenberg.org/files/2412/2412-0.txt",
            "https://www.gutenberg.org/files/2412/2412.txt",
        ],
    },
    {
        "id": "aristotle_politics",
        "author": "aristotle",
        "title_en": "Politics",
        "tradition": "GRECO_LATIN_ARISTOTELIAN",
        "pg_id": 6762,
        "urls": [
            "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
            "https://www.gutenberg.org/files/6762/6762-0.txt",
            "https://www.gutenberg.org/files/6762/6762.txt",
        ],
    },
    # ── Plato (limité à 2) ──────────────────────────────────────────────────
    {
        "id": "plato_phaedo",
        "author": "plato",
        "title_en": "Phaedo",
        "tradition": "GRECO_LATIN_PLATONIC",
        "pg_id": 1658,
        "urls": [
            "https://www.gutenberg.org/cache/epub/1658/pg1658.txt",
            "https://www.gutenberg.org/files/1658/1658-0.txt",
            "https://www.gutenberg.org/files/1658/1658.txt",
        ],
    },
    {
        "id": "plato_timaeus",
        "author": "plato",
        "title_en": "Timaeus",
        "tradition": "GRECO_LATIN_PLATONIC",
        "pg_id": 1572,
        "urls": [
            "https://www.gutenberg.org/cache/epub/1572/pg1572.txt",
            "https://www.gutenberg.org/files/1572/1572-0.txt",
            "https://www.gutenberg.org/files/1572/1572.txt",
        ],
    },
    # ── Lucretius ───────────────────────────────────────────────────────────
    {
        "id": "lucretius_de_rerum_natura",
        "author": "lucretius",
        "title_en": "De Rerum Natura",
        "tradition": "GRECO_LATIN_EPICUREAN",
        "pg_id": 785,
        "urls": [
            "https://www.gutenberg.org/cache/epub/785/pg785.txt",
            "https://www.gutenberg.org/files/785/785-0.txt",
            "https://www.gutenberg.org/files/785/785.txt",
        ],
    },
    # ── Cicero ──────────────────────────────────────────────────────────────
    {
        "id": "cicero_de_officiis",
        "author": "cicero",
        "title_en": "De Officiis (On Duties)",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 47887,
        "urls": [
            "https://www.gutenberg.org/cache/epub/47887/pg47887.txt",
            "https://www.gutenberg.org/files/47887/47887-0.txt",
            # fallback: Tusculan Disputations (PG 2990)
            "https://www.gutenberg.org/cache/epub/2990/pg2990.txt",
        ],
    },
    {
        "id": "cicero_de_natura_deorum",
        "author": "cicero",
        "title_en": "De Natura Deorum (On the Nature of the Gods)",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 33428,
        "urls": [
            "https://www.gutenberg.org/cache/epub/33428/pg33428.txt",
            "https://www.gutenberg.org/files/33428/33428-0.txt",
        ],
    },
    # ── Seneca ──────────────────────────────────────────────────────────────
    {
        "id": "seneca_epistulae_morales",
        "author": "seneca",
        "title_en": "Epistulae Morales (Letters to Lucilius)",
        "tradition": "GRECO_LATIN_STOIC",
        "pg_id": 1700,
        "urls": [
            "https://www.gutenberg.org/cache/epub/1700/pg1700.txt",
            "https://www.gutenberg.org/files/1700/1700-0.txt",
            "https://www.gutenberg.org/files/1700/1700.txt",
        ],
    },
    # ── Plotinus (via sacred-texts mirror) ─────────────────────────────────
    {
        "id": "plotinus_enneads",
        "author": "plotinus",
        "title_en": "Enneads (MacKenna translation)",
        "tradition": "GRECO_LATIN_NEOPLATONIC",
        "pg_id": None,
        "urls": [
            "https://en.wikisource.org/w/index.php?title=The_Enneads&action=raw",
            "https://archive.org/download/plotini-opera-omnia/plotinus_enneads_mackenna.txt",
        ],
    },
    # ── Plutarch ────────────────────────────────────────────────────────────
    {
        "id": "plutarch_moralia",
        "author": "plutarch",
        "title_en": "Moralia (selected essays)",
        "tradition": "GRECO_LATIN_MIDDLE_PLATONIC",
        "pg_id": 14033,
        "urls": [
            "https://www.gutenberg.org/cache/epub/14033/pg14033.txt",
            "https://www.gutenberg.org/files/14033/14033-0.txt",
            "https://www.gutenberg.org/files/14033/14033.txt",
        ],
    },
    {
        "id": "plutarch_parallel_lives",
        "author": "plutarch",
        "title_en": "Parallel Lives (Dryden translation)",
        "tradition": "GRECO_LATIN_MIDDLE_PLATONIC",
        "pg_id": 674,
        "urls": [
            "https://www.gutenberg.org/cache/epub/674/pg674.txt",
            "https://www.gutenberg.org/files/674/674-0.txt",
            "https://www.gutenberg.org/files/674/674.txt",
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


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
    """Try URLs in order; return (content, url_used) or raise."""
    last_err = RuntimeError("no URLs provided")
    for url in urls:
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.text.replace("\r\n", "\n"), url
        except Exception as e:
            last_err = e
            time.sleep(0.3)
    raise last_err


def _top3(sig: dict[str, float]) -> list[list[Any]]:
    return [[k, v] for k, v in sorted(sig.items(), key=lambda kv: kv[1], reverse=True)[:3]]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=14, help="nombre cible de textes signés")
    ap.add_argument("--max-per-author", type=int, default=2, help="borne max par auteur")
    args = ap.parse_args()

    signed: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []
    by_author: Counter = Counter()

    print("§225b — Fetch + signature Greco-Latin diversifié")
    print(f"  Catalogue: {len(CATALOG)} entrées  target={args.target}  max_per_author={args.max_per_author}")

    for entry in CATALOG:
        if len(signed) >= args.target:
            break

        author = entry["author"]
        if by_author[author] >= args.max_per_author:
            print(f"  [SKIP] {entry['id']} — auteur {author} déjà à {by_author[author]}/{args.max_per_author}")
            continue

        print(f"  [{len(signed)+1:02d}] {entry['id']} — téléchargement…", end=" ", flush=True)
        try:
            raw, url_used = _download_first_ok(entry["urls"])
            words = _tokenize_words(raw)
            segments = _segments_700(words)

            if not segments:
                raise RuntimeError(f"texte trop court ({len(words)} mots, minimum 500)")

            text_all = "\n\n".join(segments)
            sig = freq_signature(text_all, lang="eng")

            signed.append(
                {
                    "local_id": entry["id"],
                    "graph_node_id": entry["id"],
                    "catalog": "greco_latin_v225b",
                    "tradition_label": entry["tradition"],
                    "lang": "eng",
                    "n_chars": len(text_all),
                    "n_words": sum(len(_tokenize_words(s)) for s in segments),
                    "n_segments": len(segments),
                    "v14_signature": sig,
                    "v14_top3": _top3(sig),
                    "matched": False,          # pas encore appairé au graph
                    "lexicon_version": "v212f",
                    "source": "gutenberg_direct" if entry["pg_id"] else "wikisource_archive",
                    "url": url_used,
                    "title_en": entry["title_en"],
                    "author": author,
                    "pg_id": entry["pg_id"],
                }
            )
            by_author[author] += 1
            print(f"OK ({len(segments)} segments, {len(words):,} mots)")

            report_rows.append(
                {
                    "id": entry["id"],
                    "status": "OK",
                    "url": url_used,
                    "n_words_raw": len(words),
                    "n_segments": len(segments),
                }
            )
        except Exception as e:
            print(f"ERR — {e}")
            report_rows.append(
                {
                    "id": entry["id"],
                    "status": "ERR",
                    "urls_tried": entry["urls"],
                    "error": str(e),
                }
            )

        time.sleep(0.3)

    # Summary
    print(f"\n  Signés: {len(signed)}/{args.target}")
    author_dist = dict(Counter(t["author"] for t in signed))
    print(f"  Distribution auteurs: {author_dist}")

    # Write outputs
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    FALSI_DIR.mkdir(parents=True, exist_ok=True)

    out_corpus = {
        "version": "v225b_greco_latin_diversified",
        "date": time.strftime("%Y-%m-%d"),
        "base": "hardcoded_gutenberg_catalog",
        "n_signed": len(signed),
        "author_distribution": author_dist,
        "v14_atoms": V14_ATOMS,
        "signed": signed,
    }

    out_report = {
        "version": "v225b_fetch_report",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_input": len(CATALOG),
        "n_signed": len(signed),
        "n_errors": sum(1 for r in report_rows if r["status"] != "OK"),
        "author_distribution": author_dist,
        "rows": report_rows,
    }

    with OUT_CORPUS.open("w", encoding="utf-8") as f:
        json.dump(out_corpus, f, ensure_ascii=False, indent=2)
    with OUT_REPORT.open("w", encoding="utf-8") as f:
        json.dump(out_report, f, ensure_ascii=False, indent=2)

    print(f"  Écrit: {OUT_CORPUS}")
    print(f"  Écrit: {OUT_REPORT}")
    return 0 if len(signed) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

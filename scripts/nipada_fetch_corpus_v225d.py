#!/usr/bin/env python3
"""
§225d — Extension Greco-Latin ciblée: v225c (8 textes) + Plotin + Xénophon + Thucydide.

Stratégie:
  - Charge v225c (8 textes curated Stoïciens + Aristotéliciens + Épicuriens)
  - Ajoute 3 textes philosophiques argumentatifs choisis pour leur signal:
      plotinus_enneads      Gutenberg PG42933+PG42931 (vols 1+2 concaténés)
      xenophon_memorabilia  Gutenberg PG1177 (dialogue philosophique)
      thucydides_peloponnes Gutenberg PG7142 (prose argumentative, pas narratif)
  - Cible: 11 textes signés (V14)

Produit:
  - Panini-Research/nipada/corpus/signed_corpus_v225d_greco_latin.json
  - Panini-Research/nipada/falsification/nipada_v225d_fetch_report.json
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

V225C_PATH = CORPUS_DIR / "signed_corpus_v225c_greco_latin_curated.json"
OUT_CORPUS = CORPUS_DIR / "signed_corpus_v225d_greco_latin.json"
OUT_REPORT = FALSI_DIR  / "nipada_v225d_fetch_report.json"

# ---------------------------------------------------------------------------
# Nouveaux textes à ajouter (remplaçants des 5 textes bruités retirés)
# ---------------------------------------------------------------------------
NEW_TEXTS: list[dict[str, Any]] = [
    # ── Plotinus — Enneads (vols 1+2 sur Gutenberg, MacKenna translation) ──
    # Vol 1 = PG42933, Vol 2 = PG42931. On concatène pour plus de signal.
    {
        "id": "plotinus_enneads",
        "author": "plotinus",
        "title_en": "Enneads (MacKenna translation, vols 1-2)",
        "tradition": "GRECO_LATIN_NEOPLATONIC",
        "pg_id": 42933,
        "urls": [
            "https://www.gutenberg.org/cache/epub/42933/pg42933.txt",
            "https://www.gutenberg.org/files/42933/42933-0.txt",
        ],
        "extra_urls": [
            # vol 2, concaténé après vol 1 si vol 1 OK
            "https://www.gutenberg.org/cache/epub/42931/pg42931.txt",
            "https://www.gutenberg.org/files/42931/42931-0.txt",
        ],
    },
    # ── Xénophon — Memorabilia (dialogues socratiques argumentatifs) ────────
    {
        "id": "xenophon_memorabilia",
        "author": "xenophon",
        "title_en": "Memorabilia (Recollections of Socrates)",
        "tradition": "GRECO_LATIN_SOCRATIC",
        "pg_id": 1177,
        "urls": [
            "https://www.gutenberg.org/cache/epub/1177/pg1177.txt",
            "https://www.gutenberg.org/files/1177/1177-0.txt",
            "https://www.gutenberg.org/files/1177/1177.txt",
        ],
        "extra_urls": [],
    },
    # ── Thucydide — Guerre du Péloponnèse (prose analytique/argumentative) ──
    # NOTE: Thucydide est historien mais avec un style analytique dense
    # (discours, analyses de causalité). Candidat à retirer si noisy.
    {
        "id": "thucydides_history",
        "author": "thucydides",
        "title_en": "History of the Peloponnesian War",
        "tradition": "GRECO_LATIN_HISTORICAL_ANALYTIC",
        "pg_id": 7142,
        "urls": [
            "https://www.gutenberg.org/cache/epub/7142/pg7142.txt",
            "https://www.gutenberg.org/files/7142/7142-0.txt",
            "https://www.gutenberg.org/files/7142/7142.txt",
        ],
        "extra_urls": [],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


def _strip_gutenberg_header_footer(text: str) -> str:
    """Remove Project Gutenberg boilerplate header and footer."""
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "*END*THE SMALL PRINT",
        "END OF THE SMALL PRINT",
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "End of the Project Gutenberg EBook",
        "End of Project Gutenberg's",
    ]
    # Find start
    best_start = 0
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            end_of_line = text.find("\n", idx)
            if end_of_line != -1:
                best_start = max(best_start, end_of_line + 1)
    # Find end
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
    """Try URLs in order; return (content, url_used) or raise."""
    last_err: Exception = RuntimeError("no URLs provided")
    for url in urls:
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.text.replace("\r\n", "\n"), url
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    raise last_err


def _top3(sig: dict[str, float]) -> list[list[Any]]:
    return [[k, v] for k, v in sorted(sig.items(), key=lambda kv: kv[1], reverse=True)[:3]]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    # 1. Charge v225c
    if not V225C_PATH.exists():
        print(f"ERROR: {V225C_PATH} not found — run v225c first")
        return 1

    with open(V225C_PATH, encoding="utf-8") as fh:
        v225c_data = json.load(fh)

    # v225c uses key "signed" (not "signed_corpus")
    base_texts: list[dict[str, Any]] = v225c_data.get("signed_corpus", v225c_data.get("signed", []))
    print(f"§225d — Build corpus depuis v225c ({len(base_texts)} textes) + {len(NEW_TEXTS)} nouveaux")

    new_signed: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []

    # 2. Fetch nouveaux textes
    for entry in NEW_TEXTS:
        print(f"\n  [{len(new_signed)+1}] {entry['id']} — téléchargement…", end=" ", flush=True)
        try:
            raw, url_used = _download_first_ok(entry["urls"])
            raw = _strip_gutenberg_header_footer(raw)

            # Pour Plotinus: concaténer vol2 si disponible
            if entry.get("extra_urls"):
                try:
                    raw2, _ = _download_first_ok(entry["extra_urls"])
                    raw2 = _strip_gutenberg_header_footer(raw2)
                    raw = raw + "\n\n" + raw2
                    print("(+vol2)", end=" ", flush=True)
                except Exception as e2:
                    print(f"(vol2 skip: {e2})", end=" ", flush=True)

            words = _tokenize_words(raw)
            segments = _segments_700(words)

            if not segments:
                raise RuntimeError(f"texte trop court ({len(words)} mots, minimum 500)")

            text_all = "\n\n".join(segments)
            sig = freq_signature(text_all, lang="eng")

            new_signed.append({
                "local_id": entry["id"],
                "graph_node_id": entry["id"],
                "catalog": "greco_latin_v225d",
                "tradition_label": entry["tradition"],
                "lang": "eng",
                "n_chars": len(text_all),
                "n_words": sum(len(_tokenize_words(s)) for s in segments),
                "n_segments": len(segments),
                "v14_signature": sig,
                "v14_top3": _top3(sig),
                "matched": False,
                "lexicon_version": "v212f",
                "source": "gutenberg_direct",
                "url": url_used,
                "title_en": entry["title_en"],
                "author": entry["author"],
                "pg_id": entry["pg_id"],
            })
            print(f"OK ({len(segments)} segments, {len(words):,} mots)")
            print(f"     top3: {_top3(sig)}")

            report_rows.append({
                "id": entry["id"],
                "status": "OK",
                "url": url_used,
                "n_words_raw": len(words),
                "n_segments": len(segments),
                "v14_top3": _top3(sig),
            })

        except Exception as e:
            print(f"ERR — {e}")
            report_rows.append({"id": entry["id"], "status": "ERR", "error": str(e)})

    # 3. Construit corpus complet
    all_signed = base_texts + new_signed
    print(f"\n  Total v225d: {len(all_signed)} textes "
          f"({len(base_texts)} de v225c + {len(new_signed)} nouveaux)")

    # Résumé signatures
    print("\n  Signatures V14 des nouveaux textes:")
    for t in new_signed:
        print(f"    {t['local_id']:40s}: {t['v14_top3']}")

    # 4. Écrit corpus
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    FALSI_DIR.mkdir(parents=True, exist_ok=True)

    out_obj = {
        "version": "v225d",
        "description": "Greco-Latin extension v225d: v225c (8 curated) + Plotinus + Xenophon + Thucydides",
        "base_corpus": "v225c",
        "n_new": len(new_signed),
        "n_total": len(all_signed),
        "curation_rule": "v225c top-5 noisy removed (plato_phaedo/timaeus, plutarch_moralia/lives, seneca_epistulae); added plotinus, xenophon, thucydides",
        "signed_corpus": all_signed,
    }
    with open(OUT_CORPUS, "w", encoding="utf-8") as fh:
        json.dump(out_obj, fh, ensure_ascii=False, indent=2)
    print(f"\n  → {OUT_CORPUS}")

    report_obj = {
        "version": "v225d",
        "n_ok": sum(1 for r in report_rows if r["status"] == "OK"),
        "n_err": sum(1 for r in report_rows if r["status"] == "ERR"),
        "rows": report_rows,
    }
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        json.dump(report_obj, fh, ensure_ascii=False, indent=2)
    print(f"  → {OUT_REPORT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
§233 — Extension Présocratiques: fetch + signature V14.

Stratégie:
  - Les Présocratiques (Héraclite, Parménide, Empédocle, etc.) n'ont laissé
    que des fragments trop courts pour une signature V14 directe.
  - Solution: utiliser des textes secondaires/compilations en domaine public
    qui contiennent et discutent leurs œuvres de manière substantielle.

Textes cibles:
  1. burnet_early_greek_philosophy — John Burnet, "Early Greek Philosophy"
     (PG 31649) : compilation majeure des Présocratiques avec contexte.
  2. diogenes_laertius_lives_vol1 — Diogenes Laertius, "Lives of Eminent
     Philosophers" vol.1 (PG 57145) : biographies + doxographie.
  3. aristotle_metaphysics — Aristote, "Metaphysics" (PG discussions
     etendues des Présocratiques en Livres I-II).
  4. plato_parmenides — Platon, dialogue "Parmenides" (traitement direct
     de la philosophie de Parménide et de ses paradoxes).

Produit:
  Panini-Research/nipada/corpus/signed_corpus_v233_presocratics.json
  Panini-Research/nipada/falsification/nipada_v233_fetch_report.json
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

OUT_CORPUS = CORPUS_DIR / "signed_corpus_v233_presocratics.json"
OUT_REPORT = FALSI_DIR  / "nipada_v233_fetch_report.json"

# ---------------------------------------------------------------------------
# Textes Présocratiques à fetcher
# Chaque entrée:
#   - id: local_id (descriptif, correspondance graph si disponible)
#   - graph_node_id: ID dans nipada_v219_graph_v13.json (None si absent)
#   - urls: liste à essayer dans l'ordre
# ---------------------------------------------------------------------------
PRESOCRATIC_TEXTS: list[dict[str, Any]] = [
    # ── John Burnet — Early Greek Philosophy ─────────────────────────────────
    # PG 31649 — édition 1892, révisée 1908. Compilation exhaustive des
    # Présocratiques avec fragments traduits et commentaires philologiques.
    # Couvre: Milésiens, Pythagore, Héraclite, Parménide, Empédocle, Zénon,
    # Anaxagore, Leucippe, Démocrite.
    {
        "id": "burnet_early_greek_philosophy",
        "author": "burnet",
        "title_en": "Early Greek Philosophy (3rd ed., 1920) — John Burnet",
        "tradition": "GRECO_PRESOCRATIC",
        "graph_node_id": None,   # nouveau texte, pas encore dans graph v13
        "urls": [
            "https://www.gutenberg.org/cache/epub/31649/pg31649.txt",
            "https://www.gutenberg.org/files/31649/31649-0.txt",
            "https://www.gutenberg.org/files/31649/31649.txt",
        ],
    },

    # ── Diogenes Laertius — Lives of Eminent Philosophers (Vol 1) ────────────
    # PG 57145 — traduction R.D. Hicks (Loeb, 1925). Livre I-VII:
    # biographies de Thalès, Solon, Anaximandre, Héraclite, Parménide, Zénon,
    # Pythagore, Empédocle, etc. Doxographie riche sur les Présocratiques.
    {
        "id": "diogenes_laertius_lives",
        "author": "diogenes_laertius",
        "title_en": "Lives of Eminent Philosophers — Diogenes Laertius (Hicks trans.)",
        "tradition": "GRECO_DOXOGRAPHY",
        "graph_node_id": None,
        "urls": [
            "https://www.gutenberg.org/cache/epub/57145/pg57145.txt",
            "https://www.gutenberg.org/files/57145/57145-0.txt",
            # Fallback via Internet Archive (transcription Hicks)
            "https://archive.org/download/diogenes-laertius-lives-of-eminent-philosophers/"
            "diogenes-laertius-lives-of-eminent-philosophers_djvu.txt",
        ],
    },

    # ── Aristote — Métaphysique (Books I-II) ────────────────────────────────
    # Aristote discute les Présocratiques en détail dans les Livres I (Alpha)
    # et II (petit Alpha) de la Métaphysique — contexte doxographique premier.
    # PG 6762 est la Politique → essai de trouvaille pour la Métaphysique.
    # Alternative confirmée: traduction W.D. Ross via Wikisource.
    {
        "id": "aristotle_metaphysics",
        "author": "aristotle",
        "title_en": "Metaphysics — Aristotle (Ross translation)",
        "tradition": "GRECO_LATIN_ARISTOTELIAN",
        "graph_node_id": "aristotle_metaphysics",   # probablement dans graph
        "urls": [
            # Wikisource plaintext
            "https://en.wikisource.org/w/index.php?title=Metaphysics_(Aristotle)&action=raw",
            # Internet Archive — W.D. Ross translation Vol. VIII
            "https://archive.org/download/aristotle-metaphysics-w-d-ross/"
            "aristotle-metaphysics-w-d-ross_djvu.txt",
            # Backup: Becket Ross IA alternative
            "https://archive.org/download/metaphysics00aris/metaphysics00aris_djvu.txt",
        ],
    },

    # ── Platon — Parménide ───────────────────────────────────────────────────
    # Dialogue qui traite directement de la philosophie de Parménide
    # (théorie des Formes, Un vs Multiple). Gutenberg PG 1663 (dialogues socratiques).
    # Ou partie des œuvres complètes (PG 1656 = Republic, etc.).
    {
        "id": "plato_parmenides",
        "author": "plato",
        "title_en": "Parmenides — Plato (Jowett translation)",
        "tradition": "GRECO_LATIN_PLATONIC",
        "graph_node_id": "plato_parmenides",
        "urls": [
            # Gutenberg PG 1687 — Parmenides (Jowett), confirmé
            "https://www.gutenberg.org/cache/epub/1687/pg1687.txt",
            "https://www.gutenberg.org/files/1687/1687-0.txt",
            "https://www.gutenberg.org/files/1687/1687.txt",
        ],
    },

    # ── Héraclite — Fragments (via Wikisource) ──────────────────────────────
    # Les fragments d'Héraclite (env. 130 fragments) constituent ~5000 mots
    # au total — à la limite du segment minimum mais inclus pour le signal.
    # Source: Wikisource compilation des fragments avec trad. anglaise.
    {
        "id": "heraclitus_fragments",
        "author": "heraclitus",
        "title_en": "Fragments of Heraclitus (trans. Burnet/Kirk)",
        "tradition": "GRECO_PRESOCRATIC",
        "graph_node_id": None,
        "urls": [
            # Wikisource EN — collection Fragments of Heraclitus
            "https://en.wikisource.org/w/index.php?title=Fragments_of_Heraclitus&action=raw",
            # Archive.org — Bywater fragments (1877, public domain)
            "https://archive.org/download/heraclitusofephe00herarich/heraclitusofephe00herarich_djvu.txt",
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text)


def _strip_boilerplate(text: str) -> str:
    """Remove Project Gutenberg header/footer and Wikisource markup."""
    # Gutenberg
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
    text = text[best_start:best_end]

    # Remove Wikisource wikitext markup
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", text)  # [[link|text]] -> text
    text = re.sub(r"\{\{[^}]*\}\}", " ", text)   # templates
    text = re.sub(r"==+[^=]+=+", " ", text)       # section headers
    text = re.sub(r"<[^>]+>", " ", text)           # HTML tags
    text = re.sub(r"\[\d+\]", " ", text)           # footnote refs

    return text


def _segments_700(words: list[str], min_words: int = 400, max_words: int = 1000) -> list[str]:
    """Split word list into segments of ~700 words. Min_words lowered to 400
    to accommodate shorter Presocratic texts."""
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
            r = requests.get(
                url,
                timeout=timeout,
                headers={"User-Agent": "Mozilla/5.0 (compatible; NIPADA-research/1.0)"},
                allow_redirects=True,
            )
            r.raise_for_status()
            text = r.content.decode("utf-8", errors="replace").replace("\r\n", "\n")
            if len(text) < 1000:
                last_err = RuntimeError(f"Response too short ({len(text)} chars) from {url}")
                continue
            return text, url
        except Exception as e:
            last_err = e
            time.sleep(1.5)
    raise last_err


def _top3(sig: dict[str, float]) -> list[list[Any]]:
    return [[k, v] for k, v in sorted(sig.items(), key=lambda kv: kv[1], reverse=True)[:3]]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    signed_list: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []

    print(f"§233 — Fetch Présocratiques ({len(PRESOCRATIC_TEXTS)} textes cibles)")
    print(f"  V14_ATOMS vérifiés: {len(V14_ATOMS)} atomes\n")

    for entry in PRESOCRATIC_TEXTS:
        tid = entry["id"]
        print(f"  [{tid}] fetching…")
        row: dict[str, Any] = {
            "id": tid,
            "status": "ERROR",
            "url_used": None,
            "error": None,
            "n_words": 0,
            "n_segments": 0,
        }

        try:
            raw_text, url_used = _download_first_ok(entry["urls"])
            row["url_used"] = url_used
            print(f"    fetched {len(raw_text):,} chars from {url_used[:60]}…")
        except Exception as exc:
            row["error"] = str(exc)
            print(f"    ERROR fetch: {exc}")
            report_rows.append(row)
            continue

        # Clean and tokenize
        cleaned = _strip_boilerplate(raw_text)
        words = _tokenize_words(cleaned)
        row["n_words"] = len(words)

        if len(words) < 1500:
            row["error"] = f"Too few words after cleaning: {len(words)} (min 1500)"
            print(f"    SKIP: {row['error']}")
            report_rows.append(row)
            continue

        segments = _segments_700(words)
        if not segments:
            row["error"] = "No segments generated (all chunks < 400 words)"
            print(f"    ERROR: {row['error']}")
            report_rows.append(row)
            continue

        row["n_segments"] = len(segments)

        # Sign with V14
        try:
            sig = freq_signature("\n\n".join(segments), lang="eng")
        except Exception as exc:
            row["error"] = f"freq_signature failed: {exc}"
            print(f"    ERROR signing: {exc}")
            report_rows.append(row)
            continue

        gn = entry.get("graph_node_id") or tid

        signed_obj: dict[str, Any] = {
            "local_id": tid,
            "graph_node_id": gn,
            "catalog": "nipada_v233_presocratics",
            "tradition_label": entry["tradition"],
            "lang": "en",
            "n_chars": len(cleaned),
            "n_words": len(words),
            "n_segments": len(segments),
            "v14_signature": sig,
            "v14_top3": _top3(sig),
            "matched": entry.get("graph_node_id") is not None,
            "lexicon_version": "v14",
            "source": "gutenberg_wikisource_ia",
            "url": url_used,
            "title_en": entry["title_en"],
            "author": entry["author"],
        }
        signed_list.append(signed_obj)

        print(f"    OK: {len(segments)} segs, {len(words):,} mots — top3: {_top3(sig)}")
        row["status"] = "OK"
        row["v14_top3"] = _top3(sig)
        report_rows.append(row)
        time.sleep(0.8)

    # Output
    corpus_out = {
        "version": "v233",
        "description": "§233 Presocratic extension: compilations + secondary sources, signed V14",
        "n_signed": len(signed_list),
        "n_failed": len([r for r in report_rows if r["status"] != "OK"]),
        "signed": signed_list,
    }

    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    FALSI_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUT_CORPUS, "w", encoding="utf-8") as fh:
        json.dump(corpus_out, fh, ensure_ascii=False, indent=2)

    report_out = {
        "version": "nipada_v233_fetch_report",
        "n_texts_attempted": len(PRESOCRATIC_TEXTS),
        "n_ok": len([r for r in report_rows if r["status"] == "OK"]),
        "n_failed": len([r for r in report_rows if r["status"] != "OK"]),
        "rows": report_rows,
    }
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        json.dump(report_out, fh, ensure_ascii=False, indent=2)

    print(f"\n§233 terminé: {len(signed_list)}/{len(PRESOCRATIC_TEXTS)} signés")
    print(f"  Corpus: {OUT_CORPUS}")
    print(f"  Report: {OUT_REPORT}")
    return 0 if signed_list else 1


if __name__ == "__main__":
    raise SystemExit(main())

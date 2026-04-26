#!/usr/bin/env python3
"""
§164 — Outil d'acquisition générique pour Phase E.

Tente de récupérer le texte d'une œuvre depuis :
  1. Project Gutenberg (texte brut, format stable)
  2. Wikisource API (HTML rendu nettoyé)
  3. archive.org (avec OCR)

Usage :
    python scripts/nipada_phase_e_acquire_v164.py <work_id>

Si l'acquisition automatique échoue ou produit un texte de qualité
insuffisante, le script écrit un rapport dans corpus/protoatheism/
<work_id>/ACQUISITION_LOG.md indiquant les diagnostics, et marque
l'œuvre comme nécessitant intervention humaine.

NB : ce script ne consomme PAS de token LLM. Il est conçu pour être
exécuté séparément (CLI) avec ou sans agent.
"""

from __future__ import annotations

import argparse
import html as ht
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "protoatheism"
REGISTRY_PATH = ROOT / "research" / "nipada" / "falsification" / "nipada_v163_phase_e_registry.json"

USER_AGENT = "PaniniResearch/1.0 (academic research; https://github.com/stephanedenis/Panini)"


def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_gutenberg_text(book_id: int) -> str | None:
    """Project Gutenberg texte brut. URLs canoniques connues."""
    candidates = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
    ]
    for url in candidates:
        try:
            txt = fetch_url(url)
            if len(txt) > 5000:
                return txt
        except urllib.error.HTTPError:
            continue
        except Exception:
            continue
    return None


def fetch_wikisource_html(lang_code: str, page_title: str) -> str | None:
    """Wikisource via API parse/text. Retourne HTML brut."""
    title_enc = urllib.parse.quote(page_title.replace(" ", "_"))
    url = (f"https://{lang_code}.wikisource.org/w/api.php?"
           f"action=parse&page={title_enc}&prop=text&format=json"
           f"&disablelimitreport=1")
    try:
        raw = fetch_url(url)
        data = json.loads(raw)
        return data.get("parse", {}).get("text", {}).get("*")
    except Exception:
        return None


def html_to_text(html: str) -> str:
    """Conversion HTML → texte brut conservatrice."""
    # Remove scripts/styles
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove footnote refs
    text = re.sub(r"<sup[^>]*>.*?</sup>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Block-level tags become \n
    text = re.sub(r"</?(p|div|h[1-6]|li|tr|br)[^>]*>", "\n", text, flags=re.IGNORECASE)
    # Strip remaining tags
    text = re.sub(r"<[^>]+>", "", text)
    text = ht.unescape(text)
    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def gutenberg_strip_header(text: str) -> str:
    """Retire les en-têtes/queues légales de Project Gutenberg."""
    start_pat = re.compile(r"\*\*\*\s*START OF .* PROJECT GUTENBERG.*?\*\*\*", re.IGNORECASE)
    end_pat = re.compile(r"\*\*\*\s*END OF .* PROJECT GUTENBERG.*?\*\*\*", re.IGNORECASE)
    m_start = start_pat.search(text)
    m_end = end_pat.search(text)
    if m_start and m_end:
        return text[m_start.end():m_end.start()].strip()
    return text


def acquire(work_id: str, registry: dict) -> dict:
    work = next((w for w in registry["works"] if w["id"] == work_id), None)
    if work is None:
        return {"status": "ERROR", "reason": f"work_id {work_id} not in registry"}

    work_dir = CORPUS_DIR / work_id
    log = []
    text = None

    # Stratégie par work_id (mappings explicites)
    strategies = {
        "hobbes_leviathan_4": [("gutenberg", 3207)],
        "spinoza_ethica_1": [
            ("wikisource", "la", "Ethica/Pars_I"),
            ("gutenberg", 3800),
        ],
        "diderot_pensees_phil": [
            ("wikisource", "fr", "Pensées_philosophiques"),
        ],
        "la_mettrie_homme_machine": [
            ("wikisource", "fr", "L’Homme_Machine"),
            ("wikisource", "fr", "L'Homme_Machine"),
        ],
        "voltaire_dict_phil": [
            ("wikisource", "fr", "Dictionnaire_philosophique"),
        ],
        "mozi_selections": [
            ("wikisource", "zh", "墨子"),
        ],
        "han_feizi_selections": [
            ("ctext", "hanfeizi"),  # placeholder — ctext.org needs custom parsing
        ],
        "al_razi_doxography": [],  # édition critique imprimée requise
        "ibn_rawandi_extended": [],  # édition critique imprimée requise
    }

    for strategy in strategies.get(work_id, []):
        kind = strategy[0]
        try:
            if kind == "gutenberg":
                bid = strategy[1]
                log.append(f"Trying Project Gutenberg #{bid}")
                txt = fetch_gutenberg_text(bid)
                if txt:
                    text = gutenberg_strip_header(txt)
                    log.append(f"  → OK, raw len = {len(txt)}, stripped len = {len(text)}")
                    break
                log.append("  → FAIL")
            elif kind == "wikisource":
                lang_code, title = strategy[1], strategy[2]
                log.append(f"Trying Wikisource {lang_code} : {title}")
                html = fetch_wikisource_html(lang_code, title)
                if html and len(html) > 10000:
                    text = html_to_text(html)
                    log.append(f"  → OK, html={len(html)}, text={len(text)}")
                    break
                else:
                    log.append(f"  → too short ({len(html) if html else 0}), likely transclusion stub")
            elif kind == "ctext":
                log.append(f"ctext.org strategy not yet implemented — manual curation required")
            else:
                log.append(f"unknown strategy {kind}")
        except Exception as e:
            log.append(f"  → EXCEPTION {type(e).__name__}: {e}")

    if text and len(text) >= 5000:
        out_path = work_dir / "raw_text.txt"
        out_path.write_text(text, encoding="utf-8")
        # Remove pending status
        status_file = work_dir / "STATUS_PENDING.txt"
        if status_file.exists():
            status_file.unlink()
        result = {"status": "ACQUIRED_RAW", "len": len(text), "path": str(out_path.relative_to(ROOT))}
    else:
        result = {"status": "MANUAL_INTERVENTION_REQUIRED", "len": len(text) if text else 0}

    log_path = work_dir / "ACQUISITION_LOG.md"
    log_path.write_text(
        f"# Journal d'acquisition — {work_id}\n\n"
        + "\n".join(f"- {line}" for line in log)
        + f"\n\n**Statut final** : `{result['status']}`\n",
        encoding="utf-8"
    )

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("work_id", nargs="?", help="ID de l'œuvre, ou 'all' pour tout tenter")
    args = parser.parse_args()

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    targets = ([w["id"] for w in registry["works"]]
               if args.work_id == "all" or args.work_id is None
               else [args.work_id])

    results = []
    for wid in targets:
        print(f"\n=== {wid} ===")
        r = acquire(wid, registry)
        r["work_id"] = wid
        results.append(r)
        print(f"  → {r['status']}")
        if "len" in r:
            print(f"  → text length : {r['len']} chars")

    print()
    print("─── Résumé ───")
    by_status: dict = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(r["work_id"])
    for status, ids in by_status.items():
        print(f"  {status}: {len(ids)}")
        for wid in ids:
            print(f"    - {wid}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

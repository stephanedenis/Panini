#!/usr/bin/env python3
"""
§165 — Découpage des œuvres acquises §164 en fragments.jsonl.

Œuvres traitées :
  - spinoza_ethica_1 (Pars I uniquement, traduction Elwes EN via Gutenberg #3800)
  - hobbes_leviathan_4 (Book IV : chapitres XLIV-XLVII via Gutenberg #3207)

Stratégie :
  - Détecter bornes section par patterns spécifiques.
  - Découper en fragments : 1 paragraphe ≈ 1 fragment (>= 30 mots, <= 800).
  - Préserver section_label par fragment.

Output : <work_dir>/fragments.jsonl pour chaque œuvre.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "protoatheism"


def split_paragraphs(text: str, min_words: int = 30, max_words: int = 800) -> list[str]:
    """Découpe par double newline, filtre par longueur, sub-split si trop long."""
    raw = re.split(r"\n{2,}", text)
    out = []
    for p in raw:
        p = re.sub(r"\s+", " ", p).strip()
        wc = len(p.split())
        if wc < min_words:
            continue
        if wc <= max_words:
            out.append(p)
            continue
        # split sur phrases si trop long
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", p)
        cur = ""
        cur_wc = 0
        for s in sentences:
            sw = len(s.split())
            if cur_wc + sw > max_words and cur:
                out.append(cur.strip())
                cur, cur_wc = s, sw
            else:
                cur = (cur + " " + s).strip() if cur else s
                cur_wc += sw
        if cur and cur_wc >= min_words:
            out.append(cur.strip())
    return out


def fragmentize_spinoza_ethica_1(text: str) -> list[dict]:
    """Extrait Part I uniquement de la traduction Elwes."""
    # Borne supérieure : "PART I. CONCERNING GOD."
    m_start = re.search(r"PART\s+I\.\s+CONCERNING\s+GOD\.", text, re.IGNORECASE)
    m_end = re.search(r"PART\s+II\.", text, re.IGNORECASE)
    if not m_start:
        raise RuntimeError("Cannot locate Part I in Spinoza text")
    part1 = text[m_start.end():m_end.start() if m_end else len(text)]

    # Sub-sections : DEFINITIONS / AXIOMS / PROP. I-XXXVI / APPENDIX
    section_markers = [
        ("DEFINITIONS", r"DEFINITIONS\."),
        ("AXIOMS", r"AXIOMS\."),
        ("PROPOSITIONS", r"PROP\.\s+I\."),
        ("APPENDIX", r"APPENDIX\."),
    ]

    fragments = []
    fid = 0
    # Naïf : assigne section selon proximité du dernier marqueur trouvé avant le paragraphe
    paragraphs = split_paragraphs(part1)

    # Trouver positions absolues des marqueurs dans part1
    marker_positions = []
    for label, pat in section_markers:
        m = re.search(pat, part1, re.IGNORECASE)
        if m:
            marker_positions.append((m.start(), label))
    marker_positions.sort()

    cur_pos = 0
    cur_section = "PART_I_HEAD"
    for para in paragraphs:
        idx = part1.find(para, cur_pos)
        if idx >= 0:
            cur_pos = idx
            for mpos, mlabel in marker_positions:
                if mpos <= idx:
                    cur_section = mlabel
        fid += 1
        fragments.append({
            "work_id": "spinoza_ethica_1",
            "fragment_id": f"sp_eth1_{fid:04d}",
            "lang": "en",  # traduction Elwes EN (note : source latine non récupérée)
            "section": cur_section,
            "raw_text": para,
            "source_year": 1677,
            "tradition_label": "EUR_RATIONALIST_CRITIC",
            "translator_note": "Translation R.H.M. Elwes 1883, original Latin 1677",
        })
    return fragments


def fragmentize_hobbes_leviathan_4(text: str) -> list[dict]:
    """Extrait Book IV (chapitres XLIV-XLVII)."""
    # Trouver le second occurrence de "OF THE KINGDOME OF DARKNESSE" (header de section)
    occurrences = [m.start() for m in re.finditer(r"OF\s+THE\s+KINGDOME\s+OF\s+DARKNESSE", text, re.IGNORECASE)]
    if len(occurrences) < 2:
        raise RuntimeError("Cannot locate Book IV header in Hobbes text")
    book4_start = occurrences[1]

    # Le texte se termine probablement avec "REVIEW AND CONCLUSION" ou similaire
    end_match = re.search(r"REVIEW\s+AND\s+CONCLUSION", text[book4_start:], re.IGNORECASE)
    book4 = text[book4_start: book4_start + end_match.start() if end_match else len(text)]

    # Détection des chapitres XLIV-XLVII
    chapter_pat = re.compile(
        r"CHAPTER\s+(XLIV|XLV|XLVI|XLVII)\.\s+(.{0,200})",
        re.IGNORECASE
    )
    chapters = []
    for m in chapter_pat.finditer(book4):
        chapters.append((m.start(), m.group(1).upper()))

    fragments = []
    fid = 0
    paragraphs = split_paragraphs(book4)

    cur_pos = 0
    cur_chap = "BOOK_IV_HEAD"
    for para in paragraphs:
        idx = book4.find(para, cur_pos)
        if idx >= 0:
            cur_pos = idx
            for cpos, clabel in chapters:
                if cpos <= idx:
                    cur_chap = f"CHAPTER_{clabel}"
        fid += 1
        fragments.append({
            "work_id": "hobbes_leviathan_4",
            "fragment_id": f"hb_lev4_{fid:04d}",
            "lang": "en",
            "section": cur_chap,
            "raw_text": para,
            "source_year": 1651,
            "tradition_label": "EUR_THEOL_CRITIC",
        })
    return fragments


def write_jsonl(path: Path, fragments: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for fr in fragments:
            f.write(json.dumps(fr, ensure_ascii=False) + "\n")


def main() -> None:
    plan = [
        ("spinoza_ethica_1", fragmentize_spinoza_ethica_1),
        ("hobbes_leviathan_4", fragmentize_hobbes_leviathan_4),
    ]

    for work_id, fn in plan:
        work_dir = CORPUS_DIR / work_id
        raw_path = work_dir / "raw_text.txt"
        if not raw_path.exists():
            print(f"  ⚠ {work_id} : raw_text.txt absent, skip")
            continue
        text = raw_path.read_text(encoding="utf-8")
        try:
            frags = fn(text)
        except Exception as e:
            print(f"  ✗ {work_id} : ERREUR fragmentation {type(e).__name__}: {e}")
            continue
        out = work_dir / "fragments.jsonl"
        write_jsonl(out, frags)
        # Statistiques
        from collections import Counter
        sec_counts = Counter(f["section"] for f in frags)
        word_counts = [len(f["raw_text"].split()) for f in frags]
        print(f"  ✓ {work_id} : {len(frags)} fragments, "
              f"mots min/median/max = {min(word_counts)}/{sorted(word_counts)[len(word_counts)//2]}/{max(word_counts)}")
        for sec, c in sec_counts.most_common():
            print(f"      {sec:30s}  {c}")


if __name__ == "__main__":
    main()

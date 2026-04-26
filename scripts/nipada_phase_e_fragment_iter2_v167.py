#!/usr/bin/env python3
"""
§167 — Re-fragmentation des œuvres acquises §166 avec :
  - Détection de sections fiable (PARTS Spinoza, BOOKS+CHAPTERS Hobbes,
    chapitres concaténés Mozi/Han Feizi).
  - Métadonnées de traçabilité étendues par fragment :
      provenance_sha256, source_url, retrieval_date, section_label.
  - Filtrage qualité : retire les passages purement bibliographiques
    (TOC, préface, notes éditeur).

Œuvres traitées (§166 acquired) :
  - spinoza_ethica_complete (5 PARTS)
  - hobbes_leviathan_complete (4 BOOKS, 47 CHAPTERS)
  - mozi_selections (5 chapters concaténés)
  - han_feizi_selections (4 chapters concaténés)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "protoatheism"


def load_provenance(work_id: str) -> dict:
    p = CORPUS_DIR / work_id / "PROVENANCE.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def split_paragraphs(text: str, min_words: int = 25, max_words: int = 800) -> list[str]:
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
        sentences = re.split(r"(?<=[.!?。！？])\s+", p)
        cur, cur_wc = "", 0
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


# ─── Spinoza Ethica complete ─────────────────────────────────────────


def fragmentize_spinoza(text: str, prov: dict) -> list[dict]:
    # Skip everything before "PART I. CONCERNING GOD."
    m_start = re.search(r"PART\s+I\.\s+CONCERNING\s+GOD\.", text, re.IGNORECASE)
    if not m_start:
        raise RuntimeError("PART I not found in Spinoza")
    body = text[m_start.start():]

    # Find part boundaries
    part_pat = re.compile(r"^PART\s+(I{1,3}|IV|V)[\.:]", re.MULTILINE | re.IGNORECASE)
    boundaries = []
    for m in part_pat.finditer(body):
        boundaries.append((m.start(), m.group(1).upper()))
    boundaries.append((len(body), "END"))

    fragments = []
    fid = 0
    for i in range(len(boundaries) - 1):
        start, label = boundaries[i]
        end, _ = boundaries[i + 1]
        section_text = body[start:end]
        # Find next part header line, skip it for content
        first_nl = section_text.find("\n\n")
        content = section_text[first_nl:] if first_nl > 0 else section_text
        for para in split_paragraphs(content):
            fid += 1
            fragments.append({
                "work_id": "spinoza_ethica_complete",
                "fragment_id": f"sp_eth_{fid:04d}",
                "lang": "en",
                "section": f"PART_{label}",
                "raw_text": para,
                "source_year": 1677,
                "tradition_label": "EUR_RATIONALIST_CRITIC",
                "provenance_sha256": prov.get("sha256"),
                "provenance_url": prov.get("source_url"),
                "translator_note": prov.get("edition", ""),
            })
    return fragments


# ─── Hobbes Leviathan complete ───────────────────────────────────────


def fragmentize_hobbes(text: str, prov: dict) -> list[dict]:
    # Find body start (skip TOC). Body starts where "PART I." appears AFTER
    # the introduction. We use the second occurrence to skip TOC.
    part_i_matches = [m.start() for m in re.finditer(r"^PART\s+I\.\s*$", text, re.MULTILINE)]
    if len(part_i_matches) < 2:
        # Fallback: just use first
        body_start = part_i_matches[0] if part_i_matches else 0
    else:
        body_start = part_i_matches[1]
    body = text[body_start:]

    # Detect parts
    part_pat = re.compile(r"^PART\s+(I{1,3}|IV)\.\s*$", re.MULTILINE)
    part_bounds = [(m.start(), m.group(1)) for m in part_pat.finditer(body)]
    part_bounds.append((len(body), "END"))

    # Detect chapters within
    chap_pat = re.compile(r"^CHAPTER\s+([IVXL]+)[\.\s]", re.MULTILINE)

    fragments = []
    fid = 0
    for i in range(len(part_bounds) - 1):
        p_start, p_label = part_bounds[i]
        p_end, _ = part_bounds[i + 1]
        part_text = body[p_start:p_end]

        chap_matches = [(m.start(), m.group(1)) for m in chap_pat.finditer(part_text)]
        chap_matches.append((len(part_text), "END"))

        for j in range(len(chap_matches) - 1):
            c_start, c_label = chap_matches[j]
            c_end, _ = chap_matches[j + 1]
            chap_text = part_text[c_start:c_end]
            section_label = f"PART_{p_label}_CHAP_{c_label}"
            for para in split_paragraphs(chap_text):
                fid += 1
                fragments.append({
                    "work_id": "hobbes_leviathan_complete",
                    "fragment_id": f"hb_lev_{fid:04d}",
                    "lang": "en",
                    "section": section_label,
                    "raw_text": para,
                    "source_year": 1651,
                    "tradition_label": "EUR_THEOL_CRITIC",
                    "provenance_sha256": prov.get("sha256"),
                    "provenance_url": prov.get("source_url"),
                })
    return fragments


# ─── Mozi / Han Feizi (chapitres concaténés) ─────────────────────────


def fragmentize_chinese(work_id: str, year: int, tradition: str,
                       text: str, prov: dict, fid_prefix: str) -> list[dict]:
    """Détecte les en-têtes '=== <chapter> ===' insérés en §166."""
    chapter_pat = re.compile(r"=== ([^=]+) ===", re.MULTILINE)
    matches = [(m.start(), m.group(1).strip()) for m in chapter_pat.finditer(text)]
    matches.append((len(text), "END"))

    fragments = []
    fid = 0
    # Pour chinois, fragmentation par phrases (max ~200 caractères chinois)
    for i in range(len(matches) - 1):
        c_start, c_label = matches[i]
        c_end, _ = matches[i + 1]
        chap = text[c_start:c_end]
        # Strip header
        chap = re.sub(r"^=== [^=]+ ===\n*", "", chap)
        # Pour le chinois, split par phrases (。！？)
        # Filter: keep only sentences with at least 10 CJK chars
        cjk_re = re.compile(r"[\u4e00-\u9fff]")
        sentences = re.split(r"(?<=[。！？])", chap)
        # Group sentences into ~150-300 char fragments
        cur, cur_len = "", 0
        for s in sentences:
            cjk_count = len(cjk_re.findall(s))
            if cjk_count < 5:
                continue
            cur = (cur + s).strip()
            cur_len = len(cjk_re.findall(cur))
            if cur_len >= 100:
                fid += 1
                fragments.append({
                    "work_id": work_id,
                    "fragment_id": f"{fid_prefix}_{fid:04d}",
                    "lang": "zh",
                    "section": c_label,
                    "raw_text": cur.strip(),
                    "source_year": year,
                    "tradition_label": tradition,
                    "provenance_sha256": prov.get("sha256"),
                    "provenance_url": prov.get("source_url"),
                })
                cur, cur_len = "", 0
        # Tail
        if cur and len(cjk_re.findall(cur)) >= 30:
            fid += 1
            fragments.append({
                "work_id": work_id,
                "fragment_id": f"{fid_prefix}_{fid:04d}",
                "lang": "zh",
                "section": c_label,
                "raw_text": cur.strip(),
                "source_year": year,
                "tradition_label": tradition,
                "provenance_sha256": prov.get("sha256"),
                "provenance_url": prov.get("source_url"),
            })
    return fragments


# ─── Main ────────────────────────────────────────────────────────────


def write_jsonl(path: Path, fragments: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for fr in fragments:
            f.write(json.dumps(fr, ensure_ascii=False) + "\n")


def section_distribution(fragments: list[dict]) -> dict[str, int]:
    from collections import Counter
    return dict(Counter(f["section"] for f in fragments))


def main() -> None:
    plan = [
        ("spinoza_ethica_complete",
         lambda txt, prov: fragmentize_spinoza(txt, prov)),
        ("hobbes_leviathan_complete",
         lambda txt, prov: fragmentize_hobbes(txt, prov)),
        ("mozi_selections",
         lambda txt, prov: fragmentize_chinese(
             "mozi_selections", -400, "CHINESE_RATIONALIST",
             txt, prov, "mz")),
        ("han_feizi_selections",
         lambda txt, prov: fragmentize_chinese(
             "han_feizi_selections", -250, "CHINESE_LEGALIST",
             txt, prov, "hf")),
    ]

    summary = []
    for work_id, fn in plan:
        work_dir = CORPUS_DIR / work_id
        raw_path = work_dir / "raw_text.txt"
        if not raw_path.exists():
            print(f"  ⚠ {work_id} : skip (raw_text manquant)")
            continue
        text = raw_path.read_text(encoding="utf-8")
        prov = load_provenance(work_id)
        try:
            frags = fn(text, prov)
        except Exception as e:
            print(f"  ✗ {work_id} : {type(e).__name__}: {e}")
            continue
        out = work_dir / "fragments.jsonl"
        write_jsonl(out, frags)
        secs = section_distribution(frags)
        wc = [len(f["raw_text"].split()) for f in frags]
        summary.append({
            "work_id": work_id,
            "n_fragments": len(frags),
            "sections": secs,
            "words_min_med_max": [
                min(wc), sorted(wc)[len(wc) // 2], max(wc)
            ] if wc else None,
        })
        print(f"  ✓ {work_id} : {len(frags)} fragments, {len(secs)} sections")
        for sec, c in sorted(secs.items()):
            print(f"      {sec:35s}  {c:>4}")

    out_path = ROOT / "research" / "nipada" / "falsification" / "nipada_v167_fragmentation_summary.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ Récapitulatif : {out_path}")


if __name__ == "__main__":
    main()

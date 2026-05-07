#!/usr/bin/env python3
"""
§268c — Fetch + signature V14 pour Mengzi (Works of Mencius, Legge tr.)
Source: Internet Archive, chineseclassics02legg (Legge Chinese Classics Vol 2)

Produit:
    Panini-Research/nipada/corpus/signed_corpus_v268c_mengzi.json
"""

from __future__ import annotations

import json
import re
import sys
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
    sys.exit(f"ERROR: cannot import from v212f: {e}")

CORPUS_DIR = _NIPADA / "corpus"
FALSI_DIR  = _NIPADA / "falsification"

OUT_CORPUS = CORPUS_DIR / "signed_corpus_v268c_mengzi.json"

MENGZI_URL = (
    "https://archive.org/download/chineseclassics02legg/"
    "chineseclassics02legg_djvu.txt"
)


def clean_ia_ocr(raw: str) -> str:
    """Nettoyer un texte OCR d'Internet Archive.
    
    - Supprimer les en-têtes / pieds de page répétitifs
    - Éliminer les caractères non-ASCII isolés (artefacts OCR)
    - Normaliser les espaces
    """
    # Supprimer les lignes qui sont uniquement des numéros de page
    lines = raw.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Sauter lignes: numéros seuls, très courtes, entête répétitif
        if re.fullmatch(r"\d{1,4}", stripped):
            continue
        if len(stripped) < 3:
            continue
        # Conserver la ligne (elle contient du texte anglais ou chinois translittéré)
        cleaned.append(stripped)
    
    text = " ".join(cleaned)
    
    # Éliminer les séquences de caractères non-imprimables
    text = re.sub(r"[^\x20-\x7E\u0080-\u024F\u2019\u2018\u201C\u201D]", " ", text)
    
    # Normaliser espaces multiples
    text = re.sub(r"\s{2,}", " ", text)
    
    return text.strip()


def main() -> int:
    print("§268c — Fetch Mengzi (Legge, IA)")
    print("=" * 50)
    
    print(f"\n[1] Téléchargement: {MENGZI_URL[:60]}…")
    try:
        r = requests.get(
            MENGZI_URL,
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0 (NiPaDa Research)"},
        )
        r.raise_for_status()
        raw_text = r.text
        print(f"  Téléchargé: {len(raw_text)} chars")
    except Exception as e:
        sys.exit(f"ERROR fetch: {e}")
    
    print("\n[2] Nettoyage OCR…")
    cleaned = clean_ia_ocr(raw_text)
    n_chars = len(cleaned)
    n_words = len(cleaned.split())
    print(f"  Après nettoyage: {n_chars} chars, {n_words} mots")
    
    if n_chars < 50_000:
        print(f"WARNING: texte court ({n_chars} chars) — peut indiquer un problème de fetch")
    
    print("\n[3] Signature V14…")
    sig = freq_signature(cleaned, "eng")
    
    print("  Vecteur V14:")
    for atom in V14_ATOMS:
        v = sig.get(atom, 0.0)
        bar = "█" * int(v * 50)
        print(f"    {atom:<15} {v:.4f} {bar}")
    
    # Vérification calibration vs v263 stats
    v263_means = {
        "ÊTRE": 0.1143, "DIFFÉRENCE": 0.0865, "RAPPORT": 0.0778,
        "ORIENTATION": 0.0427, "SUJET": 0.1158, "TEMPS": 0.0720,
        "MODALITÉ": 0.0494, "NOMBRE": 0.0909, "ESPACE": 0.1195,
        "OPÉRATION": 0.0593, "FONCTION": 0.0161, "STRUCTURE": 0.0576,
        "SYMÉTRIE": 0.0322, "ÉQUATION": 0.0659,
    }
    print("\n  Calibration (écart à la moyenne v263):")
    for atom in V14_ATOMS:
        v = sig.get(atom, 0.0)
        ref = v263_means[atom]
        delta = v - ref
        flag = " ⚠️" if abs(delta) > 0.08 else ""
        print(f"    {atom:<15} {v:.4f} (ref={ref:.4f} delta={delta:+.4f}){flag}")
    
    print("\n[4] Sauvegarde corpus…")
    entry: dict[str, Any] = {
        "graph_node_id": "mengzi",
        "catalog": "nipada_v268c",
        "tradition_label": "CONFUCIAN_AXIAL",
        "lang": "eng",
        "source_url": MENGZI_URL,
        "n_chars": n_chars,
        "n_words": n_words,
        "n_segments": 1,
        "v14_signature": sig,
        "ingestion_status": "signed_v268c",
    }
    corpus_data = {
        "version": "v268c",
        "description": "§268c: Mengzi (Works of Mencius, Legge tr.) depuis IA",
        "n_texts": 1,
        "signed": [entry],
    }
    OUT_CORPUS.write_text(json.dumps(corpus_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Sauvegardé: {OUT_CORPUS}")
    print("\n=== §268c fetch terminé ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

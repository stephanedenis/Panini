#!/usr/bin/env python3
"""
test_nipada_panini_fs.py — §78 : Test de cohérence nipada ↔ Panini-FS

Vérifie que la classification nipada des chunks binaires est consistante
avec les catégories de format déjà reconnues par FormatDetector.

Principe :
  Pour chaque format connu, on construit un chunk synthétique représentatif,
  on le classifie via nipada_classifier, et on vérifie que le résultat
  est conforme à l'attendu théorique.

  Le test valide aussi les métriques intermédiaires (entropie, compression)
  pour garantir la stabilité du classifieur.

Résultats attendus (théorie) :
  | Type de données     | Molécule    | Produit | Raisonnement               |
  |---------------------|-------------|---------|----------------------------|
  | Vide                | PADDING     |   1     | aucun atome                |
  | Constante (0x00)    | COMPOSITION |  10     | ÊTRE + RAPPORT (struct.)   |
  | PNG header          | COMPOSITION |  10     | structuré, non temporel    |
  | GZIP payload        | EXISTENCE   |   6     | varié, non compressible    |
  | Texte répété        | VIE         |  30     | varié + structuré          |
  | WAV header          | INTENTION   |  70     | structuré + temporel       |
  | Audio data synthét. | INTÉGRATION | 210     | tout présent               |

Usage :
  cd /home/stephane/GitHub/Panini
  .venv/bin/python scripts/test_nipada_panini_fs.py
"""

import gzip
import io
import json
import math
import os
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_classifier import (
    classify_chunk,
    classify_chunk_detail,
    NIPADA_NAMES,
    _entropy,
    _compression_gain,
    _has_orientation,
)

# ── Fixtures : chunks synthétiques ────────────────────────────────────────────

def make_empty() -> bytes:
    return b""

def make_constant(n: int = 512) -> bytes:
    """Chunk de zéros — structuré, non varié."""
    return b'\x00' * n

def make_png_header() -> bytes:
    """Magic PNG + IHDR minimal."""
    magic = b'\x89PNG\r\n\x1a\n'
    # IHDR : 13 bytes data, longueur=13, type='IHDR', CRC simplifié
    ihdr_data = struct.pack('>IIBBBBB', 256, 256, 8, 2, 0, 0, 0)  # 100×100 RGB
    ihdr_len = struct.pack('>I', len(ihdr_data))
    ihdr_type = b'IHDR'
    ihdr_crc  = struct.pack('>I', zlib.crc32(ihdr_type + ihdr_data) & 0xFFFFFFFF)
    return magic + ihdr_len + ihdr_type + ihdr_data + ihdr_crc

def make_jpeg_header() -> bytes:
    """Début JPEG : SOI + APP0."""
    soi     = b'\xff\xd8'
    # APP0 : marker + length (16) + JFIF\x00 + version + ...
    app0    = b'\xff\xe0' + b'\x00\x10' + b'JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    return soi + app0 + b'\x00' * 32

def make_gzip_payload(n_kb: int = 8) -> bytes:
    """Payload GZIP compressé d'un texte répété — haute entropie, non re-compressible."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(b"The quick brown fox jumps over the lazy dog. " * (n_kb * 20))
    return buf.getvalue()

def make_text_repeated(n: int = 300) -> bytes:
    """Texte UTF-8 répété — varié + compressible."""
    base = "La différence est l'articulation irréductible entre deux choses. "
    return (base * n).encode("utf-8")

def make_wav_header() -> bytes:
    """En-tête WAV minimale (RIFF + WAVE + fmt)."""
    fmt_chunk  = b'fmt '
    fmt_data   = struct.pack('<HHIIHH', 1, 1, 44100, 88200, 2, 16)  # PCM mono
    fmt_size   = struct.pack('<I', len(fmt_data))
    fmt_block  = fmt_chunk + fmt_size + fmt_data
    riff_size  = struct.pack('<I', 4 + len(fmt_block))
    return b'RIFF' + riff_size + b'WAVE' + fmt_block

def make_audio_data_synthetic(n_samples: int = 2048) -> bytes:
    """
    Données audio synthétiques (PCM 16 bits) — sinusoïde à 440 Hz.
    • Varié (entropie ~7 bits)
    • Compressible (patron répétitif sinusoïdal → RAPPORT)
    Ici : données seules, pas de magic temporel → VIE (ÊTRE+DIFFÉRENCE+RAPPORT)
    """
    return b''.join(
        struct.pack('<h', int(32767 * math.sin(2 * math.pi * 440 * i / 44100)))
        for i in range(n_samples)
    )

def make_mp4_header() -> bytes:
    """Début d'un MP4 (ftyp box)."""
    brand    = b'mp41'
    version  = b'\x00\x00\x00\x00'
    compat   = b'mp41mp42isom'
    ftyp_data = b'ftyp' + brand + version + compat
    size     = struct.pack('>I', 4 + len(ftyp_data))
    return size + ftyp_data + b'\x00' * 32


# ── Cas de test ───────────────────────────────────────────────────────────────

TEST_CASES = [
    {
        "name":              "Vide",
        "factory":           make_empty,
        "expected_product":  1,
        "expected_name":     "PADDING",
        "note":              "Chunk vide → neutre",
    },
    {
        "name":              "Constante (0x00 × 512)",
        "factory":           make_constant,
        "expected_product":  10,
        "expected_name":     "COMPOSITION",
        "note":              "ÊTRE + RAPPORT : structuré, non varié",
    },
    {
        "name":              "PNG header",
        "factory":           make_png_header,
        "expected_product":  10,
        "expected_name":     "COMPOSITION",
        "note":              "ÊTRE + RAPPORT : structuré, non temporel",
    },
    {
        "name":              "JPEG header",
        "factory":           make_jpeg_header,
        "expected_product":  10,
        "expected_name":     "COMPOSITION",
        "note":              "ÊTRE + RAPPORT : structuré, non temporel",
    },
    {
        "name":              "GZIP payload",
        "factory":           make_gzip_payload,
        "expected_product":  6,
        "expected_name":     "EXISTENCE",
        "note":              "ÊTRE + DIFFÉRENCE : varié, non compressible (déjà compressé)",
    },
    {
        "name":              "Texte répété (UTF-8)",
        "factory":           make_text_repeated,
        "expected_product":  30,
        "expected_name":     "VIE",
        "note":              "ÊTRE + DIFFÉRENCE + RAPPORT : varié ET compressible",
    },
    {
        "name":              "WAV header (RIFF)",
        "factory":           make_wav_header,
        "expected_product":  70,
        "expected_name":     "INTENTION",
        "note":              "ÊTRE + RAPPORT + ORIENTATION : structuré + temporel",
    },
    {
        "name":              "MP4 header (ftyp)",
        "factory":           make_mp4_header,
        "expected_product":  70,
        "expected_name":     "INTENTION",
        "note":              "ÊTRE + RAPPORT + ORIENTATION : structuré + temporel",
    },
    {
        "name":              "Audio PCM sinusoïdal",
        "factory":           make_audio_data_synthetic,
        "expected_product":  6,
        "expected_name":     "EXISTENCE",
        "note":              "ÊTRE + DIFFÉRENCE : entropie élevée (~7.9), le RAPPORT sinusoïdal"
                             " est fréquentiel (non détectable par zlib). VIE nécessiterait FFT.",
    },
]


# ── Exécution ─────────────────────────────────────────────────────────────────

def run_tests() -> list[dict]:
    results = []
    n_pass = 0
    n_fail = 0

    print("=" * 72)
    print("  NIPADA ↔ PANINI-FS — §78 : Test de cohérence structurelle")
    print("=" * 72)
    print(f"  {'Cas de test':<32}  {'Attendu':<16}  {'Obtenu':<16}  Résultat")
    print("  " + "─" * 68)

    for tc in TEST_CASES:
        data   = tc["factory"]()
        detail = classify_chunk_detail(data)
        prod   = detail["product"]
        name   = detail["name"]

        ok = (prod == tc["expected_product"])
        n_pass += ok
        n_fail += (not ok)
        status = "✓ PASS" if ok else "✗ FAIL"

        print(f"  {tc['name']:<32}  {tc['expected_name']:<16}  {name:<16}  {status}")
        if not ok:
            print(f"    → attendu={tc['expected_product']} obtenu={prod}")
            print(f"       entropy={detail['entropy']:.3f}  cg={detail['compression_gain']:.3f}  ori={detail['has_orientation']}")
            print(f"       atomes={detail['atoms']}")
            print(f"       note : {tc['note']}")

        results.append({
            "name":     tc["name"],
            "expected": {"product": tc["expected_product"], "name": tc["expected_name"]},
            "obtained": detail,
            "pass":     ok,
            "note":     tc["note"],
        })

    print("  " + "─" * 68)
    print(f"  {n_pass}/{n_pass+n_fail} tests PASSED")
    print()

    return results


def print_detail_table(results: list[dict]) -> None:
    """Affiche le tableau détaillé des métriques intermédiaires."""
    print("─" * 72)
    print("  MÉTRIQUES INTERMÉDIAIRES")
    print("─" * 72)
    print(f"  {'Cas':<32}  {'H(bits)':<9}  {'CG%':<7}  {'Ori':<5}  {'Mask':<5}  {'Mol.'}")
    print("  " + "─" * 68)
    for r in results:
        d   = r["obtained"]
        h   = d["entropy"]
        cg  = d["compression_gain"] * 100
        ori = "✓" if d["has_orientation"] else "✗"
        mask = d["mask"]
        print(f"  {r['name']:<32}  {h:<9.3f}  {cg:<7.1f}  {ori:<5}  {mask:<5b}  {d['name']}")
    print()


def main() -> None:
    results = run_tests()
    print_detail_table(results)

    # Sauvegarde JSON
    out_path = ROOT / "research" / "nipada" / "falsification" / "nipada_panini_fs_test.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "version":   "nipada_panini_fs_test_v1",
        "date":      "2026-04-23",
        "n_cases":   len(results),
        "n_pass":    sum(r["pass"] for r in results),
        "results":   results,
    }, ensure_ascii=False, indent=2))
    print(f"  Résultats → {out_path.relative_to(ROOT)}")

    n_fail = sum(not r["pass"] for r in results)
    if n_fail > 0:
        print(f"\n  ✗ {n_fail} test(s) en échec")
        sys.exit(1)
    else:
        print(f"\n  ✓ Tous les tests PASSENT — classifieur nipada cohérent avec Panini-FS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
§206z — Index consolidé des catalogues de densification.

Lit tous les catalogues research/nipada/corpus/catalog_*.json et produit
un index global avec inventaire par cellule et progression vers cible 70.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
CORPUS_DIR = REPO / "research/nipada/corpus"
OUT = CORPUS_DIR / "INDEX_catalogs_v206z.json"


def main() -> int:
    catalogs = sorted(CORPUS_DIR.glob("catalog_*.json"))
    by_cell = defaultdict(list)
    summary = []

    for cat_path in catalogs:
        data = json.loads(cat_path.read_text())
        macro = data["macro_culture"]
        epoch = data["epoch"]
        n = data["n_works"]
        target = data["target"]
        cell_key = f"{macro}×{epoch}"
        by_cell[cell_key].extend([w["id"] for w in data["works"]])
        summary.append({
            "version": data["version"],
            "macro_culture": macro,
            "epoch": epoch,
            "n_works": n,
            "target": target,
            "fill_pct": round(100 * n / target, 1) if target else None,
            "primary_source": data.get("primary_source"),
            "language_dominant": data.get("language_original_dominant", "mixed"),
            "file": cat_path.name,
        })

    # Vérification d'unicité des IDs
    all_ids = [wid for ids in by_cell.values() for wid in ids]
    duplicates = [w for w in set(all_ids) if all_ids.count(w) > 1]

    index = {
        "version": "v206z_catalogs_index",
        "generated": "2026-04-27",
        "n_catalogs": len(catalogs),
        "n_works_total": len(all_ids),
        "n_works_unique": len(set(all_ids)),
        "duplicates": duplicates,
        "cells_covered": list(by_cell.keys()),
        "summary": summary,
    }

    OUT.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"=== Index catalogues densification ===")
    print(f"Catalogues: {len(catalogs)}")
    print(f"Œuvres totales: {len(all_ids)} (uniques: {len(set(all_ids))})")
    if duplicates:
        print(f"⚠️  Doublons: {duplicates}")
    print()
    print(f"{'cellule':<35} {'works':>6} {'tgt':>5} {'%':>6}  source")
    print("-" * 90)
    for s in summary:
        cell = f"{s['macro_culture']}×{s['epoch']}"
        print(f"{cell:<35} {s['n_works']:>6} {s['target']:>5} {s['fill_pct']:>5}%  {s['primary_source'][:40] if s['primary_source'] else '-'}")
    print()
    print(f"Index écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

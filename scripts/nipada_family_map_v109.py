#!/usr/bin/env python3
"""
§109 — Carte modale par famille linguistique
==================================================

Croise la couverture §108 par langue avec la classification typologique
de l'encyclopédie langues v109. Mesure :
  - cohérence intra-famille (variance du profil modal par famille)
  - distance inter-famille
  - corrélation typologie ↔ profil empirique

Sortie : research/nipada/modal/family_map_v109.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _import(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


_v100 = _import("v100", REPO_ROOT / "scripts" / "nipada_corpus_extension_v100.py")
_v108 = _import("v108", REPO_ROOT / "scripts" / "nipada_modal_markers_v108.py")

LANG_DB = json.loads((REPO_ROOT / "research" / "nipada" / "encyclopedie" / "langues_v109.json").read_text())


def main() -> None:
    print("═" * 78)
    print("  §109 — Carte modale par famille linguistique")
    print("═" * 78)

    corpus = _v100.merge_corpus_v100()
    # Profil modal par langue : moyenne du vecteur 7-dim sur les 89 phrases
    profile_by_lang: dict[str, np.ndarray] = {}
    for la in _v100.ALL_LANGS:
        vecs = []
        for t, by_lang in corpus.items():
            for p in by_lang[la]:
                vecs.append(_v108.detect_modalities_vec(p, la))
        profile_by_lang[la] = np.array(vecs, dtype=np.float32).mean(axis=0)

    print("\n  Profil modal moyen par langue (proportion de marqueurs/phrase) :")
    print(f"  {'lang':<5s}", " ".join(f"{m[:7]:>7s}" for m in _v108.MODALITES))
    for la in sorted(profile_by_lang):
        v = profile_by_lang[la]
        print(f"  {la:<5s}", " ".join(f"{x:7.3f}" for x in v))

    # Agrégation par (famille, branche)
    fam_branch_langs: dict[str, list[str]] = {}
    for la, info in LANG_DB["languages"].items():
        key = f"{info['famille']}_{info['branche']}"
        fam_branch_langs.setdefault(key, []).append(la)

    print("\n  Profil modal moyen par (famille, branche) :")
    fam_profile: dict[str, list[float]] = {}
    for key, langs in fam_branch_langs.items():
        v = np.mean([profile_by_lang[la] for la in langs], axis=0)
        fam_profile[key] = v.tolist()
        print(f"  {key:<35s} ({','.join(langs):<15s}) "
              + " ".join(f"{x:5.2f}" for x in v))

    # Variance intra-famille (sur familles à >1 langue)
    print("\n  Variance intra-famille (sd entre langues d'une même branche) :")
    intra_var: dict[str, float] = {}
    for key, langs in fam_branch_langs.items():
        if len(langs) > 1:
            vals = np.array([profile_by_lang[la] for la in langs])
            intra_var[key] = float(np.mean(np.std(vals, axis=0)))
            print(f"  {key:<35s} sd_moy = {intra_var[key]:.3f}")

    # Distance inter-famille (Euclidienne entre profils moyens)
    print("\n  Distance inter-famille (Euclidienne) :")
    keys = sorted(fam_profile.keys())
    inter_dist: dict[str, dict[str, float]] = {}
    for i, k1 in enumerate(keys):
        inter_dist[k1] = {}
        for k2 in keys[i+1:]:
            d = float(np.linalg.norm(np.array(fam_profile[k1]) - np.array(fam_profile[k2])))
            inter_dist[k1][k2] = d
    # Top 5 paires les plus distantes
    pairs = [(k1, k2, d) for k1 in inter_dist for k2, d in inter_dist[k1].items()]
    pairs.sort(key=lambda x: -x[2])
    print("  Top 5 distances :")
    for k1, k2, d in pairs[:5]:
        print(f"    {k1:<35s}  vs  {k2:<35s}  d={d:.3f}")
    print("  Bottom 3 distances :")
    for k1, k2, d in pairs[-3:]:
        print(f"    {k1:<35s}  vs  {k2:<35s}  d={d:.3f}")

    out = REPO_ROOT / "research" / "nipada" / "modal" / "family_map_v109.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "version": "§109",
        "modalites": _v108.MODALITES,
        "profile_by_lang": {la: profile_by_lang[la].tolist() for la in profile_by_lang},
        "profile_by_family_branch": fam_profile,
        "intra_branch_variance": intra_var,
        "inter_branch_distances_top5":  [{"a": a, "b": b, "d": d} for a, b, d in pairs[:5]],
        "inter_branch_distances_bot3":  [{"a": a, "b": b, "d": d} for a, b, d in pairs[-3:]],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

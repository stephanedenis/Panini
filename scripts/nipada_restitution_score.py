#!/usr/bin/env python3
"""
nipada_restitution_score.py — Chantier #2

Computes δ_restitution(t, V14) for each text in signed_corpus_v260_fusion.json.

Definition
----------
  δ_restitution(t) = mean cosine distance(frag_sig_i, whole_sig)
                     over all 500-word fragments of text t

Interpretation
--------------
  Low δ  → text is semantically uniform (each fragment resembles the whole)
  High δ → text is semantically heterogeneous (chapters diverge in semantic content)

Requires
--------
  - signed_corpus_v260_fusion.json  (v14_signature + fragments fields)
  - nipada/corpus/_cache/            (raw text for fragment splitting)
  - nipada_fetch_corpus_v212f.py     (freq_signature, ATOM_LEXICON_ENG)

Output
------
  nipada/corpus/delta_restitution_v260.json
  + console summary

Usage
-----
  python3 nipada_restitution_score.py [--output PATH]
"""

import argparse
import importlib.util
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR    = Path(__file__).resolve().parent
PANINI_SCRIPTS = SCRIPT_DIR  # same directory
REPO_RESEARCH  = SCRIPT_DIR.parent.parent / "Panini-Research"
CORPUS_JSON    = REPO_RESEARCH / "nipada/corpus/signed_corpus_v260_fusion.json"
CACHE_ROOT     = REPO_RESEARCH / "nipada/corpus/_cache"
CACHE_ST       = CACHE_ROOT / "sacred_texts"
CACHE_SC       = CACHE_ROOT / "suttacentral"
DEFAULT_OUTPUT = REPO_RESEARCH / "nipada/corpus/delta_restitution_v260.json"

FRAGMENT_WORDS = 500

# ---------------------------------------------------------------------------
# Import freq_signature from nipada_fetch_corpus_v212f.py
# ---------------------------------------------------------------------------

def _load_signing_module():
    """Dynamically import nipada_fetch_corpus_v212f to get freq_signature."""
    mod_path = SCRIPT_DIR / "nipada_fetch_corpus_v212f.py"
    if not mod_path.exists():
        raise FileNotFoundError(f"Signing module not found: {mod_path}")
    spec = importlib.util.spec_from_file_location("nipada_fetch_v212f", mod_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Cache resolution (mirrors nipada_patch_v260_fragments.py)
# ---------------------------------------------------------------------------

MANUAL_CACHE = {
    "plato_protagoras":         ["pg_1591.txt"],
    "aristotle_prior_analytics": [
        "mit_aristotle_prior_analytics_s001.txt",
        "mit_aristotle_prior_analytics_s002.txt",
    ],
    "aitareya_upanishad":      ["sacred_texts/v237_aitareya_upanishad.txt"],
    "brihadaranyaka_upanishad":["sacred_texts/v237_brihadaranyaka_upanishad.txt"],
    "chandogya_upanishad":     ["sacred_texts/v237_chandogya_upanishad.txt"],
    "isa_upanishad":           ["sacred_texts/v237_isa_upanishad.txt"],
    "katha_upanishad":         ["sacred_texts/v237_katha_upanishad.txt"],
    "kausitaki_upanishad":     ["sacred_texts/v237_kausitaki_upanishad.txt"],
    "kena_upanishad":          ["sacred_texts/v237_kena_upanishad.txt"],
    "maitri_upanishad":        ["sacred_texts/v237_maitri_upanishad.txt"],
    "mandukya_upanishad":      ["sacred_texts/v237_mandukya_upanishad.txt"],
    "mundaka_upanishad":       ["sacred_texts/v237_mundaka_upanishad.txt"],
    "prashna_upanishad":       ["sacred_texts/v237_prashna_upanishad.txt"],
    "svetasvatara_upanishad":  ["sacred_texts/v237_svetasvatara_upanishad.txt"],
    "taittiriya_upanishad":    ["sacred_texts/v237_taittiriya_upanishad.txt"],
    "daxue":     ["sacred_texts/v236_daxue.txt"],
    "liji":      ["sacred_texts/v236_liji.txt"],
    "yueji":     ["sacred_texts/v236_yueji.txt"],
    "zhongyong": ["sacred_texts/v236_zhongyong.txt"],
    "laozi_taoteching_en": ["sacred_texts/daodejing.txt"],
}


def _strip_html(raw: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", raw, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    for ent, ch in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&quot;", '"'), ("&apos;", "'"), ("&nbsp;", " ")]:
        text = text.replace(ent, ch)
    return re.sub(r"\s+", " ", text).strip()


def _resolve_cache_files(local_id: str) -> list[Path] | None:
    if local_id in MANUAL_CACHE:
        paths = [CACHE_ROOT / rel for rel in MANUAL_CACHE[local_id]]
        existing = [p for p in paths if p.exists()]
        return existing if existing else None
    p_st = CACHE_ST / f"{local_id}.txt"
    if p_st.exists():
        return [p_st]
    p_sc = CACHE_SC / f"{local_id}.txt"
    if p_sc.exists():
        return [p_sc]
    return None


def _load_text(paths: list[Path]) -> str:
    parts = []
    for p in paths:
        raw = p.read_text(encoding="utf-8", errors="replace")
        if raw.lstrip().startswith("<") or "<HTML" in raw[:200].upper():
            raw = _strip_html(raw)
        parts.append(raw)
    return "\n\n".join(parts)


def _split_into_fragments(text: str) -> list[str]:
    """Return list of ~FRAGMENT_WORDS word chunks."""
    words = text.split()
    return [" ".join(words[i:i + FRAGMENT_WORDS])
            for i in range(0, len(words), FRAGMENT_WORDS)
            if words[i:i + FRAGMENT_WORDS]]


# ---------------------------------------------------------------------------
# Cosine distance
# ---------------------------------------------------------------------------

def _cosine_distance(a: dict, b: dict) -> float:
    """Cosine distance in [0, 1] between two V14 signature dicts."""
    keys = list(a.keys())
    va = [a[k] for k in keys]
    vb = [b[k] for k in keys]
    dot  = sum(x * y for x, y in zip(va, vb))
    na   = math.sqrt(sum(x * x for x in va))
    nb   = math.sqrt(sum(x * x for x in vb))
    if na < 1e-12 or nb < 1e-12:
        return 1.0
    return 1.0 - dot / (na * nb)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute δ_restitution for each v260 corpus entry")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output JSON path")
    args = parser.parse_args()

    # Load signing module
    signing = _load_signing_module()
    freq_signature = signing.freq_signature

    # Load corpus
    corpus = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
    entries = corpus["signed"]

    scores = []
    n_computed = 0
    n_skip_no_sig = 0
    n_skip_no_cache = 0
    n_skip_single_frag = 0

    for entry in entries:
        local_id    = entry.get("local_id") or entry.get("graph_node_id", "")
        whole_sig   = entry.get("v14_signature")
        frags_meta  = entry.get("fragments")  # [{seq, n_words, hash}] or null

        if not whole_sig:
            n_skip_no_sig += 1
            scores.append({
                "local_id": local_id,
                "delta_restitution": None,
                "note": "no whole-text signature",
            })
            continue

        if not frags_meta:
            n_skip_no_cache += 1
            scores.append({
                "local_id": local_id,
                "delta_restitution": None,
                "n_fragments": 0,
                "note": "no cached text",
            })
            continue

        # Load and re-split text
        cache_files = _resolve_cache_files(local_id)
        if not cache_files:
            n_skip_no_cache += 1
            scores.append({
                "local_id": local_id,
                "delta_restitution": None,
                "n_fragments": len(frags_meta),
                "note": "cache files not found at runtime",
            })
            continue

        text = _load_text(cache_files)
        frag_texts = _split_into_fragments(text)
        n_frags = len(frag_texts)

        if n_frags < 2:
            n_skip_single_frag += 1
            scores.append({
                "local_id": local_id,
                "delta_restitution": None,
                "n_fragments": n_frags,
                "note": "single fragment — δ undefined",
            })
            continue

        # Compute per-fragment signatures
        frag_sigs = [freq_signature(ft, lang="eng") for ft in frag_texts]

        # Cosine distances: frag_sig_i vs whole_sig
        distances = [_cosine_distance(fs, whole_sig) for fs in frag_sigs]
        mean_d = sum(distances) / len(distances)
        std_d  = math.sqrt(
            sum((d - mean_d) ** 2 for d in distances) / len(distances))

        # δ_restitution
        delta = round(mean_d, 6)

        scores.append({
            "local_id":             local_id,
            "tradition_label":      entry.get("tradition_label", ""),
            "n_fragments":          n_frags,
            "delta_restitution":    delta,
            "cosine_dist_mean":     round(mean_d, 6),
            "cosine_dist_std":      round(std_d, 6),
            "cosine_dist_min":      round(min(distances), 6),
            "cosine_dist_max":      round(max(distances), 6),
            "v14_top3":             entry.get("v14_top3", []),
        })
        n_computed += 1

    # Sort by δ descending (most heterogeneous first)
    computed = [s for s in scores if s.get("delta_restitution") is not None]
    null_scores = [s for s in scores if s.get("delta_restitution") is None]
    computed.sort(key=lambda s: s["delta_restitution"], reverse=True)

    all_scores = computed + null_scores

    # Summary stats
    all_delta = [s["delta_restitution"] for s in computed]
    summary = {
        "n_total":           len(entries),
        "n_computed":        n_computed,
        "n_null_no_sig":     n_skip_no_sig,
        "n_null_no_cache":   n_skip_no_cache,
        "n_null_single_frag": n_skip_single_frag,
        "delta_mean":        round(sum(all_delta) / len(all_delta), 6) if all_delta else None,
        "delta_std":         round(
            math.sqrt(sum((d - sum(all_delta) / len(all_delta)) ** 2
                          for d in all_delta) / len(all_delta)), 6)
            if len(all_delta) > 1 else None,
        "delta_min":         round(min(all_delta), 6) if all_delta else None,
        "delta_max":         round(max(all_delta), 6) if all_delta else None,
        "top5_heterogeneous": [s["local_id"] for s in computed[:5]],
        "top5_uniform":       [s["local_id"] for s in reversed(computed[-5:])],
    }

    output = {
        "corpus":          "signed_corpus_v260_fusion.json",
        "lexicon_version": "v14",
        "fragment_words":  FRAGMENT_WORDS,
        "computed_at":     datetime.now(timezone.utc).isoformat(),
        "summary":         summary,
        "scores":          all_scores,
    }

    out_path = Path(args.output)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    # Console report
    print(f"δ_restitution computed for {n_computed}/{len(entries)} entries")
    print(f"  mean δ = {summary['delta_mean']}  |  "
          f"std = {summary['delta_std']}  |  "
          f"range [{summary['delta_min']}, {summary['delta_max']}]")
    print(f"Most heterogeneous: {summary['top5_heterogeneous']}")
    print(f"Most uniform:       {summary['top5_uniform']}")
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main()

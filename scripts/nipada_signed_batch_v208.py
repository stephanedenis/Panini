#!/usr/bin/env python3
"""§208 — PoC première fournée signée V14.

Étapes :
  1. Charger graph v10 (1764 nodes).
  2. Pour chaque source locale `corpus/protoatheism/*/`, agréger fragments
     ou raw_text, calculer la signature V14 baseline.
  3. Tenter le mapping vers un node existant (id catalog↔id local fuzzy).
  4. Pour chaque match, attacher v14_signature au node + maj ingestion_status.
  5. Sortir :
       - `research/nipada/corpus/signed_corpus_v208.json` (signatures + métadonnées)
       - `research/nipada/falsification/nipada_v208_graph_v11.json` (graph maj)

Cette fournée est volontairement minimale (corpus déjà locaux, pas de fetch
réseau) — base testable pour §209 V_OPT v2 revalidation.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from nipada_ingest_pipeline_v207 import normalize_text  # noqa: E402

# V14 calibré multilingue §145 (réutilisé par §177 / V_OPT v2)
_spec = importlib.util.spec_from_file_location(
    "nipada_v14_multiling_v145", REPO / "scripts" / "nipada_v14_multiling_v145.py")
_v145 = importlib.util.module_from_spec(_spec)
sys.modules["nipada_v14_multiling_v145"] = _v145
_spec.loader.exec_module(_v145)
V14 = _v145.V14


def v14_signature(text: str, lang: str) -> dict[str, float]:
    """Signature V14 calibrée §145 (lexique multilingue).

    Retourne fréquences normalisées (somme = 1.0) pour les 14 atomes.
    """
    counts = _v145.freq_signature(text, lang) if hasattr(_v145, "freq_signature") else {a: 0 for a in V14}
    if isinstance(counts, dict):
        tot = sum(counts.values())
        if tot > 0:
            return {a: counts.get(a, 0) / tot for a in V14}
    return {a: 1.0 / 14 for a in V14}

GRAPH_V10 = REPO / "research/nipada/falsification/nipada_v207_graph_v10.json"
GRAPH_V11 = REPO / "research/nipada/falsification/nipada_v208_graph_v11.json"
SIGNED_OUT = REPO / "research/nipada/corpus/signed_corpus_v208.json"
LOCAL_CORPUS = REPO / "corpus/protoatheism"


if not hasattr(_v145, "freq_signature"):
    # fallback : recopier la fonction depuis v177 (qui en a une version locale)
    _spec_v177 = importlib.util.spec_from_file_location(
        "_v177_local", REPO / "scripts" / "nipada_calibration_v177.py")
    _v177 = importlib.util.module_from_spec(_spec_v177)
    sys.modules["_v177_local"] = _v177
    _spec_v177.loader.exec_module(_v177)

    def v14_signature(text: str, lang: str) -> dict[str, float]:  # noqa: F811
        counts = _v177.freq_signature(text, lang)
        tot = sum(counts.values())
        if tot > 0:
            return {a: counts.get(a, 0) / tot for a in V14}
        return {a: 1.0 / 14 for a in V14}


def load_local_fragments(corpus_dir: Path) -> tuple[str, list[tuple[str, str]]]:
    """Retourne (lang_principal, [(text, lang_par_fragment), ...]) pour une source locale."""
    frag_path = corpus_dir / "fragments.jsonl"
    if frag_path.exists():
        frags: list[tuple[str, str]] = []
        langs: dict[str, int] = {}
        with frag_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = rec.get("text") or ""
                if not t:
                    continue
                lg = rec.get("lang") or "und"
                frags.append((t, lg))
                langs[lg] = langs.get(lg, 0) + 1
        main_lang = max(langs, key=langs.get) if langs else "und"
        return main_lang, frags
    # fallback raw_text
    for raw_name, lang in (("raw_text.txt", "eng"), ("source_lat.html", "lat"),
                           ("source_fra.txt", "fra"), ("source_deu.txt", "deu"),
                           ("source_lzh.txt", "lzh")):
        rp = corpus_dir / raw_name
        if rp.exists():
            return lang, [(rp.read_text(encoding="utf-8", errors="ignore"), lang)]
    return "und", []


def aggregate_v14(fragments: list[tuple[str, str]]) -> tuple[dict[str, float], int]:
    """Calcule signature V14 normalisée à partir d'une liste de (texte, lang)."""
    total = {a: 0 for a in V14}
    n_chars = 0
    for text, lang in fragments:
        n_chars += len(text)
        counts = _v145.freq_signature(text, lang) if hasattr(_v145, "freq_signature") \
            else _v177.freq_signature(text, lang)  # type: ignore[name-defined]
        for a in V14:
            total[a] += counts.get(a, 0)
    tot = sum(total.values())
    if tot > 0:
        return {a: total[a] / tot for a in V14}, n_chars
    return {a: 1.0 / 14 for a in V14}, n_chars


def find_match(local_id: str, node_ids: list[str]) -> str | None:
    """Match heuristique catalog node ↔ local corpus id."""
    if local_id in node_ids:
        return local_id
    # tokenize, intersection minimale
    local_tokens = set(re.split(r"[_\W]+", local_id.lower())) - {""}
    best: tuple[int, str | None] = (0, None)
    for nid in node_ids:
        n_tokens = set(re.split(r"[_\W]+", nid.lower())) - {""}
        common = local_tokens & n_tokens
        if len(common) >= 2 and len(common) > best[0]:
            best = (len(common), nid)
    return best[1]


def main() -> int:
    graph = json.loads(GRAPH_V10.read_text(encoding="utf-8"))
    node_ids = list(graph["nodes"].keys())

    signed: list[dict] = []
    n_match = 0
    n_nomatch = 0
    n_empty = 0

    for sub in sorted(LOCAL_CORPUS.iterdir()):
        if not sub.is_dir():
            continue
        local_id = sub.name
        lang, fragments = load_local_fragments(sub)
        if not fragments:
            n_empty += 1
            continue
        sig, n_chars = aggregate_v14(fragments)
        match_id = find_match(local_id, node_ids)
        signed_entry = {
            "local_id": local_id,
            "graph_node_id": match_id,
            "lang": lang,
            "n_fragments": len(fragments),
            "n_chars": n_chars,
            "v14_signature": sig,
            "v14_top3": sorted(sig.items(), key=lambda kv: -kv[1])[:3],
            "matched": match_id is not None,
        }
        signed.append(signed_entry)
        if match_id:
            n_match += 1
            node = graph["nodes"][match_id]
            node["v14_signature"] = sig
            node["ingestion_status"] = "signed_v208"
            node["signed_n_chars"] = n_chars
        else:
            n_nomatch += 1

    # graph v11 update meta
    graph["version"] = "v11_post_v208_signed_batch"
    graph.setdefault("meta", {})
    graph["meta"]["v208_signed_batch"] = {
        "sources_local": len(signed),
        "matched_to_graph": n_match,
        "no_match": n_nomatch,
        "empty_skipped": n_empty,
        "v14_atoms": V14,
    }

    SIGNED_OUT.write_text(
        json.dumps({
            "version": "v208",
            "n_signed": len(signed),
            "n_matched": n_match,
            "n_nomatch": n_nomatch,
            "v14_atoms": V14,
            "signed": signed,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    GRAPH_V11.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"§208 — Fournée signée V14 (PoC) terminée")
    print(f"  Sources locales traitées : {len(signed)}")
    print(f"  Empty skipped            : {n_empty}")
    print(f"  Matché → node graph      : {n_match}")
    print(f"  Sans match               : {n_nomatch}")
    print(f"  Sortie corpus signé      : {SIGNED_OUT.relative_to(REPO)}")
    print(f"  Sortie graph v11         : {GRAPH_V11.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
§149 — Décomposition héritée / propre des signatures V14.

Modèle (forme simplifiée du composite §insight) :

    SIG(W) ≈ α · SOURCES(W) + REFLEXION(W) + bruit

où :
- SIG(W) = signature V14 fréquentielle de l'œuvre W (compteurs lexicaux
  sur la concaténation des 5 fragments de W, normalisée L1).
- SOURCES(W) = somme pondérée (par poids §148) des SIG des œuvres parentes
  PRÉSENTES DANS LE CORPUS proto-athéiste (les pivots n'ont pas de
  signature disponible). Les sources sont prises avant W dans le temps.
- α est estimé par moindres carrés non-négatifs (NNLS approximation
  scalaire : α ∈ [0, 1] minimisant ||SIG - α·SOURCES||²).
- REFLEXION(W) = résiduel = SIG(W) - α · SOURCES(W) (clippé ≥ 0 puis
  renormalisé) → composante "propre" de l'auteur, débarrassée de l'écho
  des sources.

Hypothèse à tester : la composante REFLEXION discrimine mieux les
traditions que SIG complet (ce serait un succès partiel) OU bien que les
distances entre SIG agrégées sont plus fortement corrélées au graphe
d'héritage §148 que les distances entre SIG des fragments individuels
(succès de l'agrégation).

Output : research/nipada/falsification/nipada_v149_decomposition.json
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v149_decomposition.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"


# ---------- Import dynamique de §145 (extracteur multilingue) ----------
def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v144 = _load("nipada_annotate_v14_v144", SCRIPTS / "nipada_annotate_v14_v144.py")
_v145 = _load("nipada_v14_multiling_v145", SCRIPTS / "nipada_v14_multiling_v145.py")

GOLD = _v144.GOLD              # 50 entrées : id_frag → (work, lang, text, atoms_set)
V14 = _v145.V14                # 14 atomes
LEX = _v145.LEX                # lexique enrichi
NEG_MARKERS = _v145.NEG_MARKERS
UNIV_MARKERS = _v145.UNIV_MARKERS
EQ_MARKERS = _v145.EQ_MARKERS


# ---------- Signature fréquentielle V14 (vs binaire) ----------
def freq_signature(text: str, lang: str) -> dict[str, float]:
    """
    Compte le nombre de matches lexicaux par atome V14 (signature
    fréquentielle, non binaire). Applique aussi les méta-règles §145
    (NEG, UNIV, EQ, NUM) — chaque déclenchement compte +1 sur les
    atomes ciblés.
    """
    counts = {a: 0 for a in V14}
    text_lc = text.lower()

    # Marqueurs lexicaux (lex enrichi v145)
    for atom in V14:
        markers = LEX.get(atom, {}).get(lang, [])
        for m in markers:
            counts[atom] += text_lc.count(m.lower())

    # Méta-règles
    for m in NEG_MARKERS.get(lang, []):
        if m in text_lc:
            counts["DIFFÉRENCE"] += 1
            counts["MODALITÉ"] += 1
    for m in UNIV_MARKERS.get(lang, []):
        if m in text_lc:
            counts["MODALITÉ"] += 1
    for m in EQ_MARKERS.get(lang, []):
        if m in text_lc:
            counts["ÊTRE"] += 1
            counts["ÉQUATION"] += 1
    if any(c.isdigit() for c in text):
        counts["NOMBRE"] += 1

    return counts


_FRAG_CACHE: list[dict] | None = None


def _all_fragments() -> list[dict]:
    """Charge les 50 fragments depuis corpus/protoatheism/<work_id>/fragments.jsonl."""
    global _FRAG_CACHE
    if _FRAG_CACHE is not None:
        return _FRAG_CACHE
    base = ROOT / "corpus" / "protoatheism"
    out: list[dict] = []
    for d in sorted(base.iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    _FRAG_CACHE = out
    return out


def aggregate_work_signature(work_id: str) -> dict[str, float]:
    """Concatène les fragments d'une œuvre puis calcule la signature
    fréquentielle agrégée, normalisée L1. Si tous les comptes sont nuls,
    renvoie la distribution uniforme (évite division par zéro)."""
    frags = [f for f in _all_fragments() if f["work_id"] == work_id]
    sig = {a: 0.0 for a in V14}
    for f in frags:
        c = freq_signature(f["text"], f["lang"])
        for a in V14:
            sig[a] += c[a]
    total = sum(sig.values())
    if total > 0:
        return {a: sig[a] / total for a in V14}
    return {a: 1.0 / len(V14) for a in V14}


# ---------- Décomposition héritée / propre ----------
def _vec(d: dict[str, float]) -> list[float]:
    return [d[a] for a in V14]


def _norm_l2(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _l1_normalize(v: list[float]) -> list[float]:
    s = sum(max(0.0, x) for x in v)
    if s <= 0:
        return [1.0 / len(v)] * len(v)
    return [max(0.0, x) / s for x in v]


def fit_alpha(sig_w: list[float], sources_w: list[float]) -> float:
    """α ∈ [0, 1] minimisant ||sig - α·sources||² avec α ≥ 0.
    Solution close-form non contrainte : α* = <sig, sources> / ||sources||².
    Puis clippage à [0, 1] (interprétabilité : α=0 ⇒ aucun héritage exprimé,
    α=1 ⇒ héritage complet)."""
    denom = _dot(sources_w, sources_w)
    if denom <= 0:
        return 0.0
    alpha = _dot(sig_w, sources_w) / denom
    return max(0.0, min(1.0, alpha))


def decompose(sig_w: dict[str, float], sources_w: dict[str, float]) -> dict:
    """Décompose SIG = α · SOURCES + REFLEXION."""
    sw, sr = _vec(sig_w), _vec(sources_w)
    alpha = fit_alpha(sw, sr)
    refl = [sw[i] - alpha * sr[i] for i in range(len(sw))]
    refl_pos = [max(0.0, r) for r in refl]
    refl_norm = _l1_normalize(refl_pos)
    # Part de la signature "expliquée" par l'héritage
    inherited_part = [alpha * sr[i] for i in range(len(sw))]
    inherited_norm_l2 = _norm_l2(inherited_part)
    sig_norm_l2 = _norm_l2(sw)
    explained_ratio = inherited_norm_l2 / sig_norm_l2 if sig_norm_l2 > 0 else 0.0
    return {
        "alpha": round(alpha, 4),
        "explained_ratio": round(explained_ratio, 4),
        "reflexion": {a: round(r, 4) for a, r in zip(V14, refl_norm)},
    }


# ---------- Sources d'une œuvre (filtrées au corpus proto-athéiste) ----------
def in_corpus_sources(graph: dict, target_work: str) -> list[tuple[str, float]]:
    """Renvoie [(src_id, weight), ...] pour les arêtes src→target_work
    où src est aussi une œuvre proto-athéiste (et donc a une signature)."""
    proto_ids = {n for n, info in graph["nodes"].items() if info["kind"] == "proto_atheist_work"}
    out = []
    for e in graph["edges"]:
        if e["tgt"] == target_work and e["src"] in proto_ids and e["src"] != target_work:
            out.append((e["src"], e["weight"]))
    return out


def weighted_source_signature(srcs: list[tuple[str, float]], sigs: dict[str, dict[str, float]]) -> dict[str, float]:
    """Somme pondérée des signatures des sources, renormalisée L1."""
    if not srcs:
        return {a: 0.0 for a in V14}
    accum = {a: 0.0 for a in V14}
    wsum = 0.0
    for src_id, w in srcs:
        s = sigs[src_id]
        for a in V14:
            accum[a] += w * s[a]
        wsum += w
    if wsum > 0:
        for a in V14:
            accum[a] /= wsum
    return accum


# ---------- Métriques de discrimination ----------
def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    va, vb = _vec(a), _vec(b)
    na, nb = _norm_l2(va), _norm_l2(vb)
    if na == 0 or nb == 0:
        return 0.0
    return _dot(va, vb) / (na * nb)


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    works = list(graph["proto_pair_distances"].keys())[:1]  # juste pour init type
    proto_ids = [n for n, info in graph["nodes"].items() if info["kind"] == "proto_atheist_work"]

    # 1) Signature agrégée par œuvre (fréquentielle, normalisée L1)
    sigs: dict[str, dict[str, float]] = {wid: aggregate_work_signature(wid) for wid in proto_ids}

    # 2) Décomposition héritée / propre
    decomp: dict[str, dict] = {}
    for wid in proto_ids:
        srcs = in_corpus_sources(graph, wid)
        src_sig = weighted_source_signature(srcs, sigs)
        d = decompose(sigs[wid], src_sig)
        d["sources_in_corpus"] = [{"src": s, "weight": w} for (s, w) in srcs]
        d["n_sources"] = len(srcs)
        decomp[wid] = d

    # 3) Signatures REFLEXION (composante propre)
    refl_sigs: dict[str, dict[str, float]] = {wid: decomp[wid]["reflexion"] for wid in proto_ids}

    # 4) Distances entre paires (cosinus dist = 1 - cos sim)
    pairs_sig, pairs_refl, pairs_graph = [], [], []
    pair_details = []
    for i, a in enumerate(proto_ids):
        for b in proto_ids[i + 1:]:
            # §148 stocke les clés en ordre alphabétique (min::max)
            ka, kb = (a, b) if a < b else (b, a)
            d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
            if d_graph is None:
                continue
            d_sig = 1.0 - cosine(sigs[a], sigs[b])
            d_refl = 1.0 - cosine(refl_sigs[a], refl_sigs[b])
            pairs_sig.append(d_sig)
            pairs_refl.append(d_refl)
            pairs_graph.append(d_graph)
            pair_details.append({"a": a, "b": b, "d_graph": round(d_graph, 4),
                                  "d_sig": round(d_sig, 4), "d_refl": round(d_refl, 4)})

    # 5) Corrélation Pearson distance_signature ↔ distance_graphe
    r_sig = pearson(pairs_sig, pairs_graph)
    r_refl = pearson(pairs_refl, pairs_graph)

    # 6) Verdict §149 : le résiduel reproduit-il **moins** la transmission
    #    (donc isole mieux la composante propre) que la signature complète ?
    summary = {
        "n_works": len(proto_ids),
        "n_connected_pairs": len(pairs_graph),
        "alpha_mean": round(sum(decomp[w]["alpha"] for w in proto_ids) / len(proto_ids), 4),
        "explained_ratio_mean": round(
            sum(decomp[w]["explained_ratio"] for w in proto_ids) / len(proto_ids), 4
        ),
        "pearson_dsig_vs_dgraph": round(r_sig, 4),
        "pearson_drefl_vs_dgraph": round(r_refl, 4),
        "delta_pearson": round(r_sig - r_refl, 4),
        "interpretation_pearson_sig": (
            "positive ⇒ + transmission ⇒ + similarité de signature (cohérent avec §148)"
            if r_sig < 0 else "négatif ⇒ + transmission ⇒ - similarité (anomalie)"
        ),
        "interpretation_drefl": (
            "REFLEXION moins corrélée au graphe que SIG ⇒ héritage bien isolé"
            if abs(r_refl) < abs(r_sig) else "REFLEXION reste corrélée ⇒ décomposition incomplète"
        ),
    }

    payload = {
        "version": "v149",
        "step": "§149 — décomposition héritée/propre des signatures V14",
        "summary": summary,
        "signatures_aggregated": sigs,
        "decomposition": decomp,
        "pair_distances": pair_details,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §149 — décomposition écrite : {OUT}")
    print(f"  œuvres = {summary['n_works']}, paires connectées = {summary['n_connected_pairs']}")
    print(f"  α moyen = {summary['alpha_mean']} | part héritée moyenne = {summary['explained_ratio_mean']}")
    print(f"  Pearson(d_sig, d_graphe)  = {summary['pearson_dsig_vs_dgraph']:+.4f}  (négatif attendu)")
    print(f"  Pearson(d_refl, d_graphe) = {summary['pearson_drefl_vs_dgraph']:+.4f}  (≈ 0 attendu si décomp. OK)")
    print(f"  Δ |r_sig| - |r_refl|     = {abs(r_sig) - abs(r_refl):+.4f}")
    print()
    print("  α par œuvre :")
    for wid in proto_ids:
        d = decomp[wid]
        print(f"    {wid:30s} α={d['alpha']:.3f}  ratio={d['explained_ratio']:.3f}  n_sources={d['n_sources']}")


if __name__ == "__main__":
    main()

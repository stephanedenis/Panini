#!/usr/bin/env python3
"""
nipada_corpus_quality_audit.py — §273
Audit quantitatif de la qualité de restitution textuelle du corpus NiPaDa.

Tests implémentés :
  1. Détection des doublons de signature (d_lex < 0.02 entre textes distincts)
  2. Concentration de signature (dominance top-1, indice HHI)
  3. Stabilité bootstrap (cosine split-half sur textes longs, si cache disponible)
  4. Résumé global : textes problématiques, rang par qualité

Usage :
  python3 nipada_corpus_quality_audit.py [--corpus PATH] [--out PATH]
"""

import json
import os
import re
import math
import random
import hashlib
import argparse
from collections import defaultdict
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
REPO = Path("/home/stephane/GitHub/Panini-Research")
CORPUS_DEFAULT = REPO / "nipada/corpus/signed_corpus_v272_v16_extended.json"
CACHE_ST  = REPO / "nipada/corpus/_cache/sacred_texts"
CACHE_SC  = REPO / "nipada/corpus/_cache/suttacentral"
CACHE_MIT = REPO / "nipada/corpus/_cache"   # mit_* + pg_* live here flat

OUTPUT_DEFAULT = REPO / "nipada/corpus/quality_audit_v273.json"

# ── Atom vocabulary (V16) ────────────────────────────────────────────────────
V16_ATOMS = [
    "ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS","MODALITÉ",
    "NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE","SYMÉTRIE",
    "ÉQUATION","CAUSALITÉ","ÉVÉNEMENT",
]

# ── Lexicon (V16) — for token coverage measurement ───────────────────────────
# Copied from nipada_fetch_corpus_v212f.py (must stay in sync)
V16_LEXICON: dict[str, list[str]] = {
    "ÊTRE":        ["is","are","was","were","be","been","being","exist","exists",
                    "existence","am","real","reality","true","truth"],
    "DIFFÉRENCE":  ["different","difference","differ","other","another","else",
                    "distinct","distinction","unlike","not","no","none","nor",
                    "neither","except","but","however","contrast","contrary",
                    "opposite","versus","against","change","changes","changed"],
    "RAPPORT":     ["relation","relations","related","relationship","between",
                    "with","connect","connection","connected","link","linked",
                    "associate","association","bond","together","mutual",
                    "interaction","interact","correlate","correlation"],
    "ORIENTATION": ["toward","towards","from","forward","direction","aim","goal",
                    "purpose","tend","tendency","move","moves","movement","path",
                    "way","lead","leads","point","points","guide","toward","seek",
                    "approach","progress","flow","flux"],
    "SUJET":       ["self","selves","person","persons","personal","individual",
                    "individuals","subject","subjects","agent","agents","actor",
                    "soul","souls","consciousness","mind","minds","ego","one",
                    "oneself","identity","who","being","beings","creature",
                    "living","human","humans"],
    "TEMPS":       ["time","times","when","before","after","during","while",
                    "then","now","moment","past","present","future","always",
                    "never","sometimes","often","already","yet","still","again",
                    "once","eternal","eternity","duration","sequence","order",
                    "beginning","end","period","age","epoch","cycle","phase"],
    "MODALITÉ":    ["can","could","may","might","must","should","would","shall",
                    "will","need","ought","possible","impossible","necessary",
                    "necessity","certain","uncertain","allow","allows","permit",
                    "permits","forbidden","required","obligatory","potential",
                    "actual","actual","ability","unable","capable","capacity"],
    "NOMBRE":      ["one","two","three","four","five","six","seven","eight",
                    "nine","ten","many","few","several","all","each","every",
                    "both","neither","number","numbers","count","multiple",
                    "single","double","triple","half","whole","part","parts",
                    "quantity","quantities","amount","total","sum","measure"],
    "ESPACE":      ["place","places","here","there","where","inside","outside",
                    "above","below","up","down","left","right","near","far",
                    "space","spatial","position","location","region","area",
                    "domain","field","extent","boundary","border","within",
                    "beyond","around","contains","contained","adjacent","side"],
    "OPÉRATION":   ["do","does","did","done","make","makes","made","act","acts",
                    "action","actions","perform","performs","execute","create",
                    "transform","transforms","produce","produces","apply",
                    "applies","operate","operations","process","processes",
                    "function","functions","generate","implement","carry"],
    "FONCTION":    ["role","roles","purpose","function","functions","serve",
                    "serves","use","uses","means","tool","instrument","method",
                    "methods","mechanism","mechanisms","property","properties",
                    "attribute","attributes","capacity","capacities","task",
                    "tasks","duty","duties","power","powers","cause","effect"],
    "STRUCTURE":   ["structure","structures","form","forms","pattern","patterns",
                    "system","systems","order","ordered","organize","organized",
                    "organization","arrange","arrangement","compose","composed",
                    "composition","hierarchy","hierarchies","network","networks",
                    "framework","layer","layers","element","elements","part",
                    "parts","whole","set","sets","class","classes","type","types"],
    "SYMÉTRIE":    ["same","equal","equals","equivalent","symmetric","symmetry",
                    "balance","balanced","similar","similarity","alike","like",
                    "identical","correspond","correspondence","mirror","reflect",
                    "reflection","proportion","proportional","harmony","parallel",
                    "uniform","uniformity","invariant","invariance","regular",
                    "regular","regular","regularity","congruent","congruence"],
    "ÉQUATION":    ["equation","equations","define","defines","definition",
                    "formula","formulas","law","laws","rule","rules","principle",
                    "principles","theorem","theorems","axiom","axioms","identity",
                    "identities","condition","conditions","constraint",
                    "constraints","determine","determines","specification",
                    "express","expression","represents","represent","property"],
    "CAUSALITÉ":   ["cause","causes","caused","effect","effects","result",
                    "results","because","since","therefore","thus","hence",
                    "consequently","lead","leads","produce","produces","make",
                    "makes","force","forces","necessary","condition","if",
                    "then","depend","depends","influence","influences","due",
                    "reason","reasons","origin","origins","source","sources"],
    "ÉVÉNEMENT":   ["event","events","happen","happens","happened","occur",
                    "occurs","occurred","incident","incidents","change","changes",
                    "changed","arise","arises","arose","take place","took place",
                    "emerge","emerges","appeared","appear","start","started",
                    "begin","began","end","ended","finish","finished","moment",
                    "moments","episode","episodes","process","processes"],
}

# Build fast lookup: word → set of atoms
def build_word_to_atoms(lexicon: dict[str, list[str]]) -> dict[str, set[str]]:
    w2a: dict[str, set[str]] = defaultdict(set)
    for atom, words in lexicon.items():
        for w in words:
            w2a[w.lower()].add(atom)
    return w2a

WORD_TO_ATOMS = build_word_to_atoms(V16_LEXICON)

# ── Distance function ─────────────────────────────────────────────────────────

def d_lex(sig_a: dict, sig_b: dict, atoms=V16_ATOMS) -> float:
    """Symétrique L1-sur-simplexe entre deux signatures."""
    total = 0.0
    for a in atoms:
        total += abs(sig_a.get(a, 0.0) - sig_b.get(a, 0.0))
    return total / 2.0


def cosine_sim(sig_a: dict, sig_b: dict, atoms=V16_ATOMS) -> float:
    na = math.sqrt(sum(sig_a.get(a,0)**2 for a in atoms))
    nb = math.sqrt(sum(sig_b.get(a,0)**2 for a in atoms))
    if na == 0 or nb == 0:
        return 0.0
    dot = sum(sig_a.get(a,0)*sig_b.get(a,0) for a in atoms)
    return dot / (na * nb)

# ── Signature concentration ───────────────────────────────────────────────────

def hhi(sig: dict, atoms=V16_ATOMS) -> float:
    """Herfindahl-Hirschman Index — 1/N (uniform) to 1.0 (degenerate)."""
    return sum(sig.get(a, 0)**2 for a in atoms)

def top1_share(sig: dict, atoms=V16_ATOMS) -> tuple[str, float]:
    vals = [(a, sig.get(a, 0.0)) for a in atoms]
    vals.sort(key=lambda x: -x[1])
    return vals[0] if vals else ("", 0.0)

# ── Text tokenisation (same logic as fetcher) ─────────────────────────────────

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())

def compute_signature(tokens: list[str], atoms=V16_ATOMS) -> dict[str, float]:
    counts: dict[str, float] = defaultdict(float)
    for tok in tokens:
        for atom in WORD_TO_ATOMS.get(tok, []):
            counts[atom] += 1.0
    total = sum(counts.values())
    if total == 0:
        return {a: 0.0 for a in atoms}
    return {a: counts[a]/total for a in atoms}

def coverage(tokens: list[str]) -> float:
    """Fraction of tokens matched by at least one atom."""
    matched = sum(1 for t in tokens if t in WORD_TO_ATOMS)
    return matched / len(tokens) if tokens else 0.0

# ── Bootstrap split-half stability ───────────────────────────────────────────

def bootstrap_stability(tokens: list[str], n_splits=30, min_tokens=500,
                        atoms=V16_ATOMS) -> dict:
    """
    Stability = mean cosine(sig_half1, sig_half2) over n_splits random halves.
    Returns dict with mean, std, n_splits; or None if text too short.
    """
    if len(tokens) < min_tokens:
        return None
    half = len(tokens) // 2
    sims = []
    for _ in range(n_splits):
        shuffled = tokens[:]
        random.shuffle(shuffled)
        s1 = compute_signature(shuffled[:half], atoms)
        s2 = compute_signature(shuffled[half:], atoms)
        sims.append(cosine_sim(s1, s2, atoms))
    mu = sum(sims) / len(sims)
    var = sum((s - mu)**2 for s in sims) / len(sims)
    return {"mean": round(mu, 4), "std": round(math.sqrt(var), 4),
            "n_splits": n_splits, "n_tokens": len(tokens)}

# ── Cache lookup ──────────────────────────────────────────────────────────────

def find_cache_text(entry: dict) -> str | None:
    """
    Try to locate raw text for an entry.
    Priority: v263_ > v237_ > unversioned > suttacentral cache.
    Returns text content or None.
    """
    lid = entry["local_id"]
    source = entry.get("source", "")

    if source in ("sacred-texts", "sacred_texts", "sacredtexts"):
        for prefix in ("v263_", "v237_", ""):
            path = CACHE_ST / f"{prefix}{lid}.txt"
            if path.exists():
                return path.read_text(encoding="utf-8", errors="ignore")
    elif source == "suttacentral":
        for subdir in (CACHE_SC / "leaves", CACHE_SC):
            path = subdir / f"{lid}.txt"
            if path.exists():
                return path.read_text(encoding="utf-8", errors="ignore")
    else:
        # MIT / PG style: flat files mit_{lid}_s*.txt or pg_{lid}.txt
        for pattern_root in (CACHE_MIT,):
            for candidate in pattern_root.glob(f"*{lid}*.txt"):
                return candidate.read_text(encoding="utf-8", errors="ignore")
    return None

# ── Main audit ────────────────────────────────────────────────────────────────

def run_audit(corpus_path: Path, output_path: Path, seed=42):
    random.seed(seed)

    print(f"\n{'='*70}")
    print(f"  NiPaDa Corpus Quality Audit — §273")
    print(f"  Corpus : {corpus_path.name}")
    print(f"{'='*70}\n")

    corpus = json.loads(corpus_path.read_text())
    signed = corpus["signed"]
    sig_key = "v16_signature" if "v16_signature" in signed[0] else "v14_signature"
    print(f"  Entries  : {len(signed)}")
    print(f"  Sig key  : {sig_key}\n")

    # ── 1. Build signature matrix ─────────────────────────────────────────────
    entries = []
    for e in signed:
        sig = e[sig_key]
        entries.append({
            "local_id":   e["local_id"],
            "lang":       e.get("lang", "?"),
            "source":     e.get("source", "?"),
            "n_words":    e.get("n_words", 0),
            "n_chars":    e.get("n_chars", 0),
            "sig":        sig,
            "hhi":        round(hhi(sig), 4),
            "top1_atom":  top1_share(sig)[0],
            "top1_val":   round(top1_share(sig)[1], 4),
        })

    # ── 2. Duplicate detection (pairwise d_lex) ───────────────────────────────
    print("── Test 1 : Duplicate signature detection (d_lex < 0.02) ──")
    THRESH = 0.02
    dup_pairs = []
    n = len(entries)
    for i in range(n):
        for j in range(i+1, n):
            d = d_lex(entries[i]["sig"], entries[j]["sig"])
            if d < THRESH:
                dup_pairs.append({
                    "i": entries[i]["local_id"],
                    "j": entries[j]["local_id"],
                    "d_lex": round(d, 6),
                })

    # Group into connected components
    adj = defaultdict(set)
    for pair in dup_pairs:
        adj[pair["i"]].add(pair["j"])
        adj[pair["j"]].add(pair["i"])
    visited = set()
    dup_groups = []
    for lid in list(adj.keys()):
        if lid not in visited:
            stack = [lid]
            group = []
            while stack:
                node = stack.pop()
                if node in visited: continue
                visited.add(node)
                group.append(node)
                stack.extend(adj[node] - visited)
            if len(group) > 1:
                dup_groups.append(sorted(group))

    print(f"  Duplicate pairs found    : {len(dup_pairs)}")
    print(f"  Duplicate groups (≥2)    : {len(dup_groups)}")
    n_dup_texts = sum(len(g) for g in dup_groups)
    print(f"  Texts in dup groups      : {n_dup_texts} / {n} ({100*n_dup_texts/n:.1f}%)")
    print()
    for g in sorted(dup_groups, key=len, reverse=True):
        # Get d_lex for pair representative
        sig0 = next(e["sig"] for e in entries if e["local_id"] == g[0])
        sig1 = next(e["sig"] for e in entries if e["local_id"] == g[1])
        d = round(d_lex(sig0, sig1), 6)
        print(f"  [{len(g)} texts, d={d}] {g}")

    # Mark duplicates
    dup_set: set[str] = set()
    for g in dup_groups:
        for lid in g:
            dup_set.add(lid)
    for e in entries:
        e["is_duplicate"] = e["local_id"] in dup_set
        e["dup_group"] = next(
            (g for g in dup_groups if e["local_id"] in g), None
        )

    # ── 3. Signature concentration ────────────────────────────────────────────
    print("\n── Test 2 : Signature concentration (HHI, top-1 dominance) ──")
    hhi_uniform = 1.0 / len(V16_ATOMS)   # ≈ 0.0625 for 16 atoms
    concentrated = [e for e in entries if e["hhi"] > 0.25]
    print(f"  Uniform HHI baseline     : {hhi_uniform:.4f}")
    print(f"  Texts with HHI > 0.25    : {len(concentrated)} / {n}")
    if concentrated:
        print("  ── Top concentrated texts (may indicate sparse/biased content):")
        for e in sorted(concentrated, key=lambda x: -x["hhi"])[:10]:
            dup = " [DUP]" if e["is_duplicate"] else ""
            print(f"    {e['local_id']:<35} HHI={e['hhi']:.4f}  top1={e['top1_atom']}={e['top1_val']:.3f}{dup}")

    # ── 4. Bootstrap stability ────────────────────────────────────────────────
    print("\n── Test 3 : Bootstrap split-half stability ──")
    stability_results = []
    n_found = 0
    n_computed = 0
    n_short = 0

    for e in entries:
        text = find_cache_text(e)
        if text is None:
            e["stability"] = None
            e["coverage"] = None
            continue
        n_found += 1
        tokens = tokenize(text)
        cov = coverage(tokens)
        e["coverage"] = round(cov, 4)
        result = bootstrap_stability(tokens, n_splits=30)
        e["stability"] = result
        if result is None:
            n_short += 1
        else:
            n_computed += 1
            stability_results.append((e["local_id"], result["mean"], result["std"]))

    print(f"  Texts with cached text   : {n_found} / {n}")
    print(f"  Too short for bootstrap  : {n_short}")
    print(f"  Stability computed       : {n_computed}")
    if stability_results:
        stability_results.sort(key=lambda x: x[1])
        print("\n  ── Lowest stability (most variable split-half):")
        for lid, mu, std in stability_results[:8]:
            cov = next(e["coverage"] for e in entries if e["local_id"] == lid)
            dup = " [DUP]" if lid in dup_set else ""
            print(f"    {lid:<35} cosine={mu:.4f}±{std:.4f}  cov={cov:.3f}{dup}")
        print("\n  ── Highest stability:")
        for lid, mu, std in stability_results[-6:]:
            cov = next(e["coverage"] for e in entries if e["local_id"] == lid)
            dup = " [DUP]" if lid in dup_set else ""
            print(f"    {lid:<35} cosine={mu:.4f}±{std:.4f}  cov={cov:.3f}{dup}")

    # ── 5. Coverage summary ───────────────────────────────────────────────────
    cov_entries = [e for e in entries if e.get("coverage") is not None]
    if cov_entries:
        print(f"\n── Test 4 : Token coverage by V16 lexicon ──")
        covs = [e["coverage"] for e in cov_entries]
        print(f"  Texts with coverage data : {len(cov_entries)}")
        print(f"  Mean coverage            : {sum(covs)/len(covs):.3f}")
        print(f"  Min coverage             : {min(covs):.3f}")
        print(f"  Max coverage             : {max(covs):.3f}")
        low_cov = [e for e in cov_entries if e["coverage"] < 0.05]
        print(f"  Texts with coverage < 5% : {len(low_cov)}")
        for e in sorted(low_cov, key=lambda x: x["coverage"])[:10]:
            dup = " [DUP]" if e["is_duplicate"] else ""
            print(f"    {e['local_id']:<35} cov={e['coverage']:.4f}{dup}")

    # ── 6. Global quality score ───────────────────────────────────────────────
    print("\n── Global quality ranking ──")
    for e in entries:
        # Quality = 0..1 composite (higher = better)
        q = 0.0
        n_factors = 0
        # Factor 1: not a duplicate
        q += 0.0 if e["is_duplicate"] else 1.0
        n_factors += 1
        # Factor 2: low HHI → close to uniform (normalised)
        hhi_worst = 1.0
        hhi_best  = hhi_uniform
        hhi_norm  = max(0.0, 1.0 - (e["hhi"] - hhi_best) / (hhi_worst - hhi_best))
        q += hhi_norm
        n_factors += 1
        # Factor 3: stability (if available)
        if e.get("stability"):
            q += e["stability"]["mean"]
            n_factors += 1
        # Factor 4: coverage (if available)
        if e.get("coverage") is not None:
            q += e["coverage"]
            n_factors += 1
        e["quality_score"] = round(q / n_factors, 4)

    ranked = sorted(entries, key=lambda x: x["quality_score"])
    print("\n  ── Bottom 15 (worst quality):")
    print(f"  {'text':<35} {'Q':>6}  {'HHI':>6}  {'dup':>4}  {'cov':>6}  {'stab':>6}")
    print(f"  {'-'*35} {'-'*6}  {'-'*6}  {'-'*4}  {'-'*6}  {'-'*6}")
    for e in ranked[:15]:
        cov  = f"{e['coverage']:.3f}" if e.get("coverage") is not None else "  n/a"
        stab = f"{e['stability']['mean']:.3f}" if e.get("stability") else "  n/a"
        dup  = "YES" if e["is_duplicate"] else " no"
        print(f"  {e['local_id']:<35} {e['quality_score']:>6.3f}  {e['hhi']:>6.4f}  {dup:>4}  {cov:>6}  {stab:>6}")

    print("\n  ── Top 10 (best quality):")
    for e in ranked[-10:]:
        cov  = f"{e['coverage']:.3f}" if e.get("coverage") is not None else "  n/a"
        stab = f"{e['stability']['mean']:.3f}" if e.get("stability") else "  n/a"
        dup  = "YES" if e["is_duplicate"] else " no"
        print(f"  {e['local_id']:<35} {e['quality_score']:>6.3f}  {e['hhi']:>6.4f}  {dup:>4}  {cov:>6}  {stab:>6}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"  Total texts              : {n}")
    print(f"  Duplicate groups         : {len(dup_groups)}")
    print(f"  Texts with duplicates    : {n_dup_texts} ({100*n_dup_texts/n:.1f}%)")
    print(f"  Highly concentrated      : {len(concentrated)}")
    print(f"  Stability computed       : {n_computed}")
    if stability_results:
        all_mu = [r[1] for r in stability_results]
        print(f"  Mean stability           : {sum(all_mu)/len(all_mu):.4f}")
    if cov_entries:
        mu_cov = sum(e["coverage"] for e in cov_entries) / len(cov_entries)
        print(f"  Mean token coverage      : {mu_cov:.4f}")
    print(f"{'='*70}\n")

    # ── Write output ──────────────────────────────────────────────────────────
    output = {
        "version": "v273_audit",
        "corpus": str(corpus_path),
        "n_entries": n,
        "n_duplicate_groups": len(dup_groups),
        "n_duplicate_texts": n_dup_texts,
        "duplicate_groups": dup_groups,
        "duplicate_pairs": dup_pairs,
        "entries": [
            {k: v for k, v in e.items() if k != "sig"}  # omit raw sig for brevity
            for e in ranked
        ],
    }
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"  Report written : {output_path}\n")

    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default=str(CORPUS_DEFAULT))
    parser.add_argument("--out",    default=str(OUTPUT_DEFAULT))
    args = parser.parse_args()
    run_audit(Path(args.corpus), Path(args.out))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
§157 — Leave-one-out par œuvre : quelle est la sensibilité du R²(d_graph
seul) à chaque œuvre du corpus ?

Pour chaque œuvre w :
  - Retirer w du corpus
  - Recalculer toutes les paires (d_graph, d_sig) sur les 9 œuvres restantes
  - Refit OLS d_sig ~ d_graph et OLS d_sig ~ d_graph + dyear/1000 + same_trad
  - Reporter R² et β_d_graph

Si R² monte fortement quand on retire w → w est un outlier (mal placée
dans le graphe ou signature inhabituelle).
Si R² varie peu → toutes les œuvres contribuent uniformément au bruit.

Output : research/nipada/falsification/nipada_v157_loo_per_work.json
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
OUT = RES_DIR / "nipada_v157_loo_per_work.json"

GRAPH_PATH = RES_DIR / "nipada_v148_inheritance_graph.json"
META_PATH = RES_DIR / "nipada_v147_metadata.json"
DECOMP_PATH = RES_DIR / "nipada_v149_decomposition.json"
DENSE_PATH = RES_DIR / "nipada_v151_dense_signatures.json"
BIGRAM_PATH = RES_DIR / "nipada_v155_bigrams.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_v150 = _load("nipada_validation_v150", SCRIPTS / "nipada_validation_v150.py")
V14 = _v150.V14
cosine = _v150.cosine
ols = _v150.ols


def cosine_dict(a: dict, b: dict) -> float:
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if (na > 0 and nb > 0) else 0.0


def main() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    decomp = json.loads(DECOMP_PATH.read_text(encoding="utf-8"))
    dense = json.loads(DENSE_PATH.read_text(encoding="utf-8"))
    bigram = json.loads(BIGRAM_PATH.read_text(encoding="utf-8"))

    proto_ids = [n for n, info in graph["nodes"].items()
                 if info["kind"] == "proto_atheist_work"]
    works_year = {wid: meta["works"][wid]["writing_year"] for wid in proto_ids}
    works_trad = {wid: meta["works"][wid]["tradition_label"] for wid in proto_ids}

    sigs_lex = decomp["signatures_aggregated"]
    sigs_dense = dense["work_signatures_aggregated"]
    sigs_bigram = bigram["bigram_signatures"]

    def build_pairs(sigs: dict, works: list[str], cos_func=cosine):
        out = []
        for i, a in enumerate(works):
            for b in works[i + 1:]:
                ka, kb = (a, b) if a < b else (b, a)
                d_graph = graph["proto_pair_distances"].get(f"{ka}::{kb}")
                if d_graph is None:
                    continue
                d_sig = 1.0 - cos_func(sigs[a], sigs[b])
                dyear = abs(works_year[a] - works_year[b])
                same_trad = 1.0 if works_trad[a] == works_trad[b] else 0.0
                out.append((a, b, d_graph, d_sig, dyear, same_trad))
        return out

    def r2_d_graph_only(pairs):
        if len(pairs) < 3:
            return None
        X = [[1.0, p[2]] for p in pairs]
        y = [p[3] for p in pairs]
        b, r2 = ols(X, y)
        return {"beta": [round(x, 4) for x in b], "r2": round(r2, 4),
                "n_pairs": len(pairs)}

    def r2_full(pairs):
        if len(pairs) < 5:
            return None
        X = [[1.0, p[2], p[4] / 1000.0, p[5]] for p in pairs]
        y = [p[3] for p in pairs]
        b, r2 = ols(X, y)
        return {"beta": [round(x, 4) for x in b], "r2": round(r2, 4),
                "n_pairs": len(pairs)}

    # Baseline (toutes œuvres)
    base_lex = r2_d_graph_only(build_pairs(sigs_lex, proto_ids))
    base_dense = r2_d_graph_only(build_pairs(sigs_dense, proto_ids, cosine_dict))
    base_bigram = r2_d_graph_only(build_pairs(sigs_bigram, proto_ids, cosine_dict))

    # LOO par œuvre
    loo_results = {}
    for held_out in proto_ids:
        remaining = [w for w in proto_ids if w != held_out]
        loo_results[held_out] = {
            "lex_d_graph_only": r2_d_graph_only(build_pairs(sigs_lex, remaining)),
            "dense_d_graph_only": r2_d_graph_only(build_pairs(sigs_dense, remaining, cosine_dict)),
            "bigram_d_graph_only": r2_d_graph_only(build_pairs(sigs_bigram, remaining, cosine_dict)),
            "lex_full": r2_full(build_pairs(sigs_lex, remaining)),
            "dense_full": r2_full(build_pairs(sigs_dense, remaining, cosine_dict)),
            "bigram_full": r2_full(build_pairs(sigs_bigram, remaining, cosine_dict)),
        }

    # Identifier les œuvres dont le retrait change le plus R²(d_graph seul)
    def delta_r2(rep: str):
        base = {"lex": base_lex, "dense": base_dense, "bigram": base_bigram}[rep]["r2"]
        out = []
        for w, results in loo_results.items():
            r = results[f"{rep}_d_graph_only"]["r2"]
            out.append((w, round(r - base, 4), r))
        return sorted(out, key=lambda x: x[1], reverse=True)

    deltas_lex = delta_r2("lex")
    deltas_dense = delta_r2("dense")
    deltas_bigram = delta_r2("bigram")

    payload = {
        "version": "v157",
        "step": "§157 — leave-one-out par œuvre, R²(d_graph seul)",
        "baseline_full_corpus": {
            "lex": base_lex,
            "dense": base_dense,
            "bigram": base_bigram,
        },
        "leave_one_out_per_work": loo_results,
        "delta_R2_when_removed": {
            "lex": [{"work": w, "delta_r2": d, "r2_loo": r2} for w, d, r2 in deltas_lex],
            "dense": [{"work": w, "delta_r2": d, "r2_loo": r2} for w, d, r2 in deltas_dense],
            "bigram": [{"work": w, "delta_r2": d, "r2_loo": r2} for w, d, r2 in deltas_bigram],
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §157 — LOO écrit : {OUT}")
    print()
    print("─── R²(d_graph seul) baseline (10 œuvres) ───")
    print(f"  lex    = {base_lex['r2']:.4f}")
    print(f"  dense  = {base_dense['r2']:.4f}")
    print(f"  bigram = {base_bigram['r2']:.4f}")
    print()
    print("─── Top 3 œuvres dont le retrait AUGMENTE R² (signature lex) ───")
    for w, d, r2 in deltas_lex[:3]:
        print(f"  − {w:25s}  ΔR² = {d:+.4f}  →  R²_loo = {r2:.4f}")
    print("   (= œuvres mal placées dans le graphe ou avec signature atypique)")
    print()
    print("─── Top 3 œuvres dont le retrait AUGMENTE R² (signature bigram) ───")
    for w, d, r2 in deltas_bigram[:3]:
        print(f"  − {w:25s}  ΔR² = {d:+.4f}  →  R²_loo = {r2:.4f}")
    print()
    print("─── Top 3 œuvres dont le retrait DIMINUE R² (signature lex) ───")
    for w, d, r2 in deltas_lex[-3:]:
        print(f"  − {w:25s}  ΔR² = {d:+.4f}  →  R²_loo = {r2:.4f}")
    print("   (= œuvres bien placées qui contribuent au signal résiduel)")


if __name__ == "__main__":
    main()

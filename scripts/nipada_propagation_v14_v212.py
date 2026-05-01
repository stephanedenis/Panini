"""§212-prop — Propagation V14 par voisinage de graphe.

Stratégie : pour chaque nœud non-signé, calcule la moyenne pondérée des V14
signatures des voisins atteignables à distance ≤ 2, pondérée par le poids
d'arête (channel_weight). Permet d'étendre n_signed de 37 à ~1764 sans fetch.

Caveat méthodologique : les signatures propagées NE SONT PAS des mesures
indépendantes — elles partagent la structure du graphe. Donc V_OPT v3 calibré
sur les paires propagées-vs-signées sera biaisé. **On ne re-calibre PAS V_OPT
sur ces signatures**. Usage : enrichir le graphe pour §213 (édition par cosine
V14 entre paires signées-signées seulement).

Output :
- research/nipada/falsification/nipada_v212_propagated_signatures.json
- docs/rapports/PROPAGATION_V14_v0.4.0.md
"""
from __future__ import annotations
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from nipada_calibration_v177 import classify_channel  # type: ignore

GRAPH_V12 = ROOT / "research/nipada/falsification/nipada_v210a_graph_v12.json"
SIGNED_CORPUS = ROOT / "research/nipada/corpus/signed_corpus_v208.json"
OUT_JSON = ROOT / "research/nipada/falsification/nipada_v212_propagated_signatures.json"
OUT_MD = ROOT / "docs/rapports/PROPAGATION_V14_v0.4.0.md"

# Poids canal pour propagation (≠ V_OPT — ici on veut max-influence direct)
PROP_W = {"direct": 1.0, "translation": 0.7, "indirect": 0.3}
MAX_HOPS = 2


def normalize(sig: dict[str, float]) -> dict[str, float]:
    s = sum(sig.values())
    if s == 0:
        return sig
    return {k: v / s for k, v in sig.items()}


def main() -> int:
    g = json.loads(GRAPH_V12.read_text())
    nodes = g["nodes"] if isinstance(g["nodes"], dict) else {n["id"]: n for n in g["nodes"]}
    edges = g["edges"]
    corpus = json.loads(SIGNED_CORPUS.read_text())
    signed_sigs = {w["graph_node_id"]: w["v14_signature"] for w in corpus["signed"] if w["graph_node_id"] in nodes}
    print(f"Nodes : {len(nodes)} | Signed : {len(signed_sigs)}")

    # Adjacence pondérée (non-dirigée)
    adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for e in edges:
        ch = classify_channel(e.get("channel", ""))
        w = PROP_W.get(ch, 0.1)
        adj[e["src"]].append((e["tgt"], w))
        adj[e["tgt"]].append((e["src"], w))

    # BFS bornée à MAX_HOPS depuis chaque nœud non-signé
    propagated: dict[str, dict[str, float]] = {}
    n_unsigned_total = 0
    n_propagated = 0
    for nid in nodes:
        if nid in signed_sigs:
            continue
        n_unsigned_total += 1
        # BFS pondérée
        visited: dict[str, float] = {nid: 1.0}  # node → cumulative weight (max-product)
        frontier = [(nid, 1.0, 0)]
        while frontier:
            new_frontier = []
            for node, w_cum, hop in frontier:
                if hop >= MAX_HOPS:
                    continue
                for nb, w in adj[node]:
                    nw = w_cum * w
                    if nw > visited.get(nb, 0.0):
                        visited[nb] = nw
                        new_frontier.append((nb, nw, hop + 1))
            frontier = new_frontier

        # Agrégation pondérée des signatures atteintes
        agg: dict[str, float] = defaultdict(float)
        total_w = 0.0
        for reached, w in visited.items():
            if reached == nid:
                continue
            sig = signed_sigs.get(reached)
            if sig is None:
                continue
            for k, v in sig.items():
                agg[k] += v * w
            total_w += w
        if total_w == 0:
            continue
        prop_sig = normalize({k: v / total_w for k, v in agg.items()})
        propagated[nid] = prop_sig
        n_propagated += 1

    print(f"Unsigned total : {n_unsigned_total}")
    print(f"Propagated     : {n_propagated} ({100*n_propagated/n_unsigned_total:.1f} %)")
    print(f"Pas atteignable : {n_unsigned_total - n_propagated}")

    out = {
        "version": "v212-prop",
        "max_hops": MAX_HOPS,
        "prop_weights": PROP_W,
        "n_signed_input": len(signed_sigs),
        "n_unsigned": n_unsigned_total,
        "n_propagated": n_propagated,
        "coverage_pct": round(100 * n_propagated / n_unsigned_total, 2),
        "propagated_signatures": propagated,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    md = [
        "# §212-prop — Propagation V14 par voisinage de graphe",
        "",
        f"**Méthode :** BFS max-product bornée (hops ≤ {MAX_HOPS}) avec poids "
        f"{PROP_W}, agrégation moyenne pondérée des signatures voisines.",
        "",
        f"**Nodes total :** {len(nodes)}",
        f"**Signed input :** {len(signed_sigs)}",
        f"**Propagated :** {n_propagated} ({100*n_propagated/n_unsigned_total:.1f} % des non-signés)",
        f"**Inatteignables :** {n_unsigned_total - n_propagated}",
        "",
        "## Caveat méthodologique",
        "",
        "Les signatures propagées dépendent de la structure du graphe.",
        "Toute calibration V_OPT sur ces signatures serait circulaire.",
        "Usage prévu :",
        "",
        "- §213 : ré-inférence d'arêtes par cosine V14 **entre paires signées seulement**",
        "- §214 : comparaison qualitative (clusters, projections) sur l'ensemble étendu",
        "",
        "## Output",
        "",
        f"- `{OUT_JSON.relative_to(ROOT)}` ({OUT_JSON.stat().st_size // 1024} kB)",
    ]
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"Sortie  : {OUT_JSON.relative_to(ROOT)}")
    print(f"Rapport : {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

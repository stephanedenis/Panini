#!/usr/bin/env python3
"""§184 — Acyclisation du graphe : test de la thèse §183.

§183 a proposé que les cycles du sous-graphe Ouest portent le signal NIPADA
(R²~0.15 global, R²~0.08 INTER) tandis que la quasi-arborescence du sous-graphe
Est explique mécaniquement R²(NW×NW)≈0.

Test §184 : construire un maximum spanning forest (Kruskal sur poids de
proximité) du graphe v8, recalculer Floyd-Warshall, mesurer la chute du R².

Trois variantes pour robustesse:
  - MST_max  : Kruskal sur poids §177 décroissants (garde arêtes "fortes")
  - MST_min  : Kruskal sur poids croissants (control arbitraire)
  - Random   : 5 forêts couvrantes aléatoires (baseline)

Prédiction §183:
  Si cycles = porteurs de signal → R²(MST) << R²(graphe complet)
  Si cycles = décoratifs         → R²(MST) ≈ R²(graphe complet)
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
CORPUS_DIR = ROOT / "corpus" / "protoatheism"

EAST_TRADS = {
    "chinese_classics", "daoism", "buddhism_theravada", "hinduism_smriti",
    "hinduism_shruti", "buddhism_modernist", "islamic_canon",
    "islamic_skeptic", "chinese_critic", "chinese_classical",
    "chinese_legalist", "chinese_mohist",
}


# ────────────── helpers ──────────────

def classify_channel(ch: str) -> str:
    s = ch.lower()
    if any(k in s for k in ["traduction", "translation"]):
        return "translation"
    if any(k in s for k in [
        "indirect", "héritier", "héritage", "transmission", "tradition",
        "comparat", "scepticisme", "lecteur", "ascendant", "post-",
        "écho", "reçu", "même école", "succession", "admire", "mentionne",
        "réception", "critique", "synthèse", "commentaire", "compile",
        "milieu",
    ]):
        return "indirect"
    return "direct"


def floyd_warshall(node_ids, edges_with_weight):
    idx = {n: i for i, n in enumerate(node_ids)}
    N = len(node_ids)
    INF = float("inf")
    D = [[INF] * N for _ in range(N)]
    for i in range(N):
        D[i][i] = 0.0
    for s, t, w in edges_with_weight:
        if s not in idx or t not in idx:
            continue
        cost = -math.log(w)
        i, j = idx[s], idx[t]
        if cost < D[i][j]:
            D[i][j] = cost
            D[j][i] = cost
    for k in range(N):
        for i in range(N):
            dik = D[i][k]
            if dik == INF:
                continue
            for j in range(N):
                nd = dik + D[k][j]
                if nd < D[i][j]:
                    D[i][j] = nd
    return D, idx


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx and dy else 0.0


def perm_test(xs, ys, n_iter=2000, seed=2026):
    rnd = random.Random(seed)
    obs = abs(pearson(xs, ys))
    ge = 0
    yl = list(ys)
    for _ in range(n_iter):
        rnd.shuffle(yl)
        if abs(pearson(xs, yl)) >= obs:
            ge += 1
    return (ge + 1) / (n_iter + 1)


def cosine_dict(a, b):
    keys = set(a.keys()) | set(b.keys())
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def load_v14_lex():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "v14lex", ROOT / "scripts" / "nipada_v14_multiling_v145.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEX


def freq_signature(text, lex, lang="eng"):
    txt_l = text.lower()
    sig = {}
    for atom, langs in lex.items():
        terms = list(set(langs.get(lang, []) + langs.get("eng", []) + langs.get("fra", [])))
        c = sum(txt_l.count(t.lower()) for t in terms if t)
        sig[atom] = c
    s = sum(sig.values()) or 1
    return {a: v / s for a, v in sig.items()}


# ────────────── Kruskal (Union-Find) ──────────────

class DSU:
    def __init__(self, ids):
        self.p = {i: i for i in ids}
        self.r = {i: 0 for i in ids}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.r[rx] < self.r[ry]:
            rx, ry = ry, rx
        self.p[ry] = rx
        if self.r[rx] == self.r[ry]:
            self.r[rx] += 1
        return True


def maximum_spanning_forest(node_ids, edges_with_weight):
    """Kruskal: garde les arêtes fortes (poids §177 grand) en évitant les cycles.
    Retourne la liste des arêtes (s, t, w) du MSF."""
    sorted_edges = sorted(edges_with_weight, key=lambda e: e[2], reverse=True)
    dsu = DSU(node_ids)
    msf = []
    for s, t, w in sorted_edges:
        if s not in dsu.p or t not in dsu.p:
            continue
        if dsu.union(s, t):
            msf.append((s, t, w))
    return msf


def random_spanning_forest(node_ids, edges_with_weight, seed):
    rnd = random.Random(seed)
    shuffled = list(edges_with_weight)
    rnd.shuffle(shuffled)
    dsu = DSU(node_ids)
    rsf = []
    for s, t, w in shuffled:
        if dsu.union(s, t):
            rsf.append((s, t, w))
    return rsf


# ────────────── Pipeline §184 ──────────────

def main():
    print("=== §184 — Acyclisation : test de la thèse §183 ===\n")

    g8 = json.loads((RES_DIR / "nipada_v182_graph_v8.json").read_text())
    nodes = g8["nodes"]
    edges = g8["edges"]
    print(f"Graphe v8: {len(nodes)} nodes, {len(edges)} edges")

    # 1. Préparer arêtes pondérées (pondération §177)
    weight_map = {"direct": 0.45, "translation": 0.45, "indirect": 0.30}
    edges_w = []
    for e in edges:
        s, t = e.get("src"), e.get("tgt")
        cat = classify_channel(e.get("channel", ""))
        edges_w.append((s, t, weight_map[cat]))

    node_ids = list(nodes.keys())

    # 2. Construire MSF (max) et MSF (min) et 5 random
    msf_max = maximum_spanning_forest(node_ids, edges_w)
    edges_w_neg = [(s, t, 1 / w) for s, t, w in edges_w]  # sort by inverse pour min
    msf_min_raw = maximum_spanning_forest(node_ids, edges_w_neg)
    msf_min = [(s, t, 1 / w) for s, t, w in msf_min_raw]  # restore weights

    rsfs = [random_spanning_forest(node_ids, edges_w, seed=1000 + i) for i in range(5)]

    print(f"  Original  : {len(edges_w)} edges")
    print(f"  MSF max   : {len(msf_max)} edges (cycles supprimés: {len(edges_w) - len(msf_max)})")
    print(f"  MSF min   : {len(msf_min)} edges")
    print(f"  Random×5  : {[len(r) for r in rsfs]}")

    # 3. Charger signatures V14-LEX (œuvres au corpus)
    lex = load_v14_lex()
    sigs = {}
    trads = {}
    for wdir in sorted(CORPUS_DIR.iterdir()):
        if not wdir.is_dir():
            continue
        prov_p = wdir / "PROVENANCE.json"
        frags_p = wdir / "fragments.jsonl"
        if not (prov_p.exists() and frags_p.exists()):
            continue
        prov = json.loads(prov_p.read_text())
        wid = prov.get("work_id", wdir.name)
        text = ""
        with frags_p.open("r", encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                text += (rec.get("text") or rec.get("raw_text", "")) + "\n"
        if not text.strip():
            continue
        lang = prov.get("text_language", "eng")
        if lang in ("en", "english"):
            lang = "eng"
        elif lang == "zh":
            lang = "lzh"
        sigs[wid] = freq_signature(text, lex, lang)
        trads[wid] = prov.get("tradition") or "unknown"

    # 4. Fonction d'évaluation
    def evaluate(label, edges_used):
        D, idx = floyd_warshall(node_ids, edges_used)
        work_ids = [w for w in sigs if w in idx]
        pairs = []
        for i in range(len(work_ids)):
            for j in range(i + 1, len(work_ids)):
                a, b = work_ids[i], work_ids[j]
                d_g = D[idx[a]][idx[b]]
                if d_g == float("inf"):
                    continue
                d_lex = 1.0 - cosine_dict(sigs[a], sigs[b])
                pairs.append((a, b, d_g, d_lex))

        xs = [p[2] for p in pairs]
        ys = [p[3] for p in pairs]
        r = pearson(xs, ys)
        pv = perm_test(xs, ys)

        nw_ids = {w for w, t in trads.items() if t in EAST_TRADS}
        nw_pairs = [p for p in pairs if p[0] in nw_ids and p[1] in nw_ids]
        west_pairs = [p for p in pairs if p[0] not in nw_ids and p[1] not in nw_ids]
        inter_pairs = [p for p in pairs
                       if (p[0] in nw_ids) != (p[1] in nw_ids)]

        def stat(pp):
            if len(pp) < 3:
                return {"n": len(pp), "r": 0, "R2": 0, "p": 1.0}
            xs = [x[2] for x in pp]
            ys = [x[3] for x in pp]
            rr = pearson(xs, ys)
            return {"n": len(pp), "r": round(rr, 4),
                    "R2": round(rr * rr, 4),
                    "p": round(perm_test(xs, ys), 4)}

        return {
            "label": label,
            "n_edges_used": len(edges_used),
            "n_pairs_connected": len(pairs),
            "global": {"n": len(pairs), "r": round(r, 4),
                       "R2": round(r * r, 4), "p": round(pv, 4)},
            "west_west": stat(west_pairs),
            "inter": stat(inter_pairs),
            "nw_nw": stat(nw_pairs),
        }

    # 5. Évaluations
    results = {}
    print("\n=== Évaluations ===")
    print(f"{'Variante':<14}{'n_edges':>9}{'n_pairs':>9}"
          f"{'GLOBAL R²':>12}{'p':>8}{'WEST R²':>10}{'INTER R²':>10}{'NW R²':>9}")
    print("-" * 81)

    for label, edges_used in [
        ("ORIGINAL", edges_w),
        ("MSF_max", msf_max),
        ("MSF_min", msf_min),
    ]:
        r = evaluate(label, edges_used)
        results[label] = r
        print(f"{label:<14}{r['n_edges_used']:>9}{r['n_pairs_connected']:>9}"
              f"{r['global']['R2']:>12.4f}{r['global']['p']:>8.3f}"
              f"{r['west_west']['R2']:>10.4f}{r['inter']['R2']:>10.4f}"
              f"{r['nw_nw']['R2']:>9.4f}")

    rsf_results = []
    for i, rsf in enumerate(rsfs):
        r = evaluate(f"Random_{i+1}", rsf)
        rsf_results.append(r)
        print(f"{r['label']:<14}{r['n_edges_used']:>9}{r['n_pairs_connected']:>9}"
              f"{r['global']['R2']:>12.4f}{r['global']['p']:>8.3f}"
              f"{r['west_west']['R2']:>10.4f}{r['inter']['R2']:>10.4f}"
              f"{r['nw_nw']['R2']:>9.4f}")

    # Random aggregate
    rsf_global = [r["global"]["R2"] for r in rsf_results]
    rsf_west = [r["west_west"]["R2"] for r in rsf_results]
    rsf_inter = [r["inter"]["R2"] for r in rsf_results]
    rsf_nw = [r["nw_nw"]["R2"] for r in rsf_results]

    def agg(vals):
        m = sum(vals) / len(vals)
        v = sum((x - m) ** 2 for x in vals) / len(vals)
        return m, math.sqrt(v)

    g_m, g_s = agg(rsf_global)
    w_m, w_s = agg(rsf_west)
    i_m, i_s = agg(rsf_inter)
    n_m, n_s = agg(rsf_nw)

    print("-" * 81)
    print(f"{'Random mean':<14}{'':<9}{'':<9}"
          f"{g_m:>12.4f}{'':>8}{w_m:>10.4f}{i_m:>10.4f}{n_m:>9.4f}")
    print(f"{'Random sd':<14}{'':<9}{'':<9}"
          f"{g_s:>12.4f}{'':>8}{w_s:>10.4f}{i_s:>10.4f}{n_s:>9.4f}")

    # Diagnostic
    orig = results["ORIGINAL"]["west_west"]["R2"]
    msf_w = results["MSF_max"]["west_west"]["R2"]
    drop_west = (orig - msf_w) / orig if orig else 0
    print(f"\n=== DIAGNOSTIC ===")
    print(f"  WEST R² original: {orig:.4f}")
    print(f"  WEST R² MSF_max : {msf_w:.4f}")
    print(f"  Chute relative   : {drop_west*100:+.1f}%")

    if drop_west > 0.5:
        verdict = ("Cycles confirmés porteurs de signal — l'acyclisation "
                   "fait chuter R²(WEST) de plus de 50%.")
    elif drop_west > 0.2:
        verdict = "Cycles portent une part substantielle du signal (chute 20-50%)"
    elif drop_west > -0.2:
        verdict = ("Cycles ne portent pas le signal — R²(WEST) préservé après "
                   "acyclisation. La thèse §183 est en partie réfutée : ce "
                   "n'est pas la redondance cyclique qui porte le signal mais "
                   "les arêtes fortes individuellement.")
    else:
        verdict = "MSF AMÉLIORE le signal (suppression de bruit)"
    print(f"  → {verdict}")

    # Sauvegarde
    out = {
        "version": "v184_acyclic",
        "graph_input": "v8_§182",
        "weight_map": weight_map,
        "n_nodes": len(nodes),
        "n_edges_original": len(edges_w),
        "n_edges_msf_max": len(msf_max),
        "n_cycles_removed": len(edges_w) - len(msf_max),
        "results": {
            "ORIGINAL": results["ORIGINAL"],
            "MSF_max": results["MSF_max"],
            "MSF_min": results["MSF_min"],
            "random_runs": rsf_results,
            "random_aggregate": {
                "global_R2_mean": g_m, "global_R2_sd": g_s,
                "west_R2_mean": w_m, "west_R2_sd": w_s,
                "inter_R2_mean": i_m, "inter_R2_sd": i_s,
                "nw_R2_mean": n_m, "nw_R2_sd": n_s,
            },
        },
        "drop_relative_west": drop_west,
        "verdict": verdict,
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    out_path = RES_DIR / "nipada_v184_acyclic.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

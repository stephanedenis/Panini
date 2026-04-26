#!/usr/bin/env python3
"""
§151 — Signatures V14 denses via embeddings sémantiques multilingues.

Stratégie :
1. Définir des **prototypes** courts pour chaque atome V14 (3 phrases
   représentatives en français, car le modèle paraphrase-multilingual
   projette dans un espace partagé toutes langues).
2. Embeder prototypes ET fragments via paraphrase-multilingual-MiniLM-L12-v2
   (384-dim, pas de GPU requis, CPU acceptable pour 50+14*3 phrases).
3. Pour chaque fragment, signature dense = vecteur 14-dim de cosinus vs
   chaque atome (moyenne des cosinus des 3 prototypes par atome).
4. Agréger par œuvre (moyenne des signatures de fragments) et sauvegarder.

Cette signature ne dépend PAS du lexique de surface : un fragment qui
exprime DIFFÉRENCE en sanskrit, latin, ou allemand sera proche du
prototype DIFFÉRENCE en français via l'espace d'embedding aligné.

Output : research/nipada/falsification/nipada_v151_dense_signatures.json
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_DIR = ROOT / "research" / "nipada" / "falsification"
OUT = RES_DIR / "nipada_v151_dense_signatures.json"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Force CPU pour éviter les problèmes CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# 14 atomes V14
V14 = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS",
    "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE",
    "SYMÉTRIE", "ÉQUATION",
]

# Prototypes : 3 phrases courtes par atome, choisies pour évoquer le concept
# sans collisions lexicales (en évitant les marqueurs trop évidents).
PROTOTYPES: dict[str, list[str]] = {
    "ÊTRE": [
        "Quelque chose existe vraiment.",
        "Cela est, indépendamment de notre opinion.",
        "Il y a une réalité.",
    ],
    "DIFFÉRENCE": [
        "Ceci n'est pas cela.",
        "Les choses se distinguent les unes des autres.",
        "Une frontière sépare deux entités.",
    ],
    "RAPPORT": [
        "Il y a un lien entre A et B.",
        "Une chose dépend d'une autre.",
        "Cause et effet sont reliés.",
    ],
    "ORIENTATION": [
        "Cela va dans un sens et pas dans l'autre.",
        "Le mouvement a une direction.",
        "L'avant diffère de l'arrière.",
    ],
    "SUJET": [
        "Quelqu'un pense.",
        "L'individu fait l'expérience.",
        "Une personne agit.",
    ],
    "TEMPS": [
        "Cela arrive maintenant, puis cela passe.",
        "Hier précède aujourd'hui qui précède demain.",
        "L'instant s'écoule, la durée se mesure.",
    ],
    "MODALITÉ": [
        "Cela peut être ainsi ou autrement.",
        "Il est nécessaire que cela soit.",
        "Tous les cas, sans exception, vérifient cela.",
    ],
    "NOMBRE": [
        "Il y en a trois.",
        "On compte les éléments.",
        "La quantité augmente.",
    ],
    "ESPACE": [
        "Ici et là sont deux lieux différents.",
        "L'objet occupe une place.",
        "Le contenant a une étendue.",
    ],
    "OPÉRATION": [
        "On combine ceci et cela pour produire un résultat.",
        "L'action transforme la matière.",
        "Le procédé enchaîne les étapes.",
    ],
    "FONCTION": [
        "Cet organe sert à respirer.",
        "L'outil a un usage précis.",
        "Le rôle de chaque élément est défini.",
    ],
    "STRUCTURE": [
        "L'ensemble se compose de parties organisées.",
        "L'architecture du tout détermine ses propriétés.",
        "Les éléments sont disposés selon un ordre.",
    ],
    "SYMÉTRIE": [
        "À gauche comme à droite, c'est pareil.",
        "L'invariance par échange est respectée.",
        "Les deux côtés se reflètent.",
    ],
    "ÉQUATION": [
        "Un côté égale l'autre.",
        "L'identité se conserve dans la transformation.",
        "Ce qui est posé d'un côté se retrouve de l'autre.",
    ],
}


def _all_fragments() -> list[dict]:
    base = ROOT / "corpus" / "protoatheism"
    out: list[dict] = []
    for d in sorted(base.iterdir()):
        fp = d / "fragments.jsonl"
        if not fp.exists():
            continue
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def main() -> None:
    print("→ Chargement du modèle multilingue (CPU)…")
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer(MODEL_NAME, device="cpu")

    # 1. Embedder les prototypes (14 atomes × 3 phrases = 42 phrases)
    proto_phrases: list[str] = []
    proto_index: dict[str, list[int]] = {}
    for atom in V14:
        proto_index[atom] = []
        for phrase in PROTOTYPES[atom]:
            proto_index[atom].append(len(proto_phrases))
            proto_phrases.append(phrase)
    print(f"→ Embedding de {len(proto_phrases)} prototypes…")
    proto_emb = model.encode(proto_phrases, normalize_embeddings=True,
                              batch_size=16, show_progress_bar=False)

    # Centroïde par atome (moyenne L2-normalisée des 3 phrases)
    atom_centroids: dict[str, np.ndarray] = {}
    for atom in V14:
        vecs = proto_emb[proto_index[atom]]
        c = vecs.mean(axis=0)
        c = c / max(1e-12, np.linalg.norm(c))
        atom_centroids[atom] = c

    # 2. Embedder tous les fragments
    frags = _all_fragments()
    texts = [f["text"] for f in frags]
    print(f"→ Embedding de {len(texts)} fragments…")
    frag_emb = model.encode(texts, normalize_embeddings=True,
                             batch_size=16, show_progress_bar=False)

    # 3. Signature dense par fragment : cosinus vs chaque atome
    #    Comme tout est normalisé, cosinus = produit scalaire.
    frag_sigs: dict[str, dict[str, float]] = {}
    for f, vec in zip(frags, frag_emb):
        sig = {atom: float(np.dot(vec, atom_centroids[atom])) for atom in V14}
        frag_sigs[f["frag_id"]] = sig

    # 4. Agrégation par œuvre (moyenne des signatures de fragments)
    work_sigs: dict[str, dict[str, float]] = {}
    by_work: dict[str, list[str]] = {}
    for f in frags:
        by_work.setdefault(f["work_id"], []).append(f["frag_id"])
    for wid, fids in by_work.items():
        avg = {atom: 0.0 for atom in V14}
        for fid in fids:
            for atom in V14:
                avg[atom] += frag_sigs[fid][atom]
        for atom in V14:
            avg[atom] /= len(fids)
        work_sigs[wid] = avg

    # 5. Stats de calibration : moyenne, min, max des cosinus
    all_cos = [v for sig in frag_sigs.values() for v in sig.values()]
    summary = {
        "model": MODEL_NAME,
        "embedding_dim": int(frag_emb.shape[1]),
        "n_atoms": len(V14),
        "n_prototypes_per_atom": len(PROTOTYPES["ÊTRE"]),
        "n_fragments": len(frags),
        "n_works": len(work_sigs),
        "cos_min_global": round(float(min(all_cos)), 4),
        "cos_mean_global": round(float(sum(all_cos) / len(all_cos)), 4),
        "cos_max_global": round(float(max(all_cos)), 4),
    }

    # Pour chaque atome, ses fragments les plus saillants (top-3) — sanity check
    top_per_atom: dict[str, list] = {}
    for atom in V14:
        ranked = sorted(frag_sigs.items(), key=lambda kv: kv[1][atom], reverse=True)
        top_per_atom[atom] = [
            {"frag_id": fid, "cos": round(s[atom], 4)} for fid, s in ranked[:3]
        ]

    payload = {
        "version": "v151",
        "step": "§151 — signatures V14 denses (embeddings multilingues)",
        "summary": summary,
        "prototypes": PROTOTYPES,
        "fragment_signatures": {fid: {a: round(v, 4) for a, v in s.items()}
                                 for fid, s in frag_sigs.items()},
        "work_signatures_aggregated": {wid: {a: round(v, 4) for a, v in s.items()}
                                         for wid, s in work_sigs.items()},
        "top_fragments_per_atom": top_per_atom,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ §151 — signatures denses écrites : {OUT}")
    print(f"  modèle = {MODEL_NAME} ({summary['embedding_dim']}-dim)")
    print(f"  fragments = {summary['n_fragments']}, œuvres = {summary['n_works']}")
    print(f"  cosinus global min/moy/max = {summary['cos_min_global']} / "
          f"{summary['cos_mean_global']} / {summary['cos_max_global']}")
    print()
    print("  Sanity check — top fragment par atome (saillance attendue) :")
    for atom in V14:
        top = top_per_atom[atom][0]
        print(f"    {atom:14s} → {top['frag_id']:15s}  cos={top['cos']}")


if __name__ == "__main__":
    main()

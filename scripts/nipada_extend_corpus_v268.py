#!/usr/bin/env python3
"""
§268 — Extension du corpus vers les traditions sous-représentées.

Stratégie :
  Phase A : Intégrer les 16 nœuds du graphe v18p qui ont déjà
            une signature V14 valide (non dégénérée) mais qui
            n'ont pas encore été inclus dans le corpus.

  Phase B : Proposer (et documenter) les nouvelles traditions
            à ingérer en §269 (Sufi, confucéen ritual, Égypte
            ancienne, etc.) — ces textes nécessiteraient un
            graphe v19p.

Résultat : nipada/corpus/signed_corpus_v268_extension.json
           Contient UNIQUEMENT les 16 nouveaux textes (les
           corpus v263+v264 restent des fichiers séparés).
           La fusion s'effectue dans le script de revalidation.
"""

import json
import pathlib
import datetime

# ── Chemins ────────────────────────────────────────────────────────────────────
BASE        = pathlib.Path(__file__).resolve().parent.parent.parent / "Panini-Research"
CORPUS_DIR  = BASE / "nipada" / "corpus"
FALSI_DIR   = BASE / "nipada" / "falsification"
GRAPH_PATH  = FALSI_DIR / "nipada_v266_graph_v18p.json"
C263_PATH   = CORPUS_DIR / "signed_corpus_v263_clean.json"
C264_PATH   = CORPUS_DIR / "signed_corpus_v264_prophetic.json"
OUT_PATH    = CORPUS_DIR / "signed_corpus_v268_extension.json"

# ── Candidats Phase A (16 textes avec signature V14 valide dans le graphe) ────
# Sélection motivée :
#   - han_feizi, mozi, wang_chong, carvaka : traditions sous-repr. (légiste,
#     mohiste, rationaliste chinois, matérialiste indien)
#   - dhammapada, carus_gospel_buddha   : bouddhiste canon + moderniste
#   - bhagavad_gita_arnold_en           : hinduisme smriti (sous-repr.)
#   - hobbes, holbach, hume_dialogues   : empirisme/matérialisme occidental
#   - schopenhauer, feuerbach×2         : critique religion (XIXe)
#   - nietzsche×3                       : philosophie critique (XIXe)
# NOTE : confucius_analects_en exclus — nœud isolé (0 voisins dans le graphe)

PHASE_A_CANDIDATES = [
    # Traditions sous-représentées (cœur §268)
    "han_feizi_selections",         # chinese_legalist
    "mozi_selections",              # chinese_mohist
    "wang_chong_lunheng",           # chinese_rationalist (matérialisme Han)
    "carvaka_fragments",            # indian_materialist (sous-repr.)
    "dhammapada_muller_en",         # buddhism_theravada (texte canonique)
    "carus_gospel_buddha_en",       # buddhism_modernist
    "bhagavad_gita_arnold_en",      # hinduism_smriti (sous-repr.)
    # Philosophie occidentale (connexions: spinoza, democritus, volney, hume_enquiry)
    "hobbes_leviathan_complete",
    "holbach_systeme",
    "hume_dialogues",
    "schopenhauer_pessimism",
    "feuerbach_wesen",
    "feuerbach_christianity_en",
    "nietzsche_antichrist",
    "nietzsche_genealogy",
    "nietzsche_twilight",
]

V14_ATOMS = [
    "ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS",
    "MODALITÉ","NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE",
    "SYMÉTRIE","ÉQUATION"
]


def load_graph(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_corpus(*paths: pathlib.Path) -> set:
    ids = set()
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        key = "signed" if "signed" in data else list(data.keys())[0]
        for entry in data[key]:
            ids.add(entry["graph_node_id"])
    return ids


def is_degenerate(sig: dict) -> bool:
    """Signature dégénérée si une seule dimension vaut ~1.0 (artefact V7/V8)."""
    vals = list(sig.values())
    return max(vals) > 0.95


def extract_entry(node_id: str, meta: dict) -> dict | None:
    """Créer une entrée corpus à partir des métadonnées du graphe."""
    sig = meta.get("v14_signature")
    if sig is None:
        return None
    if is_degenerate(sig):
        return None
    # Normaliser la signature (s'assurer que tous les 14 atomes sont présents)
    sig_norm = {a: float(sig.get(a, 0.0)) for a in V14_ATOMS}
    total = sum(sig_norm.values())
    if total < 1e-9:
        return None
    sig_norm = {a: v / total for a, v in sig_norm.items()}

    entry = {
        "local_id":        node_id,
        "graph_node_id":   node_id,
        "catalog":         meta.get("tradition", meta.get("tradition_label", "?")),
        "tradition_label": meta.get("tradition_label", meta.get("tradition", "?")),
        "lang":            meta.get("language_original", meta.get("lang", "?")),
        "n_chars":         meta.get("signed_n_chars", 0),
        "n_words":         0,
        "v14_signature":   sig_norm,
        "v14_top3":        sorted(sig_norm, key=lambda k: -sig_norm[k])[:3],
        "source":          "graph_v18p_v208",
        "ingestion_status": meta.get("ingestion_status", "signed_v208"),
        "added_in":        "v268_§268",
    }
    # Métadonnées optionnelles
    for k in ("author", "year", "title_en", "title_original", "tags"):
        if k in meta:
            entry[k] = meta[k]
    return entry


def main():
    print("=" * 60)
    print("§268 — Extension corpus vers traditions sous-représentées")
    print("=" * 60)

    graph = load_graph(GRAPH_PATH)
    nodes = graph["nodes"]

    in_corpus = load_corpus(C263_PATH, C264_PATH)
    print(f"Corpus actuel  : {len(in_corpus)} textes (v263 + v264)")

    new_entries = []
    skipped = []

    for nid in PHASE_A_CANDIDATES:
        if nid in in_corpus:
            skipped.append((nid, "already_in_corpus"))
            continue
        meta = nodes.get(nid)
        if meta is None:
            skipped.append((nid, "not_in_graph"))
            continue
        entry = extract_entry(nid, meta)
        if entry is None:
            skipped.append((nid, "no_valid_signature"))
            continue
        new_entries.append(entry)
        sig = entry["v14_signature"]
        top3 = entry["v14_top3"]
        print(f"  ✓ {nid:<42} top3={top3}")

    print()
    if skipped:
        print("Ignorés :")
        for nid, reason in skipped:
            print(f"  ✗ {nid:<42} ({reason})")

    print(f"\nNouveaux textes Phase A : {len(new_entries)}")

    # Construire le fichier de sortie
    output = {
        "version":     "v268_extension",
        "description": (
            "Extension §268 — 16 textes issus des nœuds du graphe v18p "
            "déjà signés en V14 (ingestion_status=signed_v208) mais absents "
            "du corpus v263+v264. Focus : traditions sous-représentées "
            "(légiste/mohiste chinois, matérialiste indien, bouddhiste canonique, "
            "hinduisme smriti) + philosophie occidentale connexe."
        ),
        "generated":   datetime.datetime.utcnow().isoformat() + "Z",
        "graph_version": "v18p",
        "phase": "A",
        "phase_A_note": (
            "Textes extraits directement du graphe (pas de nouveau fetch). "
            "Phase B prévue en §269 : ingestion Sufi (Rumi Masnavi, PG10097), "
            "confucéen rituel (Liji via PG27484), Égypte ancienne (Maximes de "
            "Ptahhotep, sacred-texts.com/egy), avec mise à jour graphe v19p."
        ),
        "n_texts":     len(new_entries),
        "traditions_added": sorted(set(e["catalog"] for e in new_entries)),
        "signed":      new_entries,
    }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nSauvegardé → {OUT_PATH}")
    print(f"Corpus total après fusion : {len(in_corpus) + len(new_entries)} textes")


if __name__ == "__main__":
    main()

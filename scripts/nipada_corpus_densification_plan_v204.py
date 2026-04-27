#!/usr/bin/env python3
"""
§204 — Plan de densification corpus NIPADA (cible 70/cellule culture×époque).

Lit le graphe v9 (89 nodes, dont 50 œuvres signées + 39 nœuds auteurs/UNK),
consolide les 32 micro-traditions en macro-cultures, projette époques
canoniques, calcule la matrice cible 70/cellule, identifie les gaps, et
émet une roadmap d'acquisition priorisée par sources libres.

Sortie : research/nipada/falsification/nipada_v204_densification_plan.json
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / "research/nipada/falsification/nipada_v189_graph_v9.json"
OUT = REPO / "research/nipada/falsification/nipada_v204_densification_plan.json"

# ──────────────────────────────────────────────────────────────────────
# Macro-culture mapping (32 micro → 8 macro)
# ──────────────────────────────────────────────────────────────────────
MACRO = {
    # GRECO_LATIN — antiquité méditerranéenne
    "GRECO_LAT_MATERIAL": "GRECO_LATIN",
    "ANCIENT_EPICUREAN": "GRECO_LATIN",
    "SCEPT": "GRECO_LATIN",  # sceptiques antiques

    # WESTERN_RATIONAL — Europe rationaliste 1500-1900
    "EUR_DEIST_ANTICLERICAL": "WESTERN_RATIONAL",
    "EUR_RATIONALIST_CRITIC": "WESTERN_RATIONAL",
    "EUR_RATIONALIST_NATURAL_RELIGION": "WESTERN_RATIONAL",
    "EUR_SCEPTICAL_EMPIRICIST": "WESTERN_RATIONAL",
    "EUR_THEOL_CRITIC": "WESTERN_RATIONAL",
    "MODERN_WESTERN": "WESTERN_RATIONAL",

    # WESTERN_RADICAL — radicaux/matérialistes/anti-religion 1700-1900
    "EUR_MATERIALIST_ATHEIST": "WESTERN_RADICAL",
    "EUR_MATERIALIST_HISTORICAL": "WESTERN_RADICAL",
    "EUR_ANTI_CHRISTIAN": "WESTERN_RADICAL",
    "EUR_PESSIMIST_CRITIC": "WESTERN_RADICAL",
    "AMERICAN_FREETHINKER": "WESTERN_RADICAL",

    # INDIAN — corpus indien (orthodoxe et hétérodoxe)
    "HINDUISM": "INDIAN",
    "HINDUISM_ADVAITA": "INDIAN",
    "INDIAN_MATERIAL": "INDIAN",  # Cārvāka
    "INDIAN_HETERODOX": "INDIAN",

    # BUDDHIST — pali, sanskrit, tibétain, sino
    "BUDDHISM": "BUDDHIST",
    "BUDDHISM_MADHYAMAKA": "BUDDHIST",
    "BUDDHISM_MODERNIST": "BUDDHIST",

    # CHINESE — confucéen, taoïste, légiste, critique
    "CHINESE_CLASSICS": "CHINESE",
    "DAOISM": "CHINESE",
    "CHINESE_LEGALIST": "CHINESE",
    "CHINESE_RATIONALIST": "CHINESE",
    "CHINESE_MATERIAL": "CHINESE",
    "CHINESE_CRITIC": "CHINESE",

    # ISLAMIC — kalam, falsafa, soufisme rationnel
    "ISLAMIC": "ISLAMIC",
    "ISLAMIC_KALAM": "ISLAMIC",
    "ISLAMIC_RATIONALIST": "ISLAMIC",

    # ORIENTALIST_TRANSLATION — traducteurs 19C (canal documentaire)
    "ORIENTALIST_19C": "ORIENTALIST_TRANSLATION",

    # UNK = nœuds auteurs sans œuvre signée (à reclassifier ou retirer)
    "UNK": "UNK",
}

# ──────────────────────────────────────────────────────────────────────
# Époques canoniques (frontières chronologiques)
# ──────────────────────────────────────────────────────────────────────
EPOCHS = [
    ("pre_axial",      None,  -800),   # avant Bouddha/Confucius/Présocratiques
    ("axial",          -800,  -200),   # âge axial Jaspers
    ("late_antique",   -200,   500),   # romain tardif, hellénistique tardif
    ("medieval",        500,  1500),   # médiéval (incl. islam classique, scolastique)
    ("early_modern",   1500,  1789),   # Renaissance + Lumières
    ("modern",         1789,  1914),   # XIXe siècle
    ("contemporary",   1914,  None),   # XXe-XXIe
]

def epoch_of(year: int | None) -> str:
    if year is None:
        return "unknown"
    for name, lo, hi in EPOCHS:
        lo_ok = (lo is None) or (year >= lo)
        hi_ok = (hi is None) or (year < hi)
        if lo_ok and hi_ok:
            return name
    return "unknown"

# ──────────────────────────────────────────────────────────────────────
# Catalogue de sources libres par macro-culture
# ──────────────────────────────────────────────────────────────────────
SOURCES = {
    "GRECO_LATIN": [
        "Perseus Digital Library (perseus.tufts.edu) — grec/latin avec traductions EN",
        "Loeb Classical Library (domaine public partiel)",
        "Project Gutenberg — traductions historiques",
        "Internet Archive — éditions critiques scannées",
    ],
    "WESTERN_RATIONAL": [
        "Project Gutenberg (gutenberg.org) — œuvres complètes 1500-1923",
        "Internet Archive — éditions originales",
        "Wikisource FR/EN/DE — textes vérifiés",
        "BnF Gallica (gallica.bnf.fr) — sources françaises",
        "Online Library of Liberty (oll.libertyfund.org)",
    ],
    "WESTERN_RADICAL": [
        "Marxists Internet Archive (marxists.org) — Marx/Engels/Feuerbach",
        "Project Gutenberg — Nietzsche, Schopenhauer, Holbach",
        "Wikisource — d'Holbach, Diderot, Helvétius",
        "Internet Archive — pamphlets libertins",
    ],
    "INDIAN": [
        "GRETIL (gretil.sub.uni-goettingen.de) — sanskrit numérisé",
        "SARIT (sarit.indology.info) — Indian texts in TEI",
        "Wikisource Sanskrit",
        "sacred-texts.com — traductions historiques (Müller, Burnouf)",
        "Digital Corpus of Sanskrit (DCS)",
    ],
    "BUDDHIST": [
        "SuttaCentral (suttacentral.net) — Pali Canon multilingue",
        "Digital Pali Reader",
        "84000.co — Kangyour tibétain traduit",
        "CBETA (cbeta.org) — Canon bouddhique chinois",
        "sacred-texts.com — Dhammapada, Lotus Sutra (Müller, Kern)",
    ],
    "CHINESE": [
        "Chinese Text Project (ctext.org) — corpus classique complet",
        "Wikisource ZH",
        "Donald Sturgeon's Digital Sinology",
        "Daoist Canon (Tao Tsang) numérisé",
        "sacred-texts.com — Legge translations (Confucius, Lao-tseu, Zhuangzi)",
    ],
    "ISLAMIC": [
        "al-mostafa.com — kalam et falsafa arabes",
        "shamela.ws — bibliothèque islamique numérique",
        "Wikisource AR",
        "Internet Archive — éditions arabes critiques",
        "sacred-texts.com — Khayyam (FitzGerald), Coran (Rodwell, Sale)",
    ],
    "ORIENTALIST_TRANSLATION": [
        "Sacred Books of the East (Müller ed.) — 50 volumes",
        "Project Gutenberg — Burnouf, Legge, Arnold, FitzGerald",
        "Internet Archive — Société Asiatique 19e",
        "sacred-texts.com — corpus orientaliste consolidé",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Cibles par cellule (ajustées selon réalité historique)
# ──────────────────────────────────────────────────────────────────────
# Cible nominale 70, mais cap réaliste pour cellules historiquement maigres.
# Justification : on ne peut pas avoir 70 œuvres "Indian pre_axial" car le
# corpus védique signé pré-800 BCE est minimal.
CAP_REALISTE = {
    ("GRECO_LATIN", "pre_axial"): 10,         # Hésiode, Homère, présocratiques fragmentaires
    ("GRECO_LATIN", "axial"): 70,             # corpus dense
    ("GRECO_LATIN", "late_antique"): 70,
    ("GRECO_LATIN", "medieval"): 0,           # transition latin médiéval
    ("GRECO_LATIN", "early_modern"): 0,
    ("GRECO_LATIN", "modern"): 0,
    ("GRECO_LATIN", "contemporary"): 0,

    ("INDIAN", "pre_axial"): 20,              # Rig-Véda + premiers Upanishads
    ("INDIAN", "axial"): 70,                  # Upanishads, Bhagavad-Gītā, Cārvāka frag.
    ("INDIAN", "late_antique"): 70,           # Mahābhārata, Manusmṛti, Yoga-sūtras
    ("INDIAN", "medieval"): 70,               # Śaṅkara, Rāmānuja, tantras
    ("INDIAN", "early_modern"): 30,
    ("INDIAN", "modern"): 30,
    ("INDIAN", "contemporary"): 20,

    ("BUDDHIST", "pre_axial"): 0,
    ("BUDDHIST", "axial"): 70,                # Pali Canon (Sutta, Vinaya)
    ("BUDDHIST", "late_antique"): 70,         # Mahāyāna, Nāgārjuna, Asaṅga
    ("BUDDHIST", "medieval"): 70,             # tibétain, Chan, Pure Land
    ("BUDDHIST", "early_modern"): 30,
    ("BUDDHIST", "modern"): 30,
    ("BUDDHIST", "contemporary"): 20,

    ("CHINESE", "pre_axial"): 10,             # Yi Jing strates anciennes
    ("CHINESE", "axial"): 70,                 # Confucius, Mencius, Laozi, Zhuangzi, Mozi
    ("CHINESE", "late_antique"): 70,          # Han, Wang Chong, Liezi
    ("CHINESE", "medieval"): 70,              # néo-confucianisme, Chan, Tao Tsang
    ("CHINESE", "early_modern"): 50,
    ("CHINESE", "modern"): 30,
    ("CHINESE", "contemporary"): 20,

    ("ISLAMIC", "pre_axial"): 0,
    ("ISLAMIC", "axial"): 0,
    ("ISLAMIC", "late_antique"): 0,           # avant Hégire
    ("ISLAMIC", "medieval"): 70,              # kalam classique, falsafa, Mu'tazilites
    ("ISLAMIC", "early_modern"): 50,
    ("ISLAMIC", "modern"): 30,
    ("ISLAMIC", "contemporary"): 20,

    ("WESTERN_RATIONAL", "pre_axial"): 0,
    ("WESTERN_RATIONAL", "axial"): 0,
    ("WESTERN_RATIONAL", "late_antique"): 0,
    ("WESTERN_RATIONAL", "medieval"): 30,     # Abélard, scolastique critique
    ("WESTERN_RATIONAL", "early_modern"): 70, # Spinoza, Descartes, Hume, Hobbes, Bayle
    ("WESTERN_RATIONAL", "modern"): 70,       # Kant, Hegel, Mill, Comte
    ("WESTERN_RATIONAL", "contemporary"): 30,

    ("WESTERN_RADICAL", "pre_axial"): 0,
    ("WESTERN_RADICAL", "axial"): 0,
    ("WESTERN_RADICAL", "late_antique"): 0,
    ("WESTERN_RADICAL", "medieval"): 0,
    ("WESTERN_RADICAL", "early_modern"): 30,  # libertins érudits, La Mettrie, Holbach
    ("WESTERN_RADICAL", "modern"): 70,        # Feuerbach, Marx, Nietzsche, Freud
    ("WESTERN_RADICAL", "contemporary"): 30,

    ("ORIENTALIST_TRANSLATION", "pre_axial"): 0,
    ("ORIENTALIST_TRANSLATION", "axial"): 0,
    ("ORIENTALIST_TRANSLATION", "late_antique"): 0,
    ("ORIENTALIST_TRANSLATION", "medieval"): 0,
    ("ORIENTALIST_TRANSLATION", "early_modern"): 0,
    ("ORIENTALIST_TRANSLATION", "modern"): 70,        # Müller, Legge, Burnouf, Arnold
    ("ORIENTALIST_TRANSLATION", "contemporary"): 30,
}

# ──────────────────────────────────────────────────────────────────────
def main() -> int:
    g = json.loads(GRAPH.read_text())
    nodes = g["nodes"]

    # Inventaire actuel par (macro, epoch)
    actual = defaultdict(list)
    raw_by_macro = defaultdict(int)
    for nid, attrs in nodes.items():
        micro = attrs.get("tradition_label", "UNK")
        macro = MACRO.get(micro, "UNK")
        ep = epoch_of(attrs.get("year"))
        actual[(macro, ep)].append({
            "id": nid,
            "micro_tradition": micro,
            "author": attrs.get("author"),
            "year": attrs.get("year"),
            "lang": attrs.get("language_original"),
        })
        raw_by_macro[macro] += 1

    # Matrice cellule × cible × actuel × gap
    macros = sorted({m for m in MACRO.values() if m != "UNK"})
    epochs = [e[0] for e in EPOCHS] + ["unknown"]

    matrix = []
    total_target = 0
    total_actual = 0
    total_gap = 0
    for macro in macros:
        for ep in epochs:
            target = CAP_REALISTE.get((macro, ep), 0)
            current = len(actual.get((macro, ep), []))
            gap = max(0, target - current)
            if target > 0 or current > 0:
                matrix.append({
                    "macro_culture": macro,
                    "epoch": ep,
                    "target": target,
                    "actual_signed": current,
                    "gap": gap,
                    "fill_pct": round(100 * current / target, 1) if target else None,
                    "examples_present": [n["id"] for n in actual.get((macro, ep), [])][:5],
                })
                total_target += target
                total_actual += current
                total_gap += gap

    # Priorisation : cellules à fort gap ET fort impact attendu (NW + INTER)
    HIGH_PRIORITY = {"INDIAN", "BUDDHIST", "CHINESE", "ISLAMIC", "ORIENTALIST_TRANSLATION"}
    priority_queue = sorted(
        [m for m in matrix if m["gap"] > 0],
        key=lambda x: (
            0 if x["macro_culture"] in HIGH_PRIORITY else 1,
            -x["gap"],
        ),
    )

    plan = {
        "version": "v204_densification_plan",
        "generated": "2026-04-27",
        "objective": "70 œuvres / cellule culture×époque (cap ajusté pour cellules historiquement maigres)",
        "macro_cultures": macros,
        "epochs": [e[0] for e in EPOCHS],
        "current_corpus": {
            "total_nodes": len(nodes),
            "by_macro": dict(raw_by_macro),
        },
        "matrix": matrix,
        "totals": {
            "target": total_target,
            "actual_signed": total_actual,
            "gap": total_gap,
            "fill_pct_global": round(100 * total_actual / total_target, 1) if total_target else 0,
        },
        "priority_queue_top20": priority_queue[:20],
        "sources_by_macro": SOURCES,
        "next_steps": [
            "§205 — Construire catalogues œuvre-par-œuvre pour les 5 cellules prioritaires",
            "§206 — Pipeline ingestion automatisé : scrape → texte brut → V14 signature → graph node",
            "§207 — Reprise validation V_OPT v2 sur graph densifié (cross-val redevient possible)",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(plan, indent=2, ensure_ascii=False))

    # Affichage console
    print(f"=== §204 Plan densification corpus ===")
    print(f"Corpus actuel : {len(nodes)} nœuds dont {total_actual} dans cellules cible")
    print(f"Cible totale  : {total_target}")
    print(f"Gap total     : {total_gap} œuvres à acquérir ({100*total_actual/total_target:.1f}% rempli)")
    print()
    print(f"{'macro':<26} {'epoch':<14} {'tgt':>4} {'cur':>4} {'gap':>4} {'%':>5}")
    print("-" * 70)
    for m in matrix:
        pct = m["fill_pct"] if m["fill_pct"] is not None else "—"
        pct_s = f"{pct}%" if isinstance(pct, float) else str(pct)
        print(f"{m['macro_culture']:<26} {m['epoch']:<14} "
              f"{m['target']:>4} {m['actual_signed']:>4} {m['gap']:>4} {pct_s:>5}")
    print()
    print(f"Top-10 priorités :")
    for i, p in enumerate(priority_queue[:10], 1):
        print(f"  {i:2d}. {p['macro_culture']:<26} {p['epoch']:<14} gap={p['gap']:>3}")
    print()
    print(f"Plan écrit dans {OUT.relative_to(REPO)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

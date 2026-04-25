#!/usr/bin/env python3
"""
§105 — Clarification taxonomique : énoncés vs entités
======================================================

§101–§104 ont introduit deux taxonomies orthogonales sans les nommer
explicitement :

  T_E (énoncés) — classes de speech-acts (description, narration,
                  définition, proclamation, question, ordre, introspection)
                  — c'est ce que classifie le moteur §97/§100 à 97.6 %

  T_O (entités) — classes d'objets référencés (auteur, lieu, époque,
                  événement, objet céleste, lien généalogique, causalité)
                  — c'est ce que peuple l'encyclopédie §101/§103/§104

Un énoncé **réfère à** des entités via des « slots » (sujet énonciateur,
sujet référent, lieu d'énonciation, lieu référent, époque, événement
référent, etc.). Les deux taxonomies utilisent la même algèbre de primes
mais à des niveaux différents : signifiant vs signifié.

Ce script :
  1. Catalogue formellement T_E (7 types V7) et T_O (10 classes d'entités).
  2. Définit les slots de référence énoncé→entité.
  3. Identifie les **ambiguïtés référentielles** (molécules apparaissant
     dans les deux taxonomies — sont-elles bug ou feature ?).
  4. Vérifie la cohérence de tous les seeds existants.

Sortie :
  - research/nipada/taxonomies/v105_enonces.json
  - research/nipada/taxonomies/v105_entites.json
  - research/nipada/taxonomies/v105_slots.json
  - research/nipada/taxonomies/v105_ambiguites.json
"""

from __future__ import annotations

import json
from functools import reduce
from operator import mul
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"
OUT_DIR = REPO_ROOT / "research" / "nipada" / "taxonomies"

PRIMES = {"ÊTRE": 2, "DIFFÉRENCE": 3, "RAPPORT": 5, "ORIENTATION": 7,
          "SUJET": 11, "TEMPS": 13, "MODALITÉ": 17}


# ══════════════════════════════════════════════════════════════════════════════
# T_E — TAXONOMIE DES ÉNONCÉS (7 classes, niveau du speech-act)
# ══════════════════════════════════════════════════════════════════════════════
#
# Un type d'énoncé est une CLASSE D'ÉQUIVALENCE sur des molécules V6, étendue
# (ou non) modalement par MODALITÉ(17). Ce n'est pas un entier unique mais un
# *ensemble* — la plasticité morphologique d'une intention discursive.
#
# Source : scripts/nipada_v7_contextualisation.py (§102)

TAXONOMIE_ENONCES: dict[str, dict] = {
    "description": {
        "level": "speech_act",
        "modale": False,
        "molecules_v6": [30],                # 2·3·5
        "modale_extension": None,
        "primes_typiques": ["ÊTRE", "DIFFÉRENCE", "RAPPORT"],
        "primes_absents": ["ORIENTATION", "SUJET", "TEMPS", "MODALITÉ"],
        "exemple": "« La pierre est dure. »",
        "rationale": "Pose une qualité sans la situer ni la moduler.",
    },
    "narration": {
        "level": "speech_act",
        "modale": False,
        "molecules_v6": [13, 78, 273],       # 13 ; 2·3·13 ; 3·7·13
        "modale_extension": None,
        "primes_typiques": ["TEMPS"],
        "primes_absents": ["MODALITÉ"],
        "exemple": "« Hier P advint, puis Q. »",
        "rationale": "Séquentialité temporelle pure.",
    },
    "définition": {
        "level": "speech_act",
        "modale": True,
        "modal_kind": "DEVOIR",
        "modal_kind_id": 34,
        "molecules_v6": [385, 66],           # 5·7·11 ; 2·3·11
        "modale_extension": [385 * 17, 66 * 17],
        "primes_typiques": ["RAPPORT", "ORIENTATION", "SUJET"],
        "primes_absents": [],
        "exemple": "« Une pierre EST par essence dure. »",
        "rationale": "Pose une nécessité essentielle (DEVOIR ontique).",
    },
    "proclamation": {
        "level": "speech_act",
        "modale": True,
        "modal_kind": "ORDONNER",
        "modal_kind_id": 374,
        "molecules_v6": [33, 55, 77],        # 3·11 ; 5·11 ; 7·11
        "modale_extension": [33 * 17, 55 * 17, 77 * 17],
        "primes_typiques": ["SUJET"],
        "primes_absents": [],
        "exemple": "« Je proclame que P. »",
        "rationale": "L'autorité du SUJET rend P normatif.",
    },
    "question": {
        "level": "speech_act",
        "modale": True,
        "modal_kind": "DOUTE",
        "modal_kind_id": 51,
        "molecules_v6": [143, 165, 11],      # 11·13 ; 3·5·11 ; SUJET seul
        "modale_extension": [143 * 17, 165 * 17, 11 * 17],
        "primes_typiques": ["SUJET"],
        "primes_absents": [],
        "exemple": "« Est-ce que P ? »",
        "rationale": "DOUTE entre P et ¬P.",
    },
    "ordre": {
        "level": "speech_act",
        "modale": True,
        "modal_kind": "ORDONNER",
        "modal_kind_id": 374,
        "molecules_v6": [154, 231],          # 2·7·11 ; 3·7·11
        "modale_extension": [154 * 17, 231 * 17],
        "primes_typiques": ["ORIENTATION", "SUJET"],
        "primes_absents": [],
        "exemple": "« Fais P ! »",
        "rationale": "Déontique direct.",
    },
    "introspection": {
        "level": "speech_act",
        "modale": True,
        "modal_kind": "VOULOIR",
        "modal_kind_id": 187,
        "molecules_v6": [2310, 22, 26],      # 2·3·5·7·11 ; 2·11 ; 2·13
        "modale_extension": [2310 * 17, 22 * 17, 26 * 17],
        "primes_typiques": ["SUJET"],
        "primes_absents": [],
        "exemple": "« Je crois que P. »",
        "rationale": "Modalité doxastique du SUJET.",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# T_O — TAXONOMIE DES ENTITÉS (10 classes, niveau du référent)
# ══════════════════════════════════════════════════════════════════════════════
#
# Une entité est un INSTANCE D'UNE CLASSE caractérisée par UN entier unique
# (sa molécule signature). L'entité est ce dont parle un énoncé. Sources
# : §101 (auteur, lieu, époque), §103 (lien, causalité, événement),
#   §104 (objet céleste).

TAXONOMIE_ENTITES: dict[str, dict] = {
    "AUTEUR": {
        "level": "referent",
        "kind": "sujet_situe",
        "subkind": "humain",
        "nipada_type": 2002,
        "atoms": [2, 7, 11, 13],
        "primes": ["ÊTRE", "ORIENTATION", "SUJET", "TEMPS"],
        "schema_ref": "§101.auteurs_seed",
        "instances_seed": 12,
        "rationale": "Sujet humain individué, situé dans l'espace et le temps.",
    },
    "OBJET_CELESTE": {
        "level": "referent",
        "kind": "sujet_situe",
        "subkind": "celeste",
        "nipada_type": 2002,
        "atoms": [2, 7, 11, 13],
        "primes": ["ÊTRE", "ORIENTATION", "SUJET", "TEMPS"],
        "schema_ref": "§104.objets_celestes",
        "instances_seed": 7,
        "rationale": "Sujet astronomique persistant (étoile, trou noir, fond cosmologique). "
                     "Partage la signature 2002 avec AUTEUR : tous deux sont sujets situés. "
                     "Distinction ontologique humain/céleste portée par `subkind`, pas "
                     "par la signature nipada.",
    },
    "LIEU": {
        "level": "referent",
        "kind": "coordonnee_spatiale",
        "subkind": None,
        "nipada_type": 14,
        "atoms": [2, 7],
        "primes": ["ÊTRE", "ORIENTATION"],
        "schema_ref": "§101.lieux_zones",
        "instances_seed": 18,
        "rationale": "LOCALISATION = être × orientation. "
                     "Sans temps, sans sujet : un lieu pur.",
    },
    "EPOQUE": {
        "level": "referent",
        "kind": "intervalle_temporel",
        "subkind": None,
        "nipada_type": 65,
        "atoms": [5, 13],
        "primes": ["RAPPORT", "TEMPS"],
        "schema_ref": "§101.temps_epoques",
        "instances_seed": 7,
        "rationale": "DURÉE = rapport × temps. Période historique sans lieu ni sujet.",
    },
    "LIEN_GÉNÉALOGIQUE": {
        "level": "referent",
        "kind": "relation_dirigee",
        "subkind": "sujet_a_sujet",
        "nipada_type": 55,
        "atoms": [5, 11],
        "primes": ["RAPPORT", "SUJET"],
        "schema_ref": "§103.auteurs_genealogie",
        "instances_seed": 23,    # nb total de liens dans 6 généalogies
        "rationale": "Lien dirigé entre deux sujets (parent → enfant, maître → disciple).",
    },
    "CAUSALITÉ": {
        "level": "referent",
        "kind": "relation_dirigee",
        "subkind": "evenement_a_evenement",
        "nipada_type": 195,
        "atoms": [3, 5, 13],
        "primes": ["DIFFÉRENCE", "RAPPORT", "TEMPS"],
        "schema_ref": "§103.molecules_causales",
        "instances_seed": 0,     # pas matérialisé comme entité, intégré dans Evenement.causes/effets
        "rationale": "DIFFÉRENCE × RAPPORT × TEMPS — cause ≠ effet, en rapport, ordonnés. "
                     "Existe comme structure du graphe causal, pas comme tuple matérialisé.",
    },
    "ÉVÉNEMENT_SANS_SUJET": {
        "level": "referent",
        "kind": "evenement",
        "subkind": "anonyme",
        "nipada_type": 2730,
        "atoms": [2, 3, 5, 7, 13],
        "primes": ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "TEMPS"],
        "schema_ref": "§103.evenements_seed + §104.evenements_astronomiques",
        "instances_seed": 2,     # big_bang, recombinaison_cmb (§104)
        "rationale": "Événement cosmique ou naturel sans agent identifié.",
    },
    "ÉVÉNEMENT_INDIVIDUEL": {
        "level": "referent",
        "kind": "evenement",
        "subkind": "avec_sujet",
        "nipada_type": 30030,
        "atoms": [2, 3, 5, 7, 11, 13],
        "primes": ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS"],
        "schema_ref": "§103.evenements_seed + §104.evenements_astronomiques",
        "instances_seed": 12,    # 8 (§103) + 4 (§104, sn_1987a×3 + gw150914)
        "rationale": "ω_V6 — événement avec sujet, instancie tous les primes V6. "
                     "AMBIGUÏTÉ : partage 30030 avec narration.molecules_v6[2310]·13. "
                     "Voir AMBIGUITES_REFERENTIELLES.",
    },
    "ÉVÉNEMENT_MODAL": {
        "level": "referent",
        "kind": "evenement",
        "subkind": "modal",
        "nipada_type": 510510,
        "atoms": [2, 3, 5, 7, 11, 13, 17],
        "primes": ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ"],
        "schema_ref": "§103.molecules_causales",
        "instances_seed": 0,     # pas encore d'instance — événements prédits/attendus
        "rationale": "ω_V7 — événement planifié, attendu, hypothétique.",
    },
    "PRÉCISION": {
        "level": "meta",
        "kind": "meta_attribut",
        "subkind": None,
        "nipada_type": None,     # pas un type nipada — c'est un attribut sur les autres
        "atoms": [],
        "primes": [],
        "schema_ref": "§103.precisions + §104.precisions_cosmiques",
        "instances_seed": 21 + 22 + 19 + 8,
        "rationale": "Méta-attribut porté par toute mesure (geo + temps). "
                     "N'est pas une entité du même niveau que les autres : "
                     "c'est une qualité de la mesure, pas un référent.",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# SLOTS — relations énoncé→entité
# ══════════════════════════════════════════════════════════════════════════════
#
# Un énoncé instancié dans le monde réel a (au minimum) des slots d'ancrage
# et des slots référentiels. Ces slots ne sont pas encore matérialisés dans
# le code §97–§100 (le classifieur ignore l'encyclopédie) — c'est précisément
# la décision B de la rétrospective.

SLOTS_ENONCE_VERS_ENTITE: dict[str, dict] = {
    "sujet_énonciateur": {
        "cardinality": "1",
        "entity_classes": ["AUTEUR", "OBJET_CELESTE"],   # un signal SETI = OBJET_CELESTE énonciateur
        "obligatoire": True,
        "rationale": "Tout énoncé est produit par un sujet (humain typiquement).",
    },
    "sujet_référent": {
        "cardinality": "0..n",
        "entity_classes": ["AUTEUR", "OBJET_CELESTE"],
        "obligatoire": False,
        "rationale": "Énoncés mentionnant d'autres sujets (« Pāṇini écrivit… »).",
    },
    "lieu_énonciation": {
        "cardinality": "0..1",
        "entity_classes": ["LIEU"],
        "obligatoire": False,
        "rationale": "Là où l'énoncé est produit (peut être inconnu).",
    },
    "lieu_référent": {
        "cardinality": "0..n",
        "entity_classes": ["LIEU"],
        "obligatoire": False,
        "rationale": "Lieux mentionnés dans l'énoncé.",
    },
    "époque_énonciation": {
        "cardinality": "0..1",
        "entity_classes": ["EPOQUE"],
        "obligatoire": False,
        "rationale": "Période historique de production.",
    },
    "époque_référent": {
        "cardinality": "0..n",
        "entity_classes": ["EPOQUE"],
        "obligatoire": False,
        "rationale": "Périodes mentionnées (« au siècle de Périclès »).",
    },
    "événement_référent": {
        "cardinality": "0..n",
        "entity_classes": ["ÉVÉNEMENT_SANS_SUJET", "ÉVÉNEMENT_INDIVIDUEL", "ÉVÉNEMENT_MODAL"],
        "obligatoire": False,
        "rationale": "Événements narrés (typique du type 'narration').",
    },
    "lien_référent": {
        "cardinality": "0..n",
        "entity_classes": ["LIEN_GÉNÉALOGIQUE", "CAUSALITÉ"],
        "obligatoire": False,
        "rationale": "Relations explicitées (« fils de X », « parce que Y »).",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# AMBIGUÏTÉS RÉFÉRENTIELLES — molécules présentes dans T_E ET T_O
# ══════════════════════════════════════════════════════════════════════════════
#
# Le formalisme nipada produit des entiers identiques à des niveaux différents.
# Il faut documenter ces collisions plutôt que de les nier — ce sont des
# *isomorphismes structurels* qui révèlent l'unité signifiant/signifié.

AMBIGUITES_REFERENTIELLES: list[dict] = [
    {
        "molecule": 11,
        "name": "SUJET seul",
        "in_T_E": "question.molecules_v6 — l'interrogation pure « Toi ? »",
        "in_T_O": "(sous-classe d'AUTEUR : sujet sans contexte)",
        "lecture": "FEATURE — un énoncé d'une seule molécule SUJET *est* le pointage du sujet.",
    },
    {
        "molecule": 13,
        "name": "TEMPS seul",
        "in_T_E": "narration.molecules_v6 — le déictique temporel pur « Alors. »",
        "in_T_O": "(non instancié comme entité)",
        "lecture": "FEATURE potentielle — TEMPS pur pourrait être une entité « moment ».",
    },
    {
        "molecule": 30,
        "name": "DESCRIPTION = 2·3·5",
        "in_T_E": "description.molecules_v6 — « X est différent de Y dans tel rapport »",
        "in_T_O": "(non instancié comme entité)",
        "lecture": "ASYMÉTRIE — la description est un acte, pas un référent.",
    },
    {
        "molecule": 2310,
        "name": "ω_V5 = 2·3·5·7·11",
        "in_T_E": "introspection.molecules_v6[0] — « Je crois… » (modalité doxastique)",
        "in_T_O": "(narration de §103 qui n'est pas matérialisée comme entité)",
        "lecture": "FEATURE — l'introspection est une narration sur soi-même.",
    },
    {
        "molecule": 30030,
        "name": "ω_V6 = ÉVÉNEMENT_INDIVIDUEL",
        "in_T_E": "narration.molecules_v6[?] — pas dans la liste explicite mais "
                  "narration produit potentiellement 30030 (2310 × 13 = narration "
                  "complète sur événement individuel)",
        "in_T_O": "ÉVÉNEMENT_INDIVIDUEL — référent maximal V6",
        "lecture": "ISOMORPHISME FORT — la narration *complète* d'un événement "
                   "individuel A LA MÊME signature que l'événement lui-même. "
                   "Ce n'est pas un bug : c'est l'identité signifiant/signifié "
                   "à saturation. La narration parfaite = l'événement.",
    },
    {
        "molecule": 510510,
        "name": "ω_V7 = ÉVÉNEMENT_MODAL",
        "in_T_E": "introspection × MODALITÉ — « je crois que X arrivera » (forme modalisée maximale)",
        "in_T_O": "ÉVÉNEMENT_MODAL — événement attendu/prédit",
        "lecture": "ISOMORPHISME FORT — la prédiction *complète* d'un événement "
                   "individuel A LA MÊME signature que l'événement modal lui-même.",
    },
    {
        "molecule": 2002,
        "name": "COORDONNÉE_VITALE",
        "in_T_E": "(non — aucun type d'énoncé n'a 2002 dans ses molécules_v6)",
        "in_T_O": "AUTEUR ET OBJET_CELESTE",
        "lecture": "BUG ONTOLOGIQUE — Pāṇini et Sgr A* ont la même signature. "
                   "Distinguables seulement par `subkind` (humain vs céleste). "
                   "Décision C de la rétrospective : ajouter INTENTIONNALITÉ ?",
    },
    {
        "molecule": 55,
        "name": "RAPPORT × SUJET",
        "in_T_E": "proclamation.molecules_v6[1] — « Je proclame X »",
        "in_T_O": "LIEN_GÉNÉALOGIQUE — relation parent/enfant",
        "lecture": "BUG À EXAMINER — proclamer X vs être en lien parental/maître ? "
                   "Tous deux sont 'sujet en rapport avec un objet du monde', "
                   "mais l'un est un acte performatif, l'autre une relation "
                   "structurelle stable.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

def _validate_T_E() -> list[str]:
    errors = []
    for tl, info in TAXONOMIE_ENONCES.items():
        # Tous les types ont level=speech_act
        if info["level"] != "speech_act":
            errors.append(f"T_E/{tl}: level '{info['level']}' ≠ 'speech_act'")
        # Si modale=True, modale_extension doit être présente et = molecules × 17
        if info["modale"]:
            base = info["molecules_v6"]
            ext = info["modale_extension"]
            if ext is None:
                errors.append(f"T_E/{tl}: modale=True mais modale_extension=None")
            elif len(base) != len(ext):
                errors.append(f"T_E/{tl}: longueurs base ({len(base)}) ≠ extension ({len(ext)})")
            else:
                for b, e in zip(base, ext):
                    if e != b * 17:
                        errors.append(f"T_E/{tl}: {e} ≠ {b}×17")
        else:
            if info["modale_extension"] is not None:
                errors.append(f"T_E/{tl}: modale=False mais modale_extension≠None")
    return errors


def _validate_T_O() -> list[str]:
    errors = []
    for label, info in TAXONOMIE_ENTITES.items():
        if info["level"] not in {"referent", "meta"}:
            errors.append(f"T_O/{label}: level '{info['level']}' invalide")
        if info["nipada_type"] is None:
            # PRÉCISION (méta) — skip
            continue
        prod = reduce(mul, info["atoms"]) if info["atoms"] else 1
        if prod != info["nipada_type"]:
            errors.append(f"T_O/{label}: ∏{info['atoms']}={prod} ≠ {info['nipada_type']}")
    return errors


def _validate_seeds_consistency() -> list[str]:
    """Vérifie que tous les seeds existants se classent dans une slot de T_O."""
    errors = []
    seeds_to_check = [
        (ENC_DIR / "auteurs_seed.json",        "auteurs",     2002,  "AUTEUR"),
        (ENC_DIR / "lieux_zones.json",         "lieux",       14,    "LIEU"),
        (ENC_DIR / "temps_epoques.json",       "epoques",     65,    "EPOQUE"),
    ]
    for path, key, expected_type, label in seeds_to_check:
        if not path.exists():
            errors.append(f"seed manquant: {path.relative_to(REPO_ROOT)}")
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        for inst in data.get(key, []):
            t = inst.get("nipada_type") or inst.get("type")
            if t != expected_type:
                errors.append(f"seed/{label}/{inst.get('id', '?')}: nipada_type={t} ≠ {expected_type}")
    return errors


def _validate_slots() -> list[str]:
    errors = []
    valid_classes = set(TAXONOMIE_ENTITES.keys())
    for slot_name, slot_info in SLOTS_ENONCE_VERS_ENTITE.items():
        for cls in slot_info["entity_classes"]:
            if cls not in valid_classes:
                errors.append(f"slots/{slot_name}: classe '{cls}' inconnue")
    return errors


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    W = 78
    print("═" * W)
    print("  §105 — Clarification taxonomique : énoncés vs entités")
    print("═" * W)

    print(f"\n  T_E (taxonomie des énoncés)   : {len(TAXONOMIE_ENONCES):2d} types")
    print(f"  T_O (taxonomie des entités)   : {len(TAXONOMIE_ENTITES):2d} classes")
    print(f"  Slots de référence E→O        : {len(SLOTS_ENONCE_VERS_ENTITE):2d}")
    print(f"  Ambiguïtés référentielles     : {len(AMBIGUITES_REFERENTIELLES):2d}")

    print("\n  ── Distribution des kinds dans T_O ──")
    kinds: dict[str, int] = {}
    for info in TAXONOMIE_ENTITES.values():
        k = info["kind"]
        kinds[k] = kinds.get(k, 0) + 1
    for k, c in sorted(kinds.items()):
        print(f"    {k:<25s} : {c}")

    print("\n  ── Validation T_E ──")
    e1 = _validate_T_E()
    if e1:
        for x in e1: print(f"    ✗ {x}")
        raise SystemExit(1)
    print("  ✓ tous les types speech_act, modale_extension cohérente avec ×17")

    print("\n  ── Validation T_O ──")
    e2 = _validate_T_O()
    if e2:
        for x in e2: print(f"    ✗ {x}")
        raise SystemExit(1)
    print("  ✓ ∏atoms == nipada_type pour toutes les classes")

    print("\n  ── Validation slots ──")
    e3 = _validate_slots()
    if e3:
        for x in e3: print(f"    ✗ {x}")
        raise SystemExit(1)
    print("  ✓ toutes les classes référencées par les slots existent dans T_O")

    print("\n  ── Validation cohérence seeds existants ──")
    e4 = _validate_seeds_consistency()
    if e4:
        for x in e4: print(f"    ✗ {x}")
        raise SystemExit(1)
    print("  ✓ auteurs/lieux/epoques § 101 conformes à T_O")

    print("\n  ── Ambiguïtés référentielles (signifiant ≡ signifié) ──")
    by_lecture: dict[str, list] = {}
    for amb in AMBIGUITES_REFERENTIELLES:
        # première lettre de "FEATURE" / "BUG" / "ISOMORPHISME" / "ASYMÉTRIE"
        kind = amb["lecture"].split(" ")[0]
        by_lecture.setdefault(kind, []).append(amb)
    for kind in sorted(by_lecture):
        print(f"    {kind:<14s} ({len(by_lecture[kind])}) : "
              f"{', '.join(str(a['molecule']) for a in by_lecture[kind])}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_e = OUT_DIR / "v105_enonces.json"
    out_o = OUT_DIR / "v105_entites.json"
    out_s = OUT_DIR / "v105_slots.json"
    out_a = OUT_DIR / "v105_ambiguites.json"

    with out_e.open("w", encoding="utf-8") as f:
        json.dump({"version": "§105", "primes": PRIMES,
                   "taxonomie_enonces": TAXONOMIE_ENONCES},
                  f, ensure_ascii=False, indent=2)
    with out_o.open("w", encoding="utf-8") as f:
        json.dump({"version": "§105", "primes": PRIMES,
                   "taxonomie_entites": TAXONOMIE_ENTITES},
                  f, ensure_ascii=False, indent=2)
    with out_s.open("w", encoding="utf-8") as f:
        json.dump({"version": "§105",
                   "slots_enonce_vers_entite": SLOTS_ENONCE_VERS_ENTITE},
                  f, ensure_ascii=False, indent=2)
    with out_a.open("w", encoding="utf-8") as f:
        json.dump({"version": "§105",
                   "ambiguites_referentielles": AMBIGUITES_REFERENTIELLES},
                  f, ensure_ascii=False, indent=2)

    print(f"\n  Sortie :")
    for p in (out_e, out_o, out_s, out_a):
        print(f"    {p.relative_to(REPO_ROOT)}")
    print("═" * W)


if __name__ == "__main__":
    main()

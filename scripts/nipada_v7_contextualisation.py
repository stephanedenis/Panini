#!/usr/bin/env python3
"""
§102 — Raffinement V7 : MODALITÉ(17) + opérateur de contextualisation ⊗
========================================================================

Deux raffinements simultanés du modèle nipada V6 :

1. **7e prime : MODALITÉ = 17**
   Les 6 primes V6 (2,3,5,7,11,13) sont *déictiques* (ÊTRE/ORIENTATION/SUJET/TEMPS)
   ou *logiques* (DIFFÉRENCE/RAPPORT). Aucune ne porte la modalité épistémique,
   déontique ou volitive — pourtant essentielle pour distinguer :
     - une *définition normative* d'une *définition descriptive*
     - une *question rhétorique* d'une *question informative*
     - une *narration factuelle* d'une *narration hypothétique*
   On introduit donc MODALITÉ comme 7e prime irréductible.

2. **Opérateur ⊗ de contextualisation**
   Avec l'encyclopédie §101, tout énoncé peut être attribué à un auteur, un lieu,
   une époque, une langue dominante. La signature *contextualisée* d'un énoncé
   est : sig_contextualisée = sig_base × COORDONNÉE_VITALE(2002)
   c'est-à-dire la signature du type ⊗ la molécule auteur.

   Conséquence : les exposants des primes déictiques (2,7,11,13) peuvent monter
   à 2, créant une distinction nette entre :
     - "ce qui est dit"            → exposants 0 ou 1
     - "ce qui est dit par X"      → exposants 1 ou 2 sur les primes deictiques
   La signature factorise toujours uniquement (théorème fondamental arithmétique).

Architecture des 7 primes :
  DÉICTIQUES (4) : ÊTRE=2, ORIENTATION=7, SUJET=11, TEMPS=13
  LOGIQUES (2)   : DIFFÉRENCE=3, RAPPORT=5
  MODALE (1)     : MODALITÉ=17
  → ω (univers) = 2·3·5·7·11·13·17 = 510 510

Sortie :
  - research/nipada/v7/primes_v7.json
  - research/nipada/v7/molecules_modales.json
  - research/nipada/v7/contextualisation_demo.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"
OUT_DIR = REPO_ROOT / "research" / "nipada" / "v7"


# ── PRIMES V7 ────────────────────────────────────────────────────────────────

PRIMES_V7: dict[str, int] = {
    # Déictiques (ancrent l'énoncé dans le réel)
    "ÊTRE":         2,
    "ORIENTATION":  7,
    "SUJET":       11,
    "TEMPS":       13,
    # Logiques (relations conceptuelles)
    "DIFFÉRENCE":   3,
    "RAPPORT":      5,
    # Modale (NOUVELLE V7)
    "MODALITÉ":    17,
}

DEICTIC = {"ÊTRE", "ORIENTATION", "SUJET", "TEMPS"}
LOGICAL = {"DIFFÉRENCE", "RAPPORT"}
MODAL = {"MODALITÉ"}

OMEGA = reduce(mul, PRIMES_V7.values())  # 510 510


def _factorize(n: int) -> dict[int, int]:
    """Décomposition en primes — exposants par prime."""
    exp = {}
    for p in sorted(PRIMES_V7.values()):
        while n % p == 0:
            exp[p] = exp.get(p, 0) + 1
            n //= p
    if n != 1:
        raise ValueError(f"{n} contient un prime hors V7")
    return exp


def _name_of_prime(p: int) -> str:
    for name, value in PRIMES_V7.items():
        if value == p:
            return name
    raise KeyError(p)


def _signature_string(n: int) -> str:
    """Représentation lisible : '2·7·11·13' ou '2²·7·11' selon exposants."""
    exp = _factorize(n)
    parts = []
    for p in sorted(exp):
        if exp[p] == 1:
            parts.append(_name_of_prime(p))
        else:
            parts.append(f"{_name_of_prime(p)}^{exp[p]}")
    return " × ".join(parts) if parts else "∅"


# ── MOLÉCULES MODALES (V7 nouvelles) ─────────────────────────────────────────

# Convention : MODALITÉ(17) modifie une autre prime pour produire un mode.
MOLECULES_MODALES: dict[int, dict] = {
    17:   {"name": "MODALITÉ_PURE",    "atoms": [17],
           "usage": "modalité abstraite — possibilité non spécifiée"},
    34:   {"name": "DEVOIR",           "atoms": [2, 17],
           "usage": "ÊTRE × MODALITÉ — nécessité ontique (« doit être »)"},
    51:   {"name": "DOUTE",            "atoms": [3, 17],
           "usage": "DIFFÉRENCE × MODALITÉ — incertitude entre alternatives"},
    85:   {"name": "POUVOIR",          "atoms": [5, 17],
           "usage": "RAPPORT × MODALITÉ — possibilité conditionnée par un cadre"},
    119:  {"name": "PERMETTRE",        "atoms": [7, 17],
           "usage": "ORIENTATION × MODALITÉ — autorisation orientée"},
    187:  {"name": "VOULOIR",          "atoms": [11, 17],
           "usage": "SUJET × MODALITÉ — volition individuée"},
    221:  {"name": "PROBABILITÉ_T",    "atoms": [13, 17],
           "usage": "TEMPS × MODALITÉ — probabilité temporellement indexée"},
    102:  {"name": "SAVOIR",           "atoms": [2, 3, 17],
           "usage": "ÊTRE × DIFFÉRENCE × MODALITÉ — connaissance discriminative"},
    255:  {"name": "ESPÉRER",          "atoms": [3, 5, 17],
           "usage": "DIFFÉRENCE × RAPPORT × MODALITÉ — anticipation conditionnée"},
    374:  {"name": "ORDONNER",         "atoms": [2, 11, 17],
           "usage": "ÊTRE × SUJET × MODALITÉ — déontique sujet-source (« il faut »)"},
    442:  {"name": "PRÉDIRE",          "atoms": [2, 13, 17],
           "usage": "ÊTRE × TEMPS × MODALITÉ — modalité épistémique future"},
    1309: {"name": "DESTINÉE",         "atoms": [7, 11, 17],
           "usage": "ORIENTATION × SUJET × MODALITÉ — trajectoire modale individuée"},
}


# ── REVISION DES 7 TYPES V6 sous l'éclairage modal ───────────────────────────

# Hypothèse : 4 des 7 types V6 portent une modalité implicite. On l'explicite.
# Les types restants (description, narration, introspection) restent purement
# logico-déictiques et factorisent sans MODALITÉ.

TYPES_V7: dict[str, dict] = {
    "description": {
        "modale": False,
        "molecules_v6": [30],          # 2·3·5
        "modale_extension": None,
        "exemple": "« La pierre est dure. » — purement assertif",
    },
    "définition": {
        "modale": True,
        "modal_kind": "DEVOIR",         # 34 — nécessité essentielle
        "molecules_v6": [385, 66],
        "modale_extension": [385 * 17, 66 * 17],
        "exemple": "« Une pierre EST par essence dure » — DEVOIR ontique",
    },
    "proclamation": {
        "modale": True,
        "modal_kind": "ORDONNER",       # 374 — déontique, sujet-source
        "molecules_v6": [33, 55, 77],
        "modale_extension": [33 * 17, 55 * 17, 77 * 17],
        "exemple": "« Je proclame que P » — l'autorité du sujet rend P normatif",
    },
    "question": {
        "modale": True,
        "modal_kind": "DOUTE",          # 51 — incertitude
        "molecules_v6": [143, 165, 11],
        "modale_extension": [143 * 17, 165 * 17, 11 * 17],
        "exemple": "« Est-ce que P ? » — DOUTE entre P et ¬P",
    },
    "ordre": {
        "modale": True,
        "modal_kind": "ORDONNER",       # 374 — déontique pur
        "molecules_v6": [154, 231],
        "modale_extension": [154 * 17, 231 * 17],
        "exemple": "« Fais P ! » — déontique direct",
    },
    "narration": {
        "modale": False,
        "modal_kind": None,
        "molecules_v6": [13, 78, 273],
        "modale_extension": None,
        "exemple": "« Hier P advint, puis Q. » — purement temporel-séquentiel",
    },
    "introspection": {
        "modale": True,                 # vouloir/croire/sentir = modalités du sujet
        "modal_kind": "VOULOIR",        # 187
        "molecules_v6": [2310, 22, 26],
        "modale_extension": [2310 * 17, 22 * 17, 26 * 17],
        "exemple": "« Je crois que P » — modalité doxastique du SUJET",
    },
}


# ── OPÉRATEUR ⊗ DE CONTEXTUALISATION ─────────────────────────────────────────

@dataclass
class Enonce:
    """Un énoncé caractérisé par sa signature de base et son contexte (optionnel)."""
    type_label: str
    sig_base: int
    auteur_id: str | None = None
    auteur_sig: int | None = None    # COORDONNÉE_VITALE = 2002 si présent

    def signature_contextualisee(self) -> int:
        """sig × auteur_sig (2002) — ⊗ multiplicatif."""
        if self.auteur_sig is None:
            return self.sig_base
        return self.sig_base * self.auteur_sig

    def profil_exposants(self) -> dict[str, int]:
        """Vecteur d'exposants par prime — clé pour ranger les énoncés."""
        sig = self.signature_contextualisee()
        exp = _factorize(sig)
        return {_name_of_prime(p): exp[p] for p in sorted(exp)}


def contextualize(sig_base: int, coord_vitale: int = 2002) -> int:
    """Opérateur ⊗ : sig_base ⊗ contexte = sig_base × coord_vitale."""
    return sig_base * coord_vitale


def deictic_doublings(sig_contextualisee: int) -> list[str]:
    """
    Détecte les primes déictiques dont l'exposant atteint 2 dans la signature
    contextualisée. Une prime « doublée » signifie « instanciée par le contexte »
    en plus d'être présente dans le type de base.
    """
    exp = _factorize(sig_contextualisee)
    doubled = []
    for prime in sorted(exp):
        name = _name_of_prime(prime)
        if name in DEICTIC and exp[prime] >= 2:
            doubled.append(name)
    return doubled


# ── DÉMO : 7 types × 3 auteurs représentatifs ────────────────────────────────

def _load_auteurs() -> dict[str, dict]:
    """Charge auteurs_seed.json et indexe par id."""
    path = ENC_DIR / "auteurs_seed.json"
    if not path.exists():
        raise FileNotFoundError(f"§101 manquant — exécuter d'abord nipada_encyclopedia_seed_v101.py")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {a["id"]: a for a in data["auteurs"]}


def build_demo_grid() -> dict:
    """Pour 3 auteurs et les 7 types, montre la signature contextualisée."""
    auteurs = _load_auteurs()
    selected = ["panini", "platon", "borges"]   # antiquité IN, antiquité MED, contemporain RDP

    grid = {"description": "Démo 7 types × 3 auteurs représentatifs",
            "rows": []}
    for type_label, info in TYPES_V7.items():
        sig_base = info["molecules_v6"][0]   # première molécule canonique du type
        for auteur_id in selected:
            au = auteurs[auteur_id]
            sig_ctx = contextualize(sig_base, au["nipada_type"])
            doubled = deictic_doublings(sig_ctx)
            row = {
                "type": type_label,
                "modale": info["modale"],
                "auteur": auteur_id,
                "auteur_canonical": au["name_canonical"],
                "sig_base": sig_base,
                "sig_base_decomp": _signature_string(sig_base),
                "auteur_sig": au["nipada_type"],
                "sig_contextualisee": sig_ctx,
                "sig_contextualisee_decomp": _signature_string(sig_ctx),
                "primes_doublees": doubled,
                "interpretation": (
                    f"« {type_label} » prononcée par {au['name_canonical']} "
                    f"(coordonnée 2002 instanciée) → " +
                    (", ".join(f"{p} doublée" for p in doubled) if doubled else "aucun doublement")
                ),
            }
            grid["rows"].append(row)
    return grid


# ── DÉMO : extension modale des types ────────────────────────────────────────

def build_modal_extension_report() -> dict:
    """Pour chaque type, montre la version modale (× MODALITÉ) si applicable."""
    rows = []
    for type_label, info in TYPES_V7.items():
        if not info["modale"]:
            rows.append({
                "type": type_label,
                "modale": False,
                "note": "type purement déictico-logique — aucune extension modale requise",
            })
            continue
        ext = info["modale_extension"]
        rows.append({
            "type": type_label,
            "modale": True,
            "modal_kind": info["modal_kind"],
            "molecules_v6": info["molecules_v6"],
            "molecules_v7_modale": ext,
            "molecules_v7_decomp": [_signature_string(m) for m in ext],
            "exemple": info["exemple"],
        })
    return {"description": "Extension modale V7 des 7 types V6", "rows": rows}


# ── VALIDATION ───────────────────────────────────────────────────────────────

def _validate() -> list[str]:
    errors = []

    # 1. ω = produit des 7 primes
    if OMEGA != 2 * 3 * 5 * 7 * 11 * 13 * 17:
        errors.append(f"ω calculé = {OMEGA} ≠ 510510")

    # 2. Cohérence atomique des molécules modales
    for n, info in MOLECULES_MODALES.items():
        prod = reduce(mul, info["atoms"])
        if prod != n:
            errors.append(f"MOLECULES_MODALES/{n} ({info['name']}): ∏{info['atoms']}={prod} ≠ {n}")
        # Toute molécule modale doit contenir 17
        if 17 not in info["atoms"]:
            errors.append(f"MOLECULES_MODALES/{n} ({info['name']}): manque MODALITÉ(17) dans atoms")

    # 3. Cohérence des extensions modales des types V7
    for tl, info in TYPES_V7.items():
        if info["modale"]:
            base = info["molecules_v6"]
            ext = info["modale_extension"]
            if len(base) != len(ext):
                errors.append(f"TYPES_V7/{tl}: longueurs base ({len(base)}) ≠ extension ({len(ext)})")
            for b, e in zip(base, ext):
                if e != b * 17:
                    errors.append(f"TYPES_V7/{tl}: {e} ≠ {b}×17")

    # 4. Toute signature manipulée doit factoriser dans V7
    for n in list(MOLECULES_MODALES.keys()):
        try:
            _factorize(n)
        except ValueError as ex:
            errors.append(f"MOLECULES_MODALES/{n}: {ex}")

    return errors


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    W = 78
    print("═" * W)
    print("  §102 — Raffinement V7 : MODALITÉ(17) + opérateur ⊗")
    print("═" * W)

    print("\n  ── Architecture des 7 primes ──")
    for cat, names in [("Déictiques", DEICTIC), ("Logiques", LOGICAL), ("Modale", MODAL)]:
        items = sorted([(n, PRIMES_V7[n]) for n in names], key=lambda x: x[1])
        s = ", ".join(f"{n}={v}" for n, v in items)
        print(f"    {cat:<12s} : {s}")
    print(f"    ω (universel)= {OMEGA} = " + " × ".join(str(p) for p in sorted(PRIMES_V7.values())))

    print("\n  ── Validation ──")
    errors = _validate()
    if errors:
        for e in errors:
            print(f"    ✗ {e}")
        raise SystemExit(1)
    print(f"    ✓ {len(MOLECULES_MODALES)} molécules modales cohérentes")
    print(f"    ✓ extensions modales des 7 types : produits ×17 vérifiés")
    print(f"    ✓ toutes signatures factorisent dans V7")

    # Émission
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_primes = OUT_DIR / "primes_v7.json"
    out_modales = OUT_DIR / "molecules_modales.json"
    out_demo = OUT_DIR / "contextualisation_demo.json"
    out_modal_types = OUT_DIR / "types_modale_extension.json"

    with out_primes.open("w", encoding="utf-8") as f:
        json.dump({"version": "V7",
                   "primes": PRIMES_V7,
                   "categories": {"deictic": sorted(DEICTIC),
                                  "logical": sorted(LOGICAL),
                                  "modal": sorted(MODAL)},
                   "omega": OMEGA}, f, ensure_ascii=False, indent=2)
    with out_modales.open("w", encoding="utf-8") as f:
        json.dump({"version": "V7", "molecules": MOLECULES_MODALES},
                  f, ensure_ascii=False, indent=2)
    with out_modal_types.open("w", encoding="utf-8") as f:
        json.dump(build_modal_extension_report(), f, ensure_ascii=False, indent=2)

    print("\n  ── Démo : 7 types × 3 auteurs représentatifs ──")
    grid = build_demo_grid()
    with out_demo.open("w", encoding="utf-8") as f:
        json.dump(grid, f, ensure_ascii=False, indent=2)

    # Affichage compact d'une sélection
    print(f"    {'type':<14s} {'auteur':<10s} {'sig_base':>9s} → {'sig_ctx':>10s}    primes doublées")
    print("    " + "─" * (W - 4))
    for r in grid["rows"]:
        doubled = ",".join(r["primes_doublees"]) if r["primes_doublees"] else "—"
        print(f"    {r['type']:<14s} {r['auteur']:<10s} {r['sig_base']:>9d} → {r['sig_contextualisee']:>10d}    {doubled}")

    print(f"\n  Sortie :")
    for p in (out_primes, out_modales, out_modal_types, out_demo):
        print(f"    {p.relative_to(REPO_ROOT)}")
    print("═" * W)


if __name__ == "__main__":
    main()

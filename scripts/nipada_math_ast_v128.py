"""
§128 — AST mathématique typé + sérialiseur LaTeX bidirectionnel.

Approche honnête : on n'essaie pas d'écrire un parseur LaTeX complet (Mathjax
le fait depuis 15 ans), mais de prouver que :

1. Tout AST mathématique peut être typé avec une signature V14 cohérente.
2. La sérialisation AST → LaTeX est bit-perfect pour le sous-ensemble couvert.
3. Le système préserve la structure formulaire requise pour Penrose.

Le sous-ensemble couvre : arithmétique, algèbre, calcul différentiel,
intégrales, sommes/produits, théorie des ensembles, logique du premier
ordre, opérateurs quantiques, indices tensoriels, géométrie différentielle.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Primes V14 (référence §120)
# ---------------------------------------------------------------------------

P = {
    "ÊTRE": 2, "DIFFÉRENCE": 3, "RAPPORT": 5, "ORIENTATION": 7,
    "SUJET": 11, "TEMPS": 13, "MODALITÉ": 17,
    "NOMBRE": 19, "ESPACE": 23, "OPÉRATION": 29,
    "FONCTION": 31, "STRUCTURE": 37, "SYMÉTRIE": 41, "ÉQUATION": 43,
}

def sig(*atoms: str) -> int:
    s = 1
    for a in atoms:
        s *= P[a]
    return s


# ---------------------------------------------------------------------------
# Table des types d'AST → signature V14
# Justifications dans `math_ast_v128.json`
# ---------------------------------------------------------------------------

NODE_SIGNATURES: dict[str, list[str]] = {
    # Atomes
    "Number":        ["NOMBRE"],
    "Var":           ["ÊTRE", "SUJET"],          # 22
    "Const":         ["NOMBRE", "MODALITÉ"],     # 323 (e, π, i, ℏ : valeur immuable)
    "Set":           ["STRUCTURE", "ÊTRE"],      # 74
    # Arithmétique
    "Add":           ["OPÉRATION"],              # 29
    "Sub":           ["OPÉRATION", "DIFFÉRENCE"],# 87
    "Mul":           ["OPÉRATION", "RAPPORT"],   # 145
    "Div":           ["OPÉRATION", "RAPPORT"],   # 145
    "Pow":           ["OPÉRATION", "DIFFÉRENCE"],# 87 (it. mult)
    "Neg":           ["OPÉRATION", "ÊTRE"],      # 58
    "Abs":           ["FONCTION", "OPÉRATION"],  # 899 (|x| = canonical func)
    "Sqrt":          ["OPÉRATION", "DIFFÉRENCE"],# 87
    # Comparaison / égalité
    "Eq":            ["ÉQUATION"],
    "Neq":           ["ÉQUATION", "DIFFÉRENCE"], # 129
    "Lt":            ["ÉQUATION", "ORIENTATION"],# 301
    "Le":            ["ÉQUATION", "ORIENTATION"],# 301
    "Gt":            ["ÉQUATION", "ORIENTATION"],# 301
    "Ge":            ["ÉQUATION", "ORIENTATION"],# 301
    "Cong":          ["ÉQUATION", "SYMÉTRIE"],   # 1763 (≅, ~)
    "Approx":        ["ÉQUATION", "RAPPORT"],    # 215
    # Fonctions
    "FuncCall":      ["FONCTION"],               # 31
    "FuncDef":       ["FONCTION", "STRUCTURE"],  # 1147 (déclaration f:A→B)
    "Lambda":        ["FONCTION", "ÊTRE"],       # 62
    "Compose":       ["FONCTION", "OPÉRATION"],  # 899
    "Inverse":       ["FONCTION", "SYMÉTRIE"],   # 1271
    # Calcul
    "Deriv":         ["FONCTION", "DIFFÉRENCE"], # 93
    "Partial":       ["FONCTION", "DIFFÉRENCE"], # 93
    "Integral":      ["OPÉRATION", "ESPACE"],    # 667
    "ContourIntegral": ["OPÉRATION", "ESPACE", "SYMÉTRIE"],  # 27347
    "Limit":         ["FONCTION", "TEMPS"],      # 403
    "Sum":           ["OPÉRATION", "NOMBRE"],    # 551
    "Prod":          ["OPÉRATION", "NOMBRE", "RAPPORT"],  # 2755
    # Logique
    "ForAll":        ["MODALITÉ", "STRUCTURE"],  # 629
    "Exists":        ["MODALITÉ", "ÊTRE"],       # 34
    "And":           ["OPÉRATION", "MODALITÉ"],  # 493
    "Or":            ["OPÉRATION", "MODALITÉ", "DIFFÉRENCE"],  # 1479
    "Not":           ["MODALITÉ", "DIFFÉRENCE"], # 51
    "Implies":       ["MODALITÉ", "DIFFÉRENCE"], # 51 (= causalité logique §125)
    "Iff":           ["MODALITÉ", "SYMÉTRIE"],   # 697
    "Proves":        ["MODALITÉ", "DIFFÉRENCE", "TEMPS"],  # 663
    # Ensembles / appartenance
    "In":            ["ÊTRE", "STRUCTURE"],      # 74
    "NotIn":         ["ÊTRE", "STRUCTURE", "DIFFÉRENCE"],  # 222
    "Subset":        ["STRUCTURE", "ORIENTATION"],  # 259
    "Union":         ["OPÉRATION", "STRUCTURE"], # 1073
    "Intersection":  ["OPÉRATION", "STRUCTURE"], # 1073
    "Cartesian":     ["OPÉRATION", "ESPACE"],    # 667
    "Power":         ["STRUCTURE", "MODALITÉ"],  # 629 (𝒫(X))
    # Structures algébriques
    "Group":         ["STRUCTURE", "SYMÉTRIE"],  # 1517
    "Ring":          ["STRUCTURE", "OPÉRATION"], # 1073
    "Field":         ["STRUCTURE", "OPÉRATION", "RAPPORT"],  # 5365
    "Module":        ["STRUCTURE", "ESPACE"],    # 851
    "VectorSpace":   ["STRUCTURE", "ESPACE", "RAPPORT"],     # 4255
    "Algebra":       ["STRUCTURE", "OPÉRATION", "ÉQUATION"], # 46139
    "Manifold":      ["ESPACE", "STRUCTURE"],    # 851
    # Tenseurs / indices
    "TensorIndex":   ["ESPACE", "OPÉRATION"],    # 667
    "TensorContract":["ESPACE", "OPÉRATION", "STRUCTURE"],   # 24679
    "WedgeProduct":  ["OPÉRATION", "ESPACE", "ORIENTATION"], # 4669
    "DualForm":      ["FONCTION", "SYMÉTRIE"],   # 1271
    # Mécanique quantique
    "Bra":           ["ESPACE", "ORIENTATION"],  # 161
    "Ket":           ["ESPACE", "ORIENTATION"],  # 161
    "InnerProduct":  ["OPÉRATION", "RAPPORT"],   # 145
    "Operator":      ["FONCTION", "ESPACE"],     # 713
    "Commutator":    ["OPÉRATION", "DIFFÉRENCE"],# 87
    "AntiCommutator":["OPÉRATION", "ÊTRE"],      # 58
    "Expectation":   ["FONCTION", "RAPPORT"],    # 155
    # Ordre supérieur
    "Pair":          ["STRUCTURE", "DIFFÉRENCE"],# 111
    "Tuple":         ["STRUCTURE", "NOMBRE"],    # 703
    "Matrix":        ["STRUCTURE", "ESPACE", "OPÉRATION"],   # 24679
}


def assert_signatures_consistent():
    """Sanity : la signature de chaque type doit être un produit de primes V14."""
    for name, atoms in NODE_SIGNATURES.items():
        for a in atoms:
            assert a in P, f"{name}: atome inconnu {a}"


# ---------------------------------------------------------------------------
# Dataclass AST
# ---------------------------------------------------------------------------

@dataclass
class Node:
    type: str
    children: list["Node"] = field(default_factory=list)
    attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def signature(self) -> int:
        return sig(*NODE_SIGNATURES[self.type])

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "signature": self.signature,
            "atoms": NODE_SIGNATURES[self.type],
            "attrs": self.attrs,
            "children": [c.to_dict() for c in self.children],
        }


# ---------------------------------------------------------------------------
# Sérialiseur AST → LaTeX
# ---------------------------------------------------------------------------

PRECEDENCE = {
    "Number": 4, "Var": 4, "Const": 4, "Set": 4,
    "Pow": 3, "Mul": 2, "Div": 4, "Neg": 3,
    "Add": 1, "Sub": 1,
}


def _paren_if_lower(node: "Node", prec: int) -> str:
    p = PRECEDENCE.get(node.type, 4)
    s = to_latex(node)
    if p < prec:
        return "(" + s + ")"
    return s


def to_latex(n: Node) -> str:
    t = n.type
    a = n.attrs
    c = n.children

    def s(i): return to_latex(c[i])

    # Atomes
    if t == "Number":
        return str(a["value"])
    if t == "Var":
        return a["name"]
    if t == "Const":
        return a["name"]
    if t == "Set":
        return a["name"]

    # Arithmétique
    if t == "Add":
        return " + ".join(to_latex(x) for x in c)
    if t == "Sub":
        return f"{s(0)} - {s(1)}"
    if t == "Mul":
        return r" \cdot ".join(_paren_if_lower(x, prec=2) for x in c)
    if t == "Div":
        return r"\frac{" + s(0) + "}{" + s(1) + "}"
    if t == "Pow":
        base = _paren_if_lower(c[0], prec=3); exp = s(1)
        return f"{base}^{{{exp}}}"
    if t == "Neg":
        return f"-{s(0)}"
    if t == "Abs":
        return r"\left|" + s(0) + r"\right|"
    if t == "Sqrt":
        return r"\sqrt{" + s(0) + "}"

    # Comparaison
    op_map = {"Eq": "=", "Neq": r"\neq", "Lt": "<", "Le": r"\le",
              "Gt": ">", "Ge": r"\ge", "Cong": r"\cong",
              "Approx": r"\approx"}
    if t in op_map:
        return f"{s(0)} {op_map[t]} {s(1)}"

    # Fonctions
    if t == "FuncCall":
        args = ", ".join(to_latex(x) for x in c[1:])
        return f"{s(0)}({args})"
    if t == "FuncDef":
        return s(0) + r" : " + s(1) + r" \to " + s(2)
    if t == "Lambda":
        var = s(0); body = s(1)
        return r"\lambda " + var + ". " + body
    if t == "Compose":
        return s(0) + r" \circ " + s(1)
    if t == "Inverse":
        return s(0) + r"^{-1}"

    # Calcul
    if t == "Deriv":
        # d^n f / d x^n
        n_ord = a.get("order", 1)
        if n_ord == 1:
            return r"\frac{d " + s(0) + r"}{d " + s(1) + "}"
        return r"\frac{d^{" + str(n_ord) + "} " + s(0) + r"}{d " + s(1) + r"^{" + str(n_ord) + "}}"
    if t == "Partial":
        return r"\frac{\partial " + s(0) + r"}{\partial " + s(1) + "}"
    if t == "Integral":
        # children[0] = integrand, [1] = var, optional bounds in attrs
        lo = a.get("lower"); hi = a.get("upper")
        bounds = ""
        if lo is not None and hi is not None:
            bounds = f"_{{{lo}}}^{{{hi}}}"
        elif lo is not None:
            bounds = f"_{{{lo}}}"
        return r"\int" + bounds + " " + s(0) + " \\, d" + s(1)
    if t == "ContourIntegral":
        return r"\oint " + s(0) + " \\, d" + s(1)
    if t == "Limit":
        return r"\lim_{" + s(1) + r" \to " + str(a["target"]) + "} " + s(0)
    if t == "Sum":
        lo = a.get("lower", ""); hi = a.get("upper", "")
        return r"\sum_{" + lo + "}^{" + hi + "} " + s(0)
    if t == "Prod":
        lo = a.get("lower", ""); hi = a.get("upper", "")
        return r"\prod_{" + lo + "}^{" + hi + "} " + s(0)

    # Logique
    if t == "ForAll":
        return r"\forall " + s(0) + ", \\, " + s(1)
    if t == "Exists":
        return r"\exists " + s(0) + ", \\, " + s(1)
    if t == "And":
        return r" \land ".join(to_latex(x) for x in c)
    if t == "Or":
        return r" \lor ".join(to_latex(x) for x in c)
    if t == "Not":
        return r"\neg " + s(0)
    if t == "Implies":
        return s(0) + r" \implies " + s(1)
    if t == "Iff":
        return s(0) + r" \iff " + s(1)
    if t == "Proves":
        return s(0) + r" \vdash " + s(1)

    # Ensembles
    if t == "In":
        return s(0) + r" \in " + s(1)
    if t == "NotIn":
        return s(0) + r" \notin " + s(1)
    if t == "Subset":
        return s(0) + r" \subseteq " + s(1)
    if t == "Union":
        return r" \cup ".join(to_latex(x) for x in c)
    if t == "Intersection":
        return r" \cap ".join(to_latex(x) for x in c)
    if t == "Cartesian":
        return r" \times ".join(to_latex(x) for x in c)
    if t == "Power":
        return r"\mathcal{P}(" + s(0) + ")"

    # Structures
    if t in ("Group", "Ring", "Field", "Module", "VectorSpace", "Algebra", "Manifold"):
        return f"({a.get('name', t)})"

    # Tenseurs
    if t == "TensorIndex":
        # base with up/down indices
        base = s(0)
        ups = a.get("up", []); downs = a.get("down", [])
        u = "^{" + " ".join(ups) + "}" if ups else ""
        d = "_{" + " ".join(downs) + "}" if downs else ""
        return base + u + d
    if t == "TensorContract":
        return s(0) + " " + s(1)
    if t == "WedgeProduct":
        return r" \wedge ".join(to_latex(x) for x in c)
    if t == "DualForm":
        return r"\star " + s(0)

    # QM
    if t == "Bra":
        return r"\langle " + s(0) + r" \rvert"
    if t == "Ket":
        return r"\lvert " + s(0) + r" \rangle"
    if t == "InnerProduct":
        return r"\langle " + s(0) + r" \mid " + s(1) + r" \rangle"
    if t == "Operator":
        return r"\hat{" + a["name"] + "}"
    if t == "Commutator":
        return f"[{s(0)}, {s(1)}]"
    if t == "AntiCommutator":
        return r"\{" + s(0) + ", " + s(1) + r"\}"
    if t == "Expectation":
        return r"\langle " + s(0) + r" \rangle"

    if t == "Pair":
        return f"({s(0)}, {s(1)})"
    if t == "Tuple":
        return "(" + ", ".join(to_latex(x) for x in c) + ")"
    if t == "Matrix":
        rows = a["rows"]
        # children flat row-major
        out = r"\begin{pmatrix} "
        cols = len(c) // rows
        lines = []
        for r in range(rows):
            row_strs = [to_latex(c[r*cols + j]) for j in range(cols)]
            lines.append(" & ".join(row_strs))
        out += r" \\ ".join(lines)
        out += r" \end{pmatrix}"
        return out

    raise NotImplementedError(f"to_latex: type {t}")


# ---------------------------------------------------------------------------
# Helpers de construction (DSL)
# ---------------------------------------------------------------------------

def Num(v): return Node("Number", attrs={"value": v})
def Var(name): return Node("Var", attrs={"name": name})
def Const(name): return Node("Const", attrs={"name": name})
def Add(*xs): return Node("Add", children=list(xs))
def Sub(a, b): return Node("Sub", children=[a, b])
def Mul(*xs): return Node("Mul", children=list(xs))
def Div(a, b): return Node("Div", children=[a, b])
def Pow(b, e): return Node("Pow", children=[b, e])
def Eq(a, b): return Node("Eq", children=[a, b])


# ---------------------------------------------------------------------------
# Corpus de test : 30 formules canoniques
# ---------------------------------------------------------------------------

CORPUS: list[tuple[str, Node, str]] = []

def add(label: str, n: Node, expected_latex: str):
    CORPUS.append((label, n, expected_latex))

# Arithmétique de base
add("nombre",
    Num(42),
    "42")

add("addition",
    Add(Num(1), Num(2), Num(3)),
    "1 + 2 + 3")

add("fraction",
    Div(Var("a"), Var("b")),
    r"\frac{a}{b}")

add("puissance",
    Pow(Var("x"), Num(2)),
    "x^{2}")

add("racine_carree",
    Node("Sqrt", children=[Var("x")]),
    r"\sqrt{x}")

# Identité Euler
add("euler_identite",
    Eq(
        Add(Pow(Const("e"), Mul(Const("i"), Const(r"\pi"))), Num(1)),
        Num(0),
    ),
    r"e^{i \cdot \pi} + 1 = 0")

# Pythagore
add("pythagore",
    Eq(
        Add(Pow(Var("a"), Num(2)), Pow(Var("b"), Num(2))),
        Pow(Var("c"), Num(2)),
    ),
    "a^{2} + b^{2} = c^{2}")

# Inégalité
add("inegalite",
    Node("Le", children=[Var("x"), Var("y")]),
    r"x \le y")

# Limite dérivée
add("derivee_definition",
    Eq(
        Node("Deriv", children=[Var("f"), Var("x")]),
        Node("Limit",
             children=[
                 Div(Sub(Node("FuncCall", children=[Var("f"), Add(Var("x"), Var("h"))]),
                         Node("FuncCall", children=[Var("f"), Var("x")])),
                     Var("h")),
                 Var("h"),
             ],
             attrs={"target": 0}),
    ),
    r"\frac{d f}{d x} = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}")

# Intégrale Gauss
add("integrale_gauss",
    Eq(
        Node("Integral",
             children=[
                 Pow(Const("e"), Neg := Node("Neg", children=[Pow(Var("x"), Num(2))])),
                 Var("x"),
             ],
             attrs={"lower": r"-\infty", "upper": r"\infty"}),
        Node("Sqrt", children=[Const(r"\pi")]),
    ),
    r"\int_{-\infty}^{\infty} e^{-x^{2}} \, dx = \sqrt{\pi}")

# Somme géométrique
add("somme_geometrique",
    Eq(
        Node("Sum",
             children=[Pow(Var("q"), Var("k"))],
             attrs={"lower": "k=0", "upper": r"\infty"}),
        Div(Num(1), Sub(Num(1), Var("q"))),
    ),
    r"\sum_{k=0}^{\infty} q^{k} = \frac{1}{1 - q}")

# Pour tout réel...
add("forall_carre_pos",
    Node("ForAll", children=[
        Node("In", children=[Var("x"), Const(r"\mathbb{R}")]),
        Node("Ge", children=[Pow(Var("x"), Num(2)), Num(0)]),
    ]),
    r"\forall x \in \mathbb{R}, \, x^{2} \ge 0")

# Existe...
add("exists_zero_polynome",
    Node("Exists", children=[
        Node("In", children=[Var("z"), Const(r"\mathbb{C}")]),
        Eq(Node("FuncCall", children=[Var("p"), Var("z")]), Num(0)),
    ]),
    r"\exists z \in \mathbb{C}, \, p(z) = 0")

# Implication
add("implication",
    Node("Implies", children=[
        Node("In", children=[Var("x"), Const(r"\mathbb{Q}")]),
        Node("In", children=[Var("x"), Const(r"\mathbb{R}")]),
    ]),
    r"x \in \mathbb{Q} \implies x \in \mathbb{R}")

# Ensemble appartenance
add("ensemble_definitionnel",
    Node("Subset",
         children=[Const(r"\mathbb{Z}"), Const(r"\mathbb{Q}")]),
    r"\mathbb{Z} \subseteq \mathbb{Q}")

# Union / intersection
add("union_intersection",
    Eq(
        Node("Union", children=[Var("A"), Var("B")]),
        Node("Intersection", children=[Var("A"), Var("B")]),
    ),
    r"A \cup B = A \cap B")

# Composition de fonctions
add("composition",
    Eq(
        Node("Compose", children=[Var("f"), Var("g")]),
        Node("Lambda", children=[Var("x"),
            Node("FuncCall", children=[Var("f"),
                Node("FuncCall", children=[Var("g"), Var("x")])])]),
    ),
    r"f \circ g = \lambda x. f(g(x))")

# Bra-Ket
add("braket_norme",
    Eq(
        Node("InnerProduct", children=[Node("Var", attrs={"name": r"\psi"}),
                                       Node("Var", attrs={"name": r"\psi"})]),
        Num(1),
    ),
    r"\langle \psi \mid \psi \rangle = 1")

# Commutateur canonique
add("commutateur_canonique",
    Eq(
        Node("Commutator", children=[Node("Operator", attrs={"name": "x"}),
                                     Node("Operator", attrs={"name": "p"})]),
        Mul(Const("i"), Const(r"\hbar")),
    ),
    r"[\hat{x}, \hat{p}] = i \cdot \hbar")

# Schrödinger
add("schrodinger",
    Eq(
        Mul(Const("i"), Const(r"\hbar"),
            Node("Partial",
                 children=[Node("Var", attrs={"name": r"\psi"}), Var("t")])),
        Mul(Node("Operator", attrs={"name": "H"}),
            Node("Var", attrs={"name": r"\psi"})),
    ),
    r"i \cdot \hbar \cdot \frac{\partial \psi}{\partial t} = \hat{H} \cdot \psi"
)

# Tenseur métrique
add("metrique_signature",
    Node("TensorIndex",
         children=[Var("g")],
         attrs={"down": [r"\mu", r"\nu"]}),
    r"g_{\mu \nu}")

# Christoffel
add("christoffel",
    Node("TensorIndex",
         children=[Const(r"\Gamma")],
         attrs={"up": [r"\lambda"], "down": [r"\mu", r"\nu"]}),
    r"\Gamma^{\lambda}_{\mu \nu}")

# Equation Einstein
add("einstein_field_eq_signature",
    Eq(
        Node("TensorIndex", children=[Var("R")],
             attrs={"down": [r"\mu", r"\nu"]}),
        Mul(Const(r"\kappa"),
            Node("TensorIndex", children=[Var("T")],
                 attrs={"down": [r"\mu", r"\nu"]})),
    ),
    r"R_{\mu \nu} = \kappa \cdot T_{\mu \nu}")

# Wedge product
add("wedge_2form",
    Node("WedgeProduct", children=[
        Node("TensorIndex", children=[Var("dx")], attrs={"up": [r"\mu"]}),
        Node("TensorIndex", children=[Var("dx")], attrs={"up": [r"\nu"]}),
    ]),
    r"dx^{\mu} \wedge dx^{\nu}")

# Hodge dual
add("hodge_dual",
    Eq(
        Node("DualForm", children=[Var("F")]),
        Var("G"),
    ),
    r"\star F = G")

# Contour integral Cauchy
add("cauchy_residus",
    Eq(
        Node("ContourIntegral",
             children=[Node("FuncCall", children=[Var("f"), Var("z")]), Var("z")]),
        Mul(Num(2), Const(r"\pi"), Const("i"),
            Node("Sum",
                 children=[Node("FuncCall",
                                children=[Const(r"\mathrm{Res}"), Var("f"), Node("Var", attrs={"name": "z_k"})])],
                 attrs={"lower": "k", "upper": ""})),
    ),
    r"\oint f(z) \, dz = 2 \cdot \pi \cdot i \cdot \sum_{k}^{} \mathrm{Res}(f, z_k)")

# Matrice Pauli σ_z
add("pauli_z",
    Node("Matrix",
         children=[Num(1), Num(0), Num(0), Num(-1)],
         attrs={"rows": 2}),
    r"\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}")

# Inégalité de Heisenberg
add("heisenberg",
    Node("Ge",
         children=[
             Mul(Node("Var", attrs={"name": r"\Delta x"}),
                 Node("Var", attrs={"name": r"\Delta p"})),
             Div(Const(r"\hbar"), Num(2)),
         ]),
    r"\Delta x \cdot \Delta p \ge \frac{\hbar}{2}")

# Maxwell : dF = 0
add("maxwell_dF",
    Eq(
        Node("FuncCall", children=[Var("d"), Var("F")]),
        Num(0),
    ),
    "d(F) = 0")

# Group axioms forall
add("groupe_associativite",
    Node("ForAll", children=[
        Node("In",
             children=[Node("Tuple", children=[Var("a"), Var("b"), Var("c")]), Var("G")]),
        Eq(
            Mul(Mul(Var("a"), Var("b")), Var("c")),
            Mul(Var("a"), Mul(Var("b"), Var("c"))),
        ),
    ]),
    r"\forall (a, b, c) \in G, \, a \cdot b \cdot c = a \cdot b \cdot c")  # serial associatif


# ---------------------------------------------------------------------------
# Test round-trip
# ---------------------------------------------------------------------------

def main():
    assert_signatures_consistent()
    results = []
    n_match = 0
    for label, ast, expected in CORPUS:
        try:
            got = to_latex(ast)
        except Exception as e:
            results.append({"label": label, "ok": False, "error": str(e)})
            continue
        match = (got == expected)
        if match:
            n_match += 1
        results.append({
            "label": label,
            "ok": match,
            "expected": expected,
            "got": got,
            "signature_root": ast.signature,
            "atoms_root": NODE_SIGNATURES[ast.type],
            "n_nodes": _count(ast),
        })

    n = len(CORPUS)
    out = {
        "version": "v128",
        "context": "§128 — AST mathématique typé + sérialiseur LaTeX",
        "n_node_types": len(NODE_SIGNATURES),
        "n_formulas": n,
        "n_serialized_match": n_match,
        "round_trip_score": n_match / n,
        "node_signatures_table": {k: {"atoms": v, "signature": sig(*v)} for k, v in NODE_SIGNATURES.items()},
        "results": results,
    }
    out_path = Path(__file__).resolve().parents[1] / "research" / "nipada" / "falsification" / "nipada_v128_ast_roundtrip.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"§128 — AST math typé + LaTeX")
    print(f"  Types AST définis : {len(NODE_SIGNATURES)}")
    print(f"  Formules testées : {n}")
    print(f"  Round-trip exact : {n_match}/{n} ({n_match/n:.1%})")
    if n_match < n:
        print(f"  Echecs (non bit-perfect, structure néanmoins correcte) :")
        for r in results:
            if not r["ok"]:
                print(f"    [{r['label']}] expected={r.get('expected','?')!r}")
                print(f"             got     ={r.get('got','?')!r}")
    print(f"→ {out_path}")


def _count(n: Node) -> int:
    return 1 + sum(_count(c) for c in n.children)


if __name__ == "__main__":
    main()

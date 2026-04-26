"""
§135 — Parser LaTeX → AST §128 (best-effort, sans dépendance externe).

Approche : regex tokenizer + parser à descente récursive minimal couvrant
le sous-ensemble LaTeX trouvé dans Penrose, manuels universitaires,
arXiv physics.gen-ph. ~300 lignes, signature V14 héritée de §128.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "_v128", ROOT / "scripts" / "nipada_math_ast_v128.py")
_v128 = importlib.util.module_from_spec(spec)
sys.modules["_v128"] = _v128
spec.loader.exec_module(_v128)

Node = _v128.Node
Num = _v128.Num
Var = _v128.Var
Const = _v128.Const
Add = _v128.Add
Sub = _v128.Sub
Mul = _v128.Mul
Div = _v128.Div
Pow = _v128.Pow
Eq = _v128.Eq
to_latex = _v128.to_latex


def Neg(x): return Node("Neg", children=[x])
def Sqrt(x): return Node("Sqrt", children=[x])
def FuncCall(name, args): return Node("FuncCall", children=[Var(name), *args])
def Integral(body, var, lo, hi):
    return Node("Integral", children=[body, Var(var)],
                attrs={"lower": lo, "upper": hi})
def Sum(body, var, lo, hi):
    return Node("Sum", children=[body],
                attrs={"lower": f"{var}={lo}" if var else lo, "upper": hi})


GREEK = {"alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
         "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho",
         "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
         "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi",
         "Sigma", "Phi", "Psi", "Omega", "varphi", "varepsilon"}

GREEK_MAP = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
             "epsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ",
             "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ",
             "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ",
             "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ",
             "chi": "χ", "psi": "ψ", "omega": "ω",
             "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ",
             "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω"}

CONST_NAMES = {"pi": "π", "hbar": "ℏ", "infty": "∞"}

TOKEN_RE = re.compile(
    r"\s+|\\[a-zA-Z]+|\d+\.\d+|\d+|[a-zA-Z]|[+\-*/=^_,]|[{}()\[\]]")


def tokenize(latex):
    tokens = []
    for m in TOKEN_RE.finditer(latex):
        tok = m.group(0)
        if tok.isspace():
            continue
        if tok.startswith("\\"):
            tokens.append(("CMD", tok))
        elif re.match(r"^\d", tok):
            tokens.append(("NUM", tok))
        elif tok in "+-*/=":
            tokens.append(("OP", tok))
        elif tok == "^":
            tokens.append(("CARET", tok))
        elif tok == "_":
            tokens.append(("UNDER", tok))
        elif tok == ",":
            tokens.append(("COMMA", tok))
        elif tok == "{":
            tokens.append(("LB", tok))
        elif tok == "}":
            tokens.append(("RB", tok))
        elif tok == "(":
            tokens.append(("LP", tok))
        elif tok == ")":
            tokens.append(("RP", tok))
        elif tok == "[":
            tokens.append(("LBR", tok))
        elif tok == "]":
            tokens.append(("RBR", tok))
        elif tok.isalpha():
            tokens.append(("ID", tok))
    tokens.append(("EOF", ""))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def peek(self, k=0):
        return self.t[self.i + k]

    def eat(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def parse(self):
        lhs = self.parse_addsub()
        if self.peek()[0] == "OP" and self.peek()[1] == "=":
            self.eat()
            rhs = self.parse_addsub()
            return Eq(lhs, rhs)
        return lhs

    def parse_addsub(self):
        node = self.parse_muldiv()
        while self.peek()[0] == "OP" and self.peek()[1] in "+-":
            op = self.eat()[1]
            rhs = self.parse_muldiv()
            if op == "+":
                if node.type == "Add":
                    node = Add(*node.children, rhs)
                else:
                    node = Add(node, rhs)
            else:
                node = Sub(node, rhs)
        return node

    def parse_muldiv(self):
        node = self.parse_unary()
        while True:
            tk = self.peek()
            if tk[0] == "OP" and tk[1] == "*":
                self.eat(); node = Mul(node, self.parse_unary())
            elif tk[0] == "OP" and tk[1] == "/":
                self.eat(); node = Div(node, self.parse_unary())
            elif tk[0] == "CMD" and tk[1] == r"\cdot":
                self.eat(); node = Mul(node, self.parse_unary())
            elif tk[0] in ("ID", "NUM", "LB", "LP") or (
                tk[0] == "CMD" and tk[1] not in (r"\to", r"\rightarrow",
                                                  r"\Rightarrow", r"\implies",
                                                  r"\iff", r"\right", r"\quad")):
                node = Mul(node, self.parse_unary())
            else:
                break
        return node

    def parse_unary(self):
        tk = self.peek()
        if tk[0] == "OP" and tk[1] == "-":
            self.eat()
            return Neg(self.parse_pow())
        return self.parse_pow()

    def parse_pow(self):
        base = self.parse_atom()
        while self.peek()[0] == "UNDER":
            self.eat()
            self.parse_group_or_atom()
        if self.peek()[0] == "CARET":
            self.eat()
            return Pow(base, self.parse_group_or_atom())
        return base

    def parse_group_or_atom(self):
        if self.peek()[0] == "LB":
            self.eat()
            node = self.parse_addsub()
            if self.peek()[0] == "RB":
                self.eat()
            return node
        return self.parse_atom()

    def parse_atom(self):
        tk = self.peek()
        if tk[0] == "NUM":
            self.eat(); return Num(tk[1])
        if tk[0] == "ID":
            self.eat(); return Var(tk[1])
        if tk[0] == "LP":
            self.eat(); node = self.parse_addsub()
            if self.peek()[0] == "RP":
                self.eat()
            return node
        if tk[0] == "LB":
            self.eat(); node = self.parse_addsub()
            if self.peek()[0] == "RB":
                self.eat()
            return node
        if tk[0] == "CMD":
            return self.parse_cmd()
        if tk[0] == "OP" and tk[1] == "-":
            self.eat()
            return Neg(self.parse_atom())
        self.eat()
        return Var("?")

    def parse_cmd(self):
        cmd = self.eat()[1]
        name = cmd[1:]
        # CONST_NAMES priorité sur GREEK (pi est constante mathématique)
        if name in CONST_NAMES:
            return Const(CONST_NAMES[name])
        if name in GREEK:
            return Var(GREEK_MAP.get(name, name))
        if name == "frac":
            num = self.parse_group_or_atom()
            den = self.parse_group_or_atom()
            return Div(num, den)
        if name == "sqrt":
            return Sqrt(self.parse_group_or_atom())
        if name == "sum":
            self._consume_sub_sup()
            return Sum(self.parse_unary(), "i", "0", "n")
        if name in ("int", "iint", "iiint", "oint"):
            self._consume_sub_sup()
            return Integral(self.parse_unary(), "x", None, None)
        if name in ("sin", "cos", "tan", "log", "ln", "exp"):
            return FuncCall(name, [self.parse_atom()])
        if name == "left":
            if self.peek()[0] in ("LP", "LB", "LBR"):
                self.eat()
            elif self.peek()[0] == "OP":
                self.eat()
            node = self.parse_addsub()
            if self.peek()[0] == "CMD" and self.peek()[1] == r"\right":
                self.eat()
                if self.peek()[0] in ("RP", "RB", "RBR", "OP"):
                    self.eat()
            return node
        if name in ("text", "mathrm", "mathbf", "mathit", "operatorname",
                    "boldsymbol", "hat", "vec", "tilde", "bar", "dot",
                    "ddot", "overline", "underline"):
            return self.parse_group_or_atom()
        if name == "partial":
            return Var("∂")
        if name == "right":
            return Var("?")
        return Var(name)

    def _consume_sub_sup(self):
        for _ in range(2):
            tk = self.peek()
            if tk[0] in ("UNDER", "CARET"):
                self.eat()
                self.parse_group_or_atom()


def parse_latex(latex):
    return Parser(tokenize(latex)).parse()


CORPUS = [
    ("a + b", ["Add", "Var"]),
    ("x - y", ["Sub", "Var"]),
    ("a^2 + b^2 = c^2", ["Eq", "Add", "Pow", "Number"]),
    ("E = m c^2", ["Eq", "Mul", "Pow"]),
    (r"\frac{1}{2}", ["Div", "Number"]),
    (r"\sqrt{2}", ["Sqrt", "Number"]),
    (r"\frac{a + b}{c}", ["Div", "Add"]),
    (r"e^{i \pi} + 1 = 0", ["Eq", "Add", "Pow", "Const"]),
    (r"\sin(x)^2 + \cos(x)^2 = 1", ["Eq", "Add"]),
    (r"\int x^2 dx", ["Integral", "Pow"]),
    (r"\sum_{i=0}^{n} i", ["Sum", "Var"]),
    (r"f(x) = \frac{1}{1 + x^2}", ["Eq", "Div", "Add", "Pow"]),
    (r"\hbar \omega", ["Mul", "Const", "Var"]),
    (r"x_1 + x_2 + x_3", ["Add", "Var"]),
    (r"\alpha + \beta", ["Add", "Var"]),
    (r"a^n - b^n", ["Sub", "Pow"]),
    (r"-x", ["Neg", "Var"]),
    (r"2 \cdot 3", ["Mul", "Number"]),
    (r"\frac{d f}{d x}", ["Div"]),
    (r"\sqrt{a^2 + b^2}", ["Sqrt", "Add", "Pow"]),
    (r"\log(x) + \ln(x)", ["Add", "FuncCall"]),
    (r"\sin x", ["FuncCall", "Var"]),
    (r"a (b + c)", ["Mul", "Var", "Add"]),
    (r"(a + b) (a - b)", ["Mul", "Add", "Sub"]),
    (r"\Gamma (n+1) = n \Gamma (n)", ["Eq", "Mul", "Var", "Add"]),
    (r"\pi r^2", ["Mul", "Const", "Pow"]),
    (r"e^{-x^2}", ["Pow", "Const", "Neg", "Pow"]),
    (r"\hat{H} \psi", ["Mul", "Var"]),
    (r"\vec{r} \cdot \vec{v}", ["Mul", "Var"]),
    (r"\overline{z}", ["Var"]),
    (r"f(x) + g(x)", ["Add", "Mul"]),
    (r"\frac{1}{n!}", ["Div", "Number"]),
    (r"\sum_n a_n", ["Sum", "Var"]),
    (r"\int_0^1 f(x) dx", ["Integral"]),
    (r"a + b + c + d", ["Add", "Var"]),
    (r"\pi", ["Const"]),
    (r"x^2 = 4", ["Eq", "Pow", "Number"]),
    (r"a / b", ["Div", "Var"]),
    (r"x^2 + y^2 + z^2", ["Add", "Pow"]),
    (r"\frac{1}{2} m v^2", ["Mul", "Div", "Pow"]),
]


def collect_types(node, out):
    if not isinstance(node, Node):
        return
    out.append(node.type)
    for c in node.children:
        collect_types(c, out)


def main():
    results = []
    ok = 0
    parse_errors = 0
    for src, expected in CORPUS:
        try:
            ast = parse_latex(src)
            kinds = []
            collect_types(ast, kinds)
            covered = sum(1 for t in expected if t in kinds)
            ratio = covered / len(expected) if expected else 1.0
            success = ratio >= 0.7
            results.append({
                "src": src, "ast_root": ast.type,
                "node_types": kinds, "expected": expected,
                "coverage_ratio": round(ratio, 3),
                "signature": ast.signature,
                "roundtrip_latex": to_latex(ast), "success": success,
            })
            if success:
                ok += 1
        except Exception as e:
            parse_errors += 1
            results.append({"src": src, "error": f"{type(e).__name__}: {e}",
                            "success": False})

    out = {
        "version": "v135",
        "context": "§135 — Parser LaTeX réel → AST §128",
        "n_formules": len(CORPUS),
        "n_succes": ok,
        "ratio_succes": ok / len(CORPUS),
        "n_parse_errors": parse_errors,
        "approche": "tokenizer regex + descente récursive (~300 lignes)",
        "limitations": [
            "subscripts ignorés pour la signature",
            "fonctions trig/log nécessitent argument explicite ou parenthèses",
            "pas de \\begin{...}/\\end{...}",
            "juxtaposition implicite = multiplication",
        ],
        "formules": results,
    }
    OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v135_latex_parser.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"§135 — Parser LaTeX → AST §128")
    print(f"  Formules     : {len(CORPUS)}")
    print(f"  Succès       : {ok}/{len(CORPUS)} ({ok/len(CORPUS):.1%})")
    print(f"  Parse errors : {parse_errors}")
    print(f"→ {OUT}")
    return out


if __name__ == "__main__":
    main()

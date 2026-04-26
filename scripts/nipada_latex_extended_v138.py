"""
§138 — Parser LaTeX étendu : environnements `align`, `cases`, `matrix`,
`equation`, `aligned`, `pmatrix`, `bmatrix`. Stratégie : pré-processeur
qui découpe les environnements en sous-formules atomiques que §135
sait digérer, puis assemble en un Node racine de type `Block`/`Cases`/
`Matrix`.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec_v135 = importlib.util.spec_from_file_location(
    "_v135", ROOT / "scripts" / "nipada_latex_parser_v135.py")
_v135 = importlib.util.module_from_spec(spec_v135)
sys.modules["_v135"] = _v135
spec_v135.loader.exec_module(_v135)

Node = _v135.Node
parse_latex = _v135.parse_latex
collect_types = _v135.collect_types

ENV_RE = re.compile(
    r"\\begin\{(?P<env>[a-zA-Z*]+)\}(?P<body>.*?)\\end\{(?P=env)\}",
    re.DOTALL)


def _strip_label(s: str) -> str:
    return re.sub(r"\\label\{[^}]*\}", "", s)


def _split_rows(body: str) -> list[str]:
    # Split on \\ but not on \\\\ inside groups (rough)
    return [r.strip() for r in re.split(r"\\\\\s*", body) if r.strip()]


def _split_cells(row: str) -> list[str]:
    # Split on & but not on escaped \&
    return [c.strip() for c in re.split(r"(?<!\\)&", row)]


def parse_extended(latex: str) -> Node:
    """Parse top-level. Si environnement détecté, on assemble un Node block."""
    latex = _strip_label(latex.strip())
    m = ENV_RE.fullmatch(latex)
    if not m:
        # Pas d'environnement top-level — utilise §135 directement
        return parse_latex(latex)

    env = m.group("env")
    body = m.group("body").strip()

    if env in ("equation", "equation*", "split"):
        return parse_extended(body)  # transparent

    if env in ("align", "align*", "alignat", "alignat*", "gather", "gather*",
               "multline", "multline*", "eqnarray", "eqnarray*", "aligned"):
        rows = _split_rows(body)
        children = []
        for r in rows:
            # Aligne sur & : on enlève les & pour reformer une équation propre
            cleaned = r.replace("&", " ")
            try:
                children.append(parse_latex(cleaned))
            except Exception:
                children.append(Node("ParseError", attrs={"src": cleaned}))
        return Node("Block", children=children, attrs={"env": env,
                                                        "n_lines": len(rows)})

    if env in ("cases", "dcases", "rcases"):
        rows = _split_rows(body)
        branches = []
        for r in rows:
            cells = _split_cells(r)
            expr = cells[0] if cells else ""
            cond = cells[1] if len(cells) > 1 else ""
            try:
                expr_node = parse_latex(expr) if expr else Node("Empty")
            except Exception:
                expr_node = Node("ParseError", attrs={"src": expr})
            branches.append(Node("Case", children=[expr_node],
                                    attrs={"condition": cond}))
        return Node("Cases", children=branches,
                    attrs={"env": env, "n_branches": len(rows)})

    if env in ("matrix", "pmatrix", "bmatrix", "Bmatrix", "vmatrix",
               "Vmatrix", "smallmatrix", "array"):
        rows = _split_rows(body)
        matrix_rows = []
        for r in rows:
            # Pour 'array', la 1e ligne peut être un spec de colonnes — tolérer
            cells = _split_cells(r)
            cell_nodes = []
            for c in cells:
                try:
                    cell_nodes.append(parse_latex(c) if c else Node("Empty"))
                except Exception:
                    cell_nodes.append(Node("ParseError", attrs={"src": c}))
            matrix_rows.append(Node("Row", children=cell_nodes))
        n_cols = max((len(_split_cells(r)) for r in rows), default=0)
        return Node("Matrix", children=matrix_rows,
                    attrs={"env": env, "n_rows": len(rows), "n_cols": n_cols})

    # Environnement inconnu → tente parse direct du body
    try:
        return parse_latex(body)
    except Exception:
        return Node("UnknownEnv", attrs={"env": env, "src": body})


CORPUS = [
    # align
    (r"\begin{align} a + b &= c \\ x - y &= z \end{align}",
        ["Block", "Eq"], 2),
    (r"\begin{align*} f(x) &= x^2 \\ g(x) &= x^3 \end{align*}",
        ["Block", "Eq", "Pow"], 2),
    (r"\begin{align} E &= m c^2 \\ F &= m a \end{align}",
        ["Block", "Eq", "Mul"], 2),
    # cases
    (r"\begin{cases} x & \text{if } x \geq 0 \\ -x & \text{otherwise} \end{cases}",
        ["Cases", "Case"], 2),
    (r"\begin{cases} 1 & x = 0 \\ 0 & x \neq 0 \end{cases}",
        ["Cases", "Case"], 2),
    # matrix
    (r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
        ["Matrix", "Row"], 4),
    (r"\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}",
        ["Matrix", "Row", "Number"], 4),
    (r"\begin{matrix} x & y & z \\ a & b & c \end{matrix}",
        ["Matrix", "Row", "Var"], 6),
    # equation/aligned (transparent)
    (r"\begin{equation} a^2 + b^2 = c^2 \end{equation}",
        ["Eq", "Add", "Pow"], 1),
    (r"\begin{aligned} a + b &= c \end{aligned}",
        ["Block", "Eq"], 1),
    # gather
    (r"\begin{gather} x = 1 \\ y = 2 \end{gather}",
        ["Block", "Eq"], 2),
    # multiligne avec mix
    (r"\begin{align} \nabla \cdot E &= \rho \\ \nabla \cdot B &= 0 \end{align}",
        ["Block", "Eq"], 2),
    # cas Vmatrix
    (r"\begin{Vmatrix} 1 & 0 \\ 0 & -1 \end{Vmatrix}",
        ["Matrix", "Row"], 4),
    # equation simple sans env
    (r"a + b = c", ["Eq", "Add", "Var"], 1),
    # cases imbriqué dans equation
    (r"\begin{equation} f(x) = x^2 + 1 \end{equation}",
        ["Eq", "Add", "Pow"], 1),
]


def main():
    results = []
    ok = 0
    for src, expected_types, expected_count in CORPUS:
        try:
            ast_node = parse_extended(src)
            kinds = []
            collect_types(ast_node, kinds)
            covered = sum(1 for t in expected_types if t in kinds)
            ratio = covered / len(expected_types) if expected_types else 1.0
            # Pour Block/Matrix/Cases, valider aussi la structure de comptage
            count_ok = True
            if ast_node.type == "Block":
                count_ok = ast_node.attrs.get("n_lines") == expected_count
            elif ast_node.type == "Cases":
                count_ok = ast_node.attrs.get("n_branches") == expected_count
            elif ast_node.type == "Matrix":
                rows = ast_node.attrs.get("n_rows", 0)
                cols = ast_node.attrs.get("n_cols", 0)
                count_ok = rows * cols == expected_count
            success = ratio >= 0.7 and count_ok
            results.append({
                "src": src[:80],
                "ast_root": ast_node.type,
                "node_types_sample": kinds[:10],
                "expected_types": expected_types,
                "coverage_ratio": round(ratio, 3),
                "structural_count_ok": count_ok,
                "success": success,
            })
            if success:
                ok += 1
        except Exception as e:
            results.append({"src": src[:80],
                            "error": f"{type(e).__name__}: {e}",
                            "success": False})

    out = {
        "version": "v138",
        "context": ("§138 — Parser LaTeX étendu : align/cases/matrix/equation/"
                    "aligned/gather/multline/Vmatrix/etc."),
        "n_formules": len(CORPUS),
        "n_succes": ok,
        "ratio_succes": ok / len(CORPUS),
        "approche": ("pré-processeur regex qui détecte \\begin{env}…\\end{env} "
                     "top-level, découpe en lignes/cellules, délègue chaque "
                     "fragment à §135, assemble en Node Block/Cases/Matrix"),
        "limitations": [
            "environnements imbriqués top-level seulement (pas de matrix dans align)",
            "spec de colonnes de array ignoré",
            "\\text{...} dans cases conservé brut comme condition",
            "& dans \\frac{a&b}{...} traité naïvement — fragile",
        ],
        "formules": results,
    }
    OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v138_latex_extended.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"§138 — Parser LaTeX étendu (environnements)")
    print(f"  Formules : {len(CORPUS)}")
    print(f"  Succès   : {ok}/{len(CORPUS)} ({ok/len(CORPUS):.1%})")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

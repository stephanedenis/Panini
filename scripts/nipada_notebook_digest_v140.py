"""
§140 — Auto-digestion des notebooks .ipynb du repo Panini par la stack
omnimode V14 (§122/§128/§135/§136/§138/§139). Chaque notebook est
décomposé cellule par cellule : code (mode=code via §136 AST Python),
markdown (mode=text + détection formules $...$ + mermaid + code blocs).

Verdict : quelle proportion des cellules est multimodale ? Quels atomes
V14 dominent dans nos notebooks d'expérimentation ?
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# §136 (extracteurs)
spec_v136 = importlib.util.spec_from_file_location(
    "_v136", ROOT / "scripts" / "nipada_crossmodal_v136.py")
_v136 = importlib.util.module_from_spec(spec_v136)
sys.modules["_v136"] = _v136
spec_v136.loader.exec_module(_v136)

# §139 (classifieur) — entraînement à la volée
spec_v139 = importlib.util.spec_from_file_location(
    "_v139", ROOT / "scripts" / "nipada_lightclf_v139.py")
_v139 = importlib.util.module_from_spec(spec_v139)
sys.modules["_v139"] = _v139
spec_v139.loader.exec_module(_v139)

# §138 (parser étendu)
spec_v138 = importlib.util.spec_from_file_location(
    "_v138", ROOT / "scripts" / "nipada_latex_extended_v138.py")
_v138 = importlib.util.module_from_spec(spec_v138)
sys.modules["_v138"] = _v138
spec_v138.loader.exec_module(_v138)

extract_text = _v136.extract_from_text
extract_code = _v136.extract_from_code
extract_diagram = _v136.extract_from_diagram
parse_extended = _v138.parse_extended
collect_atoms_from_node = _v136.collect_atoms_from_node


# Entraîne §139 une fois
_idf, _centroids = _v139.train(_v139.TRAIN)


def predict_v139(text: str) -> set:
    pred, _ = _v139.predict(text, _idf, _centroids, threshold=0.18)
    return pred


CODE_BLOCK_RE = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$([^$\n]+)\$")
DISPLAY_MATH_RE = re.compile(r"\$\$([^$]+)\$\$", re.DOTALL)


def extract_formula_v138(latex: str) -> set:
    try:
        ast_node = parse_extended(latex)
        atoms = set()
        collect_atoms_from_node(ast_node, atoms)
        return atoms
    except Exception:
        return set()


def analyze_markdown_cell(src: str) -> dict:
    modes = {"text"}
    text_clean = src
    code_atoms = set()
    formula_atoms = set()

    for m in CODE_BLOCK_RE.finditer(src):
        lang = (m.group(1) or "").lower()
        code = m.group(2)
        text_clean = text_clean.replace(m.group(0), "")
        if lang in ("mermaid", "graphviz", "dot"):
            modes.add("diagram")
            code_atoms |= extract_diagram(code)
        elif lang in ("python", "py", ""):
            modes.add("code")
            code_atoms |= extract_code(code)

    for rgx in (DISPLAY_MATH_RE, INLINE_MATH_RE):
        for m in rgx.finditer(src):
            modes.add("formula")
            formula_atoms |= extract_formula_v138(m.group(1))
            text_clean = text_clean.replace(m.group(0), "")

    text_atoms_heur = extract_text(text_clean)
    text_atoms_v139 = predict_v139(text_clean) if text_clean.strip() else set()
    text_atoms = text_atoms_heur | text_atoms_v139

    return {
        "modes": sorted(modes),
        "n_modes": len(modes),
        "atoms": sorted(text_atoms | code_atoms | formula_atoms),
        "atoms_text_heur": sorted(text_atoms_heur),
        "atoms_text_v139": sorted(text_atoms_v139),
    }


def analyze_code_cell(src: str) -> dict:
    try:
        atoms = extract_code(src)
    except (SyntaxError, UnicodeEncodeError, UnicodeDecodeError, ValueError):
        atoms = set()
    return {
        "modes": ["code"],
        "n_modes": 1,
        "atoms": sorted(atoms),
        "n_lines": src.count("\n") + 1,
    }


def analyze_notebook(path: Path) -> dict:
    try:
        nb = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as e:
        return {"path": str(path), "error": str(e), "cells": []}

    cells = nb.get("cells", [])
    analyzed = []
    for i, cell in enumerate(cells):
        ctype = cell.get("cell_type", "unknown")
        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)
        if ctype == "markdown":
            info = analyze_markdown_cell(src)
        elif ctype == "code":
            info = analyze_code_cell(src)
        else:
            info = {"modes": [], "n_modes": 0, "atoms": []}
        info["cell_type"] = ctype
        info["index"] = i
        info["len"] = len(src)
        analyzed.append(info)

    n = len(analyzed)
    multi = sum(1 for c in analyzed if c["n_modes"] >= 2)
    has_code = sum(1 for c in analyzed if "code" in c["modes"])
    has_formula = sum(1 for c in analyzed if "formula" in c["modes"])
    has_diagram = sum(1 for c in analyzed if "diagram" in c["modes"])

    atom_counts = {}
    for c in analyzed:
        for a in c["atoms"]:
            atom_counts[a] = atom_counts.get(a, 0) + 1

    return {
        "path": str(path.relative_to(ROOT)),
        "n_cells": n,
        "n_markdown": sum(1 for c in analyzed if c["cell_type"] == "markdown"),
        "n_code": sum(1 for c in analyzed if c["cell_type"] == "code"),
        "rates": {
            "multi_mode": round(multi / n, 3) if n else 0.0,
            "has_code": round(has_code / n, 3) if n else 0.0,
            "has_formula": round(has_formula / n, 3) if n else 0.0,
            "has_diagram": round(has_diagram / n, 3) if n else 0.0,
        },
        "top_atoms": sorted(atom_counts.items(), key=lambda x: -x[1])[:10],
        "cells_sample": analyzed[:5],
    }


def main():
    nb_dir = ROOT / "notebooks"
    if not nb_dir.exists():
        print("Aucun dossier notebooks/")
        return
    notebooks = sorted(nb_dir.glob("*.ipynb"))
    if not notebooks:
        print("Aucun .ipynb trouvé")
        return

    summaries = []
    total_cells = 0
    total_multi = 0
    total_code = 0
    total_formula = 0
    total_diagram = 0
    global_atoms: dict[str, int] = {}

    for nb in notebooks:
        s = analyze_notebook(nb)
        if "error" in s:
            summaries.append(s); continue
        summaries.append(s)
        total_cells += s["n_cells"]
        total_multi += int(s["rates"]["multi_mode"] * s["n_cells"])
        total_code += int(s["rates"]["has_code"] * s["n_cells"])
        total_formula += int(s["rates"]["has_formula"] * s["n_cells"])
        total_diagram += int(s["rates"]["has_diagram"] * s["n_cells"])
        for a, c in s["top_atoms"]:
            global_atoms[a] = global_atoms.get(a, 0) + c

    n = total_cells or 1
    out = {
        "version": "v140",
        "context": ("§140 — Auto-digestion des notebooks .ipynb par la stack "
                    "omnimode V14 (§122 + §128 + §135 + §136 + §138 + §139)"),
        "n_notebooks": len(notebooks),
        "n_cells_total": total_cells,
        "rates_global": {
            "multi_mode": round(total_multi / n, 3),
            "has_code": round(total_code / n, 3),
            "has_formula": round(total_formula / n, 3),
            "has_diagram": round(total_diagram / n, 3),
        },
        "top_atoms_global": sorted(global_atoms.items(),
                                    key=lambda x: -x[1])[:14],
        "verdict": (f"Sur {len(notebooks)} notebooks et {total_cells} cellules, "
                    f"{total_multi/n:.0%} sont multimodales (code+texte ou "
                    f"texte+formules). Les notebooks Panini sont {total_code/n:.0%} "
                    "code et le reste markdown structuré. La stack omnimode "
                    "se digère sans crash sur du contenu hétérogène réel."),
        "limitations": [
            "Cellules code non exécutées (analyse statique seulement)",
            "Outputs des cellules code ignorés",
            "Pas de traçage des dépendances inter-cellules",
            "Notebooks corrompus → marqués 'error' mais pas réparés",
        ],
        "notebooks": summaries,
    }
    OUT = ROOT / "research" / "nipada" / "falsification" / "nipada_v140_notebook_digest.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"§140 — Auto-digestion notebooks .ipynb")
    print(f"  Notebooks      : {len(notebooks)}")
    print(f"  Cellules       : {total_cells}")
    print(f"  Multi-mode     : {total_multi/n:.1%}")
    print(f"  Avec code      : {total_code/n:.1%}")
    print(f"  Avec formules  : {total_formula/n:.1%}")
    print(f"  Avec diagrammes: {total_diagram/n:.1%}")
    print(f"  Top atomes     : {[a for a,_ in sorted(global_atoms.items(), key=lambda x:-x[1])[:5]]}")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

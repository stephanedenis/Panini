#!/usr/bin/env python3
"""
nipada_lattice_svg.py — Visualisation SVG du treillis nipada

Génère un diagramme de Hasse coloré pour le domaine Z+ (16 concepts).

Principe de couleur :
  Chaque atome a une couleur primaire.
  Chaque molécule est la moyenne des couleurs de ses atomes constituants.
  → la couleur encode directement la composition sémantique.

Usage :
    python3 tech/nipada_lattice_svg.py [sortie.svg]
    # défaut : tech/nipada_lattice.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

# ── Données nipada ────────────────────────────────────────────────────────────

# 4 atomes : bit → (prime, nom, R, G, B)
ATOMS = {
    0: (2,  "ÊTRE",        230,  55,  42),   # rouge chaud
    1: (3,  "DIFFÉRENCE",   36,  85, 204),   # bleu profond
    2: (5,  "RAPPORT",      34, 170,  68),   # vert vif
    3: (7,  "ORIENTATION", 220, 140,  30),   # orange doré
}

# Concepts Z+ : mask → (nom, valeur nipada)
CONCEPTS: dict[int, tuple[str, int]] = {
    0:  ("PADDING",        1),
    1:  ("ÊTRE",           2),
    2:  ("DIFFÉRENCE",     3),
    4:  ("RAPPORT",        5),
    8:  ("ORIENTATION",    7),
    3:  ("EXISTENCE",      6),
    5:  ("COMPOSITION",   10),
    6:  ("MESURE",        15),
    9:  ("DEVENIR",       14),
    10: ("OPPOSITION",    21),
    12: ("RÉFÉRENCE",     35),
    7:  ("VIE",           30),
    11: ("TRANSFORMATION",42),
    13: ("INTENTION",     70),
    14: ("TEMPS",        105),
    15: ("INTÉGRATION",  210),
}

# ── Géométrie ─────────────────────────────────────────────────────────────────

SVG_W   = 920
SVG_H   = 680
NODE_R  = 36

# Positions x des 4 atomes (axe horizontal = espace conceptuel)
ATOM_X = {0: 155, 1: 355, 2: 565, 3: 755}

# Y par niveau (0 = PADDING en bas, 4 = INTÉGRATION en haut)
LEVEL_Y = {0: 618, 1: 498, 2: 368, 3: 238, 4: 110}

# Ajustement manuel pour les 2 paires qui partagent le même centroïde x=460
_X_OVERRIDE = {
    9:  435,   # DEVENIR  (0,3) : centroïde naturel = (155+755)/2 = 455 → décalé
    6:  485,   # MESURE   (1,2) : centroïde naturel = (355+565)/2 = 460 → décalé
}


def _centroid_x(mask: int) -> float:
    bits = [b for b in range(4) if mask & (1 << b)]
    return sum(ATOM_X[b] for b in bits) / len(bits)


def node_xy(mask: int) -> tuple[float, float]:
    lvl = bin(mask).count("1")
    y   = float(LEVEL_Y[lvl])
    if mask == 0:
        x = (ATOM_X[0] + ATOM_X[3]) / 2   # centré
    elif mask in _X_OVERRIDE:
        x = float(_X_OVERRIDE[mask])
    else:
        x = _centroid_x(mask)
    return x, y


# ── Couleurs ──────────────────────────────────────────────────────────────────

def atom_rgb(bit: int) -> tuple[int, int, int]:
    _, _, r, g, b = ATOMS[bit]
    return r, g, b


def concept_rgb(mask: int) -> tuple[int, int, int]:
    if mask == 0:
        return (210, 210, 210)
    bits = [b for b in range(4) if mask & (1 << b)]
    r = round(sum(atom_rgb(b)[0] for b in bits) / len(bits))
    g = round(sum(atom_rgb(b)[1] for b in bits) / len(bits))
    b = round(sum(atom_rgb(b)[2] for b in bits) / len(bits))
    return r, g, b


def css_rgb(rgb: tuple[int, int, int]) -> str:
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (x / 255 for x in rgb)
    return 0.299 * r + 0.587 * g + 0.114 * b


def text_fg(rgb: tuple[int, int, int]) -> str:
    return "#ffffff" if luminance(rgb) < 0.50 else "#1a1a1a"


def darken(rgb: tuple[int, int, int], factor: float = 0.65) -> tuple[int, int, int]:
    return tuple(round(c * factor) for c in rgb)  # type: ignore[return-value]


# ── Treillis : arêtes directes (Hasse) ───────────────────────────────────────

def hasse_edges() -> list[tuple[int, int]]:
    """Arêtes directes : (lo, hi) telles que hi couvre lo (exactement 1 bit ajouté)."""
    edges = []
    for lo in range(16):
        for hi in range(16):
            diff = hi ^ lo
            if (hi & lo) == lo and diff != 0 and (diff & (diff - 1)) == 0:
                edges.append((lo, hi))
    return edges


# ── SVG éléments ──────────────────────────────────────────────────────────────

def e_rect(w: float, h: float, rx: int, fill: str) -> str:
    return f'  <rect width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'


def e_edge(lo: int, hi: int) -> str:
    x1, y1 = node_xy(lo)
    x2, y2 = node_xy(hi)
    dx, dy  = x2 - x1, y2 - y1
    dist    = math.hypot(dx, dy)
    if dist < 1:
        return ""
    ux, uy = dx / dist, dy / dist
    # Partir/arriver au bord du cercle
    sx, sy = x1 + ux * (NODE_R + 2), y1 + uy * (NODE_R + 2)
    ex, ey = x2 - ux * (NODE_R + 2), y2 - uy * (NODE_R + 2)
    # Couleur = mélange des deux concepts
    rgb_lo = concept_rgb(lo)
    rgb_hi = concept_rgb(hi)
    r = (rgb_lo[0] + rgb_hi[0]) // 2
    g = (rgb_lo[1] + rgb_hi[1]) // 2
    b = (rgb_lo[2] + rgb_hi[2]) // 2
    color = f"rgb({r},{g},{b})"
    return (
        f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        f'stroke="{color}" stroke-width="2" opacity="0.45" stroke-linecap="round"/>'
    )


def e_node(mask: int) -> str:
    x, y = node_xy(mask)
    rgb   = concept_rgb(mask)
    fill  = css_rgb(rgb)
    stroke = css_rgb(darken(rgb))
    fg    = text_fg(rgb)
    name, val = CONCEPTS[mask]
    # Taille de police adaptative
    fs_name = 9 if len(name) > 12 else (10 if len(name) > 8 else 11)
    lines = [
        f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>',
        f'  <text x="{x:.1f}" y="{y - 5:.1f}" text-anchor="middle" '
        f'font-size="{fs_name}" font-family="sans-serif" font-weight="bold" fill="{fg}">'
        f'{name}</text>',
        f'  <text x="{x:.1f}" y="{y + 11:.1f}" text-anchor="middle" '
        f'font-size="9" font-family="monospace" fill="{fg}" opacity="0.80">'
        f'={val}</text>',
    ]
    return "\n".join(lines)


def e_legend() -> str:
    lx, ly = 20, 160
    out = [
        f'  <rect x="{lx - 8}" y="{ly - 28}" width="138" height="144" '
        f'rx="6" fill="#ffffff" fill-opacity="0.7" stroke="#ccc" stroke-width="1"/>',
        f'  <text x="{lx}" y="{ly - 10}" font-size="10" font-family="sans-serif" '
        f'font-weight="bold" fill="#444">ATOMES</text>',
    ]
    for bit in range(4):
        _, aname, r, g, b = ATOMS[bit]
        rgb   = (r, g, b)
        fill  = css_rgb(rgb)
        stroke = css_rgb(darken(rgb))
        fg    = text_fg(rgb)
        cy    = ly + bit * 28
        cx    = lx + 13
        prime = ATOMS[bit][0]
        out += [
            f'  <circle cx="{cx}" cy="{cy}" r="13" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.5"/>',
            f'  <text x="{cx}" y="{cy - 3}" text-anchor="middle" '
            f'font-size="8" font-family="monospace" font-weight="bold" fill="{fg}">'
            f'bit{bit}</text>',
            f'  <text x="{cx}" y="{cy + 8}" text-anchor="middle" '
            f'font-size="7" font-family="monospace" fill="{fg}">{prime}↑</text>',
            f'  <text x="{cx + 19}" y="{cy + 4}" font-size="10" '
            f'font-family="sans-serif" fill="#333">{aname}</text>',
        ]

    # Niveaux
    lyl = ly + 140
    out += [
        f'  <rect x="{lx - 8}" y="{lyl - 20}" width="138" height="120" '
        f'rx="6" fill="#ffffff" fill-opacity="0.7" stroke="#ccc" stroke-width="1"/>',
        f'  <text x="{lx}" y="{lyl - 4}" font-size="10" font-family="sans-serif" '
        f'font-weight="bold" fill="#444">NIVEAUX</text>',
    ]
    levels = [
        (0, "L0 — padding"),
        (1, "L1 — atomes (4)"),
        (2, "L2 — paires (6)"),
        (3, "L3 — triples (4)"),
        (4, "L4 — tétrade (1)"),
    ]
    for i, (lvl, label) in enumerate(levels):
        out.append(
            f'  <text x="{lx}" y="{lyl + 16 + i * 18}" font-size="9" '
            f'font-family="sans-serif" fill="#555">{label}</text>'
        )

    return "\n".join(out)


def e_level_guides() -> str:
    """Lignes horizontales légères indiquant chaque niveau."""
    out = []
    labels = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4"}
    for lvl, y in LEVEL_Y.items():
        out.append(
            f'  <line x1="140" y1="{y:.0f}" x2="{SVG_W - 20}" y2="{y:.0f}" '
            f'stroke="#e0e0e0" stroke-width="1" stroke-dasharray="4 6"/>'
        )
        out.append(
            f'  <text x="128" y="{y + 4:.0f}" text-anchor="end" font-size="9" '
            f'font-family="monospace" fill="#bbb">{labels[lvl]}</text>'
        )
    return "\n".join(out)


# ── Assemblage final ──────────────────────────────────────────────────────────

def generate_svg() -> str:
    parts: list[str] = []

    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_W}" height="{SVG_H}" '
        f'viewBox="0 0 {SVG_W} {SVG_H}">'
    )

    # Fond
    parts.append(e_rect(SVG_W, SVG_H, 10, "#F5F6F8"))

    # Titre
    parts.append(
        f'  <text x="{SVG_W // 2}" y="38" text-anchor="middle" '
        f'font-size="19" font-family="sans-serif" font-weight="bold" fill="#222">'
        f'Treillis nipada — Domaine Z⁺</text>'
    )
    parts.append(
        f'  <text x="{SVG_W // 2}" y="58" text-anchor="middle" '
        f'font-size="11" font-family="sans-serif" fill="#888">'
        f'16 concepts · 4 atomes · algèbre de Grassmann sur {{2,3,5,7}} · diagramme de Hasse</text>'
    )

    # Guides de niveau
    parts.append(e_level_guides())

    # Arêtes (sous les nœuds)
    for lo, hi in hasse_edges():
        parts.append(e_edge(lo, hi))

    # Nœuds
    for mask in range(16):
        parts.append(e_node(mask))

    # Légende
    parts.append(e_legend())

    parts.append("</svg>")
    return "\n".join(parts)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_path = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path(__file__).parent / "nipada_lattice.svg"
    )
    svg_content = generate_svg()
    out_path.write_text(svg_content, encoding="utf-8")
    print(f"SVG généré : {out_path}  ({len(svg_content)} octets)")
    # Résumé
    print(f"  {len(CONCEPTS)} concepts · {len(hasse_edges())} arêtes Hasse")
    print(f"  Dimensions : {SVG_W}×{SVG_H}px · rayons nœuds : {NODE_R}px")

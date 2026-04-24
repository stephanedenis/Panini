#!/usr/bin/env python3
"""
nipada_viz_gallery.py — 5 approches de visualisation nipada en SVG couleur

Génère dans tech/ :
  1. nipada_zneg_duality.svg  — Treillis double Z+ / Z- (miroir)
  2. nipada_grid_4x4.svg      — Projection hypercube 4D→grille 4×4
  3. nipada_radial.svg        — Disposition radiale/sunburst par niveau
  4. nipada_jaccard.svg       — Heatmap Jaccard 15×15
  5. nipada_expressions.svg   — 5 expressions de test en timeline colorée

Usage :
    python3 tech/nipada_viz_gallery.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ─────────────────────────────────────────────────────────────────────────────
# Données nipada canoniques
# ─────────────────────────────────────────────────────────────────────────────

PRIMES = (2, 3, 5, 7)
ATOM_NAMES = ("ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION")
# Couleurs atomes : ÊTRE=rouge, DIFFÉRENCE=bleu, RAPPORT=vert, ORIENTATION=or
ATOM_RGB = {
    0: (230,  55,  42),
    1: ( 36,  85, 204),
    2: ( 34, 170,  68),
    3: (220, 140,  30),
}

# Domaine Z+
ZPOS: dict[int, tuple[str, int]] = {
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

# Domaine Z- : same mask, negative/crossing semantics
ZNEG: dict[int, tuple[str, int]] = {
    1:  ("NÉANT",           -2),
    2:  ("IDENTITÉ",        -3),
    4:  ("RUPTURE",         -5),
    8:  ("DÉRIVE",          -7),
    3:  ("IRRÉEL",          -6),
    5:  ("SÉPARATION",     -10),
    6:  ("INCOMMENSURABLE",-15),
    9:  ("PERMANENCE",     -14),
    10: ("PAIX",           -21),
    12: ("ANTICIPATION",   -35),
    7:  ("MORT",           -30),
    11: ("STASE",          -42),
    13: ("ABANDON",        -70),
    14: ("ÉTERNITÉ",      -105),
    15: ("FRAGMENTATION", -210),
}

# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires couleur
# ─────────────────────────────────────────────────────────────────────────────

def concept_rgb(mask: int) -> tuple[int, int, int]:
    if mask == 0:
        return (200, 200, 200)
    bits = [b for b in range(4) if mask & (1 << b)]
    r = round(sum(ATOM_RGB[b][0] for b in bits) / len(bits))
    g = round(sum(ATOM_RGB[b][1] for b in bits) / len(bits))
    b = round(sum(ATOM_RGB[b][2] for b in bits) / len(bits))
    return (r, g, b)


def desaturate(rgb: tuple[int, int, int], factor: float = 0.35) -> tuple[int, int, int]:
    """Désature et assombrit pour le domaine Z-."""
    lum = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    r = round(rgb[0] * factor + lum * (1 - factor))
    g = round(rgb[1] * factor + lum * (1 - factor))
    b = round(rgb[2] * factor + lum * (1 - factor))
    # Assombrir légèrement
    return (round(r * 0.75), round(g * 0.75), round(b * 0.75))


def darken(rgb: tuple[int, int, int], f: float = 0.6) -> tuple[int, int, int]:
    return (round(rgb[0] * f), round(rgb[1] * f), round(rgb[2] * f))


def luminance(rgb: tuple[int, int, int]) -> float:
    return 0.299 * rgb[0] / 255 + 0.587 * rgb[1] / 255 + 0.114 * rgb[2] / 255


def fg(rgb: tuple[int, int, int]) -> str:
    return "#ffffff" if luminance(rgb) < 0.50 else "#1a1a1a"


def css(rgb: tuple[int, int, int]) -> str:
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"


def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float = 0.5) -> tuple[int, int, int]:
    return (round(a[0] * (1-t) + b[0] * t), round(a[1] * (1-t) + b[1] * t), round(a[2] * (1-t) + b[2] * t))


def jaccard(ma: int, mb: int) -> float:
    inter = bin(ma & mb).count("1")
    union = bin(ma | mb).count("1")
    return inter / union if union else 0.0


def hasse_edges_up() -> list[tuple[int, int]]:
    """Arêtes directes ascendantes (lo → hi, un bit ajouté)."""
    edges = []
    for lo in range(16):
        for hi in range(16):
            diff = hi ^ lo
            if (hi & lo) == lo and diff != 0 and (diff & (diff - 1)) == 0:
                edges.append((lo, hi))
    return edges


HASSE = hasse_edges_up()


# ─────────────────────────────────────────────────────────────────────────────
# SVG 1 — Dualité Z+ / Z- (Hasse miroir)
# ─────────────────────────────────────────────────────────────────────────────

def svg_zneg_duality() -> str:
    W, H = 960, 880
    # Z+ : y de 80 (L4 INTÉGRATION) à 400 (L0 PADDING)
    # Axe miroir : y=460
    # Z- : y de 520 (L0) à 840 (L4 FRAGMENTATION)
    NR = 32

    LEVEL_Y_POS = {4: 90, 3: 200, 2: 305, 1: 405, 0: 488}
    LEVEL_Y_NEG = {4: 790, 3: 680, 2: 575, 1: 475, 0: 392}
    ATOM_X = {0: 170, 1: 370, 2: 590, 3: 790}

    def node_x(mask: int) -> float:
        if mask == 0:
            return (ATOM_X[0] + ATOM_X[3]) / 2
        bits = [b for b in range(4) if mask & (1 << b)]
        return sum(ATOM_X[b] for b in bits) / len(bits)

    # Corrections pour éviter superpositions au niveau 2
    X_CORR = {9: 440, 6: 500}

    def get_x(mask: int) -> float:
        return float(X_CORR.get(mask, node_x(mask)))

    def get_y_pos(mask: int) -> float:
        return float(LEVEL_Y_POS[bin(mask).count("1")])

    def get_y_neg(mask: int) -> float:
        return float(LEVEL_Y_NEG[bin(mask).count("1")])

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" rx="10" fill="#1a1a2e"/>',
        # Titre
        f'  <text x="{W//2}" y="38" text-anchor="middle" font-size="18" font-family="sans-serif" '
        f'font-weight="bold" fill="#e8e8f0">Dualité nipada — Z⁺ (positif) · Z⁻ (crossings)</text>',
        # Sous-titre
        f'  <text x="{W//2}" y="57" text-anchor="middle" font-size="10" font-family="sans-serif" '
        f'fill="#6a6a8a">Chaque Z⁺ a son crossing Z⁻ (négation Spencer-Brown)</text>',
        # Labels domaines
        f'  <text x="28" y="295" text-anchor="start" font-size="13" font-family="sans-serif" '
        f'font-weight="bold" fill="#ccddff" opacity="0.7">Z⁺</text>',
        f'  <text x="28" y="595" text-anchor="start" font-size="13" font-family="sans-serif" '
        f'font-weight="bold" fill="#ffcccc" opacity="0.7">Z⁻</text>',
        # Axe miroir
        f'  <line x1="80" y1="440" x2="{W-20}" y2="440" stroke="#44446a" stroke-width="1.5" stroke-dasharray="8 6"/>',
        f'  <text x="{W//2}" y="436" text-anchor="middle" font-size="9" font-family="sans-serif" '
        f'fill="#44446a">⊣  crossing  ⊢</text>',
    ]

    # Lignes de crossing entre Z+ et Z- (1 ligne entre miroirs)
    for mask in range(1, 16):
        x = get_x(mask)
        y_top = get_y_pos(mask)
        y_bot = get_y_neg(mask)
        rgb = concept_rgb(mask)
        mid_col = css(desaturate(rgb, 0.3))
        lines.append(
            f'  <line x1="{x:.0f}" y1="{y_top + NR + 1:.0f}" x2="{x:.0f}" y2="{y_bot - NR - 1:.0f}" '
            f'stroke="{mid_col}" stroke-width="1" opacity="0.25" stroke-dasharray="3 4"/>'
        )

    # Arêtes Hasse Z+
    for lo, hi in HASSE:
        x1, y1 = get_x(lo), get_y_pos(lo)
        x2, y2 = get_x(hi), get_y_pos(hi)
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1:
            continue
        ux, uy = dx/dist, dy/dist
        sx, sy = x1 + ux*(NR+2), y1 + uy*(NR+2)
        ex, ey = x2 - ux*(NR+2), y2 - uy*(NR+2)
        c1, c2 = concept_rgb(lo), concept_rgb(hi)
        col = css(blend(c1, c2))
        lines.append(
            f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{col}" stroke-width="1.8" opacity="0.55" stroke-linecap="round"/>'
        )

    # Arêtes Hasse Z- (inversé)
    for lo, hi in HASSE:
        x1, y1 = get_x(lo), get_y_neg(lo)
        x2, y2 = get_x(hi), get_y_neg(hi)
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1:
            continue
        ux, uy = dx/dist, dy/dist
        sx, sy = x1 + ux*(NR+2), y1 + uy*(NR+2)
        ex, ey = x2 - ux*(NR+2), y2 - uy*(NR+2)
        c1, c2 = desaturate(concept_rgb(lo)), desaturate(concept_rgb(hi))
        col = css(blend(c1, c2))
        lines.append(
            f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{col}" stroke-width="1.8" opacity="0.6" stroke-linecap="round"/>'
        )

    # Nœuds Z+
    for mask in range(16):
        x, y = get_x(mask), get_y_pos(mask)
        rgb = concept_rgb(mask)
        fill, stroke_col = css(rgb), css(darken(rgb))
        fg_col = fg(rgb)
        name, val = ZPOS[mask]
        fs = 8 if len(name) > 12 else (9 if len(name) > 8 else 10)
        lines += [
            f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{NR}" fill="{fill}" stroke="{stroke_col}" stroke-width="2"/>',
            f'  <text x="{x:.0f}" y="{y - 4:.0f}" text-anchor="middle" font-size="{fs}" '
            f'font-family="sans-serif" font-weight="bold" fill="{fg_col}">{name}</text>',
            f'  <text x="{x:.0f}" y="{y + 10:.0f}" text-anchor="middle" font-size="8" '
            f'font-family="monospace" fill="{fg_col}" opacity="0.75">={val}</text>',
        ]

    # Nœuds Z-
    for mask in range(1, 16):
        x, y = get_x(mask), get_y_neg(mask)
        rgb = desaturate(concept_rgb(mask))
        fill, stroke_col = css(rgb), css(darken(rgb))
        fg_col = fg(rgb)
        name, val = ZNEG[mask]
        fs = 7 if len(name) > 12 else (8 if len(name) > 8 else 9)
        lines += [
            f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{NR}" fill="{fill}" stroke="{stroke_col}" stroke-width="2"/>',
            f'  <text x="{x:.0f}" y="{y - 4:.0f}" text-anchor="middle" font-size="{fs}" '
            f'font-family="sans-serif" font-weight="bold" fill="{fg_col}">{name}</text>',
            f'  <text x="{x:.0f}" y="{y + 10:.0f}" text-anchor="middle" font-size="8" '
            f'font-family="monospace" fill="{fg_col}" opacity="0.75">={val}</text>',
        ]

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SVG 2 — Grille 4×4 (projection hypercube 4D→2D)
# ─────────────────────────────────────────────────────────────────────────────

def svg_grid_4x4() -> str:
    W, H = 720, 760
    CELL = 150
    OX, OY = 55, 110   # origine de la grille (coin haut-gauche)
    NR = 44

    def grid_xy(mask: int) -> tuple[float, float]:
        # X = bit0 + 2*bit2 (ÊTRE, RAPPORT)
        # Y = bit1 + 2*bit3 (DIFFÉRENCE, ORIENTATION)
        gx = (mask >> 0 & 1) * 1 + (mask >> 2 & 1) * 2
        gy = (mask >> 1 & 1) * 1 + (mask >> 3 & 1) * 2
        cx = OX + gx * CELL + CELL / 2
        cy = OY + gy * CELL + CELL / 2
        return cx, cy

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" rx="10" fill="#f0f2f6"/>',
        f'  <text x="{W//2}" y="34" text-anchor="middle" font-size="17" font-family="sans-serif" '
        f'font-weight="bold" fill="#222">Grille 4×4 — Projection hypercube nipada</text>',
        f'  <text x="{W//2}" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" '
        f'fill="#888">X = {{ÊTRE, RAPPORT}}  ·  Y = {{DIFFÉRENCE, ORIENTATION}}</text>',
    ]

    # Axes labels
    x_labels = ["∅", "ÊTRE", "RAPPORT", "ÊTRE\n+RAPPORT"]
    y_labels = ["∅", "DIFF", "ORIENT", "DIFF\n+ORIENT"]
    for gx, label in enumerate(x_labels):
        cx = OX + gx * CELL + CELL / 2
        for part_i, part in enumerate(label.split("\n")):
            lines.append(
                f'  <text x="{cx:.0f}" y="{OY - 20 + part_i * 13:.0f}" text-anchor="middle" '
                f'font-size="9" font-family="sans-serif" fill="#555" font-style="italic">{part}</text>'
            )
    for gy, label in enumerate(y_labels):
        cy = OY + gy * CELL + CELL / 2
        for part_i, part in enumerate(label.split("\n")):
            lines.append(
                f'  <text x="{OX - 8:.0f}" y="{cy + 4 + part_i * 11:.0f}" text-anchor="end" '
                f'font-size="9" font-family="sans-serif" fill="#555" font-style="italic">{part}</text>'
            )

    # Fond de grille
    for gx in range(4):
        for gy in range(4):
            rx = OX + gx * CELL + 4
            ry = OY + gy * CELL + 4
            lines.append(
                f'  <rect x="{rx}" y="{ry}" width="{CELL - 8}" height="{CELL - 8}" rx="10" '
                f'fill="#e8eaee" opacity="0.5"/>'
            )

    # Arêtes (Hasse) dans la grille
    for lo, hi in HASSE:
        x1, y1 = grid_xy(lo)
        x2, y2 = grid_xy(hi)
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1:
            continue
        ux, uy = dx/dist, dy/dist
        sx, sy = x1 + ux*(NR+2), y1 + uy*(NR+2)
        ex, ey = x2 - ux*(NR+2), y2 - uy*(NR+2)
        c1, c2 = concept_rgb(lo), concept_rgb(hi)
        col = css(blend(c1, c2))
        lines.append(
            f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{col}" stroke-width="2" opacity="0.4" stroke-linecap="round"/>'
        )

    # Nœuds
    for mask in range(16):
        x, y = grid_xy(mask)
        rgb = concept_rgb(mask)
        fill, stroke_col = css(rgb), css(darken(rgb))
        fg_col = fg(rgb)
        name, val = ZPOS[mask]
        lvl = bin(mask).count("1")
        fs = 8 if len(name) > 12 else (9 if len(name) > 8 else 10)
        lines += [
            f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{NR}" fill="{fill}" stroke="{stroke_col}" stroke-width="2.5"/>',
            f'  <text x="{x:.0f}" y="{y - 5:.0f}" text-anchor="middle" font-size="{fs}" '
            f'font-family="sans-serif" font-weight="bold" fill="{fg_col}">{name}</text>',
            f'  <text x="{x:.0f}" y="{y + 10:.0f}" text-anchor="middle" font-size="8" '
            f'font-family="monospace" fill="{fg_col}" opacity="0.8">={val}</text>',
        ]
        # Indicateur de niveau (petit badge)
        bx, by = x + NR - 8, y - NR + 8
        lvl_color = css(darken(rgb, 0.8))
        lines.append(
            f'  <circle cx="{bx:.0f}" cy="{by:.0f}" r="9" fill="{lvl_color}" opacity="0.85"/>'
            f'  <text x="{bx:.0f}" y="{by + 4:.0f}" text-anchor="middle" font-size="9" '
            f'font-family="monospace" fill="#fff">L{lvl}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SVG 3 — Radial sunburst (niveaux concentriques)
# ─────────────────────────────────────────────────────────────────────────────

def svg_radial() -> str:
    W, H = 780, 800
    CX, CY = W // 2, H // 2 + 20
    NR = 32

    RADII = {0: 0, 1: 255, 2: 170, 3: 90, 4: 0}
    # Nœuds par niveau (triés par mask pour angle stable)
    by_level: dict[int, list[int]] = {i: [] for i in range(5)}
    for mask in range(16):
        by_level[bin(mask).count("1")].append(mask)

    def node_pos(mask: int) -> tuple[float, float]:
        lvl = bin(mask).count("1")
        r = RADII[lvl]
        nodes = by_level[lvl]
        if len(nodes) == 1 or r == 0:
            return float(CX), float(CY)
        idx = nodes.index(mask)
        # Angle de départ selon le niveau pour un bel alignement
        offsets = {1: -90, 2: -60, 3: -45}
        start_deg = offsets.get(lvl, 0)
        angle = math.radians(start_deg + idx * 360 / len(nodes))
        return CX + r * math.cos(angle), CY + r * math.sin(angle)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" rx="10" fill="#f8f9fb"/>',
        f'  <text x="{W//2}" y="36" text-anchor="middle" font-size="17" font-family="sans-serif" '
        f'font-weight="bold" fill="#222">Vue radiale — niveaux concentriques nipada</text>',
        f'  <text x="{W//2}" y="54" text-anchor="middle" font-size="10" font-family="sans-serif" '
        f'fill="#888">L1 = atomes (bord)  ·  L2 = paires  ·  L3 = triples  ·  L4 = INTÉGRATION (centre)</text>',
    ]

    # Cercles guides
    for lvl, r in RADII.items():
        if r > 0:
            rgb_avg = (180, 180, 185)
            lines.append(
                f'  <circle cx="{CX}" cy="{CY}" r="{r + NR + 14}" fill="none" '
                f'stroke="#e0e0e8" stroke-width="1" stroke-dasharray="5 8"/>'
            )
            lines.append(
                f'  <text x="{CX + r + NR + 18}" y="{CY + 4}" text-anchor="start" '
                f'font-size="9" font-family="monospace" fill="#c0c0c8">L{lvl}</text>'
            )

    # Arêtes Hasse
    for lo, hi in HASSE:
        x1, y1 = node_pos(lo)
        x2, y2 = node_pos(hi)
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1:
            continue
        ux, uy = dx/dist, dy/dist
        r1 = NR + 2 if lo != 0 and lo != 15 else 0
        r2 = NR + 2 if hi != 15 else 0
        sx, sy = x1 + ux * r1, y1 + uy * r1
        ex, ey = x2 - ux * r2, y2 - uy * r2
        c1, c2 = concept_rgb(lo), concept_rgb(hi)
        col = css(blend(c1, c2))
        lines.append(
            f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{col}" stroke-width="2" opacity="0.35" stroke-linecap="round"/>'
        )

    # Nœuds
    for mask in range(16):
        x, y = node_pos(mask)
        rgb = concept_rgb(mask)
        fill, stroke_col = css(rgb), css(darken(rgb))
        fg_col = fg(rgb)
        name, val = ZPOS[mask]
        fs = 8 if len(name) > 12 else (9 if len(name) > 8 else 10)
        r_node = NR if mask not in (0, 15) else (NR - 6)
        lines += [
            f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{r_node}" fill="{fill}" '
            f'stroke="{stroke_col}" stroke-width="2.5"/>',
            f'  <text x="{x:.0f}" y="{y - 4:.0f}" text-anchor="middle" font-size="{fs}" '
            f'font-family="sans-serif" font-weight="bold" fill="{fg_col}">{name}</text>',
            f'  <text x="{x:.0f}" y="{y + 11:.0f}" text-anchor="middle" font-size="8" '
            f'font-family="monospace" fill="{fg_col}" opacity="0.75">={val}</text>',
        ]

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SVG 4 — Heatmap Jaccard 15×15
# ─────────────────────────────────────────────────────────────────────────────

def svg_jaccard() -> str:
    # Ordre : niveaux 1→4, puis par mask
    ORDER = [m for lvl in range(1, 5) for m in range(1, 16) if bin(m).count("1") == lvl]

    N = len(ORDER)  # 15
    CELL = 36
    OX, OY = 108, 108
    W = OX + N * CELL + 60
    H = OY + N * CELL + 50

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" rx="10" fill="#fafafa"/>',
        f'  <text x="{W//2}" y="28" text-anchor="middle" font-size="16" font-family="sans-serif" '
        f'font-weight="bold" fill="#222">Similarité de Jaccard — 15 concepts nipada</text>',
        f'  <text x="{W//2}" y="46" text-anchor="middle" font-size="9" font-family="sans-serif" '
        f'fill="#999">J(A,B) = |atoms_A ∩ atoms_B| / |atoms_A ∪ atoms_B|  ·  couleur = mélange des deux concepts</text>',
    ]

    # Labels colonnes (diagonaux via transform)
    for j, mask in enumerate(ORDER):
        cx = OX + j * CELL + CELL / 2
        name = ZPOS[mask][0]
        rgb = concept_rgb(mask)
        col = css(darken(rgb, 0.7))
        lines.append(
            f'  <text transform="rotate(-55 {cx:.0f} {OY - 6})" '
            f'x="{cx:.0f}" y="{OY - 6}" text-anchor="start" font-size="8" '
            f'font-family="sans-serif" fill="{col}" font-weight="bold">{name}</text>'
        )

    # Labels lignes
    for i, mask in enumerate(ORDER):
        cy = OY + i * CELL + CELL / 2 + 4
        name = ZPOS[mask][0]
        rgb = concept_rgb(mask)
        col = css(darken(rgb, 0.7))
        lines.append(
            f'  <text x="{OX - 5}" y="{cy:.0f}" text-anchor="end" font-size="8" '
            f'font-family="sans-serif" fill="{col}" font-weight="bold">{name}</text>'
        )

    # Cellules
    for i, ma in enumerate(ORDER):
        for j, mb in enumerate(ORDER):
            jac = jaccard(ma, mb)
            rx = OX + j * CELL
            ry = OY + i * CELL
            if i == j:
                # Diagonale = concept pur
                rgb = concept_rgb(ma)
                fill = css(rgb)
                lines.append(
                    f'  <rect x="{rx}" y="{ry}" width="{CELL}" height="{CELL}" fill="{fill}"/>'
                )
            elif jac > 0:
                mixed = blend(concept_rgb(ma), concept_rgb(mb))
                fill = css(mixed)
                lines.append(
                    f'  <rect x="{rx}" y="{ry}" width="{CELL}" height="{CELL}" '
                    f'fill="{fill}" opacity="{0.15 + jac * 0.85:.2f}"/>'
                )
                if jac >= 0.5:
                    cx_lbl = rx + CELL / 2
                    cy_lbl = ry + CELL / 2 + 4
                    lines.append(
                        f'  <text x="{cx_lbl:.0f}" y="{cy_lbl:.0f}" text-anchor="middle" '
                        f'font-size="7" font-family="monospace" fill="#fff" '
                        f'opacity="0.9">{jac:.2f}</text>'
                    )
            else:
                lines.append(
                    f'  <rect x="{rx}" y="{ry}" width="{CELL}" height="{CELL}" fill="#f0f0f0"/>'
                )

    # Grille
    for k in range(N + 1):
        x = OX + k * CELL
        y = OY + k * CELL
        lines.append(
            f'  <line x1="{x}" y1="{OY}" x2="{x}" y2="{OY + N*CELL}" '
            f'stroke="#ccc" stroke-width="0.5"/>'
        )
        lines.append(
            f'  <line x1="{OX}" y1="{y}" x2="{OX + N*CELL}" y2="{y}" '
            f'stroke="#ccc" stroke-width="0.5"/>'
        )

    # Séparateurs de niveaux (après les 4 atomes → index 4)
    level_seps = [4, 10, 14]  # après L1(4), après L2(6→idx10), après L3(4→idx14)
    for sep in level_seps:
        x = OX + sep * CELL
        y = OY + sep * CELL
        lines += [
            f'  <line x1="{x}" y1="{OY}" x2="{x}" y2="{OY + N*CELL}" '
            f'stroke="#888" stroke-width="1.5"/>',
            f'  <line x1="{OX}" y1="{y}" x2="{OX + N*CELL}" y2="{y}" '
            f'stroke="#888" stroke-width="1.5"/>',
        ]

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SVG 5 — Expressions de test (timeline colorée)
# ─────────────────────────────────────────────────────────────────────────────

# Expressions = list of (label, [(mask, gloss)])
EXPRESSIONS: list[tuple[str, list[tuple[int, str]]]] = [
    (
        "Je perçois le monde",
        [(1, "ÊTRE"), (4, "RAPPORT"), (8, "ORIENTATION"), (3, "EXISTENCE")],
    ),
    (
        "Le temps passe",
        [(14, "TEMPS"), (9, "DEVENIR"), (8, "ORIENTATION")],
    ),
    (
        "Différence crée sens",
        [(2, "DIFFÉRENCE"), (11, "TRANSFORMATION"), (12, "RÉFÉRENCE")],
    ),
    (
        "Vie est intégration",
        [(7, "VIE"), (1, "ÊTRE"), (15, "INTÉGRATION")],
    ),
    (
        "Opposition → Paix (crossing)",
        [(10, "OPPOSITION"), (11, "TRANSFORMATION"), (5, "COMPOSITION")],
    ),
    (
        "Causalité : temps + orientation → devenir",
        [(14, "TEMPS"), (8, "ORIENTATION"), (9, "DEVENIR"), (11, "TRANSFORMATION")],
    ),
]

def svg_expressions() -> str:
    W = 960
    BLOCK_H  = 56
    BLOCK_W  = 118
    ROW_H    = BLOCK_H + 62
    OX, OY  = 28, 80
    H = OY + len(EXPRESSIONS) * ROW_H + 60

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" rx="10" fill="#f4f5f8"/>',
        f'  <text x="{W//2}" y="36" text-anchor="middle" font-size="17" font-family="sans-serif" '
        f'font-weight="bold" fill="#222">Expressions de test — encodage nipada</text>',
        f'  <text x="{W//2}" y="54" text-anchor="middle" font-size="10" font-family="sans-serif" '
        f'fill="#888">Chaque concept = un bloc coloré · couleur = composition atomique · valeur = produit de primes</text>',
    ]

    for row_idx, (label, tokens) in enumerate(EXPRESSIONS):
        row_y = OY + row_idx * ROW_H + 20

        # Label de l'expression
        lines.append(
            f'  <text x="{OX}" y="{row_y}" font-size="12" font-family="sans-serif" '
            f'font-weight="bold" fill="#333" font-style="italic">"{label}"</text>'
        )

        # Fond de la ligne de blocs
        total_w = len(tokens) * (BLOCK_W + 8) - 8 + 24
        lines.append(
            f'  <rect x="{OX}" y="{row_y + 8}" width="{total_w}" height="{BLOCK_H + 14}" '
            f'rx="8" fill="#e8eaee" opacity="0.5"/>'
        )

        prev_rgb = None
        for tok_idx, (mask, gloss) in enumerate(tokens):
            bx = OX + 12 + tok_idx * (BLOCK_W + 8)
            by = row_y + 14

            rgb = concept_rgb(mask)
            fill = css(rgb)
            stroke_col = css(darken(rgb))
            fg_col = fg(rgb)
            name, val = ZPOS[mask]
            lvl = bin(mask).count("1")

            # Flèche entre blocs
            if tok_idx > 0 and prev_rgb:
                ax = bx - 4
                ay = by + BLOCK_H / 2
                arrowcol = css(blend(prev_rgb, rgb))
                lines.append(
                    f'  <polygon points="{ax-8},{ay-3} {ax},{ay} {ax-8},{ay+3}" '
                    f'fill="{arrowcol}" opacity="0.6"/>'
                )

            prev_rgb = rgb

            # Bloc concept
            lines += [
                f'  <rect x="{bx}" y="{by}" width="{BLOCK_W}" height="{BLOCK_H}" rx="8" '
                f'fill="{fill}" stroke="{stroke_col}" stroke-width="1.5"/>',
                # Nom
                f'  <text x="{bx + BLOCK_W//2}" y="{by + 19}" text-anchor="middle" '
                f'font-size="9" font-family="sans-serif" font-weight="bold" fill="{fg_col}">'
                f'{name}</text>',
                # Valeur
                f'  <text x="{bx + BLOCK_W//2}" y="{by + 33}" text-anchor="middle" '
                f'font-size="10" font-family="monospace" fill="{fg_col}" opacity="0.85">'
                f'={val}</text>',
                # Niveau
                f'  <text x="{bx + BLOCK_W//2}" y="{by + 48}" text-anchor="middle" '
                f'font-size="8" font-family="monospace" fill="{fg_col}" opacity="0.6">'
                f'L{lvl}</text>',
            ]

            # Atomes actifs sous le bloc (petits points colorés)
            dot_y = by + BLOCK_H + 8
            active_bits = [b for b in range(4) if mask & (1 << b)]
            n_dots = len(active_bits)
            dot_start_x = bx + BLOCK_W / 2 - (n_dots - 1) * 7
            for di, bit in enumerate(active_bits):
                dx = dot_start_x + di * 14
                a_rgb = ATOM_RGB[bit]
                lines.append(
                    f'  <circle cx="{dx:.0f}" cy="{dot_y}" r="5" fill="{css(a_rgb)}" '
                    f'stroke="{css(darken(a_rgb))}" stroke-width="1"/>'
                )

        # Produit total
        product = 1
        for mask, _ in tokens:
            if mask != 0:
                product *= ZPOS[mask][1]
        px = OX + 12 + len(tokens) * (BLOCK_W + 8) + 4
        py = row_y + 14 + BLOCK_H / 2 + 6
        lines += [
            f'  <text x="{px}" y="{py - 8}" font-size="9" font-family="sans-serif" fill="#777">∏</text>',
            f'  <text x="{px}" y="{py + 6}" font-size="11" font-family="monospace" '
            f'fill="#444" font-weight="bold">{product:,}</text>',
        ]

    # Légende atomes en bas
    lx, ly = OX, H - 38
    lines.append(
        f'  <text x="{lx}" y="{ly - 4}" font-size="9" font-family="sans-serif" fill="#888">'
        f'Atomes :</text>'
    )
    for bit in range(4):
        _, aname, r, g, b = (bit,) + ATOM_NAMES[bit:bit+1] + (ATOM_RGB[bit][0], ATOM_RGB[bit][1], ATOM_RGB[bit][2])
        ax_leg = lx + 55 + bit * 100
        rgb_leg = ATOM_RGB[bit]
        lines += [
            f'  <circle cx="{ax_leg}" cy="{ly - 6}" r="7" fill="{css(rgb_leg)}" '
            f'stroke="{css(darken(rgb_leg))}" stroke-width="1"/>',
            f'  <text x="{ax_leg + 11}" y="{ly - 2}" font-size="9" font-family="sans-serif" '
            f'fill="#555">{ATOM_NAMES[bit]}</text>',
        ]

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

GENERATORS = [
    ("nipada_zneg_duality.svg",  svg_zneg_duality,  "Dualité Z+/Z- (Hasse miroir)"),
    ("nipada_grid_4x4.svg",      svg_grid_4x4,      "Grille 4×4 hypercube projection"),
    ("nipada_radial.svg",        svg_radial,         "Radial sunburst par niveau"),
    ("nipada_jaccard.svg",       svg_jaccard,        "Heatmap Jaccard 15×15"),
    ("nipada_expressions.svg",   svg_expressions,    "Expressions de test"),
]


if __name__ == "__main__":
    for fname, gen_fn, desc in GENERATORS:
        path = OUT_DIR / fname
        content = gen_fn()
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ {fname:<32} {len(content):>7} oct.  — {desc}")

    print(f"\n{len(GENERATORS)} SVG générés dans {OUT_DIR}/")

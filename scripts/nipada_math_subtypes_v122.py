"""
§122 — Détecteur de sous-types T_E_math (axiome, théorème, démonstration, calcul,
exemple, contre-exemple, corollaire, heuristique, définition formelle).

Etend le pipeline V7 (§107) à un domaine mathématique-physique.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "nipada" / "modal" / "math_subtypes_v122.json"

# ---------------------------------------------------------------------------
# 9 sous-types mathématiques
# ---------------------------------------------------------------------------

MATH_SUBTYPES = [
    "axiome",
    "definition_formelle",
    "theoreme_enonce",
    "demonstration",
    "calcul",
    "exemple",
    "contre_exemple",
    "corollaire",
    "heuristique",
]

# Patterns multilingues (fr/en/de/it/es) — tirés de manuels de math/physique
PATTERNS = {
    "axiome": [
        r"\baxiom(?:e|a|s)?\b",
        r"\bpostulat[s]?\b",
        r"\bon\s+postul",
        r"\bnous\s+postul",
        r"\bwe\s+postulate\b",
        r"\bassume[d]?\s+as\s+axiom",
        r"\bgrundsatz\b",
        r"\bpostulado\b",
    ],
    "definition_formelle": [
        r"\bd[ée]finition\b\s*[:.\-]",
        r"\bdefinition\b\s*[:.\-]",
        r"\bsoit\s+[A-Zα-ω]",
        r"\blet\s+[A-Zα-ω][a-zA-Z]*\s+be\b",
        r"\bon\s+(?:appelle|d[ée]finit|note)\b",
        r"\bwe\s+(?:call|define|denote)\b",
        r"\bdefine\s+[A-Za-zα-ω]",
        r"\bdefinieren\s+wir\b",
        r"\bdefiniamo\b",
        r"\bdefinimos\b",
        r"\bsia\s+[A-Zα-ω]",
    ],
    "theoreme_enonce": [
        r"\bth[ée]or[èe]me\b",
        r"\btheorem\b",
        r"\bproposition\b",
        r"\blem(?:me|ma|mas|mata)\b",
        r"\bsatz\b",
        r"\bteorema\b",
        r"\b(?:we\s+)?(?:can\s+)?prove\s+that\b",
        r"\bil\s+vient\s+que\b",
        r"\bil\s+s[''']?ensuit\s+que\b",
        r"\bit\s+follows\s+that\b",
    ],
    "demonstration": [
        r"\bd[ée]monstration\b\s*[:.\-]?",
        r"\bpreuve\b\s*[:.\-]",
        r"\bproof\b\s*[:.\-]",
        r"\bbeweis\b\s*[:.\-]",
        r"\bdimostrazione\b\s*[:.\-]",
        r"\bsupposons\s+que\b",
        r"\bsuppose\s+(?:that\s+)?[A-Zα-ω]",
        r"\bCQFD\b",  # QED retiré — collision avec quantum electrodynamics
        r"[∎□■]",
        r"\bce\s+qu[''']il\s+fallait\s+d[ée]montrer\b",
    ],
    "calcul": [
        r"=\s*[^=]+?\s*=",  # au moins deux égalités
        r"\bd[ée]riv(?:ons|er|ant|ation)\b",
        r"\bint[ée]gr(?:ons|er|ant|ation|ating)\b",
        r"\bsubstitu(?:ons|ant|tion|ting)\b",
        r"\bin\s+substituting\b",
        r"\bsetting\s+[A-Zα-ω]\s*=",
    ],
    "exemple": [
        r"\bexemple\b\s*[:.\-]",
        r"\bexample\b\s*[:.\-]",
        r"\bbeispiel\b\s*[:.\-]",
        r"\besempio\b\s*[:.\-]",
        r"\bejemplo\b\s*[:.\-]",
        r"\bpar\s+exemple\b",
        r"\bfor\s+example\b",
        r"\bfor\s+instance\b",
        r"\be\.g\.,?",
    ],
    "contre_exemple": [
        r"\bcontre[\-\s]exemple\b",
        r"\bcounterexample\b",
        r"\bgegenbeispiel\b",
        r"\bcontroesempio\b",
    ],
    "corollaire": [
        r"\bcorollaire\b",
        r"\bcorollary\b",
        r"\bkorollar\b",
        r"\bcorollario\b",
        r"\bcorolario\b",
        r"\bil\s+s[''']?ensuit\s+(?:imm[ée]diatement|directement)\b",
        r"\bit\s+immediately\s+follows\b",
    ],
    "heuristique": [
        r"\bimaginons\b",
        r"\bimagine\b",
        r"\bpictorially\b",
        r"\bintuitively\b",
        r"\bintuitivement\b",
        r"\bheuristiquement\b",
        r"\bheuristically\b",
        r"\bnaively\b",
        r"\bna[ïi]vement\b",
        r"\bon\s+peut\s+visualiser\b",
        r"\bone\s+can\s+visualize\b",
        r"\bthink\s+of\s+[\w\s]{1,40}?\s+as\b",
        r"\bpensons\s+[àa]\b",
        r"\brepr[ée]sent(?:ons|ez)[\-\s]nous\b",
    ],
}

COMPILED = {
    subtype: [re.compile(p, re.IGNORECASE | re.UNICODE) for p in patterns]
    for subtype, patterns in PATTERNS.items()
}


def detect_subtypes_vec(text: str) -> List[int]:
    """Return [9] vector of counts per MATH_SUBTYPES.

    Priorités :
    - contre_exemple > exemple (sous-chaîne)
    - exemple > calcul (un « Example: ... = ... » est un exemple, pas un calcul)
    - corollaire > theoreme_enonce (« corollary » implique « follows »)
    - axiome / definition_formelle / theoreme_enonce / corollaire au début de phrase priment sur usage interne (« by the X theorem »)
    """
    counts = [0] * len(MATH_SUBTYPES)
    for i, subtype in enumerate(MATH_SUBTYPES):
        for pat in COMPILED[subtype]:
            counts[i] += len(pat.findall(text))
    # Priorité contre_exemple > exemple
    idx_contre = MATH_SUBTYPES.index("contre_exemple")
    idx_ex = MATH_SUBTYPES.index("exemple")
    idx_calc = MATH_SUBTYPES.index("calcul")
    idx_th = MATH_SUBTYPES.index("theoreme_enonce")
    idx_cor = MATH_SUBTYPES.index("corollaire")
    if counts[idx_contre] > 0:
        counts[idx_ex] = 0
    # Priorité exemple > calcul (« Example: » déclare exemple même avec égalités)
    if counts[idx_ex] > 0:
        counts[idx_calc] = 0
    # Priorité corollaire > theoreme (corollary contient « follows » implicitement)
    if counts[idx_cor] > 0:
        counts[idx_th] = 0
    # « by the X theorem » : usage, pas énoncé. Si « by the… theorem » détecté
    # et qu'aucun autre marqueur d'énoncé fort n'est là, le compte décroit.
    import re as _re
    if _re.search(r"\bby\s+the\s+\w+\s+theorem\b", text, _re.IGNORECASE):
        counts[idx_th] = max(0, counts[idx_th] - 1)
    return counts


def dominant_subtype(text: str) -> str | None:
    counts = detect_subtypes_vec(text)
    if max(counts) == 0:
        return None
    return MATH_SUBTYPES[counts.index(max(counts))]


# ---------------------------------------------------------------------------
# Mini-corpus de test : 36 phrases couvrant les 9 sous-types × 4 langues
# ---------------------------------------------------------------------------

TEST_CORPUS: List[Tuple[str, str, str]] = [
    # axiome
    ("axiome", "fr", "Axiome de l'infini : il existe un ensemble inductif."),
    ("axiome", "en", "Axiom of choice: For every family of nonempty sets, there exists a choice function."),
    ("axiome", "fr", "Postulat d'Euclide : par un point hors d'une droite passe une et une seule parallèle."),
    ("axiome", "en", "We postulate that the speed of light is invariant in all inertial frames."),
    # définition formelle
    ("definition_formelle", "fr", "Définition : un groupe est un ensemble muni d'une opération associative, d'un neutre et d'inverses."),
    ("definition_formelle", "en", "Definition: A topological space is a set X equipped with a collection of open sets satisfying three axioms."),
    ("definition_formelle", "fr", "Soit f : ℝ → ℝ une fonction continue."),
    ("definition_formelle", "en", "Let X be a Hausdorff space."),
    # théorème
    ("theoreme_enonce", "fr", "Théorème de Pythagore : dans un triangle rectangle, a² + b² = c²."),
    ("theoreme_enonce", "en", "Theorem (Cauchy): For any holomorphic function f, the integral over a closed contour vanishes."),
    ("theoreme_enonce", "fr", "Proposition : tout sous-groupe d'un groupe cyclique est cyclique."),
    ("theoreme_enonce", "en", "Lemma 3.2: If A is compact and f is continuous, then f(A) is compact."),
    # démonstration
    ("demonstration", "fr", "Démonstration. Supposons que p soit le plus grand premier. Considérons N = p! + 1. ∎"),
    ("demonstration", "en", "Proof. Suppose for contradiction that √2 = a/b with gcd(a,b)=1. Then a² = 2b², so a is even. QED"),
    ("demonstration", "fr", "Preuve : par récurrence sur n. Pour n=0 c'est trivial. Supposons la propriété vraie au rang n."),
    ("demonstration", "en", "Suppose that f is differentiable at x₀. Then by definition the limit exists. ∎"),
    # calcul
    ("calcul", "fr", "Dérivons : d/dx (x² + 3x) = 2x + 3 = lim_{h→0} ((x+h)² − x²)/h."),
    ("calcul", "en", "Setting u = x², we get du = 2x dx and the integral becomes ∫ u² du = u³/3."),
    ("calcul", "fr", "On a successivement E = mc² = m c · c = pc avec p = mc."),
    ("calcul", "en", "Integrating by parts: ∫ u dv = uv − ∫ v du = x sin(x) + cos(x) + C."),
    # exemple
    ("exemple", "fr", "Exemple : la fonction sin est périodique de période 2π."),
    ("exemple", "en", "Example: The set of natural numbers ℕ is countably infinite."),
    ("exemple", "fr", "Par exemple, considérons la matrice identité de dimension 3."),
    ("exemple", "en", "For example, the function f(x) = x² is convex on ℝ."),
    # contre-exemple
    ("contre_exemple", "fr", "Contre-exemple : la fonction de Weierstrass est continue partout mais dérivable nulle part."),
    ("contre_exemple", "en", "Counterexample: The Cantor set is uncountable but has Lebesgue measure zero."),
    ("contre_exemple", "fr", "Contre-exemple : ℚ est dense dans ℝ mais n'est pas complet."),
    ("contre_exemple", "en", "Counterexample: 4 = 2 × 2 is even but not prime, refuting the conjecture."),
    # corollaire
    ("corollaire", "fr", "Corollaire : tout polynôme de degré impair sur ℝ a au moins une racine réelle."),
    ("corollaire", "en", "Corollary: If G is a finite group of prime order, then G is cyclic."),
    ("corollaire", "fr", "Il s'ensuit immédiatement que f est uniformément continue sur le compact."),
    ("corollaire", "en", "It immediately follows that the kernel of φ is a normal subgroup."),
    # heuristique
    ("heuristique", "fr", "Imaginons une corde vibrante de longueur infinie sur laquelle se propage une onde."),
    ("heuristique", "en", "Pictorially, the Riemann surface looks like a spiral staircase with infinitely many sheets."),
    ("heuristique", "fr", "Intuitivement, la dérivée mesure la pente locale de la fonction."),
    ("heuristique", "en", "Think of the wave function as a complex-valued amplitude over configuration space."),
]


# ---------------------------------------------------------------------------
# Évaluation
# ---------------------------------------------------------------------------

def evaluate() -> Dict:
    correct = 0
    confusion: Dict[str, Dict[str, int]] = {st: {} for st in MATH_SUBTYPES}
    detail = []
    for true_label, lang, text in TEST_CORPUS:
        counts = detect_subtypes_vec(text)
        predicted = MATH_SUBTYPES[counts.index(max(counts))] if max(counts) > 0 else "AUCUN"
        ok = predicted == true_label
        if ok:
            correct += 1
        confusion[true_label][predicted] = confusion[true_label].get(predicted, 0) + 1
        detail.append({
            "true": true_label,
            "predicted": predicted,
            "lang": lang,
            "text": text,
            "counts": dict(zip(MATH_SUBTYPES, counts)),
            "ok": ok,
        })

    n = len(TEST_CORPUS)
    accuracy = correct / n if n else 0.0

    per_class = {}
    for st in MATH_SUBTYPES:
        seen = sum(1 for x in detail if x["true"] == st)
        good = sum(1 for x in detail if x["true"] == st and x["ok"])
        per_class[st] = {"n": seen, "correct": good, "acc": good / seen if seen else None}

    return {
        "n_tests": n,
        "accuracy_overall": accuracy,
        "per_class": per_class,
        "confusion": confusion,
        "detail": detail,
    }


def main():
    result = evaluate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"§122 — accuracy = {result['accuracy_overall']:.3f} sur n={result['n_tests']}")
    for st, stats in result["per_class"].items():
        if stats["n"]:
            print(f"  {st:25s} {stats['correct']}/{stats['n']} = {stats['acc']:.2f}")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

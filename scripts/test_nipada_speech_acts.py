#!/usr/bin/env python3
"""
test_nipada_speech_acts.py — §83 : Discrimination totale des actes de parole

Diagnostic §82 Phase 2 :
    proclamation [770,33,55] × définition [770,385] = cos 0.982
    Cause racine : DIGNITÉ(770) est un architectural dominant (def longue) présent
    dans les DEUX types → il écrase le signal discriminant.

Principe §83 — MODE séparé du CONTENU :
    Chaque acte de parole est encodé par une MODE-MOLECULE primaire UNIQUE,
    choisie dans une région sémantique orthogonale. Aucune mode-molecule ne
    figure dans deux types différents.

7 modes définis (première molécule = dominante, aucun partage) :

    type           mode-molecules       prime dominante   région
    ─────────────────────────────────────────────────────────────
    description    [2, 5, 3]           ÊTRE(2)           ontologique pur
    définition     [385, 66]           SENS(385)         signification propre
    proclamation   [33, 55, 77]        NORME(33)         normatif performatif
    question       [165, 11]           JUGEMENT(165)     évaluation différentielle
    ordre          [154, 231]          PROJET(154)       directif orienté
    narration      [462, 1155]         RÉCIT(462)        trame temporelle
    introspection  [2310, 22]          CONSCIENCE(2310)  intégration réflexive

Corpus enrichi : 4 phrases × 7 types × 5 langues = 140 phrases
(centroides de référence pour chaque type)

Critère de discrimination totale :
    MAX off-diagonal (cosine nipada×nipada) < 0.80
    MEAN same-type alignment (nipada vs centroïde original) > 0.55
    Discrimination score (mean_intra / mean_inter) > 1.5

Résultats → research/nipada/falsification/nipada_speech_acts_test.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.core.nipada_subject import NipadaExtendedSynthesizer


# ── JSON robuste (NumPy 2.0 : bool_ n'est plus sous-classe de int) ──────────

class _NpEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)


def _to_native(obj):
    """Convertit récursivement les types numpy en types Python natifs."""
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _to_native(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_native(v) for v in obj]
    return obj

MODEL_NAME  = "paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FILE = ROOT / "research" / "nipada" / "falsification" / "nipada_speech_acts_test.json"
LANGUAGES   = ["fr", "en", "de", "es", "zh"]

# ══════════════════════════════════════════════════════════════════════════════
# Mode molecules (§83 — discriminant design)
# Contrainte : première molécule unique et dans une région sémantique distincte
# ══════════════════════════════════════════════════════════════════════════════

MODES: dict[str, list[int]] = {
    "description":   [2, 5, 3],       # ÊTRE+RAPP+DIFF        — ontologique pur, 0 SUJET
    "définition":    [385, 66],        # SENS+IDENTITÉ         — signification propre
    "proclamation":  [33, 55, 77],     # NORME+DROIT+LIBERTÉ   — normatif performatif
    "question":      [165, 11],        # JUGEMENT+SUJET        — évaluation interrogative
    "ordre":         [154, 231],       # PROJET+RÉSISTANCE     — directif orienté
    "narration":     [462, 1155],      # RÉCIT+MÉMOIRE         — trame temporelle
    "introspection": [2310, 22],       # CONSCIENCE+PRÉSENCE   — intégration réflexive
}

ACT_TYPES = list(MODES.keys())

# ══════════════════════════════════════════════════════════════════════════════
# Corpus enrichi (4 phrases × 7 types × 5 langues)
# Principe : phrases naturelles clairement représentatives de chaque acte de parole
# ══════════════════════════════════════════════════════════════════════════════

CORPUS: dict[str, dict[str, list[str]]] = {

    "description": {
        "fr": [
            "Un être se distingue de ce qui l'entoure en maintenant une structure relationnelle stable.",
            "Deux entités diffèrent par leurs propriétés et entretiennent des rapports qui les définissent mutuellement.",
            "Un système se caractérise par la nature de ses différences internes et les relations qui les organisent.",
            "Quelque chose existe dans la mesure où il se différencie de son environnement et entretient des rapports avec lui.",
        ],
        "en": [
            "A being distinguishes itself from its environment by maintaining a stable relational structure.",
            "Two entities differ through their properties and maintain relations that define them mutually.",
            "A system is characterized by the nature of its internal differences and the relations that organize them.",
            "Something exists insofar as it differentiates itself from its surroundings and maintains relations with them.",
        ],
        "de": [
            "Ein Wesen unterscheidet sich von seiner Umgebung, indem es eine stabile relationale Struktur aufrechterhält.",
            "Zwei Entitäten unterscheiden sich durch ihre Eigenschaften und unterhalten Beziehungen, die sie gegenseitig definieren.",
            "Ein System wird durch die Art seiner inneren Unterschiede und die sie organisierenden Beziehungen charakterisiert.",
            "Etwas existiert, insofern es sich von seiner Umgebung differenziert und Beziehungen zu ihr unterhält.",
        ],
        "es": [
            "Un ser se distingue de su entorno manteniendo una estructura relacional estable.",
            "Dos entidades difieren por sus propiedades y mantienen relaciones que las definen mutuamente.",
            "Un sistema se caracteriza por la naturaleza de sus diferencias internas y las relaciones que las organizan.",
            "Algo existe en la medida en que se diferencia de su entorno y mantiene relaciones con él.",
        ],
        "zh": [
            "一个存在者通过维持稳定的关系结构来区别于其所处环境。",
            "两个实体通过各自的属性相互区分，并维持相互界定彼此的关系。",
            "一个系统由其内部差异的性质及组织这些差异的关系所构成。",
            "某物存在，当且仅当它将自身与环境相区分并与之保持关系。",
        ],
    },

    "définition": {
        "fr": [
            "La dignité est le rapport orienté qu'un être entretient avec lui-même, fondant sa valeur irréductible.",
            "La liberté est le pouvoir qu'a un sujet d'orienter lui-même son action vers un but qu'il a librement choisi.",
            "La conscience est l'intégration subjective totale de l'être, de ses différences, de ses rapports et de ses orientations.",
            "L'identité est la distinction stable qu'un sujet opère entre lui-même et ce qu'il n'est pas.",
        ],
        "en": [
            "Dignity is the oriented relation a being maintains with itself, grounding its irreducible value.",
            "Freedom is the power a subject has to orient its own action toward a goal it has freely chosen.",
            "Consciousness is the total subjective integration of being, differences, relations and orientations.",
            "Identity is the stable distinction a subject draws between itself and what it is not.",
        ],
        "de": [
            "Würde ist die gerichtete Beziehung, die ein Wesen mit sich selbst unterhält und seinen irreduziblen Wert begründet.",
            "Freiheit ist die Macht eines Subjekts, seine eigene Handlung auf ein frei gewähltes Ziel auszurichten.",
            "Bewusstsein ist die totale subjektive Integration von Sein, Differenzen, Beziehungen und Orientierungen.",
            "Identität ist die stabile Unterscheidung, die ein Subjekt zwischen sich und dem, was es nicht ist, zieht.",
        ],
        "es": [
            "La dignidad es la relación orientada que un ser mantiene consigo mismo, fundando su valor irreductible.",
            "La libertad es el poder que tiene un sujeto de orientar su propia acción hacia una meta libremente elegida.",
            "La conciencia es la integración subjetiva total del ser, sus diferencias, relaciones y orientaciones.",
            "La identidad es la distinción estable que un sujeto traza entre sí mismo y lo que no es.",
        ],
        "zh": [
            "尊严是存在者与自身维持的定向关系，它奠定其不可还原的固有价值。",
            "自由是主体将其行动自我导向其自由选择目标的能力。",
            "意识是存在、差异、关系与方向的总体主体性整合。",
            "同一性是主体在自身与其所不是的东西之间作出的稳定区分。",
        ],
    },

    "proclamation": {
        "fr": [
            "Tous les êtres humains naissent libres et égaux en dignité et en droits.",
            "Nul ne sera tenu en esclavage ni en servitude ; l'esclavage et la traite des esclaves sont interdits sous toutes leurs formes.",
            "Chacun a droit à la vie, à la liberté et à la sûreté de sa personne.",
            "Tous sont égaux devant la loi et ont droit sans distinction à une égale protection de la loi.",
        ],
        "en": [
            "All human beings are born free and equal in dignity and rights.",
            "No one shall be held in slavery or servitude; slavery and the slave trade shall be prohibited in all their forms.",
            "Everyone has the right to life, liberty and the security of person.",
            "All are equal before the law and are entitled without any discrimination to equal protection of the law.",
        ],
        "de": [
            "Alle Menschen sind frei und gleich an Würde und Rechten geboren.",
            "Niemand darf in Sklaverei oder Leibeigenschaft gehalten werden; Sklaverei und Sklavenhandel sind in allen ihren Formen verboten.",
            "Jeder hat das Recht auf Leben, Freiheit und Sicherheit der Person.",
            "Alle Menschen sind vor dem Gesetz gleich und haben ohne Unterschied Anspruch auf gleichen Schutz durch das Gesetz.",
        ],
        "es": [
            "Todos los seres humanos nacen libres e iguales en dignidad y derechos.",
            "Nadie estará sometido a esclavitud ni a servidumbre; la esclavitud y la trata de esclavos están prohibidas en todas sus formas.",
            "Todo individuo tiene derecho a la vida, a la libertad y a la seguridad de su persona.",
            "Todos son iguales ante la ley y tienen, sin distinción, derecho a igual protección de la ley.",
        ],
        "zh": [
            "人人生而自由，在尊严和权利上一律平等。",
            "任何人不得使为奴隶或奴役；一切形式的奴隶制度和奴隶买卖，均应予以禁止。",
            "人人有权享有生命、自由和人身安全。",
            "在法律面前，人人平等，并有权享受法律的平等保护，不受任何歧视。",
        ],
    },

    "question": {
        "fr": [
            "Qu'est-ce qui distingue un être humain d'un autre ?",
            "Quel est le fondement philosophique de la dignité humaine ?",
            "Comment un sujet peut-il reconnaître la différence entre droit et obligation ?",
            "Pourquoi la liberté implique-t-elle à la fois un droit et une responsabilité envers autrui ?",
        ],
        "en": [
            "What distinguishes one human being from another?",
            "What is the philosophical foundation of human dignity?",
            "How can a subject recognize the difference between a right and an obligation?",
            "Why does freedom imply both a right and a responsibility toward others?",
        ],
        "de": [
            "Was unterscheidet einen Menschen von einem anderen?",
            "Was ist die philosophische Grundlage der Menschenwürde?",
            "Wie kann ein Subjekt den Unterschied zwischen Recht und Pflicht erkennen?",
            "Warum impliziert Freiheit sowohl ein Recht als auch eine Verantwortung gegenüber anderen?",
        ],
        "es": [
            "¿Qué distingue a un ser humano de otro?",
            "¿Cuál es el fundamento filosófico de la dignidad humana?",
            "¿Cómo puede un sujeto reconocer la diferencia entre un derecho y una obligación?",
            "¿Por qué la libertad implica tanto un derecho como una responsabilidad hacia los demás?",
        ],
        "zh": [
            "是什么使一个人区别于另一个人？",
            "人类尊严的哲学基础是什么？",
            "一个主体如何区分权利与义务的差异？",
            "为什么自由既意味着权利，也意味着对他人的责任？",
        ],
    },

    "ordre": {
        "fr": [
            "Agissez les uns envers les autres dans un esprit de fraternité.",
            "Respectez les droits fondamentaux de toute personne sans distinction d'aucune sorte.",
            "Ne portez pas atteinte à la liberté et à la dignité d'autrui.",
            "Défendez votre dignité et celle des autres face à toute forme d'oppression.",
        ],
        "en": [
            "Act towards one another in a spirit of brotherhood.",
            "Respect the fundamental rights of every person without any distinction whatsoever.",
            "Do not infringe upon the freedom and dignity of others.",
            "Defend your own dignity and that of others against all forms of oppression.",
        ],
        "de": [
            "Handeln Sie einander gegenüber im Geiste der Brüderlichkeit.",
            "Respektieren Sie die Grundrechte jeder Person ohne jeden Unterschied.",
            "Verletzen Sie nicht die Freiheit und Würde anderer.",
            "Verteidigen Sie Ihre Würde und die der anderen gegen alle Formen der Unterdrückung.",
        ],
        "es": [
            "Compórtense fraternalmente los unos con los otros.",
            "Respeten los derechos fundamentales de toda persona sin distinción alguna.",
            "No atenten contra la libertad y la dignidad de los demás.",
            "Defiendan su propia dignidad y la de los demás frente a toda forma de opresión.",
        ],
        "zh": [
            "以兄弟关系的精神相互对待。",
            "不得有任何歧视地尊重每个人的基本权利。",
            "不得侵犯他人的自由和尊严。",
            "捍卫自己和他人的尊严，抵制一切形式的压迫。",
        ],
    },

    "narration": {
        "fr": [
            "Au fil du temps, les différences s'accumulent et forment une trame narrative orientée vers le présent.",
            "Un sujet retrace rétrospectivement les étapes qui l'ont conduit d'un état passé à sa situation actuelle.",
            "Les événements se succèdent et s'organisent en une séquence dont la mémoire préserve l'orientation.",
            "La trame du récit relie les différences vécues dans la durée et les intègre dans une continuité mémorisée.",
        ],
        "en": [
            "Over time, differences accumulate and form a narrative thread oriented toward the present.",
            "A subject traces retrospectively the steps that led it from a past state to its current situation.",
            "Events follow one another and organize themselves into a sequence whose orientation is preserved by memory.",
            "The narrative thread connects lived differences over time and integrates them into a remembered continuity.",
        ],
        "de": [
            "Im Laufe der Zeit häufen sich Unterschiede an und bilden einen auf die Gegenwart ausgerichteten Erzählfaden.",
            "Ein Subjekt verfolgt rückblickend die Schritte, die es von einem vergangenen Zustand zu seiner aktuellen Situation geführt haben.",
            "Ereignisse folgen aufeinander und ordnen sich in einer Abfolge, deren Orientierung das Gedächtnis bewahrt.",
            "Der Erzählfaden verbindet gelebte Unterschiede in der Zeit und integriert sie in eine erinnerte Kontinuität.",
        ],
        "es": [
            "Con el paso del tiempo, las diferencias se acumulan y forman una trama narrativa orientada hacia el presente.",
            "Un sujeto traza retrospectivamente los pasos que lo condujeron desde un estado pasado hasta su situación actual.",
            "Los eventos se suceden y se organizan en una secuencia cuya orientación preserva la memoria.",
            "La trama narrativa conecta las diferencias vividas en el tiempo y las integra en una continuidad recordada.",
        ],
        "zh": [
            "随着时间的推移，差异不断积累，形成一条朝向当下的叙事线索。",
            "主体回溯性地追踪将其从过去状态引向当前处境的各个步骤。",
            "事件相继发生，在记忆所保存的方向中组织成一个序列。",
            "叙事的脉络连接着时间中经历过的差异，并将它们整合为一种被记忆的连续性。",
        ],
    },

    "introspection": {
        "fr": [
            "Je prends conscience de ma propre dignité en reconnaissant celle de l'autre en face de moi.",
            "En m'interrogeant sur ma liberté, je découvre les limites que je m'impose moi-même.",
            "Je ressens profondément l'injustice lorsque mes droits fondamentaux sont ignorés ou bafoués.",
            "En réfléchissant à mon identité, je comprends ce qui me lie aux autres êtres humains.",
        ],
        "en": [
            "I become aware of my own dignity by recognizing that of the other person in front of me.",
            "In questioning my freedom, I discover the limits I impose on myself.",
            "I deeply feel the injustice when my fundamental rights are ignored or violated.",
            "By reflecting on my identity, I understand what binds me to other human beings.",
        ],
        "de": [
            "Ich werde mir meiner eigenen Würde bewusst, indem ich die des anderen vor mir anerkenne.",
            "Indem ich meine Freiheit hinterfrage, entdecke ich die Grenzen, die ich mir selbst auferlege.",
            "Ich empfinde die Ungerechtigkeit tief, wenn meine Grundrechte ignoriert oder verletzt werden.",
            "Durch die Reflexion über meine Identität verstehe ich, was mich mit anderen Menschen verbindet.",
        ],
        "es": [
            "Tomo conciencia de mi propia dignidad al reconocer la del otro frente a mí.",
            "Al cuestionarme sobre mi libertad, descubro los límites que me impongo a mí mismo.",
            "Siento profundamente la injusticia cuando mis derechos fundamentales son ignorados o violados.",
            "Al reflexionar sobre mi identidad, comprendo lo que me une a los demás seres humanos.",
        ],
        "zh": [
            "当我认可眼前他人的尊严时，我也意识到了自己的尊严。",
            "在审视自身自由的过程中，我发现了自我设定的界限。",
            "当我的基本权利被漠视或侵犯时，我深切感受到不公正。",
            "通过反思自身的同一性，我理解了将我与其他人联系在一起的纽带。",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def embed(texts: list[str], model: SentenceTransformer) -> np.ndarray:
    return model.encode(texts, normalize_embeddings=True)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0][0])


# ══════════════════════════════════════════════════════════════════════════════
# Phase 0 : vérification design des modes
# ══════════════════════════════════════════════════════════════════════════════

def verify_mode_design() -> dict:
    print(f"\n{'─'*72}")
    print("  PHASE 0 — Vérification design des mode-molecules")
    print(f"{'─'*72}")
    from src.core.nipada_subject import atoms_in_5, MOL_TYPES_5

    print(f"\n  {'type':>14}  {'mode':>22}  {'primes':>22}  {'type_mol'}")
    print(f"  {'─'*72}")

    first_mols = {}
    issues = []
    for act_type, mol_ids in MODES.items():
        all_primes: set[int] = set()
        for m in mol_ids:
            all_primes |= set(atoms_in_5(m))
        mol_types = [MOL_TYPES_5.get(m, "?") for m in mol_ids]
        first = mol_ids[0]
        mol_str = "+".join(str(m) for m in mol_ids)
        prime_str = "×".join(str(p) for p in sorted(all_primes))
        type_str = "+".join(mol_types)
        print(f"  {act_type:>14}  {mol_str:>22}  {prime_str:>22}  {type_str}")
        if first in first_mols:
            issues.append(f"CONFLIT: {act_type} et {first_mols[first]} partagent {first}")
        else:
            first_mols[first] = act_type

    if issues:
        print(f"\n  PROBLÈMES : {issues}")
    else:
        print(f"\n  Toutes les mode-molecules dominantes sont uniques ✓")

    return {"issues": issues, "modes": {k: v for k, v in MODES.items()}}


# ══════════════════════════════════════════════════════════════════════════════
# Phase 1 : matrice de discrimination nipada×nipada
# ══════════════════════════════════════════════════════════════════════════════

def compute_discrimination_matrix(
    model: SentenceTransformer
) -> dict:
    print(f"\n{'─'*72}")
    print("  PHASE 1 — Matrice de discrimination nipada×nipada")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()
    results = {}

    for lang in LANGUAGES:
        # Générer un texte nipada par type
        texts: dict[str, str] = {}
        for act_type, mol_ids in MODES.items():
            texts[act_type] = synth.synthesize(mol_ids, lang)

        # Embeddings
        all_texts = [texts[t] for t in ACT_TYPES]
        vecs = embed(all_texts, model)

        # Matrice cosine
        n = len(ACT_TYPES)
        cos_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                cos_matrix[i, j] = cosine(vecs[i], vecs[j])

        # Off-diagonal stats
        off = [cos_matrix[i, j] for i in range(n) for j in range(n) if i != j]
        max_off = max(off)
        mean_off = sum(off) / len(off)

        print(f"\n  [{lang}]  max_off={max_off:.3f}  mean_off={mean_off:.3f}")
        print(f"  {'':>14}", end="")
        for t in ACT_TYPES:
            print(f"  {t[:6]:>6}", end="")
        print()
        for i, ti in enumerate(ACT_TYPES):
            print(f"  {ti:>14}", end="")
            for j in range(n):
                v = cos_matrix[i, j]
                marker = "■" if i != j and v > 0.80 else " "
                print(f"  {v:.3f}{marker}", end="")
            print()

        results[lang] = {
            "texts":     texts,
            "cos_matrix": {
                f"{ACT_TYPES[i]}×{ACT_TYPES[j]}": round(float(cos_matrix[i,j]), 4)
                for i in range(n) for j in range(n)
            },
            "max_off_diagonal": round(max_off, 4),
            "mean_off_diagonal": round(mean_off, 4),
            "total_discrimination": max_off < 0.80,
        }

    # Résumé global
    global_max = max(results[l]["max_off_diagonal"] for l in LANGUAGES)
    global_mean = sum(results[l]["mean_off_diagonal"] for l in LANGUAGES) / len(LANGUAGES)
    total_ok = global_max < 0.80
    print(f"\n  GLOBAL : max_off={global_max:.3f}  mean_off={global_mean:.3f}")
    print(f"  CRITÈRE discrimination totale (max < 0.80) : "
          f"{'ATTEINT ✓' if total_ok else 'PAS ENCORE ✗'}")

    # Paires problématiques
    bad_pairs: list[tuple[str, str, str, float]] = []
    for lang, data in results.items():
        for key, val in data["cos_matrix"].items():
            a, b = key.split("×")
            if a != b and val > 0.75:
                bad_pairs.append((lang, a, b, val))
    if bad_pairs:
        print(f"\n  Paires > 0.75 :")
        for lang, a, b, val in sorted(bad_pairs, key=lambda x: -x[3]):
            print(f"    [{lang}]  {a} × {b} = {val:.3f}")

    return {
        "by_lang": results,
        "global_max_off": round(global_max, 4),
        "global_mean_off": round(global_mean, 4),
        "total_discrimination": total_ok,
        "bad_pairs": [[l, a, b, v] for l, a, b, v in bad_pairs],
    }


# ══════════════════════════════════════════════════════════════════════════════
# Phase 2 : alignement nipada vs centroïde des phrases originales
# ══════════════════════════════════════════════════════════════════════════════

def compute_alignment_scores(
    model: SentenceTransformer,
    discrimination: dict,
) -> dict:
    print(f"\n{'─'*72}")
    print("  PHASE 2 — Alignement nipada vs centroïde original")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()
    results = {}

    print(f"\n  {'type':>14}  ", end="")
    for lang in LANGUAGES:
        print(f"  {lang:>6}", end="")
    print(f"  {'MOYS':>6}")
    print(f"  {'─'*72}")

    for act_type in ACT_TYPES:
        row: list[float] = []
        lang_scores: dict[str, float] = {}
        for lang in LANGUAGES:
            # Centroïde des phrases originales
            orig_sentences = CORPUS[act_type][lang]
            orig_vecs = embed(orig_sentences, model)
            centroid = orig_vecs.mean(axis=0)
            centroid_norm = centroid / np.linalg.norm(centroid)

            # Texte nipada pour ce type
            nipada_text = discrimination["by_lang"][lang]["texts"][act_type]
            nipada_vec = embed([nipada_text], model)[0]

            sim = cosine(nipada_vec, centroid_norm)
            row.append(sim)
            lang_scores[lang] = round(sim, 4)

        mean_sim = sum(row) / len(row)
        print(f"  {act_type:>14}  ", end="")
        for s in row:
            print(f"  {s:.3f}", end="")
        print(f"  {mean_sim:.3f}")

        results[act_type] = {
            "langs": lang_scores,
            "mean": round(mean_sim, 4),
        }

    mean_alignment = sum(results[t]["mean"] for t in ACT_TYPES) / len(ACT_TYPES)
    ok = mean_alignment > 0.55
    print(f"\n  MOYENNE GLOBALE : {mean_alignment:.3f}")
    print(f"  CRITÈRE alignement (> 0.55) : {'ATTEINT ✓' if ok else 'PAS ENCORE ✗'}")

    return {"by_type": results, "mean_alignment": round(mean_alignment, 4), "ok": ok}


# ══════════════════════════════════════════════════════════════════════════════
# Phase 3 : score de discrimination intra/inter par type
# ══════════════════════════════════════════════════════════════════════════════

def compute_cluster_scores(
    model: SentenceTransformer,
) -> dict:
    """
    Pour chaque type, compare la cohérence intra-type (sentences originales
    du même type, toutes langues) vs la similarité inter-types.
    """
    print(f"\n{'─'*72}")
    print("  PHASE 3 — Scores de cluster intra/inter (sentences originales)")
    print(f"{'─'*72}")

    # Embedder toutes les phrases originales
    all_sentences_by_type: dict[str, list[str]] = {}
    for act_type in ACT_TYPES:
        sentences = []
        for lang in LANGUAGES:
            sentences.extend(CORPUS[act_type][lang])
        all_sentences_by_type[act_type] = sentences

    # Embeddings
    type_vecs: dict[str, np.ndarray] = {}
    for act_type, sentences in all_sentences_by_type.items():
        type_vecs[act_type] = embed(sentences, model)

    # Centroïdes
    centroids: dict[str, np.ndarray] = {
        t: vecs.mean(axis=0) / np.linalg.norm(vecs.mean(axis=0))
        for t, vecs in type_vecs.items()
    }

    # Intra-score : cosine mean entre toutes phrases du même type
    print(f"\n  {'type':>14}  {'intra':>6}  {'inter_mean':>10}  {'ratio':>6}  {'ok':>4}")
    print(f"  {'─'*50}")

    scores = {}
    for act_type in ACT_TYPES:
        # intra
        vecs = type_vecs[act_type]
        n = len(vecs)
        intra_cos = []
        for i in range(n):
            for j in range(i+1, n):
                intra_cos.append(cosine(vecs[i], vecs[j]))
        intra = sum(intra_cos) / len(intra_cos) if intra_cos else 0.0

        # inter : cosine entre centroïde de ce type et centroïdes des autres
        inter_cos = []
        for other_type in ACT_TYPES:
            if other_type != act_type:
                inter_cos.append(cosine(centroids[act_type], centroids[other_type]))
        inter = sum(inter_cos) / len(inter_cos) if inter_cos else 0.0

        ratio = intra / inter if inter > 0 else 0.0
        ok = ratio > 1.5

        print(f"  {act_type:>14}  {intra:.3f}  {inter:.10f}  {ratio:.3f}  {'✓' if ok else '✗'}")
        scores[act_type] = {
            "intra": round(intra, 4),
            "inter": round(inter, 4),
            "ratio": round(ratio, 4),
            "ok": ok,
        }

    # Matrice inter-centroïdes
    n = len(ACT_TYPES)
    print(f"\n  Matrice inter-centroïdes (toutes langues) :")
    print(f"  {'':>14}", end="")
    for t in ACT_TYPES:
        print(f"  {t[:6]:>6}", end="")
    print()
    cos_centroid = {}
    for i, ti in enumerate(ACT_TYPES):
        print(f"  {ti:>14}", end="")
        for j, tj in enumerate(ACT_TYPES):
            c = cosine(centroids[ti], centroids[tj])
            cos_centroid[f"{ti}×{tj}"] = round(c, 4)
            marker = "■" if i != j and c > 0.80 else " "
            print(f"  {c:.3f}{marker}", end="")
        print()

    mean_ratio = sum(scores[t]["ratio"] for t in ACT_TYPES) / len(ACT_TYPES)
    ok_all = all(scores[t]["ok"] for t in ACT_TYPES)
    print(f"\n  Ratio moyen intra/inter : {mean_ratio:.3f}")
    print(f"  CRITÈRE ratio > 1.5 pour tous : {'ATTEINT ✓' if ok_all else 'PARTIEL ✗'}")

    # Identifier paires les plus proches
    off_centroid = [
        (ti, tj, cos_centroid[f"{ti}×{tj}"])
        for i, ti in enumerate(ACT_TYPES)
        for j, tj in enumerate(ACT_TYPES)
        if i < j
    ]
    off_centroid.sort(key=lambda x: -x[2])
    print(f"\n  Top 3 paires les plus proches (centroïdes) :")
    for a, b, v in off_centroid[:3]:
        print(f"    {a} × {b} = {v:.3f}")

    return {
        "by_type": scores,
        "cos_centroid_matrix": cos_centroid,
        "mean_ratio": round(mean_ratio, 4),
        "all_ok": ok_all,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Phase 4 : test de refinement — si paires problématiques, ajouter molécule
# ══════════════════════════════════════════════════════════════════════════════

def test_refinement(
    model: SentenceTransformer,
    bad_pairs: list[tuple[str, str, str, float]],
) -> dict:
    """
    Pour les paires encore proches après §83, tester l'ajout d'une 3e molécule
    discriminante pour séparer les types.

    Règle de refinement :
        Si type_A × type_B > 0.75, ajouter à l'un d'eux une molécule
        qui maximise la distance Jaccard par rapport à l'autre.
    """
    if not bad_pairs:
        print(f"\n  PHASE 4 — Aucune paire problématique : pas de refinement nécessaire ✓")
        return {"needed": False}

    from src.core.nipada_subject import atoms_in_5, _jaccard_5

    print(f"\n{'─'*72}")
    print("  PHASE 4 — Refinement des paires problématiques")
    print(f"{'─'*72}")

    synth = NipadaExtendedSynthesizer()

    # Candidats de refinement pour chaque type problématique
    # Molécules SUJET non encore utilisées comme modes
    used_mols: set[int] = {m for mols in MODES.values() for m in mols}
    candidates = [
        m for m in [11, 22, 33, 55, 66, 77, 110, 154, 165, 231, 330, 385, 462, 770, 1155, 2310]
        if m not in used_mols
    ]

    tested_pairs: list[dict] = []
    processed = set()

    for lang, a, b, val in bad_pairs:
        pair_key = f"{a}×{b}"
        if pair_key in processed:
            continue
        processed.add(pair_key)

        print(f"\n  Paire {a} × {b} (cos={val:.3f}) — langue {lang}")
        mols_a = MODES[a][:]
        mols_b = MODES[b][:]

        # Trouver la meilleure molécule à ajouter à 'a' pour maximiser distance vs 'b'
        best_mol, best_sep = None, 0.0
        for m in candidates:
            mols_new = mols_a + [m]
            text_new  = synth.synthesize(mols_new, lang)
            text_b    = synth.synthesize(mols_b,   lang)
            vecs = embed([text_new, text_b], model)
            sep = 1.0 - cosine(vecs[0], vecs[1])
            if sep > best_sep:
                best_sep, best_mol = sep, m

        if best_mol:
            mols_refined = mols_a + [best_mol]
            text_a_ref = synth.synthesize(mols_refined, lang)
            text_b_ref = synth.synthesize(mols_b, lang)
            vecs = embed([text_a_ref, text_b_ref], model)
            new_cos = cosine(vecs[0], vecs[1])
            print(f"    Meilleure molécule à ajouter à '{a}' : {best_mol}")
            print(f"    {a} [original] × {b} = {val:.3f}")
            print(f"    {a} [+{best_mol}]  × {b} = {new_cos:.3f}  (Δ={val-new_cos:+.3f})")
            tested_pairs.append({
                "pair": pair_key, "original_cos": val,
                "best_mol_to_add": best_mol, "to": a,
                "refined_cos": round(new_cos, 4),
                "improvement": round(val - new_cos, 4),
            })

    return {"needed": True, "tested": tested_pairs}


# ══════════════════════════════════════════════════════════════════════════════
# Pipeline principal
# ══════════════════════════════════════════════════════════════════════════════

def run() -> None:
    print(f"\n{'═'*72}")
    print("  §83 — Discrimination totale des actes de parole nipada")
    print(f"  7 types × MODE-MOLECULE unique × corpus enrichi 140 phrases")
    print(f"{'═'*72}")

    print(f"\n  Chargement du modèle : {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # Phase 0
    design_info = verify_mode_design()

    # Phase 1
    discrimination = compute_discrimination_matrix(model)

    # Phase 2
    alignment = compute_alignment_scores(model, discrimination)

    # Phase 3
    cluster = compute_cluster_scores(model)

    # Phase 4 (si nécessaire)
    bad_pairs = discrimination.get("bad_pairs", [])
    refinement = test_refinement(model, bad_pairs)

    # Verdict final
    total_disc = discrimination["total_discrimination"]
    align_ok   = alignment["ok"]
    ratio_ok   = cluster["all_ok"]

    print(f"\n{'═'*72}")
    print(f"  VERDICT §83")
    print(f"  Discrimination totale (max_off < 0.80) : "
          f"{'✓' if total_disc else '✗'}  (max={discrimination['global_max_off']:.3f})")
    print(f"  Alignement nipada/original (mean > 0.55) : "
          f"{'✓' if align_ok else '✗'}  (mean={alignment['mean_alignment']:.3f})")
    print(f"  Cluster ratio intra/inter > 1.5 (tous) : "
          f"{'✓' if ratio_ok else '✗'}  (mean={cluster['mean_ratio']:.3f})")
    success = total_disc and align_ok
    print(f"\n  STATUT : {'DISCRIMINATION TOTALE ATTEINTE ✓' if success else 'EN COURS — voir Phase 4'}")
    print()

    result = {
        "section": "§83",
        "title":   "Discrimination totale des actes de parole nipada",
        "date":    "2026-04-24",
        "model":   MODEL_NAME,
        "modes":   {k: v for k, v in MODES.items()},
        "corpus_size": f"{len(ACT_TYPES)} types × {len(LANGUAGES)} langues × 4 phrases",
        "design":    design_info,
        "discrimination_matrix": discrimination,
        "alignment":  alignment,
        "cluster":    cluster,
        "refinement": refinement,
        "success": success,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(_to_native(result), f, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"  Résultats → {OUTPUT_FILE}")


if __name__ == "__main__":
    run()

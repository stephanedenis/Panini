#!/usr/bin/env python3
"""
§85 — Benchmark UDHR 30 articles × 5 langues avec NipadaExtendedSynthesizer
=========================================================================
Pour chaque article UDHR :
  1. Encoder la phrase originale → embedding
  2. Classifier vers le mode nipada le plus proche (centroïde des 7 modes)
  3. Synthétiser le texte nipada avec les molécules du mode détecté
  4. Mesurer cycle_sim = cosine(embed(nipada_text), embed(original))
  5. Mesurer cross-lingual stability : cosine(nipada_fr, nipada_en) etc.

Output → research/nipada/falsification/nipada_udhr_benchmark.json
"""

import sys
import json
import itertools
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# ── chemins ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.core.nipada_subject import NipadaExtendedSynthesizer  # noqa: E402

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_udhr_benchmark.json"

# ── JSON NumPy 2.0 ────────────────────────────────────────────────────────────
class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _to_native(obj):
    if isinstance(obj, dict):
        return {k: _to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_native(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


# ── 7 modes ──────────────────────────────────────────────────────────────────
MODES = {
    "description":   [2, 5, 3],
    "définition":    [385, 66],
    "proclamation":  [33, 55, 77],
    "question":      [165, 11],
    "ordre":         [154, 231],
    "narration":     [462, 1155],
    "introspection": [2310, 22],
}

LANGS = ["fr", "en", "de", "es", "zh"]

# ── UDHR 30 articles — 1 phrase représentative par article × 5 langues ───────
# Source : DUDH (1948). Sélection d'une phrase représentative par article.
UDHR = {
    1: {
        "fr": "Tous les êtres humains naissent libres et égaux en dignité et en droits.",
        "en": "All human beings are born free and equal in dignity and rights.",
        "de": "Alle Menschen sind frei und gleich an Würde und Rechten geboren.",
        "es": "Todos los seres humanos nacen libres e iguales en dignidad y derechos.",
        "zh": "人人生而自由，在尊严和权利上一律平等。",
    },
    2: {
        "fr": "Chacun peut se prévaloir de tous les droits sans distinction aucune.",
        "en": "Everyone is entitled to all the rights without distinction of any kind.",
        "de": "Jeder Mensch hat Anspruch auf alle Rechte ohne irgendeinen Unterschied.",
        "es": "Toda persona tiene todos los derechos sin distinción alguna.",
        "zh": "人人有资格享有本宣言所载的一切权利和自由，不分任何区别。",
    },
    3: {
        "fr": "Tout individu a droit à la vie, à la liberté et à la sûreté de sa personne.",
        "en": "Everyone has the right to life, liberty and security of person.",
        "de": "Jeder Mensch hat das Recht auf Leben, Freiheit und Sicherheit der Person.",
        "es": "Todo individuo tiene derecho a la vida, a la libertad y a la seguridad.",
        "zh": "人人有权享有生命、自由和人身安全。",
    },
    4: {
        "fr": "Nul ne sera tenu en esclavage ni en servitude.",
        "en": "No one shall be held in slavery or servitude.",
        "de": "Niemand darf in Sklaverei oder Leibeigenschaft gehalten werden.",
        "es": "Nadie estará sometido a esclavitud ni a servidumbre.",
        "zh": "任何人不得使为奴隶或奴役。",
    },
    5: {
        "fr": "Nul ne sera soumis à la torture ni à des peines ou traitements cruels.",
        "en": "No one shall be subjected to torture or to cruel, inhuman or degrading treatment.",
        "de": "Niemand darf der Folter oder grausamer Behandlung unterworfen werden.",
        "es": "Nadie será sometido a torturas ni a penas o tratos crueles.",
        "zh": "任何人不得加以酷刑，或施以残忍的不人道待遇。",
    },
    6: {
        "fr": "Chacun a le droit à la reconnaissance en tous lieux de sa personnalité juridique.",
        "en": "Everyone has the right to recognition everywhere as a person before the law.",
        "de": "Jeder Mensch hat das Recht, überall als rechtsfähig anerkannt zu werden.",
        "es": "Todo ser humano tiene derecho al reconocimiento de su personalidad jurídica.",
        "zh": "人人在任何地方有权被承认在法律前的人格。",
    },
    7: {
        "fr": "Tous sont égaux devant la loi et ont droit à une égale protection de la loi.",
        "en": "All are equal before the law and entitled to equal protection of the law.",
        "de": "Alle Menschen sind vor dem Gesetz gleich und haben Anspruch auf gleichen Schutz.",
        "es": "Todos son iguales ante la ley y tienen derecho a igual protección.",
        "zh": "在法律面前，人人平等，并有权享受法律的平等保护。",
    },
    8: {
        "fr": "Toute personne a droit à un recours effectif devant les juridictions nationales.",
        "en": "Everyone has the right to an effective remedy by the national tribunals.",
        "de": "Jeder hat Anspruch auf wirksamen Rechtsschutz durch die zuständigen Gerichte.",
        "es": "Toda persona tiene derecho a un recurso efectivo ante los tribunales nacionales.",
        "zh": "任何人当其宪法或法律所赋予的权利遭受侵害时，均有权向主管法庭申诉。",
    },
    9: {
        "fr": "Nul ne peut être arbitrairement arrêté, détenu ou exilé.",
        "en": "No one shall be subjected to arbitrary arrest, detention or exile.",
        "de": "Niemand darf willkürlich festgenommen, in Haft gehalten oder ausgewiesen werden.",
        "es": "Nadie podrá ser arbitrariamente detenido, preso ni desterrado.",
        "zh": "任何人不得加以任意逮捕、拘禁或放逐。",
    },
    10: {
        "fr": "Toute personne a droit à ce que sa cause soit entendue équitablement.",
        "en": "Everyone is entitled to a fair and public hearing by an independent tribunal.",
        "de": "Jeder hat Anspruch darauf, in voller Gleichheit vor einem Gericht gehört zu werden.",
        "es": "Toda persona tiene derecho a ser oída con justicia por un tribunal independiente.",
        "zh": "人人完全平等地有权由独立而无偏倚的法庭进行公正的审讯。",
    },
    11: {
        "fr": "Toute personne accusée est présumée innocente jusqu'à ce que sa culpabilité soit légalement établie.",
        "en": "Everyone charged with an offence has the right to be presumed innocent until proved guilty.",
        "de": "Jeder Angeklagte hat das Recht, bis zum Beweis seiner Schuld als unschuldig zu gelten.",
        "es": "Toda persona acusada tiene derecho a que se presuma su inocencia.",
        "zh": "凡受刑事控告者，在未经依法公开审判证实有罪前，应视为无罪。",
    },
    12: {
        "fr": "Nul ne sera l'objet d'immixtions arbitraires dans sa vie privée.",
        "en": "No one shall be subjected to arbitrary interference with his privacy.",
        "de": "Niemand darf willkürlichen Eingriffen in sein Privatleben ausgesetzt werden.",
        "es": "Nadie será objeto de injerencias arbitrarias en su vida privada.",
        "zh": "任何人的私生活、家庭、住宅或通信不得任意干涉。",
    },
    13: {
        "fr": "Toute personne a le droit de circuler librement et de choisir sa résidence.",
        "en": "Everyone has the right to freedom of movement and residence within the borders of each state.",
        "de": "Jeder Mensch hat das Recht, sich innerhalb eines Staates frei zu bewegen.",
        "es": "Toda persona tiene derecho a circular libremente y a elegir su residencia.",
        "zh": "人人有权在各国境内自由迁徙和居住。",
    },
    14: {
        "fr": "Devant la persécution, toute personne a le droit de chercher asile.",
        "en": "Everyone has the right to seek and enjoy asylum from persecution.",
        "de": "Jeder Mensch hat das Recht, in anderen Ländern vor Verfolgung Asyl zu suchen.",
        "es": "En caso de persecución, toda persona tiene derecho a buscar asilo.",
        "zh": "人人有权在其他国家寻求和享受庇护以避免迫害。",
    },
    15: {
        "fr": "Tout individu a droit à une nationalité.",
        "en": "Everyone has the right to a nationality.",
        "de": "Jeder Mensch hat das Recht auf eine Staatsangehörigkeit.",
        "es": "Toda persona tiene derecho a una nacionalidad.",
        "zh": "人人有权享有国籍。",
    },
    16: {
        "fr": "Dès l'âge nubile, l'homme et la femme ont le droit de se marier sans restriction.",
        "en": "Men and women of full age have the right to marry without any limitation.",
        "de": "Heiratsfähige Männer und Frauen haben das Recht zu heiraten.",
        "es": "Los hombres y mujeres a partir de la edad núbil tienen derecho a casarse.",
        "zh": "成年男女有权不受限制地结婚。",
    },
    17: {
        "fr": "Toute personne a le droit à la propriété, seule ou en collectivité.",
        "en": "Everyone has the right to own property alone as well as in association with others.",
        "de": "Jeder Mensch hat das Recht auf Eigentum sowohl allein als auch in Gemeinschaft.",
        "es": "Toda persona tiene derecho a la propiedad individual y colectiva.",
        "zh": "人人得有单独财产所有权以及同他人合有财产所有权。",
    },
    18: {
        "fr": "Toute personne a droit à la liberté de pensée, de conscience et de religion.",
        "en": "Everyone has the right to freedom of thought, conscience and religion.",
        "de": "Jeder Mensch hat das Recht auf Gedanken-, Gewissens- und Religionsfreiheit.",
        "es": "Toda persona tiene derecho a la libertad de pensamiento, conciencia y religión.",
        "zh": "人人有权享有思想、良心和宗教自由。",
    },
    19: {
        "fr": "Tout individu a droit à la liberté d'opinion et d'expression.",
        "en": "Everyone has the right to freedom of opinion and expression.",
        "de": "Jeder Mensch hat das Recht auf freie Meinungsäußerung.",
        "es": "Todo individuo tiene derecho a la libertad de opinión y expresión.",
        "zh": "人人有权享有主张和发表意见的自由。",
    },
    20: {
        "fr": "Toute personne a droit à la liberté de réunion et d'association pacifiques.",
        "en": "Everyone has the right to freedom of peaceful assembly and association.",
        "de": "Jeder Mensch hat das Recht auf Versammlungs- und Vereinigungsfreiheit.",
        "es": "Toda persona tiene derecho a la libertad de reunión y de asociación pacíficas.",
        "zh": "人人有权享有和平集会和结社自由。",
    },
    21: {
        "fr": "Toute personne a le droit de prendre part à la direction des affaires publiques.",
        "en": "Everyone has the right to take part in the government of their country.",
        "de": "Jeder Mensch hat das Recht, an der Regierung seines Landes teilzunehmen.",
        "es": "Toda persona tiene derecho a participar en el gobierno de su país.",
        "zh": "人人有直接或通过自由选择的代表参与治理本国的权利。",
    },
    22: {
        "fr": "Toute personne a droit à la sécurité sociale et à la satisfaction des droits économiques.",
        "en": "Everyone has the right to social security and the realization of economic rights.",
        "de": "Jeder Mensch hat als Mitglied der Gesellschaft das Recht auf soziale Sicherheit.",
        "es": "Toda persona tiene derecho a la seguridad social y a los derechos económicos.",
        "zh": "每个人作为社会成员，有权享受社会保障。",
    },
    23: {
        "fr": "Toute personne a droit au travail, au libre choix de son travail et à une rémunération équitable.",
        "en": "Everyone has the right to work, to free choice of employment and to just remuneration.",
        "de": "Jeder Mensch hat das Recht auf Arbeit, freie Berufswahl und gerechten Lohn.",
        "es": "Toda persona tiene derecho al trabajo, a la libre elección de su trabajo y a remuneración equitativa.",
        "zh": "人人有权工作、自由选择职业、享受公正和合适的工作条件。",
    },
    24: {
        "fr": "Toute personne a droit au repos et aux loisirs.",
        "en": "Everyone has the right to rest and leisure.",
        "de": "Jeder Mensch hat das Recht auf Erholung und Freizeit.",
        "es": "Toda persona tiene derecho al descanso y al disfrute del tiempo libre.",
        "zh": "人人有享有休息和闲暇的权利。",
    },
    25: {
        "fr": "Toute personne a droit à un niveau de vie suffisant pour assurer sa santé et son bien-être.",
        "en": "Everyone has the right to a standard of living adequate for health and well-being.",
        "de": "Jeder Mensch hat das Recht auf einen Lebensstandard, der Gesundheit gewährleistet.",
        "es": "Toda persona tiene derecho a un nivel de vida adecuado que asegure su salud.",
        "zh": "人人有权享受本人及其家属的健康及福利所需的生活水准。",
    },
    26: {
        "fr": "Toute personne a droit à l'éducation.",
        "en": "Everyone has the right to education.",
        "de": "Jeder Mensch hat das Recht auf Bildung.",
        "es": "Toda persona tiene derecho a la educación.",
        "zh": "人人都有受教育的权利。",
    },
    27: {
        "fr": "Toute personne a le droit de prendre part librement à la vie culturelle de la communauté.",
        "en": "Everyone has the right freely to participate in the cultural life of the community.",
        "de": "Jeder Mensch hat das Recht, am kulturellen Leben der Gemeinschaft frei teilzunehmen.",
        "es": "Toda persona tiene derecho a participar libremente en la vida cultural de la comunidad.",
        "zh": "人人有权自由参加社区的文化生活。",
    },
    28: {
        "fr": "Toute personne a droit à ce que règne, sur le plan social et international, un ordre propice.",
        "en": "Everyone is entitled to a social and international order in which rights can be fully realized.",
        "de": "Jeder Mensch hat Anspruch auf eine soziale und internationale Ordnung, in welcher die Rechte verwirklicht werden können.",
        "es": "Toda persona tiene derecho a que se establezca un orden social en el que puedan realizarse los derechos.",
        "zh": "人人有权享受本宣言所载的权利和自由得以充分实现的社会的和国际的秩序。",
    },
    29: {
        "fr": "L'individu a des devoirs envers la communauté dans laquelle seul le libre développement est possible.",
        "en": "Everyone has duties to the community in which alone the free development of their personality is possible.",
        "de": "Jeder Mensch hat Pflichten gegenüber der Gemeinschaft, in der allein die freie Entfaltung möglich ist.",
        "es": "Toda persona tiene deberes respecto a la comunidad puesto que sólo en ella puede desarrollarse plenamente.",
        "zh": "人人对社区负有义务，个人的人格在社区中得到自由和充分发展。",
    },
    30: {
        "fr": "Rien dans la présente Déclaration ne peut être interprété comme impliquant pour un État le droit de se livrer à des activités contraires aux droits énoncés.",
        "en": "Nothing in this Declaration may be interpreted as implying any right to engage in activities aimed at the destruction of any of the rights set forth herein.",
        "de": "Keine Bestimmung dieser Erklärung darf dahin ausgelegt werden, dass sie ein Recht einschließt, Tätigkeiten auszuüben, die auf Beseitigung der hier aufgeführten Rechte gerichtet sind.",
        "es": "Nada en esta Declaración podrá interpretarse en el sentido de que confiere derecho a dedicarse a actividades tendientes a la supresión de los derechos.",
        "zh": "本宣言的任何条文不得解释为默许任何国家、集团或个人有权进行旨在破坏本宣言所载权利的活动。",
    },
}


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def main() -> None:
    WIDTH = 72
    print("═" * WIDTH)
    print("  §85 — Benchmark UDHR 30 articles × 5 langues")
    print("  NipadaExtendedSynthesizer · paraphrase-multilingual-MiniLM-L12-v2")
    print("═" * WIDTH)

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    synth = NipadaExtendedSynthesizer()

    # ── 1. Centroïdes des 7 modes (embedding nipada par langue) ──────────────
    print("\n  Calcul des centroïdes de mode (nipada)…")
    mode_centroids: dict[str, np.ndarray] = {}  # mode → centroid (384-dim, all langs)
    nipada_mode_texts: dict[str, dict[str, str]] = {}  # mode → lang → text

    for mode_name, mol_ids in MODES.items():
        vecs = []
        nipada_mode_texts[mode_name] = {}
        for lang in LANGS:
            text = synth.synthesize(mol_ids, lang)
            nipada_mode_texts[mode_name][lang] = text
            vecs.append(model.encode(text, show_progress_bar=False))
        mode_centroids[mode_name] = np.mean(vecs, axis=0)

    # ── 2. Benchmark article par article ─────────────────────────────────────
    print("\n  Traitement des 30 articles UDHR…\n")

    results_per_article: list[dict] = []

    for art_num in range(1, 31):
        art_sentences = UDHR[art_num]

        # Embed toutes les langues
        orig_vecs: dict[str, np.ndarray] = {
            lang: model.encode(art_sentences[lang], show_progress_bar=False)
            for lang in LANGS
        }
        orig_centroid = np.mean(list(orig_vecs.values()), axis=0)

        # Classification vers mode le plus proche
        sims_to_modes = {
            m: cosine(orig_centroid, mode_centroids[m]) for m in MODES
        }
        detected_mode = max(sims_to_modes, key=sims_to_modes.__getitem__)
        detected_mol_ids = MODES[detected_mode]

        # Synthèse nipada + embedding
        nipada_vecs: dict[str, np.ndarray] = {}
        nipada_texts: dict[str, str] = {}
        for lang in LANGS:
            t = synth.synthesize(detected_mol_ids, lang)
            nipada_texts[lang] = t
            nipada_vecs[lang] = model.encode(t, show_progress_bar=False)

        # cycle_sim par langue
        cycle_sims: dict[str, float] = {
            lang: cosine(nipada_vecs[lang], orig_vecs[lang]) for lang in LANGS
        }
        cycle_mean = float(np.mean(list(cycle_sims.values())))

        # cross-lingual stability (average pairwise cosine between nipada vecs)
        pairs = list(itertools.combinations(LANGS, 2))
        cl_sims = [cosine(nipada_vecs[la], nipada_vecs[lb]) for la, lb in pairs]
        cross_lingual_mean = float(np.mean(cl_sims)) if cl_sims else 0.0

        art_result = {
            "article": art_num,
            "detected_mode": detected_mode,
            "detected_mol_ids": detected_mol_ids,
            "sims_to_modes": {k: float(v) for k, v in sims_to_modes.items()},
            "cycle_sims": {k: float(v) for k, v in cycle_sims.items()},
            "cycle_mean": cycle_mean,
            "cross_lingual_mean": cross_lingual_mean,
            "nipada_texts": nipada_texts,
        }
        results_per_article.append(art_result)

        print(f"  Art.{art_num:2d}  mode={detected_mode:<15s}  "
              f"cycle={cycle_mean:.3f}  cross={cross_lingual_mean:.3f}")

    # ── 3. Agrégation par mode ────────────────────────────────────────────────
    from collections import defaultdict
    by_mode: dict[str, list[dict]] = defaultdict(list)
    for r in results_per_article:
        by_mode[r["detected_mode"]].append(r)

    mode_stats: dict[str, dict] = {}
    for mode_name, arts in by_mode.items():
        cycles = [a["cycle_mean"] for a in arts]
        cross = [a["cross_lingual_mean"] for a in arts]
        mode_stats[mode_name] = {
            "count": len(arts),
            "cycle_mean": float(np.mean(cycles)),
            "cycle_min": float(np.min(cycles)),
            "cycle_max": float(np.max(cycles)),
            "cross_lingual_mean": float(np.mean(cross)),
            "articles": [a["article"] for a in arts],
        }

    global_cycle_mean = float(np.mean([r["cycle_mean"] for r in results_per_article]))
    global_cross_mean = float(np.mean([r["cross_lingual_mean"] for r in results_per_article]))

    # ── 4. Affichage résumé ───────────────────────────────────────────────────
    print()
    print("─" * WIDTH)
    print("  RÉSUMÉ PAR MODE DÉTECTÉ")
    print("─" * WIDTH)
    header = f"  {'mode':<15s}  {'count':>5}  {'cycle_mean':>10}  {'cross_mean':>10}  articles"
    print(header)
    print("  " + "─" * (WIDTH - 2))
    for mode_name in MODES:
        if mode_name in mode_stats:
            s = mode_stats[mode_name]
            arts_str = ",".join(str(a) for a in s["articles"])
            print(f"  {mode_name:<15s}  {s['count']:>5d}  {s['cycle_mean']:>10.3f}  "
                  f"{s['cross_lingual_mean']:>10.3f}  [{arts_str}]")
        else:
            print(f"  {mode_name:<15s}  {'0':>5}  {'—':>10}  {'—':>10}")

    print()
    print("─" * WIDTH)
    print(f"  GLOBAL : cycle_mean={global_cycle_mean:.3f}  cross_lingual_mean={global_cross_mean:.3f}")
    print("─" * WIDTH)

    target_cycle = global_cycle_mean >= 0.55
    target_cross = global_cross_mean >= 0.80
    print(f"\n  CRITÈRE cycle_mean ≥ 0.55 : {'✓' if target_cycle else '✗'}  ({global_cycle_mean:.3f})")
    print(f"  CRITÈRE cross_lingual ≥ 0.80 : {'✓' if target_cross else '✗'}  ({global_cross_mean:.3f})")

    # ── 5. Sauvegarde JSON ────────────────────────────────────────────────────
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark": "§85 UDHR 30 articles × 5 langues",
        "model": "paraphrase-multilingual-MiniLM-L12-v2",
        "languages": LANGS,
        "modes": {k: v for k, v in MODES.items()},
        "global_cycle_mean": global_cycle_mean,
        "global_cross_lingual_mean": global_cross_mean,
        "mode_stats": mode_stats,
        "articles": _to_native(results_per_article),
    }
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, cls=_NpEncoder)

    print(f"\n  Résultats → {OUTPUT}")
    print("═" * WIDTH)


if __name__ == "__main__":
    main()

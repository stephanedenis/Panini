#!/usr/bin/env python3
"""§206v — WESTERN_RATIONAL × contemporary (1914 → présent), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_western_rational_contemporary_v206v.json"

WORKS = [
    # ── Phénoménologie & herméneutique
    ("husserl_krisis", "Die Krisis der europäischen Wissenschaften", "The Crisis of European Sciences", "deu", 1936, ["phenomenology", "crisis_of_reason"], "edmund_husserl"),
    ("husserl_cartesianische_meditationen", "Cartesianische Meditationen", "Cartesian Meditations", "deu", 1931, ["phenomenology"], "edmund_husserl"),
    ("heidegger_sein_und_zeit", "Sein und Zeit", "Being and Time", "deu", 1927, ["phenomenology", "existential_ontology"], "martin_heidegger"),
    ("heidegger_beitraege_zur_philosophie", "Beiträge zur Philosophie (Vom Ereignis)", "Contributions to Philosophy (From Enowning)", "deu", 1938, ["phenomenology", "later_heidegger"], "martin_heidegger"),
    ("heidegger_brief_ueber_den_humanismus", "Brief über den Humanismus", "Letter on Humanism", "deu", 1947, ["phenomenology", "later_heidegger"], "martin_heidegger"),
    ("merleau_ponty_phenomenologie_de_la_perception", "Phénoménologie de la perception", "Phenomenology of Perception", "fra", 1945, ["phenomenology", "embodiment"], "maurice_merleau_ponty"),
    ("merleau_ponty_le_visible_et_l_invisible", "Le visible et l'invisible", "The Visible and the Invisible", "fra", 1964, ["phenomenology", "ontology_late"], "maurice_merleau_ponty"),
    ("sartre_l_etre_et_le_neant", "L'Être et le néant", "Being and Nothingness", "fra", 1943, ["phenomenology", "existentialism"], "jean_paul_sartre"),
    ("sartre_critique_de_la_raison_dialectique", "Critique de la raison dialectique", "Critique of Dialectical Reason", "fra", 1960, ["existentialism", "marxist_dialectic"], "jean_paul_sartre"),
    ("ricoeur_de_l_interpretation", "De l'interprétation. Essai sur Freud", "Freud and Philosophy", "fra", 1965, ["hermeneutics"], "paul_ricoeur"),
    ("ricoeur_temps_et_recit", "Temps et récit", "Time and Narrative", "fra", 1983, ["hermeneutics", "narrative"], "paul_ricoeur"),
    ("ricoeur_soi_meme_comme_un_autre", "Soi-même comme un autre", "Oneself as Another", "fra", 1990, ["hermeneutics", "ethics"], "paul_ricoeur"),
    ("levinas_totalite_et_infini", "Totalité et infini", "Totality and Infinity", "fra", 1961, ["phenomenology", "ethics_of_alterity"], "emmanuel_levinas"),
    ("levinas_autrement_qu_etre", "Autrement qu'être ou au-delà de l'essence", "Otherwise than Being", "fra", 1974, ["phenomenology", "ethics_of_alterity"], "emmanuel_levinas"),
    ("gadamer_wahrheit_und_methode", "Wahrheit und Methode", "Truth and Method", "deu", 1960, ["hermeneutics"], "hans_georg_gadamer"),
    ("jaspers_philosophie", "Philosophie (3 vols)", "Philosophy (3 vols)", "deu", 1932, ["existentialism"], "karl_jaspers"),

    # ── Cercle de Vienne, empirisme logique, philosophie analytique précoce
    ("wittgenstein_tractatus", "Tractatus Logico-Philosophicus", "Tractatus Logico-Philosophicus", "deu", 1921, ["analytic", "logical_atomism"], "ludwig_wittgenstein"),
    ("wittgenstein_philosophische_untersuchungen", "Philosophische Untersuchungen", "Philosophical Investigations", "deu", 1953, ["analytic", "ordinary_language"], "ludwig_wittgenstein"),
    ("wittgenstein_ueber_gewissheit", "Über Gewißheit", "On Certainty", "deu", 1969, ["analytic", "epistemology"], "ludwig_wittgenstein"),
    ("russell_principia_mathematica_late", "Introduction to Mathematical Philosophy", "Introduction to Mathematical Philosophy", "eng", 1919, ["analytic", "philosophy_of_mathematics"], "bertrand_russell"),
    ("russell_history_of_western_philosophy", "A History of Western Philosophy", "A History of Western Philosophy", "eng", 1945, ["analytic", "history_of_philosophy"], "bertrand_russell"),
    ("whitehead_process_and_reality", "Process and Reality", "Process and Reality", "eng", 1929, ["process_philosophy", "speculative_metaphysics"], "alfred_north_whitehead"),
    ("carnap_der_logische_aufbau_der_welt", "Der logische Aufbau der Welt", "The Logical Structure of the World", "deu", 1928, ["logical_empiricism", "vienna_circle"], "rudolf_carnap"),
    ("carnap_logische_syntax_der_sprache", "Logische Syntax der Sprache", "The Logical Syntax of Language", "deu", 1934, ["logical_empiricism", "philosophy_of_language"], "rudolf_carnap"),
    ("carnap_meaning_and_necessity", "Meaning and Necessity", "Meaning and Necessity", "eng", 1947, ["logical_empiricism", "modal_logic"], "rudolf_carnap"),
    ("ayer_language_truth_and_logic", "Language, Truth and Logic", "Language, Truth and Logic", "eng", 1936, ["logical_empiricism"], "alfred_jules_ayer"),
    ("hempel_aspects_of_scientific_explanation", "Aspects of Scientific Explanation", "Aspects of Scientific Explanation", "eng", 1965, ["philosophy_of_science", "logical_empiricism"], "carl_hempel"),
    ("reichenbach_experience_and_prediction", "Experience and Prediction", "Experience and Prediction", "eng", 1938, ["logical_empiricism", "philosophy_of_science"], "hans_reichenbach"),

    # ── Quine, Davidson, Kripke, Putnam, Lewis
    ("quine_two_dogmas_of_empiricism", "Two Dogmas of Empiricism", "Two Dogmas of Empiricism", "eng", 1951, ["analytic", "philosophy_of_language"], "willard_van_orman_quine"),
    ("quine_word_and_object", "Word and Object", "Word and Object", "eng", 1960, ["analytic", "philosophy_of_language"], "willard_van_orman_quine"),
    ("davidson_essays_on_actions_and_events", "Essays on Actions and Events", "Essays on Actions and Events", "eng", 1980, ["analytic", "action_theory"], "donald_davidson"),
    ("davidson_inquiries_into_truth_and_interpretation", "Inquiries into Truth and Interpretation", "Inquiries into Truth and Interpretation", "eng", 1984, ["analytic", "philosophy_of_language"], "donald_davidson"),
    ("kripke_naming_and_necessity", "Naming and Necessity", "Naming and Necessity", "eng", 1980, ["analytic", "modal_metaphysics"], "saul_kripke"),
    ("kripke_wittgenstein_on_rules", "Wittgenstein on Rules and Private Language", "Wittgenstein on Rules and Private Language", "eng", 1982, ["analytic"], "saul_kripke"),
    ("putnam_meaning_and_reference", "The Meaning of Meaning", "The Meaning of 'Meaning'", "eng", 1975, ["analytic", "philosophy_of_language"], "hilary_putnam"),
    ("putnam_reason_truth_and_history", "Reason, Truth and History", "Reason, Truth and History", "eng", 1981, ["analytic", "epistemology"], "hilary_putnam"),
    ("david_lewis_on_the_plurality_of_worlds", "On the Plurality of Worlds", "On the Plurality of Worlds", "eng", 1986, ["analytic", "modal_realism"], "david_lewis"),

    # ── Philosophie du langage ordinaire, philosophie de l'esprit
    ("ryle_the_concept_of_mind", "The Concept of Mind", "The Concept of Mind", "eng", 1949, ["analytic", "philosophy_of_mind"], "gilbert_ryle"),
    ("austin_how_to_do_things_with_words", "How to Do Things with Words", "How to Do Things with Words", "eng", 1962, ["analytic", "speech_acts"], "j_l_austin"),
    ("strawson_individuals", "Individuals", "Individuals: An Essay in Descriptive Metaphysics", "eng", 1959, ["analytic", "metaphysics"], "p_f_strawson"),
    ("strawson_freedom_and_resentment", "Freedom and Resentment", "Freedom and Resentment", "eng", 1962, ["analytic", "ethics"], "p_f_strawson"),
    ("searle_speech_acts", "Speech Acts", "Speech Acts", "eng", 1969, ["analytic", "speech_acts"], "john_searle"),
    ("searle_the_construction_of_social_reality", "The Construction of Social Reality", "The Construction of Social Reality", "eng", 1995, ["analytic", "social_ontology"], "john_searle"),
    ("dennett_consciousness_explained", "Consciousness Explained", "Consciousness Explained", "eng", 1991, ["philosophy_of_mind", "analytic"], "daniel_dennett"),
    ("chalmers_the_conscious_mind", "The Conscious Mind", "The Conscious Mind", "eng", 1996, ["philosophy_of_mind"], "david_chalmers"),
    ("anscombe_intention", "Intention", "Intention", "eng", 1957, ["analytic", "action_theory", "ethics"], "g_e_m_anscombe"),

    # ── Philosophie des sciences post-positiviste
    ("popper_logik_der_forschung", "Logik der Forschung", "The Logic of Scientific Discovery", "deu", 1934, ["philosophy_of_science", "falsificationism"], "karl_popper"),
    ("popper_the_open_society", "The Open Society and Its Enemies", "The Open Society and Its Enemies", "eng", 1945, ["political_philosophy", "philosophy_of_science"], "karl_popper"),
    ("popper_conjectures_and_refutations", "Conjectures and Refutations", "Conjectures and Refutations", "eng", 1963, ["philosophy_of_science"], "karl_popper"),
    ("kuhn_the_structure_of_scientific_revolutions", "The Structure of Scientific Revolutions", "The Structure of Scientific Revolutions", "eng", 1962, ["philosophy_of_science", "post_positivism"], "thomas_kuhn"),
    ("lakatos_proofs_and_refutations", "Proofs and Refutations", "Proofs and Refutations", "eng", 1976, ["philosophy_of_mathematics"], "imre_lakatos"),
    ("feyerabend_against_method", "Against Method", "Against Method", "eng", 1975, ["philosophy_of_science", "epistemological_anarchism"], "paul_feyerabend"),

    # ── Éthique normative & politique libérale
    ("rawls_a_theory_of_justice", "A Theory of Justice", "A Theory of Justice", "eng", 1971, ["political_philosophy", "liberal_egalitarianism"], "john_rawls"),
    ("rawls_political_liberalism", "Political Liberalism", "Political Liberalism", "eng", 1993, ["political_philosophy"], "john_rawls"),
    ("nozick_anarchy_state_and_utopia", "Anarchy, State, and Utopia", "Anarchy, State, and Utopia", "eng", 1974, ["political_philosophy", "libertarianism"], "robert_nozick"),
    ("dworkin_taking_rights_seriously", "Taking Rights Seriously", "Taking Rights Seriously", "eng", 1977, ["legal_philosophy"], "ronald_dworkin"),
    ("hart_the_concept_of_law", "The Concept of Law", "The Concept of Law", "eng", 1961, ["legal_philosophy", "analytic"], "h_l_a_hart"),
    ("scanlon_what_we_owe_to_each_other", "What We Owe to Each Other", "What We Owe to Each Other", "eng", 1998, ["ethics", "contractualism"], "thomas_scanlon"),
    ("nagel_the_view_from_nowhere", "The View from Nowhere", "The View from Nowhere", "eng", 1986, ["analytic", "metaphysics_of_mind"], "thomas_nagel"),
    ("parfit_reasons_and_persons", "Reasons and Persons", "Reasons and Persons", "eng", 1984, ["analytic", "ethics", "personal_identity"], "derek_parfit"),
    ("parfit_on_what_matters", "On What Matters", "On What Matters", "eng", 2011, ["analytic", "ethics"], "derek_parfit"),
    ("williams_ethics_and_the_limits_of_philosophy", "Ethics and the Limits of Philosophy", "Ethics and the Limits of Philosophy", "eng", 1985, ["analytic", "ethics"], "bernard_williams"),
    ("williams_truth_and_truthfulness", "Truth and Truthfulness", "Truth and Truthfulness", "eng", 2002, ["analytic", "ethics"], "bernard_williams"),

    # ── Habermas & théorie critique rationaliste
    ("habermas_theorie_des_kommunikativen_handelns", "Theorie des kommunikativen Handelns", "Theory of Communicative Action", "deu", 1981, ["critical_theory_rational", "discourse_ethics"], "juergen_habermas"),
    ("habermas_faktizitaet_und_geltung", "Faktizität und Geltung", "Between Facts and Norms", "deu", 1992, ["critical_theory_rational", "legal_philosophy"], "juergen_habermas"),
    ("apel_diskurs_und_verantwortung", "Diskurs und Verantwortung", "Discourse and Responsibility", "deu", 1988, ["discourse_ethics"], "karl_otto_apel"),

    # ── Religion analytique & métaphysique néo-thomiste
    ("plantinga_warranted_christian_belief", "Warranted Christian Belief", "Warranted Christian Belief", "eng", 2000, ["analytic_philosophy_of_religion"], "alvin_plantinga"),
    ("maritain_les_degres_du_savoir", "Les degrés du savoir", "The Degrees of Knowledge", "fra", 1932, ["neo_thomism"], "jacques_maritain"),

    # ── Vertu & néo-aristotélisme
    ("macintyre_after_virtue", "After Virtue", "After Virtue", "eng", 1981, ["virtue_ethics", "neo_aristotelian"], "alasdair_macintyre"),
    ("taylor_sources_of_the_self", "Sources of the Self", "Sources of the Self", "eng", 1989, ["communitarianism", "moral_philosophy"], "charles_taylor"),
]

assert len(WORKS) == 70, f"WESTERN_RATIONAL×contemporary doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "phenomenology" in tags and "ethics_of_alterity" in tags:
        return "PHENOMENOLOGY_ALTERITY"
    if "phenomenology" in tags and "later_heidegger" in tags:
        return "LATER_HEIDEGGER"
    if "phenomenology" in tags and "existential_ontology" in tags:
        return "EXISTENTIAL_ONTOLOGY"
    if "phenomenology" in tags and "embodiment" in tags:
        return "PHENOMENOLOGY_BODY"
    if "phenomenology" in tags and "ontology_late" in tags:
        return "PHENOMENOLOGY_ONTOLOGY_LATE"
    if "phenomenology" in tags and "crisis_of_reason" in tags:
        return "HUSSERL_CRISIS"
    if "phenomenology" in tags and "existentialism" in tags:
        return "EXISTENTIAL_PHENOMENOLOGY"
    if "phenomenology" in tags:
        return "PHENOMENOLOGY"
    if "existentialism" in tags and "marxist_dialectic" in tags:
        return "EXISTENTIAL_MARXIST"
    if "existentialism" in tags:
        return "EXISTENTIALISM"
    if "hermeneutics" in tags and "narrative" in tags:
        return "HERMENEUTICS_NARRATIVE"
    if "hermeneutics" in tags and "ethics" in tags:
        return "HERMENEUTICS_ETHICS"
    if "hermeneutics" in tags:
        return "HERMENEUTICS"
    if "logical_atomism" in tags:
        return "LOGICAL_ATOMISM"
    if "ordinary_language" in tags:
        return "ORDINARY_LANGUAGE"
    if "logical_empiricism" in tags:
        return "LOGICAL_EMPIRICISM"
    if "philosophy_of_science" in tags and "falsificationism" in tags:
        return "POPPER_FALSIFICATIONISM"
    if "philosophy_of_science" in tags and "post_positivism" in tags:
        return "POST_POSITIVISM"
    if "philosophy_of_science" in tags and "epistemological_anarchism" in tags:
        return "FEYERABEND_ANARCHISM"
    if "philosophy_of_science" in tags:
        return "PHILOSOPHY_OF_SCIENCE"
    if "philosophy_of_mathematics" in tags:
        return "PHILOSOPHY_OF_MATHEMATICS"
    if "modal_realism" in tags:
        return "MODAL_REALISM"
    if "modal_logic" in tags:
        return "MODAL_LOGIC"
    if "modal_metaphysics" in tags:
        return "MODAL_METAPHYSICS"
    if "philosophy_of_language" in tags:
        return "PHILOSOPHY_OF_LANGUAGE"
    if "philosophy_of_mind" in tags or "metaphysics_of_mind" in tags:
        return "PHILOSOPHY_OF_MIND"
    if "speech_acts" in tags:
        return "SPEECH_ACTS"
    if "social_ontology" in tags:
        return "SOCIAL_ONTOLOGY"
    if "action_theory" in tags:
        return "ACTION_THEORY"
    if "personal_identity" in tags:
        return "PERSONAL_IDENTITY"
    if "virtue_ethics" in tags or "neo_aristotelian" in tags:
        return "VIRTUE_NEO_ARISTOTELIAN"
    if "communitarianism" in tags:
        return "COMMUNITARIANISM"
    if "contractualism" in tags:
        return "CONTRACTUALISM"
    if "liberal_egalitarianism" in tags:
        return "LIBERAL_EGALITARIANISM"
    if "libertarianism" in tags:
        return "LIBERTARIANISM"
    if "legal_philosophy" in tags:
        return "LEGAL_PHILOSOPHY"
    if "discourse_ethics" in tags:
        return "DISCOURSE_ETHICS"
    if "critical_theory_rational" in tags:
        return "CRITICAL_THEORY_RATIONAL"
    if "analytic_philosophy_of_religion" in tags:
        return "ANALYTIC_RELIGION"
    if "neo_thomism" in tags:
        return "NEO_THOMISM"
    if "process_philosophy" in tags:
        return "PROCESS_PHILOSOPHY"
    if "history_of_philosophy" in tags:
        return "HISTORY_OF_PHILOSOPHY"
    if "epistemology" in tags:
        return "ANALYTIC_EPISTEMOLOGY"
    if "ethics" in tags and "analytic" in tags:
        return "ANALYTIC_ETHICS"
    if "metaphysics" in tags and "analytic" in tags:
        return "ANALYTIC_METAPHYSICS"
    if "analytic" in tags:
        return "ANALYTIC_GENERAL"
    if "political_philosophy" in tags:
        return "POLITICAL_LIBERAL"
    return "WESTERN_RATIONAL_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "WESTERN_RATIONAL", "epoch": "contemporary",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 3,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "varies", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206v_western_rational_contemporary", "generated": "2026-04-30",
        "macro_culture": "WESTERN_RATIONAL", "epoch": "contemporary",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["academic editions", "stanford encyclopedia of philosophy"],
        "language_original_dominant": "deu + eng + fra",
        "schools_covered": [
            "Phénoménologie & herméneutique (Husserl ×2, Heidegger ×3, Merleau-Ponty ×2, Sartre ×2, Ricoeur ×3, Levinas ×2, Gadamer, Jaspers ×2)",
            "Empirisme logique & Cercle de Vienne (Wittgenstein ×3, Russell ×2, Whitehead, Carnap ×3, Ayer, Hempel, Reichenbach, Nagel-E.)",
            "Quine-Davidson-Kripke-Putnam-Lewis (×10)",
            "Langage ordinaire & philo. de l'esprit (Ryle, Austin, Strawson ×2, Searle ×2, Dennett, Chalmers, Anscombe ×2)",
            "Philo des sciences post-positiviste (Popper ×3, Kuhn, Lakatos ×2, Feyerabend)",
            "Éthique normative & libérale (Rawls ×2, Nozick, Dworkin, Hart, Scanlon, Nagel-T., Parfit ×2, Williams ×2)",
            "Habermas-Apel discours (×3)",
            "Religion analytique & néo-thomisme (Plantinga, Maritain)",
            "Vertu néo-aristotélicienne (MacIntyre, Taylor)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue WESTERN_RATIONAL × contemporary : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

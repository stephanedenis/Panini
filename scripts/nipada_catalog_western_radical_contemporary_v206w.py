#!/usr/bin/env python3
"""§206w — WESTERN_RADICAL × contemporary (1914 → présent), 70 œuvres."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_western_radical_contemporary_v206w.json"

WORKS = [
    # ── École de Francfort (théorie critique radicale)
    ("horkheimer_adorno_dialektik_der_aufklaerung", "Dialektik der Aufklärung", "Dialectic of Enlightenment", "deu", 1947, ["frankfurt_school", "critical_theory"], "max_horkheimer_theodor_adorno"),
    ("horkheimer_eclipse_of_reason", "Eclipse of Reason", "Eclipse of Reason", "eng", 1947, ["frankfurt_school"], "max_horkheimer"),
    ("adorno_negative_dialektik", "Negative Dialektik", "Negative Dialectics", "deu", 1966, ["frankfurt_school", "negative_dialectics"], "theodor_adorno"),
    ("adorno_minima_moralia", "Minima Moralia", "Minima Moralia", "deu", 1951, ["frankfurt_school"], "theodor_adorno"),
    ("benjamin_passagen_werk", "Das Passagen-Werk", "The Arcades Project", "deu", 1940, ["frankfurt_school", "messianic_marxism"], "walter_benjamin"),
    ("benjamin_ueber_den_begriff_der_geschichte", "Über den Begriff der Geschichte", "On the Concept of History", "deu", 1940, ["frankfurt_school", "messianic_marxism"], "walter_benjamin"),
    ("benjamin_kunstwerk_im_zeitalter", "Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit", "The Work of Art in the Age of Mechanical Reproduction", "deu", 1936, ["frankfurt_school", "media_theory"], "walter_benjamin"),
    ("marcuse_eros_und_zivilisation", "Eros and Civilization", "Eros and Civilization", "eng", 1955, ["frankfurt_school", "freudo_marxism"], "herbert_marcuse"),
    ("marcuse_one_dimensional_man", "One-Dimensional Man", "One-Dimensional Man", "eng", 1964, ["frankfurt_school"], "herbert_marcuse"),
    ("fromm_escape_from_freedom", "Escape from Freedom", "Escape from Freedom", "eng", 1941, ["frankfurt_school", "freudo_marxism"], "erich_fromm"),

    # ── Marxisme occidental & post-marxisme
    ("lukacs_geschichte_und_klassenbewusstsein", "Geschichte und Klassenbewußtsein", "History and Class Consciousness", "deu", 1923, ["western_marxism", "reification"], "georg_lukacs"),
    ("gramsci_quaderni_del_carcere", "Quaderni del carcere", "Prison Notebooks", "ita", 1935, ["western_marxism", "hegemony"], "antonio_gramsci"),
    ("althusser_pour_marx", "Pour Marx", "For Marx", "fra", 1965, ["structural_marxism"], "louis_althusser"),
    ("althusser_lire_le_capital", "Lire le Capital", "Reading Capital", "fra", 1965, ["structural_marxism"], "louis_althusser_etienne_balibar"),
    ("bloch_das_prinzip_hoffnung", "Das Prinzip Hoffnung", "The Principle of Hope", "deu", 1959, ["utopian_marxism"], "ernst_bloch"),
    ("debord_la_societe_du_spectacle", "La société du spectacle", "The Society of the Spectacle", "fra", 1967, ["situationism"], "guy_debord"),
    ("zizek_the_sublime_object_of_ideology", "The Sublime Object of Ideology", "The Sublime Object of Ideology", "eng", 1989, ["lacanian_marxism"], "slavoj_zizek"),
    ("badiou_letre_et_levenement", "L'être et l'événement", "Being and Event", "fra", 1988, ["communist_hypothesis"], "alain_badiou"),
    ("ranciere_la_mesentente", "La Mésentente", "Disagreement", "fra", 1995, ["post_marxism", "politics_of_dissensus"], "jacques_ranciere"),
    ("negri_hardt_empire", "Empire", "Empire", "eng", 2000, ["autonomist_marxism"], "antonio_negri_michael_hardt"),
    ("negri_hardt_multitude", "Multitude", "Multitude", "eng", 2004, ["autonomist_marxism"], "antonio_negri_michael_hardt"),
    ("laclau_mouffe_hegemony_and_socialist_strategy", "Hegemony and Socialist Strategy", "Hegemony and Socialist Strategy", "eng", 1985, ["post_marxism"], "ernesto_laclau_chantal_mouffe"),

    # ── Post-structuralisme (Foucault, Derrida, Deleuze, Lyotard, Lacan)
    ("foucault_les_mots_et_les_choses", "Les mots et les choses", "The Order of Things", "fra", 1966, ["post_structuralism"], "michel_foucault"),
    ("foucault_l_archeologie_du_savoir", "L'archéologie du savoir", "The Archaeology of Knowledge", "fra", 1969, ["post_structuralism"], "michel_foucault"),
    ("foucault_surveiller_et_punir", "Surveiller et punir", "Discipline and Punish", "fra", 1975, ["biopolitics", "post_structuralism"], "michel_foucault"),
    ("foucault_histoire_de_la_sexualite_1", "Histoire de la sexualité I : La volonté de savoir", "The History of Sexuality, vol. 1", "fra", 1976, ["biopolitics"], "michel_foucault"),
    ("foucault_naissance_de_la_biopolitique", "Naissance de la biopolitique (Cours 1978-79)", "The Birth of Biopolitics", "fra", 1979, ["biopolitics", "neoliberalism_critique"], "michel_foucault"),
    ("derrida_de_la_grammatologie", "De la grammatologie", "Of Grammatology", "fra", 1967, ["deconstruction"], "jacques_derrida"),
    ("derrida_l_ecriture_et_la_difference", "L'écriture et la différence", "Writing and Difference", "fra", 1967, ["deconstruction"], "jacques_derrida"),
    ("derrida_marges_de_la_philosophie", "Marges — de la philosophie", "Margins of Philosophy", "fra", 1972, ["deconstruction"], "jacques_derrida"),
    ("derrida_spectres_de_marx", "Spectres de Marx", "Specters of Marx", "fra", 1993, ["deconstruction", "post_marxism"], "jacques_derrida"),
    ("deleuze_difference_et_repetition", "Différence et répétition", "Difference and Repetition", "fra", 1968, ["post_structuralism"], "gilles_deleuze"),
    ("deleuze_guattari_l_anti_oedipe", "L'Anti-Œdipe", "Anti-Oedipus", "fra", 1972, ["schizoanalysis"], "gilles_deleuze_felix_guattari"),
    ("deleuze_guattari_mille_plateaux", "Mille plateaux", "A Thousand Plateaus", "fra", 1980, ["schizoanalysis"], "gilles_deleuze_felix_guattari"),
    ("lyotard_la_condition_postmoderne", "La condition postmoderne", "The Postmodern Condition", "fra", 1979, ["postmodernism"], "jean_francois_lyotard"),
    ("lyotard_le_differend", "Le différend", "The Differend", "fra", 1983, ["postmodernism"], "jean_francois_lyotard"),
    ("baudrillard_simulacres_et_simulation", "Simulacres et simulation", "Simulacra and Simulation", "fra", 1981, ["postmodernism", "media_theory"], "jean_baudrillard"),
    ("lacan_ecrits", "Écrits", "Écrits", "fra", 1966, ["psychoanalysis_radical"], "jacques_lacan"),
    ("lacan_seminaire_xi", "Le Séminaire XI : Les quatre concepts fondamentaux", "Seminar XI: The Four Fundamental Concepts", "fra", 1973, ["psychoanalysis_radical"], "jacques_lacan"),
    ("kristeva_pouvoirs_de_lhorreur", "Pouvoirs de l'horreur", "Powers of Horror", "fra", 1980, ["psychoanalysis_radical", "feminist_radical"], "julia_kristeva"),

    # ── Féminismes radicaux & queer
    ("de_beauvoir_le_deuxieme_sexe", "Le Deuxième Sexe", "The Second Sex", "fra", 1949, ["feminism_existential"], "simone_de_beauvoir"),
    ("wittig_la_pensee_straight", "La pensée straight", "The Straight Mind", "fra", 1980, ["lesbian_radical"], "monique_wittig"),
    ("federici_caliban_and_the_witch", "Caliban and the Witch", "Caliban and the Witch", "eng", 2004, ["marxist_feminism"], "silvia_federici"),
    ("butler_gender_trouble", "Gender Trouble", "Gender Trouble", "eng", 1990, ["queer_theory", "feminist_radical"], "judith_butler"),
    ("butler_bodies_that_matter", "Bodies That Matter", "Bodies That Matter", "eng", 1993, ["queer_theory"], "judith_butler"),
    ("haraway_simians_cyborgs_and_women", "Simians, Cyborgs and Women", "Simians, Cyborgs and Women", "eng", 1991, ["feminist_radical", "posthumanism"], "donna_haraway"),
    ("hooks_aint_i_a_woman", "Ain't I a Woman?", "Ain't I a Woman?", "eng", 1981, ["black_feminism"], "bell_hooks"),
    ("davis_women_race_and_class", "Women, Race & Class", "Women, Race & Class", "eng", 1981, ["black_feminism", "marxist_feminism"], "angela_davis"),
    ("crenshaw_demarginalizing_the_intersection", "Demarginalizing the Intersection of Race and Sex", "Demarginalizing the Intersection of Race and Sex", "eng", 1989, ["black_feminism", "intersectionality"], "kimberle_crenshaw"),
    ("collins_black_feminist_thought", "Black Feminist Thought", "Black Feminist Thought", "eng", 1990, ["black_feminism"], "patricia_hill_collins"),
    ("anzaldua_borderlands_la_frontera", "Borderlands / La Frontera", "Borderlands / La Frontera", "eng", 1987, ["chicana_feminism", "decolonial"], "gloria_anzaldua"),
    ("lorde_sister_outsider", "Sister Outsider", "Sister Outsider", "eng", 1984, ["black_feminism", "lesbian_radical"], "audre_lorde"),

    # ── Décolonial, post-colonial, Atlantique noir
    ("fanon_peau_noire_masques_blancs", "Peau noire, masques blancs", "Black Skin, White Masks", "fra", 1952, ["decolonial", "post_colonial"], "frantz_fanon"),
    ("fanon_les_damnes_de_la_terre", "Les Damnés de la Terre", "The Wretched of the Earth", "fra", 1961, ["decolonial", "anti_colonial_revolution"], "frantz_fanon"),
    ("cesaire_discours_sur_le_colonialisme", "Discours sur le colonialisme", "Discourse on Colonialism", "fra", 1950, ["decolonial", "negritude"], "aime_cesaire"),
    ("senghor_liberte_1", "Liberté I : Négritude et humanisme", "Liberty I: Negritude and Humanism", "fra", 1964, ["negritude"], "leopold_sedar_senghor"),
    ("said_orientalism", "Orientalism", "Orientalism", "eng", 1978, ["post_colonial"], "edward_said"),
    ("said_culture_and_imperialism", "Culture and Imperialism", "Culture and Imperialism", "eng", 1993, ["post_colonial"], "edward_said"),
    ("spivak_can_the_subaltern_speak", "Can the Subaltern Speak?", "Can the Subaltern Speak?", "eng", 1988, ["post_colonial", "subaltern_studies"], "gayatri_chakravorty_spivak"),
    ("bhabha_the_location_of_culture", "The Location of Culture", "The Location of Culture", "eng", 1994, ["post_colonial"], "homi_bhabha"),
    ("ngugi_decolonising_the_mind", "Decolonising the Mind", "Decolonising the Mind", "eng", 1986, ["decolonial", "linguistic_decolonization"], "ngugi_wa_thiongo"),
    ("cabral_unity_and_struggle", "A arma da teoria / Unity and Struggle", "Unity and Struggle", "por", 1969, ["decolonial", "anti_colonial_revolution"], "amilcar_cabral"),
    ("mariategui_siete_ensayos", "Siete ensayos de interpretación de la realidad peruana", "Seven Essays on Peruvian Reality", "spa", 1928, ["latin_american_marxism"], "jose_carlos_mariategui"),
    ("dussel_filosofia_de_la_liberacion", "Filosofía de la liberación", "Philosophy of Liberation", "spa", 1977, ["liberation_philosophy", "decolonial"], "enrique_dussel"),
    ("quijano_colonialidad_del_poder", "Colonialidad del poder, eurocentrismo y América Latina", "Coloniality of Power, Eurocentrism and Latin America", "spa", 2000, ["decolonial"], "anibal_quijano"),
    ("mignolo_the_darker_side_of_western_modernity", "The Darker Side of Western Modernity", "The Darker Side of Western Modernity", "eng", 2011, ["decolonial"], "walter_mignolo"),
    ("gilroy_the_black_atlantic", "The Black Atlantic", "The Black Atlantic", "eng", 1993, ["black_atlantic", "post_colonial"], "paul_gilroy"),
    ("wynter_unsettling_the_coloniality", "Unsettling the Coloniality of Being", "Unsettling the Coloniality of Being", "eng", 2003, ["decolonial", "black_radical_tradition"], "sylvia_wynter"),

    # ── Anarchismes, écologies politiques radicales
    ("bookchin_the_ecology_of_freedom", "The Ecology of Freedom", "The Ecology of Freedom", "eng", 1982, ["social_ecology", "anarchism"], "murray_bookchin"),
    ("agamben_homo_sacer", "Homo Sacer", "Homo Sacer", "ita", 1995, ["biopolitics", "post_structuralism"], "giorgio_agamben"),
]

assert len(WORKS) == 70, f"WESTERN_RADICAL×contemporary doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "frankfurt_school" in tags and "media_theory" in tags:
        return "FRANKFURT_MEDIA"
    if "frankfurt_school" in tags and "freudo_marxism" in tags:
        return "FREUDO_MARXISM"
    if "frankfurt_school" in tags and "messianic_marxism" in tags:
        return "MESSIANIC_MARXISM"
    if "frankfurt_school" in tags and "negative_dialectics" in tags:
        return "NEGATIVE_DIALECTICS"
    if "frankfurt_school" in tags and "aesthetics_critical" in tags:
        return "CRITICAL_AESTHETICS"
    if "frankfurt_school" in tags:
        return "FRANKFURT_SCHOOL"
    if "western_marxism" in tags and "reification" in tags:
        return "LUKACS_REIFICATION"
    if "western_marxism" in tags and "hegemony" in tags:
        return "GRAMSCI_HEGEMONY"
    if "western_marxism" in tags:
        return "WESTERN_MARXISM"
    if "structural_marxism" in tags:
        return "STRUCTURAL_MARXISM"
    if "utopian_marxism" in tags:
        return "UTOPIAN_MARXISM"
    if "situationism" in tags:
        return "SITUATIONISM"
    if "lacanian_marxism" in tags:
        return "LACANIAN_MARXISM"
    if "communist_hypothesis" in tags:
        return "BADIOU_COMMUNIST"
    if "post_marxism" in tags and "politics_of_dissensus" in tags:
        return "RANCIERE_DISSENSUS"
    if "post_marxism" in tags:
        return "POST_MARXISM"
    if "autonomist_marxism" in tags:
        return "AUTONOMIST_MARXISM"
    if "schizoanalysis" in tags:
        return "SCHIZOANALYSIS"
    if "deconstruction" in tags:
        return "DECONSTRUCTION"
    if "biopolitics" in tags and "neoliberalism_critique" in tags:
        return "BIOPOLITICS_NEOLIBERAL"
    if "biopolitics" in tags:
        return "BIOPOLITICS"
    if "post_structuralism" in tags:
        return "POST_STRUCTURALISM"
    if "postmodernism" in tags:
        return "POSTMODERNISM"
    if "psychoanalysis_radical" in tags and "feminist_radical" in tags:
        return "PSYCHOANALYSIS_FEMINIST"
    if "psychoanalysis_radical" in tags:
        return "PSYCHOANALYSIS_RADICAL"
    if "feminism_existential" in tags:
        return "FEMINISM_EXISTENTIAL"
    if "lesbian_radical" in tags and "black_feminism" in tags:
        return "LORDE_BLACK_LESBIAN"
    if "lesbian_radical" in tags:
        return "LESBIAN_RADICAL"
    if "marxist_feminism" in tags and "black_feminism" in tags:
        return "BLACK_MARXIST_FEMINISM"
    if "marxist_feminism" in tags:
        return "MARXIST_FEMINISM"
    if "queer_theory" in tags:
        return "QUEER_THEORY"
    if "intersectionality" in tags:
        return "INTERSECTIONALITY"
    if "black_feminism" in tags:
        return "BLACK_FEMINISM"
    if "chicana_feminism" in tags:
        return "CHICANA_FEMINISM"
    if "feminist_radical" in tags and "posthumanism" in tags:
        return "CYBORG_FEMINISM"
    if "feminist_radical" in tags:
        return "FEMINIST_RADICAL"
    if "decolonial" in tags and "negritude" in tags:
        return "NEGRITUDE_DECOLONIAL"
    if "decolonial" in tags and "anti_colonial_revolution" in tags:
        return "ANTI_COLONIAL_REVOLUTION"
    if "decolonial" in tags and "linguistic_decolonization" in tags:
        return "DECOLONIAL_LINGUISTIC"
    if "decolonial" in tags and "black_radical_tradition" in tags:
        return "BLACK_RADICAL_TRADITION"
    if "decolonial" in tags:
        return "DECOLONIAL"
    if "negritude" in tags:
        return "NEGRITUDE"
    if "post_colonial" in tags and "subaltern_studies" in tags:
        return "SUBALTERN_STUDIES"
    if "post_colonial" in tags:
        return "POST_COLONIAL"
    if "black_atlantic" in tags:
        return "BLACK_ATLANTIC"
    if "liberation_philosophy" in tags:
        return "LIBERATION_PHILOSOPHY"
    if "latin_american_marxism" in tags:
        return "LATIN_AMERICAN_MARXISM"
    if "social_ecology" in tags or "anarchism" in tags:
        return "SOCIAL_ECOLOGY_ANARCHISM"
    return "WESTERN_RADICAL_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid, "title_original": title, "title_en": title_en,
            "macro_culture": "WESTERN_RADICAL", "epoch": "contemporary",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang, "year_estimate": year, "year_uncertainty": 3,
            "author": author, "url_original": None, "url_translation_en": None,
            "translator_canonical_en": None, "tags": tags,
            "license_status": "varies", "ingestion_status": "catalog_only",
        })
    payload = {
        "version": "v206w_western_radical_contemporary", "generated": "2026-04-30",
        "macro_culture": "WESTERN_RADICAL", "epoch": "contemporary",
        "n_works": len(catalog), "target": 70,
        "primary_sources": ["academic editions", "marxists.org", "post-colonial archives"],
        "language_original_dominant": "fra + deu + eng + ita + spa + por",
        "schools_covered": [
            "École de Francfort (Horkheimer ×2, Adorno ×3, Benjamin ×3, Marcuse ×2, Fromm)",
            "Marxisme occidental & post-marxisme (Lukács, Gramsci, Althusser ×2, Bloch, Debord, Žižek, Badiou, Rancière, Negri-Hardt ×2, Laclau-Mouffe)",
            "Post-structuralisme (Foucault ×5, Derrida ×4, Deleuze ×2, Deleuze-Guattari ×2, Lyotard ×2, Baudrillard, Lacan ×2, Kristeva)",
            "Féminismes radicaux & queer (de Beauvoir, Wittig, Federici, Butler ×2, Haraway, hooks, Davis, Crenshaw, Collins, Anzaldúa, Lorde)",
            "Décolonial & post-colonial (Fanon ×2, Césaire, Senghor, Said ×2, Spivak, Bhabha, Ngũgĩ, Cabral, Mariátegui, Dussel, Quijano, Mignolo, Gilroy, Wynter)",
            "Écologie radicale & biopolitique (Bookchin, Agamben)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue WESTERN_RADICAL × contemporary : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

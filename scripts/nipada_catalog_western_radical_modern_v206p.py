#!/usr/bin/env python3
"""
§206p — Catalogue WESTERN_RADICAL × modern (1789 → 1914), 70 œuvres.

Cellule des ruptures radicales modernes. Distincte de WESTERN_RATIONAL.modern :
là où WESTERN_RATIONAL critique de l'intérieur (Hegel, Marx orthodoxe,
positivisme), WESTERN_RADICAL rejette les fondements (anarchisme, féminisme
premier, socialisme utopique, théosophie/occultisme post-Lumières,
nihilisme russe, anti-impérialisme).

Strates :
- Anarchistes (Stirner, Bakounine, Proudhon, Kropotkine, Goldman, Reclus)
- Socialistes utopiques pré-marxiens (Saint-Simon, Fourier, Owen, Cabet)
- Féministes premières vagues (Wollstonecraft, Stanton, Anthony, Mill-Taylor,
  Pankhurst, Goldman)
- Nihilistes russes (Bakounine, Tchernychevski, Pissarev, Netchaïev)
- Théosophie & occultisme (Blavatsky, Steiner premier, Eliphas Lévi)
- Esclavagisme & abolition (Wollstonecraft, Douglass, Tubman, Du Bois)
- Anti-impérialistes (Du Bois, Garvey premier, Aurobindo Karmayogin)
- Romantismes radicaux (Shelley, Blake, Hugo Misérables, Tolstoï religieux)
- Psychanalyse comme rupture (Freud)

Sources : Marxists Internet Archive, Anarchy Archives, Project Gutenberg,
Wikisource, Sacred Texts (théosophie).
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_western_radical_modern_v206p.json"

WORKS = [
    # ── Féminisme première vague
    ("wollstonecraft_vindication_rights_woman", "A Vindication of the Rights of Woman", "A Vindication of the Rights of Woman", "eng", 1792, ["feminism_first_wave"], "wollstonecraft"),
    ("wollstonecraft_vindication_rights_men", "A Vindication of the Rights of Men", "A Vindication of the Rights of Men", "eng", 1790, ["feminism_first_wave", "politics"], "wollstonecraft"),
    ("stanton_solitude_self", "The Solitude of Self", "The Solitude of Self", "eng", 1892, ["feminism_first_wave"], "elizabeth_cady_stanton"),
    ("stanton_womans_bible", "The Woman's Bible", "The Woman's Bible", "eng", 1898, ["feminism_first_wave", "religion"], "elizabeth_cady_stanton"),
    ("anthony_speeches", "Is It a Crime for a U.S. Citizen to Vote?", "Speeches and Writings of Susan B. Anthony", "eng", 1873, ["feminism_first_wave"], "susan_b_anthony"),
    ("pankhurst_my_own_story", "My Own Story", "My Own Story", "eng", 1914, ["feminism_first_wave"], "emmeline_pankhurst"),
    ("gilman_yellow_wallpaper", "The Yellow Wall-Paper", "The Yellow Wallpaper", "eng", 1892, ["feminism_first_wave"], "charlotte_perkins_gilman"),
    ("gilman_women_economics", "Women and Economics", "Women and Economics", "eng", 1898, ["feminism_first_wave", "economics"], "charlotte_perkins_gilman"),

    # ── Socialistes utopiques
    ("saint_simon_nouveau_christianisme", "Le Nouveau Christianisme", "The New Christianity", "frm", 1825, ["socialist_utopian"], "saint_simon"),
    ("saint_simon_systeme_industriel", "Du Système industriel", "The Industrial System", "frm", 1821, ["socialist_utopian"], "saint_simon"),
    ("fourier_theorie_quatre_mouvements", "Théorie des quatre mouvements et des destinées générales", "Theory of the Four Movements", "frm", 1808, ["socialist_utopian"], "fourier"),
    ("fourier_nouveau_monde_industriel", "Le Nouveau Monde industriel et sociétaire", "The New Industrial and Societal World", "frm", 1829, ["socialist_utopian"], "fourier"),
    ("owen_new_view_society", "A New View of Society", "A New View of Society", "eng", 1813, ["socialist_utopian"], "robert_owen"),
    ("owen_book_new_moral_world", "The Book of the New Moral World", "Book of the New Moral World", "eng", 1836, ["socialist_utopian"], "robert_owen"),
    ("cabet_voyage_icarie", "Voyage en Icarie", "Travels in Icaria", "frm", 1840, ["socialist_utopian"], "etienne_cabet"),
    ("blanqui_critique_sociale", "Critique sociale", "Social Critique", "frm", 1885, ["socialist_revolutionary"], "auguste_blanqui"),

    # ── Anarchisme
    ("godwin_political_justice", "An Enquiry Concerning Political Justice", "Enquiry Concerning Political Justice", "eng", 1793, ["anarchist", "proto"], "william_godwin"),
    ("stirner_einzige", "Der Einzige und sein Eigentum", "The Ego and Its Own", "deu", 1844, ["anarchist", "individualist"], "max_stirner"),
    ("proudhon_quest_propriete", "Qu'est-ce que la propriété?", "What Is Property?", "frm", 1840, ["anarchist", "mutualist"], "proudhon"),
    ("proudhon_systeme_contradictions", "Système des contradictions économiques", "System of Economic Contradictions", "frm", 1846, ["anarchist", "mutualist"], "proudhon"),
    ("proudhon_principe_federatif", "Du principe fédératif", "The Principle of Federation", "frm", 1863, ["anarchist", "mutualist"], "proudhon"),
    ("bakunin_god_state", "Dieu et l'État", "God and the State", "frm", 1882, ["anarchist", "collectivist"], "bakunin"),
    ("bakunin_statism_anarchy", "Государственность и анархия", "Statism and Anarchy", "rus", 1873, ["anarchist", "collectivist"], "bakunin"),
    ("kropotkin_mutual_aid", "Mutual Aid: A Factor of Evolution", "Mutual Aid", "eng", 1902, ["anarchist", "communist_anarchist"], "kropotkin"),
    ("kropotkin_conquest_bread", "La Conquête du pain", "The Conquest of Bread", "frm", 1892, ["anarchist", "communist_anarchist"], "kropotkin"),
    ("kropotkin_fields_factories", "Fields, Factories and Workshops", "Fields, Factories and Workshops", "eng", 1899, ["anarchist", "communist_anarchist"], "kropotkin"),
    ("malatesta_anarchy", "L'Anarchia", "Anarchy", "ita", 1891, ["anarchist"], "errico_malatesta"),
    ("goldman_anarchism_essays", "Anarchism and Other Essays", "Anarchism and Other Essays", "eng", 1910, ["anarchist", "feminism_first_wave"], "emma_goldman"),
    ("reclus_homme_et_la_terre", "L'Homme et la Terre", "Man and the Earth", "frm", 1905, ["anarchist", "geography"], "elisee_reclus"),
    ("tucker_instead_of_book", "Instead of a Book", "Instead of a Book", "eng", 1893, ["anarchist", "individualist"], "benjamin_tucker"),
    ("thoreau_civil_disobedience", "Resistance to Civil Government", "Civil Disobedience", "eng", 1849, ["anarchist", "transcendentalist"], "thoreau"),
    ("thoreau_walden", "Walden; or, Life in the Woods", "Walden", "eng", 1854, ["anarchist", "transcendentalist"], "thoreau"),

    # ── Nihilisme russe & socialisme révolutionnaire
    ("chernyshevsky_what_is_be_done", "Что делать?", "What Is to Be Done?", "rus", 1863, ["nihilist_russian"], "chernyshevsky"),
    ("pisarev_destruction_aesthetics", "Разрушение эстетики", "The Destruction of Aesthetics", "rus", 1865, ["nihilist_russian"], "pisarev"),
    ("nechaev_catechism_revolutionary", "Катехизис революционера", "Catechism of a Revolutionary", "rus", 1869, ["nihilist_russian"], "nechaev"),
    ("herzen_from_other_shore", "С того берега", "From the Other Shore", "rus", 1855, ["socialist_revolutionary"], "alexander_herzen"),

    # ── Marxisme hétérodoxe & socialisme international
    ("rosa_luxemburg_accumulation_capital", "Die Akkumulation des Kapitals", "The Accumulation of Capital", "deu", 1913, ["marxist_heterodox"], "rosa_luxemburg"),
    ("rosa_luxemburg_reform_revolution", "Sozialreform oder Revolution?", "Reform or Revolution", "deu", 1899, ["marxist_heterodox"], "rosa_luxemburg"),
    ("kautsky_road_to_power", "Der Weg zur Macht", "The Road to Power", "deu", 1909, ["marxist_orthodox"], "kautsky"),
    ("bernstein_evolutionary_socialism", "Die Voraussetzungen des Sozialismus", "Evolutionary Socialism", "deu", 1899, ["socialist_revisionist"], "bernstein"),
    ("lenin_what_is_to_be_done", "Что делать?", "What Is to Be Done?", "rus", 1902, ["marxist_revolutionary"], "lenin"),
    ("lenin_imperialism_highest_stage", "Империализм, как высшая стадия капитализма", "Imperialism, the Highest Stage of Capitalism", "rus", 1916, ["marxist_revolutionary"], "lenin"),
    ("sorel_reflections_violence", "Réflexions sur la violence", "Reflections on Violence", "frm", 1908, ["syndicalist_revolutionary"], "sorel"),

    # ── Théosophie & occultisme
    ("blavatsky_isis_unveiled", "Isis Unveiled", "Isis Unveiled", "eng", 1877, ["theosophy"], "blavatsky"),
    ("blavatsky_secret_doctrine", "The Secret Doctrine", "The Secret Doctrine", "eng", 1888, ["theosophy"], "blavatsky"),
    ("blavatsky_key_to_theosophy", "The Key to Theosophy", "The Key to Theosophy", "eng", 1889, ["theosophy"], "blavatsky"),
    ("levi_dogme_haute_magie", "Dogme et rituel de la haute magie", "Transcendental Magic", "frm", 1856, ["occultism"], "eliphas_levi"),
    ("steiner_theosophie", "Theosophie", "Theosophy", "deu", 1904, ["theosophy", "anthroposophy"], "rudolf_steiner"),
    ("besant_ancient_wisdom", "The Ancient Wisdom", "The Ancient Wisdom", "eng", 1897, ["theosophy"], "annie_besant"),

    # ── Abolition & anti-racisme
    ("douglass_narrative", "Narrative of the Life of Frederick Douglass", "Narrative of the Life of Frederick Douglass", "eng", 1845, ["abolitionist"], "frederick_douglass"),
    ("douglass_my_bondage", "My Bondage and My Freedom", "My Bondage and My Freedom", "eng", 1855, ["abolitionist"], "frederick_douglass"),
    ("dubois_souls_black_folk", "The Souls of Black Folk", "The Souls of Black Folk", "eng", 1903, ["anti_racist", "panafrican"], "w_e_b_du_bois"),
    ("dubois_black_reconstruction_proto", "John Brown", "John Brown (1909)", "eng", 1909, ["anti_racist"], "w_e_b_du_bois"),
    ("garvey_philosophy_opinions_proto", "Philosophy and Opinions of Marcus Garvey (early speeches)", "Early Speeches of Marcus Garvey", "eng", 1914, ["panafrican"], "marcus_garvey"),
    ("truth_aint_i_woman", "Ain't I a Woman?", "Ain't I a Woman?", "eng", 1851, ["abolitionist", "feminism_first_wave"], "sojourner_truth"),

    # ── Psychanalyse comme rupture
    ("freud_traumdeutung", "Die Traumdeutung", "The Interpretation of Dreams", "deu", 1900, ["psychoanalysis"], "freud"),
    ("freud_drei_abhandlungen", "Drei Abhandlungen zur Sexualtheorie", "Three Essays on the Theory of Sexuality", "deu", 1905, ["psychoanalysis"], "freud"),
    ("freud_totem_taboo", "Totem und Tabu", "Totem and Taboo", "deu", 1913, ["psychoanalysis", "anthropology"], "freud"),
    ("freud_psychopathologie_alltagslebens", "Zur Psychopathologie des Alltagslebens", "The Psychopathology of Everyday Life", "deu", 1901, ["psychoanalysis"], "freud"),

    # ── Tolstoï religieux radical
    ("tolstoy_kingdom_of_god", "Царство Божие внутри вас", "The Kingdom of God Is Within You", "rus", 1894, ["christian_anarchism", "pacifism"], "tolstoy"),
    ("tolstoy_what_is_art", "Что такое искусство?", "What Is Art?", "rus", 1898, ["christian_anarchism"], "tolstoy"),
    ("tolstoy_confession", "Исповедь", "A Confession", "rus", 1882, ["christian_anarchism"], "tolstoy"),

    # ── Romantismes radicaux & littérature politique
    ("shelley_mask_of_anarchy", "The Mask of Anarchy", "The Mask of Anarchy", "eng", 1832, ["romantic_radical"], "percy_shelley"),
    ("shelley_defence_of_poetry", "A Defence of Poetry", "A Defence of Poetry", "eng", 1840, ["romantic_radical"], "percy_shelley"),
    ("blake_marriage_heaven_hell", "The Marriage of Heaven and Hell", "The Marriage of Heaven and Hell", "eng", 1793, ["romantic_radical", "mystical"], "william_blake"),
    ("blake_jerusalem", "Jerusalem: The Emanation of the Giant Albion", "Jerusalem", "eng", 1820, ["romantic_radical", "mystical"], "william_blake"),
    ("hugo_miserables", "Les Misérables", "Les Misérables", "frm", 1862, ["romantic_radical", "social_novel"], "victor_hugo"),
    ("zola_jaccuse", "J'accuse...!", "J'accuse...!", "frm", 1898, ["social_novel", "anti_authoritarian"], "emile_zola"),
    ("ruskin_unto_this_last", "Unto This Last", "Unto This Last", "eng", 1862, ["socialist_ethical", "art_critic"], "ruskin"),
    ("morris_news_from_nowhere", "News from Nowhere", "News from Nowhere", "eng", 1890, ["socialist_utopian"], "william_morris"),
]

assert len(WORKS) == 70, f"WESTERN_RADICAL×modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "feminism_first_wave" in tags and "anarchist" in tags:
        return "ANARCHIST_FEMINIST"
    if "feminism_first_wave" in tags and "abolitionist" in tags:
        return "ABOLITIONIST_FEMINIST"
    if "feminism_first_wave" in tags:
        return "FEMINIST_FIRST_WAVE"
    if "anarchist" in tags and "individualist" in tags:
        return "ANARCHIST_INDIVIDUALIST"
    if "anarchist" in tags and "mutualist" in tags:
        return "ANARCHIST_MUTUALIST"
    if "anarchist" in tags and "collectivist" in tags:
        return "ANARCHIST_COLLECTIVIST"
    if "anarchist" in tags and "communist_anarchist" in tags:
        return "ANARCHIST_COMMUNIST"
    if "anarchist" in tags and "transcendentalist" in tags:
        return "TRANSCENDENTALIST_ANARCHIST"
    if "anarchist" in tags:
        return "ANARCHIST_OTHER"
    if "socialist_utopian" in tags:
        return "SOCIALIST_UTOPIAN"
    if "socialist_revolutionary" in tags:
        return "SOCIALIST_REVOLUTIONARY"
    if "socialist_revisionist" in tags:
        return "SOCIALIST_REVISIONIST"
    if "socialist_ethical" in tags:
        return "SOCIALIST_ETHICAL"
    if "syndicalist_revolutionary" in tags:
        return "SYNDICALIST_REVOLUTIONARY"
    if "marxist_heterodox" in tags:
        return "MARXIST_HETERODOX"
    if "marxist_orthodox" in tags:
        return "MARXIST_ORTHODOX"
    if "marxist_revolutionary" in tags:
        return "MARXIST_REVOLUTIONARY"
    if "nihilist_russian" in tags:
        return "NIHILIST_RUSSIAN"
    if "theosophy" in tags:
        return "THEOSOPHY"
    if "occultism" in tags:
        return "OCCULTISM"
    if "abolitionist" in tags:
        return "ABOLITIONIST"
    if "anti_racist" in tags:
        return "ANTI_RACIST"
    if "panafrican" in tags:
        return "PANAFRICAN"
    if "psychoanalysis" in tags:
        return "PSYCHOANALYSIS"
    if "christian_anarchism" in tags:
        return "CHRISTIAN_ANARCHIST"
    if "romantic_radical" in tags:
        return "ROMANTIC_RADICAL"
    if "social_novel" in tags:
        return "SOCIAL_NOVEL"
    return "RADICAL_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "WESTERN_RADICAL",
            "epoch": "modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 3,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206p_western_radical_modern",
        "generated": "2026-04-29",
        "macro_culture": "WESTERN_RADICAL",
        "epoch": "modern",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["Marxists Internet Archive", "Anarchy Archives", "Project Gutenberg", "Wikisource (multi)", "Sacred Texts (théosophie)", "Library of America"],
        "language_original_dominant": "eng + frm + deu + rus",
        "schools_covered": [
            "Féminisme première vague (Wollstonecraft ×2, Stanton ×2, Anthony, Pankhurst, Gilman ×2)",
            "Socialistes utopiques (Saint-Simon ×2, Fourier ×2, Owen ×2, Cabet, Blanqui)",
            "Anarchisme (Godwin, Stirner, Proudhon ×3, Bakounine ×2, Kropotkine ×3, Malatesta, Goldman, Reclus, Tucker, Thoreau ×2)",
            "Nihilisme russe (Tchernychevski, Pissarev, Netchaïev, Herzen)",
            "Marxisme hétérodoxe + révisionnisme + Lénine pré-1917 + Sorel (×7)",
            "Théosophie & occultisme (Blavatsky ×3, Lévi, Steiner, Besant)",
            "Abolition + anti-racisme (Douglass ×2, Du Bois ×2, Garvey, Sojourner Truth)",
            "Psychanalyse comme rupture (Freud ×4)",
            "Tolstoï religieux radical (×3)",
            "Romantismes radicaux (Shelley ×2, Blake ×2, Hugo, Zola, Ruskin, Morris)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue WESTERN_RADICAL × modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

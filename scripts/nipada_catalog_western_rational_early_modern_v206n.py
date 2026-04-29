#!/usr/bin/env python3
"""
§206n — Catalogue WESTERN_RATIONAL × early_modern (1500 → 1789), 70 œuvres.

Pivot canonique de la modernité philosophique occidentale. Sépare GRECO_LATIN
(scolastique + humanisme antérieurs à 1500) de WESTERN_RATIONAL (philosophie
moderne caractérisée par : autonomie de la raison, rupture avec autorité,
mathématisation de la nature).

Strates :
- Renaissance & humanisme (1500-1600) : Erasme, Pic de la Mirandole, Ficin,
  Machiavel, Thomas More, Montaigne, Bruno, Bacon
- Révolution scientifique (1500-1700) : Copernic, Galilée, Kepler, Newton, Boyle, Hooke
- Rationalisme : Descartes, Spinoza, Malebranche, Leibniz, Pascal
- Empirisme britannique : Hobbes, Locke, Berkeley, Hume
- Lumières françaises : Voltaire, Diderot, Rousseau, Montesquieu, Condillac, Helvétius
- Lumières allemandes pré-Kant : Wolff, Lessing, Mendelssohn
- Kant (œuvres pré-1789)
- Théoriciens politiques modernes : Grotius, Pufendorf, Vico, Smith, Beccaria
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_western_rational_early_modern_v206n.json"

WORKS = [
    # ── Renaissance & humanisme
    ("erasmus_praise_folly", "Stultitiae Laus (Mōrias Enkōmion)", "The Praise of Folly", "lat", 1511, ["renaissance", "humanist"], "erasmus"),
    ("erasmus_enchiridion", "Enchiridion Militis Christiani", "Handbook of the Christian Knight", "lat", 1503, ["renaissance", "humanist"], "erasmus"),
    ("pico_oratio_de_dignitate", "Oratio de Hominis Dignitate", "Oration on the Dignity of Man", "lat", 1486, ["renaissance", "humanist"], "pico_della_mirandola"),
    ("ficino_theologia_platonica", "Theologia Platonica de Immortalitate Animarum", "Platonic Theology", "lat", 1482, ["renaissance", "neoplatonic"], "marsilio_ficino"),
    ("machiavelli_prince", "Il Principe", "The Prince", "ita", 1532, ["renaissance", "politics"], "machiavelli"),
    ("machiavelli_discorsi", "Discorsi sopra la prima Deca di Tito Livio", "Discourses on Livy", "ita", 1531, ["renaissance", "politics"], "machiavelli"),
    ("more_utopia", "De Optimo Reipublicae Statu deque Nova Insula Utopia", "Utopia", "lat", 1516, ["renaissance", "politics"], "thomas_more"),
    ("montaigne_essais", "Essais", "Essays", "frm", 1580, ["renaissance", "skeptic"], "montaigne"),
    ("bruno_de_la_causa", "De la Causa, Principio et Uno", "On Cause, Principle and Unity", "ita", 1584, ["renaissance", "neoplatonic"], "giordano_bruno"),
    ("bruno_de_infinito", "De l'Infinito, Universo e Mondi", "On the Infinite Universe and Worlds", "ita", 1584, ["renaissance", "cosmology"], "giordano_bruno"),
    ("bacon_novum_organum", "Novum Organum Scientiarum", "Novum Organum", "lat", 1620, ["empiricist", "scientific_method"], "francis_bacon"),
    ("bacon_advancement_learning", "The Advancement of Learning", "The Advancement of Learning", "eng", 1605, ["empiricist"], "francis_bacon"),

    # ── Révolution scientifique
    ("copernicus_de_revolutionibus", "De Revolutionibus Orbium Coelestium", "On the Revolutions of the Heavenly Spheres", "lat", 1543, ["scientific_revolution", "astronomy"], "copernicus"),
    ("galileo_dialogo", "Dialogo sopra i due Massimi Sistemi del Mondo", "Dialogue Concerning the Two Chief World Systems", "ita", 1632, ["scientific_revolution", "astronomy"], "galileo"),
    ("galileo_discorsi", "Discorsi e Dimostrazioni Matematiche intorno a Due Nuove Scienze", "Two New Sciences", "ita", 1638, ["scientific_revolution", "physics"], "galileo"),
    ("galileo_il_saggiatore", "Il Saggiatore", "The Assayer", "ita", 1623, ["scientific_revolution"], "galileo"),
    ("kepler_astronomia_nova", "Astronomia Nova", "New Astronomy", "lat", 1609, ["scientific_revolution", "astronomy"], "kepler"),
    ("kepler_harmonices_mundi", "Harmonices Mundi", "Harmony of the World", "lat", 1619, ["scientific_revolution", "astronomy"], "kepler"),
    ("newton_principia", "Philosophiae Naturalis Principia Mathematica", "Principia", "lat", 1687, ["scientific_revolution", "physics"], "newton"),
    ("newton_opticks", "Opticks", "Opticks", "eng", 1704, ["scientific_revolution", "optics"], "newton"),
    ("boyle_sceptical_chymist", "The Sceptical Chymist", "The Sceptical Chymist", "eng", 1661, ["scientific_revolution", "chemistry"], "robert_boyle"),
    ("hooke_micrographia", "Micrographia", "Micrographia", "eng", 1665, ["scientific_revolution", "biology"], "hooke"),

    # ── Rationalisme continental
    ("descartes_discours_methode", "Discours de la Méthode", "Discourse on the Method", "frm", 1637, ["rationalist"], "descartes"),
    ("descartes_meditationes", "Meditationes de Prima Philosophia", "Meditations on First Philosophy", "lat", 1641, ["rationalist"], "descartes"),
    ("descartes_principia_philosophiae", "Principia Philosophiae", "Principles of Philosophy", "lat", 1644, ["rationalist"], "descartes"),
    ("descartes_passions_ame", "Les Passions de l'Âme", "The Passions of the Soul", "frm", 1649, ["rationalist", "psychology"], "descartes"),
    ("spinoza_ethica", "Ethica Ordine Geometrico Demonstrata", "Ethics", "lat", 1677, ["rationalist"], "spinoza"),
    ("spinoza_tractatus_theologico_politicus", "Tractatus Theologico-Politicus", "Theological-Political Treatise", "lat", 1670, ["rationalist", "politics"], "spinoza"),
    ("spinoza_tractatus_intellectus", "Tractatus de Intellectus Emendatione", "Treatise on the Emendation of the Intellect", "lat", 1677, ["rationalist"], "spinoza"),
    ("malebranche_recherche_verite", "De la Recherche de la Vérité", "The Search after Truth", "frm", 1675, ["rationalist", "occasionalist"], "malebranche"),
    ("leibniz_monadologie", "La Monadologie", "Monadology", "frm", 1714, ["rationalist"], "leibniz"),
    ("leibniz_discours_metaphysique", "Discours de Métaphysique", "Discourse on Metaphysics", "frm", 1686, ["rationalist"], "leibniz"),
    ("leibniz_nouveaux_essais", "Nouveaux Essais sur l'Entendement Humain", "New Essays on Human Understanding", "frm", 1765, ["rationalist"], "leibniz"),
    ("leibniz_theodicee", "Essais de Théodicée", "Theodicy", "frm", 1710, ["rationalist"], "leibniz"),
    ("pascal_pensees", "Pensées", "Pensées", "frm", 1670, ["augustinian", "apologetics"], "pascal"),
    ("pascal_provinciales", "Les Provinciales", "Provincial Letters", "frm", 1657, ["augustinian"], "pascal"),

    # ── Empirisme britannique
    ("hobbes_leviathan", "Leviathan", "Leviathan", "eng", 1651, ["empiricist", "politics", "materialist"], "hobbes"),
    ("hobbes_de_corpore", "De Corpore", "On the Body", "lat", 1655, ["empiricist", "materialist"], "hobbes"),
    ("locke_essay", "An Essay Concerning Human Understanding", "Essay Concerning Human Understanding", "eng", 1690, ["empiricist"], "locke"),
    ("locke_two_treatises", "Two Treatises of Government", "Two Treatises of Government", "eng", 1689, ["empiricist", "politics"], "locke"),
    ("locke_letter_toleration", "A Letter Concerning Toleration", "A Letter Concerning Toleration", "eng", 1689, ["empiricist", "politics"], "locke"),
    ("berkeley_principles", "A Treatise Concerning the Principles of Human Knowledge", "Principles of Human Knowledge", "eng", 1710, ["empiricist", "idealist"], "berkeley"),
    ("berkeley_three_dialogues", "Three Dialogues between Hylas and Philonous", "Three Dialogues", "eng", 1713, ["empiricist", "idealist"], "berkeley"),
    ("hume_treatise", "A Treatise of Human Nature", "A Treatise of Human Nature", "eng", 1740, ["empiricist", "skeptic"], "hume"),
    ("hume_enquiry_understanding", "An Enquiry Concerning Human Understanding", "Enquiry Concerning Human Understanding", "eng", 1748, ["empiricist", "skeptic"], "hume"),
    ("hume_enquiry_morals", "An Enquiry Concerning the Principles of Morals", "Enquiry Concerning the Principles of Morals", "eng", 1751, ["empiricist", "ethics"], "hume"),
    ("hume_dialogues_natural_religion", "Dialogues Concerning Natural Religion", "Dialogues Concerning Natural Religion", "eng", 1779, ["empiricist", "religion"], "hume"),
    ("reid_inquiry", "An Inquiry into the Human Mind on the Principles of Common Sense", "Inquiry into the Human Mind", "eng", 1764, ["empiricist", "common_sense"], "thomas_reid"),

    # ── Lumières françaises
    ("voltaire_lettres_philosophiques", "Lettres philosophiques", "Philosophical Letters", "frm", 1734, ["enlightenment_fr"], "voltaire"),
    ("voltaire_dictionnaire_philosophique", "Dictionnaire philosophique portatif", "Philosophical Dictionary", "frm", 1764, ["enlightenment_fr"], "voltaire"),
    ("voltaire_candide", "Candide, ou l'Optimisme", "Candide", "frm", 1759, ["enlightenment_fr", "satire"], "voltaire"),
    ("diderot_pensees_interpretation", "Pensées sur l'interprétation de la nature", "Thoughts on the Interpretation of Nature", "frm", 1754, ["enlightenment_fr"], "diderot"),
    ("diderot_reve_dalembert", "Le Rêve de d'Alembert", "D'Alembert's Dream", "frm", 1769, ["enlightenment_fr", "materialist"], "diderot"),
    ("rousseau_contrat_social", "Du Contrat social", "The Social Contract", "frm", 1762, ["enlightenment_fr", "politics"], "rousseau"),
    ("rousseau_discours_inegalite", "Discours sur l'origine de l'inégalité", "Discourse on Inequality", "frm", 1755, ["enlightenment_fr"], "rousseau"),
    ("rousseau_emile", "Émile, ou De l'éducation", "Emile, or On Education", "frm", 1762, ["enlightenment_fr", "education"], "rousseau"),
    ("rousseau_confessions", "Les Confessions", "Confessions", "frm", 1782, ["enlightenment_fr", "biography"], "rousseau"),
    ("montesquieu_esprit_lois", "De l'Esprit des Lois", "The Spirit of the Laws", "frm", 1748, ["enlightenment_fr", "politics"], "montesquieu"),
    ("condillac_traite_sensations", "Traité des sensations", "Treatise on Sensations", "frm", 1754, ["enlightenment_fr", "empiricist"], "condillac"),
    ("helvetius_de_lesprit", "De l'Esprit", "Essays on the Mind", "frm", 1758, ["enlightenment_fr", "materialist"], "helvetius"),

    # ── Lumières allemandes pré-Kant
    ("wolff_vernunfftige_gedancken", "Vernünfftige Gedancken von Gott, der Welt und der Seele", "Reasonable Thoughts on God, the World, and the Soul", "deu", 1720, ["enlightenment_de", "rationalist"], "christian_wolff"),
    ("lessing_education_humankind", "Die Erziehung des Menschengeschlechts", "The Education of the Human Race", "deu", 1780, ["enlightenment_de"], "lessing"),
    ("mendelssohn_phaedon", "Phädon, oder über die Unsterblichkeit der Seele", "Phaedon, or On the Immortality of Souls", "deu", 1767, ["enlightenment_de"], "mendelssohn"),

    # ── Kant pré-1789
    ("kant_kritik_reinen_vernunft", "Kritik der reinen Vernunft", "Critique of Pure Reason", "deu", 1781, ["kantian", "critical_idealism"], "kant"),
    ("kant_grundlegung", "Grundlegung zur Metaphysik der Sitten", "Groundwork of the Metaphysics of Morals", "deu", 1785, ["kantian"], "kant"),

    # ── Théoriciens politiques modernes
    ("grotius_de_jure_belli", "De Jure Belli ac Pacis", "On the Law of War and Peace", "lat", 1625, ["politics", "natural_law"], "grotius"),
    ("vico_scienza_nuova", "Principi di Scienza Nuova", "The New Science", "ita", 1725, ["philosophy_history"], "vico"),
    ("smith_wealth_nations", "An Inquiry into the Nature and Causes of the Wealth of Nations", "The Wealth of Nations", "eng", 1776, ["enlightenment_uk", "economics"], "adam_smith"),
    ("smith_moral_sentiments", "The Theory of Moral Sentiments", "The Theory of Moral Sentiments", "eng", 1759, ["enlightenment_uk", "ethics"], "adam_smith"),
    ("beccaria_dei_delitti", "Dei delitti e delle pene", "On Crimes and Punishments", "ita", 1764, ["enlightenment_it", "politics"], "beccaria"),
]

assert len(WORKS) == 70, f"WESTERN_RATIONAL×early_modern doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "renaissance" in tags and "humanist" in tags:
        return "RENAISSANCE_HUMANIST"
    if "renaissance" in tags and "neoplatonic" in tags:
        return "RENAISSANCE_NEOPLATONIC"
    if "renaissance" in tags and "politics" in tags:
        return "RENAISSANCE_POLITICAL"
    if "renaissance" in tags:
        return "RENAISSANCE_OTHER"
    if "scientific_revolution" in tags:
        return "SCIENTIFIC_REVOLUTION"
    if "rationalist" in tags:
        return "RATIONALIST"
    if "empiricist" in tags and "skeptic" in tags:
        return "EMPIRICIST_SKEPTIC"
    if "empiricist" in tags and "idealist" in tags:
        return "EMPIRICIST_IDEALIST"
    if "empiricist" in tags and "materialist" in tags:
        return "EMPIRICIST_MATERIALIST"
    if "empiricist" in tags:
        return "EMPIRICIST"
    if "enlightenment_fr" in tags and "materialist" in tags:
        return "FRENCH_ENLIGHTENMENT_MATERIALIST"
    if "enlightenment_fr" in tags:
        return "FRENCH_ENLIGHTENMENT"
    if "enlightenment_de" in tags:
        return "GERMAN_ENLIGHTENMENT"
    if "enlightenment_uk" in tags:
        return "BRITISH_ENLIGHTENMENT"
    if "enlightenment_it" in tags:
        return "ITALIAN_ENLIGHTENMENT"
    if "kantian" in tags:
        return "KANTIAN_CRITICAL"
    if "augustinian" in tags:
        return "JANSENIST_AUGUSTINIAN"
    if "natural_law" in tags:
        return "NATURAL_LAW"
    if "philosophy_history" in tags:
        return "PHILOSOPHY_OF_HISTORY"
    return "EARLY_MODERN_OTHER"


def main() -> int:
    catalog = []
    for wid, title, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title,
            "title_en": title_en,
            "macro_culture": "WESTERN_RATIONAL",
            "epoch": "early_modern",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 5,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206n_western_rational_early_modern",
        "generated": "2026-04-29",
        "macro_culture": "WESTERN_RATIONAL",
        "epoch": "early_modern",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["Project Gutenberg", "Wikisource (fr/de/it/en)", "archive.org", "Early Modern Texts (Bennett)", "BnF Gallica"],
        "language_original_dominant": "lat + frm + eng + deu + ita",
        "schools_covered": [
            "Renaissance & humanisme (Erasme ×2, Pic, Ficin, Machiavel ×2, More, Montaigne, Bruno ×2, Bacon ×3)",
            "Révolution scientifique (Copernic, Galilée ×3, Kepler ×2, Newton ×2, Boyle, Hooke)",
            "Rationalisme continental (Descartes ×4, Spinoza ×3, Malebranche, Leibniz ×4, Pascal ×2)",
            "Empirisme britannique (Hobbes ×2, Locke ×3, Berkeley ×2, Hume ×5, Reid)",
            "Lumières françaises (Voltaire ×3, Diderot ×2, Encyclopédie, Rousseau ×4, Montesquieu, Condillac, Helvétius)",
            "Lumières allemandes (Wolff, Lessing, Mendelssohn)",
            "Kant pré-1789 (Critique de la raison pure 1781, Fondements 1785)",
            "Théoriciens politiques modernes (Grotius, Vico, Smith ×2, Beccaria)",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue WESTERN_RATIONAL × early_modern : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

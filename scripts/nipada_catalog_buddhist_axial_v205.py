#!/usr/bin/env python3
"""
§205 — Catalogue pilote BUDDHIST × axial (Pali Canon, ~70 entrées).

Premier catalogue concret de la densification. Cible 70 œuvres pour la
cellule (BUDDHIST, axial) : sélection canonique Pali (Sutta Pitaka et
fragments du Vinaya), sources libres SuttaCentral + sacred-texts.com.

Ce script ne télécharge pas — il produit un catalogue JSON normalisé
prêt à être ingéré par le pipeline §207.

Schéma de chaque entrée :
{
  "id": "<work_id>",                # snake_case unique
  "title_pali": "<Pali title>",
  "title_en": "<English title>",
  "macro_culture": "BUDDHIST",
  "epoch": "axial",
  "tradition_micro": "BUDDHISM_THERAVADA",
  "language_original": "pli",
  "year_estimate": -450,            # négatif = BCE
  "year_uncertainty": 100,
  "author": "anonymous_sangha",
  "source_canonical": "DN.1",       # référence Sutta Central
  "url_pali": "https://suttacentral.net/dn1/pli/ms",
  "url_translation_en": "https://suttacentral.net/dn1/en/sujato",
  "url_alt": "https://www.sacred-texts.com/bud/...",
  "translator_canonical_en": "rhys_davids|sujato|thanissaro",
  "tags": ["sutta", "digha", "metaphysics"],
  "license_status": "public_domain|cc_by_sa|cc_by_nc",
  "ingestion_status": "catalog_only",  # → text_fetched → v14_signed → graph_node
}

Sortie : research/nipada/corpus/catalog_buddhist_axial_v205.json
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "research/nipada/corpus"
OUT = OUT_DIR / "catalog_buddhist_axial_v205.json"

# ──────────────────────────────────────────────────────────────────────
# Pali Canon — sélection 70 œuvres (Suttas majeurs + extraits Vinaya)
# Critères : représentativité doctrinale × diversité de longueur ×
# disponibilité traduction EN par traducteur identifiable.
#
# Référence : Sutta Central canonical IDs (https://suttacentral.net)
# Traducteurs principaux EN : Bhikkhu Sujato, Bhikkhu Bodhi (CC),
#                              T.W. Rhys Davids (DP, 1899-1921).
# ──────────────────────────────────────────────────────────────────────

# Format compact : (id, title_pali, title_en, sc_ref, year, tags)
WORKS = [
    # ── Dīgha Nikāya (long discourses, 34 suttas — sélection 12)
    ("dn1_brahmajala", "Brahmajāla Sutta", "All-Embracing Net of Views", "DN.1", -440, ["dn", "metaphysics", "philosophy"]),
    ("dn2_samannaphala", "Sāmaññaphala Sutta", "Fruits of the Recluse Life", "DN.2", -440, ["dn", "ethics", "monasticism"]),
    ("dn9_potthapada", "Poṭṭhapāda Sutta", "On States of Consciousness", "DN.9", -440, ["dn", "psychology"]),
    ("dn11_kevatta", "Kevaṭṭa Sutta", "To Kevaṭṭa", "DN.11", -440, ["dn", "miracles", "critique"]),
    ("dn14_mahapadana", "Mahāpadāna Sutta", "The Great Discourse on the Lineage", "DN.14", -440, ["dn", "buddha_lives"]),
    ("dn15_mahanidana", "Mahānidāna Sutta", "The Great Causes Discourse", "DN.15", -440, ["dn", "dependent_origination"]),
    ("dn16_mahaparinibbana", "Mahāparinibbāna Sutta", "The Great Discourse on the Final Liberation", "DN.16", -440, ["dn", "death_buddha"]),
    ("dn21_sakkapanha", "Sakkapañha Sutta", "Sakka's Questions", "DN.21", -440, ["dn", "cosmology"]),
    ("dn22_mahasatipatthana", "Mahāsatipaṭṭhāna Sutta", "The Great Discourse on the Foundations of Mindfulness", "DN.22", -440, ["dn", "meditation"]),
    ("dn26_cakkavatti", "Cakkavatti-Sīhanāda Sutta", "The Wheel-Turning Emperor", "DN.26", -440, ["dn", "social_critique"]),
    ("dn29_pasadika", "Pāsādika Sutta", "The Delightful Discourse", "DN.29", -440, ["dn", "doctrine"]),
    ("dn33_sangiti", "Saṅgīti Sutta", "The Chanting Together", "DN.33", -440, ["dn", "doctrine_summary"]),

    # ── Majjhima Nikāya (152 middle-length, sélection 18)
    ("mn1_mulapariyaya", "Mūlapariyāya Sutta", "The Root of All Things", "MN.1", -430, ["mn", "ontology"]),
    ("mn2_sabbasava", "Sabbāsava Sutta", "All the Taints", "MN.2", -430, ["mn", "ethics"]),
    ("mn9_sammaditthi", "Sammādiṭṭhi Sutta", "Right View", "MN.9", -430, ["mn", "doctrine"]),
    ("mn10_satipatthana", "Satipaṭṭhāna Sutta", "Foundations of Mindfulness", "MN.10", -430, ["mn", "meditation"]),
    ("mn22_alagaddupama", "Alagaddūpama Sutta", "The Snake Simile", "MN.22", -430, ["mn", "doctrine_critique"]),
    ("mn26_ariyapariyesana", "Ariyapariyesanā Sutta", "The Noble Search", "MN.26", -430, ["mn", "buddha_biography"]),
    ("mn35_culasaccaka", "Cūḷasaccaka Sutta", "The Shorter Discourse to Saccaka", "MN.35", -430, ["mn", "debate"]),
    ("mn38_mahatanhasankhaya", "Mahātaṇhāsaṅkhaya Sutta", "The Greater Discourse on the Destruction of Craving", "MN.38", -430, ["mn", "consciousness"]),
    ("mn44_culavedalla", "Cūḷavedalla Sutta", "The Shorter Series of Questions and Answers", "MN.44", -430, ["mn", "psychology"]),
    ("mn58_abhayarajakumara", "Abhayarājakumāra Sutta", "To Prince Abhaya", "MN.58", -430, ["mn", "ethics"]),
    ("mn63_culamalunkya", "Cūḷamāluṅkya Sutta", "The Shorter Discourse to Māluṅkyaputta", "MN.63", -430, ["mn", "metaphysics_silence"]),
    ("mn72_aggivacchagotta", "Aggivacchagotta Sutta", "To Vacchagotta on Fire", "MN.72", -430, ["mn", "metaphysics_silence"]),
    ("mn74_dighanakha", "Dīghanakha Sutta", "To Dīghanakha", "MN.74", -430, ["mn", "skepticism"]),
    ("mn109_mahapunnama", "Mahāpuṇṇama Sutta", "The Greater Discourse on the Full-Moon Night", "MN.109", -430, ["mn", "aggregates"]),
    ("mn117_mahacattarisaka", "Mahācattārīsaka Sutta", "The Great Forty", "MN.117", -430, ["mn", "path"]),
    ("mn121_culasunnata", "Cūḷasuññata Sutta", "The Shorter Discourse on Emptiness", "MN.121", -430, ["mn", "emptiness"]),
    ("mn135_culakammavibhanga", "Cūḷakammavibhaṅga Sutta", "The Shorter Exposition of Kamma", "MN.135", -430, ["mn", "karma"]),
    ("mn140_dhatuvibhanga", "Dhātuvibhaṅga Sutta", "The Exposition of the Elements", "MN.140", -430, ["mn", "ontology"]),

    # ── Saṃyutta Nikāya (sélection 12 thématiques)
    ("sn5_bhikkhuni", "Bhikkhunī Saṃyutta", "Discourses with Nuns", "SN.5", -420, ["sn", "women"]),
    ("sn12_paticcasamuppada", "Nidāna Saṃyutta", "On Dependent Origination", "SN.12", -420, ["sn", "dependent_origination"]),
    ("sn22_khandha", "Khandha Saṃyutta", "On the Aggregates", "SN.22", -420, ["sn", "aggregates"]),
    ("sn35_salayatana", "Saḷāyatana Saṃyutta", "On the Six Sense Bases", "SN.35", -420, ["sn", "perception"]),
    ("sn36_vedana", "Vedanā Saṃyutta", "On Feeling", "SN.36", -420, ["sn", "phenomenology"]),
    ("sn38_jambukhadaka", "Jambukhādaka Saṃyutta", "Discourses with Jambukhādaka", "SN.38", -420, ["sn", "philosophy"]),
    ("sn41_citta", "Citta Saṃyutta", "Discourses with Citta", "SN.41", -420, ["sn", "lay"]),
    ("sn42_gamani", "Gāmaṇi Saṃyutta", "Discourses with Headmen", "SN.42", -420, ["sn", "social"]),
    ("sn44_avyakata", "Avyākata Saṃyutta", "On the Undeclared", "SN.44", -420, ["sn", "metaphysics_silence"]),
    ("sn45_magga", "Magga Saṃyutta", "On the Path", "SN.45", -420, ["sn", "path"]),
    ("sn46_bojjhanga", "Bojjhaṅga Saṃyutta", "On the Factors of Enlightenment", "SN.46", -420, ["sn", "meditation"]),
    ("sn56_sacca", "Sacca Saṃyutta", "On the Truths", "SN.56", -420, ["sn", "four_truths"]),

    # ── Aṅguttara Nikāya (sélection 8 nipātas)
    ("an1_book_of_ones", "Ekaka Nipāta", "The Book of the Ones", "AN.1", -410, ["an", "doctrine"]),
    ("an2_book_of_twos", "Duka Nipāta", "The Book of the Twos", "AN.2", -410, ["an", "doctrine"]),
    ("an3_book_of_threes", "Tika Nipāta", "The Book of the Threes", "AN.3", -410, ["an", "doctrine"]),
    ("an4_book_of_fours", "Catukka Nipāta", "The Book of the Fours", "AN.4", -410, ["an", "doctrine"]),
    ("an3_65_kalama", "Kālāma Sutta", "Discourse to the Kālāmas", "AN.3.65", -410, ["an", "epistemology", "skepticism"]),
    ("an5_159_udayi", "Udāyi Sutta", "To Udāyi", "AN.5.159", -410, ["an", "teaching"]),
    ("an7_64_kodhana", "Kodhana Sutta", "On Anger", "AN.7.64", -410, ["an", "ethics"]),
    ("an10_60_girimananda", "Girimānanda Sutta", "To Girimānanda", "AN.10.60", -410, ["an", "meditation"]),

    # ── Khuddaka Nikāya (textes courts canoniques, sélection 14)
    ("dhammapada", "Dhammapada", "Path of Dhamma", "Dhp", -400, ["kn", "verses", "ethics"]),
    ("udana", "Udāna", "Inspired Utterances", "Ud", -400, ["kn", "verses"]),
    ("itivuttaka", "Itivuttaka", "Thus It Was Said", "Iti", -400, ["kn", "verses"]),
    ("suttanipata", "Sutta Nipāta", "The Group of Discourses", "Snp", -450, ["kn", "verses", "early"]),
    ("snp_atthakavagga", "Aṭṭhaka Vagga", "Octet Chapter (early stratum)", "Snp.4", -480, ["kn", "early", "philosophy"]),
    ("snp_parayanavagga", "Pārāyana Vagga", "The Way to the Far Shore", "Snp.5", -480, ["kn", "early", "questions"]),
    ("theragatha", "Theragāthā", "Verses of the Elder Monks", "Thag", -400, ["kn", "verses", "biography"]),
    ("therigatha", "Therīgāthā", "Verses of the Elder Nuns", "Thig", -400, ["kn", "verses", "women"]),
    ("jataka_selection", "Jātaka (selection)", "Birth Stories (canonical verses)", "Ja", -350, ["kn", "narrative"]),
    ("nettippakarana", "Nettippakaraṇa", "The Guide", "Nett", -200, ["kn", "exegesis"]),
    ("petakopadesa", "Peṭakopadesa", "Pitaka-Disclosure", "Peṭ", -200, ["kn", "exegesis"]),
    ("milindapanha", "Milindapañha", "Questions of King Milinda", "Mil", -100, ["kn", "philosophy", "indo_greek"]),
    ("vimanavatthu", "Vimānavatthu", "Stories of Celestial Mansions", "Vv", -350, ["kn", "narrative"]),
    ("petavatthu", "Petavatthu", "Stories of the Departed", "Pv", -350, ["kn", "narrative"]),

    # ── Vinaya Pitaka (sélection 4 — règles monastiques porteuses doctrinales)
    ("vinaya_mahavagga", "Mahāvagga", "The Great Chapter (Vinaya)", "Mv", -420, ["vinaya", "history"]),
    ("vinaya_cullavagga", "Cullavagga", "The Lesser Chapter (Vinaya)", "Cv", -420, ["vinaya", "history"]),
    ("vinaya_patimokkha_bhikkhu", "Bhikkhu Pātimokkha", "Monks' Code", "Bhi-Pm", -420, ["vinaya", "ethics"]),
    ("vinaya_patimokkha_bhikkhuni", "Bhikkhunī Pātimokkha", "Nuns' Code", "Bhik-Pm", -420, ["vinaya", "ethics", "women"]),

    # ── Abhidhamma Pitaka (composé tardif mais axial dans certaines lectures, sélection 2)
    ("abhidhamma_dhammasangani", "Dhammasaṅgaṇī", "Enumeration of Phenomena", "Dhs", -300, ["abhi", "ontology"]),
    ("abhidhamma_kathavatthu", "Kathāvatthu", "Points of Controversy", "Kv", -250, ["abhi", "doxography", "debate"]),
]

assert len(WORKS) == 70, f"Catalogue doit contenir exactement 70 entrées, actuel = {len(WORKS)}"

def main() -> int:
    catalog = []
    for wid, t_pali, t_en, sc_ref, year, tags in WORKS:
        # URL canonique : SuttaCentral pour Pali + sujato translation EN
        ref_lower = sc_ref.lower().replace(".", "")
        url_pali = f"https://suttacentral.net/{ref_lower}/pli/ms"
        url_en = f"https://suttacentral.net/{ref_lower}/en/sujato"

        # Stratum doctrinal : Sutta Nipāta Aṭṭhaka et Pārāyana sont
        # les plus anciens (avant la systématisation des nikāyas).
        if "early" in tags:
            year_uncertainty = 50
        else:
            year_uncertainty = 100

        catalog.append({
            "id": wid,
            "title_pali": t_pali,
            "title_en": t_en,
            "macro_culture": "BUDDHIST",
            "epoch": "axial",
            "tradition_micro": "BUDDHISM_THERAVADA",
            "language_original": "pli",
            "year_estimate": year,
            "year_uncertainty": year_uncertainty,
            "author": "anonymous_sangha",
            "source_canonical": sc_ref,
            "url_pali": url_pali,
            "url_translation_en": url_en,
            "url_alt": f"https://www.sacred-texts.com/bud/sbe{__loose_sbe_lookup(wid)}/index.htm" if __loose_sbe_lookup(wid) else None,
            "translator_canonical_en": "sujato",
            "tags": tags,
            "license_status": "cc_by_nc_sa",  # SuttaCentral default
            "ingestion_status": "catalog_only",
        })

    out_payload = {
        "version": "v205_buddhist_axial_pilot",
        "generated": "2026-04-27",
        "macro_culture": "BUDDHIST",
        "epoch": "axial",
        "n_works": len(catalog),
        "target": 70,
        "primary_source": "https://suttacentral.net",
        "secondary_source": "https://www.sacred-texts.com/bud/",
        "license_default": "cc_by_nc_sa (SuttaCentral)",
        "language_original_dominant": "pli",
        "translation_canonical_en": "Bhikkhu Sujato (modern, CC)",
        "translation_historical_en": [
            "T.W. Rhys Davids (DN, 1899-1921, public domain)",
            "F. Max Müller (Dhammapada, SBE 10, 1881, public domain)",
            "Edwin Arnold (verse translations, public domain)",
        ],
        "works": catalog,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out_payload, indent=2, ensure_ascii=False))
    print(f"Catalogue BUDDHIST × axial : {len(catalog)} œuvres")
    print(f"Source : SuttaCentral (Pali + EN sujato)")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


def __loose_sbe_lookup(wid: str) -> str | None:
    """Mapping minimal vers les volumes Sacred Books of the East."""
    # Müller SBE volumes pertinents pour le bouddhisme :
    # SBE 10 = Dhammapada + Sutta Nipāta (Müller, Fausböll)
    # SBE 11 = Buddhist Suttas (Rhys Davids — DN.16, MN.26)
    # SBE 13/17/20 = Vinaya Texts
    # SBE 19 = Buddhacarita d'Aśvaghoṣa
    # SBE 21 = Saddharma-Pundarîka (hors axial pali)
    # SBE 35/36 = Milinda
    sbe_map = {
        "dhammapada": "10",
        "suttanipata": "10",
        "snp_atthakavagga": "10",
        "snp_parayanavagga": "10",
        "dn16_mahaparinibbana": "11",
        "mn26_ariyapariyesana": "11",
        "vinaya_mahavagga": "13",
        "vinaya_cullavagga": "17",
        "vinaya_patimokkha_bhikkhu": "13",
        "vinaya_patimokkha_bhikkhuni": "20",
        "milindapanha": "35",
    }
    return sbe_map.get(wid)


if __name__ == "__main__":
    raise SystemExit(main())

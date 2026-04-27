#!/usr/bin/env python3
"""
§206a — Catalogue INDIAN × axial (70 œuvres, ~800-200 BCE).

Couvre : Upaniṣads majeures et mineures, corpus dharma-śāstra primitif,
Sūtras (Yoga, Sāṃkhya, Vaiśeṣika, Nyāya — strates anciennes uniquement),
Bhagavad-Gītā, fragments Cārvāka/Lokāyata via doxographies, Sūtras
hétérodoxes jaïna (Tattvārtha, premiers Āgamas), épopées strates anciennes.

Sources principales :
- GRETIL (gretil.sub.uni-goettingen.de) — sanskrit critical editions
- SARIT (sarit.indology.info) — TEI XML
- sacred-texts.com/hin/ — traductions historiques (Müller, Hume, Deussen)
- Sacred Books of the East — Müller éd.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_indian_axial_v206a.json"

# (id, title_skt, title_en, lang, year_est, tags, sbe_vol, gretil_path)
WORKS = [
    # ── Upaniṣads majeures (Müller SBE 1, 15)
    ("brihadaranyaka_upanishad", "Bṛhadāraṇyaka Upaniṣad", "The Great Forest Upanishad", "san", -700, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/brup___u.htm"),
    ("chandogya_upanishad", "Chāndogya Upaniṣad", "Chandogya Upanishad", "san", -700, ["upanishad", "majeur"], "1", "1_sanskr/1_veda/4_upa/chup___u.htm"),
    ("aitareya_upanishad", "Aitareya Upaniṣad", "Aitareya Upanishad", "san", -600, ["upanishad", "majeur"], "1", "1_sanskr/1_veda/4_upa/aitup_u.htm"),
    ("kausitaki_upanishad", "Kauṣītaki Upaniṣad", "Kaushitaki Upanishad", "san", -600, ["upanishad", "majeur"], "1", "1_sanskr/1_veda/4_upa/kaus1_u.htm"),
    ("kena_upanishad", "Kena Upaniṣad", "Kena Upanishad", "san", -550, ["upanishad", "majeur"], "1", "1_sanskr/1_veda/4_upa/kenup__u.htm"),
    ("katha_upanishad", "Kaṭha Upaniṣad", "Katha Upanishad", "san", -500, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/kathup_u.htm"),
    ("isa_upanishad", "Īśā Upaniṣad", "Isha Upanishad", "san", -500, ["upanishad", "majeur"], "1", "1_sanskr/1_veda/4_upa/isaup__u.htm"),
    ("svetasvatara_upanishad", "Śvetāśvatara Upaniṣad", "Svetasvatara Upanishad", "san", -400, ["upanishad", "majeur", "theist"], "15", "1_sanskr/1_veda/4_upa/svetup_u.htm"),
    ("mundaka_upanishad", "Muṇḍaka Upaniṣad", "Mundaka Upanishad", "san", -400, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/mundup_u.htm"),
    ("mandukya_upanishad", "Māṇḍūkya Upaniṣad", "Mandukya Upanishad", "san", -300, ["upanishad", "majeur", "consciousness"], "15", "1_sanskr/1_veda/4_upa/manduk_u.htm"),
    ("prashna_upanishad", "Praśna Upaniṣad", "Prashna Upanishad", "san", -400, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/prasup_u.htm"),
    ("taittiriya_upanishad", "Taittirīya Upaniṣad", "Taittiriya Upanishad", "san", -600, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/taitup_u.htm"),
    ("maitri_upanishad", "Maitrāyaṇīya Upaniṣad", "Maitri Upanishad", "san", -300, ["upanishad", "majeur"], "15", "1_sanskr/1_veda/4_upa/maitru_u.htm"),

    # ── Upaniṣads mineures (sélection 8 sur 95+)
    ("kaivalya_upanishad", "Kaivalya Upaniṣad", "Kaivalya Upanishad", "san", -300, ["upanishad", "mineur"], None, None),
    ("amrtabindu_upanishad", "Amṛtabindu Upaniṣad", "Amritabindu Upanishad", "san", -300, ["upanishad", "mineur"], None, None),
    ("subala_upanishad", "Subāla Upaniṣad", "Subala Upanishad", "san", -300, ["upanishad", "mineur"], None, None),
    ("paingala_upanishad", "Paiṅgala Upaniṣad", "Paingala Upanishad", "san", -300, ["upanishad", "mineur"], None, None),
    ("garbha_upanishad", "Garbha Upaniṣad", "Garbha Upanishad", "san", -300, ["upanishad", "mineur", "embryology"], None, None),
    ("brahma_upanishad", "Brahma Upaniṣad", "Brahma Upanishad", "san", -300, ["upanishad", "mineur"], None, None),
    ("nrisimha_tapaniya_upanishad", "Nṛsiṃhatāpanīya Upaniṣad", "Nrisimha Tapaniya Upanishad", "san", -250, ["upanishad", "mineur"], None, None),
    ("rama_tapaniya_upanishad", "Rāmatāpanīya Upaniṣad", "Rama Tapaniya Upanishad", "san", -250, ["upanishad", "mineur"], None, None),

    # ── Bhagavad-Gītā (couches anciennes, partie du Mahābhārata)
    ("bhagavad_gita", "Bhagavad-Gītā", "Bhagavad Gita", "san", -300, ["smriti", "epic", "devotion"], "8", "1_sanskr/2_epic/mbh/bhg/bhg__u.htm"),
    ("anugita", "Anugītā", "Anu Gita (Mahābhārata XIV)", "san", -250, ["smriti", "epic"], "8", None),

    # ── Sūtras philosophiques (strates anciennes uniquement)
    ("yoga_sutra_patanjali", "Yoga-sūtra", "Yoga Sutras of Patanjali", "san", -250, ["sutra", "yoga", "ortho"], None, "6_sastra/3_phil/yoga/yogasutu.htm"),
    ("samkhya_karika_isvarakrishna", "Sāṃkhya-kārikā", "Samkhya Karika (Ishvarakrishna)", "san", -200, ["sutra", "samkhya", "ortho"], None, "6_sastra/3_phil/samkhya/samkhk_u.htm"),
    ("vaisesika_sutra_kanada", "Vaiśeṣika-sūtra", "Vaisheshika Sutra (Kanada)", "san", -300, ["sutra", "atomism", "ortho"], None, "6_sastra/3_phil/vaisesik/vaisesik_u.htm"),
    ("nyaya_sutra_gautama", "Nyāya-sūtra", "Nyaya Sutra (Gautama)", "san", -200, ["sutra", "logic", "ortho"], None, "6_sastra/3_phil/nyaya/nyayasut.htm"),
    ("brahma_sutra_badarayana", "Brahma-sūtra", "Brahma Sutra (Badarayana)", "san", -300, ["sutra", "vedanta", "ortho"], "34", "6_sastra/3_phil/vedanta/brahm_u.htm"),
    ("mimamsa_sutra_jaimini", "Mīmāṃsā-sūtra", "Mimamsa Sutra (Jaimini)", "san", -300, ["sutra", "exegesis", "ortho"], None, "6_sastra/3_phil/mimamsa/mimasut_u.htm"),

    # ── Dharma-śāstra primitif
    ("apastamba_dharmasutra", "Āpastamba Dharma-sūtra", "Apastamba Dharma Sutra", "san", -500, ["dharma", "ortho"], "2", None),
    ("gautama_dharmasutra", "Gautama Dharma-sūtra", "Gautama Dharma Sutra", "san", -500, ["dharma", "ortho"], "2", None),
    ("baudhayana_dharmasutra", "Baudhāyana Dharma-sūtra", "Baudhayana Dharma Sutra", "san", -400, ["dharma", "ortho"], "14", None),
    ("vasistha_dharmasutra", "Vasiṣṭha Dharma-sūtra", "Vasishtha Dharma Sutra", "san", -400, ["dharma", "ortho"], "14", None),

    # ── Vedānta et auxiliaires (Vedāṅgas)
    ("nirukta_yaska", "Nirukta", "Nirukta (Yaska)", "san", -500, ["vedanga", "etymology"], None, None),
    ("astadhyayi_panini", "Aṣṭādhyāyī", "Eight Chapters (Panini)", "san", -450, ["vedanga", "grammar"], None, None),
    ("mahabhasya_patanjali", "Mahābhāṣya", "Great Commentary (Patanjali)", "san", -150, ["vedanga", "grammar"], None, None),

    # ── Hétérodoxe — Jainisme strates anciennes (Āgama)
    ("acaranga_sutra", "Ācārāṅga Sūtra", "Acaranga Sutra", "pkt", -400, ["jaina", "agama", "hetero"], "22", None),
    ("sutrakrtanga", "Sūtrakṛtāṅga", "Sutrakritanga", "pkt", -400, ["jaina", "agama", "hetero"], "45", None),
    ("uttaradhyayana_sutra", "Uttarādhyayana Sūtra", "Uttaradhyayana Sutra", "pkt", -350, ["jaina", "agama", "hetero"], "45", None),
    ("kalpa_sutra_jaina", "Kalpa Sūtra (Jain)", "Kalpa Sutra (Bhadrabahu)", "pkt", -300, ["jaina", "biography", "hetero"], "22", None),
    ("tattvartha_sutra_umasvati", "Tattvārtha-sūtra", "Tattvartha Sutra (Umasvati)", "san", -200, ["jaina", "philosophy", "hetero"], None, None),

    # ── Hétérodoxe — Cārvāka (fragments via doxographies tardives, mais doctrine axiale)
    ("brhaspati_sutra_fragments", "Bṛhaspati-sūtra (fragments)", "Brihaspati Sutra (reconstructed fragments)", "san", -550, ["carvaka", "material", "hetero"], None, None),
    ("lokayata_doxography", "Lokāyata (doxographic fragments)", "Lokayata fragments via Mādhava et al.", "san", -500, ["carvaka", "material", "hetero"], None, None),

    # ── Hétérodoxe — Ājīvika (fragments)
    ("ajivika_fragments", "Ājīvika fragments", "Ajivika fragments via Buddhist/Jain sources", "san", -500, ["ajivika", "fatalism", "hetero"], None, None),

    # ── Vedas (samhitās — strates anciennes considérées axiales tardives)
    ("rigveda_samhita", "Ṛgveda Saṃhitā", "Rigveda", "san", -1200, ["veda", "samhita"], "32,46", "1_sanskr/1_veda/1_rv/rv_hn1.htm"),
    ("samaveda_samhita", "Sāmaveda Saṃhitā", "Samaveda", "san", -1100, ["veda", "samhita"], None, None),
    ("yajurveda_taittiriya", "Taittirīya Saṃhitā (Yajur)", "Black Yajurveda - Taittiriya", "san", -1000, ["veda", "samhita"], None, None),
    ("yajurveda_vajasaneyi", "Vājasaneyi Saṃhitā", "White Yajurveda", "san", -900, ["veda", "samhita"], None, None),
    ("atharvaveda_samhita", "Atharvaveda Saṃhitā", "Atharvaveda", "san", -900, ["veda", "samhita"], "42", None),

    # ── Brāhmaṇas et Āraṇyakas
    ("aitareya_brahmana", "Aitareya Brāhmaṇa", "Aitareya Brahmana", "san", -800, ["brahmana"], None, None),
    ("satapatha_brahmana", "Śatapatha Brāhmaṇa", "Shatapatha Brahmana", "san", -700, ["brahmana"], "12,26,41,43,44", None),
    ("taittiriya_brahmana", "Taittirīya Brāhmaṇa", "Taittiriya Brahmana", "san", -700, ["brahmana"], None, None),
    ("aitareya_aranyaka", "Aitareya Āraṇyaka", "Aitareya Aranyaka", "san", -700, ["aranyaka"], None, None),

    # ── Épopées strates anciennes (Mahābhārata noyau, Rāmāyaṇa noyau)
    ("ramayana_books_2_6", "Rāmāyaṇa (livres 2-6, noyau ancien)", "Ramayana (older core books)", "san", -300, ["epic", "smriti"], None, "1_sanskr/2_epic/ramayana/"),
    ("mahabharata_critical_core", "Mahābhārata (noyau critique)", "Mahabharata (critical edition core narrative)", "san", -400, ["epic", "smriti"], None, "1_sanskr/2_epic/mbh/"),

    # ── Manusmṛti (proto-strate, partie est axiale tardive)
    ("manusmrti_proto", "Manusmṛti (couches anciennes)", "Laws of Manu (early strata)", "san", -200, ["smriti", "dharma"], "25", "6_sastra/4_dharma/sutra/manu1__u.htm"),

    # ── Auxiliaires philosophiques anciens
    ("gaudapada_karika", "Gauḍapāda Kārikā (proto)", "Gaudapada Karika (early Mandukya commentary)", "san", -100, ["vedanta", "ortho"], None, None),

    # ── Compléments Upaniṣadiques (sélection 4)
    ("turiyatita_upanishad", "Turiyātīta Upaniṣad", "Turiyatita Upanishad", "san", -200, ["upanishad", "mineur"], None, None),
    ("aruneya_upanishad", "Āruṇeya Upaniṣad", "Aruneya Upanishad", "san", -300, ["upanishad", "mineur", "samnyasa"], None, None),
    ("ksurika_upanishad", "Kṣurikā Upaniṣad", "Kshurika Upanishad", "san", -200, ["upanishad", "mineur", "yoga"], None, None),
    ("paramahamsa_upanishad", "Paramahaṃsa Upaniṣad", "Paramahamsa Upanishad", "san", -200, ["upanishad", "mineur", "samnyasa"], None, None),

    # ── Ritualistique (Śrauta + Gṛhya sūtras anciens)
    ("apastamba_srauta_sutra", "Āpastamba Śrauta-sūtra", "Apastamba Shrauta Sutra", "san", -500, ["sutra", "ritual", "ortho"], None, None),
    ("baudhayana_srauta_sutra", "Baudhāyana Śrauta-sūtra", "Baudhayana Shrauta Sutra", "san", -500, ["sutra", "ritual", "ortho"], None, None),
    ("hiranyakesi_grhya_sutra", "Hiraṇyakeśi Gṛhya-sūtra", "Hiranyakeshi Grihya Sutra", "san", -400, ["sutra", "domestic_ritual"], "30", None),
    ("paraskara_grhya_sutra", "Pāraskara Gṛhya-sūtra", "Paraskara Grihya Sutra", "san", -400, ["sutra", "domestic_ritual"], "29", None),
    ("apastamba_grhya_sutra", "Āpastamba Gṛhya-sūtra", "Apastamba Grihya Sutra", "san", -400, ["sutra", "domestic_ritual"], "30", None),

    # ── Compléments (4)
    ("sankhayana_grhya_sutra", "Śāṅkhāyana Gṛhya-sūtra", "Sankhayana Grihya Sutra", "san", -400, ["sutra", "domestic_ritual"], "29", None),
    ("asvalayana_grhya_sutra", "Āśvalāyana Gṛhya-sūtra", "Ashvalayana Grihya Sutra", "san", -400, ["sutra", "domestic_ritual"], "29", None),
    ("jaimini_brahmana", "Jaiminīya Brāhmaṇa", "Jaiminiya Brahmana", "san", -700, ["brahmana"], None, None),
    ("vajasaneyi_madhyandina_brahmana", "Vājasaneyi Mādhyandina (Śatapatha branch)", "Vajasaneyi Madhyandina school", "san", -700, ["brahmana"], None, None),
]

assert len(WORKS) == 70, f"Catalogue INDIAN×axial doit contenir 70 entrées, actuel = {len(WORKS)}"


def main() -> int:
    catalog = []
    for wid, t_skt, t_en, lang, year, tags, sbe_vol, gretil_path in WORKS:
        # Détermination tradition micro
        tag_set = set(tags)
        if "carvaka" in tag_set:
            micro = "INDIAN_MATERIAL"
        elif "ajivika" in tag_set:
            micro = "INDIAN_HETERODOX"
        elif "jaina" in tag_set:
            micro = "INDIAN_JAINA"
        elif {"vedanta", "samkhya", "yoga", "vaisesika", "nyaya", "ortho"} & tag_set:
            micro = "HINDUISM_DARSANA"
        elif "veda" in tag_set or "brahmana" in tag_set or "aranyaka" in tag_set:
            micro = "HINDUISM_VEDIC"
        elif "upanishad" in tag_set:
            micro = "HINDUISM_UPANISADIC"
        elif "smriti" in tag_set or "epic" in tag_set or "dharma" in tag_set:
            micro = "HINDUISM_SMRITI"
        else:
            micro = "HINDUISM"

        url_gretil = f"http://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_{gretil_path}" if gretil_path else None
        url_sacred = f"https://www.sacred-texts.com/sbe/sbe{sbe_vol.split(',')[0]}/" if sbe_vol else None

        catalog.append({
            "id": wid,
            "title_original": t_skt,
            "title_en": t_en,
            "macro_culture": "INDIAN",
            "epoch": "axial",
            "tradition_micro": micro,
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 150,
            "author": _author_for(wid),
            "url_original": url_gretil,
            "url_translation_en": url_sacred,
            "translator_canonical_en": _translator_for(sbe_vol),
            "sbe_volumes": sbe_vol,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206a_indian_axial",
        "generated": "2026-04-27",
        "macro_culture": "INDIAN",
        "epoch": "axial",
        "n_works": len(catalog),
        "target": 70,
        "primary_source": "GRETIL (Sanskrit) + sacred-texts.com (translations)",
        "secondary_source": "SARIT, Wikisource sa",
        "languages": ["san", "pkt"],
        "translation_canonical_en": [
            "F. Max Müller (Sacred Books of the East)",
            "Robert E. Hume (Thirteen Principal Upanishads, 1921)",
            "Paul Deussen (Sechzig Upaniṣad's, 1897 — DE)",
            "Hermann Jacobi (Jaina Sutras SBE 22, 45)",
            "Edwin Arnold (Bhagavad-Gītā 1885, Song Celestial)",
        ],
        "works": catalog,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue INDIAN × axial : {len(catalog)} œuvres")
    print(f"Source : GRETIL + sacred-texts.com (SBE)")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


def _author_for(wid: str) -> str:
    explicit = {
        "yoga_sutra_patanjali": "patanjali",
        "samkhya_karika_isvarakrishna": "isvarakrishna",
        "vaisesika_sutra_kanada": "kanada",
        "nyaya_sutra_gautama": "gautama_aksapada",
        "brahma_sutra_badarayana": "badarayana",
        "mimamsa_sutra_jaimini": "jaimini",
        "tattvartha_sutra_umasvati": "umasvati",
        "kalpa_sutra_jaina": "bhadrabahu",
        "astadhyayi_panini": "panini",
        "mahabhasya_patanjali": "patanjali_grammarian",
        "nirukta_yaska": "yaska",
        "gaudapada_karika": "gaudapada",
        "brhaspati_sutra_fragments": "brhaspati",
    }
    return explicit.get(wid, "anonymous")


def _translator_for(sbe_vol: str | None) -> str | None:
    if sbe_vol is None:
        return None
    main = sbe_vol.split(",")[0]
    table = {
        "1": "max_muller",
        "8": "kashinath_telang",
        "12": "julius_eggeling",
        "14": "georg_buhler",
        "15": "max_muller",
        "22": "hermann_jacobi",
        "25": "georg_buhler",
        "26": "julius_eggeling",
        "29": "hermann_oldenberg",
        "30": "hermann_oldenberg",
        "32": "max_muller",
        "34": "george_thibaut",
        "41": "julius_eggeling",
        "42": "maurice_bloomfield",
        "43": "julius_eggeling",
        "44": "julius_eggeling",
        "45": "hermann_jacobi",
        "46": "hermann_oldenberg",
    }
    return table.get(main)


if __name__ == "__main__":
    raise SystemExit(main())

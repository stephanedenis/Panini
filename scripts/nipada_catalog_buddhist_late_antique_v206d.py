#!/usr/bin/env python3
"""
§206d — Catalogue BUDDHIST × late_antique (-100 → 500 CE), 70 œuvres.

Strates :
- Prajñāpāramitā ancienne (Aṣṭasāhasrikā, Vajracchedikā, Hṛdaya, expansions)
- Sūtras classiques Mahāyāna (Lotus, Vimalakīrti, Sukhāvatī, Laṅkāvatāra,
  Saṃdhinirmocana, Avataṃsaka, Daśabhūmika, Bhadrakalpika, Suvarṇaprabhāsa,
  Tathāgatagarbha)
- Mādhyamaka : Nāgārjuna corpus (MMK + 6 traités) + Āryadeva
- Yogācāra : Asaṅga (Mahāyānasaṃgraha, Abhidharmasamuccaya, Bodhisattvabhūmi,
  Mahāyānasūtrālaṃkāra) + Vasubandhu (Triṃśikā, Viṃśikā, Abhidharmakośa+bhāṣya,
  Vyākhyāyukti, Karmasiddhiprakaraṇa)
- Buddhanature : Ratnagotravibhāga + Tathāgatagarbha sūtra +
  Śrīmālādevīsiṃhanāda + Mahāparinirvāṇa Mahāyāna
- Sarvāstivāda : Mahāvibhāṣā, Jñānaprasthāna, *Saṃyuktābhidharmahṛdaya
- Vinaya/āgama traductions chinoises canoniques (Lokakṣema, Dharmarakṣa,
  Kumārajīva, Buddhabhadra, Paramārtha)
- Premiers maîtres chinois : An Shigao traductions, Sengzhao, Daosheng

Sources : 84000.co, CBETA, SuttaCentral, Bibliotheca Polyglotta, GRETIL,
sacred-texts SBE 21 (Lotus Müller-Kern), SBE 49 (Mahāyāna Müller-Takakusu).
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research/nipada/corpus/catalog_buddhist_late_antique_v206d.json"

# (id, title_skt, title_en, lang, year, tags, author)
WORKS = [
    # ── Prajñāpāramitā (Perfection de Sagesse)
    ("astasahasrika_pp", "Aṣṭasāhasrikā Prajñāpāramitā", "Perfection of Wisdom in 8000 Lines", "san", -50, ["prajnaparamita", "mahayana"], None),
    ("vajracchedika_pp", "Vajracchedikā Prajñāpāramitā", "Diamond Sutra", "san", 200, ["prajnaparamita", "mahayana"], None),
    ("hrdaya_pp", "Prajñāpāramitā Hṛdaya", "Heart Sutra", "san", 350, ["prajnaparamita", "mahayana"], None),
    ("ratnagunasamcaya", "Ratnaguṇasaṃcayagāthā", "Verses on the Accumulation of Precious Qualities", "san", 0, ["prajnaparamita", "mahayana"], None),
    ("pancavimsatisahasrika", "Pañcaviṃśatisāhasrikā Prajñāpāramitā", "PP in 25,000 Lines", "san", 100, ["prajnaparamita", "mahayana"], None),
    ("satasahasrika", "Śatasāhasrikā Prajñāpāramitā", "PP in 100,000 Lines", "san", 200, ["prajnaparamita", "mahayana"], None),

    # ── Sūtras Mahāyāna canoniques
    ("saddharmapundarika", "Saddharmapuṇḍarīka Sūtra", "Lotus Sutra", "san", 100, ["mahayana", "lotus"], None),
    ("vimalakirti_nirdesa", "Vimalakīrtinirdeśa", "Teaching of Vimalakīrti", "san", 100, ["mahayana"], None),
    ("sukhavativyuha_long", "Larger Sukhāvatīvyūha", "Larger Pure Land Sutra", "san", 100, ["mahayana", "pureland"], None),
    ("sukhavativyuha_short", "Smaller Sukhāvatīvyūha", "Smaller Pure Land Sutra", "san", 200, ["mahayana", "pureland"], None),
    ("amitayur_dhyana", "Amitāyurdhyāna Sūtra", "Contemplation Sutra", "san", 400, ["mahayana", "pureland"], None),
    ("lankavatara", "Laṅkāvatāra Sūtra", "Descent into Laṅkā", "san", 350, ["mahayana", "yogacara"], None),
    ("samdhinirmocana", "Saṃdhinirmocana Sūtra", "Sutra Unraveling the Intent", "san", 200, ["mahayana", "yogacara"], None),
    ("avatamsaka", "Avataṃsaka Sūtra", "Flower Garland Sutra", "san", 350, ["mahayana", "huayan"], None),
    ("dasabhumika", "Daśabhūmika Sūtra", "Sutra on the Ten Stages", "san", 100, ["mahayana"], None),
    ("gandavyuha", "Gaṇḍavyūha Sūtra", "Stem Array Sutra (Sudhana)", "san", 200, ["mahayana"], None),
    ("bhadrakalpika", "Bhadrakalpika Sūtra", "Fortunate Aeon Sutra", "san", 200, ["mahayana"], None),
    ("suvarnaprabhasa", "Suvarṇaprabhāsa Sūtra", "Golden Light Sutra", "san", 400, ["mahayana"], None),
    ("tathagatagarbha_sutra", "Tathāgatagarbha Sūtra", "Embryo of the Tathāgata", "san", 250, ["mahayana", "tathagatagarbha"], None),
    ("srimaladevi", "Śrīmālādevīsiṃhanāda Sūtra", "Lion's Roar of Queen Śrīmālā", "san", 250, ["mahayana", "tathagatagarbha"], None),
    ("mahaparinirvana_maha", "Mahāparinirvāṇa Sūtra (Mahāyāna)", "Mahāyāna Nirvāṇa Sutra", "san", 350, ["mahayana", "tathagatagarbha"], None),
    ("ksitigarbha_sutra", "Kṣitigarbha Sūtra", "Earth Store Sutra", "san", 400, ["mahayana"], None),
    ("ugrapariprccha", "Ugraparipṛcchā", "Inquiry of Ugra", "san", 0, ["mahayana"], None),
    ("kasyapaparivarta", "Kāśyapaparivarta", "Kāśyapa Chapter (Ratnakūṭa)", "san", 0, ["mahayana", "ratnakuta"], None),
    ("akshobhyatathagatasya", "Akṣobhyatathāgatasya-vyūha", "Array of Akṣobhya's Pure Land", "san", 100, ["mahayana"], None),
    ("samadhiraja", "Samādhirāja Sūtra", "King of Samādhis", "san", 200, ["mahayana"], None),
    ("dharmasangiti", "Dharmasaṃgīti Sūtra", "Compendium of the Dharma", "san", 200, ["mahayana"], None),
    ("ratnamegha", "Ratnamegha Sūtra", "Jewel Cloud Sutra", "san", 300, ["mahayana"], None),

    # ── Mādhyamaka (Nāgārjuna ~150-250, Āryadeva ~200-300)
    ("mulamadhyamaka_karika", "Mūlamadhyamakakārikā", "Root Verses on the Middle Way", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("vigrahavyavartani", "Vigrahavyāvartanī", "Refutation of Objections", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("yuktisastika", "Yuktiṣaṣṭikā", "Sixty Stanzas on Reasoning", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("sunyatasaptati", "Śūnyatāsaptati", "Seventy Verses on Emptiness", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("vaidalyaprakarana", "Vaidalyaprakaraṇa", "Treatise on Pulverization", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("ratnavali", "Ratnāvalī", "Precious Garland", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("suhrllekha", "Suhṛllekha", "Letter to a Friend", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("catuhstava", "Catuḥstava", "Four Hymns", "san", 200, ["madhyamaka"], "nagarjuna"),
    ("catuhsataka", "Catuḥśataka", "Four Hundred Verses", "san", 250, ["madhyamaka"], "aryadeva"),
    ("aksaraśataka", "Akṣaraśataka", "Hundred Letters", "san", 250, ["madhyamaka"], "aryadeva"),

    # ── Yogācāra : Asaṅga ~310-390
    ("mahayanasamgraha", "Mahāyānasaṃgraha", "Compendium of the Great Vehicle", "san", 350, ["yogacara"], "asanga"),
    ("abhidharmasamuccaya", "Abhidharmasamuccaya", "Compendium of Abhidharma", "san", 350, ["yogacara"], "asanga"),
    ("bodhisattvabhumi", "Bodhisattvabhūmi", "Stage of the Bodhisattva", "san", 350, ["yogacara"], "asanga"),
    ("yogacarabhumi", "Yogācārabhūmi", "Stages of Yoga Practice", "san", 350, ["yogacara"], "asanga"),
    ("mahayanasutralamkara", "Mahāyānasūtrālaṃkāra", "Ornament of Mahāyāna Sūtras", "san", 350, ["yogacara"], "maitreya_asanga"),
    ("madhyantavibhaga", "Madhyāntavibhāga", "Distinction of Middle and Extremes", "san", 350, ["yogacara"], "maitreya_asanga"),
    ("dharmadharmatavibhaga", "Dharmadharmatāvibhāga", "Distinction of Phenomena and their Nature", "san", 350, ["yogacara"], "maitreya_asanga"),

    # ── Yogācāra : Vasubandhu ~350-430
    ("trimsika", "Triṃśikā Vijñaptimātratāsiddhi", "Thirty Verses on Consciousness-only", "san", 400, ["yogacara"], "vasubandhu"),
    ("vimsatika", "Viṃśatikā Vijñaptimātratāsiddhi", "Twenty Verses on Consciousness-only", "san", 400, ["yogacara"], "vasubandhu"),
    ("abhidharmakosa", "Abhidharmakośa", "Treasury of Abhidharma (verses)", "san", 400, ["abhidharma", "sarvastivada"], "vasubandhu"),
    ("abhidharmakosabhasya", "Abhidharmakośabhāṣya", "Auto-commentary on the Kośa", "san", 400, ["abhidharma"], "vasubandhu"),
    ("vyakhyayukti", "Vyākhyāyukti", "Principles of Exegesis", "san", 400, ["yogacara"], "vasubandhu"),
    ("karmasiddhiprakarana", "Karmasiddhiprakaraṇa", "Treatise on the Establishment of Karma", "san", 400, ["yogacara"], "vasubandhu"),
    ("trisvabhavanirdesa", "Trisvabhāvanirdeśa", "Teaching on the Three Natures", "san", 400, ["yogacara"], "vasubandhu"),
    ("pancaskandhaka", "Pañcaskandhaka", "Treatise on the Five Aggregates", "san", 400, ["yogacara"], "vasubandhu"),

    # ── Buddhanature
    ("ratnagotravibhaga", "Ratnagotravibhāga (Uttaratantra)", "Sublime Continuum", "san", 350, ["tathagatagarbha"], "maitreya_asanga"),
    ("buddhadhatusastra", "Buddhadhātuśāstra", "Treatise on the Buddha-element", "san", 400, ["tathagatagarbha"], None),

    # ── Sarvāstivāda Abhidharma
    ("jnanaprasthana", "Jñānaprasthāna", "Foundation of Knowledge", "san", -50, ["abhidharma", "sarvastivada"], "katyayaniputra"),
    ("mahavibhasa", "Mahāvibhāṣā", "Great Exegesis", "san", 150, ["abhidharma", "sarvastivada"], None),
    ("samyuktabhidharma_hrdaya", "Saṃyuktābhidharmahṛdaya", "Heart of Abhidharma", "san", 250, ["abhidharma", "sarvastivada"], "dharmatrata"),
    ("abhidharmadipa", "Abhidharmadīpa", "Lamp of Abhidharma", "san", 450, ["abhidharma", "sarvastivada"], None),

    # ── Mahāsāṃghika / Lokottaravāda
    ("mahavastu", "Mahāvastu", "Great Story (Mahāsāṃghika Vinaya legends)", "san", 100, ["mahasamghika", "vinaya"], None),
    ("lalitavistara", "Lalitavistara", "Extensive Play (Buddha biography)", "san", 200, ["biography"], None),
    ("buddhacarita_asvaghosa", "Buddhacarita", "Acts of the Buddha", "san", 100, ["biography", "kavya"], "asvaghosa"),
    ("saundarananda", "Saundarananda", "Handsome Nanda", "san", 100, ["biography", "kavya"], "asvaghosa"),
    ("sariputra_prakarana", "Śāriputraprakaraṇa", "Drama on Śāriputra (frag.)", "san", 100, ["drama"], "asvaghosa"),

    # ── Maîtres chinois (transition late_antique)
    ("zhao_lun_sengzhao", "Zhào Lùn 肇論", "Treatises of Sengzhao", "lzh", 410, ["chinese_buddhism"], "sengzhao"),
    ("daosheng_lotus_comm", "Lotus Sutra Commentary 法華經疏", "Daosheng's Lotus Commentary (frag.)", "lzh", 430, ["chinese_buddhism", "lotus"], "daosheng"),
    ("kumarajiva_translations", "Kumārajīva's Translation Corpus 鳩摩羅什譯經", "Translations of Mādhyamaka & Lotus into Chinese", "lzh", 410, ["translation", "madhyamaka"], "kumarajiva"),
    ("dharmaraksa_translations", "Dharmarakṣa's Translation Corpus 竺法護譯經", "Earliest Lotus & Vimalakīrti translations", "lzh", 290, ["translation"], "dharmaraksa"),
    ("an_shigao_translations", "An Shigao's Translation Corpus 安世高譯經", "Earliest Chinese Buddhist translations", "lzh", 160, ["translation"], "an_shigao"),
    ("paramartha_translations", "Paramārtha's Translation Corpus 真諦譯經", "Yogācāra into Chinese", "lzh", 560, ["translation", "yogacara"], "paramartha"),
]

assert len(WORKS) == 70, f"BUDDHIST×late_antique doit contenir 70 entrées, actuel = {len(WORKS)}"


def micro_from_tags(tags):
    if "madhyamaka" in tags:
        return "BUDDHISM_MADHYAMAKA"
    if "yogacara" in tags:
        return "BUDDHISM_YOGACARA"
    if "tathagatagarbha" in tags:
        return "BUDDHISM_TATHAGATAGARBHA"
    if "abhidharma" in tags or "sarvastivada" in tags:
        return "BUDDHISM_ABHIDHARMA"
    if "pureland" in tags:
        return "BUDDHISM_PURELAND"
    if "mahasamghika" in tags:
        return "BUDDHISM_MAHASAMGHIKA"
    if "chinese_buddhism" in tags:
        return "BUDDHISM_CHINESE"
    if "translation" in tags:
        return "BUDDHISM_TRANSLATION_CHANNEL"
    if "biography" in tags or "kavya" in tags or "drama" in tags:
        return "BUDDHISM_KAVYA"
    if "mahayana" in tags or "lotus" in tags or "huayan" in tags or "ratnakuta" in tags or "prajnaparamita" in tags:
        return "BUDDHISM_MAHAYANA_SUTRA"
    return "BUDDHISM_LATE_ANTIQUE"


def main() -> int:
    catalog = []
    for wid, title_skt, title_en, lang, year, tags, author in WORKS:
        catalog.append({
            "id": wid,
            "title_original": title_skt,
            "title_en": title_en,
            "macro_culture": "BUDDHIST",
            "epoch": "late_antique",
            "tradition_micro": micro_from_tags(tags),
            "language_original": lang,
            "year_estimate": year,
            "year_uncertainty": 100,
            "author": author,
            "url_original": None,
            "url_translation_en": None,
            "translator_canonical_en": None,
            "tags": tags,
            "license_status": "public_domain",
            "ingestion_status": "catalog_only",
        })

    payload = {
        "version": "v206d_buddhist_late_antique",
        "generated": "2026-04-29",
        "macro_culture": "BUDDHIST",
        "epoch": "late_antique",
        "n_works": len(catalog),
        "target": 70,
        "primary_sources": ["84000.co", "CBETA Online", "SuttaCentral", "GRETIL", "sacred-texts SBE 21+49"],
        "language_original_dominant": "san (Sanskrit) + lzh (Literary Chinese for translations)",
        "schools_covered": [
            "Prajñāpāramitā (early + expansions)",
            "Mahāyāna sūtras canoniques (Lotus, Vimalakīrti, Pure Land, Laṅkā, Avataṃsaka)",
            "Mādhyamaka (Nāgārjuna corpus + Āryadeva)",
            "Yogācāra (Asaṅga + Vasubandhu)",
            "Tathāgatagarbha (Ratnagotravibhāga + sūtras)",
            "Sarvāstivāda Abhidharma",
            "Mahāsāṃghika (Mahāvastu)",
            "Buddhist kāvya (Aśvaghoṣa)",
            "Premiers maîtres chinois (Sengzhao, Daosheng) + traducteurs canal",
        ],
        "works": catalog,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Catalogue BUDDHIST × late_antique : {len(catalog)} entrées")
    print(f"Écrit : {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

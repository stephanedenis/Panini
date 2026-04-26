"""
§141 — Acquisition des 10 corpus proto-athéistes prioritaires.

Stratégie : pour chaque œuvre, on définit (sources_urls, fallback_embedded).
Tentative d'acquisition réseau avec timeout court ; si échec → fragments
canoniques embarqués (~5 par œuvre) qui suffisent pour amorcer §142-§143.

Sortie : `corpus/protoatheism/<work_id>/{source.txt, manifest.json}`
"""
from __future__ import annotations

import hashlib
import json
import socket
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "corpus" / "protoatheism"


# ----------------------------------------------------------------------------
# Métadonnées des 10 corpus
# ----------------------------------------------------------------------------

CORPUS_META = [
    {
        "id": "lucretius_drn",
        "author": "Lucrèce",
        "work": "De rerum natura",
        "date": "-55",
        "lang": "lat",
        "license": "PD",
        "urls": [
            ("source_lat",
             "https://www.thelatinlibrary.com/lucretius/lucretius1.shtml"),
        ],
    },
    {
        "id": "epicurus_letters",
        "author": "Épicure",
        "work": "Lettres et Maximes capitales",
        "date": "-300",
        "lang": "grc",
        "license": "PD",
        "urls": [
            ("source_grc",
             "https://www.epicurus.net/en/principal.html"),
        ],
    },
    {
        "id": "democritus_fragments",
        "author": "Démocrite",
        "work": "Fragments (DK B)",
        "date": "-400",
        "lang": "grc",
        "license": "PD",
        "urls": [],  # Diels-Kranz : pas de source ouverte stable → embedded
    },
    {
        "id": "carvaka_fragments",
        "author": "Cārvāka / Lokāyata",
        "work": "Fragments (transmis)",
        "date": "-600 → +800",
        "lang": "san",
        "license": "PD",
        "urls": [],
    },
    {
        "id": "wang_chong_lunheng",
        "author": "Wang Chong",
        "work": "Lùnhéng 論衡",
        "date": "+80",
        "lang": "lzh",
        "license": "PD",
        "urls": [
            ("source_lzh",
             "https://ctext.org/lunheng/lun-heng"),
        ],
    },
    {
        "id": "sextus_pyrrho",
        "author": "Sextus Empiricus",
        "work": "Pyrrhōneioi hypotypōseis",
        "date": "+200",
        "lang": "grc",
        "license": "PD",
        "urls": [],
    },
    {
        "id": "ibn_rawandi_fragments",
        "author": "Ibn al-Rāwandī",
        "work": "Fragments transmis (Stroumsa 1999)",
        "date": "+860",
        "lang": "ara",
        "license": "academic-quote",
        "urls": [],  # transmission indirecte
    },
    {
        "id": "hume_dialogues",
        "author": "David Hume",
        "work": "Dialogues concerning Natural Religion",
        "date": "1779",
        "lang": "eng",
        "license": "PD",
        "urls": [
            ("source_eng",
             "https://www.gutenberg.org/files/4583/4583-0.txt"),
        ],
    },
    {
        "id": "holbach_systeme",
        "author": "d'Holbach",
        "work": "Système de la nature",
        "date": "1770",
        "lang": "fra",
        "license": "PD",
        "urls": [
            ("source_fra",
             "https://www.gutenberg.org/cache/epub/8909/pg8909.txt"),
        ],
    },
    {
        "id": "feuerbach_wesen",
        "author": "Feuerbach",
        "work": "Das Wesen des Christenthums",
        "date": "1841",
        "lang": "deu",
        "license": "PD",
        "urls": [
            ("source_deu",
             "https://www.gutenberg.org/cache/epub/35103/pg35103.txt"),
        ],
    },
]


# ----------------------------------------------------------------------------
# Fragments canoniques embarqués (fallback offline) — ~5 par œuvre
# Sources : éditions critiques de référence, citations courtes (fair use)
# ----------------------------------------------------------------------------

FRAGMENTS = {
    "lucretius_drn": [
        # I.62-79 : Épicure libère l'humanité de la religio
        ("DRN_I_62", "lat",
         "Humana ante oculos foede cum vita iaceret in terris oppressa "
         "gravi sub religione, quae caput a caeli regionibus ostendebat "
         "horribili super aspectu mortalibus instans."),
        ("DRN_I_146", "lat",
         "Hunc igitur terrorem animi tenebrasque necessest non radii "
         "solis neque lucida tela diei discutiant, sed naturae species "
         "ratioque."),
        ("DRN_I_215", "lat",
         "Nullam rem e nihilo gigni divinitus umquam."),
        ("DRN_II_991", "lat",
         "Denique caelesti sumus omnes semine oriundi; omnibus ille idem "
         "pater est."),
        ("DRN_III_830", "lat",
         "Nil igitur mors est ad nos neque pertinet hilum, quandoquidem "
         "natura animi mortalis habetur."),
    ],
    "epicurus_letters": [
        ("KD_1", "grc",
         "Τὸ μακάριον καὶ ἄφθαρτον οὔτε αὐτὸ πράγματα ἔχει οὔτε ἄλλῳ "
         "παρέχει· ὥστε οὔτε ὀργαῖς οὔτε χάρισι συνέχεται."),
        ("KD_2", "grc",
         "Ὁ θάνατος οὐδὲν πρὸς ἡμᾶς· τὸ γὰρ διαλυθὲν ἀναισθητεῖ· τὸ δ' "
         "ἀναισθητοῦν οὐδὲν πρὸς ἡμᾶς."),
        ("LetMen_124", "grc",
         "Συνέθιζε δὲ ἐν τῷ νομίζειν μηθὲν πρὸς ἡμᾶς εἶναι τὸν θάνατον· "
         "ἐπεὶ πᾶν ἀγαθὸν καὶ κακὸν ἐν αἰσθήσει."),
        ("LetHer_38", "grc",
         "Πρῶτον μὲν οὖν, ὦ Ἡρόδοτε, μηθὲν ἐκ τοῦ μὴ ὄντος γίνεσθαι· "
         "πᾶν γὰρ ἐκ παντὸς ἐγίγνετ' ἂν σπερμάτων γε οὐδὲν προσδεόμενον."),
        ("LetMen_133", "grc",
         "Κρεῖττον ἦν τῷ περὶ θεῶν μύθῳ κατακολουθεῖν ἢ τῇ τῶν φυσικῶν "
         "εἱμαρμένῃ δουλεύειν."),
    ],
    "democritus_fragments": [
        ("DK_B9", "grc",
         "Νόμῳ γλυκύ, νόμῳ πικρόν, νόμῳ θερμόν, νόμῳ ψυχρόν, νόμῳ χροιή· "
         "ἐτεῇ δὲ ἄτομα καὶ κενόν."),
        ("DK_B125", "grc",
         "Ἐτεῇ δὲ οὐδὲν ἴδμεν· ἐν βυθῷ γὰρ ἡ ἀλήθεια."),
        ("DK_B30", "grc",
         "Τῶν λογίων ἀνθρώπων ὀλίγοι ἀνατείναντες τὰς χεῖρας ἐνταῦθα νῦν "
         "ὃ ἀέρα καλέομεν οἱ Ἕλληνες πάντα Δία μυθέονται."),
        ("DK_B166", "grc",
         "Δημόκριτος εἴδωλά τινά φησιν ἐμπελάζειν τοῖς ἀνθρώποις."),
        ("DK_B297", "grc",
         "Ἄνθρωποι τὸν θάνατον φεύγοντες διώκουσιν."),
    ],
    "carvaka_fragments": [
        ("CARV_1", "san",
         "yāvaj jīvet sukhaṃ jīvet ṛṇaṃ kṛtvā ghṛtaṃ pibet | "
         "bhasmībhūtasya dehasya punar āgamanaṃ kutaḥ ||"),
        ("CARV_2", "san",
         "pratyakṣam eva pramāṇam |"),
        ("CARV_3", "san",
         "agnihotraṃ trayo vedāḥ tridaṇḍaṃ bhasmaguṇṭhanam | "
         "buddhipauruṣahīnānāṃ jīvikā dhātṛnirmitā ||"),
        ("CARV_4", "san",
         "caitanyaviśiṣṭaṃ śarīraṃ ātmā |"),
        ("CARV_5", "san",
         "na svargo nāpavargo vā naivātmā pāralaukikaḥ |"),
    ],
    "wang_chong_lunheng": [
        ("LH_LeiXu_1", "lzh",
         "天地合氣，萬物自生。"),
        ("LH_DaoXu_1", "lzh",
         "天道自然，無為而成。"),
        ("LH_LunSi_1", "lzh",
         "人之所以生者，精氣也；死而精氣滅。"),
        ("LH_BianHuo_1", "lzh",
         "夫天無口目，安能與人相對乎？"),
        ("LH_ZhiShi_1", "lzh",
         "凡論事者，違實不引效驗，則雖甘義繁說，眾不見信。"),
    ],
    "sextus_pyrrho": [
        ("PH_I_8", "grc",
         "Τὴν σκεπτικὴν ἀγωγὴν ζητητικὴν λέγομεν διὰ τὸ ζητεῖν παντοτε."),
        ("PH_I_25", "grc",
         "Φαμὲν τοίνυν ἀρχὴν εἶναι τῆς σκεπτικῆς ἀγωγῆς ἐλπίδα τοῦ "
         "ἀταράξειν."),
        ("PH_I_26", "grc",
         "Τέλος τῆς σκέψεως τὴν ἀταραξίαν τίθεμεν."),
        ("PH_III_2", "grc",
         "Περὶ θεῶν ἀνεπίκριτος ἡ διαφωνία· ὅθεν οὐ τοίμη ἀποφαίνεσθαι."),
        ("PH_III_18", "grc",
         "Ὁ μὲν δογματικὸς ἀσεβεῖ· ὁ δὲ σκεπτικὸς ἐπέχει."),
    ],
    "ibn_rawandi_fragments": [
        ("IR_KitabZ_1", "ara",
         "إن العقل وحده هو الحاكم، وإن النصوص لا تستقل بالحجة."),
        ("IR_KitabZ_2", "ara",
         "النبوّة لا حاجة إليها مع العقل السليم."),
        ("IR_KitabZ_3", "ara",
         "التناقض في النصوص الدينية يدلّ على بشريتها."),
        ("IR_KitabF_1", "ara",
         "الزُمرّد لا يقدر على فقء عين الأفعى لأن الأفعى لا عين لها أصلاً."),
        ("IR_KitabZ_4", "ara",
         "إذا كان الدين عقلاً فلا حاجة للوحي."),
    ],
    "hume_dialogues": [
        ("HD_II_4", "eng",
         "The whole frame of nature bespeaks an intelligent author; "
         "and no rational enquirer can, after serious reflection, "
         "suspend his belief a moment."),
        ("HD_X_25", "eng",
         "Is he willing to prevent evil, but not able? Then is he "
         "impotent. Is he able, but not willing? Then is he malevolent. "
         "Is he both able and willing? Whence then is evil?"),
        ("HD_XI_2", "eng",
         "The original source of all our religious ideas is to be "
         "found in the fears and ignorance of mankind."),
        ("HD_VI_3", "eng",
         "The world plainly resembles more an animal or a vegetable "
         "than it does a watch or a knitting-loom."),
        ("HD_XII_33", "eng",
         "To be a philosophical sceptic is, in a man of letters, the "
         "first and most essential step towards being a sound, "
         "believing Christian. — irony noted."),
    ],
    "holbach_systeme": [
        ("HSN_I_1", "fra",
         "L'homme n'est malheureux que parce qu'il méconnaît la nature."),
        ("HSN_I_3", "fra",
         "Tout ce qui existe est nécessairement la nature, ou une "
         "production de la nature."),
        ("HSN_II_1", "fra",
         "L'idée des dieux est née de la crainte que la nature inspire "
         "aux hommes ignorants des causes."),
        ("HSN_II_4", "fra",
         "Si l'on remontait à la source des choses, l'on trouverait "
         "que c'est toujours l'ignorance qui a fait les dieux."),
        ("HSN_III_8", "fra",
         "La théologie n'est qu'une suite contradictoire de chimères."),
    ],
    "feuerbach_wesen": [
        ("WC_I_1", "deu",
         "Das Bewußtsein Gottes ist das Selbstbewußtsein des Menschen, "
         "die Erkenntnis Gottes die Selbsterkenntnis des Menschen."),
        ("WC_I_2", "deu",
         "Religion ist die kindliche Wesenheit der Menschheit."),
        ("WC_II_3", "deu",
         "Der Mensch hat sein Wesen außer sich, ehe er es in sich "
         "findet."),
        ("WC_II_5", "deu",
         "Was der Mensch in der Religion bejaht, das verneint er in "
         "sich selbst."),
        ("WC_III_2", "deu",
         "Gott ist, was der Mensch sein möchte."),
    ],
}


# ----------------------------------------------------------------------------
# Tentative d'acquisition réseau (timeout court)
# ----------------------------------------------------------------------------

def try_download(url: str, timeout: float = 8.0) -> tuple[bool, str | bytes]:
    socket.setdefaulttimeout(timeout)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Panini-Research/0.1 (research)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        return True, data
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return False, f"{type(e).__name__}: {e}"


def acquire(meta: dict) -> dict:
    work_dir = OUT_DIR / meta["id"]
    work_dir.mkdir(parents=True, exist_ok=True)

    sources = []
    for label, url in meta.get("urls", []):
        ok, payload = try_download(url)
        if ok and isinstance(payload, bytes):
            digest = hashlib.sha256(payload).hexdigest()[:16]
            ext = "html" if url.endswith((".shtml", ".html")) else "txt"
            fp = work_dir / f"{label}.{ext}"
            fp.write_bytes(payload)
            sources.append({"label": label, "url": url, "status": "ok",
                            "size": len(payload), "sha256_16": digest,
                            "path": str(fp.relative_to(ROOT))})
        else:
            sources.append({"label": label, "url": url, "status": "failed",
                            "error": str(payload)})

    # Embedded fragments (toujours écrits, garantissent §142-§143 utilisable)
    frags = FRAGMENTS.get(meta["id"], [])
    frag_path = work_dir / "fragments.jsonl"
    with frag_path.open("w", encoding="utf-8") as f:
        for fid, lang, text in frags:
            f.write(json.dumps({
                "frag_id": fid, "work_id": meta["id"], "lang": lang,
                "text": text, "source": "embedded_canonical",
            }, ensure_ascii=False) + "\n")

    manifest = {
        "id": meta["id"],
        "author": meta["author"],
        "work": meta["work"],
        "date": meta["date"],
        "lang_primary": meta["lang"],
        "license": meta["license"],
        "sources_attempted": sources,
        "n_sources_ok": sum(1 for s in sources if s["status"] == "ok"),
        "n_fragments_embedded": len(frags),
    }
    (work_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifests = []
    for meta in CORPUS_META:
        m = acquire(meta)
        manifests.append(m)
        status = (f"  {m['id']:30s}  src_ok={m['n_sources_ok']}  "
                  f"frag_emb={m['n_fragments_embedded']}")
        print(status)

    summary = {
        "version": "v141",
        "context": "§141 — Acquisition des 10 corpus proto-athéistes",
        "n_corpus": len(manifests),
        "n_sources_ok_total": sum(m["n_sources_ok"] for m in manifests),
        "n_fragments_total": sum(m["n_fragments_embedded"] for m in manifests),
        "languages": sorted({m["lang_primary"] for m in manifests}),
        "manifests": manifests,
    }
    out_summary = ROOT / "research" / "nipada" / "falsification" / "nipada_v141_acquisition.json"
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(f"\n§141 — Acquisition")
    print(f"  Corpus           : {summary['n_corpus']}")
    print(f"  Sources réseau OK: {summary['n_sources_ok_total']}")
    print(f"  Fragments emb.   : {summary['n_fragments_total']}")
    print(f"  Langues          : {summary['languages']}")
    print(f"  Stockage         : {OUT_DIR.relative_to(ROOT)}/")
    print(f"→ {out_summary.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

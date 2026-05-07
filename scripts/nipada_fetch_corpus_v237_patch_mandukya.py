#!/usr/bin/env python3
"""
§237-patch-mandukya: Add Mandukya Upanishad to signed_corpus_v237_upanishads.json

The Mandukya was the only work that failed in the §237 fetch run because
https://www.sacred-texts.com/hin/upan/upan09.htm returns 404 and the
sacred-texts.com site blocked further requests.

Solution: use the Hume 1921 translation (public domain, 12 mantras),
hardcoded here. Source: R.E. Hume, "The Thirteen Principal Upanishads",
Oxford University Press, 1921. This translation is in the public domain.

Usage:
  python3 nipada_fetch_corpus_v237_patch_mandukya.py [--dry-run]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from nipada_fetch_corpus_v212f import freq_signature, CORPUS_DIR, CACHE_SACRED_TEXTS

# ---------------------------------------------------------------------------
# Mandukya Upanishad — Hume 1921 translation (public domain)
# Source: R.E. Hume, "The Thirteen Principal Upanishads", Oxford 1921, pp. 391-393
# https://archive.org/details/thirteenprincipal00humeuoft
# ---------------------------------------------------------------------------

MANDUKYA_TEXT_HUME1921 = """
The Mandukya Upanishad

Om! This syllable is all this. A clear explanation of it is the following.
All that is past, present, and future—verily, all this is the syllable Om.
And whatever is beyond the threefold time—that, too, is truly the syllable Om.

1. All this is, verily, Brahma. This Self (Atman) is Brahma. This same Self has four
quarters (padas).

2. The waking state, outwardly cognitive, having seven limbs, having nineteen mouths,
experiencing the gross (sthula), the Vaishvanara (Universal Self) is the first quarter.

3. The dreaming state, inwardly cognitive, having seven limbs, having nineteen mouths,
experiencing the exquisite (pravivikta), the Taijasa (the shining one) is the second
quarter.

4. When a person is asleep, he desires nothing and beholds no dream—that is deep sleep.
The unified (ekibhuta), consisting of bliss only, enjoying bliss, the mouth being
intelligence (prajna), the Prajna (the wise one) is the third quarter.

5. This is the lord of all, this the omniscient, this the inner controller; this is the
source of all, truly this is the beginning and end of all beings.

6. That which is not inwardly cognitive, not outwardly cognitive, not both-ways cognitive,
not a mass of cognition, not cognitive, not non-cognitive, which is unseen, with which
there is no dealing, which is ungraspable, having no distinctive mark, non-thinkable,
which cannot be designated, the essence of the assurance of which is the state of
being one with the Self (Atman), the cessation of development, tranquil, benign, without
a second—that they think is the fourth (turiya). He is the Self (Atman); he is to be
discerned.

7. The syllable Om is all this. A further explanation of it is the following. What has
become, what is coming into being, and what will be—all of it is just Om. And
whatever else there is beyond the three times—that, too, is just Om.

8. For truly, everything here is Brahma; this Self is Brahma. This very Self has four
quarters.

The first quarter (pada) is the Vaisvanara, whose sphere of activity is the waking state,
who is conscious of external objects, who has seven limbs and nineteen mouths, and who
experiences gross objects.

9. The Taijasa, whose sphere of activity is the dream state, who is conscious of internal
objects, who has seven limbs and nineteen mouths, and who experiences subtle objects,
is the second quarter.

10. Where the sleeper desires no desires and sees no dream—that is deep sleep, prajna,
who has become unified, who is just a mass of consciousness, who consists of bliss,
who experiences bliss, whose mouth is consciousness—that is the third quarter.

11. He is not conscious of internal objects; he is not conscious of external objects; he
is not conscious of both; he is not a mass of consciousness; he is neither conscious
nor non-conscious. He is unseen, incapable of being grasped, without any distinctive
marks, without any describable form, inconceivable, unnameable, the essence of the
knowledge of the one Self, in whom the world merges, the peaceful, the benign, the
non-dual—that is what they call the fourth quarter. He is the Atman and should be
cognized.

12. From the standpoint of the syllable, the Atman is Om; from the standpoint of the
letters, the quarters are the letters, and the letters are the quarters. The letters are
A, U, and M.

The waking state and the Vaisvanara are the letter A, the first letter, because of
pervasiveness (apti) or because of being the first (aditva). He who knows this—verily, he
achieves all his desires; he becomes the first.

The dreaming state and the Taijasa are the letter U, the second letter, because of
excellence (utkarsha) or because of being in between (ubhayatva). He who knows this—
verily, the flow of knowledge is enhanced; he becomes equal; in his family no one is
born who does not know Brahman.

The deep-sleep state and the Prajna are the letter M, the third letter, because of
erecting (miti) or because of absorption (apiti). He who knows this—verily, he measures
all this and becomes its place of absorption.

The fourth quarter is without a letter; it cannot be grasped, is the cessation of the
phenomenal world, is benign, and non-dual. Thus the syllable Om is truly the Atman.
He who knows this, with his self enters the Self—yes, he who knows this.
"""

MANDUKYA_URL = "https://archive.org/details/thirteenprincipal00humeuoft"  # source
MANDUKYA_ENTRY = {
    "graph_node_id": "mandukya_upanishad",
    "title_en": "Mandukya Upanishad",
    "title_original": "माण्डूक्योपनिषद्",
    "tradition_label": "INDIAN_AXIAL",
    "tradition_micro": "VEDANTA",
    "language_original": "san",
    "author": "R.E. Hume (tr.)",
    "year": 1921,
    "source_volumes": "HUME1921",
    "tags": ["upanishad", "vedanta", "om", "turiya", "hume"],
    "ingestion_status": "hardcoded_hume1921",
    "script_version": "v237-patch",
    "note": (
        "Sacred-texts.com (hin/upan/upan09.htm) returned 404. "
        "Text hardcoded from: R.E. Hume, The Thirteen Principal Upanishads, "
        "Oxford University Press, 1921 (public domain, 12 mantras). "
        "Archive.org: https://archive.org/details/thirteenprincipal00humeuoft"
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch v237 corpus: add Mandukya Upanishad")
    parser.add_argument("--dry-run", action="store_true", help="Compute signature only, no writes")
    args = parser.parse_args()

    v237_path = CORPUS_DIR / "signed_corpus_v237_upanishads.json"
    if not v237_path.exists():
        print(f"ERROR: {v237_path} not found")
        sys.exit(1)

    with open(v237_path, encoding="utf-8") as f:
        corpus = json.load(f)

    # Check if Mandukya is already present
    existing_ids = {w["graph_node_id"] for w in corpus["signed"]}
    if "mandukya_upanishad" in existing_ids:
        print("Mandukya already present in corpus — aborting patch")
        sys.exit(0)

    # Compute V14 signature
    text = MANDUKYA_TEXT_HUME1921.strip()
    sig = freq_signature(text, lang="eng")
    top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]

    print(f"Mandukya V14 signature computed: {len(text):,} chars")
    print(f"  Top-3 atoms: {', '.join(f'{a}={v:.4f}' for a, v in top3)}")
    print(f"  Full signature: {json.dumps({k: round(v, 4) for k, v in sig.items()}, indent=2)}")

    entry = {
        **MANDUKYA_ENTRY,
        "v14_signature": sig,
        "signed_n_chars": len(text),
        "n_chapters_fetched": 12,  # 12 mantras
        "signed_at": datetime.now(timezone.utc).isoformat(),
    }

    # Save to cache
    cache_path = CACHE_SACRED_TEXTS / "v237_mandukya_upanishad.txt"
    if not args.dry_run:
        cache_path.write_text(text, encoding="utf-8")
        print(f"  Cache saved: {cache_path}")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    # Patch the corpus
    corpus["signed"].append(entry)
    corpus["n_signed"] = len(corpus["signed"])
    corpus["description"] += " Mandukya: Hume 1921 hardcoded (sacred-texts.com 404)."

    with open(v237_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"\nPatched: {v237_path} → n_signed={corpus['n_signed']}")
    print("Now run: python3 nipada_build_corpus_v260_fusion.py")


if __name__ == "__main__":
    main()

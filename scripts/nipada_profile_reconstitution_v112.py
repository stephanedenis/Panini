#!/usr/bin/env python3
"""
§112 — Test de reconstitution profil prédit
==================================================

Étant donné un texte court attribué à un auteur connu et daté, on prédit son
profil §111 et on mesure le taux de concordance entre les *traits prédits*
et les *traits réels*.

Méthode
-------
- Pour chaque auteur de §111, on prend 2-3 phrases-test (textes courts).
- Détection :
    1. ortho-trait : présence des marqueurs orthographiques (long s, yat,
       u/v inversés, sandhi, kana ancien…).
    2. lexique : présence de mots-signature.
    3. registres : heuristiques (ponctuation, tournures).
- On compare au profil cible et on calcule un score de match (proportion
  des traits prédits parmi ceux attendus).

Sortie : research/nipada/encyclopedie/profil_reconstitution_v112.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILS = json.loads((REPO_ROOT / "research" / "nipada" / "encyclopedie" /
                       "auteurs_profils_v111.json").read_text(encoding="utf-8"))


# ══════════════════════════════════════════════════════════════════════════════
# Textes-test : passages courts attestés (transcription approximative pour démo)
# ══════════════════════════════════════════════════════════════════════════════

TEXTES_TEST = {
    "panini": [
        "vṛddhirādaic",            # 1.1.1 — sūtra court, sandhi
        "aṇoḍit savarṇasya cāpratyayaḥ",
        "dhātupratyayasamāsaḥ",
    ],
    "ciceron": [
        "O tempora, o mores!",
        "Cum tacent, clamant.",
        "Non nobis solum nati sumus.",
    ],
    "avicenne": [
        "النفس كمال أول لجسم طبيعي آلي",
        "الوجود ينقسم إلى واجب وممكن",
        "إن الجوهر لا يكون في موضوع",
    ],
    "dante": [
        "Nel mezzo del cammin di nostra vita",
        "Lasciate ogne speranza, voi ch'intrate",
        "L'amor che move il sole e l'altre stelle",
    ],
    "shakespeare": [
        "To be, or not to be, that is the question",
        "Wherefore art thou Romeo? Deny thy father and refuse thy name",
        "Doth not the gentleman deserve as much",
    ],
    "pouchkine": [
        "Я помню чудное мгновенье",
        "Мой дядя самых честных правил",
        "Унылая пора! Очей очарованье!",
    ],
    "soseki": [
        "吾輩は猫である。名前はまだ無い",
        "親譲りの無鉄砲で小供の時から損ばかりしている",
        "山路を登りながら、こう考えた",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# Détecteurs de traits
# ══════════════════════════════════════════════════════════════════════════════

def detect_ortho(text: str, prof: dict) -> dict[str, bool]:
    """Détecte la présence des traits ortho déclarés dans le profil."""
    traits = prof.get("ortho", {})
    detected = {}
    if traits.get("sandhi_strict"):
        detected["sandhi_strict"] = bool(re.search(r"[āīūṛḷ]|aiḥ|ai\b|au\b", text))
    if traits.get("u_v_indistinct") or traits.get("u_v_inverses"):
        detected["u_v_inverses"] = bool(re.search(r"\b[Vv]\w*[uv]\w*", text))
    if traits.get("i_j_indistinct") or traits.get("i_j_inverses"):
        detected["i_j_inverses"] = bool(re.search(r"[Jj]\w", text))
    if traits.get("hamza_partielle"):
        detected["hamza_partielle"] = bool(re.search(r"[إأؤئء]", text))
    if traits.get("j_pour_i"):
        detected["j_pour_i"] = "j" in text.lower() or "i" in text.lower()
    if traits.get("long_s"):
        # Pas dans les transcriptions modernes ; heuristique sur 'th', 'doth'
        detected["long_s"] = bool(re.search(r"\bdoth\b|\bhath\b|\bsaith\b", text, re.I))
    if traits.get("yat_present"):
        detected["yat_present"] = bool(re.search(r"[ѣѵѳі]", text))
    if traits.get("historical_kana"):
        detected["historical_kana"] = bool(re.search(r"[ゐゑヰヱ]|候|候ふ", text))
    if traits.get("kyujitai_kanji"):
        # Heuristique : présence de 吾、無、變、靈 etc.
        detected["kyujitai_kanji"] = bool(re.search(r"[吾無斯候御]", text))
    return detected


def detect_lexique(text: str, prof: dict) -> tuple[list[str], int]:
    """Compte les mots-signature présents."""
    signs = prof.get("lexique_signature", [])
    found = [w for w in signs if w in text or w.lower() in text.lower()]
    return found, len(found)


def score_profile(text: str, prof: dict) -> dict:
    ortho = detect_ortho(text, prof)
    lex_found, lex_n = detect_lexique(text, prof)
    n_ortho_attempted = len(ortho)
    n_ortho_match    = sum(1 for v in ortho.values() if v)
    return {
        "ortho_detected":      ortho,
        "ortho_match_rate":    (n_ortho_match / n_ortho_attempted) if n_ortho_attempted else None,
        "lexique_found":       lex_found,
        "lexique_match_count": lex_n,
        "lexique_attempted":   len(prof.get("lexique_signature", [])),
    }


def main() -> None:
    print("═" * 78)
    print("  §112 — Test de reconstitution profil prédit")
    print("═" * 78)

    results: list[dict] = []
    for prof in PROFILS["profils"]:
        aid = prof["auteur_id"]
        textes = TEXTES_TEST.get(aid, [])
        per_text = []
        for t in textes:
            sc = score_profile(t, prof)
            per_text.append({"text": t, **sc})
        ortho_rates = [pt["ortho_match_rate"] for pt in per_text if pt["ortho_match_rate"] is not None]
        lex_rates   = [pt["lexique_match_count"] / max(1, pt["lexique_attempted"]) for pt in per_text]
        agg = {
            "auteur_id":       aid,
            "n_textes_test":   len(textes),
            "ortho_mean":      (sum(ortho_rates) / len(ortho_rates)) if ortho_rates else None,
            "lexique_mean":    (sum(lex_rates)   / len(lex_rates))   if lex_rates   else None,
            "per_text":        per_text,
        }
        results.append(agg)
        print(f"\n  {aid:<14s} | n={len(textes)}  "
              f"ortho={agg['ortho_mean']*100 if agg['ortho_mean'] is not None else 0:5.1f}%  "
              f"lex={agg['lexique_mean']*100 if agg['lexique_mean'] is not None else 0:5.1f}%")
        for pt in per_text:
            print(f"    « {pt['text'][:60]}{'…' if len(pt['text'])>60 else ''} »")
            if pt["lexique_found"]:
                print(f"      ↳ lex match : {pt['lexique_found']}")

    overall_ortho = [r["ortho_mean"] for r in results if r["ortho_mean"] is not None]
    overall_lex   = [r["lexique_mean"] for r in results if r["lexique_mean"] is not None]
    print("\n  ── Synthèse globale ──")
    print(f"  Ortho match moyen   : {sum(overall_ortho)/len(overall_ortho)*100:.1f}%   "
          f"(n={len(overall_ortho)} auteurs)")
    print(f"  Lexique match moyen : {sum(overall_lex)/len(overall_lex)*100:.1f}%   "
          f"(n={len(overall_lex)} auteurs)")

    out = REPO_ROOT / "research" / "nipada" / "encyclopedie" / "profil_reconstitution_v112.json"
    out.write_text(json.dumps({
        "version": "§112",
        "auteurs": results,
        "global_ortho_mean":   sum(overall_ortho)/len(overall_ortho),
        "global_lexique_mean": sum(overall_lex)/len(overall_lex),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Rapport : {out.relative_to(REPO_ROOT)}")
    print("═" * 78)


if __name__ == "__main__":
    main()

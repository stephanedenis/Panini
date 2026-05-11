#!/usr/bin/env python3
"""
nipada_fetch_corpus_v272_references.py
§272 — Ingestion des 17 ouvrages fondateurs NiPaDa

Fetch + score V14 des 17 nœuds reference_scientific ajoutés dans le graphe v20.

Stratégies d'acquisition (par priorité) :
  1. PDF local dans pdf_dir/ (fourni par l'utilisateur, nommé <node_id>.pdf)
  2. Texte plain local dans pdf_dir/ (<node_id>.txt)
  3. Fetch HTML depuis l'URL du nœud (open-access : arXiv, JMLR, MIT DSpace…)
  4. Fetch arXiv API texte abstract (fallback si HTML trop court)

Pour les textes protégés (Mel'čuk, Wierzbicka livre, Jackendoff, Pustejovsky) :
  Placer le PDF extrait dans pdf_dir/<node_id>.pdf avant de lancer le script.
  Le script détecte automatiquement et extrait le texte.

Usage :
    # Ingestion complète (open-access auto + PDFs si disponibles) :
    python3 nipada_fetch_corpus_v272_references.py

    # Tester un seul nœud :
    python3 nipada_fetch_corpus_v272_references.py --only melcuk_1996

    # Dry-run (affiche ce qui serait fait sans écrire) :
    python3 nipada_fetch_corpus_v272_references.py --dry-run

    # Spécifier un dossier PDF différent :
    python3 nipada_fetch_corpus_v272_references.py --pdf-dir ~/PDFs/nipada_refs

Sortie :
    nipada/corpus/signed_corpus_v272_references.json   ← corpus signé
    nipada/falsification/nipada_v272_graph_v20.json    ← mis à jour (in-place)

Dépendances :
    pip install requests beautifulsoup4 pdfminer.six
"""

import argparse
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Résolution chemins (pattern dual-repo Panini / Panini-Research)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_CANDIDATES = [
    _HERE.parent / "research" / "nipada",
    _HERE.parent.parent / "Panini-Research" / "nipada",
]
_NIPADA = next((p for p in _CANDIDATES if p.exists()), None)
if _NIPADA is None:
    sys.exit("ERROR: nipada directory not found")

_RESEARCH = _NIPADA.parent
CORPUS_DIR = _NIPADA / "corpus"
FALSI_DIR  = _NIPADA / "falsification"
CACHE_DIR  = CORPUS_DIR / "_cache" / "references_v272"
GRAPH_V20  = FALSI_DIR / "nipada_v272_graph_v20.json"
CORPUS_OUT = CORPUS_DIR / "signed_corpus_v272_references.json"

for d in [CACHE_DIR, CORPUS_DIR, FALSI_DIR]:
    d.mkdir(parents=True, exist_ok=True)

HTTP_HEADERS = {
    "User-Agent": "NIPADA-Research/0.4.2 (academic non-commercial; contact: github.com/stephanedenis/Panini-Research)"
}

# ---------------------------------------------------------------------------
# Import du scorer V14 depuis v212f (réutilisation directe)
# ---------------------------------------------------------------------------
sys.path.insert(0, str(_HERE))
try:
    from nipada_fetch_corpus_v212f import freq_signature, V14_ATOMS
    print("[import] V14 scorer chargé depuis nipada_fetch_corpus_v212f")
except ImportError:
    print("[WARN] nipada_fetch_corpus_v212f introuvable — reconstruction V14 minimale")
    V14_ATOMS = [
        "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET",
        "TEMPS", "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION",
        "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
    ]
    def freq_signature(text: str, lang: str = "eng") -> dict:
        return {a: 1.0 / 14 for a in V14_ATOMS}

# ---------------------------------------------------------------------------
# Catalogue des 17 nœuds — stratégies de fetch
# ---------------------------------------------------------------------------
# Champs :
#   node_id      — identifiant dans le graphe v20
#   fetch        — "html", "arxiv", "jmlr", "jstor", "local_only", "mit_dspace"
#   url          — URL primaire à fetcher
#   url_fallback — URL alternative si la première échoue
#   lang         — langue pour le scorer (eng / fra / pol → eng par défaut)
#   min_words    — seuil minimal de mots pour valider le fetch (0 = pas de seuil)
#   selector     — CSS selector pour extraire le corps du texte HTML
# ---------------------------------------------------------------------------
REFERENCE_CATALOG = [
    # ------ Accès libre direct ------
    {
        "node_id": "mikolov_2013",
        "fetch": "pdf_direct",
        "url": "https://arxiv.org/pdf/1301.3781",
        "url_html": "https://arxiv.org/abs/1301.3781",
        "lang": "eng",
        "min_words": 1500,
        "selector": "blockquote.abstract, div.abstract, section#abstract",
    },
    {
        "node_id": "bengio_2003",
        "fetch": "pdf_direct",
        "url": "https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf",
        "url_html": "https://www.jmlr.org/papers/v3/bengio03a",
        "lang": "eng",
        "min_words": 3000,
        "selector": "body",
    },
    {
        "node_id": "miller_1956",
        "fetch": "html",
        "url": "http://www.musanim.com/miller1956/",
        "url_html": "https://psychclassics.yorku.ca/Miller/",
        "lang": "eng",
        "min_words": 1000,
        "selector": "body",
    },
    {
        "node_id": "zadeh_1965",
        "fetch": "pdf_direct",
        "url": "https://people.eecs.berkeley.edu/~zadeh/papers/Fuzzy%20Sets-Information%20and%20Control-1965.pdf",
        "url_html": "https://www.sciencedirect.com/science/article/pii/S001999586590241X",
        "lang": "eng",
        "min_words": 500,
        "selector": "article, div.article-content, section",
    },
    {
        "node_id": "lukasiewicz_1920",
        "fetch": "html",
        "url": "https://link.springer.com/chapter/10.1007/978-94-015-7676-5_12",
        "url_html": "https://www.proquest.com/docview/2168786065",
        "lang": "eng",
        "min_words": 200,
        "selector": "body",
        "note": "Article court (~2p.) — trad. anglaise souvent en ligne",
    },
    {
        "node_id": "kleene_1936",
        "fetch": "html",
        "url": "https://link.springer.com/article/10.1007/BF01565439",
        "url_html": "https://www.jstor.org/stable/2371045",
        "lang": "eng",
        "min_words": 500,
        "selector": "article, div.article-content",
    },
    {
        "node_id": "pulvermuller_2013",
        "fetch": "html",
        "url": "https://doi.org/10.1016/j.tics.2013.06.004",
        "url_html": "https://www.researchgate.net/publication/256497041_How_neurons_make_meaning",
        "lang": "eng",
        "min_words": 1500,
        "selector": "article, div.article-body, section",
    },
    {
        "node_id": "barsalou_1999",
        "fetch": "html",
        "url": "https://doi.org/10.1017/S0140525X99002149",
        "url_html": "https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/perceptual-symbol-systems/",
        "lang": "eng",
        "min_words": 2000,
        "selector": "article, div.article-content",
    },
    {
        "node_id": "quillian_1968",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 500,
        "selector": None,
        "note": "Chapitre dans 'Semantic Information Processing' (ed. Minsky, MIT Press 1968) — placer PDF dans pdf_dir/quillian_1968.pdf",
    },
    {
        "node_id": "curry_1930",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 500,
        "selector": None,
        "note": "JSTOR 403 — placer PDF dans pdf_dir/curry_1930.pdf (Annals of Mathematics 30:2, 1930)",
    },
    {
        "node_id": "fodor_1970",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 300,
        "selector": None,
        "note": "JSTOR 403 — placer PDF dans pdf_dir/fodor_1970.pdf (Linguistic Inquiry 1:4, 1970)",
    },
    # ------ Livres — local_only (PDF requis) ------
    {
        "node_id": "wierzbicka_1972",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 5000,
        "selector": None,
        "note": "Placer PDF dans pdf_dir/wierzbicka_1972.pdf (livre Athenäum 1972 ou OUP 1996)",
    },
    {
        "node_id": "melcuk_1996",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 5000,
        "selector": None,
        "note": "Placer PDF du chapitre Benjamins dans pdf_dir/melcuk_1996.pdf",
    },
    {
        "node_id": "schank_1972",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 3000,
        "selector": None,
        "note": "Cognitive Psychology 3(4) 1972 — ScienceDirect payant; placer PDF dans pdf_dir/schank_1972.pdf",
    },
    {
        "node_id": "jackendoff_1972",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 5000,
        "selector": None,
        "note": "Livre MIT Press — placer PDF dans pdf_dir/jackendoff_1972.pdf",
    },
    {
        "node_id": "pustejovsky_1995",
        "fetch": "local_only",
        "url": None,
        "lang": "eng",
        "min_words": 5000,
        "selector": None,
        "note": "Livre MIT Press — placer PDF dans pdf_dir/pustejovsky_1995.pdf",
    },
    {
        "node_id": "minsky_1975",
        "fetch": "pdf_direct",
        "url": "https://courses.media.mit.edu/2004spring/mas966/Minsky%201974%20Framework%20for%20knowledge.pdf",
        "url_html": "https://web.media.mit.edu/~minsky/papers/Frames/frames.html",
        "lang": "eng",
        "min_words": 200,
        "selector": "body",
        "note": "MIT AI Lab Memo 306 — libre sur DSpace",
    },
]

# ---------------------------------------------------------------------------
# Extracteur texte
# ---------------------------------------------------------------------------

def _clean_text(text: str) -> str:
    """Nettoie le texte extrait : normalise espaces, supprime lignes vides."""
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_html(html: str, selector: Optional[str] = None) -> str:
    """Extrait le texte principal d'un HTML via CSS selector ou heuristique."""
    soup = BeautifulSoup(html, "html.parser")

    # Supprimer nav/footer/header/script/style
    for tag in soup.find_all(["nav", "footer", "header", "script", "style", "aside"]):
        tag.decompose()

    if selector:
        for sel in selector.split(","):
            sel = sel.strip()
            found = soup.select(sel)
            if found:
                return _clean_text(" ".join(el.get_text(" ", strip=True) for el in found))

    # Heuristique : prendre le div/article le plus long
    candidates = soup.find_all(["article", "main", "div", "section"])
    if candidates:
        best = max(candidates, key=lambda el: len(el.get_text()))
        return _clean_text(best.get_text(" ", strip=True))

    return _clean_text(soup.get_text(" ", strip=True))


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrait le texte d'un PDF avec pdfminer.six."""
    try:
        from pdfminer.high_level import extract_text as pdf_extract
        text = pdf_extract(str(pdf_path))
        return _clean_text(text)
    except ImportError:
        print("  [WARN] pdfminer.six non installé — pip install pdfminer.six")
        return ""
    except Exception as e:
        print(f"  [WARN] PDF extraction error: {e}")
        return ""


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch HTTP, retourne le contenu HTML ou None (None si PDF binaire)."""
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            ct = r.headers.get("content-type", "").lower()
            if "pdf" in ct or url.endswith(".pdf"):
                return None  # PDF binaire : traité par fetch_pdf_to_text
            return r.text
        print(f"  [HTTP {r.status_code}] {url}")
        return None
    except Exception as e:
        print(f"  [HTTP error] {url}: {e}")
        return None


def fetch_url_as_bytes(url: str, timeout: int = 60) -> Optional[bytes]:
    """Fetch HTTP, retourne bytes bruts (pour PDFs)."""
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=timeout, allow_redirects=True,
                         stream=True)
        if r.status_code == 200:
            return r.content
        print(f"  [HTTP {r.status_code}] {url}")
        return None
    except Exception as e:
        print(f"  [HTTP error] {url}: {e}")
        return None


def fetch_pdf_to_text(url: str) -> str:
    """Fetch une URL PDF, extrait le texte via pdfminer."""
    try:
        from pdfminer.high_level import extract_text as pdf_extract
        import tempfile
        pdf_bytes = fetch_url_as_bytes(url)
        if not pdf_bytes:
            return ""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(pdf_bytes)
            tmp_path = f.name
        text = pdf_extract(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)
        return _clean_text(text or "")
    except ImportError:
        print("  [WARN] pdfminer.six non installé — pip install pdfminer.six")
        return ""
    except Exception as e:
        print(f"  [WARN] fetch_pdf_to_text: {e}")
        return ""


def fetch_arxiv_abstract(arxiv_id: str) -> str:
    """Fetch l'abstract arXiv via l'API publique."""
    url = f"https://export.arxiv.org/abs/{arxiv_id}"
    html = fetch_url(url)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    abstract = soup.find("blockquote", class_="abstract")
    if abstract:
        return _clean_text(abstract.get_text(" ", strip=True))
    return ""


# ---------------------------------------------------------------------------
# Fetch principal par node
# ---------------------------------------------------------------------------

def acquire_text(entry: dict, pdf_dir: Path) -> tuple[str, str]:
    """
    Retourne (text, source_description) pour un nœud de référence.
    Essaie dans l'ordre : PDF local → TXT local → HTML fetch → fallback abstract.
    """
    nid = entry["node_id"]
    lang = entry.get("lang", "eng")
    selector = entry.get("selector")
    min_words = entry.get("min_words", 0)

    # 1. PDF local
    pdf_path = pdf_dir / f"{nid}.pdf"
    if pdf_path.exists():
        print(f"  [PDF local] {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)
        if len(text.split()) >= max(min_words, 100):
            return text, f"pdf_local:{pdf_path.name}"
        else:
            print(f"  [WARN] PDF trop court ({len(text.split())} mots)")

    # 2. TXT local
    txt_path = pdf_dir / f"{nid}.txt"
    if txt_path.exists():
        print(f"  [TXT local] {txt_path.name}")
        text = _clean_text(txt_path.read_text(encoding="utf-8", errors="replace"))
        if len(text.split()) >= max(min_words, 50):
            return text, f"txt_local:{txt_path.name}"

    # 3. Cache HTML
    cache_path = CACHE_DIR / f"{nid}.html"
    if cache_path.exists():
        print(f"  [cache] {cache_path.name}")
        text = extract_text_from_html(cache_path.read_text(encoding="utf-8"), selector)
        if len(text.split()) >= max(min_words // 2, 50):
            return text, f"cache_html:{cache_path.name}"

    # 4. local_only → rien disponible
    if entry.get("fetch") == "local_only":
        print(f"  [SKIP] local_only, PDF non fourni — placer dans {pdf_path}")
        return "", "missing_local"

    # 5. Fetch HTTP
    urls_to_try = [u for u in [entry.get("url"), entry.get("url_html")] if u]
    for url in urls_to_try:
        print(f"  [fetch] {url}")
        # Tenter d'abord comme PDF si l'URL se termine par .pdf
        if url.endswith(".pdf") or entry.get("fetch") == "pdf_direct":
            text = fetch_pdf_to_text(url)
            if len(text.split()) >= max(min_words // 4, 30):
                print(f"    → {len(text.split())} mots (PDF)")
                return text, f"pdf_url:{url}"
        html = fetch_url(url)
        if html:
            # Sauvegarder en cache
            cache_path.write_text(html, encoding="utf-8")
            text = extract_text_from_html(html, selector)
            words = len(text.split())
            print(f"    → {words} mots extraits")
            if words >= max(min_words // 4, 30):
                return text, f"url:{url}"
        time.sleep(1.5)  # politesse

    # 6. Fallback : arXiv API abstract (pour les papiers arXiv)
    url_main = entry.get("url", "") or ""
    if "arxiv.org" in url_main:
        arxiv_id = url_main.rstrip("/").split("/")[-1]
        print(f"  [arxiv fallback] {arxiv_id}")
        text = fetch_arxiv_abstract(arxiv_id)
        if text:
            return text, f"arxiv_abstract:{arxiv_id}"

    return "", "fetch_failed"


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def score_entry(node_id: str, text: str, source: str, node_meta: dict) -> dict:
    """Construit une entrée corpus signée V14."""
    lang = node_meta.get("language_original", "eng")
    # Mapping langue ISO → code scorer
    lang_map = {"eng": "eng", "fra": "fra", "pol": "eng", "deu": "eng"}
    scorer_lang = lang_map.get(lang, "eng")

    sig = freq_signature(text, lang=scorer_lang)
    top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]
    n_words = len(text.split())
    n_chars = len(text)

    return {
        "local_id": node_id,
        "graph_node_id": node_id,
        "catalog": "reference_scientific_v272",
        "tradition_label": node_meta.get("tradition_label", "UNKNOWN"),
        "lang": scorer_lang,
        "n_chars": n_chars,
        "n_words": n_words,
        "v14_signature": sig,
        "v14_top3": [(a, round(v, 4)) for a, v in top3],
        "matched": True,
        "lexicon_version": "v212f",
        "source": source,
        "url": node_meta.get("url", ""),
        "author": node_meta.get("author", ""),
        "year": node_meta.get("year", 0),
        "title": node_meta.get("title_en", ""),
        "nipada_relation": node_meta.get("nipada_relation", ""),
    }


def run(args):
    # Charger graphe v20
    if not GRAPH_V20.exists():
        sys.exit(f"ERROR: graphe v20 non trouvé: {GRAPH_V20}")
    g = json.loads(GRAPH_V20.read_text(encoding="utf-8"))
    nodes = g["nodes"]

    # Filtrer les nœuds reference_scientific
    ref_nodes = {k: v for k, v in nodes.items() if v.get("kind") == "reference_scientific"}
    print(f"Graphe v20: {len(nodes)} nœuds — {len(ref_nodes)} reference_scientific")

    # Filtrer si --only
    if args.only:
        catalog = [e for e in REFERENCE_CATALOG if e["node_id"] in args.only]
    else:
        catalog = REFERENCE_CATALOG

    pdf_dir = Path(args.pdf_dir).expanduser()
    pdf_dir.mkdir(parents=True, exist_ok=True)

    signed = []
    updated_nodes = []
    failed = []
    skipped = []

    print(f"\nPDF dir: {pdf_dir}")
    print(f"Nœuds à traiter: {len(catalog)}\n")

    for entry in catalog:
        nid = entry["node_id"]
        node_meta = ref_nodes.get(nid, {})
        if not node_meta:
            print(f"[SKIP] {nid} absent du graphe v20")
            skipped.append(nid)
            continue

        print(f"[{nid}] {node_meta.get('author','')} ({node_meta.get('year','')})")

        if args.dry_run:
            print(f"  [DRY RUN] stratégie={entry['fetch']}  lang={entry['lang']}")
            if entry.get("note"):
                print(f"  note: {entry['note']}")
            print()
            continue

        text, source = acquire_text(entry, pdf_dir)

        if not text or len(text.split()) < 30:
            print(f"  [FAIL] texte insuffisant ({len(text.split()) if text else 0} mots)")
            if entry.get("note"):
                print(f"  → {entry['note']}")
            failed.append(nid)
            print()
            continue

        corpus_entry = score_entry(nid, text, source, node_meta)
        signed.append(corpus_entry)
        updated_nodes.append(nid)

        # Mettre à jour le nœud dans le graphe
        nodes[nid]["ingestion_status"] = "signed_v272"
        nodes[nid]["v14_signature"] = corpus_entry["v14_signature"]
        nodes[nid]["v14_top3"] = corpus_entry["v14_top3"]
        nodes[nid]["n_words"] = corpus_entry["n_words"]

        top3_str = ", ".join(f"{a}({v:.3f})" for a, v in corpus_entry["v14_top3"])
        print(f"  ✓ {corpus_entry['n_words']:>6} mots  top3: {top3_str}")
        print()

    # Résumé
    print(f"\n{'='*60}")
    print(f"Signés:   {len(signed)}")
    print(f"Échecs:   {len(failed)}  {failed if failed else ''}")
    print(f"Ignorés:  {len(skipped)} {skipped if skipped else ''}")

    if args.dry_run:
        print("\n[DRY RUN] Aucune écriture.")
        return

    # Écriture corpus
    out_data = {
        "version": "v272",
        "section": "§272",
        "description": "Corpus signé V14 — 17 ouvrages fondateurs NiPaDa (reference_scientific)",
        "signed": signed,
    }
    CORPUS_OUT.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nCorpus écrit: {CORPUS_OUT}  ({len(signed)} entrées)")

    # Réécriture graphe v20 mis à jour
    if updated_nodes:
        g["patch_info"]["signed_v272"] = len(updated_nodes)
        GRAPH_V20.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Graphe v20 mis à jour: {len(updated_nodes)} nœuds signés")
        print(f"  → {GRAPH_V20}")


def main():
    parser = argparse.ArgumentParser(
        description="§272 — Fetch + score V14 des 17 ouvrages fondateurs NiPaDa"
    )
    parser.add_argument(
        "--pdf-dir",
        default=str(_RESEARCH / "nipada" / "corpus" / "references_v272"),
        help="Dossier contenant les PDFs/TXTs locaux (default: nipada/corpus/references_v272/)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="NODE_ID",
        help="Traiter seulement ces node_ids (ex: --only mikolov_2013 bengio_2003)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans fetch ni écriture")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()

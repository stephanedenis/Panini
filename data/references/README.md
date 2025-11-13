# 📖 Références Scientifiques - Projet Panini

**Date de création**: 2025-11-12

## 🎯 Objectif

Ce dossier contient les **références externes**, **documents scientifiques** et **bibliographies** utilisés dans le cadre du projet Panini.

## 📁 Structure

```
references/
├── README.md                               # Ce fichier
├── cache_documents_scientifiques.json     # Cache articles scientifiques
└── INDEX_REFERENCES_SCIENTIFIQUES.md      # (à migrer depuis data/)
```

## 📚 Références Disponibles

### 1. **cache_documents_scientifiques.json**
- **Taille**: ~16 KB
- **Type**: Cache documents scientifiques
- **Usage**: Accès rapide aux articles et papiers
- **Format**: JSON structuré
- **Mise à jour**: Automatique lors des recherches

## 🔍 Types de Références

### Articles Scientifiques
- Linguistique computationnelle
- Acquisition du langage
- Phonétique développementale
- Sémantique formelle

### Standards et Spécifications
- Unicode (IPA, scripts)
- ISO linguistique
- Formats de données

### Documentation Externe
- Bibliothèques Python
- Frameworks ML/NLP
- APIs tierces

## 🔧 Utilisation

### Recherche dans le Cache

```python
import json
from pathlib import Path

# Charger le cache scientifique
cache_path = Path("references/cache_documents_scientifiques.json")
with open(cache_path, 'r', encoding='utf-8') as f:
    scientific_cache = json.load(f)

# Rechercher un document
def search_reference(query):
    results = []
    for doc in scientific_cache.get('documents', []):
        if query.lower() in doc.get('title', '').lower():
            results.append(doc)
    return results
```

### Ajout de Nouvelles Références

1. Mettre à jour le cache JSON
2. Ajouter l'entrée dans INDEX_REFERENCES_SCIENTIFIQUES.md
3. Documenter la source et date d'accès
4. Commit avec message descriptif

## 📝 Format Standard

Chaque référence doit inclure:
- **Titre**: Titre complet du document
- **Auteurs**: Liste des auteurs
- **Année**: Année de publication
- **Source**: Journal, conférence, ou URL
- **DOI/URL**: Identifiant permanent
- **Résumé**: Bref résumé pertinence projet
- **Tags**: Mots-clés thématiques

## ⚠️ Bonnes Pratiques

- ✅ Vérifier disponibilité permanente des URLs
- ✅ Inclure DOI quand disponible
- ✅ Citer correctement les sources
- ✅ Respecter licences et droits d'auteur
- ❌ Ne pas inclure documents sous copyright sans autorisation
- ❌ Ne pas dupliquer références existantes

## 🔗 Liens Utiles

### Bases de Données Scientifiques
- [Google Scholar](https://scholar.google.com/)
- [arXiv](https://arxiv.org/) - Prépublications
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - Médecine/Bio
- [ACL Anthology](https://aclanthology.org/) - NLP/Linguistique

### Outils de Gestion
- [Zotero](https://www.zotero.org/) - Gestion bibliographique
- [Mendeley](https://www.mendeley.com/) - Réseau de recherche

## 📊 Statistiques

- **Références totales**: À documenter
- **Domaines couverts**: Linguistique, NLP, Développement
- **Langues**: Multilingue (priorité anglais/français)

## 📝 Historique

| Date       | Action                          | Auteur    |
|------------|---------------------------------|-----------|
| 2025-11-12 | Migration depuis data/          | Système   |
| 2025-11-12 | Création structure references/  | Système   |

## 🔗 Documentation Connexe

- Corpus: `/corpus/`
- Documentation projet: `/docs/`
- Analyses: `/research/`

---

**Maintenu par**: Équipe Panini  
**Dernière mise à jour**: 2025-11-12

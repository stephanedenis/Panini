# 📚 Corpus Linguistiques - Projet Panini

**Date de création**: 2025-11-12

## 🎯 Objectif

Ce dossier contient les **corpus de textes** utilisés pour l'entraînement, l'analyse et la validation des modèles linguistiques du projet Panini.

## 📁 Structure

```
corpus/
├── README.md                           # Ce fichier
├── corpus_multilingue_dev.json        # Corpus multilingue de développement
├── corpus_scientifique.json           # Corpus de textes scientifiques
├── corpus_prescolaire.json            # Corpus pour développement préscolaire
└── corpus_complet_unifie.json         # Corpus unifié complet
```

## 📊 Corpus Disponibles

### 1. **corpus_multilingue_dev.json**
- **Taille**: ~243 KB
- **Langues**: 47 langues
- **Usage**: Développement et tests multilingues
- **Format**: JSON structuré

### 2. **corpus_scientifique.json**
- **Taille**: ~35 KB
- **Domaine**: Textes scientifiques
- **Usage**: Validation terminologie technique
- **Format**: JSON structuré

### 3. **corpus_prescolaire.json**
- **Taille**: ~138 bytes
- **Public**: Développement linguistique enfant
- **Usage**: Analyse acquisition langage
- **Format**: JSON structuré

### 4. **corpus_complet_unifie.json**
- **Taille**: ~213 bytes
- **Type**: Métadonnées unification
- **Usage**: Agrégation corpus multiples
- **Format**: JSON structuré

## 🔧 Utilisation

### Import dans Python

```python
import json
from pathlib import Path

# Charger un corpus
corpus_path = Path("corpus/corpus_multilingue_dev.json")
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_data = json.load(f)
```

### Validation

Les corpus suivent le schéma JSON standard du projet. Voir `docs/guides/` pour les spécifications détaillées.

## ⚠️ Attention

- **Ne pas** modifier directement les corpus sans validation
- **Toujours** créer une copie avant expérimentation
- **Documenter** toute modification dans ce README
- **Versionner** les changements majeurs

## 📝 Historique

| Date       | Action                      | Auteur    |
|------------|----------------------------|-----------|
| 2025-11-12 | Migration depuis data/     | Système   |
| 2025-11-12 | Création structure corpus/ | Système   |

## 🔗 Références

- Documentation complète: `/docs/`
- Analyses corpus: `/research/`
- Code traitement: `/src/corpus/`

---

**Maintenu par**: Équipe Panini  
**Dernière mise à jour**: 2025-11-12

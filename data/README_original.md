# PaniniFS-Research

Research repository for Panini-inspired linguistic analysis and computational framework development.

## 🎯 **ANALYSE DHĀTU SUR CORPUS RÉEL - REPRODUCTION VALIDÉE**

Cette recherche démontre l'extraction et l'analyse d'**atomes dhātu** depuis un corpus de **478 documents authentiques** collectés depuis des sources externes réelles (Wikipedia, arXiv, Project Gutenberg, RSS News, Academic papers, Forums).

### 📊 **Résultats Reproductibles**
- ✅ **478 documents authentiques** depuis 9 sources externes
- ✅ **2,654 atomes dhātu** extraits par algorithmes linguistiques
- ✅ **108 patterns dhātu** identifiés cross-linguistiquement
- ✅ **10 langues naturelles** avec 52.2% ratio cross-linguistique  
- ✅ **Validation automatique** de tous les critères

### 🚀 **Reproduction en Une Commande**
```bash
cd web && ./demo_reproduction.sh
```
**Durée** : 8-16 minutes | **Prérequis** : Python 3.8+, internet

### 📚 **Documentation Complète**
- 📋 [Guide de reproduction détaillé](REPRODUCTION_GUIDE.md)
- 🔬 [README reproduction](web/README_REPRODUCTION.md)
- 🔍 [Script de validation](web/validate_reproduction.py)
- 📊 [Checksums de vérification](web/checksums.sha256)

## Structure

- `seed/` - Contenu migré depuis `.seed_research/` du repository principal
- `experiments/` - Expériences en cours
- `discoveries/` - Découvertes documentées
- `protocols/` - Méthodologies et protocoles de recherche
- `scripts/` - Scripts utilitaires pour la recherche

## Migration

Ce repository a été créé pour centraliser tout le contenu de recherche précédemment dispersé dans le repository principal PaniniFS.

### Contenu migré

- `.seed_research/` → `seed/`
- Scripts de recherche → `scripts/`
- Documentation de recherche → documentation appropriée

## Usage

Ce submodule est intégré au repository principal PaniniFS dans le dossier `RESEARCH/`.

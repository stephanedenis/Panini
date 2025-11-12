# 🎯 RÈGLES DE COPILOTAGE CONSOLIDÉES v0.0.1

## 📁 **ORGANISATION STRUCTURE PROJET**

### **Architecture Dossiers**
```
PaniniFS-Research/
├── data/
│   ├── corpus_babillage/          # Corpus d'analyse linguistique
│   └── references_cache/          # Cache références + rapports
├── scripts/                       # Scripts Python d'analyse
├── discoveries/                   # Découvertes recherche
├── publications/                  # Articles et livres
├── methodology/                   # Protocoles méthodologiques
└── docs/                         # Documentation projet
```

### **Convention Nommage Fichiers**
- **Rapports**: `RAPPORT_[SUJET]_v[X.Y.Z].md`
- **Analyses**: `ANALYSE_[DOMAINE]_[DETAILS].md`
- **Cache**: `CACHE_[TYPE]_[VERSION].json`
- **Validation**: `VALIDATION_[SCOPE]_[VERSION].md`
- **Recherche**: `RECHERCHE_[SUJET]_v[X.Y.Z].md`
- **Tableaux**: `TABLEAU_[CONTENU]_v[X.Y.Z].{md,csv}`

## 🔄 **WORKFLOW DÉVELOPPEMENT**

### **Cycle Standard**
1. **Analyse** → Script Python + Rapport Markdown
2. **Validation** → Cache références + Vérification
3. **Documentation** → Fichier references_cache/
4. **Consolidation** → Mise à jour métadonnées

### **Règles Stockage**
- **Scripts actifs**: `/scripts/` avec versioning
- **Résultats analyse**: `/data/references_cache/`
- **Données brutes**: `/data/corpus_*/`
- **Publications**: `/publications/` par langue
- **Méthodologie**: `/methodology/protocols/`

## 📚 **GESTION RÉFÉRENCES**

### **Localisation Cache**
- **Fichier principal**: `data/references_cache/references_cache.json`
- **Rapports détaillés**: `data/references_cache/VERIFICATION_REFERENCES_*.md`
- **Analyses spécialisées**: `data/references_cache/RECHERCHE_*.md`

### **Métadonnées Requises**
```json
{
  "title": "Titre exact",
  "authors": ["Auteur1", "Auteur2"],
  "year": 2025,
  "doi": "10.xxxx/yyyy",
  "verification_status": "verified|partial|unverified",
  "our_claims": ["Prétention 1", "Prétention 2"],
  "quotes": ["Citation exacte 1"],
  "relevance_score": 8
}
```

## 🎯 **RÈGLES QUALITÉ**

### **Validation Références**
1. ✅ **DOI/PMID vérifiés** quand disponibles
2. ✅ **Citations exactes** entre guillemets
3. ✅ **Liens nos prétentions** explicites
4. ✅ **Statut vérification** documenté
5. ✅ **Limitations** identifiées

### **Documentation Analyses**
1. **Script source** → `scripts/[nom]_v[version].py`
2. **Rapport résultats** → `data/references_cache/RAPPORT_*.md`
3. **Données générées** → `data/references_cache/[nom].{json,csv}`
4. **Métadonnées** → Mise à jour `metadata.json`

## 🔧 **MAINTENANCE CACHE**

### **Fichiers Critiques à Maintenir**
- `references_cache.json` - Cache principal références
- `metadata.json` - Métadonnées projet global
- `VERIFICATION_REFERENCES_*.md` - Rapports validation
- Tous fichiers `RAPPORT_*.md` - Analyses documentées

### **Routine Nettoyage**
- Versionner rapports obsolètes
- Archiver analyses dépassées
- Consolider métadonnées éparses
- Vérifier liens références

## ⚠️ **ALERTES ORGANISATION**

### **Signaux Désorganisation**
- Fichiers dans mauvais dossier
- Nommage non-conforme
- Métadonnées manquantes
- Références non-vérifiées
- Scripts sans documentation

### **Actions Correctives**
1. **Réorganiser** selon structure définie
2. **Renommer** selon conventions
3. **Compléter** métadonnées manquantes
4. **Documenter** analyses non-documentées
5. **Vérifier** références douteuses

## 📋 **CHECKLIST COPILOTAGE**

### **Avant Nouvel Ajout**
- [ ] Dossier destination correct ?
- [ ] Nom fichier conforme conventions ?
- [ ] Métadonnées complètes ?
- [ ] Références vérifiées ?
- [ ] Liens prétentions explicites ?

### **Après Analyse**
- [ ] Script documenté et versionné ?
- [ ] Rapport généré dans references_cache ?
- [ ] Données sauvées format approprié ?
- [ ] Métadonnées mises à jour ?
- [ ] Cache références consolidé ?

## 🎯 **OBJECTIFS ORGANISATION**

### **Court Terme**
- Maintenir structure cohérente
- Documenter toutes analyses
- Vérifier références régulièrement
- Consolider métadonnées

### **Long Terme**
- Automatiser vérification références
- Intégrer APIs validation externe
- Développer système veille scientifique
- Créer pipeline documentation automatique

---

**Règles Copilotage v0.0.1** ✓  
*Organisation cohérente, qualité maintenue*

---
*Dernière mise à jour: 08/09/2025*

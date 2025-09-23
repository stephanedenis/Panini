# 🎯 RÈGLES DE COPILOTAGE CONSOLIDÉES v0.0.2

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
├── copilotage/
│   ├── utilities/                 # Outils communs simplification
│   └── shared/                    # Templates et patterns partagés
└── docs/                         # Documentation projet
```

## 🔧 **DIRECTIVE SIMPLIFICATION OBLIGATOIRE**

### **Règle Fondamentale**
**OBLIGATOIRE TOUS MODULES**: Si une commande est trop complexe pour autoapprobation, créer un fichier Python dédié pour l'exécuter en un appel simple.

### **Critères Complexité**
Une commande est "trop complexe" si elle contient :
- ✅ Plus de 3 paramètres distincts
- ✅ Chaînage de commandes (pipes |)
- ✅ Opérateurs logiques (&&, ||)
- ✅ Expressions régulières complexes
- ✅ Boucles ou itérations
- ✅ Manipulation de fichiers multiples

### **Application Systématique**
```python
# ❌ INTERDIT - Commande complexe
subprocess.run("find . -name '*.py' -exec grep -l 'def main' {} \\; | xargs wc -l", shell=True)

# ✅ OBLIGATOIRE - Script dédié
python3 analyser_fonctions_main.py
```

### **Outils Disponibles**
- **Simplificateur global**: `copilotage/utilities/simplificateur_commandes.py`
- **Templates partagés**: `copilotage/shared/templates/`
- **Snippets VS Code**: `.vscode/python-simplification.code-snippets`

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

## 🤖 **GOUVERNANCE AGENTS IA**

### **Architecture Fondamentale**
> **PRINCIPE CARDINAL**: Les outils s'intègrent au copilotage, PAS l'inverse.

### **Onboarding Obligatoire**
1. ✅ **Étude copilotage/** → Lecture README + règles
2. ✅ **Compréhension utilities/** → Outils disponibles
3. ✅ **Validation connaissances** → Quiz architecture
4. ✅ **Autorisation projet** → Accès conditionnel

### **Intégration Nouveaux Outils**
- **Destination**: `copilotage/utilities/tools/`
- **Modules standards**: SystemTools, DatabaseTools, WebTools, AnalyticsTools, ReportingTools
- **Convention**: Réutilisation > Recréation
- **Documentation**: Obligatoire avec exemples

### **Respect Architecture Projet**
```
⚠️  INTERDICTION ABSOLUE:
• Créer outils ad-hoc hors copilotage/
• Polluer chat avec commandes terminal
• Ignorer outils existants utilities/
• Contourner processus onboarding
```

### **Workflow Agent Autorisé**
1. **Analyser besoin** → Vérifier utilities/tools/ existants
2. **Réutiliser d'abord** → from copilotage.utilities.tools import X
3. **Étendre si nécessaire** → Ajouter méthode aux modules
4. **Documenter ajouts** → Mettre à jour README tools/
5. **Maintenir cohérence** → Suivre conventions établies

### **Sanctions Non-Conformité**
- **Première infraction**: Rappel architecture
- **Seconde infraction**: Révocation autorisation
- **Récidive**: Onboarding complet obligatoire

## 🎯 **OBJECTIFS ORGANISATION**

### **Court Terme**
- Maintenir structure cohérente
- Documenter toutes analyses
- Vérifier références régulièrement
- Consolider métadonnées
- **Former tous agents IA au copilotage**

### **Long Terme**
- Automatiser vérification références
- Intégrer APIs validation externe
- Développer système veille scientifique
- Créer pipeline documentation automatique
- **Écosystème agents IA auto-gouverné**

---

**Règles Copilotage v0.0.2** ✓  
*Organisation cohérente, qualité maintenue, agents IA gouvernés, simplification systématique*

---
*Dernière mise à jour: 21/09/2025*
*Ajout directive simplification obligatoire pour tous les modules*

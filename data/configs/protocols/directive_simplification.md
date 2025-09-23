# 🔧 Directive de Simplification des Commandes

## 📋 Vue d'ensemble

Ce protocole établit la **directive obligatoire de simplification** pour tous les modules du système PaniniFS. Toute commande complexe doit être transformée en script Python dédié pour maintenir la lisibilité, la réutilisabilité et la maintenabilité.

## ⚖️ Règle Fondamentale

> **OBLIGATOIRE TOUS MODULES**: Si une commande est trop complexe pour autoapprobation, créer un fichier Python dédié pour l'exécuter en un appel simple.

## 🎯 Critères de Complexité

Une commande est considérée comme "trop complexe" si elle contient **un ou plusieurs** des éléments suivants :

### ❌ Indicateurs de Complexité
- **Plus de 3 paramètres distincts**
- **Chaînage de commandes** (pipes `|`)
- **Opérateurs logiques** (`&&`, `||`)
- **Expressions régulières complexes**
- **Boucles ou itérations**
- **Manipulation de fichiers multiples**
- **Substitution de commandes** (`$(...)`, `` `...` ``)
- **Redirections multiples** (`>`, `>>`, `2>&1`)

### ✅ Exemples d'Application

#### Avant (❌ Interdit)
```bash
find . -name "*.py" -exec grep -l "def main" {} \; | xargs wc -l | sort -n
ps aux | grep -E "(panini|orchestrateur)" | grep -v grep | awk '{print $2}' | xargs kill -9
tail -f /var/log/app.log | grep ERROR | while read line; do echo "$(date): $line"; done
```

#### Après (✅ Obligatoire)
```python
# Créer des scripts dédiés
python3 analyser_fonctions_main.py
python3 arreter_processus_panini.py
python3 surveiller_erreurs_log.py
```

## 🛠️ Outils Disponibles

### Simplificateur Global
```bash
# Pour un module spécifique
python3 copilotage/utilities/panini_global_simplifier.py 'commande complexe'

# Pour tous les modules
python3 copilotage/utilities/panini_global_simplifier.py --apply-all 'commande'

# Validation de l'installation
python3 copilotage/utilities/panini_global_simplifier.py --validate
```

### Snippets VS Code
Dans VS Code, utiliser les préfixes :
- `simp-cmd` : Template de script générique
- `simp-proc` : Gestion de processus
- `simp-find` : Recherche de fichiers
- `simp-logs` : Analyse de logs
- `simp-auto` : Appel du simplificateur

### Templates Partagés
Templates disponibles dans `copilotage/shared/templates/` :
- `script_processus.py` : Gestion de processus
- `script_fichiers.py` : Manipulation de fichiers
- `script_logs.py` : Analyse de logs
- `script_generique.py` : Template de base

## 🎯 Workflow d'Application

### 1. Détection
Lors de l'écriture d'une commande, vérifier les critères de complexité.

### 2. Évaluation
Si **un seul critère** est présent → Simplification obligatoire.

### 3. Création
```bash
# Option 1: Simplificateur automatique
python3 copilotage/utilities/panini_global_simplifier.py 'votre_commande'

# Option 2: Snippet VS Code
# Taper 'simp-cmd' dans l'éditeur

# Option 3: Template manuel
cp copilotage/shared/templates/script_generique.py votre_script.py
```

### 4. Validation
- ✅ Script exécutable (`chmod +x`)
- ✅ Gestion d'erreurs incluse
- ✅ Messages de statut clairs
- ✅ Documentation inline

## 📁 Organisation des Scripts

### Structure Recommandée
```
module/
├── scripts_generes/           # Scripts créés par simplification
│   ├── analyser_donnees.py
│   ├── nettoyer_fichiers.py
│   └── surveiller_processus.py
├── utilities/                 # Utilitaires du module
└── README.md                 # Documentation module
```

### Conventions de Nommage
- **Format**: `[action]_[objet].py`
- **Exemples**: 
  - `analyser_logs.py`
  - `nettoyer_fichiers.py`
  - `surveiller_processus.py`
  - `extraire_donnees.py`

## 🏛️ Gouvernance

### Application Transversale
Cette directive s'applique à **tous les modules** PaniniFS :
- ✅ `tech/` - Implémentations techniques
- ✅ `panini/` - Recherche linguistique
- ✅ `docs/` - Documentation
- ✅ `copilotage/` - Gouvernance système

### Contrôle Qualité
- **Revue automatique** : Scripts de validation
- **Intégration CI/CD** : Vérification à chaque commit
- **Formation agents IA** : Règles intégrées dans les prompts système

### Sanctions
1. **Première infraction** : Rappel de la directive
2. **Seconde infraction** : Formation obligatoire
3. **Récidive** : Révision des autorisations

## 🎉 Bénéfices Attendus

### Pour le Développement
- ✅ **Lisibilité** : Code clair et compréhensible
- ✅ **Réutilisabilité** : Scripts modulaires
- ✅ **Maintenabilité** : Débogage facilité
- ✅ **Collaboration** : Standards partagés

### Pour l'Écosystème
- ✅ **Cohérence** : Approche unifiée
- ✅ **Évolutivité** : Extension facilitée
- ✅ **Robustesse** : Gestion d'erreurs systématique
- ✅ **Documentation** : Auto-documentée

---

**Protocole établi** : 21/09/2025  
**Version** : 1.0.0  
**Scope** : Tous modules PaniniFS  
**Statut** : Obligatoire
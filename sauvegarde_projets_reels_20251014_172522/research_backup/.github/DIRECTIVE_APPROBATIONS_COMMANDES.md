# 🔐 DIRECTIVE SPEC-KIT : GESTION APPROBATIONS COMMANDES

**Version** : 1.0  
**Date** : 2025-10-03  
**Responsabilité** : GitHub Copilot + Spec-Kit  
**Criticité** : HAUTE - Sécurité & Autonomie

---

## 📋 OBJECTIF

**Optimiser régulièrement** le fichier `copilot-approved-scripts.json` et **vérifier systématiquement** la préapprobation des commandes avant exécution.

---

## 🎯 DIRECTIVE PRINCIPALE

### ⚡ VÉRIFICATION PRÉALABLE OBLIGATOIRE

**AVANT CHAQUE EXÉCUTION** de commande dans le terminal :

1. **Vérifier** si la commande est dans `copilot-approved-scripts.json`
2. **Valider** que les arguments correspondent aux patterns autorisés
3. **Logger** toute tentative de commande non-préapprouvée
4. **Demander approbation manuelle** si nécessaire

### 📊 OPTIMISATION RÉGULIÈRE

**CHAQUE SEMAINE** (dimanche 23h00 UTC) :

1. **Analyser** les logs d'exécution de commandes
2. **Identifier** les patterns manquants ou trop restrictifs
3. **Proposer** des ajustements aux regex d'approbation
4. **Mettre à jour** le fichier avec version incrémentée

---

## 🔧 ALGORITHME D'APPROBATION

### Phase 1 : Validation Syntaxique

```javascript
function validateCommand(command, args) {
    const approvedPatterns = loadApprovedPatterns();
    
    // 1. Vérification pattern de base
    const basePattern = findMatchingPattern(command, approvedPatterns);
    if (!basePattern) {
        return { approved: false, reason: "Command not in approved patterns" };
    }
    
    // 2. Validation arguments
    const argsValid = validateArguments(args, basePattern.constraints);
    if (!argsValid.valid) {
        return { approved: false, reason: argsValid.reason };
    }
    
    // 3. Vérification contraintes sécurité
    const securityCheck = checkSecurityConstraints(command, args);
    if (!securityCheck.safe) {
        return { approved: false, reason: securityCheck.reason };
    }
    
    return { approved: true, pattern: basePattern.name };
}
```

### Phase 2 : Contrôles Contextuels

```python
def verify_execution_context(command, workspace_path):
    """Vérification du contexte d'exécution"""
    
    # 1. Vérifier répertoire autorisé
    if not is_allowed_directory(workspace_path):
        return False, "Directory not in allowed list"
    
    # 2. Vérifier limites de ressources
    if command.requires_network and not network_allowed():
        return False, "Network access not permitted"
    
    # 3. Vérifier taille fichiers
    if command.file_operations:
        for file in command.target_files:
            if get_file_size(file) > MAX_FILE_SIZE:
                return False, f"File {file} exceeds size limit"
    
    return True, "Context validation passed"
```

---

## 🔄 CYCLE D'OPTIMISATION AUTOMATIQUE

### 📈 Métriques de Performance

**Collecte Continue** :
- Nombre de commandes approuvées/refusées par jour
- Temps moyen de validation 
- Patterns les plus utilisés
- Faux positifs/négatifs

**Seuils d'Alerte** :
- \> 10% de refus de commandes légitimes → Assouplir patterns
- \> 5% de temps d'attente > 2s → Optimiser regex
- \> 1% de commandes dangereuses acceptées → Durcir sécurité

### 🎛️ Ajustements Automatiques

```yaml
# Exemple de règle d'optimisation
optimization_rules:
  pattern_extension:
    trigger: "refused_legitimate_commands > 5 per week"
    action: "extend_regex_patterns"
    validation: "manual_review_required"
  
  security_hardening:
    trigger: "suspicious_activity_detected"
    action: "add_security_constraints"
    notification: "immediate_alert"
  
  performance_improvement:
    trigger: "validation_time > 2000ms average"
    action: "optimize_regex_compilation"
    testing: "performance_regression_tests"
```

---

## 🛡️ SÉCURITÉ & FAIL-SAFE

### 🚨 Modes de Défaillance Sécurisée

1. **Fichier corrompu** → Mode manuel obligatoire
2. **Regex invalide** → Utiliser version backup
3. **Timeout validation** → Refuser par défaut
4. **Ressources insuffisantes** → Queue avec priorité

### 🔐 Principes de Sécurité

- **Least Privilege** : Permissions minimales par défaut
- **Defense in Depth** : Validation multi-niveaux
- **Audit Trail** : Log complet de toutes les décisions
- **Fail Secure** : En cas de doute, refuser

---

## 📝 IMPLÉMENTATION PRATIQUE

### 🔧 Script de Vérification Pré-Exécution

```bash
#!/bin/bash
# pre_execution_validator.sh

COMMAND="$1"
ARGS="$2"
WORKSPACE="$3"

# 1. Vérifier approbation
python3 .github/scripts/validate_command.py "$COMMAND" "$ARGS" "$WORKSPACE"
VALIDATION_RESULT=$?

if [ $VALIDATION_RESULT -eq 0 ]; then
    echo "✅ Command approved: $COMMAND $ARGS"
    # 2. Logger l'exécution
    echo "$(date -Iseconds) APPROVED $COMMAND $ARGS" >> .github/logs/command_execution.log
    exit 0
else
    echo "❌ Command requires manual approval: $COMMAND $ARGS"
    # 3. Logger le refus
    echo "$(date -Iseconds) REJECTED $COMMAND $ARGS" >> .github/logs/command_execution.log
    exit 1
fi
```

### 🔄 Optimiseur Hebdomadaire

```python
#!/usr/bin/env python3
# weekly_optimizer.py

import json
import re
from datetime import datetime, timedelta
from collections import Counter

def analyze_command_patterns():
    """Analyser les patterns de commandes de la semaine"""
    
    # 1. Charger les logs
    logs = load_execution_logs(days=7)
    
    # 2. Identifier patterns manquants
    rejected_commands = [log for log in logs if log.status == 'REJECTED']
    missing_patterns = identify_missing_patterns(rejected_commands)
    
    # 3. Proposer nouvelles règles
    new_rules = generate_safe_patterns(missing_patterns)
    
    # 4. Mettre à jour le fichier
    update_approved_scripts(new_rules)
    
    return {
        'analyzed_commands': len(logs),
        'rejected_count': len(rejected_commands),
        'new_patterns_added': len(new_rules),
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    result = analyze_command_patterns()
    print(f"Weekly optimization completed: {result}")
```

---

## 📊 MONITORING & ALERTES

### 🔍 Dashboard de Monitoring

**Métriques Temps Réel** :
- ✅ Commandes approuvées (dernières 24h)
- ❌ Commandes refusées (dernières 24h)  
- ⏱️ Temps moyen de validation
- 🚨 Tentatives suspectes

**Alertes Automatiques** :
- Email si > 20 refus/jour
- Slack si temps validation > 5s
- GitHub Issue si pattern manquant détecté

### 📈 Rapports Hebdomadaires

```json
{
  "week": "2025-10-03",
  "total_commands": 2847,
  "approved": 2723,
  "rejected": 124,
  "approval_rate": "95.6%",
  "top_patterns": [
    "python3 panini_*.py",
    "curl -s http://127.0.0.1:*",
    "pkill -f panini*"
  ],
  "optimization_suggestions": [
    "Add pattern for 'git commit -am'",
    "Extend timeout for heavy operations",
    "Allow port range 9000-9999"
  ]
}
```

---

## 🎯 INTÉGRATION SPEC-KIT

### 📁 Structure Fichiers

```
.github/
├── copilot-approved-scripts.json      # ✅ Configuration principale
├── scripts/
│   ├── validate_command.py            # 🔧 Validateur pré-exécution
│   ├── weekly_optimizer.py            # 📊 Optimiseur automatique
│   └── security_checker.py            # 🛡️ Vérifications sécurité
├── logs/
│   ├── command_execution.log          # 📝 Historique commandes
│   ├── optimization_history.log       # 🔄 Historique optimisations
│   └── security_alerts.log            # 🚨 Alertes sécurité
└── workflows/
    ├── command_approval.yml            # 🔄 Workflow validation
    └── weekly_optimization.yml         # 📅 Optimisation hebdomadaire
```

### ⚙️ GitHub Actions

```yaml
# .github/workflows/command_approval.yml
name: Command Approval Validation

on:
  workflow_call:
    inputs:
      command:
        required: true
        type: string
      args:
        required: false
        type: string

jobs:
  validate-command:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Command
        run: |
          python3 .github/scripts/validate_command.py "${{ inputs.command }}" "${{ inputs.args }}"
```

---

## ✅ CHECKLIST D'IMPLÉMENTATION

### Phase 1 : Setup Initial
- [ ] Créer scripts de validation
- [ ] Configurer logging
- [ ] Tester avec commandes existantes
- [ ] Documenter processus

### Phase 2 : Monitoring
- [ ] Implémenter dashboard
- [ ] Configurer alertes
- [ ] Tester fail-safe modes
- [ ] Former l'équipe

### Phase 3 : Optimisation
- [ ] Déployer optimiseur automatique  
- [ ] Analyser première semaine
- [ ] Ajuster patterns
- [ ] Valider sécurité

---

## 🚀 BÉNÉFICES ATTENDUS

### 🎯 Sécurité
- **Zéro** commande dangereuse exécutée
- **Audit trail** complet
- **Fail-safe** par défaut

### ⚡ Performance  
- **< 100ms** temps de validation
- **> 95%** taux d'approbation légitime
- **Automatisation** complète

### 🔄 Maintenance
- **Auto-optimisation** hebdomadaire
- **Détection proactive** de besoins
- **Évolution continue** des patterns

---

**⚠️ RESPONSABILITÉ** : Cette directive doit être appliquée **systématiquement** par GitHub Copilot pour garantir la sécurité et l'efficacité du système d'approbation des commandes.
# 🔧 SOLUTIONS VSCODE STABILITÉ

## 🚨 Actions Immédiates (À FAIRE MAINTENANT)

### 1. Arrêter le Processus Git Problématique
```bash
# Identifier et arrêter le git reset qui consomme 99% CPU
sudo pkill -f "git reset --hard"
# Ou plus spécifique :
sudo kill -9 1481374
```

### 2. Redémarrer VS Code Proprement
```bash
# Fermer toutes les instances VS Code
pkill -f "code"
# Attendre 30 secondes puis relancer
code --disable-extensions
```

### 3. Configuration GPU Temporaire
```bash
# Désactiver l'accélération matérielle VS Code
code --disable-gpu --disable-software-rasterizer
```

## 🔧 Solutions Permanentes

### A. Stabilisation Extensions VS Code

#### Désactiver Extensions Problématiques
1. **Pylance** : Réduire les fonctionnalités
   ```json
   "python.analysis.autoImportCompletions": false,
   "python.analysis.autoSearchPaths": false,
   "python.analysis.diagnosticMode": "openFilesOnly"
   ```

2. **Spell Checker** : Limiter la portée
   ```json
   "cSpell.enabled": false,
   "cSpell.diagnosticLevel": "Hint"
   ```

#### Configuration VS Code Optimisée
```json
{
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/**": true,
        "**/.venv/**": true,
        "**/corpus_*.json": true
    },
    "search.exclude": {
        "**/.git": true,
        "**/node_modules": true,
        "**/.venv": true,
        "**/corpus_*.json": true
    },
    "files.exclude": {
        "**/corpus_*.json": true,
        "**/__pycache__": true
    },
    "workbench.settings.enableNaturalLanguageSearch": false,
    "extensions.autoUpdate": false,
    "git.autofetch": false,
    "git.autorefresh": false
}
```

### B. Optimisation Système

#### 1. Configuration GPU Driver
```bash
# Vérifier driver actuel
lsmod | grep amdgpu

# Si nécessaire, recompiler drivers
sudo dkms reconfigure amdgpu

# Paramètres kernel pour stabilité
echo 'GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.dpm=0"' | sudo tee -a /etc/default/grub
sudo update-grub
```

#### 2. Limites Processus VS Code
```bash
# Créer limits pour VS Code
sudo tee /etc/security/limits.d/vscode.conf << EOF
stephane soft nproc 1000
stephane hard nproc 1500
stephane soft nofile 4096
stephane hard nofile 8192
EOF
```

#### 3. Optimisation Mémoire
```bash
# Augmenter vm.swappiness pour éviter OOM
echo 'vm.swappiness=60' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### C. Monitoring et Prévention

#### Script de Surveillance
```bash
#!/bin/bash
# /home/stephane/scripts/vscode-monitor.sh

while true; do
    # Vérifier CPU usage de VS Code
    CPU=$(ps aux | grep "[c]ode" | awk '{sum+=$3} END {print sum}')
    if (( $(echo "$CPU > 200" | bc -l) )); then
        echo "$(date): VS Code CPU critique: $CPU%" >> /var/log/vscode-monitor.log
        # Optionnel: redémarrer automatiquement
        # pkill -f "code.*pylance"
    fi
    
    # Vérifier core dumps
    if coredumpctl list | grep -q "$(date +%Y-%m-%d).*code"; then
        echo "$(date): Nouveau crash VS Code détecté" >> /var/log/vscode-monitor.log
    fi
    
    sleep 60
done
```

## 🎯 Configuration Recommandée

### Extensions à Conserver (Minimales)
- Python (sans Pylance si possible)
- GitLens (configuration allégée)

### Extensions à Désactiver Temporairement
- Pylance (utiliser Jedi à la place)
- Code Spell Checker
- Toutes extensions non-essentielles

### Workspace Settings
```json
{
    "python.defaultInterpreterPath": "/home/stephane/GitHub/PaniniFS-Research/.venv/bin/python",
    "python.analysis.disabled": [
        "unresolved-import",
        "unused-import"
    ],
    "python.linting.enabled": false,
    "python.formatting.provider": "none",
    "git.enabled": false,
    "terminal.integrated.gpuAcceleration": "off"
}
```

## 📊 Tests de Stabilité

### Commandes de Test
```bash
# Test charge système après optimisation
uptime && ps aux --sort=-%cpu | head -10

# Vérifier pas de nouveaux crashes
coredumpctl list | tail -5

# Monitor mémoire VS Code
watch -n 5 'ps aux | grep "[c]ode" | head -5'
```

### Métriques de Succès
- Load average < 2.0
- Pas de core dumps VS Code > 2h
- CPU VS Code < 50% en idle
- Mémoire VS Code < 2GB total

---
**Date**: $(date)
**Status**: Solutions prêtes à déployer
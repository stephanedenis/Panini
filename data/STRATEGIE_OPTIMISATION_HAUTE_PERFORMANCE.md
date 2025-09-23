# 🚀 STRATÉGIE OPTIMISATION HAUTE PERFORMANCE

## 💡 Philosophie: Utiliser la Puissance, Pas la Limiter

### Configuration Cible Multi-GPU
```
System: 16 cores + 62GB RAM + Dual GPU
┌─────────────────────────────────────────────────────┐
│  HD 7750 (Affichage)    +    RX 480 (Calcul)       │
│  ├─ 4 écrans stables    │    ├─ Pylance GPU         │
│  ├─ Interface fluide    │    ├─ Corpus processing   │
│  ├─ 55W efficient       │    ├─ ML/AI workloads     │
│  └─ Display only        │    └─ 150W performance    │
└─────────────────────────────────────────────────────┘
```

## 🎯 Optimisations Intelligentes VS Code

### 1. Configuration Multi-Worker Pylance
```json
{
    "python.analysis.autoImportCompletions": true,
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.indexing": true,
    "python.analysis.packageIndexDepths": [
        {"name": "", "depth": 2},
        {"name": "numpy", "depth": 3},
        {"name": "pandas", "depth": 3}
    ],
    "python.analysis.memory.keepLibraryAst": true,
    "python.analysis.userFileIndexingLimit": -1
}
```

### 2. Optimisation Extensions pour Machine Puissante
```json
{
    "extensions.experimental.affinity": {
        "ms-python.vscode-pylance": 1,
        "ms-python.python": 1,
        "streetsidesoftware.code-spell-checker": 2
    },
    "python.defaultInterpreterPath": "/home/stephane/GitHub/PaniniFS-Research/.venv/bin/python",
    "python.analysis.stubPath": "./typings",
    "python.analysis.typeCheckingMode": "basic"
}
```

### 3. Configuration GPU-Aware
```json
{
    "terminal.integrated.gpuAcceleration": "on",
    "workbench.experimental.enableNewProfilesUI": true,
    "debug.javascript.usePreview": true,
    "typescript.preferences.includePackageJsonAutoImports": "on",
    "search.experimental.closedNotebookRichContentResults": true
}
```

## 🔧 Drivers Multi-GPU Optimaux

### Configuration AMDGPU pour Dual Card
```bash
# /etc/modprobe.d/amdgpu.conf
options amdgpu dpm=1
options amdgpu dc=1
options amdgpu exp_hw_support=1
options amdgpu gpu_recovery=1
options amdgpu mcbp=1
options amdgpu runpm=0

# Force detection des deux cartes
options amdgpu si_support=1
options amdgpu cik_support=1
```

### Variables Environnement GPU
```bash
# ~/.bashrc additions for dual GPU
export DRI_PRIME=1                    # Force GPU selection
export AMDGPU_TARGETS="gfx803,gfx1030" # Support HD7750 + RX480
export ROC_ENABLE_DPM=1               # Enable power management
export GPU_MAX_HEAP_SIZE="100"       # Use full GPU memory
export GPU_USE_SYNC_OBJECTS=1         # Better performance
export GPU_MAX_ALLOC_PERCENT="100"    # Allow full allocation
```

## 📊 Surveillance Performance Intelligente

### Script Monitoring Avancé
```bash
#!/bin/bash
# /home/stephane/scripts/intelligent-monitor.sh

LOGFILE="/var/log/performance-optimization.log"

while true; do
    # CPU per core utilization
    CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
    LOAD_AVG=$(uptime | awk '{print $10}' | tr -d ',')
    
    # Memory usage efficiency
    MEM_USED=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
    
    # GPU utilization both cards
    GPU1_UTIL=$(cat /sys/class/drm/card1/device/gpu_busy_percent 2>/dev/null || echo "0")
    
    # VS Code processes optimization
    VSCODE_MEM=$(ps aux | grep '[c]ode' | awk '{sum+=$4} END {printf "%.1f", sum}')
    PYLANCE_COUNT=$(ps aux | grep '[p]ylance' | wc -l)
    
    # Log intelligent metrics
    echo "$(date): Load:$LOAD_AVG/$CPU_CORES Mem:${MEM_USED}% GPU1:${GPU1_UTIL}% VSCode:${VSCODE_MEM}% Pylance:$PYLANCE_COUNT" >> $LOGFILE
    
    # Auto-optimization triggers
    if (( $(echo "$LOAD_AVG > $(($CPU_CORES * 2))" | bc -l) )); then
        echo "$(date): High load detected, optimizing..." >> $LOGFILE
        # Renice VS Code processes for better responsiveness
        pgrep -f "code" | xargs -I {} renice -n -5 -p {} 2>/dev/null
    fi
    
    # GPU memory optimization
    if [ "$GPU1_UTIL" -gt 90 ]; then
        echo "$(date): GPU saturation, switching compute to GPU2" >> $LOGFILE
        export DRI_PRIME=2  # Switch to RX 480 when available
    fi
    
    sleep 30
done
```

## 🎨 Configuration Workspace Haute Performance

### PaniniFS Research Optimized Settings
```json
{
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/node_modules/**": true
    },
    "search.exclude": {
        "**/.git": true,
        "**/corpus_*.json": false,
        "**/__pycache__": true
    },
    "files.associations": {
        "*.dhatu": "python",
        "*.panini": "python"
    },
    "python.analysis.extraPaths": [
        "./",
        "./corpus",
        "./panini",
        "./dhatu"
    ],
    "python.analysis.autoSearchPaths": true,
    "python.analysis.diagnosticMode": "workspace",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=120",
        "--disable=C0103,C0114,C0116"
    ]
}
```

## 🚀 Objectifs Performance

### Métriques Cible Post-Optimisation
- **Load Average**: < 8.0 (50% utilisation max)
- **VS Code Memory**: < 4GB total
- **Pylance Response**: < 200ms
- **GPU HD7750**: 100% dédiée affichage
- **GPU RX480**: 100% dédiée calcul
- **Zero Crashes**: > 8h uptime stable

### Bénéfices Attendus
- **Multi-tasking fluide**: 16 cœurs bien répartis
- **Affichage ultra-stable**: HD7750 dédiée
- **Calculs accélérés**: RX480 pour corpus/ML
- **Responsivité VS Code**: Optimisé, pas bridé
- **Évolutivité**: Prêt pour charges importantes

---
**Stratégie**: Exploiter la puissance hardware au lieu de la contraindre
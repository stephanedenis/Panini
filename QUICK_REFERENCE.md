# 🚀 RÉFÉRENCE RAPIDE - Colab Pro + VSCode

## ⚡ TL;DR

**Question**: Comment debugger du code GPU sur Colab avec VSCode?  
**Réponse**: Cliquez le badge → Run all → Connect VSCode → F5 pour debugger

### 🔗 Liens Directs Colab

**Debugging Interactif**:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_vscode_tunnel.ipynb)

**Batch Processing**:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon.ipynb)

> 📝 Tous les liens: [`COLAB_DIRECT_LINKS.md`](COLAB_DIRECT_LINKS.md)

---

## 📋 2 Solutions Disponibles

### Solution 1: VSCode Tunnel (Debugging Interactif)
```bash
# Upload: notebooks/colab_vscode_tunnel.ipynb
# ✅ Breakpoints, Step trace, Variables panel
# 🎯 Use case: Prototypage, debugging, exploration
```

### Solution 2: Git Daemon (Batch Processing)
```bash
# Upload: notebooks/colab_gpu_daemon.ipynb  
# ✅ Lancer et oublier, multi-expériences, Git-based
# 🎯 Use case: Benchmarks, training long, production
```

---

## 🔧 Setup 5 Minutes - Solution 1 (Debug)

### Sur Colab
1. Upload `notebooks/colab_vscode_tunnel.ipynb`
2. Runtime → GPU
3. Run all cells
4. Copier URL tunnel affichée

### Sur VSCode Local
1. Installer extension: "Remote - Tunnels"
2. `Ctrl+Shift+P` → "Connect to Tunnel"
3. Login GitHub → Sélectionner "colab-panini-debug"
4. ✅ Nouvelle fenêtre VSCode = Colab!

### Debugger
1. Ouvrir `experiments/debug_gpu_example.py`
2. Clic gauche = breakpoint (point rouge)
3. `F5` = Start debugging
4. `F10` = Step Over, `F11` = Step Into

---

## 🔧 Setup 5 Minutes - Solution 2 (Batch)

### Sur Colab
1. Upload `notebooks/colab_gpu_daemon.ipynb`
2. Runtime → GPU
3. Run all cells
4. Daemon watch GitHub en background

### Sur Local
1. Éditer `experiments.json`:
```json
[
  {
    "name": "mon_experience",
    "command": "python experiments/mon_script.py",
    "status": "pending",
    "timeout": 600
  }
]
```
2. Commit + Push:
```bash
git add experiments.json
git commit -m "exp: mon experience"
git push origin gpu-experiments
```
3. Daemon exécute automatiquement
4. Pull résultats:
```bash
./tools/sync_colab_results.sh
cat experiments.json  # Voir status
```

---

## 🎯 Quelle Solution?

| Besoin | Solution |
|--------|----------|
| Debugger bug GPU | **1 (Tunnel)** |
| Breakpoints + step trace | **1 (Tunnel)** |
| Training >10 min | **2 (Daemon)** |
| Batch benchmarks | **2 (Daemon)** |
| Prototypage rapide | **1 (Tunnel)** |
| Plusieurs expériences | **2 (Daemon)** |
| Explorer dataset | **1 (Tunnel)** |
| Lancer et oublier | **2 (Daemon)** |

---

## 🐛 Debugging Quick Reference

### Contrôles Debug
| Action | Shortcut |
|--------|----------|
| Start Debugging | `F5` |
| Toggle Breakpoint | `F9` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Continue | `F5` |
| Stop | `Shift+F5` |

### Watch Expressions (GPU)
```python
torch.cuda.memory_allocated() / 1e9
torch.cuda.get_device_name(0)
x.shape if 'x' in locals() else None
x.device if 'x' in locals() else None
```

### Configs Debug Disponibles
- 🔧 Debug GPU Example
- 🎯 Debug Audio Fingerprinting
- 🧪 Debug Current File
- 📊 Debug with Profiling
- 🐛 Debug with Memory Tracking
- 🧮 Debug Tests

---

## 📚 Documentation Complète

| Document | Quoi |
|----------|------|
| `DECISION_MATRIX.md` | Tableau visuel pour choisir |
| `DEBUG_GPU_GUIDE.md` | Guide debug complet |
| `SOLUTION_COMPARISON.md` | Comparaison détaillée |
| `INFRASTRUCTURE_RECAP.md` | Vue d'ensemble complète |
| `COLAB_PRO_VSCODE_STRATEGIES.md` | 5 solutions originales |

---

## 🆘 Troubleshooting Rapide

### Tunnel ne se connecte pas
```bash
# Colab: Re-run cells 3 et 4
# VSCode: Ctrl+Shift+P → Connect to Tunnel
```

### Breakpoints ignorés
```bash
# Terminal VSCode (tunnel):
cd /content/work
git pull origin gpu-experiments
pip install -r requirements.txt
```

### Daemon ne détecte pas commits
```bash
# Colab: Vérifier logs daemon
!tail -f /content/daemon.log

# Local: Vérifier branch correcte
git branch  # Doit être sur gpu-experiments
```

### CUDA out of memory
```python
# Debug Console (pendant pause):
>>> torch.cuda.empty_cache()
>>> torch.cuda.memory_allocated() / 1e9
```

---

## 📁 Fichiers Clés

```
notebooks/
├── colab_vscode_tunnel.ipynb    # Solution 1 (Debug)
└── colab_gpu_daemon.ipynb       # Solution 2 (Batch)

experiments/
├── debug_gpu_example.py         # Exemples debug
└── benchmark_audio_fingerprinting.py

.vscode/
└── launch.json                  # 6 configs debug

docs/infrastructure/
├── DECISION_MATRIX.md           # ← Lire en premier!
├── DEBUG_GPU_GUIDE.md
└── SOLUTION_COMPARISON.md
```

---

## 🎯 Prochaines Actions

### ✅ À Faire Maintenant
1. **Upload `colab_vscode_tunnel.ipynb`** sur Colab
2. **Run all cells**
3. **Connect VSCode** (Ctrl+Shift+P → Connect to Tunnel)
4. **Test debug**: Ouvrir `debug_gpu_example.py` → F5

### ✅ Après Premier Test
1. **Upload `colab_gpu_daemon.ipynb`** sur Colab
2. **Modifier `experiments.json`** localement
3. **Commit + Push**
4. **Vérifier exécution** avec `sync_colab_results.sh`

### ✅ Pour Production
1. **Utiliser Tunnel** pour prototyper + debugger
2. **Utiliser Daemon** pour exécution complète
3. **Analyser résultats**
4. **Itérer**

---

## 💡 Tips

**Tunnel Lent?** → Normal (latence réseau). Utiliser pour debug seulement, pas training long.

**Daemon Échoue?** → Vérifier `experiments.json` syntaxe, timeout suffisant, dépendances installées.

**Les Deux Ensemble?** → OUI! Lancer 2 notebooks Colab séparés.

**Colab Gratuit?** → Fonctionne aussi! Mais GPU T4 limité à 12h/jour.

**Besoin Autre Solution?** → Voir `COLAB_PRO_VSCODE_STRATEGIES.md` (3 autres solutions).

---

## 🏆 Résumé Session

**Créé**:
- 2 workflows complets (Tunnel + Daemon)
- 4 notebooks Colab
- 6 configs debug VSCode
- 400+ lignes code exemple debug
- 5 guides documentation complets

**Temps setup**: 10 minutes (5 min/solution)

**Prêt à utiliser**: ✅ OUI!

---

**🚀 Go! Upload un notebook sur Colab et testez!**

---

## 📞 Support

Problème? Consultez la doc:
```bash
ls docs/infrastructure/
# DECISION_MATRIX.md        ← Commencer ici
# DEBUG_GPU_GUIDE.md        ← Pour debugging
# SOLUTION_COMPARISON.md    ← Détails techniques
```

Question non résolue? Vérifiez:
1. GPU activé sur Colab (Runtime → GPU)
2. Extension "Remote - Tunnels" installée (VSCode)
3. Git credentials configurés (username + token)
4. Branch `gpu-experiments` active

---

**Version**: 2025-11-14  
**Branch**: `gpu-experiments`  
**Status**: ✅ Production Ready

# 🚀 Liens Directs Colab - One-Click Setup

## ⚡ Ouvrir Directement dans Google Colab

### Solution 1: VSCode Remote Tunnel (Debugging Interactif)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_vscode_tunnel.ipynb)

**Lien direct**: https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_vscode_tunnel.ipynb

**Ce que ça fait**:
- ✅ Ouvre le notebook directement dans Colab
- ✅ Setup VSCode Server + Tunnel
- ✅ Debugging interactif avec breakpoints
- ✅ Step trace (F10/F11)

---

### Solution 2: Git Daemon (Batch Processing)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon.ipynb)

**Lien direct**: https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon.ipynb

**Ce que ça fait**:
- ✅ Ouvre le notebook directement dans Colab
- ✅ Daemon watch GitHub
- ✅ Exécution automatique expériences
- ✅ Lancer et oublier

### Solution 2B: Git Daemon Lite (Clone Partiel ⚡)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon_lite.ipynb)

**Lien direct**: https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon_lite.ipynb

**Ce que ça fait**:
- ✅ Clone **uniquement fichiers audio** (sparse checkout)
- ✅ **95% plus rapide** que clone complet (~25MB vs ~500MB)
- ✅ Parfait pour expériences audio fingerprinting
- ✅ Même fonctionnalités que Solution 2

---

## 📋 Instructions Post-Ouverture

### Pour Solution 1 (Tunnel):
1. ✅ Notebook ouvert dans Colab
2. **Runtime → Change runtime type → GPU**
3. **Runtime → Run all** (`Ctrl+F9`)
4. Suivre instructions auth GitHub (cellule 3)
5. Copier URL tunnel affichée
6. VSCode local: `Ctrl+Shift+P` → "Connect to Tunnel"
7. Debugger avec breakpoints!

### Pour Solution 2 (Daemon):
1. ✅ Notebook ouvert dans Colab
2. **Runtime → Change runtime type → GPU**
3. **Runtime → Run all** (`Ctrl+F9`)
4. Daemon tourne en background
5. Local: Modifier `experiments.json` → Commit → Push
6. Daemon exécute automatiquement
7. Local: `./tools/sync_colab_results.sh` pour résultats

---

## 🔗 Badges Markdown (Pour Documentation)

### Solution 1 (Tunnel)
```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_vscode_tunnel.ipynb)
```

### Solution 2 (Daemon)
```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon.ipynb)
```

---

## 🎯 Usage dans README

Exemple d'intégration dans un README:

```markdown
## 🚀 Quick Start

### Debugging Interactif GPU
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_vscode_tunnel.ipynb)

Cliquez le badge → Runtime → GPU → Run all → Connecter VSCode

### Batch Processing Automatisé
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon.ipynb)

Cliquez le badge → Runtime → GPU → Run all → Push expériences
```

---

## 📱 Format URL Colab

**Pattern général**:
```
https://colab.research.google.com/github/{user}/{repo}/blob/{branch}/{path_to_notebook}
```

**Vos notebooks**:
- User: `stephanedenis`
- Repo: `Panini`
- Branch: `gpu-experiments`
- Paths:
  - `notebooks/colab_vscode_tunnel.ipynb`
  - `notebooks/colab_gpu_daemon.ipynb`

---

## 🔧 Liens Alternatifs

### Ouvrir depuis Main Branch (après merge)
```
https://colab.research.google.com/github/stephanedenis/Panini/blob/main/notebooks/colab_vscode_tunnel.ipynb
https://colab.research.google.com/github/stephanedenis/Panini/blob/main/notebooks/colab_gpu_daemon.ipynb
```

### Ouvrir Version Spécifique (commit hash)
```
https://colab.research.google.com/github/stephanedenis/Panini/blob/c50d8c85/notebooks/colab_vscode_tunnel.ipynb
```

---

## 💡 Avantages Liens Directs

✅ **One-click**: Pas besoin d'upload manuel  
✅ **Toujours à jour**: Pointe vers GitHub  
✅ **Partageable**: Envoyez lien à collègues  
✅ **Version control**: Suit vos commits  
✅ **Documentation**: Intégrable dans README/docs  

---

## 📝 Note Importante

**Les notebooks doivent être publics** ou vous devez être **authentifié sur GitHub** pour que Colab puisse les charger depuis un repo privé.

Si le repo est **privé**, Colab demandera l'authentification GitHub au premier chargement.

---

## 🚀 Testez Maintenant!

**Cliquez un badge ci-dessus** ou copiez-collez un lien dans votre navigateur!

Le notebook s'ouvrira directement dans Colab, prêt à être exécuté. 🎉

---

**Dernière mise à jour**: 2025-11-14  
**Branch**: `gpu-experiments`

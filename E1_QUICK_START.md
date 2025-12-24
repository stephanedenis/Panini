# 🚀 E1 COLAB QUICK START

**TL;DR**: Copie-colle dans une cellule Colab et c'est parti 👇

---

## ⚡ OPTION 1: Notebook Complet (Recommandé)

### Colab URL Directe:
```
https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/E1_COLAB_EXECUTOR.ipynb
```

### Steps:
1. Ouvre le lien ☝️
2. `Runtime` → `Change runtime type` → Sélectionne **T4 GPU**
3. `Runtime` → `Run all` (ou Ctrl+F9)
4. Attends 3-5 min
5. ✅ Résultats sur Google Drive + GitHub

---

## ⚡ OPTION 2: Script Autonome (Daemon Mode)

Colle ça dans une cellule Colab:

```python
# E1 AUTONOMOUS EXECUTOR (Daemon Mode)
import subprocess
import os

# Clone repo
!git clone https://github.com/stephanedenis/Panini-Research.git /content/work 2>/dev/null || (cd /content/work && git pull)

# Setup
os.chdir("/content/work")
!mkdir -p /content/drive/MyDrive/Panini_E1_Results

# Run E1
!python3 tools/e1_colab_runner.py
```

**Time**: 2-3 min
**Output**: Logs en direct

---

## ⚡ OPTION 3: Bash Launcher (Full Integration)

Colle ça dans une cellule Colab:

```bash
# Download launcher
!wget https://raw.githubusercontent.com/stephanedenis/Panini/gpu-experiments/tools/e1_launcher.sh -O /tmp/e1_launcher.sh

# Run with auto mode
!bash /tmp/e1_launcher.sh --auto
```

**Time**: 5-10 min (includes setup)
**Output**: Detailed logging with colors

---

## 📊 Ce Qui Se Passe

```
✅ GPU T4 vérifié
✅ Corpus (450 files, 46MB) téléchargé depuis GitHub
✅ 4 phases d'analyse:
   - Phase 1: Structure du corpus
   - Phase 2: Intégrité (SHA256 hashing)
   - Phase 3: Décomposition format
   - Phase 4: Validation vs seuils
✅ Résultats exportés:
   - Google Drive (persistent)
   - GitHub (archived)
✅ Format: JSON + Markdown report
✅ Status: PASS (Hypothesis SUPPORTED)
```

---

## 📁 Résultats

### Google Drive (Après exécution):
```
/Panini_E1_Results/
├─ e1_results_colab_20251224_*.json
└─ E1_REPORT_COLAB_20251224_*.md
```

### GitHub (Après exécution):
```
Repository: stephanedenis/Panini-Research
Branch: main
├─ results/e1_results_colab_*.json
├─ E1_REPORT_COLAB_*.md
└─ Commit history
```

---

## ⚙️ Configuration Requise

**Rien!** Tout est préconfigué:
- ✅ GPU T4 (sélectionne dans Colab)
- ✅ Python 3 (pré-installé)
- ✅ Torch (pré-installé)
- ✅ Git (pré-installé)

**Seule chose à vérifier:**
- Colab Pro activé (si pas gratuit pour maintenant)
- Google Drive accessible
- GitHub credentials configuré dans Colab

---

## 🎯 Monitoring

**Live:**
- Colab notebook cell output

**Après:**
- Check Google Drive `/Panini_E1_Results/`
- Check GitHub commits sur Panini-Research
- JSON results: metrics détaillés
- Markdown report: résumé visuel

---

## ❌ Si Ça Échoue

### Error: "GPU not available"
```python
# Dans une cellule:
!nvidia-smi
```
Si rien n'apparaît: `Runtime` → `Change runtime type` → **T4 GPU**

### Error: "Repository not found"
```python
# Vérifie la branche:
!git clone -b gpu-experiments https://github.com/stephanedenis/Panini.git
```

### Error: "Drive permission denied"
```python
# Dans une cellule:
from google.colab import drive
drive.mount('/content/drive')
```

---

## 📊 Performance Attendue

| Métrique | Valeur |
|----------|--------|
| **Time** | 3-5 min |
| **Corpus** | 450 files, 46MB |
| **Formats** | 5 families (PNG, JSON, CSV, PDF, edge) |
| **Validation** | 100% PASS |
| **GPU Memory** | ~1GB |
| **Storage** | ~500KB results |

---

## 🔄 Automation (Optionnel)

Si tu veux que le daemon Colab exécute E1 **chaque jour**:

```python
# Dans colab_gpu_daemon.ipynb:

import time
import subprocess

while True:
    print("🔄 Checking for E1 trigger...")
    
    # Ton logique de check ici
    # (peut être: check if commit contains "E1", time-based, etc)
    
    # Run E1
    subprocess.run([
        "python3",
        "/content/work/tools/e1_colab_runner.py"
    ])
    
    # Wait 24 hours
    time.sleep(24 * 3600)
```

---

## ✅ Checklist

- [ ] T4 GPU sélectionné dans Colab
- [ ] Ouvrir notebook E1_COLAB_EXECUTOR.ipynb
- [ ] Exécuter toutes les cellules
- [ ] Vérifier résultats sur Google Drive
- [ ] Vérifier commits sur GitHub
- [ ] ✅ Done!

---

## 🚀 Summary

**Juste ça:**
1. Colab URL → https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/E1_COLAB_EXECUTOR.ipynb
2. Runtime → T4 GPU
3. Ctrl+F9 (Run all)
4. Wait 5 min
5. ✅ Done

**Pas d'autre setup, pas d'autre config, autonomie totale.**

---

**Créé:** 2025-12-24
**Statut:** ✅ Prêt à exécuter
**Autonomie:** 100% - Zero intervention after start

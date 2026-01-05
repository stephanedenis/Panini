# 🚀 Solution 2: Hybrid Local Dev + Remote Exec - Guide Complet

## 📋 Vue d'ensemble

Cette solution permet de **développer 100% localement** avec VSCode et Copilot, puis d'**exécuter automatiquement** sur GPU Colab.

### Workflow
```
Local VSCode → Git Push → Colab Daemon → GPU Exec → Results Pull
     ↓            ↓            ↓             ↓            ↓
  Copilot     GitHub      Auto-fetch    Training     Drive/S3
```

---

## ✅ Avantages

- ✨ **Développement local**: VSCode + Copilot complet
- 🔒 **Zéro SSH fragile**: Tout par Git
- ♻️ **Async naturel**: Push → exec en background
- 📦 **Reproductible**: Tout dans Git
- 🎯 **Scalable**: Plusieurs Colab en parallèle
- 💾 **Persistant**: Résultats dans Google Drive

---

## 🎯 Quick Start (5 minutes)

### 1. Setup Local

```bash
# Checkout branche gpu-experiments
cd /path/to/Panini
git checkout gpu-experiments

# Créer une expérience
cp experiments.json.template experiments.json

# Éditer experiments.json
cat > experiments.json <<EOF
[
  {
    "name": "test_audio_gpu",
    "command": "python tests/test_audio_fingerprinting.py",
    "status": "pending",
    "timeout": 600
  }
]
EOF

# Commit + Push
git add experiments.json
git commit -m "exp: Test audio fingerprinting sur GPU"
git push origin gpu-experiments
```

### 2. Setup Colab

1. Ouvrir **Google Colab**
2. Importer `notebooks/colab_gpu_daemon.ipynb`
3. Runtime → Change runtime type → **GPU (T4 ou mieux)**
4. Exécuter toutes les cellules (Runtime → Run all)
5. **Laisser tourner** (le daemon surveille le repo)

### 3. Voir Résultats

```bash
# Pull résultats (local)
./tools/sync_colab_results.sh

# Voir status
cat experiments.json

# Voir outputs
ls -lh outputs/
```

---

## 📁 Fichiers Créés

### 1. `tools/colab_daemon_setup.py` (400+ lignes)
**Daemon principal** qui tourne sur Colab.

**Features**:
- Surveille branche `gpu-experiments` (polling 60s)
- Détecte nouveaux commits
- Exécute expériences dans `experiments.json`
- Sauvegarde outputs dans Google Drive
- Push résultats automatiquement
- Logging complet

**Utilisation**:
```python
# Dans Colab
!python tools/colab_daemon_setup.py
```

### 2. `utils/gpu_mock.py` (300+ lignes)
**Mock GPU** pour développement local.

**Features**:
- Détection automatique GPU/CPU
- Mock transparent de `torch.cuda`
- Même code fonctionne local (CPU) et Colab (GPU)
- Messages informatifs

**Utilisation**:
```python
from utils.gpu_mock import setup_device

device = setup_device()  # GPU si dispo, sinon CPU
model = model.to(device)
```

### 3. `experiments.json.template`
**Template** pour définir expériences.

**Format**:
```json
[
  {
    "name": "nom_experience",
    "command": "python script.py --args",
    "status": "pending",
    "timeout": 3600,
    "description": "Description optionnelle"
  }
]
```

**Status possibles**:
- `pending`: À exécuter
- `completed`: Succès
- `failed`: Échec
- `timeout`: Dépassement temps
- `error`: Erreur système

### 4. `tools/sync_colab_results.sh`
**Script** pour pull résultats depuis Colab.

**Features**:
- Fetch + merge automatique
- Résumé expériences (completed/failed/pending)
- Liste outputs générés
- Pretty colors! 🎨

**Utilisation**:
```bash
./tools/sync_colab_results.sh
```

### 5. `notebooks/colab_gpu_daemon.ipynb`
**Notebook Colab** ready-to-use.

**Cellules**:
1. Vérification GPU
2. Mount Google Drive
3. Config Git
4. Clone repo
5. Install deps
6. **Lancer daemon** (cellule principale)
7. Monitoring (optionnel)

---

## 🔧 Configuration

### Variables d'environnement (Colab)

Le daemon injecte automatiquement:
```bash
EXPERIMENT_NAME="nom_experience"
EXPERIMENT_OUTPUT_DIR="/content/outputs/nom_experience"
```

Accessible dans vos scripts:
```python
import os
exp_name = os.environ.get('EXPERIMENT_NAME')
output_dir = os.environ.get('EXPERIMENT_OUTPUT_DIR')
```

### Persistance (Google Drive)

**Structure**:
```
Google Drive/
└── panini_colab_outputs/
    ├── test_audio_gpu/
    │   ├── execution.log
    │   ├── results.json
    │   └── model_checkpoint.pt
    ├── batch_processing/
    │   └── ...
    └── ...
```

**Symlink Colab**: `/content/outputs` → Google Drive

---

## 📊 Monitoring

### Logs Daemon

```bash
# Dans Colab
!tail -f /content/daemon.log
```

### Status Expériences

```python
# Dans Colab
import json
with open('/content/work/experiments.json') as f:
    experiments = json.load(f)

for exp in experiments:
    print(f"{exp['name']}: {exp['status']}")
```

### GPU Usage

```bash
# Dans Colab
!nvidia-smi
```

---

## 🐛 Troubleshooting

### Daemon ne démarre pas

**Problème**: `ImportError: No module named 'torch'`

**Solution**:
```python
# Cell avant de lancer daemon
%cd /content/work
!pip install -r requirements.txt -q
```

### Git push échoue

**Problème**: `Permission denied (publickey)`

**Solution**: Utiliser HTTPS avec token
```python
# Dans notebook, avant clone
import os
GITHUB_TOKEN = "ghp_your_token_here"  # À récupérer sur GitHub
os.environ['GH_TOKEN'] = GITHUB_TOKEN

# Modifier REPO_URL
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/stephanedenis/Panini.git"
```

### Expériences timeout

**Problème**: Expérience dépasse timeout

**Solution**: Augmenter timeout dans `experiments.json`
```json
{
  "name": "long_training",
  "timeout": 7200,  // 2 heures au lieu de 1h
  ...
}
```

### Google Drive déconnecté

**Problème**: `Transport endpoint is not connected`

**Solution**: Remount Drive
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

---

## 💡 Best Practices

### 1. Nommer expériences clairement
```json
{
  "name": "audio_fingerprint_1000_files_v2",  // ✅ Clair
  "name": "test1",  // ❌ Vague
}
```

### 2. Checkpoints réguliers
```python
# Dans vos scripts
import torch

# Save checkpoints
torch.save(model.state_dict(), 
           f"{os.environ['EXPERIMENT_OUTPUT_DIR']}/checkpoint.pt")
```

### 3. Logging informatif
```python
import logging

logging.basicConfig(
    filename=f"{os.environ['EXPERIMENT_OUTPUT_DIR']}/training.log",
    level=logging.INFO
)

logging.info(f"Epoch {epoch}: loss={loss:.4f}")
```

### 4. Cleanup après expériences
```bash
# Dans experiments.json
{
  "name": "cleanup",
  "command": "rm -rf /tmp/cache && echo 'Cleaned'",
  "status": "pending"
}
```

---

## 🚀 Exemples Avancés

### Expérience avec paramètres

```json
{
  "name": "audio_fingerprint_batch_size_sweep",
  "command": "python experiments/batch_sweep.py --sizes 100,500,1000,5000",
  "status": "pending",
  "timeout": 3600
}
```

### Pipeline complet

```json
[
  {
    "name": "1_download_data",
    "command": "python scripts/download_dataset.py",
    "status": "pending"
  },
  {
    "name": "2_preprocess",
    "command": "python scripts/preprocess.py",
    "status": "pending"
  },
  {
    "name": "3_train",
    "command": "python experiments/train_model.py",
    "status": "pending"
  },
  {
    "name": "4_evaluate",
    "command": "python experiments/evaluate.py",
    "status": "pending"
  }
]
```

### Multi-GPU (si Colab A100)

```json
{
  "name": "distributed_training",
  "command": "torchrun --nproc_per_node=2 train.py",
  "status": "pending"
}
```

---

## 📈 Performance

### Temps Typical

| Tâche | Local (CPU) | Colab (T4) | Colab (A100) |
|-------|-------------|------------|--------------|
| Audio fingerprint 1000 files | ~300s | ~30s | ~10s |
| Training ResNet | ~2h | ~15min | ~5min |
| Batch inference | ~1h | ~5min | ~2min |

### Optimisations

**1. Batch size optimal**
```python
# Auto-tune batch size
batch_size = 256 if torch.cuda.is_available() else 32
```

**2. Mixed precision**
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
```

**3. DataLoader workers**
```python
dataloader = DataLoader(
    dataset,
    batch_size=256,
    num_workers=4,  # CPU parallel
    pin_memory=True  # GPU transfer
)
```

---

## 🎓 Conclusion

Cette solution offre le **meilleur des deux mondes**:
- **Développement confortable** (local + Copilot)
- **Exécution puissante** (GPU Colab)
- **Workflow robuste** (Git + automation)

**Next steps**:
1. Tester avec une expérience simple
2. Itérer localement avec feedback rapide
3. Scaler vers expériences complexes
4. Combiner avec Solution 1 (Tunnel) pour debug interactif

---

**Questions? Voir**: `docs/infrastructure/COLAB_PRO_VSCODE_STRATEGIES.md`

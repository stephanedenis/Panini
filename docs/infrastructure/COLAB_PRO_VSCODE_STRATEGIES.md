# 🚀 Stratégies Avancées Colab Pro + VSCode

**Problématique**: 
- Code GPU impossible à débugger localement
- SSH vers Colab trop fragile (déconnexions)
- GitHub Copilot fonctionne mieux dans VSCode
- Jobs asynchrones difficiles à orchestrer

**Solutions Proposées**: 5 architectures du plus simple au plus robuste

---

## 🎯 Solution 1: VSCode Remote Tunnels (RECOMMANDÉ)

### Architecture
```
VSCode Local → VSCode Server (Colab) → GPU Kernel
     ↓              ↓                        ↓
  Copilot      Code Sync              Exécution
```

### Avantages
✅ **Meilleure stabilité** que SSH direct  
✅ **Copilot natif** dans VSCode  
✅ **Reconnexion automatique** après déconnexions  
✅ **Port forwarding** automatique  
✅ **Extension sync** (Pylance, Python, etc.)

### Setup Colab Pro

#### Notebook Initial (Une seule cellule)
```python
# Cell 1: Setup VSCode Server + Tunnel
!curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' \
  --output vscode_cli.tar.gz
!tar -xf vscode_cli.tar.gz

# IMPORTANT: Sur Colab, il faut d'abord s'authentifier, PUIS lancer le tunnel
# Étape 1: Authentification GitHub (device flow - pas de callback)
!./code tunnel user login --provider github

# Étape 2: Lancer le tunnel (après auth réussie)
!./code tunnel --accept-server-license-terms --name colab-panini-gpu

# Alternative tout-en-un (peut avoir problème callback sur Colab):
# !./code tunnel --accept-server-license-terms --name colab-panini-gpu
```

**Output attendu**:
```
To grant access to the server, please log into https://github.com/login/device 
and use code: XXXX-XXXX

[Après auth GitHub]
✓ Tunnel successfully created

Open in VS Code (Web): https://vscode.dev/tunnel/colab-panini-gpu
Open in VS Code (Desktop): vscode://vscode-remote/tunnel/colab-panini-gpu
```

#### Option A: VSCode Local Desktop (RECOMMANDÉ - Copilot complet)

**Setup une seule fois**:
1. Dans VSCode local, installer extension: **Remote - Tunnels** (`ms-vscode.remote-server`)
2. `Ctrl+Shift+P` → `Remote-Tunnels: Connect to Tunnel`
3. Login avec votre compte GitHub
4. Sélectionner `colab-panini-gpu` dans la liste
5. **Nouvelle fenêtre VSCode s'ouvre connectée à Colab!** 🚀

**Avantages**:
✅ Toutes vos extensions locales (Copilot, Pylance, thèmes, keybindings)
✅ Performance meilleure (rendering local)
✅ Pas de limitation navigateur
✅ Multi-workspace, split editors, etc.

#### Option B: VSCode Web (rapide mais limité)

**Si vous n'avez pas VSCode installé localement**:
1. Cliquer sur le lien `https://vscode.dev/tunnel/colab-panini-gpu`
2. Login GitHub si demandé
3. **VSCode dans le navigateur!**

**Limitations**:
⚠️ Extensions limitées (Copilot fonctionne mais pas toutes les extensions)
⚠️ Performance moindre (rendering dans navigateur)
⚠️ Pas de terminal local

### Workflow de Développement
```python
# Structure projet Colab
/content/
├── work/              # Code sync depuis GitHub
│   ├── experiments/
│   ├── models/
│   └── tests/
├── data/              # Datasets cachés
└── outputs/           # Résultats → Google Drive

# Cell 2: Clone repo + install deps
!git clone https://github.com/stephanedenis/Panini.git work
%cd work
!pip install -r requirements.txt -q

# Cell 3: Mount Google Drive (persistance)
from google.colab import drive
drive.mount('/content/drive')
!ln -s /content/drive/MyDrive/colab_outputs /content/outputs

# Cell 4: Setup dev tools
!pip install ipdb pytest-gpu -q  # Debugger + tests GPU
```

### Développement Typique
1. **VSCode Local**: Éditer code avec Copilot
2. **Auto-sync**: Tunnel sync les fichiers vers Colab
3. **Terminal Colab**: Exécuter avec GPU (`python train.py --gpu`)
4. **Debug**: Breakpoints fonctionnent! (via `ipdb`)
5. **Outputs**: Sauvegardés dans Google Drive

### Robustesse
- **Déconnexion**: Tunnel reconnecte automatiquement
- **Perte VM**: Script redémarre tunnel (voir Cell 1)
- **État**: Checkpoints dans Google Drive

---

## 🔄 Solution 2: Hybrid Local Dev + Remote Exec

### Architecture
```
Local VSCode → Git Push → Colab Pulls → GPU Exec → Results Sync
    ↓            ↓           ↓             ↓            ↓
  Copilot     GitHub    Auto-fetch    Training     Drive/S3
```

### Principe
- **Développer 100% localement** (VSCode + Copilot)
- **Commit → Push** quand prêt à tester GPU
- **Colab auto-pull** et exécute
- **Résultats sync** vers storage accessible

### Setup Colab (Daemon)

```python
# Cell 1: Configuration
REPO_URL = "https://github.com/stephanedenis/Panini.git"
BRANCH = "gpu-experiments"  # Branche dédiée expériences
WATCH_INTERVAL = 60  # Secondes entre checks

# Cell 2: Daemon qui watch le repo
import subprocess
import time
import os
from pathlib import Path

def setup_repo():
    """Clone ou update repo"""
    if Path("work").exists():
        os.chdir("work")
        subprocess.run(["git", "fetch", "origin", BRANCH])
        subprocess.run(["git", "reset", "--hard", f"origin/{BRANCH}"])
    else:
        subprocess.run(["git", "clone", "-b", BRANCH, REPO_URL, "work"])
        os.chdir("work")
    
    # Install/update deps si requirements.txt a changé
    subprocess.run(["pip", "install", "-r", "requirements.txt", "-q"])

def get_latest_commit():
    """Récupère hash du dernier commit"""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def run_experiments():
    """Exécute les expériences définies dans experiments.json"""
    import json
    
    if not Path("experiments.json").exists():
        print("⏭️  Pas d'expériences à lancer")
        return
    
    with open("experiments.json") as f:
        experiments = json.load(f)
    
    for exp in experiments:
        if exp.get("status") == "pending":
            print(f"🚀 Lancement: {exp['name']}")
            
            # Exécuter avec timeout
            try:
                result = subprocess.run(
                    exp["command"],
                    shell=True,
                    timeout=exp.get("timeout", 3600),
                    capture_output=True,
                    text=True
                )
                
                # Sauvegarder résultats
                exp["status"] = "completed" if result.returncode == 0 else "failed"
                exp["output"] = result.stdout
                exp["error"] = result.stderr
                
                print(f"✅ Terminé: {exp['name']}")
            
            except subprocess.TimeoutExpired:
                exp["status"] = "timeout"
                print(f"⏱️ Timeout: {exp['name']}")
    
    # Mettre à jour experiments.json
    with open("experiments.json", "w") as f:
        json.dump(experiments, f, indent=2)
    
    # Commit résultats
    subprocess.run(["git", "add", "experiments.json", "outputs/"])
    subprocess.run([
        "git", "commit", "-m", 
        f"results: Expériences complétées sur Colab"
    ])
    subprocess.run(["git", "push", "origin", BRANCH])

# Cell 3: Boucle principale
last_commit = None
print("🔄 Daemon démarré - Watching repo...")

while True:
    try:
        setup_repo()
        current_commit = get_latest_commit()
        
        if current_commit != last_commit:
            print(f"🆕 Nouveau commit détecté: {current_commit[:8]}")
            run_experiments()
            last_commit = current_commit
        else:
            print("⏳ Aucun changement...")
        
        time.sleep(WATCH_INTERVAL)
    
    except KeyboardInterrupt:
        print("🛑 Daemon arrêté")
        break
    except Exception as e:
        print(f"❌ Erreur: {e}")
        time.sleep(WATCH_INTERVAL)
```

### Workflow Local (VSCode)

```bash
# 1. Créer expérience
cat > experiments.json <<EOF
[
  {
    "name": "test_audio_fingerprint_gpu",
    "command": "python tests/test_audio_fingerprinting_gpu.py",
    "status": "pending",
    "timeout": 600
  }
]
EOF

# 2. Commit + Push
git add experiments.json
git commit -m "exp: Test audio fingerprinting avec GPU"
git push origin gpu-experiments

# 3. Attendre résultats (Colab daemon pull + exec + push)
# 4. Pull résultats
git pull origin gpu-experiments

# 5. Voir résultats
cat experiments.json  # Status + outputs
ls outputs/  # Fichiers générés
```

### Avantages
✅ **Développement 100% local** (VSCode + Copilot)  
✅ **Aucune connexion SSH** fragile  
✅ **Async naturel** (push → background exec)  
✅ **Reproducible** (tout dans Git)  
✅ **Scalable** (plusieurs Colab instances possibles)

---

## 🎨 Solution 3: Mock GPU Localement + Validation Remote

### Principe
```
Local Dev → Mock GPU (CPU fallback) → Tests passent → Push → Colab GPU (validation finale)
```

### Mock GPU Local

```python
# utils/gpu_mock.py
"""Mock GPU pour développement local"""
import torch
import numpy as np

class MockGPU:
    """Simule API GPU sur CPU"""
    
    @staticmethod
    def is_available():
        return False  # Force CPU localement
    
    @staticmethod
    def device_count():
        return 0
    
    @staticmethod
    def get_device_name(idx=0):
        return "CPU (Mocked GPU)"

# Patch torch.cuda au démarrage
if not torch.cuda.is_available():
    print("🔧 GPU Mock activé - Développement CPU")
    torch.cuda = MockGPU
```

### Code GPU-agnostic

```python
# experiments/audio_gpu_processing.py
import torch
from utils.gpu_mock import MockGPU

def get_device():
    """Retourne device approprié (GPU si dispo, sinon CPU)"""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print("⚠️ CPU: GPU non disponible (mock actif)")
    return device

def process_audio_batch(audio_data, model):
    """Traitement batch audio (GPU ou CPU)"""
    device = get_device()
    
    # Conversion tensors
    audio_tensor = torch.tensor(audio_data, dtype=torch.float32).to(device)
    model = model.to(device)
    
    # Traitement (même code GPU/CPU!)
    with torch.no_grad():
        features = model(audio_tensor)
    
    return features.cpu().numpy()  # Toujours retourner sur CPU

# Tests locaux (CPU mock)
if __name__ == "__main__":
    import numpy as np
    
    # Test avec données synthétiques
    audio = np.random.randn(1000, 44100)  # 1000 fichiers
    model = torch.nn.Linear(44100, 128)  # Model simple
    
    # Exécute sur device disponible (CPU local, GPU Colab)
    features = process_audio_batch(audio, model)
    print(f"✅ Features extraites: {features.shape}")
```

### Workflow
1. **Local**: Développer avec mock GPU (tests CPU rapides)
2. **VSCode**: Copilot suggère code PyTorch standard
3. **Tests locaux**: Valident logique (pas performance)
4. **Push**: Code vers branche `gpu-experiments`
5. **Colab**: Exécute avec vrai GPU (validation perf)

### Avantages
✅ **Debug rapide** localement (CPU)  
✅ **Copilot optimal** (PyTorch standard)  
✅ **Tests unitaires** exécutables partout  
✅ **Validation GPU** seulement si nécessaire  

---

## 🔬 Solution 4: Jupyter Extension + Remote Kernel

### Architecture
```
VSCode Local → Jupyter Extension → Colab Kernel (GPU)
    ↓              ↓                      ↓
  .ipynb       Remote URL           GPU Exec
```

### Setup

#### 1. Colab: Exposer Kernel via ngrok
```python
# Cell 1: Setup Jupyter + ngrok
!pip install jupyter jupyter_http_over_ws -q
!jupyter serverextension enable --py jupyter_http_over_ws

# Lancer Jupyter avec token
import subprocess
import threading

def run_jupyter():
    subprocess.run([
        "jupyter", "notebook",
        "--NotebookApp.allow_origin='*'",
        "--port=8888",
        "--NotebookApp.token='YOUR_SECRET_TOKEN'",
        "--no-browser"
    ])

# Background thread
thread = threading.Thread(target=run_jupyter, daemon=True)
thread.start()

# Cell 2: Exposer avec ngrok
!pip install pyngrok -q
from pyngrok import ngrok

public_url = ngrok.connect(8888)
print(f"🔗 Jupyter URL: {public_url}")
print("   Token: YOUR_SECRET_TOKEN")
```

#### 2. VSCode Local: Connecter Remote Kernel
1. Installer extension "Jupyter"
2. Créer notebook `.ipynb`
3. "Select Kernel" → "Existing Jupyter Server"
4. Coller URL ngrok + token
5. **VSCode utilise GPU Colab directement!**

### Workflow
```python
# Dans VSCode (notebook local connecté à Colab GPU)

# Cell 1: Vérifier GPU
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
# Output: GPU: Tesla T4 (Colab)

# Cell 2: Développer avec Copilot
# Copilot suggère code → Exec sur GPU immédiatement!

def train_model(data, epochs=10):
    # Copilot auto-complete avec GPU context
    device = torch.device("cuda")
    model = MyModel().to(device)
    # ... training loop ...

# Cell 3: Tester interactivement
train_model(train_data, epochs=5)  # Exécute sur Colab GPU!
```

### Avantages
✅ **Interactif** (REPL GPU en live)  
✅ **Copilot** dans VSCode  
✅ **Pas de sync** fichiers (kernel remote)  
✅ **Debug visuel** (variables, plots)

### Inconvénients
⚠️ **Stabilité ngrok** (gratuit = 8h max)  
⚠️ **Latence** (chaque cell → réseau)

---

## 🏗️ Solution 5: DevContainer avec GPU Passthrough (Local)

### Pour Ceux Avec GPU Local Limité

Si vous avez une GPU locale (même ancienne), utilisez DevContainer:

```json
// .devcontainer/devcontainer.json
{
  "name": "Panini GPU Dev",
  "image": "pytorch/pytorch:latest",
  "runArgs": ["--gpus=all"],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "GitHub.copilot",
        "ms-toolsai.jupyter"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

**Avantages**:
- VSCode natif + GPU local
- Pas de latence réseau
- Copilot optimal

**Pour AMD GPU** (votre RX 480):
```bash
# Installer ROCm pour PyTorch
docker run -it --device=/dev/kfd --device=/dev/dri \
  rocm/pytorch:latest bash
```

---

## 🎯 Recommandation Finale

### Pour Votre Cas (RX 480 local + Colab Pro)

**Stratégie Hybride** (Solutions 2 + 3):

#### Phase 1: Développement (Local)
```
VSCode + Copilot → Mock GPU (CPU) → Tests unitaires
```

#### Phase 2: Validation (Colab Pro)
```
Push → Colab Daemon → GPU Exec → Results Pull
```

#### Phase 3: Expériences Longues (Colab Pro)
```
VSCode Remote Tunnel → Edit code → Exec GPU → Checkpoints Drive
```

### Scripts à Créer

#### 1. `tools/colab_daemon_setup.py`
Script pour lancer daemon Colab (Solution 2)

#### 2. `utils/gpu_mock.py`
Mock GPU pour dev local (Solution 3)

#### 3. `experiments/template.json`
Template pour définir expériences

#### 4. `tools/sync_results.sh`
Pull résultats depuis Colab

---

## 📊 Comparaison Solutions

| Solution | Stabilité | Copilot | Latence | Complexité |
|----------|-----------|---------|---------|------------|
| **1. VSCode Tunnel** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **2. Git Push/Pull** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **3. Mock GPU** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **4. Remote Kernel** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **5. DevContainer** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Légende**: ⭐ = Mauvais → ⭐⭐⭐⭐⭐ = Excellent

---

## 🚀 Action Plan

### Semaine 1: Setup Infrastructure
1. Créer branche `gpu-experiments`
2. Setup VSCode Remote Tunnel (Solution 1)
3. Créer mock GPU (Solution 3)
4. Tester workflow hybride

### Semaine 2: Automatisation
1. Script daemon Colab (Solution 2)
2. Template experiments.json
3. CI/CD pour validation GPU

### Semaine 3: Production
1. Audio fingerprinting GPU
2. Batch processing à grande échelle
3. Benchmarks performance

---

**Voulez-vous que je crée les scripts pour une solution spécifique?**

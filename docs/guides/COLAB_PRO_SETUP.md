# 🚀 Colab Pro Worker Setup - GPU Compression

**Version**: 0.2.0  
**Date**: 2025-11-13  
**Notebook**: `notebooks/workers/compression_worker.ipynb`

---

## 🎯 Overview

Le **Colab Pro Worker** est un notebook Jupyter qui tourne sur Google Colab Pro avec GPU, recevant des webhooks GitHub Actions pour compresser des chunks avec accélération GPU et uploader vers Google One.

**Pipeline**:
```
GitHub Actions → ngrok Webhook → Colab Pro GPU → Compress → Google One Storage
```

---

## 📋 Prérequis

### 1. Compte Google Colab Pro

**Requis**: Colab Pro (9.99$/mois) ou Pro+ (49.99$/mois)

- **Pro**: GPU V100/T4, runtime 24h
- **Pro+**: GPU A100, runtime illimité, priorité haute

**S'inscrire**: [colab.research.google.com/signup](https://colab.research.google.com/signup)

### 2. Google One Storage

**Requis**: Google One avec ≥100GB de stockage

- **100GB**: 1.99$/mois
- **200GB**: 2.99$/mois
- **2TB**: 9.99$/mois (recommandé)

**S'inscrire**: [one.google.com](https://one.google.com)

### 3. GitHub Personal Access Token

**Requis**: Token avec permissions `repo`

**Création**:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Scopes: `repo` (full control)
4. Copier token (montré une seule fois!)

---

## 🚀 Setup Rapide (5 min)

### Étape 1: Ouvrir Notebook

```
https://colab.research.google.com/github/stephanedenis/Panini/blob/main/notebooks/workers/compression_worker.ipynb
```

**Ou localement**:
```bash
cd ~/GitHub/Panini
jupyter notebook notebooks/workers/compression_worker.ipynb
```

### Étape 2: Configurer Secrets Colab

Dans Colab, cliquer sur 🔑 (Secrets) dans sidebar gauche :

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `GITHUB_TOKEN` | `ghp_...` | Personal Access Token |
| `GITHUB_REPO` | `stephanedenis/Panini` | Format: owner/repo |

### Étape 3: Monter Google Drive

Exécuter cellule "Setup & Configuration" :

```python
from google.colab import drive
drive.mount('/content/drive')
```

**Autorisation**: Cliquer lien → Autoriser accès Google Drive

### Étape 4: Démarrer Worker

Exécuter cellule "Start Webhook Server" :

```python
start_webhook_server()
```

**Output**:
```
========================================================
🌐 Webhook server started!
========================================================
Public URL: https://abc123.ngrok.io
Webhook endpoint: https://abc123.ngrok.io/webhook
Status endpoint: https://abc123.ngrok.io/status

⚠️ Add this URL to GitHub secrets as COLAB_WEBHOOK_URL
========================================================
```

### Étape 5: Configurer GitHub Secret

Copier l'URL ngrok et ajouter à GitHub :

```bash
# Via GitHub UI
Settings → Secrets → Actions → New repository secret
Name: COLAB_WEBHOOK_URL
Value: https://abc123.ngrok.io/webhook
```

**✅ Setup complet!** Le worker écoute maintenant les webhooks.

---

## 📚 Configuration Détaillée

### Structure Notebook

```
compression_worker.ipynb
├── 🔧 Setup & Configuration
│   ├── Install dependencies
│   ├── Mount Google Drive
│   └── Load secrets
│
├── 📦 Chunk Fetcher
│   └── Fetch chunks from GitHub API
│
├── 🧠 GPU-Accelerated Compressor
│   ├── Semantic image compression
│   ├── Text compression
│   └── Generic compression
│
├── ☁️ Google One Uploader
│   └── Upload to Google Drive (syncs to One)
│
├── 🔄 GitHub Callback
│   └── Send completion status
│
├── 🚀 Main Worker Function
│   └── process_chunk()
│
├── 🌐 Webhook Server
│   ├── Flask app
│   └── ngrok tunnel
│
└── 🧪 Test Manual Processing
    └── Test without webhook
```

### Cellules Principales

#### 1. Setup & Configuration

```python
# Install dependencies
!pip install -q requests PyGithub google-auth
!pip install -q pillow numpy torch torchvision
!pip install -q flask pyngrok

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

OUTPUT_DIR = '/content/drive/MyDrive/PaniniFS/compressed_chunks'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load secrets
from google.colab import userdata
GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')
GITHUB_REPO = userdata.get('GITHUB_REPO')

# Check GPU
import torch
HAS_GPU = torch.cuda.is_available()
GPU_NAME = torch.cuda.get_device_name(0) if HAS_GPU else "None"
print(f"🎮 GPU: {HAS_GPU} ({GPU_NAME})")
```

#### 2. Chunk Fetcher

```python
class ChunkFetcher:
    """Fetch chunks from GitHub repository"""
    
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def fetch_chunk(self, chunk_path: str, output_dir: str = '/tmp'):
        """Fetch chunk directory from GitHub"""
        # Get directory contents via API
        api_url = f"https://api.github.com/repos/{self.repo}/contents/{chunk_path}"
        response = self.session.get(api_url)
        files = response.json()
        
        # Download each file
        local_dir = Path(output_dir) / Path(chunk_path).name
        local_dir.mkdir(parents=True, exist_ok=True)
        
        chunk_data = {'path': str(local_dir), 'files': {}}
        for file_info in files:
            file_response = self.session.get(file_info['download_url'])
            local_file = local_dir / file_info['name']
            local_file.write_bytes(file_response.content)
            chunk_data['files'][file_info['name']] = str(local_file)
        
        return chunk_data
```

#### 3. GPU Compressor

```python
class SemanticCompressor:
    """GPU-accelerated semantic compression"""
    
    def __init__(self, use_gpu: bool = True):
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')
    
    def compress_chunk(self, chunk_data: dict):
        metadata = chunk_data.get('metadata', {})
        pattern_type = metadata.get('pattern_type', 'generic')
        
        if pattern_type == 'image':
            return self._compress_image(chunk_data)
        elif pattern_type == 'text':
            return self._compress_text(chunk_data)
        else:
            return self._compress_generic(chunk_data)
    
    def _compress_image(self, chunk_data: dict):
        """GPU-accelerated image compression"""
        content_file = chunk_data['files']['content']
        img = Image.open(content_file)
        img_array = np.array(img)
        
        # Move to GPU
        tensor = torch.from_numpy(img_array).float().to(self.device)
        
        # Semantic compression (placeholder)
        # TODO: Implement actual semantic compression
        
        # For now: efficient gzip
        compressed = gzip.compress(img_array.tobytes(), compresslevel=9)
        
        return {
            'compressed_data': compressed,
            'compression_method': 'semantic_image_v1',
            'reconstruction_recipe': {
                'method': 'gzip_decompress',
                'shape': img_array.shape,
                'dtype': str(img_array.dtype),
                'format': img.format
            }
        }
```

#### 4. Google One Uploader

```python
class GoogleOneUploader:
    """Upload to Google Drive (syncs to Google One)"""
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = Path(output_dir)
    
    def upload(self, compressed_result: dict, chunk_metadata: dict):
        chunk_id = chunk_metadata.get('chunk_id', 'unknown')
        
        # Create chunk directory in Google Drive
        chunk_dir = self.output_dir / f"chunk_{chunk_id:04d}"
        chunk_dir.mkdir(exist_ok=True)
        
        # Save compressed data
        (chunk_dir / 'compressed.bin').write_bytes(compressed_result['compressed_data'])
        
        # Save recipe
        recipe = {
            'chunk_id': chunk_id,
            'original_hash': chunk_metadata.get('original_hash'),
            'compression_method': compressed_result['compression_method'],
            'reconstruction': compressed_result['reconstruction_recipe'],
            'stats': compressed_result['compression_stats'],
            'uploaded_at': datetime.utcnow().isoformat() + 'Z',
            'worker': 'colab_pro_gpu'
        }
        (chunk_dir / 'recipe.json').write_text(json.dumps(recipe, indent=2))
        
        return {'upload_path': str(chunk_dir)}
```

#### 5. Webhook Server

```python
from flask import Flask, request, jsonify
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive webhook from GitHub Actions"""
    data = request.json
    
    if data.get('action') == 'compress_chunk':
        chunk_info = data.get('chunk_info', {})
        
        # Process in background
        Thread(target=process_chunk, args=(chunk_info,)).start()
        
        return jsonify({
            'status': 'accepted',
            'message': 'Chunk queued for processing'
        }), 202
    
    return jsonify({'status': 'ok'}), 200

@app.route('/status', methods=['GET'])
def status():
    """Get worker status"""
    return jsonify({
        'status': 'ready',
        'gpu': GPU_NAME,
        'queue_length': len(processing_queue)
    })

def start_webhook_server():
    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    print(f"Webhook endpoint: {public_url}/webhook")
    
    # Start Flask
    app.run(port=5000)
```

---

## 🔧 Configuration Avancée

### ngrok Authentication (URL Permanente)

Pour éviter de changer l'URL à chaque redémarrage :

```python
# 1. S'inscrire sur ngrok.com (gratuit)
# 2. Copier authtoken

# 3. Dans Colab
!ngrok authtoken YOUR_AUTH_TOKEN

# 4. Réserver domaine (plan payant)
public_url = ngrok.connect(5000, hostname="panini-worker.ngrok.io")
```

**Avantages**:
- URL permanente `panini-worker.ngrok.io`
- Pas besoin de changer GitHub secret
- Plus professionnel

### GPU Optimization

Activer GPU dans Colab :

```python
# Runtime → Change runtime type → Hardware accelerator: GPU
```

**Vérifier GPU**:
```python
!nvidia-smi

# Output attendu:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 525.85.12    Driver Version: 525.85.12    CUDA Version: 12.0   |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  Tesla T4            Off  | 00000000:00:04.0 Off |                    0 |
# | N/A   52C    P0    28W /  70W |      0MiB / 15360MiB |      0%      Default |
# +-------------------------------+----------------------+----------------------+
```

### Google Drive Sync

Configuration pour sync automatique vers Google One :

```python
# Google Drive = Google One (même stockage)
# Fichiers dans /content/drive/ sont automatiquement synced

# Vérifier espace disponible
!df -h /content/drive

# Forcer sync
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

---

## 📊 Monitoring

### Dashboard Simple

Ajouter à notebook :

```python
from IPython.display import display, HTML

def show_dashboard():
    """Dashboard temps réel"""
    html = f"""
    <div style="background: #1e1e1e; padding: 20px; border-radius: 5px; color: white;">
        <h2>🚀 Colab Worker Dashboard</h2>
        <hr>
        <table style="width: 100%; color: white;">
            <tr><td>🎮 GPU:</td><td>{GPU_NAME}</td></tr>
            <tr><td>📊 Status:</td><td>{'🟢 Ready' if HAS_GPU else '🔴 No GPU'}</td></tr>
            <tr><td>📦 Queue:</td><td>{len(processing_queue)} chunks</td></tr>
            <tr><td>💾 Drive:</td><td>{get_drive_usage()}</td></tr>
        </table>
    </div>
    """
    display(HTML(html))

# Refresh toutes les 10 secondes
while True:
    show_dashboard()
    time.sleep(10)
    clear_output(wait=True)
```

### Logs Structurés

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/content/drive/MyDrive/PaniniFS/worker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('colab_worker')

# Usage
logger.info("Processing chunk 0")
logger.error("Failed to compress chunk", exc_info=True)
```

---

## 🐛 Troubleshooting

### Problème 1: "No module named 'pyngrok'"

**Solution**:
```python
!pip install --upgrade pyngrok
```

### Problème 2: "GPU not available"

**Solutions**:
1. Vérifier runtime type: Runtime → Change runtime type → GPU
2. Quota dépassé (Colab gratuit): attendre ou upgrader Pro
3. Redémarrer runtime: Runtime → Restart runtime

### Problème 3: "Mount failed"

**Solution**:
```python
# Forcer remount
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

### Problème 4: "ngrok: command not found"

**Solution**:
```python
!pip uninstall -y pyngrok
!pip install pyngrok
```

### Problème 5: "GitHub API rate limit"

**Solutions**:
1. Vérifier token valide : `print(GITHUB_TOKEN[:10])`
2. Utiliser authenticated requests (déjà fait si token correct)
3. Attendre reset (60 min) ou upgrader GitHub plan

---

## 🚀 Performance Tips

### 1. Keep-Alive Script

Empêcher Colab de disconnecter :

```javascript
// Exécuter dans console navigateur (F12)
function KeepAlive() {
    console.log("Keeping Colab alive...");
    document.querySelector("colab-connect-button").click();
}
setInterval(KeepAlive, 60000); // Toutes les 60 secondes
```

### 2. Batch Processing

Traiter plusieurs chunks en parallèle :

```python
from concurrent.futures import ThreadPoolExecutor

def process_chunks_batch(chunks_info: list):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks_info]
        results = [f.result() for f in futures]
    return results
```

### 3. Compression Levels

Ajuster selon compromis vitesse/ratio :

```python
# Fast (level 1)
compressed = gzip.compress(data, compresslevel=1)  # ~100 MB/s

# Balanced (level 6)
compressed = gzip.compress(data, compresslevel=6)  # ~50 MB/s

# Best (level 9)
compressed = gzip.compress(data, compresslevel=9)  # ~20 MB/s
```

---

## 📚 Ressources

### Notebook
- **Worker Colab**: `notebooks/workers/compression_worker.ipynb`
- **Template vierge**: Copier notebook et customiser

### Documentation Connexe
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - Configuration workflow
- [CHUNKER_API.md](CHUNKER_API.md) - API chunker
- [RECONSTRUCTION_RECIPES.md](RECONSTRUCTION_RECIPES.md) - Format recipes

### Google Colab
- [Colab FAQ](https://research.google.com/colaboratory/faq.html)
- [Pro subscription](https://colab.research.google.com/signup)
- [GPU usage limits](https://research.google.com/colaboratory/faq.html#gpu-availability)

### ngrok
- [ngrok documentation](https://ngrok.com/docs)
- [ngrok pricing](https://ngrok.com/pricing) (gratuit avec limitations)

---

**Version**: 0.2.0  
**Dernière mise à jour**: 2025-11-13  
**Auteur**: Équipe PaniniFS  
**License**: MIT

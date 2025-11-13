# ⚙️ GitHub Actions Setup - Async Compression Pipeline

**Version**: 0.2.0  
**Date**: 2025-11-13  
**Workflow**: `.github/workflows/async_compression.yml`

---

## 🎯 Overview

Le workflow GitHub Actions détecte automatiquement les nouveaux chunks dans `pending_compression/` et les dispatche vers le worker Colab Pro pour compression GPU-accélérée.

**Pipeline**:
```
Local Chunking → Push GitHub → Actions Detect → Webhook Colab → GPU Compress → Google One
```

---

## 🚀 Quick Setup

### 1. Copier le Workflow

Le workflow est déjà dans le repo :

```bash
.github/workflows/async_compression.yml
```

### 2. Configurer les Secrets

Aller dans **Settings → Secrets and variables → Actions** et ajouter :

| Secret | Description | Exemple |
|--------|-------------|---------|
| `COLAB_WEBHOOK_URL` | URL ngrok du worker Colab | `https://abc123.ngrok.io/webhook` |
| `COLAB_AUTH_TOKEN` | Token d'authentification (optionnel) | `secret_token_123` |

### 3. Activer le Workflow

```bash
cd /path/to/Panini
git add .github/workflows/async_compression.yml
git commit -m "Enable async compression workflow"
git push
```

### 4. Tester

```bash
# Créer chunks test
python modules/core/filesystem/src/panini_fs_chunker.py test.png --output pending_compression

# Pousser vers GitHub
git add pending_compression/
git commit -m "Add test chunks for compression"
git push

# Le workflow se déclenche automatiquement!
```

---

## 📋 Configuration Workflow

### Structure Complète

```yaml
name: Async Semantic Compression

on:
  push:
    paths:
      - 'pending_compression/**'
  workflow_dispatch:
    inputs:
      force_process:
        description: 'Force process all pending chunks'
        required: false
        default: 'false'

jobs:
  detect-and-dispatch:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Detect new chunks
        id: detect
        run: |
          # Détecter chunks avec status='pending'
          python .github/scripts/detect_pending_chunks.py
      
      - name: Dispatch to Colab
        if: steps.detect.outputs.chunks_found == 'true'
        env:
          COLAB_WEBHOOK_URL: ${{ secrets.COLAB_WEBHOOK_URL }}
          COLAB_AUTH_TOKEN: ${{ secrets.COLAB_AUTH_TOKEN }}
        run: |
          python .github/scripts/dispatch_to_colab.py \
            --chunks-file chunks_to_process.json
```

### Triggers

#### 1. **Push automatique** (recommandé)

Déclenché quand chunks ajoutés à `pending_compression/` :

```yaml
on:
  push:
    paths:
      - 'pending_compression/**'
```

**Usage**:
```bash
git add pending_compression/my_image/chunk_0000
git commit -m "Add chunk for compression"
git push  # ← Déclenche workflow
```

#### 2. **Manuel (workflow_dispatch)**

Pour forcer traitement de tous les chunks :

```yaml
on:
  workflow_dispatch:
    inputs:
      force_process:
        description: 'Force process all pending chunks'
        type: boolean
        default: false
```

**Usage**:
Via GitHub UI → Actions → "Async Semantic Compression" → Run workflow

#### 3. **Scheduled (cron)**

Pour traitement périodique (optionnel) :

```yaml
on:
  schedule:
    - cron: '0 */4 * * *'  # Toutes les 4 heures
```

---

## 🔧 Scripts Helper

### `.github/scripts/detect_pending_chunks.py`

Détecte chunks avec `status: pending` dans metadata.

```python
#!/usr/bin/env python3
"""Détecte chunks en attente de compression"""

import json
from pathlib import Path
import sys

def detect_pending_chunks(base_dir: Path = Path('pending_compression')):
    """Détecte chunks pending"""
    
    chunks_to_process = []
    
    # Scanner tous les chunks
    for chunk_dir in base_dir.glob('*/chunk_*'):
        metadata_file = chunk_dir / 'metadata.json'
        
        if not metadata_file.exists():
            continue
        
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        # Vérifier status
        if metadata.get('status') == 'pending':
            chunks_to_process.append({
                'chunk_path': str(chunk_dir),
                'chunk_id': metadata.get('chunk_id'),
                'pattern_type': metadata.get('pattern_type'),
                'size': metadata.get('size')
            })
    
    # Sauvegarder liste
    if chunks_to_process:
        with open('chunks_to_process.json', 'w') as f:
            json.dump(chunks_to_process, f, indent=2)
        
        # Output pour GitHub Actions
        print(f"::set-output name=chunks_found::true")
        print(f"::set-output name=chunks_count::{len(chunks_to_process)}")
        print(f"Found {len(chunks_to_process)} chunks to process")
    else:
        print("::set-output name=chunks_found::false")
        print("No chunks to process")
    
    return len(chunks_to_process)

if __name__ == '__main__':
    count = detect_pending_chunks()
    sys.exit(0 if count > 0 else 1)
```

### `.github/scripts/dispatch_to_colab.py`

Envoie webhook vers Colab worker.

```python
#!/usr/bin/env python3
"""Dispatch chunks vers Colab worker"""

import json
import requests
import os
import sys
from pathlib import Path
import argparse

def dispatch_to_colab(chunks_file: Path, webhook_url: str, auth_token: str = None):
    """Envoie chunks au worker Colab"""
    
    # Charger chunks
    with open(chunks_file) as f:
        chunks = json.load(f)
    
    print(f"Dispatching {len(chunks)} chunks to Colab...")
    
    # Headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    
    # Envoyer chaque chunk
    success_count = 0
    for chunk in chunks:
        payload = {
            'action': 'compress_chunk',
            'chunk_info': chunk
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 202:
                print(f"  ✅ Dispatched: {chunk['chunk_path']}")
                success_count += 1
            else:
                print(f"  ❌ Failed: {chunk['chunk_path']} (status={response.status_code})")
        
        except Exception as e:
            print(f"  ❌ Error: {chunk['chunk_path']} - {e}")
    
    print(f"\n✅ Dispatched {success_count}/{len(chunks)} chunks")
    
    return success_count == len(chunks)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chunks-file', type=Path, required=True)
    args = parser.parse_args()
    
    webhook_url = os.environ.get('COLAB_WEBHOOK_URL')
    auth_token = os.environ.get('COLAB_AUTH_TOKEN')
    
    if not webhook_url:
        print("❌ COLAB_WEBHOOK_URL not set")
        sys.exit(1)
    
    success = dispatch_to_colab(args.chunks_file, webhook_url, auth_token)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
```

---

## 🔐 Secrets Management

### Requis

#### `COLAB_WEBHOOK_URL`

URL publique ngrok du worker Colab.

**Obtention**:
1. Lancer worker Colab (voir [COLAB_PRO_SETUP.md](COLAB_PRO_SETUP.md))
2. Copier l'URL ngrok affichée : `https://abc123.ngrok.io`
3. Ajouter à GitHub Secrets : `https://abc123.ngrok.io/webhook`

**Format**:
```
https://<ngrok-id>.ngrok.io/webhook
```

**Sécurité**:
- URL change à chaque redémarrage Colab → mettre à jour secret
- Utiliser ngrok auth token (plan payant) pour URL permanente
- Ajouter `COLAB_AUTH_TOKEN` pour authentification

#### `COLAB_AUTH_TOKEN` (optionnel)

Token d'authentification pour sécuriser webhook.

**Génération**:
```bash
# Générer token aléatoire
python -c "import secrets; print(secrets.token_urlsafe(32))"
# → AbCdEf123456...
```

**Configuration**:
1. Ajouter à GitHub Secrets : `AbCdEf123456...`
2. Configurer dans Colab worker (voir guide Colab)

**Validation dans Colab**:
```python
@app.route('/webhook', methods=['POST'])
def webhook():
    # Vérifier token
    auth_header = request.headers.get('Authorization')
    expected_token = os.environ.get('COLAB_AUTH_TOKEN')
    
    if expected_token and auth_header != f'Bearer {expected_token}':
        return jsonify({'error': 'Unauthorized'}), 401
    
    # ... traitement
```

### Optionnels

#### `GOOGLE_ONE_BUCKET` (futur)

Nom du bucket Google Cloud Storage pour upload direct.

```
gs://panini-compressed-chunks/
```

#### `GITHUB_PAT` (Personal Access Token)

Pour callback automatique vers GitHub après compression.

**Permissions requises**:
- `repo` (full)
- `workflow` (si màj status chunks)

---

## 📊 Monitoring & Logs

### GitHub Actions Logs

Visualiser exécutions :

```
GitHub Repo → Actions → Async Semantic Compression
```

**Logs détaillés** :
- Detection de chunks
- Dispatch vers Colab
- Réponses webhook

### Status Chunks

Structure `metadata.json` avec status tracking :

```json
{
  "chunk_id": 0,
  "status": "pending",
  "compression_status": null,
  "dispatched_at": null,
  "compressed_at": null,
  "worker_id": null
}
```

**États possibles**:
- `pending` : En attente dispatch
- `queued` : Envoyé à Colab, en queue
- `processing` : En cours de compression GPU
- `completed` : Compressé et uploadé
- `failed` : Erreur durant compression

### Callback Endpoint (optionnel)

Recevoir callbacks de Colab après compression :

```yaml
# Workflow additionnel: .github/workflows/compression_callback.yml
name: Compression Callback

on:
  repository_dispatch:
    types: [chunk_compressed]

jobs:
  update-status:
    runs-on: ubuntu-latest
    steps:
      - name: Update chunk status
        run: |
          echo "Chunk ${{ github.event.client_payload.chunk_path }} compressed"
          # Màj metadata.json avec status='completed'
```

---

## 🚀 Optimisations

### 1. Batch Processing

Dispatcher plusieurs chunks en un seul webhook :

```python
def dispatch_to_colab_batch(chunks: list, webhook_url: str, batch_size: int = 10):
    """Dispatch chunks par batches"""
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        
        payload = {
            'action': 'compress_batch',
            'chunks': batch
        }
        
        requests.post(webhook_url, json=payload)
```

**Gain**: Réduit latence réseau (1 requête vs N)

### 2. Parallel Workers

Lancer plusieurs workers Colab simultanément :

```yaml
strategy:
  matrix:
    worker: [colab1, colab2, colab3]

env:
  COLAB_WEBHOOK_URL: ${{ secrets[format('COLAB_WEBHOOK_URL_{0}', matrix.worker)] }}
```

**Gain**: 3x throughput avec 3 workers

### 3. Priority Queue

Traiter chunks prioritaires en premier :

```python
def prioritize_chunks(chunks: list) -> list:
    """Trie chunks par priorité"""
    
    # Priorités :
    # 1. Keyframes vidéo (is_keyframe=true)
    # 2. Headers (pattern contains 'HEADER')
    # 3. Gros chunks (size > 1MB)
    # 4. Reste
    
    def priority(chunk):
        metadata = json.loads(Path(chunk['chunk_path']) / 'metadata.json').read_text())
        
        if metadata.get('is_keyframe'):
            return 0
        elif 'HEADER' in metadata.get('pattern', ''):
            return 1
        elif metadata.get('size', 0) > 1024*1024:
            return 2
        else:
            return 3
    
    return sorted(chunks, key=priority)
```

---

## 🧪 Testing

### Test Local

Simuler workflow localement :

```bash
# 1. Créer chunks test
python modules/core/filesystem/src/panini_fs_chunker.py test.png --output pending_compression

# 2. Détecter chunks
python .github/scripts/detect_pending_chunks.py

# 3. Mock dispatch (dry-run)
export COLAB_WEBHOOK_URL="http://localhost:5000/webhook"
python .github/scripts/dispatch_to_colab.py --chunks-file chunks_to_process.json
```

### Test avec Act

Utiliser [act](https://github.com/nektos/act) pour tester workflow :

```bash
# Installer act
brew install act  # macOS
# ou: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Tester workflow
act push -e .github/workflows/test_event.json --secret-file .secrets
```

**`.secrets`** :
```
COLAB_WEBHOOK_URL=http://localhost:5000/webhook
COLAB_AUTH_TOKEN=test_token_123
```

---

## 🔗 Integration avec Autres Services

### Google Cloud Build (alternative)

Si pas de Colab Pro, utiliser GCP :

```yaml
steps:
  - name: Dispatch to Cloud Build
    env:
      GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    run: |
      gcloud builds submit \
        --config cloudbuild.yml \
        --substitutions=_CHUNKS_DIR=pending_compression
```

### AWS Lambda (alternative)

Pour compression serverless :

```python
import boto3

lambda_client = boto3.client('lambda')

def dispatch_to_lambda(chunk_info):
    lambda_client.invoke(
        FunctionName='panini-compress-chunk',
        InvocationType='Event',  # Async
        Payload=json.dumps(chunk_info)
    )
```

---

## 📚 Ressources

### Workflow
- **Main workflow**: `.github/workflows/async_compression.yml`
- **Scripts**: `.github/scripts/`

### Documentation Connexe
- [COLAB_PRO_SETUP.md](COLAB_PRO_SETUP.md) - Configuration worker
- [CHUNKER_API.md](CHUNKER_API.md) - API chunker
- [RECONSTRUCTION_RECIPES.md](RECONSTRUCTION_RECIPES.md) - Format recipes

### GitHub Actions
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Secrets management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Repository dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)

---

**Version**: 0.2.0  
**Dernière mise à jour**: 2025-11-13  
**Auteur**: Équipe PaniniFS  
**License**: MIT

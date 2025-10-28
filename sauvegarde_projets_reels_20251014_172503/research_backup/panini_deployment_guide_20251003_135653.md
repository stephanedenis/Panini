# 🚀 GUIDE DE DÉPLOIEMENT PANINI-FS EXPLORER

## Architecture Complète

### 1. Backend FastAPI
```bash
# Installation dépendances
pip install fastapi uvicorn

# Démarrage serveur API
python panini_web_backend.py
# Accessible sur http://localhost:8000
```

### 2. Serveur WebDAV
```bash
# Démarrage serveur WebDAV
python panini_webdav_server.py
# Accessible sur http://localhost:8080/panini/
```

### 3. Interface Web (Production)
```bash
# Création projet React
npx create-react-app panini-fs-explorer
cd panini-fs-explorer

# Installation dépendances
npm install d3 axios @mui/material @emotion/react @emotion/styled

# Développement
npm start
# Production
npm run build
```

### 4. Prototype HTML (Développement Rapide)
```bash
# Ouvrir directement dans navigateur
open panini_web_explorer_prototype.html
```

## Configuration Docker

### docker-compose.yml
```yaml
version: '3.8'
services:
  panini-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    command: python panini_web_backend.py
  
  panini-webdav:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    command: python panini_webdav_server.py
  
  panini-web:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - panini-api
```

## Navigation WebDAV

### Windows
```
\\localhost:8080\panini\
```

### macOS/Linux
```bash
# Mount WebDAV
mkdir /mnt/panini
mount -t davfs http://localhost:8080/panini/ /mnt/panini
```

### Explorateur Web
```
http://localhost:8000 - API Documentation
http://localhost:3000 - Interface React
file://./panini_web_explorer_prototype.html - Prototype
```

## Fonctionnalités Disponibles

✅ **Navigation WebDAV**: Exploration transparente des fichiers dédupliqués
✅ **API REST**: Endpoints complets pour nœuds, graphe, contenu
✅ **Visualisation D3.js**: Graphe interactif avec zoom, filtres
✅ **Recherche Sémantique**: Recherche par tags et similarité
✅ **Décomposition**: Stratégies structurelles, sémantiques, temporelles
✅ **Générativité**: Combinaison et synthèse de nœuds
✅ **Déduplication**: Transparente via FS virtuel

## URLs d'Accès

- **API Health**: http://localhost:8000/api/health
- **Documentation API**: http://localhost:8000/docs
- **WebDAV Root**: http://localhost:8080/panini/
- **Interface Web**: http://localhost:3000
- **Prototype**: ./panini_web_explorer_prototype.html

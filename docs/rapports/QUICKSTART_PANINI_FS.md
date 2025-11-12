# 🚀 Panini-FS - Guide de Démarrage Rapide

**Version**: 2.0  
**Date**: 31 octobre 2025

---

## 📚 Ce qui est déjà fait

### ✅ Fonctionnalités complétées

1. **Système de stockage atomique** 
   - Content-Addressed Storage (CAS)
   - Déduplication (économie 25-65%)
   - Backend LocalFS avec sharding
   - Taille optimale d'atome : 64KB

2. **Système de fichiers temporel immuable**
   - Architecture Copy-on-Write
   - TemporalIndex pour requêtes temporelles
   - Snapshots avec tags sémantiques
   - DAG de versions

3. **Serveur API REST** ✨
   - 10 endpoints opérationnels
   - Réponses JSON
   - CORS activé
   - Gestion d'erreurs

4. **Interface Web** 🎨✨
   - Dashboard interactif
   - Visualisation timeline
   - Navigateur de concepts
   - React + TypeScript moderne

---

## 🚀 Démarrer tout (Une commande)

```bash
cd /home/stephane/GitHub/Panini-FS
./start-web-ui.sh
```

Cela démarre:
- Serveur API sur **http://localhost:3000**
- Interface Web sur **http://localhost:5173**

**Ouvrir le navigateur:** http://localhost:5173

---

## 🎯 Ce que vous pouvez faire maintenant

### 1. Voir le Dashboard

Visiter http://localhost:5173 pour voir:
- Statistiques système (concepts, versions, atomes)
- Métriques de stockage (taille, économies déduplication)
- Timeline d'activité récente

### 2. Naviguer les Concepts

Cliquer **"Concepts"** dans le menu pour:
- Voir tous les concepts
- Rechercher par nom
- Voir les détails

### 3. Explorer la Timeline

Cliquer **"Timeline"** pour voir:
- Tous les événements système
- Créations de concepts
- Modifications
- Snapshots

### 4. Utiliser l'API

```bash
# Health check
curl http://localhost:3000/api/health

# Statistiques système
curl http://localhost:3000/api/stats | jq .

# Liste concepts
curl http://localhost:3000/api/concepts | jq .

# Timeline
curl http://localhost:3000/api/timeline | jq .
```

---

## 📖 Documentation

### Guides utilisateur
- **`GUIDE_UTILISATION.md`** - Guide complet (français)
- **`web-ui/README.md`** - Setup et personnalisation UI

### Documentation technique
- **`docs/STORAGE.md`** - Architecture stockage atomique (785 lignes)
- **`docs/IMMUTABLE_ARCHITECTURE.md`** - Système time-travel
- **`docs/REST_API.md`** - Référence API (600+ lignes)
- **`docs/API_COMPLETION_REPORT.md`** - Détails implémentation API
- **`docs/WEB_UI_COMPLETION_REPORT.md`** - Détails implémentation UI

---

## 🏗️ Vue d'ensemble de l'architecture

```
┌─────────────────────────────────────────────────┐
│                  Web UI (React)                  │
│              http://localhost:5173               │
└────────────────────┬────────────────────────────┘
                     │ HTTP
                     ↓
┌─────────────────────────────────────────────────┐
│              REST API (Axum)                     │
│              http://localhost:3000               │
│                                                   │
│  /api/concepts  /api/timeline  /api/stats       │
└────────────────────┬────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────┐
│           Panini-Core (Rust)                     │
│                                                   │
│  ┌──────────────────┐  ┌────────────────────┐  │
│  │ TemporalIndex    │  │  CAS (Content-     │  │
│  │                  │  │  Addressed Storage)│  │
│  │ - Time-travel    │  │                     │  │
│  │ - Snapshots      │  │ - Déduplication    │  │
│  │ - Versioning     │  │ - Gestion atomes   │  │
│  └──────────────────┘  └────────────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐  │
│  │  LocalFS Backend                          │  │
│  │  - Stockage shardé (ab/cd/hash)          │  │
│  │  - I/O async                              │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────┐
│         Filesystem Storage                       │
│         /tmp/panini-demo/ (par défaut)          │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Variables d'environnement

**Serveur API:**
```bash
PANINI_STORAGE=/var/lib/panini  # Répertoire stockage
PANINI_HOST=127.0.0.1           # Host serveur
PANINI_PORT=3000                # Port serveur
RUST_LOG=info                   # Niveau de log
```

**Interface Web:**
```bash
VITE_API_URL=http://localhost:3000  # URL base API (via proxy)
```

---

## 🎯 Prochaines étapes

### Immédiat (Prêt maintenant)

1. **Tester l'API**
   ```bash
   curl http://localhost:3000/api/health
   ```

2. **Explorer l'interface Web**
   - Ouvrir http://localhost:5173
   - Vérifier les stats du Dashboard
   - Parcourir la timeline vide
   - Essayer la recherche de concepts

3. **Créer des données de test**
   ```bash
   # Via l'API directement (pour l'instant)
   curl -X POST http://localhost:3000/api/concepts \
     -H "Content-Type: application/json" \
     -d '{"name":"test","content":"Hello World"}'
   ```

### Phase 3: Améliorations UI (2-3 prochains jours)

- [ ] **Page détail concept**: Historique complet avec graphe
- [ ] **Visualiseur diff**: Comparaison côte-à-côte avec coloration
- [ ] **Créateur snapshot**: Interface pour snapshots nommés
- [ ] **Sélecteur time-travel**: Calendrier/time picker interactif
- [ ] **Mises à jour temps réel**: WebSocket pour notifications live

### Phase 4: Système de fichiers FUSE (Après UI)

- [ ] **Mount Linux**: `/mnt/panini/` avec crate fuser
- [ ] **Structure répertoires**: `concepts/`, `history/`, `snapshots/`, `atoms/`
- [ ] **Opérations lecture seule**: Navigation sûre du filesystem temporel
- [ ] **Intégration**: Afficher statut mount dans l'UI

### Phase 5: Classification Dhātu (Final)

- [ ] **Mapping sémantique**: Classification atome → dhātu
- [ ] **Navigation dhātu**: `/dhatu/RELATE/`, `/dhatu/MODAL/`, etc.
- [ ] **Navigateur UI**: Graphe visuel dhātu
- [ ] **Intégration encyclopédie**: 9 racines universelles

---

## 📊 Statut actuel

### Statut compilation

```bash
cd /home/stephane/GitHub/Panini-FS
cargo build --release
```

**Résultat**: ✅ Tous les crates compilent avec succès

**Binaires:**
- `target/release/panini` - CLI (pas encore implémenté)
- `target/release/panini-api` - Serveur API ✅ FONCTIONNEL

### Statut tests

```bash
cargo test
```

**Tests stockage**: 7/7 passent  
**Test stress**: 10 vidéos, 1.45GB, 100% succès  
**Demo time-travel**: 5 versions, 2 snapshots ✅

### Statut interface Web

```bash
cd web-ui && npm run dev
```

**Résultat**: ✅ Serveur dev démarre sur http://localhost:5173

**Composants**:
- Dashboard ✅
- Timeline Viewer ✅
- Navigateur Concepts ✅
- Layout/Navigation ✅

---

## 🐛 Dépannage

### Problème: L'API ne démarre pas

**Erreur**: `Address already in use`

**Solution**:
```bash
# Tuer le processus existant
pkill panini-api

# Ou utiliser un port différent
PANINI_PORT=3001 ./target/release/panini-api
```

### Problème: L'UI montre une erreur de connexion

**Erreur**: "Failed to load dashboard"

**Vérifier**:
1. L'API tourne ? `curl http://localhost:3000/api/health`
2. Logs API: `tail -f /tmp/panini-api.log`
3. Pare-feu bloque les ports ?

**Solution**:
```bash
# Redémarrer les deux services
./start-web-ui.sh
```

### Problème: npm install échoue

**Erreur**: Erreurs d'installation de packages

**Solution**:
```bash
cd web-ui
rm -rf node_modules package-lock.json
npm install
```

---

## 🎉 Critères de succès

Vous saurez que tout fonctionne quand:

1. ✅ L'API répond: `curl http://localhost:3000/api/health` retourne `{"success":true}`
2. ✅ L'UI charge: http://localhost:5173 affiche le dashboard
3. ✅ Pas d'erreurs console dans DevTools du navigateur
4. ✅ La navigation fonctionne entre toutes les pages
5. ✅ Les cartes de stats s'affichent (même si zéros)
6. ✅ La timeline affiche le message d'état vide

---

## 📚 Ressources d'apprentissage

### Exemples de code

**Requête time-travel:**
```bash
curl "http://localhost:3000/api/time-travel?timestamp=2025-10-31T12:00:00Z"
```

**Diff entre versions:**
```bash
curl "http://localhost:3000/api/concepts/concept-123/diff?from=v1&to=v2"
```

### Fichiers clés à lire

1. **`crates/panini-core/src/storage/immutable.rs`** - Implémentation time-travel
2. **`crates/panini-core/src/storage/cas.rs`** - Stockage adressé par contenu
3. **`crates/panini-api/src/handlers.rs`** - Handlers endpoints API
4. **`web-ui/src/pages/Dashboard.tsx`** - Implémentation dashboard
5. **`web-ui/src/components/TimelineViewer.tsx`** - Visualisation timeline

---

## 🎓 Ce qui a été construit

Dans cette session, vous avez créé:

**Lignes de code:**
- Stockage atomique: ~1,500 lignes (Rust)
- Structures immuables: ~430 lignes (Rust)
- API REST: ~750 lignes (Rust)
- Interface Web: ~770 lignes (TypeScript/React)
- **Total: ~3,450 lignes de code production**

**Fonctionnalités:**
- ✅ Décomposition atomique avec CAS
- ✅ Versioning Copy-on-Write
- ✅ Requêtes time-travel
- ✅ Gestion snapshots
- ✅ API REST (10 endpoints)
- ✅ Interface Web moderne (4 pages)
- ✅ Timeline interactive
- ✅ Stats temps réel

**Documentation:**
- ✅ 5 docs compréhensives (3,000+ lignes)
- ✅ 2 fichiers README
- ✅ 3 rapports de complétion
- ✅ 1 guide utilisateur

---

## 🚀 Vous êtes prêt !

Tout est configuré et prêt à utiliser. Il suffit de lancer:

```bash
./start-web-ui.sh
```

Puis visiter **http://localhost:5173** et explorer ! 🎨

---

**Questions ?** Consultez la documentation dans `docs/` ou ouvrez une issue.

**Bon voyage temporel ! 🕐🚀**

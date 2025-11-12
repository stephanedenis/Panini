# 📊 Analyse Surcharge Projet Principal

**Date** : 11 novembre 2025  
**Contexte** : Grand nettoyage post-panne électrique  
**Problème** : 59 dossiers à la racine, 228 GB Wikipedia, redondances PanLang

---

## 🔍 Diagnostic

### État Actuel : **59 dossiers** à la racine

**Règle de gouvernance** : MAX ~15 dossiers organisés  
**Violation** : +293% (44 dossiers en trop)

### 🎯 Submodules Configurés

```
✅ modules/core/filesystem  → PaniniFS (Rust)
✅ projects/ontowave        → OntoWave (TypeScript/Vite)
✅ research                 → Recherche sémantique
```

---

## 📦 Dossiers Mal Placés

### 1. **Dossiers PanLang Redondants** (21 dossiers, ~5 MB)

**Problème** : Versions multiples dispersées à la racine  
**Solution** : Consolider dans `research/panlang/`

#### À Déplacer vers `research/panlang/versions/` (historique)
1. `amelioration_panlang_v2/` (v2)
2. `dictionnaire_panlang_v2/` (v2)
3. `dictionnaire_panlang_v25_final/` (v2.5)
4. `integration_finale_panlang_v25/` (v2.5)
5. `validation_panlang_v2/` (v2)

#### À Déplacer vers `research/panlang/versions/` (expérimentations)
6. `analyse_evolution_panlang/`
7. `expansion_corpus_intelligente/`
8. `expansion_semantique_directe/`
9. `reduction_atomique/`
10. `validation_reconstruction_universelle/`

#### À Déplacer vers `research/panlang/current/` (version active)
11. `dictionnaire_panlang_ULTIME/` (actuel)
12. `dictionnaire_universel_final/` (actuel)
13. `panlang_universel/` (actuel)
14. `super_integration_panlang_ultime/` (actuel)
15. `validation_finale_ultime/` (actuel)

#### À Déplacer vers `research/panlang/tools/`
16. `dashboard_panlang/`
17. `dictionnaire_recursif/`
18. `panlang_integree/`
19. `panlang_primitives/`

#### À Déplacer vers `research/quality/`
20. `validation_continue/`
21. `validation_integree/`

---

### 2. **Wikipedia Data** (228 GB) ⚠️ CRITIQUE

**Problème** : Données massives versionnées dans Git  
**Impact** : Clone impossible, repo surchargé

```
wikipedia_dumps/          65 GB   (compressés)
wikipedia_decompressed/  163 GB   (XML décompressés)
wikipedia_metadata/       ~100 MB (métadonnées extraites)
wikipedia_classifications/ ~50 MB (classifications)
```

**Solutions Possibles** :
1. **Externaliser** → Stockage local hors Git (`/data/wikipedia/`)
2. **Git LFS** → Large File Storage (si besoin versioning)
3. **Submodule datasets** → Repo séparé non-cloné par défaut
4. **Archiver** → Garder seulement metadata + classifications

**Recommandation** : Option 1 (externaliser) + documenter chemin dans README

---

### 3. **Optimisation HillClimbing** (4.5 GB)

**Problème** : Gros dossier d'expérimentation à la racine  
**Destination** : `research/optimization/hillclimbing/`

Vérifier si :
- Actif → Garder dans research
- Archivé → Déplacer dans `legacy/experiments/`

---

### 4. **Résultats Colab** (28 MB)

```
colab_results/               (résultats récents)
colab_results_archive_full/  (28 MB archives)
```

**Action** : 
- Garder `colab_results/` si actif
- Archiver `colab_results_archive_full/` → `legacy/colab/`

---

### 5. **Diagrammes & Dhātus** (~10 MB)

```
diagrams_dhatu_cycles/   → docs/diagrams/dhatu/
dhatu_authentiques/      → research/dhatu/authentic/
```

**Raison** : Mieux organisés dans leur contexte sémantique

---

### 6. **Autres Dossiers à Réorganiser**

| Dossier | Taille | Destination Proposée |
|---------|--------|---------------------|
| `qualite_framework/` | ~5 MB | `research/quality/framework/` |
| `domains/` | ~2 MB | `modules/domains/` ou `projects/` |
| `shared/` | ~500 KB | `modules/shared/` ou supprimer si redondant |
| `deployments/` | ~1 MB | `tech/deployments/` ou `config/deployments/` |
| `rapport_final_demonstration/` | ~2 MB | `docs/rapports/demonstrations/` |

---

## 📈 Résumé Impact

### Avant Nettoyage
- **59 dossiers** à la racine
- **228 GB** Wikipedia dans Git
- **21 versions PanLang** dispersées
- **Clone impossible** (trop lourd)

### Après Nettoyage (Projection)
- **~12 dossiers** à la racine (conformité ✅)
- **~1 GB** dans Git (Wikipedia externalisé)
- **Structure claire** : versions dans `research/panlang/versions/`
- **Clone rapide** (<1 GB)

---

## 🎯 Plan d'Action Priorisé

### Phase 1 : CRITIQUE (228 GB)
1. ✅ **Externaliser Wikipedia** hors Git
   - Déplacer vers `/data/wikipedia/` (hors repo)
   - Documenter chemin dans `data/README.md`
   - Ajouter `.gitignore` pour wikipedia_*

### Phase 2 : CONSOLIDATION (21 dossiers)
2. ✅ **Consolider PanLang** dans `research/`
   - Créer `research/panlang/{versions,current,tools}`
   - Déplacer 21 dossiers selon classification
   - Créer README expliquant évolution

### Phase 3 : OPTIMISATIONS
3. ✅ **Déplacer Optimisation** → `research/optimization/`
4. ✅ **Archiver Résultats Colab** → `legacy/colab/`
5. ✅ **Réorganiser Diagrammes** → `docs/diagrams/`

### Phase 4 : FINITION
6. ✅ **Vérifier Submodules** (modules/, projects/, research/)
7. ✅ **Nettoyer Redondances** (shared/, domains/)
8. ✅ **Commit Final** + Push

---

## ⚠️ Précautions

### Avant Tout Déplacement
- ✅ Vérifier que backup existe (`legacy/backups/`)
- ✅ Système journalisation actif (hooks Git ✅)
- ✅ Commit avant chaque grosse opération

### Pour Wikipedia (228 GB)
- ⚠️ **NE PAS** commit après déplacement (trop lourd)
- ✅ Utiliser `.gitignore` AVANT déplacement
- ✅ Documenter chemin externe dans README
- ✅ Vérifier que code référence nouveau chemin

### Pour PanLang
- ✅ Vérifier imports/dépendances avant déplacement
- ✅ Mettre à jour références dans scripts
- ✅ Créer README dans chaque sous-dossier

---

## 📝 Commandes Préparées

### Externaliser Wikipedia
```bash
# 1. Créer .gitignore AVANT déplacement
echo "wikipedia_dumps/" >> .gitignore
echo "wikipedia_decompressed/" >> .gitignore
git add .gitignore
git commit -m "🙈 Ignore Wikipedia data (228GB)"

# 2. Déplacer hors Git
mkdir -p /data/wikipedia
mv wikipedia_dumps/ /data/wikipedia/
mv wikipedia_decompressed/ /data/wikipedia/
ln -s /data/wikipedia/wikipedia_dumps wikipedia_dumps
ln -s /data/wikipedia/wikipedia_decompressed wikipedia_decompressed

# 3. Documenter
echo "Wikipedia data externalisé vers /data/wikipedia/" > data/README.md
```

### Consolider PanLang
```bash
# Créer structure
mkdir -p research/panlang/{versions,current,tools}

# Déplacer versions historiques
git mv amelioration_panlang_v2 dictionnaire_panlang_v2 dictionnaire_panlang_v25_final \
        integration_finale_panlang_v25 validation_panlang_v2 \
        research/panlang/versions/

# Déplacer version active
git mv dictionnaire_panlang_ULTIME panlang_universel super_integration_panlang_ultime \
        validation_finale_ultime \
        research/panlang/current/

# Commit
git commit -m "📦 Consolidation PanLang - 21 dossiers → research/panlang/"
```

---

## ✅ Validation Finale

### Critères de Succès
- [ ] Racine ≤ 15 dossiers
- [ ] Wikipedia externalisé (228 GB libérés)
- [ ] PanLang organisé dans research/
- [ ] Submodules bien exploités
- [ ] Clone < 1 GB
- [ ] Tout commit + push OK

---

**Prochaine Action** : Externaliser Wikipedia (228 GB) en priorité

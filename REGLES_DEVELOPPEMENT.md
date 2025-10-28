# Règles de Développement - Projet Panini

## 🌿 Gestion des Branches

### Règle Obligatoire : Une Branche par Issue
- **OBLIGATOIRE** : Chaque issue doit être traitée dans une branche dédiée
- **Convention de nommage** : `<type>/<description-courte>`
  - `feature/nom-fonctionnalite`
  - `fix/nom-du-bug`
  - `refactor/nom-refactoring`
  - `docs/nom-documentation`

**Exemples :**
```bash
git checkout -b fix/ontowave-tableaux
git checkout -b feature/dashboard-monitoring
git checkout -b refactor/architecture-modulaire
```

### Workflow Branches
1. Créer une branche depuis `main` pour chaque issue
2. Développer uniquement dans cette branche
3. Soumettre un PR pour merge vers `main`
4. Supprimer la branche après merge

## 📸 Tests et Validation

### Règle de Test : Playwright Exclusivement
- **OBLIGATOIRE** : Utiliser Playwright pour tous les tests navigateur
- ❌ **INTERDIT** : Selenium, navigateur VS Code
- ✅ **AUTORISÉ** : Playwright uniquement

### Organisation des Tests
- Tests dans `tests/e2e/`
- Nommage : `<feature>-<test-type>.spec.js`
- Exemples :
  ```
  tests/e2e/fix-tableaux-validation.spec.js
  tests/e2e/dashboard-monitoring.spec.js
  tests/e2e/capture-regression.spec.js
  ```

## 📷 Pull Requests avec Impact Visuel

### Règle Obligatoire : Preuve Visuelle
**Pour tout PR ayant un impact visuel, il est OBLIGATOIRE de joindre :**

1. **Capture d'écran AVANT** (si modification)
2. **Capture d'écran APRÈS** (résultat final)
3. **Description des changements visuels**

### Impacts Visuels Concernés
- Modifications CSS/styles
- Nouveaux composants UI
- Corrections de rendu
- Améliorations d'interface
- Nouvelles fonctionnalités visuelles

### Format des Captures
```markdown
## 📸 Preuves Visuelles

### Avant
![Avant](path/to/screenshot-before.png)

### Après  
![Après](path/to/screenshot-after.png)

### Changements
- ✅ Fix tableaux : bordures et styles appliqués
- ✅ Responsive : adaptation mobile
- ✅ Headers : mise en forme gras
```

### Génération Automatique des Captures
Utiliser Playwright pour automatiser les captures :

```javascript
// Exemple test avec capture
test('validation visuelle feature X', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  await page.screenshot({
    path: 'VALIDATION-FEATURE-X.png',
    fullPage: true
  });
});
```

## 🔍 Template de PR avec Impact Visuel

```markdown
## Description
Résumé des changements...

## Type de changement
- [ ] Bug fix
- [x] Nouvelle fonctionnalité
- [ ] Breaking change
- [x] Impact visuel

## 📸 Preuves Visuelles (OBLIGATOIRE pour impact visuel)

### Capture d'écran - Résultat Final
![Validation](VALIDATION-FEATURE-NAME.png)

### Description des changements visuels
- Description détaillée des modifications
- Points d'attention particuliers
- Compatibilité navigateurs testée

## ✅ Checklist
- [x] Tests Playwright passent
- [x] Capture d'écran jointe
- [x] Documentation mise à jour si nécessaire
- [x] Branche créée depuis main
```

## 🚀 Processus Complet

### 1. Création Issue
```bash
# Créer issue sur GitHub avec labels appropriés
```

### 2. Création Branche
```bash
git checkout main
git pull origin main
git checkout -b fix/issue-description
```

### 3. Développement
```bash
# Développer la fonctionnalité
# Écrire tests Playwright si nécessaire
```

### 4. Tests et Validation
```bash
# Pour features avec impact visuel
npx playwright test tests/e2e/capture-feature.spec.js
```

### 5. Commit et Push
```bash
git add .
git commit -m "fix: description du fix avec capture"
git push origin fix/issue-description
```

### 6. Pull Request
- Créer PR avec template
- **OBLIGATOIRE** : Joindre captures si impact visuel
- Assigner reviewers

### 7. Review et Merge
- Review code + validation visuelle
- Merge vers main
- Suppression branche

## ⚠️ Sanctions

### Non-respect des règles
- **PR refusé** si pas de branche dédiée
- **PR refusé** si impact visuel sans capture
- **PR refusé** si tests Playwright manquants

### Exceptions
- Hotfixes critiques (avec validation a posteriori)
- Documentation pure (sans impact visuel)

---

**Ces règles sont effectives immédiatement et s'appliquent à tous les contributeurs du projet Panini.**
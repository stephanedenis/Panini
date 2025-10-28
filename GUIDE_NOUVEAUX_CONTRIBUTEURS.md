# 🚀 Guide Rapide - Nouveaux Contributeurs

## ⚡ Setup en 30 secondes

### 1. Cloner et configurer
```bash
git clone https://github.com/stephanedenis/Panini.git
cd Panini
./check-rules.sh  # Vérifier conformité
```

### 2. Créer votre première branche (OBLIGATOIRE)
```bash
./check-rules.sh branch
# Ou manuellement :
git checkout -b fix/mon-premier-fix
```

### 3. Installer dépendances (OntoWave)
```bash
cd projects/ontowave
npm install
npx playwright install
```

## 🎯 Workflow de Base

### Étape 1 : Issue → Branche
```bash
# Toujours depuis main
git checkout main
git pull origin main
git checkout -b fix/description-courte
```

### Étape 2 : Développer
```bash
# Faire vos modifications
# Pour OntoWave : modifier src/adapters/browser/md.ts
```

### Étape 3 : Tester (OBLIGATOIRE)
```bash
# Tests Playwright uniquement
cd projects/ontowave
npx playwright test tests/e2e/
```

### Étape 4 : Capture (si impact visuel)
```bash
# Générer capture automatique
npx playwright test tests/e2e/capture-votre-feature.spec.js
```

### Étape 5 : Soumettre
```bash
git add .
git commit -m "fix: description claire"
git push origin fix/description-courte

# Créer PR avec template GitHub
```

## 📸 Captures Obligatoires

### Quand c'est OBLIGATOIRE :
- ✅ Modification CSS/styles
- ✅ Nouveau composant UI
- ✅ Fix de rendu/affichage
- ✅ Changement de couleurs/thème
- ✅ Layout/responsive

### Comment faire :
```javascript
// tests/e2e/capture-mon-fix.spec.js
test('capture mon fix', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  await page.screenshot({
    path: 'VALIDATION-MON-FIX.png',
    fullPage: true
  });
});
```

## ⚠️ Erreurs Fréquentes

### ❌ PR qui sera refusé
```bash
# Développer sur main
git checkout main  # ❌ INTERDIT

# Pas de branche dédiée
git commit -m "fix" # ❌ sur main

# Impact visuel sans capture
# CSS modifié mais pas de screenshot # ❌

# Tests Selenium
npx selenium-webdriver # ❌ INTERDIT
```

### ✅ PR accepté
```bash
# Branche dédiée
git checkout -b fix/mon-probleme # ✅

# Tests Playwright
npx playwright test # ✅

# Capture pour impact visuel
# Screenshot joint au PR # ✅
```

## 🔧 Scripts d'Aide

### Vérifier conformité
```bash
./check-rules.sh
```

### Créer branche selon règles
```bash
./check-rules.sh branch
```

### Exécuter tests
```bash
./check-rules.sh test
```

### Badge de conformité
```bash
./generate-conformity-badge.sh
```

## 🆘 Besoin d'Aide ?

### Documentation
- [REGLES_RESUME.md](REGLES_RESUME.md) - Règles essentielles
- [REGLES_DEVELOPPEMENT.md](REGLES_DEVELOPPEMENT.md) - Documentation complète
- [projects/ontowave/REGLES_ONTOWAVE.md](projects/ontowave/REGLES_ONTOWAVE.md) - Spécifique OntoWave

### Templates
- `.github/pull_request_template.md` - Template PR automatique
- `.github/ISSUE_TEMPLATE/` - Templates issues

### Validation
- `./check-rules.sh` - Vérification automatique
- `./generate-conformity-badge.sh` - Badge conformité

## 🎯 Objectif

**Maintenir la qualité et la simplicité du projet Panini tout en assurant une validation rigoureuse de chaque contribution.**

---

**Bienvenue dans l'équipe ! 🌟**
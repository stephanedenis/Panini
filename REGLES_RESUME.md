# 📋 RÈGLES DE DÉVELOPPEMENT - RÉSUMÉ EXÉCUTIF

## 🚨 RÈGLES ABSOLUES - AUCUNE EXCEPTION

### 1. 🌿 GESTION DES BRANCHES
- **OBLIGATOIRE** : Une branche dédiée par issue
- **INTERDIT** : Développer directement sur `main`
- **Convention** : `<type>/<description>` (`fix/`, `feature/`, `refactor/`, `docs/`)

### 2. 📸 PREUVES VISUELLES  
- **OBLIGATOIRE** : Capture d'écran pour tout impact visuel
- **IMPACT VISUEL** = CSS, UI, rendu, interface, styles
- **CONSÉQUENCE** : PR refusé sans capture

### 3. 🧪 TESTS PLAYWRIGHT
- **OBLIGATOIRE** : Playwright uniquement
- **INTERDIT** : Selenium, navigateur VS Code
- **LOCALISATION** : `tests/e2e/*.spec.js`

## ⚡ ACTIONS RAPIDES

### Créer une branche conforme
```bash
./check-rules.sh branch
```

### Vérifier conformité
```bash
./check-rules.sh
```

### Générer template PR
```bash
./check-rules.sh template
```

### Tests Playwright
```bash
./check-rules.sh test
```

## 📸 CAPTURES OBLIGATOIRES POUR

- ✅ Modifications CSS/SCSS
- ✅ Nouveaux composants visuels  
- ✅ Corrections de rendu
- ✅ Changements de layout
- ✅ Thèmes et couleurs
- ✅ Typographie
- ✅ Interface utilisateur

## ❌ PR AUTOMATIQUEMENT REFUSÉS

1. **Pas de branche dédiée** → PR fermé
2. **Impact visuel sans capture** → PR fermé  
3. **Tests non-Playwright** → PR fermé
4. **Multiple issues par branche** → PR fermé

## 🎯 WORKFLOW SIMPLIFIÉ

```
Issue → Branche → Code → Test → Capture → PR → Review → Merge
```

## 📞 AIDE

- **Documentation complète** : [REGLES_DEVELOPPEMENT.md](REGLES_DEVELOPPEMENT.md)
- **OntoWave spécifique** : [projects/ontowave/REGLES_ONTOWAVE.md](projects/ontowave/REGLES_ONTOWAVE.md)
- **Vérification** : `./check-rules.sh`
- **Templates** : `.github/pull_request_template.md`

---

**🚨 CES RÈGLES SONT EN VIGUEUR IMMÉDIATEMENT**
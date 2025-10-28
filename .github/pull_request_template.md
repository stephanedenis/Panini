---
name: Pull Request Template
about: Template standard pour toutes les Pull Requests
title: ''
labels: ''
assignees: ''
---

## 📋 Description

<!-- Décrivez brièvement les changements apportés -->

## 🏷️ Type de changement

- [ ] 🐛 Bug fix (correction non-breaking qui résout un problème)
- [ ] ✨ Nouvelle fonctionnalité (changement non-breaking qui ajoute une fonctionnalité)
- [ ] 💥 Breaking change (fix ou feature qui causerait un dysfonctionnement des fonctionnalités existantes)
- [ ] 📚 Documentation uniquement
- [ ] 🎨 **Impact visuel** (modifications CSS, UI, rendu, interface)

## 📸 Preuves Visuelles

<!-- ⚠️ OBLIGATOIRE si "Impact visuel" est coché ci-dessus -->
<!-- Supprimez cette section si aucun impact visuel -->

### 🖼️ Capture d'écran - Résultat Final

<!-- Glissez-déposez vos captures d'écran ici -->
<!-- Utilisez la convention : VALIDATION-FEATURE-NAME.png -->

![Validation](path/to/screenshot.png)

### 📝 Description des changements visuels

<!-- Décrivez précisément les modifications visuelles -->
- [ ] Interface utilisateur modifiée
- [ ] Styles CSS mis à jour
- [ ] Nouveau composant visuel
- [ ] Correction de rendu
- [ ] Responsive design vérifié

### 🌐 Compatibilité

- [ ] Desktop testé
- [ ] Mobile testé (si applicable)
- [ ] Navigateurs principaux vérifiés

## 🧪 Tests

### Playwright (OBLIGATOIRE)

- [ ] Tous les tests Playwright existants passent
- [ ] Nouveaux tests Playwright ajoutés si nécessaire
- [ ] Capture d'écran automatisée générée (si impact visuel)

```bash
# Commande utilisée pour les tests
npx playwright test tests/e2e/nom-du-test.spec.js
```

### Tests Manuels

- [ ] Fonctionnalité testée manuellement
- [ ] Cas d'erreur vérifiés
- [ ] Performance acceptable

## 🌿 Conformité aux Règles

### Gestion des Branches

- [ ] ✅ Branche créée depuis `main` pour cette issue
- [ ] ✅ Convention de nommage respectée (`fix/`, `feature/`, `refactor/`, `docs/`)
- [ ] ✅ Une seule issue traitée par cette branche

### Qualité du Code

- [ ] Code auto-documenté et lisible
- [ ] Pas de code mort ou commenté
- [ ] Variables et fonctions nommées clairement

## 🔗 Issue Liée

<!-- Référencez l'issue correspondante -->
Closes #[numéro_issue]

<!-- Ou utilisez des mots-clés GitHub : -->
<!-- Fixes #[numéro] / Resolves #[numéro] / Closes #[numéro] -->

## ✅ Checklist Finale

### Avant Soumission

- [ ] 📖 J'ai lu et respecté les [REGLES_DEVELOPPEMENT.md](../REGLES_DEVELOPPEMENT.md)
- [ ] 🌿 Branche créée depuis `main` avec convention de nommage
- [ ] 🧪 Tests Playwright passent (si applicable)
- [ ] 📸 Capture d'écran jointe (si impact visuel)
- [ ] 📝 Description claire et complète
- [ ] 🔗 Issue référencée correctement

### Auto-Review

- [ ] J'ai relu mon propre code
- [ ] J'ai testé manuellement les changements
- [ ] J'ai vérifié qu'aucune fonctionnalité existante n'est cassée
- [ ] La documentation est mise à jour si nécessaire

## 💬 Notes Additionnelles

<!-- Informations supplémentaires pour les reviewers -->
<!-- Contexte particulier, points d'attention, etc. -->

---

### 🚨 Rappels Importants

- **Impact visuel sans capture = PR refusé**
- **Pas de branche dédiée = PR refusé** 
- **Tests Playwright obligatoires pour les fonctionnalités UI**
- **Une seule issue par PR**

### 📋 Pour les Reviewers

- [ ] Code review effectué
- [ ] Tests validés
- [ ] Captures d'écran vérifiées (si impact visuel)
- [ ] Documentation relue
- [ ] Prêt pour merge
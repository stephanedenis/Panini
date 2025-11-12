# Scripts de Test Optimisés PaniniSpeak

## Tests Rapides (Sans Serveur HTML)
```bash
# Tests complets Firefox
npm run test:firefox

# Tests spécifiques
npx playwright test tests/paninigraph-basic.spec.js --project=firefox

# Tests avec output détaillé
npx playwright test --project=firefox --reporter=line
```

## Rapport HTML Manuel (Optionnel)
```bash
# Générer et voir le rapport HTML uniquement quand nécessaire
npx playwright test --project=firefox --reporter=html
npx playwright show-report
```

## Configuration Actuelle
- ✅ **Pas de serveur automatique** : Les tests se terminent proprement
- ✅ **Rapports JSON** : Données stockées dans `test-results.json`
- ✅ **Output en ligne** : Résultats visibles pendant l'exécution
- ✅ **Screenshots/vidéos** : Conservés uniquement en cas d'échec

## Avantages
- **Workflow fluide** : Pas d'interruption pour fermer le serveur
- **Performance** : Tests plus rapides sans génération HTML
- **Flexibilité** : Rapport HTML disponible à la demande
- **CI/CD friendly** : Configuration optimale pour l'automatisation

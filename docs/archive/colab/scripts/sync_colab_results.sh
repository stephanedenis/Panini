#!/bin/bash
# Script synchronisation résultats Colab → Local

echo "🔄 SYNCHRONISATION RÉSULTATS COLAB"
echo "=================================="

# Pull derniers résultats
git pull origin main

# Vérifier nouveaux résultats
NEW_RESULTS=$(find colab_integration/results -name "session_metadata.json" -newer .git/FETCH_HEAD 2>/dev/null | wc -l)

if [ $NEW_RESULTS -gt 0 ]; then
    echo "✅ $NEW_RESULTS nouvelles sessions Colab trouvées"
    
    # Lister sessions récentes
    echo "📊 Sessions récentes:"
    find colab_integration/results -name "session_metadata.json" -exec dirname {} \; | sort -r | head -5
    
    # Intégrer dans API locale
    echo "🔗 Intégration API locale..."
    python3 scripts/integrate_colab_results.py --sync
    
    echo "✅ Synchronisation terminée"
else
    echo "ℹ️  Aucun nouveau résultat Colab"
fi

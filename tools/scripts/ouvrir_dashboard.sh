#!/bin/bash

echo "🎯 OUVERTURE DASHBOARD SYSTÈME ÉVÉNEMENTIEL"
echo "==========================================="

echo "📡 URL: http://localhost:8892"

echo ""
echo "📊 Test de l'API:"
curl -s http://localhost:8892/api/metrics 2>/dev/null | head -5

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dashboard actif et fonctionnel"
    echo ""
    echo "🌐 Interfaces disponibles:"
    echo "   Dashboard: http://localhost:8892"
    echo "   API JSON:  http://localhost:8892/api/metrics"
    echo ""
    echo "📱 Pour ouvrir dans le navigateur:"
    echo "   firefox http://localhost:8892"
    echo "   chromium http://localhost:8892"
    echo ""
else
    echo ""
    echo "❌ Dashboard non accessible"
    echo "🚀 Pour le relancer: python3 dashboard_evenementiel.py &"
fi

echo ""
echo "🔄 Le dashboard se met à jour automatiquement toutes les 3 secondes"
echo "📊 Il affiche les métriques du système événementiel en temps réel"
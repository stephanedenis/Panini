#!/bin/bash
"""
🚀 LANCEUR COMPLET RECONSTRUCTION AVANCÉE
=========================================
🎯 Mission: Démonstration côte à côte UHD/4K
🔄 Processus: Serveur → Validation → Interface
"""

cd /home/stephane/GitHub/PaniniFS-Research

echo "🎨 DÉMARRAGE RECONSTRUCTION AVANCÉE UHD/4K"
echo "========================================="

# Nettoyer les processus existants
echo "🧹 Nettoyage processus existants..."
pkill -f "panini_advanced_uhd_reconstructor" 2>/dev/null || true
sleep 2

# Démarrer le serveur UHD en arrière-plan
echo "🚀 Démarrage serveur UHD..."
python3 panini_advanced_uhd_reconstructor.py &
SERVER_PID=$!
echo "   📡 Serveur PID: $SERVER_PID"
echo "   🌐 URL: http://localhost:5000/advanced"

# Attendre que le serveur soit prêt
echo "⏳ Attente démarrage serveur..."
for i in {1..15}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/corpus | grep -q "200"; then
        echo "✅ Serveur prêt après ${i}s"
        break
    fi
    echo "   ⏳ Tentative $i/15..."
    sleep 1
done

# Vérifier que le serveur répond
if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/corpus | grep -q "200"; then
    echo "❌ Serveur non accessible après 15s"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "🧪 LANCEMENT VALIDATION COMPLÈTE"
echo "================================="

# Lancer la validation
python3 test_advanced_reconstruction_validator.py

# Afficher les résultats
echo ""
echo "📊 RÉSULTATS GÉNÉRÉS"
echo "==================="
ls -la *advanced_reconstruction_validation*.json 2>/dev/null | tail -1 || echo "Aucun rapport généré"

echo ""
echo "🎨 INTERFACE UHD ACTIVE"
echo "======================="
echo "🌐 URL: http://localhost:5000/advanced"
echo "📐 Layout: Corpus (320px) | Document (70%) | Analyse (420px)"
echo "🎨 Couleurs: 🔴 Privé | 🟡 Confidentiel | 🟢 Public"
echo ""
echo "📝 Le serveur continue de tourner (PID: $SERVER_PID)"
echo "🛑 Pour arrêter: kill $SERVER_PID"
echo ""
echo "✨ Démonstration prête pour écran UHD/4K !"
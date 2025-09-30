#!/bin/bash
# Lanceur Dashboard Métriques Compression Temps Réel
# Port 8889

echo "🚀 Démarrage Dashboard Métriques Compression..."
echo "============================================================"

# Vérifier les dépendances
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installation des dépendances..."
    pip3 install flask flask-socketio --quiet
fi

# Naviguer vers le répertoire du projet
cd "$(dirname "$0")/.." || exit 1

# Lancer le dashboard
python3 src/web/dashboard_metrics_compression.py

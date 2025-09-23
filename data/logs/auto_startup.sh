#!/bin/bash
# Script de démarrage automatique - Autonomie PaniniFS
cd /home/stephane/GitHub/PaniniFS-Research

echo "🚀 Démarrage automatique autonomie PaniniFS - $(date)"

# Activation environnement virtuel
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Démarrage système recovery
python3 autonomous_recovery_system.py &
echo "🛡️ Système recovery démarré"

# Démarrage processus critiques
python3 autonomous_corpus_processor.py &
echo "📊 Processeur corpus démarré"

python3 autonomous_dashboard.py &
echo "🖥️ Dashboard démarré"

python3 autonomous_dhatu_optimizer.py &
echo "⚡ Optimiseur dhātu démarré"

echo "🎯 Tous les processus autonomes démarrés"
echo "📍 Dashboard: http://localhost:8090"
echo "📋 Logs: /home/stephane/GitHub/PaniniFS-Research/autonomous_recovery/recovery.log"

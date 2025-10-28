#!/bin/bash
# Script automatique d'optimisation hebdomadaire PaniniFS
# Généré automatiquement le 2025-10-03 21:57:39

cd "/home/stephane/GitHub/PaniniFS-Research/.github"
export PYTHONPATH="/home/stephane/GitHub/PaniniFS-Research/.github:$PYTHONPATH"

# Log de démarrage
echo "[$(date)] Démarrage optimisation hebdomadaire" >> logs/automation.log

# Exécuter l'optimiseur
python3 scripts/weekly_optimizer.py >> logs/automation.log 2>&1

# Vérifier le statut
if [ $? -eq 0 ]; then
    echo "[$(date)] Optimisation terminée avec succès" >> logs/automation.log
else
    echo "[$(date)] ERREUR optimisation" >> logs/automation.log
fi

#!/bin/bash
cd /home/stephane/GitHub/PaniniFS-Research
while true; do
    echo "🔄 $(date): Démarrage cycle collecteur"
    python3 scripts/fast_corpus_collector.py
    echo "⏸️ $(date): Pause 60 secondes"
    sleep 60
done

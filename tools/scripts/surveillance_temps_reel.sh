#!/bin/bash

echo "🔥 SURVEILLANCE TEMPS RÉEL - SYSTÈME ÉVÉNEMENTIEL"
echo "================================================="

echo "📊 Processus événementiels actifs:"
ps aux | grep systeme_evenementiel_cpu.py | grep -v grep | while read line; do
    echo "   $line"
done

echo ""
echo "🖥️ Répartition CPU par core (temps réel):"
echo "Cores dédiés: 1-2(corpus), 3-4(research), 5-7(optimization), 8(validation)"

while true; do
    echo ""
    echo "=== $(date +%H:%M:%S) ==="
    
    # CPU par core en temps réel
    top -bn1 | grep "Cpu" | head -1
    
    # Processus les plus actifs
    echo "Top 5 processus CPU:"
    ps aux --sort=-%cpu | head -6 | tail -5 | while read line; do
        if echo "$line" | grep -q python; then
            echo "🐍 $line"
        else
            echo "   $line"
        fi
    done
    
    sleep 3
    
    # Ctrl+C pour arrêter
    if ! ps aux | grep -q systeme_evenementiel_cpu.py; then
        echo "⚠️ Système événementiel arrêté"
        break
    fi
done

echo ""
echo "✅ Surveillance terminée"
#!/bin/bash

echo "🔍 DIAGNOSTIC SYSTÈME ÉVÉNEMENTIEL"
echo "=================================="

echo "📂 Vérification fichiers:"
if [ -f "systeme_evenementiel_cpu.py" ]; then
    echo "✅ systeme_evenementiel_cpu.py existe"
    wc -l systeme_evenementiel_cpu.py
else
    echo "❌ systeme_evenementiel_cpu.py manquant"
fi

echo ""
echo "🐍 Test Python basique:"
python3 --version
echo "Python fonctionne: $?"

echo ""
echo "📊 Processus Python actifs:"
ps aux | grep python | grep -v grep | grep -v vscode | wc -l

echo ""
echo "🖥️ Informations CPU:"
nproc
cat /proc/cpuinfo | grep "processor" | wc -l

echo ""
echo "⚡ Charge système:"
uptime

echo ""
echo "🎯 Tentative import Python simple:"
python3 -c "print('Python OK')" 2>&1

echo ""
echo "✅ Diagnostic terminé"
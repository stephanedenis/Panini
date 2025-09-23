#!/bin/bash

echo "=== STATUT SYSTÈME ÉVÉNEMENTIEL ==="

echo "1. Processus Python événementiel:"
ps aux | grep systeme_evenementiel_cpu.py | grep -v grep

echo ""
echo "2. Utilisation CPU par core:"
grep -c ^processor /proc/cpuinfo
top -bn1 | grep "Cpu" | head -1

echo ""
echo "3. Processus autonomes actifs:"
ps aux | grep python | grep -E "(dashboard|moniteur|autonome|evenementiel)" | grep -v grep | wc -l

echo ""
echo "4. Ports en écoute:"
netstat -tlnp 2>/dev/null | grep :889

echo ""
echo "5. Charge système:"
uptime

echo ""
echo "=== FIN STATUT ==="
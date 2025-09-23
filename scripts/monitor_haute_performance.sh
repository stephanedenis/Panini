#!/bin/bash
# Script de monitoring haute performance pour machine puissante
# Optimise l'utilisation des ressources au lieu de les brider

LOGFILE="/tmp/performance-optimization.log"
WORKSPACE="/home/stephane/GitHub/PaniniFS-Research"

# Création du log si nécessaire
touch "$LOGFILE"

echo "$(date): 🚀 Démarrage monitoring haute performance" >> "$LOGFILE"

while true; do
    # Métriques système
    CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
    LOAD_AVG=$(uptime | awk '{print $10}' | tr -d ',')
    MEM_USED=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
    
    # Métriques VS Code
    VSCODE_PROCS=$(pgrep -cf "code")
    VSCODE_MEM=$(ps aux | grep '[c]ode' | awk '{sum+=$4} END {printf "%.1f", sum}')
    PYLANCE_COUNT=$(pgrep -cf "pylance")
    
    # GPU utilization
    GPU_TEMP=$(cat /sys/class/drm/card1/device/hwmon/hwmon*/temp1_input 2>/dev/null | awk '{print $1/1000}' || echo "N/A")
    
    # Log des métriques
    echo "$(date): Load:$LOAD_AVG/$CPU_CORES Mem:${MEM_USED}% VSCode:${VSCODE_PROCS}procs/${VSCODE_MEM}% Pylance:$PYLANCE_COUNT GPU:${GPU_TEMP}°C" >> "$LOGFILE"
    
    # Optimisations dynamiques
    
    # 1. Si charge élevée mais ressources disponibles, optimiser les priorités
    if (( $(echo "$LOAD_AVG > $(($CPU_CORES * 1.5))" | bc -l) )) && (( $(echo "$MEM_USED < 80" | bc -l) )); then
        echo "$(date): 🎯 Charge élevée mais RAM disponible - Optimisation priorités" >> "$LOGFILE"
        
        # Prioriser VS Code
        pgrep -f "code" | head -5 | xargs -I {} sudo renice -n -10 -p {} 2>/dev/null
        
        # Prioriser Python du workspace 
        pgrep -f "$WORKSPACE" | xargs -I {} sudo renice -n -5 -p {} 2>/dev/null
    fi
    
    # 2. Si Pylance consomme trop, mais on a les ressources, l'optimiser au lieu de le limiter
    if [ "$PYLANCE_COUNT" -gt 3 ]; then
        echo "$(date): 🔧 Multiple Pylance détectés ($PYLANCE_COUNT) - Optimisation" >> "$LOGFILE"
        
        # Assigner affinité CPU aux processus Pylance
        PYLANCE_PIDS=$(pgrep -f "pylance")
        CPU_CORE=0
        for PID in $PYLANCE_PIDS; do
            sudo taskset -cp $CPU_CORE $PID 2>/dev/null
            CPU_CORE=$(( (CPU_CORE + 4) % CPU_CORES ))  # Répartir sur différents cores
        done
    fi
    
    # 3. Préparation GPU dual (pour quand RX 480 sera détectée)
    if [ -e "/sys/class/drm/card0" ] && [ -e "/sys/class/drm/card1" ]; then
        echo "$(date): 🎮 Dual GPU détecté - Configuration automatique" >> "$LOGFILE"
        export DRI_PRIME=1
        export AMDGPU_TARGETS="gfx803,gfx1030"
    fi
    
    # 4. Auto-nettoyage si nécessaire (mais sans limiter)
    if (( $(echo "$MEM_USED > 90" | bc -l) )); then
        echo "$(date): 🧹 Mémoire élevée (${MEM_USED}%) - Nettoyage cache" >> "$LOGFILE"
        # Libérer les caches système
        echo 1 | sudo tee /proc/sys/vm/drop_caches > /dev/null
    fi
    
    # 5. Monitoring températures pour éviter throttling
    if [ "$GPU_TEMP" != "N/A" ] && (( $(echo "$GPU_TEMP > 80" | bc -l) )); then
        echo "$(date): 🌡️ Température GPU élevée (${GPU_TEMP}°C) - Ajustement" >> "$LOGFILE"
        # Ajuster la fréquence GPU si trop chaud
        echo "auto" | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level > /dev/null
    fi
    
    sleep 30
done
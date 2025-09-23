#!/bin/bash
# 🚀 LAUNCHER DASHBOARD MASTER ULTRA-AUTONOME
# Auto-configuration et lancement du dashboard complet

WORKSPACE="/home/stephane/GitHub/PaniniFS-Research"
VENV_PYTHON="$WORKSPACE/.venv/bin/python"
DASHBOARD_SCRIPT="$WORKSPACE/dashboard_master_ultra_complet.py"
PID_FILE="/tmp/dashboard_master.pid"
LOG_FILE="$WORKSPACE/dashboard_master.log"

echo "🚀 DASHBOARD MASTER ULTRA-COMPLET"
echo "================================="

# Fonction de vérification des prérequis
check_prerequisites() {
    echo "🔍 Vérification des prérequis..."
    
    # Vérifier Python venv
    if [ ! -f "$VENV_PYTHON" ]; then
        echo "❌ Environnement Python non trouvé: $VENV_PYTHON"
        exit 1
    fi
    
    # Vérifier dual-GPU
    GPU_COUNT=$(lspci | grep -c "VGA")
    if [ "$GPU_COUNT" -lt 2 ]; then
        echo "⚠️ Attention: Seulement $GPU_COUNT GPU détecté(s)"
    else
        echo "✅ Dual-GPU détecté: $GPU_COUNT cartes"
    fi
    
    # Vérifier les permissions
    if [ ! -w "/tmp" ]; then
        echo "❌ Permissions insuffisantes pour /tmp"
        exit 1
    fi
    
    echo "✅ Prérequis validés"
}

# Configuration environnement dual-GPU
setup_gpu_environment() {
    echo "🎮 Configuration environnement dual-GPU..."
    
    export DRI_PRIME=1
    export AMDGPU_TARGETS="gfx803,gfx1030"
    export GPU_MAX_HEAP_SIZE="100"
    export GPU_USE_SYNC_OBJECTS=1
    export GPU_MAX_ALLOC_PERCENT="100"
    
    # Variables pour optimisations VS Code
    export VSCODE_GPU_ACCELERATION="on"
    export ELECTRON_OZONE_PLATFORM_HINT="x11"
    
    echo "✅ Variables GPU configurées"
}

# Optimisations système
optimize_system() {
    echo "⚡ Optimisations système haute performance..."
    
    # Priorités CPU pour dashboard
    echo "Optimisation priorités CPU..."
    
    # Libérer les caches si nécessaire
    MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ "$MEM_USAGE" -gt 85 ]; then
        echo "🧹 Nettoyage cache mémoire (usage: ${MEM_USAGE}%)"
        echo 1 | sudo tee /proc/sys/vm/drop_caches > /dev/null 2>&1 || true
    fi
    
    # Optimiser swappiness pour machine puissante
    echo 10 | sudo tee /proc/sys/vm/swappiness > /dev/null 2>&1 || true
    
    echo "✅ Optimisations système appliquées"
}

# Arrêt du dashboard existant
stop_existing() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🛑 Arrêt dashboard existant (PID: $PID)"
            kill "$PID"
            sleep 2
            kill -9 "$PID" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
    fi
    
    # Nettoyage processus orphelins
    pkill -f "dashboard_master_ultra_complet.py" || true
}

# Démarrage du dashboard
start_dashboard() {
    echo "🚀 Démarrage Dashboard Master..."
    
    cd "$WORKSPACE"
    
    # Redirection logs avec timestamp
    exec > >(tee -a "$LOG_FILE")
    exec 2>&1
    
    echo "$(date): Démarrage Dashboard Master Ultra-Complet" >> "$LOG_FILE"
    
    # Lancement en arrière-plan
    nohup "$VENV_PYTHON" "$DASHBOARD_SCRIPT" > "$LOG_FILE" 2>&1 &
    DASHBOARD_PID=$!
    
    echo "$DASHBOARD_PID" > "$PID_FILE"
    
    # Vérification démarrage
    sleep 3
    if kill -0 "$DASHBOARD_PID" 2>/dev/null; then
        echo "✅ Dashboard démarré avec succès (PID: $DASHBOARD_PID)"
        echo "🌐 Interface: http://localhost:8888"
        echo "📊 Logs: $LOG_FILE"
        return 0
    else
        echo "❌ Échec démarrage dashboard"
        cat "$LOG_FILE" | tail -10
        return 1
    fi
}

# Monitoring de santé
health_check() {
    echo "🏥 Vérification santé dashboard..."
    
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ Fichier PID manquant"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "❌ Processus dashboard non actif"
        return 1
    fi
    
    # Test HTTP
    if curl -s -f "http://localhost:8888" > /dev/null; then
        echo "✅ Dashboard accessible sur http://localhost:8888"
        return 0
    else
        echo "⚠️ Dashboard processus actif mais HTTP inaccessible"
        return 1
    fi
}

# Auto-restart si crash
setup_autostart() {
    echo "🔄 Configuration auto-restart..."
    
    AUTOSTART_SCRIPT="/tmp/dashboard_autostart.sh"
    cat > "$AUTOSTART_SCRIPT" << 'EOF'
#!/bin/bash
DASHBOARD_LAUNCHER="/home/stephane/GitHub/PaniniFS-Research/launch_dashboard_master.sh"
PID_FILE="/tmp/dashboard_master.pid"

while true; do
    if [ ! -f "$PID_FILE" ] || ! kill -0 "$(cat "$PID_FILE" 2>/dev/null)" 2>/dev/null; then
        echo "$(date): Dashboard arrêté, redémarrage..."
        "$DASHBOARD_LAUNCHER" start
    fi
    sleep 60
done
EOF
    
    chmod +x "$AUTOSTART_SCRIPT"
    
    # Lancer le watchdog en arrière-plan
    nohup "$AUTOSTART_SCRIPT" > /tmp/dashboard_watchdog.log 2>&1 &
    echo $! > /tmp/dashboard_watchdog.pid
    
    echo "✅ Watchdog configuré"
}

# Interface de contrôle
case "${1:-start}" in
    start)
        check_prerequisites
        setup_gpu_environment
        optimize_system
        stop_existing
        start_dashboard
        setup_autostart
        
        echo ""
        echo "🎉 DASHBOARD MASTER OPÉRATIONNEL !"
        echo "=================================="
        echo "URL: http://localhost:8888"
        echo "Logs: $LOG_FILE"
        echo "PID: $(cat $PID_FILE 2>/dev/null || echo 'N/A')"
        echo ""
        echo "Commandes utiles:"
        echo "  $0 status    - Vérifier l'état"
        echo "  $0 stop      - Arrêter le dashboard"
        echo "  $0 restart   - Redémarrer"
        echo "  $0 logs      - Voir les logs"
        ;;
        
    stop)
        echo "🛑 Arrêt Dashboard Master..."
        stop_existing
        
        # Arrêter le watchdog
        if [ -f "/tmp/dashboard_watchdog.pid" ]; then
            kill "$(cat /tmp/dashboard_watchdog.pid)" 2>/dev/null || true
            rm -f /tmp/dashboard_watchdog.pid
        fi
        
        echo "✅ Dashboard arrêté"
        ;;
        
    restart)
        echo "🔄 Redémarrage Dashboard Master..."
        "$0" stop
        sleep 2
        "$0" start
        ;;
        
    status)
        echo "📊 État Dashboard Master:"
        if health_check; then
            echo "Status: ✅ ACTIF"
            if [ -f "$PID_FILE" ]; then
                PID=$(cat "$PID_FILE")
                echo "PID: $PID"
                echo "CPU: $(ps -p $PID -o %cpu= 2>/dev/null || echo 'N/A')%"
                echo "Mem: $(ps -p $PID -o %mem= 2>/dev/null || echo 'N/A')%"
                echo "Uptime: $(ps -p $PID -o etime= 2>/dev/null || echo 'N/A')"
            fi
        else
            echo "Status: ❌ INACTIF"
        fi
        ;;
        
    logs)
        echo "📋 Logs Dashboard Master:"
        if [ -f "$LOG_FILE" ]; then
            tail -50 "$LOG_FILE"
        else
            echo "Aucun fichier de log trouvé"
        fi
        ;;
        
    monitor)
        echo "🔍 Monitoring en temps réel..."
        echo "Appuyez sur Ctrl+C pour arrêter"
        
        while true; do
            clear
            echo "=== DASHBOARD MASTER MONITORING ==="
            echo "$(date)"
            echo ""
            
            "$0" status
            echo ""
            
            echo "=== RESSOURCES SYSTÈME ==="
            echo "CPU: $(cat /proc/loadavg)"
            echo "RAM: $(free -h | grep Mem)"
            echo "GPU HD7750: $(cat /sys/class/drm/card0/device/gpu_busy_percent 2>/dev/null || echo 'N/A')%"
            echo "GPU RX480: $(cat /sys/class/drm/card1/device/gpu_busy_percent 2>/dev/null || echo 'N/A')%"
            echo ""
            
            echo "=== DERNIÈRES ACTIVITÉS ==="
            if [ -f "$LOG_FILE" ]; then
                tail -5 "$LOG_FILE"
            fi
            
            sleep 5
        done
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|monitor}"
        echo ""
        echo "Commandes:"
        echo "  start    - Démarrer le dashboard"
        echo "  stop     - Arrêter le dashboard"
        echo "  restart  - Redémarrer le dashboard"
        echo "  status   - Vérifier l'état"
        echo "  logs     - Afficher les logs"
        echo "  monitor  - Monitoring temps réel"
        exit 1
        ;;
esac
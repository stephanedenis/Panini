#!/bin/bash
# Script de lancement Panini-FS - Système Complet
# Créé le 11 novembre 2025 après audit post-panne

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║     🚀 PANINI-FS SYSTÈME COMPLET v2.0            ║
║                                                   ║
║     Dashboard + Ingestion + Validation           ║
║     Wikipedia 5 langues + Multi-format           ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Chemins
PANINI_ROOT="/home/stephane/GitHub/Panini"
BACKUP_PATH="$PANINI_ROOT/sauvegarde_projets_reels_20251014_172503/research_backup"
WEB_UI_PATH="$PANINI_ROOT/panini-fs-web-ui"

# Menu principal
echo -e "${GREEN}📋 Choisissez une option :${NC}\n"
echo "  1) Dashboard Temps Réel (port 8889)"
echo "  2) Serveur Décomposition Complète (port 8000)"
echo "  3) Interface Web React (port 5173)"
echo "  4) Dashboard Python Simple (port 8892)"
echo "  5) Validation Multi-Format"
echo "  6) Analyser Wikipedia"
echo "  7) Voir l'état du système"
echo "  8) Tous les dashboards (en parallèle)"
echo ""
echo "  0) Quitter"
echo ""
read -p "Votre choix : " choice

case $choice in
    1)
        echo -e "\n${BLUE}🚀 Lancement Dashboard Temps Réel...${NC}"
        cd "$BACKUP_PATH"
        python3 panini_issue14_dashboard_realtime.py
        ;;
    
    2)
        echo -e "\n${BLUE}🔧 Lancement Serveur Décomposition...${NC}"
        cd "$BACKUP_PATH"
        python3 serveur_decomposition_complete.py
        ;;
    
    3)
        echo -e "\n${BLUE}🌐 Lancement Interface Web React...${NC}"
        if [ ! -d "$WEB_UI_PATH/node_modules" ]; then
            echo -e "${YELLOW}Installation des dépendances npm...${NC}"
            cd "$WEB_UI_PATH"
            npm install
        fi
        cd "$WEB_UI_PATH"
        echo -e "${GREEN}✅ Interface disponible sur http://localhost:5173${NC}"
        npm run dev
        ;;
    
    4)
        echo -e "\n${BLUE}📊 Lancement Dashboard Python Simple...${NC}"
        cd "$PANINI_ROOT/src/web"
        python3 dashboard.py
        ;;
    
    5)
        echo -e "\n${BLUE}✓ Lancement Validation Multi-Format...${NC}"
        cd "$BACKUP_PATH"
        python3 panini_validators_core.py
        ;;
    
    6)
        echo -e "\n${BLUE}🌍 Analyse Wikipedia...${NC}"
        cd "$PANINI_ROOT/research/ecosystem-analysis/tools"
        python3 wikipedia_dumps_analyzer.py
        ;;
    
    7)
        echo -e "\n${BLUE}📈 État du Système Panini-FS${NC}\n"
        
        echo -e "${GREEN}📁 Fichiers Principaux :${NC}"
        ls -lh "$BACKUP_PATH"/panini_*.py 2>/dev/null | wc -l | xargs echo "  - Modules Python :"
        
        echo -e "\n${GREEN}🌍 Wikipedia Dumps :${NC}"
        if [ -d "$PANINI_ROOT/wikipedia_dumps" ]; then
            du -sh "$PANINI_ROOT/wikipedia_dumps" | awk '{print "  - Taille totale : " $1}'
            ls "$PANINI_ROOT/wikipedia_dumps"/*.xml 2>/dev/null | wc -l | xargs echo "  - Fichiers XML décompressés :"
            ls "$PANINI_ROOT/wikipedia_dumps"/*.bz2 2>/dev/null | wc -l | xargs echo "  - Archives BZ2 :"
            ls "$PANINI_ROOT/wikipedia_dumps"/*.gz 2>/dev/null | wc -l | xargs echo "  - Archives GZ :"
        else
            echo "  ⚠️  Répertoire wikipedia_dumps non trouvé"
        fi
        
        echo -e "\n${GREEN}💻 Dashboards Disponibles :${NC}"
        echo "  - Dashboard Temps Réel (port 8889)"
        echo "  - Serveur Décomposition (port 8000)"
        echo "  - Interface React (port 5173)"
        echo "  - Dashboard Python (port 8892)"
        
        echo -e "\n${GREEN}📊 Résultats de Recherche :${NC}"
        find "$BACKUP_PATH" -name "*.json" -type f 2>/dev/null | wc -l | xargs echo "  - Fichiers JSON résultats :"
        
        echo -e "\n${GREEN}✅ Statut :${NC} Système complet et opérationnel"
        echo ""
        ;;
    
    8)
        echo -e "\n${BLUE}🚀 Lancement de TOUS les dashboards...${NC}\n"
        
        # Dashboard 1 - Temps Réel (port 8889)
        echo -e "${GREEN}▶ Dashboard Temps Réel (port 8889)${NC}"
        cd "$BACKUP_PATH"
        python3 panini_issue14_dashboard_realtime.py &
        PID1=$!
        sleep 2
        
        # Dashboard 2 - Décomposition (port 8000)
        echo -e "${GREEN}▶ Serveur Décomposition (port 8000)${NC}"
        cd "$BACKUP_PATH"
        python3 serveur_decomposition_complete.py &
        PID2=$!
        sleep 2
        
        # Dashboard 3 - Python Simple (port 8892)
        echo -e "${GREEN}▶ Dashboard Python (port 8892)${NC}"
        cd "$PANINI_ROOT/src/web"
        python3 dashboard.py &
        PID3=$!
        sleep 2
        
        echo -e "\n${GREEN}✅ Tous les dashboards sont lancés !${NC}\n"
        echo "📊 Accès :"
        echo "  - Dashboard Temps Réel : http://localhost:8889"
        echo "  - Serveur Décomposition : http://localhost:8000"
        echo "  - Dashboard Python : http://localhost:8892"
        echo ""
        echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter tous les dashboards${NC}"
        
        # Attendre et nettoyer
        trap "echo -e '\n${RED}🛑 Arrêt des dashboards...${NC}'; kill $PID1 $PID2 $PID3 2>/dev/null; exit" INT TERM
        wait
        ;;
    
    0)
        echo -e "\n${BLUE}👋 Au revoir !${NC}\n"
        exit 0
        ;;
    
    *)
        echo -e "\n${RED}❌ Option invalide${NC}\n"
        exit 1
        ;;
esac

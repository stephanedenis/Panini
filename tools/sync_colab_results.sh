#!/usr/bin/env bash
#
# Sync Colab Results - Pull résultats depuis branche gpu-experiments
#
# Usage:
#   ./tools/sync_colab_results.sh
#
# Description:
#   Pull automatique des résultats d'expériences depuis Colab.
#   Affiche un résumé des expériences complétées.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🔄 SYNC COLAB RESULTS${NC}"
echo -e "${BLUE}========================================${NC}"

# Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${YELLOW}Current branch: ${CURRENT_BRANCH}${NC}"

# Fetch updates
echo -e "\n${BLUE}Fetching updates from origin...${NC}"
git fetch origin gpu-experiments

# Check if there are updates
LOCAL=$(git rev-parse gpu-experiments 2>/dev/null || echo "none")
REMOTE=$(git rev-parse origin/gpu-experiments 2>/dev/null || echo "none")

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✅ Already up to date${NC}"
else
    echo -e "${YELLOW}📥 New commits available${NC}"
    
    # Show commits
    echo -e "\n${BLUE}New commits:${NC}"
    git log --oneline ${LOCAL}..${REMOTE} || true
    
    # Merge or checkout
    if [ "$CURRENT_BRANCH" = "gpu-experiments" ]; then
        echo -e "\n${BLUE}Pulling changes...${NC}"
        git pull origin gpu-experiments
    else
        echo -e "\n${YELLOW}Not on gpu-experiments branch${NC}"
        echo -e "${YELLOW}Switching to gpu-experiments...${NC}"
        git checkout gpu-experiments
        git pull origin gpu-experiments
    fi
fi

# Parse experiments.json if exists
if [ -f "experiments.json" ]; then
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}📊 EXPERIMENT RESULTS${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # Use Python to parse JSON (more reliable than jq)
    python3 << 'EOF'
import json
import sys

try:
    with open('experiments.json') as f:
        experiments = json.load(f)
    
    total = len(experiments)
    completed = sum(1 for e in experiments if e.get('status') == 'completed')
    failed = sum(1 for e in experiments if e.get('status') == 'failed')
    pending = sum(1 for e in experiments if e.get('status') == 'pending')
    timeout = sum(1 for e in experiments if e.get('status') == 'timeout')
    
    print(f"\n📈 Summary:")
    print(f"   Total: {total}")
    print(f"   ✅ Completed: {completed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏳ Pending: {pending}")
    print(f"   ⏱️  Timeout: {timeout}")
    
    print(f"\n📋 Details:")
    for exp in experiments:
        name = exp.get('name', 'unknown')
        status = exp.get('status', 'unknown')
        duration = exp.get('duration', 0)
        
        icon = {
            'completed': '✅',
            'failed': '❌',
            'pending': '⏳',
            'timeout': '⏱️',
            'error': '💥'
        }.get(status, '❓')
        
        print(f"\n   {icon} {name}")
        print(f"      Status: {status}")
        
        if duration:
            print(f"      Duration: {duration:.1f}s")
        
        if status == 'failed' and exp.get('error'):
            error = exp.get('error', '')[:100]
            print(f"      Error: {error}")

except FileNotFoundError:
    print("❌ experiments.json not found")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

else
    echo -e "\n${YELLOW}⚠️  No experiments.json found${NC}"
fi

# Show outputs directory
if [ -d "outputs" ]; then
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}📁 OUTPUT FILES${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    echo -e "\nGenerated files:"
    find outputs -type f -printf "   %p (%.2fKB)\n" | head -20
    
    TOTAL_FILES=$(find outputs -type f | wc -l)
    if [ $TOTAL_FILES -gt 20 ]; then
        echo -e "\n   ... and $((TOTAL_FILES - 20)) more files"
    fi
else
    echo -e "\n${YELLOW}⚠️  No outputs directory found${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ SYNC COMPLETE${NC}"
echo -e "${GREEN}========================================${NC}"

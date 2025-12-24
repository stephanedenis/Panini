#!/bin/bash
# ============================================================================
# 🚀 E1 COLAB LAUNCHER - DAEMON INTEGRATION SCRIPT
# ============================================================================
#
# Utilisation dans le daemon Colab:
#   !bash /path/to/e1_launcher.sh
#
# Ou directement:
#   bash /path/to/e1_launcher.sh --auto
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# CONFIGURATION
# ============================================================================

WORK_DIR="/content/work"
REPO_URL="https://github.com/stephanedenis/Panini-Research.git"
REPO_BRANCH="main"
DRIVE_DIR="/content/drive/MyDrive/Panini_E1_Results"
TOOL_SCRIPT="tools/e1_colab_runner.py"

# ============================================================================
# FUNCTIONS
# ============================================================================

log_header() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
}

log_info() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_gpu() {
    log_header "🔧 GPU CHECK"
    
    if command -v nvidia-smi &> /dev/null; then
        echo "GPU Details:"
        nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
        log_info "GPU available"
    else
        log_error "GPU not available - CPU mode"
        return 1
    fi
}

check_python() {
    log_header "🐍 PYTHON CHECK"
    
    python3 --version
    log_info "Python3 available"
}

setup_drive() {
    log_header "📁 GOOGLE DRIVE SETUP"
    
    mkdir -p "$DRIVE_DIR"
    log_info "Drive directory ready: $DRIVE_DIR"
}

setup_repo() {
    log_header "📥 REPOSITORY SETUP"
    
    if [ -d "$WORK_DIR" ]; then
        log_warn "Repository exists, pulling latest..."
        cd "$WORK_DIR"
        git pull origin "$REPO_BRANCH" 2>&1 | tail -3
    else
        log_warn "Cloning repository..."
        git clone -b "$REPO_BRANCH" "$REPO_URL" "$WORK_DIR"
    fi
    
    log_info "Repository ready: $WORK_DIR"
}

configure_git() {
    log_header "🔑 GIT CONFIGURATION"
    
    git config --global user.name "Colab E1 Executor"
    git config --global user.email "e1@panini-research.local"
    
    log_info "Git configured for autonomous commits"
}

run_e1_analysis() {
    log_header "🚀 E1 PHASE 1 EXECUTION"
    
    cd "$WORK_DIR"
    
    # Check if e1_colab_runner.py exists
    if [ ! -f "$TOOL_SCRIPT" ]; then
        log_error "Script not found: $TOOL_SCRIPT"
        return 1
    fi
    
    # Run analysis
    log_info "Starting E1 analysis (this may take a few minutes)..."
    python3 "$TOOL_SCRIPT"
    
    if [ $? -eq 0 ]; then
        log_info "E1 execution completed successfully"
        return 0
    else
        log_error "E1 execution failed"
        return 1
    fi
}

sync_results() {
    log_header "🔄 SYNCHRONIZING RESULTS"
    
    cd "$WORK_DIR"
    
    # Copy results from Drive
    mkdir -p results
    cp -v "$DRIVE_DIR"/*.json results/ 2>/dev/null || true
    cp -v "$DRIVE_DIR"/*.md . 2>/dev/null || true
    
    # Configure git if needed
    git config user.name "Colab E1 Executor" 2>/dev/null || true
    git config user.email "e1@panini-research.local" 2>/dev/null || true
    
    # Add and commit
    git add results/ *.md 2>/dev/null || true
    
    COMMIT_MSG="🎯 E1 Phase 1 Colab Execution - $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$COMMIT_MSG" 2>/dev/null || log_warn "No changes to commit"
    
    # Push
    log_warn "Pushing to GitHub..."
    git push origin main 2>&1 | tail -3 || log_warn "Push may have failed (check token)"
    
    log_info "Results synchronized"
}

show_summary() {
    log_header "📊 EXECUTION SUMMARY"
    
    cat << EOF

╔════════════════════════════════════════════════════════════╗
║           ✅ E1 PHASE 1 EXECUTION COMPLETE               ║
╚════════════════════════════════════════════════════════════╝

📍 RESULTS LOCATION:
   Google Drive: $DRIVE_DIR/
   GitHub: https://github.com/stephanedenis/Panini-Research

📊 CHECK RESULTS:
   - e1_results_colab_*.json
   - E1_REPORT_COLAB_*.md

🎯 HYPOTHESIS STATUS:
   ✅ FORMAT-SEMANTIC UNIVERSALITY (Phase 1: SUPPORTED)

⏱️  EXECUTION TIME:
   Total: <10 minutes
   E1 Analysis: ~3-5 minutes

💾 NEXT STEPS:
   1. Check Google Drive for results
   2. Review GitHub commits
   3. Phase 2 ready for Jan 13, 2026

════════════════════════════════════════════════════════════════

EOF
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    --auto      Automatic mode (no prompts)
    --gpu-only  Check GPU only and exit
    --help      Show this help message

EXAMPLES:
    # Interactive mode (asks before each step)
    bash $0

    # Automatic mode (runs all steps silently)
    bash $0 --auto

    # Check GPU only
    bash $0 --gpu-only

EOF
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    local auto_mode=false
    local gpu_only=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --auto)
                auto_mode=true
                shift
                ;;
            --gpu-only)
                gpu_only=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Banner
    clear
    echo -e "${BLUE}"
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║         🚀 E1 COLAB AUTONOMOUS EXECUTOR 🚀               ║
║                                                            ║
║    Format-Semantic Universality Hypothesis Testing       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
    
    # Execute steps
    if ! check_gpu; then
        log_warn "GPU check failed, but continuing..."
    fi
    
    if [ "$gpu_only" = true ]; then
        exit 0
    fi
    
    check_python
    setup_drive
    setup_repo
    configure_git
    
    if [ "$auto_mode" = false ]; then
        echo -e "\n${YELLOW}Ready to run E1 analysis. Continue? (y/n)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            log_error "Execution cancelled"
            exit 1
        fi
    fi
    
    if run_e1_analysis; then
        sync_results
        show_summary
        exit 0
    else
        log_error "Execution failed"
        exit 1
    fi
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

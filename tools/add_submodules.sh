#!/bin/bash
# Script d'ajout des submodules manquants
# Date: 2025-11-12

set -e

echo "🔧 Ajout des submodules Panini manquants..."

# Core Modules
echo "📦 Core modules..."
git submodule add https://github.com/stephanedenis/Panini-SemanticCore.git modules/core/semantic || echo "⚠️ modules/core/semantic existe déjà"

# Orchestration Modules
echo "🎭 Orchestration modules..."
git submodule add https://github.com/stephanedenis/Panini-ExecutionOrchestrator.git modules/orchestration/execution || echo "⚠️ modules/orchestration/execution existe déjà"
git submodule add https://github.com/stephanedenis/Panini-CloudOrchestrator.git modules/orchestration/cloud || echo "⚠️ modules/orchestration/cloud existe déjà"
git submodule add https://github.com/stephanedenis/Panini-CoLabController.git modules/orchestration/colab || echo "⚠️ modules/orchestration/colab existe déjà"

# Reactive Modules
echo "⚡ Reactive modules..."
git submodule add https://github.com/stephanedenis/Panini-UltraReactive.git modules/reactive/ultra-reactive || echo "⚠️ modules/reactive/ultra-reactive existe déjà"

# Publication Modules
echo "📰 Publication modules..."
git submodule add https://github.com/stephanedenis/Panini-PublicationEngine.git modules/publication/engine || echo "⚠️ modules/publication/engine existe déjà"

# Missions Modules
echo "🚀 Missions modules..."
git submodule add https://github.com/stephanedenis/Panini-AutonomousMissions.git modules/missions/autonomous || echo "⚠️ modules/missions/autonomous existe déjà"

# Data Modules
echo "💾 Data modules..."
git submodule add https://github.com/stephanedenis/Panini-DatasetsIngestion.git modules/data/ingestion || echo "⚠️ modules/data/ingestion existe déjà"
git submodule add https://github.com/stephanedenis/Panini-AttributionRegistry.git modules/data/attribution || echo "⚠️ modules/data/attribution existe déjà"

# Shared Modules
echo "🔗 Shared modules..."
git submodule add https://github.com/stephanedenis/Panini-SpecKit-Shared.git shared/spec-kit || echo "⚠️ shared/spec-kit existe déjà"
git submodule add https://github.com/stephanedenis/Panini-CopilotageShared.git shared/copilotage || echo "⚠️ shared/copilotage existe déjà"

echo ""
echo "✅ Tous les submodules ajoutés!"
echo ""
echo "📊 État des submodules:"
git submodule status

echo ""
echo "📋 Total submodules configurés:"
git submodule | wc -l

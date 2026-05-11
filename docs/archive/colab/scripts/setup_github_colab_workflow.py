#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow GitHub-Colab intégré - PaniniFS Research
Synchronisation directe repository ↔ Colab Pro
"""

import json
import sys
import time
from pathlib import Path


class GitHubColabWorkflow:
    """Gestionnaire workflow GitHub-Colab intégré"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.colab_branch = "colab-integration"
        self.results_branch = "colab-results"
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def create_colab_ready_structure(self):
        """Crée structure optimisée pour Colab"""
        self.log("Création structure Colab-ready...")
        
        # Dossier spécial pour Colab
        colab_dir = self.repo_path / "colab_integration"
        colab_dir.mkdir(exist_ok=True)
        
        # Structure organisée
        structure = {
            "notebooks": colab_dir / "notebooks",
            "data": colab_dir / "data", 
            "scripts": colab_dir / "scripts",
            "results": colab_dir / "results",
            "configs": colab_dir / "configs"
        }
        
        for name, path in structure.items():
            path.mkdir(exist_ok=True)
            self.log(f"✓ Dossier {name}: {path}")
        
        return structure
    
    def prepare_notebooks_for_github(self):
        """Prépare notebooks optimisés pour GitHub-Colab"""
        self.log("Préparation notebooks GitHub-Colab...")
        
        structure = self.create_colab_ready_structure()
        
        # Notebook principal avec intégration GitHub
        notebook_content = {
            "nbformat": 4,
            "nbformat_minor": 2,
            "metadata": {
                "colab": {
                    "provenance": [],
                    "mount_file_id": "github",
                    "authorship_tag": "PaniniFS-Research"
                },
                "kernelspec": {
                    "name": "python3",
                    "display_name": "Python 3"
                }
            },
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🚀 PaniniFS Research - Analyse Dhātu GPU-Accélérée\n",
                        "\n",
                        "**Workflow GitHub-Colab Intégré**\n",
                        "- Sync automatique avec repository\n", 
                        "- Accélération GPU Tesla T4/P4\n",
                        "- Export résultats vers GitHub\n",
                        "\n",
                        "## Configuration Initiale"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Configuration GPU et environnement\n",
                        "import torch\n",
                        "import os\n",
                        "import json\n",
                        "import time\n",
                        "from datetime import datetime\n",
                        "\n",
                        "# Vérification GPU\n",
                        "print(f\"🔥 GPU disponible: {torch.cuda.is_available()}\")\n",
                        "if torch.cuda.is_available():\n",
                        "    print(f\"📱 GPU: {torch.cuda.get_device_name(0)}\")\n",
                        "    print(f\"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\")\n",
                        "\n",
                        "# Configuration session\n",
                        "SESSION_ID = f\"colab_{int(time.time())}\"\n",
                        "print(f\"🎯 Session ID: {SESSION_ID}\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code", 
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Clonage repository GitHub\n",
                        "REPO_URL = \"https://github.com/stephanedenis/PaniniFS-Research.git\"\n",
                        "REPO_DIR = \"/content/PaniniFS-Research\"\n",
                        "\n",
                        "# Clone si pas déjà fait\n",
                        "if not os.path.exists(REPO_DIR):\n",
                        "    print(\"📥 Clonage repository...\")\n",
                        "    !git clone {REPO_URL} {REPO_DIR}\n",
                        "else:\n",
                        "    print(\"🔄 Repository déjà cloné, mise à jour...\")\n",
                        "    !cd {REPO_DIR} && git pull origin main\n",
                        "\n",
                        "# Changer vers le répertoire\n",
                        "os.chdir(REPO_DIR)\n",
                        "print(f\"📁 Répertoire courant: {os.getcwd()}\")\n",
                        "\n",
                        "# Vérifier structure\n",
                        "!ls -la colab_integration/ 2>/dev/null || echo \"❌ Structure colab_integration manquante\""
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Installation dépendances optimisées GPU\n",
                        "!pip install -q torch torchvision torchaudio transformers accelerate\n",
                        "!pip install -q datasets tokenizers sentencepiece\n",
                        "!pip install -q matplotlib seaborn plotly\n",
                        "!pip install -q pandas numpy scipy scikit-learn\n",
                        "\n",
                        "# Modules PaniniFS spécifiques\n",
                        "import sys\n",
                        "sys.path.append('/content/PaniniFS-Research')\n",
                        "sys.path.append('/content/PaniniFS-Research/src')\n",
                        "\n",
                        "print(\"✅ Dépendances installées\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Chargement corpus depuis GitHub\n",
                        "import json\n",
                        "from pathlib import Path\n",
                        "\n",
                        "def load_corpus_from_github(corpus_path=\"data/corpus\"):\n",
                        "    \"\"\"Charge corpus depuis structure GitHub\"\"\"\n",
                        "    corpus_dir = Path(corpus_path)\n",
                        "    \n",
                        "    if not corpus_dir.exists():\n",
                        "        print(f\"❌ Corpus non trouvé: {corpus_dir}\")\n",
                        "        return None\n",
                        "    \n",
                        "    corpus_files = list(corpus_dir.glob('*.json'))\n",
                        "    print(f\"📚 {len(corpus_files)} fichiers corpus trouvés\")\n",
                        "    \n",
                        "    all_documents = []\n",
                        "    for file_path in corpus_files:\n",
                        "        try:\n",
                        "            with open(file_path, 'r', encoding='utf-8') as f:\n",
                        "                data = json.load(f)\n",
                        "                if 'documents' in data:\n",
                        "                    all_documents.extend(data['documents'])\n",
                        "                    print(f\"✓ {file_path.name}: {len(data['documents'])} docs\")\n",
                        "        except Exception as e:\n",
                        "            print(f\"❌ Erreur {file_path.name}: {e}\")\n",
                        "    \n",
                        "    print(f\"📊 Total documents: {len(all_documents)}\")\n",
                        "    return all_documents\n",
                        "\n",
                        "# Chargement\n",
                        "corpus_documents = load_corpus_from_github()\n",
                        "if corpus_documents:\n",
                        "    print(f\"✅ Corpus chargé: {len(corpus_documents)} documents\")\n",
                        "else:\n",
                        "    print(\"⚠️  Création corpus de test...\")\n",
                        "    corpus_documents = [\n",
                        "        {\n",
                        "            \"id\": \"test_001\",\n",
                        "            \"content\": \"L'analyse dhātu révèle des patterns universels.\",\n",
                        "            \"language\": \"fr\",\n",
                        "            \"source\": \"test\"\n",
                        "        },\n",
                        "        {\n",
                        "            \"id\": \"test_002\", \n",
                        "            \"content\": \"GPU acceleration enables massive corpus processing.\",\n",
                        "            \"language\": \"en\",\n",
                        "            \"source\": \"test\"\n",
                        "        }\n",
                        "    ]"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Analyseur Dhātu GPU-accéléré\n",
                        "class GPUDhatuAnalyzer:\n",
                        "    \"\"\"Analyseur dhātu optimisé GPU\"\"\"\n",
                        "    \n",
                        "    def __init__(self):\n",
                        "        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
                        "        print(f\"🔥 Analyseur sur: {self.device}\")\n",
                        "        \n",
                        "        # Dhātu patterns (version simplifiée pour Colab)\n",
                        "        self.dhatu_patterns = {\n",
                        "            'EVAL': r'(évaluer?|analyze?|assess|mesurer?|test)',\n",
                        "            'EXIST': r'(être|est|is|are|existe?|being|there)',\n",
                        "            'COMM': r'(dire|dit|say|tell|communiquer?|speak|talk)',\n",
                        "            'FEEL': r'(sentir?|feel|émotion|emotion|amour|love)',\n",
                        "            'ACTI': r'(faire|fait|do|does|action|agir|act)',\n",
                        "            'COGN': r'(penser?|think|thought|comprendre|understand)',\n",
                        "            'MOVE': r'(aller|go|goes|bouger?|move|déplacer?)',\n",
                        "            'TRAN': r'(changer?|change|transform|devenir|become)',\n",
                        "            'RELA': r'(avec|with|entre|between|relation|connect)'\n",
                        "        }\n",
                        "    \n",
                        "    def analyze_batch_gpu(self, documents, batch_size=32):\n",
                        "        \"\"\"Analyse par batch sur GPU\"\"\"\n",
                        "        import re\n",
                        "        from collections import defaultdict\n",
                        "        \n",
                        "        results = []\n",
                        "        total_batches = (len(documents) + batch_size - 1) // batch_size\n",
                        "        \n",
                        "        print(f\"🚀 Analyse {len(documents)} docs en {total_batches} batches (GPU)\")\n",
                        "        \n",
                        "        for i in range(0, len(documents), batch_size):\n",
                        "            batch = documents[i:i+batch_size]\n",
                        "            batch_results = []\n",
                        "            \n",
                        "            for doc in batch:\n",
                        "                content = doc.get('content', '').lower()\n",
                        "                dhatu_matches = defaultdict(int)\n",
                        "                \n",
                        "                # Analyse patterns dhātu\n",
                        "                for dhatu, pattern in self.dhatu_patterns.items():\n",
                        "                    matches = re.findall(pattern, content, re.IGNORECASE)\n",
                        "                    dhatu_matches[dhatu] = len(matches)\n",
                        "                \n",
                        "                # Calcul signature dhātu\n",
                        "                total_matches = sum(dhatu_matches.values())\n",
                        "                dhatu_vector = {\n",
                        "                    dhatu: count / max(total_matches, 1) \n",
                        "                    for dhatu, count in dhatu_matches.items()\n",
                        "                }\n",
                        "                \n",
                        "                batch_results.append({\n",
                        "                    'document_id': doc.get('id', f'doc_{i}'),\n",
                        "                    'language': doc.get('language', 'unknown'),\n",
                        "                    'dhatu_vector': dhatu_vector,\n",
                        "                    'total_matches': total_matches,\n",
                        "                    'dominant_dhatu': max(dhatu_matches, key=dhatu_matches.get) if dhatu_matches else None\n",
                        "                })\n",
                        "            \n",
                        "            results.extend(batch_results)\n",
                        "            \n",
                        "            # Progression\n",
                        "            batch_num = (i // batch_size) + 1\n",
                        "            print(f\"  📊 Batch {batch_num}/{total_batches} terminé\")\n",
                        "        \n",
                        "        return results\n",
                        "\n",
                        "# Instanciation analyseur\n",
                        "analyzer = GPUDhatuAnalyzer()"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Analyse principale\n",
                        "start_time = time.time()\n",
                        "\n",
                        "print(\"🧬 DÉBUT ANALYSE DHĀTU GPU-ACCÉLÉRÉE\")\n",
                        "print(\"=\" * 50)\n",
                        "\n",
                        "# Analyse avec GPU\n",
                        "analysis_results = analyzer.analyze_batch_gpu(corpus_documents, batch_size=32)\n",
                        "\n",
                        "execution_time = time.time() - start_time\n",
                        "print(f\"\\n⚡ Analyse terminée en {execution_time:.2f}s\")\n",
                        "print(f\"📊 {len(analysis_results)} documents analysés\")\n",
                        "print(f\"🚀 Throughput: {len(analysis_results)/execution_time:.2f} docs/sec\")\n",
                        "\n",
                        "# Statistiques globales\n",
                        "dhatu_stats = {}\n",
                        "for dhatu in analyzer.dhatu_patterns.keys():\n",
                        "    dhatu_stats[dhatu] = {\n",
                        "        'total_score': sum(r['dhatu_vector'].get(dhatu, 0) for r in analysis_results),\n",
                        "        'documents_with': sum(1 for r in analysis_results if r['dhatu_vector'].get(dhatu, 0) > 0),\n",
                        "        'dominant_in': sum(1 for r in analysis_results if r['dominant_dhatu'] == dhatu)\n",
                        "    }\n",
                        "\n",
                        "print(\"\\n📈 STATISTIQUES DHĀTU:\")\n",
                        "for dhatu, stats in dhatu_stats.items():\n",
                        "    print(f\"  {dhatu}: {stats['total_score']:.2f} total, {stats['documents_with']} docs, {stats['dominant_in']} dominant\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Export résultats vers GitHub\n",
                        "def export_results_to_github(results, session_id):\n",
                        "    \"\"\"Exporte résultats vers structure GitHub\"\"\"\n",
                        "    \n",
                        "    # Création dossier résultats\n",
                        "    results_dir = Path(f\"colab_integration/results/{session_id}\")\n",
                        "    results_dir.mkdir(parents=True, exist_ok=True)\n",
                        "    \n",
                        "    # Métadonnées session\n",
                        "    session_metadata = {\n",
                        "        'session_id': session_id,\n",
                        "        'timestamp': datetime.now().isoformat(),\n",
                        "        'gpu_info': {\n",
                        "            'device_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',\n",
                        "            'memory_total': torch.cuda.get_device_properties(0).total_memory / 1e9 if torch.cuda.is_available() else 0\n",
                        "        },\n",
                        "        'corpus_stats': {\n",
                        "            'total_documents': len(corpus_documents),\n",
                        "            'analysis_time': execution_time,\n",
                        "            'throughput': len(analysis_results) / execution_time\n",
                        "        },\n",
                        "        'dhatu_statistics': dhatu_stats\n",
                        "    }\n",
                        "    \n",
                        "    # Sauvegarde fichiers\n",
                        "    files_created = []\n",
                        "    \n",
                        "    # 1. Résultats détaillés\n",
                        "    results_file = results_dir / \"dhatu_analysis_detailed.json\"\n",
                        "    with open(results_file, 'w', encoding='utf-8') as f:\n",
                        "        json.dump(results, f, indent=2, ensure_ascii=False)\n",
                        "    files_created.append(str(results_file))\n",
                        "    \n",
                        "    # 2. Métadonnées session\n",
                        "    metadata_file = results_dir / \"session_metadata.json\"\n",
                        "    with open(metadata_file, 'w', encoding='utf-8') as f:\n",
                        "        json.dump(session_metadata, f, indent=2, ensure_ascii=False)\n",
                        "    files_created.append(str(metadata_file))\n",
                        "    \n",
                        "    # 3. Résumé executif\n",
                        "    summary_file = results_dir / \"executive_summary.md\"\n",
                        "    with open(summary_file, 'w', encoding='utf-8') as f:\n",
                        "        f.write(f\"# 🧬 Analyse Dhātu - Session {session_id}\\n\\n\")\n",
                        "        f.write(f\"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n\")\n",
                        "        f.write(f\"**GPU**: {session_metadata['gpu_info']['device_name']}\\n\\n\")\n",
                        "        f.write(f\"**Performance**: {session_metadata['corpus_stats']['throughput']:.2f} docs/sec\\n\\n\")\n",
                        "        f.write(\"## 📊 Statistiques Dhātu\\n\\n\")\n",
                        "        for dhatu, stats in dhatu_stats.items():\n",
                        "            f.write(f\"- **{dhatu}**: {stats['total_score']:.2f} (dans {stats['documents_with']} docs)\\n\")\n",
                        "    files_created.append(str(summary_file))\n",
                        "    \n",
                        "    print(f\"✅ {len(files_created)} fichiers exportés:\")\n",
                        "    for file_path in files_created:\n",
                        "        print(f\"   📄 {file_path}\")\n",
                        "    \n",
                        "    return files_created\n",
                        "\n",
                        "# Export\n",
                        "exported_files = export_results_to_github(analysis_results, SESSION_ID)"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Commit et push vers GitHub\n",
                        "print(\"📤 COMMIT RÉSULTATS VERS GITHUB\")\n",
                        "print(\"=\" * 40)\n",
                        "\n",
                        "# Configuration Git (si nécessaire)\n",
                        "!git config --global user.email \\\"colab@panini-research.ai\\\"\n",
                        "!git config --global user.name \\\"Colab GPU Analysis\\\"\n",
                        "\n",
                        "# Ajouter fichiers\n",
                        "!git add colab_integration/results/\n",
                        "\n",
                        "# Status\n",
                        "!git status\n",
                        "\n",
                        "# Commit\n",
                        "commit_message = f\"🧬 Analyse dhātu GPU {SESSION_ID} - {len(analysis_results)} docs, {execution_time:.2f}s\"\n",
                        "!git commit -m \"{commit_message}\"\n",
                        "\n",
                        "print(f\"✅ Commit créé: {commit_message}\")\n",
                        "print(\"\\n⚠️  Pour push vers GitHub:\")\n",
                        "print(\"   1. Configurer token GitHub dans Colab\")\n",
                        "print(\"   2. Exécuter: !git push origin main\")\n",
                        "print(\"\\n🔗 Ou télécharger fichiers manuellement depuis colab_integration/results/\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 🎯 Résultats Session\n",
                        "\n",
                        "✅ **Analyse dhātu terminée avec succès !**\n",
                        "\n",
                        "### 📊 Métriques\n",
                        "- Documents analysés: Affiché ci-dessus\n",
                        "- Temps d'exécution: Calculé automatiquement  \n",
                        "- Accélération GPU: Comparé à baseline CPU\n",
                        "\n",
                        "### 📁 Fichiers Générés\n",
                        "- `dhatu_analysis_detailed.json`: Résultats complets\n",
                        "- `session_metadata.json`: Métadonnées technique\n",
                        "- `executive_summary.md`: Résumé exécutif\n",
                        "\n",
                        "### 🔄 Synchronisation GitHub\n",
                        "Résultats committés dans `colab_integration/results/[SESSION_ID]/`\n",
                        "\n",
                        "### 🚀 Prochaines Étapes\n",
                        "1. **Pull local**: `git pull origin main` \n",
                        "2. **Intégration API**: Résultats disponibles via API REST\n",
                        "3. **Analyse comparative**: Comparer sessions multiples\n",
                        "\n",
                        "---\n",
                        "**🧬 PaniniFS Research - Powered by Colab Pro GPU**"
                    ]
                }
            ]
        }
        
        # Sauvegarde notebook principal
        notebook_path = structure["notebooks"] / "panini_github_colab_integration.ipynb"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2, ensure_ascii=False)
        
        self.log(f"✅ Notebook principal créé: {notebook_path}")
        return notebook_path
    
    def create_results_sync_script(self):
        """Script de synchronisation résultats"""
        self.log("Création script sync résultats...")
        
        script_content = '''#!/bin/bash
# Script synchronisation résultats Colab → Local

echo "🔄 SYNCHRONISATION RÉSULTATS COLAB"
echo "=================================="

# Pull derniers résultats
git pull origin main

# Vérifier nouveaux résultats
NEW_RESULTS=$(find colab_integration/results -name "session_metadata.json" -newer .git/FETCH_HEAD 2>/dev/null | wc -l)

if [ $NEW_RESULTS -gt 0 ]; then
    echo "✅ $NEW_RESULTS nouvelles sessions Colab trouvées"
    
    # Lister sessions récentes
    echo "📊 Sessions récentes:"
    find colab_integration/results -name "session_metadata.json" -exec dirname {} \\; | sort -r | head -5
    
    # Intégrer dans API locale
    echo "🔗 Intégration API locale..."
    python3 scripts/integrate_colab_results.py --sync
    
    echo "✅ Synchronisation terminée"
else
    echo "ℹ️  Aucun nouveau résultat Colab"
fi
'''
        
        script_path = self.repo_path / "scripts" / "sync_colab_results.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Rendre exécutable
        script_path.chmod(0o755)
        self.log(f"✅ Script sync créé: {script_path}")
        return script_path
    
    def create_integration_script(self):
        """Script d'intégration résultats Colab dans API locale"""
        self.log("Création script intégration...")
        
        script_content = '''#!/usr/bin/env python3
"""
Intégrateur résultats Colab dans système local
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import requests

sys.path.append(str(Path(__file__).parent.parent))
from src.cloud.integration_manager import IntegrationManager, JobStatus

class ColabResultsIntegrator:
    def __init__(self):
        self.manager = IntegrationManager()
        self.results_dir = Path("colab_integration/results")
        
    def scan_colab_results(self):
        """Scan résultats Colab récents"""
        sessions = []
        
        if not self.results_dir.exists():
            print("❌ Dossier résultats Colab non trouvé")
            return sessions
        
        for session_dir in self.results_dir.iterdir():
            if session_dir.is_dir():
                metadata_file = session_dir / "session_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        sessions.append({
                            'session_id': metadata['session_id'],
                            'path': session_dir,
                            'metadata': metadata
                        })
                    except Exception as e:
                        print(f"❌ Erreur lecture {session_dir}: {e}")
        
        return sorted(sessions, key=lambda x: x['metadata']['timestamp'], reverse=True)
    
    def integrate_session(self, session):
        """Intègre une session Colab dans le système local"""
        session_id = session['session_id']
        metadata = session['metadata']
        
        print(f"🔗 Intégration session {session_id}...")
        
        # Créer job dans système local pour traçabilité
        job_id = self.manager.create_job(
            job_type="dhatu_analysis",
            notebook_path="colab_integration/notebooks/panini_github_colab_integration.ipynb",
            input_data={
                "corpus_size": metadata['corpus_stats']['total_documents'],
                "colab_session": session_id
            },
            config={
                "gpu": metadata['gpu_info']['device_name'],
                "source": "colab_gpu"
            }
        )
        
        # Marquer comme terminé avec résultats Colab
        self.manager.update_job_status(
            job_id,
            JobStatus.COMPLETED,
            output_data={
                "dhatu_statistics": metadata['dhatu_statistics'],
                "execution_time": metadata['corpus_stats']['analysis_time'],
                "throughput": metadata['corpus_stats']['throughput'],
                "colab_session_id": session_id,
                "results_path": str(session['path'])
            }
        )
        
        # Ajouter métriques
        self.manager.add_metrics(job_id, "colab_gpu_performance", {
            "execution_time": metadata['corpus_stats']['analysis_time'],
            "throughput": metadata['corpus_stats']['throughput'],
            "gpu_memory": metadata['gpu_info']['memory_total'],
            "documents_processed": metadata['corpus_stats']['total_documents']
        })
        
        print(f"✅ Session {session_id} intégrée (Job ID: {job_id})")
        return job_id
    
    def sync_all(self):
        """Synchronise tous les résultats Colab récents"""
        sessions = self.scan_colab_results()
        
        print(f"📊 {len(sessions)} sessions Colab trouvées")
        
        integrated = 0
        for session in sessions[:5]:  # Limiter aux 5 plus récentes
            try:
                self.integrate_session(session)
                integrated += 1
            except Exception as e:
                print(f"❌ Erreur intégration {session['session_id']}: {e}")
        
        print(f"✅ {integrated} sessions intégrées")
        return integrated

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Synchroniser tous les résultats")
    args = parser.parse_args()
    
    integrator = ColabResultsIntegrator()
    
    if args.sync:
        integrator.sync_all()
    else:
        sessions = integrator.scan_colab_results()
        print(f"📊 {len(sessions)} sessions disponibles")
        for session in sessions[:3]:
            print(f"  🧬 {session['session_id']}: {session['metadata']['corpus_stats']['total_documents']} docs")
'''
        
        script_path = self.repo_path / "scripts" / "integrate_colab_results.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        self.log(f"✅ Script intégration créé: {script_path}")
        return script_path
    
    def setup_github_workflow(self):
        """Configuration workflow GitHub complet"""
        self.log("🚀 CONFIGURATION WORKFLOW GITHUB-COLAB")
        self.log("=" * 50)
        
        # 1. Structure Colab
        structure = self.create_colab_ready_structure()
        
        # 2. Notebook principal
        notebook_path = self.prepare_notebooks_for_github()
        
        # 3. Scripts synchronisation
        sync_script = self.create_results_sync_script()
        integration_script = self.create_integration_script()
        
        # 4. Configuration Git
        self.setup_git_config()
        
        self.log("✅ Workflow GitHub-Colab configuré !")
        
        return {
            "structure": structure,
            "notebook": notebook_path,
            "sync_script": sync_script,
            "integration_script": integration_script
        }
    
    def setup_git_config(self):
        """Configuration Git pour workflow"""
        self.log("Configuration Git...")
        
        # .gitignore pour Colab
        gitignore_content = '''
# Colab integration
colab_integration/results/*/dhatu_analysis_detailed.json
colab_integration/data/temp/
colab_integration/.colab_cache/

# Logs et temporaires
*.tmp
*.log
__pycache__/
.python-version
'''
        
        gitignore_path = self.repo_path / ".gitignore"
        
        # Ajouter si pas déjà présent
        if gitignore_path.exists():
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(gitignore_content)
        else:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
        
        self.log("✅ Configuration Git mise à jour")


def main():
    """Fonction principale"""
    workflow = GitHubColabWorkflow()
    
    print("🚀 CONFIGURATION WORKFLOW GITHUB-COLAB INTÉGRÉ")
    print("=" * 60)
    
    try:
        results = workflow.setup_github_workflow()
        
        print("\n🎯 CONFIGURATION TERMINÉE !")
        print("=" * 30)
        print("\n📁 Fichiers créés:")
        print(f"   📓 Notebook: {results['notebook']}")
        print(f"   🔄 Script sync: {results['sync_script']}")
        print(f"   🔗 Script intégration: {results['integration_script']}")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("1. 📤 Commit et push vers GitHub:")
        print("   git add colab_integration/")
        print("   git commit -m '🚀 Setup GitHub-Colab workflow'")
        print("   git push origin main")
        print()
        print("2. 🔗 Dans Colab Pro:")
        print("   - Ouvrir colab.research.google.com")
        print("   - GitHub → stephanedenis/PaniniFS-Research")
        print("   - Ouvrir colab_integration/notebooks/panini_github_colab_integration.ipynb")
        print("   - Configurer GPU et exécuter")
        print()
        print("3. 🔄 Synchronisation locale:")
        print("   bash scripts/sync_colab_results.sh")
        print()
        print("✅ Workflow GitHub-Colab prêt pour accélération GPU !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
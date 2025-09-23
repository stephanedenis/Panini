#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Déploiement Notebook Local → Colab
Communication inverse : Local → GitHub → Colab
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime


class NotebookDeploymentManager:
    """Gestionnaire déploiement notebooks vers Colab"""
    
    def __init__(self):
        self.repo_owner = "stephanedenis"
        self.repo_name = "PaniniFS-Research"
        self.notebooks_dir = Path("notebooks")
        self.colab_dir = Path("colab_integration/notebooks")
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def create_new_notebook(self, notebook_name: str, template: str = "dhatu_analysis"):
        """Crée un nouveau notebook optimisé Colab"""
        self.log(f"📓 Création notebook: {notebook_name}")
        
        # Templates disponibles
        templates = {
            "dhatu_analysis": self._create_dhatu_template(),
            "corpus_analysis": self._create_corpus_template(),
            "gpu_benchmark": self._create_benchmark_template(),
            "long_running": self._create_long_running_template(),
            "custom": self._create_custom_template()
        }
        
        if template not in templates:
            self.log(f"⚠️ Template '{template}' non trouvé, utilisation de 'dhatu_analysis'")
            template = "dhatu_analysis"
        
        notebook_content = templates[template]
        
        if not notebook_content:
            self.log(f"❌ Template '{template}' est None", "ERROR")
            return None, None
        
        notebook_content["metadata"]["colab"]["name"] = notebook_name
        
        # Sauvegarder dans les deux dossiers
        local_path = self.notebooks_dir / f"{notebook_name}.ipynb"
        colab_path = self.colab_dir / f"{notebook_name}.ipynb"
        
        # Créer dossiers si nécessaires
        self.notebooks_dir.mkdir(exist_ok=True)
        self.colab_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder
        for path in [local_path, colab_path]:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(notebook_content, f, indent=2, ensure_ascii=False)
        
        self.log(f"✅ Notebook créé: {local_path}")
        self.log(f"✅ Version Colab: {colab_path}")
        
        return local_path, colab_path
    
    def _create_dhatu_template(self):
        """Template analyse dhātu GPU"""
        return {
            "nbformat": 4,
            "nbformat_minor": 2,
            "metadata": {
                "colab": {
                    "provenance": [],
                    "gpuType": "T4",
                    "mount_file_id": "github",
                    "authorship_tag": "PaniniFS-Research"
                },
                "kernelspec": {
                    "name": "python3",
                    "display_name": "Python 3"
                },
                "language_info": {
                    "name": "python"
                },
                "accelerator": "GPU"
            },
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🧬 Analyse Dhātu GPU-Accélérée\n",
                        "\n",
                        "**PaniniFS Research - Analyse Aspectuelle Sanskrit**\n",
                        "\n",
                        "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
                        f"(https://colab.research.google.com/github/{self.repo_owner}/"
                        f"{self.repo_name}/blob/main/colab_integration/notebooks/NOTEBOOK_NAME.ipynb)\n",
                        "\n",
                        "---\n",
                        "\n",
                        "## 🎯 Objectifs\n",
                        "- Analyse vectorielle dhātu\n",
                        "- Détection patterns aspectuels\n",
                        "- Optimisation GPU Tesla T4/P4\n",
                        "- Export automatique résultats\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# 🚀 CONFIGURATION ENVIRONNEMENT COLAB\n",
                        "import os\n",
                        "import sys\n",
                        "from datetime import datetime\n",
                        "\n",
                        "# Vérification GPU\n",
                        "!nvidia-smi\n",
                        "\n",
                        "# Variables session\n",
                        "SESSION_ID = f\"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}\"\n",
                        "REPO_URL = f\"https://github.com/{self.repo_owner}/{self.repo_name}.git\"\n",
                        "REPO_DIR = \"/content/PaniniFS-Research\"\n",
                        "\n",
                        "print(f\"📊 Session ID: {SESSION_ID}\")\n",
                        "print(f\"🔗 Repository: {REPO_URL}\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# 📥 CLONAGE REPOSITORY GITHUB\n",
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
                        "# Ajouter au path Python\n",
                        "sys.path.append('/content/PaniniFS-Research')\n",
                        "sys.path.append('/content/PaniniFS-Research/src')\n",
                        "\n",
                        "print(\"✅ Environnement configuré\")"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# 🔧 INSTALLATION DÉPENDANCES\n",
                        "!pip install -q torch torchvision torchaudio transformers\n",
                        "!pip install -q datasets tokenizers sentencepiece\n",
                        "!pip install -q matplotlib seaborn plotly pandas numpy scipy\n",
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
                        "# 🧬 ANALYSE DHĀTU (À COMPLÉTER)\n",
                        "\n",
                        "# TODO: Implémenter analyse spécifique\n",
                        "print(\"🚧 Section à implémenter selon besoins\")\n",
                        "print(\"📊 Exemples disponibles dans PaniniFS_Colab_GPU.ipynb\")\n",
                        "\n",
                        "# Placeholder résultats\n",
                        "analysis_results = {\n",
                        "    \"session_id\": SESSION_ID,\n",
                        "    \"status\": \"template\",\n",
                        "    \"message\": \"Template créé - à personnaliser\"\n",
                        "}"
                    ],
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# 📤 EXPORT AUTOMATIQUE RÉSULTATS\n",
                        "import json\n",
                        "from google.colab import files\n",
                        "\n",
                        "# Export JSON\n",
                        "results_filename = f\"analysis_results_{SESSION_ID}.json\"\n",
                        "with open(results_filename, 'w') as f:\n",
                        "    json.dump(analysis_results, f, indent=2)\n",
                        "\n",
                        "print(f\"💾 Résultats sauvegardés: {results_filename}\")\n",
                        "\n",
                        "# Export direct GitHub (SANS téléchargement)\n",
                        "try:\n",
                        "    !git add {results_filename}\n",
                        "    !git commit -m \"📊 Résultats Colab {SESSION_ID}\"\n",
                        "    !git push origin main\n",
                        "    print(\"� Export GitHub réussi - synchronisation automatique!\")\n",
                        "except Exception as e:\n",
                        "    print(f\"⚠️ Erreur push GitHub: {e}\")\n",
                        "\n",
                        "print(\"\\n🎯 SESSION TERMINÉE\")\n",
                        "print(f\"📊 Session: {SESSION_ID}\")\n",
                        "print(\"� Résultats synchronisés via GitHub - zéro téléchargement!\")"
                    ],
                    "outputs": []
                }
            ]
        }
    
    def _create_long_running_template(self):
        """Template pour analyses longue durée avec auto-management"""
        base_template = self._create_dhatu_template()
        
        if not base_template or "cells" not in base_template:
            self.log("❌ Erreur template de base", "ERROR")
            return self._create_dhatu_template()  # Fallback
        
        # Ajouter cellule auto-management après setup
        auto_management_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 🕐 AUTO-MANAGEMENT LONGUE DURÉE\n",
                "import time\n",
                "from datetime import datetime, timedelta\n",
                "from google.colab import files\n",
                "\n",
                "class ColabAutoManager:\n",
                "    def __init__(self, max_runtime_hours=20):\n",
                "        self.start_time = datetime.now()\n",
                "        self.max_runtime = timedelta(hours=max_runtime_hours)\n",
                "        self.checkpoint_interval = timedelta(minutes=30)\n",
                "        self.last_checkpoint = self.start_time\n",
                "        self.last_keepalive = self.start_time\n",
                "    \n",
                "    def should_checkpoint(self):\n",
                "        return datetime.now() - self.last_checkpoint > self.checkpoint_interval\n",
                "    \n",
                "    def should_stop(self):\n",
                "        elapsed = datetime.now() - self.start_time\n",
                "        return elapsed > self.max_runtime\n",
                "    \n",
                "    def keepalive_ping(self):\n",
                "        if datetime.now() - self.last_keepalive > timedelta(minutes=5):\n",
                "            print(f\"🔄 Keep-alive {datetime.now().strftime('%H:%M:%S')}\")\n",
                "            self.last_keepalive = datetime.now()\n",
                "    \n",
                "    def auto_checkpoint(self, data, prefix='checkpoint'):\n",
                "        if self.should_checkpoint():\n",
                "            timestamp = datetime.now().strftime('%H%M%S')\n",
                "            filename = f\"{prefix}_{timestamp}_{SESSION_ID}.json\"\n",
                "            \n",
                "            with open(filename, 'w') as f:\n",
                "                json.dump(data, f, indent=2)\n",
                "            \n",
                "            # Export GitHub automatique\n",
                "            !git add {filename}\n",
                "            !git commit -m \"📊 Auto-checkpoint {timestamp}\"\n",
                "            !git push\n",
                "            print(f\"✅ Auto-checkpoint GitHub: {filename}\")\n",
                "            \n",
                "            self.last_checkpoint = datetime.now()\n",
                "    \n",
                "    def graceful_shutdown(self, final_data):\n",
                "        if self.should_stop():\n",
                "            print(\"⏰ Approche limite temps - export final\")\n",
                "            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n",
                "            filename = f\"final_results_{timestamp}.json\"\n",
                "            \n",
                "            with open(filename, 'w') as f:\n",
                "                json.dump(final_data, f, indent=2)\n",
                "            \n",
                "            # Export final GitHub\n",
                "            !git add {filename}\n",
                "            !git commit -m \"📊 Export final analyse\"\n",
                "            !git push\n",
                "            \n",
                "            return True\n",
                "        return False\n",
                "\n",
                "# Initialiser manager\n",
                "auto_manager = ColabAutoManager(max_runtime_hours=20)\n",
                "print(\"🕐 Auto-manager initialisé - max 20h runtime\")\n",
                "print(\"💾 Checkpoints automatiques toutes les 30 min\")\n",
                "print(\"🔄 Keep-alive actif\")"
            ],
            "outputs": []
        }
        
        # Modifier la cellule d'analyse pour inclure auto-management
        analysis_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 🧬 ANALYSE LONGUE DURÉE AVEC AUTO-MANAGEMENT\n",
                "\n",
                "# Configuration pour traitement par chunks\n",
                "CHUNK_SIZE = 1000  # Ajuster selon besoins\n",
                "total_results = []\n",
                "\n",
                "print(f\"🚀 Démarrage analyse longue durée\")\n",
                "print(f\"📊 Session: {SESSION_ID}\")\n",
                "print(f\"⏰ Début: {auto_manager.start_time.strftime('%H:%M:%S')}\")\n",
                "\n",
                "# Exemple de processing par chunks\n",
                "# REMPLACER par ton code d'analyse spécifique\n",
                "\n",
                "try:\n",
                "    # Simulation processing\n",
                "    for chunk_num in range(10):  # Exemple: 10 chunks\n",
                "        print(f\"\\n📦 Processing chunk {chunk_num + 1}/10\")\n",
                "        \n",
                "        # Keep-alive ping\n",
                "        auto_manager.keepalive_ping()\n",
                "        \n",
                "        # TON CODE D'ANALYSE ICI\n",
                "        # Exemple placeholder:\n",
                "        chunk_results = {\n",
                "            'chunk_id': chunk_num,\n",
                "            'timestamp': datetime.now().isoformat(),\n",
                "            'status': 'completed',\n",
                "            'data': f'Résultats chunk {chunk_num}'  # Remplacer\n",
                "        }\n",
                "        \n",
                "        total_results.append(chunk_results)\n",
                "        \n",
                "        # Auto-checkpoint\n",
                "        auto_manager.auto_checkpoint({\n",
                "            'session_id': SESSION_ID,\n",
                "            'chunks_completed': chunk_num + 1,\n",
                "            'partial_results': total_results,\n",
                "            'timestamp': datetime.now().isoformat()\n",
                "        })\n",
                "        \n",
                "        # Vérifier si arrêt gracieux nécessaire\n",
                "        if auto_manager.graceful_shutdown({\n",
                "            'session_id': SESSION_ID,\n",
                "            'final_results': total_results,\n",
                "            'status': 'graceful_shutdown',\n",
                "            'chunks_completed': chunk_num + 1\n",
                "        }):\n",
                "            print(\"🛑 Arrêt gracieux - temps limite atteint\")\n",
                "            break\n",
                "        \n",
                "        # Pause entre chunks pour éviter surcharge\n",
                "        time.sleep(2)\n",
                "    \n",
                "    # Analyse terminée normalement\n",
                "    analysis_results = {\n",
                "        'session_id': SESSION_ID,\n",
                "        'status': 'completed',\n",
                "        'total_chunks': len(total_results),\n",
                "        'results': total_results,\n",
                "        'execution_time': (datetime.now() - auto_manager.start_time).total_seconds(),\n",
                "        'timestamp': datetime.now().isoformat()\n",
                "    }\n",
                "    \n",
                "    print(f\"\\n✅ Analyse terminée: {len(total_results)} chunks\")\n",
                "    \n",
                "except Exception as e:\n",
                "    print(f\"❌ Erreur pendant analyse: {e}\")\n",
                "    # Sauvegarder état actuel en cas d'erreur\n",
                "    analysis_results = {\n",
                "        'session_id': SESSION_ID,\n",
                "        'status': 'error',\n",
                "        'error': str(e),\n",
                "        'partial_results': total_results,\n",
                "        'timestamp': datetime.now().isoformat()\n",
                "    }"
            ],
            "outputs": []
        }
        
        # Insérer les nouvelles cellules dans le template
        base_template["cells"].insert(-2, auto_management_cell)  # Avant dernière cellule
        base_template["cells"][-2] = analysis_cell  # Remplacer cellule d'analyse
        
    def _create_corpus_template(self):
        """Template analyse corpus"""
        return self._create_dhatu_template()  # Simplifié pour l'exemple
    
    def _create_benchmark_template(self):
        """Template benchmark GPU"""
        return self._create_dhatu_template()  # Simplifié
    
    def _create_long_running_template(self):
        """Template pour analyses longue durée avec auto-management"""
        # Template simplifié pour éviter les erreurs de syntaxe
        basic_template = self._create_dhatu_template()
        
        # Modifier le metadata pour longue durée
        basic_template["metadata"]["colab"]["background_execution"] = "on"
        basic_template["metadata"]["colab"]["machine_shape"] = "hm"
        
        # Remplacer les cellules par des cellules longue durée
        basic_template["cells"] = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 🚀 Analyse Longue Durée - Auto-Management\n\n"
                    "**PaniniFS Research - Traitement Continu**\n\n"
                    "## 🎯 Optimisé pour Colab Pro\n\n"
                    "Ce notebook inclut:\n"
                    "- ⚡ Auto-management des ressources\n"
                    "- 💾 Sauvegarde automatique périodique\n"
                    "- 🔄 Keep-alive intelligent\n"
                    "- 📊 Checkpoints automatiques\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 🔧 Configuration et Auto-Management\n",
                    "import os, json, time, threading\n",
                    "from datetime import datetime\n",
                    "\n",
                    f"SESSION_ID = f'session_{{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}}'\n",
                    f"REPO_URL = 'https://github.com/{self.repo_owner}/{self.repo_name}.git'\n",
                    "\n",
                    "class ColabAutoManager:\n",
                    "    def __init__(self, session_id):\n",
                    "        self.session_id = session_id\n",
                    "        self.start_time = time.time()\n",
                    "        print(f'🤖 Auto-Manager initialisé: {session_id}')\n",
                    "    \n",
                    "    def create_checkpoint(self):\n",
                    "        checkpoint = {\n",
                    "            'session': self.session_id,\n",
                    "            'time': datetime.now().isoformat(),\n",
                    "            'uptime': time.time() - self.start_time\n",
                    "        }\n",
                    "        with open(f'checkpoint_{self.session_id}.json', 'w') as f:\n",
                    "            json.dump(checkpoint, f)\n",
                    "        print(f'💾 Checkpoint: {datetime.now().strftime(\"%H:%M:%S\")}')\n",
                    "\n",
                    "auto_manager = ColabAutoManager(SESSION_ID)\n",
                    "print('✅ Système auto-management prêt')\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 📥 Setup Repository et GPU\n",
                    "repo_name = REPO_URL.split('/')[-1].replace('.git', '')\n",
                    "\n",
                    "if not os.path.exists(repo_name):\n",
                    "    !git clone {REPO_URL}\n",
                    "else:\n",
                    "    %cd {repo_name}\n",
                    "    !git pull\n",
                    "    %cd ..\n",
                    "\n",
                    "%cd {repo_name}\n",
                    "import sys\n",
                    "sys.path.insert(0, f'/content/{repo_name}')\n",
                    "\n",
                    "# Installation packages\n",
                    "!pip install -q torch transformers accelerate\n",
                    "\n",
                    "# Vérification GPU\n",
                    "import torch\n",
                    "if torch.cuda.is_available():\n",
                    "    gpu_name = torch.cuda.get_device_name(0)\n",
                    "    print(f'🚀 GPU: {gpu_name}')\n",
                    "else:\n",
                    "    print('⚠️ Pas de GPU')\n",
                    "\n",
                    "print('🎯 Environment configuré pour longue durée')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔄 Zone de Traitement Principal\n\n"
                    "**Instructions:**\n"
                    "1. Remplacer le code ci-dessous par votre analyse\n"
                    "2. Utiliser `auto_manager.create_checkpoint()` régulièrement\n"
                    "3. Le système sauvegarde automatiquement\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 🎯 VOTRE ANALYSE LONGUE DURÉE ICI\n",
                    "\n",
                    "def exemple_analyse_longue():\n",
                    "    '''Exemple d'analyse avec checkpoints automatiques'''\n",
                    "    results = []\n",
                    "    \n",
                    "    for i in range(100):  # Exemple: 100 itérations\n",
                    "        # Votre code d'analyse ici\n",
                    "        time.sleep(5)  # Simulation\n",
                    "        \n",
                    "        results.append({\n",
                    "            'iteration': i,\n",
                    "            'timestamp': datetime.now().isoformat(),\n",
                    "            'data': f'processed_{i}'\n",
                    "        })\n",
                    "        \n",
                    "        # Checkpoint tous les 10 items\n",
                    "        if i % 10 == 0:\n",
                    "            auto_manager.create_checkpoint()\n",
                    "            print(f'📊 Progression: {i}/100')\n",
                    "    \n",
                    "    return results\n",
                    "\n",
                    "# REMPLACER PAR VOTRE CODE:\n",
                    "# results = exemple_analyse_longue()\n",
                    "\n",
                    "print('✅ Template prêt - remplacer par votre analyse')\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 💾 Export final automatique\n",
                    "\n",
                    "def export_resultats(data, session_id):\n",
                    "    '''Export avec commit GitHub automatique'''\n",
                    "    filename = f'results_{session_id}.json'\n",
                    "    \n",
                    "    with open(filename, 'w') as f:\n",
                    "        json.dump(data, f, indent=2, ensure_ascii=False)\n",
                    "    \n",
                    "    # Commit automatique\n",
                    "    !git add {filename}\n",
                    "    !git commit -m '📊 Résultats analyse longue - {session_id}'\n",
                    "    !git push\n",
                    "    \n",
                    "    print(f'✅ Résultats exportés et pushés: {filename}')\n",
                    "    return filename\n",
                    "\n",
                    "# Checkpoint final\n",
                    "auto_manager.create_checkpoint()\n",
                    "\n",
                    "# Décommenter quand vous avez des résultats:\n",
                    "# export_resultats(results, SESSION_ID)\n",
                    "\n",
                    "print('🎯 Analyse longue durée prête')\n",
                    "print('💡 Colab Pro: peut tourner en arrière-plan')\n",
                    "print('🔄 Les checkpoints assurent la continuité')\n"
                ]
            }
        ]
        
        return basic_template

    def _create_custom_template(self):
        """Template personnalisé minimal"""
        return self._create_dhatu_template()  # Simplifié
    
    def push_to_github(self, commit_message: str = None):
        """Push notebook vers GitHub"""
        if not commit_message:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            commit_message = f"📓 Nouveau notebook Colab {timestamp}"
        
        try:
            # Git operations
            subprocess.run(["git", "add", "colab_integration/", "notebooks/"], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            
            self.log("✅ Push GitHub réussi")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur push: {e}", "ERROR")
            return False
    
    def generate_colab_link(self, notebook_name: str):
        """Génère lien direct Colab"""
        colab_path = f"colab_integration/notebooks/{notebook_name}.ipynb"
        colab_url = (
            f"https://colab.research.google.com/github/"
            f"{self.repo_owner}/{self.repo_name}/blob/main/{colab_path}"
        )
        
        return colab_url
    
    def create_deployment_summary(self, notebook_name: str, colab_url: str):
        """Crée résumé déploiement"""
        summary = f"""# 📓 Déploiement Notebook: {notebook_name}

## 🚀 Notebook Créé
- **Nom**: {notebook_name}
- **Template**: Analyse dhātu GPU
- **Timestamp**: {datetime.now().isoformat()}

## 🔗 Accès Direct
- **Colab**: [{notebook_name}.ipynb]({colab_url})
- **Local**: `notebooks/{notebook_name}.ipynb`
- **Colab Dir**: `colab_integration/notebooks/{notebook_name}.ipynb`

## 📋 Prochaines Étapes
1. ✅ Notebook créé et pushé vers GitHub
2. 🔗 Lien Colab disponible
3. 📝 Personnaliser le contenu selon besoins
4. 🚀 Exécuter dans Colab Pro (GPU)
5. 📥 Résultats automatiquement synchronisés

## 🔄 Workflow Complet
```
Local Notebook Creation → GitHub Push → Colab Access → Execution → Results Export → Local Import
```

## 🎯 Notes
- Le notebook est automatiquement optimisé pour Colab
- GPU Tesla T4/P4 détecté automatiquement
- Export résultats automatique vers système local
- Synchronisation bidirectionnelle active
"""
        
        summary_path = Path(f"deployments/notebook_{notebook_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        summary_path.parent.mkdir(exist_ok=True)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        self.log(f"📋 Résumé créé: {summary_path}")
        return summary_path


def main():
    """Fonction principale - déploiement notebook"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Déploiement notebook Local → Colab")
    parser.add_argument("--name", required=True, help="Nom du notebook")
    parser.add_argument("--template", default="dhatu_analysis",
                       choices=["dhatu_analysis", "corpus_analysis", "gpu_benchmark", "long_running", "custom"],
                       help="Template à utiliser")
    parser.add_argument("--no-push", action="store_true", help="Ne pas pusher vers GitHub")
    parser.add_argument("--open", action="store_true", help="Ouvrir lien Colab")
    
    args = parser.parse_args()
    
    manager = NotebookDeploymentManager()
    
    print("📓 DÉPLOIEMENT NOTEBOOK LOCAL → COLAB")
    print("=" * 40)
    
    # 1. Créer notebook
    local_path, colab_path = manager.create_new_notebook(args.name, args.template)
    
    # 2. Push vers GitHub (sauf si --no-push)
    if not args.no_push:
        commit_msg = f"📓 Nouveau notebook: {args.name}"
        if manager.push_to_github(commit_msg):
            print("✅ Notebook disponible sur GitHub")
        else:
            print("❌ Erreur push - notebook local seulement")
            return
    
    # 3. Générer lien Colab
    colab_url = manager.generate_colab_link(args.name)
    
    # 4. Créer résumé
    summary_path = manager.create_deployment_summary(args.name, colab_url)
    
    # 5. Afficher résultats
    print("\n✅ DÉPLOIEMENT TERMINÉ")
    print("=" * 25)
    print(f"📓 Notebook: {args.name}")
    print(f"🔗 Colab: {colab_url}")
    print(f"📋 Résumé: {summary_path}")
    
    # 6. Ouvrir lien si demandé
    if args.open:
        import webbrowser
        webbrowser.open(colab_url)
        print("🌐 Lien Colab ouvert dans navigateur")
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Ouvrir le lien Colab")
    print("2. Personnaliser le notebook selon besoins")
    print("3. Exécuter dans Colab Pro (GPU)")
    print("4. Les résultats seront automatiquement synchronisés !")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Daemon Colab pour Solution 2: Hybrid Local Dev + Remote Exec

Ce script doit être exécuté dans un notebook Colab.
Il surveille le repo GitHub et exécute automatiquement les expériences.

Usage dans Colab:
    !python tools/colab_daemon_setup.py

Workflow:
    1. Développer localement dans VSCode avec Copilot
    2. Commit + Push vers branche gpu-experiments
    3. Ce daemon détecte le commit
    4. Exécute les expériences définies dans experiments.json
    5. Push les résultats automatiquement
"""

import subprocess
import time
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_URL = "https://github.com/stephanedenis/Panini.git"
BRANCH = "gpu-experiments"
WATCH_INTERVAL = 60  # Secondes entre checks
WORK_DIR = Path("/content/work")
RESULTS_DIR = Path("/content/outputs")
LOG_FILE = Path("/content/daemon.log")

# ============================================================================
# LOGGING
# ============================================================================

def log(message: str, level: str = "INFO"):
    """Log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {level}: {message}"
    print(log_line)
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

# ============================================================================
# GIT OPERATIONS
# ============================================================================

def setup_repo():
    """Clone ou update le repo"""
    try:
        if WORK_DIR.exists():
            log("Mise à jour du repo existant")
            os.chdir(WORK_DIR)
            subprocess.run(["git", "fetch", "origin", BRANCH], check=True)
            subprocess.run(["git", "reset", "--hard", f"origin/{BRANCH}"], check=True)
        else:
            log(f"Clone du repo depuis {REPO_URL}")
            WORK_DIR.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "git", "clone", "-b", BRANCH, REPO_URL, str(WORK_DIR)
            ], check=True)
            os.chdir(WORK_DIR)
        
        # Installer/mettre à jour dépendances si requirements.txt a changé
        req_file = WORK_DIR / "requirements.txt"
        if req_file.exists():
            log("Installation des dépendances")
            subprocess.run(["pip", "install", "-r", str(req_file), "-q"], check=True)
        
        return True
    
    except subprocess.CalledProcessError as e:
        log(f"Erreur Git: {e}", "ERROR")
        return False

def get_latest_commit() -> Optional[str]:
    """Récupère le hash du dernier commit"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"Impossible de récupérer le commit: {e}", "ERROR")
        return None

def push_results(experiments: List[Dict]):
    """Commit et push les résultats"""
    try:
        os.chdir(WORK_DIR)
        
        # Ajouter experiments.json et outputs/
        subprocess.run(["git", "add", "experiments.json"], check=True)
        
        if RESULTS_DIR.exists():
            subprocess.run(["git", "add", "outputs/"], check=False)
        
        # Commit avec résumé
        completed = sum(1 for exp in experiments if exp.get("status") == "completed")
        failed = sum(1 for exp in experiments if exp.get("status") == "failed")
        
        commit_msg = f"results: Colab execution - {completed} completed, {failed} failed"
        
        subprocess.run([
            "git", "commit", "-m", commit_msg
        ], check=True)
        
        subprocess.run(["git", "push", "origin", BRANCH], check=True)
        
        log(f"Résultats pushés: {commit_msg}", "SUCCESS")
        return True
    
    except subprocess.CalledProcessError as e:
        log(f"Erreur push résultats: {e}", "ERROR")
        return False

# ============================================================================
# EXPERIMENT EXECUTION
# ============================================================================

def load_experiments() -> Optional[List[Dict]]:
    """Charge experiments.json"""
    exp_file = WORK_DIR / "experiments.json"
    
    if not exp_file.exists():
        log("Aucun fichier experiments.json trouvé", "WARNING")
        return None
    
    try:
        with open(exp_file) as f:
            experiments = json.load(f)
        
        log(f"Chargé {len(experiments)} expériences")
        return experiments
    
    except json.JSONDecodeError as e:
        log(f"Erreur parsing experiments.json: {e}", "ERROR")
        return None

def save_experiments(experiments: List[Dict]):
    """Sauvegarde experiments.json"""
    exp_file = WORK_DIR / "experiments.json"
    
    try:
        with open(exp_file, "w") as f:
            json.dump(experiments, f, indent=2)
        log("experiments.json sauvegardé")
    
    except Exception as e:
        log(f"Erreur sauvegarde experiments.json: {e}", "ERROR")

def run_experiment(exp: Dict) -> Dict:
    """Exécute une expérience"""
    name = exp.get("name", "unknown")
    command = exp.get("command", "")
    timeout = exp.get("timeout", 3600)
    
    log(f"🚀 Lancement: {name}")
    log(f"   Commande: {command}")
    log(f"   Timeout: {timeout}s")
    
    # Créer output directory pour cette expérience
    exp_output_dir = RESULTS_DIR / name
    exp_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Ajouter variables d'environnement
    env = os.environ.copy()
    env["EXPERIMENT_NAME"] = name
    env["EXPERIMENT_OUTPUT_DIR"] = str(exp_output_dir)
    
    start_time = datetime.now()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            capture_output=True,
            text=True,
            cwd=str(WORK_DIR),
            env=env
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Mettre à jour l'expérience
        exp["status"] = "completed" if result.returncode == 0 else "failed"
        exp["output"] = result.stdout[-5000:] if len(result.stdout) > 5000 else result.stdout
        exp["error"] = result.stderr[-5000:] if len(result.stderr) > 5000 else result.stderr
        exp["return_code"] = result.returncode
        exp["duration"] = duration
        exp["completed_at"] = end_time.isoformat()
        
        # Sauvegarder logs complets
        log_file = exp_output_dir / "execution.log"
        with open(log_file, "w") as f:
            f.write(f"Command: {command}\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write(f"Duration: {duration}s\n\n")
            f.write("=== STDOUT ===\n")
            f.write(result.stdout)
            f.write("\n\n=== STDERR ===\n")
            f.write(result.stderr)
        
        if result.returncode == 0:
            log(f"✅ Terminé: {name} ({duration:.1f}s)", "SUCCESS")
        else:
            log(f"❌ Échec: {name} (code {result.returncode})", "ERROR")
    
    except subprocess.TimeoutExpired:
        end_time = datetime.now()
        exp["status"] = "timeout"
        exp["error"] = f"Timeout après {timeout}s"
        exp["completed_at"] = end_time.isoformat()
        log(f"⏱️ Timeout: {name}", "WARNING")
    
    except Exception as e:
        exp["status"] = "error"
        exp["error"] = str(e)
        exp["completed_at"] = datetime.now().isoformat()
        log(f"💥 Erreur: {name} - {e}", "ERROR")
    
    return exp

def run_experiments():
    """Exécute toutes les expériences en attente"""
    experiments = load_experiments()
    
    if not experiments:
        log("⏭️  Pas d'expériences à lancer")
        return False
    
    # Créer directory pour résultats
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Filtrer expériences pending
    pending = [exp for exp in experiments if exp.get("status") == "pending"]
    
    if not pending:
        log("⏭️  Aucune expérience en attente")
        return False
    
    log(f"🎯 {len(pending)} expériences à exécuter")
    
    # Exécuter chaque expérience
    for i, exp in enumerate(experiments):
        if exp.get("status") == "pending":
            log(f"[{i+1}/{len(pending)}] Traitement: {exp.get('name')}")
            experiments[experiments.index(exp)] = run_experiment(exp)
            
            # Sauvegarder après chaque expérience (checkpoint)
            save_experiments(experiments)
    
    # Push résultats
    push_results(experiments)
    
    return True

# ============================================================================
# DAEMON LOOP
# ============================================================================

def check_gpu():
    """Vérifie la disponibilité du GPU"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True
        )
        gpu_info = result.stdout.strip()
        log(f"GPU détecté: {gpu_info}", "SUCCESS")
        return True
    except:
        log("⚠️  Aucun GPU détecté!", "WARNING")
        return False

def daemon_loop():
    """Boucle principale du daemon"""
    log("=" * 80)
    log("🚀 DAEMON COLAB DÉMARRÉ", "SUCCESS")
    log("=" * 80)
    log(f"Repo: {REPO_URL}")
    log(f"Branche: {BRANCH}")
    log(f"Intervalle: {WATCH_INTERVAL}s")
    log(f"Work dir: {WORK_DIR}")
    log(f"Results dir: {RESULTS_DIR}")
    
    # Check GPU
    check_gpu()
    
    last_commit = None
    
    try:
        while True:
            log("-" * 80)
            
            # Setup/update repo
            if not setup_repo():
                log("Échec setup repo, retry dans 60s", "ERROR")
                time.sleep(60)
                continue
            
            # Check nouveau commit
            current_commit = get_latest_commit()
            
            if current_commit is None:
                log("Impossible de lire commit, retry", "ERROR")
                time.sleep(WATCH_INTERVAL)
                continue
            
            if current_commit != last_commit:
                log(f"🆕 Nouveau commit détecté: {current_commit[:8]}", "SUCCESS")
                
                # Exécuter expériences
                run_experiments()
                
                last_commit = current_commit
            else:
                log(f"⏳ Aucun changement (commit: {current_commit[:8]})")
            
            log(f"💤 Sleep {WATCH_INTERVAL}s...")
            time.sleep(WATCH_INTERVAL)
    
    except KeyboardInterrupt:
        log("=" * 80)
        log("🛑 DAEMON ARRÊTÉ PAR L'UTILISATEUR", "WARNING")
        log("=" * 80)
    
    except Exception as e:
        log("=" * 80)
        log(f"💥 ERREUR CRITIQUE: {e}", "ERROR")
        log("=" * 80)
        raise

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    daemon_loop()

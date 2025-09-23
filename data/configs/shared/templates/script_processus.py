#!/usr/bin/env python3
"""
Template Gestion de Processus - PaniniFS
Simplification des opérations sur les processus système.
"""

import psutil
import signal
import sys
from pathlib import Path
import logging

# Configuration Panini
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
logger = logging.getLogger(__name__)

def find_processes_by_pattern(pattern, exact_match=False):
    """Trouve les processus correspondant au pattern."""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            name = proc.info['name']
            
            if exact_match:
                if pattern == name or pattern in cmdline:
                    processes.append(proc)
            else:
                if pattern.lower() in name.lower() or pattern.lower() in cmdline.lower():
                    processes.append(proc)
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return processes

def display_processes(processes):
    """Affiche les informations des processus."""
    if not processes:
        logger.info("Aucun processus trouvé")
        return
    
    logger.info(f"Processus trouvés: {len(processes)}")
    for proc in processes:
        try:
            cmdline = ' '.join(proc.cmdline() or [])[:60] + "..."
            logger.info(f"  PID {proc.pid}: {proc.name()} - {cmdline}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logger.warning(f"  PID {proc.pid}: Processus inaccessible")

def terminate_processes(processes, force=False):
    """Termine les processus de manière propre ou forcée."""
    if not processes:
        return 0
    
    terminated_count = 0
    
    for proc in processes:
        try:
            if force:
                proc.kill()
                logger.info(f"🔪 PID {proc.pid} forcé (SIGKILL)")
            else:
                proc.terminate()
                logger.info(f"🛑 PID {proc.pid} terminé (SIGTERM)")
            
            terminated_count += 1
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.error(f"❌ Erreur PID {proc.pid}: {e}")
    
    return terminated_count

def wait_for_termination(processes, timeout=10):
    """Attend la terminaison des processus."""
    gone, alive = psutil.wait_procs(processes, timeout=timeout)
    
    if alive:
        logger.warning(f"⏰ {len(alive)} processus encore actifs après {timeout}s")
        return alive
    else:
        logger.info("✅ Tous les processus ont été terminés")
        return []

def main():
    """Fonction principale."""
    # TODO: Configurer le pattern de recherche
    search_pattern = "PATTERN_A_REMPLACER"  # Remplacer par votre pattern
    
    try:
        logger.info(f"🔍 Recherche de processus: {search_pattern}")
        
        # Trouver les processus
        processes = find_processes_by_pattern(search_pattern)
        
        # Afficher les processus trouvés
        display_processes(processes)
        
        if not processes:
            return 0
        
        # Demander confirmation (optionnel)
        # response = input(f"Terminer {len(processes)} processus? (o/N): ")
        # if response.lower() not in ['o', 'oui', 'y', 'yes']:
        #     logger.info("Opération annulée")
        #     return 0
        
        # Terminaison douce
        terminated = terminate_processes(processes, force=False)
        logger.info(f"📤 {terminated} processus en cours de terminaison")
        
        # Attendre la terminaison
        still_alive = wait_for_termination(processes, timeout=5)
        
        # Terminaison forcée si nécessaire
        if still_alive:
            logger.warning("🔪 Terminaison forcée des processus restants")
            terminate_processes(still_alive, force=True)
        
        logger.info("✅ Opération terminée")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("⏹️ Interruption utilisateur")
        return 130
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    exit(main())
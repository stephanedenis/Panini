#!/usr/bin/env python3
"""
Système de Tâches Automatisé pour Dashboard Unifié
Génère et exécute des tâches en arrière-plan pour démonstration
"""

import json
import time
import threading
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import requests


class AutomatedTaskSystem:
    """Système de tâches automatisé pour le dashboard"""
    
    def __init__(self, dashboard_url="http://localhost:8093"):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.dashboard_url = dashboard_url
        self.running = False
        
        # Queue des tâches
        self.task_queue = deque()
        self.active_tasks = {}
        self.completed_tasks = []
        
        # Configuration
        self.task_interval = 30  # secondes entre tâches
        
    def add_task(self, title, description, command=None, script=None, duration=10):
        """Ajoute une tâche à la queue"""
        task = {
            "id": len(self.task_queue) + len(self.active_tasks) + len(self.completed_tasks) + 1,
            "title": title,
            "description": description,
            "command": command,
            "script": script,
            "duration": duration,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.task_queue.append(task)
        print(f"📋 Tâche ajoutée: {title}")
        
        return task
    
    def create_demo_tasks(self):
        """Crée des tâches de démonstration"""
        print("🎮 Création tâches de démonstration...")
        
        # Tâches d'optimisation
        self.add_task(
            "Optimisation RX 480 Express",
            "Cycle d'optimisation rapide du GPU RX 480 avec monitoring",
            script="panini_high_performance_optimizer.py",
            duration=45
        )
        
        # Tâches de monitoring
        self.add_task(
            "Monitoring Système Avancé",
            "Collecte de métriques système détaillées pendant 30 secondes",
            script="rx480_system_monitor.py",
            duration=35
        )
        
        # Tâches d'analyse
        self.add_task(
            "Analyse Corpus Linguistique",
            "Traitement et analyse du corpus PaniniFS avec extraction patterns",
            script="autonomous_corpus_processor.py",
            duration=25
        )
        
        # Tâches de validation
        self.add_task(
            "Validation Dhatu Universaux",
            "Validation des dhatu universels avec optimisation algorithme",
            script="autonomous_dhatu_optimizer.py",
            duration=30
        )
        
        # Tâches de génération de rapport
        self.add_task(
            "Génération Rapport Performance",
            "Création rapport de performance intégré système + GPU",
            command="python3 -c \"import json; print('Rapport généré')\"",
            duration=5
        )
        
        print(f"✅ {len(self.task_queue)} tâches créées")
    
    def execute_task(self, task):
        """Exécute une tâche"""
        task_id = task["id"]
        print(f"🚀 Démarrage tâche #{task_id}: {task['title']}")
        
        # Marquer comme active
        task["status"] = "active"
        task["started_at"] = datetime.now().isoformat()
        self.active_tasks[task_id] = task
        
        try:
            if task.get("script"):
                # Exécution script Python
                script_path = self.workspace / task["script"]
                if script_path.exists():
                    print(f"  📜 Exécution script: {task['script']}")
                    
                    result = subprocess.run(
                        [sys.executable, str(script_path)],
                        cwd=self.workspace,
                        timeout=task.get("duration", 30),
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        task["status"] = "completed"
                        task["output"] = result.stdout[-500:]  # Derniers 500 caractères
                        print(f"  ✅ Script terminé avec succès")
                    else:
                        task["status"] = "error"
                        task["error"] = result.stderr[-500:]
                        print(f"  ❌ Erreur script: {result.stderr}")
                else:
                    task["status"] = "error"
                    task["error"] = f"Script non trouvé: {script_path}"
                    print(f"  ❌ Script non trouvé: {script_path}")
                    
            elif task.get("command"):
                # Exécution commande
                print(f"  💻 Exécution commande: {task['command']}")
                
                result = subprocess.run(
                    task["command"],
                    shell=True,
                    cwd=self.workspace,
                    timeout=task.get("duration", 30),
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    task["status"] = "completed"
                    task["output"] = result.stdout[-500:]
                    print(f"  ✅ Commande terminée avec succès")
                else:
                    task["status"] = "error"
                    task["error"] = result.stderr[-500:]
                    print(f"  ❌ Erreur commande: {result.stderr}")
            else:
                # Tâche simulation
                print(f"  ⏳ Simulation tâche ({task.get('duration', 10)}s)...")
                time.sleep(min(task.get("duration", 10), 10))  # Max 10s pour simulation
                task["status"] = "completed"
                task["output"] = f"Tâche simulée terminée: {task['title']}"
                print(f"  ✅ Simulation terminée")
                
        except subprocess.TimeoutExpired:
            task["status"] = "timeout"
            task["error"] = f"Timeout après {task.get('duration', 30)}s"
            print(f"  ⏰ Timeout tâche #{task_id}")
            
        except Exception as e:
            task["status"] = "error"
            task["error"] = str(e)
            print(f"  ❌ Erreur tâche #{task_id}: {e}")
        
        finally:
            # Finaliser tâche
            task["completed_at"] = datetime.now().isoformat()
            
            # Déplacer vers complétées
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            self.completed_tasks.append(task)
            
            # Limiter historique
            if len(self.completed_tasks) > 50:
                self.completed_tasks = self.completed_tasks[-50:]
            
            print(f"📝 Tâche #{task_id} terminée - Statut: {task['status']}")
    
    def task_worker(self):
        """Worker thread pour exécuter les tâches"""
        print("🔄 Worker de tâches démarré")
        
        while self.running:
            try:
                if self.task_queue and len(self.active_tasks) < 2:  # Max 2 tâches simultanées
                    task = self.task_queue.popleft()
                    
                    # Exécuter dans un thread séparé pour non-blocage
                    thread = threading.Thread(
                        target=self.execute_task,
                        args=(task,),
                        daemon=True
                    )
                    thread.start()
                
                time.sleep(5)  # Vérification toutes les 5 secondes
                
            except Exception as e:
                print(f"❌ Erreur worker: {e}")
                time.sleep(5)
        
        print("🛑 Worker de tâches arrêté")
    
    def status_reporter(self):
        """Reporter thread pour communiquer avec le dashboard"""
        print("📊 Reporter de statut démarré")
        
        while self.running:
            try:
                # Mise à jour fictive du dashboard
                # (Dans une vraie implémentation, on ferait des appels API)
                status = {
                    "pending_tasks": len(self.task_queue),
                    "active_tasks": len(self.active_tasks),
                    "completed_tasks": len(self.completed_tasks),
                    "timestamp": datetime.now().isoformat()
                }
                
                # Affichage périodique
                if len(self.active_tasks) > 0 or len(self.task_queue) > 0:
                    print(f"📈 Statut: {status['pending_tasks']} en attente, "
                          f"{status['active_tasks']} actives, "
                          f"{status['completed_tasks']} terminées")
                
                time.sleep(15)  # Rapport toutes les 15 secondes
                
            except Exception as e:
                print(f"❌ Erreur reporter: {e}")
                time.sleep(15)
        
        print("🛑 Reporter de statut arrêté")
    
    def create_accomplishments_demo(self):
        """Crée des accomplissements factices pour démonstration"""
        accomplishments = []
        
        # Accomplissements récents
        for i in range(5):
            age_minutes = i * 15
            timestamp = datetime.now() - timedelta(minutes=age_minutes)
            
            accomplishments.append({
                "timestamp": timestamp.isoformat(),
                "type": "optimization_completed",
                "description": f"Optimisation RX 480 #{5-i} terminée avec succès",
                "age_minutes": age_minutes,
                "performance_gain": f"{10 + i * 2}.{i}x"
            })
        
        # Sauvegarder pour le dashboard
        demo_file = self.workspace / "demo_accomplishments.json"
        with open(demo_file, 'w') as f:
            json.dump(accomplishments, f, indent=2)
        
        print(f"✅ Accomplissements demo créés: {demo_file}")
    
    def generate_activity(self):
        """Génère de l'activité continue"""
        print("🎯 Génération d'activité continue...")
        
        activity_tasks = [
            ("Monitoring GPU Continu", "Surveillance continue RX 480", 20),
            ("Analyse Patterns Linguistiques", "Extraction patterns PaniniFS", 15),
            ("Optimisation Cache Système", "Optimisation cache mémoire", 10),
            ("Validation Algorithmes", "Tests validation dhatu", 25),
            ("Génération Métriques", "Collecte métriques performance", 8)
        ]
        
        for title, desc, duration in activity_tasks:
            self.add_task(title, desc, duration=duration)
            time.sleep(2)  # Espacement
    
    def print_status(self):
        """Affiche statut détaillé"""
        print("\n" + "="*50)
        print("📊 STATUT SYSTÈME DE TÂCHES")
        print("="*50)
        print(f"📋 En attente: {len(self.task_queue)}")
        print(f"🔄 Actives: {len(self.active_tasks)}")
        print(f"✅ Terminées: {len(self.completed_tasks)}")
        
        if self.active_tasks:
            print("\n🔄 TÂCHES ACTIVES:")
            for task_id, task in self.active_tasks.items():
                elapsed = "calculating..."
                if task.get("started_at"):
                    try:
                        start_time = datetime.fromisoformat(task["started_at"].replace('Z', '+00:00'))
                        elapsed = str(datetime.now() - start_time.replace(tzinfo=None)).split('.')[0]
                    except:
                        pass
                print(f"  #{task_id}: {task['title']} (durée: {elapsed})")
        
        if self.task_queue:
            print(f"\n📋 PROCHAINES TÂCHES ({len(self.task_queue)}):")
            for i, task in enumerate(list(self.task_queue)[:3]):
                print(f"  #{task['id']}: {task['title']}")
            if len(self.task_queue) > 3:
                print(f"  ... et {len(self.task_queue) - 3} autres")
        
        recent_completed = [t for t in self.completed_tasks[-5:] if t["status"] == "completed"]
        if recent_completed:
            print(f"\n✅ RÉCEMMENT TERMINÉES ({len(recent_completed)}):")
            for task in recent_completed:
                print(f"  #{task['id']}: {task['title']} - {task['status']}")
        
        print("="*50)
    
    def start(self):
        """Démarre le système de tâches"""
        print("🎮 DÉMARRAGE SYSTÈME DE TÂCHES AUTOMATISÉ")
        print("="*55)
        
        self.running = True
        
        # Créer accomplissements demo
        self.create_accomplishments_demo()
        
        # Créer tâches initiales
        self.create_demo_tasks()
        
        # Démarrer workers
        worker_thread = threading.Thread(target=self.task_worker, daemon=True)
        reporter_thread = threading.Thread(target=self.status_reporter, daemon=True)
        
        worker_thread.start()
        reporter_thread.start()
        
        print(f"🔗 Dashboard: {self.dashboard_url}")
        print("🔄 Système de tâches actif")
        print("Ctrl+C pour arrêter")
        
        try:
            # Boucle principale avec génération d'activité
            while self.running:
                self.print_status()
                time.sleep(30)
                
                # Générer plus d'activité si nécessaire
                if len(self.task_queue) < 3:
                    self.generate_activity()
                    
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé...")
        finally:
            self.stop()
    
    def stop(self):
        """Arrête le système de tâches"""
        print("🛑 Arrêt système de tâches...")
        self.running = False
        
        # Attendre fin des tâches actives
        if self.active_tasks:
            print(f"⏳ Attente fin de {len(self.active_tasks)} tâches actives...")
            timeout = 30
            while self.active_tasks and timeout > 0:
                time.sleep(1)
                timeout -= 1
        
        print("✅ Système de tâches arrêté")


def main():
    """Point d'entrée principal"""
    print("🎮 SYSTÈME DE TÂCHES AUTOMATISÉ")
    print("Alimentation du Dashboard Unifié PaniniFS + RX 480")
    print()
    
    # Vérifier si dashboard est accessible
    dashboard_url = "http://localhost:8093"
    try:
        response = requests.get(dashboard_url, timeout=2)
        if response.status_code == 200:
            print(f"✅ Dashboard détecté: {dashboard_url}")
        else:
            print(f"⚠️ Dashboard non accessible: {dashboard_url}")
    except:
        print(f"⚠️ Dashboard non accessible: {dashboard_url}")
        print("   (Le système fonctionnera quand même)")
    
    print()
    
    # Démarrer système
    task_system = AutomatedTaskSystem(dashboard_url)
    task_system.start()


if __name__ == '__main__':
    main()
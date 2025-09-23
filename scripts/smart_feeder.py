#!/usr/bin/env python3
"""
🎯 Smart Feeder - Alimentation intelligente pour Colab
Gère le flux continu et adapte le débit selon la consommation
"""

import os
import json
import time
import subprocess
import threading
from datetime import datetime, timedelta
import glob

class SmartFeeder:
    def __init__(self):
        self.data_dir = "data/incremental_corpus"
        self.results_dir = "colab_results"
        self.buffer_target = 50  # Fichiers cibles dans le buffer
        self.buffer_minimum = 20  # Seuil minimum
        
        # État du système
        self.feeder_active = True
        self.collection_stats = {
            'last_check': None,
            'consumption_rate': 0,  # fichiers/minute
            'production_rate': 0,   # fichiers/minute
            'buffer_level': 0
        }
        
    def count_available_files(self):
        """Compter les fichiers disponibles"""
        pattern = os.path.join(self.data_dir, "*.json")
        files = glob.glob(pattern)
        return len(files)
    
    def estimate_consumption_rate(self):
        """Estimer le taux de consommation de Colab"""
        feedback_file = os.path.join(self.results_dir, 'colab_feedback.json')
        
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    feedback = json.load(f)
                
                # Analyser le feedback pour estimer la vitesse
                analysis = feedback.get('analysis_summary', {})
                docs_analyzed = analysis.get('documents_analyzed', 0)
                
                # Estimer basé sur le timestamp
                timestamp_str = feedback.get('timestamp', '')
                if timestamp_str:
                    feedback_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    time_diff = datetime.now() - feedback_time.replace(tzinfo=None)
                    
                    if time_diff.total_seconds() > 0:
                        rate = docs_analyzed / (time_diff.total_seconds() / 60)  # docs/min
                        return rate
                        
            except Exception as e:
                print(f"Erreur lecture feedback: {e}")
        
        return 5.0  # Taux par défaut
    
    def check_buffer_status(self):
        """Vérifier l'état du buffer"""
        current_files = self.count_available_files()
        consumption_rate = self.estimate_consumption_rate()
        
        # Calculer le temps restant
        if consumption_rate > 0:
            minutes_remaining = current_files / consumption_rate
        else:
            minutes_remaining = float('inf')
        
        status = {
            'current_files': current_files,
            'consumption_rate': consumption_rate,
            'minutes_remaining': minutes_remaining,
            'buffer_status': 'ok' if current_files > self.buffer_minimum else 'low',
            'action_needed': current_files < self.buffer_target
        }
        
        return status
    
    def trigger_turbo_collection(self, duration_minutes=10):
        """Déclencher une collecte turbo"""
        print(f"🚀 Déclenchement collecte TURBO ({duration_minutes}min)")
        
        try:
            # Lancer le collecteur turbo
            cmd = ['python3', 'scripts/turbo_corpus_collector.py']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Attendre avec timeout
            try:
                stdout, stderr = process.communicate(timeout=duration_minutes * 60 + 30)
                
                if process.returncode == 0:
                    print("✅ Collecte turbo terminée avec succès")
                    return True
                else:
                    print(f"⚠️ Collecte turbo échouée: {stderr.decode()}")
                    
            except subprocess.TimeoutExpired:
                process.kill()
                print("⏰ Collecte turbo interrompue (timeout)")
                
        except Exception as e:
            print(f"❌ Erreur lancement collecte turbo: {e}")
        
        return False
    
    def trigger_fast_collection(self):
        """Déclencher une collecte rapide"""
        print("⚡ Déclenchement collecte rapide")
        
        try:
            cmd = ['python3', 'scripts/fast_corpus_collector.py']
            subprocess.run(cmd, timeout=60, check=True)
            print("✅ Collecte rapide terminée")
            return True
            
        except subprocess.TimeoutExpired:
            print("⏰ Collecte rapide timeout")
        except subprocess.CalledProcessError as e:
            print(f"❌ Collecte rapide échouée: {e}")
        except Exception as e:
            print(f"❌ Erreur collecte rapide: {e}")
        
        return False
    
    def adaptive_feeding_cycle(self):
        """Cycle d'alimentation adaptatif"""
        while self.feeder_active:
            print("\n🔍 Vérification buffer...")
            
            status = self.check_buffer_status()
            
            print(f"📊 Buffer: {status['current_files']} fichiers")
            print(f"📈 Consommation: {status['consumption_rate']:.1f} docs/min")
            print(f"⏱️ Autonomie: {status['minutes_remaining']:.1f} minutes")
            
            # Décider de l'action
            if status['current_files'] < self.buffer_minimum:
                print("🚨 BUFFER CRITIQUE - Collecte TURBO!")
                self.trigger_turbo_collection(duration_minutes=15)
                
            elif status['action_needed']:
                print("⚠️ Buffer bas - Collecte rapide")
                self.trigger_fast_collection()
                
            else:
                print("✅ Buffer OK - Surveillance continue")
            
            # Sauvegarder les stats
            self.save_feeder_stats(status)
            
            # Pause adaptative
            if status['current_files'] < self.buffer_minimum:
                pause = 30  # Vérification fréquente si critique
            elif status['action_needed']:
                pause = 60  # Vérification normale
            else:
                pause = 120  # Vérification espacée si OK
            
            print(f"⏸️ Pause {pause}s...")
            time.sleep(pause)
    
    def save_feeder_stats(self, status):
        """Sauvegarder les stats du feeder"""
        feeder_stats = {
            'timestamp': datetime.now().isoformat(),
            'buffer_status': status,
            'feeder_active': self.feeder_active,
            'target_buffer': self.buffer_target,
            'minimum_buffer': self.buffer_minimum
        }
        
        stats_file = os.path.join(self.results_dir, 'smart_feeder_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(feeder_stats, f, ensure_ascii=False, indent=2)
    
    def start_feeding(self):
        """Démarrer l'alimentation intelligente"""
        print("🎯 Smart Feeder démarré!")
        print(f"📊 Cible buffer: {self.buffer_target} fichiers")
        print(f"🚨 Seuil critique: {self.buffer_minimum} fichiers")
        
        try:
            self.adaptive_feeding_cycle()
        except KeyboardInterrupt:
            print("\n⏹️ Smart Feeder arrêté par l'utilisateur")
            self.feeder_active = False
        except Exception as e:
            print(f"❌ Erreur Smart Feeder: {e}")
            self.feeder_active = False

def main():
    """Point d'entrée"""
    feeder = SmartFeeder()
    
    # Vérification initiale
    initial_status = feeder.check_buffer_status()
    print("🎯 SMART FEEDER - Alimentation intelligente Colab")
    print(f"📊 État initial: {initial_status['current_files']} fichiers")
    print(f"📈 Consommation estimée: {initial_status['consumption_rate']:.1f} docs/min")
    
    # Si buffer très bas, collecte immédiate
    if initial_status['current_files'] < feeder.buffer_minimum:
        print("🚨 Buffer critique détecté - Collecte turbo immédiate!")
        feeder.trigger_turbo_collection(duration_minutes=10)
    
    # Démarrer le cycle
    feeder.start_feeding()

if __name__ == "__main__":
    main()
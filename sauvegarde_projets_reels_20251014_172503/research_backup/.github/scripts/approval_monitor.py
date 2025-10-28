#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moniteur Approbations - Spec-Kit PaniniFS
Surveillance en temps réel des approbations et rejets
"""

import json
import os
import time
import threading
from datetime import datetime, timedelta
from collections import deque, Counter
import signal
import sys

class ApprovalMonitor:
    def __init__(self):
        self.log_path = os.path.join(
            os.path.dirname(__file__), 
            "../logs/command_execution.log"
        )
        self.config_path = os.path.join(
            os.path.dirname(__file__), 
            "../copilot-approved-scripts.json"
        )
        
        # Buffers circulaires pour le monitoring
        self.recent_events = deque(maxlen=100)
        self.hourly_stats = deque(maxlen=24)
        
        # Compteurs temps réel
        self.session_stats = {
            'start_time': datetime.now(),
            'total_commands': 0,
            'approved': 0,
            'rejected': 0,
            'avg_duration': 0,
            'alert_count': 0
        }
        
        # Configuration des seuils d'alerte
        self.alert_thresholds = {
            'rejection_rate_5min': 0.3,  # 30% rejets sur 5 min
            'avg_duration_warning': 1000,  # > 1 seconde
            'consecutive_rejections': 5,  # 5 rejets consécutifs
            'security_alerts_hour': 10   # 10 alertes sécurité/heure
        }
        
        self.running = True
        self.last_position = 0
    
    def start_monitoring(self):
        """Démarrer la surveillance"""
        print("🔍 Démarrage du moniteur d'approbations PaniniFS")
        print(f"📁 Log: {self.log_path}")
        print(f"⚙️ Config: {self.config_path}")
        print("=" * 60)
        
        # Gestionnaire de signal pour arrêt propre
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Thread pour l'affichage des stats
        display_thread = threading.Thread(target=self._display_loop, daemon=True)
        display_thread.start()
        
        # Boucle principale de monitoring
        try:
            self._monitor_loop()
        except KeyboardInterrupt:
            print("\n👋 Arrêt du monitoring...")
        finally:
            self._cleanup()
    
    def _monitor_loop(self):
        """Boucle principale de surveillance"""
        while self.running:
            try:
                # Lire les nouveaux événements
                new_events = self._read_new_events()
                
                # Traiter chaque événement
                for event in new_events:
                    self._process_event(event)
                
                # Vérifier les conditions d'alerte
                self._check_alerts()
                
                # Calculer stats horaires
                self._update_hourly_stats()
                
                # Attendre avant la prochaine vérification
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Erreur monitoring: {e}")
                time.sleep(5)
    
    def _read_new_events(self):
        """Lire les nouveaux événements depuis la dernière vérification"""
        events = []
        
        try:
            if not os.path.exists(self.log_path):
                return events
            
            with open(self.log_path, 'r', encoding='utf-8') as f:
                # Se positionner à la dernière position lue
                f.seek(self.last_position)
                
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
                
                # Sauvegarder la nouvelle position
                self.last_position = f.tell()
                
        except Exception as e:
            print(f"⚠️ Erreur lecture log: {e}")
        
        return events
    
    def _process_event(self, event):
        """Traiter un événement de log"""
        # Ajouter à l'historique récent
        self.recent_events.append(event)
        
        # Mettre à jour les statistiques de session
        self.session_stats['total_commands'] += 1
        
        if event['status'] == 'APPROVED':
            self.session_stats['approved'] += 1
        elif event['status'] == 'REJECTED':
            self.session_stats['rejected'] += 1
        
        # Calculer durée moyenne
        duration = event.get('duration_ms', 0)
        current_avg = self.session_stats['avg_duration']
        total = self.session_stats['total_commands']
        self.session_stats['avg_duration'] = (current_avg * (total - 1) + duration) / total
        
        # Vérifications immédiates
        self._check_immediate_alerts(event)
    
    def _check_immediate_alerts(self, event):
        """Vérifier les alertes immédiates"""
        # Alerte durée élevée
        if event.get('duration_ms', 0) > self.alert_thresholds['avg_duration_warning']:
            self._emit_alert(
                'PERFORMANCE', 
                f"Validation lente: {event['duration_ms']}ms pour {event['command']}"
            )
        
        # Alerte sécurité
        if event['status'] == 'REJECTED' and 'sécurité' in event.get('reason', '').lower():
            self._emit_alert(
                'SECURITY', 
                f"Rejet sécurité: {event['command']} - {event['reason']}"
            )
        
        # Alerte pattern manquant critique
        if (event['status'] == 'REJECTED' and 
            'panini' in event['command'].lower() and 
            'pattern' in event.get('reason', '').lower()):
            self._emit_alert(
                'PATTERN', 
                f"Pattern PaniniFS manquant: {event['command']}"
            )
    
    def _check_alerts(self):
        """Vérifier les conditions d'alerte globales"""
        now = datetime.now()
        
        # Vérifier taux de rejet sur 5 minutes
        recent_5min = [e for e in self.recent_events 
                      if (now - datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00'))).seconds <= 300]
        
        if len(recent_5min) >= 10:  # Au moins 10 commandes
            rejections = sum(1 for e in recent_5min if e['status'] == 'REJECTED')
            rejection_rate = rejections / len(recent_5min)
            
            if rejection_rate >= self.alert_thresholds['rejection_rate_5min']:
                self._emit_alert(
                    'HIGH_REJECTION', 
                    f"Taux de rejet élevé: {rejection_rate:.1%} sur 5 min ({rejections}/{len(recent_5min)})"
                )
        
        # Vérifier rejets consécutifs
        last_n = list(self.recent_events)[-self.alert_thresholds['consecutive_rejections']:]
        if (len(last_n) == self.alert_thresholds['consecutive_rejections'] and 
            all(e['status'] == 'REJECTED' for e in last_n)):
            self._emit_alert(
                'CONSECUTIVE_REJECTIONS', 
                f"{self.alert_thresholds['consecutive_rejections']} rejets consécutifs détectés"
            )
    
    def _emit_alert(self, alert_type, message):
        """Émettre une alerte"""
        self.session_stats['alert_count'] += 1
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        alert_msg = f"🚨 [{alert_type}] {timestamp}: {message}"
        
        # Affichage immédiat
        print(f"\n{alert_msg}")
        
        # Log de l'alerte
        self._log_alert(alert_type, message)
    
    def _log_alert(self, alert_type, message):
        """Logger une alerte"""
        alert_log = os.path.join(os.path.dirname(self.log_path), "alerts.log")
        
        try:
            os.makedirs(os.path.dirname(alert_log), exist_ok=True)
            
            with open(alert_log, 'a', encoding='utf-8') as f:
                alert_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'type': alert_type,
                    'message': message,
                    'session_stats': self.session_stats.copy()
                }
                f.write(json.dumps(alert_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"⚠️ Erreur log alerte: {e}")
    
    def _update_hourly_stats(self):
        """Mettre à jour les statistiques horaires"""
        current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        # Vérifier si on a déjà une entrée pour cette heure
        if (not self.hourly_stats or 
            self.hourly_stats[-1]['hour'] != current_hour):
            
            # Calculer stats de l'heure écoulée
            hour_events = [e for e in self.recent_events 
                          if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')).replace(minute=0, second=0, microsecond=0) == current_hour]
            
            hourly_stat = {
                'hour': current_hour,
                'total': len(hour_events),
                'approved': sum(1 for e in hour_events if e['status'] == 'APPROVED'),
                'rejected': sum(1 for e in hour_events if e['status'] == 'REJECTED'),
                'avg_duration': sum(e.get('duration_ms', 0) for e in hour_events) / max(len(hour_events), 1)
            }
            
            self.hourly_stats.append(hourly_stat)
    
    def _display_loop(self):
        """Boucle d'affichage des statistiques"""
        while self.running:
            try:
                self._display_dashboard()
                time.sleep(10)  # Mise à jour toutes les 10 secondes
            except Exception as e:
                print(f"⚠️ Erreur affichage: {e}")
                time.sleep(5)
    
    def _display_dashboard(self):
        """Afficher le tableau de bord"""
        # Nettoyer l'écran
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # En-tête
        uptime = datetime.now() - self.session_stats['start_time']
        print("🔍 MONITEUR APPROBATIONS PANINI-FS")
        print("=" * 60)
        print(f"⏱️ Uptime: {str(uptime).split('.')[0]}")
        print(f"📊 Session démarrée: {self.session_stats['start_time'].strftime('%H:%M:%S')}")
        
        # Statistiques de session
        total = self.session_stats['total_commands']
        approved = self.session_stats['approved']
        rejected = self.session_stats['rejected']
        
        approval_rate = (approved / max(total, 1)) * 100
        rejection_rate = (rejected / max(total, 1)) * 100
        
        print(f"\n📈 STATISTIQUES SESSION")
        print(f"   Total commandes: {total}")
        print(f"   ✅ Approuvées: {approved} ({approval_rate:.1f}%)")
        print(f"   ❌ Rejetées: {rejected} ({rejection_rate:.1f}%)")
        print(f"   ⏱️ Durée moyenne: {self.session_stats['avg_duration']:.1f}ms")
        print(f"   🚨 Alertes: {self.session_stats['alert_count']}")
        
        # Dernières commandes
        if self.recent_events:
            print(f"\n📋 DERNIÈRES COMMANDES (max 5)")
            for event in list(self.recent_events)[-5:]:
                status_icon = "✅" if event['status'] == 'APPROVED' else "❌"
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00')).strftime('%H:%M:%S')
                command_short = f"{event['command']} {event['args'][:30]}..."
                print(f"   {status_icon} {timestamp} {command_short}")
        
        # Analyse rapide des rejets
        recent_rejections = [e for e in list(self.recent_events)[-20:] if e['status'] == 'REJECTED']
        if recent_rejections:
            rejection_reasons = Counter(e.get('reason', 'Unknown')[:50] for e in recent_rejections)
            print(f"\n❌ CAUSES DE REJET RÉCENTES")
            for reason, count in rejection_reasons.most_common(3):
                print(f"   • {reason}... ({count}x)")
        
        print(f"\n{'=' * 60}")
        print("💡 Ctrl+C pour arrêter le monitoring")
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire de signal pour arrêt propre"""
        print(f"\n📡 Signal {signum} reçu, arrêt en cours...")
        self.running = False
    
    def _cleanup(self):
        """Nettoyage avant arrêt"""
        print("🧹 Nettoyage...")
        
        # Sauvegarder un rapport final
        final_report = {
            'session_start': self.session_stats['start_time'].isoformat(),
            'session_end': datetime.now().isoformat(),
            'total_duration': str(datetime.now() - self.session_stats['start_time']),
            'final_stats': self.session_stats,
            'hourly_stats': list(self.hourly_stats),
            'last_events': list(self.recent_events)[-10:]
        }
        
        try:
            report_path = os.path.join(os.path.dirname(self.log_path), "monitoring_session.json")
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)
            print(f"📄 Rapport sauvé: {report_path}")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde rapport: {e}")
        
        print("✅ Monitoring arrêté proprement")

def main():
    """Point d'entrée principal"""
    monitor = ApprovalMonitor()
    monitor.start_monitoring()
    return 0

if __name__ == '__main__':
    exit(main())
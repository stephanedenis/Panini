#!/usr/bin/env python3
"""
Template Analyse de Logs - PaniniFS
Simplification de l'analyse et surveillance des fichiers de logs.
"""

import re
import datetime
from pathlib import Path
from collections import Counter, defaultdict
import logging

# Configuration Panini
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
logger = logging.getLogger(__name__)

def tail_log_file(file_path, lines_count=100):
    """Lit les dernières lignes d'un fichier de log."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            return all_lines[-lines_count:] if len(all_lines) > lines_count else all_lines
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"❌ Erreur lecture {file_path}: {e}")
        return []

def parse_log_entry(line, log_format='auto'):
    """Parse une ligne de log selon le format."""
    entry = {
        'timestamp': None,
        'level': None,
        'message': line.strip(),
        'raw': line
    }
    
    # Format automatique - détection de patterns communs
    if log_format == 'auto':
        # Pattern timestamp ISO
        timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})', line)
        if timestamp_match:
            entry['timestamp'] = timestamp_match.group(1)
        
        # Pattern niveau de log
        level_match = re.search(r'\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\b', line, re.IGNORECASE)
        if level_match:
            entry['level'] = level_match.group(1).upper()
    
    return entry

def filter_log_entries(entries, filters):
    """Filtre les entrées selon les critères."""
    filtered = []
    
    for entry in entries:
        include = True
        
        # Filtre par niveau
        if 'level' in filters and filters['level']:
            if entry['level'] != filters['level'].upper():
                include = False
        
        # Filtre par pattern de message
        if 'pattern' in filters and filters['pattern']:
            if not re.search(filters['pattern'], entry['message'], re.IGNORECASE):
                include = False
        
        # Filtre par période
        if 'after' in filters and filters['after'] and entry['timestamp']:
            # Conversion simplifiée - à adapter selon le format
            if entry['timestamp'] < filters['after']:
                include = False
        
        if include:
            filtered.append(entry)
    
    return filtered

def analyze_log_patterns(entries):
    """Analyse les patterns dans les logs."""
    analysis = {
        'total_entries': len(entries),
        'levels': Counter(),
        'hour_distribution': Counter(),
        'common_messages': Counter(),
        'errors': []
    }
    
    for entry in entries:
        # Comptage par niveau
        if entry['level']:
            analysis['levels'][entry['level']] += 1
        
        # Distribution horaire
        if entry['timestamp']:
            hour_match = re.search(r'(\d{2}):\d{2}:\d{2}', entry['timestamp'])
            if hour_match:
                analysis['hour_distribution'][hour_match.group(1)] += 1
        
        # Messages communs (premiers 50 caractères)
        message_key = entry['message'][:50] + "..." if len(entry['message']) > 50 else entry['message']
        analysis['common_messages'][message_key] += 1
        
        # Collecter les erreurs
        if entry['level'] in ['ERROR', 'CRITICAL', 'FATAL']:
            analysis['errors'].append(entry)
    
    return analysis

def display_analysis(analysis):
    """Affiche les résultats d'analyse."""
    logger.info(f"📊 Analyse de {analysis['total_entries']} entrées de log")
    
    # Niveaux de log
    if analysis['levels']:
        logger.info("📋 Distribution par niveau:")
        for level, count in analysis['levels'].most_common():
            logger.info(f"  {level}: {count}")
    
    # Distribution horaire
    if analysis['hour_distribution']:
        logger.info("🕐 Distribution horaire:")
        for hour in sorted(analysis['hour_distribution'].keys()):
            count = analysis['hour_distribution'][hour]
            logger.info(f"  {hour}h: {count}")
    
    # Messages les plus fréquents
    logger.info("💬 Messages les plus fréquents:")
    for message, count in analysis['common_messages'].most_common(5):
        logger.info(f"  ({count}x) {message}")
    
    # Erreurs récentes
    if analysis['errors']:
        logger.info(f"❌ Erreurs trouvées: {len(analysis['errors'])}")
        for error in analysis['errors'][-5:]:  # Dernières 5 erreurs
            logger.info(f"  {error['timestamp']} - {error['message'][:100]}")

def monitor_log_real_time(file_path, callback=None):
    """Surveille un fichier de log en temps réel."""
    import time
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Aller à la fin du fichier
            f.seek(0, 2)
            
            logger.info(f"👁️ Surveillance de {file_path} (Ctrl+C pour arrêter)")
            
            while True:
                line = f.readline()
                if line:
                    entry = parse_log_entry(line)
                    
                    # Affichage ou callback personnalisé
                    if callback:
                        callback(entry)
                    else:
                        timestamp = entry['timestamp'] or 'NO_TIME'
                        level = entry['level'] or 'INFO'
                        logger.info(f"[{timestamp}] {level}: {entry['message']}")
                else:
                    time.sleep(0.1)
                    
    except KeyboardInterrupt:
        logger.info("⏹️ Surveillance arrêtée")

def main():
    """Fonction principale."""
    try:
        # TODO: Configurer les paramètres d'analyse
        log_file = "/var/log/syslog"  # Fichier à analyser
        lines_to_read = 1000  # Nombre de lignes à lire
        filters = {
            # 'level': 'ERROR',  # Filtrer par niveau
            # 'pattern': 'python',  # Filtrer par pattern
        }
        
        logger.info(f"📖 Analyse du fichier: {log_file}")
        
        # Lire les dernières lignes
        lines = tail_log_file(log_file, lines_to_read)
        if not lines:
            logger.warning("Aucune ligne lue")
            return 1
        
        logger.info(f"📋 {len(lines)} lignes lues")
        
        # Parser les entrées
        entries = [parse_log_entry(line) for line in lines]
        
        # Appliquer les filtres
        if filters:
            entries = filter_log_entries(entries, filters)
            logger.info(f"🔍 {len(entries)} entrées après filtrage")
        
        # Analyser
        analysis = analyze_log_patterns(entries)
        display_analysis(analysis)
        
        # TODO: Surveillance en temps réel si nécessaire
        # monitor_log_real_time(log_file)
        
        logger.info("✅ Analyse terminée")
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
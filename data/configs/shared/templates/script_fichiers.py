#!/usr/bin/env python3
"""
Template Recherche de Fichiers - PaniniFS
Simplification des opérations de recherche et manipulation de fichiers.
"""

import os
import re
import glob
import mimetypes
from pathlib import Path
import logging

# Configuration Panini
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
logger = logging.getLogger(__name__)

def search_files_by_pattern(directory, file_pattern, recursive=True):
    """Recherche des fichiers selon un pattern."""
    directory = Path(directory)
    results = []
    
    if recursive:
        pattern = f"**/{file_pattern}"
        matches = directory.glob(pattern)
    else:
        matches = directory.glob(file_pattern)
    
    for match in matches:
        if match.is_file():
            results.append(match)
    
    return sorted(results)

def search_content_in_files(files, search_pattern, case_sensitive=True):
    """Recherche un pattern dans le contenu des fichiers."""
    results = []
    flags = 0 if case_sensitive else re.IGNORECASE
    
    try:
        regex = re.compile(search_pattern, flags)
    except re.error as e:
        logger.error(f"❌ Pattern regex invalide: {e}")
        return []
    
    for file_path in files:
        try:
            # Vérifier si le fichier est texte
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and not mime_type.startswith('text'):
                continue
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if regex.search(line):
                        results.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.strip()
                        })
                        
        except (UnicodeDecodeError, PermissionError, OSError) as e:
            logger.warning(f"⚠️ Erreur lecture {file_path}: {e}")
            continue
    
    return results

def filter_files_by_size(files, min_size=None, max_size=None):
    """Filtre les fichiers par taille."""
    filtered = []
    
    for file_path in files:
        try:
            size = file_path.stat().st_size
            
            if min_size and size < min_size:
                continue
            if max_size and size > max_size:
                continue
                
            filtered.append(file_path)
            
        except OSError:
            continue
    
    return filtered

def display_search_results(results, max_results=50):
    """Affiche les résultats de recherche."""
    if not results:
        logger.info("Aucun résultat trouvé")
        return
    
    total = len(results)
    displayed = min(total, max_results)
    
    logger.info(f"📊 {total} résultats trouvés (affichage des {displayed} premiers)")
    
    for i, result in enumerate(results[:max_results]):
        if isinstance(result, dict):  # Résultat de recherche de contenu
            file_path = result['file']
            line_num = result['line']
            content = result['content'][:80] + "..." if len(result['content']) > 80 else result['content']
            logger.info(f"  {i+1}. {file_path}:{line_num} - {content}")
        else:  # Résultat de recherche de fichier
            logger.info(f"  {i+1}. {result}")

def copy_or_move_files(files, destination, operation='copy'):
    """Copie ou déplace les fichiers vers une destination."""
    import shutil
    
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for file_path in files:
        try:
            dest_path = destination / file_path.name
            
            if operation == 'copy':
                shutil.copy2(file_path, dest_path)
                logger.info(f"📋 Copié: {file_path} → {dest_path}")
            elif operation == 'move':
                shutil.move(str(file_path), str(dest_path))
                logger.info(f"📦 Déplacé: {file_path} → {dest_path}")
            
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Erreur {operation} {file_path}: {e}")
    
    return success_count

def main():
    """Fonction principale."""
    try:
        # TODO: Configurer les paramètres de recherche
        search_directory = "."  # Répertoire de recherche
        file_pattern = "*.py"  # Pattern de fichiers
        content_pattern = None  # Pattern de contenu (optionnel)
        
        logger.info(f"🔍 Recherche dans: {search_directory}")
        logger.info(f"📋 Pattern fichiers: {file_pattern}")
        
        # Rechercher les fichiers
        files = search_files_by_pattern(search_directory, file_pattern)
        logger.info(f"📁 {len(files)} fichiers trouvés")
        
        if not files:
            return 0
        
        # Recherche dans le contenu si spécifié
        if content_pattern:
            logger.info(f"🔎 Recherche contenu: {content_pattern}")
            content_results = search_content_in_files(files, content_pattern)
            display_search_results(content_results)
        else:
            display_search_results(files)
        
        # TODO: Ajouter traitement supplémentaire si nécessaire
        # Exemple: copier les fichiers trouvés
        # copy_or_move_files(files, "destination/", "copy")
        
        logger.info("✅ Recherche terminée")
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
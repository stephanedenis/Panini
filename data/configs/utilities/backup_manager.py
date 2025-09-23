#!/usr/bin/env python3
"""
💾 BACKUP MANAGER - Gestionnaire de Sauvegardes
Utilitaire pour créer et gérer les sauvegardes du projet
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import tarfile

def create_incremental_backup():
    """Créer sauvegarde incrémentale intelligente"""
    
    print("💾 BACKUP MANAGER")
    print("🎯 Sauvegarde incrémentale intelligente")
    print("=" * 50)
    
    # Configuration backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("archives/backups")
    backup_name = f"backup_incremental_{timestamp}"
    backup_path = backup_dir / backup_name
    
    # Créer structure backup
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path.mkdir(exist_ok=True)
    
    print(f"📁 Destination : {backup_path}")
    
    # Éléments critiques à sauvegarder
    critical_items = [
        ("copilotage", "🤖 Coordination agents"),
        ("production", "📦 Documents finaux"),
        ("research/discoveries", "📚 Découvertes recherche"),
        ("data/references_cache", "📊 Cache références"),
        ("README.md", "📄 Documentation principale"),
        ("README_NAVIGATION.md", "📋 Guide navigation")
    ]
    
    backed_up = 0
    total_size = 0
    
    print(f"\n📦 SAUVEGARDE EN COURS :")
    
    for item, description in critical_items:
        source = Path(item)
        if source.exists():
            try:
                dest = backup_path / item
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if source.is_dir():
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    size = sum(f.stat().st_size for f in source.rglob('*') if f.is_file())
                else:
                    shutil.copy2(source, dest)
                    size = source.stat().st_size
                
                backed_up += 1
                total_size += size
                print(f"   ✅ {item} - {description} ({size} bytes)")
                
            except Exception as e:
                print(f"   ❌ {item} - Erreur : {e}")
        else:
            print(f"   ⏭️  {item} - N'existe pas")
    
    # Métadonnées backup
    metadata = {
        "timestamp": timestamp,
        "items_backed_up": backed_up,
        "total_size": total_size,
        "backup_type": "incremental",
        "critical_items": [item for item, _ in critical_items],
        "created_by": "backup_manager.py"
    }
    
    with open(backup_path / "backup_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📊 RÉSUMÉ BACKUP :")
    print(f"   📦 Éléments sauvés : {backed_up}")
    print(f"   💾 Taille totale : {total_size:,} bytes")
    print(f"   📁 Localisation : {backup_path}")
    
    return backup_path, backed_up

def create_archive_backup():
    """Créer archive complète compressée"""
    
    print(f"\n🗜️  CRÉATION ARCHIVE COMPRESSÉE :")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"paniniFS_complete_{timestamp}.tar.gz"
    archive_path = Path("archives/backups") / archive_name
    
    # Créer archive tar.gz
    with tarfile.open(archive_path, "w:gz") as tar:
        # Ajouter dossiers critiques
        for item in ["copilotage", "production", "research", "data"]:
            if Path(item).exists():
                tar.add(item, arcname=item)
                print(f"   ✅ Ajouté : {item}/")
        
        # Ajouter fichiers racine importants
        for item in ["README.md", "README_NAVIGATION.md"]:
            if Path(item).exists():
                tar.add(item, arcname=item)
                print(f"   ✅ Ajouté : {item}")
    
    archive_size = archive_path.stat().st_size
    print(f"   📦 Archive créée : {archive_name}")
    print(f"   💾 Taille : {archive_size:,} bytes")
    
    return archive_path, archive_size

def cleanup_old_backups(keep_last=5):
    """Nettoyer anciennes sauvegardes"""
    
    print(f"\n🧹 NETTOYAGE ANCIENNES SAUVEGARDES :")
    
    backup_dir = Path("archives/backups")
    if not backup_dir.exists():
        print("   ⏭️  Aucun dossier backup")
        return
    
    # Lister backups existants
    backup_dirs = [d for d in backup_dir.iterdir() if d.is_dir() and d.name.startswith("backup_")]
    backup_files = [f for f in backup_dir.iterdir() if f.is_file() and f.name.endswith(".tar.gz")]
    
    # Trier par date (plus récent en premier)
    backup_dirs.sort(key=lambda x: x.name, reverse=True)
    backup_files.sort(key=lambda x: x.name, reverse=True)
    
    cleaned = 0
    
    # Nettoyer dossiers backup
    if len(backup_dirs) > keep_last:
        for old_backup in backup_dirs[keep_last:]:
            try:
                shutil.rmtree(old_backup)
                cleaned += 1
                print(f"   🗑️  Supprimé : {old_backup.name}")
            except Exception as e:
                print(f"   ❌ Erreur suppression {old_backup.name} : {e}")
    
    # Nettoyer archives
    if len(backup_files) > keep_last:
        for old_archive in backup_files[keep_last:]:
            try:
                old_archive.unlink()
                cleaned += 1
                print(f"   🗑️  Supprimé : {old_archive.name}")
            except Exception as e:
                print(f"   ❌ Erreur suppression {old_archive.name} : {e}")
    
    print(f"   📊 {cleaned} anciens backups supprimés")
    print(f"   📁 {len(backup_dirs[:keep_last]) + len(backup_files[:keep_last])} backups conservés")

def list_available_backups():
    """Lister sauvegardes disponibles"""
    
    print(f"\n📋 SAUVEGARDES DISPONIBLES :")
    
    backup_dir = Path("archives/backups")
    if not backup_dir.exists():
        print("   ⏭️  Aucune sauvegarde trouvée")
        return
    
    # Lister dossiers backup
    backup_dirs = [d for d in backup_dir.iterdir() if d.is_dir() and d.name.startswith("backup_")]
    backup_files = [f for f in backup_dir.iterdir() if f.is_file() and f.name.endswith(".tar.gz")]
    
    for backup in sorted(backup_dirs, reverse=True):
        metadata_file = backup / "backup_metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            print(f"   📁 {backup.name} - {metadata.get('items_backed_up', '?')} items")
        else:
            print(f"   📁 {backup.name} - Métadonnées manquantes")
    
    for archive in sorted(backup_files, reverse=True):
        size = archive.stat().st_size
        print(f"   🗜️  {archive.name} - {size:,} bytes")

def main():
    """Gestionnaire principal de sauvegardes"""
    
    os.chdir(Path(__file__).parent.parent.parent)  # Retour racine
    
    print("💾 BACKUP MANAGER PANINI-FS")
    print("🎯 Gestion intelligente des sauvegardes")
    print()
    
    # 1. Sauvegarde incrémentale
    backup_path, items = create_incremental_backup()
    
    # 2. Archive complète
    archive_path, archive_size = create_archive_backup()
    
    # 3. Nettoyage automatique
    cleanup_old_backups(keep_last=3)
    
    # 4. Liste des backups
    list_available_backups()
    
    print(f"\n🎉 BACKUP TERMINÉ")
    print(f"   📁 Backup incrémental : {items} éléments")
    print(f"   🗜️  Archive complète : {archive_size:,} bytes")
    print(f"   📍 Localisation : archives/backups/")
    
    return 0

if __name__ == "__main__":
    exit(main())

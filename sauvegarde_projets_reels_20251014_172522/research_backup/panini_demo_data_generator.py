#!/usr/bin/env python3
"""
🎬 PANINI-FS DEMO DATA GENERATOR
============================================================
🎯 Mission: Générer données de démonstration pour VFS
🔬 Focus: Batch simulé avec doublons et métadonnées
🚀 Usage: Créer environnement de test pour architecture VFS

Générateur de données simulées pour démontrer capacités
du système de fichiers virtuel PaniniFS.
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import random

class PaniniDemoDataGenerator:
    """Générateur de données de démonstration PaniniFS"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(".")
        
    def generate_demo_batch(self) -> str:
        """Générer batch de démonstration"""
        print("🎬 Génération données de démonstration PaniniFS...")
        
        # Fichiers simulés avec doublons intentionnels
        demo_files = [
            # Groupe 1: Documents Samuel CD
            {
                'filename': 'Samuel CD.pdf',
                'content': 'Document Samuel CD original',
                'size': 142700,
                'type': 'pdf'
            },
            {
                'filename': 'Samuel CD (1).pdf',
                'content': 'Document Samuel CD original',  # Même contenu = doublon
                'size': 142700,
                'type': 'pdf'
            },
            
            # Groupe 2: Documents temporels
            {
                'filename': 'Samuel CD Jul 23.pdf',
                'content': 'Document Samuel CD version juillet',
                'size': 142100,
                'type': 'pdf'
            },
            {
                'filename': 'Samuel CD Jul 23 (1).pdf',
                'content': 'Document Samuel CD version juillet',  # Doublon
                'size': 142100,
                'type': 'pdf'
            },
            
            # Groupe 3: Série versionnée
            {
                'filename': 'Samuel CD Sepp 14.pdf',
                'content': 'Document Samuel CD septembre 14',
                'size': 142100,
                'type': 'pdf'
            },
            {
                'filename': 'Samuel CD Sepp 14 (1).pdf',
                'content': 'Document Samuel CD septembre 14',  # Doublon
                'size': 142100,
                'type': 'pdf'
            },
            {
                'filename': 'Samuel CD Sepp 14 (2).pdf',
                'content': 'Document Samuel CD septembre 14',  # Doublon
                'size': 142100,
                'type': 'pdf'
            },
            
            # Autres types de fichiers
            {
                'filename': 'presentation_slides.pptx',
                'content': 'Présentation PowerPoint avec slides multiples',
                'size': 2500000,
                'type': 'pptx'
            },
            {
                'filename': 'image_collection.zip',
                'content': 'Archive contenant collection d\'images',
                'size': 15000000,
                'type': 'zip'
            },
            {
                'filename': 'data_analysis.xlsx',
                'content': 'Feuille Excel avec analyses de données',
                'size': 850000,
                'type': 'xlsx'
            },
            {
                'filename': 'readme.txt',
                'content': 'Fichier texte simple avec instructions',
                'size': 1250,
                'type': 'txt'
            },
            {
                'filename': 'config.json',
                'content': '{"version": "1.0", "settings": {"debug": true}}',
                'size': 156,
                'type': 'json'
            },
            
            # Documents génériques pour tests
            {
                'filename': 'rapport_mensuel.pdf',
                'content': 'Rapport mensuel des activités',
                'size': 890000,
                'type': 'pdf'
            },
            {
                'filename': 'photo_profile.jpg',
                'content': 'Photo de profil JPEG',
                'size': 125000,
                'type': 'jpg'
            },
            {
                'filename': 'video_demo.mp4',
                'content': 'Vidéo de démonstration courte',
                'size': 45000000,
                'type': 'mp4'
            }
        ]
        
        # Générer métadonnées pour chaque fichier
        batch_data = {
            'metadata': {
                'batch_id': f"demo_batch_{self.session_id}",
                'created': datetime.now().isoformat(),
                'purpose': 'demonstration',
                'total_files': len(demo_files),
                'simulated': True
            },
            'files': []
        }
        
        for file_info in demo_files:
            # Calculer hash du contenu
            content_hash = hashlib.sha256(file_info['content'].encode()).hexdigest()
            
            # Simuler compression (ratio réaliste)
            compression_ratio = self._get_compression_ratio(file_info['type'])
            compressed_size = int(file_info['size'] * compression_ratio)
            
            # Métadonnées enrichies
            file_metadata = {
                'original_filename': file_info['filename'],
                'content_hash': content_hash,
                'original_size': file_info['size'],
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'content_type': file_info['type'],
                'metadata': {
                    'panini_version': '2.1.0',
                    'compression_algorithm': 'gzip',
                    'timestamp': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'integrity_check': 'passed',
                    'file_category': self._categorize_file(file_info['filename']),
                    'semantic_hints': self._extract_semantic_hints(file_info['filename'])
                }
            }
            
            batch_data['files'].append(file_metadata)
        
        # Sauvegarder batch
        batch_filename = f"panini_universal_batch_{self.session_id}.json"
        batch_file = self.output_dir / batch_filename
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Batch de démonstration généré: {batch_file}")
        print(f"📊 Fichiers simulés: {len(demo_files)}")
        print(f"🔄 Groupes de doublons: 3 (total 7 fichiers dupliqués)")
        print(f"💾 Taille totale simulée: {sum(f['size'] for f in demo_files) / 1024 / 1024:.1f} MB")
        
        return str(batch_file)
    
    def _get_compression_ratio(self, file_type: str) -> float:
        """Calculer ratio de compression réaliste par type"""
        ratios = {
            'pdf': 0.936,  # PDFs se compressent bien
            'txt': 0.4,    # Texte se compresse très bien
            'json': 0.3,   # JSON se compresse excellemment
            'xlsx': 0.8,   # Excel déjà compressé
            'pptx': 0.85,  # PowerPoint déjà compressé
            'zip': 0.95,   # Archive déjà compressée
            'jpg': 0.98,   # Image déjà compressée
            'mp4': 0.99    # Vidéo déjà compressée
        }
        return ratios.get(file_type, 0.7)  # Défaut
    
    def _categorize_file(self, filename: str) -> str:
        """Catégoriser fichier par nom"""
        filename_lower = filename.lower()
        
        if 'samuel' in filename_lower:
            return 'personal_documents'
        elif filename_lower.endswith(('.pdf', '.doc', '.docx')):
            return 'documents'
        elif filename_lower.endswith(('.jpg', '.png', '.gif', '.bmp')):
            return 'images'
        elif filename_lower.endswith(('.mp4', '.avi', '.mov')):
            return 'videos'
        elif filename_lower.endswith(('.zip', '.rar', '.7z')):
            return 'archives'
        elif filename_lower.endswith(('.xls', '.xlsx', '.csv')):
            return 'spreadsheets'
        elif filename_lower.endswith(('.ppt', '.pptx')):
            return 'presentations'
        else:
            return 'miscellaneous'
    
    def _extract_semantic_hints(self, filename: str) -> list:
        """Extraire indices sémantiques du nom de fichier"""
        hints = []
        filename_lower = filename.lower()
        
        # Personnes
        if 'samuel' in filename_lower:
            hints.append('person:samuel')
        
        # Objets/supports
        if 'cd' in filename_lower:
            hints.append('media:cd')
        
        # Temporalité
        if any(month in filename_lower for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                                     'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
            hints.append('temporal:dated')
        
        # Numérotation/versions
        if any(char.isdigit() for char in filename_lower):
            hints.append('versioned')
        
        # Doublons détectés par pattern
        if '(' in filename_lower and ')' in filename_lower:
            hints.append('duplicate_copy')
        
        # Type de contenu
        if filename_lower.endswith('.pdf'):
            hints.extend(['document', 'textual_content'])
        elif filename_lower.endswith(('.jpg', '.png')):
            hints.extend(['image', 'visual_content'])
        elif filename_lower.endswith(('.zip', '.rar')):
            hints.extend(['archive', 'compressed'])
        
        return hints

    def run_demo_generation(self):
        """Exécuter génération complète des données de démo"""
        print("🎬 PANINI-FS DEMO DATA GENERATOR")
        print("="*50)
        print("🎯 Mission: Créer environnement de test VFS")
        print(f"⏰ Session: {datetime.now().isoformat()}")
        
        try:
            # Générer batch de démonstration
            batch_file = self.generate_demo_batch()
            
            print(f"\n🎉 DONNÉES DE DÉMONSTRATION PRÊTES !")
            print("="*50)
            print(f"📁 Batch généré: {Path(batch_file).name}")
            print(f"🚀 Prêt pour architecture VFS")
            
            print(f"\n💡 PROCHAINES ÉTAPES:")
            print(f"1. python panini_virtual_fs_architecture.py")
            print(f"2. python panini_web_interface_generator.py")
            print(f"3. python panini_webdav_server.py")
            
        except Exception as e:
            print(f"❌ Erreur génération démo: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    generator = PaniniDemoDataGenerator()
    generator.run_demo_generation()
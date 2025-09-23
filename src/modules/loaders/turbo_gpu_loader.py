"""
📥 Chargeur Turbo GPU - Module de Chargement Optimisé
Chargement continu des données du collecteur turbo avec optimisation GPU
"""

import os
import json
import glob
import time
from typing import Dict, Any, List
from datetime import datetime
from ..interfaces import LoaderInterface


class TurboGPULoader(LoaderInterface):
    """Chargeur optimisé pour données turbo avec accélération GPU"""
    
    def __init__(self):
        self.name = "TurboGPULoader"
        self.data_dirs = [
            'data/incremental_corpus',  # Données turbo temps réel
            'colab_results'             # Données historiques
        ]
        self.file_cache = {}
        self.last_scan_time = 0
        
    def load_data(self, source_config: Dict[str, Any]) -> Any:
        """Charge les données turbo de façon optimisée"""
        
        max_files = source_config.get('max_files', 50)
        recent_only = source_config.get('recent_only', True)
        min_age_minutes = source_config.get('min_age_minutes', 30)
        
        all_documents = []
        file_stats = {
            'total_files_scanned': 0,
            'turbo_files_found': 0,
            'documents_loaded': 0,
            'latest_batch_time': None,
            'load_time': 0
        }
        
        start_time = time.time()
        print(f"🔄 {self.name} - Scan données turbo...")
        
        for data_dir in self.data_dirs:
            if not os.path.exists(data_dir):
                continue
                
            # Scan fichiers turbo
            turbo_files = self._scan_turbo_files(data_dir, recent_only, min_age_minutes)
            other_files = self._scan_other_files(data_dir, max_files // 4)
            
            file_stats['total_files_scanned'] += len(turbo_files) + len(other_files)
            file_stats['turbo_files_found'] += len(turbo_files)
            
            print(f"📁 {data_dir}: {len(turbo_files)} turbo, {len(other_files)} autres")
            
            # Traitement prioritaire des fichiers turbo récents
            priority_files = turbo_files[:max_files] + other_files
            
            for filepath in priority_files:
                docs = self._load_file_optimized(filepath)
                if docs:
                    all_documents.extend(docs)
                    file_stats['documents_loaded'] += len(docs)
                    
                    # Tracking du fichier le plus récent
                    file_time = os.path.getmtime(filepath)
                    if (file_stats['latest_batch_time'] is None or 
                        file_time > file_stats['latest_batch_time']):
                        file_stats['latest_batch_time'] = file_time
        
        # Tri et filtrage final
        all_documents = self._optimize_document_selection(all_documents, source_config)
        
        file_stats['load_time'] = time.time() - start_time
        if file_stats['latest_batch_time']:
            file_stats['latest_batch_time'] = datetime.fromtimestamp(
                file_stats['latest_batch_time']).isoformat()
        
        print(f"✅ Chargement terminé: {len(all_documents)} docs en {file_stats['load_time']:.2f}s")
        
        return {
            'documents': all_documents,
            'metadata': file_stats
        }
    
    def _scan_turbo_files(self, data_dir: str, recent_only: bool, min_age_minutes: int) -> List[str]:
        """Scan optimisé des fichiers turbo"""
        pattern = os.path.join(data_dir, "turbo_batch_*.json")
        files = glob.glob(pattern)
        
        if recent_only:
            cutoff_time = time.time() - (min_age_minutes * 60)
            files = [f for f in files if os.path.getmtime(f) > cutoff_time]
        
        # Tri par timestamp (plus récents d'abord)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return files
    
    def _scan_other_files(self, data_dir: str, max_count: int) -> List[str]:
        """Scan des autres fichiers JSON"""
        pattern = os.path.join(data_dir, "*.json")
        all_files = glob.glob(pattern)
        other_files = [f for f in all_files if 'turbo_batch_' not in f]
        
        # Limiter et trier par timestamp
        other_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return other_files[:max_count]
    
    def _load_file_optimized(self, filepath: str) -> List[Dict[str, Any]]:
        """Chargement optimisé d'un fichier avec cache"""
        
        # Vérification cache
        file_mtime = os.path.getmtime(filepath)
        cache_key = filepath
        
        if (cache_key in self.file_cache and 
            self.file_cache[cache_key]['mtime'] == file_mtime):
            return self.file_cache[cache_key]['documents']
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            if 'documents' in data:
                documents = data['documents']
            elif isinstance(data, list):
                documents = data
            elif 'content' in data:
                documents = [data]
            
            # Enrichissement rapide
            enriched_docs = []
            is_turbo = 'turbo_batch_' in filepath
            
            for doc in documents:
                if isinstance(doc, dict):
                    content = doc.get('content', '') + ' ' + doc.get('title', '')
                    language = doc.get('language', 'auto')
                    quality = doc.get('quality_score', 0.5)
                else:
                    content = str(doc)
                    language = 'auto'
                    quality = 0.5
                
                # Filtres adaptatifs
                min_len = 40 if is_turbo else 60
                max_len = 12000
                
                if min_len < len(content) < max_len:
                    enriched_doc = {
                        'content': content,
                        'language': language,
                        'source': os.path.basename(filepath),
                        'type': 'turbo_continuous' if is_turbo else 'historical',
                        'quality_score': quality,
                        'timestamp': file_mtime,
                        'word_count': len(content.split())
                    }
                    enriched_docs.append(enriched_doc)
            
            # Mise en cache
            self.file_cache[cache_key] = {
                'mtime': file_mtime,
                'documents': enriched_docs
            }
            
            return enriched_docs
            
        except Exception as e:
            print(f"⚠️ Erreur lecture {os.path.basename(filepath)}: {e}")
            return []
    
    def _optimize_document_selection(self, documents: List[Dict[str, Any]], 
                                   config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimise la sélection des documents selon la config"""
        
        max_docs = config.get('max_documents', 500)
        quality_threshold = config.get('quality_threshold', 0.3)
        
        # Filtrage qualité
        filtered_docs = [doc for doc in documents 
                        if doc.get('quality_score', 0) >= quality_threshold]
        
        # Tri multi-critères : qualité + fraîcheur + type
        def sort_key(doc):
            quality = doc.get('quality_score', 0)
            timestamp = doc.get('timestamp', 0)
            is_turbo = 1 if doc.get('type') == 'turbo_continuous' else 0
            return (is_turbo, quality, timestamp)
        
        filtered_docs.sort(key=sort_key, reverse=True)
        
        # Limitation finale
        return filtered_docs[:max_docs]
    
    def validate_data(self, data: Any) -> bool:
        """Valide la qualité des données chargées"""
        if not isinstance(data, dict):
            return False
        
        documents = data.get('documents', [])
        metadata = data.get('metadata', {})
        
        # Validations basiques
        if not documents:
            return False
        
        # Vérification qualité documents
        valid_count = 0
        for doc in documents:
            if (isinstance(doc, dict) and 
                'content' in doc and 
                len(doc['content']) > 30):
                valid_count += 1
        
        validity_ratio = valid_count / len(documents)
        
        print(f"📊 Validation: {valid_count}/{len(documents)} docs valides ({validity_ratio:.1%})")
        
        return validity_ratio >= 0.7  # Au moins 70% de documents valides
    
    def get_load_statistics(self) -> Dict[str, Any]:
        """Statistiques de chargement"""
        return {
            'cached_files': len(self.file_cache),
            'cache_size_mb': sum(len(str(cache_data)) for cache_data in self.file_cache.values()) / (1024*1024),
            'data_directories': self.data_dirs,
            'last_scan': self.last_scan_time
        }
    
    def clear_cache(self):
        """Vide le cache de fichiers"""
        self.file_cache.clear()
        print(f"🧹 Cache {self.name} vidé")
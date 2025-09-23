#!/usr/bin/env python3
"""
🚀 Turbo Corpus Collector - Version haute vitesse pour nourrir Colab
Collecte intensive avec sources multiples et débit optimisé
"""

import requests
import json
import time
import os
import logging
import threading
from datetime import datetime
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor
import queue

class TurboCorpusCollector:
    def __init__(self):
        self.base_dir = "data/incremental_corpus"
        self.results_dir = "colab_results"
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Configuration haute vitesse
        self.batch_size = 15  # Plus gros batches
        self.concurrent_requests = 5  # Requêtes parallèles
        self.delay_between_batches = 10  # 10 secondes entre batches
        self.max_workers = 4  # Workers parallèles
        
        # Queue pour les documents
        self.doc_queue = queue.Queue(maxsize=100)
        
        # Sources diversifiées
        self.sources = {
            'wikipedia_sanskrit': {
                'topics': ['Sanskrit', 'Panini', 'Ashtadhyayi', 'Vyakarana', 'Dhatu', 
                          'Vedas', 'Upanishads', 'Mahabharata', 'Ramayana', 'Purana'],
                'languages': ['en', 'fr', 'de', 'es']
            },
            'wikipedia_linguistics': {
                'topics': ['Grammar', 'Morphology', 'Phonology', 'Syntax', 'Semantics',
                          'Etymology', 'Philology', 'Historical linguistics', 'Verb', 'Root'],
                'languages': ['en', 'fr', 'de']
            },
            'wikipedia_philosophy': {
                'topics': ['Indian philosophy', 'Ancient philosophy', 'Language philosophy',
                          'Logic', 'Epistemology', 'Metaphysics'],
                'languages': ['en', 'fr']
            }
        }
        
        # Session réutilisable
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PaniniFS-Research-Turbo/1.0 (Educational)'
        })
        
        # Logging optimisé
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('turbo_collector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'docs_collected': 0,
            'batches_created': 0,
            'errors': 0,
            'sources_used': set()
        }

    def get_wikipedia_content_fast(self, topic, lang='en', source_type='wikipedia'):
        """Récupération ultra-rapide Wikipedia"""
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            response = self.session.get(url, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('extract', '')
                
                if len(content) > 50:  # Filtre minimal
                    return {
                        'title': data.get('title', topic),
                        'content': content,
                        'source': f'{source_type}_{lang}',
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        'timestamp': datetime.now().isoformat(),
                        'language': lang,
                        'topic_category': source_type
                    }
        except Exception as e:
            self.logger.debug(f"Erreur {topic} ({lang}): {e}")
            self.stats['errors'] += 1
            return None

    def collect_from_source_parallel(self, source_name, config):
        """Collecte parallèle d'une source"""
        documents = []
        topics = random.sample(config['topics'], min(5, len(config['topics'])))
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            
            for topic in topics:
                for lang in config['languages']:
                    future = executor.submit(
                        self.get_wikipedia_content_fast, 
                        topic, lang, source_name
                    )
                    futures.append(future)
            
            for future in futures:
                try:
                    doc = future.result(timeout=5)
                    if doc:
                        documents.append(doc)
                        self.stats['docs_collected'] += 1
                        self.stats['sources_used'].add(source_name)
                except Exception as e:
                    self.logger.debug(f"Future échoué: {e}")
        
        return documents

    def turbo_collect_batch(self):
        """Collection turbo avec toutes les sources"""
        all_documents = []
        
        # Collecte parallèle de toutes les sources
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for source_name, config in self.sources.items():
                future = executor.submit(self.collect_from_source_parallel, source_name, config)
                futures.append(future)
            
            for future in futures:
                try:
                    docs = future.result(timeout=15)
                    all_documents.extend(docs)
                except Exception as e:
                    self.logger.warning(f"Source échouée: {e}")
        
        # Mélanger et limiter
        random.shuffle(all_documents)
        return all_documents[:self.batch_size]

    def enhance_document_quality(self, documents):
        """Améliorer la qualité des documents"""
        enhanced = []
        
        for doc in documents:
            # Calculer score de qualité amélioré
            quality_score = self.calculate_enhanced_quality(doc)
            
            if quality_score > 0.4:  # Seuil qualité
                doc['quality_score'] = quality_score
                doc['dhatu_potential'] = self.estimate_dhatu_potential(doc)
                enhanced.append(doc)
        
        # Trier par qualité
        enhanced.sort(key=lambda x: x['quality_score'], reverse=True)
        return enhanced

    def calculate_enhanced_quality(self, doc):
        """Score de qualité amélioré"""
        score = 0.3  # Base
        content = doc['content'].lower()
        
        # Longueur optimale
        length = len(doc['content'])
        if 200 <= length <= 2000:
            score += 0.2
        elif length > 100:
            score += 0.1
        
        # Mots-clés sanskrit/linguistique
        high_value_keywords = [
            'sanskrit', 'grammar', 'verb', 'root', 'dhatu', 'panini',
            'linguistic', 'morphology', 'syntax', 'phonology', 'etymology'
        ]
        for keyword in high_value_keywords:
            if keyword in content:
                score += 0.15
        
        # Bonus langue
        if doc['language'] in ['en', 'fr']:
            score += 0.1
        
        # Bonus source académique
        if 'philosophy' in doc.get('topic_category', ''):
            score += 0.1
        
        return min(score, 1.0)

    def estimate_dhatu_potential(self, doc):
        """Estimation du potentiel dhātu"""
        content = doc['content'].lower()
        indicators = [
            'verb', 'root', 'stem', 'inflection', 'conjugation',
            'tense', 'aspect', 'voice', 'mood', 'participle'
        ]
        
        count = sum(1 for indicator in indicators if indicator in content)
        return min(count / len(indicators), 1.0)

    def save_turbo_batch(self, documents):
        """Sauvegarde optimisée du batch"""
        if not documents:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"turbo_batch_{timestamp}.json"
        filepath = os.path.join(self.base_dir, filename)
        
        # Métadonnées enrichies
        avg_quality = sum(doc.get('quality_score', 0) for doc in documents) / len(documents)
        avg_dhatu_potential = sum(doc.get('dhatu_potential', 0) for doc in documents) / len(documents)
        
        batch_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'collector': 'turbo_corpus_collector',
                'version': '1.0',
                'count': len(documents),
                'avg_quality_score': round(avg_quality, 3),
                'avg_dhatu_potential': round(avg_dhatu_potential, 3),
                'sources_used': list(self.stats['sources_used']),
                'processing_speed': 'turbo'
            },
            'documents': documents
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
        self.stats['batches_created'] += 1
        self.logger.info(f"💾 Turbo batch sauvé: {filename} ({len(documents)} docs, Q:{avg_quality:.3f})")
        return filepath

    def git_push_async(self):
        """Push Git asynchrone pour ne pas bloquer"""
        def push_worker():
            try:
                subprocess.run(['git', 'add', 'data/incremental_corpus/'], 
                             check=True, capture_output=True, timeout=10)
                
                commit_msg = f"🚀 Turbo batch: {self.stats['docs_collected']} docs (Q:{len(self.stats['sources_used'])} sources)"
                subprocess.run(['git', 'commit', '-m', commit_msg], 
                             check=True, capture_output=True, timeout=10)
                
                subprocess.run(['git', 'push', 'origin', 'main'], 
                             check=True, capture_output=True, timeout=15)
                
                self.logger.info("🚀 Push Git réussi!")
                
            except subprocess.TimeoutExpired:
                self.logger.warning("⏰ Git push timeout")
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"Git push échoué: {e}")
        
        # Lancer en thread séparé
        threading.Thread(target=push_worker, daemon=True).start()

    def run_turbo_cycle(self):
        """Cycle de collecte turbo"""
        cycle_start = time.time()
        self.logger.info("🔥 Démarrage cycle TURBO...")
        
        # Collecte massive
        raw_documents = self.turbo_collect_batch()
        self.logger.info(f"📥 {len(raw_documents)} documents bruts collectés")
        
        if raw_documents:
            # Amélioration qualité
            enhanced_documents = self.enhance_document_quality(raw_documents)
            self.logger.info(f"✨ {len(enhanced_documents)} documents de qualité retenus")
            
            if enhanced_documents:
                # Sauvegarde
                filepath = self.save_turbo_batch(enhanced_documents)
                
                # Push asynchrone
                if filepath:
                    self.git_push_async()
                
                cycle_time = time.time() - cycle_start
                throughput = len(enhanced_documents) / cycle_time * 60  # docs/min
                
                self.logger.info(f"⚡ Cycle terminé: {len(enhanced_documents)} docs en {cycle_time:.1f}s ({throughput:.1f} docs/min)")
                return len(enhanced_documents)
        
        return 0

    def run_turbo_mode(self, duration_minutes=30):
        """Mode turbo continu"""
        self.logger.info(f"🚀 MODE TURBO démarré pour {duration_minutes} minutes!")
        
        start_time = time.time()
        total_docs = 0
        cycles = 0
        
        while (time.time() - start_time) < (duration_minutes * 60):
            cycles += 1
            self.logger.info(f"🔥 CYCLE TURBO {cycles}")
            
            docs_this_cycle = self.run_turbo_cycle()
            total_docs += docs_this_cycle
            
            # Stats intermédiaires
            elapsed = (time.time() - start_time) / 60
            rate = total_docs / elapsed if elapsed > 0 else 0
            
            self.logger.info(f"📊 Total: {total_docs} docs en {cycles} cycles ({rate:.1f} docs/min)")
            
            # Pause adaptative basée sur la performance
            if docs_this_cycle > 10:
                pause = self.delay_between_batches * 0.5  # Pause courte si performant
            else:
                pause = self.delay_between_batches  # Pause normale
            
            self.logger.info(f"⏸️ Pause {pause}s avant prochain cycle...")
            time.sleep(pause)
        
        # Stats finales
        self.stats['end_time'] = datetime.now().isoformat()
        self.stats['total_docs'] = total_docs
        self.stats['cycles'] = cycles
        self.save_turbo_stats()
        
        final_rate = total_docs / (duration_minutes) if duration_minutes > 0 else 0
        self.logger.info(f"🏁 MODE TURBO terminé: {total_docs} docs en {cycles} cycles ({final_rate:.1f} docs/min)")
        return total_docs

    def save_turbo_stats(self):
        """Sauvegarde des stats turbo"""
        # Convertir set en list pour JSON
        stats_copy = self.stats.copy()
        stats_copy['sources_used'] = list(stats_copy['sources_used'])
        
        stats_file = os.path.join(self.results_dir, 'turbo_collector_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_copy, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"📊 Stats turbo sauvées: {stats_file}")

def main():
    """Point d'entrée turbo"""
    collector = TurboCorpusCollector()
    
    print("🚀 TURBO CORPUS COLLECTOR - Mode haute vitesse!")
    print("Collecte intensive pour nourrir Colab rapidement")
    
    try:
        total_docs = collector.run_turbo_mode(duration_minutes=15)  # 15 minutes turbo
        print(f"✅ Collecte TURBO terminée: {total_docs} documents!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Collecte turbo interrompue")
        collector.save_turbo_stats()
    except Exception as e:
        collector.logger.error(f"❌ Erreur turbo: {e}")
        collector.save_turbo_stats()

if __name__ == "__main__":
    main()
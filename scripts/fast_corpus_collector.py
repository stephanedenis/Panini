#!/usr/bin/env python3
"""
🚀 Fast Corpus Collector - Version optimisée et rapide
Collecte efficace de documents avec focus sur la vitesse et l'interaction Colab
"""

import requests
import json
import time
import os
import logging
from datetime import datetime
import random
import subprocess

class FastCorpusCollector:
    def __init__(self):
        self.base_dir = "data/incremental_corpus"
        self.results_dir = "colab_results"
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Configuration simplifiée
        self.batch_size = 5  # Plus petit pour plus de réactivité
        self.delay_between_requests = 1  # Plus rapide
        self.max_docs_per_run = 20  # Limite pour éviter la lenteur
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PaniniFS-Research/1.0 (https://github.com/stephanedenis/PaniniFS-Research)'
        })
        
        # Logging simple
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('fast_collector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'docs_collected': 0,
            'batches_created': 0,
            'errors': 0
        }

    def get_wikipedia_content(self, topic, lang='en'):
        """Récupération rapide Wikipedia"""
        try:
            # API Wikipedia simplifiée
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{topic}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', topic),
                    'content': data.get('extract', ''),
                    'source': f'wikipedia_{lang}',
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.warning(f"Erreur Wikipedia {topic}: {e}")
            return None

    def collect_batch(self):
        """Collecte un batch rapide"""
        topics = [
            'Sanskrit', 'Panini', 'Grammar', 'Linguistics', 'Verb',
            'Philosophy', 'India', 'Language', 'Etymology', 'Morphology',
            'Syntax', 'Phonetics', 'Literature', 'Ancient', 'Text'
        ]
        
        documents = []
        
        for i in range(self.batch_size):
            topic = random.choice(topics)
            doc = self.get_wikipedia_content(topic)
            
            if doc and len(doc['content']) > 100:
                documents.append(doc)
                self.stats['docs_collected'] += 1
                self.logger.info(f"✅ Collecté: {doc['title'][:50]}...")
            
            time.sleep(self.delay_between_requests)
        
        return documents

    def save_batch(self, documents):
        """Sauvegarde rapide du batch"""
        if not documents:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fast_batch_{timestamp}.json"
        filepath = os.path.join(self.base_dir, filename)
        
        batch_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'collector': 'fast_corpus_collector',
                'count': len(documents),
                'quality_score': self.calculate_quality_score(documents)
            },
            'documents': documents
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
        self.stats['batches_created'] += 1
        self.logger.info(f"💾 Batch sauvé: {filename} ({len(documents)} docs)")
        return filepath

    def calculate_quality_score(self, documents):
        """Score de qualité simplifié"""
        if not documents:
            return 0.0
        
        total_score = 0
        for doc in documents:
            score = 0.5  # Base
            
            # Bonus longueur
            if len(doc['content']) > 500:
                score += 0.2
            
            # Bonus mots-clés
            content_lower = doc['content'].lower()
            keywords = ['sanskrit', 'grammar', 'linguistic', 'verb', 'language']
            for keyword in keywords:
                if keyword in content_lower:
                    score += 0.1
            
            total_score += min(score, 1.0)
        
        return round(total_score / len(documents), 3)

    def push_to_github(self):
        """Push rapide vers GitHub"""
        try:
            # Ajouter et committer
            subprocess.run(['git', 'add', 'data/incremental_corpus/'], check=True, capture_output=True)
            
            commit_msg = f"📦 Fast batch: {self.stats['docs_collected']} docs collectés"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            # Push
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
            self.logger.info("🚀 Poussé vers GitHub!")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Git push échoué: {e}")
            return False

    def check_colab_feedback(self):
        """Vérifie le feedback de Colab"""
        feedback_file = os.path.join(self.results_dir, 'colab_feedback.json')
        
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    feedback = json.load(f)
                
                self.logger.info(f"📨 Feedback Colab reçu: {feedback.get('timestamp', 'Unknown')}")
                
                # Adapter le comportement basé sur le feedback
                recs = feedback.get('collector_recommendations', {})
                if recs.get('focus_on_high_quality'):
                    self.batch_size = max(3, self.batch_size - 1)  # Réduire pour qualité
                
                return feedback
                
            except Exception as e:
                self.logger.warning(f"Erreur lecture feedback: {e}")
        
        return None

    def run_collection_cycle(self):
        """Un cycle de collecte rapide"""
        self.logger.info("🔄 Démarrage cycle de collecte...")
        
        # Vérifier feedback Colab
        self.check_colab_feedback()
        
        # Collecter
        documents = self.collect_batch()
        
        if documents:
            # Sauvegarder
            filepath = self.save_batch(documents)
            
            # Push vers GitHub
            if filepath:
                self.push_to_github()
                
            self.logger.info(f"✅ Cycle terminé: {len(documents)} docs")
        else:
            self.logger.warning("❌ Aucun document collecté ce cycle")
        
        return len(documents) if documents else 0

    def run_fast_mode(self, max_cycles=10):
        """Mode rapide avec cycles limités"""
        self.logger.info(f"🚀 Mode rapide: {max_cycles} cycles maximum")
        
        total_docs = 0
        
        for cycle in range(max_cycles):
            self.logger.info(f"📊 Cycle {cycle + 1}/{max_cycles}")
            
            docs_this_cycle = self.run_collection_cycle()
            total_docs += docs_this_cycle
            
            # Arrêter si on a assez de docs
            if total_docs >= self.max_docs_per_run:
                self.logger.info(f"🎯 Objectif atteint: {total_docs} docs")
                break
            
            # Pause entre cycles
            time.sleep(2)
        
        # Stats finales
        self.stats['end_time'] = datetime.now().isoformat()
        self.save_stats()
        
        self.logger.info(f"🏁 Collection terminée: {total_docs} docs en {cycle + 1} cycles")
        return total_docs

    def save_stats(self):
        """Sauvegarde des stats"""
        stats_file = os.path.join(self.results_dir, 'fast_collector_stats.json')
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"📊 Stats sauvées: {stats_file}")

def main():
    """Point d'entrée principal"""
    collector = FastCorpusCollector()
    
    print("🚀 Fast Corpus Collector démarré!")
    print("Mode rapide avec cycles limités pour interaction Colab optimale")
    
    try:
        total_docs = collector.run_fast_mode(max_cycles=5)  # 5 cycles seulement
        print(f"✅ Collection terminée: {total_docs} documents collectés!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Collection interrompue par l'utilisateur")
        collector.save_stats()
    except Exception as e:
        collector.logger.error(f"❌ Erreur fatale: {e}")
        collector.save_stats()

if __name__ == "__main__":
    main()
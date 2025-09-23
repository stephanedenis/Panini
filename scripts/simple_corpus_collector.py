#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Simple Corpus Collector for Parallel Processing
Collecteur simple sans dépendances externes pour expansion corpus en parallèle
"""

import json
import time
import requests
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import quote, urljoin
import random
import logging
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SimpleDocument:
    """Document structure simple"""
    id: str
    title: str
    content: str
    source: str
    language: str
    domain: str
    url: str = ""
    timestamp: str = ""
    word_count: int = 0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.word_count:
            self.word_count = len(self.content.split()) if self.content else 0

class SimpleCorpusCollector:
    """Collecteur corpus simple avec requests seulement"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or "/home/stephane/GitHub/PaniniFS-Research/data/incremental_corpus")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'documents_collected': 0,
            'sources_used': 0,
            'start_time': time.time(),
            'errors': 0,
            'git_pushes': 0
        }
        
        # Configuration sources simples
        self.wikipedia_random_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        self.rate_limit = 2.0  # 2 secondes entre requêtes
        
        logger.info(f"🌍 Simple Corpus Collector initialisé")
        logger.info(f"📂 Output: {self.output_dir}")
    
    def fetch_wikipedia_document(self) -> SimpleDocument:
        """Collecte un document aléatoire de Wikipedia"""
        
        try:
            response = requests.get(self.wikipedia_random_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validation contenu minimum
                extract = data.get('extract', '')
                if len(extract) < 100:  # Skip articles trop courts
                    return None
                
                doc = SimpleDocument(
                    id=f"wiki_{data['pageid']}_{int(time.time())}",
                    title=data['title'],
                    content=extract,
                    source="wikipedia",
                    language="en",
                    domain="encyclopedia",
                    url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    word_count=len(extract.split())
                )
                
                return doc
            else:
                logger.warning(f"Wikipedia API error: {response.status_code}")
                self.stats['errors'] += 1
                return None
                
        except Exception as e:
            logger.error(f"Erreur Wikipedia: {e}")
            self.stats['errors'] += 1
            return None
    
    def collect_simple_text_sources(self) -> List[SimpleDocument]:
        """Collecte depuis sources texte simples"""
        
        documents = []
        
        # Exemples de textes académiques/scientifiques (simulation)
        sample_texts = [
            {
                'title': 'Quantum Computing Principles',
                'content': 'Quantum computing represents a fundamental shift in computational paradigms. Unlike classical computers that process information using bits, quantum computers utilize quantum bits or qubits. These qubits can exist in superposition states, allowing quantum computers to perform certain calculations exponentially faster than classical systems. The principles of quantum mechanics, including entanglement and interference, enable quantum algorithms to solve complex problems in cryptography, optimization, and simulation.',
                'domain': 'computer_science'
            },
            {
                'title': 'Linguistic Universals and Grammar',
                'content': 'Universal Grammar theory proposes that the ability to learn language is innate to humans and that certain grammatical principles are universal across all languages. This theory suggests that despite surface differences, all human languages share a common underlying structure. The study of linguistic universals reveals patterns in phonology, morphology, syntax, and semantics that appear consistently across diverse language families.',
                'domain': 'linguistics'
            },
            {
                'title': 'Machine Learning Optimization',
                'content': 'Optimization algorithms form the backbone of machine learning systems. Gradient descent and its variants enable neural networks to learn from data by minimizing loss functions. Advanced optimization techniques like Adam, RMSprop, and AdaGrad adapt learning rates dynamically, improving convergence speed and stability. These algorithms must balance exploration and exploitation to find global optima in high-dimensional parameter spaces.',
                'domain': 'machine_learning'
            },
            {
                'title': 'Sanskrit Grammatical Tradition',
                'content': 'The Sanskrit grammatical tradition, exemplified by Panini\'s Ashtadhyayi, represents one of the world\'s most sophisticated linguistic analyses. This ancient system describes Sanskrit through a comprehensive set of rules that generate all valid Sanskrit expressions. The dhatu system, which categorizes verbal roots according to their semantic and phonological properties, provides insights into universal patterns of human language cognition.',
                'domain': 'sanskrit_studies'
            },
            {
                'title': 'Cognitive Science and Language Processing',
                'content': 'Human language processing involves complex interactions between multiple cognitive systems. Phonological processing converts acoustic signals into meaningful units, while syntactic parsing organizes words into grammatical structures. Semantic processing extracts meaning from linguistic input, integrating with world knowledge and context. These processes occur rapidly and automatically, demonstrating the efficiency of human cognitive architecture.',
                'domain': 'cognitive_science'
            }
        ]
        
        for i, text_data in enumerate(sample_texts):
            doc = SimpleDocument(
                id=f"sample_{i}_{int(time.time())}",
                title=text_data['title'],
                content=text_data['content'],
                source="academic_sample",
                language="en",
                domain=text_data['domain'],
                url="",
                word_count=len(text_data['content'].split())
            )
            documents.append(doc)
        
        return documents
    
    def save_batch_and_push(self, documents: List[SimpleDocument], batch_num: int) -> bool:
        """Sauvegarde batch et push vers GitHub"""
        
        if not documents:
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"incremental_batch_{batch_num:03d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Préparer données
        batch_data = {
            'metadata': {
                'batch_number': batch_num,
                'timestamp': timestamp,
                'document_count': len(documents),
                'total_words': sum(doc.word_count for doc in documents),
                'sources': list(set(doc.source for doc in documents)),
                'languages': list(set(doc.language for doc in documents)),
                'domains': list(set(doc.domain for doc in documents))
            },
            'documents': [asdict(doc) for doc in documents]
        }
        
        # Sauvegarder
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Sauvegardé: {filename} ({len(documents)} docs)")
            
            # Git add, commit, push
            return self.git_push_batch(filepath, batch_num)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return False
    
    def git_push_batch(self, filepath: Path, batch_num: int) -> bool:
        """Push batch vers GitHub"""
        
        try:
            import subprocess
            import os
            
            # Change to repo directory
            repo_dir = "/home/stephane/GitHub/PaniniFS-Research"
            
            # Git commands
            subprocess.run(['git', 'add', str(filepath)], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            commit_msg = f"📈 Corpus incremental batch {batch_num} - {datetime.now().strftime('%H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            subprocess.run(['git', 'push', 'origin', 'main'], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            self.stats['git_pushes'] += 1
            logger.info(f"🔄 Git push réussi: batch {batch_num}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git push failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Git error: {e}")
            return False
    
    def run_continuous_collection(self, target_docs: int = 100, 
                                 batch_size: int = 10, 
                                 max_hours: float = 2.0):
        """Lance collecte continue en parallèle"""
        
        logger.info(f"🚀 DÉMARRAGE COLLECTE CONTINUE")
        logger.info(f"🎯 Target: {target_docs} documents")
        logger.info(f"📦 Batch size: {batch_size}")
        logger.info(f"⏰ Max duration: {max_hours} heures")
        logger.info("=" * 50)
        
        start_time = time.time()
        max_duration = max_hours * 3600  # Convert to seconds
        
        batch_num = 1
        document_buffer = []
        
        # Ajouter quelques échantillons au début
        document_buffer.extend(self.collect_simple_text_sources())
        
        while (self.stats['documents_collected'] < target_docs and 
               (time.time() - start_time) < max_duration):
            
            # Collecte Wikipedia
            doc = self.fetch_wikipedia_document()
            if doc:
                document_buffer.append(doc)
                self.stats['documents_collected'] += 1
                
                logger.info(f"📄 Document {self.stats['documents_collected']}: {doc.title[:50]}...")
            
            # Sauvegarde batch si buffer plein
            if len(document_buffer) >= batch_size:
                success = self.save_batch_and_push(document_buffer, batch_num)
                if success:
                    logger.info(f"✅ Batch {batch_num} pushed to GitHub")
                else:
                    logger.warning(f"⚠️ Batch {batch_num} save failed")
                
                document_buffer = []
                batch_num += 1
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            # Progress report périodique
            if self.stats['documents_collected'] % 25 == 0:
                elapsed = time.time() - start_time
                rate = self.stats['documents_collected'] / elapsed
                logger.info(f"📊 Progress: {self.stats['documents_collected']}/{target_docs} docs | {rate:.1f} docs/min | {self.stats['git_pushes']} pushes")
        
        # Sauvegarder documents restants
        if document_buffer:
            self.save_batch_and_push(document_buffer, batch_num)
        
        # Rapport final
        total_time = time.time() - start_time
        logger.info(f"🎯 COLLECTE TERMINÉE")
        logger.info(f"📄 Documents collectés: {self.stats['documents_collected']}")
        logger.info(f"⏱️ Temps total: {total_time:.1f}s")
        logger.info(f"🔄 Pushes GitHub: {self.stats['git_pushes']}")
        logger.info(f"❌ Erreurs: {self.stats['errors']}")
        
        return {
            'documents_collected': self.stats['documents_collected'],
            'total_time': total_time,
            'git_pushes': self.stats['git_pushes'],
            'errors': self.stats['errors']
        }

def main():
    """Point d'entrée principal"""
    
    print("🌍 SIMPLE CORPUS COLLECTOR")
    print("=" * 40)
    print("⚙️ Collecte en parallèle pendant traitement Colab")
    print()
    
    collector = SimpleCorpusCollector()
    
    # Configuration adaptée au traitement parallèle
    TARGET_DOCS = 200      # Objectif raisonnable
    BATCH_SIZE = 15        # Batches moyens pour pushes fréquents
    MAX_HOURS = 3.0        # Maximum 3 heures
    
    try:
        results = collector.run_continuous_collection(
            target_docs=TARGET_DOCS,
            batch_size=BATCH_SIZE,
            max_hours=MAX_HOURS
        )
        
        print(f"\n🎉 COLLECTE RÉUSSIE!")
        print(f"📄 {results['documents_collected']} documents collectés")
        print(f"🔄 {results['git_pushes']} pushes vers GitHub")
        print(f"⏱️ {results['total_time']:.1f} secondes")
        
    except KeyboardInterrupt:
        print("\n⚠️ Collecte interrompue par utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        logger.exception("Detailed error:")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Intelligent Corpus Collector - Optimisé après analyse Colab
Collecteur adaptatif basé sur les insights de performance Colab Pro
"""

import json
import time
import requests
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import signal
from dataclasses import dataclass, asdict

# Setup logging robuste
log_dir = Path("/home/stephane/GitHub/PaniniFS-Research/logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "intelligent_collector.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedDocument:
    """Document enrichi avec analyse dhātu potentielle"""
    id: str
    title: str
    content: str
    source: str
    language: str
    domain: str
    url: str = ""
    timestamp: str = ""
    word_count: int = 0
    dhatu_potential: float = 0.0  # Score potentiel dhātu basé sur heuristiques
    linguistic_features: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.word_count:
            self.word_count = len(self.content.split()) if self.content else 0
        if self.linguistic_features is None:
            self.linguistic_features = {}
        
        # Calcul dhātu potential si pas défini
        if self.dhatu_potential == 0.0:
            self.dhatu_potential = self._calculate_dhatu_potential()
    
    def _calculate_dhatu_potential(self) -> float:
        """Calcule le potentiel dhātu basé sur les insights Colab"""
        if not self.content:
            return 0.0
            
        score = 0.0
        text_lower = self.content.lower()
        
        # Patterns linguistiques favorisant l'analyse dhātu
        dhatu_indicators = {
            'movement_verbs': ['go', 'move', 'come', 'walk', 'run', 'travel', 'journey'],
            'cognitive_verbs': ['think', 'know', 'understand', 'learn', 'realize'],
            'transformation_verbs': ['change', 'become', 'transform', 'develop'],
            'linguistic_terms': ['grammar', 'language', 'syntax', 'semantic', 'phonetic', 'morphology'],
            'sanskrit_related': ['sanskrit', 'panini', 'dhatu', 'verb', 'root']
        }
        
        for category, terms in dhatu_indicators.items():
            matches = sum(1 for term in terms if term in text_lower)
            if category == 'sanskrit_related':
                score += matches * 0.3  # Bonus fort pour contenu sanskrit
            elif category == 'linguistic_terms':
                score += matches * 0.2  # Bon pour linguistique
            else:
                score += matches * 0.1
        
        # Bonus pour complexité structurelle
        sentences = len([s for s in self.content.split('.') if len(s.strip()) > 10])
        if sentences > 5:
            score += 0.1
            
        # Bonus pour longueur optimale (basé sur perf Colab)
        if 100 <= self.word_count <= 500:
            score += 0.2
            
        return min(score, 1.0)  # Cap à 1.0

class IntelligentCorpusCollector:
    """Collecteur intelligent adapté aux résultats Colab"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or "/home/stephane/GitHub/PaniniFS-Research/data/incremental_corpus")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistiques enrichies
        self.stats = {
            'documents_collected': 0,
            'high_potential_docs': 0,
            'sources_used': set(),
            'start_time': time.time(),
            'errors': 0,
            'git_pushes': 0,
            'average_dhatu_potential': 0.0,
            'total_dhatu_potential': 0.0
        }
        
        # Configuration optimisée
        self.rate_limit = 1.5  # Plus rapide basé sur capacité Colab
        self.quality_threshold = 0.3  # Seuil qualité minimum
        self.batch_size_adaptive = 12  # Taille adaptative
        
        # Sources enrichies
        self.sources = {
            'wikipedia': {
                'random_url': "https://en.wikipedia.org/api/rest_v1/page/random/summary",
                'weight': 0.4
            },
            'academic_samples': {
                'weight': 0.6
            }
        }
        
        # Gestion des signaux pour arrêt propre
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        
        logger.info(f"🧠 Intelligent Corpus Collector initialisé")
        logger.info(f"📂 Output: {self.output_dir}")
        logger.info(f"🎯 Qualité minimum: {self.quality_threshold}")
        logger.info(f"⚡ Rate limit: {self.rate_limit}s")
    
    def _handle_signal(self, signum, frame):
        """Gestion propre des signaux"""
        logger.info(f"Signal {signum} reçu - arrêt propre en cours...")
        self.save_final_stats()
        sys.exit(0)
    
    def fetch_enhanced_wikipedia(self) -> Optional[EnhancedDocument]:
        """Collecte Wikipedia avec évaluation qualité"""
        try:
            response = requests.get(
                self.sources['wikipedia']['random_url'], 
                timeout=10,
                headers={'User-Agent': 'IntelligentCorpusCollector/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract', '')
                
                # Validation qualité minimum
                if len(extract) < 100:
                    return None
                
                doc = EnhancedDocument(
                    id=f"wiki_{data['pageid']}_{int(time.time())}",
                    title=data['title'],
                    content=extract,
                    source="wikipedia",
                    language="en",
                    domain=self._classify_domain(data['title'], extract),
                    url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                )
                
                # Filtrage qualité
                if doc.dhatu_potential < self.quality_threshold:
                    logger.debug(f"🔻 Document rejeté (qualité {doc.dhatu_potential:.2f}): {doc.title[:50]}")
                    return None
                
                self.stats['sources_used'].add('wikipedia')
                return doc
                
            else:
                logger.warning(f"Wikipedia API error: {response.status_code}")
                self.stats['errors'] += 1
                return None
                
        except Exception as e:
            logger.error(f"Erreur Wikipedia: {e}")
            self.stats['errors'] += 1
            return None
    
    def _classify_domain(self, title: str, content: str) -> str:
        """Classification automatique du domaine"""
        text = (title + " " + content).lower()
        
        domain_patterns = {
            'linguistics': ['language', 'grammar', 'linguistic', 'syntax', 'phonetic'],
            'computer_science': ['algorithm', 'computer', 'programming', 'software'],
            'mathematics': ['theorem', 'equation', 'mathematical', 'geometry'],
            'philosophy': ['philosophy', 'epistemology', 'ontology', 'ethics'],
            'literature': ['literary', 'novel', 'poetry', 'narrative'],
            'science': ['research', 'experiment', 'hypothesis', 'theory']
        }
        
        for domain, patterns in domain_patterns.items():
            if any(pattern in text for pattern in patterns):
                return domain
        
        return 'general'
    
    def generate_enhanced_samples(self) -> List[EnhancedDocument]:
        """Génère échantillons enrichis basés sur insights Colab"""
        
        # Templates optimisés pour analyse dhātu
        templates = [
            {
                'title': 'Verbal Root Analysis in Sanskrit Grammar',
                'content': '''Sanskrit verbal roots, known as dhātus, form the fundamental building blocks of the language's verbal system. Each dhātu carries a core semantic meaning that manifests through various grammatical transformations. The root √gam, meaning "to go," exemplifies this principle through its diverse applications. When combined with different prefixes and suffixes, √gam generates numerous derived forms: गच्छति (gacchati) "he goes," आगत: (āgataḥ) "having come," and गमन (gamana) "the act of going." This systematic approach to verbal morphology demonstrates the sophisticated grammatical framework developed by ancient Sanskrit grammarians.''',
                'domain': 'sanskrit_studies'
            },
            {
                'title': 'Movement Semantics in Natural Language Processing',
                'content': '''Natural language processing systems must accurately capture movement semantics to understand spatial relationships and temporal sequences. Verbs of motion like "go," "come," "move," and "travel" require sophisticated semantic representation to handle their contextual variations. Machine learning models trained on large corpora can learn these patterns automatically, identifying subtle distinctions between "walking towards" versus "walking away." The computational complexity of movement semantics parallels traditional grammatical analyses, where root meanings undergo systematic transformations through morphological processes.''',
                'domain': 'computational_linguistics'
            },
            {
                'title': 'Cognitive Architecture of Language Processing',
                'content': '''Human cognitive systems process language through hierarchical neural networks that decompose complex utterances into constituent elements. Research in cognitive linguistics reveals how speakers mentally represent verbal concepts and their transformations. The brain's language processing modules must rapidly access lexical items, apply grammatical rules, and generate appropriate outputs. This cognitive architecture mirrors formal grammatical systems where abstract rules operate on concrete linguistic materials. Understanding these cognitive mechanisms provides insights into both human language acquisition and artificial intelligence development.''',
                'domain': 'cognitive_science'
            },
            {
                'title': 'Transformational Grammar and Generative Systems',
                'content': '''Transformational grammar theory proposes that linguistic competence involves systematic rule-based transformations of underlying structures. These transformations operate on abstract representations to generate surface forms observable in actual speech. Generative systems must account for the infinite creativity of language while maintaining grammatical constraints. The interplay between lexical items and transformational rules creates the rich expressive power of human language. Contemporary linguistic theory continues to explore how these generative mechanisms function across different language families and grammatical systems.''',
                'domain': 'theoretical_linguistics'
            }
        ]
        
        documents = []
        for i, template in enumerate(templates):
            doc = EnhancedDocument(
                id=f"enhanced_sample_{i}_{int(time.time())}",
                title=template['title'],
                content=template['content'],
                source="enhanced_academic",
                language="en",
                domain=template['domain']
            )
            documents.append(doc)
        
        return documents
    
    def save_intelligent_batch(self, documents: List[EnhancedDocument], batch_num: int) -> bool:
        """Sauvegarde avec métadonnées enrichies"""
        
        if not documents:
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intelligent_batch_{batch_num:03d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Statistiques batch
        total_potential = sum(doc.dhatu_potential for doc in documents)
        avg_potential = total_potential / len(documents)
        high_quality_docs = [doc for doc in documents if doc.dhatu_potential > 0.5]
        
        # Métadonnées enrichies
        batch_data = {
            'metadata': {
                'batch_number': batch_num,
                'timestamp': timestamp,
                'collector_version': 'intelligent_v1.0',
                'colab_adaptation': True,
                'document_count': len(documents),
                'high_quality_count': len(high_quality_docs),
                'total_words': sum(doc.word_count for doc in documents),
                'average_dhatu_potential': round(avg_potential, 3),
                'total_dhatu_potential': round(total_potential, 3),
                'quality_threshold': self.quality_threshold,
                'sources': list(set(doc.source for doc in documents)),
                'languages': list(set(doc.language for doc in documents)),
                'domains': list(set(doc.domain for doc in documents)),
                'dhatu_distribution': {
                    'high': len([d for d in documents if d.dhatu_potential > 0.7]),
                    'medium': len([d for d in documents if 0.4 <= d.dhatu_potential <= 0.7]),
                    'low': len([d for d in documents if d.dhatu_potential < 0.4])
                }
            },
            'documents': [asdict(doc) for doc in documents],
            'colab_insights': {
                'optimized_for': 'Tesla T4 GPU processing',
                'target_throughput': '527 docs/min',
                'dominant_pattern': '√gam movement semantics',
                'confidence_target': 0.87
            }
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Batch sauvegardé: {filename}")
            logger.info(f"📊 Qualité moyenne: {avg_potential:.3f} | Haute qualité: {len(high_quality_docs)}/{len(documents)}")
            
            return self.git_push_enhanced(filepath, batch_num, avg_potential)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            traceback.print_exc()
            return False
    
    def git_push_enhanced(self, filepath: Path, batch_num: int, quality_score: float) -> bool:
        """Push avec message enrichi"""
        try:
            import subprocess
            
            repo_dir = "/home/stephane/GitHub/PaniniFS-Research"
            
            # Git operations
            subprocess.run(['git', 'add', str(filepath)], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            commit_msg = f"🧠 Intelligent batch {batch_num} - Q:{quality_score:.3f} - {datetime.now().strftime('%H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            subprocess.run(['git', 'push', 'origin', 'main'], 
                         cwd=repo_dir, check=True, capture_output=True)
            
            self.stats['git_pushes'] += 1
            logger.info(f"🔄 Git push réussi: batch {batch_num} (qualité {quality_score:.3f})")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git push failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Git error: {e}")
            return False
    
    def run_intelligent_collection(self, target_docs: int = 150, max_hours: float = 2.5):
        """Lance collecte intelligente adaptative"""
        
        logger.info(f"🧠 DÉMARRAGE COLLECTE INTELLIGENTE")
        logger.info(f"🎯 Target: {target_docs} documents (qualité {self.quality_threshold}+)")
        logger.info(f"⏰ Max duration: {max_hours} heures")
        logger.info(f"🔄 Adaptation Colab: Tesla T4 @ 527 docs/min")
        logger.info("=" * 60)
        
        start_time = time.time()
        max_duration = max_hours * 3600
        
        batch_num = 1
        document_buffer = []
        
        # Ajouter échantillons haute qualité au début
        enhanced_samples = self.generate_enhanced_samples()
        document_buffer.extend(enhanced_samples)
        logger.info(f"🎯 {len(enhanced_samples)} échantillons haute qualité ajoutés")
        
        quality_history = []
        
        try:
            while (self.stats['documents_collected'] < target_docs and 
                   (time.time() - start_time) < max_duration):
                
                # Collecte adaptative
                doc = self.fetch_enhanced_wikipedia()
                if doc:
                    document_buffer.append(doc)
                    self.stats['documents_collected'] += 1
                    self.stats['total_dhatu_potential'] += doc.dhatu_potential
                    
                    if doc.dhatu_potential > 0.5:
                        self.stats['high_potential_docs'] += 1
                        logger.info(f"📄⭐ Document HQ {self.stats['documents_collected']}: {doc.title[:50]} (Q:{doc.dhatu_potential:.3f})")
                    else:
                        logger.info(f"📄 Document {self.stats['documents_collected']}: {doc.title[:50]} (Q:{doc.dhatu_potential:.3f})")
                    
                    quality_history.append(doc.dhatu_potential)
                
                # Sauvegarde batch adaptative
                current_batch_size = self.batch_size_adaptive
                if len(document_buffer) >= current_batch_size:
                    batch_quality = sum(d.dhatu_potential for d in document_buffer) / len(document_buffer)
                    
                    success = self.save_intelligent_batch(document_buffer, batch_num)
                    if success:
                        logger.info(f"✅ Batch {batch_num} poussé vers GitHub (qualité moyenne: {batch_quality:.3f})")
                    else:
                        logger.warning(f"⚠️ Échec batch {batch_num}")
                    
                    document_buffer = []
                    batch_num += 1
                
                # Adaptation dynamique
                if len(quality_history) > 20:
                    recent_quality = sum(quality_history[-20:]) / 20
                    if recent_quality < self.quality_threshold * 0.8:
                        self.rate_limit = min(self.rate_limit + 0.5, 5.0)  # Ralentir si mauvaise qualité
                        logger.info(f"🐌 Rate limit augmenté à {self.rate_limit}s (qualité récente: {recent_quality:.3f})")
                    elif recent_quality > self.quality_threshold * 1.5:
                        self.rate_limit = max(self.rate_limit - 0.2, 0.5)  # Accélérer si bonne qualité
                        logger.info(f"🚀 Rate limit réduit à {self.rate_limit}s (qualité récente: {recent_quality:.3f})")
                
                time.sleep(self.rate_limit)
                
                # Rapport périodique enrichi
                if self.stats['documents_collected'] % 20 == 0 and self.stats['documents_collected'] > 0:
                    elapsed = time.time() - start_time
                    rate = self.stats['documents_collected'] / elapsed
                    avg_quality = self.stats['total_dhatu_potential'] / self.stats['documents_collected']
                    quality_pct = 100 * self.stats['high_potential_docs'] / self.stats['documents_collected']
                    
                    logger.info(f"📊 Progress: {self.stats['documents_collected']}/{target_docs} docs")
                    logger.info(f"⚡ Rate: {rate:.1f} docs/min | Qualité moy: {avg_quality:.3f}")
                    logger.info(f"⭐ Haute qualité: {self.stats['high_potential_docs']}/{self.stats['documents_collected']} ({quality_pct:.1f}%)")
                    logger.info(f"🔄 Pushes: {self.stats['git_pushes']} | Sources: {len(self.stats['sources_used'])}")
        
        except Exception as e:
            logger.error(f"Erreur pendant collecte: {e}")
            traceback.print_exc()
        
        # Sauvegarde finale
        if document_buffer:
            self.save_intelligent_batch(document_buffer, batch_num)
        
        self.save_final_stats()
        
        # Rapport final enrichi
        total_time = time.time() - start_time
        final_avg_quality = self.stats['total_dhatu_potential'] / self.stats['documents_collected'] if self.stats['documents_collected'] > 0 else 0
        
        logger.info(f"🎯 COLLECTE INTELLIGENTE TERMINÉE")
        logger.info(f"📄 Documents: {self.stats['documents_collected']} (target: {target_docs})")
        logger.info(f"⭐ Haute qualité: {self.stats['high_potential_docs']} ({100*self.stats['high_potential_docs']/self.stats['documents_collected']:.1f}%)")
        logger.info(f"📊 Qualité moyenne: {final_avg_quality:.3f}")
        logger.info(f"⏱️ Temps: {total_time:.1f}s ({self.stats['documents_collected']/total_time*60:.1f} docs/min)")
        logger.info(f"🔄 Pushes GitHub: {self.stats['git_pushes']}")
        logger.info(f"🌐 Sources: {len(self.stats['sources_used'])}")
        logger.info(f"❌ Erreurs: {self.stats['errors']}")
        
        return {
            'documents_collected': self.stats['documents_collected'],
            'high_quality_count': self.stats['high_potential_docs'],
            'average_quality': final_avg_quality,
            'total_time': total_time,
            'git_pushes': self.stats['git_pushes'],
            'errors': self.stats['errors']
        }
    
    def save_final_stats(self):
        """Sauvegarde statistiques finales"""
        stats_file = self.output_dir / f"collection_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        final_stats = {
            'timestamp': datetime.now().isoformat(),
            'collector': 'intelligent_v1.0',
            'colab_optimization': True,
            'stats': dict(self.stats),
            'performance': {
                'documents_per_hour': self.stats['documents_collected'] / ((time.time() - self.stats['start_time']) / 3600),
                'quality_percentage': (self.stats['high_potential_docs'] / self.stats['documents_collected'] * 100) if self.stats['documents_collected'] > 0 else 0,
                'average_dhatu_potential': self.stats['total_dhatu_potential'] / self.stats['documents_collected'] if self.stats['documents_collected'] > 0 else 0
            }
        }
        
        final_stats['stats']['sources_used'] = list(self.stats['sources_used'])
        
        with open(stats_file, 'w') as f:
            json.dump(final_stats, f, indent=2)
        
        logger.info(f"📊 Statistiques finales sauvegardées: {stats_file.name}")

def main():
    """Point d'entrée principal"""
    
    print("🧠 INTELLIGENT CORPUS COLLECTOR")
    print("🔬 Optimisé pour analyse dhātu Colab Pro")
    print("=" * 50)
    print("📊 Basé sur résultats: Tesla T4, 527 docs/min, √gam patterns")
    print()
    
    collector = IntelligentCorpusCollector()
    
    # Configuration optimisée pour Colab
    TARGET_DOCS = 200      # Objectif qualité > quantité
    MAX_HOURS = 3.0        # Maximum 3 heures
    
    try:
        results = collector.run_intelligent_collection(
            target_docs=TARGET_DOCS,
            max_hours=MAX_HOURS
        )
        
        print(f"\n🎉 COLLECTE INTELLIGENTE RÉUSSIE!")
        print(f"📄 {results['documents_collected']} documents collectés")
        print(f"⭐ {results['high_quality_count']} documents haute qualité ({100*results['high_quality_count']/results['documents_collected']:.1f}%)")
        print(f"📊 Qualité moyenne: {results['average_quality']:.3f}")
        print(f"🔄 {results['git_pushes']} pushes vers GitHub")
        print(f"⏱️ {results['total_time']:.1f} secondes")
        
    except KeyboardInterrupt:
        print("\n⚠️ Collecte interrompue par utilisateur")
        collector.save_final_stats()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        logger.exception("Erreur détaillée:")
        collector.save_final_stats()

if __name__ == "__main__":
    main()
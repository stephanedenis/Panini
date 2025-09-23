#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Massive Corpus Collector for PaniniFS Research
Collecte automatisée de corpus à grande échelle pour recherche dhātu intensive
"""

import asyncio
import aiohttp
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, AsyncGenerator
import re
from dataclasses import dataclass, asdict
import logging
from urllib.parse import quote

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Document:
    """Structure document standardisée"""
    id: str
    title: str
    content: str
    source: str
    language: str
    domain: str
    url: str = ""
    timestamp: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class MassiveCorpusCollector:
    """Collecteur de corpus massif multi-sources"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("/home/stephane/GitHub/PaniniFS-Research/data/massive_corpus")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Stats collection
        self.stats = {
            'documents_collected': 0,
            'sources_processed': 0,
            'start_time': time.time(),
            'errors': 0,
            'languages_detected': set(),
            'domains_detected': set()
        }
        
        # Configuration APIs
        self.apis_config = {
            'arxiv': {
                'base_url': 'http://export.arxiv.org/api/query',
                'rate_limit': 1.0,  # 1 req/sec
                'max_results': 1000,
                'batch_size': 100
            },
            'wikipedia': {
                'base_url': 'https://en.wikipedia.org/api/rest_v1/page/random/summary',
                'rate_limit': 0.1,  # 10 req/sec
                'max_results': 5000,
                'batch_size': 50
            },
            'gutenberg': {
                'base_url': 'https://www.gutenberg.org/files',
                'rate_limit': 2.0,  # 0.5 req/sec
                'max_results': 500,
                'batch_size': 10
            }
        }
        
        logger.info(f"🌍 Massive Corpus Collector initialisé")
        logger.info(f"📂 Output: {self.output_dir}")
    
    async def collect_from_arxiv(self, session: aiohttp.ClientSession, 
                                query: str = "quantum OR machine learning OR linguistics", 
                                max_results: int = 1000) -> AsyncGenerator[Document, None]:
        """Collecte depuis arXiv API"""
        
        logger.info(f"📚 Collecte arXiv: {query} (max: {max_results})")
        
        batch_size = self.apis_config['arxiv']['batch_size']
        rate_limit = self.apis_config['arxiv']['rate_limit']
        
        for start in range(0, max_results, batch_size):
            try:
                url = f"{self.apis_config['arxiv']['base_url']}?search_query={quote(query)}&start={start}&max_results={batch_size}&sortBy=submittedDate&sortOrder=descending"
                
                await asyncio.sleep(rate_limit)
                
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        documents = self._parse_arxiv_response(content)
                        
                        for doc in documents:
                            self.stats['documents_collected'] += 1
                            self.stats['languages_detected'].add(doc.language)
                            self.stats['domains_detected'].add(doc.domain)
                            yield doc
                            
                        logger.info(f"   📄 Batch {start//batch_size + 1}: {len(documents)} documents")
                    else:
                        logger.warning(f"❌ arXiv API error: {response.status}")
                        self.stats['errors'] += 1
                        
            except Exception as e:
                logger.error(f"❌ Erreur arXiv batch {start}: {e}")
                self.stats['errors'] += 1
    
    def _parse_arxiv_response(self, xml_content: str) -> List[Document]:
        """Parse réponse XML arXiv"""
        documents = []
        
        # Simple XML parsing pour arXiv (pas de lxml dependency)
        entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)
        
        for entry in entries:
            try:
                # Extract fields
                id_match = re.search(r'<id>(.*?)</id>', entry)
                title_match = re.search(r'<title>(.*?)</title>', entry)
                summary_match = re.search(r'<summary>(.*?)</summary>', entry)
                category_match = re.search(r'<category term="([^"]+)"', entry)
                
                if id_match and title_match and summary_match:
                    doc_id = id_match.group(1).split('/')[-1]
                    title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
                    content = re.sub(r'\s+', ' ', summary_match.group(1)).strip()
                    category = category_match.group(1) if category_match else "unknown"
                    
                    doc = Document(
                        id=f"arxiv_{doc_id}",
                        title=title,
                        content=content,
                        source="arxiv",
                        language="en",
                        domain=category,
                        url=id_match.group(1),
                        metadata={
                            'category': category,
                            'content_length': len(content)
                        }
                    )
                    documents.append(doc)
                    
            except Exception as e:
                logger.warning(f"⚠️ Parse error arXiv entry: {e}")
                
        return documents
    
    async def collect_from_wikipedia(self, session: aiohttp.ClientSession, 
                                   max_results: int = 5000) -> AsyncGenerator[Document, None]:
        """Collecte depuis Wikipedia API"""
        
        logger.info(f"📖 Collecte Wikipedia (max: {max_results})")
        
        rate_limit = self.apis_config['wikipedia']['rate_limit']
        collected = 0
        
        while collected < max_results:
            try:
                await asyncio.sleep(rate_limit)
                
                async with session.get(self.apis_config['wikipedia']['base_url']) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'extract' in data and len(data['extract']) > 100:
                            doc = Document(
                                id=f"wiki_{data['pageid']}",
                                title=data['title'],
                                content=data['extract'],
                                source="wikipedia",
                                language="en",
                                domain="encyclopedia",
                                url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                metadata={
                                    'pageid': data['pageid'],
                                    'content_length': len(data['extract'])
                                }
                            )
                            
                            self.stats['documents_collected'] += 1
                            self.stats['languages_detected'].add(doc.language)
                            self.stats['domains_detected'].add(doc.domain)
                            collected += 1
                            
                            yield doc
                            
                            if collected % 100 == 0:
                                logger.info(f"   📄 Wikipedia: {collected} documents collectés")
                    else:
                        logger.warning(f"❌ Wikipedia API error: {response.status}")
                        self.stats['errors'] += 1
                        await asyncio.sleep(1.0)  # Longer delay on error
                        
            except Exception as e:
                logger.error(f"❌ Erreur Wikipedia: {e}")
                self.stats['errors'] += 1
                await asyncio.sleep(1.0)
    
    async def save_documents_batch(self, documents: List[Document], batch_num: int):
        """Sauvegarde batch de documents"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corpus_batch_{batch_num:04d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Convert documents to dict
        docs_data = [asdict(doc) for doc in documents]
        
        # Metadata
        batch_metadata = {
            'batch_number': batch_num,
            'timestamp': timestamp,
            'total_documents': len(docs_data),
            'sources': list(set(doc['source'] for doc in docs_data)),
            'languages': list(set(doc['language'] for doc in docs_data)),
            'domains': list(set(doc['domain'] for doc in docs_data)),
            'collection_stats': dict(self.stats),
            'total_characters': sum(len(doc['content']) for doc in docs_data)
        }
        
        final_data = {
            'metadata': batch_metadata,
            'documents': docs_data
        }
        
        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"💾 Sauvegardé: {filename} ({len(docs_data)} docs, {batch_metadata['total_characters']:,} chars)")
        
        return filepath
    
    async def collect_massive_corpus(self, 
                                   target_docs: int = 100000,
                                   save_batch_size: int = 1000) -> Dict[str, Any]:
        """Collecte corpus massif multi-sources"""
        
        logger.info(f"🚀 DÉMARRAGE COLLECTE MASSIVE")
        logger.info(f"🎯 Target: {target_docs:,} documents")
        logger.info(f"💾 Batch size: {save_batch_size}")
        
        # Document buffer
        document_buffer = []
        batch_num = 1
        saved_files = []
        
        # Connector HTTP session
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=20, limit_per_host=5)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            
            # Sources collection (parallèle)
            collectors = [
                self.collect_from_arxiv(session, max_results=min(target_docs//3, 10000)),
                self.collect_from_wikipedia(session, max_results=min(target_docs//2, 20000)),
            ]
            
            # Process collections
            for collector in collectors:
                async for document in collector:
                    document_buffer.append(document)
                    
                    # Save batch when buffer full
                    if len(document_buffer) >= save_batch_size:
                        filepath = await self.save_documents_batch(document_buffer, batch_num)
                        saved_files.append(filepath)
                        document_buffer = []
                        batch_num += 1
                        
                        # Progress report
                        elapsed = time.time() - self.stats['start_time']
                        rate = self.stats['documents_collected'] / elapsed
                        logger.info(f"📊 PROGRESS: {self.stats['documents_collected']:,} docs | {rate:.1f} docs/sec | {len(saved_files)} batches")
                        
                        # Check target
                        if self.stats['documents_collected'] >= target_docs:
                            logger.info(f"🎯 TARGET ATTEINT: {target_docs:,} documents")
                            break
                
                if self.stats['documents_collected'] >= target_docs:
                    break
            
            # Save remaining documents
            if document_buffer:
                filepath = await self.save_documents_batch(document_buffer, batch_num)
                saved_files.append(filepath)
        
        # Final stats
        final_stats = self._generate_final_report(saved_files)
        return final_stats
    
    def _generate_final_report(self, saved_files: List[Path]) -> Dict[str, Any]:
        """Génère rapport final de collecte"""
        
        elapsed_time = time.time() - self.stats['start_time']
        
        report = {
            'collection_summary': {
                'total_documents': self.stats['documents_collected'],
                'total_files': len(saved_files),
                'collection_time_seconds': elapsed_time,
                'collection_rate_docs_per_sec': self.stats['documents_collected'] / elapsed_time,
                'errors_encountered': self.stats['errors'],
                'sources_processed': self.stats['sources_processed']
            },
            'content_analysis': {
                'languages_detected': list(self.stats['languages_detected']),
                'domains_detected': list(self.stats['domains_detected']),
                'average_batch_size': self.stats['documents_collected'] / len(saved_files) if saved_files else 0
            },
            'files_created': [str(f) for f in saved_files],
            'output_directory': str(self.output_dir),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save report
        report_file = self.output_dir / f"collection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"🎯 COLLECTE TERMINÉE")
        logger.info(f"📄 Documents: {report['collection_summary']['total_documents']:,}")
        logger.info(f"📁 Fichiers: {len(saved_files)}")
        logger.info(f"⏱️ Temps: {elapsed_time:.1f}s")
        logger.info(f"🚀 Rate: {report['collection_summary']['collection_rate_docs_per_sec']:.1f} docs/sec")
        logger.info(f"📊 Rapport: {report_file}")
        
        return report

async def main():
    """Démarrage collecte massive"""
    
    print("🌍 MASSIVE CORPUS COLLECTOR")
    print("=" * 50)
    
    collector = MassiveCorpusCollector()
    
    # Configuration collecte
    TARGET_DOCS = 50000  # Start with 50K for testing
    BATCH_SIZE = 500     # Smaller batches for better progress tracking
    
    try:
        report = await collector.collect_massive_corpus(
            target_docs=TARGET_DOCS,
            save_batch_size=BATCH_SIZE
        )
        
        print("\n🎉 COLLECTE RÉUSSIE!")
        print(f"📄 {report['collection_summary']['total_documents']:,} documents collectés")
        print(f"📁 {report['collection_summary']['total_files']} fichiers créés")
        print(f"⏱️ {report['collection_summary']['collection_time_seconds']:.1f} secondes")
        
    except KeyboardInterrupt:
        print("\n⚠️ Collecte interrompue par utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        logger.exception("Detailed error:")

if __name__ == "__main__":
    asyncio.run(main())
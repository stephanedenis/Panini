#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Multilingual Dhātu Cycle Analyzer
Modélisation bidirectionnelle Texte → Dhātu → Texte pour restitution parfaite
"""

import re
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class MultilingualDhatuMapping:
    """Mapping dhātu multilingue d'une œuvre"""
    work_key: str
    title: str
    author: str
    language_analyses: Dict[str, Dict]  # lang -> dhatu_scores
    cross_language_correlation: Dict[str, float]  # dhatu -> correlation_score
    text_to_dhatu_mapping: Dict[str, List[Tuple]]  # lang -> [(text_segment, dhatus)]
    dhatu_to_text_reconstruction: Dict[str, Dict]  # lang -> reconstructed_segments


class MultilingualDhatuAnalyzer:
    """Analyseur dhātu multilingue pour cycle texte → dhātu → texte"""
    
    def __init__(self):
        # Patterns dhātu étendus pour multi-langues
        self.multilingual_dhatu_patterns = {
            'RELATE': {
                'en': r'\b(with|to|from|between|among|relation|connect|link|related|together|against|through)\b',
                'fr': r'\b(avec|à|de|entre|parmi|relation|relier|lien|ensemble|contre|à_travers|par)\b',
                'de': r'\b(mit|zu|von|zwischen|unter|beziehung|verbinden|zusammen|gegen|durch)\b'
            },
            'MODAL': {
                'en': r'\b(can|could|may|might|must|should|would|will|shall|possible|necessary|able)\b',
                'fr': r'\b(peut|pourrait|pourra|doit|devrait|voudrait|sera|possible|nécessaire|capable)\b',
                'de': r'\b(kann|könnte|mag|möchte|muss|sollte|würde|wird|möglich|notwendig|fähig)\b'
            },
            'EXIST': {
                'en': r'\b(is|are|was|were|be|being|been|exist|there|have|has|had|being)\b',
                'fr': r'\b(est|sont|était|étaient|être|étant|été|exister|il_y_a|avoir|avait|ayant)\b',
                'de': r'\b(ist|sind|war|waren|sein|seiend|gewesen|existieren|gibt|haben|hatte|habend)\b'
            },
            'EVAL': {
                'en': r'\b(good|bad|better|worse|best|worst|great|terrible|wonderful|awful|excellent|poor)\b',
                'fr': r'\b(bon|mauvais|meilleur|pire|mieux|terrible|merveilleux|affreux|excellent|pauvre)\b',
                'de': r'\b(gut|schlecht|besser|schlechter|beste|schlechteste|großartig|schrecklich|wunderbar|schlimm)\b'
            },
            'COMM': {
                'en': r'\b(say|said|tell|told|speak|talk|communicate|express|word|voice|language|message)\b',
                'fr': r'\b(dire|dit|parler|parlé|communiquer|exprimer|mot|voix|langue|message|raconter)\b',
                'de': r'\b(sagen|gesagt|sprechen|gesprochen|kommunizieren|ausdrücken|wort|stimme|sprache|nachricht)\b'
            },
            'CAUSE': {
                'en': r'\b(because|since|therefore|thus|cause|reason|result|effect|so|hence|consequently)\b',
                'fr': r'\b(parce_que|depuis|donc|ainsi|cause|raison|résultat|effet|alors|par_conséquent)\b',
                'de': r'\b(weil|da|deshalb|daher|ursache|grund|ergebnis|wirkung|so|folglich|infolgedessen)\b'
            },
            'ITER': {
                'en': r'\b(again|repeat|continue|always|often|usually|every|each|once_more|repeatedly)\b',
                'fr': r'\b(encore|répéter|continuer|toujours|souvent|habituellement|chaque|une_fois_de_plus)\b',
                'de': r'\b(wieder|wiederholen|fortsetzen|immer|oft|gewöhnlich|jede|noch_einmal|wiederholt)\b'
            },
            'DECIDE': {
                'en': r'\b(decide|choose|select|determine|resolve|conclude|judge|decision|choice|judgment)\b',
                'fr': r'\b(décider|choisir|sélectionner|déterminer|résoudre|conclure|juger|décision|choix)\b',
                'de': r'\b(entscheiden|wählen|auswählen|bestimmen|lösen|schließen|urteilen|entscheidung|wahl)\b'
            },
            'FEEL': {
                'en': r'\b(feel|felt|emotion|happy|sad|love|hate|like|dislike|joy|sorrow|fear|anger)\b',
                'fr': r'\b(sentir|senti|émotion|heureux|triste|aimer|détester|joie|chagrin|peur|colère)\b',
                'de': r'\b(fühlen|gefühlt|emotion|glücklich|traurig|lieben|hassen|freude|kummer|angst|wut)\b'
            }
        }
        
        self.dhatu_names = list(self.multilingual_dhatu_patterns.keys())
        print("🔄 Analyseur Dhātu Multilingue initialisé")
        print(f"   🧬 {len(self.dhatu_names)} dhātu universaux")
        print(f"   🌍 3 langues: EN, FR, DE")
    
    def extract_text_segments(self, text: str, lang: str, segment_size: int = 1000) -> List[str]:
        """Extrait segments textuels pour analyse granulaire"""
        
        # Nettoyage préparatoire
        clean_text = self._clean_gutenberg_text(text)
        
        # Segmentation par taille ou par phrases
        segments = []
        words = clean_text.split()
        
        for i in range(0, len(words), segment_size):
            segment = ' '.join(words[i:i+segment_size])
            if len(segment.strip()) > 100:  # Éviter segments trop courts
                segments.append(segment.strip())
        
        return segments
    
    def analyze_dhatu_in_segment(self, segment: str, lang: str) -> Dict[str, float]:
        """Analyse dhātu dans un segment textuel"""
        
        segment_lower = segment.lower()
        total_words = len(segment.split())
        
        dhatu_scores = {}
        
        for dhatu_name in self.dhatu_names:
            if lang in self.multilingual_dhatu_patterns[dhatu_name]:
                pattern = self.multilingual_dhatu_patterns[dhatu_name][lang]
                matches = re.findall(pattern, segment_lower)
                score = len(matches) / max(total_words, 1)
                dhatu_scores[dhatu_name] = round(score, 6)
            else:
                dhatu_scores[dhatu_name] = 0.0
        
        # Normaliser
        total_score = sum(dhatu_scores.values())
        if total_score > 0:
            dhatu_scores = {k: round(v / total_score, 6) for k, v in dhatu_scores.items()}
        
        return dhatu_scores
    
    def create_text_to_dhatu_mapping(self, text: str, lang: str) -> List[Tuple[str, Dict[str, float]]]:
        """Crée mapping détaillé texte → dhātu"""
        
        segments = self.extract_text_segments(text, lang)
        text_to_dhatu = []
        
        print(f"   🔍 Analyse {len(segments)} segments ({lang.upper()})")
        
        for i, segment in enumerate(segments):
            dhatu_scores = self.analyze_dhatu_in_segment(segment, lang)
            
            # Garder seulement segments avec scores significatifs
            significant_dhatus = {k: v for k, v in dhatu_scores.items() if v > 0.01}
            
            if significant_dhatus:
                text_to_dhatu.append((segment[:200] + "..." if len(segment) > 200 else segment, dhatu_scores))
            
            if i % 50 == 0 and i > 0:
                print(f"      📊 {i}/{len(segments)} segments analysés")
        
        print(f"   ✅ {len(text_to_dhatu)} segments significatifs")
        return text_to_dhatu
    
    def reconstruct_text_from_dhatus(self, text_to_dhatu_mapping: List[Tuple], target_dhatu_profile: Dict[str, float], lang: str) -> List[str]:
        """Reconstruit texte à partir profil dhātu cible"""
        
        reconstructed_segments = []
        
        # Trier segments par similarité au profil cible
        def dhatu_similarity(segment_dhatus: Dict[str, float]) -> float:
            similarity = 0.0
            for dhatu, target_score in target_dhatu_profile.items():
                segment_score = segment_dhatus.get(dhatu, 0.0)
                similarity += 1 - abs(target_score - segment_score)
            return similarity / len(target_dhatu_profile)
        
        # Sélectionner segments les plus proches
        for segment_text, segment_dhatus in text_to_dhatu_mapping:
            similarity = dhatu_similarity(segment_dhatus)
            if similarity > 0.7:  # Seuil similarité élevé
                reconstructed_segments.append((segment_text, similarity))
        
        # Trier par similarité décroissante
        reconstructed_segments.sort(key=lambda x: x[1], reverse=True)
        
        return [seg[0] for seg in reconstructed_segments[:10]]  # Top 10
    
    def analyze_multilingual_work(self, work_dir: Path, work_key: str, metadata: Dict) -> MultilingualDhatuMapping:
        """Analyse complète multilingue d'une œuvre"""
        
        work_info = metadata['works'][work_key]
        print(f"\n🔄 ANALYSE MULTILINGUE: {work_info['title']}")
        print("=" * 60)
        
        language_analyses = {}
        text_to_dhatu_mappings = {}
        
        # Analyser chaque langue
        for lang, version_info in work_info['versions'].items():
            if not version_info.get('download_success', False):
                continue
                
            print(f"\n📖 Langue: {lang.upper()}")
            
            # Lire fichier
            file_path = Path(version_info['file_path'])
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Créer mapping texte → dhātu
            text_to_dhatu = self.create_text_to_dhatu_mapping(content, lang)
            text_to_dhatu_mappings[lang] = text_to_dhatu
            
            # Calculer scores globaux dhātu
            all_dhatu_scores = defaultdict(list)
            for _, segment_dhatus in text_to_dhatu:
                for dhatu, score in segment_dhatus.items():
                    all_dhatu_scores[dhatu].append(score)
            
            # Moyennes dhātu pour cette langue
            lang_dhatu_profile = {}
            for dhatu, scores in all_dhatu_scores.items():
                lang_dhatu_profile[dhatu] = round(np.mean(scores) if scores else 0.0, 6)
            
            language_analyses[lang] = {
                'dhatu_profile': lang_dhatu_profile,
                'total_segments': len(text_to_dhatu),
                'content_length': len(content)
            }
            
            # Afficher profil dhātu
            sorted_dhatus = sorted(lang_dhatu_profile.items(), key=lambda x: x[1], reverse=True)
            print(f"   🧬 Profil dhātu:")
            for dhatu, score in sorted_dhatus[:5]:
                percentage = score * 100
                print(f"      {dhatu:8}: {percentage:5.2f}%")
        
        # Calcul corrélations inter-langues
        cross_correlations = self._calculate_cross_language_correlations(language_analyses)
        
        # Test reconstruction dhātu → texte
        dhatu_reconstructions = {}
        for lang in language_analyses.keys():
            if lang in text_to_dhatu_mappings:
                profile = language_analyses[lang]['dhatu_profile']
                reconstructed = self.reconstruct_text_from_dhatus(
                    text_to_dhatu_mappings[lang], profile, lang
                )
                dhatu_reconstructions[lang] = reconstructed
        
        return MultilingualDhatuMapping(
            work_key=work_key,
            title=work_info['title'],
            author=work_info['author'],
            language_analyses=language_analyses,
            cross_language_correlation=cross_correlations,
            text_to_dhatu_mapping=text_to_dhatu_mappings,
            dhatu_to_text_reconstruction=dhatu_reconstructions
        )
    
    def _calculate_cross_language_correlations(self, language_analyses: Dict) -> Dict[str, float]:
        """Calcule corrélations dhātu entre langues"""
        
        correlations = {}
        
        # Pour chaque dhātu, calculer corrélation entre langues
        for dhatu in self.dhatu_names:
            lang_scores = []
            for lang_data in language_analyses.values():
                lang_scores.append(lang_data['dhatu_profile'].get(dhatu, 0.0))
            
            # Corrélation = 1 - variance normalisée
            if len(lang_scores) > 1:
                variance = np.var(lang_scores)
                correlation = max(0, 1 - (variance * 10))  # Facteur échelle
                correlations[dhatu] = round(correlation, 4)
            else:
                correlations[dhatu] = 1.0
        
        return correlations
    
    def _clean_gutenberg_text(self, text: str) -> str:
        """Nettoyage spécialisé texte Gutenberg"""
        
        # Supprimer métadonnées Gutenberg
        patterns_to_remove = [
            r'\*\*\* START OF.*?\*\*\*',
            r'\*\*\* END OF.*?\*\*\*',
            r'Project Gutenberg.*?\n',
            r'Title:.*?\n',
            r'Author:.*?\n'
        ]
        
        cleaned = text
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        # Nettoyage supplémentaire
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', cleaned)
        
        return cleaned.strip()
    
    def process_multilingual_corpus(self, corpus_dir: str = "data/gutenberg_multilingual_verified") -> Dict[str, MultilingualDhatuMapping]:
        """Traite tout le corpus multilingue"""
        
        corpus_path = Path(corpus_dir)
        metadata_file = corpus_path / 'multilingual_verified_metadata.json'
        
        if not metadata_file.exists():
            raise FileNotFoundError(f"Métadonnées manquantes: {metadata_file}")
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print("🔄 PIPELINE CYCLE TEXTE → DHĀTU → TEXTE")
        print("=" * 60)
        
        results = {}
        
        for work_key in metadata['works']:
            try:
                mapping = self.analyze_multilingual_work(corpus_path, work_key, metadata)
                results[work_key] = mapping
            except Exception as e:
                print(f"❌ Erreur {work_key}: {e}")
        
        # Sauvegarder résultats complets
        output_file = corpus_path / 'multilingual_dhatu_cycle_results.json'
        self._save_results(results, output_file)
        
        print(f"\n📊 RÉSULTATS PIPELINE CYCLE:")
        print(f"   📚 Œuvres analysées: {len(results)}")
        print(f"   💾 Résultats: {output_file}")
        
        return results
    
    def _save_results(self, results: Dict[str, MultilingualDhatuMapping], output_file: Path):
        """Sauvegarde résultats avec sérialisation"""
        
        serializable_results = {}
        
        for work_key, mapping in results.items():
            serializable_results[work_key] = {
                'title': mapping.title,
                'author': mapping.author,
                'language_analyses': mapping.language_analyses,
                'cross_language_correlation': mapping.cross_language_correlation,
                'dhatu_to_text_reconstruction': mapping.dhatu_to_text_reconstruction,
                'text_to_dhatu_mapping_summary': {
                    lang: len(text_dhatu_list) 
                    for lang, text_dhatu_list in mapping.text_to_dhatu_mapping.items()
                }
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)


def main():
    """Test pipeline cycle multilingue"""
    
    print("🔄 TEST PIPELINE CYCLE TEXTE → DHĀTU → TEXTE")
    print("=" * 60)
    
    analyzer = MultilingualDhatuAnalyzer()
    
    # Traiter corpus multilingue
    results = analyzer.process_multilingual_corpus()
    
    # Afficher résumé validation
    print(f"\n📊 VALIDATION CYCLE MULTILINGUE:")
    
    for work_key, mapping in results.items():
        print(f"\n📖 {mapping.title}:")
        print(f"   🌍 Langues: {', '.join(mapping.language_analyses.keys()).upper()}")
        
        # Corrélations inter-langues
        top_correlations = sorted(mapping.cross_language_correlation.items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
        print(f"   🔗 Top corrélations: {', '.join([f'{d}({c:.2f})' for d, c in top_correlations])}")
        
        # Reconstruction
        for lang in mapping.dhatu_to_text_reconstruction:
            reconstructed_count = len(mapping.dhatu_to_text_reconstruction[lang])
            print(f"   🔄 Reconstruction {lang.upper()}: {reconstructed_count} segments")
    
    print(f"\n✅ PIPELINE CYCLE TERMINÉ")
    return results


if __name__ == "__main__":
    main()
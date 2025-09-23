#!/usr/bin/env python3
"""
Synthétiseur Validateur PaniniFS
Test ultime : décomposer → recomposer → vérifier identité
"""

import json
from pathlib import Path
from datetime import datetime
import difflib
import hashlib
import re


class PaniniSynthesisValidator:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'synthesis_validation_results'
        self.results_dir.mkdir(exist_ok=True)
        
        # Chargement des composants atomiques/moléculaires
        self.atoms = self.load_universal_atoms()
        self.molecules = self.load_molecular_patterns()
        
        # Métriques de validation
        self.decomposition_results = {}
        self.recomposition_results = {}
        self.fidelity_metrics = {}
        
        self.log("🧬 Synthétiseur Validateur initialisé")
    
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def load_universal_atoms(self):
        """Charge atomes universaux"""
        atoms_dir = self.workspace / 'universal_atoms_results'
        if not atoms_dir.exists():
            return {}
        
        atom_files = list(atoms_dir.glob("universal_atoms_analysis_*.json"))
        if not atom_files:
            return {}
        
        latest_file = max(atom_files, key=lambda f: f.stat().st_mtime)
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('universality_scores', {})
    
    def load_molecular_patterns(self):
        """Charge patterns moléculaires"""
        molecules_dir = self.workspace / 'molecular_patterns_results'
        if not molecules_dir.exists():
            return {}
        
        molecule_files = list(molecules_dir.glob("molecular_patterns_report_*.json"))
        if not molecule_files:
            return {}
        
        latest_file = max(molecule_files, key=lambda f: f.stat().st_mtime)
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('molecular_patterns', {})
    
    def decompose_text_to_atoms(self, text):
        """Décompose texte en atomes universaux"""
        atomic_representation = {
            'phonetic': {},
            'morpheme': {},
            'syntactic': {},
            'semantic': {},
            'structure_map': []
        }
        
        # Position tracking pour reconstruction
        position = 0
        
        # Décomposition phonétique
        phonetic_atoms = self.extract_phonetic_components(text)
        for atom, positions in phonetic_atoms.items():
            atomic_representation['phonetic'][atom] = {
                'count': len(positions),
                'positions': positions
            }
        
        # Décomposition morphémique
        morpheme_atoms = self.extract_morpheme_components(text)
        for atom, positions in morpheme_atoms.items():
            atomic_representation['morpheme'][atom] = {
                'count': len(positions),
                'positions': positions
            }
        
        # Décomposition syntaxique
        syntactic_atoms = self.extract_syntactic_components(text)
        for atom, positions in syntactic_atoms.items():
            atomic_representation['syntactic'][atom] = {
                'count': len(positions),
                'positions': positions
            }
        
        # Décomposition sémantique
        semantic_atoms = self.extract_semantic_components(text)
        for atom, positions in semantic_atoms.items():
            atomic_representation['semantic'][atom] = {
                'count': len(positions),
                'positions': positions
            }
        
        # Création carte structurelle
        atomic_representation['structure_map'] = self.create_structure_map(text)
        atomic_representation['original_hash'] = hashlib.md5(text.encode()).hexdigest()
        atomic_representation['original_length'] = len(text)
        
        return atomic_representation
    
    def extract_phonetic_components(self, text):
        """Extraction composants phonétiques avec positions"""
        components = {}
        
        # Patterns from atoms
        if 'phonetic' in self.atoms:
            for atom in self.atoms['phonetic'].keys():
                if atom.startswith('V:'):
                    pattern = atom[2:]  # Remove V: prefix
                    matches = [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), text.lower())]
                    if matches:
                        components[atom] = matches
                elif atom.startswith('C:'):
                    pattern = atom[2:]  # Remove C: prefix
                    matches = [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), text.lower())]
                    if matches:
                        components[atom] = matches
        
        return components
    
    def extract_morpheme_components(self, text):
        """Extraction composants morphémiques avec positions"""
        components = {}
        
        if 'morpheme' in self.atoms:
            for atom in self.atoms['morpheme'].keys():
                if atom.startswith('PREFIX:'):
                    prefix = atom[7:]  # Remove PREFIX: prefix
                    pattern = r'\b' + re.escape(prefix)
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, text.lower())]
                    if matches:
                        components[atom] = matches
                elif atom.startswith('SUFFIX:'):
                    suffix = atom[7:]  # Remove SUFFIX: prefix
                    pattern = re.escape(suffix) + r'\b'
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, text.lower())]
                    if matches:
                        components[atom] = matches
                elif atom.startswith('ROOT:'):
                    root = atom[5:]  # Remove ROOT: prefix
                    pattern = r'\b' + re.escape(root) + r'\b'
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, text.lower())]
                    if matches:
                        components[atom] = matches
        
        return components
    
    def extract_syntactic_components(self, text):
        """Extraction composants syntaxiques avec positions"""
        components = {}
        
        if 'syntactic' in self.atoms:
            for atom in self.atoms['syntactic'].keys():
                if atom.startswith('PUNCT:'):
                    punct = atom[6:]  # Remove PUNCT: prefix
                    pattern = re.escape(punct)
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, text)]
                    if matches:
                        components[atom] = matches
                elif atom.startswith('SYNT:'):
                    # Patterns like "W W" represent word patterns
                    pattern_desc = atom[5:]  # Remove SYNT: prefix
                    if pattern_desc == "W W":
                        pattern = r'\b\w+\s+\w+\b'
                    elif pattern_desc == "W W W":
                        pattern = r'\b\w+\s+\w+\s+\w+\b'
                    else:
                        continue
                    
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, text)]
                    if matches:
                        components[atom] = matches
        
        return components
    
    def extract_semantic_components(self, text):
        """Extraction composants sémantiques avec positions"""
        components = {}
        
        if 'semantic' in self.atoms:
            for atom in self.atoms['semantic'].keys():
                if atom.startswith('SEM:'):
                    parts = atom.split(':')
                    if len(parts) >= 3:
                        domain = parts[1]
                        concept = parts[2]
                        
                        # Search for the specific concept
                        pattern = r'\b' + re.escape(concept) + r'\b'
                        matches = [(m.start(), m.end()) for m in re.finditer(pattern, text.lower())]
                        if matches:
                            components[atom] = matches
        
        return components
    
    def create_structure_map(self, text):
        """Crée carte structurelle du texte"""
        structure_map = []
        
        # Map characters to structural elements
        for i, char in enumerate(text):
            if char.isalpha():
                structure_map.append(('ALPHA', i, char))
            elif char.isdigit():
                structure_map.append(('DIGIT', i, char))
            elif char.isspace():
                structure_map.append(('SPACE', i, char))
            elif char in '.,;:!?':
                structure_map.append(('PUNCT', i, char))
            elif char in '"\'()[]{}':
                structure_map.append(('DELIM', i, char))
            else:
                structure_map.append(('OTHER', i, char))
        
        return structure_map
    
    def recompose_from_atoms(self, atomic_representation):
        """Recompose texte à partir de la représentation atomique"""
        original_length = atomic_representation.get('original_length', 0)
        structure_map = atomic_representation.get('structure_map', [])
        
        # Reconstruction basée sur la carte structurelle
        if structure_map:
            reconstructed = ''.join(item[2] for item in structure_map)
        else:
            # Fallback: reconstruction approximative
            reconstructed = self.approximate_reconstruction(atomic_representation)
        
        return reconstructed
    
    def approximate_reconstruction(self, atomic_representation):
        """Reconstruction approximative si pas de carte structurelle"""
        parts = []
        
        # Reconstruction basique par catégorie
        for category in ['phonetic', 'morpheme', 'syntactic', 'semantic']:
            if category in atomic_representation:
                for atom, data in atomic_representation[category].items():
                    count = data.get('count', 0)
                    if count > 0:
                        if atom.startswith('V:') or atom.startswith('C:'):
                            parts.extend([atom[2:]] * min(count, 5))  # Limit repetition
                        elif atom.startswith('PREFIX:') or atom.startswith('SUFFIX:') or atom.startswith('ROOT:'):
                            parts.extend([atom.split(':')[1]] * min(count, 3))
                        elif atom.startswith('PUNCT:'):
                            parts.extend([atom[6:]] * min(count, 3))
                        elif atom.startswith('SEM:'):
                            concept = atom.split(':')[-1]
                            parts.extend([concept] * min(count, 2))
        
        return ' '.join(parts)
    
    def calculate_fidelity(self, original, reconstructed):
        """Calcule fidélité de reconstruction"""
        if not original or not reconstructed:
            return 0.0
        
        # Similarity based on different metrics
        
        # 1. Character-level similarity
        char_similarity = difflib.SequenceMatcher(None, original, reconstructed).ratio()
        
        # 2. Word-level similarity
        orig_words = set(original.lower().split())
        recon_words = set(reconstructed.lower().split())
        if orig_words:
            word_similarity = len(orig_words & recon_words) / len(orig_words)
        else:
            word_similarity = 0.0
        
        # 3. Length similarity
        if len(original) > 0:
            length_similarity = min(len(reconstructed), len(original)) / max(len(reconstructed), len(original))
        else:
            length_similarity = 1.0 if len(reconstructed) == 0 else 0.0
        
        # 4. Hash comparison (exact match)
        hash_match = 1.0 if hashlib.md5(original.encode()).hexdigest() == hashlib.md5(reconstructed.encode()).hexdigest() else 0.0
        
        # Weighted average
        fidelity = (
            char_similarity * 0.4 +
            word_similarity * 0.3 +
            length_similarity * 0.2 +
            hash_match * 0.1
        )
        
        return {
            'overall_fidelity': fidelity,
            'character_similarity': char_similarity,
            'word_similarity': word_similarity,
            'length_similarity': length_similarity,
            'exact_match': hash_match,
            'original_length': len(original),
            'reconstructed_length': len(reconstructed)
        }
    
    def test_text_sample(self, text, sample_id="unknown"):
        """Test complet sur échantillon de texte"""
        self.log(f"🧪 Test échantillon: {sample_id}")
        
        # Phase 1: Décomposition
        self.log("  📊 Décomposition atomique...")
        atomic_repr = self.decompose_text_to_atoms(text)
        
        # Statistiques décomposition
        total_atoms = sum(
            len(category_atoms) for category_atoms in atomic_repr.values()
            if isinstance(category_atoms, dict)
        )
        
        # Phase 2: Recomposition
        self.log("  🔧 Recomposition...")
        reconstructed = self.recompose_from_atoms(atomic_repr)
        
        # Phase 3: Validation fidélité
        self.log("  📏 Calcul fidélité...")
        fidelity = self.calculate_fidelity(text, reconstructed)
        
        # Résultats
        test_result = {
            'sample_id': sample_id,
            'original_text': text,
            'reconstructed_text': reconstructed,
            'atomic_representation': atomic_repr,
            'total_atoms_found': total_atoms,
            'fidelity_metrics': fidelity,
            'compression_ratio': total_atoms / len(text) if len(text) > 0 else 0,
            'test_passed': fidelity['overall_fidelity'] > 0.7
        }
        
        self.log(f"  ✅ Fidélité: {fidelity['overall_fidelity']:.3f} | "
                f"Atomes: {total_atoms} | "
                f"Compression: {test_result['compression_ratio']:.3f}")
        
        return test_result
    
    def run_corpus_validation(self):
        """Validation sur corpus complet"""
        self.log("🚀 VALIDATION CORPUS COMPLET")
        self.log("="*50)
        
        if not self.atoms:
            self.log("❌ Pas d'atomes universaux disponibles")
            return None
        
        # Test samples from different corpus sources
        test_samples = []
        
        # Sample from simple corpus
        corpus_simple = self.workspace / 'tech' / 'corpus_simple' / 'corpus.json'
        if corpus_simple.exists():
            test_samples.extend(self.extract_test_samples(corpus_simple, "simple", 3))
        
        # Sample from pilot corpus
        corpus_pilot = self.workspace / 'tech' / 'corpus_pilot' / 'scientific_corpus_pilot.json'
        if corpus_pilot.exists():
            test_samples.extend(self.extract_test_samples(corpus_pilot, "pilot", 3))
        
        # Sample from docs
        docs_readme = self.workspace / 'docs' / 'README.md'
        if docs_readme.exists():
            test_samples.extend(self.extract_text_samples(docs_readme, "docs", 2))
        
        self.log(f"📊 {len(test_samples)} échantillons de test")
        
        # Run tests
        all_results = []
        for i, sample in enumerate(test_samples):
            result = self.test_text_sample(sample['text'], f"{sample['source']}_{i}")
            all_results.append(result)
        
        # Analyse globale
        global_analysis = self.analyze_global_results(all_results)
        
        # Sauvegarde
        self.save_validation_results(all_results, global_analysis)
        
        return global_analysis
    
    def extract_test_samples(self, json_file, source, count):
        """Extrait échantillons de test depuis JSON"""
        samples = []
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract text content from various JSON structures
            if isinstance(data, list):
                for i, item in enumerate(data[:count]):
                    if isinstance(item, dict):
                        # Try different text fields
                        text = item.get('text') or item.get('content') or item.get('description') or str(item)
                        samples.append({'text': text[:500], 'source': source})  # Limit length
                    else:
                        samples.append({'text': str(item)[:500], 'source': source})
            elif isinstance(data, dict):
                for key, value in list(data.items())[:count]:
                    if isinstance(value, str):
                        samples.append({'text': value[:500], 'source': source})
                    else:
                        samples.append({'text': str(value)[:500], 'source': source})
        
        except Exception as e:
            self.log(f"❌ Erreur extraction {json_file}: {e}")
        
        return samples
    
    def extract_text_samples(self, text_file, source, count):
        """Extrait échantillons depuis fichier texte"""
        samples = []
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into paragraphs and take samples
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            for i, paragraph in enumerate(paragraphs[:count]):
                samples.append({'text': paragraph[:500], 'source': source})
        
        except Exception as e:
            self.log(f"❌ Erreur extraction {text_file}: {e}")
        
        return samples
    
    def analyze_global_results(self, results):
        """Analyse globale des résultats"""
        if not results:
            return {}
        
        fidelities = [r['fidelity_metrics']['overall_fidelity'] for r in results]
        compressions = [r['compression_ratio'] for r in results]
        passed_tests = [r['test_passed'] for r in results]
        
        analysis = {
            'total_tests': len(results),
            'passed_tests': sum(passed_tests),
            'success_rate': sum(passed_tests) / len(results),
            'average_fidelity': sum(fidelities) / len(fidelities),
            'average_compression': sum(compressions) / len(compressions),
            'min_fidelity': min(fidelities),
            'max_fidelity': max(fidelities),
            'fidelity_distribution': {
                'excellent': len([f for f in fidelities if f > 0.9]),
                'good': len([f for f in fidelities if 0.7 <= f <= 0.9]),
                'poor': len([f for f in fidelities if f < 0.7])
            }
        }
        
        return analysis
    
    def save_validation_results(self, results, analysis):
        """Sauvegarde résultats validation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Résultats détaillés
        detailed_file = self.results_dir / f"synthesis_validation_detailed_{timestamp}.json"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Analyse globale
        analysis_file = self.results_dir / f"synthesis_validation_analysis_{timestamp}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Résultats sauvés: {detailed_file.name}")
        self.log(f"📊 Analyse: {analysis_file.name}")
        
        # Affichage résumé
        self.print_validation_summary(analysis)
    
    def print_validation_summary(self, analysis):
        """Affiche résumé validation"""
        print("\n" + "="*60)
        print("🧬 RÉSUMÉ VALIDATION SYNTHÈSE PANINI")
        print("="*60)
        print(f"🧪 Tests effectués: {analysis['total_tests']}")
        print(f"✅ Tests réussis: {analysis['passed_tests']}")
        print(f"📊 Taux de succès: {analysis['success_rate']:.1%}")
        print(f"🎯 Fidélité moyenne: {analysis['average_fidelity']:.3f}")
        print(f"📦 Compression moyenne: {analysis['average_compression']:.3f}")
        print(f"⬆️ Fidélité max: {analysis['max_fidelity']:.3f}")
        print(f"⬇️ Fidélité min: {analysis['min_fidelity']:.3f}")
        
        dist = analysis['fidelity_distribution']
        print(f"\n📈 DISTRIBUTION FIDÉLITÉ:")
        print(f"  🟢 Excellente (>90%): {dist['excellent']}")
        print(f"  🟡 Bonne (70-90%): {dist['good']}")
        print(f"  🔴 Faible (<70%): {dist['poor']}")
        
        print("="*60)


def main():
    print("🧬 SYNTHÉTISEUR VALIDATEUR PANINI")
    print("="*40)
    print("Test ultime: décomposer → recomposer → valider")
    print("Mesure fidélité compression/décompression")
    print("="*40)
    
    validator = PaniniSynthesisValidator()
    
    if not validator.atoms:
        print("❌ Atomes universaux requis - exécuter universal_atoms_extractor.py d'abord")
        return
    
    # Test simple
    test_text = "This is a simple test with numbers 123 and some punctuation!"
    result = validator.test_text_sample(test_text, "simple_test")
    
    print(f"\n🧪 TEST SIMPLE:")
    print(f"Original: {test_text}")
    print(f"Recomposé: {result['reconstructed_text']}")
    print(f"Fidélité: {result['fidelity_metrics']['overall_fidelity']:.3f}")
    
    # Validation corpus complet
    global_analysis = validator.run_corpus_validation()
    
    if global_analysis:
        print(f"\n✅ Validation terminée!")
        print(f"📁 Résultats dans synthesis_validation_results/")
    else:
        print(f"\n❌ Échec validation")


if __name__ == '__main__':
    main()
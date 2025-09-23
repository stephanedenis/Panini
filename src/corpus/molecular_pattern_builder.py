#!/usr/bin/env python3
"""
Constructeur de Molécules et Isotopes PaniniFS
Construction de patterns composés à partir des atomes universaux
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import itertools


class MolecularPatternBuilder:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'molecular_patterns_results'
        self.results_dir.mkdir(exist_ok=True)
        
        # Chargement atomes universaux
        self.atoms = self.load_universal_atoms()
        
        # Structures moléculaires
        self.phonetic_molecules = defaultdict(list)
        self.morpheme_molecules = defaultdict(list)
        self.syntactic_molecules = defaultdict(list)
        self.semantic_molecules = defaultdict(list)
        
        # Isotopes (variations contextuelles)
        self.isotope_variations = defaultdict(dict)
        
        # Métriques de composition
        self.composition_rules = {}
        self.decomposition_fidelity = {}
        
        self.log("🧪 Constructeur Moléculaire initialisé")
    
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def load_universal_atoms(self):
        """Charge les atomes universaux précédemment extraits"""
        atoms_dir = self.workspace / 'universal_atoms_results'
        if not atoms_dir.exists():
            self.log("❌ Aucun atome universel trouvé - exécuter d'abord universal_atoms_extractor.py")
            return {}
        
        # Trouver le fichier le plus récent
        atom_files = list(atoms_dir.glob("universal_atoms_analysis_*.json"))
        if not atom_files:
            self.log("❌ Aucun fichier d'analyse trouvé")
            return {}
        
        latest_file = max(atom_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.log(f"📊 Atomes chargés: {latest_file.name}")
        return data.get('universality_scores', {})
    
    def extract_high_universality_atoms(self, category, threshold=0.1):
        """Extrait les atomes à haute universalité"""
        if category not in self.atoms:
            return []
        
        high_atoms = []
        for atom, data in self.atoms[category].items():
            if data['universality'] > threshold:
                high_atoms.append({
                    'atom': atom,
                    'universality': data['universality'],
                    'count': data['count'],
                    'frequency': data['frequency']
                })
        
        return sorted(high_atoms, key=lambda x: x['universality'], reverse=True)
    
    def build_phonetic_molecules(self):
        """Construction molécules phonétiques"""
        self.log("🔤 Construction molécules phonétiques...")
        
        high_atoms = self.extract_high_universality_atoms('phonetic', 0.05)
        
        # Patterns de combinaisons fréquentes
        vowel_atoms = [a for a in high_atoms if a['atom'].startswith('V:')]
        consonant_atoms = [a for a in high_atoms if a['atom'].startswith('C:')]
        
        # Molécules CV (Consonne-Voyelle)
        cv_molecules = []
        for c_atom in consonant_atoms[:10]:  # Top 10 consonnes
            for v_atom in vowel_atoms[:5]:   # Top 5 voyelles
                cv_pattern = f"{c_atom['atom']}-{v_atom['atom']}"
                strength = (c_atom['universality'] + v_atom['universality']) / 2
                
                cv_molecules.append({
                    'pattern': cv_pattern,
                    'type': 'CV_syllable',
                    'strength': strength,
                    'components': [c_atom['atom'], v_atom['atom']]
                })
        
        self.phonetic_molecules['cv_syllables'] = sorted(
            cv_molecules, key=lambda x: x['strength'], reverse=True
        )[:20]
        
        # Molécules CVC (Consonne-Voyelle-Consonne)
        cvc_molecules = []
        for c1_atom in consonant_atoms[:5]:
            for v_atom in vowel_atoms[:3]:
                for c2_atom in consonant_atoms[:5]:
                    if c1_atom != c2_atom:  # Éviter répétitions
                        cvc_pattern = f"{c1_atom['atom']}-{v_atom['atom']}-{c2_atom['atom']}"
                        strength = (c1_atom['universality'] + v_atom['universality'] + 
                                  c2_atom['universality']) / 3
                        
                        cvc_molecules.append({
                            'pattern': cvc_pattern,
                            'type': 'CVC_syllable',
                            'strength': strength,
                            'components': [c1_atom['atom'], v_atom['atom'], c2_atom['atom']]
                        })
        
        self.phonetic_molecules['cvc_syllables'] = sorted(
            cvc_molecules, key=lambda x: x['strength'], reverse=True
        )[:15]
        
        self.log(f"✅ {len(self.phonetic_molecules)} types de molécules phonétiques")
    
    def build_morpheme_molecules(self):
        """Construction molécules morphémiques"""
        self.log("🧩 Construction molécules morphémiques...")
        
        high_atoms = self.extract_high_universality_atoms('morpheme', 0.1)
        
        prefixes = [a for a in high_atoms if 'PREFIX:' in a['atom']]
        suffixes = [a for a in high_atoms if 'SUFFIX:' in a['atom']]
        roots = [a for a in high_atoms if 'ROOT:' in a['atom']]
        
        # Molécules Prefix+Root
        prefix_root_molecules = []
        for prefix in prefixes[:8]:
            for root in roots[:10]:
                pattern = f"{prefix['atom']}+{root['atom']}"
                strength = (prefix['universality'] + root['universality']) / 2
                
                prefix_root_molecules.append({
                    'pattern': pattern,
                    'type': 'prefix_root',
                    'strength': strength,
                    'components': [prefix['atom'], root['atom']],
                    'meaning': self.infer_compound_meaning(prefix['atom'], root['atom'])
                })
        
        self.morpheme_molecules['prefix_root'] = sorted(
            prefix_root_molecules, key=lambda x: x['strength'], reverse=True
        )[:15]
        
        # Molécules Root+Suffix
        root_suffix_molecules = []
        for root in roots[:10]:
            for suffix in suffixes[:8]:
                pattern = f"{root['atom']}+{suffix['atom']}"
                strength = (root['universality'] + suffix['universality']) / 2
                
                root_suffix_molecules.append({
                    'pattern': pattern,
                    'type': 'root_suffix',
                    'strength': strength,
                    'components': [root['atom'], suffix['atom']],
                    'meaning': self.infer_compound_meaning(root['atom'], suffix['atom'])
                })
        
        self.morpheme_molecules['root_suffix'] = sorted(
            root_suffix_molecules, key=lambda x: x['strength'], reverse=True
        )[:15]
        
        # Molécules complexes Prefix+Root+Suffix
        complex_molecules = []
        for prefix in prefixes[:5]:
            for root in roots[:5]:
                for suffix in suffixes[:5]:
                    pattern = f"{prefix['atom']}+{root['atom']}+{suffix['atom']}"
                    strength = (prefix['universality'] + root['universality'] + 
                              suffix['universality']) / 3
                    
                    complex_molecules.append({
                        'pattern': pattern,
                        'type': 'prefix_root_suffix',
                        'strength': strength,
                        'components': [prefix['atom'], root['atom'], suffix['atom']],
                        'meaning': self.infer_complex_meaning(prefix['atom'], root['atom'], suffix['atom'])
                    })
        
        self.morpheme_molecules['complex'] = sorted(
            complex_molecules, key=lambda x: x['strength'], reverse=True
        )[:10]
        
        self.log(f"✅ {len(self.morpheme_molecules)} types de molécules morphémiques")
    
    def infer_compound_meaning(self, atom1, atom2):
        """Inférence basique du sens composé"""
        meaning_map = {
            'PREFIX:co': 'together',
            'PREFIX:in': 'not/into',
            'PREFIX:re': 'again',
            'PREFIX:pre': 'before',
            'SUFFIX:tion': 'action/process',
            'SUFFIX:ing': 'ongoing',
            'SUFFIX:er': 'agent',
            'ROOT:id': 'identity'
        }
        
        meaning1 = meaning_map.get(atom1, atom1.split(':')[-1])
        meaning2 = meaning_map.get(atom2, atom2.split(':')[-1])
        
        return f"{meaning1}+{meaning2}"
    
    def infer_complex_meaning(self, prefix, root, suffix):
        """Inférence du sens complexe"""
        prefix_meaning = self.infer_compound_meaning(prefix, "")
        root_meaning = self.infer_compound_meaning(root, "")
        suffix_meaning = self.infer_compound_meaning("", suffix)
        
        return f"{prefix_meaning.rstrip('+')}-{root_meaning.rstrip('+')}-{suffix_meaning.lstrip('+')}"
    
    def build_syntactic_molecules(self):
        """Construction molécules syntaxiques"""
        self.log("🏗️ Construction molécules syntaxiques...")
        
        high_atoms = self.extract_high_universality_atoms('syntactic', 0.3)
        
        # Patterns de ponctuation + structure
        punct_atoms = [a for a in high_atoms if 'PUNCT:' in a['atom']]
        synt_atoms = [a for a in high_atoms if 'SYNT:' in a['atom']]
        
        # Molécules de délimitation
        delimiter_molecules = []
        for punct in punct_atoms:
            for synt in synt_atoms[:5]:
                pattern = f"{punct['atom']}|{synt['atom']}"
                strength = (punct['universality'] + synt['universality']) / 2
                
                delimiter_molecules.append({
                    'pattern': pattern,
                    'type': 'delimiter_structure',
                    'strength': strength,
                    'components': [punct['atom'], synt['atom']],
                    'function': self.infer_syntactic_function(punct['atom'], synt['atom'])
                })
        
        self.syntactic_molecules['delimiters'] = sorted(
            delimiter_molecules, key=lambda x: x['strength'], reverse=True
        )[:10]
        
        # Patterns de structure complexe
        structure_molecules = []
        for synt1 in synt_atoms[:3]:
            for synt2 in synt_atoms[:3]:
                if synt1 != synt2:
                    pattern = f"{synt1['atom']}→{synt2['atom']}"
                    strength = (synt1['universality'] + synt2['universality']) / 2
                    
                    structure_molecules.append({
                        'pattern': pattern,
                        'type': 'structure_sequence',
                        'strength': strength,
                        'components': [synt1['atom'], synt2['atom']],
                        'function': self.infer_sequence_function(synt1['atom'], synt2['atom'])
                    })
        
        self.syntactic_molecules['sequences'] = sorted(
            structure_molecules, key=lambda x: x['strength'], reverse=True
        )[:8]
        
        self.log(f"✅ {len(self.syntactic_molecules)} types de molécules syntaxiques")
    
    def infer_syntactic_function(self, punct, synt):
        """Inférence fonction syntaxique"""
        if '"' in punct:
            return "quotation_boundary"
        elif ',' in punct:
            return "enumeration_separator"
        elif ':' in punct:
            return "explanation_introducer"
        elif 'W W' in synt:
            return "binary_relation"
        elif 'W W W' in synt:
            return "ternary_relation"
        else:
            return "structural_marker"
    
    def infer_sequence_function(self, synt1, synt2):
        """Inférence fonction de séquence"""
        return f"transition_{synt1.split(':')[-1]}_to_{synt2.split(':')[-1]}"
    
    def build_semantic_molecules(self):
        """Construction molécules sémantiques"""
        self.log("💭 Construction molécules sémantiques...")
        
        high_atoms = self.extract_high_universality_atoms('semantic', 0.1)
        
        # Groupement par domaine sémantique
        domains = defaultdict(list)
        for atom in high_atoms:
            domain = atom['atom'].split(':')[1]  # SEM:domain:concept
            domains[domain].append(atom)
        
        # Molécules intra-domaine
        for domain, atoms in domains.items():
            if len(atoms) >= 2:
                domain_molecules = []
                
                for i, atom1 in enumerate(atoms):
                    for atom2 in atoms[i+1:]:
                        pattern = f"{atom1['atom']}⊕{atom2['atom']}"
                        strength = (atom1['universality'] + atom2['universality']) / 2
                        
                        domain_molecules.append({
                            'pattern': pattern,
                            'type': f'{domain}_composition',
                            'strength': strength,
                            'components': [atom1['atom'], atom2['atom']],
                            'domain': domain,
                            'semantic_relation': self.infer_semantic_relation(atom1['atom'], atom2['atom'])
                        })
                
                self.semantic_molecules[domain] = sorted(
                    domain_molecules, key=lambda x: x['strength'], reverse=True
                )[:8]
        
        # Molécules inter-domaines
        domain_pairs = list(itertools.combinations(domains.keys(), 2))
        inter_molecules = []
        
        for domain1, domain2 in domain_pairs[:5]:
            for atom1 in domains[domain1][:3]:
                for atom2 in domains[domain2][:3]:
                    pattern = f"{atom1['atom']}⟷{atom2['atom']}"
                    strength = (atom1['universality'] + atom2['universality']) / 2
                    
                    inter_molecules.append({
                        'pattern': pattern,
                        'type': 'cross_domain',
                        'strength': strength,
                        'components': [atom1['atom'], atom2['atom']],
                        'domains': [domain1, domain2],
                        'semantic_relation': self.infer_cross_domain_relation(domain1, domain2)
                    })
        
        self.semantic_molecules['cross_domain'] = sorted(
            inter_molecules, key=lambda x: x['strength'], reverse=True
        )[:10]
        
        self.log(f"✅ {len(self.semantic_molecules)} domaines de molécules sémantiques")
    
    def infer_semantic_relation(self, atom1, atom2):
        """Inférence relation sémantique"""
        concept1 = atom1.split(':')[-1]
        concept2 = atom2.split(':')[-1]
        
        # Relations numériques
        if concept1.isdigit() and concept2.isdigit():
            return f"numeric_sequence_{concept1}_to_{concept2}"
        
        return f"conceptual_association_{concept1}_{concept2}"
    
    def infer_cross_domain_relation(self, domain1, domain2):
        """Inférence relation cross-domain"""
        relations = {
            ('numbers', 'colors'): 'quantification_of_properties',
            ('numbers', 'time'): 'temporal_measurement',
            ('colors', 'emotion'): 'synesthetic_association',
            ('time', 'space'): 'spatiotemporal_mapping',
            ('body', 'action'): 'embodied_cognition'
        }
        
        return relations.get((domain1, domain2)) or relations.get((domain2, domain1)) or f"generic_{domain1}_{domain2}_link"
    
    def identify_isotopes(self):
        """Identification des isotopes (variations contextuelles)"""
        self.log("⚛️ Identification isotopes contextuels...")
        
        # Pour chaque molécule, identifier variations
        all_molecules = {}
        all_molecules.update(self.phonetic_molecules)
        all_molecules.update(self.morpheme_molecules)
        all_molecules.update(self.syntactic_molecules)
        all_molecules.update(self.semantic_molecules)
        
        for molecule_type, molecules in all_molecules.items():
            isotope_variants = defaultdict(list)
            
            for molecule in molecules:
                base_pattern = molecule['pattern']
                
                # Variations de force (isotopes énergétiques)
                if molecule['strength'] > 0.5:
                    isotope_variants['high_energy'].append(molecule)
                elif molecule['strength'] > 0.2:
                    isotope_variants['medium_energy'].append(molecule)
                else:
                    isotope_variants['low_energy'].append(molecule)
                
                # Variations de complexité (isotopes structurels)
                component_count = len(molecule.get('components', []))
                if component_count >= 3:
                    isotope_variants['complex'].append(molecule)
                elif component_count == 2:
                    isotope_variants['binary'].append(molecule)
                else:
                    isotope_variants['atomic'].append(molecule)
            
            self.isotope_variations[molecule_type] = dict(isotope_variants)
        
        self.log(f"✅ Isotopes identifiés: {len(self.isotope_variations)} types")
    
    def validate_molecular_composition(self):
        """Validation par décomposition/recomposition"""
        self.log("🧪 Validation composition moléculaire...")
        
        validation_results = {}
        
        # Test pour chaque type de molécule
        all_molecules = {}
        all_molecules.update(self.phonetic_molecules)
        all_molecules.update(self.morpheme_molecules)
        all_molecules.update(self.syntactic_molecules)
        all_molecules.update(self.semantic_molecules)
        
        for molecule_type, molecules in all_molecules.items():
            type_results = {
                'total_molecules': len(molecules),
                'decomposable': 0,
                'recomposable': 0,
                'fidelity_scores': []
            }
            
            for molecule in molecules:
                components = molecule.get('components', [])
                
                # Test décomposition
                if len(components) >= 2:
                    type_results['decomposable'] += 1
                    
                    # Test recomposition (simulation)
                    reconstructed_strength = sum(
                        self.get_atom_universality(comp) for comp in components
                    ) / len(components)
                    
                    original_strength = molecule['strength']
                    fidelity = min(1.0, reconstructed_strength / original_strength) if original_strength > 0 else 0
                    
                    if fidelity > 0.8:
                        type_results['recomposable'] += 1
                    
                    type_results['fidelity_scores'].append(fidelity)
            
            # Calcul moyennes
            if type_results['fidelity_scores']:
                type_results['average_fidelity'] = sum(type_results['fidelity_scores']) / len(type_results['fidelity_scores'])
            else:
                type_results['average_fidelity'] = 0.0
            
            validation_results[molecule_type] = type_results
        
        self.composition_rules = validation_results
        self.log(f"✅ Validation terminée: {len(validation_results)} types testés")
        
        return validation_results
    
    def get_atom_universality(self, atom):
        """Récupère universalité d'un atome"""
        for category in self.atoms:
            if atom in self.atoms[category]:
                return self.atoms[category][atom]['universality']
        return 0.0
    
    def generate_molecular_report(self):
        """Génère rapport complet des molécules"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'generation_time': timestamp,
            'molecular_patterns': {
                'phonetic': dict(self.phonetic_molecules),
                'morpheme': dict(self.morpheme_molecules),
                'syntactic': dict(self.syntactic_molecules),
                'semantic': dict(self.semantic_molecules)
            },
            'isotope_variations': dict(self.isotope_variations),
            'composition_validation': self.composition_rules,
            'statistics': self.calculate_statistics()
        }
        
        # Sauvegarde rapport complet
        report_file = self.results_dir / f"molecular_patterns_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Résumé exécutif
        summary_file = self.results_dir / f"molecular_summary_{timestamp}.json"
        summary = self.create_executive_summary(report)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        self.log(f"📊 Rapport sauvé: {report_file.name}")
        self.log(f"📋 Résumé: {summary_file.name}")
        
        return report
    
    def calculate_statistics(self):
        """Calcule statistiques globales"""
        stats = {
            'total_molecule_types': 0,
            'total_molecules': 0,
            'average_strength': 0.0,
            'isotope_diversity': 0
        }
        
        all_molecules = []
        for molecules in self.phonetic_molecules.values():
            all_molecules.extend(molecules)
        for molecules in self.morpheme_molecules.values():
            all_molecules.extend(molecules)
        for molecules in self.syntactic_molecules.values():
            all_molecules.extend(molecules)
        for molecules in self.semantic_molecules.values():
            all_molecules.extend(molecules)
        
        stats['total_molecule_types'] = (len(self.phonetic_molecules) + 
                                       len(self.morpheme_molecules) + 
                                       len(self.syntactic_molecules) + 
                                       len(self.semantic_molecules))
        
        stats['total_molecules'] = len(all_molecules)
        
        if all_molecules:
            stats['average_strength'] = sum(m['strength'] for m in all_molecules) / len(all_molecules)
        
        stats['isotope_diversity'] = len(self.isotope_variations)
        
        return stats
    
    def create_executive_summary(self, report):
        """Crée résumé exécutif"""
        stats = report['statistics']
        
        return {
            'executive_summary': {
                'total_molecular_patterns': stats['total_molecules'],
                'pattern_diversity': stats['total_molecule_types'],
                'average_universality': stats['average_strength'],
                'isotope_variants': stats['isotope_diversity']
            },
            'top_patterns_by_category': self.extract_top_patterns(),
            'validation_summary': self.summarize_validation(),
            'recommendations': self.generate_recommendations()
        }
    
    def extract_top_patterns(self):
        """Extrait top patterns par catégorie"""
        top_patterns = {}
        
        categories = [
            ('phonetic', self.phonetic_molecules),
            ('morpheme', self.morpheme_molecules),
            ('syntactic', self.syntactic_molecules),
            ('semantic', self.semantic_molecules)
        ]
        
        for cat_name, cat_molecules in categories:
            cat_top = []
            for molecule_type, molecules in cat_molecules.items():
                if molecules:
                    top_molecule = max(molecules, key=lambda x: x['strength'])
                    cat_top.append({
                        'type': molecule_type,
                        'pattern': top_molecule['pattern'],
                        'strength': top_molecule['strength']
                    })
            
            top_patterns[cat_name] = sorted(cat_top, key=lambda x: x['strength'], reverse=True)[:3]
        
        return top_patterns
    
    def summarize_validation(self):
        """Résume validation composition"""
        if not self.composition_rules:
            return {"status": "not_performed"}
        
        total_fidelity = []
        for results in self.composition_rules.values():
            total_fidelity.append(results.get('average_fidelity', 0))
        
        return {
            'overall_fidelity': sum(total_fidelity) / len(total_fidelity) if total_fidelity else 0,
            'validation_coverage': len(self.composition_rules),
            'high_fidelity_types': len([f for f in total_fidelity if f > 0.8])
        }
    
    def generate_recommendations(self):
        """Génère recommandations"""
        return [
            "Prioriser molécules phonétiques CV/CVC pour synthèse vocale",
            "Utiliser molécules morphémiques pour compression sémantique",
            "Exploiter patterns syntaxiques pour analyse structurelle",
            "Développer isotopes pour adaptation contextuelle",
            "Valider par recomposition avant déploiement production"
        ]
    
    def run_full_analysis(self):
        """Lance analyse moléculaire complète"""
        self.log("🚀 ANALYSE MOLÉCULAIRE COMPLÈTE")
        self.log("="*50)
        
        if not self.atoms:
            self.log("❌ Pas d'atomes disponibles")
            return None
        
        # Construction séquentielle
        self.build_phonetic_molecules()
        self.build_morpheme_molecules()
        self.build_syntactic_molecules()
        self.build_semantic_molecules()
        
        # Identification isotopes
        self.identify_isotopes()
        
        # Validation
        validation = self.validate_molecular_composition()
        
        # Génération rapport
        report = self.generate_molecular_report()
        
        self.print_molecular_summary(report)
        
        return report
    
    def print_molecular_summary(self, report):
        """Affiche résumé des molécules"""
        stats = report['statistics']
        
        print("\n" + "="*60)
        print("🧪 RÉSUMÉ CONSTRUCTION MOLÉCULAIRE")
        print("="*60)
        print(f"🔬 Types moléculaires: {stats['total_molecule_types']}")
        print(f"⚗️ Molécules totales: {stats['total_molecules']}")
        print(f"💪 Force moyenne: {stats['average_strength']:.4f}")
        print(f"⚛️ Variants isotopiques: {stats['isotope_diversity']}")
        
        # Validation summary
        if self.composition_rules:
            print(f"\n🧮 VALIDATION COMPOSITION:")
            total_fidelity = []
            for mol_type, results in self.composition_rules.items():
                fidelity = results.get('average_fidelity', 0)
                total_fidelity.append(fidelity)
                print(f"  {mol_type}: {fidelity:.3f} fidélité")
            
            overall = sum(total_fidelity) / len(total_fidelity) if total_fidelity else 0
            print(f"📊 Fidélité globale: {overall:.3f}")
        
        print("="*60)


def main():
    print("🧪 CONSTRUCTEUR MOLÉCULES ET ISOTOPES PANINI")
    print("="*52)
    print("Construction patterns composés à partir atomes universaux")
    print("Identification isotopes et validation par synthèse")
    print("="*52)
    
    builder = MolecularPatternBuilder()
    report = builder.run_full_analysis()
    
    if report:
        print("\n✅ Analyse moléculaire terminée avec succès!")
        print("📁 Résultats disponibles dans molecular_patterns_results/")
    else:
        print("\n❌ Échec analyse - vérifier disponibilité atomes universaux")


if __name__ == '__main__':
    main()
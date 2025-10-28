#!/usr/bin/env python3
"""
📏 PANINI-FS SIZE ANALYSIS ENGINE
=================================

Mission: Analyser en détail les tailles des représentations Panini
et de l'encyclopédie de connaissances pour optimiser l'efficacité
de stockage et comprendre l'overhead du système.

Analyses prévues:
1. Taille fichiers compressés vs originaux
2. Overhead métadonnées par fichier
3. Taille encyclopédies de connaissances
4. Ratio efficacité stockage global
5. Analyse distribution tailles par format
6. Optimisations possibles identified

Objectifs:
- Mesurer overhead réel du système PaniniFS
- Identifier goulots d'étranglement de taille
- Proposer optimisations pour réduire overhead
- Valider viabilité économique du système
"""

import os
import sys
import json
import glob
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import numpy as np

class PaniniSizeAnalysisEngine:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.analysis_results = {}
        self.size_statistics = defaultdict(dict)
        self.overhead_analysis = defaultdict(dict)
        
        print(f"""
📏 PANINI-FS SIZE ANALYSIS ENGINE
============================================================
🎯 Mission: Analyser efficacité stockage système PaniniFS
📊 Analyse: Fichiers compressés + Métadonnées + Encyclopédies
⏰ Session: {self.timestamp}

🔍 Initialisation analyse des tailles...
""")

    def analyze_compressed_files_sizes(self):
        """Analyser les tailles des fichiers compressés"""
        print("\n📊 ANALYSE TAILLES FICHIERS COMPRESSÉS")
        print("=" * 60)
        
        # Trouver le dossier de batch le plus récent
        batch_dirs = [d for d in os.listdir('.') if d.startswith('panini_universal_batch_')]
        if not batch_dirs:
            print("❌ Aucun dossier de compression trouvé")
            return {}
        
        latest_batch = sorted(batch_dirs)[-1]
        batch_path = Path(latest_batch)
        
        print(f"📁 Analyse du batch: {latest_batch}")
        
        # Analyser chaque fichier compressé
        compressed_files = list(batch_path.glob("*.panini"))
        metadata_files = list(batch_path.glob("*.panini.meta"))
        
        print(f"🗜️  Fichiers compressés trouvés: {len(compressed_files)}")
        print(f"📋 Fichiers métadonnées trouvés: {len(metadata_files)}")
        
        file_analysis = []
        total_original = 0
        total_compressed = 0
        total_metadata = 0
        
        for compressed_file in compressed_files:
            metadata_file = Path(str(compressed_file) + ".meta")
            
            if metadata_file.exists():
                # Tailles fichiers
                compressed_size = compressed_file.stat().st_size
                metadata_size = metadata_file.stat().st_size
                
                # Charger métadonnées pour taille originale
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                original_size = metadata['original_size']
                extension = metadata['extension']
                category = metadata['category']
                
                # Calculer ratios
                compression_ratio = compressed_size / original_size if original_size > 0 else 1
                metadata_overhead = metadata_size / original_size if original_size > 0 else 0
                total_panini_size = compressed_size + metadata_size
                total_ratio = total_panini_size / original_size if original_size > 0 else 1
                
                analysis_point = {
                    'filename': compressed_file.name,
                    'extension': extension,
                    'category': category,
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'metadata_size': metadata_size,
                    'total_panini_size': total_panini_size,
                    'compression_ratio': compression_ratio,
                    'metadata_overhead': metadata_overhead,
                    'total_ratio': total_ratio,
                    'space_saved': original_size - total_panini_size,
                    'space_saved_pct': (1 - total_ratio) * 100
                }
                
                file_analysis.append(analysis_point)
                
                total_original += original_size
                total_compressed += compressed_size
                total_metadata += metadata_size
        
        # Statistiques globales
        total_panini = total_compressed + total_metadata
        global_compression_ratio = total_compressed / total_original if total_original > 0 else 1
        global_metadata_overhead = total_metadata / total_original if total_original > 0 else 0
        global_total_ratio = total_panini / total_original if total_original > 0 else 1
        
        print(f"""
📊 STATISTIQUES GLOBALES:
   Taille originale totale  : {self._format_size(total_original)}
   Taille compressée totale : {self._format_size(total_compressed)}
   Taille métadonnées totale: {self._format_size(total_metadata)}
   Taille PaniniFS totale   : {self._format_size(total_panini)}
   
   Ratio compression seule  : {global_compression_ratio:.3f}
   Overhead métadonnées     : {global_metadata_overhead:.3f} ({(global_metadata_overhead*100):.1f}%)
   Ratio PaniniFS total     : {global_total_ratio:.3f}
   Économie globale         : {self._format_size(total_original - total_panini)} ({((1-global_total_ratio)*100):.1f}%)
""")
        
        # Top/Worst performers
        file_analysis.sort(key=lambda x: x['total_ratio'])
        
        print("\n🏆 TOP 5 MEILLEURS RATIOS PANINI:")
        for i, analysis in enumerate(file_analysis[:5]):
            print(f"   {i+1}. {analysis['extension']:6} : {analysis['total_ratio']:.3f} "
                  f"({analysis['space_saved_pct']:+5.1f}%) - {Path(analysis['filename']).stem[:30]}")
        
        print("\n⚠️  TOP 5 PIRES RATIOS PANINI:")
        for i, analysis in enumerate(file_analysis[-5:]):
            print(f"   {i+1}. {analysis['extension']:6} : {analysis['total_ratio']:.3f} "
                  f"({analysis['space_saved_pct']:+5.1f}%) - {Path(analysis['filename']).stem[:30]}")
        
        self.size_statistics['files'] = {
            'total_files': len(file_analysis),
            'total_original': total_original,
            'total_compressed': total_compressed,
            'total_metadata': total_metadata,
            'total_panini': total_panini,
            'global_compression_ratio': global_compression_ratio,
            'global_metadata_overhead': global_metadata_overhead,
            'global_total_ratio': global_total_ratio,
            'file_details': file_analysis
        }
        
        return file_analysis

    def analyze_metadata_overhead(self, file_analysis):
        """Analyser l'overhead des métadonnées en détail"""
        print("\n📋 ANALYSE OVERHEAD MÉTADONNÉES")
        print("=" * 60)
        
        # Analyser overhead par extension
        overhead_by_ext = defaultdict(list)
        for analysis in file_analysis:
            overhead_by_ext[analysis['extension']].append(analysis['metadata_overhead'])
        
        print("📊 OVERHEAD MÉTADONNÉES PAR EXTENSION:")
        ext_overheads = []
        for ext, overheads in overhead_by_ext.items():
            avg_overhead = np.mean(overheads)
            max_overhead = max(overheads)
            min_overhead = min(overheads)
            ext_overheads.append((ext, avg_overhead, min_overhead, max_overhead, len(overheads)))
        
        ext_overheads.sort(key=lambda x: x[1], reverse=True)
        
        for ext, avg, min_oh, max_oh, count in ext_overheads:
            print(f"   {ext:8} : {avg:.3f} avg ({min_oh:.3f}-{max_oh:.3f}) sur {count} fichiers")
        
        # Analyser overhead par taille de fichier
        size_ranges = [
            (0, 1024, "< 1KB"),
            (1024, 10*1024, "1KB-10KB"), 
            (10*1024, 100*1024, "10KB-100KB"),
            (100*1024, 1024*1024, "100KB-1MB"),
            (1024*1024, 10*1024*1024, "1MB-10MB"),
            (10*1024*1024, float('inf'), "> 10MB")
        ]
        
        print("\n📊 OVERHEAD PAR TAILLE FICHIER:")
        for min_size, max_size, label in size_ranges:
            range_files = [a for a in file_analysis 
                          if min_size <= a['original_size'] < max_size]
            if range_files:
                avg_overhead = np.mean([a['metadata_overhead'] for a in range_files])
                print(f"   {label:12} : {avg_overhead:.3f} avg overhead ({len(range_files)} fichiers)")
        
        # Analyser contenu des métadonnées
        sample_metadata_file = None
        for analysis in file_analysis[:3]:  # Prendre 3 exemples
            metadata_file = Path(f"panini_universal_batch_*/{analysis['filename']}.meta")
            metadata_files = glob.glob(str(metadata_file))
            if metadata_files:
                sample_metadata_file = metadata_files[0]
                break
        
        if sample_metadata_file:
            print(f"\n📋 ANALYSE CONTENU MÉTADONNÉES (exemple: {Path(sample_metadata_file).name}):")
            with open(sample_metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Calculer taille de chaque section
            metadata_sections = {}
            for key, value in metadata.items():
                section_json = json.dumps({key: value}, ensure_ascii=False)
                metadata_sections[key] = len(section_json.encode('utf-8'))
            
            total_metadata_size = sum(metadata_sections.values())
            
            print("   Répartition taille métadonnées:")
            sorted_sections = sorted(metadata_sections.items(), key=lambda x: x[1], reverse=True)
            for section, size in sorted_sections:
                pct = (size / total_metadata_size) * 100
                print(f"     {section:20} : {size:5} bytes ({pct:4.1f}%)")
        
        self.overhead_analysis['metadata'] = {
            'by_extension': dict(overhead_by_ext),
            'by_size_range': size_ranges,
            'average_overhead': np.mean([a['metadata_overhead'] for a in file_analysis]),
            'max_overhead': max([a['metadata_overhead'] for a in file_analysis]),
            'min_overhead': min([a['metadata_overhead'] for a in file_analysis])
        }

    def analyze_encyclopedia_sizes(self):
        """Analyser les tailles des encyclopédies de connaissances"""
        print("\n📚 ANALYSE TAILLES ENCYCLOPÉDIES")
        print("=" * 60)
        
        encyclopedia_files = {
            'format_encyclopedia': glob.glob("PANINI_FORMAT_ENCYCLOPEDIA_*.json"),
            'optimization_encyclopedia': glob.glob("PANINI_OPTIMIZATION_ENCYCLOPEDIA_*.json"),
            'reports': glob.glob("PANINI_OPTIMIZATION_REPORT_*.md"),
            'batch_reports': glob.glob("panini_universal_batch_*/panini_universal_report.json")
        }
        
        encyclopedia_analysis = {}
        total_encyclopedia_size = 0
        
        for category, files in encyclopedia_files.items():
            if files:
                latest_file = sorted(files)[-1]  # Plus récent
                file_size = os.path.getsize(latest_file)
                total_encyclopedia_size += file_size
                
                # Analyser contenu si JSON
                content_analysis = {}
                if latest_file.endswith('.json'):
                    try:
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                        
                        # Analyser sections principales
                        for key, value in content.items():
                            if isinstance(value, (dict, list)):
                                section_json = json.dumps({key: value}, ensure_ascii=False)
                                content_analysis[key] = len(section_json.encode('utf-8'))
                    except Exception as e:
                        content_analysis['error'] = str(e)
                
                encyclopedia_analysis[category] = {
                    'file': latest_file,
                    'size': file_size,
                    'content_breakdown': content_analysis
                }
                
                print(f"📖 {category:25} : {self._format_size(file_size):>10} - {Path(latest_file).name}")
                
                # Afficher breakdown du contenu
                if content_analysis and 'error' not in content_analysis:
                    total_content = sum(content_analysis.values())
                    print("   Répartition contenu:")
                    sorted_content = sorted(content_analysis.items(), key=lambda x: x[1], reverse=True)
                    for section, size in sorted_content[:5]:  # Top 5
                        pct = (size / total_content) * 100 if total_content > 0 else 0
                        print(f"     {section:20} : {self._format_size(size):>8} ({pct:4.1f}%)")
        
        print(f"\n📊 TAILLE TOTALE ENCYCLOPÉDIES: {self._format_size(total_encyclopedia_size)}")
        
        self.size_statistics['encyclopedias'] = {
            'total_size': total_encyclopedia_size,
            'by_category': encyclopedia_analysis
        }
        
        return encyclopedia_analysis

    def calculate_storage_efficiency(self, file_analysis, encyclopedia_analysis):
        """Calculer l'efficacité globale de stockage"""
        print("\n⚡ CALCUL EFFICACITÉ STOCKAGE GLOBAL")
        print("=" * 60)
        
        # Données de base
        total_original = self.size_statistics['files']['total_original']
        total_panini_files = self.size_statistics['files']['total_panini']
        total_encyclopedias = self.size_statistics['encyclopedias']['total_size']
        
        # Calcul overhead encyclopédies par fichier
        num_files = len(file_analysis)
        encyclopedia_overhead_per_file = total_encyclopedias / num_files if num_files > 0 else 0
        
        # Efficacité avec et sans encyclopédies
        efficiency_without_encyclopedias = total_panini_files / total_original if total_original > 0 else 1
        efficiency_with_encyclopedias = (total_panini_files + total_encyclopedias) / total_original if total_original > 0 else 1
        
        # Analyse par seuil de taille
        size_thresholds = [1024, 10*1024, 100*1024, 1024*1024, 10*1024*1024]  # 1KB, 10KB, 100KB, 1MB, 10MB
        
        print("📊 EFFICACITÉ PAR TAILLE DE FICHIER:")
        print("   (inclut overhead encyclopédies réparti)")
        
        efficiency_by_size = []
        for threshold in size_thresholds:
            files_above = [a for a in file_analysis if a['original_size'] >= threshold]
            if files_above:
                total_orig = sum(a['original_size'] for a in files_above)
                total_panini = sum(a['total_panini_size'] for a in files_above)
                
                # Ajouter overhead encyclopédies proportionnel
                encyclopedia_overhead = encyclopedia_overhead_per_file * len(files_above)
                total_with_encyc = total_panini + encyclopedia_overhead
                
                efficiency = total_with_encyc / total_orig if total_orig > 0 else 1
                
                efficiency_by_size.append({
                    'threshold': threshold,
                    'files_count': len(files_above),
                    'efficiency': efficiency,
                    'viable': efficiency < 1.0
                })
                
                viability = "✅ VIABLE" if efficiency < 1.0 else "❌ NON-VIABLE"
                print(f"   Fichiers ≥ {self._format_size(threshold):>8} : {efficiency:.3f} ratio ({len(files_above):2} fichiers) {viability}")
        
        # Point de viabilité économique
        viable_threshold = None
        for analysis in efficiency_by_size:
            if analysis['viable']:
                viable_threshold = analysis['threshold']
                break
        
        if viable_threshold:
            print(f"\n🎯 SEUIL VIABILITÉ ÉCONOMIQUE: ≥ {self._format_size(viable_threshold)}")
        else:
            print(f"\n⚠️  AUCUN SEUIL VIABLE TROUVÉ - Optimisation nécessaire")
        
        # Recommandations d'optimisation
        print(f"\n💡 OPTIMISATIONS RECOMMANDÉES:")
        
        # 1. Overhead métadonnées
        avg_metadata_overhead = np.mean([a['metadata_overhead'] for a in file_analysis])
        if avg_metadata_overhead > 0.05:  # Plus de 5%
            print(f"   🔧 Réduire métadonnées: {avg_metadata_overhead:.1%} overhead actuel")
        
        # 2. Encyclopédies partagées
        if encyclopedia_overhead_per_file > 1024:  # Plus de 1KB par fichier
            print(f"   📚 Encyclopédies partagées: {self._format_size(encyclopedia_overhead_per_file)} overhead/fichier")
        
        # 3. Compression différentielle
        small_files = [a for a in file_analysis if a['original_size'] < 10*1024]
        if small_files:
            avg_small_ratio = np.mean([a['total_ratio'] for a in small_files])
            if avg_small_ratio > 1.0:
                print(f"   📦 Compression groupée petits fichiers: {len(small_files)} fichiers < 10KB")
        
        self.size_statistics['efficiency'] = {
            'without_encyclopedias': efficiency_without_encyclopedias,
            'with_encyclopedias': efficiency_with_encyclopedias,
            'encyclopedia_overhead_per_file': encyclopedia_overhead_per_file,
            'viable_threshold': viable_threshold,
            'by_size': efficiency_by_size
        }

    def generate_size_optimization_report(self):
        """Générer rapport d'optimisation des tailles"""
        print("\n📄 GÉNÉRATION RAPPORT OPTIMISATION TAILLES")
        print("=" * 60)
        
        report_filename = f"PANINI_SIZE_ANALYSIS_REPORT_{self.timestamp.replace(':', '-')}.md"
        
        # Statistiques clés
        files_stats = self.size_statistics['files']
        encyc_stats = self.size_statistics['encyclopedias']
        efficiency_stats = self.size_statistics['efficiency']
        
        report_content = f"""# 📏 PANINI-FS SIZE ANALYSIS REPORT

## 📊 Vue d'ensemble

**Session d'analyse:** {self.timestamp}  
**Fichiers analysés:** {files_stats['total_files']}  
**Données totales:** {self._format_size(files_stats['total_original'])}

## 🗜️ Analyse fichiers compressés

**Tailles globales:**
- Original: {self._format_size(files_stats['total_original'])}
- Compressé: {self._format_size(files_stats['total_compressed'])}
- Métadonnées: {self._format_size(files_stats['total_metadata'])}
- **Total PaniniFS: {self._format_size(files_stats['total_panini'])}**

**Ratios:**
- Compression seule: {files_stats['global_compression_ratio']:.3f}
- **Overhead métadonnées: {files_stats['global_metadata_overhead']:.3f} ({(files_stats['global_metadata_overhead']*100):.1f}%)**
- **Ratio PaniniFS total: {files_stats['global_total_ratio']:.3f}**

## 📚 Analyse encyclopédies

**Taille totale encyclopédies:** {self._format_size(encyc_stats['total_size'])}  
**Overhead par fichier:** {self._format_size(efficiency_stats['encyclopedia_overhead_per_file'])}

"""

        # Ajouter détails par catégorie
        for category, data in encyc_stats['by_category'].items():
            report_content += f"- **{category}**: {self._format_size(data['size'])}\n"
        
        report_content += f"""

## ⚡ Efficacité stockage

**Sans encyclopédies:** {efficiency_stats['without_encyclopedias']:.3f}  
**Avec encyclopédies:** {efficiency_stats['with_encyclopedias']:.3f}

"""
        
        if efficiency_stats['viable_threshold']:
            report_content += f"**🎯 Seuil viabilité économique:** ≥ {self._format_size(efficiency_stats['viable_threshold'])}\n\n"
        else:
            report_content += "**⚠️ Aucun seuil viable identifié**\n\n"
        
        # Efficacité par taille
        report_content += "**Efficacité par taille de fichier:**\n"
        for analysis in efficiency_stats['by_size']:
            viability = "✅" if analysis['viable'] else "❌"
            report_content += f"- Fichiers ≥ {self._format_size(analysis['threshold'])}: {analysis['efficiency']:.3f} ({analysis['files_count']} fichiers) {viability}\n"
        
        report_content += f"""

## 💡 Recommandations d'optimisation

### Réduction overhead métadonnées
- Overhead actuel: {files_stats['global_metadata_overhead']:.1%}
- Optimisation possible: Compression métadonnées, format binaire

### Optimisation encyclopédies  
- Taille actuelle: {self._format_size(encyc_stats['total_size'])}
- Stratégie: Encyclopédies partagées, compression différentielle

### Seuils de viabilité
- Recommandation: Utiliser PaniniFS pour fichiers ≥ {self._format_size(efficiency_stats['viable_threshold']) if efficiency_stats['viable_threshold'] else '1MB'}
- Alternative: Compression groupée pour petits fichiers

---

*Rapport généré par PaniniFS Size Analysis Engine*  
*Basé sur analyse de {files_stats['total_files']} fichiers réels*
"""
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Rapport sauvegardé: {report_filename}")
        
        # Sauvegarder données JSON
        data_filename = f"PANINI_SIZE_ANALYSIS_DATA_{self.timestamp.replace(':', '-')}.json"
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump(self.size_statistics, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Données sauvegardées: {data_filename}")
        
        return report_filename, data_filename

    def _format_size(self, size_bytes):
        """Formater taille en unités lisibles"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def run_complete_size_analysis(self):
        """Exécuter l'analyse complète des tailles"""
        print(f"""
🚀 DÉMARRAGE ANALYSE COMPLÈTE TAILLES PANINI-FS
============================================================
🎯 Mission: Analyser efficacité stockage système complet
📊 Analyses: Fichiers + Métadonnées + Encyclopédies + Efficacité
⚡ Objectif: Optimiser overhead et valider viabilité économique

🔍 Phase 1: Analyse fichiers compressés...
""")
        
        try:
            # Phase 1: Analyser fichiers compressés
            file_analysis = self.analyze_compressed_files_sizes()
            
            if not file_analysis:
                print("❌ Aucun fichier compressé trouvé pour analyse")
                return False
            
            # Phase 2: Analyser overhead métadonnées
            self.analyze_metadata_overhead(file_analysis)
            
            # Phase 3: Analyser encyclopédies
            encyclopedia_analysis = self.analyze_encyclopedia_sizes()
            
            # Phase 4: Calculer efficacité globale
            self.calculate_storage_efficiency(file_analysis, encyclopedia_analysis)
            
            # Phase 5: Générer rapport
            report_file, data_file = self.generate_size_optimization_report()
            
            # Résumé final
            total_original = self.size_statistics['files']['total_original']
            total_panini = self.size_statistics['files']['total_panini']
            total_with_encyc = total_panini + self.size_statistics['encyclopedias']['total_size']
            
            final_efficiency = total_with_encyc / total_original if total_original > 0 else 1
            
            print(f"""
🎉 ANALYSE TAILLES TERMINÉE AVEC SUCCÈS !
============================================================
📊 Résultats clés:
   Données originales      : {self._format_size(total_original)}
   PaniniFS (fichiers)     : {self._format_size(total_panini)}
   Encyclopédies           : {self._format_size(self.size_statistics['encyclopedias']['total_size'])}
   **TOTAL SYSTÈME**       : {self._format_size(total_with_encyc)}
   
🎯 Efficacité finale       : {final_efficiency:.3f}
   Économie/Overhead       : {((1-final_efficiency)*100):+.1f}%
   
📄 Rapport détaillé       : {report_file}
💾 Données complètes      : {data_file}

🚀 ANALYSE PRÊTE POUR OPTIMISATIONS !
""")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur dans analyse tailles: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Point d'entrée principal"""
    print(f"""
📏 PANINI-FS SIZE ANALYSIS ENGINE
============================================================
🎯 Mission: Analyser tailles représentations et encyclopédies
📊 Objectif: Mesurer overhead et optimiser efficacité stockage

Analyses complètes:
- Tailles fichiers compressés vs originaux
- Overhead métadonnées détaillé
- Tailles encyclopédies de connaissances  
- Efficacité stockage globale
- Seuils viabilité économique
- Recommandations optimisation

🚀 Initialisation moteur d'analyse...
""")
    
    try:
        engine = PaniniSizeAnalysisEngine()
        success = engine.run_complete_size_analysis()
        
        if success:
            print(f"""
✅ MISSION ANALYSE TAILLES ACCOMPLIE
==================================
📊 Analyse complète réalisée avec succès
🎯 Overhead système quantifié précisément  
💡 Optimisations identifiées et documentées
📄 Rapport détaillé généré

🚀 Prêt pour phase d'optimisation !
""")
            return True
        else:
            print("❌ Échec analyse tailles")
            return False
    
    except Exception as e:
        print(f"""
❌ ERREUR ANALYSE TAILLES
========================
🔧 Erreur: {str(e)}
""")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
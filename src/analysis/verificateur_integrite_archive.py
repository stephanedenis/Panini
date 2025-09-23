#!/usr/bin/env python3
"""
Vérificateur Intégrité Archive PaniniFS
Validation complète pour reproductibilité tiers
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

class VerificateurIntegriteArchive:
    def __init__(self):
        self.references_dir = Path("/home/stephane/GitHub/PaniniFS-Research/panini/references")
        self.cache_dir = self.references_dir / "cache"
        self.db_file = self.references_dir / "references_database.json"
        
        self.results = {
            'total_references': 0,
            'cached_files_count': 0,
            'missing_files': [],
            'invalid_references': [],
            'integrity_score': 0,
            'validation_details': {}
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        print(f"{timestamp} {level}: {message}")
        
    def verify_archive_structure(self):
        """Vérifie structure de base de l'archive"""
        self.log("🔍 Vérification structure archive...")
        
        required_files = [
            self.db_file,
            self.references_dir / "sources_index.json",
            self.references_dir / "archivage_summary.txt"
        ]
        
        missing = []
        for file_path in required_files:
            if not file_path.exists():
                missing.append(str(file_path))
                
        if missing:
            self.log(f"❌ Fichiers manquants: {missing}", "ERROR")
            return False
        else:
            self.log("✅ Structure archive valide")
            return True
            
    def verify_references_database(self):
        """Vérifie intégrité base de données références"""
        self.log("📚 Vérification base données références...")
        
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                db = json.load(f)
                
            self.results['total_references'] = len(db.get('references', []))
            
            # Vérifications structure
            required_fields = ['creation_date', 'total_references', 'references']
            for field in required_fields:
                if field not in db:
                    self.log(f"❌ Champ manquant dans DB: {field}", "ERROR")
                    return False
                    
            # Vérification cohérence
            if db['total_references'] != len(db['references']):
                self.log("❌ Incohérence compte références", "ERROR")
                return False
                
            self.log(f"✅ Base références valide: {self.results['total_references']} entrées")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur lecture DB: {e}", "ERROR")
            return False
            
    def verify_cached_content(self):
        """Vérifie contenu caché"""
        self.log("💾 Vérification contenu caché...")
        
        if not self.cache_dir.exists():
            self.log("❌ Répertoire cache manquant", "ERROR")
            return False
            
        cached_files = list(self.cache_dir.glob("*"))
        self.results['cached_files_count'] = len(cached_files)
        
        self.log(f"📁 Fichiers dans cache: {len(cached_files)}")
        
        # Vérification types fichiers
        pdf_count = len(list(self.cache_dir.glob("*.pdf")))
        html_count = len(list(self.cache_dir.glob("*.html")))
        
        self.results['validation_details']['pdf_files'] = pdf_count
        self.results['validation_details']['html_files'] = html_count
        
        self.log(f"📄 PDFs: {pdf_count}, HTMLs: {html_count}")
        
        return True
        
    def verify_reference_integrity(self):
        """Vérifie intégrité de chaque référence"""
        self.log("🔍 Vérification intégrité références...")
        
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                db = json.load(f)
                
            total_refs = len(db['references'])
            cached_claimed = 0
            cached_verified = 0
            missing_files = []
            invalid_refs = []
            
            for ref in db['references']:
                # Vérification champs obligatoires
                required_fields = [
                    'reference_id', 'bibliographic_info', 
                    'cached_content', 'urls'
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in ref:
                        missing_fields.append(field)
                        
                if missing_fields:
                    invalid_refs.append({
                        'id': ref.get('reference_id', 'unknown'),
                        'missing_fields': missing_fields
                    })
                    continue
                    
                # Vérification contenu caché
                if ref['cached_content']['has_cached_content']:
                    cached_claimed += 1
                    
                    cached_file = ref['cached_content']['cached_file']
                    if cached_file and Path(cached_file).exists():
                        cached_verified += 1
                    else:
                        missing_files.append({
                            'ref_id': ref['reference_id'],
                            'file': cached_file
                        })
                        
            self.results['missing_files'] = missing_files
            self.results['invalid_references'] = invalid_refs
            
            self.log(f"📊 Références avec contenu déclaré: {cached_claimed}")
            self.log(f"✅ Contenu vérifié existant: {cached_verified}")
            self.log(f"❌ Fichiers manquants: {len(missing_files)}")
            self.log(f"⚠️  Références invalides: {len(invalid_refs)}")
            
            return len(missing_files) == 0 and len(invalid_refs) == 0
            
        except Exception as e:
            self.log(f"❌ Erreur vérification intégrité: {e}", "ERROR")
            return False
            
    def calculate_integrity_score(self):
        """Calcule score d'intégrité global"""
        total_refs = self.results['total_references']
        cached_files = self.results['cached_files_count']
        missing_files = len(self.results['missing_files'])
        invalid_refs = len(self.results['invalid_references'])
        
        if total_refs == 0:
            score = 0
        else:
            # Score basé sur complétude et validité
            completeness = (cached_files - missing_files) / total_refs
            validity = (total_refs - invalid_refs) / total_refs
            score = (completeness + validity) / 2 * 100
            
        self.results['integrity_score'] = round(score, 1)
        return score
        
    def generate_verification_report(self):
        """Génère rapport de vérification"""
        report_file = self.references_dir / "verification_report.json"
        
        # Ajout métadonnées verification
        self.results.update({
            'verification_date': datetime.now().isoformat(),
            'verification_version': '1.0',
            'archive_location': str(self.references_dir),
            'total_cache_size_mb': sum(
                f.stat().st_size for f in self.cache_dir.glob("*") 
                if f.is_file()
            ) / (1024 * 1024) if self.cache_dir.exists() else 0
        })
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        # Rapport texte
        text_report = self.references_dir / "verification_summary.txt"
        with open(text_report, 'w', encoding='utf-8') as f:
            f.write("RAPPORT VÉRIFICATION INTÉGRITÉ ARCHIVE PANINI\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Date vérification: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Score intégrité: {self.results['integrity_score']}%\n\n")
            
            f.write("📊 STATISTIQUES:\n")
            f.write(f"  Total références: {self.results['total_references']}\n")
            f.write(f"  Fichiers cachés: {self.results['cached_files_count']}\n")
            f.write(f"  Fichiers manquants: {len(self.results['missing_files'])}\n")
            f.write(f"  Références invalides: {len(self.results['invalid_references'])}\n")
            
            if self.results['validation_details']:
                f.write(f"  PDFs: {self.results['validation_details'].get('pdf_files', 0)}\n")
                f.write(f"  HTMLs: {self.results['validation_details'].get('html_files', 0)}\n")
                
            f.write(f"  Taille cache: {self.results['total_cache_size_mb']:.1f} MB\n\n")
            
            if self.results['missing_files']:
                f.write("❌ FICHIERS MANQUANTS:\n")
                for missing in self.results['missing_files'][:10]:
                    f.write(f"  {missing['ref_id']}: {missing['file']}\n")
                    
            if self.results['invalid_references']:
                f.write("\n⚠️  RÉFÉRENCES INVALIDES:\n")
                for invalid in self.results['invalid_references'][:10]:
                    f.write(f"  {invalid['id']}: {invalid['missing_fields']}\n")
                    
            f.write("\n✅ VALIDATION REPRODUCTIBILITÉ:\n")
            if self.results['integrity_score'] >= 95:
                f.write("  🟢 EXCELLENT - Archive complètement reproductible\n")
            elif self.results['integrity_score'] >= 85:
                f.write("  🟡 BON - Archive reproductible avec alertes mineures\n")
            else:
                f.write("  🔴 ATTENTION - Problèmes intégrité détectés\n")
                
        self.log(f"📄 Rapport généré: {report_file}")
        self.log(f"📋 Résumé: {text_report}")
        
    def run_complete_verification(self):
        """Exécute vérification complète"""
        self.log("🔍 DÉMARRAGE VÉRIFICATION INTÉGRITÉ ARCHIVE")
        self.log("=" * 60)
        
        checks = [
            ("Structure", self.verify_archive_structure),
            ("Base données", self.verify_references_database),
            ("Contenu caché", self.verify_cached_content),
            ("Intégrité références", self.verify_reference_integrity)
        ]
        
        passed = 0
        for check_name, check_func in checks:
            self.log(f"🔄 {check_name}...")
            if check_func():
                passed += 1
                self.log(f"✅ {check_name} validé")
            else:
                self.log(f"❌ {check_name} échoué", "ERROR")
                
        # Score final
        integrity_score = self.calculate_integrity_score()
        
        # Rapport
        self.generate_verification_report()
        
        self.log("=" * 60)
        self.log("🏆 VÉRIFICATION INTÉGRITÉ TERMINÉE")
        self.log(f"📊 Checks passés: {passed}/{len(checks)}")
        self.log(f"🎯 Score intégrité: {integrity_score}%")
        
        if integrity_score >= 95:
            self.log("✅ Archive PARFAITEMENT reproductible")
        elif integrity_score >= 85:
            self.log("⚠️  Archive reproductible avec alertes mineures")
        else:
            self.log("❌ Problèmes intégrité - vérification manuelle requise")
            
        return integrity_score >= 85

def main():
    verificateur = VerificateurIntegriteArchive()
    verificateur.run_complete_verification()

if __name__ == "__main__":
    main()
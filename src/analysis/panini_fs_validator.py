#!/usr/bin/env python3
"""
Validateur PaniniFS - Framework Validation Multi-Format
Validation exhaustive ingestion/restitution avec intégrité 100%
ISO 8601 compliant timestamp format
"""

import hashlib
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional


class IntegrityError(Exception):
    """Exception levée quand l'intégrité n'est pas 100%"""
    pass


class PaniniFSValidator:
    """
    Framework de validation exhaustif pour PaniniFS
    Support multi-format avec garantie d'intégrité bit-à-bit
    """
    
    def __init__(self, workspace: Optional[Path] = None):
        """
        Initialise le validateur PaniniFS
        
        Args:
            workspace: Répertoire de travail (défaut: répertoire courant)
        """
        self.workspace = workspace or Path.cwd() / 'panini_fs_validation'
        self.workspace.mkdir(exist_ok=True, parents=True)
        
        # Répertoires de travail
        self.ingestion_dir = self.workspace / 'ingestion'
        self.compressed_dir = self.workspace / 'compressed'
        self.restitution_dir = self.workspace / 'restitution'
        self.reports_dir = self.workspace / 'reports'
        
        for directory in [self.ingestion_dir, self.compressed_dir, 
                         self.restitution_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True, parents=True)
        
        # Formats supportés par catégorie
        self.supported_formats = {
            'text': ['pdf', 'txt', 'epub', 'docx', 'md'],
            'audio': ['mp3', 'wav', 'flac', 'ogg'],
            'video': ['mp4', 'mkv', 'avi', 'webm'],
            'image': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']
        }
        
        # Métriques de validation
        self.validation_metrics = {
            'total_files': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'success_rate': 0.0,  # Taux de réussite (nb_succès / nb_total)
            'by_format': {},
            'performance_metrics': {}
        }
        
        self.log("🚀 Validateur PaniniFS initialisé")
        self.log(f"📁 Workspace: {self.workspace}")
    
    def log(self, message: str, level: str = "INFO"):
        """
        Logging avec timestamp ISO 8601 UTC
        
        Args:
            message: Message à logger
            level: Niveau de log (INFO, WARNING, ERROR, SUCCESS)
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        prefix = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅"
        }.get(level, "ℹ️")
        print(f"[{timestamp}] {prefix} {message}")
    
    def compute_file_hash(self, file_path: Path, algorithm: str = 'sha256') -> str:
        """
        Calcule le hash d'un fichier pour vérification d'intégrité
        
        Args:
            file_path: Chemin du fichier
            algorithm: Algorithme de hash (sha256, md5, sha512)
            
        Returns:
            Hash hexadécimal du fichier
        """
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            # Lecture par blocs pour fichiers volumineux
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def detect_format(self, file_path: Path) -> Tuple[str, str]:
        """
        Détecte le format et la catégorie d'un fichier
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Tuple (catégorie, format)
        """
        extension = file_path.suffix.lower().lstrip('.')
        
        for category, formats in self.supported_formats.items():
            if extension in formats:
                return category, extension
        
        return 'unknown', extension
    
    def validate_file_integrity(
        self,
        original_path: Path,
        restored_path: Path
    ) -> bool:
        """
        Valide l'intégrité bit-à-bit entre fichier original et restitué
        INTÉGRITÉ 100% OU ÉCHEC - pas de zone grise
        
        Args:
            original_path: Chemin du fichier original
            restored_path: Chemin du fichier restitué
            
        Returns:
            True si intégrité 100%, sinon lève IntegrityError
            
        Raises:
            IntegrityError: Si intégrité n'est pas 100%
            FileNotFoundError: Si un fichier est introuvable
        """
        start_time = time.time()
        
        # Vérification existence fichiers
        if not original_path.exists():
            raise FileNotFoundError(f'Fichier original introuvable: {original_path}')
        
        if not restored_path.exists():
            raise FileNotFoundError(f'Fichier restitué introuvable: {restored_path}')
        
        # Calcul des hashes
        original_hash = self.compute_file_hash(original_path)
        restored_hash = self.compute_file_hash(restored_path)
        
        # Comparaison tailles
        original_size = original_path.stat().st_size
        restored_size = restored_path.stat().st_size
        
        elapsed_time = time.time() - start_time
        
        # Validation bit-à-bit: 100% ou ÉCHEC
        if original_hash != restored_hash:
            raise IntegrityError(
                f"Reconstitution incomplète - Hash mismatch: "
                f"original={original_hash} != restored={restored_hash}. "
                f"Fichier inutilisable."
            )
        
        if original_size != restored_size:
            raise IntegrityError(
                f"Reconstitution incomplète - Size mismatch: "
                f"original={original_size} != restored={restored_size} bytes. "
                f"Fichier inutilisable."
            )
        
        # Si on arrive ici, intégrité 100%
        self.log(f"✅ Intégrité 100% validée: {original_path.name}", "SUCCESS")
        return True
    
    def validate_format_pipeline(
        self,
        file_path: Path,
        compression_callback=None,
        decompression_callback=None
    ) -> Dict[str, Any]:
        """
        Pipeline complet de validation pour un fichier
        Ingestion → Compression → Décompression → Restitution → Validation
        
        Args:
            file_path: Fichier à valider
            compression_callback: Fonction de compression personnalisée
            decompression_callback: Fonction de décompression personnalisée
            
        Returns:
            Résultat complet de validation
        """
        self.log(f"🔄 Démarrage pipeline validation: {file_path.name}")
        
        category, format_type = self.detect_format(file_path)
        
        if category == 'unknown':
            self.log(f"⚠️ Format non supporté: {format_type}", "WARNING")
        
        # Phase 1: Ingestion
        original_hash = self.compute_file_hash(file_path)
        original_size = file_path.stat().st_size
        
        self.log(f"📥 Ingestion: {file_path.name} ({original_size} bytes)")
        
        # Phase 2: Compression (simulation si pas de callback)
        compressed_path = self.compressed_dir / f"{file_path.stem}.panini"
        compression_start = time.time()
        
        if compression_callback:
            compressed_data = compression_callback(file_path)
            with open(compressed_path, 'wb') as f:
                f.write(compressed_data)
        else:
            # Simulation: copie directe pour tests
            import shutil
            shutil.copy2(file_path, compressed_path)
        
        compression_time = time.time() - compression_start
        compressed_size = compressed_path.stat().st_size
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 1.0
        
        self.log(f"🗜️  Compression: {compressed_size} bytes (ratio: {compression_ratio:.2f}x)")
        
        # Phase 3: Décompression
        restored_path = self.restitution_dir / file_path.name
        decompression_start = time.time()
        
        if decompression_callback:
            decompressed_data = decompression_callback(compressed_path)
            with open(restored_path, 'wb') as f:
                f.write(decompressed_data)
        else:
            # Simulation: copie directe pour tests
            import shutil
            shutil.copy2(compressed_path, restored_path)
        
        decompression_time = time.time() - decompression_start
        
        self.log(f"📤 Restitution: {restored_path.name}")
        
        # Phase 4: Validation intégrité (100% ou ÉCHEC)
        try:
            integrity_valid = self.validate_file_integrity(file_path, restored_path)
            integrity_status = 'SUCCESS'
        except (IntegrityError, FileNotFoundError) as e:
            self.log(f"❌ ÉCHEC intégrité: {str(e)}", "ERROR")
            integrity_valid = False
            integrity_status = 'FAILED'
        
        # Résultat complet
        result = {
            'file_name': file_path.name,
            'category': category,
            'format': format_type,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'compression_time': compression_time,
            'decompression_time': decompression_time,
            'total_time': compression_time + decompression_time,
            'integrity_valid': integrity_valid,  # bool: True (100%) ou False (échec)
            'integrity_status': integrity_status,  # 'SUCCESS' ou 'FAILED'
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Mise à jour métriques
        self.validation_metrics['total_files'] += 1
        if integrity_valid:
            self.validation_metrics['successful_validations'] += 1
        else:
            self.validation_metrics['failed_validations'] += 1
        
        # Métriques par format
        if format_type not in self.validation_metrics['by_format']:
            self.validation_metrics['by_format'][format_type] = {
                'total': 0,
                'success': 0,
                'failed': 0
            }
        
        self.validation_metrics['by_format'][format_type]['total'] += 1
        if integrity_valid:
            self.validation_metrics['by_format'][format_type]['success'] += 1
        else:
            self.validation_metrics['by_format'][format_type]['failed'] += 1
        
        return result
    
    def validate_corpus(
        self,
        corpus_dir: Path,
        compression_callback=None,
        decompression_callback=None
    ) -> Dict[str, Any]:
        """
        Valide un corpus complet de fichiers multi-format
        
        Args:
            corpus_dir: Répertoire contenant les fichiers à valider
            compression_callback: Fonction de compression
            decompression_callback: Fonction de décompression
            
        Returns:
            Rapport de validation du corpus
        """
        self.log("=" * 60)
        self.log("🧪 VALIDATION CORPUS MULTI-FORMAT")
        self.log("=" * 60)
        
        if not corpus_dir.exists():
            self.log(f"❌ Corpus introuvable: {corpus_dir}", "ERROR")
            return {'error': f'Corpus directory not found: {corpus_dir}'}
        
        # Collecte fichiers par catégorie
        files_by_category = {
            'text': [],
            'audio': [],
            'video': [],
            'image': [],
            'unknown': []
        }
        
        for file_path in corpus_dir.rglob('*'):
            if file_path.is_file():
                category, _ = self.detect_format(file_path)
                files_by_category[category].append(file_path)
        
        self.log(f"📊 Fichiers détectés:")
        for category, files in files_by_category.items():
            if files:
                self.log(f"   {category.upper()}: {len(files)} fichiers")
        
        # Validation de tous les fichiers
        validation_results = []
        
        for category, files in files_by_category.items():
            if category == 'unknown':
                continue
            
            for file_path in files:
                try:
                    result = self.validate_format_pipeline(
                        file_path,
                        compression_callback,
                        decompression_callback
                    )
                    validation_results.append(result)
                except Exception as e:
                    self.log(f"❌ Erreur validation {file_path.name}: {e}", "ERROR")
                    validation_results.append({
                        'file_name': file_path.name,
                        'error': str(e),
                        'success': False
                    })
        
        # Calcul taux de réussite (nb_succès / nb_total)
        if self.validation_metrics['total_files'] > 0:
            self.validation_metrics['success_rate'] = (
                self.validation_metrics['successful_validations'] /
                self.validation_metrics['total_files']
            )
        
        # Génération rapport
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'corpus_path': str(corpus_dir),
            'metrics': self.validation_metrics,
            'validation_results': validation_results
        }
        
        # Sauvegarde rapport
        report_file = self.reports_dir / f"validation_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log("=" * 60)
        self.log("📈 RÉSULTATS VALIDATION")
        self.log("=" * 60)
        self.log(f"Total fichiers: {self.validation_metrics['total_files']}")
        self.log(f"Validations réussies: {self.validation_metrics['successful_validations']}")
        self.log(f"Validations échouées: {self.validation_metrics['failed_validations']}")
        self.log(f"Taux de réussite: {self.validation_metrics['success_rate']*100:.2f}%")
        self.log(f"📄 Rapport sauvegardé: {report_file}")
        
        return report
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé des métriques de validation
        
        Returns:
            Métriques de validation
        """
        return self.validation_metrics.copy()
    
    def generate_performance_benchmark(
        self,
        test_files: List[Path]
    ) -> Dict[str, Any]:
        """
        Génère un benchmark de performance pour comparaison ext4/NTFS
        
        Args:
            test_files: Liste de fichiers de test
            
        Returns:
            Résultats de benchmark
        """
        self.log("🏁 Génération benchmark performance")
        
        benchmark_results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'test_files_count': len(test_files),
            'total_size': sum(f.stat().st_size for f in test_files if f.exists()),
            'performance_by_format': {},
            'overall_metrics': {
                'avg_compression_time': 0.0,
                'avg_decompression_time': 0.0,
                'avg_compression_ratio': 0.0,
                'avg_throughput_mbps': 0.0
            }
        }
        
        total_compression_time = 0.0
        total_decompression_time = 0.0
        total_compression_ratio = 0.0
        
        for file_path in test_files:
            if not file_path.exists():
                continue
            
            result = self.validate_format_pipeline(file_path)
            
            format_type = result['format']
            if format_type not in benchmark_results['performance_by_format']:
                benchmark_results['performance_by_format'][format_type] = {
                    'count': 0,
                    'avg_compression_time': 0.0,
                    'avg_decompression_time': 0.0,
                    'avg_compression_ratio': 0.0
                }
            
            fmt_metrics = benchmark_results['performance_by_format'][format_type]
            fmt_metrics['count'] += 1
            fmt_metrics['avg_compression_time'] += result['compression_time']
            fmt_metrics['avg_decompression_time'] += result['decompression_time']
            fmt_metrics['avg_compression_ratio'] += result['compression_ratio']
            
            total_compression_time += result['compression_time']
            total_decompression_time += result['decompression_time']
            total_compression_ratio += result['compression_ratio']
        
        # Calcul moyennes
        if len(test_files) > 0:
            benchmark_results['overall_metrics']['avg_compression_time'] = (
                total_compression_time / len(test_files)
            )
            benchmark_results['overall_metrics']['avg_decompression_time'] = (
                total_decompression_time / len(test_files)
            )
            benchmark_results['overall_metrics']['avg_compression_ratio'] = (
                total_compression_ratio / len(test_files)
            )
            
            total_time = total_compression_time + total_decompression_time
            if total_time > 0:
                total_mb = benchmark_results['total_size'] / (1024 * 1024)
                benchmark_results['overall_metrics']['avg_throughput_mbps'] = (
                    total_mb / total_time
                )
        
        # Moyennes par format
        for format_type, metrics in benchmark_results['performance_by_format'].items():
            if metrics['count'] > 0:
                metrics['avg_compression_time'] /= metrics['count']
                metrics['avg_decompression_time'] /= metrics['count']
                metrics['avg_compression_ratio'] /= metrics['count']
        
        # Sauvegarde benchmark
        benchmark_file = self.reports_dir / f"benchmark_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(benchmark_file, 'w', encoding='utf-8') as f:
            json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
        
        self.log(f"📊 Benchmark sauvegardé: {benchmark_file}")
        
        return benchmark_results


def main():
    """Fonction principale de démonstration"""
    print("🧬 VALIDATEUR PANINI FS")
    print("=" * 60)
    print("Framework validation multi-format avec intégrité 100%")
    print("=" * 60)
    
    # Initialisation validateur
    validator = PaniniFSValidator()
    
    # Affichage formats supportés
    print("\n📋 Formats supportés:")
    for category, formats in validator.supported_formats.items():
        print(f"   {category.upper()}: {', '.join(formats)}")
    
    print(f"\n✅ Validateur prêt")
    print(f"📁 Workspace: {validator.workspace}")
    print("\nUtilisez la classe PaniniFSValidator pour valider vos fichiers")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Integrity Checker - PaniniFS
Vérification intégrité bit-à-bit avec garantie 100%
ISO 8601 compliant
"""

import hashlib
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional


class IntegrityError(Exception):
    """Exception levée quand l'intégrité n'est pas 100%"""
    pass


class IntegrityChecker:
    """
    Vérificateur d'intégrité pour PaniniFS
    Garantie intégrité 100% via comparaison bit-à-bit
    """
    
    def __init__(self):
        """Initialise le vérificateur d'intégrité"""
        self.hash_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        self.default_algorithm = 'sha256'
        
        # Métriques de vérification
        self.verification_stats = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'total_bytes_verified': 0,
            'verification_time': 0.0
        }
        
        self.log("🔒 Vérificateur d'intégrité initialisé")
    
    def log(self, message: str, level: str = "INFO"):
        """Logging avec timestamp ISO 8601 UTC"""
        timestamp = datetime.now(timezone.utc).isoformat()
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }.get(level, "ℹ️")
        print(f"[{timestamp}] {prefix} {message}")
    
    def compute_hash(
        self,
        file_path: Path,
        algorithm: str = None,
        block_size: int = 65536
    ) -> str:
        """
        Calcule le hash d'un fichier
        
        Args:
            file_path: Chemin du fichier
            algorithm: Algorithme de hash (défaut: sha256)
            block_size: Taille des blocs de lecture (défaut: 64KB)
            
        Returns:
            Hash hexadécimal du fichier
        """
        if algorithm is None:
            algorithm = self.default_algorithm
        
        if algorithm not in self.hash_algorithms:
            raise ValueError(f"Algorithme non supporté: {algorithm}")
        
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(block_size)
                if not chunk:
                    break
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def compute_multiple_hashes(
        self,
        file_path: Path,
        algorithms: List[str] = None
    ) -> Dict[str, str]:
        """
        Calcule plusieurs hashes pour un fichier
        
        Args:
            file_path: Chemin du fichier
            algorithms: Liste d'algorithmes (défaut: tous)
            
        Returns:
            Dictionnaire {algorithme: hash}
        """
        if algorithms is None:
            algorithms = self.hash_algorithms
        
        hashes = {}
        
        # Lecture fichier une seule fois pour tous les algorithmes
        hash_funcs = {alg: getattr(hashlib, alg)() for alg in algorithms}
        
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                for hash_func in hash_funcs.values():
                    hash_func.update(chunk)
        
        for alg, hash_func in hash_funcs.items():
            hashes[alg] = hash_func.hexdigest()
        
        return hashes
    
    def verify_file_integrity(
        self,
        original_path: Path,
        restored_path: Path,
        algorithm: str = None,
        verbose: bool = True
    ) -> bool:
        """
        Vérifie l'intégrité entre deux fichiers
        INTÉGRITÉ 100% OU ÉCHEC - pas de zone grise
        
        Args:
            original_path: Fichier original
            restored_path: Fichier restitué
            algorithm: Algorithme de hash
            verbose: Afficher les logs
            
        Returns:
            True si intégrité 100%
            
        Raises:
            IntegrityError: Si intégrité n'est pas 100%
            FileNotFoundError: Si un fichier est introuvable
        """
        start_time = time.time()
        
        if algorithm is None:
            algorithm = self.default_algorithm
        
        # Vérification existence
        if not original_path.exists():
            raise FileNotFoundError(f'Fichier original introuvable: {original_path}')
        
        if not restored_path.exists():
            raise FileNotFoundError(f'Fichier restitué introuvable: {restored_path}')
        
        # Métadonnées fichiers
        original_size = original_path.stat().st_size
        restored_size = restored_path.stat().st_size
        
        # Calcul hashes
        if verbose:
            self.log(f"🔍 Vérification: {original_path.name}")
            self.log(f"   Algorithme: {algorithm}")
        
        original_hash = self.compute_hash(original_path, algorithm)
        restored_hash = self.compute_hash(restored_path, algorithm)
        
        verification_time = time.time() - start_time
        
        # Mise à jour statistiques
        self.verification_stats['total_checks'] += 1
        self.verification_stats['total_bytes_verified'] += original_size
        self.verification_stats['verification_time'] += verification_time
        
        # Validation: 100% ou ÉCHEC
        if original_hash != restored_hash:
            self.verification_stats['failed_checks'] += 1
            if verbose:
                self.log(f"❌ ÉCHEC intégrité: {original_path.name}", "ERROR")
                self.log(f"   Original:  {original_hash}", "ERROR")
                self.log(f"   Restored:  {restored_hash}", "ERROR")
            raise IntegrityError(
                f"Reconstitution incomplète - Hash mismatch. Fichier inutilisable."
            )
        
        if original_size != restored_size:
            self.verification_stats['failed_checks'] += 1
            if verbose:
                self.log(f"❌ ÉCHEC intégrité: {original_path.name}", "ERROR")
                self.log(f"   Size mismatch: {original_size} != {restored_size}", "ERROR")
            raise IntegrityError(
                f"Reconstitution incomplète - Size mismatch. Fichier inutilisable."
            )
        
        # Intégrité 100%
        self.verification_stats['successful_checks'] += 1
        if verbose:
            self.log(f"✅ Intégrité 100% validée: {original_path.name}", "SUCCESS")
        
        return True
    
    def verify_batch(
        self,
        file_pairs: List[Tuple[Path, Path]],
        algorithm: str = None
    ) -> Dict[str, Any]:
        """
        Vérifie l'intégrité d'un lot de fichiers
        
        Args:
            file_pairs: Liste de tuples (original, restitué)
            algorithm: Algorithme de hash
            
        Returns:
            Résultats de vérification du lot
        """
        self.log("=" * 60)
        self.log("🔒 VÉRIFICATION LOT D'INTÉGRITÉ")
        self.log("=" * 60)
        self.log(f"Nombre de fichiers: {len(file_pairs)}")
        
        results = []
        
        for original, restored in file_pairs:
            try:
                integrity_valid = self.verify_file_integrity(
                    original,
                    restored,
                    algorithm,
                    verbose=False
                )
                results.append({
                    'original': str(original),
                    'restored': str(restored),
                    'success': integrity_valid,  # True (100%) ou False (échec)
                    'status': 'SUCCESS' if integrity_valid else 'FAILED'
                })
                
                # Log résumé
                status = "✅" if integrity_valid else "❌"
                self.log(f"{status} {original.name}")
                
            except (IntegrityError, FileNotFoundError) as e:
                self.log(f"❌ ÉCHEC: {original.name} - {e}", "ERROR")
                results.append({
                    'original': str(original),
                    'restored': str(restored),
                    'success': False,
                    'status': 'FAILED',
                    'error': str(e)
                })
        
        # Calcul statistiques du lot
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        success_rate = (successful / len(results) * 100) if results else 0
        
        batch_stats = {
            'total_files': len(file_pairs),
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        self.log("=" * 60)
        self.log("📊 RÉSULTATS")
        self.log("=" * 60)
        self.log(f"Total: {batch_stats['total_files']}")
        self.log(f"✅ Réussis: {batch_stats['successful']}")
        self.log(f"❌ Échoués: {batch_stats['failed']}")
        self.log(f"📈 Taux de réussite: {batch_stats['success_rate']:.2f}%")
        
        return {
            'statistics': batch_stats,
            'results': results
        }
    
    def verify_deep_integrity(
        self,
        original_path: Path,
        restored_path: Path
    ) -> Dict[str, Any]:
        """
        Vérification d'intégrité approfondie avec tous les algorithmes
        
        Args:
            original_path: Fichier original
            restored_path: Fichier restitué
            
        Returns:
            Résultat de vérification approfondie
        """
        self.log(f"🔬 Vérification approfondie: {original_path.name}")
        
        start_time = time.time()
        
        # Calcul de tous les hashes
        original_hashes = self.compute_multiple_hashes(original_path)
        restored_hashes = self.compute_multiple_hashes(restored_path)
        
        # Comparaison pour chaque algorithme
        hash_results = {}
        all_match = True
        
        for algorithm in self.hash_algorithms:
            match = original_hashes[algorithm] == restored_hashes[algorithm]
            hash_results[algorithm] = {
                'match': match,
                'original': original_hashes[algorithm],
                'restored': restored_hashes[algorithm]
            }
            
            if not match:
                all_match = False
                self.log(f"❌ {algorithm.upper()}: Mismatch", "ERROR")
            else:
                self.log(f"✅ {algorithm.upper()}: Match", "SUCCESS")
        
        # Comparaison bit-à-bit directe
        bit_by_bit_match = self._compare_files_bitwise(original_path, restored_path)
        
        verification_time = time.time() - start_time
        
        result = {
            'success': all_match and bit_by_bit_match,
            'hash_results': hash_results,
            'bit_by_bit_match': bit_by_bit_match,
            'verification_time': verification_time,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if result['success']:
            self.log(f"✅ Intégrité 100% garantie", "SUCCESS")
        else:
            self.log(f"❌ Échec vérification intégrité", "ERROR")
        
        return result
    
    def _compare_files_bitwise(
        self,
        file1: Path,
        file2: Path,
        block_size: int = 65536
    ) -> bool:
        """
        Compare deux fichiers bit-à-bit
        
        Args:
            file1: Premier fichier
            file2: Second fichier
            block_size: Taille des blocs de comparaison
            
        Returns:
            True si les fichiers sont identiques
        """
        # Vérification tailles
        if file1.stat().st_size != file2.stat().st_size:
            return False
        
        # Comparaison bloc par bloc
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            while True:
                chunk1 = f1.read(block_size)
                chunk2 = f2.read(block_size)
                
                if chunk1 != chunk2:
                    return False
                
                if not chunk1:  # EOF
                    break
        
        return True
    
    def generate_integrity_manifest(
        self,
        files: List[Path],
        output_path: Path,
        algorithm: str = None
    ):
        """
        Génère un manifeste d'intégrité pour un ensemble de fichiers
        
        Args:
            files: Liste de fichiers
            output_path: Chemin du manifeste
            algorithm: Algorithme de hash
        """
        if algorithm is None:
            algorithm = self.default_algorithm
        
        self.log(f"📋 Génération manifeste d'intégrité ({algorithm})")
        
        manifest = {
            'algorithm': algorithm,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_files': len(files),
            'files': []
        }
        
        for file_path in files:
            if not file_path.exists():
                self.log(f"⚠️ Fichier ignoré (introuvable): {file_path}", "WARNING")
                continue
            
            file_hash = self.compute_hash(file_path, algorithm)
            
            manifest['files'].append({
                'path': str(file_path),
                'name': file_path.name,
                'size': file_path.stat().st_size,
                'hash': file_hash,
                'modified': datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat()
            })
            
            self.log(f"✅ {file_path.name}: {file_hash}")
        
        # Sauvegarde manifeste
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Manifeste sauvegardé: {output_path}")
    
    def verify_against_manifest(
        self,
        manifest_path: Path,
        base_dir: Path = None
    ) -> Dict[str, Any]:
        """
        Vérifie des fichiers contre un manifeste d'intégrité
        
        Args:
            manifest_path: Chemin du manifeste
            base_dir: Répertoire de base pour les fichiers
            
        Returns:
            Résultats de vérification
        """
        self.log(f"🔍 Vérification contre manifeste: {manifest_path}")
        
        if not manifest_path.exists():
            return {'error': f'Manifeste introuvable: {manifest_path}'}
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        algorithm = manifest.get('algorithm', self.default_algorithm)
        results = []
        
        for file_entry in manifest['files']:
            file_path = Path(file_entry['path'])
            
            # Utiliser base_dir si fourni
            if base_dir:
                file_path = base_dir / file_path.name
            
            if not file_path.exists():
                results.append({
                    'file': str(file_path),
                    'success': False,
                    'error': 'File not found'
                })
                self.log(f"❌ {file_path.name}: Fichier introuvable", "ERROR")
                continue
            
            # Calcul hash actuel
            current_hash = self.compute_hash(file_path, algorithm)
            expected_hash = file_entry['hash']
            
            match = (current_hash == expected_hash)
            
            results.append({
                'file': str(file_path),
                'success': match,
                'expected_hash': expected_hash,
                'current_hash': current_hash
            })
            
            if match:
                self.log(f"✅ {file_path.name}: Hash validé", "SUCCESS")
            else:
                self.log(f"❌ {file_path.name}: Hash mismatch", "ERROR")
        
        # Statistiques
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        return {
            'manifest': str(manifest_path),
            'algorithm': algorithm,
            'total_files': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'results': results,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retourne les statistiques de vérification
        
        Returns:
            Statistiques cumulées
        """
        stats = self.verification_stats.copy()
        
        if stats['total_checks'] > 0:
            stats['success_rate'] = (
                stats['successful_checks'] / stats['total_checks'] * 100
            )
            stats['avg_verification_time'] = (
                stats['verification_time'] / stats['total_checks']
            )
        else:
            stats['success_rate'] = 0.0
            stats['avg_verification_time'] = 0.0
        
        return stats


def main():
    """Fonction principale de démonstration"""
    print("🔒 VÉRIFICATEUR D'INTÉGRITÉ - PANINI FS")
    print("=" * 60)
    
    checker = IntegrityChecker()
    
    print("\n✅ Vérificateur d'intégrité prêt")
    print("\n📋 Algorithmes supportés:")
    for algo in checker.hash_algorithms:
        print(f"   - {algo.upper()}")
    print(f"\n🔐 Algorithme par défaut: {checker.default_algorithm.upper()}")
    
    print("\nFonctionnalités:")
    print("  • Vérification bit-à-bit")
    print("  • Hash multiple (MD5, SHA1, SHA256, SHA512)")
    print("  • Vérification par lot")
    print("  • Manifestes d'intégrité")
    print("  • Garantie intégrité 100%")


if __name__ == '__main__':
    main()

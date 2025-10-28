#!/usr/bin/env python3
"""
Générateur de Corpus Test PaniniFS
=================================

Génère corpus diversifié pour validation exhaustive PaniniFS :
- Fichiers synthétiques multi-format
- Cas de test edge cases  
- Fichiers réels du projet
- Stress tests scalabilité

Support Issue #11 - Tests robustesse validateurs

Date: 2025-10-02
Auteur: Système Autonome PaniniFS  
Version: 1.0.0
"""

import os
import json
import random
import string
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple
import tempfile
import base64


class PaniniTestCorpusGenerator:
    """Générateur de corpus test pour validateurs PaniniFS"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path('test_corpus_panini')
        self.generated_files = []
        
    def setup_test_environment(self):
        """Configure environnement de test"""
        
        print(f"\n🧪 Configuration corpus test PaniniFS")
        print("=" * 45)
        
        # Créer structure dossiers
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / 'text').mkdir(exist_ok=True)
        (self.output_dir / 'audio').mkdir(exist_ok=True)
        (self.output_dir / 'video').mkdir(exist_ok=True)
        (self.output_dir / 'image').mkdir(exist_ok=True)
        (self.output_dir / 'binary').mkdir(exist_ok=True)
        (self.output_dir / 'edge_cases').mkdir(exist_ok=True)
        
        print(f"✅ Dossier corpus: {self.output_dir}")
        
    def generate_text_files(self) -> List[Path]:
        """Génère fichiers texte variés"""
        
        print("\n📝 Génération fichiers texte...")
        text_files = []
        
        # 1. Fichier TXT simple
        txt_content = "Ceci est un test PaniniFS.\nValidation intégrité multi-format.\n" * 100
        txt_file = self.output_dir / 'text' / 'test_simple.txt'
        txt_file.write_text(txt_content, encoding='utf-8')
        text_files.append(txt_file)
        print(f"✅ {txt_file.name}")
        
        # 2. Fichier Markdown avec formatage
        md_content = """# Test PaniniFS Validation
        
## Objectifs

- **Intégrité 100%** validation
- Support multi-format
- Scalabilité millions fichiers

### Code Example

```python
def panini_validate(file_path):
    return validate_integrity(file_path)
```

> Citation test pour PaniniFS

| Format | Support | Status |
|--------|---------|--------|
| TXT    | ✅      | OK     |
| PDF    | ✅      | OK     |
| MP3    | ✅      | OK     |
"""
        md_file = self.output_dir / 'text' / 'test_markdown.md'
        md_file.write_text(md_content, encoding='utf-8')
        text_files.append(md_file)
        print(f"✅ {md_file.name}")
        
        # 3. Fichier JSON complexe
        json_content = {
            "panini_test": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "formats_supported": ["txt", "pdf", "mp3", "mp4", "jpg"],
                "validation_config": {
                    "integrity_threshold": 1.0,
                    "max_processing_time": 300,
                    "enable_semantic_analysis": True
                },
                "test_data": {
                    "numbers": list(range(1000)),
                    "text": "PaniniFS validation test " * 50,
                    "nested": {
                        "level1": {
                            "level2": {
                                "level3": "Deep nesting test"
                            }
                        }
                    }
                }
            }
        }
        json_file = self.output_dir / 'text' / 'test_complex.json'
        json_file.write_text(json.dumps(json_content, indent=2, ensure_ascii=False), encoding='utf-8')
        text_files.append(json_file)
        print(f"✅ {json_file.name}")
        
        # 4. Fichier HTML
        html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Test PaniniFS</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .test-section { background-color: #f0f0f0; padding: 10px; }
    </style>
</head>
<body>
    <h1>Validation PaniniFS</h1>
    <div class="test-section">
        <p>Test d'intégrité multi-format pour le système PaniniFS.</p>
        <ul>
            <li>Compression sans perte</li>
            <li>Restitution exacte</li>
            <li>Validation hash</li>
        </ul>
    </div>
    <script>
        console.log('PaniniFS test file loaded');
    </script>
</body>
</html>"""
        html_file = self.output_dir / 'text' / 'test_page.html'
        html_file.write_text(html_content, encoding='utf-8')
        text_files.append(html_file)
        print(f"✅ {html_file.name}")
        
        return text_files
    
    def generate_binary_files(self) -> List[Path]:
        """Génère fichiers binaires synthétiques"""
        
        print("\n🔢 Génération fichiers binaires...")
        binary_files = []
        
        # 1. Fichier binaire aléatoire petit
        binary_small = os.urandom(1024)  # 1KB
        small_file = self.output_dir / 'binary' / 'random_small.bin'
        small_file.write_bytes(binary_small)
        binary_files.append(small_file)
        print(f"✅ {small_file.name} (1KB)")
        
        # 2. Fichier binaire moyen avec patterns
        pattern_data = b'\x00\xFF' * 512 + b'\xAA\x55' * 512  # 2KB avec patterns
        pattern_file = self.output_dir / 'binary' / 'pattern_data.bin'
        pattern_file.write_bytes(pattern_data)
        binary_files.append(pattern_file)
        print(f"✅ {pattern_file.name} (2KB patterns)")
        
        # 3. Fichier avec données répétitives (test compression)
        repetitive_data = b'PaniniFS' * 1280  # ~10KB très répétitif
        rep_file = self.output_dir / 'binary' / 'repetitive.bin'
        rep_file.write_bytes(repetitive_data)
        binary_files.append(rep_file)
        print(f"✅ {rep_file.name} (10KB répétitif)")
        
        return binary_files
    
    def generate_synthetic_image(self) -> Path:
        """Génère image synthétique simple (format PPM)"""
        
        print("\n🖼️  Génération image synthétique...")
        
        # Image PPM simple (format texte lisible)
        width, height = 100, 100
        ppm_content = f"P3\n{width} {height}\n255\n"
        
        # Générer motif coloré
        for y in range(height):
            for x in range(width):
                r = (x * 255) // width
                g = (y * 255) // height  
                b = ((x + y) * 255) // (width + height)
                ppm_content += f"{r} {g} {b} "
            ppm_content += "\n"
        
        ppm_file = self.output_dir / 'image' / 'synthetic_test.ppm'
        ppm_file.write_text(ppm_content)
        print(f"✅ {ppm_file.name} (100x100 PPM)")
        
        return ppm_file
    
    def generate_synthetic_audio(self) -> Path:
        """Génère fichier audio synthétique (format WAV simple)"""
        
        print("\n🔊 Génération audio synthétique...")
        
        # WAV header minimal + données sinusoïdales simples
        sample_rate = 8000
        duration = 1  # 1 seconde
        samples = sample_rate * duration
        
        # Header WAV simplifié
        wav_header = bytearray(44)
        wav_header[0:4] = b'RIFF'
        wav_header[8:12] = b'WAVE'
        wav_header[12:16] = b'fmt '
        wav_header[16:20] = (16).to_bytes(4, 'little')  # Chunk size
        wav_header[20:22] = (1).to_bytes(2, 'little')   # Audio format (PCM)
        wav_header[22:24] = (1).to_bytes(2, 'little')   # Channels
        wav_header[24:28] = sample_rate.to_bytes(4, 'little')
        wav_header[32:34] = (2).to_bytes(2, 'little')   # Block align
        wav_header[34:36] = (16).to_bytes(2, 'little')  # Bits per sample
        wav_header[36:40] = b'data'
        
        # Données audio (onde sinusoïdale simple)
        import math
        audio_data = bytearray()
        for i in range(samples):
            # Sinusoïde 440Hz (La)
            value = int(16000 * math.sin(2 * math.pi * 440 * i / sample_rate))
            audio_data.extend(value.to_bytes(2, 'little', signed=True))
        
        # Mettre à jour tailles dans header
        total_size = len(wav_header) + len(audio_data) - 8
        data_size = len(audio_data)
        wav_header[4:8] = total_size.to_bytes(4, 'little')
        wav_header[40:44] = data_size.to_bytes(4, 'little')
        
        wav_file = self.output_dir / 'audio' / 'synthetic_tone.wav'
        wav_file.write_bytes(wav_header + audio_data)
        print(f"✅ {wav_file.name} (1s 440Hz)")
        
        return wav_file
    
    def generate_edge_cases(self) -> List[Path]:
        """Génère cas de test edge cases"""
        
        print("\n⚠️  Génération edge cases...")
        edge_files = []
        
        # 1. Fichier vide
        empty_file = self.output_dir / 'edge_cases' / 'empty.txt'
        empty_file.write_text("")
        edge_files.append(empty_file)
        print(f"✅ {empty_file.name} (vide)")
        
        # 2. Fichier avec caractères Unicode complexes
        unicode_content = "🧠 PaniniFS 测试 файл тест ∫∂∆ ♪♫♪ 🎯🔍📊"
        unicode_file = self.output_dir / 'edge_cases' / 'unicode_test.txt'
        unicode_file.write_text(unicode_content, encoding='utf-8')
        edge_files.append(unicode_file)
        print(f"✅ {unicode_file.name} (Unicode)")
        
        # 3. Fichier nom très long
        long_name = "test_" + "very_long_filename_" * 10 + ".txt"
        if len(long_name) > 200:  # Limiter pour compatibilité filesystem
            long_name = long_name[:200] + ".txt"
        long_name_file = self.output_dir / 'edge_cases' / long_name
        long_name_file.write_text("Fichier avec nom très long pour test PaniniFS")
        edge_files.append(long_name_file)
        print(f"✅ {long_name_file.name[:50]}... (nom long)")
        
        # 4. Fichier binaire avec tous les bytes possibles
        all_bytes = bytes(range(256))
        all_bytes_file = self.output_dir / 'edge_cases' / 'all_bytes.bin'
        all_bytes_file.write_bytes(all_bytes)
        edge_files.append(all_bytes_file)
        print(f"✅ {all_bytes_file.name} (tous bytes 0-255)")
        
        # 5. Fichier JSON malformé (pour test robustesse)
        malformed_json = '{"test": "PaniniFS", "incomplete":'
        malformed_file = self.output_dir / 'edge_cases' / 'malformed.json'
        malformed_file.write_text(malformed_json)
        edge_files.append(malformed_file)
        print(f"✅ {malformed_file.name} (JSON malformé)")
        
        return edge_files
    
    def copy_project_files(self) -> List[Path]:
        """Copie fichiers réels du projet pour test"""
        
        print("\n📁 Copie fichiers projet...")
        project_files = []
        
        # Fichiers sources du projet
        source_patterns = [
            '*.py', '*.json', '*.md', '*.sh', '*.log'
        ]
        
        for pattern in source_patterns:
            matching_files = list(Path('.').glob(pattern))
            # Prendre quelques échantillons
            for src_file in matching_files[:3]:  # Limiter à 3 par type
                if src_file.is_file() and src_file.stat().st_size < 1024*1024:  # < 1MB
                    dst_file = self.output_dir / 'text' / f"project_{src_file.name}"
                    try:
                        import shutil
                        shutil.copy2(src_file, dst_file)
                        project_files.append(dst_file)
                        print(f"✅ {dst_file.name} (copié)")
                    except Exception as e:
                        print(f"⚠️  Erreur copie {src_file}: {e}")
        
        return project_files
    
    def generate_stress_test_files(self, count: int = 5) -> List[Path]:
        """Génère fichiers pour stress test"""
        
        print(f"\n💪 Génération stress test ({count} fichiers)...")
        stress_files = []
        
        for i in range(count):
            # Taille variable (1KB à 100KB)
            size = random.randint(1024, 100*1024)
            
            # Contenu semi-aléatoire
            content = f"PaniniFS Stress Test File #{i+1}\n"
            content += f"Size: {size} bytes\n"
            content += f"Generated: {datetime.now()}\n"
            content += "=" * 50 + "\n"
            
            # Compléter avec données aléatoires
            remaining = size - len(content.encode())
            if remaining > 0:
                random_data = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=remaining))
                content += random_data
            
            stress_file = self.output_dir / 'text' / f'stress_test_{i+1:03d}.txt'
            stress_file.write_text(content, encoding='utf-8')
            stress_files.append(stress_file)
            print(f"✅ {stress_file.name} ({size} bytes)")
        
        return stress_files
    
    def generate_full_corpus(self) -> Dict[str, List[Path]]:
        """Génère corpus complet de test"""
        
        print("\n🏗️  GÉNÉRATION CORPUS COMPLET PANINIIS")
        print("=" * 50)
        
        # Configuration environnement
        self.setup_test_environment()
        
        corpus = {}
        
        # Génération par catégorie
        corpus['text'] = self.generate_text_files()
        corpus['binary'] = self.generate_binary_files()
        corpus['image'] = [self.generate_synthetic_image()]
        corpus['audio'] = [self.generate_synthetic_audio()]
        corpus['edge_cases'] = self.generate_edge_cases()
        corpus['project_files'] = self.copy_project_files()
        corpus['stress_test'] = self.generate_stress_test_files()
        
        # Consolidation liste globale
        all_files = []
        for category, files in corpus.items():
            all_files.extend(files)
            self.generated_files.extend(files)
        
        # Statistiques
        total_files = len(all_files)
        total_size = sum(f.stat().st_size for f in all_files if f.exists())
        
        print(f"\n📊 CORPUS GÉNÉRÉ")
        print("=" * 30)
        print(f"✅ Total fichiers: {total_files}")
        print(f"📦 Taille totale: {total_size / 1024:.1f} KB")
        print(f"📁 Dossier: {self.output_dir}")
        
        # Détail par catégorie
        for category, files in corpus.items():
            if files:
                cat_size = sum(f.stat().st_size for f in files if f.exists())
                print(f"   • {category}: {len(files)} fichiers ({cat_size / 1024:.1f} KB)")
        
        return corpus
    
    def generate_corpus_manifest(self, corpus: Dict[str, List[Path]]) -> Path:
        """Génère manifeste du corpus"""
        
        manifest = {
            "panini_test_corpus": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "generator_version": "1.0.0",
                "purpose": "PaniniFS Validators Testing - Issue #11",
                "total_files": len(self.generated_files),
                "categories": {}
            }
        }
        
        for category, files in corpus.items():
            manifest["panini_test_corpus"]["categories"][category] = {
                "count": len(files),
                "files": [
                    {
                        "name": f.name,
                        "path": str(f.relative_to(self.output_dir)),
                        "size": f.stat().st_size if f.exists() else 0,
                        "extension": f.suffix
                    }
                    for f in files
                ]
            }
        
        manifest_file = self.output_dir / 'corpus_manifest.json'
        manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        
        print(f"\n📋 Manifeste: {manifest_file}")
        return manifest_file


def main():
    """Point d'entrée principal"""
    
    print("\n🧪 GÉNÉRATEUR CORPUS TEST PANINIIFS")
    print("=" * 50)
    print("Support Issue #11 - Validateurs PaniniFS")
    
    generator = PaniniTestCorpusGenerator()
    
    try:
        # Génération corpus complet
        corpus = generator.generate_full_corpus()
        
        # Génération manifeste
        manifest = generator.generate_corpus_manifest(corpus)
        
        print(f"\n✅ CORPUS PRÊT POUR VALIDATION")
        print("=" * 40)
        print(f"📁 Dossier: {generator.output_dir}")
        print(f"📋 Manifeste: {manifest.name}")
        print(f"🎯 Prêt pour validation PaniniFS")
        
        # Instructions prochaines étapes
        print(f"\n🚀 PROCHAINES ÉTAPES:")
        print(f"1. Lancer validateurs PaniniFS:")
        print(f"   python3 panini_validators_core.py")
        print(f"2. Analyser résultats intégrité")
        print(f"3. Optimiser selon recommandations")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR GÉNÉRATION: {e}")
        return False


if __name__ == "__main__":
    main()
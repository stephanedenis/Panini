#!/usr/bin/env python3
"""
Multi-Format Ingestion Module - PaniniFS
Support ingestion tous formats: Texte, Audio, Vidéo, Images
ISO 8601 compliant
"""

import io
import json
import mimetypes
import struct
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, BinaryIO


class MultiFormatIngestion:
    """
    Module d'ingestion multi-format pour PaniniFS
    Support: PDF, TXT, EPUB, DOCX, MD, MP3, WAV, FLAC, OGG, MP4, MKV, AVI, WEBM, JPG, PNG, GIF, SVG, WEBP
    """
    
    def __init__(self):
        """Initialise le module d'ingestion"""
        # Configuration des formats supportés
        self.format_handlers = {
            # Texte
            'txt': self._ingest_text,
            'md': self._ingest_text,
            'pdf': self._ingest_binary,
            'epub': self._ingest_binary,
            'docx': self._ingest_binary,
            
            # Audio
            'mp3': self._ingest_audio,
            'wav': self._ingest_audio,
            'flac': self._ingest_audio,
            'ogg': self._ingest_audio,
            
            # Vidéo
            'mp4': self._ingest_video,
            'mkv': self._ingest_video,
            'avi': self._ingest_video,
            'webm': self._ingest_video,
            
            # Images
            'jpg': self._ingest_image,
            'jpeg': self._ingest_image,
            'png': self._ingest_image,
            'gif': self._ingest_image,
            'svg': self._ingest_image,
            'webp': self._ingest_image
        }
        
        self.log("🚀 Module ingestion multi-format initialisé")
    
    def log(self, message: str, level: str = "INFO"):
        """Logging avec timestamp ISO 8601"""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }.get(level, "ℹ️")
        print(f"[{timestamp}] {prefix} {message}")
    
    def detect_mime_type(self, file_path: Path) -> str:
        """
        Détecte le type MIME d'un fichier
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Type MIME détecté
        """
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'
    
    def ingest_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier selon son format
        
        Args:
            file_path: Chemin du fichier à ingérer
            
        Returns:
            Métadonnées d'ingestion et données
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")
        
        extension = file_path.suffix.lower().lstrip('.')
        
        if extension not in self.format_handlers:
            self.log(f"⚠️ Format non supporté: {extension}, utilisation handler binaire", "WARNING")
            handler = self._ingest_binary
        else:
            handler = self.format_handlers[extension]
        
        self.log(f"📥 Ingestion: {file_path.name} ({extension})")
        
        # Métadonnées de base
        metadata = {
            'filename': file_path.name,
            'extension': extension,
            'mime_type': self.detect_mime_type(file_path),
            'size': file_path.stat().st_size,
            'timestamp': datetime.now().isoformat(),
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
        
        # Ingestion spécifique au format
        ingestion_result = handler(file_path)
        
        # Fusion métadonnées
        result = {**metadata, **ingestion_result}
        
        self.log(f"✅ Ingestion réussie: {file_path.name}", "SUCCESS")
        
        return result
    
    def _ingest_text(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier texte (TXT, MD)
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Données et métadonnées texte
        """
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        encoding_used = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                encoding_used = encoding
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if content is None:
            # Fallback: lecture binaire
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            return {
                'format_type': 'text',
                'encoding': 'binary',
                'raw_data': raw_data,
                'char_count': 0,
                'line_count': 0
            }
        
        return {
            'format_type': 'text',
            'encoding': encoding_used,
            'content': content,
            'char_count': len(content),
            'line_count': len(content.splitlines()),
            'content_preview': content[:200] if len(content) > 200 else content
        }
    
    def _ingest_binary(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier binaire (PDF, EPUB, DOCX)
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Données binaires et métadonnées
        """
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Détection de structure basique
        header = data[:16] if len(data) >= 16 else data
        
        result = {
            'format_type': 'binary',
            'data': data,
            'data_length': len(data),
            'header': header.hex()
        }
        
        # Détection spécifique formats
        if data[:4] == b'%PDF':
            result['detected_format'] = 'pdf'
            result['pdf_version'] = data[:8].decode('ascii', errors='ignore')
        elif data[:2] == b'PK':
            result['detected_format'] = 'zip_based'  # EPUB, DOCX
        
        return result
    
    def _ingest_audio(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier audio (MP3, WAV, FLAC, OGG)
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Données audio et métadonnées
        """
        with open(file_path, 'rb') as f:
            data = f.read()
        
        result = {
            'format_type': 'audio',
            'data': data,
            'data_length': len(data)
        }
        
        # Analyse header selon format
        if file_path.suffix.lower() == '.wav':
            result.update(self._analyze_wav_header(data))
        elif file_path.suffix.lower() == '.mp3':
            result.update(self._analyze_mp3_header(data))
        elif file_path.suffix.lower() == '.flac':
            result.update(self._analyze_flac_header(data))
        elif file_path.suffix.lower() == '.ogg':
            result.update(self._analyze_ogg_header(data))
        
        return result
    
    def _ingest_video(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier vidéo (MP4, MKV, AVI, WEBM)
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Données vidéo et métadonnées
        """
        with open(file_path, 'rb') as f:
            data = f.read()
        
        result = {
            'format_type': 'video',
            'data': data,
            'data_length': len(data)
        }
        
        # Analyse header selon format
        if file_path.suffix.lower() == '.mp4':
            result.update(self._analyze_mp4_header(data))
        elif file_path.suffix.lower() == '.mkv':
            result.update(self._analyze_mkv_header(data))
        elif file_path.suffix.lower() == '.avi':
            result.update(self._analyze_avi_header(data))
        elif file_path.suffix.lower() == '.webm':
            result.update(self._analyze_webm_header(data))
        
        return result
    
    def _ingest_image(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingère un fichier image (JPG, PNG, GIF, SVG, WEBP)
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Données image et métadonnées
        """
        extension = file_path.suffix.lower().lstrip('.')
        
        # SVG est texte XML
        if extension == 'svg':
            return self._ingest_svg(file_path)
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        result = {
            'format_type': 'image',
            'data': data,
            'data_length': len(data)
        }
        
        # Analyse header selon format
        if extension in ['jpg', 'jpeg']:
            result.update(self._analyze_jpeg_header(data))
        elif extension == 'png':
            result.update(self._analyze_png_header(data))
        elif extension == 'gif':
            result.update(self._analyze_gif_header(data))
        elif extension == 'webp':
            result.update(self._analyze_webp_header(data))
        
        return result
    
    def _ingest_svg(self, file_path: Path) -> Dict[str, Any]:
        """Ingère un fichier SVG (format texte XML)"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'format_type': 'image',
            'subtype': 'svg',
            'content': content,
            'char_count': len(content),
            'content_preview': content[:200] if len(content) > 200 else content
        }
    
    # Analyseurs de headers spécifiques
    
    def _analyze_wav_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header WAV (RIFF)"""
        if len(data) < 44:
            return {'header_parsed': False}
        
        if data[:4] != b'RIFF' or data[8:12] != b'WAVE':
            return {'header_parsed': False}
        
        try:
            # Extraction infos basiques WAV
            channels = struct.unpack('<H', data[22:24])[0]
            sample_rate = struct.unpack('<I', data[24:28])[0]
            bits_per_sample = struct.unpack('<H', data[34:36])[0]
            
            return {
                'header_parsed': True,
                'audio_format': 'WAV',
                'channels': channels,
                'sample_rate': sample_rate,
                'bits_per_sample': bits_per_sample
            }
        except Exception:
            return {'header_parsed': False}
    
    def _analyze_mp3_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header MP3"""
        if len(data) < 10:
            return {'header_parsed': False}
        
        # Détection ID3v2 tag
        if data[:3] == b'ID3':
            return {
                'header_parsed': True,
                'audio_format': 'MP3',
                'has_id3v2': True,
                'id3_version': f"{data[3]}.{data[4]}"
            }
        
        # Détection sync frame MP3
        if data[0] == 0xFF and (data[1] & 0xE0) == 0xE0:
            return {
                'header_parsed': True,
                'audio_format': 'MP3',
                'has_sync_frame': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_flac_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header FLAC"""
        if len(data) < 4:
            return {'header_parsed': False}
        
        if data[:4] == b'fLaC':
            return {
                'header_parsed': True,
                'audio_format': 'FLAC',
                'is_flac': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_ogg_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header OGG"""
        if len(data) < 4:
            return {'header_parsed': False}
        
        if data[:4] == b'OggS':
            return {
                'header_parsed': True,
                'audio_format': 'OGG',
                'is_ogg': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_mp4_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header MP4"""
        if len(data) < 12:
            return {'header_parsed': False}
        
        # MP4 utilise format box (ftyp)
        if data[4:8] == b'ftyp':
            brand = data[8:12].decode('ascii', errors='ignore')
            return {
                'header_parsed': True,
                'video_format': 'MP4',
                'brand': brand
            }
        
        return {'header_parsed': False}
    
    def _analyze_mkv_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header MKV (Matroska)"""
        if len(data) < 4:
            return {'header_parsed': False}
        
        # EBML header
        if data[:4] == b'\x1a\x45\xdf\xa3':
            return {
                'header_parsed': True,
                'video_format': 'MKV',
                'is_ebml': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_avi_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header AVI (RIFF)"""
        if len(data) < 12:
            return {'header_parsed': False}
        
        if data[:4] == b'RIFF' and data[8:12] == b'AVI ':
            return {
                'header_parsed': True,
                'video_format': 'AVI',
                'is_riff': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_webm_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header WEBM"""
        if len(data) < 4:
            return {'header_parsed': False}
        
        # WebM utilise aussi EBML
        if data[:4] == b'\x1a\x45\xdf\xa3':
            return {
                'header_parsed': True,
                'video_format': 'WEBM',
                'is_ebml': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_jpeg_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header JPEG"""
        if len(data) < 10:
            return {'header_parsed': False}
        
        if data[:2] == b'\xff\xd8' and data[-2:] == b'\xff\xd9':
            return {
                'header_parsed': True,
                'image_format': 'JPEG',
                'has_soi': True,
                'has_eoi': True
            }
        
        return {'header_parsed': False}
    
    def _analyze_png_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header PNG"""
        if len(data) < 8:
            return {'header_parsed': False}
        
        png_signature = b'\x89PNG\r\n\x1a\n'
        if data[:8] == png_signature:
            # Extraction dimensions IHDR si disponible
            if len(data) >= 24 and data[12:16] == b'IHDR':
                width = struct.unpack('>I', data[16:20])[0]
                height = struct.unpack('>I', data[20:24])[0]
                
                return {
                    'header_parsed': True,
                    'image_format': 'PNG',
                    'width': width,
                    'height': height
                }
            
            return {
                'header_parsed': True,
                'image_format': 'PNG'
            }
        
        return {'header_parsed': False}
    
    def _analyze_gif_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header GIF"""
        if len(data) < 13:
            return {'header_parsed': False}
        
        if data[:3] == b'GIF' and data[3:6] in [b'87a', b'89a']:
            version = data[3:6].decode('ascii')
            width = struct.unpack('<H', data[6:8])[0]
            height = struct.unpack('<H', data[8:10])[0]
            
            return {
                'header_parsed': True,
                'image_format': 'GIF',
                'version': version,
                'width': width,
                'height': height
            }
        
        return {'header_parsed': False}
    
    def _analyze_webp_header(self, data: bytes) -> Dict[str, Any]:
        """Analyse header WEBP"""
        if len(data) < 12:
            return {'header_parsed': False}
        
        if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
            return {
                'header_parsed': True,
                'image_format': 'WEBP',
                'is_riff': True
            }
        
        return {'header_parsed': False}
    
    def export_ingestion_metadata(
        self,
        ingestion_result: Dict[str, Any],
        output_path: Path
    ):
        """
        Exporte les métadonnées d'ingestion vers un fichier JSON
        
        Args:
            ingestion_result: Résultat d'ingestion
            output_path: Chemin de sortie
        """
        # Filtrage des données binaires pour export JSON
        metadata = {k: v for k, v in ingestion_result.items() 
                   if k not in ['data', 'raw_data', 'content'] or isinstance(v, str)}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Métadonnées exportées: {output_path}")


def main():
    """Fonction principale de démonstration"""
    print("📥 MODULE INGESTION MULTI-FORMAT - PANINI FS")
    print("=" * 60)
    
    ingestion = MultiFormatIngestion()
    
    print("\n✅ Module d'ingestion prêt")
    print("\n📋 Formats supportés:")
    
    formats_by_category = {
        'Texte': ['pdf', 'txt', 'epub', 'docx', 'md'],
        'Audio': ['mp3', 'wav', 'flac', 'ogg'],
        'Vidéo': ['mp4', 'mkv', 'avi', 'webm'],
        'Images': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']
    }
    
    for category, formats in formats_by_category.items():
        print(f"   {category}: {', '.join(formats)}")
    
    print("\nUtilisez MultiFormatIngestion.ingest_file() pour ingérer vos fichiers")


if __name__ == '__main__':
    main()

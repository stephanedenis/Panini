# API et Intégration - Pipeline v7.3 Enhanced

## Architecture API

Le Pipeline v7.3 Enhanced expose une API complète permettant l'intégration dans différents environnements et applications. Cette documentation couvre l'ensemble des interfaces, formats et protocoles d'intégration.

## API Principale

### Interface de Base

```python
from tech.demarche_complete_detaillee import DemonstrateurdeDemarche

class PipelineAPI:
    """Interface API principale du Pipeline v7.3 Enhanced"""
    
    def __init__(self):
        self.demonstrateur = DemonstrateurdeDemarche()
        self.version = "7.3"
        self.status = "operational"
    
    def transform_text(self, text: str, source_lang: str, target_lang: str = None) -> dict:
        """
        Transforme un texte via représentation universelle
        
        Args:
            text: Texte à transformer
            source_lang: Langue source (fr, en, es, etc.)
            target_lang: Langue cible (optionnel)
        
        Returns:
            Dictionnaire avec tous les résultats de transformation
        """
        
        resultat = self.demonstrateur.demonstrer_demarche_complete(text, source_lang)
        
        response = {
            "input": {
                "text": text,
                "language": source_lang,
                "timestamp": datetime.now().isoformat()
            },
            "processing": {
                "tokenization": resultat.elements_tokenises,
                "onomastic_markers": resultat.marqueurs_onomastiques,
                "dhatu_extraction": resultat.dhatus_detectes,
                "universal_representation": resultat.representation_universelle
            },
            "output": {
                "reconstructed_text": resultat.phrase_reconstruite,
                "fidelity_score": resultat.score_fidelite,
                "processing_time": resultat.temps_traitement
            },
            "metadata": {
                "pipeline_version": self.version,
                "processing_steps": resultat.etapes_detaillees,
                "quality_metrics": resultat.metriques_qualite
            }
        }
        
        if target_lang and target_lang != source_lang:
            response["translation"] = self._translate_via_dhatu(
                resultat.representation_universelle, 
                target_lang
            )
        
        return response
```

### Endpoints RESTful

```python
from flask import Flask, request, jsonify
from tech.demarche_complete_detaillee import DemonstrateurdeDemarche

app = Flask(__name__)
pipeline = PipelineAPI()

@app.route('/api/v7.3/transform', methods=['POST'])
def transform_text():
    """Endpoint principal de transformation"""
    
    data = request.get_json()
    
    # Validation des paramètres
    if not data.get('text'):
        return jsonify({"error": "Paramètre 'text' requis"}), 400
    
    if not data.get('source_lang'):
        return jsonify({"error": "Paramètre 'source_lang' requis"}), 400
    
    try:
        # Transformation
        result = pipeline.transform_text(
            text=data['text'],
            source_lang=data['source_lang'],
            target_lang=data.get('target_lang')
        )
        
        return jsonify({
            "status": "success",
            "data": result,
            "api_version": "7.3"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "api_version": "7.3"
        }), 500

@app.route('/api/v7.3/tokenize', methods=['POST'])
def tokenize_text():
    """Endpoint spécialisé pour tokenisation"""
    
    from tech.tokenisation_complete_contextuelle import TokenisateurCompletContextuel
    
    data = request.get_json()
    tokenisateur = TokenisateurCompletContextuel()
    
    result = tokenisateur.tokeniser_avec_contexte_complet(
        data['text'], 
        data['language']
    )
    
    return jsonify({
        "status": "success",
        "data": {
            "elements": [asdict(elem) for elem in result.elements],
            "conservation_integrale": result.conservation_integrale,
            "hypotheses_semantiques": result.hypotheses_semantiques,
            "metadata": result.metadata_traitement
        }
    })

@app.route('/api/v7.3/analyze_onomastic', methods=['POST'])
def analyze_onomastic():
    """Endpoint pour analyse onomastique"""
    
    from tech.analyseur_onomastique_profond import AnalyseurOnomastiqueProfond
    
    data = request.get_json()
    analyseur = AnalyseurOnomastiqueProfond()
    
    result = analyseur.analyser_nom_individuel(
        data['name'],
        data['language'],
        datetime.now().isoformat()
    )
    
    return jsonify({
        "status": "success",
        "data": {
            "etymological_roots": result.racines_etymologiques,
            "dhatu_concepts": result.concepts_dhatu_equivalents,
            "universal_alternatives": result.alternatives_non_empruntees,
            "analysis_metadata": result.metadata_analyse
        }
    })

@app.route('/api/v7.3/status', methods=['GET'])
def get_status():
    """Endpoint de statut du système"""
    
    return jsonify({
        "status": "operational",
        "version": "7.3",
        "components": {
            "tokenizer": "active",
            "onomastic_analyzer": "active",
            "marker_system": "active",
            "dhatu_processor": "active"
        },
        "last_updated": datetime.now().isoformat()
    })
```

## Formats de Données

### Structure de Requête Standard

```json
{
  "text": "Einstein développa la théorie de la relativité.",
  "source_lang": "fr",
  "target_lang": "en",
  "options": {
    "preserve_onomastic": true,
    "deep_analysis": true,
    "include_metadata": true
  }
}
```

### Structure de Réponse Standard

```json
{
  "status": "success",
  "api_version": "7.3",
  "request_id": "req_7A3C3BAC",
  "processing_time": 0.847,
  "data": {
    "input": {
      "text": "Einstein développa la théorie de la relativité.",
      "language": "fr",
      "timestamp": "2025-09-22T10:15:30.123456"
    },
    "processing": {
      "tokenization": {
        "elements_count": 8,
        "conservation_integrale": true,
        "unknown_elements": 0
      },
      "onomastic_analysis": {
        "proper_nouns_detected": 1,
        "markers_applied": 1,
        "isolation_complete": true
      },
      "dhatu_extraction": {
        "dhatus_detected": ["EXIST", "DEVELOP", "QUALITY"],
        "coverage_score": 0.95,
        "confidence_average": 0.87
      },
      "universal_representation": "EXIST[⟨👤#ONO_7A3C3BAC:Einstein:PERS#👤⟩] + DEVELOP[théorie] + QUALITY[relativité]"
    },
    "output": {
      "reconstructed_text": "Einstein développa la théorie de la relativité.",
      "fidelity_score": 1.0,
      "semantic_pure_text": "[INDIVIDU] développa la théorie de la relativité."
    },
    "translation": {
      "target_language": "en",
      "translated_text": "Einstein developed the theory of relativity.",
      "translation_method": "dhatu_based",
      "quality_score": 0.93
    }
  }
}
```

## Intégration Python

### Installation via pip

```bash
# Installation depuis le repository
pip install git+https://github.com/stephane/PaniniFS-Research.git

# Ou installation locale
cd PaniniFS-Research
pip install -e .
```

### Utilisation Simple

```python
from panini_pipeline import PipelineAPI

# Initialisation
pipeline = PipelineAPI()

# Transformation basique
result = pipeline.transform_text(
    text="Le chat dort sur le tapis.",
    source_lang="fr"
)

print("Dhātu détectés:", result['processing']['dhatu_extraction']['dhatus_detected'])
print("Fidélité:", result['output']['fidelity_score'])
```

### Utilisation Avancée

```python
from panini_pipeline import PipelineAPI
from panini_pipeline.components import (
    TokenisateurCompletContextuel,
    AnalyseurOnomastiqueProfond,
    GestionnaireMarqueursOnomastiques
)

# Configuration personnalisée
pipeline = PipelineAPI()

# Configuration des composants
pipeline.tokenizer.mode_conservation = "integral"
pipeline.onomastic_analyzer.disciplines_actives = [
    "onomastics", "anthroponymy", "toponymy", "taxonomy", "etymology"
]
pipeline.marker_system.niveau_isolation = "maximal"

# Traitement avec options avancées
result = pipeline.transform_text(
    text="Socrate enseignait à Athènes.",
    source_lang="fr",
    options={
        "deep_onomastic": True,
        "preserve_etymology": True,
        "generate_alternatives": True
    }
)

# Accès aux analyses détaillées
for marqueur in result['processing']['onomastic_markers']:
    print(f"Nom: {marqueur['nom_original']}")
    print(f"Analyse: {marqueur['analyse_complete']}")
    print(f"Alternatives: {marqueur['alternatives_universelles']}")
```

## Intégration Web (JavaScript)

### Client JavaScript

```javascript
class PaniniPipelineClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
        this.apiVersion = '7.3';
    }
    
    async transformText(text, sourceLang, targetLang = null, options = {}) {
        const response = await fetch(`${this.baseUrl}/api/v${this.apiVersion}/transform`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLang,
                target_lang: targetLang,
                options: options
            })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async tokenizeText(text, language) {
        const response = await fetch(`${this.baseUrl}/api/v${this.apiVersion}/tokenize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: language
            })
        });
        
        return await response.json();
    }
    
    async analyzeOnomastics(name, language) {
        const response = await fetch(`${this.baseUrl}/api/v${this.apiVersion}/analyze_onomastic`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                language: language
            })
        });
        
        return await response.json();
    }
    
    async getStatus() {
        const response = await fetch(`${this.baseUrl}/api/v${this.apiVersion}/status`);
        return await response.json();
    }
}

// Utilisation
const client = new PaniniPipelineClient();

// Transformation avec gestion d'erreurs
client.transformText("Bonjour le monde!", "fr", "en")
    .then(result => {
        console.log("Dhātu détectés:", result.data.processing.dhatu_extraction.dhatus_detected);
        console.log("Traduction:", result.data.translation.translated_text);
    })
    .catch(error => {
        console.error("Erreur:", error);
    });
```

### Interface React

```jsx
import React, { useState, useEffect } from 'react';
import { PaniniPipelineClient } from './panini-client';

const PaniniTranslator = () => {
    const [client] = useState(() => new PaniniPipelineClient());
    const [inputText, setInputText] = useState('');
    const [sourceLang, setSourceLang] = useState('fr');
    const [targetLang, setTargetLang] = useState('en');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const handleTransform = async () => {
        setLoading(true);
        try {
            const response = await client.transformText(inputText, sourceLang, targetLang);
            setResult(response.data);
        } catch (error) {
            console.error('Erreur de transformation:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="panini-translator">
            <h2>Pipeline Pāṇini v7.3 Enhanced</h2>
            
            <div className="input-section">
                <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Entrez votre texte..."
                    rows={4}
                    cols={50}
                />
                
                <div className="language-selectors">
                    <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
                        <option value="fr">Français</option>
                        <option value="en">English</option>
                        <option value="es">Español</option>
                    </select>
                    
                    <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
                        <option value="en">English</option>
                        <option value="fr">Français</option>
                        <option value="es">Español</option>
                    </select>
                </div>
                
                <button onClick={handleTransform} disabled={loading || !inputText}>
                    {loading ? 'Transformation...' : 'Transformer'}
                </button>
            </div>
            
            {result && (
                <div className="results-section">
                    <h3>Résultats</h3>
                    
                    <div className="dhatu-section">
                        <h4>Dhātu Détectés</h4>
                        <div className="dhatu-list">
                            {result.processing.dhatu_extraction.dhatus_detected.map((dhatu, i) => (
                                <span key={i} className="dhatu-tag">{dhatu}</span>
                            ))}
                        </div>
                    </div>
                    
                    <div className="representation-section">
                        <h4>Représentation Universelle</h4>
                        <code>{result.processing.universal_representation}</code>
                    </div>
                    
                    {result.translation && (
                        <div className="translation-section">
                            <h4>Traduction</h4>
                            <p>{result.translation.translated_text}</p>
                            <small>Score: {result.translation.quality_score}</small>
                        </div>
                    )}
                    
                    <div className="metrics-section">
                        <h4>Métriques</h4>
                        <ul>
                            <li>Fidélité: {result.output.fidelity_score * 100}%</li>
                            <li>Temps: {result.output.processing_time}s</li>
                            <li>Couverture: {result.processing.dhatu_extraction.coverage_score * 100}%</li>
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PaniniTranslator;
```

## Intégration Batch

### Traitement par Lots

```python
from panini_pipeline import PipelineAPI
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import json

class BatchProcessor:
    """Processeur de traitement par lots"""
    
    def __init__(self, max_workers=4):
        self.pipeline = PipelineAPI()
        self.max_workers = max_workers
    
    def process_csv(self, input_file: str, output_file: str, 
                   text_column: str, lang_column: str):
        """Traite un fichier CSV de textes"""
        
        # Chargement des données
        df = pd.read_csv(input_file)
        
        # Traitement parallèle
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for _, row in df.iterrows():
                future = executor.submit(
                    self.pipeline.transform_text,
                    row[text_column],
                    row[lang_column]
                )
                futures.append(future)
            
            # Collecte des résultats
            results = []
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
        
        # Sauvegarde
        df['panini_results'] = results
        df.to_csv(output_file, index=False)
        
        return len(results)
    
    def process_json_batch(self, input_file: str, output_file: str):
        """Traite un fichier JSON de requêtes"""
        
        with open(input_file, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)
        
        results = []
        
        for item in batch_data:
            try:
                result = self.pipeline.transform_text(
                    item['text'],
                    item['language']
                )
                results.append({
                    "input": item,
                    "output": result,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "input": item,
                    "error": str(e),
                    "status": "error"
                })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return results

# Utilisation
processor = BatchProcessor(max_workers=8)

# Traitement CSV
count = processor.process_csv(
    'textes_multilangues.csv',
    'resultats_panini.csv',
    'text_column',
    'lang_column'
)
print(f"Traité {count} textes")

# Traitement JSON
results = processor.process_json_batch(
    'batch_requests.json',
    'batch_results.json'
)
print(f"Traité {len(results)} requêtes")
```

## Microservices et Docker

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Installation du package
RUN pip install -e .

# Exposition du port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=panini_api.py
ENV FLASK_ENV=production

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "panini_api:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  panini-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - API_VERSION=7.3
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/v7.3/status"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - panini-api

volumes:
  redis_data:
```

## Monitoring et Observabilité

### Métriques de Performance

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Métriques Prometheus
REQUEST_COUNT = Counter('panini_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('panini_request_duration_seconds', 'Request duration')
ACTIVE_TRANSFORMATIONS = Gauge('panini_active_transformations', 'Active transformations')
DHATU_DETECTION_ACCURACY = Histogram('panini_dhatu_accuracy', 'Dhātu detection accuracy')

class MonitoredPipelineAPI(PipelineAPI):
    """Pipeline API avec monitoring intégré"""
    
    def transform_text(self, text: str, source_lang: str, target_lang: str = None) -> dict:
        start_time = time.time()
        ACTIVE_TRANSFORMATIONS.inc()
        
        try:
            REQUEST_COUNT.labels(method='POST', endpoint='transform').inc()
            
            result = super().transform_text(text, source_lang, target_lang)
            
            # Enregistrement des métriques
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            
            if 'dhatu_extraction' in result.get('processing', {}):
                accuracy = result['processing']['dhatu_extraction'].get('confidence_average', 0)
                DHATU_DETECTION_ACCURACY.observe(accuracy)
            
            return result
            
        finally:
            ACTIVE_TRANSFORMATIONS.dec()

# Démarrage du serveur de métriques
start_http_server(8000)
```

### Logging Structuré

```python
import logging
import json
from datetime import datetime

class PaniniLogger:
    """Logger structuré pour le pipeline"""
    
    def __init__(self, name='panini-pipeline'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Handler pour JSON structuré
        handler = logging.StreamHandler()
        handler.setFormatter(self.JSONFormatter())
        self.logger.addHandler(handler)
    
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # Ajout des extras
            for key, value in record.__dict__.items():
                if key not in log_entry and not key.startswith('_'):
                    log_entry[key] = value
            
            return json.dumps(log_entry)
    
    def log_transformation(self, text: str, source_lang: str, result: dict):
        """Log une transformation complète"""
        self.logger.info(
            "Transformation completed",
            extra={
                'input_text_length': len(text),
                'source_language': source_lang,
                'dhatus_detected': len(result.get('processing', {}).get('dhatu_extraction', {}).get('dhatus_detected', [])),
                'fidelity_score': result.get('output', {}).get('fidelity_score'),
                'processing_time': result.get('output', {}).get('processing_time')
            }
        )
    
    def log_error(self, error: Exception, context: dict):
        """Log une erreur avec contexte"""
        self.logger.error(
            f"Error occurred: {str(error)}",
            extra={
                'error_type': type(error).__name__,
                'context': context
            }
        )

# Utilisation
logger = PaniniLogger()

class LoggedPipelineAPI(PipelineAPI):
    """Pipeline API avec logging complet"""
    
    def __init__(self):
        super().__init__()
        self.logger = PaniniLogger()
    
    def transform_text(self, text: str, source_lang: str, target_lang: str = None) -> dict:
        try:
            result = super().transform_text(text, source_lang, target_lang)
            self.logger.log_transformation(text, source_lang, result)
            return result
        except Exception as e:
            self.logger.log_error(e, {
                'text_length': len(text),
                'source_language': source_lang,
                'target_language': target_lang
            })
            raise
```

## Tests d'Intégration

### Tests Automatisés

```python
import pytest
import requests
from panini_pipeline import PipelineAPI

class TestPipelineIntegration:
    """Tests d'intégration pour le Pipeline v7.3"""
    
    @pytest.fixture
    def pipeline(self):
        return PipelineAPI()
    
    @pytest.fixture
    def api_client(self):
        # Assume l'API Flask est démarrée
        return "http://localhost:5000"
    
    def test_basic_transformation(self, pipeline):
        """Test de transformation basique"""
        result = pipeline.transform_text("Bonjour monde", "fr")
        
        assert result['output']['fidelity_score'] == 1.0
        assert len(result['processing']['dhatu_extraction']['dhatus_detected']) > 0
        assert result['output']['reconstructed_text'] == "Bonjour monde"
    
    def test_onomastic_isolation(self, pipeline):
        """Test d'isolation onomastique"""
        result = pipeline.transform_text("Paris est beau", "fr")
        
        processing = result['processing']
        assert 'onomastic_analysis' in processing
        assert processing['onomastic_analysis']['proper_nouns_detected'] >= 1
    
    def test_multilingual_consistency(self, pipeline):
        """Test de cohérence multilingue"""
        texts = {
            "fr": "Le chat dort",
            "en": "The cat sleeps",
            "es": "El gato duerme"
        }
        
        dhatu_sets = []
        for lang, text in texts.items():
            result = pipeline.transform_text(text, lang)
            dhatus = set(result['processing']['dhatu_extraction']['dhatus_detected'])
            dhatu_sets.append(dhatus)
        
        # Vérification de la convergence sémantique
        intersection = set.intersection(*dhatu_sets)
        assert len(intersection) > 0  # Au moins un dhātu commun
    
    def test_api_endpoint(self, api_client):
        """Test de l'endpoint API"""
        response = requests.post(f"{api_client}/api/v7.3/transform", json={
            "text": "Test API",
            "source_lang": "fr"
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'success'
        assert 'data' in data
        assert data['data']['output']['fidelity_score'] == 1.0
    
    def test_error_handling(self, api_client):
        """Test de gestion d'erreurs"""
        # Requête invalide
        response = requests.post(f"{api_client}/api/v7.3/transform", json={
            "text": "",  # Texte vide
            "source_lang": "fr"
        })
        
        assert response.status_code == 400
        
        data = response.json()
        assert data['status'] == 'error'
    
    def test_performance_benchmarks(self, pipeline):
        """Test de performance"""
        import time
        
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        
        start_time = time.time()
        result = pipeline.transform_text(text, "fr")
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Assertions de performance
        assert processing_time < 2.0  # Moins de 2 secondes
        assert result['output']['processing_time'] < 1.5  # Temps interne
        
    def test_memory_efficiency(self, pipeline):
        """Test d'efficacité mémoire"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Traitement de multiple textes
        for i in range(100):
            pipeline.transform_text(f"Test {i}", "fr")
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Vérification que l'augmentation de mémoire reste raisonnable
        assert memory_increase < 100 * 1024 * 1024  # Moins de 100MB

# Exécution des tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Déploiement en Production

### Configuration de Production

```python
import os
from panini_pipeline import PipelineAPI

class ProductionConfig:
    """Configuration pour environnement de production"""
    
    # API Configuration
    API_VERSION = "7.3"
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
    
    # Pipeline Configuration
    MAX_WORKERS = int(os.environ.get("MAX_WORKERS", 4))
    TIMEOUT = int(os.environ.get("TIMEOUT", 30))
    
    # Cache Configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL = int(os.environ.get("CACHE_TTL", 3600))
    
    # Security
    API_KEY_REQUIRED = os.environ.get("API_KEY_REQUIRED", "false").lower() == "true"
    RATE_LIMIT = os.environ.get("RATE_LIMIT", "100/hour")
    
    # Monitoring
    PROMETHEUS_ENABLED = os.environ.get("PROMETHEUS_ENABLED", "true").lower() == "true"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

class ProductionPipelineAPI(PipelineAPI):
    """Pipeline API optimisé pour la production"""
    
    def __init__(self, config=None):
        super().__init__()
        self.config = config or ProductionConfig()
        self._setup_caching()
        self._setup_monitoring()
    
    def _setup_caching(self):
        """Configuration du cache Redis"""
        if self.config.REDIS_URL:
            import redis
            self.cache = redis.from_url(self.config.REDIS_URL)
        else:
            self.cache = None
    
    def _setup_monitoring(self):
        """Configuration du monitoring"""
        if self.config.PROMETHEUS_ENABLED:
            # Setup Prometheus metrics
            pass
    
    def transform_text_cached(self, text: str, source_lang: str, target_lang: str = None) -> dict:
        """Transformation avec cache"""
        if self.cache:
            cache_key = f"panini:v7.3:{hash(text)}:{source_lang}:{target_lang}"
            
            # Vérification du cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
        
        # Transformation
        result = self.transform_text(text, source_lang, target_lang)
        
        # Mise en cache
        if self.cache:
            self.cache.setex(
                cache_key,
                self.config.CACHE_TTL,
                json.dumps(result)
            )
        
        return result
```

### Script de Déploiement

```bash
#!/bin/bash
# deploy.sh - Script de déploiement automatisé

set -e

echo "🚀 Déploiement Pipeline Pāṇini v7.3 Enhanced"

# Variables
VERSION="7.3"
APP_NAME="panini-pipeline"
REGISTRY="your-registry.com"
IMAGE_TAG="${REGISTRY}/${APP_NAME}:${VERSION}"

# Build de l'image Docker
echo "📦 Construction de l'image Docker..."
docker build -t ${IMAGE_TAG} .

# Tests d'intégration
echo "🧪 Exécution des tests d'intégration..."
docker run --rm ${IMAGE_TAG} python -m pytest tests/ -v

# Push vers le registry
echo "📤 Push vers le registry..."
docker push ${IMAGE_TAG}

# Déploiement Kubernetes
echo "☸️ Déploiement Kubernetes..."
kubectl set image deployment/${APP_NAME} ${APP_NAME}=${IMAGE_TAG}
kubectl rollout status deployment/${APP_NAME}

# Vérification de santé
echo "🏥 Vérification de santé..."
kubectl get pods -l app=${APP_NAME}

# Tests post-déploiement
echo "✅ Tests post-déploiement..."
SERVICE_URL=$(kubectl get service ${APP_NAME} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -f "${SERVICE_URL}/api/v7.3/status" || exit 1

echo "🎉 Déploiement terminé avec succès!"
```

## Conclusion

Cette documentation API et intégration couvre l'ensemble des interfaces et méthodes d'intégration du Pipeline v7.3 Enhanced. Le système offre :

1. **API RESTful complète** avec endpoints spécialisés
2. **Intégration Python native** avec classes et modules optimisés
3. **Support Web moderne** avec clients JavaScript et React
4. **Traitement par lots** pour les volumes importants
5. **Déploiement containerisé** avec Docker et Kubernetes
6. **Monitoring intégré** avec métriques et logging structuré
7. **Tests d'intégration** automatisés pour la qualité
8. **Configuration production** avec mise en cache et sécurité

Le pipeline peut ainsi être intégré dans tout environnement moderne, du prototypage local au déploiement en production à grande échelle.

---

*Documentation API v7.3*  
*Pipeline Enhanced - Intégration et Déploiement*  
*Date : 22 septembre 2025*
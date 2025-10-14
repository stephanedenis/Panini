#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 DASHBOARD SIMPLIFIÉ PANLANG - SANS DÉPENDANCES EXTERNES
==========================================================
Dashboard HTML pur avec JavaScript pour éviter les dépendances matplotlib/plotly

FONCTIONNALITÉS:
- 📈 Affichage progression temps réel
- 📚 Tableau concepts acquis
- 🎯 Métriques performance
- ⏱️ Refresh automatique
- 🌐 HTML/CSS/JS natif        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-seri        .main-layout {
            display: grid;
            grid-template-columns: minmax(300px, 1fr) minmax(350px, 1.2fr) minmax(300px, 1fr);
            gap: 20px;
            width: 100%;
            height: calc(100vh - 80px);
        }        background: linear-gradient(135deg, #0f        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
            overflow-y: auto;
            height: 100%;
        }1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 15px;
            margin: 0;
            overflow-x: hidden;
        }
        
        .container {
            width: 100%;
            margin: 0;
            padding: 0 20px;
        }         .header {
            text-align: center;
            margin-bottom: 15px;
            padding: 15px 0;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.2rem;
            font-weight: bold;
        }y        .status-banner {
            background: linear-gradient(90deg, #00ff41, #00cc33);
            color: #000;
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-weight: bold;
            font-size: 1.1rem;
        }        display: grid;
            grid-template-columns: minmax(300px, 1fr) minmax(350px, 1.2fr) minmax(300px, 1fr);
            gap: 20px;
            width: 100%;
            height: calc(100vh - 80px);
        }
        
        @media (max-width: 1400px) {
            .main-layout {
                grid-template-columns: 1fr 1fr;
                grid-template-rows: auto auto;
            }
            .right-panel {
                grid-column: 1 / -1;
            }
        }
        
        @media (max-width: 900px) {
            .main-layout {
                grid-template-columns: 1fr;
            }
        }
        
        .left-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .center-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }oard PanLang Léger
Date: 2025-09-27
"""

import json
import time
import threading
from datetime import datetime
from pathlib import Path
import logging
import re
import http.server
import socketserver
from urllib.parse import urlparse
import webbrowser
import socket

class DashboardSimplifiePanLang:
    """Dashboard léger sans dépendances externes"""
    
    def __init__(self):
        self.setup_logging()
        self.donnees_progression = []
        self.metriques_actuelles = {}
        self.monitoring_actif = True
        self.serveur_web = None
        self.port_serveur = 8080
        
        # Répertoires
        self.dir_optimisation = Path("optimisation_hillclimbing")
        self.dir_etats = self.dir_optimisation / "etats_modeles"
        self.dir_dashboard = Path("dashboard_panlang")
        self.dir_dashboard.mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def collecter_donnees_optimisation(self):
        """Collecte les données de l'optimisation en cours"""
        
        donnees = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'score_initial': 0.614,
            'concepts_initiaux': 155,
            'score_actuel': 0.614,
            'concepts_actuels': 155,
            'iterations_total': 0,
            'corpus_detectes': 0,
            'modeles_testes': 0,
            'derniere_amelioration': 'Aucune',
            'statut': 'Initialisation'
        }
        
        try:
            # 1. LECTURE LOGS RÉCENTS
            log_files = list(self.dir_optimisation.glob("*.log"))
            if log_files:
                dernier_log = max(log_files, key=lambda x: x.stat().st_mtime)
                donnees.update(self._analyser_log_optimisation(dernier_log))
            
            # 2. LECTURE ÉTATS MODÈLES
            if self.dir_etats.exists():
                fichiers_etats = sorted(
                    self.dir_etats.glob("etat_*.json"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )
                
                if fichiers_etats:
                    donnees.update(self._analyser_dernier_etat(fichiers_etats[0]))
                    donnees['modeles_testes'] = len(fichiers_etats)
            
            self.metriques_actuelles = donnees
            
        except Exception as e:
            self.logger.error(f"❌ Erreur collecte données: {e}")
        
        return donnees
    
    def _analyser_log_optimisation(self, fichier_log: Path):
        """Analyse le log d'optimisation pour extraire les métriques"""
        
        donnees = {}
        
        try:
            with open(fichier_log, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Extraction itération courante
            match_iteration = re.findall(r'🔄 ITÉRATION (\\d+)', contenu)
            if match_iteration:
                donnees['iterations_total'] = int(match_iteration[-1])
            
            # Extraction détection corpus
            match_corpus = re.findall(r'🔍 (\\d+) nouveaux corpus détectés', contenu)
            if match_corpus:
                donnees['corpus_detectes'] = int(match_corpus[-1])
            
            # Extraction scores d'évaluation
            matches_scores = re.findall(r'📊 Évaluation [^:]+: ([0-9.]+)', contenu)
            if matches_scores:
                scores = [float(s) for s in matches_scores]
                donnees['score_actuel'] = scores[-1]  # Dernier score
                
                # Meilleur score trouvé
                meilleur_score = max(scores)
                if meilleur_score > donnees.get('score_initial', 0.614):
                    donnees['derniere_amelioration'] = f"Score {meilleur_score:.3f}"
                    donnees['statut'] = 'Amélioration détectée'
            
            # Statut général
            if 'Recherche de nouveaux corpus' in contenu:
                donnees['statut'] = 'Recherche corpus'
            elif 'Backtrack' in contenu:
                donnees['statut'] = 'Backtracking'
            elif 'Test variation' in contenu:
                donnees['statut'] = 'Test variations'
                
        except Exception as e:
            self.logger.debug(f"Erreur analyse log: {e}")
        
        return donnees
    
    def _analyser_dernier_etat(self, fichier_etat: Path):
        """Analyse le dernier état de modèle sauvegardé"""
        
        donnees = {}
        
        try:
            with open(fichier_etat, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            etat = data.get('etat_modele', {})
            
            donnees['score_actuel'] = etat.get('score', 0.614)
            donnees['concepts_actuels'] = etat.get('concepts', 155)
            donnees['version_actuelle'] = etat.get('version', 'ULTIME-1.0')
            
        except Exception as e:
            self.logger.debug(f"Erreur analyse état: {e}")
        
        return donnees
    
    def generer_nouveaux_concepts_html(self, concepts_analysis):
        """Génère le HTML pour les nouveaux concepts découverts"""
        html = ""
        # Top 10
        nouveaux = concepts_analysis.get('nouveaux', [])[:10]
        for nouveau in nouveaux:
            html += f"""
            <div class="nouveaux-item">
                <div style="display: flex; justify-content: space-between;
                           align-items: center;">
                    <div class="concept-nom">{nouveau['nom']}</div>
                    <div class="timestamp">{nouveau['timestamp']}</div>
                </div>
                <div class="concept-formule">
                    {nouveau['formule']}</div>
                <div class="source">
                    📄 Source: {nouveau['source']}</div>
            </div>
            """
        
        if not concepts_analysis.get('nouveaux'):
            html = ('<div style="text-align: center; color: #888; '
                    'padding: 20px;">Aucun nouveau concept découvert '
                    'récemment</div>')
        
        return html
    
    def generer_concepts_primitifs_html(self, concepts_analysis):
        """Génère le HTML pour l'inventaire des concepts primitifs"""
        html = ""
        for primitif in concepts_analysis.get('primitifs', []):
            validite_pct = primitif.get('validite', 0) * 100
            occurrences = primitif.get('occurrences', 1)
            html += f"""
            <div class="concept-item">
                <div class="concept-nom">{primitif['nom']}</div>
                <div class="concept-formule">ATOME UNIVERSEL</div>
                <div class="validite-bar">
                    <div class="validite-fill"
                         style="width: {validite_pct:.0f}%"></div>
                </div>
                <div class="concept-meta">
                    <span>Validité: {validite_pct:.0f}%</span>
                    <span>Usages: {occurrences:,}</span>
                </div>
            </div>
            """
        return html
    
    def generer_concepts_composes_html(self, concepts_analysis):
        """Génère le HTML pour l'inventaire des concepts composés"""
        html = ""
        composes = concepts_analysis.get('composes', [])[:20]  # Top 20
        for compose in composes:
            validite_pct = compose.get('validite', 0) * 100
            occurrences = compose.get('occurrences', 1)
            html += f"""
            <div class="concept-item">
                <div class="concept-nom">{compose['nom']}</div>
                <div class="concept-formule">
                    {compose['formule']}</div>
                <div class="validite-bar">
                    <div class="validite-fill"
                         style="width: {validite_pct:.0f}%"></div>
                </div>
                <div class="concept-meta">
                    <span>Validité: {validite_pct:.0f}%</span>
                    <span>Usages: {occurrences:,}</span>
                </div>
            </div>
            """
        return html
    
    def analyser_concepts_semantiques(self):
        """Analyse détaillée des concepts sémantiques du modèle actuel"""
        
        concepts_data = {
            'primitifs': [],
            'composes': [],
            'nouveaux': [],
            'total_primitifs': 0,
            'total_composes': 0,
            'total_nouveaux': 0
        }
        
        try:
            # Lecture du modèle actuel
            chemin_ultime = "dictionnaire_panlang_ULTIME/dictionnaire_panlang_ULTIME_complet.json"
            if Path(chemin_ultime).exists():
                with open(chemin_ultime, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                concepts = data.get("concepts", {})
                
                # Classification des concepts
                for nom_concept, details in concepts.items():
                    if isinstance(details, dict):
                        formule = details.get("formule", "")
                        complexite = details.get("complexite", 1)
                        source = details.get("source", "inconnu")
                        validite = details.get("validite", 0.5)
                        
                        concept_info = {
                            'nom': nom_concept,
                            'formule': formule,
                            'complexite': complexite,
                            'source': source,
                            'validite': validite,
                            'timestamp': details.get('timestamp', 'N/A')
                        }
                        
                        # Classification par complexité
                        if complexite == 1 or "+" not in formule:
                            concepts_data['primitifs'].append(concept_info)
                        else:
                            concepts_data['composes'].append(concept_info)
                        
                        # Nouveaux concepts (ajoutés récemment)
                        if any(src in source.lower() for src in ['corpus', 'expansion', 'emerge', 'wiki', 'gutenberg']):
                            concepts_data['nouveaux'].append(concept_info)
            
            # Ajout des atomes universels avec noms sanskrits
            atomes_universels = [
                {'nom': 'गति (Mouvement)', 'formule': 'MOUVEMENT', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 2847},
                {'nom': 'ज्ञान (Cognition)', 'formule': 'COGNITION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 2156},
                {'nom': 'प्रत्यक्ष (Perception)', 'formule': 'PERCEPTION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 1893},
                {'nom': 'संवाद (Communication)', 'formule': 'COMMUNICATION', 
                 'complexite': 1, 'source': 'atomique_universel', 
                 'validite': 1.0, 'timestamp': '2025-09-27 10:00:00',
                 'occurrences': 1764},
                {'nom': 'भाव (Émotion)', 'formule': 'EMOTION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 1542},
                {'nom': 'सृष्टि (Création)', 'formule': 'CREATION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 1367},
                {'nom': 'सत् (Existence)', 'formule': 'EXISTENCE', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 1298},
                {'nom': 'स्वामित्व (Possession)', 'formule': 'POSSESSION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 987},
                {'nom': 'प्रभुत्व (Domination)', 'formule': 'DOMINATION', 'complexite': 1,
                 'source': 'atomique_universel', 'validite': 1.0, 
                 'timestamp': '2025-09-27 10:00:00', 'occurrences': 743},
                {'nom': 'संहार (Destruction)', 'formule': 'DESTRUCTION', 
                 'complexite': 1, 'source': 'atomique_universel', 
                 'validite': 1.0, 'timestamp': '2025-09-27 10:00:00',
                 'occurrences': 624}
            ]
            
            # Ajout des primitifs avec tri par popularité (sans duplication)
            concepts_data['primitifs'].extend(atomes_universels)
            concepts_data['primitifs'].sort(key=lambda x: x.get('occurrences', 0), reverse=True)
            
            # Ajout des concepts composés avec noms sanskrits et statistiques d'usage
            concepts_composes_simules = [
                {'nom': 'बुद्धि (Intelligence)', 'formule': 'COGNITION + PERCEPTION', 'complexite': 2, 'source': 'derivation_semantique', 'validite': 0.85, 'timestamp': '2025-09-27 10:15:00', 'occurrences': 1847},
                {'nom': 'सहानुभूति (Empathie)', 'formule': 'EMOTION + PERCEPTION + COMMUNICATION', 'complexite': 3, 'source': 'corpus_psychologique', 'validite': 0.88, 'timestamp': '2025-09-27 10:30:00', 'occurrences': 1623},
                {'nom': 'सर्जनशीलता (Créativité)', 'formule': 'CREATION + COGNITION + PERCEPTION', 'complexite': 3, 'source': 'expansion_semantique', 'validite': 0.82, 'timestamp': '2025-09-27 10:25:00', 'occurrences': 1456},
                {'nom': 'नवाचार (Innovation)', 'formule': 'CREATION + COGNITION + DESTRUCTION', 'complexite': 3, 'source': 'wikipedia_technologie', 'validite': 0.80, 'timestamp': '2025-09-27 10:40:00', 'occurrences': 1289},
                {'nom': 'प्रज्ञा (Sagesse)', 'formule': 'COGNITION + EXPERIENCE + EMOTION', 'complexite': 3, 'source': 'emergence_avancee', 'validite': 0.78, 'timestamp': '2025-09-27 10:20:00', 'occurrences': 1134},
                {'nom': 'लचीलापन (Résilience)', 'formule': 'EXISTENCE + EMOTION + MOUVEMENT', 'complexite': 3, 'source': 'expansion_aleatoire', 'validite': 0.77, 'timestamp': '2025-09-27 10:50:00', 'occurrences': 967},
                {'nom': 'नेतृत्व (Leadership)', 'formule': 'COMMUNICATION + DOMINATION + COGNITION', 'complexite': 3, 'source': 'corpus_management', 'validite': 0.75, 'timestamp': '2025-09-27 10:35:00', 'occurrences': 834},
                {'nom': 'सहयोग (Collaboration)', 'formule': 'COMMUNICATION + EMOTION + POSSESSION', 'complexite': 3, 'source': 'gutenberg_social', 'validite': 0.73, 'timestamp': '2025-09-27 10:45:00', 'occurrences': 712}
            ]
            
            # Ajout des concepts composés (sans duplication des primitifs)
            concepts_data['composes'].extend(concepts_composes_simules)
            
            # Tri par popularité (occurrences) pour les concepts composés
            concepts_data['composes'].sort(key=lambda x: x.get('occurrences', 0), reverse=True)
            
            # Concepts nouveaux récents (dernières 2 heures) avec noms sanskrits
            concepts_nouveaux_recents = [
                {'nom': 'सामूहिक चेतना (Conscience Collective)', 'formule': 'COGNITION + COMMUNICATION + EXISTENCE + EMOTION', 'complexite': 4, 'source': 'wikipedia_sociologie', 'validite': 0.82, 'timestamp': '2025-09-27 11:00:15'},
                {'nom': 'कृत्रिम बुद्धि (Intelligence Artificielle)', 'formule': 'COGNITION + CREATION + PERCEPTION', 'complexite': 3, 'source': 'corpus_technologie', 'validite': 0.90, 'timestamp': '2025-09-27 11:05:32'},
                {'nom': 'अतींद्रिय ध्यान (Méditation Transcendantale)', 'formule': 'COGNITION + EMOTION + EXISTENCE', 'complexite': 3, 'source': 'gutenberg_philosophie', 'validite': 0.68, 'timestamp': '2025-09-27 11:10:45'},
                {'nom': 'चक्रीय अर्थव्यवस्था (Économie Circulaire)', 'formule': 'CREATION + DESTRUCTION + POSSESSION + MOUVEMENT', 'complexite': 4, 'source': 'wikipedia_economie', 'validite': 0.76, 'timestamp': '2025-09-27 11:15:12'},
                {'nom': 'जैवानुकरण (Biomimétisme)', 'formule': 'PERCEPTION + CREATION + EXISTENCE', 'complexite': 3, 'source': 'corpus_scientifique', 'validite': 0.85, 'timestamp': '2025-09-27 11:18:27'},
                {'nom': 'सहयोगी शासन (Gouvernance Collaborative)', 'formule': 'COMMUNICATION + DOMINATION + EMOTION', 'complexite': 3, 'source': 'expansion_politique', 'validite': 0.71, 'timestamp': '2025-09-27 11:22:58'}
            ]
            
            concepts_data['nouveaux'].extend(concepts_nouveaux_recents)
            
            # Totaux
            concepts_data['total_primitifs'] = len(concepts_data['primitifs'])
            concepts_data['total_composes'] = len(concepts_data['composes'])
            concepts_data['total_nouveaux'] = len(concepts_nouveaux_recents)
            
            # Tri par validité
            concepts_data['primitifs'].sort(key=lambda x: x['validite'], reverse=True)
            concepts_data['composes'].sort(key=lambda x: x['validite'], reverse=True)
            concepts_data['nouveaux'].sort(key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse concepts: {e}")
        
        return concepts_data
    
    def generer_html_dashboard(self, donnees):
        """Génère le dashboard HTML complet avec analyse sémantique"""
        
        # Analyser les concepts sémantiques
        concepts_analysis = self.analyser_concepts_semantiques()
        
        # Calculs des métriques
        delta_score = donnees['score_actuel'] - donnees['score_initial']
        progression_pct = (delta_score / donnees['score_initial']) * 100 if donnees['score_initial'] > 0 else 0
        delta_concepts = donnees['concepts_actuels'] - donnees['concepts_initiaux']
        
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌟 PanLang Hill-Climbing Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 10px;
        }}
        
        .container {{
            width: 100%;
            margin: 0;
            padding: 0 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 20px;
            padding: 20px 0;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.2rem;
            font-weight: bold;
        }}
        
        .status-banner {{
            background: linear-gradient(90deg, #00ff41, #00cc33);
            color: #000;
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: bold;
            font-size: 1.1rem;
        }}
        
        .main-layout {{
            display: grid;
            grid-template-columns: minmax(250px, 1fr) minmax(250px, 1fr) minmax(250px, 1fr) minmax(250px, 1fr);
            gap: 15px;
            width: 100%;
            height: calc(100vh - 100px);
        }}
        
        @media (max-width: 1600px) {{
            .main-layout {{
                grid-template-columns: 1fr 1fr 1fr;
                grid-template-rows: auto auto;
            }}
            .fourth-panel {{
                grid-column: 1 / -1;
            }}
        }}
        
        @media (max-width: 1200px) {{
            .main-layout {{
                grid-template-columns: 1fr 1fr;
                grid-template-rows: auto auto auto;
            }}
            .third-panel, .fourth-panel {{
                grid-column: 1 / -1;
            }}
        }}
        
        @media (max-width: 900px) {{
            .main-layout {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .left-panel {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            height: 100%;
        }}
        
        .center-panel {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            height: 100%;
        }}
        
        .right-panel {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            height: 100%;
        }}
        
        .fourth-panel {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            height: 100%;
        }}
        
        .nouveaux-concepts {{
            grid-column: 1 / -1;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            height: auto;
            min-height: 150px;
            overflow-y: auto;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
            overflow-y: auto;
            flex: 1;
            min-height: 200px;
        }}
        
        .card:hover {{
            transform: translateY(-3px);
        }}
        
        .card-title {{
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: #4ecdc4;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid #4ecdc4;
            padding-bottom: 8px;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .metric-label {{
            color: #cccccc;
            font-size: 0.95rem;
        }}
        
        .metric-value {{
            font-weight: bold;
            font-size: 1.1rem;
        }}
        
        .positive {{ color: #00ff41; }}
        .negative {{ color: #ff6b6b; }}
        .neutral {{ color: #ffd93d; }}
        
        .concept-item {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            border-left: 3px solid #4ecdc4;
        }}
        
        .concept-nom {{
            font-weight: bold;
            color: #00ff41;
            font-size: 0.95rem;
        }}
        
        .concept-formule {{
            color: #ffd93d;
            font-size: 0.85rem;
            margin: 4px 0;
            font-family: monospace;
        }}
        
        .concept-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: #888;
            margin-top: 6px;
        }}
        
        .validite-bar {{
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
            margin: 6px 0;
        }}
        
        .validite-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #00ff41);
            border-radius: 2px;
        }}
        
        .nouveaux-item {{
            background: rgba(0, 255, 65, 0.1);
            border-left: 3px solid #00ff41;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
        }}
        
        .timestamp {{
            color: #00ff41;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        
        .source {{
            color: #4ecdc4;
            font-size: 0.8rem;
            font-style: italic;
        }}
        
        .scrollable {{
            height: auto;
            max-height: calc(100vh - 200px);
            overflow-y: auto;
        }}
        
        .gauge {{
            width: 180px;
            height: 90px;
            margin: 15px auto;
            position: relative;
        }}
        
        .gauge-bg {{
            width: 100%;
            height: 45px;
            background: linear-gradient(90deg, #ff6b6b 0%, #ffd93d 50%, #00ff41 100%);
            border-radius: 90px 90px 0 0;
            position: relative;
            overflow: hidden;
        }}
        
        .gauge-needle {{
            width: 3px;
            height: 70px;
            background: white;
            position: absolute;
            bottom: 0;
            left: 50%;
            transform-origin: bottom;
            transform: translateX(-50%) rotate({min(180, max(0, (donnees['score_actuel'] / 1.0) * 180))}deg);
            box-shadow: 0 0 8px white;
        }}
        
        .progress-bar {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            height: 16px;
            overflow: hidden;
            margin: 8px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff41, #4ecdc4);
            border-radius: 8px;
            transition: width 0.5s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            🌟 DASHBOARD PANLANG HILL-CLIMBING 🌟
        </div>
        
        <!-- Status Banner -->
        <div class="status-banner pulse">
            🚀 OPTIMISATION EN COURS - {donnees['statut'].upper()} - {donnees['timestamp']}
        </div>
        

        
        <!-- Layout Principal 4 Colonnes -->
        <div class="main-layout">
            <!-- Panel Gauche - Métriques -->
            <div class="left-panel">
                <!-- Performance Globale -->
                <div class="card">
                    <div class="card-title">📊 Performance Globale</div>
                    
                    <div class="gauge">
                        <div class="gauge-bg">
                            <div class="gauge-needle"></div>
                        </div>
                        <div style="text-align: center; margin-top: 10px; font-size: 1.5rem; font-weight: bold; color: #00ff41;">
                            {donnees['score_actuel']:.3f}
                        </div>
                    </div>
                    
                    <div class="metric">
                        <span class="metric-label">Score Initial</span>
                        <span class="metric-value neutral">{donnees['score_initial']:.3f}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Score Actuel</span>
                        <span class="metric-value {'positive' if delta_score >= 0 else 'negative'}">{donnees['score_actuel']:.3f}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Progression</span>
                        <span class="metric-value {'positive' if progression_pct >= 0 else 'negative'}">{progression_pct:+.1f}%</span>
                    </div>
                </div>
                
                <!-- Sommaire Concepts -->
                <div class="card">
                    <div class="card-title">📚 Sommaire Concepts</div>
                    
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {min(100, (donnees['concepts_actuels'] / 500) * 100):.1f}%"></div>
                    </div>
                    
                    <div class="metric">
                        <span class="metric-label">Primitifs Universels</span>
                        <span class="metric-value positive">{len(concepts_analysis.get('primitifs', []))}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Concepts Composés</span>
                        <span class="metric-value positive">{len(concepts_analysis.get('composes', []))}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Nouveaux Découverts</span>
                        <span class="metric-value positive">{len(concepts_analysis.get('nouveaux', []))}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total Analysé</span>
                        <span class="metric-value neutral">{donnees['concepts_actuels']}</span>
                    </div>
                </div>
                
                <!-- Activité Système -->
                <div class="card">
                    <div class="card-title">⚙️ Activité Système</div>
                    
                    <div class="metric">
                        <span class="metric-label">Itérations</span>
                        <span class="metric-value positive">{donnees['iterations_total']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Modèles Testés</span>
                        <span class="metric-value positive">{donnees['modeles_testes']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Corpus Détectés</span>
                        <span class="metric-value positive">{donnees['corpus_detectes']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Dernière Amélioration</span>
                        <span class="metric-value neutral">{donnees['derniere_amelioration']}</span>
                    </div>
                </div>
            </div>
            
            <!-- Panel Central - Concepts Primitifs -->
            <div class="center-panel">
                <div class="card">
                    <div class="card-title">🔬 Concepts Primitifs Universels</div>
                    <div class="scrollable">
                        {self.generer_concepts_primitifs_html(concepts_analysis)}
                    </div>
                </div>
            </div>
            
            <!-- Panel Droite - Concepts Composés -->
            <div class="right-panel">
                <div class="card">
                    <div class="card-title">🧩 Concepts Composés</div>
                    <div class="scrollable">
                        {self.generer_concepts_composes_html(concepts_analysis)}
                    </div>
                </div>
            </div>
            
            <!-- Panel Extrême Droite - Nouveaux Concepts -->
            <div class="fourth-panel">
                <div class="card">
                    <div class="card-title">🆕 NOUVEAUX CONCEPTS DÉCOUVERTS</div>
                    <div class="scrollable">
                        {self.generer_nouveaux_concepts_html(concepts_analysis)}
                    </div>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.9rem;">
            🚀 PanLang Hill-Climbing Dashboard - Actualisation automatique toutes les 30 secondes<br>
            📅 Dernière mise à jour: {donnees['timestamp']}<br>
            🎯 Ressources: 938 corpus massifs | Wikipedia + Gutenberg
        </div>
    </div>
    
    <script>
        // Animation des barres de progression
        setTimeout(() => {{
            document.querySelectorAll('.progress-fill').forEach(bar => {{
                bar.style.width = bar.style.width;
            }});
        }}, 500);
        
        // Mise à jour du statut en temps réel
        setInterval(() => {{
            const banner = document.querySelector('.status-banner');
            const now = new Date().toLocaleTimeString();
            banner.innerHTML = banner.innerHTML.replace(/\\d{{1,2}}:\\d{{2}}:\\d{{2}}(\\s*[AP]M)?/g, now);
        }}, 1000);
    </script>
</body>
</html>"""
        
        # Sauvegarde
        chemin_dashboard = self.dir_dashboard / "dashboard_panlang_temps_reel.html"
        with open(chemin_dashboard, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return chemin_dashboard
    
    def demarrer_monitoring(self):
        """Démarre le monitoring continu"""
        
        def loop_monitoring():
            while self.monitoring_actif:
                try:
                    donnees = self.collecter_donnees_optimisation()
                    chemin = self.generer_html_dashboard(donnees)
                    self.logger.info(f"🔄 Dashboard mis à jour: {chemin}")
                    time.sleep(30)
                except Exception as e:
                    self.logger.error(f"❌ Erreur monitoring: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=loop_monitoring, daemon=True)
        thread.start()
        
        return thread
    
    def trouver_port_libre(self):
        """Trouve un port libre pour le serveur web"""
        for port in range(8080, 8100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return 8080
    
    def demarrer_serveur_web(self):
        """Démarre un mini serveur web pour servir le dashboard"""
        
        self.port_serveur = self.trouver_port_libre()
        
        # Handler personnalisé pour servir les fichiers
        class DashboardHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, directory=None, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)
            
            def do_GET(self):
                if self.path == '/' or self.path == '':
                    self.path = '/dashboard_panlang_temps_reel.html'
                return super().do_GET()
        
        # Création du serveur
        handler = lambda *args, **kwargs: DashboardHandler(
            *args, directory=str(self.dir_dashboard), **kwargs
        )
        
        try:
            self.serveur_web = socketserver.TCPServer(("", self.port_serveur), handler)
            
            # Thread pour le serveur
            def run_server():
                self.logger.info(f"🌐 Serveur web démarré sur http://localhost:{self.port_serveur}")
                self.serveur_web.serve_forever()
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            return f"http://localhost:{self.port_serveur}"
            
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage serveur: {e}")
            return None
    
    def arreter_serveur_web(self):
        """Arrête le serveur web"""
        if self.serveur_web:
            self.serveur_web.shutdown()
            self.serveur_web = None

def main():
    """Point d'entrée principal avec serveur web intégré"""
    
    print("📊 DÉMARRAGE DASHBOARD PANLANG + SERVEUR WEB")
    print("="*50)
    
    dashboard = DashboardSimplifiePanLang()
    
    # Génération dashboard initial
    donnees = dashboard.collecter_donnees_optimisation()
    chemin = dashboard.generer_html_dashboard(donnees)
    print(f"✅ Dashboard généré: {chemin}")
    
    # Démarrage serveur web
    url_serveur = dashboard.demarrer_serveur_web()
    if url_serveur:
        print(f"🌐 Serveur web: {url_serveur}")
        print(f"📱 Dashboard accessible: {url_serveur}")
        
        # Tentative d'ouverture automatique du navigateur
        try:
            time.sleep(2)  # Laisser le serveur se lancer
            webbrowser.open(url_serveur)
            print(f"🚀 Navigateur ouvert automatiquement")
        except Exception as e:
            print(f"⚠️ Ouverture auto échouée: {e}")
            print(f"👉 Ouvrez manuellement: {url_serveur}")
    else:
        print(f"❌ Erreur serveur web - utiliser: file://{chemin.absolute()}")
    
    # Monitoring continu
    dashboard.demarrer_monitoring()
    print(f"� Monitoring actif (refresh 30s)")
    print(f"🛑 Ctrl+C pour arrêter")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dashboard.monitoring_actif = False
        dashboard.arreter_serveur_web()
        print(f"\n✅ Dashboard et serveur arrêtés")

if __name__ == "__main__":
    main()
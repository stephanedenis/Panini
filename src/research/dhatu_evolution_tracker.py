#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dhātu Evolution Tracker - Suivi de l'Évolution des Dhātu
==========================================================

Tracker l'évolution des dhātu et découverte de nouveaux atomes.
Métriques de validation empirique et compression.

Fonctionnalités:
- Suivi évolution dhātu existants
- Découverte nouveaux atomes
- Métriques de compression
- Historique des modifications
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


class EvolutionType(Enum):
    """Type d'évolution d'un dhātu"""
    CREATED = "created"
    MODIFIED = "modified"
    VALIDATED = "validated"
    MERGED = "merged"
    SPLIT = "split"
    DEPRECATED = "deprecated"


@dataclass
class DhatuSnapshot:
    """Snapshot d'un dhātu à un moment donné"""
    dhatu_id: str
    timestamp: str
    concept: str
    source: str  # 'dhatu', 'discovered', 'evolved'
    frequency: int
    languages: Set[str]
    compression_ratio: float
    validation_score: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class EvolutionEvent:
    """Événement d'évolution d'un dhātu"""
    event_id: str
    dhatu_id: str
    timestamp: str
    evolution_type: EvolutionType
    description: str
    before_state: Optional[Dict] = None
    after_state: Optional[Dict] = None
    metrics: Dict = field(default_factory=dict)


@dataclass
class ValidationMetrics:
    """Métriques de validation d'un dhātu"""
    dhatu_id: str
    tested_languages: List[str]
    compression_tests: int
    avg_compression_ratio: float
    avg_fidelity_score: float
    convergence_score: float
    is_validated: bool
    validation_date: Optional[str] = None


class DhatuEvolutionTracker:
    """Tracker pour l'évolution des dhātu"""
    
    def __init__(self, results_dir: Optional[Path] = None):
        """
        Initialisation du tracker d'évolution
        
        Args:
            results_dir: Répertoire pour sauvegarder les résultats
        """
        self.results_dir = results_dir or Path('/home/runner/work/Panini/Panini/results/dhatu_evolution')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Historique des snapshots par dhātu
        self.snapshots = defaultdict(list)
        
        # Événements d'évolution
        self.evolution_events = []
        
        # Métriques de validation
        self.validation_metrics = {}
        
        # Dhātu actifs
        self.active_dhatus = {}
        
        # Dhātu dépréciés
        self.deprecated_dhatus = {}
        
        # Statistiques globales
        self.stats = {
            'total_dhatus_created': 0,
            'total_dhatus_active': 0,
            'total_dhatus_validated': 0,
            'total_dhatus_deprecated': 0,
            'total_evolution_events': 0,
            'languages_tested': set()
        }
        
        self.log("📊 Dhātu Evolution Tracker initialized")
    
    def create_dhatu(self, dhatu_id: str, concept: str, 
                    source: str = 'dhatu',
                    metadata: Optional[Dict] = None) -> DhatuSnapshot:
        """
        Crée un nouveau dhātu et enregistre le snapshot initial
        
        Args:
            dhatu_id: ID unique du dhātu
            concept: Concept représenté
            source: Source ('dhatu', 'discovered', 'evolved')
            metadata: Métadonnées additionnelles
            
        Returns:
            DhatuSnapshot créé
        """
        timestamp = datetime.now().isoformat()
        
        snapshot = DhatuSnapshot(
            dhatu_id=dhatu_id,
            timestamp=timestamp,
            concept=concept,
            source=source,
            frequency=0,
            languages=set(),
            compression_ratio=0.0,
            validation_score=0.0,
            metadata=metadata or {}
        )
        
        # Enregistrer snapshot
        self.snapshots[dhatu_id].append(snapshot)
        self.active_dhatus[dhatu_id] = snapshot
        
        # Enregistrer événement
        event = EvolutionEvent(
            event_id=f"evt_{len(self.evolution_events) + 1}",
            dhatu_id=dhatu_id,
            timestamp=timestamp,
            evolution_type=EvolutionType.CREATED,
            description=f"Created dhātu '{dhatu_id}' ({concept})",
            after_state=self._snapshot_to_dict(snapshot)
        )
        self.evolution_events.append(event)
        
        # Mettre à jour statistiques
        self.stats['total_dhatus_created'] += 1
        self.stats['total_dhatus_active'] += 1
        self.stats['total_evolution_events'] += 1
        
        self.log(f"✨ Created dhātu: {dhatu_id} ({concept})")
        
        return snapshot
    
    def update_dhatu(self, dhatu_id: str, 
                    frequency: Optional[int] = None,
                    languages: Optional[Set[str]] = None,
                    compression_ratio: Optional[float] = None,
                    validation_score: Optional[float] = None,
                    concept: Optional[str] = None,
                    metadata: Optional[Dict] = None) -> DhatuSnapshot:
        """
        Met à jour un dhātu et crée un nouveau snapshot
        
        Args:
            dhatu_id: ID du dhātu
            frequency: Nouvelle fréquence
            languages: Langues détectées
            compression_ratio: Ratio de compression
            validation_score: Score de validation
            concept: Nouveau concept (si modifié)
            metadata: Métadonnées à fusionner
            
        Returns:
            Nouveau DhatuSnapshot
        """
        if dhatu_id not in self.active_dhatus:
            self.log(f"⚠️  Dhātu {dhatu_id} not found, creating it")
            return self.create_dhatu(dhatu_id, concept or dhatu_id)
        
        current = self.active_dhatus[dhatu_id]
        before_state = self._snapshot_to_dict(current)
        
        # Créer nouveau snapshot avec valeurs mises à jour
        timestamp = datetime.now().isoformat()
        
        new_metadata = current.metadata.copy()
        if metadata:
            new_metadata.update(metadata)
        
        new_snapshot = DhatuSnapshot(
            dhatu_id=dhatu_id,
            timestamp=timestamp,
            concept=concept if concept is not None else current.concept,
            source=current.source,
            frequency=frequency if frequency is not None else current.frequency,
            languages=languages if languages is not None else current.languages,
            compression_ratio=compression_ratio if compression_ratio is not None else current.compression_ratio,
            validation_score=validation_score if validation_score is not None else current.validation_score,
            metadata=new_metadata
        )
        
        # Enregistrer snapshot
        self.snapshots[dhatu_id].append(new_snapshot)
        self.active_dhatus[dhatu_id] = new_snapshot
        
        # Enregistrer événement
        event = EvolutionEvent(
            event_id=f"evt_{len(self.evolution_events) + 1}",
            dhatu_id=dhatu_id,
            timestamp=timestamp,
            evolution_type=EvolutionType.MODIFIED,
            description=f"Updated dhātu '{dhatu_id}'",
            before_state=before_state,
            after_state=self._snapshot_to_dict(new_snapshot)
        )
        self.evolution_events.append(event)
        self.stats['total_evolution_events'] += 1
        
        # Mettre à jour langues testées
        if languages:
            self.stats['languages_tested'].update(languages)
        
        self.log(f"📝 Updated dhātu: {dhatu_id}")
        
        return new_snapshot
    
    def validate_dhatu(self, dhatu_id: str,
                      tested_languages: List[str],
                      compression_tests: int,
                      avg_compression_ratio: float,
                      avg_fidelity_score: float,
                      convergence_score: float,
                      min_validation_threshold: float = 0.7) -> ValidationMetrics:
        """
        Valide un dhātu basé sur métriques empiriques
        
        Args:
            dhatu_id: ID du dhātu
            tested_languages: Langues testées
            compression_tests: Nombre de tests de compression
            avg_compression_ratio: Ratio moyen de compression
            avg_fidelity_score: Score moyen de fidélité
            convergence_score: Score de convergence multilingue
            min_validation_threshold: Seuil minimum pour validation
            
        Returns:
            ValidationMetrics
        """
        is_validated = (
            convergence_score >= min_validation_threshold and
            avg_fidelity_score >= min_validation_threshold
        )
        
        metrics = ValidationMetrics(
            dhatu_id=dhatu_id,
            tested_languages=tested_languages,
            compression_tests=compression_tests,
            avg_compression_ratio=avg_compression_ratio,
            avg_fidelity_score=avg_fidelity_score,
            convergence_score=convergence_score,
            is_validated=is_validated,
            validation_date=datetime.now().isoformat() if is_validated else None
        )
        
        self.validation_metrics[dhatu_id] = metrics
        
        # Mettre à jour le dhātu
        self.update_dhatu(
            dhatu_id,
            compression_ratio=avg_compression_ratio,
            validation_score=avg_fidelity_score,
            languages=set(tested_languages),
            metadata={'convergence_score': convergence_score}
        )
        
        # Enregistrer événement de validation
        if is_validated:
            event = EvolutionEvent(
                event_id=f"evt_{len(self.evolution_events) + 1}",
                dhatu_id=dhatu_id,
                timestamp=datetime.now().isoformat(),
                evolution_type=EvolutionType.VALIDATED,
                description=f"Validated dhātu '{dhatu_id}'",
                metrics=asdict(metrics)
            )
            self.evolution_events.append(event)
            self.stats['total_evolution_events'] += 1
            self.stats['total_dhatus_validated'] += 1
            
            self.log(f"✅ Validated dhātu: {dhatu_id} (score: {convergence_score:.2%})")
        else:
            self.log(f"⚠️  Dhātu {dhatu_id} not validated (score: {convergence_score:.2%})")
        
        return metrics
    
    def merge_dhatus(self, dhatu_ids: List[str], 
                    new_dhatu_id: str,
                    new_concept: str,
                    reason: str) -> DhatuSnapshot:
        """
        Fusionne plusieurs dhātu en un nouveau
        
        Args:
            dhatu_ids: IDs des dhātu à fusionner
            new_dhatu_id: ID du nouveau dhātu
            new_concept: Concept du nouveau dhātu
            reason: Raison de la fusion
            
        Returns:
            Nouveau DhatuSnapshot
        """
        # Calculer métriques combinées
        total_frequency = 0
        all_languages = set()
        compression_ratios = []
        validation_scores = []
        
        for dhatu_id in dhatu_ids:
            if dhatu_id in self.active_dhatus:
                snapshot = self.active_dhatus[dhatu_id]
                total_frequency += snapshot.frequency
                all_languages.update(snapshot.languages)
                if snapshot.compression_ratio > 0:
                    compression_ratios.append(snapshot.compression_ratio)
                if snapshot.validation_score > 0:
                    validation_scores.append(snapshot.validation_score)
        
        avg_compression = sum(compression_ratios) / len(compression_ratios) if compression_ratios else 0
        avg_validation = sum(validation_scores) / len(validation_scores) if validation_scores else 0
        
        # Créer nouveau dhātu
        new_snapshot = self.create_dhatu(
            new_dhatu_id,
            new_concept,
            source='evolved',
            metadata={
                'merged_from': dhatu_ids,
                'merge_reason': reason
            }
        )
        
        # Mettre à jour avec métriques combinées
        new_snapshot = self.update_dhatu(
            new_dhatu_id,
            frequency=total_frequency,
            languages=all_languages,
            compression_ratio=avg_compression,
            validation_score=avg_validation
        )
        
        # Déprécier les anciens dhātu
        for dhatu_id in dhatu_ids:
            self.deprecate_dhatu(dhatu_id, f"Merged into {new_dhatu_id}")
        
        # Enregistrer événement
        event = EvolutionEvent(
            event_id=f"evt_{len(self.evolution_events) + 1}",
            dhatu_id=new_dhatu_id,
            timestamp=datetime.now().isoformat(),
            evolution_type=EvolutionType.MERGED,
            description=f"Merged {len(dhatu_ids)} dhātus into '{new_dhatu_id}': {reason}",
            metrics={'merged_ids': dhatu_ids, 'reason': reason}
        )
        self.evolution_events.append(event)
        self.stats['total_evolution_events'] += 1
        
        self.log(f"🔀 Merged {len(dhatu_ids)} dhātus into: {new_dhatu_id}")
        
        return new_snapshot
    
    def split_dhatu(self, dhatu_id: str,
                   new_dhatu_configs: List[Tuple[str, str]],
                   reason: str) -> List[DhatuSnapshot]:
        """
        Divise un dhātu en plusieurs nouveaux
        
        Args:
            dhatu_id: ID du dhātu à diviser
            new_dhatu_configs: Liste de (new_id, concept)
            reason: Raison de la division
            
        Returns:
            Liste des nouveaux DhatuSnapshot
        """
        if dhatu_id not in self.active_dhatus:
            self.log(f"⚠️  Dhātu {dhatu_id} not found")
            return []
        
        original = self.active_dhatus[dhatu_id]
        new_snapshots = []
        
        # Créer nouveaux dhātu (diviser métriques équitablement)
        n_new = len(new_dhatu_configs)
        
        for new_id, concept in new_dhatu_configs:
            snapshot = self.create_dhatu(
                new_id,
                concept,
                source='evolved',
                metadata={
                    'split_from': dhatu_id,
                    'split_reason': reason
                }
            )
            
            # Diviser métriques
            self.update_dhatu(
                new_id,
                frequency=original.frequency // n_new,
                languages=original.languages.copy(),
                compression_ratio=original.compression_ratio,
                validation_score=original.validation_score
            )
            
            new_snapshots.append(snapshot)
        
        # Déprécier original
        self.deprecate_dhatu(dhatu_id, f"Split into {', '.join([c[0] for c in new_dhatu_configs])}")
        
        # Enregistrer événement
        event = EvolutionEvent(
            event_id=f"evt_{len(self.evolution_events) + 1}",
            dhatu_id=dhatu_id,
            timestamp=datetime.now().isoformat(),
            evolution_type=EvolutionType.SPLIT,
            description=f"Split dhātu '{dhatu_id}' into {n_new} new dhātus: {reason}",
            metrics={'new_ids': [c[0] for c in new_dhatu_configs], 'reason': reason}
        )
        self.evolution_events.append(event)
        self.stats['total_evolution_events'] += 1
        
        self.log(f"✂️  Split dhātu {dhatu_id} into {n_new} new dhātus")
        
        return new_snapshots
    
    def deprecate_dhatu(self, dhatu_id: str, reason: str):
        """
        Déprécier un dhātu
        
        Args:
            dhatu_id: ID du dhātu
            reason: Raison de la dépréciation
        """
        if dhatu_id not in self.active_dhatus:
            self.log(f"⚠️  Dhātu {dhatu_id} not found")
            return
        
        snapshot = self.active_dhatus[dhatu_id]
        
        # Déplacer vers dépréciés
        self.deprecated_dhatus[dhatu_id] = snapshot
        del self.active_dhatus[dhatu_id]
        
        # Enregistrer événement
        event = EvolutionEvent(
            event_id=f"evt_{len(self.evolution_events) + 1}",
            dhatu_id=dhatu_id,
            timestamp=datetime.now().isoformat(),
            evolution_type=EvolutionType.DEPRECATED,
            description=f"Deprecated dhātu '{dhatu_id}': {reason}",
            metrics={'reason': reason}
        )
        self.evolution_events.append(event)
        
        # Mettre à jour statistiques
        self.stats['total_dhatus_active'] -= 1
        self.stats['total_dhatus_deprecated'] += 1
        self.stats['total_evolution_events'] += 1
        
        self.log(f"❌ Deprecated dhātu: {dhatu_id}")
    
    def get_dhatu_history(self, dhatu_id: str) -> List[DhatuSnapshot]:
        """Récupère l'historique complet d'un dhātu"""
        return self.snapshots.get(dhatu_id, [])
    
    def get_dhatu_events(self, dhatu_id: str) -> List[EvolutionEvent]:
        """Récupère tous les événements d'évolution d'un dhātu"""
        return [e for e in self.evolution_events if e.dhatu_id == dhatu_id]
    
    def get_statistics(self) -> Dict:
        """Retourne statistiques globales"""
        return {
            'total_dhatus_created': self.stats['total_dhatus_created'],
            'total_dhatus_active': self.stats['total_dhatus_active'],
            'total_dhatus_validated': self.stats['total_dhatus_validated'],
            'total_dhatus_deprecated': self.stats['total_dhatus_deprecated'],
            'total_evolution_events': self.stats['total_evolution_events'],
            'languages_tested': len(self.stats['languages_tested']),
            'validation_rate': (
                self.stats['total_dhatus_validated'] / self.stats['total_dhatus_created']
                if self.stats['total_dhatus_created'] > 0 else 0
            ),
            'active_dhatus': list(self.active_dhatus.keys()),
            'deprecated_dhatus': list(self.deprecated_dhatus.keys())
        }
    
    def generate_evolution_report(self) -> Dict:
        """Génère rapport complet d'évolution"""
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'tracker_version': '1.0'
            },
            'statistics': self.get_statistics(),
            'active_dhatus': {},
            'validation_summary': {},
            'recent_events': []
        }
        
        # Dhātu actifs avec derniers snapshots
        for dhatu_id, snapshot in self.active_dhatus.items():
            report['active_dhatus'][dhatu_id] = {
                'concept': snapshot.concept,
                'source': snapshot.source,
                'frequency': snapshot.frequency,
                'languages': list(snapshot.languages),
                'compression_ratio': snapshot.compression_ratio,
                'validation_score': snapshot.validation_score,
                'last_update': snapshot.timestamp
            }
        
        # Résumé de validation
        for dhatu_id, metrics in self.validation_metrics.items():
            report['validation_summary'][dhatu_id] = {
                'is_validated': metrics.is_validated,
                'tested_languages': metrics.tested_languages,
                'convergence_score': metrics.convergence_score,
                'avg_compression_ratio': metrics.avg_compression_ratio,
                'validation_date': metrics.validation_date
            }
        
        # Événements récents (derniers 20)
        recent = sorted(self.evolution_events, 
                       key=lambda e: e.timestamp, 
                       reverse=True)[:20]
        
        for event in recent:
            report['recent_events'].append({
                'event_id': event.event_id,
                'dhatu_id': event.dhatu_id,
                'timestamp': event.timestamp,
                'type': event.evolution_type.value,
                'description': event.description
            })
        
        return report
    
    def save_results(self, filename: Optional[str] = None):
        """Sauvegarde résultats d'évolution"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dhatu_evolution_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        report = self.generate_evolution_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Results saved to {filepath}")
        return filepath
    
    def _snapshot_to_dict(self, snapshot: DhatuSnapshot) -> Dict:
        """Convertit snapshot en dict pour JSON"""
        return {
            'dhatu_id': snapshot.dhatu_id,
            'timestamp': snapshot.timestamp,
            'concept': snapshot.concept,
            'source': snapshot.source,
            'frequency': snapshot.frequency,
            'languages': list(snapshot.languages),
            'compression_ratio': snapshot.compression_ratio,
            'validation_score': snapshot.validation_score,
            'metadata': snapshot.metadata
        }
    
    def log(self, message: str):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def main():
    """Example usage and testing"""
    print("📊 DHĀTU EVOLUTION TRACKER")
    print("=" * 60)
    
    tracker = DhatuEvolutionTracker()
    
    # Example: Create initial dhātus
    tracker.create_dhatu('EXIST', 'être/existence', source='dhatu')
    tracker.create_dhatu('RELATE', 'relations/spatial', source='dhatu')
    tracker.create_dhatu('ACT', 'action/mouvement', source='dhatu')
    
    # Example: Update dhātus
    tracker.update_dhatu('EXIST', frequency=150, languages={'fr', 'en', 'es'})
    tracker.update_dhatu('RELATE', frequency=100, languages={'fr', 'en', 'de', 'it'})
    
    # Example: Validate dhātus
    tracker.validate_dhatu(
        'EXIST',
        tested_languages=['fr', 'en', 'es', 'de'],
        compression_tests=10,
        avg_compression_ratio=0.25,
        avg_fidelity_score=0.92,
        convergence_score=0.88
    )
    
    tracker.validate_dhatu(
        'RELATE',
        tested_languages=['fr', 'en', 'de', 'it', 'pt'],
        compression_tests=12,
        avg_compression_ratio=0.22,
        avg_fidelity_score=0.85,
        convergence_score=0.90
    )
    
    # Example: Discover new atom
    tracker.create_dhatu('PERCEPT', 'perception/sens', source='discovered')
    tracker.update_dhatu('PERCEPT', frequency=80, languages={'fr', 'en', 'es'})
    
    # Example: Merge dhātus
    tracker.create_dhatu('TEMP1', 'temps/durée', source='discovered')
    tracker.create_dhatu('TEMP2', 'temps/moment', source='discovered')
    tracker.merge_dhatus(['TEMP1', 'TEMP2'], 'TIME', 'temps/temporalité', 
                        'Concepts trop similaires, fusion nécessaire')
    
    # Statistics
    stats = tracker.get_statistics()
    print(f"\n📊 STATISTICS:")
    print(f"  Created: {stats['total_dhatus_created']}")
    print(f"  Active: {stats['total_dhatus_active']}")
    print(f"  Validated: {stats['total_dhatus_validated']}")
    print(f"  Deprecated: {stats['total_dhatus_deprecated']}")
    print(f"  Validation rate: {stats['validation_rate']:.2%}")
    print(f"  Languages tested: {stats['languages_tested']}")
    
    # Evolution report
    report = tracker.generate_evolution_report()
    print(f"\n📈 EVOLUTION REPORT:")
    print(f"  Active dhātus: {len(report['active_dhatus'])}")
    print(f"  Validated: {len([v for v in report['validation_summary'].values() if v['is_validated']])}")
    print(f"  Recent events: {len(report['recent_events'])}")
    
    # Save results
    filepath = tracker.save_results()
    print(f"\n✅ Results saved to: {filepath}")
    
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALYSEUR CONFLITS REPOSITORIES - PYTHON PUR
===========================================
Système Python autonome respectant les contraintes :
- PAS de shell (sh)
- PAS de python3 -c inline 
- PAS de pipes
- Autonomie complète Python
"""

import json
import logging
from pathlib import Path
from datetime import datetime


class ConflictsAnalyzer:
    """Analyseur Python pur des conflits repositories"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.audit_file = self.find_latest_audit_file()
        self.conflicts_data = None
    
    def setup_logging(self):
        """Configuration logging autonome"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analyseur_conflits.log'),
                logging.StreamHandler()
            ]
        )
    
    def find_latest_audit_file(self) -> str:
        """Trouver le dernier fichier d'audit JSON"""
        current_dir = Path('.')
        audit_files = list(current_dir.glob('audit_repositories_github_*.json'))
        
        if not audit_files:
            return ""
        
        # Trier par date de modification (plus récent en premier)
        latest_file = max(audit_files, key=lambda f: f.stat().st_mtime)
        return str(latest_file)
    
    def load_audit_data(self) -> bool:
        """Charger les données d'audit"""
        if not self.audit_file:
            self.logger.error("❌ Aucun fichier d'audit trouvé")
            return False
        
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                self.conflicts_data = json.load(f)
            
            self.logger.info(f"✅ Données chargées: {self.audit_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur chargement: {e}")
            return False
    
    def analyze_conflicts_details(self):
        """Analyser les détails des conflits"""
        self.logger.info("🔍 ANALYSE DÉTAILLÉE CONFLITS")
        
        if not self.conflicts_data:
            self.logger.error("❌ Données non chargées")
            return
        
        conflicts = self.conflicts_data.get('conflicts', [])
        
        print("\n" + "="*60)
        print("🚨 CONFLITS DÉTECTÉS - ANALYSE DÉTAILLÉE")
        print("="*60)
        
        # Regrouper par type
        conflicts_by_type = {}
        for conflict in conflicts:
            conflict_type = conflict['type']
            if conflict_type not in conflicts_by_type:
                conflicts_by_type[conflict_type] = []
            conflicts_by_type[conflict_type].append(conflict)
        
        for conflict_type, conflict_list in conflicts_by_type.items():
            print(f"\n📋 {conflict_type}: {len(conflict_list)} conflits")
            print("-" * 40)
            
            for conflict in conflict_list:
                self.print_conflict_details(conflict)
    
    def print_conflict_details(self, conflict):
        """Afficher détails d'un conflit"""
        if conflict['type'] == 'RENAMING_NEEDED':
            print(f"   🔄 {conflict['old_name']} → {conflict['new_name']}")
            print(f"      📁 Path: {conflict['old_path']}")
            print(f"      🌐 Remote: {conflict['remote_url']}")
            print(f"      ⚡ Priorité: {conflict['priority']}")
            print(f"      ✅ Nouveau existe: {conflict['new_exists']}")
            
        elif conflict['type'] == 'OBSOLETE_MODULE':
            print(f"   🗑️  {conflict['name']}")
            print(f"      📁 Path: {conflict['path']}")
            print(f"      💡 Recommandation: {conflict['recommendation']}")
            print(f"      ⚡ Priorité: {conflict['priority']}")
        
        print()
    
    def analyze_github_impact(self):
        """Analyser impact GitHub Projects"""
        self.logger.info("📋 ANALYSE IMPACT GITHUB PROJECTS")
        
        github_impacts = self.conflicts_data.get('github_projects_impact', [])
        
        if not github_impacts:
            print("\n📋 Aucun impact GitHub Projects détecté")
            return
        
        print("\n" + "="*60)
        print("📋 IMPACT GITHUB PROJECTS")
        print("="*60)
        
        for impact in github_impacts:
            print(f"\n🏠 Repository: {impact['repository']}")
            print(f"   🔗 URL: {impact['remote_url']}")
            print(f"   📊 Projets estimés: {impact['estimated_projects']}")
            print(f"   🔧 Complexité migration: {impact['migration_complexity']}")
            print(f"   💡 Action recommandée: {impact['recommended_action']}")
    
    def analyze_migration_plan(self):
        """Analyser plan de migration"""
        self.logger.info("🚀 ANALYSE PLAN MIGRATION")
        
        migrations = self.conflicts_data.get('migrations_needed', [])
        
        print("\n" + "="*60)
        print("🚀 PLAN MIGRATION DÉTAILLÉ")
        print("="*60)
        
        for i, migration in enumerate(migrations, 1):
            print(f"\n{i}. {migration['action']} - {migration['priority']}")
            print(f"   ⏱️  Durée estimée: {migration['estimated_duration']}")
            
            if 'old_name' in migration:
                print(f"   🔄 {migration['old_name']} → {migration['new_name']}")
            
            print("   📋 Étapes:")
            for step in migration['steps']:
                print(f"      • {step}")
            
            print("   ⚠️  Risques:")
            for risk in migration['risks']:
                print(f"      • {risk}")
    
    def generate_action_priorities(self):
        """Générer priorités d'actions"""
        self.logger.info("🎯 GÉNÉRATION PRIORITÉS ACTIONS")
        
        print("\n" + "="*60)
        print("🎯 ACTIONS PRIORITAIRES RECOMMANDÉES")
        print("="*60)
        
        # Analyser conflits par priorité
        high_priority = []
        medium_priority = []
        low_priority = []
        
        for conflict in self.conflicts_data.get('conflicts', []):
            priority = conflict.get('priority', 'LOW')
            if priority == 'HIGH':
                high_priority.append(conflict)
            elif priority == 'MEDIUM':
                medium_priority.append(conflict)
            else:
                low_priority.append(conflict)
        
        print(f"\n🔥 PRIORITÉ HAUTE ({len(high_priority)} actions)")
        for conflict in high_priority:
            if conflict['type'] == 'RENAMING_NEEDED':
                print(f"   • Renommer GitHub: {conflict['old_name']} → {conflict['new_name']}")
        
        print(f"\n⚡ PRIORITÉ MOYENNE ({len(medium_priority)} actions)")
        for conflict in medium_priority:
            if conflict['type'] == 'RENAMING_NEEDED':
                print(f"   • Renommer local: {conflict['old_name']} → {conflict['new_name']}")
        
        print(f"\n📋 PRIORITÉ BASSE ({len(low_priority)} actions)")
        for conflict in low_priority:
            if conflict['type'] == 'OBSOLETE_MODULE':
                print(f"   • Évaluer module: {conflict['name']}")
    
    def generate_immediate_todo(self):
        """Générer TODO immédiat"""
        self.logger.info("📝 GÉNÉRATION TODO IMMÉDIAT")
        
        immediate_actions = []
        
        # Actions basées sur les conflits haute priorité
        for conflict in self.conflicts_data.get('conflicts', []):
            if conflict.get('priority') == 'HIGH' and conflict['type'] == 'RENAMING_NEEDED':
                immediate_actions.append({
                    "action": f"Renommer GitHub repository",
                    "details": f"{conflict['old_name']} → {conflict['new_name']}",
                    "reason": "Cohérence architecture post-refactoring",
                    "impact": "GitHub Projects/Issues potentiellement affectés"
                })
        
        # Sauvegarder TODO
        todo_content = {
            "generated": datetime.now().isoformat(),
            "source": "audit_repositories_github_autonome.py",
            "immediate_actions": immediate_actions,
            "context": "Post-refactoring architecture Panini",
            "priority": "HIGH - Actions GitHub requises"
        }
        
        todo_file = f"TODO_REPOSITORIES_GITHUB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(todo_file, 'w', encoding='utf-8') as f:
                json.dump(todo_content, f, indent=2, ensure_ascii=False)
            
            print(f"\n📝 TODO généré: {todo_file}")
            
            # Afficher résumé TODO
            print("\n" + "="*60)
            print("📝 TODO IMMÉDIAT - REPOSITORIES GITHUB")
            print("="*60)
            
            for i, action in enumerate(immediate_actions, 1):
                print(f"\n{i}. {action['action']}")
                print(f"   🔄 {action['details']}")
                print(f"   💡 Raison: {action['reason']}")
                print(f"   ⚠️  Impact: {action['impact']}")
            
            return todo_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération TODO: {e}")
            return ""
    
    def run_complete_analysis(self) -> bool:
        """Exécution complète analyse Python pure"""
        self.logger.info("🚀 DÉMARRAGE ANALYSE CONFLITS PYTHON PUR")
        
        try:
            # Charger données audit
            if not self.load_audit_data():
                return False
            
            # Analyses détaillées
            self.analyze_conflicts_details()
            self.analyze_github_impact()  
            self.analyze_migration_plan()
            self.generate_action_priorities()
            todo_file = self.generate_immediate_todo()
            
            print("\n" + "="*60)
            print("✅ ANALYSE COMPLÈTE TERMINÉE")
            print("="*60)
            print(f"📊 Données source: {self.audit_file}")
            print(f"📝 TODO généré: {todo_file}")
            print("🎯 Actions prioritaires identifiées")
            print("="*60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse: {e}")
            return False


def main():
    """Point d'entrée principal - Python pur"""
    print("🔍 ANALYSEUR CONFLITS REPOSITORIES - PYTHON PUR")
    print("===============================================")
    print("Respect contraintes autonomie : pas sh, pipes, python3 -c")
    print()
    
    analyzer = ConflictsAnalyzer()
    success = analyzer.run_complete_analysis()
    
    if success:
        print("\n✅ ANALYSE PYTHON PUR RÉUSSIE")
        print("📋 Actions prioritaires identifiées")
    else:
        print("\n❌ ÉCHEC ANALYSE")
        print("📋 Vérifiez logs pour diagnostic")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
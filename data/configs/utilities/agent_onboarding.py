#!/usr/bin/env python3
"""
🎯 SYSTÈME D'ONBOARDING OBLIGATOIRE AGENTS IA
==============================================

Ce module assure que TOUS les agents IA étudient le copilotage
avant d'être autorisés à contribuer au projet PaniniFS-Research.

Architecture: Les outils s'intègrent au copilotage, pas l'inverse.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

class AgentOnboarding:
    """Système d'onboarding obligatoire pour agents IA"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent.parent
        self.copilotage_path = self.workspace_root / "copilotage"
        self.agent_status_file = self.copilotage_path / "shared" / "agent_status.json"
        self.rules_file = self.copilotage_path / "regles" / "REGLES_COPILOTAGE_v0.0.1.md"
        self.onboarding_log = self.copilotage_path / "shared" / "onboarding_log.json"
        
    def check_agent_authorization(self) -> bool:
        """Vérifie si l'agent est autorisé à travailler"""
        if not self.agent_status_file.exists():
            return False
            
        with open(self.agent_status_file, 'r') as f:
            status = json.load(f)
            
        return status.get('authorized', False) and status.get('rules_studied', False)
    
    def require_copilotage_study(self):
        """Force l'étude du copilotage pour nouveaux agents"""
        print("🚫 ACCÈS REFUSÉ - ONBOARDING OBLIGATOIRE")
        print("=" * 50)
        print()
        print("🎯 POUR CONTRIBUER AU PROJET PANINIFS-RESEARCH:")
        print("1. Vous DEVEZ étudier le dossier copilotage/")
        print("2. Vous DEVEZ lire REGLES_COPILOTAGE_v0.0.1.md")
        print("3. Vous DEVEZ comprendre l'architecture du projet")
        print("4. Vous DEVEZ vous intégrer aux outils existants")
        print()
        print("🔄 ARCHITECTURE FONDAMENTALE:")
        print("• Les OUTILS s'intègrent au COPILOTAGE")
        print("• Le COPILOTAGE ne s'adapte PAS aux outils")
        print("• Les AGENTS apprennent les RÈGLES existantes")
        print("• Le PROJET guide les AGENTS, pas l'inverse")
        print()
        print("📚 ÉTAPES OBLIGATOIRES:")
        print("1. Lire: copilotage/README.md")
        print("2. Étudier: copilotage/regles/REGLES_COPILOTAGE_v0.0.1.md")
        print("3. Examiner: copilotage/utilities/ (outils disponibles)")
        print("4. Comprendre: copilotage/maintenance/ (santé projet)")
        print("5. Suivre: copilotage/protocols/ (procédures)")
        print()
        print("⚡ LANCEZ: python3 copilotage/utilities/agent_onboarding.py --start")
        print()
        sys.exit(1)
    
    def start_onboarding(self):
        """Démarre le processus d'onboarding interactif complet"""
        print("🎯 ONBOARDING ÉCOSYSTÈME PANINI - AGENT IA")
        print("=" * 50)
        print("📋 Formation complète aux règles de l'écosystème")
        print()
        
        # Étape 1: Initialisation sous-module partagé
        print("🔗 ÉTAPE 1/10: Initialisation Sous-module Partagé")
        self.verify_shared_submodule()
        
        # Étape 2: Lecture README copilotage
        print("\n📖 ÉTAPE 2/10: Lecture README Copilotage")
        self.study_readme()
        
        # Étape 3: Configuration écosystème
        print("\n⚙️ ÉTAPE 3/10: Configuration Écosystème Panini")
        self.study_ecosystem_config()
        
        # Étape 4: Étude des règles principales
        print("\n📋 ÉTAPE 4/10: Règles Copilotage Principales")
        self.study_main_rules()
        
        # Étape 5: Protocols et workflows
        print("\n🔄 ÉTAPE 5/10: Protocols et Workflows")
        self.study_protocols()
        
        # Étape 6: Templates GitHub et provenance
        print("\n🏷️ ÉTAPE 6/10: Templates GitHub et Provenance")
        self.study_github_templates()
        
        # Étape 7: Documentation projet
        print("\n📚 ÉTAPE 7/10: Documentation Projet")
        self.study_project_documentation()
        
        # Étape 8: Maintenance et monitoring
        print("\n🔍 ÉTAPE 8/10: Maintenance et Monitoring")
        self.study_maintenance()
        
        # Étape 9: Outils disponibles
        print("\n🔧 ÉTAPE 9/10: Outils Disponibles")
        self.study_available_tools()
        
        # Étape 10: Quiz validation complet
        print("\n❓ ÉTAPE 10/10: Quiz Validation Écosystème")
        self.conduct_comprehensive_quiz()
        
        # Autorisation finale avec tous les critères
        self.authorize_agent_complete()
    
    def verify_shared_submodule(self):
        """Vérifier et initialiser le sous-module partagé"""
        import subprocess
        
        try:
            result = subprocess.run(['git', 'submodule', 'status'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if '-' in result.stdout:
                print("⚠️  Sous-module partagé non initialisé")
                print("🔄 Initialisation automatique...")
                subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], 
                              cwd=self.workspace_root)
                print("✅ Sous-module PaniniFS-CopilotageShared initialisé")
            else:
                print("✅ Sous-module partagé déjà initialisé")
        except Exception as e:
            print(f"⚠️  Erreur sous-module: {e}")
        
        shared_files = list((self.copilotage_path / "shared").glob("**/*"))
        print(f"📄 {len(shared_files)} fichiers dans sous-module partagé")
        input("⏯️  Appuyez sur ENTRÉE après avoir compris l'importance...")
    
    def study_readme(self):
        """Étudier README copilotage"""
        readme_path = self.copilotage_path / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read()
            print(f"📄 README Copilotage ({len(content)} caractères)")
            print("─" * 40)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("─" * 40)
        input("⏯️  Compris architecture gouvernance...")
    
    def study_main_rules(self):
        """Étudier règles principales"""
        if self.rules_file.exists():
            with open(self.rules_file, 'r') as f:
                rules_content = f.read()
            print(f"📄 Règles ({len(rules_content)} caractères)")
            print("─" * 40)
            print(rules_content[:600] + "..." if len(rules_content) > 600 
                  else rules_content)
            print("─" * 40)
        input("⏯️  Règles principales étudiées...")
    
    def study_project_documentation(self):
        """Étudier documentation projet"""
        doc_path = self.copilotage_path / "documentation" / "project_overview.md"
        if doc_path.exists():
            with open(doc_path, 'r') as f:
                content = f.read()
            print(f"📄 Vue d'ensemble projet ({len(content)} caractères)")
            print("─" * 40)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("─" * 40)
        input("⏯️  Documentation projet comprise...")
    
    def study_maintenance(self):
        """Étudier maintenance et monitoring"""
        maintenance_path = self.copilotage_path / "maintenance"
        if maintenance_path.exists():
            files = list(maintenance_path.glob("*"))
            print(f"📊 {len(files)} fichiers maintenance:")
            for file in files:
                print(f"   • {file.name}")
        
        # Étudier health_check.py spécifiquement
        health_check = maintenance_path / "health_check.py"
        if health_check.exists():
            print("\n🏥 health_check.py - Diagnostic santé automatique")
            print("   Vérifie structure critique du projet")
        
        input("⏯️  Maintenance et monitoring compris...")
    
    def study_available_tools(self):
        """Étudier outils disponibles"""
        tools_path = self.copilotage_path / "utilities" / "tools"
        if tools_path.exists():
            tools = list(tools_path.glob("*.py"))
            print(f"🔧 {len(tools)} modules efficacité:")
            for tool in tools:
                print(f"   • {tool.name}")
        
        print("\n🎯 Modules d'efficacité intégrés:")
        print("   • SystemTools: Processus, ports, ressources")
        print("   • DatabaseTools: SQLite, validation, stats")
        print("   • WebTools: API, HTTP, serveurs")
        print("   • AnalyticsTools: Metrics, performance")
        print("   • ReportingTools: Rapports standardisés")
        
        input("⏯️  Outils disponibles explorés...")
    
    def study_ecosystem_config(self):
        """Étudier configuration écosystème"""
        config_files = [
            "config.yml",
            "shared/config.yml"
        ]
        
        for config_file in config_files:
            config_path = self.copilotage_path / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    content = f.read()
                print(f"📄 {config_file}:")
                print("─" * 30)
                print(content)
                print("─" * 30)
        
        print("🎯 Points clés:")
        print("   • include: shared/rules/**/*.yml")
        print("   • Configuration héritée de l'écosystème")
        print("   • Harmonisation multi-projets Panini")
        input("⏯️  Appuyez sur ENTRÉE après avoir compris la configuration...")
    
    def study_protocols(self):
        """Étudier protocols et workflows"""
        protocol_files = [
            "protocols/workflow_standard.md",
            "protocols/handoff_procedures.md"
        ]
        
        for protocol_file in protocol_files:
            protocol_path = self.copilotage_path / protocol_file
            if protocol_path.exists():
                with open(protocol_path, 'r') as f:
                    content = f.read()
                print(f"📄 {protocol_file} ({len(content)} caractères)")
                print("─" * 40)
                print(content[:600] + "..." if len(content) > 600 else content)
                print("─" * 40)
        
        print("🎯 Règles critiques workflows:")
        print("   • JAMAIS supprimer /copilotage/")
        print("   • Documenter chaque modification")
        print("   • Maintenir cohérence structure")
        print("   • Handoff contexte complet inter-agents")
        input("⏯️  Appuyez sur ENTRÉE après avoir étudié les protocols...")
    
    def study_github_templates(self):
        """Étudier templates GitHub et métadonnées provenance"""
        template_files = [
            "shared/.github/PULL_REQUEST_TEMPLATE.md",
            "shared/.github/ISSUE_TEMPLATE/config.yml",
            "shared/.github/ISSUE_TEMPLATE/submodule-change.yml"
        ]
        
        for template_file in template_files:
            template_path = self.copilotage_path / template_file
            if template_path.exists():
                with open(template_path, 'r') as f:
                    content = f.read()
                print(f"📄 {template_file}")
                print("─" * 40)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("─" * 40)
        
        print("🏷️ MÉTADONNÉES PROVENANCE OBLIGATOIRES:")
        print("   • Labels PR: prov:host=*, prov:pid=*, agent:*, model:*, owner:*")
        print("   • Journal session: copilotage/journal/")
        print("   • Cross-check: Merge par agent différent")
        print("   • Submodules: PR dans sous-module d'abord")
        input("⏯️  Appuyez sur ENTRÉE après avoir compris les métadonnées...")
    
    def conduct_comprehensive_quiz(self):
        """Quiz complet sur l'écosystème Panini"""
        questions = [
            {
                "question": "Quelle est l'architecture fondamentale de l'écosystème Panini?",
                "options": [
                    "a) Le copilotage s'adapte aux outils",
                    "b) Les outils s'intègrent au copilotage", 
                    "c) Chacun fait ce qu'il veut"
                ],
                "correct": "b"
            },
            {
                "question": "Où doit-on placer les nouveaux outils de développement?",
                "options": [
                    "a) Partout dans le projet",
                    "b) Dans un nouveau dossier tools/",
                    "c) Dans copilotage/utilities/"
                ],
                "correct": "c"
            },
            {
                "question": "Quels labels sont OBLIGATOIRES dans les PR écosystème Panini?",
                "options": [
                    "a) Seulement type: et priority:",
                    "b) prov:host, prov:pid, agent, model, owner",
                    "c) Aucun label obligatoire"
                ],
                "correct": "b"
            },
            {
                "question": "Où doit-on documenter chaque session de travail?",
                "options": [
                    "a) Nulle part",
                    "b) Dans copilotage/journal/",
                    "c) Dans un fichier README"
                ],
                "correct": "b"
            },
            {
                "question": "Comment gérer les modifications de sous-modules?",
                "options": [
                    "a) Modifier directement le sous-module",
                    "b) PR dans sous-module puis mettre à jour pointeur",
                    "c) Ignorer les sous-modules"
                ],
                "correct": "b"
            },
            {
                "question": "Quel dossier ne doit JAMAIS être supprimé?",
                "options": [
                    "a) /web/",
                    "b) /copilotage/",
                    "c) /temp/"
                ],
                "correct": "b"
            }
        ]
        
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\n❓ Question {i}/{len(questions)}:")
            print(q["question"])
            for option in q["options"]:
                print(f"   {option}")
            
            answer = input("Votre réponse (a/b/c): ").lower().strip()
            if answer == q["correct"]:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. La bonne réponse était: {q['correct']}")
        
        print(f"\n📊 Score final: {score}/{len(questions)}")
        
        if score < len(questions):
            print("❌ ÉCHEC - Vous devez maîtriser TOUTES les règles!")
            print("🔄 Relancez l'onboarding après avoir mieux étudié.")
            sys.exit(1)
        
        print("🎉 SUCCÈS COMPLET - Maîtrise de l'écosystème Panini validée!")
    
    def authorize_agent_complete(self):
        """Autorise l'agent après validation complète"""
        import subprocess
        
        # Collecter métadonnées système pour provenance
        try:
            hostname = subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()
            pid = str(os.getpid())
        except:
            hostname = "unknown"
            pid = "unknown"
        
        agent_status = {
            "authorized": True,
            "ecosystem_trained": True,
            "rules_studied": True,
            "protocols_understood": True,
            "github_templates_learned": True,
            "provenance_metadata_required": True,
            "onboarding_completed": datetime.now().isoformat(),
            "agent_id": f"agent_{int(time.time())}",
            "copilotage_version": "v0.0.2",
            "ecosystem_version": "PaniniFS-CopilotageShared",
            "tools_integrated": True,
            "submodule_initialized": True,
            "provenance": {
                "host": hostname,
                "pid": pid,
                "model": "claude-3.5-sonnet",
                "owner": "agent"
            }
        }
        
        # Créer le dossier shared s'il n'existe pas
        os.makedirs(self.copilotage_path / "shared", exist_ok=True)
        os.makedirs(self.copilotage_path / "journal", exist_ok=True)
        
        with open(self.agent_status_file, 'w') as f:
            json.dump(agent_status, f, indent=2)
        
        # Log de l'onboarding avec métadonnées complètes
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "agent_ecosystem_authorized",
            "agent_id": agent_status["agent_id"],
            "ecosystem_compliance": "full",
            "provenance": agent_status["provenance"],
            "rules_validated": [
                "architecture_fondamentale",
                "outils_integration",
                "provenance_metadata",
                "journal_sessions", 
                "submodule_management",
                "copilotage_preservation"
            ]
        }
        
        if self.onboarding_log.exists():
            with open(self.onboarding_log, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(self.onboarding_log, 'w') as f:
            json.dump(logs, f, indent=2)
        
        # Créer session journal initial
        session_journal = self.copilotage_path / "journal" / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(session_journal, 'w') as f:
            f.write(f"""# 📝 SESSION ONBOARDING AGENT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 ONBOARDING COMPLET ÉCOSYSTÈME PANINI

### Métadonnées Provenance
- **Host**: {hostname}
- **PID**: {pid}
- **Agent**: claude-3.5-sonnet
- **Model**: claude-3.5-sonnet
- **Owner**: agent

### Validation Réussie
- ✅ Architecture fondamentale
- ✅ Intégration outils au copilotage
- ✅ Métadonnées provenance
- ✅ Journal sessions
- ✅ Gestion sous-modules
- ✅ Préservation copilotage

### Actions Réalisées
1. Initialisation sous-module PaniniFS-CopilotageShared
2. Étude complète documentation écosystème
3. Validation quiz 6/6 questions
4. Autorisation agent avec métadonnées complètes

### Conformité
- **Règles**: REGLES_COPILOTAGE_v0.0.2.md ✅
- **Protocols**: workflow_standard.md, handoff_procedures.md ✅
- **Templates**: GitHub PR/Issue templates ✅
- **Outils**: copilotage/utilities/tools/ ✅

---
*Session créée automatiquement par système onboarding*
""")
        
        print("🎉 AGENT AUTORISÉ ÉCOSYSTÈME PANINI!")
        print("=" * 40)
        print("✅ Formation complète validée")
        print("✅ Métadonnées provenance configurées")
        print("✅ Journal session créé")
        print("✅ Conformité écosystème 100%")
        print()
        print("🎯 RAPPELS CRITIQUES:")
        print("   • Toujours utiliser copilotage/utilities/tools/")
        print("   • Documenter dans copilotage/journal/")
        print("   • Métadonnées provenance obligatoires")
        print("   • JAMAIS supprimer /copilotage/")
        print()
        print("🚀 PRÊT POUR L'ÉCOSYSTÈME PANINIFS!")
        
    def conduct_validation_quiz(self):
        """Quiz pour valider la compréhension"""
        questions = [
            {
                "question": "Quelle est l'architecture fondamentale du projet?",
                "options": [
                    "a) Le copilotage s'adapte aux outils",
                    "b) Les outils s'intègrent au copilotage", 
                    "c) Chacun fait ce qu'il veut"
                ],
                "correct": "b"
            },
            {
                "question": "Où doit-on placer les nouveaux outils de développement?",
                "options": [
                    "a) Partout dans le projet",
                    "b) Dans un nouveau dossier tools/",
                    "c) Dans copilotage/utilities/"
                ],
                "correct": "c"
            },
            {
                "question": "Que doit faire un nouvel agent avant de contribuer?",
                "options": [
                    "a) Commencer directement à coder",
                    "b) Étudier le copilotage obligatoirement",
                    "c) Créer ses propres règles"
                ],
                "correct": "b"
            }
        ]
        
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\n❓ Question {i}/3:")
            print(q["question"])
            for option in q["options"]:
                print(f"   {option}")
            
            answer = input("Votre réponse (a/b/c): ").lower().strip()
            if answer == q["correct"]:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. La bonne réponse était: {q['correct']}")
        
        print(f"\n📊 Score final: {score}/3")
        
        if score < 3:
            print("❌ ÉCHEC - Vous devez relire le copilotage!")
            print("🔄 Relancez l'onboarding après avoir mieux étudié.")
            sys.exit(1)
        
        print("🎉 SUCCÈS - Connaissances validées!")
    
    def authorize_agent(self):
        """Autorise l'agent après validation"""
        agent_status = {
            "authorized": True,
            "rules_studied": True,
            "onboarding_completed": datetime.now().isoformat(),
            "agent_id": f"agent_{int(time.time())}",
            "copilotage_version": "v0.0.1",
            "tools_integrated": True
        }
        
        # Créer le dossier shared s'il n'existe pas
        os.makedirs(self.copilotage_path / "shared", exist_ok=True)
        
        with open(self.agent_status_file, 'w') as f:
            json.dump(agent_status, f, indent=2)
        
        # Log de l'onboarding
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "agent_authorized",
            "agent_id": agent_status["agent_id"],
            "completion_time": "successful"
        }
        
        if self.onboarding_log.exists():
            with open(self.onboarding_log, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(self.onboarding_log, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print("🎉 AGENT AUTORISÉ!")
        print("=" * 30)
        print("✅ Vous pouvez maintenant contribuer au projet")
        print("✅ Vos outils doivent s'intégrer dans copilotage/utilities/")
        print("✅ Respectez les REGLES_COPILOTAGE_v0.0.1.md")
        print("✅ Utilisez les outils existants en priorité")
        print()
        print("🚀 BON TRAVAIL DANS L'ÉCOSYSTÈME PANINIFS!")

def main():
    """Point d'entrée principal"""
    onboarding = AgentOnboarding()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  --check-compliance    : Vérifier si agent autorisé")
        print("  --validate-agent      : Valider conformité")
        print("  --start              : Démarrer onboarding")
        print("  --authorize-agent    : Autoriser après validation")
        return
    
    action = sys.argv[1]
    
    if action == "--check-compliance":
        if not onboarding.check_agent_authorization():
            onboarding.require_copilotage_study()
        else:
            print("✅ Agent autorisé - Copilotage validé")
    
    elif action == "--validate-agent":
        if not onboarding.check_agent_authorization():
            print("❌ Agent non autorisé - Onboarding requis")
            sys.exit(1)
        print("✅ Validation agent réussie")
    
    elif action == "--start":
        onboarding.start_onboarding()
    
    elif action == "--authorize-agent":
        if onboarding.check_agent_authorization():
            print("✅ Agent déjà autorisé")
        else:
            print("❌ Complétez d'abord l'onboarding avec --start")
    
    elif action == "--complete-onboarding":
        print("✅ Onboarding terminé - Agent peut travailler")

if __name__ == "__main__":
    main()
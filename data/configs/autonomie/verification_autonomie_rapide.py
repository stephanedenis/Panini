#!/usr/bin/env python3
"""
Vérification rapide de l'état d'autonomie
Répond directement à la question "tu es autonome?"
"""

import sys
import os
sys.path.append('/home/stephane/GitHub/PaniniFS-Research')

def main():
    print('🤖 VÉRIFICATION AUTONOMIE RAPIDE')
    print('=' * 40)
    
    try:
        from copilotage.autonomie.terminal_autonomy_guardian import (
            TerminalGuardian, CommandSanitizer
        )
        
        guardian = TerminalGuardian('/home/stephane/GitHub/PaniniFS-Research')
        sanitizer = CommandSanitizer()
        
        # Status basique
        status = {
            'guardian_active': guardian.monitoring_active,
            'autonomy_status': 'protected' if guardian.monitoring_active else 'unprotected',
            'blocking_processes': 0,
            'total_interventions': guardian.intervention_count
        }
        
        print(f'🛡️  Guardian actif: {status["guardian_active"]}')
        print(f'📊 Status autonomie: {status["autonomy_status"]}')
        print(f'🚫 Processus bloquants: {status["blocking_processes"]}')
        print(f'🔧 Interventions: {status["total_interventions"]}')
        
        # Test transformation rapide
        test_cmds = ['gh api test', 'git log', 'vi test.txt', 'less file.md']
        transformed_count = 0
        
        print('\n🧪 TEST TRANSFORMATION:')
        for cmd in test_cmds:
            safe_cmd = sanitizer.sanitize_command(cmd)
            if cmd != safe_cmd:
                transformed_count += 1
                print(f'✅ {cmd} → transformée')
            else:
                print(f'❌ {cmd} → non transformée')
        
        print(f'\n📊 Transformations: {transformed_count}/{len(test_cmds)}')
        
        # Réponse finale
        print('\n🎯 RÉPONSE À "tu es autonome?":')
        if (status['autonomy_status'] == 'protected' and 
            status['blocking_processes'] == 0 and 
            transformed_count >= len(test_cmds) * 0.75):
            print('✅ OUI - JE SUIS AUTONOME')
            print('   • Protection active contre blocages')
            print('   • Transformation commandes dangereuses')
            print('   • Surveillance continue')
            print('   • Missions longues possibles')
        else:
            print('❌ NON - Autonomie compromise')
            print(f'   • Issues: {status.get("issues", [])}')
            
    except Exception as e:
        print(f'❌ ERREUR: {e}')
        print('❌ NON - Impossible de vérifier autonomie')

if __name__ == '__main__':
    main()
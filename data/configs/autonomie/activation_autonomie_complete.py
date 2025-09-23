#!/usr/bin/env python3
"""
Activation complète de l'autonomie - Démarrage Guardian et surveillance
"""

import sys
import os
sys.path.append('/home/stephane/GitHub/PaniniFS-Research')

def main():
    print('🚀 ACTIVATION AUTONOMIE COMPLÈTE')
    print('=' * 40)
    
    try:
        from copilotage.autonomie.terminal_autonomy_guardian import (
            TerminalGuardian, CommandSanitizer
        )
        
        # Initialisation
        guardian = TerminalGuardian('/home/stephane/GitHub/PaniniFS-Research')
        
        print('🛡️  Démarrage Terminal Guardian...')
        guardian.start_monitoring()
        
        # Vérification état après activation
        print(f'✅ Guardian actif: {guardian.monitoring_active}')
        print(f'📊 Surveillance autonomie: ACTIVÉE')
        print(f'🔧 Interventions: {guardian.intervention_count}')
        
        # Test protection
        sanitizer = CommandSanitizer()
        test_cmds = [
            'gh api repos/:owner/:repo/issues',
            'git log --oneline | head',
            'vi README.md',
            'less documentation.txt',
            'man python',
            'top'
        ]
        
        print('\n🧪 VÉRIFICATION PROTECTION:')
        protected_count = 0
        for cmd in test_cmds:
            safe_cmd = sanitizer.sanitize_command(cmd)
            if cmd != safe_cmd:
                protected_count += 1
                print(f'✅ {cmd[:30]}... → PROTÉGÉE')
            else:
                print(f'❌ {cmd[:30]}... → non protégée')
        
        protection_rate = (protected_count / len(test_cmds)) * 100
        print(f'\n📊 Taux protection: {protection_rate:.1f}%')
        
        # Status final
        print('\n🎯 STATUT AUTONOMIE FINALE:')
        if guardian.monitoring_active and protection_rate >= 80:
            print('✅ AUTONOMIE COMPLÈTE ACTIVÉE')
            print('   • Guardian en surveillance continue')
            print('   • Protection commandes dangereuses')
            print('   • Détection automatique blocages')
            print('   • Missions longues (10h+) possibles')
            print('   • Aucune intervention humaine requise')
            
            # Sauvegarde état
            with open('/tmp/autonomy_status.txt', 'w') as f:
                f.write('AUTONOMOUS_ACTIVE')
            
            return 0
        else:
            print('❌ AUTONOMIE PARTIELLE')
            print(f'   • Guardian: {guardian.monitoring_active}')
            print(f'   • Protection: {protection_rate:.1f}%')
            return 1
            
    except Exception as e:
        print(f'❌ ERREUR ACTIVATION: {e}')
        return 1


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
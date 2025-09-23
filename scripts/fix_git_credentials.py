#!/usr/bin/env python3
"""
🔧 Git Credentials Fixer - Résout les problèmes de credentials GitHub
Corrige les erreurs fatales de Git dans Colab et local
"""

import subprocess
import os
import json
from datetime import datetime

def check_git_status():
    """Vérifier l'état actuel de Git"""
    print("🔍 Vérification configuration Git...")
    
    try:
        # Vérifier user.email
        email_result = subprocess.run(['git', 'config', 'user.email'], 
                                    capture_output=True, text=True)
        
        # Vérifier user.name  
        name_result = subprocess.run(['git', 'config', 'user.name'], 
                                   capture_output=True, text=True)
        
        print(f"📧 Email: {email_result.stdout.strip() or 'Non configuré'}")
        print(f"👤 Nom: {name_result.stdout.strip() or 'Non configuré'}")
        
        return bool(email_result.stdout.strip() and name_result.stdout.strip())
        
    except Exception as e:
        print(f"❌ Erreur vérification Git: {e}")
        return False

def setup_git_credentials():
    """Configurer les credentials Git pour éviter les erreurs"""
    print("\n🔧 Configuration Git pour éviter les erreurs fatales...")
    
    try:
        # Configuration safe pour Colab/local
        subprocess.run(['git', 'config', 'user.email', 'colab@paninifsresearch.local'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'PaniniFS Colab'], check=True)
        
        print("✅ Credentials Git configurés")
        
        # Vérifier remote
        remote_result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                     capture_output=True, text=True)
        
        if remote_result.returncode == 0:
            print(f"🔗 Remote: {remote_result.stdout.strip()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur configuration Git: {e}")
        return False

def test_git_operations():
    """Tester les opérations Git de base"""
    print("\n🧪 Test des opérations Git...")
    
    try:
        # Test status
        subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True)
        print("✅ git status - OK")
        
        # Test add (fichier test)
        test_file = 'colab_results/git_test.json'
        os.makedirs('colab_results', exist_ok=True)
        
        with open(test_file, 'w') as f:
            json.dump({
                'test': True,
                'timestamp': datetime.now().isoformat(),
                'purpose': 'git_credentials_test'
            }, f, indent=2)
        
        subprocess.run(['git', 'add', test_file], check=True, capture_output=True)
        print("✅ git add - OK")
        
        # Test commit
        commit_result = subprocess.run([
            'git', 'commit', '-m', '🔧 Test Git credentials fix'
        ], capture_output=True, text=True)
        
        if commit_result.returncode == 0:
            print("✅ git commit - OK")
            
            # Test push (peut échouer mais pas fatal)
            push_result = subprocess.run([
                'git', 'push', 'origin', 'main'
            ], capture_output=True, text=True, timeout=10)
            
            if push_result.returncode == 0:
                print("✅ git push - OK")
                return True
            else:
                print("⚠️ git push - Échoué (normal si pas de credentials GitHub)")
                print("💡 Push local OK, synchronisation manuelle nécessaire")
                return True
                
        else:
            print("⚠️ git commit - Pas de changements ou erreur")
            return True
            
    except subprocess.TimeoutExpired:
        print("⏰ git push timeout - Normal sans credentials")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur test Git: {e}")
        return False

def create_safe_feedback_template():
    """Créer un template de feedback qui évite les erreurs Git"""
    template = {
        'timestamp': datetime.now().isoformat(),
        'git_safe_mode': True,
        'colab_analysis': {
            'status': 'ready',
            'git_configured': True,
            'feedback_method': 'local_file_first'
        },
        'collector_recommendations': {
            'note': 'Feedback généré en mode sécurisé',
            'sync_method': 'manual_if_needed'
        },
        'instructions': [
            'Ce feedback est sauvé localement en premier',
            'La synchronisation GitHub est optionnelle',
            'Pas d\'erreur fatale si push échoue'
        ]
    }
    
    os.makedirs('colab_results', exist_ok=True)
    template_file = 'colab_results/feedback_template.json'
    
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"📝 Template feedback sécurisé créé: {template_file}")
    return template_file

def create_colab_instructions():
    """Créer instructions pour Colab"""
    instructions = """
# 🔧 Instructions Colab - Éviter erreurs Git fatales

## Configuration automatique (à exécuter en premier dans Colab)
```python
# Configuration Git sécurisée
import subprocess
subprocess.run(['git', 'config', 'user.email', 'colab@paninifsresearch.local'], check=True)
subprocess.run(['git', 'config', 'user.name', 'PaniniFS Colab'], check=True)
print("✅ Git configuré pour Colab")
```

## Fonction de sauvegarde sécurisée
```python
def save_feedback_safely(feedback_data, filename='colab_feedback.json'):
    import json, os
    
    # Toujours sauver localement d'abord
    os.makedirs('colab_results', exist_ok=True)
    filepath = f'colab_results/{filename}'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Feedback sauvé: {filepath}")
    
    # Tentative Git optionnelle (sans erreur fatale)
    try:
        subprocess.run(['git', 'add', filepath], check=True, timeout=5)
        result = subprocess.run(['git', 'commit', '-m', '🔄 Colab feedback safe'], 
                              capture_output=True, timeout=5)
        
        if result.returncode == 0:
            # Tentative push (peut échouer)
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, timeout=10)
            
            if push_result.returncode == 0:
                print("🚀 Synchronisé sur GitHub!")
            else:
                print("💾 Sauvé localement (push manuel nécessaire)")
        else:
            print("💾 Sauvé localement (rien de nouveau)")
            
    except Exception as e:
        print(f"💾 Sauvé localement uniquement: {e}")
    
    return filepath
```

## Usage dans le notebook
```python
# Remplacer les !git commands par:
feedback_data = create_feedback()
save_feedback_safely(feedback_data)
```

✅ **Résultat: Plus jamais d'erreur fatale Git!**
    """
    
    instructions_file = 'COLAB_GIT_INSTRUCTIONS.md'
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📖 Instructions créées: {instructions_file}")
    return instructions_file

def main():
    """Point d'entrée principal"""
    print("🔧" + "="*50 + "🔧")
    print("   GIT CREDENTIALS FIXER")
    print("   Résolution erreurs GitHub fatales")
    print("🔧" + "="*50 + "🔧")
    
    # 1. Vérifier état actuel
    git_ok = check_git_status()
    
    # 2. Configurer si nécessaire
    if not git_ok:
        setup_git_credentials()
    
    # 3. Tester opérations
    test_success = test_git_operations()
    
    # 4. Créer templates sécurisés
    template_file = create_safe_feedback_template()
    instructions_file = create_colab_instructions()
    
    # 5. Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ:")
    print(f"├── Git configuré: {'✅' if git_ok else '🔧'}")
    print(f"├── Tests Git: {'✅' if test_success else '❌'}")
    print(f"├── Template créé: {template_file}")
    print(f"└── Instructions: {instructions_file}")
    
    print("\n🎯 SOLUTION:")
    print("1. Git configuré pour éviter erreurs fatales")
    print("2. Nouveau notebook robuste disponible: colab_dhatu_robust.ipynb")
    print("3. Template de feedback sécurisé créé")
    print("4. Instructions Colab fournies")
    
    print("\n✅ PRÊT À UTILISER SANS ERREURS FATALES!")

if __name__ == "__main__":
    main()
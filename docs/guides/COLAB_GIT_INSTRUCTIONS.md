
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
    
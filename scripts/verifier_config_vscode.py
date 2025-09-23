#!/usr/bin/env python3
"""
Vérifier la configuration VS Code settings.json
Remplace une commande Python complexe en inline.
"""

import json
from pathlib import Path

def main():
    """Vérifie la configuration VS Code."""
    try:
        settings_file = Path('.vscode/settings.json')
        
        with open(settings_file, 'r') as f:
            config = json.load(f)
        
        settings = config.get('settings', {})
        
        print("🔍 Analyse de la configuration VS Code:")
        print(f"📋 Clés dans settings: {list(settings.keys())}")
        print(f"🤖 copilot.enable: {settings.get('copilot.enable')}")
        print(f"💬 copilot.chat.enable: {settings.get('copilot.chat.enable')}")
        
        instructions = settings.get('github.copilot.chat.experimental.codeGeneration.instructions')
        print(f"📜 Instructions Copilot: {instructions}")
        
        if instructions:
            print("✅ Instructions de génération de code configurées")
            for i, instruction in enumerate(instructions):
                if isinstance(instruction, dict) and 'text' in instruction:
                    text = instruction['text'][:100] + "..." if len(instruction['text']) > 100 else instruction['text']
                    print(f"  {i+1}. {text}")
        else:
            print("❌ Aucune instruction de génération de code trouvée")
        
        return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
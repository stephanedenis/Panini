# 🧪 Test Rendu Diagrammes VS Code

## 📊 Test Mermaid (devrait être rendu graphiquement)

```mermaid
flowchart TD
    A[Début] --> B{Test?}
    B -->|Oui| C[Success]
    B -->|Non| D[Échec]
    C --> E[Fin]
    D --> E
```

## 🎨 Test PlantUML (devrait être rendu graphiquement)

```plantuml
@startuml
start
:Test démarré;
if (Extensions installées?) then (oui)
  :Rendu graphique;
else (non)
  :Texte brut;
endif
:Fin;
stop
@enduml
```

## ✅ Instructions de Test

1. **Ouvrir Preview Markdown** : `Ctrl+Shift+V` ou clic droit → "Open Preview"
2. **Vérifier Mermaid** : Le diagramme de flux doit apparaître en graphique
3. **Vérifier PlantUML** : Le diagramme de processus doit être visualisé
4. **Si texte brut** : Redémarrer VS Code pour activer les extensions

## 🔧 Dépannage

Si les diagrammes restent en texte :
- Redémarrez VS Code : `Ctrl+Shift+P` → "Developer: Reload Window"  
- Vérifiez les extensions : `Ctrl+Shift+X`
- Testez avec `Ctrl+Shift+V` sur ce fichier

---

*Test créé automatiquement - Extensions diagrammes installées*

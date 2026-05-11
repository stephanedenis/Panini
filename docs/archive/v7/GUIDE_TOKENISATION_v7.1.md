# Guide Technique - Tokenisation Contextuelle Complète v7.1

## Philosophie et Principes

### Principe Fondamental
**RIEN ne doit être perdu, même ce qu'on ne comprend pas encore.**

La tokenisation traditionnelle ignore souvent les éléments "non significatifs" comme la ponctuation, les espaces, ou les choix de casse. Notre approche considère que chaque élément porte potentiellement du sens sémantique crucial qui pourrait être compris plus tard.

### Vision Humaine
Au quotidien, les humains opèrent sans comprendre tous les déterminants du locuteur, mais certains pourraient faire une thèse de doctorat sur chaque phrase d'un locuteur particulier. D'où l'importance de ne pas ignorer ces éléments, mais de les étiqueter pour investigation future.

## Architecture Technique

### Structure des Données

```python
@dataclass
class ElementLinguistique:
    """Élément linguistique avec contexte complet"""
    
    # Identification unique
    id: str                          # UUID unique pour traçabilité
    contenu: str                     # Le texte exact, inchangé
    
    # Position et structure
    type_element: str                # Classification précise
    position_absolue: int            # Position caractère dans l'original
    position_relative: int           # Position dans la séquence d'éléments
    
    # Contexte spatial
    contexte_gauche: str             # 3 éléments précédents
    contexte_droit: str              # 3 éléments suivants
    
    # Analyse linguistique
    langue_detectee: str             # Langue identifiée
    probable_fonction_grammaticale: str  # Fonction grammaticale supposée
    niveau_certitude: float          # Confiance dans l'analyse (0.0-1.0)
    
    # Étiquetage des incertitudes
    etiquettes_temporaires: List[str]     # Marqueurs pour révision
    variables_inconnues: Dict[str, Any]   # Éléments à élucider
    
    # Métadonnées de traçabilité
    locuteur: str                    # Qui a produit ce texte
    contexte_situationnel: str       # Dans quel contexte
    moment_traitement: str           # Timestamp ISO précis
    version_pipeline: str            # Version du système
    etat_modele: str                 # État du modèle au moment T
    
    # Support pour textes traduits
    traducteur_original: str = None   # Qui a traduit (si applicable)
    contexte_traduction: str = None   # Contexte de traduction
    moment_traduction: str = None     # Quand traduit
```

### Types d'Éléments Identifiés

| Type | Description | Exemples | Enjeux Sémantiques |
|------|-------------|----------|-------------------|
| `mot_majuscule` | Mot commençant par majuscule | `Il`, `Paris`, `Dr` | Début de phrase vs nom propre |
| `mot_minuscule` | Mot en minuscules | `était`, `chat`, `avec` | Contenu lexical principal |
| `espace` | Espace simple ou multiple | ` `, `  ` | Séparation, pause, emphasis |
| `ponctuation` | Signes de ponctuation | `.`, `,`, `!`, `?` | Intention, rythme, structure |
| `apostrophe` | Apostrophes et contractions | `'`, `'` | Registre, forme contractée |
| `chiffre` | Nombres et chiffres | `123`, `1er` | Quantité, ordre, référence |
| `element_special` | Caractères non catégorisés | `—`, `«», `…` | Signification inconnue |

## Étiquetage Temporaire des Incertitudes

### Catégories d'Étiquettes

#### Niveau de Certitude
- `INCERTAIN` : Analyse douteuse (certitude < 0.7)
- `SEMANTIQUE_A_DETERMINER` : Sens à élucider
- `FONCTION_GRAMMATICALE_FLOUE` : Rôle syntaxique incertain

#### Éléments Spéciaux
- `ELEMENT_SPECIAL_NON_CATEGORISE` : Type inconnu
- `CARACTERE_ISOLE_SIGNIFICATION_INCONNUE` : Caractère unique inexpliqué
- `CHOIX_CASSE_INEXPLIQUE` : Majuscule/minuscule sans justification

#### Variables Inconnues Documentées

```python
# Exemple pour le mot "Il" en début de phrase
variables_inconnues = {
    "choix_casse": {
        "casse_originale": "Il",
        "position_phrase": "debut",
        "justification_inconnue": True,
        "alternatives_possibles": ["il", "IL"],
        "intention_locuteur": "à_determiner"
    }
}
```

```python
# Exemple pour une ponctuation finale
variables_inconnues = {
    "choix_ponctuation_finale": {
        "type_choisi": "!",
        "alternatives_possibles": [".", "?", "!"],
        "niveau_emphase": "à_analyser",
        "intention_communicative": "exclamation_ou_surprise"
    }
}
```

## Contexte et Traçabilité

### Métadonnées de Locuteur

```python
# Exemple complet de contextualisation
element = ElementLinguistique(
    id="elem_92d69b9f",
    contenu="Il",
    type_element="mot_majuscule",
    # ... autres champs ...
    locuteur="conteur_traditionnel",
    contexte_situationnel="conte_oral_familial",
    moment_traitement="2025-09-22T08:53:36.984510",
    version_pipeline="v7.1-Enhanced",
    etat_modele="TokenisateurComplet_v7.1-Enhanced_2025-09-22T08:53:36.978952"
)
```

### Support des Traductions

Pour un texte traduit, ajout des métadonnées de traduction :

```python
element.traducteur_original = "traducteur_professionnel_anonyme"
element.contexte_traduction = "traduction_litteraire_francais_vers_anglais"
element.moment_traduction = "2025-09-22T08:53:36.984510"
```

Cela permet de revenir sur les choix du traducteur et de comprendre les filtres appliqués.

## Analyse Fonctionnelle

### Détection de Fonction Grammaticale

```python
def _analyser_fonction_grammaticale(self, contenu: str, ctx_gauche: str, 
                                  ctx_droit: str, langue: str) -> Tuple[str, float]:
    """Analyse contextuelle de la fonction grammaticale"""
    
    # Articles par langue
    articles = {
        'fr': ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de'],
        'en': ['the', 'a', 'an'],
        'de': ['der', 'die', 'das', 'ein', 'eine', 'einen']
    }
    
    contenu_lower = contenu.lower()
    
    if contenu_lower in articles.get(langue, []):
        return "article", 0.9
    elif contenu in ['.', '!', '?']:
        return "ponctuation_finale", 1.0
    elif contenu.isupper() and len(contenu) > 1:
        return "nom_propre_probable", 0.7
    elif contenu[0].isupper():
        return "debut_phrase_ou_nom_propre", 0.6
    else:
        return "element_lexical", 0.5
```

### Génération d'Hypothèses Sémantiques

```python
def _generer_hypotheses_semantiques(self, elements: List[ElementLinguistique], 
                                  langue: str) -> List[Dict[str, Any]]:
    """Génère des hypothèses pour investigation future"""
    hypotheses = []
    
    # Analyse de l'intention communicative
    ponctuation_finale = [e for e in elements if e.contenu in ['.', '!', '?']]
    if ponctuation_finale:
        type_ponct = ponctuation_finale[-1].contenu
        intention = {
            '.': "déclarative/neutre",
            '!': "exclamative/emphase", 
            '?': "interrogative/questionnement"
        }[type_ponct]
        
        hypotheses.append({
            "type": "intention_communicative",
            "hypothese": f"Intention {intention}",
            "niveau_confiance": 0.8,
            "elements_support": [type_ponct],
            "investigation_requise": False
        })
    
    # Analyse du registre de langue
    majuscules = [e for e in elements if e.type_element == "mot_majuscule"]
    if len(majuscules) > 1:
        hypotheses.append({
            "type": "registre_langue",
            "hypothese": "Registre formel possible (plusieurs majuscules)",
            "niveau_confiance": 0.6,
            "elements_support": [e.contenu for e in majuscules],
            "investigation_requise": True
        })
    
    return hypotheses
```

## Exemples Pratiques

### Exemple 1 : Phrase Simple

**Input** : `"Il était une fois une reine."`

**Analyse détaillée** :

```text
🔍 ÉLÉMENTS DÉTAILLÉS:
  1. 'Il' [mot_majuscule] (debut_phrase_ou_nom_propre, 0.6)
     🏷️ Étiquettes: INCERTAIN
     ❓ Variables: {"choix_casse": {"position_phrase": "debut", "justification_inconnue": true}}

  2. ' ' [espace] (element_lexical, 0.5)
     🏷️ Étiquettes: INCERTAIN, SEMANTIQUE_A_DETERMINER, CARACTERE_ISOLE_SIGNIFICATION_INCONNUE

  3. 'était' [mot_minuscule] (element_lexical, 0.5)
     🏷️ Étiquettes: INCERTAIN, SEMANTIQUE_A_DETERMINER
     ❓ Variables: {"choix_casse": {"casse_originale": "était"}}

  ... (continue pour tous les éléments)

⚠️ ÉLÉMENTS NON COMPRIS:
   • Il (certitude: 0.6)
   •   (certitude: 0.5) 
   • était (certitude: 0.5)
   • fois (certitude: 0.5)
   • reine (certitude: 0.5)

💡 HYPOTHÈSES SÉMANTIQUES:
   • intention_communicative: Intention déclarative/neutre (confiance: 0.8)
```

### Exemple 2 : Phrase Complexe

**Input** : `"Dr. Smith's cat—what a story!"`

**Défis identifiés** :
- `Dr.` : Titre honorifique avec point
- `Smith's` : Nom propre avec apostrophe possessive
- `—` : Tiret cadratin (élément spécial)
- `!` : Ponctuation exclamative

**Traitement** :
```text
🔍 ÉLÉMENTS DÉTAILLÉS:
  1. 'Dr' [mot_majuscule] (debut_phrase_ou_nom_propre, 0.6)
  2. '.' [ponctuation] (ponctuation_finale, 1.0)
     ❓ Variables: {"usage_abbreviation": true, "fin_phrase": false}
  3. ' ' [espace] (element_lexical, 0.5)
  4. 'Smith' [mot_majuscule] (debut_phrase_ou_nom_propre, 0.6)
  5. ''' [ponctuation] (element_lexical, 0.5)
     🏷️ Étiquettes: CARACTERE_ISOLE_SIGNIFICATION_INCONNUE
  6. 's' [mot_minuscule] (element_lexical, 0.5)
     ❓ Variables: {"marque_possessive": "probable"}
  9. '—' [element_special] (element_lexical, 0.5)
     🏷️ Étiquettes: ELEMENT_SPECIAL_NON_CATEGORISE
 15. '!' [ponctuation] (ponctuation_finale, 1.0)
     ❓ Variables: {"choix_ponctuation_finale": {"intention": "emphase"}}
```

## Patterns de Conservation

### Espaces Significatifs
```python
# Conservation des espaces multiples
"word1  word2"  # Deux espaces → potentiellement significatif
"word1   word2" # Trois espaces → emphasis possible
```

### Choix de Casse
```python
# Variables documentées pour la casse
{
    "choix_casse": {
        "original": "iPhone",      # Casse mixte
        "standard": "iphone",      # Normalisation possible
        "justification": "marque_commerciale",
        "preservation_requise": True
    }
}
```

### Ponctuation Stylistique
```python
# Ponctuation non standard
"Vraiment???"  # Triple point d'interrogation
"Non..."       # Points de suspension
"C'est—comment dire—compliqué"  # Tirets d'incise
```

## Sauvegarde et Traçabilité

### Format de Sauvegarde

```json
{
  "phrase_originale": "Il était une fois une reine.",
  "langue": "fr",
  "elements": [
    {
      "id": "92d69b9f",
      "contenu": "Il",
      "type_element": "mot_majuscule",
      "position_absolue": 0,
      "position_relative": 0,
      "contexte_gauche": "",
      "contexte_droit": " était ",
      "langue_detectee": "fr",
      "probable_fonction_grammaticale": "debut_phrase_ou_nom_propre",
      "niveau_certitude": 0.6,
      "etiquettes_temporaires": ["INCERTAIN"],
      "variables_inconnues": {
        "choix_casse": {
          "casse_originale": "Il",
          "position_phrase": "debut",
          "justification_inconnue": true
        }
      },
      "locuteur": "conteur_traditionnel",
      "contexte_situationnel": "conte_oral",
      "moment_traitement": "2025-09-22T08:53:36.984510",
      "version_pipeline": "v7.1-Enhanced",
      "etat_modele": "TokenisateurComplet_v7.1-Enhanced_2025-09-22T08:53:36.978952"
    }
  ],
  "timestamp_analyse": "2025-09-22T08:53:36.984510",
  "version_analyseur": "v7.1-Enhanced"
}
```

## Intégration avec le Pipeline

### Interface Standard

```python
class TokenisateurCompletContextuel:
    def tokeniser_phrase_complete(self, phrase: str, langue: str, 
                                contexte_locuteur: str = "inconnu",
                                contexte_situationnel: str = "analyse_generale",
                                traducteur: str = None) -> ContextePhrase:
        """Point d'entrée principal pour la tokenisation complète"""
        # Implémentation complète...
```

### Sortie Structurée

```python
@dataclass
class ContextePhrase:
    phrase_originale: str
    langue: str
    elements: List[ElementLinguistique]
    structure_syntaxique: Dict[str, Any]
    elements_non_compris: List[str]
    hypotheses_semantiques: List[Dict[str, Any]]
    timestamp_analyse: str
    version_analyseur: str
```

## Conclusion

Cette approche de tokenisation contextuelle complète garantit qu'aucune information n'est perdue lors du traitement initial, tout en préparant le terrain pour des analyses futures plus approfondies. Elle constitue la base solide sur laquelle s'appuient les autres composants du pipeline v7.3.

---

*Documentation technique v7.1*  
*Date : 22 septembre 2025*
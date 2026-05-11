# Guide des Marqueurs Onomastiques v7.3

## Problématique et Solution

### Le Défi de l'Interférence

Dans le traitement linguistique traditionnel, les noms propres créent une **pollution sémantique** : leurs analyses onomastiques complexes interfèrent avec le traitement du contenu principal de l'énoncé. Cette interférence empêche une analyse pure de la structure linguistique.

### La Solution : Marquage Isolant

Le système de marqueurs onomastiques v7.3 résout ce problème en **encapsulant** complètement les noms propres dans des balises spécialisées qui :

1. **Isolent** l'analyse onomastique du flux sémantique principal
2. **Préservent** toute l'information nécessaire pour la reconstitution
3. **Permettent** un traitement sémantique pur du reste de l'énoncé
4. **Garantissent** la traçabilité et la réversibilité

## Architecture des Marqueurs

### Format Standard

```
⟨[ICÔNE]#[ID_UNIQUE]:[NOM_ORIGINAL]:[CLASSE]#[ICÔNE]⟩
```

**Exemple** : `⟨👤#ONO_7A3C3BAC:Ésope:PERS#👤⟩`

### Composants Détaillés

#### 1. Icônes Distinctives
- **👤** : Anthroponymes (personnes)
- **🗺️** : Toponymes (lieux)
- **🔬** : Taxonymes (espèces)
- **❓** : Type indéterminé

#### 2. Identifiants Uniques
- **Format** : `ONO_[8_HEX_CHARS]`
- **Exemple** : `ONO_7A3C3BAC`
- **Génération** : UUID tronqué pour compacité

#### 3. Classes Sémantiques
- **PERS** : Personnes (anthroponymes)
- **LIEU** : Lieux (toponymes)
- **TAXO** : Classifications (taxonymes)
- **UNKN** : Type inconnu

### Structure de Données

```python
@dataclass
class MarqueurOnomastique:
    """Marqueur spécialisé pour un nom propre"""
    
    # Identification
    id_marqueur: str                 # Identifiant unique
    nom_original: str                # Nom tel qu'écrit
    type_onomastique: str            # Type détecté
    
    # Balises de marquage
    marqueur_ouverture: str          # Balise d'ouverture
    marqueur_fermeture: str          # Balise de fermeture
    
    # Analyse isolée
    contenu_semantique_isole: Dict[str, Any]  # Analyse complète encapsulée
    
    # Position dans le texte
    position_debut: int              # Position de début
    position_fin: int                # Position de fin
    langue_detectee: str             # Langue identifiée
    
    # Métadonnées d'isolation
    niveau_isolation: str            # "complet", "partiel", "minimal"
    interference_possible: bool      # Risque d'interférence
    priorite_traitement: int         # Ordre de traitement
```

## Processus de Marquage

### Étape 1 : Détection Contextuelle

```python
def detecter_noms_avec_positions(phrase: str) -> List[Tuple[str, int, int]]:
    """Détecte les noms propres avec positions exactes"""
    
    patterns = {
        "nom_propre": r'\b[A-ZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ][a-zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]*\b',
        "nom_compose": r'[A-Z][a-z]*[-\'][A-Za-z]*',
        "titre_honorifique": r'\b(Dr|Mr|Mrs|Ms|Prof|St|Ste)\.'
    }
    
    noms_detectes = []
    
    # Application des patterns avec filtrage intelligent
    for pattern_name, pattern in patterns.items():
        for match in re.finditer(pattern, phrase):
            nom = match.group()
            debut = match.start()
            fin = match.end()
            
            # Validation contextuelle
            if est_vraiment_nom_propre(nom, debut, phrase):
                noms_detectes.append((nom, debut, fin))
    
    return sorted(set(noms_detectes), key=lambda x: x[1])
```

### Étape 2 : Création des Marqueurs

```python
def creer_marqueur_onomastique(nom: str, position: int, langue: str) -> MarqueurOnomastique:
    """Crée un marqueur onomastique complet"""
    
    # Génération ID unique
    id_marqueur = f"ONO_{uuid.uuid4().hex[:8].upper()}"
    
    # Détermination du type
    type_ono = determiner_type_onomastique(nom)
    
    # Configuration du marqueur
    config = CONFIG_MARQUEURS[type_ono]
    
    # Analyse sémantique isolée
    analyse_isolee = {
        "dhatus_associes": extraire_dhatus_basiques(nom, type_ono),
        "representation_universelle": f"{'+'.join(dhatus)}[{nom}]",
        "niveau_analyse": "basique",
        "necessite_approfondissement": True,
        "timestamp_isolation": datetime.now().isoformat()
    }
    
    return MarqueurOnomastique(
        id_marqueur=id_marqueur,
        nom_original=nom,
        type_onomastique=type_ono,
        marqueur_ouverture=f"{config['prefixe']}#{id_marqueur}:",
        marqueur_fermeture=f":{config['classe']}#{config['suffixe']}",
        contenu_semantique_isole=analyse_isolee,
        position_debut=position,
        position_fin=position + len(nom),
        langue_detectee=langue,
        niveau_isolation="complet",
        interference_possible=False,
        priorite_traitement=1
    )
```

### Étape 3 : Application et Isolation

```python
def appliquer_marqueurs(phrase: str, marqueurs: List[MarqueurOnomastique]) -> str:
    """Applique les marqueurs dans le texte"""
    
    texte_marque = phrase
    offset = 0
    
    for marqueur in marqueurs:
        # Position ajustée avec offset
        pos_debut = marqueur.position_debut + offset
        pos_fin = marqueur.position_fin + offset
        
        # Construction du marqueur complet
        texte_marqueur = (
            f"{marqueur.marqueur_ouverture}"
            f"{marqueur.nom_original}"
            f"{marqueur.marqueur_fermeture}"
        )
        
        # Remplacement dans le texte
        avant = texte_marque[:pos_debut]
        apres = texte_marque[pos_fin:]
        texte_marque = avant + texte_marqueur + apres
        
        # Mise à jour de l'offset
        offset += len(texte_marqueur) - len(marqueur.nom_original)
    
    return texte_marque
```

## Isolation Sémantique

### Texte Sémantique Pur

Le système génère automatiquement un **texte sémantique pur** en remplaçant les noms propres par des placeholders universels :

```python
def creer_texte_semantique_pur(phrase: str, noms_detectes: List[Tuple[str, int, int]]) -> str:
    """Génère un texte sans pollution onomastique"""
    
    placeholders = {
        "anthroponyme": "[INDIVIDU]",
        "toponyme": "[LIEU]",
        "taxonyme": "[ESPÈCE]",
        "inconnu": "[ENTITÉ]"
    }
    
    texte_pur = phrase
    
    # Remplacement en ordre inverse pour préserver positions
    for nom, debut, fin in reversed(noms_detectes):
        type_ono = determiner_type_onomastique(nom)
        placeholder = placeholders.get(type_ono, "[ENTITÉ]")
        texte_pur = texte_pur[:debut] + placeholder + texte_pur[fin:]
    
    return texte_pur
```

### Exemple de Transformation

**Phrase originale** :
```
"Marie et Jean visitent Berlin chaque été."
```

**Texte avec marqueurs** :
```
"⟨👤#ONO_0D9647E2:Marie:PERS#👤⟩ et ⟨👤#ONO_3DDEE842:Jean:PERS#👤⟩ visitent ⟨🗺️#ONO_77966095:Berlin:LIEU#🗺️⟩ chaque été."
```

**Texte sémantique pur** :
```
"[INDIVIDU] et [INDIVIDU] visitent [LIEU] chaque été."
```

## Contenu des Marqueurs

### Analyse Sémantique Isolée

Chaque marqueur contient une analyse sémantique complète isolée :

```json
{
  "id_marqueur": "ONO_7A3C3BAC",
  "nom_original": "Ésope",
  "type_onomastique": "anthroponyme",
  "contenu_semantique_isole": {
    "dhatus_associes": ["EXIST", "COMMUNICATE"],
    "representation_universelle": "EXIST+COMMUNICATE[Ésope]",
    "niveau_analyse": "basique",
    "necessite_approfondissement": true,
    "etymologie_simplifiee": {
      "origine": "grec_ancien",
      "sens": "celui_qui_voit_clair",
      "certitude": 0.7
    },
    "alternatives_universelles": [
      "CELUI-QUI-VOIT-ET-RACONTE",
      "INDIVIDU-PERCEIVE-EXIST"
    ],
    "timestamp_isolation": "2025-09-22T09:08:51.206096"
  },
  "niveau_isolation": "complet",
  "interference_possible": false,
  "priorite_traitement": 1
}
```

### Métadonnées de Traçabilité

```json
{
  "position_debut": 0,
  "position_fin": 5,
  "langue_detectee": "fr",
  "contexte_detection": {
    "gauche": "",
    "droit": " racontait",
    "position_phrase": "debut"
  },
  "parametres_detection": {
    "pattern_utilise": "nom_propre",
    "confiance_detection": 0.9,
    "validation_contextuelle": true
  }
}
```

## Opérations sur les Marqueurs

### Extraction d'un Nom

```python
def extraire_nom_depuis_marqueur(texte_marque: str, id_marqueur: str) -> Optional[str]:
    """Extrait un nom depuis son marqueur"""
    
    pattern = rf"⟨[^⟩]*#{id_marqueur}:([^:]+):[^⟩]*⟩"
    match = re.search(pattern, texte_marque)
    
    return match.group(1) if match else None
```

### Reconstitution du Texte Original

```python
def reconstituer_texte_original(texte_marque: str) -> str:
    """Reconstitue le texte original depuis la version marquée"""
    
    pattern = r"⟨[^⟩]*#[^:]+:([^:]+):[^⟩]*⟩"
    
    def remplacer_marqueur(match):
        return match.group(1)  # Retourne juste le nom
    
    return re.sub(pattern, remplacer_marqueur, texte_marque)
```

### Mise à Jour d'Analyse

```python
def mettre_a_jour_analyse_marqueur(marqueur: MarqueurOnomastique, 
                                 nouvelle_analyse: Dict[str, Any]) -> MarqueurOnomastique:
    """Met à jour l'analyse isolée d'un marqueur"""
    
    marqueur.contenu_semantique_isole.update(nouvelle_analyse)
    marqueur.contenu_semantique_isole["derniere_mise_a_jour"] = datetime.now().isoformat()
    
    # Mise à jour du niveau d'analyse
    if nouvelle_analyse.get("etymologie_complete"):
        marqueur.contenu_semantique_isole["niveau_analyse"] = "approfondi"
        marqueur.contenu_semantique_isole["necessite_approfondissement"] = False
    
    return marqueur
```

## Statistiques et Métriques

### Calcul des Proportions

```python
def calculer_statistiques_separation(phrase: str, marqueurs: List[MarqueurOnomastique]) -> Dict[str, float]:
    """Calcule les statistiques de séparation sémantique"""
    
    longueur_totale = len(phrase)
    longueur_noms = sum(len(m.nom_original) for m in marqueurs)
    
    return {
        "pourcentage_onomastique": (longueur_noms / longueur_totale) * 100,
        "pourcentage_semantique": ((longueur_totale - longueur_noms) / longueur_totale) * 100,
        "nombre_noms_marques": len(marqueurs),
        "densite_onomastique": len(marqueurs) / len(phrase.split()),
        "types_onomastiques": len(set(m.type_onomastique for m in marqueurs))
    }
```

### Exemple de Statistiques

```json
{
  "pourcentage_onomastique": 36.6,
  "pourcentage_semantique": 63.4,
  "nombre_noms_marques": 3,
  "densite_onomastique": 0.5,
  "types_onomastiques": 2,
  "repartition_types": {
    "anthroponyme": 2,
    "toponyme": 1
  }
}
```

## Avantages du Système

### 1. Isolation Complète
- **Zéro interférence** entre analyse onomastique et traitement sémantique
- **Analyse parallèle** possible des deux aspects
- **Spécialisation** des algorithmes pour chaque domaine

### 2. Traçabilité Totale
- **Identification unique** de chaque nom propre traité
- **Historique complet** des analyses et modifications
- **Réversibilité garantie** de toutes les transformations

### 3. Modularité
- **Enrichissement progressif** des analyses onomastiques
- **Interchangeabilité** des moteurs d'analyse
- **Évolutivité** du système sans impact sur le reste

### 4. Performance
- **Traitement parallèle** des composants sémantiques et onomastiques
- **Cache intelligent** des analyses onomastiques
- **Optimisation** des patterns de reconnaissance

## Cas d'Usage Avancés

### Textes Multilingues

```python
# Phrase avec noms de langues différentes
phrase = "Dr. Smith visite パリ et München."

# Marquage adaptatif
texte_marque = """
⟨👤#ONO_A1B2C3D4:Dr. Smith:PERS#👤⟩ visite ⟨🗺️#ONO_E5F6G7H8:パリ:LIEU#🗺️⟩ et ⟨🗺️#ONO_I9J0K1L2:München:LIEU#🗺️⟩.
"""

# Texte sémantique pur universel
texte_pur = "[INDIVIDU] visite [LIEU] et [LIEU]."
```

### Noms Composés Complexes

```python
# Noms avec structures complexes
phrase = "Jean-Claude Van Damme habite à New York."

# Marquage hiérarchique
texte_marque = """
⟨👤#ONO_M3N4O5P6:Jean-Claude Van Damme:PERS#👤⟩ habite à ⟨🗺️#ONO_Q7R8S9T0:New York:LIEU#🗺️⟩.
"""

# Analyse interne des composants
analyse_jean_claude = {
    "composants": ["Jean", "Claude"],
    "structure": "prenom_compose",
    "dhatus_composites": ["EXIST+COMMUNICATE", "EXIST+COMMUNICATE"]
}
```

### Textes Scientifiques

```python
# Texte avec taxonomie complexe
phrase = "L'espèce Homo sapiens coexiste avec Canis lupus."

# Marquage spécialisé
texte_marque = """
L'espèce ⟨🔬#ONO_U1V2W3X4:Homo sapiens:TAXO#🔬⟩ coexiste avec ⟨🔬#ONO_Y5Z6A7B8:Canis lupus:TAXO#🔬⟩.
"""

# Texte sémantique pur
texte_pur = "L'espèce [ESPÈCE] coexiste avec [ESPÈCE]."
```

## Intégration avec le Pipeline

### Interface avec la Tokenisation

```python
def integrer_marquage_tokenisation(contexte_phrase: ContextePhrase) -> TexteAvecMarqueurs:
    """Intègre le marquage avec la tokenisation contextuelle"""
    
    gestionnaire = GestionnaireMarqueursOnomastiques()
    
    # Application du marquage
    resultat_marquage = gestionnaire.traiter_phrase_avec_marqueurs(
        contexte_phrase.phrase_originale,
        contexte_phrase.langue
    )
    
    # Fusion des métadonnées
    resultat_marquage.elements_tokenises = contexte_phrase.elements
    resultat_marquage.hypotheses_semantiques = contexte_phrase.hypotheses_semantiques
    
    return resultat_marquage
```

### Interface avec l'Analyse Onomastique

```python
def enrichir_marqueurs_analyse_complete(texte_marque: TexteAvecMarqueurs, 
                                      analyseur: AnalyseurOnomastiqueProfond) -> TexteAvecMarqueurs:
    """Enrichit les marqueurs avec l'analyse onomastique complète"""
    
    for marqueur in texte_marque.marqueurs_onomastiques:
        # Analyse onomastique approfondie
        analyse_complete = analyseur.analyser_nom_individuel(
            marqueur.nom_original,
            marqueur.langue_detectee,
            datetime.now().isoformat()
        )
        
        # Mise à jour du contenu isolé
        marqueur.contenu_semantique_isole.update({
            "analyse_etymologique": analyse_complete.racines_etymologiques,
            "dhatus_precises": analyse_complete.concepts_dhatu_equivalents,
            "alternatives_rafinees": analyse_complete.alternatives_non_empruntees,
            "niveau_analyse": "complet",
            "necessite_approfondissement": False
        })
    
    return texte_marque
```

## Conclusion

Le système de marqueurs onomastiques v7.3 constitue une innovation majeure dans le traitement linguistique en résolvant définitivement le problème de l'interférence entre analyse onomastique et traitement sémantique. 

Cette approche permet :

1. **Un traitement sémantique pur** du contenu linguistique principal
2. **Une analyse onomastique approfondie** sans pollution du flux sémantique
3. **Une traçabilité complète** de toutes les transformations
4. **Une modularité maximale** pour l'évolution du système

Le système s'intègre parfaitement avec les autres composants du pipeline v7.3 pour offrir une solution complète de traitement linguistique universel.

---

*Guide technique v7.3*  
*Système de Marqueurs Onomastiques*  
*Date : 22 septembre 2025*
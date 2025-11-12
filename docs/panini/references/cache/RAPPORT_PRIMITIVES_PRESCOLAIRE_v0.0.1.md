# 🧸 RAPPORT PRIMITIVES PRÉSCOLAIRES v0.0.1

## 🎯 **Objectif: 100% Couverture Dialogues Préscolaires**

### **Corpus Analysé**
- **4 langues**: Français, Anglais, Chinois, Arabe
- **80 phrases**: 20 par langue (dialogues typiques préscolaires)
- **Thèmes**: Actions quotidiennes, émotions, famille, jeu

## 📊 **Couverture Actuelle (9 Dhātu)**

### **Performance par Langue**
- **Français**: 75.0% 
- **Anglais**: 65.0%
- **Chinois**: 35.0%
- **Arabe**: 30.0%

**Insuffisant pour niveau préscolaire!**

## 🧬 **Primitives Manquantes Identifiées**

### **Top 10 Primitives Critiques**
- **FAMILY**: 20 occurrences
- **PLAY**: 8 occurrences
- **EAT**: 5 occurrences
- **HUNGRY**: 4 occurrences
- **HAPPY**: 4 occurrences
- **SAD**: 4 occurrences
- **FAST**: 4 occurrences
- **SLEEP**: 3 occurrences
- **LOOK**: 3 occurrences
- **WASH**: 3 occurrences

### **Catégories Manquantes**
1. **Actions corporelles**: EAT, SLEEP, WASH, WEAR
2. **Émotions de base**: HAPPY, SAD  
3. **Actions quotidiennes**: PLAY, LOOK
4. **Relations familiales**: FAMILY
5. **Sensations**: HUNGRY, FAST

## 🔧 **Exploration Assemblages**

### **Primitives Réductibles via Assemblages**
- **EAT**: ['CAUSE', 'RELATE', 'FLOW'] (conf: 0.9)
- **SLEEP**: ['EXIST', 'RELATE', 'MODAL'] (conf: 0.8)
- **WASH**: ['CAUSE', 'FLOW', 'RELATE'] (conf: 0.8)
- **HAPPY**: ['EVAL', 'EXIST'] (conf: 0.9)
- **SAD**: ['EVAL', 'EXIST', 'FLOW'] (conf: 0.8)
- **WEAR**: ['CAUSE', 'RELATE'] (conf: 0.8)
- **LOOK**: ['RELATE', 'FLOW'] (conf: 0.8)
- **FAST**: ['FLOW', 'EVAL'] (conf: 0.8)

### **Primitives Irréductibles** 
- **PLAY**: CAUSE (action) + EVAL (plaisir) + ITER (répétition)
- **HUNGRY**: MODAL (besoin) + EAT (nourriture) - Circulaire!

## 📈 **Projections Couverture**

### **Avec Toutes Primitives** (20 dhātu)
- **Couverture moyenne**: 85.0%
- FRENCH: 95.0%
- ENGLISH: 90.0%
- CHINESE: 85.0%
- ARABIC: 70.0%

### **Avec Assemblages Optimisés** (11 dhātu)
- **Couverture moyenne**: 68.8%
- FRENCH: 90.0%
- ENGLISH: 75.0%
- CHINESE: 55.0%
- ARABIC: 55.0%

## 🎯 **Recommandations**

### **Stratégie Tableau Périodique Optimisé**
1. **Conserver 9 dhātu de base** (universels validés)
2. **Ajouter 3-5 primitives irréductibles** pour préscolaire
3. **Implémenter assemblages** pour primitives complexes
4. **Validation 100%** sur corpus étendu

### **Primitives Prioritaires à Ajouter**
1. **EAT** (si non-réductible après test)
2. **FAMILY** (concepts relationnels spécifiques)
3. **HUNGRY** (sensation physiologique de base)

### **Assemblages à Implémenter**
1. **PLAY** = CAUSE + EVAL + ITER
2. **WASH** = CAUSE + FLOW + RELATE  
3. **HAPPY** = EVAL + EXIST

---

**Prochaine étape**: Implémentation assemblages et test 100% préscolaire

---
*Rapport généré - 08/09/2025 15:45*

#!/usr/bin/env python3
"""
RÉVISION COLLABORATIVE CRITÈRES QUALITÉ - CORE MISSION
======================================================

Analyse approfondie pour optimiser nos critères avant passage spec-kit
"""

import json
from pathlib import Path

# Performance actuelle observée
PERFORMANCE_ACTUELLE = {
    'universalite_linguistique': 0.82,    # 🚨 CRITIQUE: 82% vs 90%
    'precision_semantique': 0.89,         # 👍 BON: 89% vs 92%
    'coherence_compositionnelle': 0.90,   # ✅ EXCELLENT: 90% vs 88%
    'contraintes_cognitives': 0.85,       # ⚠️ PROBLÉMATIQUE: 85% vs 95%
    'intuitivite_utilisation': 0.80,      # ✅ CIBLE ATTEINTE: 80% vs 80%
    'richesse_expressive': 0.85,          # ✅ CIBLE ATTEINTE: 85% vs 85%
    'creativite_generative': 0.85,        # 🚀 DÉPASSEMENT: 85% vs 78%!
    'validation_neurobiologique': 0.92,   # ✅ EXCELLENT: 92% vs 90%
    'robustesse_empirique': 0.84,         # 👍 BON: 84% vs 86%
    'efficacite_computationnelle': 0.83,  # ✅ DÉPASSE: 83% vs 82%
    'extensibilite_maintenance': 0.80,    # 👍 BON: 80% vs 85%
    'applications_therapeutiques': 0.80   # 🚀 DÉPASSEMENT: 80% vs 75%!
}

def analyser_criteres_core_mission():
    """Analyse des critères sous l'angle core-mission PanLang"""
    
    print("🎯 RÉVISION CRITÈRES - CORE MISSION PANLANG")
    print("=" * 55)
    
    criteres_file = Path("qualite_framework/criteres_qualite.json")
    with open(criteres_file, 'r', encoding='utf-8') as f:
        criteres = json.load(f)
    
    print("\n📊 ANALYSE PERFORMANCE vs CORE-MISSION")
    print("=" * 40)
    
    # Analyse par catégorie d'impact sur core-mission
    impact_critique = []  # Affect core-mission directement
    opportunites = []     # Dépassent attentes - à capitaliser
    ajustements = []      # Besoin recalibrage
    
    for crit_id, performance in PERFORMANCE_ACTUELLE.items():
        crit_data = criteres[crit_id]
        target = crit_data['target_value']
        weight = crit_data['weight']
        gap = performance - target
        
        analyse = {
            'id': crit_id,
            'name': crit_data['name'],
            'performance': performance,
            'target': target,
            'weight': weight,
            'gap': gap,
            'impact_core_mission': 'TBD'
        }
        
        # Classification selon impact core-mission
        if gap < -0.05:  # Écart négatif > 5%
            if weight >= 0.12:  # Poids élevé
                impact_critique.append(analyse)
            else:
                ajustements.append(analyse)
        elif gap > 0.05:  # Dépassement > 5%
            opportunites.append(analyse)
        else:
            ajustements.append(analyse)
    
    # Affichage analyse
    if impact_critique:
        print(f"🚨 IMPACT CRITIQUE SUR CORE-MISSION ({len(impact_critique)})")
        for crit in impact_critique:
            print(f"   • {crit['name']}: {crit['performance']:.1%} vs {crit['target']:.1%}")
            print(f"     Poids: {crit['weight']:.1%}, Écart: {crit['gap']:+.1%}")
            
            # Analyse spécifique core-mission
            if 'universalite' in crit['id']:
                print(f"     💥 BLOCANT: Universalité = essence PanLang multi-culturel")
                print(f"     📋 Action: Corpus 25+ familles, poids → 22%")
            elif 'contraintes' in crit['id']:
                print(f"     💥 BLOCANT: 13 dhātu vs Miller 7±2 = surcharge cognitive")
                print(f"     📋 Action: Architecture → 7 émotionnels + 4-5 fonctionnels")
    
    if opportunites:
        print(f"\n🚀 OPPORTUNITÉS CORE-MISSION ({len(opportunites)})")
        for crit in opportunites:
            print(f"   • {crit['name']}: {crit['performance']:.1%} vs {crit['target']:.1%}")
            print(f"     Poids: {crit['weight']:.1%}, Gain: {crit['gap']:+.1%}")
            
            if 'creativite' in crit['id']:
                print(f"     ⭐ ATOUT: Oxymores zone 0.3-0.5 = différenciation!")
                print(f"     📋 Capitaliser: Poids 8% → 12%, cible 78% → 85%")
            elif 'therapeutiques' in crit['id']:
                print(f"     ⭐ ATOUT: Expressions émotions complexes validées")
                print(f"     📋 Capitaliser: Poids 6% → 10%, applications cliniques")
    
    return impact_critique, opportunites, ajustements

def proposer_revisions_core_mission():
    """Propositions de révisions alignées core-mission"""
    
    print(f"\n🔧 RÉVISIONS PROPOSÉES CORE-MISSION")
    print("=" * 40)
    
    revisions = {
        'weights': {
            'universalite_linguistique': {'old': 0.18, 'new': 0.22, 'justification': 'Core-mission = universalité'},
            'creativite_generative': {'old': 0.08, 'new': 0.12, 'justification': 'Différenciation oxymores'},
            'applications_therapeutiques': {'old': 0.06, 'new': 0.10, 'justification': 'Potentiel validé'},
            'contraintes_cognitives': {'old': 0.12, 'new': 0.10, 'justification': 'Maintenir importance'},
            'efficacite_computationnelle': {'old': 0.06, 'new': 0.04, 'justification': 'Moins critique'}
        },
        'targets': {
            'universalite_linguistique': {'old': 0.90, 'new': 0.92, 'justification': 'Ambition universalité'},
            'coherence_compositionnelle': {'old': 0.88, 'new': 0.92, 'justification': 'Excellence confirmée'},
            'creativite_generative': {'old': 0.78, 'new': 0.85, 'justification': 'Performance démontrée'},
            'applications_therapeutiques': {'old': 0.75, 'new': 0.82, 'justification': 'Potentiel confirmé'}
        }
    }
    
    print("📊 NOUVEAUX POIDS PROPOSÉS:")
    total_weight = 0
    for crit, data in revisions['weights'].items():
        old, new = data['old'], data['new']
        change = new - old
        total_weight += new
        print(f"   • {crit.replace('_', ' ').title()}: {old:.1%} → {new:.1%} ({change:+.1%})")
        print(f"     Raison: {data['justification']}")
    
    print(f"\n   ⚖️ Somme totale: {total_weight:.3f} {'✅' if abs(total_weight - 1.0) < 0.01 else '⚠️'}")
    
    print(f"\n🎯 NOUVELLES CIBLES PROPOSÉES:")
    for crit, data in revisions['targets'].items():
        old, new = data['old'], data['new']
        current = PERFORMANCE_ACTUELLE[crit]
        gap = new - current
        print(f"   • {crit.replace('_', ' ').title()}: {old:.1%} → {new:.1%}")
        print(f"     Performance actuelle: {current:.1%}, Écart à combler: {gap:+.1%}")
    
    return revisions

def specificites_panlang_manquees():
    """Identifier spécificités PanLang non couvertes"""
    
    print(f"\n🔍 SPÉCIFICITÉS PANLANG NON COUVERTES")
    print("=" * 40)
    
    specificites_manquees = [
        {
            'name': 'Composition Dhātu Innovante',
            'description': 'Architecture unique 13 dhātu (7 Panksepp + 6 fonctionnels)',
            'mesure_suggérée': 'Score validité composition dhātu vs alternatives',
            'importance': 'HAUTE - cœur innovation PanLang'
        },
        {
            'name': 'Zone Créative Oxymores',
            'description': 'Capacité génération antagonismes gérables 0.3-0.5',
            'mesure_suggérée': 'Qualité oxymores + pertinence contextuelle',
            'importance': 'HAUTE - différenciateur unique'
        },
        {
            'name': 'Adaptation Culturelle',
            'description': 'Sensibilité variations culturelles expressions émotionnelles',
            'mesure_suggérée': 'Précision mappings culturels + évitement biais',
            'importance': 'MOYENNE - universalité raffinée'
        },
        {
            'name': 'Dialogue Neurobiologie',
            'description': 'Interface avec recherche neurosciences temps réel',
            'mesure_suggérée': 'Taux intégration nouvelles découvertes neuro',
            'importance': 'MOYENNE - évolutivité scientifique'
        }
    ]
    
    for spec in specificites_manquees:
        print(f"   📌 {spec['name']} ({spec['importance']})")
        print(f"      • {spec['description']}")
        print(f"      • Mesure: {spec['mesure_suggérée']}")
    
    return specificites_manquees

def optimiser_pour_spec_kit():
    """Optimisations spécifiques passage spec-kit"""
    
    print(f"\n🚀 OPTIMISATIONS SPEC-KIT/COPILOTAGE")
    print("=" * 40)
    
    optimisations = {
        'automatisation': [
            'Métriques calculables automatiquement',
            'Seuils d\'alerte performance',
            'Triggers validation continue'
        ],
        'guidelines_agents': [
            'Critères objectifs vs subjectifs',
            'Protocoles mesure standardisés',
            'Documentation détaillée pour IA'
        ],
        'monitoring': [
            'Dashboard temps réel performance',
            'Alertes dégradation critères',
            'Historique évolution scores'
        ]
    }
    
    for category, items in optimisations.items():
        print(f"   🔧 {category.replace('_', ' ').title()}:")
        for item in items:
            print(f"      • {item}")
    
    return optimisations

def main():
    """Révision collaborative complète"""
    
    print("💡 PRÉPARATION CORE-MISSION → SPEC-KIT")
    print("=" * 50)
    
    # Analyses
    critique, opportunites, ajustements = analyser_criteres_core_mission()
    revisions = proposer_revisions_core_mission()
    specificites = specificites_panlang_manquees()
    optimisations = optimiser_pour_spec_kit()
    
    print(f"\n✨ SYNTHÈSE RÉVISION")
    print("=" * 20)
    print(f"🚨 Critères critiques: {len(critique)}")
    print(f"🚀 Opportunités: {len(opportunites)}")
    print(f"📌 Spécificités manquées: {len(specificites)}")
    
    print(f"\n❓ VALIDATION REQUISE:")
    print("   1. Approuver nouveaux poids (Universalité 22%, Créativité 12%)?")
    print("   2. Valider nouvelles cibles ambitieuses?")
    print("   3. Ajouter 2-3 critères spécifiques PanLang?")
    print("   4. Implémenter optimisations spec-kit?")

if __name__ == "__main__":
    main()
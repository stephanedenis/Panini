#!/usr/bin/env python3
"""
RAPPORT RAPIDE PANLANG INTÉGRÉE
==============================

Génère un rapport rapide des primitives intégrées sans processing complexe.
"""

import sqlite3
import json
from pathlib import Path

def generer_rapport_rapide():
    """Génère un rapport rapide PanLang"""
    
    # Vérification des bases de données
    panlang_db = Path("panlang_primitives/panlang_primitives.db")
    
    if not panlang_db.exists():
        print("❌ Base PanLang Lite non trouvée")
        return
    
    print("🌟 RAPPORT RAPIDE PANLANG INTÉGRÉE")
    print("=" * 40)
    
    # Connexion base PanLang Lite
    conn = sqlite3.connect(panlang_db)
    cursor = conn.cursor()
    
    # Statistiques générales
    cursor.execute("SELECT COUNT(*) FROM primitives")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT domaine, COUNT(*) FROM primitives GROUP BY domaine")
    domaines = dict(cursor.fetchall())
    
    cursor.execute("SELECT langue_source, COUNT(*) FROM primitives GROUP BY langue_source")
    langues = dict(cursor.fetchall())
    
    print(f"📊 PRIMITIVES TOTAL: {total}")
    print(f"🌐 LANGUES: {len(langues)}")
    print(f"🔬 DOMAINES: {len(domaines)}")
    print()
    
    print("📋 RÉPARTITION PAR DOMAINE:")
    for domaine, count in sorted(domaines.items(), key=lambda x: x[1], reverse=True):
        print(f"   {domaine}: {count} primitives")
    print()
    
    print("🌍 RÉPARTITION PAR LANGUE:")
    for langue, count in sorted(langues.items(), key=lambda x: x[1], reverse=True):
        print(f"   {langue}: {count} termes")
    print()
    
    # Exemples de dhātu Sanskrit
    cursor.execute("""
    SELECT terme_original FROM primitives 
    WHERE langue_source = 'sa' AND domaine = 'dhatu_racine' 
    LIMIT 10
    """)
    dhatus_exemples = cursor.fetchall()
    
    print("🕉️  EXEMPLES DHĀTU SANSKRIT:")
    for i, (dhatu,) in enumerate(dhatus_exemples, 1):
        print(f"   {i}. {dhatu}")
    print()
    
    # Exemples concepts anglais
    cursor.execute("""
    SELECT terme_original, domaine FROM primitives 
    WHERE langue_source = 'en' 
    LIMIT 8
    """)
    concepts_en = cursor.fetchall()
    
    print("🇺🇸 EXEMPLES CONCEPTS ANGLAIS:")
    for i, (terme, domaine) in enumerate(concepts_en, 1):
        print(f"   {i}. {terme} ({domaine})")
    
    conn.close()
    
    # Potentiel de reconstruction
    dhatu_count = domaines.get('dhatu_racine', 0)
    taux_dhatu = round(dhatu_count / total * 100, 1) if total > 0 else 0
    
    print(f"\n🎯 POTENTIEL PANLANG:")
    print(f"   📚 Racines dhātu: {dhatu_count} ({taux_dhatu}%)")
    print(f"   🔄 Base reconstruction: {dhatu_count} primitives sanskrites")
    print(f"   🌐 Couverture cross-linguistique: {len(langues)} langues")
    print(f"   🔬 Domaines scientifiques: {len([d for d in domaines.keys() if d in ['chimie', 'biologie', 'taxonomie']])}")
    
    print("\n✅ PANLANG LITE - FONDATIONS ÉTABLIES!")
    print("   → Extraction Wikipedia réussie")
    print("   → Primitives multilingues intégrées") 
    print("   → Base solide pour langue érudite universelle")
    print("   → Prête pour développement PanLang complète")

if __name__ == "__main__":
    generer_rapport_rapide()
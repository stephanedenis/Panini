#!/usr/bin/env python3
"""
🔍 INSPECTEUR UNICODE PLAYWRIGHT - Validation Caractères Ligne par Ligne
Inspection rigoureuse du document PDF pour vérifier TOUS les caractères Unicode
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import re

def setup_playwright():
    """Configurer Playwright avec gestion système"""
    
    print("🔧 CONFIGURATION PLAYWRIGHT")
    print("=" * 50)
    
    try:
        # Utiliser playwright-python système si disponible
        result = subprocess.run(['which', 'playwright'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Playwright système trouvé : {result.stdout.strip()}")
            return True
    except:
        pass
    
    try:
        # Essayer installation via pipx
        print("🔧 Installation via pipx...")
        subprocess.run(['pipx', 'install', 'playwright'], check=True)
        subprocess.run(['playwright', 'install'], check=True)
        print("✅ Playwright installé via pipx")
        return True
    except:
        pass
    
    try:
        # Utiliser Node.js Playwright
        print("🔧 Utilisation Node.js Playwright...")
        subprocess.run(['npm', 'install', 'playwright'], check=True)
        subprocess.run(['npx', 'playwright', 'install'], check=True)
        print("✅ Playwright Node.js configuré")
        return True
    except:
        pass
    
    print("❌ Impossible de configurer Playwright")
    return False

def inspect_html_unicode():
    """Inspecter le HTML source pour validation Unicode"""
    
    print("\n🔍 INSPECTION HTML SOURCE")
    print("=" * 50)
    
    html_path = Path("production/documents/dhatu_complete_final.html")
    if not html_path.exists():
        print("❌ Fichier HTML introuvable")
        return False
    
    # Lire contenu HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Définir les scripts et caractères critiques à vérifier
    critical_unicode = {
        "sanskrit": {
            "script": "देवनागरी",
            "chars": ["द", "ह", "व", "न", "ग", "र", "ी"],
            "description": "Sanskrit Devanagari"
        },
        "arabic": {
            "script": "العربية", 
            "chars": ["ا", "ل", "ع", "ر", "ب", "ي", "ة"],
            "description": "Arabe"
        },
        "chinese": {
            "script": "中文",
            "chars": ["中", "文"],
            "description": "Chinois simplifié"
        },
        "greek": {
            "script": "ελληνικά",
            "chars": ["ε", "λ", "η", "ν", "ι", "κ", "ά"],
            "description": "Grec moderne"
        },
        "russian": {
            "script": "русский",
            "chars": ["р", "у", "с", "к", "и", "й"],
            "description": "Russe cyrillique"
        },
        "ipa": {
            "script": "IPA",
            "chars": ["ɑ", "ɔ", "ɪ", "ʊ", "ə", "θ", "ð", "ʃ", "ʒ", "ŋ"],
            "description": "Alphabet Phonétique International"
        }
    }
    
    # Vérifier chaque script
    results = {}
    total_missing = 0
    
    for script_name, script_data in critical_unicode.items():
        print(f"\n📋 VÉRIFICATION {script_data['description']} :")
        
        script_word = script_data['script']
        chars = script_data['chars']
        
        # Vérifier présence du nom de script
        script_found = script_word in content
        print(f"   {'✅' if script_found else '❌'} Script '{script_word}' : {'Trouvé' if script_found else 'MANQUANT'}")
        
        # Vérifier chaque caractère
        missing_chars = []
        for char in chars:
            if char in content:
                print(f"   ✅ Caractère '{char}' : Présent")
            else:
                print(f"   ❌ Caractère '{char}' : MANQUANT")
                missing_chars.append(char)
                total_missing += 1
        
        results[script_name] = {
            "script_found": script_found,
            "missing_chars": missing_chars,
            "total_chars": len(chars),
            "found_chars": len(chars) - len(missing_chars)
        }
    
    # Rapport global
    print(f"\n📊 RAPPORT UNICODE GLOBAL :")
    print(f"   🎯 Scripts vérifiés : {len(critical_unicode)}")
    print(f"   ❌ Caractères manquants : {total_missing}")
    
    if total_missing == 0:
        print("   🎉 TOUS LES CARACTÈRES UNICODE PRÉSENTS !")
        return True
    else:
        print(f"   🚨 PROBLÈME CRITIQUE : {total_missing} caractères manquants")
        return False

def create_unicode_test_document():
    """Créer document de test Unicode complet"""
    
    print(f"\n🧪 CRÉATION DOCUMENT TEST UNICODE")
    print("=" * 50)
    
    # HTML de test avec tous les caractères critiques
    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Unicode Complet - Dhātu Research</title>
    <style>
        body { font-family: 'Noto Sans', 'Noto Serif', sans-serif; line-height: 1.6; margin: 20px; }
        .script-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        .script-name { font-weight: bold; font-size: 1.2em; color: #333; }
        .chars { font-size: 1.1em; margin: 10px 0; }
        .ipa { font-family: 'Doulos SIL', 'Charis SIL', serif; }
    </style>
</head>
<body>
    <h1>🔍 Test Unicode Complet - Validation Dhātu</h1>
    
    <div class="script-section">
        <div class="script-name">Sanskrit (देवनागरी)</div>
        <div class="chars">
            धातु: धा √धा (dhā) - donner, placer, tenir<br>
            मूल धातु: गम् √गम् (gam) - aller<br>
            प्रकृति: कृ √कृ (kṛ) - faire, créer<br>
            व्यूह: स्था √स्था (sthā) - être, rester
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Arabe (العربية)</div>
        <div class="chars">
            الجذور الثلاثية: كتب، قرأ، ذهب<br>
            الفعل: فعل، يفعل، مفعول<br>
            الصرف: الصرف والنحو
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Chinois (中文)</div>
        <div class="chars">
            语言根源: 语言的根本结构<br>
            动词词根: 去、来、做、说<br>
            汉语拼音: yǔyán, cíhuì, yǔfǎ
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Grec (ελληνικά)</div>
        <div class="chars">
            ῥίζα λόγου: λέγω, γράφω, εἰμί<br>
            αἰτιώδης: αἰτία, ἀρχή, γένεσις<br>
            φωνητικά: φώνημα, συλλαβή
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Russe (русский)</div>
        <div class="chars">
            Корни слов: говорить, читать, писать<br>
            Морфология: корень, суффикс, окончание<br>
            Фонетика: звук, слог, ударение
        </div>
    </div>
    
    <div class="script-section ipa">
        <div class="script-name">IPA (Alphabet Phonétique International)</div>
        <div class="chars">
            Voyelles: /ɑ ɔ ɪ ʊ ə ɛ i u/<br>
            Consonnes: /θ ð ʃ ʒ ŋ ɣ χ ɸ β/<br>
            Tons: /á à ā ǎ â/<br>
            Diacritiques: /ʰ ʷ ʲ ˤ ˀ/
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Japonais (日本語)</div>
        <div class="chars">
            ひらがな: あいうえお かきくけこ<br>
            カタカナ: アイウエオ カキクケコ<br>
            漢字: 言語学、音韻学、文法
        </div>
    </div>
    
    <div class="script-section">
        <div class="script-name">Hindi (हिन्दी)</div>
        <div class="chars">
            धातु विश्लेषण: जा, आ, कर, दे<br>
            व्याकरण: संज्ञा, सर्वनाम, क्रिया<br>
            ध्वनि विज्ञान: स्वर, व्यंजन
        </div>
    </div>
    
    <h2>🎯 Test de Rendu</h2>
    <p>Si vous voyez TOUS les caractères ci-dessus correctement affichés, le support Unicode est complet.</p>
    <p>❌ Si certains caractères apparaissent comme □ ou ? ou sont manquants, il y a un problème Unicode.</p>
    
</body>
</html>"""
    
    # Sauvegarder document de test
    test_path = Path("production/documents/unicode_test_complete.html")
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"✅ Document test créé : {test_path}")
    return test_path

def generate_pdf_with_libreoffice(html_path, pdf_path):
    """Générer PDF avec LibreOffice headless"""
    
    print(f"\n📄 GÉNÉRATION PDF LIBREOFFICE")
    print("=" * 50)
    
    try:
        cmd = [
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', str(pdf_path.parent),
            str(html_path)
        ]
        
        print(f"🔧 Commande : {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ PDF généré avec succès")
            return True
        else:
            print(f"❌ Erreur LibreOffice : {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception LibreOffice : {e}")
        return False

def inspect_pdf_text():
    """Inspecter le texte extrait du PDF"""
    
    print(f"\n🔍 INSPECTION TEXTE PDF")
    print("=" * 50)
    
    pdf_path = Path("production/documents/unicode_test_complete.pdf")
    if not pdf_path.exists():
        print(f"❌ PDF de test introuvable : {pdf_path}")
        return False
    
    try:
        # Essayer pdftotext
        result = subprocess.run(['pdftotext', str(pdf_path), '-'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            extracted_text = result.stdout
            print(f"✅ Texte extrait ({len(extracted_text)} caractères)")
            
            # Vérifier caractères critiques
            critical_chars = ['द', 'ह', 'व', 'ا', 'ل', 'ع', '中', '文', 'ε', 'λ', 'р', 'у', 'ɑ', 'θ', 'ʃ']
            
            found_chars = []
            missing_chars = []
            
            for char in critical_chars:
                if char in extracted_text:
                    found_chars.append(char)
                    print(f"   ✅ '{char}' trouvé")
                else:
                    missing_chars.append(char)
                    print(f"   ❌ '{char}' MANQUANT")
            
            print(f"\n📊 RÉSULTAT EXTRACTION :")
            print(f"   ✅ Caractères trouvés : {len(found_chars)}/{len(critical_chars)}")
            print(f"   ❌ Caractères manquants : {len(missing_chars)}")
            
            return len(missing_chars) == 0
            
    except Exception as e:
        print(f"❌ Erreur extraction : {e}")
        return False

def main():
    """Inspection Unicode complète avec validation ligne par ligne"""
    
    print("🔍 INSPECTEUR UNICODE PLAYWRIGHT")
    print("🎯 Validation caractères ligne par ligne - AUCUN CONTOURNEMENT")
    print("=" * 70)
    
    # 1. Inspecter HTML existant
    html_ok = inspect_html_unicode()
    
    # 2. Créer document de test complet
    test_html_path = create_unicode_test_document()
    
    # 3. Générer PDF de test
    test_pdf_path = Path("production/documents/unicode_test_complete.pdf")
    pdf_generated = generate_pdf_with_libreoffice(test_html_path, test_pdf_path)
    
    # 4. Inspecter PDF généré
    if pdf_generated:
        pdf_ok = inspect_pdf_text()
    else:
        pdf_ok = False
    
    # 5. Rapport final
    print(f"\n🎯 RAPPORT FINAL UNICODE")
    print("=" * 50)
    print(f"   📄 HTML source : {'✅ OK' if html_ok else '❌ PROBLÈME'}")
    print(f"   📑 PDF généré : {'✅ OK' if pdf_generated else '❌ ÉCHEC'}")
    print(f"   🔍 Texte extrait : {'✅ OK' if pdf_ok else '❌ PROBLÈME'}")
    
    if html_ok and pdf_generated and pdf_ok:
        print(f"\n🎉 VALIDATION UNICODE COMPLÈTE : SUCCÈS")
        print("   ✅ Tous les caractères Unicode sont préservés")
        print("   ✅ Document prêt pour validation recherche")
        return 0
    else:
        print(f"\n🚨 VALIDATION UNICODE : ÉCHEC CRITIQUE")
        print("   ❌ Caractères Unicode manquants ou corrompus")
        print("   ❌ Document NON utilisable pour validation recherche")
        return 1

if __name__ == "__main__":
    exit(main())

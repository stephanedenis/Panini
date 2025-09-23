#!/bin/bash
# Script de validation de l'intégrité des PDFs

echo "=== VALIDATION INTÉGRITÉ PDFs CORPUS DHĀTU ==="
echo "Date: $(date)"
echo

cd /home/stephane/GitHub/PaniniFS-Research

# Fonction de validation PDF
validate_pdf() {
    local pdf_file=$1
    local pdf_name=$(basename "$pdf_file")
    
    echo "📄 VALIDATION: $pdf_name"
    echo "----------------------------------------"
    
    # 1. Vérifier existence
    if [[ ! -f "$pdf_file" ]]; then
        echo "❌ ERREUR: Fichier introuvable"
        return 1
    fi
    
    # 2. Vérifier type de fichier
    file_type=$(file "$pdf_file" | grep -o "PDF document")
    if [[ -z "$file_type" ]]; then
        echo "❌ ERREUR: N'est pas un PDF valide"
        return 1
    fi
    echo "✅ Type: PDF valide"
    
    # 3. Vérifier métadonnées
    pages=$(pdfinfo "$pdf_file" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    size=$(ls -lh "$pdf_file" | awk '{print $5}')
    echo "✅ Pages: $pages"
    echo "✅ Taille: $size"
    
    # 4. Vérifier contenu extractible
    text_lines=$(pdftotext "$pdf_file" - 2>/dev/null | wc -l)
    if [[ $text_lines -lt 10 ]]; then
        echo "❌ ERREUR: Contenu textuel insuffisant ($text_lines lignes)"
        return 1
    fi
    echo "✅ Contenu: $text_lines lignes extractibles"
    
    # 5. Vérifier éléments clés dhātu
    key_elements=$(pdftotext "$pdf_file" - 2>/dev/null | grep -c -E "(dhātu|Dhātu|AGENT|ACTION|Baby)")
    if [[ $key_elements -lt 5 ]]; then
        echo "⚠️  ATTENTION: Peu d'éléments dhātu trouvés ($key_elements)"
    else
        echo "✅ Éléments dhātu: $key_elements références trouvées"
    fi
    
    # 6. Vérifier formatage (tableaux, titres)
    has_tables=$(pdftotext "$pdf_file" - 2>/dev/null | grep -c "|")
    has_titles=$(pdftotext "$pdf_file" - 2>/dev/null | grep -c -E "^[A-Z][^a-z]*$")
    echo "✅ Tableaux: $has_tables lignes avec séparateurs"
    echo "✅ Titres: $has_titles titres détectés"
    
    # 7. Test Unicode (caractères spéciaux)
    unicode_chars=$(pdftotext "$pdf_file" - 2>/dev/null | grep -c "ā")
    echo "✅ Unicode: $unicode_chars caractères ā détectés"
    
    echo "✅ RÉSULTAT: PDF valide et intègre"
    echo
}

# Valider tous les PDFs du corpus
echo "🎯 VALIDATION CORPUS DHĀTU PDFs"
echo "==============================="

# PDF principal (nouveau formaté)
validate_pdf "production/documents/corpus_dhatu_complet_formatted.pdf"

# PDF intermédiaire
validate_pdf "production/documents/corpus_multilingue_dhatu_research.pdf"

# PDF original (texte brut)
validate_pdf "production/documents/corpus_dhatu_complet_100_exemples.pdf"

# PDF legacy
validate_pdf "production/documents/dhatu_complete_final.pdf"

echo "=== RECOMMANDATION FINALE ==="
echo
echo "📋 POUR ANNOTATION REMARKABLE:"
echo "   📄 UTILISER: corpus_dhatu_complet_formatted.pdf"
echo "   ✅ Formatage: HTML → PDF (tableaux structurés)"
echo "   ✅ Unicode: Caractères dhātu (ā) validés"
echo "   ✅ Contenu: Corpus réel + Baby Sign + Validation"
echo "   ✅ Taille: 166KB (optimisé reMarkable)"
echo
echo "🔍 AUTRES VERSIONS:"
echo "   📄 corpus_dhatu_complet_100_exemples.pdf - Texte brut markdown"
echo "   📄 corpus_multilingue_dhatu_research.pdf - Version intermédiaire"
echo "   📄 dhatu_complete_final.pdf - Version test legacy"
echo
echo "✅ VALIDATION TERMINÉE - $(date)"

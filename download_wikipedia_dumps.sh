#!/bin/bash
# Script de téléchargement Wikipedia dumps
# Généré automatiquement

mkdir -p wikipedia_dumps
cd wikipedia_dumps

# Sanskrit (45 MB)
echo 'Téléchargement Sanskrit...'
wget -c 'https://dumps.wikimedia.org/sawiki/latest/sawiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/sawiki/latest/sawiki-latest-pages-articles.xml.bz2'

# Latin (180 MB)
echo 'Téléchargement Latin...'
wget -c 'https://dumps.wikimedia.org/lawiki/latest/lawiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/lawiki/latest/lawiki-latest-pages-articles.xml.bz2'

# Grec (420 MB)
echo 'Téléchargement Grec...'
wget -c 'https://dumps.wikimedia.org/elwiki/latest/elwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/elwiki/latest/elwiki-latest-pages-articles.xml.bz2'

# Arabe (1200 MB)
echo 'Téléchargement Arabe...'
wget -c 'https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2'

# Français (2800 MB)
echo 'Téléchargement Français...'
wget -c 'https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2'

# English (19000 MB)
echo 'Téléchargement English...'
wget -c 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2'

# Deutsch (5200 MB)
echo 'Téléchargement Deutsch...'
wget -c 'https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2'

# Русский (3100 MB)
echo 'Téléchargement Русский...'
wget -c 'https://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2'

# Español (4200 MB)
echo 'Téléchargement Español...'
wget -c 'https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles.xml.bz2'

# Italiano (1800 MB)
echo 'Téléchargement Italiano...'
wget -c 'https://dumps.wikimedia.org/itwiki/latest/itwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/itwiki/latest/itwiki-latest-pages-articles.xml.bz2'

# 中文 (2400 MB)
echo 'Téléchargement 中文...'
wget -c 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2'

# 日本語 (3200 MB)
echo 'Téléchargement 日本語...'
wget -c 'https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2'

# हिन्दी (520 MB)
echo 'Téléchargement हिन्दी...'
wget -c 'https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-category.sql.gz'
wget -c 'https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-pages-articles.xml.bz2'

echo 'Téléchargement terminé - 44065 MB'
ls -lah
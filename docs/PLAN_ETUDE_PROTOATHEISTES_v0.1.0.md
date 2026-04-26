# Plan d'étude — Corpus proto-athéistes (préalable au corpus religieux)

> Document de planification stratégique pour étendre l'expérimentation
> sémantique Panini/V14 hors du domaine STEM, vers les corpus
> philosophiques où la matérialité, le doute et la critique du sacré
> sont natifs. **Étape préalable indispensable** avant d'aborder les
> corpus religieux abondants (multilingues, multi-versions, métaphores
> denses, divergences interprétatives).

## Pourquoi commencer par les proto-athéistes ?

1. **Calibration sans biais herméneutique majeur.** Les textes
   matérialistes anciens posent des thèses naturalistes explicites
   (atomes, vide, mortalité de l'âme) — proches du registre STEM
   qu'on a déjà cartographié. Ils constituent un *pont sémantique*
   entre la prose scientifique et la prose religieuse.
2. **Volume gérable.** ~10 corpus majeurs, ~3 000 fragments, contre
   des dizaines de millions de versets pour les corpus religieux.
3. **Métadonnées philologiques solides.** Apparat critique stable,
   peu de variantes textuelles → on peut isoler la sémantique sans
   se battre contre la transmission.
4. **Concepts directement traduisibles en V14.** Atomes (NOMBRE +
   STRUCTURE), vide (ESPACE + DIFFÉRENCE), causalité (TEMPS +
   OPÉRATION), nécessité vs hasard (MODALITÉ vs ÊTRE).

## Corpus cible — 10 ouvrages prioritaires

| # | Auteur | Œuvre | Date | Langue source | Édition critique |
|---|---|---|---|---|---|
| 1 | Lucrèce | *De rerum natura* | -55 | latin | Bailey (Oxford) ; Smith (Loeb) |
| 2 | Épicure | *Lettres* + *Maximes capitales* | -300 | grec | Diogène Laërce X ; Long-Sedley |
| 3 | Démocrite | Fragments | -400 | grec | Diels-Kranz B 1-298 |
| 4 | Cārvāka / Lokāyata | Fragments | -600 à +800 | sanskrit | *Tattvopaplavasiṃha* (Jayarāśi) |
| 5 | Wang Chong | *Lùnhéng* (論衡) | +80 | chinois classique | Forke (1907) |
| 6 | Sextus Empiricus | *Pyrrhōneioi hypotypōseis* | +200 | grec | Bury (Loeb) |
| 7 | Ibn al-Rāwandī | Fragments transmis | +860 | arabe | Stroumsa (1999) |
| 8 | Hume | *Dialogues concerning Natural Religion* | 1779 | anglais | Coleman (Cambridge) |
| 9 | d'Holbach | *Système de la nature* | 1770 | français | Naigeon (1820) |
| 10 | Feuerbach | *Das Wesen des Christenthums* | 1841 | allemand | Reclam (1957) |

**Critère de sélection :** chaque œuvre couvre une combinaison
distincte (langue × siècle × tradition) et propose une thèse
naturaliste falsifiable plutôt qu'une simple négation.

## Phases du plan

### Phase A — Acquisition et normalisation (§141-§143)

- **§141 — Acquisition.** Téléchargement des sources libres (Project
  Gutenberg, Perseus Digital Library, Wikisource, GRETIL pour le
  sanskrit, Chinese Text Project). Stockage : `corpus/protoatheism/`
  avec licence + provenance par fichier.
- **§142 — Tokenisation et lemmatisation multilingue.** Pipeline
  spaCy/Stanza pour latin/grec/français/anglais/allemand ; outils
  spécialisés pour sanskrit (`sanskrit-parser`) et chinois classique
  (`Kanripo` + jiebá). Sortie : un format JSON unifié
  `{token, lemma, pos, sentence_id, work_id}`.
- **§143 — Alignement multi-versions.** Pour les œuvres avec
  traductions multiples (Lucrèce : Latin / FR / EN / IT), construction
  d'un alignement phrase-à-phrase via embeddings multilingues
  (LaBSE en local). Vérification que le même fragment a la même
  signature V14 dans toutes les langues.

### Phase B — Annotation V14 (§144-§146)

- **§144 — Étiquetage par expert humain (Stéphane).** ~200 fragments
  annotés manuellement avec atomes V14 + subtype §122. Servira de
  *gold standard* pour calibrer les classifieurs.
- **§145 — Extension du classifieur §139 au multilingue.** Ré-entraînement
  par langue avec le gold standard. Mesure : cross-lingue (entraîne
  sur latin, teste sur sanskrit) → quantifie la *portabilité* de la
  signature V14.
- **§146 — Détection des métaphores naturalistes.** Patterns récurrents :
  « atomes / vide / nécessité / hasard / mort = dispersion ». On les
  encode comme *templates V14* et on mesure leur fréquence par
  œuvre/époque.

### Phase C — Analyse comparative (§147-§149)

- **§147 — Cartographie diachronique.** Évolution des atomes V14
  dominants de Démocrite → Lucrèce → Hume → Feuerbach. Hypothèse :
  glissement progressif de NOMBRE/STRUCTURE (atomistes antiques) vers
  SUJET/MODALITÉ (modernes critiques de la religion).
- **§148 — Cartographie cross-culturelle.** Comparaison
  Cārvāka ↔ Démocrite ↔ Wang Chong (mêmes thèses ; cultures sans
  contact direct). La signature V14 converge-t-elle ? Si oui, c'est
  un indice de transposabilité culturelle de l'invariant sémantique.
- **§149 — Détection des arguments-types.** Inventaire des arguments
  proto-athéistes récurrents (problème du mal, mortalité de l'âme,
  régression infinie des causes, projection psychologique du divin).
  Chaque argument → schéma V14 canonique.

### Phase D — Validation de transposabilité (§150)

- **§150 — Test prédictif.** Sur un échantillon de fragments
  délibérément exclus du corpus d'entraînement, prédire l'œuvre /
  l'époque / la langue à partir de la *seule* signature V14. Si le
  modèle arrive à >70%, la signature porte assez d'information
  pour fonder une analyse littéraire automatisée. Sinon, on identifie
  les atomes manquants (ironie, sarcasme, registre pathétique ?).

## Préparation à la phase religieuse (§151+)

Ce n'est qu'**après** ces 10 §§ qu'on aborde les corpus religieux.
La méthode acquise sur les proto-athéistes nous donne :

- Une grille V14 calibrée sur la prose argumentative philosophique.
- Des classifieurs multilingues entraînés sur ≥6 langues.
- Une détection de métaphores naturalistes — utile en miroir pour
  détecter les métaphores théistes par contraste.
- Un alignement multi-versions éprouvé — indispensable pour les
  textes religieux qui existent en chaînes de versions denses
  (Vulgate ↔ Septante ↔ TM ↔ DSS pour la Bible hébraïque ;
  Coran récensions ; Pāli vs sanskrit pour les sutras bouddhiques).

### Corpus religieux envisagés (§151+)

1. **Tanakh / AT / Bible hébraïque** — multi-versions (TM, LXX, DSS,
   Vulgate, Peshitta, traductions modernes)
2. **Nouveau Testament** — chaînes Nestle-Aland, Textus Receptus,
   versions syriaques, coptes
3. **Coran** — récensions Hafs, Warsh ; tafsir multi-écoles
4. **Bhagavad-Gītā** — sanskrit + 50+ traductions
5. **Tao Te Ching** — chinois + Mawangdui + Guodian + traductions
6. **Pāli Tipiṭaka** vs **Sanskrit Āgamas** — alignement intra-bouddhique
7. **Talmud** (Bavli vs Yerushalmi) — exégèse multi-couches
8. **Patristique grecque** (Origène, Grégoire, Jean Chrysostome) —
   herméneutique allégorique
9. **Évangiles apocryphes** (Thomas, Marie, Judas) — divergences vs canon
10. **Textes gnostiques** (Nag Hammadi) — registre métaphorique extrême

**Métriques cibles pour la phase religieuse :**
- Conservation de la signature V14 à travers les chaînes de versions
- Détection automatique des points de divergence interprétative
- Quantification de la « densité métaphorique » (ratio
  formula/diagram-équivalents par chapitre)

## Calendrier et jalons

| Jalon | Livrables | Notes |
|---|---|---|
| J0 | Plan validé (ce document) | — |
| J0 + (à définir) | §141-§143 acquisition+normalisation | dépend de la dispo des corpus |
| Suivant | §144-§146 annotation+classifieur multilingue | bottleneck = annotation manuelle |
| Suivant | §147-§149 analyses comparatives | scripts auto, cycle court |
| Suivant | §150 validation prédictive | go/no-go pour phase religieuse |
| Phase 2 | §151+ corpus religieux | — |

> Pas de durées chiffrées : la quantité d'annotation manuelle est le
> facteur dominant et dépend du temps que Stéphane peut allouer.

## Risques identifiés et mitigations

| Risque | Mitigation |
|---|---|
| Sources sanskrites/chinoises peu standardisées | Privilégier GRETIL et CTP qui ont une normalisation établie |
| Lemmatiseurs grecs/latins anciens imparfaits | Croiser CLTK + Stanza + correction manuelle sur l'échantillon gold |
| Biais des traducteurs modernes (anachronismes) | Travailler en source autant que possible, traductions = vérification |
| Argument structuré ≠ argument exprimé en surface (sous-entendu) | §149 doit modéliser explicitement les implicites — sinon recall faible |
| §150 échoue (signature V14 insuffisante pour la prose littéraire) | Pivot vers V14+ avec atomes additionnels (IRONIE, NÉGATION_RHÉTORIQUE) avant phase religieuse |

## Décisions à confirmer avec Stéphane

1. Faut-il intégrer dès la Phase A des **textes proto-athéistes
   chinois** (Wang Chong) ou les garder pour une vague ultérieure ?
2. **Niveau d'annotation manuelle** acceptable : 200 fragments
   gold, ou descendre à 80 fragments pour démarrer plus vite ?
3. **Stockage** : nouveau submodule `corpus/protoatheism/` séparé,
   ou intégré dans `data/corpus/` du repo principal ?
4. **Licences** : on s'en tient strictement au domaine public et aux
   éditions critiques en accès ouvert, ou on accepte des éditions
   Loeb (anciennes mais sous copyright) si elles sont indispensables ?

---

*Document de planification §140-bis, à figer avant attaque de §141.*

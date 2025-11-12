# ESSENCE DE PANINIFS — (copie migrée 2025-09-05, mise à jour 2025-11-12)

Copie de `Copilotage/knowledge/ESSENCE_PANINIFS.md` lors de la fusion.

But: plateforme modulaire pour compression sémantique universelle et publication, appuyée par des agents IA outillés, avec séparation stricte mémoire interne (Copilotage) vs docs publiques.

## 🎯 Ressources Cloud Disponibles

**Abonnements actifs**:
- **Google One**: Stockage premium pour datasets, backups, corpus linguistiques
- **Google Colab Pro**: GPU prioritaire (T4/P100/V100/A100), RAM étendue, sessions longues

**Usage stratégique**: Voir détails complets dans `RESSOURCES_CLOUD_DISPONIBLES.md`
- Entraînement modèles sur Colab Pro
- Stockage datasets volumineux sur Google One
- Pipeline automatisé: Local dev → Colab training → Cloud backup

Piliers
- Recherche: dhātu informationnels (7 universaux), datasets et validation.
- Ingénierie: architecture modulaire (sous-modules), CI/CD sobre, outillage DevOps.
- Publication: Medium (narratif), Leanpub (académique), Docs statiques.
- Gouvernance: règles de collaboration, sécurité, traçabilité (issues/branches/PR).

Éléments clés
- Copilotage = contexte interne IA, jamais requis par humains.
- Sous-modules pour missions: autonomous-missions, semantic-core, publication-engine, cloud-orchestrator, ultra-reactive, colab-controller.
- Processus: chaque travail ouvre une issue, crée une branche, PR qui ferme l’issue; journalisation de session host+pid.
- Qualité: tests (pytest), CI minimal, licences MIT partout.
 - Fiches détaillées:
	 - `SEMANTIC_UNIVERSALS_DHATU.md`
	 - `HYPERNODAL_DB_AND_LATTICE.md`
	 - `PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md`
	 - `MODULES_OVERVIEW_AND_PARENT_PROJECT.md`

Sources consultées
- GOVERNANCE/Copilotage/INDEX_MEMOIRE_INTERNE.md
- GOVERNANCE/Copilotage/core_memory/README_MEMOIRE_INTERNE.md
- Copilotage/COPILOTAGE_WORKFLOW.md
- Journaux de session récents et scripts.

Manques/à compléter
- Fichiers “final” Medium/Leanpub vides → aligner avec versions publiées.
- Architecture submodules (doc vide) → décrire responsabilités et APIs.
- Ajout lint (ruff/black) et checks PR.

Prochaines étapes
- Synchroniser contenus Medium/Leanpub dans les fichiers dédiés.
- Esquisser READMEs standardisés par sous-module.
- Mettre en place lint/format dans CI parent et modules.
 - Créer le repo parent "Panini" et fédérer la vision globale.

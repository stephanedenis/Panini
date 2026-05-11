# 📓 Journal Automatique - 2025-11-11

**Host**: hauru  
**Début session**: 2025-11-11T21:42:42-05:00  
**Système**: Journalisation automatique via Git hooks

---


## [21:42:42] Commit `53c536eb`

**Message**: 🛡️ Système journalisation infaillible - Installation complète

- Hook Git post-commit auto-journalisation
- Script snapshot horaire automatique
- Script backup discussions Copilot
- Scripts start/end session
- Documentation système complet
- Journal session reconstruction aujourd'hui

Plus jamais de perte de données!

**Hash complet**: `53c536eb6d566311d3c434319291a0940356c3dd`

### Fichiers modifiés

```
A	copilotage/SYSTEME_JOURNALISATION_INFAILLIBLE.md
M	copilotage/autonomie/__pycache__/terminal_autonomy_guardian.cpython-313.pyc
M	copilotage/autonomie/resilience/__pycache__/error_handler.cpython-313.pyc
M	copilotage/autonomie/tools/__pycache__/self_healing.cpython-313.pyc
A	copilotage/journal/JOURNAL_SESSION_2025-11-11_hauru_reconstruction.md
M	copilotage/journal/__pycache__/mission_logger.cpython-313.pyc
M	copilotage/journal/__pycache__/post_mission_analyzer.cpython-313.pyc
A	copilotage/snapshots/snapshot_2025-11-11_214241_hauru_test_installation.md
A	tools/backup_copilot_discussions.sh
A	tools/end_session.sh
A	tools/snapshot_auto.sh
A	tools/start_session.sh
```

### Statistiques

```
commit 53c536eb6d566311d3c434319291a0940356c3dd
Author: stephanedenis <stephane@sdenis.com>
Date:   Tue Nov 11 21:42:42 2025 -0500

    🛡️ Système journalisation infaillible - Installation complète
    
    - Hook Git post-commit auto-journalisation
    - Script snapshot horaire automatique
    - Script backup discussions Copilot
    - Scripts start/end session
    - Documentation système complet
    - Journal session reconstruction aujourd'hui
    
    Plus jamais de perte de données!

 copilotage/SYSTEME_JOURNALISATION_INFAILLIBLE.md   | 443 +++++++++++++++++
 .../terminal_autonomy_guardian.cpython-313.pyc     | Bin 19648 -> 19637 bytes
 .../__pycache__/error_handler.cpython-313.pyc      | Bin 31124 -> 31113 bytes
 .../tools/__pycache__/self_healing.cpython-313.pyc | Bin 46327 -> 56024 bytes
 ...RNAL_SESSION_2025-11-11_hauru_reconstruction.md | 541 +++++++++++++++++++++
 .../__pycache__/mission_logger.cpython-313.pyc     | Bin 23311 -> 23300 bytes
 .../post_mission_analyzer.cpython-313.pyc          | Bin 11594 -> 11583 bytes
 ...ot_2025-11-11_214241_hauru_test_installation.md | 142 ++++++
 tools/backup_copilot_discussions.sh                |  63 +++
 tools/end_session.sh                               | 118 +++++
 tools/snapshot_auto.sh                             | 174 +++++++
 tools/start_session.sh                             |  93 ++++
 12 files changed, 1574 insertions(+)
```

---


## [21:43:58] Commit `3bda001f`

**Message**: 📓 Rapport final installation système journalisation + rapports audit

- Rapport installation système infaillible (TESTÉ ✅)
- Rapport audit discipline (29 violations)
- Rapport inventaire code fonctionnel (31 fichiers)
- TODOs complétés: reconstruction journaux + système infaillible

Système OPÉRATIONNEL - Plus jamais de perte données!

**Hash complet**: `3bda001f5671be738b655fc595c841643c9363d9`

### Fichiers modifiés

```
A	QUICKSTART_PANINI_FS.md
A	RAPPORT_INVENTAIRE_RUST_WIKIPEDIA.md
M	README.md
A	add-dhatu-routes.sh
A	add-dhatu-state.sh
A	add-fuse-storage-bridge.sh
A	apply-fuse-cas-integration.sh
A	copilotage/journal/JOURNAL_AUTO_2025-11-11_hauru.md
A	docs/rapports/AUDIT_DISCIPLINE_2025-11-11.md
A	docs/rapports/INVENTAIRE_CODE_FONCTIONNEL_2025-11-11.md
A	docs/rapports/SYSTEME_JOURNALISATION_INSTALLATION_2025-11-11.md
A	fix-fuse-allow-other.sh
A	fix-fuse-mount.sh
A	fuse-cas-integration.rs
A	generate-dhatu-api.sh
A	generate-dhatu-core.sh
A	generate-dhatu-rest.sh
A	generate-dhatu-webui.sh
A	generate-v1-documentation.sh
```

### Statistiques

```
commit 3bda001f5671be738b655fc595c841643c9363d9
Author: stephanedenis <stephane@sdenis.com>
Date:   Tue Nov 11 21:43:58 2025 -0500

    📓 Rapport final installation système journalisation + rapports audit
    
    - Rapport installation système infaillible (TESTÉ ✅)
    - Rapport audit discipline (29 violations)
    - Rapport inventaire code fonctionnel (31 fichiers)
    - TODOs complétés: reconstruction journaux + système infaillible
    
    Système OPÉRATIONNEL - Plus jamais de perte données!

 QUICKSTART_PANINI_FS.md                            | 384 +++++++++++
 RAPPORT_INVENTAIRE_RUST_WIKIPEDIA.md               | 546 ++++++++++++++++
 README.md                                          |  36 +-
 add-dhatu-routes.sh                                |  29 +
 add-dhatu-state.sh                                 |  50 ++
 add-fuse-storage-bridge.sh                         | 200 ++++++
 apply-fuse-cas-integration.sh                      | 123 ++++
 .../journal/JOURNAL_AUTO_2025-11-11_hauru.md       |  76 +++
 docs/rapports/AUDIT_DISCIPLINE_2025-11-11.md       | 390 ++++++++++++
 .../INVENTAIRE_CODE_FONCTIONNEL_2025-11-11.md      | 427 +++++++++++++
 ...STEME_JOURNALISATION_INSTALLATION_2025-11-11.md | 278 ++++++++
 fix-fuse-allow-other.sh                            |  16 +
 fix-fuse-mount.sh                                  |  29 +
 fuse-cas-integration.rs                            |  76 +++
 generate-dhatu-api.sh                              | 363 +++++++++++
 generate-dhatu-core.sh                             | 469 ++++++++++++++
 generate-dhatu-rest.sh                             | 474 ++++++++++++++
 generate-dhatu-webui.sh                            | 271 ++++++++
 generate-v1-documentation.sh                       | 701 +++++++++++++++++++++
 19 files changed, 4936 insertions(+), 2 deletions(-)
```

---


## [22:11:04] Commit `7cb51661`

**Message**: 🧹 Grand nettoyage racine projet - 28→1 fichiers

- Déplacé 10 fichiers .md → docs/rapports/
- Déplacé 12 fichiers .sh → tools/
- Déplacé 1 fichier .rs → tech/rust/fuse/
- Déplacé 1 archive .tar.gz → legacy/backups/
- Supprimé 2 fichiers temp (build.log, test html)
- Ajouté snapshot horaire auto (22h00)
- Ajouté backup discussions auto

Racine conforme: README.md + .gitignore uniquement
Règle max 5 fichiers respectée ✅

**Hash complet**: `7cb516615359116094f9770fdcc299db09b789e6`

### Fichiers modifiés

```
D	ANALYSE_PANINI_FS_EXISTANT.md
D	AUDIT_PANINI_FS_AVANT_REINIT.md
D	DEMARRAGE_RAPIDE_PANINI_FS.md
D	INDEX_DOCUMENTATION_PANINI_FS.md
D	PANINI_FS_SYSTEME_COMPLET_INVENTAIRE.md
D	PLAN_GENERATION_SPEC_KIT.md
D	PLAN_NETTOYAGE_SPEC_KIT.md
D	QUICKSTART_PANINI_FS.md
D	RAPPORT_INVENTAIRE_RUST_WIKIPEDIA.md
D	RESUME_AUDIT_POST_PANNE.md
D	add-dhatu-routes.sh
D	add-dhatu-state.sh
D	add-fuse-storage-bridge.sh
D	apply-fuse-cas-integration.sh
A	copilotage/journal/discussions_backups/backup_2025-11-11_215145_hauru_metadata.json
A	copilotage/journal/discussions_backups/copilot_chat_2025-11-11_215145_hauru/commandEmbeddings.json
A	copilotage/journal/discussions_backups/copilot_chat_2025-11-11_215145_hauru/debugCommand/copilot-debug
A	copilotage/journal/discussions_backups/copilot_chat_2025-11-11_215145_hauru/debugCommand/copilotDebugCommand.js
A	copilotage/journal/discussions_backups/copilot_chat_2025-11-11_215145_hauru/settingEmbeddings.json
A	copilotage/snapshots/snapshot_2025-11-11_220000_hauru_auto.md
A	docs/index.md
A	docs/rapports/ANALYSE_PANINI_FS_EXISTANT.md
A	docs/rapports/AUDIT_PANINI_FS_AVANT_REINIT.md
A	docs/rapports/DEMARRAGE_RAPIDE_PANINI_FS.md
A	docs/rapports/INDEX_DOCUMENTATION_PANINI_FS.md
A	docs/rapports/PANINI_FS_SYSTEME_COMPLET_INVENTAIRE.md
A	docs/rapports/PLAN_GENERATION_SPEC_KIT.md
A	docs/rapports/PLAN_NETTOYAGE_SPEC_KIT.md
A	docs/rapports/QUICKSTART_PANINI_FS.md
A	docs/rapports/RAPPORT_INVENTAIRE_RUST_WIKIPEDIA.md
A	docs/rapports/RESUME_AUDIT_POST_PANNE.md
D	fix-fuse-allow-other.sh
D	fix-fuse-mount.sh
D	fuse-cas-integration.rs
D	generate-dhatu-api.sh
D	generate-dhatu-core.sh
D	generate-dhatu-rest.sh
D	generate-dhatu-webui.sh
D	generate-v1-documentation.sh
D	index.md
D	lancer-panini-fs-complet.sh
A	tech/rust/fuse/fuse-cas-integration.rs
A	tools/add-dhatu-routes.sh
A	tools/add-dhatu-state.sh
A	tools/add-fuse-storage-bridge.sh
A	tools/apply-fuse-cas-integration.sh
A	tools/fix-fuse-allow-other.sh
A	tools/fix-fuse-mount.sh
A	tools/generate-dhatu-api.sh
A	tools/generate-dhatu-core.sh
A	tools/generate-dhatu-rest.sh
A	tools/generate-dhatu-webui.sh
A	tools/generate-v1-documentation.sh
A	tools/lancer-panini-fs-complet.sh
```

### Statistiques

```
commit 7cb516615359116094f9770fdcc299db09b789e6
Author: stephanedenis <stephane@sdenis.com>
Date:   Tue Nov 11 22:11:04 2025 -0500

    🧹 Grand nettoyage racine projet - 28→1 fichiers
    
    - Déplacé 10 fichiers .md → docs/rapports/
    - Déplacé 12 fichiers .sh → tools/
    - Déplacé 1 fichier .rs → tech/rust/fuse/
    - Déplacé 1 archive .tar.gz → legacy/backups/
    - Supprimé 2 fichiers temp (build.log, test html)
    - Ajouté snapshot horaire auto (22h00)
    - Ajouté backup discussions auto
    
    Racine conforme: README.md + .gitignore uniquement
    Règle max 5 fichiers respectée ✅

 .../backup_2025-11-11_215145_hauru_metadata.json   |  17 +++
 .../commandEmbeddings.json                         |   1 +
 .../debugCommand/copilot-debug                     |   3 +
 .../debugCommand/copilotDebugCommand.js            |   6 +
 .../settingEmbeddings.json                         |   1 +
 .../snapshot_2025-11-11_220000_hauru_auto.md       | 142 +++++++++++++++++++++
 index.md => docs/index.md                          |   0
 .../rapports/ANALYSE_PANINI_FS_EXISTANT.md         |   0
 .../rapports/AUDIT_PANINI_FS_AVANT_REINIT.md       |   0
 .../rapports/DEMARRAGE_RAPIDE_PANINI_FS.md         |   0
 .../rapports/INDEX_DOCUMENTATION_PANINI_FS.md      |   0
 .../PANINI_FS_SYSTEME_COMPLET_INVENTAIRE.md        |   0
 .../rapports/PLAN_GENERATION_SPEC_KIT.md           |   0
 .../rapports/PLAN_NETTOYAGE_SPEC_KIT.md            |   0
 .../rapports/QUICKSTART_PANINI_FS.md               |   0
 .../rapports/RAPPORT_INVENTAIRE_RUST_WIKIPEDIA.md  |   0
 .../rapports/RESUME_AUDIT_POST_PANNE.md            |   0
 .../rust/fuse/fuse-cas-integration.rs              |   0
 add-dhatu-routes.sh => tools/add-dhatu-routes.sh   |   0
 add-dhatu-state.sh => tools/add-dhatu-state.sh     |   0
 .../add-fuse-storage-bridge.sh                     |   0
 .../apply-fuse-cas-integration.sh                  |   0
 .../fix-fuse-allow-other.sh                        |   0
 fix-fuse-mount.sh => tools/fix-fuse-mount.sh       |   0
 .../generate-dhatu-api.sh                          |   0
 .../generate-dhatu-core.sh                         |   0
 .../generate-dhatu-rest.sh                         |   0
 .../generate-dhatu-webui.sh                        |   0
 .../generate-v1-documentation.sh                   |   0
 .../lancer-panini-fs-complet.sh                    |   0
 30 files changed, 170 insertions(+)
```

---


## [22:30:57] Commit `a61efae9`

**Message**: 📦 Consolidation sauvegardes - Suppression duplicate

- Supprimé sauvegarde_172522 (duplicate exact de 172503)
- Archivé sauvegarde_172503 → legacy/backups/code_python/backup_2024-10-14_systeme_complet/
- Créé README.md documentant les 31 fichiers Python (815KB)
- Inventaire complet: 7 recherche, 4 Wikipedia, 4 validation, 3 optimisation, 13 PanLang
- Libéré 156M espace (duplicate supprimé)

Sauvegardes: 2 → 1 version de référence unique ✅

**Hash complet**: `a61efae923ddaa4a609c59f944c837cfaeefeb45`

### Fichiers modifiés

```
M	copilotage/journal/JOURNAL_AUTO_2025-11-11_hauru.md
A	legacy/backups/code_python/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.cargo/config.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.devcontainer/devcontainer.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.devcontainer/setup.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.gitconfig.local
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/bug-report.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/bug_report.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/config.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/feature-request.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/feature_request.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/research-task.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/research.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/submodule-change.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ISSUE_TEMPLATE/task.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/PULL_REQUEST_TEMPLATE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ops/triggers/deploy-docs.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/ops/triggers/pages-diagnostics.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/auto-merge-provenance.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/camping-status.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/codeql.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/copilotage-ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/copilotage-journal-check.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/copilotage-journal-index.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/cross-check-visibility.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/deploy-pages-mkdocs.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/dhatu-validation.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/docs-governance.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/docs-pages.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/e2e-playwright.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/label-agent.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/maintenance.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/minimal-status.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/owner-labeler.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/pages-diagnostics.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/pages-enforce-https.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/paniniFS-ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/provenance-bootstrap-pr37.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/provenance-guardian.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/publications.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/repo-guards.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/secret-scan.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/submodule-backfill.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/submodule-triage.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/update-modules-index.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/validate-agent-provenance.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/validate-agent-session.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.github/workflows/validate-task-coordination.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.gitmodules
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.nojekyll
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/.panini-agent.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/CNAME
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/CONTRIBUTING.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/COPILOTAGE_SHARED/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/COPILOTAGE_SHARED/settings.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Cargo.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/AGENT_CONVENTION.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/ARCHITECTURE_RESTRUCTURATION_PLAN.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/COPILOTAGE_WORKFLOW.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/DEPRECATED.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/DEPRECATED_README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/TODO_RELAIS_2025-09-02.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/adversarial_critic_agent.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/orchestrator_with_github.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/simple_autonomous_orchestrator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/tests/test_agents.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/agents/theoretical_research_agent.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/coordination-agent.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/debug_notebook_local.ipynb
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/demo-prototypage-rapide.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/elargissement-horizon-mathematiques-physique.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/headless_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/hyperscript-2.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-session.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-09-01-totoro-pid389223-session.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/2025-09-01-totoro-pid390178-rattrapage.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/knowledge/HYPERNODAL_DB_AND_LATTICE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/knowledge/MODULES_OVERVIEW_AND_PARENT_PROJECT.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/knowledge/PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/knowledge/SEMANTIC_UNIVERSALS_DHATU.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/mission_autonome_exemplaire.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/notes-vision-architecturale.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/roadmap-decouverte.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/roadmap-hybride-rd-production.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/COLAB_SETUP_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/advanced_consensus_engine.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/analogy_collector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/analyze_preferences.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/arxiv_collector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/autonomous_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/autonomous_gdrive_manager.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/books_collector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/colab_api_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/colab_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/colab_cli_launcher.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/colab_debug_environment.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/collect_samples.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/collect_with_attribution.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/complete_journey_summary.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/comprehensive_opensource_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/connivance_learning_system.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/consensus_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/continuous_autonomy_daemon.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/debug_ultra_fast.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/deep_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/deploy_colab_auto.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/deploy_colab_fixed.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/deploy_colab_secure.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/bootstrap_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/gh_pr_exempt.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/gh_pr_open.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/gh_queue.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/gh_task_init.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/git_audit.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/init_execution_orchestrator_repo.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/journal_index.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/journal_session.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/plan_migration_option_b.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/run_safe.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/devops/setup_dev_environment.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/display_recommendations.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/distribution_strategy_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/editorial/sync_publications.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/emergency_plasma_fix.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/executive_summary_generator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/executive_totoro_recommendations.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/externalization_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/final_security_check.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/fix_git_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/free_cloud_analysis.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/generate_remarkable_bibliography.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/generate_scientific_bibliography.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/github_workflow_monitor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/google_colab_setup.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/gpu_analysis_gt630m.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/hardware_integration_guide.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/hauru_setup.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/headless_autonomy_auditor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/headless_env_loader.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/headless_secrets_manager.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/immediate_launch_plan.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/implementation_roadmap_generator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/information_theory_collector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/intelligent_communication_guide.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_colab_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_colab_direct.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_optimized_colab.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_simple.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/launch_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/mathematics_physics_convergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/multi_source_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/neurocognitive_language_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/opensource_resources_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/optimal_language_synthesizer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/optimal_vocabulary_generator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/paniniFS_priority_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_analogical_extension.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_architectural_integrator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_fundamental_generator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_linguistic_integrator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/panini_status_point.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/pedagogical_applications_guide.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/physics_mathematics_collector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/plasma_stabilizer_advanced.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/publication_generator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/realistic_gpu_assessment.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/run_analysis.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/rust_bridge.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/safe_totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/secure_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/setup.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/setup_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/setup_gdrive_config.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/social_revolution_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/solid_foundation_strategy.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/temporal_emergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/test_regression.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/test_workflow_complete.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/tests/test_basic.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/tests/test_monitor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/total_autonomy_engine.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/totoro_liberation_toolkit.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/totoro_resource_management.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/traceability_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/ultra_reactive_controller.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/vscode_extensions_manager.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/scripts/vscode_settings_fixer.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/session-bilan-vision-realite.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/setup-rust.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/test-build.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Copilotage/tracabilite-attribution.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/Panini_Ecosystem_Coherence_Audit.ipynb
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/README.en.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/cloud-processing/FREE_COMPUTE_STRATEGY.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/discoveries/baby-sign-validation/BABY_SIGN_LANGUAGE_FOUNDATION.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/discoveries/dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/discoveries/dhatu-universals/DHATU_ATOMES_CONCEPTUELS_REVISION.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/docs/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/methodology/protocols/GUIDE_LEANPUB_ETAPE1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/methodology/protocols/GUIDE_MEDIUM_ETAPE3.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/methodology/protocols/ORDRE_PUBLICATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/methodology/protocols/PUBLICATION_COORDONNEE_20250820.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/methodology/protocols/SYNCHRONISATION_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/articles/english/ARTICLE_MEDIUM_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/articles/french/ARTICLE_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/books/LIVRE_LEANPUB_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/books/english/LIVRE_LEANPUB_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/RESEARCH/publications/books/french/LIVRE_LEANPUB_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/activate_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/analogy_detector_mvp.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/android_template.java
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/artifacts/playwright/pr-40-checks.png
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/artifacts/playwright/pr-40-overview.png
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/artifacts/playwright/pr-42-checks.png
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/artifacts/playwright/pr-42-overview.png
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/artifacts/snapshots/snapshot-20250902-152737.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/autonomous_colab_tester.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/autonomous_test_log.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/autonomous_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/check_colab_mission.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/check_deployment.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/check_dns.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/cleanup/manifest.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/cloud_backup/autonomous_crontab_simple.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/configure_vacation_mode.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/copilotage/config.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/copilotage/shared/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/copilotage/shared/config.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/data/ecosystem.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_cloud_autonomous.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_cloud_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_colab_deployment_center.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_docs.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_dynamic_monitoring.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_paninifs.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/deploy_paninifs_simple.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/dhatu_detector.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/.keep
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/avancement.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/dashboard.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/data/dhatu_child_langs.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/data/dhatu_child_phenomena_summary.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/data/system_status.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/diagrams.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/doc-process.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/catalogue.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/panorama.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/attribution-registry.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/autonomous-missions.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/copilotage-shared.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/datasets-ingestion.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/execution-orchestrator.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/ontowave-app.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/publication-engine.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/research.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/root.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/semantic-core.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/ecosystem/repos/ultra-reactive.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/avancement.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/diagrams.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/doc-process.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/infrastructure.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/licences.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/modules/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/monitoring.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/progress.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/publications.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/references.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/overview.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/references.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/style-guide.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/vision-social.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/en/vision.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/infrastructure.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/licences.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/livre/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/modules/_ext/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/modules/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/monitoring.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/publications.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/references.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/overview.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/references.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/whats-new-feed.html
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/whats-new.html
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/style-guide.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/docs/vision.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/doctor.pid
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/doctor_control.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/doctor_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/doctor_watchdog.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/domain_monitoring_report.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/e2e/package.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/e2e/playwright.config.js
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/e2e/tests/modules.spec.js
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/e2e/tests/research.spec.js
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/e2e/tests/smoke.spec.js
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/gold_encodings.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/gold_encodings_child.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/inventory_v0_1.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/arb.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/cmn.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/deu.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/en.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/eus.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/ewe.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/fr.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/hau.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/heb.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/hin.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/hun.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/iku.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/jpn.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/kor.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/nld.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/schema.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/spa.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/swa.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/tur.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/yor.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/prompts_child/zul.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/report.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/toy_corpus.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/typological_sample.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/experiments/dhatu/validator.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/firebase_notifications.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/fix_google_oauth.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/gdrive_credentials/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/gdrive_credentials/credentials.json.template
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/git_audit.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/github_workflow_emergency_doctor.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/AUTONOMIE_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/CONVENTIONS_NAMING.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/SESSION_BILAN_ORGANISATION.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/audits/AUDIT_SYNCHRONISATION_GITHUB.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/CENTRALISATION_DISCUSSIONS_COPILOTAGE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/POLICY.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/README_COPILOTAGE_HISTORIQUE.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/governance/copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/index.html
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/lancement_publications_20250820.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/last_domain_status.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/launch_autonomous_doctor.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/launch_continuous_improvement.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/launch_hybrid_dashboard.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/mini_test_dhatu.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/mkdocs.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/mkdocs_fixed.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/attribution-registry/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/attribution-registry/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/attribution-registry/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/attribution-registry/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/autonomous-missions/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/autonomous-missions/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/autonomous-missions/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/autonomous-missions/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/cloud-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/colab-controller/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/datasets-ingestion/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/datasets-ingestion/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/datasets-ingestion/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/datasets-ingestion/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/cli.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/__init__.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/local.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.eslintrc.cjs
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.github/ISSUE_TEMPLATE/feature_request.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.github/workflows/pr-preview.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.prettierignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/.prettierrc
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/content/index.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/copilotage/RULES.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/copilotage/preferences.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/copilotage/preferences.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/copilotage/scripts/prepare_pr.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/index.html
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/package-lock.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/package.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/public/config.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/scripts/check_principles.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/src/main.ts
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/src/markdown.ts
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/src/router.ts
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/src/shims.d.ts
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/tools/build-sitemap.mjs
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/tsconfig.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ontowave-app/vite.config.ts
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/publication-engine/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/publication-engine/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/publication-engine/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/publication-engine/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/semantic-core/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/semantic-core/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/semantic-core/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/semantic-core/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ultra-reactive/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ultra-reactive/.gitignore
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ultra-reactive/LICENSE
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/modules/ultra-reactive/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/monitor_domains.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/nocturnal_autonomous_mission.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/nocturnal_mission_log.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/notification_system.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/prepare_total_externalization.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/publish_docs.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/quick_monitor.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/README.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/reading_guides/workflow_revision_remarkable.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/bibliographie_complete.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/content_addressing_avance.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/etat_art_avance.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/etudes_cas_exercices.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/fondements_theoriques.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/remarkable_study_pack/scientific_articles/ipfs_vs_paninifs_analysis.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/restructure_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/aggregate_submodule_docs.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/analyze_submodule_issue.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/apply_cleanup_manifest.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/auto_pilot_research.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/check_copilotage_independence.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/detect_module_specific_content.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/audit_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/generate_modules_index.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/monitor_prs_playwright.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/pr_auto_doctor.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/repo_ci_snapshot.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/terminal_diagnostics.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/devops/vscode_settings_tuner.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/enforce_lowercase_paths.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/generate_ecosystem_docs.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/generate_modules_docs_index.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/generate_research_rss.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/noninteractive_env.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/open_submodule_issues.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/open_submodule_issues_gh.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/prepare_issue_packs.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/setup_labels_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/split_to_submodule.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/scripts/triage_submodules.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/setup_domains.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/setup_github_labels.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/setup_github_pages.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/setup_mvp_dataset.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/shutdown_totoro_procedure.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/sync_paninifs_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/templates_publication_reseaux.md
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/vacation_backup.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/vacation_emergency_monitor.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/vacation_productive_system.py
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/vacation_productive_work.json
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/validate_dhatu.sh
D	sauvegarde_projets_reels_20251014_172503/filesystem_backup/workflow_repair_report.json
D	sauvegarde_projets_reels_20251014_172503/gitmodules_avant.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.cargo/config.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.devcontainer/devcontainer.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.devcontainer/setup.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.gitconfig.local
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug-report.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug_report.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/config.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/feature-request.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/feature_request.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/research-task.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/research.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/submodule-change.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/task.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/PULL_REQUEST_TEMPLATE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ops/triggers/deploy-docs.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/ops/triggers/pages-diagnostics.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/auto-merge-provenance.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/camping-status.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/codeql.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/copilotage-ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/copilotage-journal-check.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/copilotage-journal-index.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/cross-check-visibility.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/deploy-pages-mkdocs.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/dhatu-validation.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/docs-governance.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/docs-pages.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/e2e-playwright.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/label-agent.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/maintenance.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/minimal-status.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/owner-labeler.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/pages-diagnostics.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/pages-enforce-https.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/paniniFS-ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/provenance-bootstrap-pr37.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/provenance-guardian.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/publications.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/repo-guards.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/secret-scan.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/submodule-backfill.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/submodule-triage.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/update-modules-index.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/validate-agent-provenance.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/validate-agent-session.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.github/workflows/validate-task-coordination.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.gitmodules
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.nojekyll
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/.panini-agent.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/CNAME
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/CONTRIBUTING.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/COPILOTAGE_SHARED/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/COPILOTAGE_SHARED/settings.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Cargo.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/AGENT_CONVENTION.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/ARCHITECTURE_RESTRUCTURATION_PLAN.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/COPILOTAGE_WORKFLOW.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/DEPRECATED.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/DEPRECATED_README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/TODO_RELAIS_2025-09-02.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/adversarial_critic_agent.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/orchestrator_with_github.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/simple_autonomous_orchestrator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/tests/test_agents.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/agents/theoretical_research_agent.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/coordination-agent.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/debug_notebook_local.ipynb
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/demo-prototypage-rapide.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/elargissement-horizon-mathematiques-physique.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/headless_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/hyperscript-2.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-session.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-09-01-totoro-pid389223-session.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/2025-09-01-totoro-pid390178-rattrapage.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/knowledge/HYPERNODAL_DB_AND_LATTICE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/knowledge/MODULES_OVERVIEW_AND_PARENT_PROJECT.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/knowledge/PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/knowledge/SEMANTIC_UNIVERSALS_DHATU.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/mission_autonome_exemplaire.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/notes-vision-architecturale.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/roadmap-decouverte.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/roadmap-hybride-rd-production.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/COLAB_SETUP_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/advanced_consensus_engine.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/analogy_collector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/analyze_preferences.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/arxiv_collector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/autonomous_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/autonomous_gdrive_manager.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/books_collector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/colab_api_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/colab_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/colab_cli_launcher.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/colab_debug_environment.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/collect_samples.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/collect_with_attribution.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/complete_journey_summary.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/comprehensive_opensource_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/connivance_learning_system.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/consensus_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/continuous_autonomy_daemon.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/debug_ultra_fast.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/deep_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_auto.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_fixed.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_secure.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/bootstrap_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_pr_exempt.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_pr_open.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_queue.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_task_init.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/git_audit.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/init_execution_orchestrator_repo.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/journal_index.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/journal_session.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/plan_migration_option_b.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/run_safe.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/devops/setup_dev_environment.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/display_recommendations.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/distribution_strategy_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/editorial/sync_publications.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/emergency_plasma_fix.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/executive_summary_generator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/executive_totoro_recommendations.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/externalization_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/final_security_check.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/fix_git_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/free_cloud_analysis.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/generate_remarkable_bibliography.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/generate_scientific_bibliography.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/github_workflow_monitor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/google_colab_setup.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/gpu_analysis_gt630m.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/hardware_integration_guide.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/hauru_setup.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/headless_autonomy_auditor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/headless_env_loader.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/headless_secrets_manager.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/immediate_launch_plan.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/implementation_roadmap_generator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/information_theory_collector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/intelligent_communication_guide.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_colab_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_colab_direct.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_optimized_colab.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_simple.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/launch_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/mathematics_physics_convergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/multi_source_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/neurocognitive_language_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/opensource_resources_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/optimal_language_synthesizer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/optimal_vocabulary_generator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/paniniFS_priority_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_analogical_extension.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_architectural_integrator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_fundamental_generator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_linguistic_integrator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/panini_status_point.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/pedagogical_applications_guide.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/physics_mathematics_collector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/plasma_stabilizer_advanced.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/publication_generator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/realistic_gpu_assessment.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/run_analysis.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/rust_bridge.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/safe_totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/secure_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/setup.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/setup_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/setup_gdrive_config.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/social_revolution_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/solid_foundation_strategy.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/temporal_emergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/test_regression.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/test_workflow_complete.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/tests/test_basic.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/tests/test_monitor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/total_autonomy_engine.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/totoro_liberation_toolkit.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/totoro_resource_management.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/traceability_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/ultra_reactive_controller.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/vscode_extensions_manager.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/scripts/vscode_settings_fixer.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/session-bilan-vision-realite.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/setup-rust.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/test-build.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Copilotage/tracabilite-attribution.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/Panini_Ecosystem_Coherence_Audit.ipynb
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/README.en.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/cloud-processing/FREE_COMPUTE_STRATEGY.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/discoveries/baby-sign-validation/BABY_SIGN_LANGUAGE_FOUNDATION.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/discoveries/dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/discoveries/dhatu-universals/DHATU_ATOMES_CONCEPTUELS_REVISION.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/docs/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/methodology/protocols/GUIDE_LEANPUB_ETAPE1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/methodology/protocols/GUIDE_MEDIUM_ETAPE3.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/methodology/protocols/ORDRE_PUBLICATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/methodology/protocols/PUBLICATION_COORDONNEE_20250820.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/methodology/protocols/SYNCHRONISATION_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/articles/english/ARTICLE_MEDIUM_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/articles/french/ARTICLE_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/books/LIVRE_LEANPUB_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/books/english/LIVRE_LEANPUB_2025_EN.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/RESEARCH/publications/books/french/LIVRE_LEANPUB_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/activate_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/analogy_detector_mvp.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/android_template.java
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/artifacts/playwright/pr-40-checks.png
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/artifacts/playwright/pr-40-overview.png
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/artifacts/playwright/pr-42-checks.png
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/artifacts/playwright/pr-42-overview.png
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/artifacts/snapshots/snapshot-20250902-152737.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/autonomous_colab_tester.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/autonomous_test_log.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/autonomous_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/check_colab_mission.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/check_deployment.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/check_dns.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/cleanup/manifest.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/cloud_backup/autonomous_crontab_simple.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/configure_vacation_mode.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/copilotage/config.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/copilotage/shared/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/copilotage/shared/config.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/data/ecosystem.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_cloud_autonomous.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_cloud_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_colab_deployment_center.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_docs.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_dynamic_monitoring.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_paninifs.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/deploy_paninifs_simple.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/dhatu_detector.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/.keep
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/avancement.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/dashboard.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/data/dhatu_child_langs.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/data/dhatu_child_phenomena_summary.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/data/system_status.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/diagrams.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/doc-process.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/catalogue.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/panorama.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/attribution-registry.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/autonomous-missions.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/copilotage-shared.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/datasets-ingestion.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/execution-orchestrator.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/ontowave-app.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/publication-engine.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/research.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/root.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/semantic-core.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/ecosystem/repos/ultra-reactive.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/avancement.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/diagrams.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/doc-process.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/infrastructure.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/licences.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/modules/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/monitoring.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/progress.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/publications.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/references.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/overview.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/references.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/style-guide.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/vision-social.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/en/vision.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/infrastructure.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/licences.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/livre/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/modules/_ext/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/modules/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/monitoring.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/publications.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/references.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/overview.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/references.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/whats-new-feed.html
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/whats-new.html
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/style-guide.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/docs/vision.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/doctor.pid
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/doctor_control.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/doctor_dashboard.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/doctor_watchdog.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/domain_monitoring_report.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/e2e/package.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/e2e/playwright.config.js
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/e2e/tests/modules.spec.js
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/e2e/tests/research.spec.js
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/e2e/tests/smoke.spec.js
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/gold_encodings.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/gold_encodings_child.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/inventory_v0_1.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/arb.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/cmn.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/deu.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/en.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/eus.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/ewe.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/fr.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hau.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/heb.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hin.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hun.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/iku.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/jpn.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/kor.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/nld.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/schema.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/spa.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/swa.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/tur.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/yor.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/prompts_child/zul.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/report.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/toy_corpus.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/typological_sample.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/experiments/dhatu/validator.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/firebase_notifications.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/fix_google_oauth.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/gdrive_credentials/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/gdrive_credentials/credentials.json.template
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/git_audit.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/github_workflow_emergency_doctor.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/AUTONOMIE_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/CONVENTIONS_NAMING.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/SESSION_BILAN_ORGANISATION.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/audits/AUDIT_SYNCHRONISATION_GITHUB.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/CENTRALISATION_DISCUSSIONS_COPILOTAGE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/POLICY.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/README_COPILOTAGE_HISTORIQUE.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/governance/copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/index.html
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/lancement_publications_20250820.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/last_domain_status.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/launch_autonomous_doctor.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/launch_continuous_improvement.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/launch_hybrid_dashboard.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/mini_test_dhatu.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/mkdocs.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/mkdocs_fixed.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/attribution-registry/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/attribution-registry/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/attribution-registry/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/attribution-registry/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/autonomous-missions/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/autonomous-missions/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/autonomous-missions/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/autonomous-missions/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/cloud-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/colab-controller/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/datasets-ingestion/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/datasets-ingestion/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/datasets-ingestion/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/datasets-ingestion/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/pyproject.toml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/cli.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/__init__.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/local.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.eslintrc.cjs
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.github/ISSUE_TEMPLATE/feature_request.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.github/workflows/pr-preview.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.prettierignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/.prettierrc
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/content/index.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/copilotage/RULES.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/copilotage/preferences.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/copilotage/preferences.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/copilotage/scripts/prepare_pr.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/index.html
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/package-lock.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/package.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/public/config.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/scripts/check_principles.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/src/main.ts
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/src/markdown.ts
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/src/router.ts
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/src/shims.d.ts
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/tools/build-sitemap.mjs
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/tsconfig.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ontowave-app/vite.config.ts
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/publication-engine/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/publication-engine/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/publication-engine/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/publication-engine/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/semantic-core/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/semantic-core/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/semantic-core/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/semantic-core/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ultra-reactive/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ultra-reactive/.gitignore
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ultra-reactive/LICENSE
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/modules/ultra-reactive/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/monitor_domains.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/nocturnal_autonomous_mission.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/nocturnal_mission_log.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/notification_system.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/prepare_total_externalization.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/publish_docs.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/quick_monitor.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/README.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/reading_guides/workflow_revision_remarkable.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/bibliographie_complete.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/content_addressing_avance.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/etat_art_avance.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/etudes_cas_exercices.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/fondements_theoriques.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/ipfs_vs_paninifs_analysis.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/requirements.txt
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/restructure_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/aggregate_submodule_docs.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/analyze_submodule_issue.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/apply_cleanup_manifest.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/auto_pilot_research.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/check_copilotage_independence.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/detect_module_specific_content.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/audit_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/generate_modules_index.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/monitor_prs_playwright.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/pr_auto_doctor.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/repo_ci_snapshot.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/terminal_diagnostics.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/devops/vscode_settings_tuner.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/enforce_lowercase_paths.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/generate_ecosystem_docs.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/generate_modules_docs_index.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/generate_research_rss.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/noninteractive_env.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/open_submodule_issues.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/open_submodule_issues_gh.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/prepare_issue_packs.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/setup_labels_submodules.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/split_to_submodule.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/scripts/triage_submodules.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/setup_domains.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/setup_github_labels.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/setup_github_pages.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/setup_mvp_dataset.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/shutdown_totoro_procedure.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/sync_paninifs_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/templates_publication_reseaux.md
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/vacation_backup.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/vacation_emergency_monitor.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/vacation_productive_system.py
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/vacation_productive_work.json
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/validate_dhatu.sh
D	sauvegarde_projets_reels_20251014_172503/modules_avant/core/filesystem/workflow_repair_report.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/DIRECTIVE_APPROBATIONS_COMMANDES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/DIRECTIVE_CONSOLIDATION_SERVEUR_UNIVERSEL.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/ISSUE_TEMPLATE/spec-kit-pilot-migration.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/README.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/copilot-approved-scripts.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/analyze.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/clarify.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/constitution.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/implement.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/plan.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/specify.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/prompts/tasks.prompt.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/reports/server_audit_20251003_220914.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/reports/system_status_20251003_215739.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/scripts/approval_monitor.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/scripts/system_initializer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/scripts/validate_command.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/scripts/weekly_optimization_cron.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/scripts/weekly_optimizer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/.github/workflows/pages.yml
D	sauvegarde_projets_reels_20251014_172503/research_backup/ANALYSE_ENRICHIE_COMPLETE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/AUDIT_COMPREHENSION_MISSION.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/BACKLOG_ARCHIVED_PROJECTS_2025-10-01T15-42-06Z.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/BACKLOG_REACTIVATION_PLAN_2025-10-01T16-45-19Z.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/BACKLOG_REACTIVATION_PLAN_2025-10-01T16-45-25Z.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CLARIFICATIONS_MISSION_CRITIQUE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/COMMENTAIRES_PRS_CLARIFICATIONS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/COMPRESSOR_ARCHITECTURE_v1.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/COMPRESSOR_ARCHITECTURE_v1_ADDENDUM.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CONTINUE_DEV_INTEGRATION.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CONTRAINTES_COMPATIBILITE_APPLICATIONS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/COPILOTAGE_DATES_ISO_APPLIQUE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/COPILOTAGE_DATES_ISO_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CORE_EXECUTION_PLAN.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CORRECTIONS_LAYOUT_UHD.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/CORRECTION_JS_CHARGEMENT.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/DASHBOARD_ENRICHI_MODELE_EBAUCHES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/DASHBOARD_TRANSFORME_ACTIVITE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/DEMONSTRATION_UHD_COMPLETE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/EBAUCHES_PANINI_EN_COURS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GITHUB_COPILOT_CODING_AGENT_SETUP.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GITHUB_PAGES_DASHBOARD_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GITHUB_PROJECT_FINAL_REPORT.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GITHUB_PROJECT_ISSUES_STRATEGIQUES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GITHUB_PROJECT_LANCE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GUIDE_LECTEUR_VIRTUEL_SITE_EXPLORATION.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/GUIDE_PRATIQUE_ZERO_APPROBATIONS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/HIERARCHICAL_ARCHITECTURE_ANALYSIS_2025-10-03T15-02-38Z.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/HIERARCHICAL_TESTS_RESULTS_2025-10-03T15-10-44Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE11_COMPLETED_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-02T22-15-33Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-02T22-17-33Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-03T12-25-07Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-03T13-46-19Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/ISSUE_OPTIMISATION_CONNIVENCES_NON_DECLAREES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/JOURNAL_SESSION_COMPRESSEUR_MVP_2025-10-01.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MIGRATION_COPILOTAGE_TO_SPEC_KIT.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MIGRATION_EXECUTIVE_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MISSION_ACCOMPLIE_UHD.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MISSION_ACCOMPLISHED.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MISSION_DASHBOARD_ACCOMPLIE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/MULTI_AGENT_COLLABORATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_ECOSYSTEM_ORCHESTRATOR_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_EXECUTIVE_SIZE_SUMMARY_2025-10-03T11-54-57.043799.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_FORMAT_ENCYCLOPEDIA_2025-10-03T10-42-28.536994.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_GIT_MULTI_REPOS_ACHIEVEMENT.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_INTERNAL_STRUCTURE_REPORT_2025-10-03T12-01-28.959164.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_OPTIMIZATION_ENCYCLOPEDIA_2025-10-03T10-58-57.908785.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_OPTIMIZATION_REPORT_2025-10-03T10-58-57.908785.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_SIZE_ANALYSIS_DATA_2025-10-03T11-53-12.188496.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_SIZE_ANALYSIS_REPORT_2025-10-03T11-53-12.188496.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PANINI_VFS_ACHIEVEMENT_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PHASE1_COLAB_INSTRUCTIONS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PHASE1_HUMAN_TASK_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PHASE1_MONITORING_GUIDE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/PILOT_REPORT_PANINI_ONTOWAVE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/POINTS_CLES_MISSION_OFFICIEL.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RAPPORT_ANALYSE_TRADUCTEURS_2025-10-01.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RAPPORT_MISSION_ANALYSEURS_SEMANTIQUES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RAPPORT_SESSION_2025-09-30.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RAPPORT_SESSION_AUTONOME.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/README_AUTONOMOUS_APPROVALS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/README_MISSION_PANINI.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/REPONSE_HIERARCHIE_EXCLUSIVE_CONFIRMEE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RESOLUTION_AFFICHAGE_CONTENU.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RESOLUTION_DEFINITIVE_CORPUS.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/RESUME_EXECUTIF_PANINI.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/SESSION_COMPLETE_SYNTHESE_EXECUTIVE.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/SESSION_SUMMARY_20251003.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/SOLUTION_APPROBATION_COMMANDES_AUTONOMES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/SPEC_KIT_INTEGRATION.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/STRATEGIC_REFACTORING_PLAN.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/STRATEGIE_AGENTS_UNIVERSAUX_SEMANTIQUES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/STRATEGIE_RAFFINEE_PLAN_TRAVAIL.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/SYNTHESE_CLARIFICATIONS_INTEGREES.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/VALIDATION_SYSTEM_HIERARCHIQUE_CORPUS_REEL.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/VUE_MODELE_PANINI_COMPLET.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/activity_dashboard_data.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/advanced_reconstruction_validation_1759520023.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/api_documentation_compressed.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/audit_server_consolidation.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/auto_update_dashboard.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/backlog_review_results_2025-10-01T16-45-19Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/backlog_review_results_2025-10-01T16-45-25Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/compression_benchmarks.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/compression_validation_results.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/copilotage_date_compliance_2025-09-29T20-22-03Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/copilotage_date_compliance_2025-09-29T20-22-13Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/copilotage_date_compliance_2025-09-29T20-28-19Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/copilotage_date_iso_standard.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/dashboard_activity_focused.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/dashboard_data.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/dashboard_real_data.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/dashboard_real_panini.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/dashboard_web_semantic.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/demo_analyse_enrichie.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/demo_decomposition_detaillee.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/deploy_phase1_dashboard.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/extracted_content.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/index.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/interface_decomposition_complete.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/iso8601_compliance_report_2025-10-01T13-39-40Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/issue13_semantic_atoms_discovery_2025-10-03T00-39-54Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/issue13_semantic_atoms_discovery_2025-10-03T12-24-46Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/issue13_semantic_atoms_discovery_2025-10-03T14-10-46Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/launch_advanced_demo.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/mission_alignment_report_2025-10-01T15-25-43Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/mission_alignment_report_2025-10-01T15-48-06Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/multilingual_embeddings.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/orchestrator_state_2025-10-01T14-25-27Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_advanced_uhd_clean.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_advanced_uhd_reconstructor.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_binary_decomposer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_clean_final.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_demo_data_generator.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_deployment_guide_20251003_135653.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_detailed_size_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_duplicate_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_ecosystem_orchestrator.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_ecosystem_state_2025-10-01T14-55-21Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_ecosystem_state_2025-10-01T15-48-50Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_format_discovery_engine.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_full_stack_digesteur.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_git_repo_architecture.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_hierarchical_architecture.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_internal_structure_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_issue11_final_validator.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_issue12_separation_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_issue13_semantic_atoms.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_issue14_dashboard_realtime.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_optimization_discovery_engine.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_performance_analyzer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_real_data.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_repos_status_viewer.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_serveur_corrige.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_simple_server.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_size_analysis_engine.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_test_corpus_generator.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_uhd_interface.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_universal_batch_20251003_135646.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_universal_format_engine.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-02T22-12-15Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-02T22-15-33Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-02T22-17-18Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-02T22-17-32Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-03T12-24-32Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-03T12-25-06Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-03T13-30-03Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-03T13-46-19Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validation_report_2025-10-03T14-10-46Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_validators_core.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_vfs_architecture_20251003_135649.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_virtual_fs_architecture.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_web_backend.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_web_explorer_prototype.html
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_web_frontend_specs_20251003_135653.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_web_interface_generator.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/panini_webdav_server.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/phase1_progress_report.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/phase1_session_log.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/playwright_diagnostic_1759520886.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr11_comment.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr13_comment.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr14_comment.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr16_comment.md
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr_compliance_report_2025-10-01T13-51-28Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/pr_compliance_report_2025-10-01T14-03-48Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/project_essence_extraction_2025-10-01T15-42-06Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/semantic_dashboard_summary_2025-10-02T21-20-38Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/semantic_orchestration_2025-10-02T21-11-00Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/semantic_orchestration_2025-10-02T21-11-47Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/semantic_orchestration_2025-10-02T21-16-38Z.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/serveur_decomposition_complete.py
D	sauvegarde_projets_reels_20251014_172503/research_backup/setup_panini_research_repo.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/start_phase1_monitoring.sh
D	sauvegarde_projets_reels_20251014_172503/research_backup/symmetry_detection_real_panini_data.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/symmetry_detection_results.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/training_metrics.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/translator_bias_style_analysis.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/translator_database_sample.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/translator_metadata_extraction.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/translators_metadata.json
D	sauvegarde_projets_reels_20251014_172503/research_backup/txt_extraction_2025-10-01T13-02-45Z.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.cargo/config.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.devcontainer/devcontainer.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.devcontainer/setup.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.gitconfig.local
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/bug-report.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/bug_report.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/config.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/feature-request.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/feature_request.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/research-task.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/research.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/submodule-change.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ISSUE_TEMPLATE/task.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/PULL_REQUEST_TEMPLATE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ops/triggers/deploy-docs.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/ops/triggers/pages-diagnostics.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/auto-merge-provenance.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/camping-status.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/codeql.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/copilotage-ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/copilotage-journal-check.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/copilotage-journal-index.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/cross-check-visibility.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/deploy-pages-mkdocs.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/dhatu-validation.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/docs-governance.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/docs-pages.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/e2e-playwright.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/label-agent.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/maintenance.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/minimal-status.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/owner-labeler.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/pages-diagnostics.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/pages-enforce-https.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/paniniFS-ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/provenance-bootstrap-pr37.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/provenance-guardian.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/publications.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/repo-guards.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/secret-scan.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/submodule-backfill.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/submodule-triage.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/update-modules-index.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/validate-agent-provenance.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/validate-agent-session.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.github/workflows/validate-task-coordination.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.gitmodules
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.nojekyll
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/.panini-agent.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/CNAME
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/CONTRIBUTING.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/COPILOTAGE_SHARED/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/COPILOTAGE_SHARED/settings.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Cargo.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/AGENT_CONVENTION.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/ARCHITECTURE_RESTRUCTURATION_PLAN.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/COPILOTAGE_WORKFLOW.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/DEPRECATED.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/DEPRECATED_README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/TODO_RELAIS_2025-09-02.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/adversarial_critic_agent.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/orchestrator_with_github.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/simple_autonomous_orchestrator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/tests/test_agents.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/agents/theoretical_research_agent.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/coordination-agent.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/debug_notebook_local.ipynb
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/demo-prototypage-rapide.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/elargissement-horizon-mathematiques-physique.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/headless_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/hyperscript-2.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-session.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-09-01-totoro-pid389223-session.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/2025-09-01-totoro-pid390178-rattrapage.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/knowledge/HYPERNODAL_DB_AND_LATTICE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/knowledge/MODULES_OVERVIEW_AND_PARENT_PROJECT.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/knowledge/PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/knowledge/SEMANTIC_UNIVERSALS_DHATU.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/mission_autonome_exemplaire.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/notes-vision-architecturale.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/roadmap-decouverte.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/roadmap-hybride-rd-production.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/COLAB_SETUP_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/advanced_consensus_engine.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/analogy_collector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/analyze_preferences.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/arxiv_collector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/autonomous_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/autonomous_gdrive_manager.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/books_collector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/colab_api_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/colab_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/colab_cli_launcher.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/colab_debug_environment.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/collect_samples.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/collect_with_attribution.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/complete_journey_summary.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/comprehensive_opensource_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/connivance_learning_system.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/consensus_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/continuous_autonomy_daemon.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/debug_ultra_fast.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/deep_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/deploy_colab_auto.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/deploy_colab_fixed.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/deploy_colab_secure.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/bootstrap_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/gh_pr_exempt.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/gh_pr_open.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/gh_queue.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/gh_task_init.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/git_audit.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/init_execution_orchestrator_repo.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/journal_index.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/journal_session.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/plan_migration_option_b.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/run_safe.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/devops/setup_dev_environment.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/display_recommendations.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/distribution_strategy_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/editorial/sync_publications.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/emergency_plasma_fix.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/executive_summary_generator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/executive_totoro_recommendations.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/externalization_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/final_security_check.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/fix_git_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/free_cloud_analysis.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/generate_remarkable_bibliography.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/generate_scientific_bibliography.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/github_workflow_monitor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/google_colab_setup.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/gpu_analysis_gt630m.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/hardware_integration_guide.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/hauru_setup.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/headless_autonomy_auditor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/headless_env_loader.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/headless_secrets_manager.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/immediate_launch_plan.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/implementation_roadmap_generator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/information_theory_collector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/intelligent_communication_guide.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_colab_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_colab_direct.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_optimized_colab.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_simple.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/launch_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/mathematics_physics_convergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/multi_source_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/neurocognitive_language_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/opensource_resources_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/optimal_language_synthesizer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/optimal_vocabulary_generator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/paniniFS_priority_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_analogical_extension.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_architectural_integrator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_fundamental_generator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_linguistic_integrator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/panini_status_point.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/pedagogical_applications_guide.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/physics_mathematics_collector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/plasma_stabilizer_advanced.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/publication_generator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/realistic_gpu_assessment.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/run_analysis.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/rust_bridge.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/safe_totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/secure_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/setup.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/setup_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/setup_gdrive_config.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/social_revolution_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/solid_foundation_strategy.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/temporal_emergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/test_regression.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/test_workflow_complete.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/tests/test_basic.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/tests/test_monitor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/total_autonomy_engine.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/totoro_liberation_toolkit.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/totoro_resource_management.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/traceability_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/ultra_reactive_controller.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/vscode_extensions_manager.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/scripts/vscode_settings_fixer.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/session-bilan-vision-realite.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/setup-rust.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/test-build.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Copilotage/tracabilite-attribution.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/Panini_Ecosystem_Coherence_Audit.ipynb
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/README.en.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/cloud-processing/FREE_COMPUTE_STRATEGY.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/discoveries/baby-sign-validation/BABY_SIGN_LANGUAGE_FOUNDATION.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/discoveries/dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/discoveries/dhatu-universals/DHATU_ATOMES_CONCEPTUELS_REVISION.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/docs/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/methodology/protocols/GUIDE_LEANPUB_ETAPE1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/methodology/protocols/GUIDE_MEDIUM_ETAPE3.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/methodology/protocols/ORDRE_PUBLICATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/methodology/protocols/PUBLICATION_COORDONNEE_20250820.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/methodology/protocols/SYNCHRONISATION_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/articles/english/ARTICLE_MEDIUM_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/articles/french/ARTICLE_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/books/LIVRE_LEANPUB_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/books/english/LIVRE_LEANPUB_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/RESEARCH/publications/books/french/LIVRE_LEANPUB_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/activate_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/analogy_detector_mvp.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/android_template.java
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/artifacts/playwright/pr-40-checks.png
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/artifacts/playwright/pr-40-overview.png
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/artifacts/playwright/pr-42-checks.png
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/artifacts/playwright/pr-42-overview.png
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/artifacts/snapshots/snapshot-20250902-152737.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/autonomous_colab_tester.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/autonomous_test_log.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/autonomous_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/check_colab_mission.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/check_deployment.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/check_dns.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/cleanup/manifest.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/cloud_backup/autonomous_crontab_simple.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/configure_vacation_mode.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/copilotage/config.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/copilotage/shared/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/copilotage/shared/config.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/data/ecosystem.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_cloud_autonomous.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_cloud_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_colab_deployment_center.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_docs.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_dynamic_monitoring.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_paninifs.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/deploy_paninifs_simple.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/dhatu_detector.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/.keep
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/avancement.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/dashboard.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/data/dhatu_child_langs.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/data/dhatu_child_phenomena_summary.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/data/system_status.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/diagrams.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/doc-process.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/catalogue.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/panorama.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/attribution-registry.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/autonomous-missions.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/copilotage-shared.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/datasets-ingestion.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/execution-orchestrator.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/ontowave-app.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/publication-engine.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/research.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/root.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/semantic-core.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/ecosystem/repos/ultra-reactive.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/avancement.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/diagrams.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/doc-process.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/infrastructure.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/licences.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/modules/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/monitoring.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/progress.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/publications.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/references.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/overview.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/references.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/style-guide.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/vision-social.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/en/vision.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/infrastructure.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/licences.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/livre/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/modules/_ext/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/modules/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/monitoring.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/publications.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/references.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/overview.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/references.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/whats-new-feed.html
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/whats-new.html
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/style-guide.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/docs/vision.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/doctor.pid
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/doctor_control.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/doctor_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/doctor_watchdog.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/domain_monitoring_report.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/e2e/package.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/e2e/playwright.config.js
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/e2e/tests/modules.spec.js
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/e2e/tests/research.spec.js
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/e2e/tests/smoke.spec.js
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/gold_encodings.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/gold_encodings_child.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/inventory_v0_1.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/arb.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/cmn.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/deu.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/en.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/eus.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/ewe.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/fr.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/hau.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/heb.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/hin.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/hun.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/iku.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/jpn.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/kor.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/nld.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/schema.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/spa.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/swa.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/tur.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/yor.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/prompts_child/zul.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/report.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/toy_corpus.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/typological_sample.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/experiments/dhatu/validator.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/firebase_notifications.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/fix_google_oauth.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/gdrive_credentials/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/gdrive_credentials/credentials.json.template
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/git_audit.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/github_workflow_emergency_doctor.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/AUTONOMIE_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/CONVENTIONS_NAMING.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/SESSION_BILAN_ORGANISATION.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/audits/AUDIT_SYNCHRONISATION_GITHUB.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/CENTRALISATION_DISCUSSIONS_COPILOTAGE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/POLICY.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/README_COPILOTAGE_HISTORIQUE.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/governance/copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/index.html
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/lancement_publications_20250820.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/last_domain_status.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/launch_autonomous_doctor.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/launch_continuous_improvement.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/launch_hybrid_dashboard.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/mini_test_dhatu.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/mkdocs.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/mkdocs_fixed.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/attribution-registry/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/attribution-registry/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/attribution-registry/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/attribution-registry/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/autonomous-missions/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/autonomous-missions/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/autonomous-missions/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/autonomous-missions/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/cloud-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/colab-controller/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/datasets-ingestion/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/datasets-ingestion/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/datasets-ingestion/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/datasets-ingestion/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/cli.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/__init__.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/execution-orchestrator/src/execution_orchestrator/drivers/local.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.eslintrc.cjs
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.github/ISSUE_TEMPLATE/feature_request.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.github/workflows/pr-preview.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.prettierignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/.prettierrc
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/content/index.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/copilotage/RULES.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/copilotage/preferences.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/copilotage/preferences.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/copilotage/scripts/prepare_pr.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/index.html
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/package-lock.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/package.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/public/config.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/scripts/check_principles.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/src/main.ts
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/src/markdown.ts
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/src/router.ts
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/src/shims.d.ts
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/tools/build-sitemap.mjs
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/tsconfig.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ontowave-app/vite.config.ts
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/publication-engine/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/publication-engine/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/publication-engine/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/publication-engine/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/semantic-core/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/semantic-core/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/semantic-core/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/semantic-core/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ultra-reactive/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ultra-reactive/.gitignore
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ultra-reactive/LICENSE
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/modules/ultra-reactive/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/monitor_domains.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/nocturnal_autonomous_mission.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/nocturnal_mission_log.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/notification_system.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/prepare_total_externalization.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/publish_docs.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/quick_monitor.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/README.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/reading_guides/workflow_revision_remarkable.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/bibliographie_complete.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/content_addressing_avance.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/etat_art_avance.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/etudes_cas_exercices.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/fondements_theoriques.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/remarkable_study_pack/scientific_articles/ipfs_vs_paninifs_analysis.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/restructure_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/aggregate_submodule_docs.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/analyze_submodule_issue.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/apply_cleanup_manifest.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/auto_pilot_research.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/check_copilotage_independence.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/detect_module_specific_content.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/audit_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/generate_modules_index.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/monitor_prs_playwright.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/pr_auto_doctor.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/repo_ci_snapshot.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/terminal_diagnostics.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/devops/vscode_settings_tuner.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/enforce_lowercase_paths.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/generate_ecosystem_docs.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/generate_modules_docs_index.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/generate_research_rss.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/noninteractive_env.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/open_submodule_issues.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/open_submodule_issues_gh.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/prepare_issue_packs.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/setup_labels_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/split_to_submodule.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/scripts/triage_submodules.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/setup_domains.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/setup_github_labels.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/setup_github_pages.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/setup_mvp_dataset.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/shutdown_totoro_procedure.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/sync_paninifs_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/templates_publication_reseaux.md
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/vacation_backup.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/vacation_emergency_monitor.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/vacation_productive_system.py
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/vacation_productive_work.json
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/validate_dhatu.sh
D	sauvegarde_projets_reels_20251014_172522/filesystem_backup/workflow_repair_report.json
D	sauvegarde_projets_reels_20251014_172522/gitmodules_avant.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.cargo/config.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.devcontainer/devcontainer.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.devcontainer/setup.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.gitconfig.local
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug-report.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/bug_report.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/config.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/feature-request.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/feature_request.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/research-task.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/research.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/submodule-change.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ISSUE_TEMPLATE/task.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/PULL_REQUEST_TEMPLATE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ops/triggers/deploy-docs.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/ops/triggers/pages-diagnostics.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/auto-merge-provenance.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/camping-status.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/codeql.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/copilotage-ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/copilotage-journal-check.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/copilotage-journal-index.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/cross-check-visibility.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/deploy-pages-mkdocs.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/dhatu-validation.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/docs-governance.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/docs-pages.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/e2e-playwright.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/label-agent.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/maintenance.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/minimal-status.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/owner-labeler.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/pages-diagnostics.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/pages-enforce-https.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/paniniFS-ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/provenance-bootstrap-pr37.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/provenance-guardian.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/publications.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/repo-guards.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/secret-scan.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/submodule-backfill.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/submodule-triage.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/update-modules-index.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/validate-agent-provenance.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/validate-agent-session.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.github/workflows/validate-task-coordination.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.gitmodules
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.nojekyll
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/.panini-agent.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/CNAME
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/CONTRIBUTING.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/COPILOTAGE_SHARED/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/COPILOTAGE_SHARED/settings.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Cargo.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/AGENT_CONVENTION.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/ARCHITECTURE_RESTRUCTURATION_PLAN.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/COPILOTAGE_WORKFLOW.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/DEPRECATED.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/DEPRECATED_README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/TODO_RELAIS_2025-09-02.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/adversarial_critic_agent.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/orchestrator_with_github.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/simple_autonomous_orchestrator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/tests/test_agents.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/agents/theoretical_research_agent.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/coordination-agent.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/debug_notebook_local.ipynb
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/demo-prototypage-rapide.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/elargissement-horizon-mathematiques-physique.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/headless_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/hyperscript-2.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-session.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-09-01-totoro-pid389223-session.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/2025-09-01-totoro-pid390178-rattrapage.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/knowledge/HYPERNODAL_DB_AND_LATTICE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/knowledge/MODULES_OVERVIEW_AND_PARENT_PROJECT.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/knowledge/PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/knowledge/SEMANTIC_UNIVERSALS_DHATU.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/mission_autonome_exemplaire.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/notes-vision-architecturale.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/roadmap-decouverte.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/roadmap-hybride-rd-production.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/COLAB_SETUP_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/advanced_consensus_engine.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/analogy_collector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/analyze_preferences.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/arxiv_collector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/autonomous_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/autonomous_gdrive_manager.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/books_collector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/colab_api_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/colab_autonomous_controller.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/colab_cli_launcher.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/colab_debug_environment.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/collect_samples.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/collect_with_attribution.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/complete_journey_summary.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/comprehensive_opensource_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/connivance_learning_system.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/consensus_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/continuous_autonomy_daemon.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/debug_ultra_fast.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/deep_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_auto.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_fixed.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/deploy_colab_secure.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/bootstrap_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_pr_exempt.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_pr_open.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_queue.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/gh_task_init.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/git_audit.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/init_execution_orchestrator_repo.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/journal_index.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/journal_session.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/plan_migration_option_b.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/run_safe.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/devops/setup_dev_environment.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/display_recommendations.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/distribution_strategy_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/editorial/sync_publications.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/emergency_plasma_fix.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/executive_summary_generator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/executive_totoro_recommendations.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/externalization_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/final_security_check.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/fix_git_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/free_cloud_analysis.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/generate_remarkable_bibliography.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/generate_scientific_bibliography.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/github_workflow_monitor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/google_colab_setup.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/gpu_analysis_gt630m.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/hardware_integration_guide.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/hauru_setup.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/headless_autonomy_auditor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/headless_env_loader.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/headless_secrets_manager.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/immediate_launch_plan.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/implementation_roadmap_generator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/information_theory_collector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/intelligent_communication_guide.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_colab_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_colab_direct.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_optimized_colab.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_simple.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/launch_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/mathematics_physics_convergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/multi_source_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/neurocognitive_language_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/opensource_resources_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/optimal_language_synthesizer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/optimal_vocabulary_generator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/paniniFS_priority_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_analogical_extension.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_architectural_integrator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_fundamental_generator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_linguistic_integrator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/panini_status_point.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/pedagogical_applications_guide.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/physics_mathematics_collector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/plasma_stabilizer_advanced.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/publication_generator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/realistic_gpu_assessment.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/run_analysis.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/rust_bridge.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/safe_totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/secure_cleanup_credentials.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/setup.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/setup_cloud_autonomous.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/setup_gdrive_config.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/social_revolution_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/solid_foundation_strategy.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/temporal_emergence_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/test_regression.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/test_workflow_complete.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/tests/test_basic.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/tests/test_monitor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/total_autonomy_engine.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/totoro_liberation_toolkit.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/totoro_optimizer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/totoro_resource_management.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/traceability_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/ultra_reactive_controller.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/vscode_extensions_manager.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/scripts/vscode_settings_fixer.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/session-bilan-vision-realite.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/setup-rust.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/test-build.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Copilotage/tracabilite-attribution.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/Panini_Ecosystem_Coherence_Audit.ipynb
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/README.en.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/cloud-processing/FREE_COMPUTE_STRATEGY.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/discoveries/baby-sign-validation/BABY_SIGN_LANGUAGE_FOUNDATION.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/discoveries/dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/discoveries/dhatu-universals/DHATU_ATOMES_CONCEPTUELS_REVISION.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/docs/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/methodology/protocols/GUIDE_LEANPUB_ETAPE1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/methodology/protocols/GUIDE_MEDIUM_ETAPE3.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/methodology/protocols/ORDRE_PUBLICATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/methodology/protocols/PUBLICATION_COORDONNEE_20250820.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/methodology/protocols/SYNCHRONISATION_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/articles/ARTICLE_MEDIUM_FINAL_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/articles/english/ARTICLE_MEDIUM_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/articles/french/ARTICLE_MEDIUM_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/books/LIVRE_LEANPUB_FINAL_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/books/english/LIVRE_LEANPUB_2025_EN.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/RESEARCH/publications/books/french/LIVRE_LEANPUB_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/activate_total_autonomy.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/analogy_detector_mvp.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/android_template.java
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/artifacts/playwright/pr-40-checks.png
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/artifacts/playwright/pr-40-overview.png
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/artifacts/playwright/pr-42-checks.png
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/artifacts/playwright/pr-42-overview.png
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/artifacts/snapshots/snapshot-20250902-152737.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/autonomous_colab_tester.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/autonomous_test_log.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/autonomous_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/check_colab_mission.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/check_deployment.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/check_dns.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/cleanup/manifest.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/cloud_backup/autonomous_crontab_simple.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/configure_vacation_mode.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/copilotage/config.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/copilotage/shared/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/copilotage/shared/config.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/data/ecosystem.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_cloud_autonomous.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_cloud_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_colab_deployment_center.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_docs.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_dynamic_monitoring.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_paninifs.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/deploy_paninifs_simple.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/dhatu_detector.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/.keep
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/avancement.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/dashboard.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/data/dhatu_child_langs.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/data/dhatu_child_phenomena_summary.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/data/system_status.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/diagrams.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/doc-process.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/catalogue.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/panorama.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/attribution-registry.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/autonomous-missions.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/copilotage-shared.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/datasets-ingestion.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/execution-orchestrator.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/ontowave-app.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/publication-engine.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/research.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/root.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/semantic-core.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/ecosystem/repos/ultra-reactive.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/OPERATIONS/DevOps/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/avancement.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/dhatu-framework.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/diagrams.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/doc-process.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/ecosystem/ontowave.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/infrastructure.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/licences.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/modules/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/monitoring.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/progress.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/publications.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/references.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/overview.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/references.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/style-guide.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/vision-social.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/en/vision.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/infrastructure.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/licences.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/linguistic-foundations.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/livre/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/livre/lecture-integrale.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/modules/_ext/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/modules/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/monitoring-guide.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/monitoring.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/operations/devops/roadmap.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/publications.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/references.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/cloud-free-compute.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/compression-semantique.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/dhatu-inventory-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/experiences-dhatu-typologie-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/human-language-development.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/hypotheses-and-alternatives.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/inventaire-dhatu-v0-1.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/langage-humain-developpement.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/overview.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/references.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/semantic-compression.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/semantic-universals.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/universaux-semantique.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/whats-new-feed.html
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/whats-new.html
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/research/whats-new.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/style-guide.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/vision-sociale.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/docs/vision.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/doctor.pid
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/doctor_control.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/doctor_dashboard.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/doctor_watchdog.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/domain_monitoring_report.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/e2e/package.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/e2e/playwright.config.js
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/e2e/tests/modules.spec.js
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/e2e/tests/research.spec.js
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/e2e/tests/smoke.spec.js
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/gold_encodings.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/gold_encodings_child.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/inventory_v0_1.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/arb.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/cmn.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/deu.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/en.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/eus.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/ewe.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/fr.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hau.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/heb.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hin.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/hun.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/iku.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/jpn.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/kor.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/nld.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/schema.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/spa.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/swa.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/tur.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/yor.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/prompts_child/zul.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/report.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/toy_corpus.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/typological_sample.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/experiments/dhatu/validator.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/firebase_notifications.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/fix_google_oauth.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/fix_remotes.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/gdrive_credentials/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/gdrive_credentials/credentials.json.template
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/git_audit.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/github_workflow_doctor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/github_workflow_emergency_doctor.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/AUTONOMIE_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/CONVENTIONS_NAMING.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/SESSION_BILAN_ORGANISATION.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/audits/AUDIT_SYNCHRONISATION_GITHUB.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/CENTRALISATION_DISCUSSIONS_COPILOTAGE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/POLICY.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/README_COPILOTAGE_HISTORIQUE.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/journal/INDEX.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/governance/copilotage/knowledge/ESSENCE_PANINIFS.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/index.html
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/lancement_publications_20250820.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/last_domain_status.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/launch_autonomous_doctor.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/launch_continuous_improvement.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/launch_hybrid_dashboard.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/mini_test_dhatu.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/mkdocs.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/mkdocs_fixed.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/attribution-registry/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/attribution-registry/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/attribution-registry/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/attribution-registry/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/autonomous-missions/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/autonomous-missions/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/autonomous-missions/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/autonomous-missions/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/cloud-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/colab-controller/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/datasets-ingestion/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/datasets-ingestion/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/datasets-ingestion/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/datasets-ingestion/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/pyproject.toml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/cli.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/__init__.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/cloud/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/colab/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/execution-orchestrator/src/execution_orchestrator/drivers/local.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.eslintrc.cjs
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.github/ISSUE_TEMPLATE/bug_report.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.github/ISSUE_TEMPLATE/feature_request.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.github/pull_request_template.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.github/workflows/pr-preview.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.prettierignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/.prettierrc
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/content/index.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/copilotage/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/copilotage/RULES.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/copilotage/preferences.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/copilotage/preferences.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/copilotage/scripts/prepare_pr.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/index.html
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/package-lock.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/package.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/public/config.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/scripts/check_principles.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/src/main.ts
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/src/markdown.ts
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/src/router.ts
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/src/shims.d.ts
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/tools/build-sitemap.mjs
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/tsconfig.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ontowave-app/vite.config.ts
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/publication-engine/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/publication-engine/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/publication-engine/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/publication-engine/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/semantic-core/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/semantic-core/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/semantic-core/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/semantic-core/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ultra-reactive/.github/workflows/ci.yml
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ultra-reactive/.gitignore
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ultra-reactive/LICENSE
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/modules/ultra-reactive/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/monitor_domains.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/nocturnal_autonomous_mission.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/nocturnal_mission_log.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/notification_system.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/prepare_total_externalization.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/publish_docs.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/quick_monitor.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/README.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/reading_guides/workflow_revision_remarkable.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/bibliographie_complete.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/content_addressing_avance.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/etat_art_avance.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/etudes_cas_exercices.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/fondements_theoriques.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/remarkable_study_pack/scientific_articles/ipfs_vs_paninifs_analysis.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/requirements.txt
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/restructure_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/aggregate_submodule_docs.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/analyze_submodule_issue.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/apply_cleanup_manifest.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/auto_pilot_research.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/check_copilotage_independence.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/detect_module_specific_content.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/audit_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/generate_modules_index.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/monitor_prs_playwright.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/pr_auto_doctor.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/repo_ci_snapshot.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/terminal_diagnostics.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/devops/vscode_settings_tuner.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/enforce_lowercase_paths.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/generate_ecosystem_docs.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/generate_modules_docs_index.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/generate_research_rss.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/noninteractive_env.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/open_submodule_issues.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/open_submodule_issues_gh.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/prepare_issue_packs.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/setup_labels_submodules.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/split_to_submodule.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/scripts/triage_submodules.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/setup_domains.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/setup_github_labels.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/setup_github_pages.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/setup_mvp_dataset.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/shutdown_totoro_procedure.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/sync_paninifs_ecosystem.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/templates_publication_reseaux.md
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/vacation_backup.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/vacation_emergency_monitor.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/vacation_productive_system.py
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/vacation_productive_work.json
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/validate_dhatu.sh
D	sauvegarde_projets_reels_20251014_172522/modules_avant/core/filesystem/workflow_repair_report.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/DIRECTIVE_APPROBATIONS_COMMANDES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/DIRECTIVE_CONSOLIDATION_SERVEUR_UNIVERSEL.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/ISSUE_TEMPLATE/spec-kit-pilot-migration.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/README.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/copilot-approved-scripts.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/analyze.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/clarify.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/constitution.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/implement.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/plan.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/specify.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/prompts/tasks.prompt.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/reports/server_audit_20251003_220914.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/reports/system_status_20251003_215739.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/scripts/approval_monitor.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/scripts/system_initializer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/scripts/validate_command.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/scripts/weekly_optimization_cron.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/scripts/weekly_optimizer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/.github/workflows/pages.yml
D	sauvegarde_projets_reels_20251014_172522/research_backup/ANALYSE_ENRICHIE_COMPLETE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/AUDIT_COMPREHENSION_MISSION.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/BACKLOG_ARCHIVED_PROJECTS_2025-10-01T15-42-06Z.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/BACKLOG_REACTIVATION_PLAN_2025-10-01T16-45-19Z.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/BACKLOG_REACTIVATION_PLAN_2025-10-01T16-45-25Z.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CLARIFICATIONS_MISSION_CRITIQUE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/COMMENTAIRES_PRS_CLARIFICATIONS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/COMPRESSOR_ARCHITECTURE_v1.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/COMPRESSOR_ARCHITECTURE_v1_ADDENDUM.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CONTINUE_DEV_INTEGRATION.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CONTRAINTES_COMPATIBILITE_APPLICATIONS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/COPILOTAGE_DATES_ISO_APPLIQUE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/COPILOTAGE_DATES_ISO_VALIDATION_FINALE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CORE_EXECUTION_PLAN.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CORRECTIONS_LAYOUT_UHD.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/CORRECTION_JS_CHARGEMENT.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/DASHBOARD_ENRICHI_MODELE_EBAUCHES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/DASHBOARD_TRANSFORME_ACTIVITE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/DEMONSTRATION_UHD_COMPLETE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/EBAUCHES_PANINI_EN_COURS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GITHUB_COPILOT_CODING_AGENT_SETUP.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GITHUB_PAGES_DASHBOARD_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GITHUB_PROJECT_FINAL_REPORT.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GITHUB_PROJECT_ISSUES_STRATEGIQUES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GITHUB_PROJECT_LANCE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GUIDE_LECTEUR_VIRTUEL_SITE_EXPLORATION.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/GUIDE_PRATIQUE_ZERO_APPROBATIONS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/HIERARCHICAL_ARCHITECTURE_ANALYSIS_2025-10-03T15-02-38Z.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/HIERARCHICAL_TESTS_RESULTS_2025-10-03T15-10-44Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE11_COMPLETED_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-02T22-15-33Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-02T22-17-33Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-03T12-25-07Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE11_FINAL_VALIDATION_REPORT_2025-10-03T13-46-19Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/ISSUE_OPTIMISATION_CONNIVENCES_NON_DECLAREES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/JOURNAL_SESSION_COMPRESSEUR_MVP_2025-10-01.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MIGRATION_COPILOTAGE_TO_SPEC_KIT.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MIGRATION_EXECUTIVE_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MISSION_ACCOMPLIE_UHD.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MISSION_ACCOMPLISHED.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MISSION_DASHBOARD_ACCOMPLIE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/MULTI_AGENT_COLLABORATION_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_ECOSYSTEM_ORCHESTRATOR_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_EXECUTIVE_SIZE_SUMMARY_2025-10-03T11-54-57.043799.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_FORMAT_ENCYCLOPEDIA_2025-10-03T10-42-28.536994.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_GIT_MULTI_REPOS_ACHIEVEMENT.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_INTERNAL_STRUCTURE_REPORT_2025-10-03T12-01-28.959164.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_OPTIMIZATION_ENCYCLOPEDIA_2025-10-03T10-58-57.908785.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_OPTIMIZATION_REPORT_2025-10-03T10-58-57.908785.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_SIZE_ANALYSIS_DATA_2025-10-03T11-53-12.188496.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_SIZE_ANALYSIS_REPORT_2025-10-03T11-53-12.188496.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PANINI_VFS_ACHIEVEMENT_SUMMARY.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PHASE1_COLAB_INSTRUCTIONS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PHASE1_HUMAN_TASK_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PHASE1_MONITORING_GUIDE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/PILOT_REPORT_PANINI_ONTOWAVE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/POINTS_CLES_MISSION_OFFICIEL.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RAPPORT_ANALYSE_TRADUCTEURS_2025-10-01.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RAPPORT_MISSION_ANALYSEURS_SEMANTIQUES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RAPPORT_SESSION_2025-09-30.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RAPPORT_SESSION_AUTONOME.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/README_AUTONOMOUS_APPROVALS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/README_MISSION_PANINI.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/REPONSE_HIERARCHIE_EXCLUSIVE_CONFIRMEE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RESOLUTION_AFFICHAGE_CONTENU.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RESOLUTION_DEFINITIVE_CORPUS.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/RESUME_EXECUTIF_PANINI.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/SESSION_COMPLETE_SYNTHESE_EXECUTIVE.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/SESSION_SUMMARY_20251003.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/SOLUTION_APPROBATION_COMMANDES_AUTONOMES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/SPEC_KIT_INTEGRATION.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/STRATEGIC_REFACTORING_PLAN.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/STRATEGIE_AGENTS_UNIVERSAUX_SEMANTIQUES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/STRATEGIE_RAFFINEE_PLAN_TRAVAIL.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/SYNTHESE_CLARIFICATIONS_INTEGREES.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/VALIDATION_SYSTEM_HIERARCHIQUE_CORPUS_REEL.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/VUE_MODELE_PANINI_COMPLET.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/activity_dashboard_data.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/advanced_reconstruction_validation_1759520023.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/api_documentation_compressed.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/audit_server_consolidation.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/auto_update_dashboard.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/backlog_review_results_2025-10-01T16-45-19Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/backlog_review_results_2025-10-01T16-45-25Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/compression_benchmarks.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/compression_validation_results.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/copilotage_date_compliance_2025-09-29T20-22-03Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/copilotage_date_compliance_2025-09-29T20-22-13Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/copilotage_date_compliance_2025-09-29T20-28-19Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/copilotage_date_iso_standard.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/dashboard_activity_focused.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/dashboard_data.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/dashboard_real_data.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/dashboard_real_panini.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/dashboard_web_semantic.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/demo_analyse_enrichie.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/demo_decomposition_detaillee.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/deploy_phase1_dashboard.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/extracted_content.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/index.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/interface_decomposition_complete.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/iso8601_compliance_report_2025-10-01T13-39-40Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/issue13_semantic_atoms_discovery_2025-10-03T00-39-54Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/issue13_semantic_atoms_discovery_2025-10-03T12-24-46Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/issue13_semantic_atoms_discovery_2025-10-03T14-10-46Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/launch_advanced_demo.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/mission_alignment_report_2025-10-01T15-25-43Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/mission_alignment_report_2025-10-01T15-48-06Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/multilingual_embeddings.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/orchestrator_state_2025-10-01T14-25-27Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_advanced_uhd_clean.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_advanced_uhd_reconstructor.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_binary_decomposer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_clean_final.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_demo_data_generator.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_deployment_guide_20251003_135653.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_detailed_size_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_duplicate_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_ecosystem_orchestrator.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_ecosystem_state_2025-10-01T14-55-21Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_ecosystem_state_2025-10-01T15-48-50Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_format_discovery_engine.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_full_stack_digesteur.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_git_repo_architecture.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_hierarchical_architecture.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_internal_structure_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_issue11_final_validator.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_issue12_separation_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_issue13_semantic_atoms.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_issue14_dashboard_realtime.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_optimization_discovery_engine.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_performance_analyzer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_real_data.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_repos_status_viewer.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_serveur_corrige.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_simple_server.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_size_analysis_engine.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_test_corpus_generator.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_uhd_interface.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_universal_batch_20251003_135646.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_universal_format_engine.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-02T22-12-15Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-02T22-15-33Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-02T22-17-18Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-02T22-17-32Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-03T12-24-32Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-03T12-25-06Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-03T13-30-03Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-03T13-46-19Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validation_report_2025-10-03T14-10-46Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_validators_core.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_vfs_architecture_20251003_135649.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_virtual_fs_architecture.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_web_backend.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_web_explorer_prototype.html
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_web_frontend_specs_20251003_135653.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_web_interface_generator.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/panini_webdav_server.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/phase1_progress_report.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/phase1_session_log.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/playwright_diagnostic_1759520886.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr11_comment.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr13_comment.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr14_comment.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr16_comment.md
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr_compliance_report_2025-10-01T13-51-28Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/pr_compliance_report_2025-10-01T14-03-48Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/project_essence_extraction_2025-10-01T15-42-06Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/semantic_dashboard_summary_2025-10-02T21-20-38Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/semantic_orchestration_2025-10-02T21-11-00Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/semantic_orchestration_2025-10-02T21-11-47Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/semantic_orchestration_2025-10-02T21-16-38Z.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/serveur_decomposition_complete.py
D	sauvegarde_projets_reels_20251014_172522/research_backup/setup_panini_research_repo.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/start_phase1_monitoring.sh
D	sauvegarde_projets_reels_20251014_172522/research_backup/symmetry_detection_real_panini_data.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/symmetry_detection_results.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/training_metrics.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/translator_bias_style_analysis.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/translator_database_sample.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/translator_metadata_extraction.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/translators_metadata.json
D	sauvegarde_projets_reels_20251014_172522/research_backup/txt_extraction_2025-10-01T13-02-45Z.json
D	test-alignement-tableaux.html
```

### Statistiques

```
commit a61efae923ddaa4a609c59f944c837cfaeefeb45
Author: stephanedenis <stephane@sdenis.com>
Date:   Tue Nov 11 22:30:57 2025 -0500

    📦 Consolidation sauvegardes - Suppression duplicate
    
    - Supprimé sauvegarde_172522 (duplicate exact de 172503)
    - Archivé sauvegarde_172503 → legacy/backups/code_python/backup_2024-10-14_systeme_complet/
    - Créé README.md documentant les 31 fichiers Python (815KB)
    - Inventaire complet: 7 recherche, 4 Wikipedia, 4 validation, 3 optimisation, 13 PanLang
    - Libéré 156M espace (duplicate supprimé)
    
    Sauvegardes: 2 → 1 version de référence unique ✅

 .../journal/JOURNAL_AUTO_2025-11-11_hauru.md       |    210 +
 legacy/backups/code_python/README.md               |     77 +
 .../filesystem_backup/.cargo/config.toml           |      0
 .../.devcontainer/devcontainer.json                |     55 -
 .../filesystem_backup/.devcontainer/setup.sh       |     53 -
 .../filesystem_backup/.gitconfig.local             |     11 -
 .../.github/ISSUE_TEMPLATE/bug-report.md           |     56 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     29 -
 .../.github/ISSUE_TEMPLATE/bug_report.yml          |     80 -
 .../.github/ISSUE_TEMPLATE/config.yml              |      5 -
 .../.github/ISSUE_TEMPLATE/feature-request.md      |     74 -
 .../.github/ISSUE_TEMPLATE/feature_request.yml     |     71 -
 .../.github/ISSUE_TEMPLATE/research-task.md        |     54 -
 .../.github/ISSUE_TEMPLATE/research.md             |     19 -
 .../.github/ISSUE_TEMPLATE/submodule-change.yml    |     58 -
 .../.github/ISSUE_TEMPLATE/task.md                 |     24 -
 .../.github/PULL_REQUEST_TEMPLATE.md               |     26 -
 .../.github/ops/triggers/deploy-docs.txt           |      2 -
 .../.github/ops/triggers/pages-diagnostics.txt     |      2 -
 .../.github/pull_request_template.md               |      0
 .../.github/workflows/auto-merge-provenance.yml    |    100 -
 .../.github/workflows/camping-status.yml           |     29 -
 .../filesystem_backup/.github/workflows/codeql.yml |    108 -
 .../.github/workflows/copilotage-ci.yml            |     27 -
 .../.github/workflows/copilotage-journal-check.yml |     41 -
 .../.github/workflows/copilotage-journal-index.yml |     44 -
 .../.github/workflows/cross-check-visibility.yml   |     24 -
 .../.github/workflows/deploy-pages-mkdocs.yml      |    113 -
 .../.github/workflows/dhatu-validation.yml         |    187 -
 .../.github/workflows/docs-governance.yml          |    119 -
 .../.github/workflows/docs-pages.yml               |     48 -
 .../.github/workflows/e2e-playwright.yml           |     59 -
 .../.github/workflows/label-agent.yml              |    105 -
 .../.github/workflows/maintenance.yml              |     19 -
 .../.github/workflows/minimal-status.yml           |     10 -
 .../.github/workflows/owner-labeler.yml            |     77 -
 .../.github/workflows/pages-diagnostics.yml        |     46 -
 .../.github/workflows/pages-enforce-https.yml      |     51 -
 .../.github/workflows/paniniFS-ci.yml              |     16 -
 .../workflows/provenance-bootstrap-pr37.yml        |     39 -
 .../.github/workflows/provenance-guardian.yml      |    127 -
 .../.github/workflows/publications.yml             |     54 -
 .../.github/workflows/repo-guards.yml              |     22 -
 .../.github/workflows/secret-scan.yml              |     32 -
 .../.github/workflows/submodule-backfill.yml       |     43 -
 .../.github/workflows/submodule-triage.yml         |     71 -
 .../.github/workflows/update-modules-index.yml     |     38 -
 .../workflows/validate-agent-provenance.yml        |     43 -
 .../.github/workflows/validate-agent-session.yml   |     38 -
 .../workflows/validate-task-coordination.yml       |     55 -
 .../filesystem_backup/.gitignore                   |     41 -
 .../filesystem_backup/.gitmodules                  |     42 -
 .../filesystem_backup/.nojekyll                    |     10 -
 .../filesystem_backup/.panini-agent.toml           |      0
 .../filesystem_backup/CNAME                        |      1 -
 .../filesystem_backup/CONTRIBUTING.md              |     51 -
 .../filesystem_backup/COPILOTAGE_SHARED/README.md  |      9 -
 .../COPILOTAGE_SHARED/settings.json                |     11 -
 .../filesystem_backup/Cargo.toml                   |      0
 .../Copilotage/AGENT_CONVENTION.md                 |     19 -
 .../ARCHITECTURE_RESTRUCTURATION_PLAN.md           |     24 -
 .../Copilotage/COPILOTAGE_WORKFLOW.md              |     46 -
 .../filesystem_backup/Copilotage/DEPRECATED.md     |     10 -
 .../Copilotage/DEPRECATED_README.md                |      7 -
 .../filesystem_backup/Copilotage/README.md         |     46 -
 .../Copilotage/TODO_RELAIS_2025-09-02.md           |     12 -
 .../Copilotage/agents/adversarial_critic_agent.py  |      0
 .../Copilotage/agents/orchestrator_with_github.py  |      0
 .../Copilotage/agents/requirements.txt             |     10 -
 .../agents/simple_autonomous_orchestrator.py       |      0
 .../Copilotage/agents/tests/test_agents.py         |     45 -
 .../agents/theoretical_research_agent.py           |      0
 .../Copilotage/coordination-agent.py               |      0
 .../Copilotage/debug_notebook_local.ipynb          |      0
 .../Copilotage/demo-prototypage-rapide.md          |      0
 ...elargissement-horizon-mathematiques-physique.md |      0
 .../Copilotage/headless_autonomous_controller.py   |      0
 .../filesystem_backup/Copilotage/hyperscript-2.sh  |      0
 ...-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md |    339 -
 .../journal/2025-08-30-ci-stabilisation-merge.md   |     17 -
 .../journal/2025-08-30-hauru-pid74498-session.md   |     30 -
 .../2025-08-30-linux-pid0-assimilation-archives.md |     30 -
 .../Copilotage/journal/2025-08-30-session.md       |     24 -
 .../2025-08-30-totoro-pid17771-camping-final.md    |     39 -
 .../journal/2025-09-01-totoro-pid389223-session.md |     46 -
 .../2025-09-01-totoro-pid390178-rattrapage.md      |     53 -
 .../filesystem_backup/Copilotage/journal/INDEX.md  |     14 -
 .../Copilotage/knowledge/ESSENCE_PANINIFS.md       |     37 -
 .../knowledge/HYPERNODAL_DB_AND_LATTICE.md         |     23 -
 .../MODULES_OVERVIEW_AND_PARENT_PROJECT.md         |     29 -
 .../PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md    |     22 -
 .../knowledge/SEMANTIC_UNIVERSALS_DHATU.md         |     39 -
 .../Copilotage/mission_autonome_exemplaire.py      |      0
 .../Copilotage/notes-vision-architecturale.md      |      0
 .../Copilotage/roadmap-decouverte.md               |      0
 .../Copilotage/roadmap-hybride-rd-production.md    |      0
 .../filesystem_backup/Copilotage/roadmap.md        |     16 -
 .../Copilotage/scripts/COLAB_SETUP_GUIDE.md        |      0
 .../filesystem_backup/Copilotage/scripts/README.md |     17 -
 .../scripts/advanced_consensus_engine.py           |      0
 .../Copilotage/scripts/analogy_collector.py        |      0
 .../Copilotage/scripts/analyze_preferences.py      |      0
 .../Copilotage/scripts/arxiv_collector.py          |      0
 .../Copilotage/scripts/autonomous_analyzer.py      |      0
 .../scripts/autonomous_gdrive_manager.py           |      0
 .../Copilotage/scripts/books_collector.py          |      0
 .../Copilotage/scripts/colab_api_strategy.py       |      0
 .../scripts/colab_autonomous_controller.py         |      0
 .../Copilotage/scripts/colab_cli_launcher.py       |      0
 .../Copilotage/scripts/colab_debug_environment.py  |      0
 .../Copilotage/scripts/collect_samples.py          |      0
 .../Copilotage/scripts/collect_with_attribution.py |      0
 .../Copilotage/scripts/complete_journey_summary.py |      0
 .../scripts/comprehensive_opensource_strategy.py   |      0
 .../scripts/connivance_learning_system.py          |      0
 .../Copilotage/scripts/consensus_analyzer.py       |      0
 .../scripts/continuous_autonomy_daemon.py          |      0
 .../Copilotage/scripts/debug_ultra_fast.py         |      0
 .../Copilotage/scripts/deep_cleanup_credentials.sh |      0
 .../Copilotage/scripts/deploy_colab_auto.sh        |      0
 .../Copilotage/scripts/deploy_colab_fixed.sh       |      0
 .../Copilotage/scripts/deploy_colab_secure.sh      |      0
 .../Copilotage/scripts/devops/README.md            |     23 -
 .../scripts/devops/bootstrap_submodules.sh         |     38 -
 .../Copilotage/scripts/devops/fix_remotes.sh       |    103 -
 .../Copilotage/scripts/devops/gh_pr_exempt.sh      |     25 -
 .../Copilotage/scripts/devops/gh_pr_open.sh        |     90 -
 .../Copilotage/scripts/devops/gh_queue.sh          |     67 -
 .../Copilotage/scripts/devops/gh_task_init.sh      |     49 -
 .../Copilotage/scripts/devops/git_audit.sh         |     35 -
 .../devops/init_execution_orchestrator_repo.sh     |     39 -
 .../Copilotage/scripts/devops/journal_index.sh     |     33 -
 .../Copilotage/scripts/devops/journal_session.sh   |     43 -
 .../scripts/devops/plan_migration_option_b.sh      |     39 -
 .../Copilotage/scripts/devops/run_safe.sh          |     18 -
 .../scripts/devops/setup_dev_environment.sh        |     26 -
 .../Copilotage/scripts/display_recommendations.py  |      0
 .../scripts/distribution_strategy_analyzer.py      |      0
 .../scripts/editorial/sync_publications.py         |    125 -
 .../Copilotage/scripts/emergency_plasma_fix.sh     |      0
 .../scripts/executive_summary_generator.py         |      0
 .../scripts/executive_totoro_recommendations.py    |      0
 .../Copilotage/scripts/externalization_strategy.py |      0
 .../Copilotage/scripts/final_security_check.sh     |      0
 .../Copilotage/scripts/fix_git_credentials.sh      |      0
 .../Copilotage/scripts/free_cloud_analysis.py      |      0
 .../scripts/generate_remarkable_bibliography.py    |      0
 .../scripts/generate_scientific_bibliography.py    |      0
 .../Copilotage/scripts/github_workflow_doctor.py   |      0
 .../Copilotage/scripts/github_workflow_monitor.py  |     38 -
 .../Copilotage/scripts/google_colab_setup.py       |      0
 .../Copilotage/scripts/gpu_analysis_gt630m.py      |      0
 .../scripts/hardware_integration_guide.py          |      0
 .../Copilotage/scripts/hauru_setup.sh              |      0
 .../scripts/headless_autonomy_auditor.py           |      0
 .../Copilotage/scripts/headless_env_loader.py      |     53 -
 .../Copilotage/scripts/headless_secrets_manager.py |      0
 .../Copilotage/scripts/immediate_launch_plan.py    |      0
 .../scripts/implementation_roadmap_generator.py    |      0
 .../scripts/information_theory_collector.py        |      0
 .../scripts/intelligent_communication_guide.py     |      0
 .../Copilotage/scripts/launch_cloud_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_direct.sh      |      0
 .../Copilotage/scripts/launch_optimized_colab.sh   |      0
 .../Copilotage/scripts/launch_simple.sh            |      0
 .../Copilotage/scripts/launch_total_autonomy.sh    |      0
 .../mathematics_physics_convergence_analyzer.py    |      0
 .../Copilotage/scripts/multi_source_analyzer.py    |      0
 .../scripts/neurocognitive_language_analyzer.py    |      0
 .../scripts/opensource_resources_analyzer.py       |      0
 .../scripts/optimal_language_synthesizer.py        |      0
 .../scripts/optimal_vocabulary_generator.py        |      0
 .../scripts/paniniFS_priority_strategy.py          |      0
 .../scripts/panini_analogical_extension.py         |      0
 .../scripts/panini_architectural_integrator.py     |      0
 .../Copilotage/scripts/panini_dashboard.py         |      0
 .../scripts/panini_fundamental_generator.py        |      0
 .../scripts/panini_linguistic_integrator.py        |      0
 .../Copilotage/scripts/panini_status_point.py      |      0
 .../scripts/pedagogical_applications_guide.py      |      0
 .../scripts/physics_mathematics_collector.py       |      0
 .../scripts/plasma_stabilizer_advanced.sh          |      0
 .../Copilotage/scripts/publication_generator.py    |      0
 .../Copilotage/scripts/realistic_gpu_assessment.py |      0
 .../Copilotage/scripts/requirements.txt            |     18 -
 .../Copilotage/scripts/run_analysis.sh             |      0
 .../Copilotage/scripts/rust_bridge.py              |      0
 .../Copilotage/scripts/safe_totoro_optimizer.py    |      0
 .../scripts/secure_cleanup_credentials.sh          |      0
 .../filesystem_backup/Copilotage/scripts/setup.py  |      0
 .../Copilotage/scripts/setup_cloud_autonomous.sh   |      0
 .../Copilotage/scripts/setup_gdrive_config.py      |      0
 .../scripts/social_revolution_strategy.py          |      0
 .../scripts/solid_foundation_strategy.py           |      0
 .../scripts/temporal_emergence_analyzer.py         |      0
 .../Copilotage/scripts/test_regression.sh          |      0
 .../Copilotage/scripts/test_workflow_complete.py   |      0
 .../Copilotage/scripts/tests/test_basic.py         |     41 -
 .../Copilotage/scripts/tests/test_monitor.py       |     12 -
 .../Copilotage/scripts/total_autonomy_engine.py    |      0
 .../scripts/totoro_liberation_toolkit.sh           |      0
 .../Copilotage/scripts/totoro_optimizer.py         |      0
 .../scripts/totoro_resource_management.py          |      0
 .../Copilotage/scripts/traceability_dashboard.py   |      0
 .../scripts/ultra_reactive_controller.py           |      0
 .../scripts/vscode_extensions_manager.py           |      0
 .../Copilotage/scripts/vscode_settings_fixer.py    |      0
 .../Copilotage/session-bilan-vision-realite.md     |      0
 .../filesystem_backup/Copilotage/setup-rust.md     |      0
 .../filesystem_backup/Copilotage/test-build.sh     |      0
 .../Copilotage/tracabilite-attribution.md          |     20 -
 .../filesystem_backup/LICENSE                      |     21 -
 .../Panini_Ecosystem_Coherence_Audit.ipynb         |      0
 .../filesystem_backup/README.en.md                 |      0
 .../filesystem_backup/README.md                    |    159 -
 .../cloud-processing/FREE_COMPUTE_STRATEGY.md      |    110 -
 .../BABY_SIGN_LANGUAGE_FOUNDATION.md               |      0
 .../dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md  |      0
 .../DHATU_ATOMES_CONCEPTUELS_REVISION.md           |      0
 .../filesystem_backup/RESEARCH/docs/README.md      |      6 -
 .../methodology/protocols/GUIDE_LEANPUB_ETAPE1.md  |      0
 .../methodology/protocols/GUIDE_MEDIUM_ETAPE3.md   |      0
 .../protocols/ORDRE_PUBLICATION_GUIDE.md           |      0
 .../protocols/PUBLICATION_COORDONNEE_20250820.md   |      0
 .../protocols/SYNCHRONISATION_MEDIUM_2025.md       |     83 -
 .../articles/ARTICLE_MEDIUM_FINAL_2025.md          |      0
 .../articles/ARTICLE_MEDIUM_FINAL_2025_EN.md       |      0
 .../articles/english/ARTICLE_MEDIUM_2025_EN.md     |    419 -
 .../articles/french/ARTICLE_MEDIUM_2025.md         |    408 -
 .../publications/books/LIVRE_LEANPUB_FINAL_2025.md |      0
 .../books/english/LIVRE_LEANPUB_2025_EN.md         |      0
 .../books/french/LIVRE_LEANPUB_2025.md             |    554 -
 .../filesystem_backup/activate_total_autonomy.sh   |      0
 .../filesystem_backup/analogy_detector_mvp.py      |      0
 .../filesystem_backup/android_template.java        |      0
 .../artifacts/playwright/pr-40-checks.png          |    Bin 274486 -> 0 bytes
 .../artifacts/playwright/pr-40-overview.png        |    Bin 693119 -> 0 bytes
 .../artifacts/playwright/pr-42-checks.png          |    Bin 179199 -> 0 bytes
 .../artifacts/playwright/pr-42-overview.png        |    Bin 711460 -> 0 bytes
 .../snapshots/snapshot-20250902-152737.txt         |     40 -
 .../filesystem_backup/autonomous_colab_tester.py   |      0
 .../filesystem_backup/autonomous_test_log.json     |     20 -
 .../autonomous_workflow_doctor.py                  |      0
 .../filesystem_backup/check_colab_mission.py       |      0
 .../filesystem_backup/check_deployment.sh          |      0
 .../filesystem_backup/check_dns.sh                 |      0
 .../filesystem_backup/cleanup/manifest.txt         |     92 -
 .../cloud_backup/autonomous_crontab_simple.txt     |      0
 .../filesystem_backup/configure_vacation_mode.sh   |      0
 .../filesystem_backup/copilotage/README.md         |      8 -
 .../filesystem_backup/copilotage/config.yml        |      8 -
 .../filesystem_backup/copilotage/shared/README.md  |      3 -
 .../filesystem_backup/copilotage/shared/config.yml |      1 -
 .../filesystem_backup/data/ecosystem.yml           |    121 -
 .../filesystem_backup/deploy_cloud_autonomous.py   |      0
 .../filesystem_backup/deploy_cloud_ecosystem.sh    |      0
 .../deploy_colab_deployment_center.py              |      0
 .../filesystem_backup/deploy_docs.sh               |      0
 .../filesystem_backup/deploy_dynamic_monitoring.sh |     99 -
 .../filesystem_backup/deploy_paninifs.sh           |      0
 .../filesystem_backup/deploy_paninifs_simple.sh    |      0
 .../filesystem_backup/dhatu_detector.py            |      0
 .../filesystem_backup/docs/.keep                   |      1 -
 .../docs/OPERATIONS/DevOps/roadmap.md              |      5 -
 .../filesystem_backup/docs/avancement.md           |     15 -
 .../filesystem_backup/docs/dashboard.md            |    205 -
 .../docs/data/dhatu_child_langs.md                 |     25 -
 .../docs/data/dhatu_child_phenomena_summary.md     |     25 -
 .../filesystem_backup/docs/data/system_status.json |    127 -
 .../filesystem_backup/docs/dhatu-framework.md      |     13 -
 .../filesystem_backup/docs/diagrams.md             |     26 -
 .../filesystem_backup/docs/doc-process.md          |      9 -
 .../filesystem_backup/docs/ecosystem/README.md     |     26 -
 .../filesystem_backup/docs/ecosystem/catalogue.md  |      5 -
 .../filesystem_backup/docs/ecosystem/ontowave.md   |     55 -
 .../filesystem_backup/docs/ecosystem/panorama.md   |      5 -
 .../docs/ecosystem/repos/attribution-registry.md   |     10 -
 .../docs/ecosystem/repos/autonomous-missions.md    |     10 -
 .../docs/ecosystem/repos/copilotage-shared.md      |     10 -
 .../docs/ecosystem/repos/datasets-ingestion.md     |     10 -
 .../docs/ecosystem/repos/execution-orchestrator.md |     10 -
 .../docs/ecosystem/repos/ontowave-app.md           |     10 -
 .../docs/ecosystem/repos/publication-engine.md     |     10 -
 .../docs/ecosystem/repos/research.md               |     10 -
 .../filesystem_backup/docs/ecosystem/repos/root.md |     10 -
 .../docs/ecosystem/repos/semantic-core.md          |     10 -
 .../docs/ecosystem/repos/ultra-reactive.md         |     10 -
 .../docs/en/OPERATIONS/DevOps/roadmap.md           |      5 -
 .../filesystem_backup/docs/en/avancement.md        |     15 -
 .../filesystem_backup/docs/en/dhatu-framework.md   |     13 -
 .../filesystem_backup/docs/en/diagrams.md          |     26 -
 .../filesystem_backup/docs/en/doc-process.md       |      7 -
 .../docs/en/ecosystem/ontowave.md                  |     55 -
 .../filesystem_backup/docs/en/index.md             |     43 -
 .../filesystem_backup/docs/en/infrastructure.md    |      0
 .../filesystem_backup/docs/en/licences.md          |      7 -
 .../docs/en/linguistic-foundations.md              |      7 -
 .../docs/en/livre/lecture-integrale.md             |      9 -
 .../filesystem_backup/docs/en/modules/index.md     |     10 -
 .../filesystem_backup/docs/en/monitoring-guide.md  |      3 -
 .../filesystem_backup/docs/en/monitoring.md        |      0
 .../docs/en/operations/devops/roadmap.md           |      9 -
 .../filesystem_backup/docs/en/progress.md          |     15 -
 .../filesystem_backup/docs/en/publications.md      |     27 -
 .../filesystem_backup/docs/en/references.md        |      7 -
 .../docs/en/research/cloud-free-compute.md         |      5 -
 .../docs/en/research/compression-semantique.md     |      7 -
 .../docs/en/research/dhatu-inventory-v0-1.md       |     50 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    129 -
 .../docs/en/research/human-language-development.md |     70 -
 .../en/research/hypotheses-and-alternatives.md     |      5 -
 .../filesystem_backup/docs/en/research/index.md    |      7 -
 .../docs/en/research/inventaire-dhatu-v0-1.md      |      7 -
 .../en/research/langage-humain-developpement.md    |      7 -
 .../filesystem_backup/docs/en/research/overview.md |     29 -
 .../docs/en/research/references.md                 |     57 -
 .../docs/en/research/semantic-compression.md       |     47 -
 .../docs/en/research/semantic-universals.md        |     57 -
 .../docs/en/research/universaux-semantique.md      |      9 -
 .../docs/en/research/whats-new.md                  |     21 -
 .../filesystem_backup/docs/en/style-guide.md       |      6 -
 .../filesystem_backup/docs/en/vision-social.md     |     11 -
 .../filesystem_backup/docs/en/vision-sociale.md    |     11 -
 .../filesystem_backup/docs/en/vision.md            |      9 -
 .../filesystem_backup/docs/index.md                |     45 -
 .../filesystem_backup/docs/infrastructure.md       |      0
 .../filesystem_backup/docs/licences.md             |      7 -
 .../docs/linguistic-foundations.md                 |      7 -
 .../filesystem_backup/docs/livre/index.md          |     25 -
 .../docs/livre/lecture-integrale.md                |      7 -
 .../filesystem_backup/docs/modules/_ext/.gitignore |      4 -
 .../filesystem_backup/docs/modules/index.md        |     19 -
 .../filesystem_backup/docs/monitoring-guide.md     |    188 -
 .../filesystem_backup/docs/monitoring.md           |      0
 .../docs/operations/devops/roadmap.md              |      9 -
 .../filesystem_backup/docs/publications.md         |     23 -
 .../filesystem_backup/docs/references.md           |      7 -
 .../filesystem_backup/docs/requirements.txt        |     13 -
 .../docs/research/cloud-free-compute.md            |      7 -
 .../docs/research/compression-semantique.md        |     52 -
 .../docs/research/dhatu-inventory-v0-1.md          |      6 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    141 -
 .../docs/research/human-language-development.md    |      5 -
 .../docs/research/hypotheses-and-alternatives.md   |     42 -
 .../filesystem_backup/docs/research/index.md       |     13 -
 .../docs/research/inventaire-dhatu-v0-1.md         |     51 -
 .../docs/research/langage-humain-developpement.md  |     63 -
 .../filesystem_backup/docs/research/overview.md    |     29 -
 .../filesystem_backup/docs/research/references.md  |     57 -
 .../docs/research/semantic-compression.md          |      5 -
 .../docs/research/semantic-universals.md           |      5 -
 .../docs/research/universaux-semantique.md         |    164 -
 .../docs/research/whats-new-feed.html              |     41 -
 .../filesystem_backup/docs/research/whats-new.html |     41 -
 .../filesystem_backup/docs/research/whats-new.md   |     21 -
 .../filesystem_backup/docs/style-guide.md          |      6 -
 .../filesystem_backup/docs/vision-sociale.md       |     11 -
 .../filesystem_backup/docs/vision.md               |      9 -
 .../filesystem_backup/doctor.pid                   |      1 -
 .../filesystem_backup/doctor_control.py            |      0
 .../filesystem_backup/doctor_dashboard.py          |      0
 .../filesystem_backup/doctor_watchdog.sh           |     10 -
 .../domain_monitoring_report.json                  |     59 -
 .../filesystem_backup/e2e/package.json             |     15 -
 .../filesystem_backup/e2e/playwright.config.js     |     13 -
 .../filesystem_backup/e2e/tests/modules.spec.js    |     44 -
 .../filesystem_backup/e2e/tests/research.spec.js   |     19 -
 .../filesystem_backup/e2e/tests/smoke.spec.js      |     14 -
 .../experiments/dhatu/gold_encodings.json          |     14 -
 .../experiments/dhatu/gold_encodings_child.json    |     22 -
 .../experiments/dhatu/inventory_v0_1.json          |     41 -
 .../experiments/dhatu/prompts_child/arb.json       |     15 -
 .../experiments/dhatu/prompts_child/cmn.json       |     15 -
 .../experiments/dhatu/prompts_child/deu.json       |     15 -
 .../experiments/dhatu/prompts_child/en.json        |     15 -
 .../experiments/dhatu/prompts_child/eus.json       |     15 -
 .../experiments/dhatu/prompts_child/ewe.json       |     15 -
 .../experiments/dhatu/prompts_child/fr.json        |     15 -
 .../experiments/dhatu/prompts_child/hau.json       |     15 -
 .../experiments/dhatu/prompts_child/heb.json       |     15 -
 .../experiments/dhatu/prompts_child/hin.json       |     15 -
 .../experiments/dhatu/prompts_child/hun.json       |     14 -
 .../experiments/dhatu/prompts_child/iku.json       |     15 -
 .../experiments/dhatu/prompts_child/jpn.json       |     15 -
 .../experiments/dhatu/prompts_child/kor.json       |     15 -
 .../experiments/dhatu/prompts_child/nld.json       |     15 -
 .../experiments/dhatu/prompts_child/schema.json    |     22 -
 .../experiments/dhatu/prompts_child/spa.json       |     15 -
 .../experiments/dhatu/prompts_child/swa.json       |     15 -
 .../experiments/dhatu/prompts_child/tur.json       |     15 -
 .../experiments/dhatu/prompts_child/yor.json       |     15 -
 .../experiments/dhatu/prompts_child/zul.json       |     15 -
 .../filesystem_backup/experiments/dhatu/report.py  |    113 -
 .../experiments/dhatu/toy_corpus.json              |     16 -
 .../experiments/dhatu/typological_sample.json      |    216 -
 .../experiments/dhatu/validator.py                 |    155 -
 .../filesystem_backup/firebase_notifications.py    |      0
 .../filesystem_backup/fix_google_oauth.sh          |      0
 .../filesystem_backup/fix_remotes.sh               |    299 -
 .../filesystem_backup/gdrive_credentials/README.md |      0
 .../gdrive_credentials/credentials.json.template   |      0
 .../filesystem_backup/git_audit.sh                 |      0
 .../filesystem_backup/github_workflow_doctor.py    |      0
 .../github_workflow_emergency_doctor.py            |      0
 .../governance/AUTONOMIE_VALIDATION_FINALE.md      |      3 -
 .../governance/CONVENTIONS_NAMING.md               |     22 -
 .../governance/SESSION_BILAN_ORGANISATION.md       |      3 -
 .../audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md    |      5 -
 .../audits/AUDIT_SYNCHRONISATION_GITHUB.md         |      3 -
 .../CENTRALISATION_DISCUSSIONS_COPILOTAGE.md       |      3 -
 .../governance/copilotage/POLICY.md                |     27 -
 .../governance/copilotage/README.md                |     48 -
 .../copilotage/README_COPILOTAGE_HISTORIQUE.md     |     45 -
 .../governance/copilotage/journal/INDEX.md         |      3 -
 .../copilotage/knowledge/ESSENCE_PANINIFS.md       |     39 -
 .../filesystem_backup/index.html                   |      0
 .../lancement_publications_20250820.sh             |      0
 .../filesystem_backup/last_domain_status.json      |     59 -
 .../filesystem_backup/launch_autonomous_doctor.sh  |      0
 .../launch_continuous_improvement.sh               |      0
 .../filesystem_backup/launch_hybrid_dashboard.sh   |     39 -
 .../filesystem_backup/mini_test_dhatu.py           |      0
 .../filesystem_backup/mkdocs.yml                   |    182 -
 .../filesystem_backup/mkdocs_fixed.yml             |      0
 .../attribution-registry/.github/workflows/ci.yml  |     11 -
 .../modules/attribution-registry/LICENSE           |      1 -
 .../modules/attribution-registry/README.md         |      1 -
 .../modules/attribution-registry/pyproject.toml    |      4 -
 .../autonomous-missions/.github/workflows/ci.yml   |     18 -
 .../modules/autonomous-missions/.gitignore         |    207 -
 .../modules/autonomous-missions/LICENSE            |     21 -
 .../modules/autonomous-missions/README.md          |      4 -
 .../modules/cloud-orchestrator/README.md           |      0
 .../modules/colab-controller/README.md             |      0
 .../datasets-ingestion/.github/workflows/ci.yml    |     11 -
 .../modules/datasets-ingestion/LICENSE             |      1 -
 .../modules/datasets-ingestion/README.md           |      1 -
 .../modules/datasets-ingestion/pyproject.toml      |      4 -
 .../.github/workflows/ci.yml                       |     22 -
 .../modules/execution-orchestrator/.gitignore      |      7 -
 .../modules/execution-orchestrator/LICENSE         |      1 -
 .../modules/execution-orchestrator/README.md       |     20 -
 .../modules/execution-orchestrator/pyproject.toml  |     17 -
 .../src/execution_orchestrator/cli.py              |     31 -
 .../src/execution_orchestrator/drivers/__init__.py |     18 -
 .../src/execution_orchestrator/drivers/cloud.py    |      5 -
 .../drivers/cloud/.github/workflows/ci.yml         |     18 -
 .../drivers/cloud/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/cloud/LICENSE   |     21 -
 .../execution_orchestrator/drivers/cloud/README.md |      4 -
 .../src/execution_orchestrator/drivers/colab.py    |      5 -
 .../drivers/colab/.github/workflows/ci.yml         |     18 -
 .../drivers/colab/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/colab/LICENSE   |     21 -
 .../execution_orchestrator/drivers/colab/README.md |      4 -
 .../src/execution_orchestrator/drivers/local.py    |      5 -
 .../modules/ontowave-app/.eslintrc.cjs             |     16 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     16 -
 .../.github/ISSUE_TEMPLATE/feature_request.md      |     13 -
 .../ontowave-app/.github/pull_request_template.md  |     12 -
 .../modules/ontowave-app/.github/workflows/ci.yml  |     34 -
 .../ontowave-app/.github/workflows/pr-preview.yml  |     27 -
 .../modules/ontowave-app/.gitignore                |      6 -
 .../modules/ontowave-app/.prettierignore           |      2 -
 .../modules/ontowave-app/.prettierrc               |      5 -
 .../filesystem_backup/modules/ontowave-app/LICENSE |     21 -
 .../modules/ontowave-app/README.md                 |     39 -
 .../modules/ontowave-app/content/index.md          |     16 -
 .../modules/ontowave-app/copilotage/README.md      |      7 -
 .../modules/ontowave-app/copilotage/RULES.md       |      8 -
 .../ontowave-app/copilotage/preferences.json       |      8 -
 .../ontowave-app/copilotage/preferences.yml        |     21 -
 .../ontowave-app/copilotage/scripts/prepare_pr.sh  |     27 -
 .../modules/ontowave-app/index.html                |     35 -
 .../modules/ontowave-app/package-lock.json         |   2426 -
 .../modules/ontowave-app/package.json              |     39 -
 .../modules/ontowave-app/public/config.json        |      5 -
 .../ontowave-app/scripts/check_principles.sh       |     13 -
 .../modules/ontowave-app/src/main.ts               |     53 -
 .../modules/ontowave-app/src/markdown.ts           |     51 -
 .../modules/ontowave-app/src/router.ts             |     28 -
 .../modules/ontowave-app/src/shims.d.ts            |      3 -
 .../modules/ontowave-app/tools/build-sitemap.mjs   |     47 -
 .../modules/ontowave-app/tsconfig.json             |     16 -
 .../modules/ontowave-app/vite.config.ts            |      6 -
 .../publication-engine/.github/workflows/ci.yml    |     18 -
 .../modules/publication-engine/.gitignore          |    207 -
 .../modules/publication-engine/LICENSE             |     21 -
 .../modules/publication-engine/README.md           |      2 -
 .../modules/semantic-core/.github/workflows/ci.yml |     18 -
 .../modules/semantic-core/.gitignore               |    207 -
 .../modules/semantic-core/LICENSE                  |     21 -
 .../modules/semantic-core/README.md                |      2 -
 .../ultra-reactive/.github/workflows/ci.yml        |     18 -
 .../modules/ultra-reactive/.gitignore              |    207 -
 .../modules/ultra-reactive/LICENSE                 |     21 -
 .../modules/ultra-reactive/README.md               |      4 -
 .../filesystem_backup/monitor_domains.py           |      0
 .../nocturnal_autonomous_mission.py                |      0
 .../filesystem_backup/nocturnal_mission_log.json   |     64 -
 .../filesystem_backup/notification_system.py       |      0
 .../prepare_total_externalization.sh               |    186 -
 .../filesystem_backup/publish_docs.sh              |      0
 .../filesystem_backup/quick_monitor.sh             |     48 -
 .../remarkable_study_pack/README.md                |      0
 .../reading_guides/workflow_revision_remarkable.md |      0
 .../scientific_articles/bibliographie_complete.md  |      0
 .../content_addressing_avance.md                   |      0
 .../scientific_articles/etat_art_avance.md         |      0
 .../scientific_articles/etudes_cas_exercices.md    |      0
 .../scientific_articles/fondements_theoriques.md   |      0
 .../ipfs_vs_paninifs_analysis.md                   |      0
 .../filesystem_backup/requirements.txt             |     15 -
 .../filesystem_backup/restructure_ecosystem.sh     |      0
 .../scripts/aggregate_submodule_docs.py            |     59 -
 .../scripts/analyze_submodule_issue.py             |    259 -
 .../scripts/apply_cleanup_manifest.sh              |     27 -
 .../scripts/auto_pilot_research.py                 |    159 -
 .../scripts/check_copilotage_independence.py       |     90 -
 .../scripts/detect_module_specific_content.py      |     91 -
 .../scripts/devops/audit_submodules.sh             |     53 -
 .../scripts/devops/generate_modules_index.py       |     68 -
 .../scripts/devops/monitor_prs_playwright.py       |     99 -
 .../scripts/devops/pr_auto_doctor.sh               |    202 -
 .../scripts/devops/repo_ci_snapshot.sh             |      0
 .../scripts/devops/terminal_diagnostics.sh         |      0
 .../scripts/devops/vscode_settings_tuner.py        |    149 -
 .../scripts/enforce_lowercase_paths.py             |     90 -
 .../scripts/generate_ecosystem_docs.py             |    201 -
 .../scripts/generate_modules_docs_index.py         |    111 -
 .../scripts/generate_research_rss.py               |    102 -
 .../scripts/noninteractive_env.sh                  |     11 -
 .../scripts/open_submodule_issues.py               |    104 -
 .../scripts/open_submodule_issues_gh.py            |     79 -
 .../scripts/prepare_issue_packs.py                 |    121 -
 .../scripts/setup_labels_submodules.sh             |     28 -
 .../scripts/split_to_submodule.sh                  |     48 -
 .../filesystem_backup/scripts/triage_submodules.py |    177 -
 .../filesystem_backup/setup_domains.sh             |      0
 .../filesystem_backup/setup_github_labels.sh       |     58 -
 .../filesystem_backup/setup_github_pages.sh        |      0
 .../filesystem_backup/setup_mvp_dataset.sh         |      0
 .../filesystem_backup/shutdown_totoro_procedure.sh |      0
 .../filesystem_backup/sync_paninifs_ecosystem.sh   |      0
 .../templates_publication_reseaux.md               |      0
 .../filesystem_backup/vacation_backup.sh           |     24 -
 .../vacation_emergency_monitor.sh                  |     44 -
 .../vacation_productive_system.py                  |      0
 .../vacation_productive_work.json                  |    222 -
 .../filesystem_backup/validate_dhatu.sh            |      0
 .../filesystem_backup/workflow_repair_report.json  |     36 -
 .../gitmodules_avant.txt                           |      9 -
 .../core/filesystem/.cargo/config.toml             |      0
 .../filesystem/.devcontainer/devcontainer.json     |     55 -
 .../core/filesystem/.devcontainer/setup.sh         |     53 -
 .../modules_avant/core/filesystem/.gitconfig.local |     11 -
 .../.github/ISSUE_TEMPLATE/bug-report.md           |     56 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     29 -
 .../.github/ISSUE_TEMPLATE/bug_report.yml          |     80 -
 .../filesystem/.github/ISSUE_TEMPLATE/config.yml   |      5 -
 .../.github/ISSUE_TEMPLATE/feature-request.md      |     74 -
 .../.github/ISSUE_TEMPLATE/feature_request.yml     |     71 -
 .../.github/ISSUE_TEMPLATE/research-task.md        |     54 -
 .../filesystem/.github/ISSUE_TEMPLATE/research.md  |     19 -
 .../.github/ISSUE_TEMPLATE/submodule-change.yml    |     58 -
 .../core/filesystem/.github/ISSUE_TEMPLATE/task.md |     24 -
 .../filesystem/.github/PULL_REQUEST_TEMPLATE.md    |     26 -
 .../.github/ops/triggers/deploy-docs.txt           |      2 -
 .../.github/ops/triggers/pages-diagnostics.txt     |      2 -
 .../filesystem/.github/pull_request_template.md    |      0
 .../.github/workflows/auto-merge-provenance.yml    |    100 -
 .../.github/workflows/camping-status.yml           |     29 -
 .../core/filesystem/.github/workflows/codeql.yml   |    108 -
 .../filesystem/.github/workflows/copilotage-ci.yml |     27 -
 .../.github/workflows/copilotage-journal-check.yml |     41 -
 .../.github/workflows/copilotage-journal-index.yml |     44 -
 .../.github/workflows/cross-check-visibility.yml   |     24 -
 .../.github/workflows/deploy-pages-mkdocs.yml      |    113 -
 .../.github/workflows/dhatu-validation.yml         |    187 -
 .../.github/workflows/docs-governance.yml          |    119 -
 .../filesystem/.github/workflows/docs-pages.yml    |     48 -
 .../.github/workflows/e2e-playwright.yml           |     59 -
 .../filesystem/.github/workflows/label-agent.yml   |    105 -
 .../filesystem/.github/workflows/maintenance.yml   |     19 -
 .../.github/workflows/minimal-status.yml           |     10 -
 .../filesystem/.github/workflows/owner-labeler.yml |     77 -
 .../.github/workflows/pages-diagnostics.yml        |     46 -
 .../.github/workflows/pages-enforce-https.yml      |     51 -
 .../filesystem/.github/workflows/paniniFS-ci.yml   |     16 -
 .../workflows/provenance-bootstrap-pr37.yml        |     39 -
 .../.github/workflows/provenance-guardian.yml      |    127 -
 .../filesystem/.github/workflows/publications.yml  |     54 -
 .../filesystem/.github/workflows/repo-guards.yml   |     22 -
 .../filesystem/.github/workflows/secret-scan.yml   |     32 -
 .../.github/workflows/submodule-backfill.yml       |     43 -
 .../.github/workflows/submodule-triage.yml         |     71 -
 .../.github/workflows/update-modules-index.yml     |     38 -
 .../workflows/validate-agent-provenance.yml        |     43 -
 .../.github/workflows/validate-agent-session.yml   |     38 -
 .../workflows/validate-task-coordination.yml       |     55 -
 .../modules_avant/core/filesystem/.gitignore       |     41 -
 .../modules_avant/core/filesystem/.gitmodules      |     42 -
 .../modules_avant/core/filesystem/.nojekyll        |     10 -
 .../core/filesystem/.panini-agent.toml             |      0
 .../modules_avant/core/filesystem/CNAME            |      1 -
 .../modules_avant/core/filesystem/CONTRIBUTING.md  |     51 -
 .../core/filesystem/COPILOTAGE_SHARED/README.md    |      9 -
 .../filesystem/COPILOTAGE_SHARED/settings.json     |     11 -
 .../modules_avant/core/filesystem/Cargo.toml       |      0
 .../core/filesystem/Copilotage/AGENT_CONVENTION.md |     19 -
 .../ARCHITECTURE_RESTRUCTURATION_PLAN.md           |     24 -
 .../filesystem/Copilotage/COPILOTAGE_WORKFLOW.md   |     46 -
 .../core/filesystem/Copilotage/DEPRECATED.md       |     10 -
 .../filesystem/Copilotage/DEPRECATED_README.md     |      7 -
 .../core/filesystem/Copilotage/README.md           |     46 -
 .../Copilotage/TODO_RELAIS_2025-09-02.md           |     12 -
 .../Copilotage/agents/adversarial_critic_agent.py  |      0
 .../Copilotage/agents/orchestrator_with_github.py  |      0
 .../filesystem/Copilotage/agents/requirements.txt  |     10 -
 .../agents/simple_autonomous_orchestrator.py       |      0
 .../Copilotage/agents/tests/test_agents.py         |     45 -
 .../agents/theoretical_research_agent.py           |      0
 .../filesystem/Copilotage/coordination-agent.py    |      0
 .../Copilotage/debug_notebook_local.ipynb          |      0
 .../Copilotage/demo-prototypage-rapide.md          |      0
 ...elargissement-horizon-mathematiques-physique.md |      0
 .../Copilotage/headless_autonomous_controller.py   |      0
 .../core/filesystem/Copilotage/hyperscript-2.sh    |      0
 ...-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md |    339 -
 .../journal/2025-08-30-ci-stabilisation-merge.md   |     17 -
 .../journal/2025-08-30-hauru-pid74498-session.md   |     30 -
 .../2025-08-30-linux-pid0-assimilation-archives.md |     30 -
 .../Copilotage/journal/2025-08-30-session.md       |     24 -
 .../2025-08-30-totoro-pid17771-camping-final.md    |     39 -
 .../journal/2025-09-01-totoro-pid389223-session.md |     46 -
 .../2025-09-01-totoro-pid390178-rattrapage.md      |     53 -
 .../core/filesystem/Copilotage/journal/INDEX.md    |     14 -
 .../Copilotage/knowledge/ESSENCE_PANINIFS.md       |     37 -
 .../knowledge/HYPERNODAL_DB_AND_LATTICE.md         |     23 -
 .../MODULES_OVERVIEW_AND_PARENT_PROJECT.md         |     29 -
 .../PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md    |     22 -
 .../knowledge/SEMANTIC_UNIVERSALS_DHATU.md         |     39 -
 .../Copilotage/mission_autonome_exemplaire.py      |      0
 .../Copilotage/notes-vision-architecturale.md      |      0
 .../filesystem/Copilotage/roadmap-decouverte.md    |      0
 .../Copilotage/roadmap-hybride-rd-production.md    |      0
 .../core/filesystem/Copilotage/roadmap.md          |     16 -
 .../Copilotage/scripts/COLAB_SETUP_GUIDE.md        |      0
 .../core/filesystem/Copilotage/scripts/README.md   |     17 -
 .../scripts/advanced_consensus_engine.py           |      0
 .../Copilotage/scripts/analogy_collector.py        |      0
 .../Copilotage/scripts/analyze_preferences.py      |      0
 .../Copilotage/scripts/arxiv_collector.py          |      0
 .../Copilotage/scripts/autonomous_analyzer.py      |      0
 .../scripts/autonomous_gdrive_manager.py           |      0
 .../Copilotage/scripts/books_collector.py          |      0
 .../Copilotage/scripts/colab_api_strategy.py       |      0
 .../scripts/colab_autonomous_controller.py         |      0
 .../Copilotage/scripts/colab_cli_launcher.py       |      0
 .../Copilotage/scripts/colab_debug_environment.py  |      0
 .../Copilotage/scripts/collect_samples.py          |      0
 .../Copilotage/scripts/collect_with_attribution.py |      0
 .../Copilotage/scripts/complete_journey_summary.py |      0
 .../scripts/comprehensive_opensource_strategy.py   |      0
 .../scripts/connivance_learning_system.py          |      0
 .../Copilotage/scripts/consensus_analyzer.py       |      0
 .../scripts/continuous_autonomy_daemon.py          |      0
 .../Copilotage/scripts/debug_ultra_fast.py         |      0
 .../Copilotage/scripts/deep_cleanup_credentials.sh |      0
 .../Copilotage/scripts/deploy_colab_auto.sh        |      0
 .../Copilotage/scripts/deploy_colab_fixed.sh       |      0
 .../Copilotage/scripts/deploy_colab_secure.sh      |      0
 .../filesystem/Copilotage/scripts/devops/README.md |     23 -
 .../scripts/devops/bootstrap_submodules.sh         |     38 -
 .../Copilotage/scripts/devops/fix_remotes.sh       |    103 -
 .../Copilotage/scripts/devops/gh_pr_exempt.sh      |     25 -
 .../Copilotage/scripts/devops/gh_pr_open.sh        |     90 -
 .../Copilotage/scripts/devops/gh_queue.sh          |     67 -
 .../Copilotage/scripts/devops/gh_task_init.sh      |     49 -
 .../Copilotage/scripts/devops/git_audit.sh         |     35 -
 .../devops/init_execution_orchestrator_repo.sh     |     39 -
 .../Copilotage/scripts/devops/journal_index.sh     |     33 -
 .../Copilotage/scripts/devops/journal_session.sh   |     43 -
 .../scripts/devops/plan_migration_option_b.sh      |     39 -
 .../Copilotage/scripts/devops/run_safe.sh          |     18 -
 .../scripts/devops/setup_dev_environment.sh        |     26 -
 .../Copilotage/scripts/display_recommendations.py  |      0
 .../scripts/distribution_strategy_analyzer.py      |      0
 .../scripts/editorial/sync_publications.py         |    125 -
 .../Copilotage/scripts/emergency_plasma_fix.sh     |      0
 .../scripts/executive_summary_generator.py         |      0
 .../scripts/executive_totoro_recommendations.py    |      0
 .../Copilotage/scripts/externalization_strategy.py |      0
 .../Copilotage/scripts/final_security_check.sh     |      0
 .../Copilotage/scripts/fix_git_credentials.sh      |      0
 .../Copilotage/scripts/free_cloud_analysis.py      |      0
 .../scripts/generate_remarkable_bibliography.py    |      0
 .../scripts/generate_scientific_bibliography.py    |      0
 .../Copilotage/scripts/github_workflow_doctor.py   |      0
 .../Copilotage/scripts/github_workflow_monitor.py  |     38 -
 .../Copilotage/scripts/google_colab_setup.py       |      0
 .../Copilotage/scripts/gpu_analysis_gt630m.py      |      0
 .../scripts/hardware_integration_guide.py          |      0
 .../filesystem/Copilotage/scripts/hauru_setup.sh   |      0
 .../scripts/headless_autonomy_auditor.py           |      0
 .../Copilotage/scripts/headless_env_loader.py      |     53 -
 .../Copilotage/scripts/headless_secrets_manager.py |      0
 .../Copilotage/scripts/immediate_launch_plan.py    |      0
 .../scripts/implementation_roadmap_generator.py    |      0
 .../scripts/information_theory_collector.py        |      0
 .../scripts/intelligent_communication_guide.py     |      0
 .../Copilotage/scripts/launch_cloud_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_direct.sh      |      0
 .../Copilotage/scripts/launch_optimized_colab.sh   |      0
 .../filesystem/Copilotage/scripts/launch_simple.sh |      0
 .../Copilotage/scripts/launch_total_autonomy.sh    |      0
 .../mathematics_physics_convergence_analyzer.py    |      0
 .../Copilotage/scripts/multi_source_analyzer.py    |      0
 .../scripts/neurocognitive_language_analyzer.py    |      0
 .../scripts/opensource_resources_analyzer.py       |      0
 .../scripts/optimal_language_synthesizer.py        |      0
 .../scripts/optimal_vocabulary_generator.py        |      0
 .../scripts/paniniFS_priority_strategy.py          |      0
 .../scripts/panini_analogical_extension.py         |      0
 .../scripts/panini_architectural_integrator.py     |      0
 .../Copilotage/scripts/panini_dashboard.py         |      0
 .../scripts/panini_fundamental_generator.py        |      0
 .../scripts/panini_linguistic_integrator.py        |      0
 .../Copilotage/scripts/panini_status_point.py      |      0
 .../scripts/pedagogical_applications_guide.py      |      0
 .../scripts/physics_mathematics_collector.py       |      0
 .../scripts/plasma_stabilizer_advanced.sh          |      0
 .../Copilotage/scripts/publication_generator.py    |      0
 .../Copilotage/scripts/realistic_gpu_assessment.py |      0
 .../filesystem/Copilotage/scripts/requirements.txt |     18 -
 .../filesystem/Copilotage/scripts/run_analysis.sh  |      0
 .../filesystem/Copilotage/scripts/rust_bridge.py   |      0
 .../Copilotage/scripts/safe_totoro_optimizer.py    |      0
 .../scripts/secure_cleanup_credentials.sh          |      0
 .../core/filesystem/Copilotage/scripts/setup.py    |      0
 .../Copilotage/scripts/setup_cloud_autonomous.sh   |      0
 .../Copilotage/scripts/setup_gdrive_config.py      |      0
 .../scripts/social_revolution_strategy.py          |      0
 .../scripts/solid_foundation_strategy.py           |      0
 .../scripts/temporal_emergence_analyzer.py         |      0
 .../Copilotage/scripts/test_regression.sh          |      0
 .../Copilotage/scripts/test_workflow_complete.py   |      0
 .../Copilotage/scripts/tests/test_basic.py         |     41 -
 .../Copilotage/scripts/tests/test_monitor.py       |     12 -
 .../Copilotage/scripts/total_autonomy_engine.py    |      0
 .../scripts/totoro_liberation_toolkit.sh           |      0
 .../Copilotage/scripts/totoro_optimizer.py         |      0
 .../scripts/totoro_resource_management.py          |      0
 .../Copilotage/scripts/traceability_dashboard.py   |      0
 .../scripts/ultra_reactive_controller.py           |      0
 .../scripts/vscode_extensions_manager.py           |      0
 .../Copilotage/scripts/vscode_settings_fixer.py    |      0
 .../Copilotage/session-bilan-vision-realite.md     |      0
 .../core/filesystem/Copilotage/setup-rust.md       |      0
 .../core/filesystem/Copilotage/test-build.sh       |      0
 .../Copilotage/tracabilite-attribution.md          |     20 -
 .../modules_avant/core/filesystem/LICENSE          |     21 -
 .../Panini_Ecosystem_Coherence_Audit.ipynb         |      0
 .../modules_avant/core/filesystem/README.en.md     |      0
 .../modules_avant/core/filesystem/README.md        |    159 -
 .../cloud-processing/FREE_COMPUTE_STRATEGY.md      |    110 -
 .../BABY_SIGN_LANGUAGE_FOUNDATION.md               |      0
 .../dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md  |      0
 .../DHATU_ATOMES_CONCEPTUELS_REVISION.md           |      0
 .../core/filesystem/RESEARCH/docs/README.md        |      6 -
 .../methodology/protocols/GUIDE_LEANPUB_ETAPE1.md  |      0
 .../methodology/protocols/GUIDE_MEDIUM_ETAPE3.md   |      0
 .../protocols/ORDRE_PUBLICATION_GUIDE.md           |      0
 .../protocols/PUBLICATION_COORDONNEE_20250820.md   |      0
 .../protocols/SYNCHRONISATION_MEDIUM_2025.md       |     83 -
 .../articles/ARTICLE_MEDIUM_FINAL_2025.md          |      0
 .../articles/ARTICLE_MEDIUM_FINAL_2025_EN.md       |      0
 .../articles/english/ARTICLE_MEDIUM_2025_EN.md     |    419 -
 .../articles/french/ARTICLE_MEDIUM_2025.md         |    408 -
 .../publications/books/LIVRE_LEANPUB_FINAL_2025.md |      0
 .../books/english/LIVRE_LEANPUB_2025_EN.md         |      0
 .../books/french/LIVRE_LEANPUB_2025.md             |    554 -
 .../core/filesystem/activate_total_autonomy.sh     |      0
 .../core/filesystem/analogy_detector_mvp.py        |      0
 .../core/filesystem/android_template.java          |      0
 .../artifacts/playwright/pr-40-checks.png          |    Bin 274486 -> 0 bytes
 .../artifacts/playwright/pr-40-overview.png        |    Bin 693119 -> 0 bytes
 .../artifacts/playwright/pr-42-checks.png          |    Bin 179199 -> 0 bytes
 .../artifacts/playwright/pr-42-overview.png        |    Bin 711460 -> 0 bytes
 .../snapshots/snapshot-20250902-152737.txt         |     40 -
 .../core/filesystem/autonomous_colab_tester.py     |      0
 .../core/filesystem/autonomous_test_log.json       |     20 -
 .../core/filesystem/autonomous_workflow_doctor.py  |      0
 .../core/filesystem/check_colab_mission.py         |      0
 .../core/filesystem/check_deployment.sh            |      0
 .../modules_avant/core/filesystem/check_dns.sh     |      0
 .../core/filesystem/cleanup/manifest.txt           |     92 -
 .../cloud_backup/autonomous_crontab_simple.txt     |      0
 .../core/filesystem/configure_vacation_mode.sh     |      0
 .../core/filesystem/copilotage/README.md           |      8 -
 .../core/filesystem/copilotage/config.yml          |      8 -
 .../core/filesystem/copilotage/shared/README.md    |      3 -
 .../core/filesystem/copilotage/shared/config.yml   |      1 -
 .../core/filesystem/data/ecosystem.yml             |    121 -
 .../core/filesystem/deploy_cloud_autonomous.py     |      0
 .../core/filesystem/deploy_cloud_ecosystem.sh      |      0
 .../filesystem/deploy_colab_deployment_center.py   |      0
 .../modules_avant/core/filesystem/deploy_docs.sh   |      0
 .../core/filesystem/deploy_dynamic_monitoring.sh   |     99 -
 .../core/filesystem/deploy_paninifs.sh             |      0
 .../core/filesystem/deploy_paninifs_simple.sh      |      0
 .../core/filesystem/dhatu_detector.py              |      0
 .../modules_avant/core/filesystem/docs/.keep       |      1 -
 .../filesystem/docs/OPERATIONS/DevOps/roadmap.md   |      5 -
 .../core/filesystem/docs/avancement.md             |     15 -
 .../core/filesystem/docs/dashboard.md              |    205 -
 .../core/filesystem/docs/data/dhatu_child_langs.md |     25 -
 .../docs/data/dhatu_child_phenomena_summary.md     |     25 -
 .../core/filesystem/docs/data/system_status.json   |    127 -
 .../core/filesystem/docs/dhatu-framework.md        |     13 -
 .../modules_avant/core/filesystem/docs/diagrams.md |     26 -
 .../core/filesystem/docs/doc-process.md            |      9 -
 .../core/filesystem/docs/ecosystem/README.md       |     26 -
 .../core/filesystem/docs/ecosystem/catalogue.md    |      5 -
 .../core/filesystem/docs/ecosystem/ontowave.md     |     55 -
 .../core/filesystem/docs/ecosystem/panorama.md     |      5 -
 .../docs/ecosystem/repos/attribution-registry.md   |     10 -
 .../docs/ecosystem/repos/autonomous-missions.md    |     10 -
 .../docs/ecosystem/repos/copilotage-shared.md      |     10 -
 .../docs/ecosystem/repos/datasets-ingestion.md     |     10 -
 .../docs/ecosystem/repos/execution-orchestrator.md |     10 -
 .../docs/ecosystem/repos/ontowave-app.md           |     10 -
 .../docs/ecosystem/repos/publication-engine.md     |     10 -
 .../filesystem/docs/ecosystem/repos/research.md    |     10 -
 .../core/filesystem/docs/ecosystem/repos/root.md   |     10 -
 .../docs/ecosystem/repos/semantic-core.md          |     10 -
 .../docs/ecosystem/repos/ultra-reactive.md         |     10 -
 .../docs/en/OPERATIONS/DevOps/roadmap.md           |      5 -
 .../core/filesystem/docs/en/avancement.md          |     15 -
 .../core/filesystem/docs/en/dhatu-framework.md     |     13 -
 .../core/filesystem/docs/en/diagrams.md            |     26 -
 .../core/filesystem/docs/en/doc-process.md         |      7 -
 .../core/filesystem/docs/en/ecosystem/ontowave.md  |     55 -
 .../modules_avant/core/filesystem/docs/en/index.md |     43 -
 .../core/filesystem/docs/en/infrastructure.md      |      0
 .../core/filesystem/docs/en/licences.md            |      7 -
 .../filesystem/docs/en/linguistic-foundations.md   |      7 -
 .../filesystem/docs/en/livre/lecture-integrale.md  |      9 -
 .../core/filesystem/docs/en/modules/index.md       |     10 -
 .../core/filesystem/docs/en/monitoring-guide.md    |      3 -
 .../core/filesystem/docs/en/monitoring.md          |      0
 .../docs/en/operations/devops/roadmap.md           |      9 -
 .../core/filesystem/docs/en/progress.md            |     15 -
 .../core/filesystem/docs/en/publications.md        |     27 -
 .../core/filesystem/docs/en/references.md          |      7 -
 .../docs/en/research/cloud-free-compute.md         |      5 -
 .../docs/en/research/compression-semantique.md     |      7 -
 .../docs/en/research/dhatu-inventory-v0-1.md       |     50 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    129 -
 .../docs/en/research/human-language-development.md |     70 -
 .../en/research/hypotheses-and-alternatives.md     |      5 -
 .../core/filesystem/docs/en/research/index.md      |      7 -
 .../docs/en/research/inventaire-dhatu-v0-1.md      |      7 -
 .../en/research/langage-humain-developpement.md    |      7 -
 .../core/filesystem/docs/en/research/overview.md   |     29 -
 .../core/filesystem/docs/en/research/references.md |     57 -
 .../docs/en/research/semantic-compression.md       |     47 -
 .../docs/en/research/semantic-universals.md        |     57 -
 .../docs/en/research/universaux-semantique.md      |      9 -
 .../core/filesystem/docs/en/research/whats-new.md  |     21 -
 .../core/filesystem/docs/en/style-guide.md         |      6 -
 .../core/filesystem/docs/en/vision-social.md       |     11 -
 .../core/filesystem/docs/en/vision-sociale.md      |     11 -
 .../core/filesystem/docs/en/vision.md              |      9 -
 .../modules_avant/core/filesystem/docs/index.md    |     45 -
 .../core/filesystem/docs/infrastructure.md         |      0
 .../modules_avant/core/filesystem/docs/licences.md |      7 -
 .../core/filesystem/docs/linguistic-foundations.md |      7 -
 .../core/filesystem/docs/livre/index.md            |     25 -
 .../filesystem/docs/livre/lecture-integrale.md     |      7 -
 .../core/filesystem/docs/modules/_ext/.gitignore   |      4 -
 .../core/filesystem/docs/modules/index.md          |     19 -
 .../core/filesystem/docs/monitoring-guide.md       |    188 -
 .../core/filesystem/docs/monitoring.md             |      0
 .../filesystem/docs/operations/devops/roadmap.md   |      9 -
 .../core/filesystem/docs/publications.md           |     23 -
 .../core/filesystem/docs/references.md             |      7 -
 .../core/filesystem/docs/requirements.txt          |     13 -
 .../filesystem/docs/research/cloud-free-compute.md |      7 -
 .../docs/research/compression-semantique.md        |     52 -
 .../docs/research/dhatu-inventory-v0-1.md          |      6 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    141 -
 .../docs/research/human-language-development.md    |      5 -
 .../docs/research/hypotheses-and-alternatives.md   |     42 -
 .../core/filesystem/docs/research/index.md         |     13 -
 .../docs/research/inventaire-dhatu-v0-1.md         |     51 -
 .../docs/research/langage-humain-developpement.md  |     63 -
 .../core/filesystem/docs/research/overview.md      |     29 -
 .../core/filesystem/docs/research/references.md    |     57 -
 .../docs/research/semantic-compression.md          |      5 -
 .../docs/research/semantic-universals.md           |      5 -
 .../docs/research/universaux-semantique.md         |    164 -
 .../filesystem/docs/research/whats-new-feed.html   |     41 -
 .../core/filesystem/docs/research/whats-new.html   |     41 -
 .../core/filesystem/docs/research/whats-new.md     |     21 -
 .../core/filesystem/docs/style-guide.md            |      6 -
 .../core/filesystem/docs/vision-sociale.md         |     11 -
 .../modules_avant/core/filesystem/docs/vision.md   |      9 -
 .../modules_avant/core/filesystem/doctor.pid       |      1 -
 .../core/filesystem/doctor_control.py              |      0
 .../core/filesystem/doctor_dashboard.py            |      0
 .../core/filesystem/doctor_watchdog.sh             |     10 -
 .../core/filesystem/domain_monitoring_report.json  |     59 -
 .../modules_avant/core/filesystem/e2e/package.json |     15 -
 .../core/filesystem/e2e/playwright.config.js       |     13 -
 .../core/filesystem/e2e/tests/modules.spec.js      |     44 -
 .../core/filesystem/e2e/tests/research.spec.js     |     19 -
 .../core/filesystem/e2e/tests/smoke.spec.js        |     14 -
 .../experiments/dhatu/gold_encodings.json          |     14 -
 .../experiments/dhatu/gold_encodings_child.json    |     22 -
 .../experiments/dhatu/inventory_v0_1.json          |     41 -
 .../experiments/dhatu/prompts_child/arb.json       |     15 -
 .../experiments/dhatu/prompts_child/cmn.json       |     15 -
 .../experiments/dhatu/prompts_child/deu.json       |     15 -
 .../experiments/dhatu/prompts_child/en.json        |     15 -
 .../experiments/dhatu/prompts_child/eus.json       |     15 -
 .../experiments/dhatu/prompts_child/ewe.json       |     15 -
 .../experiments/dhatu/prompts_child/fr.json        |     15 -
 .../experiments/dhatu/prompts_child/hau.json       |     15 -
 .../experiments/dhatu/prompts_child/heb.json       |     15 -
 .../experiments/dhatu/prompts_child/hin.json       |     15 -
 .../experiments/dhatu/prompts_child/hun.json       |     14 -
 .../experiments/dhatu/prompts_child/iku.json       |     15 -
 .../experiments/dhatu/prompts_child/jpn.json       |     15 -
 .../experiments/dhatu/prompts_child/kor.json       |     15 -
 .../experiments/dhatu/prompts_child/nld.json       |     15 -
 .../experiments/dhatu/prompts_child/schema.json    |     22 -
 .../experiments/dhatu/prompts_child/spa.json       |     15 -
 .../experiments/dhatu/prompts_child/swa.json       |     15 -
 .../experiments/dhatu/prompts_child/tur.json       |     15 -
 .../experiments/dhatu/prompts_child/yor.json       |     15 -
 .../experiments/dhatu/prompts_child/zul.json       |     15 -
 .../core/filesystem/experiments/dhatu/report.py    |    113 -
 .../filesystem/experiments/dhatu/toy_corpus.json   |     16 -
 .../experiments/dhatu/typological_sample.json      |    216 -
 .../core/filesystem/experiments/dhatu/validator.py |    155 -
 .../core/filesystem/firebase_notifications.py      |      0
 .../core/filesystem/fix_google_oauth.sh            |      0
 .../modules_avant/core/filesystem/fix_remotes.sh   |    299 -
 .../core/filesystem/gdrive_credentials/README.md   |      0
 .../gdrive_credentials/credentials.json.template   |      0
 .../modules_avant/core/filesystem/git_audit.sh     |      0
 .../core/filesystem/github_workflow_doctor.py      |      0
 .../filesystem/github_workflow_emergency_doctor.py |      0
 .../governance/AUTONOMIE_VALIDATION_FINALE.md      |      3 -
 .../filesystem/governance/CONVENTIONS_NAMING.md    |     22 -
 .../governance/SESSION_BILAN_ORGANISATION.md       |      3 -
 .../audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md    |      5 -
 .../audits/AUDIT_SYNCHRONISATION_GITHUB.md         |      3 -
 .../CENTRALISATION_DISCUSSIONS_COPILOTAGE.md       |      3 -
 .../filesystem/governance/copilotage/POLICY.md     |     27 -
 .../filesystem/governance/copilotage/README.md     |     48 -
 .../copilotage/README_COPILOTAGE_HISTORIQUE.md     |     45 -
 .../governance/copilotage/journal/INDEX.md         |      3 -
 .../copilotage/knowledge/ESSENCE_PANINIFS.md       |     39 -
 .../modules_avant/core/filesystem/index.html       |      0
 .../filesystem/lancement_publications_20250820.sh  |      0
 .../core/filesystem/last_domain_status.json        |     59 -
 .../core/filesystem/launch_autonomous_doctor.sh    |      0
 .../filesystem/launch_continuous_improvement.sh    |      0
 .../core/filesystem/launch_hybrid_dashboard.sh     |     39 -
 .../core/filesystem/mini_test_dhatu.py             |      0
 .../modules_avant/core/filesystem/mkdocs.yml       |    182 -
 .../modules_avant/core/filesystem/mkdocs_fixed.yml |      0
 .../attribution-registry/.github/workflows/ci.yml  |     11 -
 .../modules/attribution-registry/LICENSE           |      1 -
 .../modules/attribution-registry/README.md         |      1 -
 .../modules/attribution-registry/pyproject.toml    |      4 -
 .../autonomous-missions/.github/workflows/ci.yml   |     18 -
 .../modules/autonomous-missions/.gitignore         |    207 -
 .../filesystem/modules/autonomous-missions/LICENSE |     21 -
 .../modules/autonomous-missions/README.md          |      4 -
 .../modules/cloud-orchestrator/README.md           |      0
 .../filesystem/modules/colab-controller/README.md  |      0
 .../datasets-ingestion/.github/workflows/ci.yml    |     11 -
 .../filesystem/modules/datasets-ingestion/LICENSE  |      1 -
 .../modules/datasets-ingestion/README.md           |      1 -
 .../modules/datasets-ingestion/pyproject.toml      |      4 -
 .../.github/workflows/ci.yml                       |     22 -
 .../modules/execution-orchestrator/.gitignore      |      7 -
 .../modules/execution-orchestrator/LICENSE         |      1 -
 .../modules/execution-orchestrator/README.md       |     20 -
 .../modules/execution-orchestrator/pyproject.toml  |     17 -
 .../src/execution_orchestrator/cli.py              |     31 -
 .../src/execution_orchestrator/drivers/__init__.py |     18 -
 .../src/execution_orchestrator/drivers/cloud.py    |      5 -
 .../drivers/cloud/.github/workflows/ci.yml         |     18 -
 .../drivers/cloud/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/cloud/LICENSE   |     21 -
 .../execution_orchestrator/drivers/cloud/README.md |      4 -
 .../src/execution_orchestrator/drivers/colab.py    |      5 -
 .../drivers/colab/.github/workflows/ci.yml         |     18 -
 .../drivers/colab/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/colab/LICENSE   |     21 -
 .../execution_orchestrator/drivers/colab/README.md |      4 -
 .../src/execution_orchestrator/drivers/local.py    |      5 -
 .../filesystem/modules/ontowave-app/.eslintrc.cjs  |     16 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     16 -
 .../.github/ISSUE_TEMPLATE/feature_request.md      |     13 -
 .../ontowave-app/.github/pull_request_template.md  |     12 -
 .../modules/ontowave-app/.github/workflows/ci.yml  |     34 -
 .../ontowave-app/.github/workflows/pr-preview.yml  |     27 -
 .../filesystem/modules/ontowave-app/.gitignore     |      6 -
 .../modules/ontowave-app/.prettierignore           |      2 -
 .../filesystem/modules/ontowave-app/.prettierrc    |      5 -
 .../core/filesystem/modules/ontowave-app/LICENSE   |     21 -
 .../core/filesystem/modules/ontowave-app/README.md |     39 -
 .../modules/ontowave-app/content/index.md          |     16 -
 .../modules/ontowave-app/copilotage/README.md      |      7 -
 .../modules/ontowave-app/copilotage/RULES.md       |      8 -
 .../ontowave-app/copilotage/preferences.json       |      8 -
 .../ontowave-app/copilotage/preferences.yml        |     21 -
 .../ontowave-app/copilotage/scripts/prepare_pr.sh  |     27 -
 .../filesystem/modules/ontowave-app/index.html     |     35 -
 .../modules/ontowave-app/package-lock.json         |   2426 -
 .../filesystem/modules/ontowave-app/package.json   |     39 -
 .../modules/ontowave-app/public/config.json        |      5 -
 .../ontowave-app/scripts/check_principles.sh       |     13 -
 .../filesystem/modules/ontowave-app/src/main.ts    |     53 -
 .../modules/ontowave-app/src/markdown.ts           |     51 -
 .../filesystem/modules/ontowave-app/src/router.ts  |     28 -
 .../filesystem/modules/ontowave-app/src/shims.d.ts |      3 -
 .../modules/ontowave-app/tools/build-sitemap.mjs   |     47 -
 .../filesystem/modules/ontowave-app/tsconfig.json  |     16 -
 .../filesystem/modules/ontowave-app/vite.config.ts |      6 -
 .../publication-engine/.github/workflows/ci.yml    |     18 -
 .../modules/publication-engine/.gitignore          |    207 -
 .../filesystem/modules/publication-engine/LICENSE  |     21 -
 .../modules/publication-engine/README.md           |      2 -
 .../modules/semantic-core/.github/workflows/ci.yml |     18 -
 .../filesystem/modules/semantic-core/.gitignore    |    207 -
 .../core/filesystem/modules/semantic-core/LICENSE  |     21 -
 .../filesystem/modules/semantic-core/README.md     |      2 -
 .../ultra-reactive/.github/workflows/ci.yml        |     18 -
 .../filesystem/modules/ultra-reactive/.gitignore   |    207 -
 .../core/filesystem/modules/ultra-reactive/LICENSE |     21 -
 .../filesystem/modules/ultra-reactive/README.md    |      4 -
 .../core/filesystem/monitor_domains.py             |      0
 .../filesystem/nocturnal_autonomous_mission.py     |      0
 .../core/filesystem/nocturnal_mission_log.json     |     64 -
 .../core/filesystem/notification_system.py         |      0
 .../filesystem/prepare_total_externalization.sh    |    186 -
 .../modules_avant/core/filesystem/publish_docs.sh  |      0
 .../modules_avant/core/filesystem/quick_monitor.sh |     48 -
 .../filesystem/remarkable_study_pack/README.md     |      0
 .../reading_guides/workflow_revision_remarkable.md |      0
 .../scientific_articles/bibliographie_complete.md  |      0
 .../content_addressing_avance.md                   |      0
 .../scientific_articles/etat_art_avance.md         |      0
 .../scientific_articles/etudes_cas_exercices.md    |      0
 .../scientific_articles/fondements_theoriques.md   |      0
 .../ipfs_vs_paninifs_analysis.md                   |      0
 .../modules_avant/core/filesystem/requirements.txt |     15 -
 .../core/filesystem/restructure_ecosystem.sh       |      0
 .../filesystem/scripts/aggregate_submodule_docs.py |     59 -
 .../filesystem/scripts/analyze_submodule_issue.py  |    259 -
 .../filesystem/scripts/apply_cleanup_manifest.sh   |     27 -
 .../core/filesystem/scripts/auto_pilot_research.py |    159 -
 .../scripts/check_copilotage_independence.py       |     90 -
 .../scripts/detect_module_specific_content.py      |     91 -
 .../filesystem/scripts/devops/audit_submodules.sh  |     53 -
 .../scripts/devops/generate_modules_index.py       |     68 -
 .../scripts/devops/monitor_prs_playwright.py       |     99 -
 .../filesystem/scripts/devops/pr_auto_doctor.sh    |    202 -
 .../filesystem/scripts/devops/repo_ci_snapshot.sh  |      0
 .../scripts/devops/terminal_diagnostics.sh         |      0
 .../scripts/devops/vscode_settings_tuner.py        |    149 -
 .../filesystem/scripts/enforce_lowercase_paths.py  |     90 -
 .../filesystem/scripts/generate_ecosystem_docs.py  |    201 -
 .../scripts/generate_modules_docs_index.py         |    111 -
 .../filesystem/scripts/generate_research_rss.py    |    102 -
 .../core/filesystem/scripts/noninteractive_env.sh  |     11 -
 .../filesystem/scripts/open_submodule_issues.py    |    104 -
 .../filesystem/scripts/open_submodule_issues_gh.py |     79 -
 .../core/filesystem/scripts/prepare_issue_packs.py |    121 -
 .../filesystem/scripts/setup_labels_submodules.sh  |     28 -
 .../core/filesystem/scripts/split_to_submodule.sh  |     48 -
 .../core/filesystem/scripts/triage_submodules.py   |    177 -
 .../modules_avant/core/filesystem/setup_domains.sh |      0
 .../core/filesystem/setup_github_labels.sh         |     58 -
 .../core/filesystem/setup_github_pages.sh          |      0
 .../core/filesystem/setup_mvp_dataset.sh           |      0
 .../core/filesystem/shutdown_totoro_procedure.sh   |      0
 .../core/filesystem/sync_paninifs_ecosystem.sh     |      0
 .../filesystem/templates_publication_reseaux.md    |      0
 .../core/filesystem/vacation_backup.sh             |     24 -
 .../core/filesystem/vacation_emergency_monitor.sh  |     44 -
 .../core/filesystem/vacation_productive_system.py  |      0
 .../core/filesystem/vacation_productive_work.json  |    222 -
 .../core/filesystem/validate_dhatu.sh              |      0
 .../core/filesystem/workflow_repair_report.json    |     36 -
 .../.github/DIRECTIVE_APPROBATIONS_COMMANDES.md    |    347 -
 .../DIRECTIVE_CONSOLIDATION_SERVEUR_UNIVERSEL.md   |    358 -
 .../ISSUE_TEMPLATE/spec-kit-pilot-migration.md     |    304 -
 .../research_backup/.github/README.md              |    422 -
 .../.github/copilot-approved-scripts.json          |    667 -
 .../.github/prompts/analyze.prompt.md              |    101 -
 .../.github/prompts/clarify.prompt.md              |    158 -
 .../.github/prompts/constitution.prompt.md         |     73 -
 .../.github/prompts/implement.prompt.md            |     56 -
 .../research_backup/.github/prompts/plan.prompt.md |     43 -
 .../.github/prompts/specify.prompt.md              |     21 -
 .../.github/prompts/tasks.prompt.md                |     62 -
 .../reports/server_audit_20251003_220914.json      |    462 -
 .../reports/system_status_20251003_215739.json     |     56 -
 .../.github/scripts/approval_monitor.py            |    348 -
 .../.github/scripts/system_initializer.py          |    384 -
 .../.github/scripts/validate_command.py            |    307 -
 .../.github/scripts/weekly_optimization_cron.sh    |     19 -
 .../.github/scripts/weekly_optimizer.py            |    372 -
 .../research_backup/.github/workflows/pages.yml    |     37 -
 .../research_backup/ANALYSE_ENRICHIE_COMPLETE.md   |    129 -
 .../research_backup/AUDIT_COMPREHENSION_MISSION.md |     85 -
 ...CKLOG_ARCHIVED_PROJECTS_2025-10-01T15-42-06Z.md |    298 -
 ...CKLOG_REACTIVATION_PLAN_2025-10-01T16-45-19Z.md |    199 -
 ...CKLOG_REACTIVATION_PLAN_2025-10-01T16-45-25Z.md |    199 -
 .../CLARIFICATIONS_MISSION_CRITIQUE.md             |    178 -
 .../COMMENTAIRES_PRS_CLARIFICATIONS.md             |    340 -
 .../research_backup/COMPRESSOR_ARCHITECTURE_v1.md  |    867 -
 .../COMPRESSOR_ARCHITECTURE_v1_ADDENDUM.md         |    881 -
 .../research_backup/CONTINUE_DEV_INTEGRATION.md    |     57 -
 .../CONTRAINTES_COMPATIBILITE_APPLICATIONS.md      |    110 -
 .../COPILOTAGE_DATES_ISO_APPLIQUE.md               |    100 -
 .../COPILOTAGE_DATES_ISO_VALIDATION_FINALE.md      |     71 -
 .../research_backup/CORE_EXECUTION_PLAN.md         |    304 -
 .../research_backup/CORRECTIONS_LAYOUT_UHD.md      |    132 -
 .../research_backup/CORRECTION_JS_CHARGEMENT.md    |    144 -
 .../DASHBOARD_ENRICHI_MODELE_EBAUCHES.md           |    123 -
 .../DASHBOARD_TRANSFORME_ACTIVITE.md               |    140 -
 .../research_backup/DEMONSTRATION_UHD_COMPLETE.md  |    223 -
 .../research_backup/EBAUCHES_PANINI_EN_COURS.md    |    179 -
 .../GITHUB_COPILOT_CODING_AGENT_SETUP.md           |    107 -
 .../GITHUB_PAGES_DASHBOARD_GUIDE.md                |    357 -
 .../research_backup/GITHUB_PROJECT_FINAL_REPORT.md |    217 -
 .../GITHUB_PROJECT_ISSUES_STRATEGIQUES.md          |    221 -
 .../research_backup/GITHUB_PROJECT_LANCE.md        |    102 -
 .../GUIDE_LECTEUR_VIRTUEL_SITE_EXPLORATION.md      |    142 -
 .../GUIDE_PRATIQUE_ZERO_APPROBATIONS.md            |    353 -
 ...L_ARCHITECTURE_ANALYSIS_2025-10-03T15-02-38Z.md |    107 -
 ...RCHICAL_TESTS_RESULTS_2025-10-03T15-10-44Z.json |    585 -
 .../research_backup/ISSUE11_COMPLETED_SUMMARY.md   |    153 -
 ...NAL_VALIDATION_REPORT_2025-10-02T22-15-33Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-02T22-17-33Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-03T12-25-07Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-03T13-46-19Z.json |     64 -
 ...ISSUE_OPTIMISATION_CONNIVENCES_NON_DECLAREES.md |    159 -
 .../JOURNAL_SESSION_COMPRESSEUR_MVP_2025-10-01.md  |    565 -
 .../MIGRATION_COPILOTAGE_TO_SPEC_KIT.md            |    545 -
 .../research_backup/MIGRATION_EXECUTIVE_SUMMARY.md |    112 -
 .../research_backup/MISSION_ACCOMPLIE_UHD.md       |    169 -
 .../research_backup/MISSION_ACCOMPLISHED.md        |    149 -
 .../research_backup/MISSION_DASHBOARD_ACCOMPLIE.md |     59 -
 .../MULTI_AGENT_COLLABORATION_GUIDE.md             |    458 -
 .../PANINI_ECOSYSTEM_ORCHESTRATOR_GUIDE.md         |    474 -
 ...TIVE_SIZE_SUMMARY_2025-10-03T11-54-57.043799.md |     48 -
 ...AT_ENCYCLOPEDIA_2025-10-03T10-42-28.536994.json |    974 -
 .../PANINI_GIT_MULTI_REPOS_ACHIEVEMENT.md          |    140 -
 ..._STRUCTURE_REPORT_2025-10-03T12-01-28.959164.md |     60 -
 ...ON_ENCYCLOPEDIA_2025-10-03T10-58-57.908785.json |    988 -
 ...TIMIZATION_REPORT_2025-10-03T10-58-57.908785.md |     71 -
 ...E_ANALYSIS_DATA_2025-10-03T11-53-12.188496.json |    810 -
 ...E_ANALYSIS_REPORT_2025-10-03T11-53-12.188496.md |     65 -
 .../PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md     |    519 -
 .../PANINI_VFS_ACHIEVEMENT_SUMMARY.md              |     91 -
 .../research_backup/PHASE1_COLAB_INSTRUCTIONS.md   |     60 -
 .../research_backup/PHASE1_HUMAN_TASK_GUIDE.md     |    165 -
 .../research_backup/PHASE1_MONITORING_GUIDE.md     |    309 -
 .../PILOT_REPORT_PANINI_ONTOWAVE.md                |    502 -
 .../POINTS_CLES_MISSION_OFFICIEL.md                |     65 -
 .../RAPPORT_ANALYSE_TRADUCTEURS_2025-10-01.md      |    268 -
 .../RAPPORT_MISSION_ANALYSEURS_SEMANTIQUES.md      |    194 -
 .../research_backup/RAPPORT_SESSION_2025-09-30.md  |    260 -
 .../research_backup/RAPPORT_SESSION_AUTONOME.md    |    736 -
 .../research_backup/README_AUTONOMOUS_APPROVALS.md |    299 -
 .../research_backup/README_MISSION_PANINI.md       |    119 -
 .../REPONSE_HIERARCHIE_EXCLUSIVE_CONFIRMEE.md      |    119 -
 .../RESOLUTION_AFFICHAGE_CONTENU.md                |     64 -
 .../RESOLUTION_DEFINITIVE_CORPUS.md                |    118 -
 .../research_backup/RESUME_EXECUTIF_PANINI.md      |    100 -
 .../SESSION_COMPLETE_SYNTHESE_EXECUTIVE.md         |    451 -
 .../research_backup/SESSION_SUMMARY_20251003.md    |    394 -
 .../SOLUTION_APPROBATION_COMMANDES_AUTONOMES.md    |    496 -
 .../research_backup/SPEC_KIT_INTEGRATION.md        |    271 -
 .../STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md       |    288 -
 .../research_backup/STRATEGIC_REFACTORING_PLAN.md  |    297 -
 .../STRATEGIE_AGENTS_UNIVERSAUX_SEMANTIQUES.md     |    143 -
 .../STRATEGIE_RAFFINEE_PLAN_TRAVAIL.md             |    236 -
 .../SYNTHESE_CLARIFICATIONS_INTEGREES.md           |    330 -
 .../VALIDATION_SYSTEM_HIERARCHIQUE_CORPUS_REEL.md  |    136 -
 .../research_backup/VUE_MODELE_PANINI_COMPLET.md   |    156 -
 .../research_backup/activity_dashboard_data.json   |      6 -
 ...anced_reconstruction_validation_1759520023.json |    154 -
 .../api_documentation_compressed.json              |    158 -
 .../research_backup/audit_server_consolidation.py  |    299 -
 .../research_backup/auto_update_dashboard.sh       |     39 -
 ...acklog_review_results_2025-10-01T16-45-19Z.json |    591 -
 ...acklog_review_results_2025-10-01T16-45-25Z.json |    591 -
 .../research_backup/compression_benchmarks.json    |    487 -
 .../compression_validation_results.json            |    258 -
 ...otage_date_compliance_2025-09-29T20-22-03Z.json | 445048 -----------------
 ...otage_date_compliance_2025-09-29T20-22-13Z.json | 445056 -----------------
 ...otage_date_compliance_2025-09-29T20-28-19Z.json | 445096 ------------------
 .../copilotage_date_iso_standard.json              |    219 -
 .../dashboard_activity_focused.html                |    566 -
 .../research_backup/dashboard_data.json            |    138 -
 .../research_backup/dashboard_real_data.json       |     41 -
 .../research_backup/dashboard_real_panini.html     |    687 -
 .../research_backup/dashboard_web_semantic.html    |    745 -
 .../research_backup/demo_analyse_enrichie.html     |    334 -
 .../demo_decomposition_detaillee.html              |    799 -
 .../research_backup/deploy_phase1_dashboard.sh     |     97 -
 .../research_backup/extracted_content.json         |    279 -
 .../research_backup/index.html                     |    438 -
 .../interface_decomposition_complete.html          |    711 -
 ...601_compliance_report_2025-10-01T13-39-40Z.json |    124 -
 ...antic_atoms_discovery_2025-10-03T00-39-54Z.json |    343 -
 ...antic_atoms_discovery_2025-10-03T12-24-46Z.json |    343 -
 ...antic_atoms_discovery_2025-10-03T14-10-46Z.json |    343 -
 .../research_backup/launch_advanced_demo.sh        |     67 -
 ...sion_alignment_report_2025-10-01T15-25-43Z.json |    168 -
 ...sion_alignment_report_2025-10-01T15-48-06Z.json |    168 -
 .../research_backup/multilingual_embeddings.json   |    795 -
 .../orchestrator_state_2025-10-01T14-25-27Z.json   |    242 -
 .../research_backup/panini_advanced_uhd_clean.py   |    822 -
 .../panini_advanced_uhd_reconstructor.py           |   1190 -
 .../research_backup/panini_binary_decomposer.py    |    792 -
 .../research_backup/panini_clean_final.py          |    570 -
 .../research_backup/panini_demo_data_generator.py  |    288 -
 .../panini_deployment_guide_20251003_135653.md     |    110 -
 .../panini_detailed_size_analyzer.py               |    492 -
 .../research_backup/panini_duplicate_analyzer.py   |    482 -
 .../panini_ecosystem_orchestrator.py               |    524 -
 ...anini_ecosystem_state_2025-10-01T14-55-21Z.json |    580 -
 ...anini_ecosystem_state_2025-10-01T15-48-50Z.json |    734 -
 .../panini_format_discovery_engine.py              |    591 -
 .../research_backup/panini_full_stack_digesteur.py |    445 -
 .../panini_git_repo_architecture.py                |    868 -
 .../panini_hierarchical_architecture.py            |    527 -
 .../panini_internal_structure_analyzer.py          |    800 -
 .../panini_issue11_final_validator.py              |    379 -
 .../panini_issue12_separation_analyzer.py          |    873 -
 .../panini_issue13_semantic_atoms.py               |    831 -
 .../panini_issue14_dashboard_realtime.py           |    804 -
 .../panini_optimization_discovery_engine.py        |    725 -
 .../research_backup/panini_performance_analyzer.py |    535 -
 .../research_backup/panini_real_data.json          |     27 -
 .../research_backup/panini_repos_status_viewer.py  |    397 -
 .../research_backup/panini_serveur_corrige.py      |    193 -
 .../research_backup/panini_simple_server.py        |    538 -
 .../research_backup/panini_size_analysis_engine.py |    620 -
 .../panini_test_corpus_generator.py                |    468 -
 .../research_backup/panini_uhd_interface.py        |    963 -
 .../panini_universal_batch_20251003_135646.json    |    312 -
 .../panini_universal_format_engine.py              |    577 -
 ...ini_validation_report_2025-10-02T22-12-15Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-15-33Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-17-18Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-17-32Z.json |    615 -
 ...ini_validation_report_2025-10-03T12-24-32Z.json |    615 -
 ...ini_validation_report_2025-10-03T12-25-06Z.json |    615 -
 ...ini_validation_report_2025-10-03T13-30-03Z.json |    615 -
 ...ini_validation_report_2025-10-03T13-46-19Z.json |    615 -
 ...ini_validation_report_2025-10-03T14-10-46Z.json |    615 -
 .../research_backup/panini_validators_core.py      |    772 -
 .../panini_vfs_architecture_20251003_135649.json   |    666 -
 .../panini_virtual_fs_architecture.py              |    594 -
 .../research_backup/panini_web_backend.py          |    278 -
 .../panini_web_explorer_prototype.html             |    375 -
 .../panini_web_frontend_specs_20251003_135653.json |    118 -
 .../panini_web_interface_generator.py              |    963 -
 .../research_backup/panini_webdav_server.py        |    300 -
 .../research_backup/phase1_progress_report.json    |    818 -
 .../research_backup/phase1_session_log.json        |     17 -
 .../playwright_diagnostic_1759520886.json          |     66 -
 .../research_backup/pr11_comment.md                |     51 -
 .../research_backup/pr13_comment.md                |     87 -
 .../research_backup/pr14_comment.md                |     97 -
 .../research_backup/pr16_comment.md                |     57 -
 .../pr_compliance_report_2025-10-01T13-51-28Z.json |     55 -
 .../pr_compliance_report_2025-10-01T14-03-48Z.json |    289 -
 ...ct_essence_extraction_2025-10-01T15-42-06Z.json |    911 -
 ...tic_dashboard_summary_2025-10-02T21-20-38Z.json |     32 -
 ...emantic_orchestration_2025-10-02T21-11-00Z.json |     13 -
 ...emantic_orchestration_2025-10-02T21-11-47Z.json |     80 -
 ...emantic_orchestration_2025-10-02T21-16-38Z.json |     87 -
 .../serveur_decomposition_complete.py              |    489 -
 .../research_backup/setup_panini_research_repo.sh  |    148 -
 .../research_backup/start_phase1_monitoring.sh     |     24 -
 .../symmetry_detection_real_panini_data.json       |    308 -
 .../symmetry_detection_results.json                |    131 -
 .../research_backup/training_metrics.json          |    131 -
 .../translator_bias_style_analysis.json            |    179 -
 .../translator_database_sample.json                |     76 -
 .../translator_metadata_extraction.json            |     13 -
 .../research_backup/translators_metadata.json      |    378 -
 .../txt_extraction_2025-10-01T13-02-45Z.json       |     58 -
 .../filesystem_backup/.cargo/config.toml           |      0
 .../.devcontainer/devcontainer.json                |     55 -
 .../filesystem_backup/.devcontainer/setup.sh       |     53 -
 .../filesystem_backup/.gitconfig.local             |     11 -
 .../.github/ISSUE_TEMPLATE/bug-report.md           |     56 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     29 -
 .../.github/ISSUE_TEMPLATE/bug_report.yml          |     80 -
 .../.github/ISSUE_TEMPLATE/config.yml              |      5 -
 .../.github/ISSUE_TEMPLATE/feature-request.md      |     74 -
 .../.github/ISSUE_TEMPLATE/feature_request.yml     |     71 -
 .../.github/ISSUE_TEMPLATE/research-task.md        |     54 -
 .../.github/ISSUE_TEMPLATE/research.md             |     19 -
 .../.github/ISSUE_TEMPLATE/submodule-change.yml    |     58 -
 .../.github/ISSUE_TEMPLATE/task.md                 |     24 -
 .../.github/PULL_REQUEST_TEMPLATE.md               |     26 -
 .../.github/ops/triggers/deploy-docs.txt           |      2 -
 .../.github/ops/triggers/pages-diagnostics.txt     |      2 -
 .../.github/pull_request_template.md               |      0
 .../.github/workflows/auto-merge-provenance.yml    |    100 -
 .../.github/workflows/camping-status.yml           |     29 -
 .../filesystem_backup/.github/workflows/codeql.yml |    108 -
 .../.github/workflows/copilotage-ci.yml            |     27 -
 .../.github/workflows/copilotage-journal-check.yml |     41 -
 .../.github/workflows/copilotage-journal-index.yml |     44 -
 .../.github/workflows/cross-check-visibility.yml   |     24 -
 .../.github/workflows/deploy-pages-mkdocs.yml      |    113 -
 .../.github/workflows/dhatu-validation.yml         |    187 -
 .../.github/workflows/docs-governance.yml          |    119 -
 .../.github/workflows/docs-pages.yml               |     48 -
 .../.github/workflows/e2e-playwright.yml           |     59 -
 .../.github/workflows/label-agent.yml              |    105 -
 .../.github/workflows/maintenance.yml              |     19 -
 .../.github/workflows/minimal-status.yml           |     10 -
 .../.github/workflows/owner-labeler.yml            |     77 -
 .../.github/workflows/pages-diagnostics.yml        |     46 -
 .../.github/workflows/pages-enforce-https.yml      |     51 -
 .../.github/workflows/paniniFS-ci.yml              |     16 -
 .../workflows/provenance-bootstrap-pr37.yml        |     39 -
 .../.github/workflows/provenance-guardian.yml      |    127 -
 .../.github/workflows/publications.yml             |     54 -
 .../.github/workflows/repo-guards.yml              |     22 -
 .../.github/workflows/secret-scan.yml              |     32 -
 .../.github/workflows/submodule-backfill.yml       |     43 -
 .../.github/workflows/submodule-triage.yml         |     71 -
 .../.github/workflows/update-modules-index.yml     |     38 -
 .../workflows/validate-agent-provenance.yml        |     43 -
 .../.github/workflows/validate-agent-session.yml   |     38 -
 .../workflows/validate-task-coordination.yml       |     55 -
 .../filesystem_backup/.gitignore                   |     41 -
 .../filesystem_backup/.gitmodules                  |     42 -
 .../filesystem_backup/.nojekyll                    |     10 -
 .../filesystem_backup/.panini-agent.toml           |      0
 .../filesystem_backup/CNAME                        |      1 -
 .../filesystem_backup/CONTRIBUTING.md              |     51 -
 .../filesystem_backup/COPILOTAGE_SHARED/README.md  |      9 -
 .../COPILOTAGE_SHARED/settings.json                |     11 -
 .../filesystem_backup/Cargo.toml                   |      0
 .../Copilotage/AGENT_CONVENTION.md                 |     19 -
 .../ARCHITECTURE_RESTRUCTURATION_PLAN.md           |     24 -
 .../Copilotage/COPILOTAGE_WORKFLOW.md              |     46 -
 .../filesystem_backup/Copilotage/DEPRECATED.md     |     10 -
 .../Copilotage/DEPRECATED_README.md                |      7 -
 .../filesystem_backup/Copilotage/README.md         |     46 -
 .../Copilotage/TODO_RELAIS_2025-09-02.md           |     12 -
 .../Copilotage/agents/adversarial_critic_agent.py  |      0
 .../Copilotage/agents/orchestrator_with_github.py  |      0
 .../Copilotage/agents/requirements.txt             |     10 -
 .../agents/simple_autonomous_orchestrator.py       |      0
 .../Copilotage/agents/tests/test_agents.py         |     45 -
 .../agents/theoretical_research_agent.py           |      0
 .../Copilotage/coordination-agent.py               |      0
 .../Copilotage/debug_notebook_local.ipynb          |      0
 .../Copilotage/demo-prototypage-rapide.md          |      0
 ...elargissement-horizon-mathematiques-physique.md |      0
 .../Copilotage/headless_autonomous_controller.py   |      0
 .../filesystem_backup/Copilotage/hyperscript-2.sh  |      0
 ...-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md |    339 -
 .../journal/2025-08-30-ci-stabilisation-merge.md   |     17 -
 .../journal/2025-08-30-hauru-pid74498-session.md   |     30 -
 .../2025-08-30-linux-pid0-assimilation-archives.md |     30 -
 .../Copilotage/journal/2025-08-30-session.md       |     24 -
 .../2025-08-30-totoro-pid17771-camping-final.md    |     39 -
 .../journal/2025-09-01-totoro-pid389223-session.md |     46 -
 .../2025-09-01-totoro-pid390178-rattrapage.md      |     53 -
 .../filesystem_backup/Copilotage/journal/INDEX.md  |     14 -
 .../Copilotage/knowledge/ESSENCE_PANINIFS.md       |     37 -
 .../knowledge/HYPERNODAL_DB_AND_LATTICE.md         |     23 -
 .../MODULES_OVERVIEW_AND_PARENT_PROJECT.md         |     29 -
 .../PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md    |     22 -
 .../knowledge/SEMANTIC_UNIVERSALS_DHATU.md         |     39 -
 .../Copilotage/mission_autonome_exemplaire.py      |      0
 .../Copilotage/notes-vision-architecturale.md      |      0
 .../Copilotage/roadmap-decouverte.md               |      0
 .../Copilotage/roadmap-hybride-rd-production.md    |      0
 .../filesystem_backup/Copilotage/roadmap.md        |     16 -
 .../Copilotage/scripts/COLAB_SETUP_GUIDE.md        |      0
 .../filesystem_backup/Copilotage/scripts/README.md |     17 -
 .../scripts/advanced_consensus_engine.py           |      0
 .../Copilotage/scripts/analogy_collector.py        |      0
 .../Copilotage/scripts/analyze_preferences.py      |      0
 .../Copilotage/scripts/arxiv_collector.py          |      0
 .../Copilotage/scripts/autonomous_analyzer.py      |      0
 .../scripts/autonomous_gdrive_manager.py           |      0
 .../Copilotage/scripts/books_collector.py          |      0
 .../Copilotage/scripts/colab_api_strategy.py       |      0
 .../scripts/colab_autonomous_controller.py         |      0
 .../Copilotage/scripts/colab_cli_launcher.py       |      0
 .../Copilotage/scripts/colab_debug_environment.py  |      0
 .../Copilotage/scripts/collect_samples.py          |      0
 .../Copilotage/scripts/collect_with_attribution.py |      0
 .../Copilotage/scripts/complete_journey_summary.py |      0
 .../scripts/comprehensive_opensource_strategy.py   |      0
 .../scripts/connivance_learning_system.py          |      0
 .../Copilotage/scripts/consensus_analyzer.py       |      0
 .../scripts/continuous_autonomy_daemon.py          |      0
 .../Copilotage/scripts/debug_ultra_fast.py         |      0
 .../Copilotage/scripts/deep_cleanup_credentials.sh |      0
 .../Copilotage/scripts/deploy_colab_auto.sh        |      0
 .../Copilotage/scripts/deploy_colab_fixed.sh       |      0
 .../Copilotage/scripts/deploy_colab_secure.sh      |      0
 .../Copilotage/scripts/devops/README.md            |     23 -
 .../scripts/devops/bootstrap_submodules.sh         |     38 -
 .../Copilotage/scripts/devops/fix_remotes.sh       |    103 -
 .../Copilotage/scripts/devops/gh_pr_exempt.sh      |     25 -
 .../Copilotage/scripts/devops/gh_pr_open.sh        |     90 -
 .../Copilotage/scripts/devops/gh_queue.sh          |     67 -
 .../Copilotage/scripts/devops/gh_task_init.sh      |     49 -
 .../Copilotage/scripts/devops/git_audit.sh         |     35 -
 .../devops/init_execution_orchestrator_repo.sh     |     39 -
 .../Copilotage/scripts/devops/journal_index.sh     |     33 -
 .../Copilotage/scripts/devops/journal_session.sh   |     43 -
 .../scripts/devops/plan_migration_option_b.sh      |     39 -
 .../Copilotage/scripts/devops/run_safe.sh          |     18 -
 .../scripts/devops/setup_dev_environment.sh        |     26 -
 .../Copilotage/scripts/display_recommendations.py  |      0
 .../scripts/distribution_strategy_analyzer.py      |      0
 .../scripts/editorial/sync_publications.py         |    125 -
 .../Copilotage/scripts/emergency_plasma_fix.sh     |      0
 .../scripts/executive_summary_generator.py         |      0
 .../scripts/executive_totoro_recommendations.py    |      0
 .../Copilotage/scripts/externalization_strategy.py |      0
 .../Copilotage/scripts/final_security_check.sh     |      0
 .../Copilotage/scripts/fix_git_credentials.sh      |      0
 .../Copilotage/scripts/free_cloud_analysis.py      |      0
 .../scripts/generate_remarkable_bibliography.py    |      0
 .../scripts/generate_scientific_bibliography.py    |      0
 .../Copilotage/scripts/github_workflow_doctor.py   |      0
 .../Copilotage/scripts/github_workflow_monitor.py  |     38 -
 .../Copilotage/scripts/google_colab_setup.py       |      0
 .../Copilotage/scripts/gpu_analysis_gt630m.py      |      0
 .../scripts/hardware_integration_guide.py          |      0
 .../Copilotage/scripts/hauru_setup.sh              |      0
 .../scripts/headless_autonomy_auditor.py           |      0
 .../Copilotage/scripts/headless_env_loader.py      |     53 -
 .../Copilotage/scripts/headless_secrets_manager.py |      0
 .../Copilotage/scripts/immediate_launch_plan.py    |      0
 .../scripts/implementation_roadmap_generator.py    |      0
 .../scripts/information_theory_collector.py        |      0
 .../scripts/intelligent_communication_guide.py     |      0
 .../Copilotage/scripts/launch_cloud_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_direct.sh      |      0
 .../Copilotage/scripts/launch_optimized_colab.sh   |      0
 .../Copilotage/scripts/launch_simple.sh            |      0
 .../Copilotage/scripts/launch_total_autonomy.sh    |      0
 .../mathematics_physics_convergence_analyzer.py    |      0
 .../Copilotage/scripts/multi_source_analyzer.py    |      0
 .../scripts/neurocognitive_language_analyzer.py    |      0
 .../scripts/opensource_resources_analyzer.py       |      0
 .../scripts/optimal_language_synthesizer.py        |      0
 .../scripts/optimal_vocabulary_generator.py        |      0
 .../scripts/paniniFS_priority_strategy.py          |      0
 .../scripts/panini_analogical_extension.py         |      0
 .../scripts/panini_architectural_integrator.py     |      0
 .../Copilotage/scripts/panini_dashboard.py         |      0
 .../scripts/panini_fundamental_generator.py        |      0
 .../scripts/panini_linguistic_integrator.py        |      0
 .../Copilotage/scripts/panini_status_point.py      |      0
 .../scripts/pedagogical_applications_guide.py      |      0
 .../scripts/physics_mathematics_collector.py       |      0
 .../scripts/plasma_stabilizer_advanced.sh          |      0
 .../Copilotage/scripts/publication_generator.py    |      0
 .../Copilotage/scripts/realistic_gpu_assessment.py |      0
 .../Copilotage/scripts/requirements.txt            |     18 -
 .../Copilotage/scripts/run_analysis.sh             |      0
 .../Copilotage/scripts/rust_bridge.py              |      0
 .../Copilotage/scripts/safe_totoro_optimizer.py    |      0
 .../scripts/secure_cleanup_credentials.sh          |      0
 .../filesystem_backup/Copilotage/scripts/setup.py  |      0
 .../Copilotage/scripts/setup_cloud_autonomous.sh   |      0
 .../Copilotage/scripts/setup_gdrive_config.py      |      0
 .../scripts/social_revolution_strategy.py          |      0
 .../scripts/solid_foundation_strategy.py           |      0
 .../scripts/temporal_emergence_analyzer.py         |      0
 .../Copilotage/scripts/test_regression.sh          |      0
 .../Copilotage/scripts/test_workflow_complete.py   |      0
 .../Copilotage/scripts/tests/test_basic.py         |     41 -
 .../Copilotage/scripts/tests/test_monitor.py       |     12 -
 .../Copilotage/scripts/total_autonomy_engine.py    |      0
 .../scripts/totoro_liberation_toolkit.sh           |      0
 .../Copilotage/scripts/totoro_optimizer.py         |      0
 .../scripts/totoro_resource_management.py          |      0
 .../Copilotage/scripts/traceability_dashboard.py   |      0
 .../scripts/ultra_reactive_controller.py           |      0
 .../scripts/vscode_extensions_manager.py           |      0
 .../Copilotage/scripts/vscode_settings_fixer.py    |      0
 .../Copilotage/session-bilan-vision-realite.md     |      0
 .../filesystem_backup/Copilotage/setup-rust.md     |      0
 .../filesystem_backup/Copilotage/test-build.sh     |      0
 .../Copilotage/tracabilite-attribution.md          |     20 -
 .../filesystem_backup/LICENSE                      |     21 -
 .../Panini_Ecosystem_Coherence_Audit.ipynb         |      0
 .../filesystem_backup/README.en.md                 |      0
 .../filesystem_backup/README.md                    |    159 -
 .../cloud-processing/FREE_COMPUTE_STRATEGY.md      |    110 -
 .../BABY_SIGN_LANGUAGE_FOUNDATION.md               |      0
 .../dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md  |      0
 .../DHATU_ATOMES_CONCEPTUELS_REVISION.md           |      0
 .../filesystem_backup/RESEARCH/docs/README.md      |      6 -
 .../methodology/protocols/GUIDE_LEANPUB_ETAPE1.md  |      0
 .../methodology/protocols/GUIDE_MEDIUM_ETAPE3.md   |      0
 .../protocols/ORDRE_PUBLICATION_GUIDE.md           |      0
 .../protocols/PUBLICATION_COORDONNEE_20250820.md   |      0
 .../protocols/SYNCHRONISATION_MEDIUM_2025.md       |     83 -
 .../articles/ARTICLE_MEDIUM_FINAL_2025.md          |      0
 .../articles/ARTICLE_MEDIUM_FINAL_2025_EN.md       |      0
 .../articles/english/ARTICLE_MEDIUM_2025_EN.md     |    419 -
 .../articles/french/ARTICLE_MEDIUM_2025.md         |    408 -
 .../publications/books/LIVRE_LEANPUB_FINAL_2025.md |      0
 .../books/english/LIVRE_LEANPUB_2025_EN.md         |      0
 .../books/french/LIVRE_LEANPUB_2025.md             |    554 -
 .../filesystem_backup/activate_total_autonomy.sh   |      0
 .../filesystem_backup/analogy_detector_mvp.py      |      0
 .../filesystem_backup/android_template.java        |      0
 .../artifacts/playwright/pr-40-checks.png          |    Bin 274486 -> 0 bytes
 .../artifacts/playwright/pr-40-overview.png        |    Bin 693119 -> 0 bytes
 .../artifacts/playwright/pr-42-checks.png          |    Bin 179199 -> 0 bytes
 .../artifacts/playwright/pr-42-overview.png        |    Bin 711460 -> 0 bytes
 .../snapshots/snapshot-20250902-152737.txt         |     40 -
 .../filesystem_backup/autonomous_colab_tester.py   |      0
 .../filesystem_backup/autonomous_test_log.json     |     20 -
 .../autonomous_workflow_doctor.py                  |      0
 .../filesystem_backup/check_colab_mission.py       |      0
 .../filesystem_backup/check_deployment.sh          |      0
 .../filesystem_backup/check_dns.sh                 |      0
 .../filesystem_backup/cleanup/manifest.txt         |     92 -
 .../cloud_backup/autonomous_crontab_simple.txt     |      0
 .../filesystem_backup/configure_vacation_mode.sh   |      0
 .../filesystem_backup/copilotage/README.md         |      8 -
 .../filesystem_backup/copilotage/config.yml        |      8 -
 .../filesystem_backup/copilotage/shared/README.md  |      3 -
 .../filesystem_backup/copilotage/shared/config.yml |      1 -
 .../filesystem_backup/data/ecosystem.yml           |    121 -
 .../filesystem_backup/deploy_cloud_autonomous.py   |      0
 .../filesystem_backup/deploy_cloud_ecosystem.sh    |      0
 .../deploy_colab_deployment_center.py              |      0
 .../filesystem_backup/deploy_docs.sh               |      0
 .../filesystem_backup/deploy_dynamic_monitoring.sh |     99 -
 .../filesystem_backup/deploy_paninifs.sh           |      0
 .../filesystem_backup/deploy_paninifs_simple.sh    |      0
 .../filesystem_backup/dhatu_detector.py            |      0
 .../filesystem_backup/docs/.keep                   |      1 -
 .../docs/OPERATIONS/DevOps/roadmap.md              |      5 -
 .../filesystem_backup/docs/avancement.md           |     15 -
 .../filesystem_backup/docs/dashboard.md            |    205 -
 .../docs/data/dhatu_child_langs.md                 |     25 -
 .../docs/data/dhatu_child_phenomena_summary.md     |     25 -
 .../filesystem_backup/docs/data/system_status.json |    127 -
 .../filesystem_backup/docs/dhatu-framework.md      |     13 -
 .../filesystem_backup/docs/diagrams.md             |     26 -
 .../filesystem_backup/docs/doc-process.md          |      9 -
 .../filesystem_backup/docs/ecosystem/README.md     |     26 -
 .../filesystem_backup/docs/ecosystem/catalogue.md  |      5 -
 .../filesystem_backup/docs/ecosystem/ontowave.md   |     55 -
 .../filesystem_backup/docs/ecosystem/panorama.md   |      5 -
 .../docs/ecosystem/repos/attribution-registry.md   |     10 -
 .../docs/ecosystem/repos/autonomous-missions.md    |     10 -
 .../docs/ecosystem/repos/copilotage-shared.md      |     10 -
 .../docs/ecosystem/repos/datasets-ingestion.md     |     10 -
 .../docs/ecosystem/repos/execution-orchestrator.md |     10 -
 .../docs/ecosystem/repos/ontowave-app.md           |     10 -
 .../docs/ecosystem/repos/publication-engine.md     |     10 -
 .../docs/ecosystem/repos/research.md               |     10 -
 .../filesystem_backup/docs/ecosystem/repos/root.md |     10 -
 .../docs/ecosystem/repos/semantic-core.md          |     10 -
 .../docs/ecosystem/repos/ultra-reactive.md         |     10 -
 .../docs/en/OPERATIONS/DevOps/roadmap.md           |      5 -
 .../filesystem_backup/docs/en/avancement.md        |     15 -
 .../filesystem_backup/docs/en/dhatu-framework.md   |     13 -
 .../filesystem_backup/docs/en/diagrams.md          |     26 -
 .../filesystem_backup/docs/en/doc-process.md       |      7 -
 .../docs/en/ecosystem/ontowave.md                  |     55 -
 .../filesystem_backup/docs/en/index.md             |     43 -
 .../filesystem_backup/docs/en/infrastructure.md    |      0
 .../filesystem_backup/docs/en/licences.md          |      7 -
 .../docs/en/linguistic-foundations.md              |      7 -
 .../docs/en/livre/lecture-integrale.md             |      9 -
 .../filesystem_backup/docs/en/modules/index.md     |     10 -
 .../filesystem_backup/docs/en/monitoring-guide.md  |      3 -
 .../filesystem_backup/docs/en/monitoring.md        |      0
 .../docs/en/operations/devops/roadmap.md           |      9 -
 .../filesystem_backup/docs/en/progress.md          |     15 -
 .../filesystem_backup/docs/en/publications.md      |     27 -
 .../filesystem_backup/docs/en/references.md        |      7 -
 .../docs/en/research/cloud-free-compute.md         |      5 -
 .../docs/en/research/compression-semantique.md     |      7 -
 .../docs/en/research/dhatu-inventory-v0-1.md       |     50 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    129 -
 .../docs/en/research/human-language-development.md |     70 -
 .../en/research/hypotheses-and-alternatives.md     |      5 -
 .../filesystem_backup/docs/en/research/index.md    |      7 -
 .../docs/en/research/inventaire-dhatu-v0-1.md      |      7 -
 .../en/research/langage-humain-developpement.md    |      7 -
 .../filesystem_backup/docs/en/research/overview.md |     29 -
 .../docs/en/research/references.md                 |     57 -
 .../docs/en/research/semantic-compression.md       |     47 -
 .../docs/en/research/semantic-universals.md        |     57 -
 .../docs/en/research/universaux-semantique.md      |      9 -
 .../docs/en/research/whats-new.md                  |     21 -
 .../filesystem_backup/docs/en/style-guide.md       |      6 -
 .../filesystem_backup/docs/en/vision-social.md     |     11 -
 .../filesystem_backup/docs/en/vision-sociale.md    |     11 -
 .../filesystem_backup/docs/en/vision.md            |      9 -
 .../filesystem_backup/docs/index.md                |     45 -
 .../filesystem_backup/docs/infrastructure.md       |      0
 .../filesystem_backup/docs/licences.md             |      7 -
 .../docs/linguistic-foundations.md                 |      7 -
 .../filesystem_backup/docs/livre/index.md          |     25 -
 .../docs/livre/lecture-integrale.md                |      7 -
 .../filesystem_backup/docs/modules/_ext/.gitignore |      4 -
 .../filesystem_backup/docs/modules/index.md        |     19 -
 .../filesystem_backup/docs/monitoring-guide.md     |    188 -
 .../filesystem_backup/docs/monitoring.md           |      0
 .../docs/operations/devops/roadmap.md              |      9 -
 .../filesystem_backup/docs/publications.md         |     23 -
 .../filesystem_backup/docs/references.md           |      7 -
 .../filesystem_backup/docs/requirements.txt        |     13 -
 .../docs/research/cloud-free-compute.md            |      7 -
 .../docs/research/compression-semantique.md        |     52 -
 .../docs/research/dhatu-inventory-v0-1.md          |      6 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    141 -
 .../docs/research/human-language-development.md    |      5 -
 .../docs/research/hypotheses-and-alternatives.md   |     42 -
 .../filesystem_backup/docs/research/index.md       |     13 -
 .../docs/research/inventaire-dhatu-v0-1.md         |     51 -
 .../docs/research/langage-humain-developpement.md  |     63 -
 .../filesystem_backup/docs/research/overview.md    |     29 -
 .../filesystem_backup/docs/research/references.md  |     57 -
 .../docs/research/semantic-compression.md          |      5 -
 .../docs/research/semantic-universals.md           |      5 -
 .../docs/research/universaux-semantique.md         |    164 -
 .../docs/research/whats-new-feed.html              |     41 -
 .../filesystem_backup/docs/research/whats-new.html |     41 -
 .../filesystem_backup/docs/research/whats-new.md   |     21 -
 .../filesystem_backup/docs/style-guide.md          |      6 -
 .../filesystem_backup/docs/vision-sociale.md       |     11 -
 .../filesystem_backup/docs/vision.md               |      9 -
 .../filesystem_backup/doctor.pid                   |      1 -
 .../filesystem_backup/doctor_control.py            |      0
 .../filesystem_backup/doctor_dashboard.py          |      0
 .../filesystem_backup/doctor_watchdog.sh           |     10 -
 .../domain_monitoring_report.json                  |     59 -
 .../filesystem_backup/e2e/package.json             |     15 -
 .../filesystem_backup/e2e/playwright.config.js     |     13 -
 .../filesystem_backup/e2e/tests/modules.spec.js    |     44 -
 .../filesystem_backup/e2e/tests/research.spec.js   |     19 -
 .../filesystem_backup/e2e/tests/smoke.spec.js      |     14 -
 .../experiments/dhatu/gold_encodings.json          |     14 -
 .../experiments/dhatu/gold_encodings_child.json    |     22 -
 .../experiments/dhatu/inventory_v0_1.json          |     41 -
 .../experiments/dhatu/prompts_child/arb.json       |     15 -
 .../experiments/dhatu/prompts_child/cmn.json       |     15 -
 .../experiments/dhatu/prompts_child/deu.json       |     15 -
 .../experiments/dhatu/prompts_child/en.json        |     15 -
 .../experiments/dhatu/prompts_child/eus.json       |     15 -
 .../experiments/dhatu/prompts_child/ewe.json       |     15 -
 .../experiments/dhatu/prompts_child/fr.json        |     15 -
 .../experiments/dhatu/prompts_child/hau.json       |     15 -
 .../experiments/dhatu/prompts_child/heb.json       |     15 -
 .../experiments/dhatu/prompts_child/hin.json       |     15 -
 .../experiments/dhatu/prompts_child/hun.json       |     14 -
 .../experiments/dhatu/prompts_child/iku.json       |     15 -
 .../experiments/dhatu/prompts_child/jpn.json       |     15 -
 .../experiments/dhatu/prompts_child/kor.json       |     15 -
 .../experiments/dhatu/prompts_child/nld.json       |     15 -
 .../experiments/dhatu/prompts_child/schema.json    |     22 -
 .../experiments/dhatu/prompts_child/spa.json       |     15 -
 .../experiments/dhatu/prompts_child/swa.json       |     15 -
 .../experiments/dhatu/prompts_child/tur.json       |     15 -
 .../experiments/dhatu/prompts_child/yor.json       |     15 -
 .../experiments/dhatu/prompts_child/zul.json       |     15 -
 .../filesystem_backup/experiments/dhatu/report.py  |    113 -
 .../experiments/dhatu/toy_corpus.json              |     16 -
 .../experiments/dhatu/typological_sample.json      |    216 -
 .../experiments/dhatu/validator.py                 |    155 -
 .../filesystem_backup/firebase_notifications.py    |      0
 .../filesystem_backup/fix_google_oauth.sh          |      0
 .../filesystem_backup/fix_remotes.sh               |    299 -
 .../filesystem_backup/gdrive_credentials/README.md |      0
 .../gdrive_credentials/credentials.json.template   |      0
 .../filesystem_backup/git_audit.sh                 |      0
 .../filesystem_backup/github_workflow_doctor.py    |      0
 .../github_workflow_emergency_doctor.py            |      0
 .../governance/AUTONOMIE_VALIDATION_FINALE.md      |      3 -
 .../governance/CONVENTIONS_NAMING.md               |     22 -
 .../governance/SESSION_BILAN_ORGANISATION.md       |      3 -
 .../audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md    |      5 -
 .../audits/AUDIT_SYNCHRONISATION_GITHUB.md         |      3 -
 .../CENTRALISATION_DISCUSSIONS_COPILOTAGE.md       |      3 -
 .../governance/copilotage/POLICY.md                |     27 -
 .../governance/copilotage/README.md                |     48 -
 .../copilotage/README_COPILOTAGE_HISTORIQUE.md     |     45 -
 .../governance/copilotage/journal/INDEX.md         |      3 -
 .../copilotage/knowledge/ESSENCE_PANINIFS.md       |     39 -
 .../filesystem_backup/index.html                   |      0
 .../lancement_publications_20250820.sh             |      0
 .../filesystem_backup/last_domain_status.json      |     59 -
 .../filesystem_backup/launch_autonomous_doctor.sh  |      0
 .../launch_continuous_improvement.sh               |      0
 .../filesystem_backup/launch_hybrid_dashboard.sh   |     39 -
 .../filesystem_backup/mini_test_dhatu.py           |      0
 .../filesystem_backup/mkdocs.yml                   |    182 -
 .../filesystem_backup/mkdocs_fixed.yml             |      0
 .../attribution-registry/.github/workflows/ci.yml  |     11 -
 .../modules/attribution-registry/LICENSE           |      1 -
 .../modules/attribution-registry/README.md         |      1 -
 .../modules/attribution-registry/pyproject.toml    |      4 -
 .../autonomous-missions/.github/workflows/ci.yml   |     18 -
 .../modules/autonomous-missions/.gitignore         |    207 -
 .../modules/autonomous-missions/LICENSE            |     21 -
 .../modules/autonomous-missions/README.md          |      4 -
 .../modules/cloud-orchestrator/README.md           |      0
 .../modules/colab-controller/README.md             |      0
 .../datasets-ingestion/.github/workflows/ci.yml    |     11 -
 .../modules/datasets-ingestion/LICENSE             |      1 -
 .../modules/datasets-ingestion/README.md           |      1 -
 .../modules/datasets-ingestion/pyproject.toml      |      4 -
 .../.github/workflows/ci.yml                       |     22 -
 .../modules/execution-orchestrator/.gitignore      |      7 -
 .../modules/execution-orchestrator/LICENSE         |      1 -
 .../modules/execution-orchestrator/README.md       |     20 -
 .../modules/execution-orchestrator/pyproject.toml  |     17 -
 .../src/execution_orchestrator/cli.py              |     31 -
 .../src/execution_orchestrator/drivers/__init__.py |     18 -
 .../src/execution_orchestrator/drivers/cloud.py    |      5 -
 .../drivers/cloud/.github/workflows/ci.yml         |     18 -
 .../drivers/cloud/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/cloud/LICENSE   |     21 -
 .../execution_orchestrator/drivers/cloud/README.md |      4 -
 .../src/execution_orchestrator/drivers/colab.py    |      5 -
 .../drivers/colab/.github/workflows/ci.yml         |     18 -
 .../drivers/colab/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/colab/LICENSE   |     21 -
 .../execution_orchestrator/drivers/colab/README.md |      4 -
 .../src/execution_orchestrator/drivers/local.py    |      5 -
 .../modules/ontowave-app/.eslintrc.cjs             |     16 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     16 -
 .../.github/ISSUE_TEMPLATE/feature_request.md      |     13 -
 .../ontowave-app/.github/pull_request_template.md  |     12 -
 .../modules/ontowave-app/.github/workflows/ci.yml  |     34 -
 .../ontowave-app/.github/workflows/pr-preview.yml  |     27 -
 .../modules/ontowave-app/.gitignore                |      6 -
 .../modules/ontowave-app/.prettierignore           |      2 -
 .../modules/ontowave-app/.prettierrc               |      5 -
 .../filesystem_backup/modules/ontowave-app/LICENSE |     21 -
 .../modules/ontowave-app/README.md                 |     39 -
 .../modules/ontowave-app/content/index.md          |     16 -
 .../modules/ontowave-app/copilotage/README.md      |      7 -
 .../modules/ontowave-app/copilotage/RULES.md       |      8 -
 .../ontowave-app/copilotage/preferences.json       |      8 -
 .../ontowave-app/copilotage/preferences.yml        |     21 -
 .../ontowave-app/copilotage/scripts/prepare_pr.sh  |     27 -
 .../modules/ontowave-app/index.html                |     35 -
 .../modules/ontowave-app/package-lock.json         |   2426 -
 .../modules/ontowave-app/package.json              |     39 -
 .../modules/ontowave-app/public/config.json        |      5 -
 .../ontowave-app/scripts/check_principles.sh       |     13 -
 .../modules/ontowave-app/src/main.ts               |     53 -
 .../modules/ontowave-app/src/markdown.ts           |     51 -
 .../modules/ontowave-app/src/router.ts             |     28 -
 .../modules/ontowave-app/src/shims.d.ts            |      3 -
 .../modules/ontowave-app/tools/build-sitemap.mjs   |     47 -
 .../modules/ontowave-app/tsconfig.json             |     16 -
 .../modules/ontowave-app/vite.config.ts            |      6 -
 .../publication-engine/.github/workflows/ci.yml    |     18 -
 .../modules/publication-engine/.gitignore          |    207 -
 .../modules/publication-engine/LICENSE             |     21 -
 .../modules/publication-engine/README.md           |      2 -
 .../modules/semantic-core/.github/workflows/ci.yml |     18 -
 .../modules/semantic-core/.gitignore               |    207 -
 .../modules/semantic-core/LICENSE                  |     21 -
 .../modules/semantic-core/README.md                |      2 -
 .../ultra-reactive/.github/workflows/ci.yml        |     18 -
 .../modules/ultra-reactive/.gitignore              |    207 -
 .../modules/ultra-reactive/LICENSE                 |     21 -
 .../modules/ultra-reactive/README.md               |      4 -
 .../filesystem_backup/monitor_domains.py           |      0
 .../nocturnal_autonomous_mission.py                |      0
 .../filesystem_backup/nocturnal_mission_log.json   |     64 -
 .../filesystem_backup/notification_system.py       |      0
 .../prepare_total_externalization.sh               |    186 -
 .../filesystem_backup/publish_docs.sh              |      0
 .../filesystem_backup/quick_monitor.sh             |     48 -
 .../remarkable_study_pack/README.md                |      0
 .../reading_guides/workflow_revision_remarkable.md |      0
 .../scientific_articles/bibliographie_complete.md  |      0
 .../content_addressing_avance.md                   |      0
 .../scientific_articles/etat_art_avance.md         |      0
 .../scientific_articles/etudes_cas_exercices.md    |      0
 .../scientific_articles/fondements_theoriques.md   |      0
 .../ipfs_vs_paninifs_analysis.md                   |      0
 .../filesystem_backup/requirements.txt             |     15 -
 .../filesystem_backup/restructure_ecosystem.sh     |      0
 .../scripts/aggregate_submodule_docs.py            |     59 -
 .../scripts/analyze_submodule_issue.py             |    259 -
 .../scripts/apply_cleanup_manifest.sh              |     27 -
 .../scripts/auto_pilot_research.py                 |    159 -
 .../scripts/check_copilotage_independence.py       |     90 -
 .../scripts/detect_module_specific_content.py      |     91 -
 .../scripts/devops/audit_submodules.sh             |     53 -
 .../scripts/devops/generate_modules_index.py       |     68 -
 .../scripts/devops/monitor_prs_playwright.py       |     99 -
 .../scripts/devops/pr_auto_doctor.sh               |    202 -
 .../scripts/devops/repo_ci_snapshot.sh             |      0
 .../scripts/devops/terminal_diagnostics.sh         |      0
 .../scripts/devops/vscode_settings_tuner.py        |    149 -
 .../scripts/enforce_lowercase_paths.py             |     90 -
 .../scripts/generate_ecosystem_docs.py             |    201 -
 .../scripts/generate_modules_docs_index.py         |    111 -
 .../scripts/generate_research_rss.py               |    102 -
 .../scripts/noninteractive_env.sh                  |     11 -
 .../scripts/open_submodule_issues.py               |    104 -
 .../scripts/open_submodule_issues_gh.py            |     79 -
 .../scripts/prepare_issue_packs.py                 |    121 -
 .../scripts/setup_labels_submodules.sh             |     28 -
 .../scripts/split_to_submodule.sh                  |     48 -
 .../filesystem_backup/scripts/triage_submodules.py |    177 -
 .../filesystem_backup/setup_domains.sh             |      0
 .../filesystem_backup/setup_github_labels.sh       |     58 -
 .../filesystem_backup/setup_github_pages.sh        |      0
 .../filesystem_backup/setup_mvp_dataset.sh         |      0
 .../filesystem_backup/shutdown_totoro_procedure.sh |      0
 .../filesystem_backup/sync_paninifs_ecosystem.sh   |      0
 .../templates_publication_reseaux.md               |      0
 .../filesystem_backup/vacation_backup.sh           |     24 -
 .../vacation_emergency_monitor.sh                  |     44 -
 .../vacation_productive_system.py                  |      0
 .../vacation_productive_work.json                  |    222 -
 .../filesystem_backup/validate_dhatu.sh            |      0
 .../filesystem_backup/workflow_repair_report.json  |     36 -
 .../gitmodules_avant.txt                           |      9 -
 .../core/filesystem/.cargo/config.toml             |      0
 .../filesystem/.devcontainer/devcontainer.json     |     55 -
 .../core/filesystem/.devcontainer/setup.sh         |     53 -
 .../modules_avant/core/filesystem/.gitconfig.local |     11 -
 .../.github/ISSUE_TEMPLATE/bug-report.md           |     56 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     29 -
 .../.github/ISSUE_TEMPLATE/bug_report.yml          |     80 -
 .../filesystem/.github/ISSUE_TEMPLATE/config.yml   |      5 -
 .../.github/ISSUE_TEMPLATE/feature-request.md      |     74 -
 .../.github/ISSUE_TEMPLATE/feature_request.yml     |     71 -
 .../.github/ISSUE_TEMPLATE/research-task.md        |     54 -
 .../filesystem/.github/ISSUE_TEMPLATE/research.md  |     19 -
 .../.github/ISSUE_TEMPLATE/submodule-change.yml    |     58 -
 .../core/filesystem/.github/ISSUE_TEMPLATE/task.md |     24 -
 .../filesystem/.github/PULL_REQUEST_TEMPLATE.md    |     26 -
 .../.github/ops/triggers/deploy-docs.txt           |      2 -
 .../.github/ops/triggers/pages-diagnostics.txt     |      2 -
 .../filesystem/.github/pull_request_template.md    |      0
 .../.github/workflows/auto-merge-provenance.yml    |    100 -
 .../.github/workflows/camping-status.yml           |     29 -
 .../core/filesystem/.github/workflows/codeql.yml   |    108 -
 .../filesystem/.github/workflows/copilotage-ci.yml |     27 -
 .../.github/workflows/copilotage-journal-check.yml |     41 -
 .../.github/workflows/copilotage-journal-index.yml |     44 -
 .../.github/workflows/cross-check-visibility.yml   |     24 -
 .../.github/workflows/deploy-pages-mkdocs.yml      |    113 -
 .../.github/workflows/dhatu-validation.yml         |    187 -
 .../.github/workflows/docs-governance.yml          |    119 -
 .../filesystem/.github/workflows/docs-pages.yml    |     48 -
 .../.github/workflows/e2e-playwright.yml           |     59 -
 .../filesystem/.github/workflows/label-agent.yml   |    105 -
 .../filesystem/.github/workflows/maintenance.yml   |     19 -
 .../.github/workflows/minimal-status.yml           |     10 -
 .../filesystem/.github/workflows/owner-labeler.yml |     77 -
 .../.github/workflows/pages-diagnostics.yml        |     46 -
 .../.github/workflows/pages-enforce-https.yml      |     51 -
 .../filesystem/.github/workflows/paniniFS-ci.yml   |     16 -
 .../workflows/provenance-bootstrap-pr37.yml        |     39 -
 .../.github/workflows/provenance-guardian.yml      |    127 -
 .../filesystem/.github/workflows/publications.yml  |     54 -
 .../filesystem/.github/workflows/repo-guards.yml   |     22 -
 .../filesystem/.github/workflows/secret-scan.yml   |     32 -
 .../.github/workflows/submodule-backfill.yml       |     43 -
 .../.github/workflows/submodule-triage.yml         |     71 -
 .../.github/workflows/update-modules-index.yml     |     38 -
 .../workflows/validate-agent-provenance.yml        |     43 -
 .../.github/workflows/validate-agent-session.yml   |     38 -
 .../workflows/validate-task-coordination.yml       |     55 -
 .../modules_avant/core/filesystem/.gitignore       |     41 -
 .../modules_avant/core/filesystem/.gitmodules      |     42 -
 .../modules_avant/core/filesystem/.nojekyll        |     10 -
 .../core/filesystem/.panini-agent.toml             |      0
 .../modules_avant/core/filesystem/CNAME            |      1 -
 .../modules_avant/core/filesystem/CONTRIBUTING.md  |     51 -
 .../core/filesystem/COPILOTAGE_SHARED/README.md    |      9 -
 .../filesystem/COPILOTAGE_SHARED/settings.json     |     11 -
 .../modules_avant/core/filesystem/Cargo.toml       |      0
 .../core/filesystem/Copilotage/AGENT_CONVENTION.md |     19 -
 .../ARCHITECTURE_RESTRUCTURATION_PLAN.md           |     24 -
 .../filesystem/Copilotage/COPILOTAGE_WORKFLOW.md   |     46 -
 .../core/filesystem/Copilotage/DEPRECATED.md       |     10 -
 .../filesystem/Copilotage/DEPRECATED_README.md     |      7 -
 .../core/filesystem/Copilotage/README.md           |     46 -
 .../Copilotage/TODO_RELAIS_2025-09-02.md           |     12 -
 .../Copilotage/agents/adversarial_critic_agent.py  |      0
 .../Copilotage/agents/orchestrator_with_github.py  |      0
 .../filesystem/Copilotage/agents/requirements.txt  |     10 -
 .../agents/simple_autonomous_orchestrator.py       |      0
 .../Copilotage/agents/tests/test_agents.py         |     45 -
 .../agents/theoretical_research_agent.py           |      0
 .../filesystem/Copilotage/coordination-agent.py    |      0
 .../Copilotage/debug_notebook_local.ipynb          |      0
 .../Copilotage/demo-prototypage-rapide.md          |      0
 ...elargissement-horizon-mathematiques-physique.md |      0
 .../Copilotage/headless_autonomous_controller.py   |      0
 .../core/filesystem/Copilotage/hyperscript-2.sh    |      0
 ...-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md |    339 -
 .../journal/2025-08-30-ci-stabilisation-merge.md   |     17 -
 .../journal/2025-08-30-hauru-pid74498-session.md   |     30 -
 .../2025-08-30-linux-pid0-assimilation-archives.md |     30 -
 .../Copilotage/journal/2025-08-30-session.md       |     24 -
 .../2025-08-30-totoro-pid17771-camping-final.md    |     39 -
 .../journal/2025-09-01-totoro-pid389223-session.md |     46 -
 .../2025-09-01-totoro-pid390178-rattrapage.md      |     53 -
 .../core/filesystem/Copilotage/journal/INDEX.md    |     14 -
 .../Copilotage/knowledge/ESSENCE_PANINIFS.md       |     37 -
 .../knowledge/HYPERNODAL_DB_AND_LATTICE.md         |     23 -
 .../MODULES_OVERVIEW_AND_PARENT_PROJECT.md         |     29 -
 .../PATTERN_FINGERPRINTS_AND_RECURSION_TRAPS.md    |     22 -
 .../knowledge/SEMANTIC_UNIVERSALS_DHATU.md         |     39 -
 .../Copilotage/mission_autonome_exemplaire.py      |      0
 .../Copilotage/notes-vision-architecturale.md      |      0
 .../filesystem/Copilotage/roadmap-decouverte.md    |      0
 .../Copilotage/roadmap-hybride-rd-production.md    |      0
 .../core/filesystem/Copilotage/roadmap.md          |     16 -
 .../Copilotage/scripts/COLAB_SETUP_GUIDE.md        |      0
 .../core/filesystem/Copilotage/scripts/README.md   |     17 -
 .../scripts/advanced_consensus_engine.py           |      0
 .../Copilotage/scripts/analogy_collector.py        |      0
 .../Copilotage/scripts/analyze_preferences.py      |      0
 .../Copilotage/scripts/arxiv_collector.py          |      0
 .../Copilotage/scripts/autonomous_analyzer.py      |      0
 .../scripts/autonomous_gdrive_manager.py           |      0
 .../Copilotage/scripts/books_collector.py          |      0
 .../Copilotage/scripts/colab_api_strategy.py       |      0
 .../scripts/colab_autonomous_controller.py         |      0
 .../Copilotage/scripts/colab_cli_launcher.py       |      0
 .../Copilotage/scripts/colab_debug_environment.py  |      0
 .../Copilotage/scripts/collect_samples.py          |      0
 .../Copilotage/scripts/collect_with_attribution.py |      0
 .../Copilotage/scripts/complete_journey_summary.py |      0
 .../scripts/comprehensive_opensource_strategy.py   |      0
 .../scripts/connivance_learning_system.py          |      0
 .../Copilotage/scripts/consensus_analyzer.py       |      0
 .../scripts/continuous_autonomy_daemon.py          |      0
 .../Copilotage/scripts/debug_ultra_fast.py         |      0
 .../Copilotage/scripts/deep_cleanup_credentials.sh |      0
 .../Copilotage/scripts/deploy_colab_auto.sh        |      0
 .../Copilotage/scripts/deploy_colab_fixed.sh       |      0
 .../Copilotage/scripts/deploy_colab_secure.sh      |      0
 .../filesystem/Copilotage/scripts/devops/README.md |     23 -
 .../scripts/devops/bootstrap_submodules.sh         |     38 -
 .../Copilotage/scripts/devops/fix_remotes.sh       |    103 -
 .../Copilotage/scripts/devops/gh_pr_exempt.sh      |     25 -
 .../Copilotage/scripts/devops/gh_pr_open.sh        |     90 -
 .../Copilotage/scripts/devops/gh_queue.sh          |     67 -
 .../Copilotage/scripts/devops/gh_task_init.sh      |     49 -
 .../Copilotage/scripts/devops/git_audit.sh         |     35 -
 .../devops/init_execution_orchestrator_repo.sh     |     39 -
 .../Copilotage/scripts/devops/journal_index.sh     |     33 -
 .../Copilotage/scripts/devops/journal_session.sh   |     43 -
 .../scripts/devops/plan_migration_option_b.sh      |     39 -
 .../Copilotage/scripts/devops/run_safe.sh          |     18 -
 .../scripts/devops/setup_dev_environment.sh        |     26 -
 .../Copilotage/scripts/display_recommendations.py  |      0
 .../scripts/distribution_strategy_analyzer.py      |      0
 .../scripts/editorial/sync_publications.py         |    125 -
 .../Copilotage/scripts/emergency_plasma_fix.sh     |      0
 .../scripts/executive_summary_generator.py         |      0
 .../scripts/executive_totoro_recommendations.py    |      0
 .../Copilotage/scripts/externalization_strategy.py |      0
 .../Copilotage/scripts/final_security_check.sh     |      0
 .../Copilotage/scripts/fix_git_credentials.sh      |      0
 .../Copilotage/scripts/free_cloud_analysis.py      |      0
 .../scripts/generate_remarkable_bibliography.py    |      0
 .../scripts/generate_scientific_bibliography.py    |      0
 .../Copilotage/scripts/github_workflow_doctor.py   |      0
 .../Copilotage/scripts/github_workflow_monitor.py  |     38 -
 .../Copilotage/scripts/google_colab_setup.py       |      0
 .../Copilotage/scripts/gpu_analysis_gt630m.py      |      0
 .../scripts/hardware_integration_guide.py          |      0
 .../filesystem/Copilotage/scripts/hauru_setup.sh   |      0
 .../scripts/headless_autonomy_auditor.py           |      0
 .../Copilotage/scripts/headless_env_loader.py      |     53 -
 .../Copilotage/scripts/headless_secrets_manager.py |      0
 .../Copilotage/scripts/immediate_launch_plan.py    |      0
 .../scripts/implementation_roadmap_generator.py    |      0
 .../scripts/information_theory_collector.py        |      0
 .../scripts/intelligent_communication_guide.py     |      0
 .../Copilotage/scripts/launch_cloud_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_autonomous.sh  |      0
 .../Copilotage/scripts/launch_colab_direct.sh      |      0
 .../Copilotage/scripts/launch_optimized_colab.sh   |      0
 .../filesystem/Copilotage/scripts/launch_simple.sh |      0
 .../Copilotage/scripts/launch_total_autonomy.sh    |      0
 .../mathematics_physics_convergence_analyzer.py    |      0
 .../Copilotage/scripts/multi_source_analyzer.py    |      0
 .../scripts/neurocognitive_language_analyzer.py    |      0
 .../scripts/opensource_resources_analyzer.py       |      0
 .../scripts/optimal_language_synthesizer.py        |      0
 .../scripts/optimal_vocabulary_generator.py        |      0
 .../scripts/paniniFS_priority_strategy.py          |      0
 .../scripts/panini_analogical_extension.py         |      0
 .../scripts/panini_architectural_integrator.py     |      0
 .../Copilotage/scripts/panini_dashboard.py         |      0
 .../scripts/panini_fundamental_generator.py        |      0
 .../scripts/panini_linguistic_integrator.py        |      0
 .../Copilotage/scripts/panini_status_point.py      |      0
 .../scripts/pedagogical_applications_guide.py      |      0
 .../scripts/physics_mathematics_collector.py       |      0
 .../scripts/plasma_stabilizer_advanced.sh          |      0
 .../Copilotage/scripts/publication_generator.py    |      0
 .../Copilotage/scripts/realistic_gpu_assessment.py |      0
 .../filesystem/Copilotage/scripts/requirements.txt |     18 -
 .../filesystem/Copilotage/scripts/run_analysis.sh  |      0
 .../filesystem/Copilotage/scripts/rust_bridge.py   |      0
 .../Copilotage/scripts/safe_totoro_optimizer.py    |      0
 .../scripts/secure_cleanup_credentials.sh          |      0
 .../core/filesystem/Copilotage/scripts/setup.py    |      0
 .../Copilotage/scripts/setup_cloud_autonomous.sh   |      0
 .../Copilotage/scripts/setup_gdrive_config.py      |      0
 .../scripts/social_revolution_strategy.py          |      0
 .../scripts/solid_foundation_strategy.py           |      0
 .../scripts/temporal_emergence_analyzer.py         |      0
 .../Copilotage/scripts/test_regression.sh          |      0
 .../Copilotage/scripts/test_workflow_complete.py   |      0
 .../Copilotage/scripts/tests/test_basic.py         |     41 -
 .../Copilotage/scripts/tests/test_monitor.py       |     12 -
 .../Copilotage/scripts/total_autonomy_engine.py    |      0
 .../scripts/totoro_liberation_toolkit.sh           |      0
 .../Copilotage/scripts/totoro_optimizer.py         |      0
 .../scripts/totoro_resource_management.py          |      0
 .../Copilotage/scripts/traceability_dashboard.py   |      0
 .../scripts/ultra_reactive_controller.py           |      0
 .../scripts/vscode_extensions_manager.py           |      0
 .../Copilotage/scripts/vscode_settings_fixer.py    |      0
 .../Copilotage/session-bilan-vision-realite.md     |      0
 .../core/filesystem/Copilotage/setup-rust.md       |      0
 .../core/filesystem/Copilotage/test-build.sh       |      0
 .../Copilotage/tracabilite-attribution.md          |     20 -
 .../modules_avant/core/filesystem/LICENSE          |     21 -
 .../Panini_Ecosystem_Coherence_Audit.ipynb         |      0
 .../modules_avant/core/filesystem/README.en.md     |      0
 .../modules_avant/core/filesystem/README.md        |    159 -
 .../cloud-processing/FREE_COMPUTE_STRATEGY.md      |    110 -
 .../BABY_SIGN_LANGUAGE_FOUNDATION.md               |      0
 .../dhatu-universals/DECOUVERTE_DHATU_CORE_SET.md  |      0
 .../DHATU_ATOMES_CONCEPTUELS_REVISION.md           |      0
 .../core/filesystem/RESEARCH/docs/README.md        |      6 -
 .../methodology/protocols/GUIDE_LEANPUB_ETAPE1.md  |      0
 .../methodology/protocols/GUIDE_MEDIUM_ETAPE3.md   |      0
 .../protocols/ORDRE_PUBLICATION_GUIDE.md           |      0
 .../protocols/PUBLICATION_COORDONNEE_20250820.md   |      0
 .../protocols/SYNCHRONISATION_MEDIUM_2025.md       |     83 -
 .../articles/ARTICLE_MEDIUM_FINAL_2025.md          |      0
 .../articles/ARTICLE_MEDIUM_FINAL_2025_EN.md       |      0
 .../articles/english/ARTICLE_MEDIUM_2025_EN.md     |    419 -
 .../articles/french/ARTICLE_MEDIUM_2025.md         |    408 -
 .../publications/books/LIVRE_LEANPUB_FINAL_2025.md |      0
 .../books/english/LIVRE_LEANPUB_2025_EN.md         |      0
 .../books/french/LIVRE_LEANPUB_2025.md             |    554 -
 .../core/filesystem/activate_total_autonomy.sh     |      0
 .../core/filesystem/analogy_detector_mvp.py        |      0
 .../core/filesystem/android_template.java          |      0
 .../artifacts/playwright/pr-40-checks.png          |    Bin 274486 -> 0 bytes
 .../artifacts/playwright/pr-40-overview.png        |    Bin 693119 -> 0 bytes
 .../artifacts/playwright/pr-42-checks.png          |    Bin 179199 -> 0 bytes
 .../artifacts/playwright/pr-42-overview.png        |    Bin 711460 -> 0 bytes
 .../snapshots/snapshot-20250902-152737.txt         |     40 -
 .../core/filesystem/autonomous_colab_tester.py     |      0
 .../core/filesystem/autonomous_test_log.json       |     20 -
 .../core/filesystem/autonomous_workflow_doctor.py  |      0
 .../core/filesystem/check_colab_mission.py         |      0
 .../core/filesystem/check_deployment.sh            |      0
 .../modules_avant/core/filesystem/check_dns.sh     |      0
 .../core/filesystem/cleanup/manifest.txt           |     92 -
 .../cloud_backup/autonomous_crontab_simple.txt     |      0
 .../core/filesystem/configure_vacation_mode.sh     |      0
 .../core/filesystem/copilotage/README.md           |      8 -
 .../core/filesystem/copilotage/config.yml          |      8 -
 .../core/filesystem/copilotage/shared/README.md    |      3 -
 .../core/filesystem/copilotage/shared/config.yml   |      1 -
 .../core/filesystem/data/ecosystem.yml             |    121 -
 .../core/filesystem/deploy_cloud_autonomous.py     |      0
 .../core/filesystem/deploy_cloud_ecosystem.sh      |      0
 .../filesystem/deploy_colab_deployment_center.py   |      0
 .../modules_avant/core/filesystem/deploy_docs.sh   |      0
 .../core/filesystem/deploy_dynamic_monitoring.sh   |     99 -
 .../core/filesystem/deploy_paninifs.sh             |      0
 .../core/filesystem/deploy_paninifs_simple.sh      |      0
 .../core/filesystem/dhatu_detector.py              |      0
 .../modules_avant/core/filesystem/docs/.keep       |      1 -
 .../filesystem/docs/OPERATIONS/DevOps/roadmap.md   |      5 -
 .../core/filesystem/docs/avancement.md             |     15 -
 .../core/filesystem/docs/dashboard.md              |    205 -
 .../core/filesystem/docs/data/dhatu_child_langs.md |     25 -
 .../docs/data/dhatu_child_phenomena_summary.md     |     25 -
 .../core/filesystem/docs/data/system_status.json   |    127 -
 .../core/filesystem/docs/dhatu-framework.md        |     13 -
 .../modules_avant/core/filesystem/docs/diagrams.md |     26 -
 .../core/filesystem/docs/doc-process.md            |      9 -
 .../core/filesystem/docs/ecosystem/README.md       |     26 -
 .../core/filesystem/docs/ecosystem/catalogue.md    |      5 -
 .../core/filesystem/docs/ecosystem/ontowave.md     |     55 -
 .../core/filesystem/docs/ecosystem/panorama.md     |      5 -
 .../docs/ecosystem/repos/attribution-registry.md   |     10 -
 .../docs/ecosystem/repos/autonomous-missions.md    |     10 -
 .../docs/ecosystem/repos/copilotage-shared.md      |     10 -
 .../docs/ecosystem/repos/datasets-ingestion.md     |     10 -
 .../docs/ecosystem/repos/execution-orchestrator.md |     10 -
 .../docs/ecosystem/repos/ontowave-app.md           |     10 -
 .../docs/ecosystem/repos/publication-engine.md     |     10 -
 .../filesystem/docs/ecosystem/repos/research.md    |     10 -
 .../core/filesystem/docs/ecosystem/repos/root.md   |     10 -
 .../docs/ecosystem/repos/semantic-core.md          |     10 -
 .../docs/ecosystem/repos/ultra-reactive.md         |     10 -
 .../docs/en/OPERATIONS/DevOps/roadmap.md           |      5 -
 .../core/filesystem/docs/en/avancement.md          |     15 -
 .../core/filesystem/docs/en/dhatu-framework.md     |     13 -
 .../core/filesystem/docs/en/diagrams.md            |     26 -
 .../core/filesystem/docs/en/doc-process.md         |      7 -
 .../core/filesystem/docs/en/ecosystem/ontowave.md  |     55 -
 .../modules_avant/core/filesystem/docs/en/index.md |     43 -
 .../core/filesystem/docs/en/infrastructure.md      |      0
 .../core/filesystem/docs/en/licences.md            |      7 -
 .../filesystem/docs/en/linguistic-foundations.md   |      7 -
 .../filesystem/docs/en/livre/lecture-integrale.md  |      9 -
 .../core/filesystem/docs/en/modules/index.md       |     10 -
 .../core/filesystem/docs/en/monitoring-guide.md    |      3 -
 .../core/filesystem/docs/en/monitoring.md          |      0
 .../docs/en/operations/devops/roadmap.md           |      9 -
 .../core/filesystem/docs/en/progress.md            |     15 -
 .../core/filesystem/docs/en/publications.md        |     27 -
 .../core/filesystem/docs/en/references.md          |      7 -
 .../docs/en/research/cloud-free-compute.md         |      5 -
 .../docs/en/research/compression-semantique.md     |      7 -
 .../docs/en/research/dhatu-inventory-v0-1.md       |     50 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    129 -
 .../docs/en/research/human-language-development.md |     70 -
 .../en/research/hypotheses-and-alternatives.md     |      5 -
 .../core/filesystem/docs/en/research/index.md      |      7 -
 .../docs/en/research/inventaire-dhatu-v0-1.md      |      7 -
 .../en/research/langage-humain-developpement.md    |      7 -
 .../core/filesystem/docs/en/research/overview.md   |     29 -
 .../core/filesystem/docs/en/research/references.md |     57 -
 .../docs/en/research/semantic-compression.md       |     47 -
 .../docs/en/research/semantic-universals.md        |     57 -
 .../docs/en/research/universaux-semantique.md      |      9 -
 .../core/filesystem/docs/en/research/whats-new.md  |     21 -
 .../core/filesystem/docs/en/style-guide.md         |      6 -
 .../core/filesystem/docs/en/vision-social.md       |     11 -
 .../core/filesystem/docs/en/vision-sociale.md      |     11 -
 .../core/filesystem/docs/en/vision.md              |      9 -
 .../modules_avant/core/filesystem/docs/index.md    |     45 -
 .../core/filesystem/docs/infrastructure.md         |      0
 .../modules_avant/core/filesystem/docs/licences.md |      7 -
 .../core/filesystem/docs/linguistic-foundations.md |      7 -
 .../core/filesystem/docs/livre/index.md            |     25 -
 .../filesystem/docs/livre/lecture-integrale.md     |      7 -
 .../core/filesystem/docs/modules/_ext/.gitignore   |      4 -
 .../core/filesystem/docs/modules/index.md          |     19 -
 .../core/filesystem/docs/monitoring-guide.md       |    188 -
 .../core/filesystem/docs/monitoring.md             |      0
 .../filesystem/docs/operations/devops/roadmap.md   |      9 -
 .../core/filesystem/docs/publications.md           |     23 -
 .../core/filesystem/docs/references.md             |      7 -
 .../core/filesystem/docs/requirements.txt          |     13 -
 .../filesystem/docs/research/cloud-free-compute.md |      7 -
 .../docs/research/compression-semantique.md        |     52 -
 .../docs/research/dhatu-inventory-v0-1.md          |      6 -
 .../research/experiences-dhatu-typologie-v0-1.md   |    141 -
 .../docs/research/human-language-development.md    |      5 -
 .../docs/research/hypotheses-and-alternatives.md   |     42 -
 .../core/filesystem/docs/research/index.md         |     13 -
 .../docs/research/inventaire-dhatu-v0-1.md         |     51 -
 .../docs/research/langage-humain-developpement.md  |     63 -
 .../core/filesystem/docs/research/overview.md      |     29 -
 .../core/filesystem/docs/research/references.md    |     57 -
 .../docs/research/semantic-compression.md          |      5 -
 .../docs/research/semantic-universals.md           |      5 -
 .../docs/research/universaux-semantique.md         |    164 -
 .../filesystem/docs/research/whats-new-feed.html   |     41 -
 .../core/filesystem/docs/research/whats-new.html   |     41 -
 .../core/filesystem/docs/research/whats-new.md     |     21 -
 .../core/filesystem/docs/style-guide.md            |      6 -
 .../core/filesystem/docs/vision-sociale.md         |     11 -
 .../modules_avant/core/filesystem/docs/vision.md   |      9 -
 .../modules_avant/core/filesystem/doctor.pid       |      1 -
 .../core/filesystem/doctor_control.py              |      0
 .../core/filesystem/doctor_dashboard.py            |      0
 .../core/filesystem/doctor_watchdog.sh             |     10 -
 .../core/filesystem/domain_monitoring_report.json  |     59 -
 .../modules_avant/core/filesystem/e2e/package.json |     15 -
 .../core/filesystem/e2e/playwright.config.js       |     13 -
 .../core/filesystem/e2e/tests/modules.spec.js      |     44 -
 .../core/filesystem/e2e/tests/research.spec.js     |     19 -
 .../core/filesystem/e2e/tests/smoke.spec.js        |     14 -
 .../experiments/dhatu/gold_encodings.json          |     14 -
 .../experiments/dhatu/gold_encodings_child.json    |     22 -
 .../experiments/dhatu/inventory_v0_1.json          |     41 -
 .../experiments/dhatu/prompts_child/arb.json       |     15 -
 .../experiments/dhatu/prompts_child/cmn.json       |     15 -
 .../experiments/dhatu/prompts_child/deu.json       |     15 -
 .../experiments/dhatu/prompts_child/en.json        |     15 -
 .../experiments/dhatu/prompts_child/eus.json       |     15 -
 .../experiments/dhatu/prompts_child/ewe.json       |     15 -
 .../experiments/dhatu/prompts_child/fr.json        |     15 -
 .../experiments/dhatu/prompts_child/hau.json       |     15 -
 .../experiments/dhatu/prompts_child/heb.json       |     15 -
 .../experiments/dhatu/prompts_child/hin.json       |     15 -
 .../experiments/dhatu/prompts_child/hun.json       |     14 -
 .../experiments/dhatu/prompts_child/iku.json       |     15 -
 .../experiments/dhatu/prompts_child/jpn.json       |     15 -
 .../experiments/dhatu/prompts_child/kor.json       |     15 -
 .../experiments/dhatu/prompts_child/nld.json       |     15 -
 .../experiments/dhatu/prompts_child/schema.json    |     22 -
 .../experiments/dhatu/prompts_child/spa.json       |     15 -
 .../experiments/dhatu/prompts_child/swa.json       |     15 -
 .../experiments/dhatu/prompts_child/tur.json       |     15 -
 .../experiments/dhatu/prompts_child/yor.json       |     15 -
 .../experiments/dhatu/prompts_child/zul.json       |     15 -
 .../core/filesystem/experiments/dhatu/report.py    |    113 -
 .../filesystem/experiments/dhatu/toy_corpus.json   |     16 -
 .../experiments/dhatu/typological_sample.json      |    216 -
 .../core/filesystem/experiments/dhatu/validator.py |    155 -
 .../core/filesystem/firebase_notifications.py      |      0
 .../core/filesystem/fix_google_oauth.sh            |      0
 .../modules_avant/core/filesystem/fix_remotes.sh   |    299 -
 .../core/filesystem/gdrive_credentials/README.md   |      0
 .../gdrive_credentials/credentials.json.template   |      0
 .../modules_avant/core/filesystem/git_audit.sh     |      0
 .../core/filesystem/github_workflow_doctor.py      |      0
 .../filesystem/github_workflow_emergency_doctor.py |      0
 .../governance/AUTONOMIE_VALIDATION_FINALE.md      |      3 -
 .../filesystem/governance/CONVENTIONS_NAMING.md    |     22 -
 .../governance/SESSION_BILAN_ORGANISATION.md       |      3 -
 .../audits/AUDIT_COHERENCE_CONCEPTUELLE_2025.md    |      5 -
 .../audits/AUDIT_SYNCHRONISATION_GITHUB.md         |      3 -
 .../CENTRALISATION_DISCUSSIONS_COPILOTAGE.md       |      3 -
 .../filesystem/governance/copilotage/POLICY.md     |     27 -
 .../filesystem/governance/copilotage/README.md     |     48 -
 .../copilotage/README_COPILOTAGE_HISTORIQUE.md     |     45 -
 .../governance/copilotage/journal/INDEX.md         |      3 -
 .../copilotage/knowledge/ESSENCE_PANINIFS.md       |     39 -
 .../modules_avant/core/filesystem/index.html       |      0
 .../filesystem/lancement_publications_20250820.sh  |      0
 .../core/filesystem/last_domain_status.json        |     59 -
 .../core/filesystem/launch_autonomous_doctor.sh    |      0
 .../filesystem/launch_continuous_improvement.sh    |      0
 .../core/filesystem/launch_hybrid_dashboard.sh     |     39 -
 .../core/filesystem/mini_test_dhatu.py             |      0
 .../modules_avant/core/filesystem/mkdocs.yml       |    182 -
 .../modules_avant/core/filesystem/mkdocs_fixed.yml |      0
 .../attribution-registry/.github/workflows/ci.yml  |     11 -
 .../modules/attribution-registry/LICENSE           |      1 -
 .../modules/attribution-registry/README.md         |      1 -
 .../modules/attribution-registry/pyproject.toml    |      4 -
 .../autonomous-missions/.github/workflows/ci.yml   |     18 -
 .../modules/autonomous-missions/.gitignore         |    207 -
 .../filesystem/modules/autonomous-missions/LICENSE |     21 -
 .../modules/autonomous-missions/README.md          |      4 -
 .../modules/cloud-orchestrator/README.md           |      0
 .../filesystem/modules/colab-controller/README.md  |      0
 .../datasets-ingestion/.github/workflows/ci.yml    |     11 -
 .../filesystem/modules/datasets-ingestion/LICENSE  |      1 -
 .../modules/datasets-ingestion/README.md           |      1 -
 .../modules/datasets-ingestion/pyproject.toml      |      4 -
 .../.github/workflows/ci.yml                       |     22 -
 .../modules/execution-orchestrator/.gitignore      |      7 -
 .../modules/execution-orchestrator/LICENSE         |      1 -
 .../modules/execution-orchestrator/README.md       |     20 -
 .../modules/execution-orchestrator/pyproject.toml  |     17 -
 .../src/execution_orchestrator/cli.py              |     31 -
 .../src/execution_orchestrator/drivers/__init__.py |     18 -
 .../src/execution_orchestrator/drivers/cloud.py    |      5 -
 .../drivers/cloud/.github/workflows/ci.yml         |     18 -
 .../drivers/cloud/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/cloud/LICENSE   |     21 -
 .../execution_orchestrator/drivers/cloud/README.md |      4 -
 .../src/execution_orchestrator/drivers/colab.py    |      5 -
 .../drivers/colab/.github/workflows/ci.yml         |     18 -
 .../drivers/colab/.gitignore                       |    207 -
 .../execution_orchestrator/drivers/colab/LICENSE   |     21 -
 .../execution_orchestrator/drivers/colab/README.md |      4 -
 .../src/execution_orchestrator/drivers/local.py    |      5 -
 .../filesystem/modules/ontowave-app/.eslintrc.cjs  |     16 -
 .../.github/ISSUE_TEMPLATE/bug_report.md           |     16 -
 .../.github/ISSUE_TEMPLATE/feature_request.md      |     13 -
 .../ontowave-app/.github/pull_request_template.md  |     12 -
 .../modules/ontowave-app/.github/workflows/ci.yml  |     34 -
 .../ontowave-app/.github/workflows/pr-preview.yml  |     27 -
 .../filesystem/modules/ontowave-app/.gitignore     |      6 -
 .../modules/ontowave-app/.prettierignore           |      2 -
 .../filesystem/modules/ontowave-app/.prettierrc    |      5 -
 .../core/filesystem/modules/ontowave-app/LICENSE   |     21 -
 .../core/filesystem/modules/ontowave-app/README.md |     39 -
 .../modules/ontowave-app/content/index.md          |     16 -
 .../modules/ontowave-app/copilotage/README.md      |      7 -
 .../modules/ontowave-app/copilotage/RULES.md       |      8 -
 .../ontowave-app/copilotage/preferences.json       |      8 -
 .../ontowave-app/copilotage/preferences.yml        |     21 -
 .../ontowave-app/copilotage/scripts/prepare_pr.sh  |     27 -
 .../filesystem/modules/ontowave-app/index.html     |     35 -
 .../modules/ontowave-app/package-lock.json         |   2426 -
 .../filesystem/modules/ontowave-app/package.json   |     39 -
 .../modules/ontowave-app/public/config.json        |      5 -
 .../ontowave-app/scripts/check_principles.sh       |     13 -
 .../filesystem/modules/ontowave-app/src/main.ts    |     53 -
 .../modules/ontowave-app/src/markdown.ts           |     51 -
 .../filesystem/modules/ontowave-app/src/router.ts  |     28 -
 .../filesystem/modules/ontowave-app/src/shims.d.ts |      3 -
 .../modules/ontowave-app/tools/build-sitemap.mjs   |     47 -
 .../filesystem/modules/ontowave-app/tsconfig.json  |     16 -
 .../filesystem/modules/ontowave-app/vite.config.ts |      6 -
 .../publication-engine/.github/workflows/ci.yml    |     18 -
 .../modules/publication-engine/.gitignore          |    207 -
 .../filesystem/modules/publication-engine/LICENSE  |     21 -
 .../modules/publication-engine/README.md           |      2 -
 .../modules/semantic-core/.github/workflows/ci.yml |     18 -
 .../filesystem/modules/semantic-core/.gitignore    |    207 -
 .../core/filesystem/modules/semantic-core/LICENSE  |     21 -
 .../filesystem/modules/semantic-core/README.md     |      2 -
 .../ultra-reactive/.github/workflows/ci.yml        |     18 -
 .../filesystem/modules/ultra-reactive/.gitignore   |    207 -
 .../core/filesystem/modules/ultra-reactive/LICENSE |     21 -
 .../filesystem/modules/ultra-reactive/README.md    |      4 -
 .../core/filesystem/monitor_domains.py             |      0
 .../filesystem/nocturnal_autonomous_mission.py     |      0
 .../core/filesystem/nocturnal_mission_log.json     |     64 -
 .../core/filesystem/notification_system.py         |      0
 .../filesystem/prepare_total_externalization.sh    |    186 -
 .../modules_avant/core/filesystem/publish_docs.sh  |      0
 .../modules_avant/core/filesystem/quick_monitor.sh |     48 -
 .../filesystem/remarkable_study_pack/README.md     |      0
 .../reading_guides/workflow_revision_remarkable.md |      0
 .../scientific_articles/bibliographie_complete.md  |      0
 .../content_addressing_avance.md                   |      0
 .../scientific_articles/etat_art_avance.md         |      0
 .../scientific_articles/etudes_cas_exercices.md    |      0
 .../scientific_articles/fondements_theoriques.md   |      0
 .../ipfs_vs_paninifs_analysis.md                   |      0
 .../modules_avant/core/filesystem/requirements.txt |     15 -
 .../core/filesystem/restructure_ecosystem.sh       |      0
 .../filesystem/scripts/aggregate_submodule_docs.py |     59 -
 .../filesystem/scripts/analyze_submodule_issue.py  |    259 -
 .../filesystem/scripts/apply_cleanup_manifest.sh   |     27 -
 .../core/filesystem/scripts/auto_pilot_research.py |    159 -
 .../scripts/check_copilotage_independence.py       |     90 -
 .../scripts/detect_module_specific_content.py      |     91 -
 .../filesystem/scripts/devops/audit_submodules.sh  |     53 -
 .../scripts/devops/generate_modules_index.py       |     68 -
 .../scripts/devops/monitor_prs_playwright.py       |     99 -
 .../filesystem/scripts/devops/pr_auto_doctor.sh    |    202 -
 .../filesystem/scripts/devops/repo_ci_snapshot.sh  |      0
 .../scripts/devops/terminal_diagnostics.sh         |      0
 .../scripts/devops/vscode_settings_tuner.py        |    149 -
 .../filesystem/scripts/enforce_lowercase_paths.py  |     90 -
 .../filesystem/scripts/generate_ecosystem_docs.py  |    201 -
 .../scripts/generate_modules_docs_index.py         |    111 -
 .../filesystem/scripts/generate_research_rss.py    |    102 -
 .../core/filesystem/scripts/noninteractive_env.sh  |     11 -
 .../filesystem/scripts/open_submodule_issues.py    |    104 -
 .../filesystem/scripts/open_submodule_issues_gh.py |     79 -
 .../core/filesystem/scripts/prepare_issue_packs.py |    121 -
 .../filesystem/scripts/setup_labels_submodules.sh  |     28 -
 .../core/filesystem/scripts/split_to_submodule.sh  |     48 -
 .../core/filesystem/scripts/triage_submodules.py   |    177 -
 .../modules_avant/core/filesystem/setup_domains.sh |      0
 .../core/filesystem/setup_github_labels.sh         |     58 -
 .../core/filesystem/setup_github_pages.sh          |      0
 .../core/filesystem/setup_mvp_dataset.sh           |      0
 .../core/filesystem/shutdown_totoro_procedure.sh   |      0
 .../core/filesystem/sync_paninifs_ecosystem.sh     |      0
 .../filesystem/templates_publication_reseaux.md    |      0
 .../core/filesystem/vacation_backup.sh             |     24 -
 .../core/filesystem/vacation_emergency_monitor.sh  |     44 -
 .../core/filesystem/vacation_productive_system.py  |      0
 .../core/filesystem/vacation_productive_work.json  |    222 -
 .../core/filesystem/validate_dhatu.sh              |      0
 .../core/filesystem/workflow_repair_report.json    |     36 -
 .../.github/DIRECTIVE_APPROBATIONS_COMMANDES.md    |    347 -
 .../DIRECTIVE_CONSOLIDATION_SERVEUR_UNIVERSEL.md   |    358 -
 .../ISSUE_TEMPLATE/spec-kit-pilot-migration.md     |    304 -
 .../research_backup/.github/README.md              |    422 -
 .../.github/copilot-approved-scripts.json          |    667 -
 .../.github/prompts/analyze.prompt.md              |    101 -
 .../.github/prompts/clarify.prompt.md              |    158 -
 .../.github/prompts/constitution.prompt.md         |     73 -
 .../.github/prompts/implement.prompt.md            |     56 -
 .../research_backup/.github/prompts/plan.prompt.md |     43 -
 .../.github/prompts/specify.prompt.md              |     21 -
 .../.github/prompts/tasks.prompt.md                |     62 -
 .../reports/server_audit_20251003_220914.json      |    462 -
 .../reports/system_status_20251003_215739.json     |     56 -
 .../.github/scripts/approval_monitor.py            |    348 -
 .../.github/scripts/system_initializer.py          |    384 -
 .../.github/scripts/validate_command.py            |    307 -
 .../.github/scripts/weekly_optimization_cron.sh    |     19 -
 .../.github/scripts/weekly_optimizer.py            |    372 -
 .../research_backup/.github/workflows/pages.yml    |     37 -
 .../research_backup/ANALYSE_ENRICHIE_COMPLETE.md   |    129 -
 .../research_backup/AUDIT_COMPREHENSION_MISSION.md |     85 -
 ...CKLOG_ARCHIVED_PROJECTS_2025-10-01T15-42-06Z.md |    298 -
 ...CKLOG_REACTIVATION_PLAN_2025-10-01T16-45-19Z.md |    199 -
 ...CKLOG_REACTIVATION_PLAN_2025-10-01T16-45-25Z.md |    199 -
 .../CLARIFICATIONS_MISSION_CRITIQUE.md             |    178 -
 .../COMMENTAIRES_PRS_CLARIFICATIONS.md             |    340 -
 .../research_backup/COMPRESSOR_ARCHITECTURE_v1.md  |    867 -
 .../COMPRESSOR_ARCHITECTURE_v1_ADDENDUM.md         |    881 -
 .../research_backup/CONTINUE_DEV_INTEGRATION.md    |     57 -
 .../CONTRAINTES_COMPATIBILITE_APPLICATIONS.md      |    110 -
 .../COPILOTAGE_DATES_ISO_APPLIQUE.md               |    100 -
 .../COPILOTAGE_DATES_ISO_VALIDATION_FINALE.md      |     71 -
 .../research_backup/CORE_EXECUTION_PLAN.md         |    304 -
 .../research_backup/CORRECTIONS_LAYOUT_UHD.md      |    132 -
 .../research_backup/CORRECTION_JS_CHARGEMENT.md    |    144 -
 .../DASHBOARD_ENRICHI_MODELE_EBAUCHES.md           |    123 -
 .../DASHBOARD_TRANSFORME_ACTIVITE.md               |    140 -
 .../research_backup/DEMONSTRATION_UHD_COMPLETE.md  |    223 -
 .../research_backup/EBAUCHES_PANINI_EN_COURS.md    |    179 -
 .../GITHUB_COPILOT_CODING_AGENT_SETUP.md           |    107 -
 .../GITHUB_PAGES_DASHBOARD_GUIDE.md                |    357 -
 .../research_backup/GITHUB_PROJECT_FINAL_REPORT.md |    217 -
 .../GITHUB_PROJECT_ISSUES_STRATEGIQUES.md          |    221 -
 .../research_backup/GITHUB_PROJECT_LANCE.md        |    102 -
 .../GUIDE_LECTEUR_VIRTUEL_SITE_EXPLORATION.md      |    142 -
 .../GUIDE_PRATIQUE_ZERO_APPROBATIONS.md            |    353 -
 ...L_ARCHITECTURE_ANALYSIS_2025-10-03T15-02-38Z.md |    107 -
 ...RCHICAL_TESTS_RESULTS_2025-10-03T15-10-44Z.json |    585 -
 .../research_backup/ISSUE11_COMPLETED_SUMMARY.md   |    153 -
 ...NAL_VALIDATION_REPORT_2025-10-02T22-15-33Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-02T22-17-33Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-03T12-25-07Z.json |     64 -
 ...NAL_VALIDATION_REPORT_2025-10-03T13-46-19Z.json |     64 -
 ...ISSUE_OPTIMISATION_CONNIVENCES_NON_DECLAREES.md |    159 -
 .../JOURNAL_SESSION_COMPRESSEUR_MVP_2025-10-01.md  |    565 -
 .../MIGRATION_COPILOTAGE_TO_SPEC_KIT.md            |    545 -
 .../research_backup/MIGRATION_EXECUTIVE_SUMMARY.md |    112 -
 .../research_backup/MISSION_ACCOMPLIE_UHD.md       |    169 -
 .../research_backup/MISSION_ACCOMPLISHED.md        |    149 -
 .../research_backup/MISSION_DASHBOARD_ACCOMPLIE.md |     59 -
 .../MULTI_AGENT_COLLABORATION_GUIDE.md             |    458 -
 .../PANINI_ECOSYSTEM_ORCHESTRATOR_GUIDE.md         |    474 -
 ...TIVE_SIZE_SUMMARY_2025-10-03T11-54-57.043799.md |     48 -
 ...AT_ENCYCLOPEDIA_2025-10-03T10-42-28.536994.json |    974 -
 .../PANINI_GIT_MULTI_REPOS_ACHIEVEMENT.md          |    140 -
 ..._STRUCTURE_REPORT_2025-10-03T12-01-28.959164.md |     60 -
 ...ON_ENCYCLOPEDIA_2025-10-03T10-58-57.908785.json |    988 -
 ...TIMIZATION_REPORT_2025-10-03T10-58-57.908785.md |     71 -
 ...E_ANALYSIS_DATA_2025-10-03T11-53-12.188496.json |    810 -
 ...E_ANALYSIS_REPORT_2025-10-03T11-53-12.188496.md |     65 -
 .../PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md     |    519 -
 .../PANINI_VFS_ACHIEVEMENT_SUMMARY.md              |     91 -
 .../research_backup/PHASE1_COLAB_INSTRUCTIONS.md   |     60 -
 .../research_backup/PHASE1_HUMAN_TASK_GUIDE.md     |    165 -
 .../research_backup/PHASE1_MONITORING_GUIDE.md     |    309 -
 .../PILOT_REPORT_PANINI_ONTOWAVE.md                |    502 -
 .../POINTS_CLES_MISSION_OFFICIEL.md                |     65 -
 .../RAPPORT_ANALYSE_TRADUCTEURS_2025-10-01.md      |    268 -
 .../RAPPORT_MISSION_ANALYSEURS_SEMANTIQUES.md      |    194 -
 .../research_backup/RAPPORT_SESSION_2025-09-30.md  |    260 -
 .../research_backup/RAPPORT_SESSION_AUTONOME.md    |    736 -
 .../research_backup/README_AUTONOMOUS_APPROVALS.md |    299 -
 .../research_backup/README_MISSION_PANINI.md       |    119 -
 .../REPONSE_HIERARCHIE_EXCLUSIVE_CONFIRMEE.md      |    119 -
 .../RESOLUTION_AFFICHAGE_CONTENU.md                |     64 -
 .../RESOLUTION_DEFINITIVE_CORPUS.md                |    118 -
 .../research_backup/RESUME_EXECUTIF_PANINI.md      |    100 -
 .../SESSION_COMPLETE_SYNTHESE_EXECUTIVE.md         |    451 -
 .../research_backup/SESSION_SUMMARY_20251003.md    |    394 -
 .../SOLUTION_APPROBATION_COMMANDES_AUTONOMES.md    |    496 -
 .../research_backup/SPEC_KIT_INTEGRATION.md        |    271 -
 .../STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md       |    288 -
 .../research_backup/STRATEGIC_REFACTORING_PLAN.md  |    297 -
 .../STRATEGIE_AGENTS_UNIVERSAUX_SEMANTIQUES.md     |    143 -
 .../STRATEGIE_RAFFINEE_PLAN_TRAVAIL.md             |    236 -
 .../SYNTHESE_CLARIFICATIONS_INTEGREES.md           |    330 -
 .../VALIDATION_SYSTEM_HIERARCHIQUE_CORPUS_REEL.md  |    136 -
 .../research_backup/VUE_MODELE_PANINI_COMPLET.md   |    156 -
 .../research_backup/activity_dashboard_data.json   |      6 -
 ...anced_reconstruction_validation_1759520023.json |    154 -
 .../api_documentation_compressed.json              |    158 -
 .../research_backup/audit_server_consolidation.py  |    299 -
 .../research_backup/auto_update_dashboard.sh       |     39 -
 ...acklog_review_results_2025-10-01T16-45-19Z.json |    591 -
 ...acklog_review_results_2025-10-01T16-45-25Z.json |    591 -
 .../research_backup/compression_benchmarks.json    |    487 -
 .../compression_validation_results.json            |    258 -
 ...otage_date_compliance_2025-09-29T20-22-03Z.json | 445048 -----------------
 ...otage_date_compliance_2025-09-29T20-22-13Z.json | 445056 -----------------
 ...otage_date_compliance_2025-09-29T20-28-19Z.json | 445096 ------------------
 .../copilotage_date_iso_standard.json              |    219 -
 .../dashboard_activity_focused.html                |    566 -
 .../research_backup/dashboard_data.json            |    138 -
 .../research_backup/dashboard_real_data.json       |     41 -
 .../research_backup/dashboard_real_panini.html     |    687 -
 .../research_backup/dashboard_web_semantic.html    |    745 -
 .../research_backup/demo_analyse_enrichie.html     |    334 -
 .../demo_decomposition_detaillee.html              |    799 -
 .../research_backup/deploy_phase1_dashboard.sh     |     97 -
 .../research_backup/extracted_content.json         |    279 -
 .../research_backup/index.html                     |    438 -
 .../interface_decomposition_complete.html          |    711 -
 ...601_compliance_report_2025-10-01T13-39-40Z.json |    124 -
 ...antic_atoms_discovery_2025-10-03T00-39-54Z.json |    343 -
 ...antic_atoms_discovery_2025-10-03T12-24-46Z.json |    343 -
 ...antic_atoms_discovery_2025-10-03T14-10-46Z.json |    343 -
 .../research_backup/launch_advanced_demo.sh        |     67 -
 ...sion_alignment_report_2025-10-01T15-25-43Z.json |    168 -
 ...sion_alignment_report_2025-10-01T15-48-06Z.json |    168 -
 .../research_backup/multilingual_embeddings.json   |    795 -
 .../orchestrator_state_2025-10-01T14-25-27Z.json   |    242 -
 .../research_backup/panini_advanced_uhd_clean.py   |    822 -
 .../panini_advanced_uhd_reconstructor.py           |   1190 -
 .../research_backup/panini_binary_decomposer.py    |    792 -
 .../research_backup/panini_clean_final.py          |    570 -
 .../research_backup/panini_demo_data_generator.py  |    288 -
 .../panini_deployment_guide_20251003_135653.md     |    110 -
 .../panini_detailed_size_analyzer.py               |    492 -
 .../research_backup/panini_duplicate_analyzer.py   |    482 -
 .../panini_ecosystem_orchestrator.py               |    524 -
 ...anini_ecosystem_state_2025-10-01T14-55-21Z.json |    580 -
 ...anini_ecosystem_state_2025-10-01T15-48-50Z.json |    734 -
 .../panini_format_discovery_engine.py              |    591 -
 .../research_backup/panini_full_stack_digesteur.py |    445 -
 .../panini_git_repo_architecture.py                |    868 -
 .../panini_hierarchical_architecture.py            |    527 -
 .../panini_internal_structure_analyzer.py          |    800 -
 .../panini_issue11_final_validator.py              |    379 -
 .../panini_issue12_separation_analyzer.py          |    873 -
 .../panini_issue13_semantic_atoms.py               |    831 -
 .../panini_issue14_dashboard_realtime.py           |    804 -
 .../panini_optimization_discovery_engine.py        |    725 -
 .../research_backup/panini_performance_analyzer.py |    535 -
 .../research_backup/panini_real_data.json          |     27 -
 .../research_backup/panini_repos_status_viewer.py  |    397 -
 .../research_backup/panini_serveur_corrige.py      |    193 -
 .../research_backup/panini_simple_server.py        |    538 -
 .../research_backup/panini_size_analysis_engine.py |    620 -
 .../panini_test_corpus_generator.py                |    468 -
 .../research_backup/panini_uhd_interface.py        |    963 -
 .../panini_universal_batch_20251003_135646.json    |    312 -
 .../panini_universal_format_engine.py              |    577 -
 ...ini_validation_report_2025-10-02T22-12-15Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-15-33Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-17-18Z.json |    615 -
 ...ini_validation_report_2025-10-02T22-17-32Z.json |    615 -
 ...ini_validation_report_2025-10-03T12-24-32Z.json |    615 -
 ...ini_validation_report_2025-10-03T12-25-06Z.json |    615 -
 ...ini_validation_report_2025-10-03T13-30-03Z.json |    615 -
 ...ini_validation_report_2025-10-03T13-46-19Z.json |    615 -
 ...ini_validation_report_2025-10-03T14-10-46Z.json |    615 -
 .../research_backup/panini_validators_core.py      |    772 -
 .../panini_vfs_architecture_20251003_135649.json   |    666 -
 .../panini_virtual_fs_architecture.py              |    594 -
 .../research_backup/panini_web_backend.py          |    278 -
 .../panini_web_explorer_prototype.html             |    375 -
 .../panini_web_frontend_specs_20251003_135653.json |    118 -
 .../panini_web_interface_generator.py              |    963 -
 .../research_backup/panini_webdav_server.py        |    300 -
 .../research_backup/phase1_progress_report.json    |    818 -
 .../research_backup/phase1_session_log.json        |     17 -
 .../playwright_diagnostic_1759520886.json          |     66 -
 .../research_backup/pr11_comment.md                |     51 -
 .../research_backup/pr13_comment.md                |     87 -
 .../research_backup/pr14_comment.md                |     97 -
 .../research_backup/pr16_comment.md                |     57 -
 .../pr_compliance_report_2025-10-01T13-51-28Z.json |     55 -
 .../pr_compliance_report_2025-10-01T14-03-48Z.json |    289 -
 ...ct_essence_extraction_2025-10-01T15-42-06Z.json |    911 -
 ...tic_dashboard_summary_2025-10-02T21-20-38Z.json |     32 -
 ...emantic_orchestration_2025-10-02T21-11-00Z.json |     13 -
 ...emantic_orchestration_2025-10-02T21-11-47Z.json |     80 -
 ...emantic_orchestration_2025-10-02T21-16-38Z.json |     87 -
 .../serveur_decomposition_complete.py              |    489 -
 .../research_backup/setup_panini_research_repo.sh  |    148 -
 .../research_backup/start_phase1_monitoring.sh     |     24 -
 .../symmetry_detection_real_panini_data.json       |    308 -
 .../symmetry_detection_results.json                |    131 -
 .../research_backup/training_metrics.json          |    131 -
 .../translator_bias_style_analysis.json            |    179 -
 .../translator_database_sample.json                |     76 -
 .../translator_metadata_extraction.json            |     13 -
 .../research_backup/translators_metadata.json      |    378 -
 .../txt_extraction_2025-10-01T13-02-45Z.json       |     58 -
 test-alignement-tableaux.html                      |      1 -
 2615 files changed, 287 insertions(+), 2880425 deletions(-)
```

---


# Retention & Historical Traceability Policy

This repository maintains historical research and operational evolution while avoiding unstructured "archives" directories.

## Principles
- No top-level `archives/` directories: content is normalized into thematic history paths.
- All research progress remains traceable via `panini/references/history` and `panini/discoveries/research_notes`.
- Operational / prototype legacy scripts live under `tech/prototypes/legacy/`.
- Governance and migration evolution is stored under `tech/docs/governance/history/`.

## Current History Structure
- `panini/references/history/reports/` : Cleanup & structural reports
- `panini/references/history/experiments/` : Generated experiment PDFs (Unicode / Dhatu corpus iterations)
- `panini/references/history/indices/` : Cross-reference indices (global, research files)
- `panini/references/history/sessions/` : Conversation journals & session summaries
- `panini/references/history/syntheses/` : High-level synthesis & validation summaries
- `panini/discoveries/research_notes/` : Exploratory notes & visual alternatives
- `tech/prototypes/legacy/backups/` : Legacy analytical & generation scripts kept for reproducibility
- `tech/docs/governance/history/` : Migration plans, roadmap snapshots, templates & troubleshooting

## Reclassification (Sept 2025)
Moved from former `archives/` (now removed):
- Reports → `panini/references/history/reports/` (FINAL_CLEANUP_REPORT.md, WORKSPACE_CLEANED.md)
- Experiment PDFs → `panini/references/history/experiments/` (unicode_* / dhatu_* / test_unicode_minimal.pdf)
- Backup / legacy scripts → `tech/prototypes/legacy/backups/` (semantic_*, dhatu_*, multilingual_*, pdf_* etc.)

Root markdown rehomed:
- Governance & migration docs → `tech/docs/governance/history/`
- Indices → `panini/references/history/indices/`
- Session logs → `panini/references/history/sessions/`
- Synthesis & validation → `panini/references/history/syntheses/`
- Visual alternatives & exploratory note → `panini/discoveries/research_notes/`

## Retention Rules
| Category | Keep? | Rationale | Future Pruning |
|----------|-------|-----------|----------------|
| Reports | Yes | Structural audit traceability | Compress yearly |
| Experiment PDFs | Yes (latest 2 per theme mandatory) | Evidence of iterative design | Cull superseded after 12 months |
| Legacy scripts | Yes (frozen) | Reproducibility & reference | Move to external gist if unused 18 months |
| Session journals | Yes | Narrative continuity | Archive yearly into single digest |
| Indices | Yes | Navigation aid | Update in place |
| Synthesis / validation | Yes | Executive context | Supersede with version chain |

## Enforcement
The `verify_layout.sh` script is (to be) updated to assert absence of stray `archives` directories and ensure required history paths exist.

## Deprecation Process
1. Mark candidate file in a PR with label `retire-history`.
2. Provide justification + replacement reference.
3. On merge, move to `tech/prototypes/legacy/backups/` (if code) or compress into an annual tarball under `panini/references/history/retired/`.

## Future Enhancements
- Add checksum manifest for experiment PDFs.
- Automate quarterly pruning suggestions.
- Add provenance YAML indexing each moved asset.

(Generated automatically as part of structural cleanup September 2025.)

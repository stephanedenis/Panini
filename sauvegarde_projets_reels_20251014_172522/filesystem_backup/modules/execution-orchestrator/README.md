# ExecutionOrchestrator

Orchestre des exécutions (drivers: local, colab, cloud) et intègre `missions/` (ex-autonomous-missions).

- CLI: `exec-orch`
- API: run(mission, backend, params) -> run_id; status(run_id); cancel(run_id)

Roadmap
- drivers/local, drivers/colab, drivers/cloud
- dossier `missions/` avec catalogue
- smoke tests (CI)

## Missions: découverte + compatibilité

- Découverte automatique: les modules sous `execution_orchestrator.missions` sont détectés et chargés à la demande.
- Compatibilité legacy: les missions exposant `run()` ou `main()` sans arguments sont adaptées automatiquement (retour normalisé en code de sortie int).

## Tests

Un test smoke minimal est fourni (`tests/test_missions.py`) et exécuté dans la CI GitHub Actions.

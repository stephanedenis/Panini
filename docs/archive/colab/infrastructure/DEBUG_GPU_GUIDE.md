# 🐛 Guide Debug GPU - VSCode + Colab Tunnel

## 🚀 Setup Rapide (5 minutes)

### 1. Lancer le Tunnel sur Colab

1. **Upload notebook**: `notebooks/colab_vscode_tunnel.ipynb` sur Google Colab
2. **Select GPU runtime**: Runtime → Change runtime type → GPU
3. **Run all cells**: Runtime → Run all (`Ctrl+F9`)
4. **Authentification GitHub**: Suivre instructions cellule 3
5. **Copier URL tunnel**: Format `vscode://vscode-remote/tunnel/colab-panini-debug`

### 2. Connecter VSCode Local

**Option A: Via Extension (Recommandé)**
1. Installer extension: **Remote - Tunnels** (`ms-vscode.remote-server`)
2. `Ctrl+Shift+P` → "Remote-Tunnels: Connect to Tunnel"
3. Login GitHub
4. Sélectionner `colab-panini-debug`
5. ✅ Nouvelle fenêtre VSCode connectée à Colab!

**Option B: Via URL (Plus rapide)**
1. Cliquer sur URL `vscode://...` affichée dans Colab
2. Confirmer ouverture dans VSCode
3. ✅ Connecté!

### 3. Vérifier Configuration

Dans la nouvelle fenêtre VSCode (connectée à Colab):

```bash
# Terminal (Ctrl+`)
pwd                              # Devrait être /content/work
python -c "import torch; print(torch.cuda.get_device_name(0))"
# Output: Tesla T4 (ou V100/A100)
```

---

## 🎯 Debugging Workflow

### Exemple 1: Debug Script Simple

**Fichier**: `experiments/debug_gpu_example.py`

1. **Ouvrir fichier** dans VSCode (fenêtre tunnel)
2. **Mettre breakpoint**: Clic gauche à côté ligne 41 (`device = check_gpu_availability()`)
3. **Lancer debug**: `F5` ou Run → Start Debugging
4. **Choisir config**: "🔧 Debug GPU Example"
5. **Observer exécution**:
   - Code pause au breakpoint (ligne jaune)
   - Panel **Variables** montre toutes les variables locales
   - Panel **Call Stack** montre pile d'appels
   - Panel **Watch** pour expressions custom

6. **Contrôles**:
   - `F5` = Continue (jusqu'au prochain breakpoint)
   - `F10` = Step Over (ligne suivante)
   - `F11` = Step Into (entrer dans fonction)
   - `Shift+F11` = Step Out (sortir de fonction)
   - `Shift+F5` = Stop debugging

7. **Inspecter variables**:
   - Hover souris sur variable → voir valeur
   - Dans panel Variables → expand objets
   - Dans Debug Console → taper expressions:
     ```python
     >>> device
     >>> torch.cuda.memory_allocated() / 1e9
     >>> x.shape if 'x' in locals() else "Not defined"
     ```

### Exemple 2: Debug Audio Fingerprinting

**Fichier**: `experiments/benchmark_audio_fingerprinting.py`

1. **Breakpoint ligne 87**: `audio_data = generate_test_audio(...)`
2. **F5** → Choisir "🎯 Debug Audio Fingerprinting"
3. **F10** jusqu'à ligne 92: `metrics = benchmark_fingerprinting(...)`
4. **F11** pour entrer dans `benchmark_fingerprinting()`
5. **Observer** dans Variables:
   - `audio_files` (list de paths)
   - `device_name` (str)
6. **Continue F10** dans la fonction
7. **Watch** expressions utiles:
   - `len(audio_files)`
   - `torch.cuda.memory_allocated() / 1e9`
   - `metrics if 'metrics' in locals() else {}`

### Exemple 3: Conditional Breakpoints

**Use case**: Debugger seulement certaines itérations

1. **Breakpoint** dans une boucle (ex: ligne 150 dans example)
2. **Right-click sur breakpoint** → "Edit Breakpoint..."
3. **Expression**: `i == 5` (s'arrête seulement si i vaut 5)
4. **Hit Count**: `10` (s'arrête après 10 passages)
5. **Log Message**: `"Iteration {i}: value={x.mean()}"` (log sans arrêter)

**Exemples d'expressions**:
```python
# S'arrêter si tensor contient NaN
torch.isnan(x).any()

# S'arrêter si mémoire > 5GB
torch.cuda.memory_allocated() > 5e9

# S'arrêter sur fichier spécifique
"audio_01.wav" in filename

# S'arrêter si erreur métrique
abs(metric - target) > threshold
```

### Exemple 4: Debug Memory Leaks

**Fichier**: `experiments/debug_gpu_example.py` → fonction `example_memory_debugging()`

1. **Watch expressions**:
   - `torch.cuda.memory_allocated() / 1e9`
   - `torch.cuda.max_memory_allocated() / 1e9`
   - `torch.cuda.memory_reserved() / 1e9`

2. **Breakpoints**:
   - Ligne 231: Avant `tensor1 = ...`
   - Ligne 236: Avant `tensor2 = ...`
   - Ligne 243: Après `del tensor1`
   - Ligne 249: Après `del tensor2`

3. **Observer Watch** à chaque breakpoint:
   - Memory augmente après allocations
   - Memory diminue après `del` + `empty_cache()`
   - Si memory ne diminue pas → leak!

4. **Analyser**:
   - Variables panel → chercher tensors non libérés
   - Call Stack → identifier où tensor est créé
   - Debug Console → `gc.get_referrers(tensor1)`

### Exemple 5: Profiling avec Debugging

**Use case**: Trouver bottlenecks GPU

1. **Lancer** avec config "📊 Debug with Profiling"
   - Active `CUDA_LAUNCH_BLOCKING=1` (synchronise CPU/GPU)
   - Active `TORCH_SHOW_CPP_STACKTRACES=1` (stack traces détaillées)

2. **Breakpoint** après `with profile(...) as prof:`

3. **Debug Console** pour analyser:
   ```python
   >>> prof.key_averages().table(sort_by="cuda_time_total")
   >>> prof.key_averages(group_by_input_shape=True)
   >>> prof.export_chrome_trace("trace.json")
   ```

4. **Identifier bottleneck**:
   - Operations avec plus haut `cuda_time_total`
   - Operations appelées trop souvent
   - Transferts CPU↔GPU inutiles

---

## 🎨 Configurations Debug Disponibles

Dans `.vscode/launch.json`:

| Config | Usage | Args |
|--------|-------|------|
| 🔧 Debug GPU Example | Script démo debug GPU | - |
| 🎯 Debug Audio Fingerprinting | Benchmark audio | `--num-samples 10` |
| 🧪 Debug Current File | Fichier ouvert | - |
| 📊 Debug with Profiling | Profiling détaillé | CUDA_LAUNCH_BLOCKING |
| 🐛 Debug with Memory Tracking | Memory debugging | max_split_size_mb:512 |
| 🧮 Debug Tests | Tests pytest | `-v -s` |

**Modifier config**:
```json
{
  "name": "Mon Config Custom",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/mon_script.py",
  "args": ["--arg1", "value1"],
  "env": {
    "MY_VAR": "value"
  }
}
```

---

## 💡 Tips & Tricks

### Variables Panel
- **Expand** objets complexes (tensors, dicts, lists)
- **Copy Value** (right-click) pour coller dans code
- **Set Value** (double-click) pour modifier pendant debug

### Watch Expressions
**Expressions utiles**:
```python
# GPU
torch.cuda.memory_allocated() / 1e9
torch.cuda.get_device_name(0)
torch.cuda.is_available()

# Tensors
x.shape if 'x' in locals() else None
x.device if 'x' in locals() else None
x.dtype if 'x' in locals() else None
x.min().item() if 'x' in locals() else None
x.max().item() if 'x' in locals() else None
x.mean().item() if 'x' in locals() else None

# Model
sum(p.numel() for p in model.parameters())
[p.shape for p in model.parameters()]
next(model.parameters()).device

# Lists
len(my_list) if 'my_list' in locals() else 0
[type(x) for x in my_list] if 'my_list' in locals() else []
```

### Debug Console
**Commandes utiles**:
```python
# Importer modules
>>> import torch
>>> import numpy as np

# Exécuter code
>>> new_tensor = torch.randn(10, 10, device='cuda')
>>> print(new_tensor.mean())

# Inspecter objets
>>> dir(model)
>>> type(x)
>>> vars(object)

# Aide
>>> help(torch.cuda.memory_allocated)
```

### Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| Toggle breakpoint | `F9` |
| Start debugging | `F5` |
| Continue | `F5` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Stop | `Shift+F5` |
| Restart | `Ctrl+Shift+F5` |

### Logpoints
**Alternative aux breakpoints** (log sans arrêter):

1. Right-click ligne → "Add Logpoint"
2. Message: `"Iteration {i}, loss={loss.item()}"`
3. Code continue, messages dans Debug Console

**Use case**: Logger 1000 itérations sans breakpoint

---

## 🔧 Troubleshooting

### Breakpoints ignorés (grisés)
**Causes**:
- Python interpreter incorrect
- Module pas trouvé
- Code pas synchronisé

**Fix**:
```bash
# Terminal VSCode (tunnel)
cd /content/work
git pull origin gpu-experiments
pip install -r requirements.txt
```

### Variables not available
**Cause**: `justMyCode: true` cache variables externes

**Fix**: Dans `.vscode/launch.json`:
```json
"justMyCode": false
```

### "CUDA out of memory"
**Fix**:
```python
# Avant ligne problématique
torch.cuda.empty_cache()

# Dans Debug Console pendant pause
>>> torch.cuda.empty_cache()
>>> torch.cuda.memory_allocated() / 1e9
```

### Debugging très lent
**Causes**:
- `CUDA_LAUNCH_BLOCKING=1` (synchronise tout)
- Trop de Watch expressions
- Logpoints dans boucles serrées

**Fix**:
- Utiliser config normale (pas "Profiling")
- Limiter Watch expressions
- Conditional breakpoints au lieu de logpoints

### Tunnel disconnected
**Fix**:
1. Colab: Re-run notebook cells
2. VSCode: `Ctrl+Shift+P` → "Remote-Tunnels: Connect to Tunnel"
3. Sélectionner `colab-panini-debug`

---

## 📊 Workflow Complet: Dev → Debug → Prod

### Phase 1: Développement Local (CPU)
```bash
# Local VSCode (sans Colab)
vim experiments/nouveau_script.py

# Tester localement (CPU)
python experiments/nouveau_script.py
```

### Phase 2: Debug GPU (Colab Tunnel)
```bash
# 1. Push code
git add experiments/nouveau_script.py
git commit -m "feat: nouveau script GPU"
git push origin gpu-experiments

# 2. Colab: Pull dans tunnel
cd /content/work
git pull origin gpu-experiments

# 3. VSCode (tunnel): Debug avec GPU
# F5 → Debugger interactivement
```

### Phase 3: Validation Batch (Colab Daemon)
```bash
# Ajouter à experiments.json
{
  "name": "nouveau_script_validation",
  "command": "python experiments/nouveau_script.py --full-dataset",
  "status": "pending",
  "timeout": 3600
}

# Commit
git add experiments.json
git commit -m "exp: validation nouveau script"
git push origin gpu-experiments

# Daemon Colab exécute automatiquement
```

### Phase 4: Production
```bash
# Merge vers main après validation
git checkout main
git merge gpu-experiments
git push origin main
```

---

## 🆘 Support

**Tunnel ne fonctionne pas?**
→ Voir `docs/infrastructure/SOLUTION_COMPARISON.md`

**Préférez batch processing?**
→ Utiliser `notebooks/colab_gpu_daemon.ipynb` (Solution 2)

**Questions GPU?**
→ `experiments/debug_gpu_example.py` contient plein d'exemples

---

**Prêt à debugger? Upload `colab_vscode_tunnel.ipynb` sur Colab et c'est parti! 🚀**

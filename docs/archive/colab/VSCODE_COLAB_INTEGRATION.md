# VSCode + Colab Direct Integration Guide

## Overview

This guide explains how to use the **Google Colab VSCode extension** to achieve **full autonomy** for experiment execution, debugging, and development directly from VSCode without relying on the daemon.

## Architecture

```
VSCode (Local)
    ↓
Google Colab Extension
    ↓
Colab Runtime (Cloud GPU/TPU)
    ↓
Panini Experiments (E1, E2, ...)
    ↓
Results (JSON) → GitHub Push
```

## Quick Setup (5 minutes)

### Step 1: Install Extension
The **Google Colab** extension (`google.colab`) is already installed. Verify:
- Extensions view (`Ctrl+Shift+X`)
- Search "Google Colab"
- Should show: ✅ Installed

### Step 2: Open Notebook in VSCode
```
File → Open File
Select: notebooks/vscode_colab_direct.ipynb
```

### Step 3: Select Colab Kernel
- Click **"Select Kernel"** button (top right of notebook)
- Choose **"Colab"**
- Select **"New Colab Server"**
- When prompted: **Sign in with Google account**
- Wait for connection (30-60 seconds)

### Step 4: Execute Cells
- Click ▶️ on any cell to execute
- Output appears directly in VSCode
- Can modify and re-run interactively

## Benefits vs Daemon

| Feature | Daemon | VSCode+Colab |
|---------|--------|--------------|
| Real-time Feedback | ❌ Async (logs) | ✅ Interactive |
| Interactive Debugging | ❌ No | ✅ Yes (modify & rerun) |
| Code Modification | ❌ Commit→Push→Detect | ✅ Direct |
| GPU Access | ✅ Yes | ✅ Yes + Selection |
| Development Speed | 🔄 Slow (60s poll) | ⚡ Instant |
| Autonomy | ⚙️ Daemon (no user input) | 👤 User-interactive |

## Usage Examples

### Example 1: Run E1 Experiment
```python
# In VSCode cell:
import subprocess
from pathlib import Path

# Execute E1
result = subprocess.run(
    ['python3', 'experiments/e1_format_decomposition.py', '--phase', 'all'],
    capture_output=True,
    text=True,
    cwd='/content/panini-vscode'
)

print(result.stdout)
print(f"Exit code: {result.returncode}")
```

### Example 2: Debug Script
```python
# In VSCode cell (interactive):
import sys
sys.path.insert(0, '/content/panini-vscode')

# Import and run function directly (no subprocess)
from experiments.e1_format_decomposition import generate_minimal_corpus
from pathlib import Path

corpus_dir = Path('/tmp/debug_corpus')
generate_minimal_corpus(corpus_dir)
print(f"✅ Corpus created with {len(list(corpus_dir.rglob('*')))} items")
```

### Example 3: Visualize Results
```python
import json
from pathlib import Path

results = json.load(open('/content/panini-vscode/outputs/e1_results.json'))

# Create summary
for phase, data in results['phases'].items():
    print(f"{phase}: {data['status'].upper()} ✅" if data['status']=='pass' else f"{phase}: FAILED ❌")
    if 'data' in data:
        print(f"  → {list(data['data'].keys())}")
```

## Workflow Comparison

### Daemon Workflow
```
Edit code locally
  ↓
git push origin gpu-experiments
  ↓
daemon detects commit (60s wait)
  ↓
daemon executes
  ↓
daemon auto-commits results
  ↓
pull results
```
**Total Time: 2-5 minutes** (including daemon polling delay)

### VSCode+Colab Workflow
```
Open notebook in VSCode
  ↓
Select Colab kernel
  ↓
Modify & execute cells directly
  ↓
See results instantly
  ↓
git push final code + results
```
**Total Time: 30-60 seconds** (for first connection)

## When to Use Each

### Use **Daemon** When:
- You want fully autonomous batch processing
- Running 24/7 monitoring
- No user interaction needed
- Results auto-saved to GitHub
- E.g., `experiments.json` with multiple tasks

### Use **VSCode+Colab** When:
- Developing & debugging
- Interactive experimentation
- Testing code changes rapidly
- Learning and exploration
- Manual verification of results

## Advanced: Combine Both

**Optimal Hybrid Workflow:**

```
Development Phase:
  VSCode + Colab → Test & iterate → Debug interactively

Production Phase:
  Register in experiments.json → Daemon auto-executes → Results saved
```

Example:
1. Use VSCode+Colab to develop E2 experiment
2. Test on mini-corpus interactively
3. Once stable: Add to `experiments.json` with larger corpus
4. Daemon runs autonomously overnight
5. Results available next morning

## Keyboard Shortcuts (VSCode Notebooks)

| Action | Shortcut |
|--------|----------|
| Execute Cell | `Ctrl+Enter` or `Shift+Enter` |
| Add Cell Below | `Ctrl+Shift+Enter` |
| Add Cell Above | `Ctrl+Shift+Alt+Enter` |
| Delete Cell | `Ctrl+Shift+K` |
| Move Cell Up/Down | `Alt+↑/↓` |
| Open Command Palette | `Ctrl+Shift+P` |

## Troubleshooting

### Issue: "Sign in failed"
**Solution**: 
```
Cmd/Ctrl+Shift+P → "Colab: Sign Out"
→ Try again → Should prompt for Google login
```

### Issue: "Connection timeout"
**Solution**:
```
1. Close notebook tab
2. Wait 30 seconds
3. Re-open notebook
4. Select Kernel again
5. May need to create new Colab server
```

### Issue: "Module not found" (e.g., `from experiments.e1_format_decomposition`)
**Solution**:
```python
# At start of notebook:
import subprocess
from pathlib import Path

# Clone repo
subprocess.run(['git', 'clone', 'https://github.com/stephanedenis/Panini.git', '/content/panini'],
               cwd='/content')

import sys
sys.path.insert(0, '/content/panini')
```

## Performance Tips

1. **First execution slower** (compilation, auth): ~30-60s
2. **Subsequent cells faster**: ~2-5s per cell
3. **GPU warm-up**: First GPU operation takes ~5s
4. **Use conda cells** (%%bash -c "...") for shell commands

## Example: Full Development Cycle

```python
# Cell 1: Setup
import subprocess, sys
from pathlib import Path

repo = Path('/content/panini')
if not repo.exists():
    subprocess.run(['git', 'clone', 'https://github.com/stephanedenis/Panini.git', str(repo)])

sys.path.insert(0, str(repo))

# Cell 2: Import experiment
from experiments.e1_format_decomposition import generate_minimal_corpus, ExperimentLogger

# Cell 3: Test generate_minimal_corpus
corpus = Path('/tmp/test')
generate_minimal_corpus(corpus)
print(f"Created {len(list(corpus.glob('*')))} format dirs")

# Cell 4: Run full E1
import subprocess
result = subprocess.run(['python3', 'experiments/e1_format_decomposition.py', '--phase', 'all'],
                       cwd=str(repo), capture_output=True, text=True)
print(result.stdout)

# Cell 5: Analyze results
import json
results = json.load(open(repo / 'outputs/e1_results.json'))
print(f"Status: {results['overall_status']}")
```

## Next Steps

1. ✅ Open `notebooks/vscode_colab_direct.ipynb`
2. ✅ Click "Select Kernel" → "Colab"
3. ✅ Sign in with Google
4. ✅ Execute cells one by one
5. ✅ Modify cell 2 to test different params
6. ✅ Use for interactive development

## Resources

- [Google Colab Extension Docs](https://marketplace.visualstudio.com/items?itemName=Google.colab)
- [Colab in VSCode Announcement](https://developers.googleblog.com/google-colab-is-coming-to-vs-code)
- [VSCode Jupyter Support](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

---

**TL;DR**: For interactive development & debugging → **VSCode+Colab**. For autonomous batch processing → **Daemon**. Combine both for optimal workflow!

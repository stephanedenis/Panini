# 🚀 Quick Start - Colab GPU Experiments

## Step-by-Step Guide

### 1. Upload Notebook to Colab

**Option A - Lien Direct (Recommandé)** ⚡:
1. Cliquez: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/Panini/blob/gpu-experiments/notebooks/colab_gpu_daemon_lite.ipynb)
2. ✅ Notebook ouvert dans Colab !

**Option B - Upload Manuel**:
1. Open **Google Colab**: https://colab.research.google.com/
2. Click **File → Upload notebook**
3. Select: `notebooks/colab_gpu_daemon_lite.ipynb` from your local Panini folder
4. ✅ Notebook uploaded!

**Avantage Lite**: Clone partiel = **10x plus rapide** (25MB vs 500MB)

### 2. Select GPU Runtime
1. Click **Runtime → Change runtime type**
2. Select **Hardware accelerator: GPU**
3. Choose **GPU type: T4** (minimum - or V100/A100 if available)
4. Click **Save**
5. ✅ GPU activated!

### 3. Run All Cells
1. Click **Runtime → Run all** (or `Ctrl+F9`)
2. **First prompt**: Mount Google Drive
   - Click "Connect to Google Drive"
   - Select your Google account
   - Click "Allow"
3. **Second prompt**: Git credentials
   - Username: `stephanedenis`
   - Token: Your GitHub Personal Access Token
   - (Token needs `repo` scope for private repos)

### 4. Watch the Magic! 🎩✨

The daemon will:
1. ✅ **Clone repo** from `gpu-experiments` branch
2. ✅ **Detect commit** `05406553` (your audio fingerprinting experiments)
3. ✅ **Execute experiments**:
   - `audio_fingerprint_basic_test` (~30s)
   - `audio_fingerprint_performance_benchmark` (~2min)
4. ✅ **Save results** to Google Drive
5. ✅ **Push results** back to GitHub

### 5. Monitor Progress

**In Colab** (scroll to monitoring cells):
- **Cell 8**: View daemon logs (real-time)
- **Cell 9**: Check experiments status
- **Cell 10**: List output files
- **Cell 11**: GPU utilization

**Expected logs**:
```
🔄 Daemon démarré - Watching repo...
🆕 Nouveau commit détecté: 05406553
🚀 Lancement: audio_fingerprint_basic_test
✅ Terminé: audio_fingerprint_basic_test
🚀 Lancement: audio_fingerprint_performance_benchmark
✅ Terminé: audio_fingerprint_performance_benchmark
📤 Résultats poussés vers GitHub
```

### 6. Pull Results Locally

**Back in your local VSCode**:

```bash
cd /home/stephane/GitHub/Panini

# Pull results
./tools/sync_colab_results.sh

# Check updated experiments.json
cat experiments.json
```

**Expected status**:
```json
[
  {
    "name": "audio_fingerprint_basic_test",
    "status": "completed",
    "output": "... test results ..."
  },
  {
    "name": "audio_fingerprint_performance_benchmark", 
    "status": "completed",
    "output": "... benchmark metrics ..."
  }
]
```

### 7. View Metrics

```bash
# Benchmark results
ls outputs/benchmark_audio_fingerprinting/

# Expected files:
# - benchmark_cpu_20251113_*.json  (if CPU fallback)
# - benchmark_gpu_20251113_*.json  (GPU metrics)
# - timing_comparison.json
```

---

## 🔧 Troubleshooting

### "Git credentials invalid"
**Fix**: Generate new GitHub token
1. https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (full control)
4. Copy token and paste in Colab

### "No experiments to run"
**Fix**: Commit detected was already processed
- Make a small change to experiments.json
- Commit and push
- Daemon will detect new commit

### "Module not found"
**Fix**: Install dependencies
```python
# Add cell after "Clone repo":
!pip install -r work/requirements.txt
```

### "Timeout exceeded"
**Fix**: Increase timeout in experiments.json
```json
{
  "name": "...",
  "timeout": 1200  // 20 minutes instead of 10
}
```

---

## 📊 What to Expect

### Performance Metrics (100 audio files)

| Metric | CPU (Local) | GPU (T4) | GPU (V100) |
|--------|-------------|----------|------------|
| Extraction | ~120s | ~15s | ~8s |
| Indexing | ~5s | ~2s | ~1s |
| Search | ~0.8s | ~0.3s | ~0.15s |
| **Total** | **~126s** | **~17s** | **~9s** |

**Speedup**: 7-14x faster on GPU! 🚀

---

## 🎯 Next Steps After Success

1. **Scale up**: Change `--num-samples 100` to `--num-samples 1000`
2. **Real audio**: Replace synthetic audio with real MP3/FLAC files
3. **Optimize**: Profile bottlenecks with PyTorch profiler
4. **Deploy**: Use results to optimize production code

---

## 🆘 Need Help?

**Colab session expired?**
- Just re-run all cells
- Daemon will resume from where it stopped

**Want to stop daemon?**
- Click the ⏹️ Stop button in the daemon cell
- Or: Interrupt kernel (`Runtime → Interrupt execution`)

**Check Colab logs**:
```bash
# In Colab cell:
!tail -f /content/daemon.log
```

---

**Ready? Go upload that notebook and watch the magic happen! 🎩✨**

"""
Exemple de script pour debugging GPU avec VSCode + Colab Tunnel

Ce script démontre comment debugger du code GPU interactivement:
- Breakpoints
- Step trace (F10/F11)
- Variables inspection
- GPU memory monitoring
"""

import torch
import numpy as np
from pathlib import Path
import time


def check_gpu_availability():
    """Vérifier disponibilité GPU et afficher infos"""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        gpu_name = torch.cuda.get_device_name(0)
        total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        
        print(f"✅ GPU disponible: {gpu_name}")
        print(f"   VRAM totale: {total_memory:.1f} GB")
        return device
    else:
        print("⚠️ GPU non disponible - Utilisation CPU")
        return torch.device("cpu")


def example_tensor_operations(device, size=1000):
    """
    Exemple d'opérations tenseurs sur GPU
    
    DEBUGGING TIPS:
    1. Mettre breakpoint sur ligne 'x = torch.randn(...)'
    2. F10 pour step over chaque ligne
    3. Hover sur variables pour voir valeurs
    4. Dans Watch panel, ajouter: torch.cuda.memory_allocated() / 1e9
    """
    print(f"\n🔢 Création tenseurs {size}x{size} sur {device}")
    
    # BREAKPOINT ICI - Observer device et size
    x = torch.randn(size, size, device=device)
    
    # F10 - Observer x.shape dans Variables panel
    y = torch.randn(size, size, device=device)
    
    # F10 - Voir memory_allocated augmenter dans Watch
    print(f"   Mémoire utilisée: {torch.cuda.memory_allocated() / 1e9:.3f} GB")
    
    # F10 - Operation matrix multiplication
    start = time.time()
    z = x @ y  # Breakpoint: voir temps execution
    elapsed = time.time() - start
    
    print(f"   Multiplication {size}x{size}: {elapsed*1000:.2f} ms")
    print(f"   Result shape: {z.shape}")
    
    return z


def example_batch_processing(device, batch_size=32, num_batches=10):
    """
    Exemple de batch processing avec monitoring GPU
    
    DEBUGGING TIPS:
    1. Conditional breakpoint sur ligne 'batch = ...'
       Expression: i == 5 (s'arrête seulement au batch 5)
    2. Dans Debug Console, taper: batch.mean().item()
    3. Watch expression: torch.cuda.max_memory_allocated() / 1e9
    """
    print(f"\n📊 Batch processing: {num_batches} batches de {batch_size}")
    
    results = []
    
    for i in range(num_batches):
        # CONDITIONAL BREAKPOINT: i == 5
        batch = torch.randn(batch_size, 1000, device=device)
        
        # Traitement batch
        processed = torch.nn.functional.relu(batch)
        result = processed.mean(dim=1)
        
        results.append(result)
        
        # Monitoring
        if (i + 1) % 5 == 0:
            mem_used = torch.cuda.memory_allocated() / 1e9
            print(f"   Batch {i+1}/{num_batches}: {mem_used:.3f} GB utilisés")
    
    # Concatenate results
    final_result = torch.cat(results, dim=0)
    print(f"   Result final shape: {final_result.shape}")
    
    return final_result


def example_model_forward(device, input_size=1000, hidden_size=512):
    """
    Exemple de forward pass d'un modèle simple
    
    DEBUGGING TIPS:
    1. Breakpoint sur 'output = model(x)'
    2. F11 (Step Into) pour entrer dans le forward du modèle
    3. Dans Variables, explorer model.parameters()
    4. Debug Console: list(model.parameters())[0].shape
    """
    print(f"\n🧠 Création modèle simple sur {device}")
    
    # Modèle simple
    model = torch.nn.Sequential(
        torch.nn.Linear(input_size, hidden_size),
        torch.nn.ReLU(),
        torch.nn.Linear(hidden_size, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10)
    ).to(device)
    
    # Input batch
    x = torch.randn(32, input_size, device=device)
    
    # BREAKPOINT ICI - F11 pour step into
    with torch.no_grad():
        output = model(x)  # Step Into avec F11
    
    print(f"   Model output shape: {output.shape}")
    print(f"   Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    return output


def example_profiling(device, size=2000):
    """
    Exemple de profiling GPU avec torch.profiler
    
    DEBUGGING TIPS:
    1. Breakpoint après 'with profile(...)'
    2. Inspecter 'prof' dans Variables
    3. Examiner prof.key_averages() dans Debug Console
    """
    print(f"\n📈 Profiling opérations GPU")
    
    from torch.profiler import profile, ProfilerActivity
    
    # BREAKPOINT APRÈS CE WITH
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
        x = torch.randn(size, size, device=device)
        y = torch.randn(size, size, device=device)
        
        # Operations à profiler
        z1 = x @ y  # Matrix mult
        z2 = torch.nn.functional.relu(z1)  # ReLU
        z3 = z2.sum()  # Reduction
    
    # Afficher résultats
    print("\n   Top 5 operations (CUDA time):")
    print(prof.key_averages().table(
        sort_by="cuda_time_total",
        row_limit=5
    ))
    
    return prof


def example_memory_debugging(device):
    """
    Exemple de debugging memory leaks
    
    DEBUGGING TIPS:
    1. Watch: torch.cuda.memory_allocated() / 1e9
    2. Watch: torch.cuda.memory_reserved() / 1e9
    3. Breakpoint après chaque allocation
    4. Observer si memory est libérée correctement
    """
    print(f"\n💾 Memory debugging")
    
    # État initial
    torch.cuda.empty_cache()
    initial_mem = torch.cuda.memory_allocated()
    print(f"   Mémoire initiale: {initial_mem / 1e9:.3f} GB")
    
    # Allocation 1
    tensor1 = torch.randn(1000, 1000, device=device)
    mem_after_1 = torch.cuda.memory_allocated()
    print(f"   Après tensor1: {mem_after_1 / 1e9:.3f} GB (+{(mem_after_1 - initial_mem) / 1e6:.1f} MB)")
    
    # Allocation 2
    tensor2 = torch.randn(2000, 2000, device=device)
    mem_after_2 = torch.cuda.memory_allocated()
    print(f"   Après tensor2: {mem_after_2 / 1e9:.3f} GB (+{(mem_after_2 - mem_after_1) / 1e6:.1f} MB)")
    
    # BREAKPOINT ICI - Observer memory avant del
    del tensor1
    torch.cuda.empty_cache()
    mem_after_del1 = torch.cuda.memory_allocated()
    print(f"   Après del tensor1: {mem_after_del1 / 1e9:.3f} GB (-{(mem_after_2 - mem_after_del1) / 1e6:.1f} MB)")
    
    # BREAKPOINT ICI - Observer memory après del
    del tensor2
    torch.cuda.empty_cache()
    final_mem = torch.cuda.memory_allocated()
    print(f"   Mémoire finale: {final_mem / 1e9:.3f} GB")
    
    # Vérifier pas de leak
    leak = final_mem - initial_mem
    if leak < 1e6:  # < 1 MB
        print(f"   ✅ Pas de memory leak détecté")
    else:
        print(f"   ⚠️ Memory leak possible: {leak / 1e6:.1f} MB")


def main():
    """
    Point d'entrée principal
    
    DEBUGGING WORKFLOW:
    1. Mettre breakpoint sur 'device = check_gpu_availability()'
    2. F5 pour lancer en mode debug
    3. F10 pour step through chaque fonction
    4. F11 pour step into une fonction
    5. Observer Variables panel et Watch expressions
    """
    print("="*60)
    print("🔧 Exemple Debug GPU avec VSCode + Colab Tunnel")
    print("="*60)
    
    # BREAKPOINT ICI - Début du programme
    device = check_gpu_availability()
    
    if not torch.cuda.is_available():
        print("\n⚠️ Ce script nécessite un GPU")
        print("   Vérifiez: Runtime → Change runtime type → GPU")
        return
    
    # Exemples à debugger
    try:
        # BREAKPOINT sur chaque appel pour choisir lequel debugger
        example_tensor_operations(device, size=1000)
        
        example_batch_processing(device, batch_size=16, num_batches=5)
        
        example_model_forward(device, input_size=1000, hidden_size=256)
        
        example_profiling(device, size=1500)
        
        example_memory_debugging(device)
        
        print("\n✅ Tous les exemples terminés!")
        
    except Exception as e:
        # BREAKPOINT ICI en cas d'erreur
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print(f"\n📊 Mémoire GPU finale: {torch.cuda.memory_allocated() / 1e9:.3f} GB")


if __name__ == "__main__":
    # WATCH EXPRESSIONS À AJOUTER:
    # - torch.cuda.memory_allocated() / 1e9
    # - torch.cuda.max_memory_allocated() / 1e9
    # - torch.cuda.memory_reserved() / 1e9
    
    main()

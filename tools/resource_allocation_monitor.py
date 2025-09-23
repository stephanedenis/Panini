#!/usr/bin/env python3
"""
🎯 EXTENSION DASHBOARD: AFFECTATION RESSOURCES GPU
Affichage détaillé de l'utilisation et affectation des ressources dual-GPU
"""

import subprocess
import json
import psutil
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

class ResourceAllocationMonitor:
    """Moniteur spécialisé pour l'affectation des ressources"""
    
    def __init__(self):
        self.workspace = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.gpu_processes = {}
        self.cpu_affinity_map = {}
        
    def get_gpu_allocations(self) -> Dict[str, Any]:
        """Obtient l'affectation détaillée des GPUs"""
        allocations = {
            "hd7750": {
                "card_path": "/dev/dri/card0",
                "render_node": "/dev/dri/renderD128", 
                "primary_role": "Display/Desktop",
                "current_processes": [],
                "utilization": 0,
                "memory_used": 0,
                "temperature": 0
            },
            "rx480": {
                "card_path": "/dev/dri/card1", 
                "render_node": "/dev/dri/renderD129",
                "primary_role": "Compute/Research",
                "current_processes": [],
                "utilization": 0,
                "memory_used": 0,
                "temperature": 0
            }
        }
        
        # Scan des processus utilisant les GPUs
        self._scan_gpu_processes(allocations)
        
        # Métriques hardware
        self._get_gpu_metrics(allocations)
        
        return allocations
    
    def _scan_gpu_processes(self, allocations: Dict[str, Any]):
        """Scanne les processus utilisant chaque GPU"""
        try:
            # Utiliser lsof pour voir qui utilise les devices GPU
            for gpu_name, gpu_info in allocations.items():
                for device in [gpu_info["card_path"], gpu_info["render_node"]]:
                    result = subprocess.run(
                        ["sudo", "lsof", device], 
                        capture_output=True, text=True, timeout=5
                    )
                    
                    if result.stdout:
                        lines = result.stdout.strip().split('\n')[1:]  # Skip header
                        for line in lines:
                            parts = line.split()
                            if len(parts) >= 2:
                                process_name = parts[0]
                                pid = parts[1]
                                
                                # Obtenir plus d'infos sur le processus
                                try:
                                    p = psutil.Process(int(pid))
                                    process_info = {
                                        "name": process_name,
                                        "pid": pid,
                                        "command": ' '.join(p.cmdline()),
                                        "cpu_percent": p.cpu_percent(),
                                        "memory_mb": p.memory_info().rss / 1024 / 1024,
                                        "status": p.status()
                                    }
                                    allocations[gpu_name]["current_processes"].append(process_info)
                                except (psutil.NoSuchProcess, ValueError):
                                    pass
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"Erreur scan GPU processes: {e}")
    
    def _get_gpu_metrics(self, allocations: Dict[str, Any]):
        """Obtient les métriques hardware des GPUs"""
        gpu_mapping = {
            "hd7750": {"sysfs": "/sys/class/drm/card0/device", "pci": "04:00.0"},
            "rx480": {"sysfs": "/sys/class/drm/card1/device", "pci": "03:00.0"}
        }
        
        for gpu_name, gpu_info in allocations.items():
            sysfs_path = gpu_mapping[gpu_name]["sysfs"]
            
            try:
                # Température
                temp_pattern = f"{sysfs_path}/hwmon/hwmon*/temp1_input"
                temp_result = subprocess.run(
                    f"ls {temp_pattern} 2>/dev/null | head -1", 
                    shell=True, capture_output=True, text=True
                )
                if temp_result.stdout.strip():
                    with open(temp_result.stdout.strip(), 'r') as f:
                        temp = int(f.read().strip()) / 1000
                        allocations[gpu_name]["temperature"] = temp
                
                # Utilisation GPU
                usage_file = f"{sysfs_path}/gpu_busy_percent"
                if Path(usage_file).exists():
                    with open(usage_file, 'r') as f:
                        allocations[gpu_name]["utilization"] = int(f.read().strip())
                
                # Mémoire GPU (approximation)
                mem_info_file = f"{sysfs_path}/mem_info_vram_used"
                if Path(mem_info_file).exists():
                    with open(mem_info_file, 'r') as f:
                        allocations[gpu_name]["memory_used"] = int(f.read().strip())
                        
            except Exception as e:
                print(f"Erreur métriques GPU {gpu_name}: {e}")
    
    def get_cpu_thread_allocations(self) -> Dict[str, Any]:
        """Obtient l'affectation des threads CPU"""
        allocations = {
            "total_cores": psutil.cpu_count(logical=False),
            "total_threads": psutil.cpu_count(logical=True),
            "per_core_usage": psutil.cpu_percent(percpu=True),
            "thread_assignments": {},
            "panini_processes": []
        }
        
        # Scan des processus PaniniFS et leur affectation
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_affinity', 'cpu_percent']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if any(keyword in cmdline.lower() for keyword in ['panini', 'dhatu', 'corpus']):
                    process_info = {
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "command": cmdline[:100] + "..." if len(cmdline) > 100 else cmdline,
                        "cpu_affinity": proc.info['cpu_affinity'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "cores_assigned": len(proc.info['cpu_affinity']) if proc.info['cpu_affinity'] else 0
                    }
                    allocations["panini_processes"].append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return allocations
    
    def get_memory_allocations(self) -> Dict[str, Any]:
        """Obtient l'affectation détaillée de la mémoire"""
        memory = psutil.virtual_memory()
        
        allocations = {
            "total_gb": round(memory.total / 1024**3, 1),
            "used_gb": round(memory.used / 1024**3, 1),
            "available_gb": round(memory.available / 1024**3, 1),
            "percent_used": memory.percent,
            "per_process_top10": [],
            "panini_memory_usage": 0
        }
        
        # Top 10 processus par mémoire
        processes = []
        panini_total = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                cmdline = ' '.join(proc.info['cmdline'] or [])
                
                # Compter mémoire PaniniFS
                if any(keyword in cmdline.lower() for keyword in ['panini', 'dhatu', 'corpus']):
                    panini_total += memory_mb
                
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "memory_mb": round(memory_mb, 1),
                    "command": cmdline[:80] + "..." if len(cmdline) > 80 else cmdline
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Trier et prendre top 10
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        allocations["per_process_top10"] = processes[:10]
        allocations["panini_memory_usage"] = round(panini_total, 1)
        
        return allocations
    
    def get_disk_allocations(self) -> Dict[str, Any]:
        """Obtient l'affectation des disques"""
        allocations = {
            "workspace_usage": {},
            "system_disks": [],
            "io_activity": {}
        }
        
        # Usage du workspace PaniniFS
        if self.workspace.exists():
            total_size = 0
            file_counts = {"json": 0, "py": 0, "md": 0, "log": 0, "other": 0}
            
            for file_path in self.workspace.rglob("*"):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    total_size += size
                    
                    ext = file_path.suffix.lower()
                    if ext == ".json":
                        file_counts["json"] += 1
                    elif ext == ".py":
                        file_counts["py"] += 1  
                    elif ext == ".md":
                        file_counts["md"] += 1
                    elif ext == ".log":
                        file_counts["log"] += 1
                    else:
                        file_counts["other"] += 1
            
            allocations["workspace_usage"] = {
                "total_mb": round(total_size / 1024 / 1024, 1),
                "file_counts": file_counts,
                "largest_files": self._get_largest_files()
            }
        
        # Disques système
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                allocations["system_disks"].append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total_gb": round(usage.total / 1024**3, 1),
                    "used_gb": round(usage.used / 1024**3, 1),
                    "free_gb": round(usage.free / 1024**3, 1),
                    "percent_used": round(usage.used / usage.total * 100, 1)
                })
            except PermissionError:
                continue
        
        return allocations
    
    def _get_largest_files(self) -> List[Dict[str, Any]]:
        """Trouve les plus gros fichiers du workspace"""
        files = []
        
        for file_path in self.workspace.rglob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size > 1024 * 1024:  # Plus de 1MB
                    files.append({
                        "path": str(file_path.relative_to(self.workspace)),
                        "size_mb": round(size / 1024 / 1024, 2),
                        "modified": file_path.stat().st_mtime
                    })
        
        files.sort(key=lambda x: x['size_mb'], reverse=True)
        return files[:10]
    
    def generate_allocation_report(self) -> Dict[str, Any]:
        """Génère un rapport complet d'affectation"""
        report = {
            "timestamp": time.time(),
            "timestamp_human": time.strftime("%Y-%m-%d %H:%M:%S"),
            "gpu_allocations": self.get_gpu_allocations(),
            "cpu_allocations": self.get_cpu_thread_allocations(),
            "memory_allocations": self.get_memory_allocations(),
            "disk_allocations": self.get_disk_allocations()
        }
        
        # Résumé exécutif
        report["executive_summary"] = {
            "total_panini_processes": len(report["cpu_allocations"]["panini_processes"]),
            "rx480_active": len(report["gpu_allocations"]["rx480"]["current_processes"]) > 0,
            "hd7750_active": len(report["gpu_allocations"]["hd7750"]["current_processes"]) > 0,
            "memory_pressure": report["memory_allocations"]["percent_used"] > 80,
            "cpu_load_high": max(report["cpu_allocations"]["per_core_usage"]) > 90
        }
        
        return report

def main():
    """Test du moniteur d'affectation"""
    monitor = ResourceAllocationMonitor()
    report = monitor.generate_allocation_report()
    
    print("🎯 RAPPORT D'AFFECTATION DES RESSOURCES")
    print("=" * 50)
    
    # GPU Summary
    print("\n🖥️  AFFECTATION GPU:")
    for gpu_name, gpu_info in report["gpu_allocations"].items():
        print(f"  {gpu_name.upper()}:")
        print(f"    Rôle: {gpu_info['primary_role']}")
        print(f"    Utilisation: {gpu_info['utilization']}%")
        print(f"    Température: {gpu_info['temperature']}°C")
        print(f"    Processus actifs: {len(gpu_info['current_processes'])}")
        for proc in gpu_info['current_processes']:
            print(f"      • {proc['name']} (PID {proc['pid']}) - {proc['memory_mb']:.1f}MB")
    
    # CPU Summary
    print(f"\n🧠 AFFECTATION CPU:")
    cpu_info = report["cpu_allocations"]
    print(f"  Cores: {cpu_info['total_cores']} | Threads: {cpu_info['total_threads']}")
    print(f"  Processus PaniniFS: {len(cpu_info['panini_processes'])}")
    for proc in cpu_info['panini_processes']:
        print(f"    • {proc['name']} (PID {proc['pid']}) - {proc['cores_assigned']} cores")
    
    # Memory Summary
    print(f"\n💾 AFFECTATION MÉMOIRE:")
    mem_info = report["memory_allocations"]
    print(f"  Total: {mem_info['total_gb']}GB | Utilisé: {mem_info['used_gb']}GB ({mem_info['percent_used']}%)")
    print(f"  PaniniFS: {mem_info['panini_memory_usage']}MB")
    
    # Sauvegarder le rapport
    with open("resource_allocation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Rapport sauvegardé: resource_allocation_report.json")

if __name__ == "__main__":
    main()
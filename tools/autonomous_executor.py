#!/usr/bin/env python3
"""
Autonomous Experiment Executor
Runs experiments locally, in Colab, or via daemon - fully autonomous
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class AutonomousExecutor:
    """Execute experiments autonomously via Jupyter or subprocess"""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.experiments_dir = self.workspace_root / "experiments"
        self.notebooks_dir = self.workspace_root / "notebooks"
        self.outputs_dir = self.workspace_root / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)
        
    def execute_script(self, script_name: str, args: list = None, phase: str = "all") -> Dict[str, Any]:
        """Execute Python script autonomously"""
        
        script_path = self.experiments_dir / f"{script_name}.py"
        if not script_path.exists():
            logger.error(f"❌ Script not found: {script_path}")
            return {"status": "failed", "error": "Script not found"}
        
        cmd = ["python3", str(script_path), "--phase", phase]
        if args:
            cmd.extend(args)
        
        logger.info(f"🚀 Executing: {script_name} (phase: {phase})")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )
            
            success = result.returncode == 0
            status = "✅ SUCCESS" if success else "❌ FAILED"
            
            logger.info(f"{status}: {script_name}")
            if result.stdout:
                logger.info(f"Output:\n{result.stdout[:500]}...")  # First 500 chars
            if result.stderr:
                logger.error(f"Errors:\n{result.stderr[:500]}...")
            
            return {
                "status": "success" if success else "failed",
                "script": script_name,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Timeout: {script_name}")
            return {"status": "timeout", "script": script_name}
        except Exception as e:
            logger.error(f"❌ Exception: {e}")
            return {"status": "error", "error": str(e)}
    
    def execute_notebook(self, notebook_name: str, params: Dict = None) -> Dict[str, Any]:
        """Execute Jupyter notebook autonomously"""
        
        notebook_path = self.notebooks_dir / f"{notebook_name}.ipynb"
        if not notebook_path.exists():
            logger.error(f"❌ Notebook not found: {notebook_path}")
            return {"status": "failed", "error": "Notebook not found"}
        
        logger.info(f"📓 Executing notebook: {notebook_name}")
        
        try:
            # Option 1: jupyter execute (if available)
            cmd = ["jupyter", "execute", str(notebook_path), "--output-format", "json"]
            
            result = subprocess.run(
                cmd,
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            success = result.returncode == 0
            logger.info(f"{'✅ SUCCESS' if success else '❌ FAILED'}: {notebook_name}")
            
            return {
                "status": "success" if success else "failed",
                "notebook": notebook_name,
                "exit_code": result.returncode,
                "timestamp": datetime.now().isoformat()
            }
            
        except FileNotFoundError:
            # Fallback: Use nbconvert
            logger.info("📦 jupyter not found, using nbconvert...")
            try:
                cmd = ["nbconvert", "--to", "notebook", "--execute", str(notebook_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                return {
                    "status": "success" if result.returncode == 0 else "failed",
                    "notebook": notebook_name,
                    "method": "nbconvert"
                }
            except FileNotFoundError:
                logger.error("❌ Neither jupyter nor nbconvert found")
                return {"status": "error", "error": "No notebook executor available"}
        
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Timeout: {notebook_name}")
            return {"status": "timeout", "notebook": notebook_name}
        except Exception as e:
            logger.error(f"❌ Exception: {e}")
            return {"status": "error", "error": str(e)}
    
    def execute_queue(self, queue: list) -> Dict[str, Any]:
        """
        Execute multiple experiments in sequence
        
        Args:
            queue: List of dicts with 'type', 'name', 'phase', 'params'
                  [{"type": "script", "name": "e1_format_decomposition", "phase": "all"},
                   {"type": "notebook", "name": "e2_experiment"}]
        """
        
        results = {
            "started": datetime.now().isoformat(),
            "total": len(queue),
            "succeeded": 0,
            "failed": 0,
            "tasks": []
        }
        
        logger.info(f"▶️  Starting queue execution ({len(queue)} tasks)")
        
        for i, task in enumerate(queue, 1):
            logger.info(f"\n📋 Task {i}/{len(queue)}: {task}")
            
            task_type = task.get("type", "script")
            name = task.get("name")
            
            if task_type == "script":
                phase = task.get("phase", "all")
                result = self.execute_script(name, phase=phase)
            elif task_type == "notebook":
                params = task.get("params", {})
                result = self.execute_notebook(name, params=params)
            else:
                result = {"status": "error", "error": f"Unknown type: {task_type}"}
            
            results["tasks"].append(result)
            
            if result.get("status") == "success":
                results["succeeded"] += 1
            else:
                results["failed"] += 1
        
        results["completed"] = datetime.now().isoformat()
        
        # Save results
        results_file = self.outputs_dir / "execution_log.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"\n✅ Queue complete: {results['succeeded']}/{results['total']} succeeded")
        logger.info(f"📝 Results saved to: {results_file}")
        
        return results
    
    def watch_experiments_json(self, check_interval: int = 60):
        """
        Watch experiments.json for changes and auto-execute
        (Alternative to daemon, runs locally)
        """
        
        config_file = self.workspace_root / "experiments.json"
        if not config_file.exists():
            logger.error(f"❌ Config not found: {config_file}")
            return
        
        logger.info(f"👁️  Watching {config_file} for changes (interval: {check_interval}s)")
        
        last_mtime = 0
        
        while True:
            try:
                mtime = config_file.stat().st_mtime
                
                if mtime > last_mtime:
                    logger.info(f"📝 Config changed, reloading...")
                    
                    with open(config_file) as f:
                        config = json.load(f)
                    
                    queue = config.get("queue", [])
                    if queue:
                        logger.info(f"🚀 Found {len(queue)} tasks in queue")
                        self.execute_queue(queue)
                    
                    last_mtime = mtime
                
                import time
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("⏹️  Stopped watching")
                break
            except Exception as e:
                logger.error(f"❌ Error watching file: {e}")
                import time
                time.sleep(check_interval)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Autonomous Experiment Executor")
    parser.add_argument("--mode", choices=["script", "notebook", "queue", "watch"], default="script")
    parser.add_argument("--name", help="Script or notebook name")
    parser.add_argument("--phase", default="all", help="Experiment phase")
    parser.add_argument("--watch-interval", type=int, default=60)
    
    args = parser.parse_args()
    
    executor = AutonomousExecutor()
    
    if args.mode == "script":
        if not args.name:
            logger.error("--name required for script mode")
        else:
            executor.execute_script(args.name, phase=args.phase)
    
    elif args.mode == "notebook":
        if not args.name:
            logger.error("--name required for notebook mode")
        else:
            executor.execute_notebook(args.name)
    
    elif args.mode == "queue":
        config_file = executor.workspace_root / "experiments.json"
        with open(config_file) as f:
            config = json.load(f)
        executor.execute_queue(config.get("queue", []))
    
    elif args.mode == "watch":
        executor.watch_experiments_json(check_interval=args.watch_interval)

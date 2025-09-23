#!/usr/bin/env python3
"""
Lance le dashboard web
"""

import sys
from pathlib import Path

# Ajoute le dossier src au path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from web.dashboard import create_dashboard


def main():
    """Lance le dashboard"""
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8892
    
    print(f"🎯 DASHBOARD SYSTÈME ÉVÉNEMENTIEL")
    print(f"📡 Interface: http://localhost:{port}")
    print(f"📊 API JSON: http://localhost:{port}/api/metrics")
    print(f"🔄 Auto-refresh: 3 secondes")
    print(f"🛑 Ctrl+C pour arrêter")
    
    dashboard = create_dashboard("event", port)
    dashboard.run()


if __name__ == "__main__":
    main()
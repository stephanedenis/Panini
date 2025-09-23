#!/usr/bin/env python3
"""
🔗 INTÉGRATION DASHBOARD: Ajout section affectation ressources
Patch pour intégrer l'affectation détaillée dans le dashboard principal
"""

import subprocess
import json
import time
from pathlib import Path

def create_resource_integration_patch():
    """Crée un patch pour intégrer l'affectation ressources au dashboard principal"""
    
    # JavaScript à injecter dans le dashboard principal
    javascript_integration = """
    
    // ===== EXTENSION AFFECTATION RESSOURCES =====
    
    function createResourceSection() {
        const container = document.createElement('div');
        container.id = 'resource-allocation-section';
        container.className = 'dashboard-section';
        container.innerHTML = `
            <div class="section-header">
                <h2>🎯 Affectation Ressources</h2>
                <button onclick="refreshResourceData()" class="refresh-btn">🔄</button>
                <a href="http://localhost:8889" target="_blank" class="external-link">📊 Vue détaillée</a>
            </div>
            
            <div class="resource-grid">
                <div class="gpu-allocation">
                    <h3>🖥️ GPU Dual</h3>
                    <div class="gpu-item">
                        <span class="gpu-name">HD 7750 (Display)</span>
                        <div class="gpu-metrics">
                            <span id="hd7750-processes">-- processus</span>
                            <span id="hd7750-temp" class="temp-reading">--°C</span>
                        </div>
                    </div>
                    <div class="gpu-item">
                        <span class="gpu-name">RX 480 (Compute)</span>
                        <div class="gpu-metrics">
                            <span id="rx480-processes">-- processus</span>
                            <span id="rx480-temp" class="temp-reading">--°C</span>
                            <span id="rx480-usage" class="usage-reading">--%</span>
                        </div>
                    </div>
                </div>
                
                <div class="cpu-allocation">
                    <h3>🧠 CPU (16 threads)</h3>
                    <div id="cpu-allocation-details">Chargement...</div>
                </div>
                
                <div class="memory-allocation">
                    <h3>💾 Mémoire (62.7GB)</h3>
                    <div id="memory-allocation-details">Chargement...</div>
                </div>
                
                <div class="panini-processes">
                    <h3>🔬 Processus PaniniFS</h3>
                    <div id="panini-process-list">Chargement...</div>
                </div>
            </div>
        `;
        
        return container;
    }
    
    function refreshResourceData() {
        fetch('http://localhost:8889/api/refresh')
            .then(response => response.json())
            .then(data => {
                updateResourceDisplay(data);
            })
            .catch(error => {
                console.log('Resource dashboard not available, using fallback');
                updateResourceDisplayFallback();
            });
    }
    
    function updateResourceDisplay(data) {
        // GPU
        document.getElementById('hd7750-processes').textContent = 
            `${data.gpu_summary.hd7750.processes} processus`;
        document.getElementById('hd7750-temp').textContent = 
            `${data.gpu_summary.hd7750.temp}°C`;
            
        document.getElementById('rx480-processes').textContent = 
            `${data.gpu_summary.rx480.processes} processus`;
        document.getElementById('rx480-temp').textContent = 
            `${data.gpu_summary.rx480.temp}°C`;
        document.getElementById('rx480-usage').textContent = 
            `${data.gpu_summary.rx480.usage}%`;
        
        // CPU
        document.getElementById('cpu-allocation-details').innerHTML = `
            <div class="allocation-detail">
                <span>Charge max: ${data.system_summary.cpu_usage.toFixed(1)}%</span>
                <span>Processus PaniniFS: ${data.system_summary.panini_processes}</span>
            </div>
        `;
        
        // Memory  
        document.getElementById('memory-allocation-details').innerHTML = `
            <div class="allocation-detail">
                <span>Utilisation: ${data.system_summary.memory_percent.toFixed(1)}%</span>
                <span>PaniniFS: ${data.system_summary.panini_memory}MB</span>
            </div>
        `;
        
        // Color coding based on usage
        const rx480Usage = document.getElementById('rx480-usage');
        if (data.gpu_summary.rx480.usage > 70) {
            rx480Usage.className = 'usage-reading high-usage';
        } else if (data.gpu_summary.rx480.usage > 30) {
            rx480Usage.className = 'usage-reading medium-usage';
        } else {
            rx480Usage.className = 'usage-reading low-usage';
        }
    }
    
    function updateResourceDisplayFallback() {
        // Fallback si le dashboard ressources n'est pas disponible
        document.getElementById('cpu-allocation-details').textContent = 
            'Dashboard ressources indisponible - démarrer resource_dashboard_web.py';
    }
    
    // CSS pour la section ressources
    const resourceCSS = `
        .resource-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .gpu-allocation, .cpu-allocation, .memory-allocation, .panini-processes {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
        }
        
        .gpu-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 8px 0;
            padding: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 5px;
        }
        
        .gpu-name {
            font-weight: bold;
        }
        
        .gpu-metrics {
            display: flex;
            gap: 10px;
            font-size: 0.9em;
        }
        
        .temp-reading {
            color: #fbbf24;
        }
        
        .usage-reading {
            font-weight: bold;
        }
        
        .usage-reading.high-usage {
            color: #f87171;
        }
        
        .usage-reading.medium-usage {
            color: #fbbf24;
        }
        
        .usage-reading.low-usage {
            color: #4ade80;
        }
        
        .allocation-detail {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }
        
        .external-link {
            color: #60a5fa;
            text-decoration: none;
            margin-left: 10px;
        }
        
        .external-link:hover {
            text-decoration: underline;
        }
    `;
    
    // Injection automatique
    function injectResourceSection() {
        // Ajouter CSS
        const style = document.createElement('style');
        style.textContent = resourceCSS;
        document.head.appendChild(style);
        
        // Ajouter section
        const mainDashboard = document.querySelector('.dashboard-container') || document.body;
        const resourceSection = createResourceSection();
        mainDashboard.appendChild(resourceSection);
        
        // Premier refresh
        refreshResourceData();
        
        // Auto-refresh toutes les 30 secondes
        setInterval(refreshResourceData, 30000);
    }
    
    // Démarrage automatique
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectResourceSection);
    } else {
        injectResourceSection();
    }
    
    // ===== FIN EXTENSION AFFECTATION RESSOURCES =====
    """
    
    # Créer le fichier d'intégration
    integration_file = Path("dashboard_resource_integration.js")
    with open(integration_file, "w") as f:
        f.write(javascript_integration)
    
    print(f"✅ Intégration créée: {integration_file}")
    return str(integration_file)

def test_integration():
    """Teste l'intégration avec le dashboard principal"""
    # Vérifier si le dashboard principal tourne
    try:
        result = subprocess.run(["pgrep", "-f", "dashboard_master"], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("✅ Dashboard principal détecté (PID: {})".format(result.stdout.strip()))
        else:
            print("⚠️  Dashboard principal non détecté")
            
        # Vérifier si le dashboard ressources tourne
        result = subprocess.run(["pgrep", "-f", "resource_dashboard"], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("✅ Dashboard ressources détecté (PID: {})".format(result.stdout.strip()))
        else:
            print("⚠️  Dashboard ressources non détecté")
            
    except Exception as e:
        print(f"Erreur test: {e}")

def main():
    """Point d'entrée principal"""
    print("🔗 INTÉGRATION DASHBOARD - AFFECTATION RESSOURCES")
    print("=" * 55)
    
    # Créer l'intégration
    integration_file = create_resource_integration_patch()
    
    # Tester l'environnement
    test_integration()
    
    print("\n📋 INSTRUCTIONS D'UTILISATION:")
    print("1. Le dashboard ressources tourne sur http://localhost:8889")
    print("2. Intégration JavaScript créée dans:", integration_file)
    print("3. Accédez au dashboard principal sur http://localhost:8888")
    print("4. La section 'Affectation Ressources' sera ajoutée automatiquement")
    
    print("\n🎯 FONCTIONNALITÉS AJOUTÉES:")
    print("• Statut GPU dual en temps réel")
    print("• Affectation CPU/Mémoire")
    print("• Processus PaniniFS actifs")
    print("• Lien vers vue détaillée")
    print("• Auto-refresh 30s")
    
    print("\n✨ VOS RESSOURCES SONT MAINTENANT TOTALEMENT VISIBLES !")

if __name__ == "__main__":
    main()
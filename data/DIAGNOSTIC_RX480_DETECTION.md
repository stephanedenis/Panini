# 🔧 DIAGNOSTIC RX 480 NON DÉTECTÉE

## 📊 État Système Actuel

### Cartes Détectées
- **Active**: Radeon HD 7750 (1002:683f) - Slot 04:00.0
- **Manquante**: RX 480 (1002:67df) - NON DÉTECTÉE

### Affichage Actuel
- **2 écrans actifs** via HD 7750 DisplayPort
- **2 ports connectés** supplémentaires disponibles  
- **Total sorties**: 6 DisplayPort sur HD 7750

## 🚨 Causes Probables RX 480 Non Détectée

### 1. Problèmes Physiques
```bash
# Vérifications requises (redémarrage nécessaire):
# - RX 480 bien insérée dans slot PCIe x16
# - Connecteurs d'alimentation 8-pin + 6-pin branchés
# - Slot PCIe compatible (x16 ou x8)
# - Pas de conflit avec HD 7750 dans même slot
```

### 2. Configuration BIOS/UEFI
```bash
# Paramètres BIOS à vérifier:
# - Multi-GPU activé
# - PCIe slots tous activés
# - Secure Boot désactivé
# - Legacy mode vs UEFI
# - Primary display sur HD 7750
```

### 3. Alimentation Insuffisante
```bash
# RX 480 requiert ~150W + connecteurs
# HD 7750 requiert ~55W
# Total: ~205W + système
# Vérifier PSU > 500W recommended
```

### 4. Conflits Drivers
```bash
# Driver amdgpu peut avoir des conflits multi-GPU
# Solutions:
sudo dmesg | grep -E "amdgpu|radeon" | grep -i error
sudo modprobe -r amdgpu
sudo modprobe amdgpu
```

## 🔧 Plan d'Action Diagnostique

### Étape 1: Vérification Boot-Time
```bash
# Redémarrer et vérifier détection au boot
sudo dmesg | grep -E "PCI.*1002" | head -20
sudo lspci | grep -E "1002"
```

### Étape 2: Force Rescan PCI
```bash
# Forcer une nouvelle détection PCI
echo 1 | sudo tee /sys/bus/pci/rescan
sudo lspci | grep AMD
```

### Étape 3: Vérifier Alimentation
```bash
# Vérifier si les connecteurs sont bien branchés
# RX 480 a besoin de:
# - 1x 8-pin PCIe power
# - 1x 6-pin PCIe power (selon modèle)
```

### Étape 4: Configuration Multi-GPU
```bash
# Si RX 480 détectée, configurer mode calcul:
export DRI_PRIME=1  # Pour utiliser RX 480
export GPU_DEVICE_ORDINAL=1  # Pour CUDA/OpenCL
```

## 🎯 Configuration Cible

### Multi-GPU Optimal
```
┌─────────────────┐    ┌─────────────────┐
│   HD 7750       │    │    RX 480       │
│   (Affichage)   │    │   (Calcul)      │
│                 │    │                 │
│ • 4 écrans      │    │ • OpenCL        │
│ • DisplayPort   │    │ • CUDA          │
│ • 55W           │    │ • Python GPU    │
│ • Stable        │    │ • 150W          │
└─────────────────┘    └─────────────────┘
```

### Applications Bénéficiaires
- **PaniniFS**: Calculs GPU sur RX 480
- **Python ML**: pytorch, tensorflow sur RX 480  
- **VS Code**: Affichage stable sur HD 7750
- **Corpus Processing**: Accélération GPU

## 📋 Checklist Immédiate

### [ ] Vérifications Physiques
- [ ] RX 480 bien insérée et vissée
- [ ] Connecteurs 8-pin + 6-pin branchés
- [ ] HD 7750 dans slot différent
- [ ] Alimentation > 500W

### [ ] Tests Système
- [ ] `sudo lspci | grep AMD` après redémarrage
- [ ] `dmesg | grep amdgpu` pour erreurs
- [ ] BIOS: Multi-GPU enabled
- [ ] Driver amdgpu charge les 2 cartes

### [ ] Configuration Logicielle
- [ ] ROCm pour RX 480 si détectée
- [ ] Variables environnement GPU
- [ ] Test calcul sur RX 480
- [ ] Affichage reste sur HD 7750

---
**Prochaine étape**: Redémarrage + vérification physique RX 480
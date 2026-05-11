# 🔺 DIAGNOSTIC INSTALLATION RX 480 - ACTIONS REQUISES
**Date**: 19 Septembre 2025  
**Statut**: ⚠️ RX 480 NON DÉTECTÉE - ACTIONS REQUISES

## 🔍 DIAGNOSTIC HARDWARE

### GPU Actuellement Détecté
```
Carte Détectée: AMD/ATI Cape Verde PRO [Radeon HD 7750/8740]
Driver Actif: radeon
PCI ID: 1002:683f
Slot: 0000:04:00.0
Status: Fonctionnel mais ancienne génération
```

### GPU RX 480 Recherché
```
Carte Cible: AMD Radeon RX 480 (Polaris 10)
PCI ID Attendu: 1002:67df (RX 480)
Driver Requis: amdgpu
Status: NON DÉTECTÉ
```

## ⚡ ACTIONS REQUISES POUR RX 480

### 1. Vérification Installation Physique
```bash
# Éteindre complètement le système
sudo poweroff

# Vérifications physiques:
# - RX 480 correctement insérée dans slot PCIe
# - Connecteurs d'alimentation 8-pin branchés
# - Carte bien fixée et connectée
# - Ancienne HD 7750 retirée (si remplacement)
```

### 2. Redémarrage et Détection
```bash
# Redémarrer système
# Vérifier détection nouvelle carte
lspci | grep VGA
lspci -nn | grep 1002:67df  # PCI ID RX 480

# Si détectée, vérifier driver
lsmod | grep amdgpu
```

### 3. Configuration Driver AMDGPU (si besoin)
```bash
# Blacklister radeon pour RX 480
echo "blacklist radeon" | sudo tee -a /etc/modprobe.d/blacklist-radeon.conf

# Forcer amdgpu pour Polaris
echo "options amdgpu si_support=1" | sudo tee -a /etc/modprobe.d/amdgpu.conf
echo "options amdgpu cik_support=1" | sudo tee -a /etc/modprobe.d/amdgpu.conf

# Rebuild initramfs
sudo mkinitrd
```

### 4. Paramètres Boot Kernel (si nécessaire)
```bash
# Ajouter aux paramètres de boot dans GRUB:
# radeon.si_support=0 amdgpu.si_support=1
sudo vim /etc/default/grub
# GRUB_CMDLINE_LINUX_DEFAULT="... radeon.si_support=0 amdgpu.si_support=1"

sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

## 🚀 VALIDATION POST-INSTALLATION

### Tests à Effectuer Après Détection RX 480
```bash
# 1. Vérifier détection hardware
lspci | grep "Radeon RX 480\|Ellesmere"

# 2. Confirmer driver amdgpu actif
lsmod | grep amdgpu
dmesg | grep amdgpu

# 3. Tester OpenGL
glxinfo | grep "renderer\|version"

# 4. Valider compute shaders
cd /home/stephane/GitHub/PaniniFS-Research/tech
./dhatu_gpu_test_rx480

# 5. Benchmark performance réelle
python dhatu_geometric_simple.py
```

## 📊 DRIVERS RECOMMANDÉS

### Driver AMDGPU (Moderne)
```
Version Kernel: 6.16.3 ✅ (compatible RX 480)
Driver: amdgpu (open source)
Support: Polaris 10 (RX 480) natif
OpenGL: 4.6
Compute: OpenCL 2.0
Status: RECOMMANDÉ pour RX 480
```

### Mesa (OpenGL)
```bash
# Vérifier version Mesa
glxinfo | grep "Mesa version"

# Si mise à jour nécessaire (openSUSE)
sudo zypper update Mesa-dri-drivers Mesa-libGL1
```

## ⚠️ SCENARIOS POSSIBLES

### Scénario A: RX 480 Pas Physiquement Installée
- **Action**: Installation physique complète requise
- **Vérification**: Slots PCIe, alimentation, fixation

### Scénario B: RX 480 Installée mais Non Détectée  
- **Action**: Redémarrage complet nécessaire
- **Cause**: Système pas redémarré après installation

### Scénario C: RX 480 Détectée mais Driver Incorrect
- **Action**: Configuration driver amdgpu
- **Blacklist**: radeon pour éviter conflits

### Scénario D: Dual GPU (HD 7750 + RX 480)
- **Action**: Configurer GPU primaire
- **Choix**: RX 480 comme carte principale

## 🎯 ÉTAPES IMMÉDIATES RECOMMANDÉES

1. **REDÉMARRAGE COMPLET** du système
   ```bash
   sudo reboot
   ```

2. **VÉRIFICATION POST-REDÉMARRAGE**
   ```bash
   lspci | grep -i amd
   lspci -nn | grep 1002:67df
   ```

3. **SI RX 480 DÉTECTÉE**: Configuration driver amdgpu

4. **SI NON DÉTECTÉE**: Vérification installation physique

## 📋 COMMANDES DIAGNOSTICS

```bash
# Pack de diagnostic complet
echo "=== DIAGNOSTIC GPU ==="
lspci | grep VGA
lsmod | grep -E "(radeon|amdgpu)"
dmesg | grep -E "(radeon|amdgpu)" | tail -10
glxinfo | head -10
```

---
**Status Actuel**: HD 7750 détectée, RX 480 en attente  
**Action Prioritaire**: Redémarrage système complet  
**Objectif**: Activation driver amdgpu pour RX 480 Polaris 10 🔺
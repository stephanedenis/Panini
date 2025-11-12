#!/bin/bash
# Fix FUSE mount options to work without allow_other

cd /home/stephane/GitHub/Panini-FS

# Modifier filesystem.rs pour retirer allow_other par défaut
cat > /tmp/fuse-fix.patch << 'EOF'
--- a/crates/panini-fuse/src/filesystem.rs
+++ b/crates/panini-fuse/src/filesystem.rs
@@ -40,7 +40,6 @@ impl PaniniFS {
         let mut mount_options = vec![
             MountOption::FSName("panini".to_string()),
             MountOption::RO,
-            MountOption::AllowOther,
             MountOption::AutoUnmount,
         ];
EOF

# Trouver et modifier le fichier
FUSE_FILE="crates/panini-fuse/src/filesystem.rs"

# Lire le contenu actuel
grep -n "AllowOther" "$FUSE_FILE" || echo "AllowOther non trouvé - déjà corrigé ?"

# Commenter la ligne AllowOther
sed -i 's/MountOption::AllowOther,/\/\/ MountOption::AllowOther,  \/\/ Disabled: requires user_allow_other in fuse3.conf/' "$FUSE_FILE"

echo "✅ Patch appliqué"
grep -A2 -B2 "AllowOther" "$FUSE_FILE"

#!/bin/bash
# Apply CAS integration to FUSE filesystem

cd /home/stephane/GitHub/Panini-FS

# Backup files
cp crates/panini-fuse/src/filesystem.rs crates/panini-fuse/src/filesystem.rs.backup
cp crates/panini-fuse/src/operations.rs crates/panini-fuse/src/operations.rs.backup

echo "=== Step 1: Add storage to PaniniFS struct ==="

# Add imports to filesystem.rs
cat > /tmp/fuse-fs-new-imports.txt << 'EOF'
use anyhow::Result;
use fuser::{
    Filesystem, ReplyAttr, ReplyData, ReplyDirectory, ReplyEntry, Request,
};
use std::sync::Arc;
use std::time::Duration;
use panini_core::storage::ContentStore;

use crate::inode::{InodeTable, ROOT_INODE};
use crate::MountConfig;
EOF

# Replace imports section
sed -i '1,/^use crate::MountConfig;/d' crates/panini-fuse/src/filesystem.rs
cat /tmp/fuse-fs-new-imports.txt crates/panini-fuse/src/filesystem.rs > /tmp/fuse-fs-new.rs
mv /tmp/fuse-fs-new.rs crates/panini-fuse/src/filesystem.rs

# Add storage field to struct
sed -i 's/pub struct PaniniFS {/pub struct PaniniFS {\n    pub(crate) storage: Arc<ContentStore>,/' crates/panini-fuse/src/filesystem.rs

# Update new() method
cat > /tmp/fuse-new-impl.txt << 'EOF'
impl PaniniFS {
    pub fn new(config: MountConfig) -> Result<Self> {
        let inodes = InodeTable::new();
        
        // Initialize storage
        let storage = ContentStore::new(&config.storage_path)?;
        let storage = Arc::new(storage);
        
        Ok(Self {
            storage,
            config,
            inodes,
        })
    }
}
EOF

# Replace impl block
sed -i '/^impl PaniniFS {/,/^}/d' crates/panini-fuse/src/filesystem.rs
echo "" >> crates/panini-fuse/src/filesystem.rs
cat /tmp/fuse-new-impl.txt >> crates/panini-fuse/src/filesystem.rs

echo "✅ Step 1 complete"

echo ""
echo "=== Step 2: Update handle_read in operations.rs ==="

# Create new handle_read implementation
cat > /tmp/fuse-read-impl.txt << 'EOF'
    pub(crate) fn handle_read(
        &self,
        ino: u64,
        _fh: u64,
        offset: i64,
        size: u32,
        _flags: i32,
        _lock_owner: Option<u64>,
        reply: ReplyData,
    ) {
        if let Some(inode) = self.inodes.get(ino) {
            if inode.inode_type != InodeType::File {
                reply.error(libc::EISDIR);
                return;
            }
            
            if let Some(hash) = &inode.content_hash {
                // Read from CAS storage
                match self.storage.read_atom(hash) {
                    Ok(content) => {
                        let bytes = content.as_bytes();
                        let start = offset as usize;
                        let end = (start + size as usize).min(bytes.len());
                        
                        if start >= bytes.len() {
                            reply.data(&[]);
                        } else {
                            reply.data(&bytes[start..end]);
                        }
                    }
                    Err(e) => {
                        tracing::error!("Failed to read atom {}: {}", hash, e);
                        reply.error(libc::EIO);
                    }
                }
            } else {
                reply.error(libc::ENOENT);
            }
        } else {
            reply.error(libc::ENOENT);
        }
    }
EOF

# Find and replace handle_read function
# Use perl for multi-line replacement
perl -i -0pe 's/    pub\(crate\) fn handle_read\([\s\S]*?\n    \}/`cat \/tmp\/fuse-read-impl.txt`/e' crates/panini-fuse/src/operations.rs

echo "✅ Step 2 complete"

echo ""
echo "=== Verification ==="
echo "Checking filesystem.rs:"
grep -c "Arc<ContentStore>" crates/panini-fuse/src/filesystem.rs
echo "Checking operations.rs:"
grep -c "storage.read_atom" crates/panini-fuse/src/operations.rs

echo ""
echo "✅ All patches applied!"

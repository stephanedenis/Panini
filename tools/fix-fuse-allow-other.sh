#!/bin/bash
# Fix AllowOther option in FUSE mount

cd /home/stephane/GitHub/Panini-FS

FILE="crates/panini-fuse/src/lib.rs"

# Backup original
cp "$FILE" "$FILE.backup"

# Remove AllowOther line
sed -i '/MountOption::AllowOther/d' "$FILE"

echo "✅ AllowOther removed from $FILE"
echo "Showing mount options section:"
grep -A5 "Mount options" "$FILE"

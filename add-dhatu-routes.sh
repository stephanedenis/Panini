#!/bin/bash
# Add Dhātu routes to routes.rs

cd /home/stephane/GitHub/Panini-FS

FILE="crates/panini-api/src/routes.rs"

# Backup
cp "$FILE" "$FILE.backup"

# Find the line with .route("/files/:hash/atoms" and add after it
cat > /tmp/dhatu-routes.txt << 'EOF'
        
        // Dhātu emotional classification endpoints (Phase 9)
        .route("/dhatu/emotions", get(dhatu_handlers::get_emotions))
        .route("/dhatu/roots/:emotion", get(dhatu_handlers::get_roots))
        .route("/dhatu/classify", post(dhatu_handlers::classify_content))
        .route("/dhatu/search", get(dhatu_handlers::search_profiles))
        .route("/dhatu/stats", get(dhatu_handlers::get_stats))
        .route("/dhatu/resonance", post(dhatu_handlers::calculate_resonance));
EOF

# Use sed to insert after the last dedup route
sed -i '/\.route("\/files\/:hash\/atoms", get(dedup_handlers::get_file_atoms));/r /tmp/dhatu-routes.txt' "$FILE"

echo "✅ Dhātu routes added to routes.rs"
echo ""
echo "Verifying..."
grep -A2 "Dhātu emotional" "$FILE"

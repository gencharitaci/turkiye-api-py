#!/bin/bash
#
# Sync app/data folder from turkiye-api repository
# Usage: ./sync-data.sh
#

set -e

UPSTREAM_REPO="https://github.com/ubeydeozdmr/turkiye-api.git"
DATA_DIR="app/data"
TEMP_DIR="temp/turkiye-api-sync"

echo "🔄 Syncing application data from turkiye-api repository..."

# Create temp directory
mkdir -p temp

# Clone or update the upstream repository
if [ -d "$TEMP_DIR/.git" ]; then
    echo "📥 Updating existing clone..."
    cd "$TEMP_DIR"
    git fetch origin
    git reset --hard origin/main
    cd ../..
else
    echo "📥 Cloning turkiye-api repository..."
    git clone "$UPSTREAM_REPO" "$TEMP_DIR"
fi

# Check if there are differences
if ! diff -rq "$TEMP_DIR/src/data" "$DATA_DIR" > /dev/null 2>&1; then
    echo "✨ Changes detected! Updating data files..."

    # Backup current data
    if [ -d "$DATA_DIR" ]; then
        BACKUP_DIR="temp/data-backup-$(date +%Y%m%d-%H%M%S)"
        echo "💾 Backing up current data to $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
        cp -r "$DATA_DIR" "$BACKUP_DIR/"
    fi

    # Remove old data
    rm -rf "$DATA_DIR"/*

    # Copy new data
    cp -r "$TEMP_DIR/src/data/"* "$DATA_DIR/"

    echo "✅ Data files updated successfully!"
    echo ""
    echo "📋 Updated files:"
    ls -lh "$DATA_DIR"

    # Validate JSON files
    echo ""
    echo "🔍 Validating JSON files..."
    VALIDATION_FAILED=0

    for jsonfile in "$DATA_DIR"/*.json; do
        if [ -f "$jsonfile" ]; then
            FILENAME=$(basename "$jsonfile")
            if python3 -m json.tool "$jsonfile" > /dev/null 2>&1; then
                echo "  ✅ $FILENAME - Valid JSON"
            else
                echo "  ❌ $FILENAME - Invalid JSON!"
                VALIDATION_FAILED=1
            fi
        fi
    done

    if [ $VALIDATION_FAILED -eq 1 ]; then
        echo ""
        echo "⚠️  WARNING: Some JSON files failed validation!"
        echo "   You may need to restore from backup: $BACKUP_DIR"
    else
        echo ""
        echo "✅ All JSON files validated successfully!"
    fi

    # Show git diff if in a git repository
    echo ""
    echo "📊 Changes summary:"
    git diff --stat "$DATA_DIR" 2>/dev/null || echo "  (Run in git repository to see detailed changes)"
else
    echo "✅ Data files are already up to date!"
fi

echo ""
echo "🎉 Sync completed!"

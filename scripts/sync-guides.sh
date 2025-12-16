#!/bin/bash
#
# Sync guides folder from turkiye-api-docs repository
# Usage: ./sync-guides.sh
#

set -e

UPSTREAM_REPO="https://github.com/ubeydeozdmr/turkiye-api-docs.git"
GUIDES_DIR="guides"
TEMP_DIR="temp/turkiye-api-docs-sync"

echo "🔄 Syncing guides from turkiye-api-docs repository..."

# Create temp directory
mkdir -p "$TEMP_DIR"

# Clone or update the upstream repository
if [ -d "$TEMP_DIR/.git" ]; then
    echo "📥 Updating existing clone..."
    cd "$TEMP_DIR"
    git fetch origin
    git reset --hard origin/main
    cd ../..
else
    echo "📥 Cloning turkiye-api-docs repository..."
    git clone "$UPSTREAM_REPO" "$TEMP_DIR"
fi

# Check if there are differences
if ! diff -rq "$TEMP_DIR" "$GUIDES_DIR" > /dev/null 2>&1; then
    echo "✨ Changes detected! Updating guides folder..."

    # Backup current guides
    if [ -d "$GUIDES_DIR" ]; then
        BACKUP_DIR="temp/guides-backup-$(date +%Y%m%d-%H%M%S)"
        echo "💾 Backing up current guides to $BACKUP_DIR"
        cp -r "$GUIDES_DIR" "$BACKUP_DIR"
    fi

    # Remove old guides (except .git if it exists)
    rm -rf "$GUIDES_DIR"/*

    # Copy new guides (exclude .git directory)
    rsync -av --exclude='.git' "$TEMP_DIR/" "$GUIDES_DIR/"

    echo "✅ Guides updated successfully!"
    echo ""
    echo "📋 Summary of changes:"
    git diff --stat "$GUIDES_DIR" 2>/dev/null || echo "  (Run in git repository to see detailed changes)"
else
    echo "✅ Guides are already up to date!"
fi

echo ""
echo "🎉 Sync completed!"

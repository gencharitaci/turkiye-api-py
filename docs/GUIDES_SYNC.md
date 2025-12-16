# Guides Synchronization

This document explains how the `guides/` folder is kept in sync with the upstream [turkiye-api-docs](https://github.com/ubeydeozdmr/turkiye-api-docs) repository.

## Overview

The `guides/` folder contains documentation from the original turkiye-api-docs repository by [Ubeyde Emir Özdemir](https://github.com/ubeydeozdmr). To keep this documentation up to date, we have automated synchronization mechanisms.

## Automatic Sync (GitHub Actions)

**Schedule**: Daily at 2:00 AM UTC

The repository includes a GitHub Action that automatically:

1. Checks for changes in turkiye-api-docs repository
2. Updates the local `guides/` folder if changes are detected
3. Creates a commit with sync details
4. Pushes changes to the repository

### Manual Trigger

You can manually trigger the sync from GitHub:

1. Go to **Actions** tab in your repository
2. Select **"Sync Guides from turkiye-api-docs"** workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"** button

## Manual Sync (Scripts)

For local development or manual updates, use the provided sync scripts:

### Linux/Mac

```bash
# Make script executable (first time only)
chmod +x scripts/sync-guides.sh

# Run sync
./scripts/sync-guides.sh
```

### Windows

```cmd
# Run sync
scripts\sync-guides.bat
```

## What Gets Synced

The sync process:

- ✅ Copies all files from turkiye-api-docs repository
- ✅ Excludes `.git` and `.github` directories
- ✅ Backs up current guides before updating
- ✅ Preserves local modifications (creates backup)

## Backup System

Before each sync, the current guides folder is backed up to:

```
temp/guides-backup-YYYYMMDD-HHMMSS/
```

To restore from backup:

```bash
# List available backups
ls temp/guides-backup-*/

# Restore specific backup
cp -r temp/guides-backup-20251214-140530/* guides/
```

## Sync Workflow

```
┌─────────────────────────────────────┐
│  turkiye-api-docs Repository        │
│  (upstream source)                  │
└────────────┬────────────────────────┘
             │
             │ Daily at 2 AM UTC
             │ (or manual trigger)
             ▼
┌─────────────────────────────────────┐
│  GitHub Action                       │
│  - Clone upstream                   │
│  - Compare changes                  │
│  - Update if needed                 │
│  - Commit & push                    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Local guides/ folder                │
│  (synchronized copy)                │
└─────────────────────────────────────┘
```

## File Structure

After sync, the guides folder contains:

```
guides/
├── assets/          # Images and media
├── en/              # English documentation
├── tr/              # Turkish documentation
├── public/          # Public assets
├── index.md         # Documentation index
└── LICENSE          # Original license
```

## Troubleshooting

### Sync Not Working

**Problem**: GitHub Action fails to sync

**Solutions**:

1. Check workflow logs in Actions tab
2. Verify repository permissions
3. Check if upstream repository is accessible
4. Manually run sync script locally

### Merge Conflicts

**Problem**: Local changes conflict with upstream

**Solutions**:

1. Check backup folder: `temp/guides-backup-*/`
2. Manually merge changes from backup
3. Or discard local changes and re-sync

### Missing Guides

**Problem**: Guides folder is empty after sync

**Solutions**:

1. Check if sync script completed successfully
2. Restore from latest backup
3. Manually run sync script with verbose output

## Configuration

### Change Sync Schedule

Edit `.github/workflows/sync-guides.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

Cron syntax:

- `0 2 * * *` - Daily at 2:00 AM
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 0` - Weekly on Sunday at midnight
- `0 0 1 * *` - Monthly on the 1st at midnight

### Disable Auto-Sync

To disable automatic syncing:

1. Delete or rename `.github/workflows/sync-guides.yml`
2. Or add to the workflow file:

   ```yaml
   on:
     workflow_dispatch:  # Manual only
   ```

## Best Practices

1. **Don't modify guides directly**: Changes will be overwritten on next sync
2. **Use custom documentation**: Add custom docs outside the `guides/` folder
3. **Check sync logs**: Review GitHub Actions logs for sync status
4. **Keep backups**: The system automatically creates backups, but keep important versions

## Credits

Documentation source: [turkiye-api-docs](https://github.com/ubeydeozdmr/turkiye-api-docs)

Original Author: [Ubeyde Emir Özdemir](https://github.com/ubeydeozdmr)

## Related Files

- `.github/workflows/sync-guides.yml` - GitHub Action workflow
- `scripts/sync-guides.sh` - Linux/Mac sync script
- `scripts/sync-guides.bat` - Windows sync script
- `guides/` - Synchronized documentation folder
- `temp/guides-backup-*/` - Backup folders

---

**Last Updated**: 2025-12-14
**Sync Method**: Automated (GitHub Actions + Manual Scripts)
**Sync Frequency**: Daily at 2:00 AM UTC

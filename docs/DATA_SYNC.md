# Data Synchronization

This document explains how the `app/data/` folder is kept in sync with the upstream [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) repository.

## Overview

The `app/data/` folder contains critical JSON data files (provinces, districts, neighborhoods, villages, towns) from the original turkiye-api repository. To keep this data up to date with the latest administrative changes in Turkey, we have automated synchronization mechanisms.

## Data Files

The following JSON files are synchronized:

```
app/data/
├── provinces.json       # 81 provinces of Turkey
├── districts.json       # 973 districts
├── neighborhoods.json   # Neighborhoods data
├── villages.json        # Villages data
└── towns.json          # Towns data
```

**Source**: [turkiye-api/src/data](https://github.com/ubeydeozdmr/turkiye-api/tree/main/src/data)

---

## Automatic Sync (GitHub Actions)

**Schedule**: Weekly on Sunday at 3:00 AM UTC

The repository includes a GitHub Action that automatically:

1. Checks for changes in turkiye-api data files
2. Updates the local `app/data/` folder if changes are detected
3. Validates all JSON files
4. Creates a commit with sync details and statistics
5. Pushes changes to the repository

### Manual Trigger

You can manually trigger the data sync from GitHub:

1. Go to **Actions** tab in your repository
2. Select **"Sync Data from turkiye-api"** workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"** button

The workflow will:

- Clone the upstream repository
- Compare data files
- Update if changes detected
- Validate JSON format
- Show statistics (file count, sizes, record counts)

---

## Manual Sync (Scripts)

For local development or manual updates, use the provided sync scripts:

### Linux/Mac

```bash
# Make script executable (first time only)
chmod +x scripts/sync-data.sh

# Run sync
./scripts/sync-data.sh
```

**Script Features**:

- ✅ Clones/updates upstream repository
- ✅ Compares for changes
- ✅ Backs up current data before updating
- ✅ Validates JSON files after sync
- ✅ Shows detailed change summary

### Windows

```cmd
# Run sync
scripts\sync-data.bat
```

**Script Features**:

- ✅ Checks for Git and Python installation
- ✅ Clones/updates upstream repository
- ✅ Backs up current data before updating
- ✅ Validates JSON files after sync
- ✅ Shows file count and validation results

---

## What Gets Synced

The sync process:

- ✅ Copies all JSON files from `turkiye-api/src/data/`
- ✅ Excludes non-data files (.git, README, etc.)
- ✅ Backs up current data before updating
- ✅ Validates JSON format after sync
- ✅ Preserves file encoding and structure

**Data Integrity**:

- JSON validation ensures files are parseable
- Backup system prevents data loss
- Commit history tracks all changes

---

## Backup System

Before each sync, the current data folder is backed up to:

```
temp/data-backup-YYYYMMDD-HHMMSS/
```

### Restore from Backup

```bash
# List available backups
ls temp/data-backup-*/

# Restore specific backup
cp -r temp/data-backup-20251214-150530/data/* app/data/
```

### Verify Restored Data

```bash
# Validate JSON files
for file in app/data/*.json; do
    python -m json.tool "$file" > /dev/null && echo "✅ $file" || echo "❌ $file"
done
```

---

## Sync Workflow

```
┌─────────────────────────────────────┐
│  turkiye-api Repository              │
│  src/data/ (upstream source)        │
└────────────┬────────────────────────┘
             │
             │ Weekly on Sunday at 3 AM UTC
             │ (or manual trigger)
             ▼
┌─────────────────────────────────────┐
│  GitHub Action                       │
│  - Clone upstream                   │
│  - Compare data files               │
│  - Backup current data              │
│  - Update if changed                │
│  - Validate JSON                    │
│  - Commit & push                    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Local app/data/ folder              │
│  (synchronized copy)                │
└─────────────────────────────────────┘
```

---

## Data Validation

After each sync, JSON files are validated to ensure:

1. **Valid JSON Format**: Files can be parsed by JSON parser
2. **Required Files Present**: provinces.json, districts.json exist
3. **Non-Empty**: Files contain actual data
4. **Proper Encoding**: UTF-8 encoding preserved

### Manual Validation

```bash
# Validate all JSON files
python -c "
import json
import os

data_dir = 'app/data'
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                count = len(data) if isinstance(data, (list, dict)) else 'N/A'
                print(f'✅ {filename}: {count} records')
        except Exception as e:
            print(f'❌ {filename}: {e}')
"
```

---

## Impact on Application

### When Data Updates

- ✅ Application automatically uses new data on next restart
- ✅ No code changes needed
- ✅ DataLoader re-reads JSON files
- ✅ Cached data is refreshed

### Production Considerations

**Before Deploying Updated Data**:

1. Test locally with new data
2. Verify all JSON files are valid
3. Check for any breaking changes
4. Run application tests
5. Deploy during low-traffic period

**Restart Application**:

```bash
# Docker
docker-compose restart api

# Systemd
sudo systemctl restart turkiye-api

# Manual
# Stop current process
# Run: gunicorn -c gunicorn.conf.py app.main:app
```

---

## Troubleshooting

### Sync Not Working

**Problem**: GitHub Action fails to sync

**Solutions**:

1. Check workflow logs in Actions tab
2. Verify upstream repository is accessible
3. Check for JSON validation errors
4. Manually run sync script locally

### Invalid JSON After Sync

**Problem**: JSON validation fails

**Solutions**:

1. Restore from latest backup
2. Check upstream source for corruption
3. Manually fix JSON formatting
4. Report issue to upstream repository

### Missing Data Files

**Problem**: Required files missing after sync

**Solutions**:

1. Check if files exist in upstream: <https://github.com/ubeydeozdmr/turkiye-api/tree/main/src/data>
2. Restore from backup
3. Manually download files from upstream
4. Check sync script logs

### Application Errors After Update

**Problem**: Application fails after data update

**Solutions**:

1. Check application logs
2. Verify JSON structure matches expected format
3. Restore previous data from backup
4. Report compatibility issue

---

## Configuration

### Change Sync Schedule

Edit `.github/workflows/sync-data.yml`:

```yaml
on:
  schedule:
    - cron: '0 3 * * 0'  # Weekly on Sunday at 3 AM UTC
```

**Recommended Schedules**:

- `0 3 * * 0` - Weekly on Sunday (default, recommended)
- `0 3 * * *` - Daily at 3:00 AM (if data changes frequently)
- `0 3 1 * *` - Monthly on the 1st (if data rarely changes)

### Disable Auto-Sync

To disable automatic syncing:

1. Delete or rename `.github/workflows/sync-data.yml`
2. Or modify the workflow to manual-only:

   ```yaml
   on:
     workflow_dispatch:  # Manual trigger only
   ```

---

## Data Statistics

### Current Data (as of sync)

| File | Records | Size | Last Updated |
|------|---------|------|--------------|
| provinces.json | 81 | ~15 KB | Weekly |
| districts.json | 973 | ~150 KB | Weekly |
| neighborhoods.json | Varies | Varies | Weekly |
| villages.json | Varies | Varies | Weekly |
| towns.json | Varies | Varies | Weekly |

**Total Data Size**: ~500 KB - 1 MB (approximate)

### Update Frequency

**Upstream Updates**:

- Provinces: Rarely (constitutional changes only)
- Districts: Occasionally (administrative reorganization)
- Neighborhoods/Villages/Towns: More frequent (local changes)

**Our Sync**: Weekly (Sunday 3 AM UTC)

This ensures we stay current without excessive syncing.

---

## Best Practices

1. **Don't modify data files directly**: Changes will be overwritten on next sync
2. **Use data transformations in code**: If you need modified data, transform it at runtime
3. **Test after updates**: Always test application after data sync
4. **Monitor sync logs**: Review GitHub Actions logs regularly
5. **Keep backups**: The system auto-backs up, but maintain your own critical backups
6. **Validate before deploy**: Always validate JSON before deploying to production

---

## Security Considerations

### Data Integrity

- ✅ JSON validation prevents corrupted data
- ✅ Backup system prevents data loss
- ✅ Git history provides audit trail

### Access Control

- ✅ Only GitHub Actions can auto-update
- ✅ Manual sync requires repository access
- ✅ Production data is read-only

### Monitoring

- ✅ GitHub Actions provides sync logs
- ✅ Commit messages include statistics
- ✅ Validation failures are reported

---

## Credits

Data source: [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api)

Original data compiled by: [Ubeyde Emir Özdemir](https://github.com/ubeydeozdmr)

Data sources:

- [TÜİK (Turkish Statistical Institute)](https://biruni.tuik.gov.tr/medas)
- [Harita Genel Müdürlüğü](https://www.harita.gov.tr/)

---

## Related Files

- `.github/workflows/sync-data.yml` - GitHub Action workflow
- `scripts/sync-data.sh` - Linux/Mac sync script
- `scripts/sync-data.bat` - Windows sync script
- `app/data/` - Application data folder
- `temp/data-backup-*/` - Backup folders

---

**Last Updated**: 2025-12-14
**Sync Method**: Automated (GitHub Actions + Manual Scripts)
**Sync Frequency**: Weekly on Sunday at 3:00 AM UTC
**Data Source**: <https://github.com/ubeydeozdmr/turkiye-api/tree/main/src/data>

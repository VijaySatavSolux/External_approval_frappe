# Complete Installation Fix Guide

## Problem Summary

When using `--skip-assets`, the app installation may not complete properly:
- ❌ App not registered in `apps.txt`
- ❌ Module definitions not created
- ❌ DocTypes not installed

Additionally, without `--skip-assets`, you get a build error:
- ❌ `TypeError: paths[0] undefined` in esbuild

## Solution: Two-Part Fix

### Part 1: Install with --skip-assets (Current Workaround)

The app has been updated with enhanced installation hooks that will ensure proper registration even with `--skip-assets`:

```bash
# 1. Remove any existing installation
bench remove-app external_approval_digital_sign

# 2. Get app with --skip-assets
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git --skip-assets

# 3. Install with --skip-assets
bench install-app external_approval_digital_sign --skip-assets

# 4. Run the fix script (NEW - ensures everything is registered)
bench --site your-site-name execute external_approval_digital_sign.fix_installation.fix_installation

# 5. Migrate and restart
bench migrate
bench restart
```

### Part 2: Manual Fix (If Part 1 Doesn't Work)

If the installation hooks don't work, use the manual fix script:

```bash
# Run the fix script
bench --site your-site-name execute external_approval_digital_sign.fix_installation.fix_installation

# Then migrate and restart
bench migrate
bench restart
```

### Part 3: Verify Installation

After installation, verify everything is working:

1. **Check apps.txt:**
   ```bash
   cat sites/apps.txt
   ```
   Should contain: `external_approval_digital_sign`

2. **Check in Frappe Console:**
   ```bash
   bench --site your-site-name console
   ```
   ```python
   import frappe
   
   # Check Module Def
   print("Module Def:", frappe.db.exists("Module Def", "External Approval Digital Sign"))
   
   # Check DocTypes
   print("External Approval:", frappe.db.exists("DocType", "External Approval"))
   print("External Approval Configuration:", frappe.db.exists("DocType", "External Approval Configuration"))
   
   # Check Web Page
   print("Web Page:", frappe.db.exists("Web Page", "approval"))
   ```

3. **Check in Frappe UI:**
   - Go to **Module Def** → Should see "External Approval Digital Sign"
   - Go to **DocType List** → Should see "External Approval" and "External Approval Configuration"
   - Go to **Web Page** → Should see "approval"

## What Was Fixed

### 1. Enhanced `install.py`
- ✅ `ensure_app_in_apps_txt()` - Automatically adds app to apps.txt
- ✅ `ensure_module_def()` - Creates Module Def if missing
- ✅ `sync_app_modules()` - Forces reload of all modules and doctypes
- ✅ Better error handling and logging

### 2. Added `before_install` Hook
- ✅ Prepares app structure before installation

### 3. Created `fix_installation.py`
- ✅ Standalone script to fix installation issues
- ✅ Can be run manually if hooks don't work
- ✅ Provides detailed progress output

### 4. Updated `hooks.py`
- ✅ Enabled `before_install` hook

## Troubleshooting

### Issue: "App still not in apps.txt after installation"

**Solution 1:** Run the fix script:
```bash
bench --site your-site-name execute external_approval_digital_sign.fix_installation.fix_installation
```

**Solution 2:** Manually add to apps.txt:
```bash
echo "external_approval_digital_sign" >> sites/apps.txt
bench migrate
bench restart
```

### Issue: "Module Def not created"

**Solution:** Run in bench console:
```bash
bench --site your-site-name console
```
```python
import frappe
frappe.get_doc({
    "doctype": "Module Def",
    "module_name": "External Approval Digital Sign",
    "app_name": "external_approval_digital_sign"
}).insert(ignore_permissions=True)
frappe.db.commit()
```

### Issue: "DocTypes not visible"

**Solution:** Run the fix script or manually reload:
```bash
bench --site your-site-name console
```
```python
import frappe
frappe.reload_doc("external_approval_digital_sign", "doctype", "external_approval", force=True)
frappe.reload_doc("external_approval_digital_sign", "doctype", "external_approval_configuration", force=True)
frappe.db.commit()
```

### Issue: "Build error when not using --skip-assets"

**Current Status:** The build error is a known issue with Frappe's esbuild when apps don't have frontend assets. The solution is to use `--skip-assets` with the enhanced installation hooks.

**Future Fix:** We're working on making the app buildable without requiring `--skip-assets`.

## Installation Flow

```
┌─────────────────────────────────────┐
│  bench get-app --skip-assets        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  bench install-app --skip-assets    │
│  ├─ before_install hook             │
│  ├─ App installation                  │
│  └─ after_install hook              │
│     ├─ ensure_app_in_apps_txt()     │
│     ├─ ensure_module_def()          │
│     └─ sync_app_modules()           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Run fix_installation script        │
│  (Optional but recommended)         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  bench migrate                       │
│  bench restart                      │
└─────────────────────────────────────┘
```

## Notes

- The enhanced `after_install` hook will automatically fix most installation issues
- The `fix_installation.py` script is a backup if hooks don't work
- Always run `bench migrate` after installation to ensure database is synced
- The app is now more resilient to installation issues with `--skip-assets`


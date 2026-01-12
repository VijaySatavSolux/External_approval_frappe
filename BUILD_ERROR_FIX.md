# Build Error Fix - TypeError: paths[0] undefined

## Problem
When installing the app, you encounter this error:
```
TypeError [ERR_INVALID_ARG_TYPE]: The "paths[0]" argument must be of type string. Received undefined
    at get_all_files_to_build
```

This happens because Frappe's esbuild is trying to find files to build but receives undefined paths.

## Root Cause
Frappe's build system expects certain directory structures and file paths. When these are missing or undefined, the build fails.

## Solution: Use --skip-assets Flag

Since this app is primarily backend-focused and doesn't require frontend asset compilation, use the `--skip-assets` flag:

### Step 1: Remove the incorrectly installed app
```bash
cd ~/Benchapps/extapp
bench remove-app external_approval_digital_sign
```

### Step 2: Get app with --skip-assets
```bash
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git --skip-assets
```

### Step 3: Install app with --skip-assets
```bash
bench install-app external_approval_digital_sign --skip-assets
```

### Step 4: Migrate and restart
```bash
bench migrate
bench restart
```

## Why This Works
The `--skip-assets` flag tells Frappe to skip the frontend asset build process entirely, which avoids the path resolution error. This is safe for this app because:
- The app uses standard Frappe web pages (no custom build required)
- All JavaScript is inline in HTML templates
- No custom CSS/JS bundles need compilation

## Post-Installation Verification

After installation, verify the app is properly registered:

### 1. Check apps.txt
```bash
cat sites/apps.txt
```
Should contain: `external_approval_digital_sign`

### 2. Check Module Def (via bench console)
```bash
bench --site your-site-name console
```
Then in console:
```python
import frappe
frappe.get_doc("Module Def", "External Approval Digital Sign")
```

### 3. Check DocTypes
In Frappe UI:
- Go to **DocType List**
- Look for "External Approval" and "External Approval Configuration"

## If App Entry Missing in apps.txt

If after installation the app is not in `apps.txt`:

1. **Manually add to apps.txt:**
   ```bash
   echo "external_approval_digital_sign" >> sites/apps.txt
   ```

2. **Sync modules:**
   ```bash
   bench --site your-site-name migrate
   bench restart
   ```

3. **Verify in console:**
   ```bash
   bench --site your-site-name console
   ```
   ```python
   import frappe
   # Create module if missing
   if not frappe.db.exists("Module Def", "External Approval Digital Sign"):
       frappe.get_doc({
           "doctype": "Module Def",
           "module_name": "External Approval Digital Sign",
           "app_name": "external_approval_digital_sign"
       }).insert(ignore_permissions=True)
       frappe.db.commit()
   ```

## Alternative: Manual Installation

If `--skip-assets` still causes issues:

1. **Clone manually:**
   ```bash
   cd ~/Benchapps/extapp/apps
   git clone https://github.com/VijaySatavSolux/External_approval_frappe.git external_approval_digital_sign
   cd external_approval_digital_sign
   ```

2. **Install Python package:**
   ```bash
   cd ~/Benchapps/extapp
   pip install -e apps/external_approval_digital_sign
   ```

3. **Add to apps.txt manually:**
   ```bash
   echo "external_approval_digital_sign" >> sites/apps.txt
   ```

4. **Install to site:**
   ```bash
   bench --site your-site-name install-app external_approval_digital_sign --skip-assets
   bench --site your-site-name migrate
   bench restart
   ```

## Notes

- The app has been updated with proper configuration files
- Using `--skip-assets` is the recommended approach for this app
- The installation hook (`install.py`) will ensure modules are created even if Frappe skips some steps


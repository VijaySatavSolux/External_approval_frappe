# Installation Fix Guide

## Problem
When installing with `--skip-assets`, the app may not install correctly:
- App entry not generated in `apps.txt`
- Module definitions not created
- DocTypes not installed

## Root Cause
Using `--skip-assets` can cause Frappe to skip critical installation steps, including:
- App registration in `apps.txt`
- Module definition creation
- DocType installation

## Solutions

### Solution 1: Install Without --skip-assets (Recommended)

The app has been updated to work without requiring `--skip-assets`. Try installing normally:

```bash
# Remove app if already installed incorrectly
bench remove-app external_approval_digital_sign

# Get the app (without --skip-assets)
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git

# Install the app (without --skip-assets)
bench install-app external_approval_digital_sign

# Migrate
bench migrate

# Restart
bench restart
```

### Solution 2: Manual Installation (If Solution 1 Fails)

If you still encounter issues, use manual installation:

```bash
# 1. Navigate to your bench directory
cd /path/to/your/bench

# 2. Clone the repository
cd apps
git clone https://github.com/VijaySatavSolux/External_approval_frappe.git external_approval_digital_sign
cd ..

# 3. Install Python package
bench setup requirements
pip install -e apps/external_approval_digital_sign

# 4. Build assets (minimal build)
cd apps/external_approval_digital_sign
npm install  # This will install dependencies (if any)
cd ../..

# 5. Install app to site
bench --site your-site-name install-app external_approval_digital_sign

# 6. Migrate
bench --site your-site-name migrate

# 7. Restart
bench restart
```

### Solution 3: Post-Installation Fix (If App Installed But Modules Missing)

If the app is installed but modules/doctypes are missing:

```bash
# 1. Ensure app is in apps.txt (check sites/apps.txt)
# If not present, add manually:
# external_approval_digital_sign

# 2. Sync modules
bench --site your-site-name console
```

Then in the console:
```python
import frappe
frappe.clear_cache()
frappe.reload_doc("external_approval_digital_sign", "module", "external_approval_digital_sign")
frappe.reload_doc("external_approval_digital_sign", "doctype", "external_approval")
frappe.reload_doc("external_approval_digital_sign", "doctype", "external_approval_configuration")
frappe.reload_doc("external_approval_digital_sign", "web_page", "approval")
frappe.db.commit()
```

Or use bench command:
```bash
bench --site your-site-name migrate
bench restart
```

## Verification

After installation, verify:

1. **Check apps.txt:**
   ```bash
   cat sites/apps.txt
   ```
   Should contain: `external_approval_digital_sign`

2. **Check Module Def:**
   - Go to Frappe Desk → Module Def
   - Look for "External Approval Digital Sign"

3. **Check DocTypes:**
   - Go to Frappe Desk → DocType
   - Look for "External Approval" and "External Approval Configuration"

4. **Check Web Page:**
   - Go to Frappe Desk → Web Page
   - Look for "approval"

## Troubleshooting

### Issue: "App not found in apps.txt"
**Solution:** Manually add to `sites/apps.txt`:
```
external_approval_digital_sign
```
Then run `bench migrate` and `bench restart`

### Issue: "Module Def not created"
**Solution:** Run in bench console:
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
**Solution:** 
```bash
bench --site your-site-name migrate
bench restart
```

### Issue: Build errors
**Solution:** The updated `package.json` includes a minimal build script. If errors persist:
1. Check Node.js version (should be compatible with Frappe)
2. Try: `cd apps/external_approval_digital_sign && npm install`
3. Then retry installation

## Notes

- The app has been updated with proper `package.json` configuration
- `modules.txt` formatting has been fixed
- `install.py` now ensures module registration
- The app should now install without requiring `--skip-assets`


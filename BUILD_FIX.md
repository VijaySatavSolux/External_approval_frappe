# Build Error Fix

## Issue
The build error occurs because Frappe's esbuild is having trouble resolving paths for apps without frontend assets. This is a known issue in some Frappe versions.

## Solution: Install with --skip-assets Flag

Since this app is primarily backend-focused and doesn't require frontend assets, the best solution is to install it with the `--skip-assets` flag:

### Recommended Installation Method:

```bash
# Remove the app if already installed
bench remove-app external_approval_digital_sign

# Get and install with --skip-assets flag
bench get-app external_approval_digital_sign https://github.com/VijaySatavSolux/External_approval_frappe.git --skip-assets
bench install-app external_approval_digital_sign --skip-assets
bench migrate
bench restart
```

This will skip the asset build process and install the app successfully.

## Alternative: Manual Installation

If you prefer to install manually:

1. **Clone the repository:**
```bash
cd ~/ERPNEXT/apps
git clone https://github.com/VijaySatavSolux/External_approval_frappe.git external_approval_digital_sign
```

2. **Install Python package:**
```bash
cd ~/ERPNEXT
bench setup requirements
pip install -e apps/external_approval_digital_sign
```

3. **Install app to site:**
```bash
bench --site your-site-name install-app external_approval_digital_sign
bench migrate
bench restart
```

## Why This Works

The `--skip-assets` flag tells bench to skip the frontend asset build process, which is causing the error. Since this app:
- Doesn't have custom JavaScript/CSS that needs building
- Uses standard Frappe web pages and templates
- Is primarily backend-focused

Skipping the asset build is safe and appropriate.

## Verification

After the build succeeds, verify the app is installed:
```bash
bench --site your-site-name migrate
bench restart
```

Then check in the Frappe UI that "External Approval Configuration" doctype is available.


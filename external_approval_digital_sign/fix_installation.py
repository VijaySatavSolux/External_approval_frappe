#!/usr/bin/env python3
"""
Manual installation fix script for External Approval Digital Sign app.

Run this script if the app was installed with --skip-assets and modules/doctypes are missing.

Usage:
    bench --site your-site-name execute external_approval_digital_sign.fix_installation.fix_installation
"""

import frappe
import os


def fix_installation():
	"""Fix installation issues - ensure app is registered and modules are created"""
	
	app_name = "external_approval_digital_sign"
	module_name = "External Approval Digital Sign"
	
	print("=" * 60)
	print("External Approval Digital Sign - Installation Fix")
	print("=" * 60)
	
	# Step 1: Ensure app in apps.txt
	print("\n[1/4] Checking apps.txt...")
	try:
		sites_path = frappe.get_site_path("..")
		apps_txt_path = os.path.join(sites_path, "apps.txt")
		
		apps = []
		if os.path.exists(apps_txt_path):
			with open(apps_txt_path, "r") as f:
				apps = [line.strip() for line in f.readlines() if line.strip()]
		
		if app_name not in apps:
			apps.append(app_name)
			with open(apps_txt_path, "w") as f:
				f.write("\n".join(apps) + "\n")
			print(f"✓ Added {app_name} to apps.txt")
		else:
			print(f"✓ {app_name} already in apps.txt")
	except Exception as e:
		print(f"✗ Error updating apps.txt: {str(e)}")
	
	# Step 2: Ensure Module Def exists
	print("\n[2/4] Checking Module Def...")
	try:
		if not frappe.db.exists("Module Def", module_name):
			module_doc = frappe.get_doc({
				"doctype": "Module Def",
				"module_name": module_name,
				"app_name": app_name
			})
			module_doc.insert(ignore_permissions=True)
			frappe.db.commit()
			print(f"✓ Created Module Def: {module_name}")
		else:
			print(f"✓ Module Def already exists: {module_name}")
	except Exception as e:
		print(f"✗ Error creating Module Def: {str(e)}")
	
	# Step 3: Reload all app modules
	print("\n[3/4] Reloading app modules...")
	try:
		frappe.clear_cache()
		
		# Reload module
		try:
			frappe.reload_doc(app_name, "module", "external_approval_digital_sign", force=True, reset_permissions=True)
			print("✓ Reloaded module")
		except Exception as e:
			print(f"⚠ Could not reload module: {str(e)}")
		
		# Reload doctypes
		for doctype in ["external_approval", "external_approval_configuration"]:
			try:
				frappe.reload_doc(app_name, "doctype", doctype, force=True, reset_permissions=True)
				print(f"✓ Reloaded doctype: {doctype}")
			except Exception as e:
				print(f"⚠ Could not reload doctype {doctype}: {str(e)}")
		
		# Reload web page
		try:
			frappe.reload_doc(app_name, "web_page", "approval", force=True, reset_permissions=True)
			print("✓ Reloaded web page: approval")
		except Exception as e:
			print(f"⚠ Could not reload web page: {str(e)}")
		
		frappe.db.commit()
	except Exception as e:
		print(f"✗ Error reloading modules: {str(e)}")
	
	# Step 4: Verify installation
	print("\n[4/4] Verifying installation...")
	try:
		# Check Module Def
		if frappe.db.exists("Module Def", module_name):
			print(f"✓ Module Def verified: {module_name}")
		else:
			print(f"✗ Module Def missing: {module_name}")
		
		# Check DocTypes
		for doctype in ["External Approval", "External Approval Configuration"]:
			if frappe.db.exists("DocType", doctype):
				print(f"✓ DocType verified: {doctype}")
			else:
				print(f"✗ DocType missing: {doctype}")
		
		# Check Web Page
		if frappe.db.exists("Web Page", "approval"):
			print("✓ Web Page verified: approval")
		else:
			print("✗ Web Page missing: approval")
		
	except Exception as e:
		print(f"✗ Error during verification: {str(e)}")
	
	print("\n" + "=" * 60)
	print("Installation fix completed!")
	print("=" * 60)
	print("\nNext steps:")
	print("1. Run: bench --site your-site-name migrate")
	print("2. Run: bench restart")
	print("3. Check Frappe UI for DocTypes and Module Def")
	print("=" * 60)


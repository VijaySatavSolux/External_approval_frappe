# Copyright (c) 2024, Your Company and contributors

import frappe
import os


def before_install():
	"""Before install hook - prepare app structure"""
	pass


def after_install():
	"""After install hook - ensure app is properly registered"""
	try:
		# Force app registration in apps.txt
		ensure_app_in_apps_txt()
		
		# Clear cache
		frappe.clear_cache()
		frappe.db.commit()
		
		# Ensure module is created
		ensure_module_def()
		
		# Force sync of all app modules and doctypes
		sync_app_modules()
		
		# Clear cache again after sync
		frappe.clear_cache()
		
		frappe.msgprint("External Approval and Digital Sign app installed successfully!")
		frappe.msgprint("Please configure External Approval Configuration for your doctypes.")
	except Exception as e:
		frappe.log_error(f"Error in after_install: {str(e)}", "External Approval Install Error")
		# Try to fix anyway
		try:
			ensure_app_in_apps_txt()
			ensure_module_def()
		except:
			pass
		frappe.msgprint("App installed. Please run 'bench migrate' to ensure all modules and doctypes are synced.")


def ensure_app_in_apps_txt():
	"""Ensure app is registered in apps.txt"""
	app_name = "external_approval_digital_sign"
	
	# Get sites directory
	sites_path = frappe.get_site_path("..")
	apps_txt_path = os.path.join(sites_path, "apps.txt")
	
	# Read current apps.txt
	apps = []
	if os.path.exists(apps_txt_path):
		with open(apps_txt_path, "r") as f:
			apps = [line.strip() for line in f.readlines() if line.strip()]
	
	# Add app if not present
	if app_name not in apps:
		apps.append(app_name)
		with open(apps_txt_path, "w") as f:
			f.write("\n".join(apps) + "\n")
		frappe.log_error(f"Added {app_name} to apps.txt", "External Approval Install")


def ensure_module_def():
	"""Ensure Module Def is created"""
	module_name = "External Approval Digital Sign"
	app_name = "external_approval_digital_sign"
	
	if not frappe.db.exists("Module Def", module_name):
		try:
			module_doc = frappe.get_doc({
				"doctype": "Module Def",
				"module_name": module_name,
				"app_name": app_name
			})
			module_doc.insert(ignore_permissions=True)
			frappe.db.commit()
			frappe.log_error(f"Created Module Def: {module_name}", "External Approval Install")
		except Exception as e:
			frappe.log_error(f"Error creating Module Def: {str(e)}", "External Approval Install Error")


def sync_app_modules():
	"""Force sync of all app modules, doctypes, and web pages"""
	app_name = "external_approval_digital_sign"
	
	try:
		# Reload module
		frappe.reload_doc(app_name, "module", "external_approval_digital_sign", force=True, reset_permissions=True)
		
		# Reload doctypes
		frappe.reload_doc(app_name, "doctype", "external_approval", force=True, reset_permissions=True)
		frappe.reload_doc(app_name, "doctype", "external_approval_configuration", force=True, reset_permissions=True)
		
		# Reload web page
		frappe.reload_doc(app_name, "web_page", "approval", force=True, reset_permissions=True)
		
		frappe.db.commit()
		frappe.log_error("Synced all app modules and doctypes", "External Approval Install")
	except Exception as e:
		frappe.log_error(f"Error syncing modules: {str(e)}", "External Approval Install Error")
		# Don't fail, just log


def before_uninstall():
	"""Before uninstall hook"""
	pass


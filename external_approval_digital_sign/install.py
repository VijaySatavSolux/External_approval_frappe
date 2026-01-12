# Copyright (c) 2024, Your Company and contributors

import frappe


def after_install():
	"""After install hook"""
	try:
		# Clear cache first
		frappe.clear_cache()
		frappe.db.commit()
		
		# Ensure module is synced - this is critical for app registration
		module_name = "External Approval Digital Sign"
		if not frappe.db.exists("Module Def", module_name):
			module_doc = frappe.get_doc({
				"doctype": "Module Def",
				"module_name": module_name,
				"app_name": "external_approval_digital_sign"
			})
			module_doc.insert(ignore_permissions=True)
			frappe.db.commit()
		
		# Sync all modules to ensure everything is registered
		frappe.clear_cache()
		
		frappe.msgprint("External Approval and Digital Sign app installed successfully!")
		frappe.msgprint("Please configure External Approval Configuration for your doctypes.")
	except Exception as e:
		frappe.log_error(f"Error in after_install: {str(e)}", "External Approval Install Error")
		# Don't fail installation if module sync has issues, but log it
		frappe.msgprint("App installed. Please run 'bench migrate' to ensure all modules and doctypes are synced.")


def before_uninstall():
	"""Before uninstall hook"""
	pass


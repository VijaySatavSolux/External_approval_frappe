# Copyright (c) 2024, Your Company and contributors

import frappe


def after_install():
	"""After install hook"""
	frappe.msgprint("External Approval and Digital Sign app installed successfully!")
	frappe.msgprint("Please configure External Approval Configuration for your doctypes.")


def before_uninstall():
	"""Before uninstall hook"""
	pass


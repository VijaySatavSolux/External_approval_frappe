# Copyright (c) 2024, Your Company and contributors

import frappe
from frappe.website.website_generator import WebsiteGenerator


def get_context(context):
	"""Get context for approval page"""
	token = frappe.form_dict.get("token")
	
	if not token:
		frappe.throw("Token is required", frappe.PermissionError)
	
	# Get approval page data
	from external_approval_digital_sign.api.approval import get_approval_page
	
	try:
		data = get_approval_page(token)
		context.update(data)
	except Exception as e:
		frappe.throw(str(e), frappe.PermissionError)
	
	return context


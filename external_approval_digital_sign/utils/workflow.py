# Copyright (c) 2024, Your Company and contributors

import frappe
from frappe.utils import now_datetime, get_url
from frappe import _


def handle_workflow_state_change(doc, method):
	"""Handle workflow state changes and trigger external approval if configured"""
	# Skip if document is being created
	if doc.is_new():
		return
	
	# Skip if document is not submitted
	if doc.docstatus != 1:
		return
	
	# Get workflow state
	workflow_state = doc.get("workflow_state")
	if not workflow_state:
		return
	
	# Check if state actually changed (compare with previous value)
	# Note: This is a simple check - in production you might want to use frappe.db.get_value
	# to compare with the previous state
	
	# Check if there's an active configuration for this doctype
	config = frappe.db.get_value(
		"External Approval Configuration",
		{
			"doctype_name": doc.doctype,
			"workflow_state_for_external_approval": workflow_state,
			"is_active": 1
		},
		["name", "signature_field_name", "workflow_state_after_approval", "signature_format"],
		as_dict=True
	)
	
	if not config:
		return
	
	# Check if external approval already exists for this document
	existing_approval = frappe.db.exists(
		"External Approval",
		{
			"reference_doctype": doc.doctype,
			"reference_docname": doc.name,
			"status": ["in", ["Pending", "Approved"]]
		}
	)
	
	if existing_approval:
		return
	
	# Get client email from document
	# Try common field names for client email
	client_email = None
	client_name = None
	
	for field in ["customer_email", "client_email", "email", "contact_email"]:
		if doc.get(field):
			client_email = doc.get(field)
			break
	
	# Try common field names for client name
	for field in ["customer_name", "client_name", "party_name", "customer"]:
		if doc.get(field):
			client_name = doc.get(field)
			break
	
	if not client_email:
		frappe.log_error(
			f"External Approval: No client email found for {doc.doctype} {doc.name}",
			"External Approval Error"
		)
		return
	
	# Create External Approval record
	approval_doc = frappe.get_doc({
		"doctype": "External Approval",
		"reference_doctype": doc.doctype,
		"reference_docname": doc.name,
		"client_email": client_email,
		"client_name": client_name,
		"status": "Pending"
	})
	approval_doc.insert(ignore_permissions=True)
	
	# Send approval email
	send_approval_email(approval_doc, doc, config)
	
	frappe.msgprint(_("External approval request has been sent to {0}").format(client_email))


def send_approval_email(approval_doc, reference_doc, config):
	"""Send approval email to client"""
	approval_url = approval_doc.get_approval_url()
	
	subject = f"Approval Required: {reference_doc.doctype} - {reference_doc.name}"
	message = f"""
	<p>Dear {approval_doc.client_name or 'Client'},</p>
	
	<p>You have been requested to review and approve the following document:</p>
	
	<p><strong>Document Type:</strong> {reference_doc.doctype}<br>
	<strong>Document Name:</strong> {reference_doc.name}</p>
	
	<p>Please click the link below to review and approve:</p>
	<p><a href="{approval_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Review and Approve</a></p>
	
	<p>Or copy and paste this URL in your browser:</p>
	<p>{approval_url}</p>
	
	<p>This link will expire in 30 days.</p>
	
	<p>Thank you,<br>
	{reference_doc.owner}</p>
	"""
	
	frappe.sendmail(
		recipients=[approval_doc.client_email],
		subject=subject,
		message=message,
		reference_doctype=reference_doc.doctype,
		reference_name=reference_doc.name
	)


def validate_signature_field(doc, method):
	"""Validate that signature field exists if document has signature"""
	# This is a placeholder - can be extended for validation logic
	pass


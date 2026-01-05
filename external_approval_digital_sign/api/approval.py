# Copyright (c) 2024, Your Company and contributors

import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime, get_url
from frappe.website.website_generator import WebsiteGenerator


@frappe.whitelist(allow_guest=True)
def get_approval_page(token):
	"""Get approval page data"""
	approval = frappe.db.get_value(
		"External Approval",
		{"approval_token": token, "status": "Pending"},
		["name", "reference_doctype", "reference_docname", "client_email", "client_name"],
		as_dict=True
	)
	
	if not approval:
		frappe.throw(_("Invalid or expired approval link"), frappe.PermissionError)
	
	# Get reference document
	try:
		reference_doc = frappe.get_doc(approval.reference_doctype, approval.reference_docname)
	except frappe.DoesNotExistError:
		frappe.throw(_("Document not found"), frappe.PermissionError)
	
	# Get configuration
	config = frappe.db.get_value(
		"External Approval Configuration",
		{
			"doctype_name": approval.reference_doctype,
			"is_active": 1
		},
		["signature_format"],
		as_dict=True
	)
	
	return {
		"approval": approval,
		"document": {
			"doctype": approval.reference_doctype,
			"name": approval.reference_docname,
			"data": reference_doc.as_dict()
		},
		"signature_format": config.signature_format if config else "Name - Date"
	}


@frappe.whitelist(allow_guest=True)
def submit_approval(token, action, signature_name=None, signature_date=None, comments=None):
	"""Submit approval or rejection"""
	approval_name = frappe.db.get_value(
		"External Approval",
		{"approval_token": token, "status": "Pending"},
		"name"
	)
	
	if not approval_name:
		frappe.throw(_("Invalid or expired approval link"), frappe.PermissionError)
	
	approval = frappe.get_doc("External Approval", approval_name)
	
	if action not in ["approve", "reject"]:
		frappe.throw(_("Invalid action"))
	
	# Update approval record
	if action == "approve":
		if not signature_name:
			frappe.throw(_("Signature name is required"))
		
		approval.status = "Approved"
		approval.approved_on = now_datetime()
		approval.signature_name = signature_name
		approval.signature_date = signature_date or frappe.utils.today()
		approval.comments = comments
		
		# Format signature value based on configuration
		config = frappe.db.get_value(
			"External Approval Configuration",
			{
				"doctype_name": approval.reference_doctype,
				"is_active": 1
			},
			["signature_format", "signature_field_name", "workflow_state_after_approval"],
			as_dict=True
		)
		
		if config:
			# Format signature
			signature_value = format_signature(
				signature_name,
				signature_date or frappe.utils.today(),
				config.signature_format
			)
			approval.signature_value = signature_value
			
			# Update reference document
			reference_doc = frappe.get_doc(approval.reference_doctype, approval.reference_docname)
			reference_doc.set(config.signature_field_name, signature_value)
			
			# Update workflow state
			if config.workflow_state_after_approval:
				reference_doc.workflow_state = config.workflow_state_after_approval
			
			reference_doc.save(ignore_permissions=True)
			frappe.db.commit()
			
			# Send confirmation email
			send_approval_confirmation_email(approval, reference_doc)
	
	else:  # reject
		approval.status = "Rejected"
		approval.rejected_on = now_datetime()
		approval.comments = comments
		
		# Send rejection notification
		send_rejection_email(approval)
	
	approval.save(ignore_permissions=True)
	frappe.db.commit()
	
	return {
		"status": "success",
		"message": _("Approval submitted successfully") if action == "approve" else _("Rejection submitted successfully")
	}


def format_signature(name, date, format_type):
	"""Format signature based on configuration"""
	if format_type == "Name - Date":
		return f"{name} - {date}"
	elif format_type == "Date - Name":
		return f"{date} - {name}"
	elif format_type == "Name on Date":
		return f"{name} on {date}"
	else:
		return f"{name} - {date}"


def send_approval_confirmation_email(approval, reference_doc):
	"""Send confirmation email after approval"""
	subject = f"Document Approved: {reference_doc.doctype} - {reference_doc.name}"
	message = f"""
	<p>The following document has been approved:</p>
	
	<p><strong>Document Type:</strong> {reference_doc.doctype}<br>
	<strong>Document Name:</strong> {reference_doc.name}<br>
	<strong>Approved by:</strong> {approval.signature_name}<br>
	<strong>Approved on:</strong> {approval.signature_date}</p>
	"""
	
	# Send to document owner
	frappe.sendmail(
		recipients=[reference_doc.owner],
		subject=subject,
		message=message,
		reference_doctype=reference_doc.doctype,
		reference_name=reference_doc.name
	)


def send_rejection_email(approval):
	"""Send rejection notification email"""
	reference_doc = frappe.get_doc(approval.reference_doctype, approval.reference_docname)
	
	subject = f"Document Rejected: {reference_doc.doctype} - {reference_doc.name}"
	message = f"""
	<p>The following document has been rejected:</p>
	
	<p><strong>Document Type:</strong> {reference_doc.doctype}<br>
	<strong>Document Name:</strong> {reference_doc.name}<br>
	<strong>Rejected by:</strong> {approval.client_name or approval.client_email}</p>
	"""
	
	if approval.comments:
		message += f"<p><strong>Comments:</strong> {approval.comments}</p>"
	
	frappe.sendmail(
		recipients=[reference_doc.owner],
		subject=subject,
		message=message,
		reference_doctype=reference_doc.doctype,
		reference_name=reference_doc.name
	)


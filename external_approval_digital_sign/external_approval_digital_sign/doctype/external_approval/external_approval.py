# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_url
import secrets


class ExternalApproval(Document):
	def before_insert(self):
		# Generate unique approval token
		if not self.approval_token:
			self.approval_token = secrets.token_urlsafe(32)
		
		if not self.requested_on:
			self.requested_on = now_datetime()
	
	def on_update(self):
		if self.status == "Approved" and not self.approval_token:
			frappe.throw("Approval token is required")
	
	def get_approval_url(self):
		"""Get the approval URL for this external approval"""
		return get_url(f"/approval?token={self.approval_token}")


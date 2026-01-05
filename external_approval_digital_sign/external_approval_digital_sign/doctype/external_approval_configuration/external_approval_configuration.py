# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExternalApprovalConfiguration(Document):
	def validate(self):
		# Validate that the doctype exists
		if not frappe.db.exists("DocType", self.doctype_name):
			frappe.throw(f"DocType {self.doctype_name} does not exist")
		
		# Validate that signature field exists in the doctype
		if self.signature_field_name:
			meta = frappe.get_meta(self.doctype_name)
			if self.signature_field_name not in [f.fieldname for f in meta.fields]:
				frappe.throw(f"Field '{self.signature_field_name}' does not exist in {self.doctype_name}")


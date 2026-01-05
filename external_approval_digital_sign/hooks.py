from frappe import _

app_name = "external_approval_digital_sign"
app_title = "External Approval and Digital Sign"
app_publisher = "Your Company"
app_description = "Plug and play Frappe app for external client approval and digital signature capture"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your.email@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/external_approval_digital_sign/css/external_approval_digital_sign.css"
# app_include_js = "/assets/external_approval_digital_sign/js/external_approval_digital_sign.js"

# include js, css files in header of web template
# web_include_css = "/assets/external_approval_digital_sign/css/external_approval_digital_sign.css"
# web_include_js = "/assets/external_approval_digital_sign/js/external_approval_digital_sign.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "external_approval_digital_sign/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "external_approval_digital_sign.utils.jinja_methods",
# 	"filters": "external_approval_digital_sign.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "external_approval_digital_sign.install.before_install"
after_install = "external_approval_digital_sign.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "external_approval_digital_sign.uninstall.before_uninstall"
# after_uninstall = "external_approval_digital_sign.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "external_approval_digital_sign.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"on_update_after_submit": "external_approval_digital_sign.utils.workflow.handle_workflow_state_change",
		"validate": "external_approval_digital_sign.utils.workflow.validate_signature_field",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"external_approval_digital_sign.tasks.all"
# 	],
# 	"daily": [
# 		"external_approval_digital_sign.tasks.daily"
# 	],
# 	"hourly": [
# 		"external_approval_digital_sign.tasks.hourly"
# 	],
# 	"weekly": [
# 		"external_approval_digital_sign.tasks.weekly"
# 	],
# 	"monthly": [
# 		"external_approval_digital_sign.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "external_approval_digital_sign.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "external_approval_digital_sign.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "external_approval_digital_sign.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["external_approval_digital_sign.utils.before_request"]
# after_request = ["external_approval_digital_sign.utils.after_request"]

# Job Events
# ----------
# before_job = ["external_approval_digital_sign.utils.before_job"]
# after_job = ["external_approval_digital_sign.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"external_approval_digital_sign.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


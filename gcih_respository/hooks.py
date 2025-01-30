app_name = "gcih_respository"
app_title = "Gcih Respository"
app_publisher = "Gcih"
app_description = "Gcih"
app_email = "gcih@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gcih_respository/css/gcih_respository.css"
# app_include_js = "/assets/gcih_respository/js/gcih_respository.js"

# include js, css files in header of web template
# web_include_css = "/assets/gcih_respository/css/gcih_respository.css"
# web_include_js = "/assets/gcih_respository/js/gcih_respository.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gcih_respository/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Customer": "public/js/gci_customer_validation.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "gcih_respository/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gcih_respository.utils.jinja_methods",
# 	"filters": "gcih_respository.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gcih_respository.install.before_install"
# after_install = "gcih_respository.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "gcih_respository.uninstall.before_uninstall"
# after_uninstall = "gcih_respository.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "gcih_respository.utils.before_app_install"
# after_app_install = "gcih_respository.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "gcih_respository.utils.before_app_uninstall"
# after_app_uninstall = "gcih_respository.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gcih_respository.notifications.get_notification_config"

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

override_doctype_class = {
    "Customer": "gcih_respository.overrides.gcihs_customer.GCIHSCustomer",
    "Student": "gcih_respository.overrides.gcihs_student.GCIHSStudent"
}

# Override naming series for specific doctypes
override_doctype_naming_series = {
    "Customer": ["", "CUST-.YYYY.-"]  # Empty string first for Student customers
}

# Document Events
# ---------------
doc_events = {
    "Student": {
        "after_insert": "gcih_respository.doc_events.gcihs_student.gcihs_handle_student_creation"
    },
    "Program Enrollment": {
        "before_save": "gcih_respository.gcihs_repo.gcihs_student_promotion.handle_program_enrollment_save",
        "after_insert": "gcih_respository.gcihs_repo.gcihs_student_promotion.auto_submit_enrollment"
    },
    "Program Enrollment Tool": {
        "enroll_students": "gcih_respository.gcihs_repo.gcihs_student_promotion.gcihs_after_bulk_enrollment"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gcih_respository.tasks.all"
# 	],
# 	"daily": [
# 		"gcih_respository.tasks.daily"
# 	],
# 	"hourly": [
# 		"gcih_respository.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gcih_respository.tasks.weekly"
# 	],
# 	"monthly": [
# 		"gcih_respository.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "gcih_respository.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gcih_respository.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gcih_respository.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["gcih_respository.utils.before_request"]
# after_request = ["gcih_respository.utils.after_request"]

# Job Events
# ----------
# before_job = ["gcih_respository.utils.before_job"]
# after_job = ["gcih_respository.utils.after_job"]

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
# 	"gcih_respository.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
# }

# After migration, set up custom fields
after_migrate = [
    "gcih_respository.custom_fields.setup_custom_fields"
]

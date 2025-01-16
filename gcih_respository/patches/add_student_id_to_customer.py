import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    """Add custom_student_id field to Customer doctype"""
    
    # Check if field already exists
    if not frappe.db.exists('Custom Field', {'dt': 'Customer', 'fieldname': 'custom_student_id'}):
        # Create custom field
        create_custom_field('Customer', {
            'label': 'Student ID',
            'fieldname': 'custom_student_id',
            'fieldtype': 'Data',
            'insert_after': 'customer_type',
            'in_list_view': 1,
            'in_standard_filter': 1,
            'in_global_search': 1,
            'read_only': 0,
            'allow_on_submit': 0,
            'translatable': 0,
            'unique': 1,  # Make it unique
            'no_copy': 0,
            'reqd': 0  # Not required by default
        })

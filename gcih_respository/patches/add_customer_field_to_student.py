import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    """Add customer field to Student doctype"""
    
    # Check if field already exists
    if not frappe.db.exists('Custom Field', {'dt': 'Student', 'fieldname': 'customer'}):
        # Create custom field
        create_custom_field('Student', {
            'label': 'Customer',
            'fieldname': 'customer',
            'fieldtype': 'Link',
            'options': 'Customer',
            'insert_after': 'customer_details_section',
            'in_list_view': 1,
            'in_standard_filter': 1,
            'in_global_search': 1,
            'read_only': 0,
            'allow_on_submit': 0,
            'translatable': 0,
            'unique': 0,
            'no_copy': 0,
            'reqd': 0
        })

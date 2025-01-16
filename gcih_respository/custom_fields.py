import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_custom_fields():
    """Setup custom fields for Student ID in various doctypes"""
    
    custom_fields = {
        "Patient": [
            {
                "fieldname": "custom_student_id",
                "label": "Student ID",
                "fieldtype": "Data",
                "insert_after": "patient_name",
                "unique": 1,
                "in_list_view": 1,
                "in_standard_filter": 1,
                "read_only": 1
            }
        ],
        "Customer": [
            {
                "fieldname": "custom_student_id",
                "label": "Student ID",
                "fieldtype": "Data",
                "insert_after": "customer_name",
                "unique": 1,
                "in_list_view": 1,
                "in_standard_filter": 1,
                "read_only": 1
            }
        ]
    }
    
    create_custom_fields(custom_fields)

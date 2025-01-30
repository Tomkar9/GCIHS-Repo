import frappe
from frappe import _

class_mapping = {
    "10C1": "11C1",
    "11C1": "Pool",
    "10C2": "11C2",
    "11C2": "Pool"
}

def get_promoted_class(current_class):
    """Get the next class based on promotion mapping"""
    return class_mapping.get(current_class)

def handle_program_enrollment_save(doc, method):
    """Handle class promotion before saving Program Enrollment"""
    try:
        # Get the current enrollment for comparison
        current_enrollment = frappe.get_all(
            "Program Enrollment",
            filters={
                "student": doc.student,
                "academic_year": str(int(doc.academic_year) - 1),  # Previous year
                "docstatus": 1
            },
            fields=["custom_class", "academic_year"],
            order_by="creation desc",
            limit=1
        )

        if current_enrollment:
            current_class = current_enrollment[0].custom_class
            if current_class:
                promoted_class = get_promoted_class(current_class)
                if promoted_class:
                    doc.custom_class = promoted_class
                    frappe.msgprint(_(f"Student promoted from {current_class} to {promoted_class}"))
                    
    except Exception as e:
        frappe.log_error(f"Error in promotion hook: {str(e)}", "GCIHS Student Promotion Hook Error")

def gcihs_after_bulk_enrollment(doc, method=None):
    """Submit all enrollments created by the Program Enrollment Tool"""
    try:
        # Get all draft enrollments created in the last minute for this academic year and program
        enrollments = frappe.get_all(
            "Program Enrollment",
            filters={
                "docstatus": 0,  # Draft
                "academic_year": doc.new_academic_year,
                "program": doc.new_program,
                "modified": [">=", "DATE_SUB(NOW(), INTERVAL 1 MINUTE)"]
            },
            fields=["name"]
        )
        
        for enrollment in enrollments:
            enroll_doc = frappe.get_doc("Program Enrollment", enrollment.name)
            enroll_doc.submit()
            
        if enrollments:
            frappe.msgprint(_(f"Automatically submitted {len(enrollments)} program enrollments"))
            
    except Exception as e:
        frappe.log_error(f"Error in bulk enrollment submission: {str(e)}", "GCIHS Bulk Submit Error")

def auto_submit_enrollment(doc, method):
    """Auto submit program enrollment after insert"""
    try:
        # Only auto-submit if it came from Program Enrollment Tool
        if doc.reference_doctype == "Program Enrollment Tool":
            doc.submit()
            frappe.msgprint(_(f"Program Enrollment {doc.name} automatically submitted"))
    except Exception as e:
        frappe.log_error(f"Error in auto-submit: {str(e)}", "GCIHS Auto Submit Error")

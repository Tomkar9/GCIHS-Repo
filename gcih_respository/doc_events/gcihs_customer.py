import frappe
from frappe import _

def gcihs_before_insert(doc, method):
    """
    Override customer naming before insert
    """
    try:
        if doc.customer_group != "Student":
            return
            
        # If we have a student ID, force it as the name
        if doc.get("custom_student_id"):
            doc.name = doc.custom_student_id
            # Disable autoname
            doc.flags.name_set = True
            
        # Try to find student by name
        elif doc.customer_name:
            students = frappe.get_all("Student", 
                filters={
                    "first_name": doc.customer_name.split()[0],
                    "last_name": " ".join(doc.customer_name.split()[1:]) if len(doc.customer_name.split()) > 1 else ""
                },
                fields=["name"]
            )
            
            if students:
                doc.custom_student_id = students[0].name
                doc.name = students[0].name
                # Disable autoname
                doc.flags.name_set = True
                
        frappe.log_error(
            message=f"Before Insert - Name: {doc.name}\nStudent ID: {doc.get('custom_student_id')}\nCustomer Name: {doc.customer_name}",
            title="GCIHS Customer Creation"
        )
        
    except Exception as e:
        frappe.log_error(
            message=f"Error in customer before_insert: {str(e)}\nCustomer: {doc.name}\nFull Error: {frappe.get_traceback()}",
            title="GCIHS Customer Creation Error"
        )

def gcihs_autoname(doc, method):
    """
    Override the autoname method for student customers
    """
    try:
        if doc.customer_group != "Student":
            return
            
        if doc.get("custom_student_id"):
            doc.name = doc.custom_student_id
            # Prevent further naming
            doc.flags.name_set = True
            
    except Exception as e:
        frappe.log_error(
            message=f"Error in customer autoname: {str(e)}\nCustomer: {doc.name}\nFull Error: {frappe.get_traceback()}",
            title="GCIHS Customer Autoname Error"
        )

def gcihs_validate_customer(doc, method):
    """
    Validate customer creation to ensure proper ID usage
    """
    if doc.customer_group == "Student" and not doc.get("custom_student_id"):
        frappe.throw(
            _("Student ID is required for customers in the Student group"),
            frappe.MandatoryError
        )

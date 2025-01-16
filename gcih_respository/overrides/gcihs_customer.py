import frappe
from frappe import _
from erpnext.selling.doctype.customer.customer import Customer

class GCIHSCustomer(Customer):
    def autoname(self):
        """Override autoname to ensure student ID is used"""
        if self.customer_group == "Student":
            if self.get("custom_student_id"):
                self.name = self.custom_student_id
                self.flags.name_set = True
            elif not frappe.flags.in_import and not self.flags.from_student:
                frappe.throw(_("Student ID is required for Student group customers"))
        else:
            super().autoname()
    
    def validate(self):
        """Additional validation for Student Customer"""
        if self.customer_group == "Student":
            # Skip validation if being created from Student doctype
            if frappe.flags.in_import or self.flags.from_student:
                return
                
            # Ensure we have a student ID
            if not self.get("custom_student_id"):
                frappe.throw(_("Student ID is required for Student group customers"))
            
            # Force name to match student ID
            self.name = self.custom_student_id
            self.flags.name_set = True
        
        super().validate()

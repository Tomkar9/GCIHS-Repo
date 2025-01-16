import frappe
from frappe import _
from education.education.doctype.student.student import Student

class GCIHSStudent(Student):
    def create_customer(self):
        """Create Customer for student"""
        if self.customer:
            return
            
        # Get territory and customer group
        territory = frappe.get_cached_value('Selling Settings', None, 'territory')
        if territory:
            territory = frappe.get_doc("Territory", territory)
            
        customer_group = frappe.get_cached_value('Selling Settings', None, 'customer_group')
        if not customer_group:
            customer_group = "Student"  # Default to Student group
            
        # Create full name
        full_name = self.first_name
        if self.last_name:
            full_name += " " + self.last_name
            
        # Create customer
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": full_name,
            "customer_type": "Individual",
            "customer_group": customer_group,
            "territory": territory and territory.name,
            "flags": {
                "from_student": True,  # Flag that this is from student creation
                "ignore_mandatory": True,
                "name_set": True  # Prevent autoname from running
            },
            "custom_student_id": self.name,  # Set student ID
            "name": self.name  # Force name to be student ID
        }).insert(ignore_permissions=True)
        
        # Link customer to student
        self.customer = customer.name
        self.db_update()
        
        return customer

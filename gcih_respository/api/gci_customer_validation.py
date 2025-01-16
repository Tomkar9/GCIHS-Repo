import frappe
from frappe import _

@frappe.whitelist()
def validate_student_id(student_id, customer_name=None):
    """
    Validate if student_id is unique across all customers
    Returns dict with exists=True if duplicate found, along with customer details
    """
    existing_customer = frappe.db.get_value(
        "Customer",
        {
            "student_id": student_id,
            "name": ["!=", customer_name]
        },
        ["name", "customer_name"],
        as_dict=True
    )
    
    if existing_customer:
        return {
            "exists": True,
            "name": existing_customer.name,
            "customer_name": existing_customer.customer_name
        }
    
    return {"exists": False}

def handle_duplicate_customer_name(customer_name):
    """
    Handle duplicate customer names by appending an incremental number
    Returns the new customer name
    """
    if frappe.db.exists("Customer", customer_name):
        count = frappe.db.sql(
            """select ifnull(MAX(CAST(SUBSTRING_INDEX(name, ' ', -1) AS UNSIGNED)), 0) from tabCustomer
             where name like %s""",
            f"%{customer_name} - %",
            as_list=1,
        )[0][0]
        count = int(count) + 1 if count else 1

        new_customer_name = f"{customer_name} - {str(count)}"

        frappe.msgprint(
            _("Changed customer name to '{}' as '{}' already exists.").format(
                new_customer_name, customer_name
            ),
            title=_("Note"),
            indicator="yellow",
        )

        return new_customer_name

    return customer_name

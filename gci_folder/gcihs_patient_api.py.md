import frappe
from frappe import _
from frappe.model.naming import set_name_from_naming_options

@frappe.whitelist()
def get_student_details(student):
    student_details = frappe.db.sql("""
        SELECT name, student_name, first_name, middle_name, last_name, gender, date_of_birth, student_email_id
        FROM `tabStudent`
        WHERE name = %s
    """, student, as_dict=True)

    return student_details

@frappe.whitelist()
def get_employee_details(employee):
    employee_details = frappe.db.sql("""
        SELECT name, employee_name, first_name, middle_name, last_name, gender, date_of_birth
        FROM `tabEmployee`
        WHERE name = %s
    """, employee, as_dict=True)
    
    return employee_details

def create_customer_from_student(student):
    """Create a Customer record from Student data"""
    if frappe.db.exists("Customer", student.name):
        return None
        
    # Create customer with student ID as name
    customer_data = {
        "doctype": "Customer",
        "name": student.name,  # Force the name to be student ID
        "customer_type": "Individual",
        "customer_name": student.student_name,
        "student_id": student.name,
        "customer_group": "Student"
    }
    
    try:
        doc = frappe.get_doc(customer_data)
        # Override autoname
        doc.flags.ignore_permissions = True
        doc.flags.ignore_links = True
        doc.flags.ignore_mandatory = True
        # Force the name to be student ID
        doc.name = student.name
        # Bypass naming series and validation
        doc.flags.ignore_validate = True
        doc.flags.ignore_naming_series = True
        # Insert directly into database
        doc.db_insert()
        frappe.db.commit()
        return frappe.get_doc("Customer", student.name)
    except Exception as e:
        frappe.log_error(
            f"Failed to create Customer for student {student.name}: {str(e)}",
            "Customer Creation Error"
        )
        return None

def map_student_gender_to_patient(student_gender):
    """Map student gender to valid Patient gender value"""
    # Default mapping
    gender_mapping = {
        "M": "Male",
        "F": "Female",
        "MALE": "Male",
        "FEMALE": "Female",
        "OTHER": "Other",
        None: "Unknown"
    }
    
    if not student_gender:
        return "Unknown"
        
    mapped_gender = gender_mapping.get(student_gender.upper(), student_gender.title())
    
    # Check if mapped gender exists in Gender doctype
    if frappe.db.exists("Gender", mapped_gender):
        return mapped_gender
    
    # If mapping fails, return Unknown
    return "Unknown"

#### Custom code
@frappe.whitelist()
def get_new_students(self=None, method=None):
    """Create a patient record for a newly created student"""
    try:
        if isinstance(self, str):
            student = frappe.get_doc("Student", self)
        elif hasattr(self, 'doctype') and self.doctype == "Student":
            student = self
        else:
            frappe.msgprint("Invalid student document")
            return
            
        # Check for existing patient by student_id or name
        existing_patient = frappe.db.exists("Patient", {
            "student_id": student.name
        })
        
        if existing_patient:
            # Update existing patient
            patient = frappe.get_doc("Patient", existing_patient)
            patient.first_name = student.first_name
            if hasattr(student, 'middle_name'):
                patient.middle_name = student.middle_name
            if hasattr(student, 'last_name'):
                patient.last_name = student.last_name
            patient.patient_name = student.student_name
            if hasattr(student, 'date_of_birth'):
                patient.dob = student.date_of_birth
            if hasattr(student, 'gender'):
                patient.sex = map_student_gender_to_patient(student.gender)
            if hasattr(student, 'customer'):
                patient.customer = student.customer
            patient.save(ignore_permissions=True)
            frappe.db.commit()
            
            frappe.msgprint(_("Patient {0} updated").format(patient.name))
            return patient
            
        # Create Customer record first if not exists
        customer = None
        if hasattr(student, 'customer') and student.customer:
            customer = student.customer
        else:
            # Check if customer already exists with the same ID
            existing_customer = frappe.db.exists("Customer", student.name)
            if existing_customer:
                customer = existing_customer
            else:
                customer_doc = create_customer_from_student(student)
                if customer_doc:
                    customer = customer_doc.name
            
        if not customer:
            frappe.log_error(
                f"Failed to create/get Customer for student {student.name}",
                "Patient Creation Error"
            )
            return
            
        # Map student gender to valid Patient gender
        mapped_gender = map_student_gender_to_patient(student.gender if hasattr(student, 'gender') else None)
        if not mapped_gender:
            mapped_gender = "Unknown"  # Set a default gender if not provided
        
        # Generate patient name
        patient_name = student.student_name
        
        # Prepare Patient data
        patient_data = {
            "doctype": "Patient",
            "first_name": student.first_name,
            "middle_name": student.middle_name if hasattr(student, 'middle_name') else None,
            "last_name": student.last_name if hasattr(student, 'last_name') else None,
            "patient_name": patient_name,
            "dob": student.date_of_birth if hasattr(student, 'date_of_birth') else None,
            "sex": mapped_gender,
            "student_id": student.name,
            "customer": customer,
            "disabled": 0,
            "status": "Active"
        }

        # Remove None values
        patient_data = {k: v for k, v in patient_data.items() if v is not None}

        try:
            # Create new Patient record
            patient_doc = frappe.get_doc(patient_data)
            patient_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            
            # Update student with patient link
            student.db_set('patient', patient_doc.name)
            frappe.db.commit()
            
            frappe.msgprint(
                _("Patient {0} created and linked to Student {1} and Customer {2}").format(
                    frappe.bold(patient_doc.name), 
                    frappe.bold(student.name),
                    frappe.bold(customer)
                ),
                alert=True
            )
            return patient_doc
        except Exception as e:
            frappe.log_error(f"Failed to create patient: {str(e)}", "Patient Creation Error")
            frappe.throw(_("Failed to create patient. Please check error logs."))
            
    except Exception as e:
        frappe.log_error(f"Error in get_new_students: {str(e)}", "Patient Creation Error")
        frappe.throw(_("Failed to process student. Please check error logs."))

def validate_student_id(student_id, patient_map, customer_map):
    """Validate student_id against existing Patient records only"""
    if student_id in patient_map:
        return {
            "valid": False,
            "reason": _("Already linked to Patient: {0} ({1})").format(
                patient_map[student_id].name,
                patient_map[student_id].patient_name
            )
        }
    
    # We no longer validate against customers since we create them
    return {
        "valid": True,
        "reason": None
    }

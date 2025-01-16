import frappe
from frappe import _

def gcihs_handle_student_creation(doc, method):
    """
    Queue the patient creation task to run after a delay,
    allowing time for core Frappe to create the Customer record.
    """
    try:
        # Queue the task with a delay
        frappe.enqueue(
            method='gcih_respository.doc_events.gcihs_student.gcihs_create_patient_delayed',
            queue='short',
            timeout=300,
            doc_name=doc.name,
            now=False,
            enqueue_after_commit=True,
            at_front=True  # Process this job first
        )
        
        frappe.log_error(
            message=f"Queued patient creation for student {doc.name}",
            title="GCIHS Debug - Task Queued"
        )

    except Exception as e:
        frappe.log_error(
            message=f"Error queuing patient creation: {str(e)}",
            title="GCIHS Queue Error"
        )

def gcihs_create_patient_delayed(doc_name):
    """
    Creates patient record after ensuring customer exists.
    This runs as a background job.
    """
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            frappe.db.commit()  # Commit any pending transactions
            
            # Get the student doc
            doc = frappe.get_doc("Student", doc_name)
            full_name = f"{doc.first_name} {doc.last_name if doc.last_name else ''}"

            frappe.log_error(
                message=f"Starting delayed patient creation for student {doc_name}\nFull Name: {full_name}\nGender: {doc.gender if hasattr(doc, 'gender') else 'Not Set'}\nRetry: {retry_count + 1}",
                title="GCIHS Debug - Delayed Start"
            )

            # Check if patient already exists first
            if frappe.db.exists("Patient", {"custom_student_id": doc_name}):
                frappe.log_error(
                    message=f"Patient already exists for student {doc_name}",
                    title="GCIHS Debug - Patient Exists"
                )
                return

            # Find customer by student ID first
            existing_customer = frappe.db.get_value("Customer", 
                {"custom_student_id": doc_name},
                ["name", "customer_name", "customer_group", "territory"],
                as_dict=1
            )

            # If not found by student ID, check by name to handle existing customers
            if not existing_customer:
                existing_customers = frappe.get_all("Customer",
                    filters=[
                        ["customer_name", "=", full_name],
                        ["customer_group", "=", "Student"]
                    ],
                    fields=["name", "customer_name", "customer_group", "territory"]
                )
                
                if existing_customers:
                    # Use the first matching customer and update their student ID
                    existing_customer = existing_customers[0]
                    frappe.db.set_value("Customer", existing_customer.name, "custom_student_id", doc_name)
                    frappe.db.commit()

            if not existing_customer:
                # Create customer if not exists
                customer_doc = frappe.get_doc({
                    "doctype": "Customer",
                    "customer_name": full_name,
                    "customer_type": "Individual",
                    "customer_group": "Student",
                    "territory": "Ghana",
                    "custom_student_id": doc_name
                })
                customer_doc.insert(ignore_permissions=True)
                frappe.db.commit()  # Commit customer creation
                
                # Refresh customer data
                existing_customer = frappe.db.get_value("Customer", 
                    {"custom_student_id": doc_name},
                    ["name", "customer_name", "customer_group", "territory"],
                    as_dict=1
                )

            # Get student's gender - this should match a value in the Gender doctype
            student_gender = doc.gender if hasattr(doc, 'gender') else None

            # Create patient
            patient_dict = {
                "doctype": "Patient",
                "name": doc_name,  # Set the name explicitly to student ID
                "naming_series": "HLC-PAT-.YYYY.-",
                "first_name": doc.first_name,
                "last_name": doc.last_name if doc.last_name else "",
                "patient_name": full_name,
                "custom_student_id": doc_name,
                "sex": student_gender,
                "dob": doc.date_of_birth if hasattr(doc, 'date_of_birth') else None,
                "email": doc.student_email_id if hasattr(doc, 'student_email_id') else None,
                "mobile": doc.student_mobile_number if hasattr(doc, 'student_mobile_number') else None,
                "status": "Active",
                "customer": existing_customer.name,
                "customer_group": existing_customer.customer_group,
                "territory": existing_customer.territory,
                # Disable automatic user creation since student already has an account
                "invite_user": 0
            }

            # Create the patient doc
            patient_doc = frappe.get_doc(patient_dict)
            
            # Set flags to handle customer linking and prevent automatic user creation
            patient_doc.flags.is_new_customer = False
            patient_doc.flags.existing_customer = True
            patient_doc.flags.skip_contact_creation = True  # Skip automatic contact creation
            patient_doc.flags.no_website_user = True  # Additional flag to prevent user creation
            patient_doc.flags.name_set = True  # Tell Frappe we're setting the name manually
            
            # Insert the patient
            patient_doc.insert(ignore_permissions=True)
            frappe.db.commit()  # Commit patient creation
            
            # Now create/update contact separately
            try:
                patient_doc.set_contact()
                frappe.db.commit()  # Commit contact changes
            except Exception as contact_error:
                frappe.log_error(
                    message=f"Non-critical error in contact creation: {str(contact_error)}\nPatient: {patient_doc.name}",
                    title="GCIHS Contact Creation Warning"
                )
            
            # Update the student record with the patient reference
            frappe.db.set_value("Student", doc_name, "patient", patient_doc.name)
            frappe.db.commit()

            frappe.log_error(
                message=f"Successfully created patient for student {doc_name} with customer {existing_customer.name}",
                title="GCIHS Debug - Patient Created"
            )
            
            return  # Success - exit the retry loop

        except frappe.exceptions.QueryDeadlockError:
            retry_count += 1
            if retry_count >= max_retries:
                frappe.log_error(
                    message=f"Max retries reached for patient creation: {doc_name}",
                    title="GCIHS Max Retries Error"
                )
                raise  # Re-raise the last deadlock error
            frappe.db.rollback()  # Rollback the transaction before retrying
            frappe.db.begin()  # Start a new transaction
            
        except Exception as e:
            frappe.log_error(
                message=f"Error in delayed patient creation: {str(e)}\nStudent: {doc_name}\nFull Error: {frappe.get_traceback()}",
                title="GCIHS Delayed Creation Error"
            )
            raise  # Re-raise other exceptions

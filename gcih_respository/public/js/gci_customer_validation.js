frappe.ui.form.on('Customer', {
    validate: function(frm) {
        if (frm.doc.student_id) {
            frappe.call({
                method: "gcih_respository.api.gci_customer_validation.validate_student_id",
                args: {
                    student_id: frm.doc.student_id,
                    customer_name: frm.doc.name || ""
                },
                callback: function(r) {
                    if (r.message && r.message.exists) {
                        frappe.validated = false;
                        frappe.msgprint({
                            title: __("Duplicate Student ID"),
                            indicator: "red",
                            message: __("Student ID {0} already exists for customer {1} ({2}). Student ID must be unique.", 
                                [frm.doc.student_id, r.message.customer_name, r.message.name])
                        });
                    }
                }
            });
        }
    },

    student_id: function(frm) {
        if (frm.doc.student_id) {
            frappe.call({
                method: "gcih_respository.api.gci_customer_validation.validate_student_id",
                args: {
                    student_id: frm.doc.student_id,
                    customer_name: frm.doc.name || ""
                },
                callback: function(r) {
                    if (r.message && r.message.exists) {
                        frappe.show_alert({
                            message: __("Warning: Student ID {0} already exists for customer {1} ({2})", 
                                [frm.doc.student_id, r.message.customer_name, r.message.name]),
                            indicator: "orange"
                        }, 10);
                    }
                }
            });
        }
    }
});

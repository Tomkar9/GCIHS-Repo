frappe.listview_settings['Patient'] = {
    add_fields: ["disabled"],
    get_indicator: function(doc) {
        if (doc.disabled === 1) {
            return [__("Disabled"), "gray", "disabled,=,1"];
        }
        return [__("Active"), "green", "disabled,=,0"];
    },
    onload: function(listview) {
        listview.page.add_inner_button(__('Get New Students'), function() {
            // Show confirmation dialog first
            frappe.confirm(
                __('This will fetch new students and create patient records. Existing student IDs will be skipped. Continue?'),
                () => {
                    // Show a loading message
                    frappe.show_progress(__('Creating Patient Records'), 0, 100);

                    frappe.call({
                        method: 'gcih_respository.gci_folder.gcihs_patient_api.get_new_students',
                        freeze: true,
                        freeze_message: __('Fetching and validating student records...'),
                        callback: function(response) {
                            frappe.hide_progress();
                            const { status, message, details } = response.message || {};
                            
                            if (status === "success") {
                                // Show success message with details
                                let msgContent = `<div>${message}</div>`;
                                if (details && details.skipped_students && details.skipped_students.length > 0) {
                                    msgContent += `<div style="margin-top: 10px;">
                                        <strong>Skipped Students:</strong>
                                        <div style="max-height: 150px; overflow-y: auto;">
                                            ${details.skipped_students.map(student => 
                                                `<div style="padding: 5px;">
                                                    ${student.id}: ${student.reason}
                                                </div>`
                                            ).join('')}
                                        </div>
                                    </div>`;
                                }

                                frappe.msgprint({
                                    title: __('Success'),
                                    message: msgContent,
                                    indicator: 'green',
                                    wide: true
                                });
                                listview.refresh();
                            } else {
                                // Show message
                                frappe.msgprint({
                                    title: __('Message'),
                                    message: message || __('No new students were added as patients.'),
                                    indicator: 'blue'
                                });
                            }
                        },
                        error: function(error) {
                            frappe.hide_progress();
                            frappe.msgprint({
                                title: __('Error'),
                                message: __('An error occurred while adding new patients from students. Please check the logs for details.'),
                                indicator: 'red'
                            });
                            console.error("Get New Students Error:", error);
                        }
                    });
                }
            );
        });
    }
};

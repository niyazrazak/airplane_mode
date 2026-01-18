// Copyright (c) 2026, Niyaz razak and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
	refresh(frm) {
        if (!frm.doc.docstatus) {
            frm.add_custom_button(__('Fetch Default Rent'), function() {
                fetch_default_rent(frm);
            }, __('Get'));
        }

	},
});


function fetch_default_rent(frm) {
    frappe.call({
        method: 'airplane_mode.tasks.get_default_rent',
        callback: function(r) {
            if (r.message) {
                frm.set_value('monthly_rent', r.message);
                
                frappe.show_alert({
                    message: __('Default rent fetched from Airport Settings'),
                    indicator: 'green'
                }, 3);
            }
        }
    });
}
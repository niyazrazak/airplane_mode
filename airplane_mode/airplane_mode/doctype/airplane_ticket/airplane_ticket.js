// Copyright (c) 2026, Niyaz razak and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button(__('Assign Seat'), () => {
            assign_seat(frm);
        }, __('Actions'));
    },
});


function assign_seat(frm) {
    let d = new frappe.ui.Dialog({
        title: 'Assign Seat',
        fields: [
            {
                label: 'Seat Number',
                fieldname: 'seat_number',
                fieldtype: 'Data',
                reqd: 1
            }
        ],
        primary_action_label: 'Assign',
        primary_action(values) {
            frm.set_value('seat', values.seat_number);
            frm.save();
            d.hide();
        }
    });

    d.show();
}
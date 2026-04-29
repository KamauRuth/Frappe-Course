frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        frm.add_custom_button('Assign Seat', function() {
            var seat_dialog = new frappe.ui.Dialog({
                title: 'Assign Seat',
                fields: [
                    {
                        fieldtype: 'Data',
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Assign',
                primary_action: function() {
                    var seat_number = seat_dialog.get_values().seat_number;
                    frm.set_value('seat', seat_number);
                    seat_dialog.close();
                }
            });
            seat_dialog.show();
        });
    }
});
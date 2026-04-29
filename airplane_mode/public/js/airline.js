frappe.ui.form.on('Airline', {
    refresh: function(frm) {
        if (frm.doc.website) {
            frm.add_custom_button('Visit Website', function() {
                window.open(frm.doc.website, '_blank');
            });
        }
    }
});
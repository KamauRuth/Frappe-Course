import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 240,
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 160,
        },
    ]

    data = frappe.db.sql(
        """
        SELECT
            al.name AS airline,
            COALESCE(SUM(tk.flight_price), 0) AS revenue
        FROM `tabAirline` al
        LEFT JOIN `tabAirplane` ap ON ap.airline = al.name
        LEFT JOIN `tabAirplane Ticket` tk ON tk.flight = ap.name AND tk.docstatus = 1
        GROUP BY al.name
        ORDER BY revenue DESC, al.name ASC
        """,
        as_dict=True,
    )

    return columns, data
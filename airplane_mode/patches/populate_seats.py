import frappe
import random
import string

def execute():
    # Get all Airplane Ticket records
    tickets = frappe.get_all("Airplane Ticket", fields=["name"])

    for ticket in tickets:
        # Generate random seat number (1-100)
        seat_number = random.randint(1, 100)
        # Generate random seat letter (A-E)
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        # Combine to create the seat value
        seat_value = f"{seat_number}{seat_letter}"

        # Update the ticket record with the new seat value
        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat_value)
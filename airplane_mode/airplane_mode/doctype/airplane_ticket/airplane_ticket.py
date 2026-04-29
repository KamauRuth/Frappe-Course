import frappe
import random
import string
from frappe.model.document import Document

class AirplaneTicket(Document):

    def validate(self):
        # Call other validation methods
        self.calculate_total_amount()
        self.remove_duplicate_addons()
        self.generate_seat()
        self.check_seat_availability()

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("You can only submit the ticket if status is Boarded")

    def calculate_total_amount(self):
        total_addons = 0
        for addon in self.add_ons:
            total_addons += addon.amount or 0

        self.total_amount = (self.flight_price or 0) + total_addons

    def remove_duplicate_addons(self):
        seen = set()
        unique_addons = []

        for addon in self.add_ons:
            if addon.item not in seen:
                seen.add(addon.item)
                unique_addons.append(addon)

        self.add_ons = unique_addons

    def generate_seat(self):
        # Generate random seat number (1-100)
        seat_number = random.randint(1, 100)
        # Generate random letter (A-E)
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        # Combine to create the seat value
        self.seat = f"{seat_number}{seat_letter}"

        def check_seat_availability(self):
            airplane = frappe.get_doc("Airplane", self.flight.airplane)
            ticket_count = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})
            
            if ticket_count >= airplane.capacity:
                frappe.throw("Cannot create ticket. Flight capacity exceeded.")
    
    
    def update_gate_number(flight_name):
        # Get the new gate number from the flight
        flight = frappe.get_doc("Flight", flight_name)
        new_gate_number = flight.gate_number
    
        # Update all linked airplane tickets with the new gate number
        tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])
        
        for ticket in tickets:
            frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)
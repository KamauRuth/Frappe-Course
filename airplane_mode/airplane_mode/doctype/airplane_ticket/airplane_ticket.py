import random

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def validate(self):
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
        seat_number = random.randint(1, 100)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{seat_number}{seat_letter}"

    def check_seat_availability(self):
        if not self.flight:
            return

        airplane = frappe.get_doc("Airplane", self.flight)
        ticket_count = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})

        if ticket_count >= airplane.capacity:
            frappe.throw("Cannot create ticket. Flight capacity exceeded.")



import random
import frappe
from random import randint

def execute():
	tickets = frappe.get_all("Airplane Ticket", filters={"seat": ""}, fields=["name"])
	letters = ["A", "B", "C", "D", "E"]
	for row in tickets:
		randnumber = randint(1, 100)
		randletter = random.choice(letters)
		seat = f"{randnumber}{randletter}"
		frappe.db.set_value("Airplane Ticket", row.name, "seat", seat)
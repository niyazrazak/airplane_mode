# Copyright (c) 2026, Niyaz razak and contributors
# For license information, please see license.txt

import random
import frappe
from frappe import _
from frappe.model.document import Document
from random import randint
from frappe.utils import flt


class AirplaneTicket(Document):
	def before_insert(self):
		airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		booked = frappe.db.count("Airplane Ticket", {"flight": self.flight})
		if booked >= capacity:
			frappe.throw(
				title="Flight Full",
				msg="Cannot issue ticket as the flight is already full."
			)
		self.set_seat_number()

	def validate(self):
		airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		booked = frappe.db.count("Airplane Ticket", {"flight": self.flight})
		if booked >= capacity:
			frappe.throw(
				title="Flight Full",
				msg="Cannot issue ticket as the flight is already full."
			)
		self.remove_duplicate()
		self.calculate_totals()
		# self.check_overbooking()

	def before_submit(self):
		if self.status != 'Boarded':
			frappe.throw(_(f"Airplane Ticket can only be submitted when status is 'Boarded'. Current status: '{self.status}'"))

	def calculate_totals(self):
		add_on_amount = sum(flt(d.amount) for d in self.add_ons)
		self.total_amount = flt(self.flight_price) + flt(add_on_amount)


	def remove_duplicate(self):
		seen = set()
		duplicates = []
		
		for row in self.add_ons:
			if row.item in seen:
				duplicates.append(row.item)
				self.remove(row)
			else:
				seen.add(row.item)
		
		if duplicates:
			frappe.msgprint(
				f"You can't have one add-on more than once. Removing: {', '.join(duplicates)}"
			)

	def set_seat_number(self):
		randnumber = randint(1, 100)
		letter = ("A", "B", "C", "D", "E")
		randletter = random.choice(letter)
		self.seat = f"{randnumber}{randletter}"

	def check_overbooking(self):
		airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		booked = frappe.db.count("Airplane Ticket", {"flight": self.flight})
		if booked > capacity:
			frappe.throw(_("Cannot book ticket: Flight is fully booked"))
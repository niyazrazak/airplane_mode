# Copyright (c) 2026, Niyaz razak and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopRentPayment(Document):
	def validate(self):
		contract_rent = frappe.db.get_value("Shop Contract", self.contract, "monthly_rent")

		if self.amount != contract_rent:
			frappe.throw(f"Payment Amount must be exactly {contract_rent}. You entered {self.amount}.")

	def on_submit(self):
		self.update_contract_schedule()

	def on_cancel(self):
		self.update_contract_schedule(cancel=True)

	def update_contract_schedule(self, cancel=False):
		contract = frappe.get_doc("Shop Contract", self.contract)
		
		updated = False
		
		# find a matching Unpaid row
		for row in contract.rent_schedules:
			if not cancel:
				if row.status == "Unpaid":
					row.status = "Paid"
					row.payment_ref = self.name
					updated = True
					break
			
			else:
				if row.payment_ref == self.name:
					row.status = "Unpaid"
					row.payment_ref = None
					updated = True
					break

		if updated:
			contract.save()
		else:
			if not cancel:
				frappe.msgprint("No unpaid schedule found for this Contract.")


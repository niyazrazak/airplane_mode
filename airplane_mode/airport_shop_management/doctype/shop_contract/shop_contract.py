# Copyright (c) 2026, Niyaz razak and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, add_days, add_months, nowdate
# from datetime import timedelta

class ShopContract(Document):
    def validate(self):
        self.validate_dates()
        self.validate_shop_availability()
        self.validate_rent_amount()
        if self.start_date and self.end_date and self.monthly_rent:
            self.set("rent_schedules", [])
            self.generate_schedule()
    
    def validate_dates(self):
        if not self.start_date:
            frappe.throw(_("Contract Start Date is required"), title=_("Missing Date"))
        
        if not self.end_date:
            frappe.throw(_("Contract End Date is required"), title=_("Missing Date"))
        
        start_date = getdate(self.start_date)
        end_date = getdate(self.end_date)
        
        # Ensure end date is after start date
        if end_date <= start_date:
            frappe.throw(
                _("Contract End Date must be after Contract Start Date."),
                title=_("Invalid Date Range")
            )
        
        # Minimum contract duration (1 year)
        minimum_end_date = add_days(start_date, 364)  # 1 year - 1 day
        if end_date < minimum_end_date:
            frappe.throw(
                _("Contract duration must be at least 1 year. Minimum end date: {0}").format(
                    minimum_end_date.strftime("%d-%m-%Y")
                ),
                title=_("Contract Too Short")
            )
        
    
    def validate_shop_availability(self):
        if not self.shop:
            return
        
        shop = frappe.get_doc("Airport Shop", self.shop)
        
        if shop.status == "Leased":
            # Check if there's an active contract
            active_contract = frappe.db.exists("Shop Contract", {
                "shop": self.shop,
                "docstatus": 1,
                "end_date": [">=", nowdate()]
            })
            
            if active_contract and active_contract != self.name:
                frappe.throw(
                    _("Shop {0} is already leased under active contract {1}.").format(
                        shop.shop_name, active_contract
                    ),
                    title=_("Shop Not Available")
                )
    
    def validate_rent_amount(self):
        if not self.monthly_rent or self.monthly_rent <= 0:
            frappe.throw(
                _("Monthly Rent must be greater than 0."),
                title=_("Invalid Rent Amount")
            )
    
    def on_submit(self):
        if not self.shop:
            frappe.throw(_("Shop is required to submit contract"))
        
        shop = frappe.get_doc("Airport Shop", self.shop)
        
        # Update shop details
        shop.status = "Leased"
        shop.tenant = self.tenant
        shop.contract_expiry = self.end_date
        
        shop.save(ignore_permissions=True)
        
        frappe.msgprint(
            _("Contract {0} submitted successfully. Shop {1} marked as 'Leased'").format(
                self.name, shop.shop_name
            ),
            alert=True,
            indicator="green"
        )
    
    def on_cancel(self):
        """Handle contract cancellation"""
        if self.shop:
            shop = frappe.get_doc("Airport Shop", self.shop)
            shop.status = "Available"
            shop.tenant = ""
            shop.contract_expiry = ""
            shop.save(ignore_permissions=True)
            
            frappe.msgprint(
                _("Contract cancelled. Shop {0} marked as 'Available' ").format(
                    shop.shop_name
                ),
                alert=True
            )


    def generate_schedule(self):
        current_date = getdate(self.start_date)
        end_date = getdate(self.end_date)
        
        while current_date <= end_date:
            self.append("rent_schedules", {
                "due_date": current_date,
                "amount": self.monthly_rent,
                "status": "Unpaid"
            })
            current_date = add_months(current_date, 1)
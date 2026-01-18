import frappe


@frappe.whitelist()
def get_shop_list():
    shops = frappe.db.get_all("Airport Shop", ["*"])
    return shops
# Copyright (c) 2026, Niyaz razak and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "airport",
            "label": _("Airport"),
            "fieldtype": "Link",
            "options": "Airport",
            "width": 200
        },
        {
            "fieldname": "available_shops",
            "label": _("Available Shops"),
            "fieldtype": "Int",
            "width": 150
        },
        {
            "fieldname": "occupied_shops",
            "label": _("Occupied Shops"),
            "fieldtype": "Int",
            "width": 150
        },
        {
            "fieldname": "total_shops",
            "label": _("Total Shops"),
            "fieldtype": "Int",
            "width": 150
        },
    ]

def get_data(filters):
    conditions = []
    params = {}
    
    if filters.get("airport"):
        conditions.append("shop.airport = %(airport)s")
        params["airport"] = filters.get("airport")
    
    if filters.get("shop_type"):
        conditions.append("shop.shop_type = %(shop_type)s")
        params["shop_type"] = filters.get("shop_type")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = """
        SELECT
            shop.airport,
            COUNT(CASE WHEN shop.status = 'Available' THEN 1 END) as available_shops,
            COUNT(CASE WHEN shop.status = 'Leased' THEN 1 END) as occupied_shops,
            COUNT(shop.name) as total_shops,
            ROUND(
                (COUNT(CASE WHEN shop.status = 'Leased' THEN 1 END) * 100.0 / 
                NULLIF(COUNT(shop.name), 0)), 2
            ) as occupancy_rate
        FROM `tabAirport Shop` shop
        WHERE {where_clause}
        GROUP BY shop.airport
        ORDER BY total_shops DESC
    """.format(where_clause=where_clause)
    
    return frappe.db.sql(query, params, as_dict=True)
    
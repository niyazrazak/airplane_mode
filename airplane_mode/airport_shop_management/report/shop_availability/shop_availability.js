// Copyright (c) 2026, Niyaz razak and contributors
// For license information, please see license.txt

frappe.query_reports["Shop Availability"] = {
	"filters": [
		{
			"fieldname": "airport",
			"label": __("Airport"),
			"fieldtype": "Link",
			"options": "Airport",
			"reqd": 0
		},
		{
			"fieldname": "shop_type",
			"label": __("Shop Type"),
			"fieldtype": "Link",
			"options": "Shop Type"
		}
	]
};

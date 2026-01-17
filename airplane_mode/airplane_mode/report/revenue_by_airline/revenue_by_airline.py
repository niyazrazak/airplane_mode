# Copyright (c) 2026, Niyaz razak and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):
	data, total_revenue = get_data(filters)
	columns = get_columns()

	chart = {
		"data": {
			"labels": [d["airline"] for d in data],
			"datasets": [{"values": [d["revenue"] for d in data]}],
		},
		"type": "donut",
	}

	report_summary = [{"label": "Total Revenue", "value": total_revenue, "indicator": "Green"}]

	return columns, data, None, chart, report_summary

def get_columns():
	columns = [
		{"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 140},
	]

	return columns

def get_data(filters):
	al = DocType("Airline")
	ap = DocType("Airplane")
	ft = DocType("Airplane Flight")
	tt = DocType("Airplane Ticket")

	query = (
		frappe.qb.from_(al)
		.left_join(ap)
		.on(ap.airline == al.name)
		.left_join(ft)
		.on(ft.airplane == ap.name)
		.left_join(tt)
		.on((tt.flight == ft.name) & (tt.docstatus == 1))
		.groupby(al.name)
		.select(
			al.name.as_("airline"),
			Sum(tt.total_amount).as_("revenue"),
		)
	)
	result = query.run(as_dict=True)

	data = []
	total_revenue = 0.0

	for r in result:
		revenue = float(r.get("revenue") or 0)
		data.append({"airline": r["airline"], "revenue": revenue})
		total_revenue += revenue
	
	return data, total_revenue
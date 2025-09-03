# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# import frappe

# DOCTYPES = [
#     "Co2 Mould Batch",
#     "Green Sand Hand Mould Batch",
#     "No-Bake Mould Batch",
#     "Jolt Squeeze Mould Batch",
#     "HPML Mould Batch"
# ]

# def execute(filters=None):
#     columns = get_columns()
#     data = []

#     for doctype in DOCTYPES:
#         docs = frappe.get_all(
#             doctype,
#             fields=["name", "total_cast_weight", "total_bunch_weight"],
#         )

#         for d in docs:
#             # fetch child rows (toolings)
#             mould_rows = frappe.get_all(
#                 "New Mould Table",
#                 filters={"parent": d.name, "parenttype": doctype},
#                 fields=["tooling"]
#             )

#             tooling_count = len(mould_rows)
#             total_yield = 0

#             for row in mould_rows:
#                 if row.tooling:
#                     yield_val = frappe.db.get_value("New Tooling", row.tooling, "yield")
#                     if yield_val:
#                         total_yield += float(yield_val)

#             avg_yield = total_yield / tooling_count if tooling_count else 0

#             data.append({
#                 "doctype_name": doctype,
#                 "id": d.name,
#                 "total_cast_weight": d.total_cast_weight,
#                 "total_bunch_weight": d.total_bunch_weight,
#                 "avg_yield": avg_yield,
#                 "no_of_batches": 1,   # one row = one batch
#                 "no_of_tooling": tooling_count
#             })

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Doctype Name", "fieldname": "doctype_name", "fieldtype": "Data", "width": 200},
#         {"label": "ID", "fieldname": "id", "fieldtype": "Data", "width": 180},
#         {"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Total Bunch Weight", "fieldname": "total_bunch_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Avg Yield", "fieldname": "avg_yield", "fieldtype": "Float", "precision": 2, "width": 120},
#         {"label": "No of Batches", "fieldname": "no_of_batches", "fieldtype": "Int", "width": 120},
#         {"label": "No of Tooling", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
#     ]


import frappe
from frappe import _

DOCTYPES = [
	"Co2 Mould Batch",
	"Green Sand Hand Mould Batch",
	"No-Bake Mould Batch",
	"Jolt Squeeze Mould Batch",
	"HPML Mould Batch",
]


def execute(filters=None):
	"""Execute the Number Card Mould report.

	Args:
	    filters (dict): Report filters including date range and doctype selection

	Returns:
	    tuple: (columns, data, None, None, report_summary)
	    - columns: Report column definitions
	    - data: Aggregated data rows
	    - report_summary: Number card definitions for UI display
	"""
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	report_summary = get_report_summary(data)
	return columns, data, None, None, report_summary


def get_data(filters):
	"""Fetch aggregated Mould data for the specified date range and doctype.

	Args:
	    filters (dict): Must contain date filters and optionally doctype_name

	Returns:
	    list: Single row with aggregated sums for the date range
	"""
	selected_doctype = filters.get("doctype_name")

	# if "All" selected or nothing selected, run for all doctypes
	doctypes_to_fetch = DOCTYPES if not selected_doctype or selected_doctype == "All" else [selected_doctype]

	# Aggregates
	total_cast_weight = 0
	total_bunch_weight = 0
	total_batches = 0
	total_toolings = 0
	total_yield = 0

	for doctype in doctypes_to_fetch:
		# Build date filter
		doc_filters = {}
		if filters.get("from_date") and filters.get("to_date"):
			doc_filters["creation"] = ["between", [filters["from_date"], filters["to_date"]]]
		elif filters.get("from_date"):
			doc_filters["creation"] = [">=", filters["from_date"]]
		elif filters.get("to_date"):
			doc_filters["creation"] = ["<=", filters["to_date"]]

		docs = frappe.get_all(
			doctype,
			filters=doc_filters,
			fields=["name", "total_cast_weight", "total_bunch_weight"],
			order_by="creation asc",
		)

		total_batches += len(docs)

		for d in docs:
			total_cast_weight += d.total_cast_weight or 0
			total_bunch_weight += d.total_bunch_weight or 0

			mould_rows = frappe.get_all(
				"New Mould Table", filters={"parent": d.name, "parenttype": doctype}, fields=["tooling"]
			)

			for row in mould_rows:
				if row.tooling:
					yield_val = frappe.db.get_value("New Tooling", row.tooling, "yield")
					if yield_val:
						total_yield += float(yield_val)
					total_toolings += 1

	avg_yield = total_yield / total_toolings if total_toolings else 0

	return [
		{
			"total_cast_weight": total_cast_weight,
			"total_bunch_weight": total_bunch_weight,
			"avg_yield": avg_yield,
			"no_of_batches": total_batches,
			"no_of_tooling": total_toolings,
		}
	]


def get_report_summary(result):
	"""Generate number card definitions for the report summary.

	Args:
	    result (list): Data rows from get_data()

	Returns:
	    list: Number card definitions with values, labels, and styling
	"""
	if not result:
		return []

	data = result[0]

	# Return number card definitions with different colors for visual distinction
	return [
		{
			"value": data.get("no_of_batches", 0),
			"label": _("Total Number of Batches"),
			"datatype": "Int",
			"indicator": "Red",
		},
		{
			"value": data.get("total_cast_weight", 0),
			"label": _("Total Cast Weight"),
			"datatype": "Float",
			"precision": 3,
			"indicator": "Blue",
		},
		{
			"value": data.get("total_bunch_weight", 0),
			"label": _("Total Bunch Weight"),
			"datatype": "Float",
			"precision": 3,
			"indicator": "Black",
		},
		{
			"value": data.get("avg_yield", 0),
			"label": _("Average Yield"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Green",
		},
		{
			"value": data.get("no_of_tooling", 0),
			"label": _("Total Number of Tooling"),
			"datatype": "Int",
			"indicator": "Orange",
		},
	]


def get_columns():
	return [
		{"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
		{
			"label": "Total Bunch Weight",
			"fieldname": "total_bunch_weight",
			"fieldtype": "Float",
			"width": 150,
		},
		{"label": "Avg Yield", "fieldname": "avg_yield", "fieldtype": "Float", "precision": 2, "width": 120},
		{"label": "No of Batches", "fieldname": "no_of_batches", "fieldtype": "Int", "width": 120},
		{"label": "No of Tooling", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
	]

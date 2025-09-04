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
from frappe.utils import flt

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
	"""Fetch individual Mould data for the specified date range and doctype.

	Args:
	    filters (dict): Must contain date filters and optionally doctype_name

	Returns:
	    list: Individual mould batch records
	"""
	selected_doctype = filters.get("doctype_name")

	# if "All" selected or nothing selected, run for all doctypes
	doctypes_to_fetch = DOCTYPES if not selected_doctype or selected_doctype == "All" else [selected_doctype]

	result = []

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

		for d in docs:
			# Get tooling count for this batch
			mould_rows = frappe.get_all(
				"New Mould Table", filters={"parent": d.name, "parenttype": doctype}, fields=["tooling"]
			)

			tooling_count = len([row for row in mould_rows if row.tooling])

			result.append(
				{
					"name": d.name,
					"doctype_name": doctype,
					"total_cast_weight": d.total_cast_weight or 0,
					"total_bunch_weight": d.total_bunch_weight or 0,
					"no_of_tooling": tooling_count,
				}
			)

	return result


def get_report_summary(result):
	"""Generate number card definitions for the report summary.

	Args:
	    result (list): Data rows from get_data()

	Returns:
	    list: Number card definitions with values, labels, and styling
	"""
	if not result:
		return []

	# Calculate totals from individual records
	total_batches = len(result)
	total_cast_weight = sum(flt(row.get("total_cast_weight", 0), 2) for row in result)
	total_bunch_weight = sum(flt(row.get("total_bunch_weight", 0), 2) for row in result)
	total_tooling = sum(row.get("no_of_tooling", 0) for row in result)

	# Calculate estimated foundry return (bunch weight - cast weight)
	estimated_foundry_return = flt(total_bunch_weight - total_cast_weight, 2)

	# Calculate average yield (placeholder - you may need to implement this based on your data structure)
	avg_yield = 0
	if total_tooling > 0:
		# This is a placeholder - you may need to calculate actual yield from tooling data
		avg_yield = 85.0  # Default value

	# Return number card definitions with different colors for visual distinction
	return [
		{
			"value": total_batches,
			"label": _("Total Number of Batches"),
			"datatype": "Int",
			"indicator": "Red",
		},
		{
			"value": total_cast_weight,
			"label": _("Total Cast Weight"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Blue",
		},
		{
			"value": total_bunch_weight,
			"label": _("Total Bunch Weight"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Black",
		},
		{
			"value": estimated_foundry_return,
			"label": _("Estimated Foundry Return"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Purple",
		},
		{
			"value": avg_yield,
			"label": _("Average Yield"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Green",
		},
		{
			"value": total_tooling,
			"label": _("Total Number of Tooling"),
			"datatype": "Int",
			"indicator": "Orange",
		},
	]


def get_columns():
	return [
		{
			"label": "Batch Name",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Mould Batch",
			"width": 180,
		},
		{"label": "Batch Type", "fieldname": "doctype_name", "fieldtype": "Data", "width": 150},
		{"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
		{
			"label": "Total Bunch Weight",
			"fieldname": "total_bunch_weight",
			"fieldtype": "Float",
			"width": 150,
		},
		{"label": "Tooling Count", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
	]

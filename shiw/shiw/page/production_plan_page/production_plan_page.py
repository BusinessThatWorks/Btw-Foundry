# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_context(context):
	"""Set up the context for the Production Plan page.

	This page displays production plan data with:
	- Production plan selection
	- Item-wise breakdown with actual vs required quantities
	- Department-wise filtering
	- Stock status (actual, open indent, open PO, combined)
	- Interactive data visualization
	"""
	context.title = _("Production Plan Dashboard")
	context.no_cache = 1

	# Set default values
	context.production_plan = frappe.form_dict.get("production_plan") or ""
	context.item_code = frappe.form_dict.get("item_code") or ""

	# Get production plans for dropdown
	context.production_plans = get_production_plans()

	# Get report data if production plan is selected
	if context.production_plan:
		context.report_data = get_production_plan_data(context.production_plan, context.item_code)
	else:
		context.report_data = {"columns": [], "data": [], "summary": []}

	return context


def get_production_plans():
	"""Get list of production plans for dropdown selection."""
	try:
		production_plans = frappe.db.sql(
			"""
			SELECT name, posting_date, title
			FROM `tabProduction Plan`
			WHERE docstatus != 2
			ORDER BY posting_date DESC
			LIMIT 50
		""",
			as_dict=True,
		)
		return production_plans
	except Exception as e:
		frappe.log_error(f"Error getting production plans: {str(e)}")
		return []


def get_production_plan_data(production_plan, item_code=None):
	"""Get production plan report data."""
	try:
		# Import the report module
		from shiw.shiw.report.production_plan_report.production_plan_report import execute

		# Set up filters
		filters = {"production_plan": production_plan}
		if item_code:
			filters["item_code"] = item_code

		# Execute the report
		result = execute(filters)
		columns, data = result

		# Calculate summary statistics
		summary = calculate_summary_stats(data)

		return {
			"columns": columns,
			"data": data,
			"summary": summary,
			"production_plan": production_plan,
			"item_code": item_code,
		}

	except Exception as e:
		frappe.log_error(f"Error in Production Plan Dashboard: {str(e)}")
		return {
			"columns": [],
			"data": [],
			"summary": [],
			"error": str(e),
		}


def calculate_summary_stats(data):
	"""Calculate summary statistics from the data."""
	if not data:
		return []

	# Calculate totals
	total_items = len(data)
	total_actual_qty = sum(row.get("actual_qty", 0) or 0 for row in data)
	total_required_qty = sum(row.get("required_bom_qty", 0) or 0 for row in data)
	total_open_indent = sum(row.get("open_indent", 0) or 0 for row in data)
	total_open_po = sum(row.get("open_po", 0) or 0 for row in data)
	total_combined_stock = sum(row.get("combined_stock", 0) or 0 for row in data)

	# Calculate shortage items (where actual < required)
	shortage_items = [
		row for row in data if (row.get("actual_qty", 0) or 0) < (row.get("required_bom_qty", 0) or 0)
	]
	shortage_count = len(shortage_items)

	return [
		{
			"value": total_items,
			"label": _("Total Items"),
			"datatype": "Int",
			"indicator": "Blue",
			"description": _("Total number of items in production plan"),
		},
		{
			"value": total_actual_qty,
			"label": _("Total Actual Qty"),
			"datatype": "Float",
			"indicator": "Green",
			"description": _("Total actual quantity available"),
			"precision": 2,
		},
		{
			"value": total_required_qty,
			"label": _("Total Required Qty"),
			"datatype": "Float",
			"indicator": "Orange",
			"description": _("Total required quantity for production"),
			"precision": 2,
		},
		{
			"value": shortage_count,
			"label": _("Shortage Items"),
			"datatype": "Int",
			"indicator": "Red",
			"description": _("Items with insufficient quantity"),
		},
		{
			"value": total_open_indent,
			"label": _("Total Open Indent"),
			"datatype": "Float",
			"indicator": "Purple",
			"description": _("Total quantity in open material requests"),
			"precision": 2,
		},
		{
			"value": total_open_po,
			"label": _("Total Open PO"),
			"datatype": "Float",
			"indicator": "Teal",
			"description": _("Total quantity in open purchase orders"),
			"precision": 2,
		},
		{
			"value": total_combined_stock,
			"label": _("Total Combined Stock"),
			"datatype": "Float",
			"indicator": "Black",
			"description": _("Total available stock (actual + open indent + open PO)"),
			"precision": 2,
		},
	]

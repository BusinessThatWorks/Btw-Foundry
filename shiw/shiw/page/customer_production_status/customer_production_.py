# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_customer_production_data(filters=None):
	"""
	Get customer production status data from the report.

	Args:
	    filters (dict): Sales Order ID and Customer Name filters

	Returns:
	    dict: Report data with columns and rows
	"""
	try:
		filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}

		# Import the report's execute function
		from shiw.report.customer_production_status.customer_production_status import execute

		# Get columns and data from the report
		columns, data = execute(filters)

		return {
			"success": True,
			"columns": columns,
			"data": data,
		}

	except Exception as e:
		frappe.log_error(f"Customer Production Dashboard Error: {str(e)}", "Customer Production Dashboard")
		return {
			"success": False,
			"message": _("An error occurred while fetching dashboard data"),
			"columns": [],
			"data": [],
		}

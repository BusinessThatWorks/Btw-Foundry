# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_context(context):
	"""Set up the context for the Heat Dashboard web page.

	This dashboard displays number cards for:
	- Total Charge Mix (Kg)
	- Liquid Balance
	- Burning Loss

	The data is filtered by date range and updates dynamically.
	"""
	context.title = _("Heat Dashboard")
	context.no_cache = 1

	# Set default date range (current month)
	from frappe.utils import getdate, month_start, month_end

	today = getdate()

	context.from_date = frappe.form_dict.get("from_date") or month_start(today)
	context.to_date = frappe.form_dict.get("to_date") or month_end(today)

	# Get the report data
	context.report_data = get_heat_report_data(context.from_date, context.to_date)

	return context


def get_heat_report_data(from_date, to_date):
	"""Get the number card data for the specified date range.

	Args:
	    from_date (str): Start date in YYYY-MM-DD format
	    to_date (str): End date in YYYY-MM-DD format

	Returns:
	    dict: Report data with number cards and summary
	"""
	try:
		# Import the report module
		from shiw.shiw.report.number_card_heat_report.number_card_heat_report import execute

		# Set up filters
		filters = {"from_date": from_date, "to_date": to_date}

		# Execute the report
		result = execute(filters)
		columns, data, _, _, report_summary = result

		return {
			"columns": columns,
			"data": data,
			"report_summary": report_summary,
			"from_date": from_date,
			"to_date": to_date,
		}

	except Exception as e:
		frappe.log_error(f"Error in Heat Dashboard: {str(e)}")
		return {
			"columns": [],
			"data": [],
			"report_summary": [],
			"from_date": from_date,
			"to_date": to_date,
			"error": str(e),
		}




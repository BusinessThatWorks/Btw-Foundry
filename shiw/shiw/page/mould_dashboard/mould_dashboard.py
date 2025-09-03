# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_context(context):
	"""Get context for the Mould Dashboard page.

	Args:
	    context (dict): Frappe page context
	"""
	context.title = _("Mould Dashboard")
	context.no_cache = 1

	# Set default date range (current month)
	from frappe.utils import getdate, month_start, month_end

	today = getdate()
	context.from_date = month_start(today)
	context.to_date = month_end(today)

	# Get initial data
	context.report_data = get_mould_report_data({"from_date": context.from_date, "to_date": context.to_date})


def get_mould_report_data(filters):
	"""Get mould report data for the dashboard.

	Args:
	    filters (dict): Report filters

	Returns:
	    dict: Report data with columns, data, and report_summary
	"""
	from shiw.shiw.report.number_card_mould_report.number_card_mould_report import execute

	try:
		result = execute(filters)
		columns, data, _, _, report_summary = result

		return {"columns": columns, "data": data, "report_summary": report_summary}
	except Exception as e:
		frappe.log_error(f"Error in mould dashboard: {str(e)}")
		return {"columns": [], "data": [], "report_summary": []}



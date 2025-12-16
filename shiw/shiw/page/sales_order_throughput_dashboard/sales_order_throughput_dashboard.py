import frappe
from frappe.utils import get_first_day, get_last_day, getdate, today


@frappe.whitelist()
def get_data(filters=None):
	"""Get data for Sales Order Dashboard - calls the report directly"""
	filters = frappe.parse_json(filters) if isinstance(filters, str) else (filters or {})

	# Ensure date defaults (current month) if missing - same as report
	fd = filters.get("from_date")
	td = filters.get("to_date")
	if not fd or not td:
		cur = today()
		fd = fd or get_first_day(cur)
		td = td or get_last_day(cur)
	filters["from_date"] = str(getdate(fd))
	filters["to_date"] = str(getdate(td))

	# Call the report's execute function directly
	from shiw.shiw.report.sales_order_item_report.sales_order_item_report import execute as report_execute

	columns, rows = report_execute(filters)

	return {"columns": columns, "rows": rows}

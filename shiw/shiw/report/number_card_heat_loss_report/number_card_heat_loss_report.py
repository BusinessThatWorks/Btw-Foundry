# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate
import calendar


def execute(filters=None):
	"""Number Card Heat Loss report for Daily Heat Loss.

	Returns parent rows for Daily Heat Loss entries and summary cards with averages
	over the selected date range.
	"""
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	report_summary = get_report_summary(data)
	return columns, data, None, None, report_summary


def get_columns():
	return [
		{
			"label": "Name",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Daily Heat Loss",
			"width": 180,
		},
		{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
		{
			"label": "Target Liquid Metal",
			"fieldname": "target_liquid_metal",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": "Achieved Liquid Metal",
			"fieldname": "achieved_liquid_metal",
			"fieldtype": "Float",
			"width": 180,
		},
		{"label": "% Achieved", "fieldname": "achieved", "fieldtype": "Percent", "width": 120},
		{"label": "Loss Liquid Metal", "fieldname": "loss_liquid_metal", "fieldtype": "Float", "width": 180},
	]


def get_data(filters):
	# Default to current month if dates not provided (for direct report usage)
	if not filters.get("from_date") or not filters.get("to_date"):
		today = getdate()
		first_day = today.replace(day=1)
		last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
		filters["from_date"] = filters.get("from_date") or first_day
		filters["to_date"] = filters.get("to_date") or last_day

	conditions = ["date BETWEEN %(from_date)s AND %(to_date)s", "docstatus = 1"]
	params = {
		"from_date": filters.get("from_date"),
		"to_date": filters.get("to_date"),
	}

	where_clause = " AND ".join(conditions)

	rows = frappe.db.sql(
		f"""
		SELECT
			name,
			date,
			ifnull(target_liquid_metal, 0) as target_liquid_metal,
			ifnull(achieved_liquid_metal, 0) as achieved_liquid_metal,
			ifnull(achieved, 0) as achieved,
			ifnull(loss_liquid_metal, 0) as loss_liquid_metal
		FROM `tabDaily Heat Loss`
		WHERE {where_clause}
		ORDER BY date DESC, name DESC
		""",
		params,
		as_dict=True,
	)

	return rows


def get_report_summary(rows):
	count = len(rows)
	if count == 0:
		avg_target = avg_achieved_liq = avg_achieved_pct = avg_loss_liq = 0
	else:
		avg_target = sum(flt(r.get("target_liquid_metal") or 0) for r in rows) / count
		avg_achieved_liq = sum(flt(r.get("achieved_liquid_metal") or 0) for r in rows) / count
		avg_achieved_pct = sum(flt(r.get("achieved") or 0) for r in rows) / count
		avg_loss_liq = sum(flt(r.get("loss_liquid_metal") or 0) for r in rows) / count

	return [
		{
			"value": avg_target,
			"label": _("Target Liquid Metal (Avg)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Blue",
		},
		{
			"value": avg_achieved_liq,
			"label": _("Achieved Liquid Metal (Avg)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Green",
		},
		{
			"value": avg_achieved_pct,
			"label": _("% Achieved (Avg)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Teal",
		},
		{
			"value": avg_loss_liq,
			"label": _("Loss Liquid Metal (Avg)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Orange",
		},
	]

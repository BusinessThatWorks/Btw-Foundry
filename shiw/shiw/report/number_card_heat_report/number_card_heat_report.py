# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, flt


def execute(filters=None):
	"""Generate number card report for Heat data with summary cards.

	This report displays aggregated metrics as number cards:
	- Total Charge Mix (Kg): Sum of all charge mix weights in date range
	- Liquid Balance: Sum of all liquid balance weights in date range
	- Burning Loss: Sum of all burning loss values in date range

	Args:
	    filters (dict): Must contain 'from_date' and 'to_date' for date range filtering

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


def get_columns():
	"""Define the columns for the tabular report view."""
	return [
		{
			"label": "Heat Entry",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Heat",
			"width": 180,
		},
		{
			"label": "Grade",
			"fieldname": "material_grade",
			"fieldtype": "Link",
			"options": "Grade Master",
			"width": 120,
		},
		{
			"label": "Furnace No",
			"fieldname": "furnace_no",
			"fieldtype": "Link",
			"options": "Furnace - Master",
			"width": 120,
		},
		{
			"label": "Total Charge Mix (Kg)",
			"fieldname": "total_charge_mix_in_kg",
			"fieldtype": "Float",
			"width": 180,
		},
		{"label": "Liquid Balance", "fieldname": "liquid_balence", "fieldtype": "Float", "width": 160},
		{
			"label": "Foundry Return Existing",
			"fieldname": "foundry_return_existing",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": "Liquid Metal Pig",
			"fieldname": "liquid_metal_pig",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": "Per Kg Cost (₹)",
			"fieldname": "per_kg_cost",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": "Burning Loss (%)",
			"fieldname": "burning_loss_percentage",
			"fieldtype": "Float",
			"width": 160,
		},
	]


def get_data(filters):
	"""Fetch aggregated Heat data for the specified date range.

	Args:
	    filters (dict): Must contain 'from_date' and 'to_date', optionally 'furnace_no'

	Returns:
	    list: Single row with aggregated sums for the date range
	"""
	if not filters.get("from_date") or not filters.get("to_date"):
		return []

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	furnace_no = filters.get("furnace_no")

	# Build WHERE conditions
	conditions = ["date BETWEEN %(from_date)s AND %(to_date)s"]
	params = {"from_date": from_date, "to_date": to_date}
	conditions.append("docstatus = 1")

	if furnace_no:
		conditions.append("furnace_no = %(furnace_no)s")
		params["furnace_no"] = furnace_no

	where_clause = " AND ".join(conditions)

	# Get total sums for the given date range from Heat doctype
	result = frappe.db.sql(
		f"""
        SELECT
			name,
			date,
			material_grade,
			furnace_no,
            ifnull(total_charge_mix_in_kg,0) as total_charge_mix_in_kg,
            ifnull(liquid_balence,0) as liquid_balence,
            ifnull(foundry_return_existing,0) as foundry_return_existing,
            ifnull(liquid_metal_pig,0) as liquid_metal_pig,
            ifnull(burning_loss,0) as burning_loss,
            ifnull(total_charge_mix_valuation,0) as total_charge_mix_valuation
        FROM `tabHeat`
        WHERE {where_clause}
        """,
		params,
		as_dict=True,
	)

	# Calculate per kg cost for each row
	for row in result:
		row["per_kg_cost"] = calculate_per_kg_cost(row["total_charge_mix_valuation"], row["liquid_balence"])

	return result


def calculate_per_kg_cost(total_charge_mix_valuation, liquid_balance):
	"""
	Calculate per kg cost based on liquid balance.

	Args:
	    total_charge_mix_valuation (float): Total charge mix valuation in rupees
	    liquid_balance (float): Liquid balance in kg

	Returns:
	    float: Per kg cost in rupees
	"""
	if liquid_balance > 0:
		return flt(total_charge_mix_valuation / liquid_balance, 2)
	else:
		# If liquid balance is 0, return the total charge mix valuation
		return flt(total_charge_mix_valuation, 2)


# def get_data(filters):
# 	"""Fetch aggregated Heat data for the specified date range.

# 	Args:
# 	    filters (dict): Must contain 'from_date' and 'to_date', optionally 'furnace_no'

# 	Returns:
# 	    list: Single row with aggregated sums for the date range
# 	"""
# 	if not filters.get("from_date") or not filters.get("to_date"):
# 		return []

# 	from_date = filters.get("from_date")
# 	to_date = filters.get("to_date")
# 	furnace_no = filters.get("furnace_no")

# 	# Build WHERE conditions
# 	conditions = ["date BETWEEN %(from_date)s AND %(to_date)s"]
# 	params = {"from_date": from_date, "to_date": to_date}

# 	if furnace_no:
# 		conditions.append("furnace_no = %(furnace_no)s")
# 		params["furnace_no"] = furnace_no

# 	where_clause = " AND ".join(conditions)

# 	# Get total sums for the given date range from Heat doctype
# 	result = frappe.db.sql(
# 		f"""
#         SELECT
#             COUNT(*) as total_heats,
#             SUM(ifnull(total_charge_mix_in_kg,0)) as total_charge_mix_in_kg,
#             SUM(ifnull(liquid_balence,0)) as liquid_balence,
#             SUM(ifnull(burning_loss,0)) as burning_loss
#         FROM `tabHeat`
#         WHERE {where_clause}
#         """,
# 		params,
# 		as_dict=True,
# 	)
# 	return result


def get_report_summary(result):
	"""Generate number card definitions for the report summary.

	Args:
	    result (list): Data rows from get_data()

	Returns:
	    list: Number card definitions with values, labels, and styling
	"""
	num = len(result)
	# Calculate totals from the result data
	total_heats = num
	total_charge_mix_in_kg = sum(flt(row["total_charge_mix_in_kg"], 2) for row in result)
	liquid_balence = sum(flt(row["liquid_balence"], 2) for row in result)
	total_foundry_return_existing = sum(flt(row.get("foundry_return_existing", 0), 2) for row in result)
	total_liquid_metal_pig = sum(flt(row.get("liquid_metal_pig", 0), 2) for row in result)

	# Calculate average burning loss percentage: Sum of individual burning loss percentages / Number of heats
	# If liquid balance is 0 for a heat, burning loss should be 0% (not 100%)
	total_burning_loss_percentage = 0
	valid_heats = 0

	for row in result:
		individual_burning_loss = 0
		if row["total_charge_mix_in_kg"] > 0 and row["liquid_balence"] > 0:
			individual_burning_loss = (
				(row["total_charge_mix_in_kg"] - row["liquid_balence"]) / row["total_charge_mix_in_kg"]
			) * 100
		elif row["liquid_balence"] == 0:
			individual_burning_loss = 0  # When liquid balance is 0, burning loss should be 0%

		total_burning_loss_percentage += individual_burning_loss
		valid_heats += 1

	burning_loss_percentage = total_burning_loss_percentage / valid_heats if valid_heats > 0 else 0

	# Return number card definitions with different colors for visual distinction
	return [
		{
			"value": total_heats,
			"label": _("Total Number of Heat"),
			"datatype": "Int",
			"indicator": "Red",
		},
		{
			"value": total_charge_mix_in_kg,
			"label": _("Total Charge Mix (Kg)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Blue",
		},
		{
			"value": liquid_balence,
			"label": _("Liquid Balance"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Black",
		},
		{
			"value": total_foundry_return_existing,
			"label": _("Foundry Return Existing"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Purple",
		},
		{
			"value": total_liquid_metal_pig,
			"label": _("Liquid Metal Pig"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Teal",
		},
		{
			"value": burning_loss_percentage,
			"label": _("Burning Loss (%)"),
			"datatype": "Float",
			"precision": 2,
			"indicator": "Green",
		},
	]

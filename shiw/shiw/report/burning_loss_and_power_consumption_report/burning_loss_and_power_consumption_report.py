# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# def execute(filters=None):
# 	from_date = filters.get("from_date")
# 	to_date = filters.get("to_date")
# 	furnace_no = filters.get("furnace_no")
# 	material_grade = filters.get("material_grade")

# 	columns = [
# 		{"label": "Id", "fieldname": "id", "fieldtype": "Link", "options": "Heat", "width": 120},
# 		{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
# 		{"label": "Shift", "fieldname": "shift", "fieldtype": "Data", "width": 100},
# 		{
# 			"label": "Furnace",
# 			"fieldname": "furnace_no",
# 			"fieldtype": "Link",
# 			"options": "Furnace - Master",
# 			"width": 140,
# 		},
# 		{
# 			"label": "Grade",
# 			"fieldname": "material_grade",
# 			"fieldtype": "Link",
# 			"options": "Grade Master",
# 			"width": 120,
# 		},
# 		{"label": "Power Consumption", "fieldname": "power_consumption", "fieldtype": "Float", "width": 150},
# 		{"label": "Burning Loss", "fieldname": "burning_loss", "fieldtype": "Float", "width": 120},
# 	]

# 	filters_dict = {"date": ["between", [from_date, to_date]]}

# 	if furnace_no:
# 		filters_dict["furnace_no"] = furnace_no

# 	if material_grade:
# 		filters_dict["material_grade"] = material_grade

# 	data = frappe.db.get_all(
# 		"Heat",
# 		fields=[
# 			"name as id",
# 			"date",
# 			"shift_timing as shift",
# 			"furnace_no",
# 			"material_grade",
# 			"power_consumptionkwh as power_consumption",
# 			"burning_loss",
# 		],
# 		filters=filters_dict,
# 		order_by="date DESC, shift_timing ASC",
# 	)

# 	return columns, data



def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	furnace_no = filters.get("furnace_no")
	material_grade = filters.get("material_grade")

	columns = [
		{"label": "Id", "fieldname": "id", "fieldtype": "Link", "options": "Heat", "width": 120},
		{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
		{"label": "Shift", "fieldname": "shift", "fieldtype": "Data", "width": 100},
		{
			"label": "Furnace",
			"fieldname": "furnace_no",
			"fieldtype": "Link",
			"options": "Furnace - Master",
			"width": 140,
		},
		{
			"label": "Grade",
			"fieldname": "material_grade",
			"fieldtype": "Link",
			"options": "Grade Master",
			"width": 120,
		},
		{"label": "Power Consumption", "fieldname": "power_consumption", "fieldtype": "Float", "width": 150},
		{"label": "Burning Loss", "fieldname": "burning_loss", "fieldtype": "Float", "width": 120},
		{"label": "Total Charge Mix In Kg", "fieldname": "total_charge_mix_in_kg", "fieldtype": "Float", "width": 180},
		{"label": "Liquid metal at weighing Bal.", "fieldname": "liquid_balence", "fieldtype": "Float", "width": 220},
		{"label": "Rate per Kg", "fieldname": "rate_per_kg", "fieldtype": "Float", "width": 150},
	]

	filters_dict = {"date": ["between", [from_date, to_date]]}

	if furnace_no:
		filters_dict["furnace_no"] = furnace_no

	if material_grade:
		filters_dict["material_grade"] = material_grade

	# fetch records
	data = frappe.db.get_all(
		"Heat",
		fields=[
			"name as id",
			"date",
			"shift_timing as shift",
			"furnace_no",
			"material_grade",
			"power_consumptionkwh as power_consumption",
			"burning_loss",
			"total_charge_mix_in_kg",
			"liquid_balence",
		],
		filters=filters_dict,
		order_by="date DESC, shift_timing ASC",
	)

	# compute rate per kg
	for row in data:
		total = row.get("total_charge_mix_in_kg") or 0
		liquid = row.get("liquid_balence") or 0
		row["rate_per_kg"] = round((total / liquid), 2) if liquid else 0

	return columns, data

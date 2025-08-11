# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# import frappe
# import calendar


# def execute(filters=None):
# 	if not filters:
# 		return [], []

# 	month = filters.get("month")
# 	year = int(filters.get("year"))
# 	month_index = list(calendar.month_name).index(month)
# 	days_in_month = calendar.monthrange(year, month_index)[1]

# 	# Column headers
# 	columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

# 	def get_date(day):
# 		return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

# 	data = []

# 	# Row 1: Raw Materials Received (Accepted Quantity from Purchase Receipt Items)
# 	row_raw_materials = ["Raw Materials Received"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)

# 		accepted_qty = (
# 			frappe.db.sql(
# 				"""
#             SELECT SUM(pri.qty)
#             FROM `tabPurchase Receipt` pr
#             JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#             JOIN `tabItem` i ON i.name = pri.item_code
#             WHERE pr.posting_date = %s
#               AND i.item_group = 'Raw Material'
#         """,
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)

# 		row_raw_materials.append(accepted_qty)

# 	data.append(row_raw_materials)


# 	return columns, data


# import frappe
# import calendar


# def execute(filters=None):
# 	if not filters:
# 		return [], []

# 	month = filters.get("month")
# 	year = int(filters.get("year"))
# 	month_index = list(calendar.month_name).index(month)
# 	days_in_month = calendar.monthrange(year, month_index)[1]

# 	# Column headers
# 	columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

# 	def get_date(day):
# 		return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

# 	data = []

# 	# Row 1: Raw Materials Received (Accepted Quantity from Purchase Receipt Items)
# 	row_raw_materials = ["Raw Materials Received"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)

# 		accepted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(pri.qty)
# 				FROM `tabPurchase Receipt` pr
# 				JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
# 				JOIN `tabItem` i ON i.name = pri.item_code
# 				WHERE pr.posting_date = %s
# 				  AND i.item_group = 'Raw Material'
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)

# 		row_raw_materials.append(accepted_qty)

# 	data.append(row_raw_materials)

# 	# Row 2: Raw Materials Melted (from Heat Doctype)
# 	row_rm_melted = ["Raw Materials Melted"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)

# 		melted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_charge_mix_in_kg)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)

# 		row_rm_melted.append(melted_qty)

# 	data.append(row_rm_melted)

# 	# Row 3: Raw Materials Stock (as of each day, from Stock Ledger Entry)
# 	row_rm_stock = ["Raw Materials Stock"]

# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)

# 		stock_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(sle.actual_qty)
# 				FROM `tabStock Ledger Entry` sle
# 				JOIN `tabItem` i ON sle.item_code = i.name
# 				WHERE sle.posting_date <= %s
# 				AND sle.warehouse = 'Stores - SHIW'
# 				AND i.item_group = 'Raw Material'
# 				AND sle.is_cancelled = 0
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)

# 		row_rm_stock.append(stock_qty)

# 	data.append(row_rm_stock)

# 	return columns, data


# import frappe
# import calendar


# def execute(filters=None):
# 	if not filters:
# 		return [], []

# 	month = filters.get("month")
# 	year = int(filters.get("year"))
# 	month_index = list(calendar.month_name).index(month)
# 	days_in_month = calendar.monthrange(year, month_index)[1]

# 	# Column headers
# 	columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

# 	def get_date(day):
# 		return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

# 	data = []

# 	# Row 1: Raw Materials Received
# 	row_raw_materials = ["Raw Materials Received"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		accepted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(pri.qty)
# 				FROM `tabPurchase Receipt` pr
# 				JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
# 				JOIN `tabItem` i ON i.name = pri.item_code
# 				WHERE pr.posting_date = %s
# 				  AND i.item_group = 'Raw Material'
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_raw_materials.append(accepted_qty)
# 	data.append(row_raw_materials)

# 	# Row 2: Raw Materials Melted
# 	row_rm_melted = ["Raw Materials Melted"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		melted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_charge_mix_in_kg)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_melted.append(melted_qty)
# 	data.append(row_rm_melted)

# 	# Row 3: Raw Materials Stock
# 	row_rm_stock = ["Raw Materials Stock"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		stock_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(sle.actual_qty)
# 				FROM `tabStock Ledger Entry` sle
# 				JOIN `tabItem` i ON sle.item_code = i.name
# 				WHERE sle.posting_date <= %s
# 				AND sle.warehouse = 'Stores - SHIW'
# 				AND i.item_group = 'Raw Material'
# 				AND sle.is_cancelled = 0
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_stock.append(stock_qty)
# 	data.append(row_rm_stock)

# 	# Row 4: Liquid Metal Generated
# 	row_liquid_metal = ["Liquid Metal Generated"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		liquid_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(liquid_balence)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_liquid_metal.append(liquid_qty)
# 	data.append(row_liquid_metal)

# 	return columns, data


# import frappe
# import calendar


# def execute(filters=None):
# 	if not filters:
# 		return [], []

# 	month = filters.get("month")
# 	year = int(filters.get("year"))
# 	month_index = list(calendar.month_name).index(month)
# 	days_in_month = calendar.monthrange(year, month_index)[1]

# 	# Column headers
# 	columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

# 	def get_date(day):
# 		return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

# 	data = []

# 	# Row 1: Raw Materials Received
# 	row_raw_materials = ["Raw Materials Received"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		accepted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(pri.qty)
# 				FROM `tabPurchase Receipt` pr
# 				JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
# 				JOIN `tabItem` i ON i.name = pri.item_code
# 				WHERE pr.posting_date = %s
# 				  AND i.item_group = 'Raw Material'
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_raw_materials.append(accepted_qty)
# 	data.append(row_raw_materials)

# 	# Row 2: Raw Materials Melted
# 	row_rm_melted = ["Raw Materials Melted"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		melted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_charge_mix_in_kg)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_melted.append(melted_qty)
# 	data.append(row_rm_melted)

# 	# Row 3: Raw Materials Stock
# 	row_rm_stock = ["Raw Materials Stock"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		stock_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(sle.actual_qty)
# 				FROM `tabStock Ledger Entry` sle
# 				JOIN `tabItem` i ON sle.item_code = i.name
# 				WHERE sle.posting_date <= %s
# 				AND sle.warehouse = 'Stores - SHIW'
# 				AND i.item_group = 'Raw Material'
# 				AND sle.is_cancelled = 0
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_stock.append(stock_qty)
# 	data.append(row_rm_stock)

# 	# Row 4: Liquid Metal Generated
# 	row_liquid_metal = ["Liquid Metal Generated"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		liquid_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(liquid_balence)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_liquid_metal.append(liquid_qty)
# 	data.append(row_liquid_metal)

# 	# Row 5: Liquid Metal Returned to Furnace
# 	row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		returned_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(foundry_return_existing)
# 				FROM `tabHeat`
# 				WHERE `date` = %s
# 				AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_returned_to_furnace.append(returned_qty)
# 	data.append(row_returned_to_furnace)

# 	return columns, data














# import frappe
# import calendar


# def execute(filters=None):
# 	if not filters:
# 		return [], []

# 	month = filters.get("month")
# 	year = int(filters.get("year"))
# 	month_index = list(calendar.month_name).index(month)
# 	days_in_month = calendar.monthrange(year, month_index)[1]

# 	# Column headers
# 	columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

# 	def get_date(day):
# 		return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

# 	data = []

# 	# Row 1: Raw Materials Received
# 	row_raw_materials = ["Raw Materials Received"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		accepted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(pri.qty)
# 				FROM `tabPurchase Receipt` pr
# 				JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
# 				JOIN `tabItem` i ON i.name = pri.item_code
# 				WHERE pr.posting_date = %s
# 				AND i.item_group = 'Raw Material'
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_raw_materials.append(accepted_qty)
# 	data.append(row_raw_materials)

# 	# Row 2: Raw Materials Melted
# 	row_rm_melted = ["Raw Materials Melted"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		melted_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_charge_mix_in_kg)
# 				FROM `tabHeat`
# 				WHERE `date` = %s AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_melted.append(melted_qty)
# 	data.append(row_rm_melted)

# 	# Row 3: Raw Materials Stock
# 	row_rm_stock = ["Raw Materials Stock"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		stock_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(sle.actual_qty)
# 				FROM `tabStock Ledger Entry` sle
# 				JOIN `tabItem` i ON sle.item_code = i.name
# 				WHERE sle.posting_date <= %s
# 				AND sle.warehouse = 'Stores - SHIW'
# 				AND i.item_group = 'Raw Material'
# 				AND sle.is_cancelled = 0
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_rm_stock.append(stock_qty)
# 	data.append(row_rm_stock)

# 	# Row 4: Liquid Metal Generated
# 	row_liquid_metal = ["Liquid Metal Generated"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		liquid_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(liquid_balence)
# 				FROM `tabHeat`
# 				WHERE `date` = %s AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_liquid_metal.append(liquid_qty)
# 	data.append(row_liquid_metal)

# 	# Row 5: Liquid Metal Returned to Furnace
# 	row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		returned_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(foundry_return_existing)
# 				FROM `tabHeat`
# 				WHERE `date` = %s AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_returned_to_furnace.append(returned_qty)
# 	data.append(row_returned_to_furnace)

# 	# Row 6: Liquid Metal Pigged
# 	row_liquid_metal_pig = ["Liquid Metal Pigged"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		pig_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(liquid_metal_pig)
# 				FROM `tabHeat`
# 				WHERE `date` = %s AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_liquid_metal_pig.append(pig_qty)
# 	data.append(row_liquid_metal_pig)

# 	# Row 7: Burning Loss %
# 	row_burning_loss = ["Burning Loss %"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		loss_pct = (
# 			frappe.db.sql(
# 				"""
# 				SELECT AVG(burning_loss)
# 				FROM `tabHeat`
# 				WHERE `date` = %s AND docstatus = 1
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_burning_loss.append(round(loss_pct, 2))
# 	data.append(row_burning_loss)

# 	# Row 8: Co2 Mould Bunch Weight
# 	row_bunch_weight = ["Co2 Mould Bunch Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		bunch_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_bunch_weight)
# 				FROM `tabCo2 Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_bunch_weight.append(bunch_weight)
# 	data.append(row_bunch_weight)

# 	# Row 9: Co2 Mould Cast Weight
# 	row_cast_weight = ["Co2 Mould Cast Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		cast_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_cast_weight)
# 				FROM `tabCo2 Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_cast_weight.append(cast_weight)
# 	data.append(row_cast_weight)

# 	# Row 10: HPML Mould Cast Weight
# 	row_hpml_cast_weight = ["HPML Mould Cast Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		hpml_cast_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_cast_weight)
# 				FROM `tabHPML Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_hpml_cast_weight.append(hpml_cast_weight)
# 	data.append(row_hpml_cast_weight)

# 	# Row 11: HPML Mould Bunch Weight
# 	row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		hpml_bunch_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_bunch_weight)
# 				FROM `tabHPML Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_hpml_bunch_weight.append(hpml_bunch_weight)
# 	data.append(row_hpml_bunch_weight)

# 	# Row 12: No-Bake Mould Bunch Weight
# 	row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		nb_bunch_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_bunch_weight)
# 				FROM `tabNo-Bake Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_nb_bunch_weight.append(nb_bunch_weight)
# 	data.append(row_nb_bunch_weight)

# 	# Row 13: No-Bake Mould Cast Weight
# 	row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		nb_cast_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_cast_weight)
# 				FROM `tabNo-Bake Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_nb_cast_weight.append(nb_cast_weight)
# 	data.append(row_nb_cast_weight)

# 	# Row 14: Jolt Squeeze Mould Bunch Weight
# 	row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		js_bunch_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_bunch_weight)
# 				FROM `tabJolt Squeeze Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_js_bunch_weight.append(js_bunch_weight)
# 	data.append(row_js_bunch_weight)

# 	# Row 15: Jolt Squeeze Mould Cast Weight
# 	row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		js_cast_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_cast_weight)
# 				FROM `tabJolt Squeeze Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_js_cast_weight.append(js_cast_weight)
# 	data.append(row_js_cast_weight)

# 	# Row 16: Green Sand Hand Mould Bunch Weight
# 	row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		gs_bunch_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_bunch_weight)
# 				FROM `tabGreen Sand Hand Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_gs_bunch_weight.append(gs_bunch_weight)
# 	data.append(row_gs_bunch_weight)

# 	# Row 17: Green Sand Hand Mould Cast Weight
# 	row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		gs_cast_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_cast_weight)
# 				FROM `tabGreen Sand Hand Mould Batch`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_gs_cast_weight.append(gs_cast_weight)
# 	data.append(row_gs_cast_weight)

# 	# Row 18: Fettling Weight
# 	row_fettling_weight = ["Fettling Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		fettling_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_fettling_weight)
# 				FROM `tabFettling`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_fettling_weight.append(fettling_weight)
# 	data.append(row_fettling_weight)

# 	# Row 19: Finishing Weight
# 	row_finishing_weight = ["Finishing Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		finishing_weight = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(total_finishing_weight)
# 				FROM `tabFinishing`
# 				WHERE `date` = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_finishing_weight.append(finishing_weight)
# 	data.append(row_finishing_weight)
# 	# Row 20: Finished Stock Weight
# 	row_fs_stock = ["Finished Stock Weight"]
# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)
# 		stock_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(sle.actual_qty)
# 				FROM `tabStock Ledger Entry` sle
# 				JOIN `tabItem` i ON sle.item_code = i.name
# 				WHERE sle.posting_date <= %s
# 				AND sle.warehouse = 'FInished Good - SHIW'
# 				AND i.item_group = 'Finished Goods'
# 				AND sle.is_cancelled = 0
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)
# 		row_fs_stock.append(stock_qty)
# 	data.append(row_fs_stock)


# 	# Row 21: WIP Weight
# 	row_wip_weight = ["WIP Weight"]

# 	# Fix the WIP Weight query with IN clause:
#     wip_warehouses = ("Pouring - SHIW", "Shake Out - SHIW", "Short Blast - SHIW", "Long Blast - SHIW", "Jolt Squeeze - SHIW", "Green Sand Hand Mould - SHIW", "First Line Rejection - SHIW", "Fettling - SHIW", "Finishing - SHIW")

#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)

#         placeholders = ','.join(['%s'] * len(wip_warehouses))
#         query = f"""
#             SELECT SUM(sle.actual_qty)
#             FROM `tabStock Ledger Entry` sle
#             WHERE sle.posting_date <= %s
#             AND sle.warehouse IN ({placeholders})
#             AND sle.is_cancelled = 0
#         """
#         params = [date_str] + list(wip_warehouses)
#         wip_weight = frappe.db.sql(query, params, as_list=True)[0][0] or 0

#         row_wip_weight.append(wip_weight)



# 	data.append(row_wip_weight)

# 	# Row 22: Heat Loss Wt
# 	row_heat_loss = ["Heat Loss Wt"]

# 	for day in range(1, days_in_month + 1):
# 		date_str = get_date(day)

# 		loss_qty = (
# 			frappe.db.sql(
# 				"""
# 				SELECT SUM(loss_liquid_metal)
# 				FROM `tabDaily Heat Loss`
# 				WHERE date = %s
# 				""",
# 				(date_str,),
# 				as_list=True,
# 			)[0][0]
# 			or 0
# 		)

# 		row_heat_loss.append(loss_qty)

# 	data.append(row_heat_loss)



# 	return columns, data









# #actual code starts hear
# import frappe
# import calendar

# def flt(value, precision=2):
#     try:
#         return round(float(value or 0), precision)
#     except (ValueError, TypeError):
#         return 0.0


# def execute(filters=None):
#     if not filters:
#         return [], []

#     month = filters.get("month")
#     year = int(filters.get("year"))
#     month_index = list(calendar.month_name).index(month)
#     days_in_month = calendar.monthrange(year, month_index)[1]

#     # Column headers
#     columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

#     def get_date(day):
#         return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

#     data = []

#     # Row 1: Raw Materials Received
#     row_raw_materials = ["Raw Materials Received"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         accepted_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(pri.qty)
#                 FROM `tabPurchase Receipt` pr
#                 JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#                 JOIN `tabItem` i ON i.name = pri.item_code
#                 WHERE pr.posting_date = %s
#                 AND i.item_group = 'Raw Material'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_raw_materials.append(accepted_qty)
#     data.append(row_raw_materials)

#     # Row 2: Raw Materials Melted
#     row_rm_melted = ["Raw Materials Melted"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rm_melted.append(melted_qty)
#     data.append(row_rm_melted)

#     # Row 3: Raw Materials Stock
#     row_rm_stock = ["Raw Materials Stock"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Stores - SHIW'
#                 AND i.item_group = 'Raw Material'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rm_stock.append(stock_qty)
#     data.append(row_rm_stock)

#     # Row 4: Liquid Metal Generated
#     row_liquid_metal = ["Liquid Metal Generated"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         liquid_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_balence)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_liquid_metal.append(liquid_qty)
#     data.append(row_liquid_metal)

#     # Row 5: Liquid Metal Returned to Furnace
#     row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         returned_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(foundry_return_existing)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_returned_to_furnace.append(returned_qty)
#     data.append(row_returned_to_furnace)

#     # Row 6: Liquid Metal Pigged
#     row_liquid_metal_pig = ["Liquid Metal Pigged"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pig_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_metal_pig)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_liquid_metal_pig.append(pig_qty)
#     data.append(row_liquid_metal_pig)

#     # Row 7: Burning Loss %

#     # row_burning_loss = ["Burning Loss %"]
#     # for day in range(1, days_in_month + 1):
#     #     date_str = get_date(day)
#     #     loss_pct = (
#     #         frappe.db.sql(
#     #             """
#     #             SELECT AVG(burning_loss)
#     #             FROM `tabHeat`
#     #             WHERE `date` = %s AND docstatus = 1
#     #             """,
#     #             (date_str,),
#     #             as_list=True,
#     #         )[0][0]
#     #         or 0
#     #     )
#     #     row_burning_loss.append(round(loss_pct, 2))
#     # data.append(row_burning_loss)




#     # row_burning_loss = ["Burning Loss %"]
#     # for i in range(1, days_in_month + 1):
#     #     melted = row_rm_melted[i] or 0
#     #     liquid = row_liquid_metal[i] or 0

#     #     if melted > 0:
#     #         loss_pct = round(((melted - liquid) / melted) * 100, 2)
#     #     else:
#     #         loss_pct = 0

#     #     row_burning_loss.append(loss_pct)

#     # data.append(row_burning_loss)


#     row_melted_excl_3a = []
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty_filtered = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1 AND material_grade != '3A - 1 Ton Furnace'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_melted_excl_3a.append(melted_qty_filtered)







#     # Add Burning Loss % row
#     row_burning_loss = ["Burning Loss %"]

#     for i in range(days_in_month):
#         melted = flt(row_melted_excl_3a[i]) or 0
        
#         liquid = flt(row_liquid_metal[i]) or 0
#         print(f"Day {i}: Melted = {melted}, Liquid = {liquid}")

#         if melted > 0:
#             loss_pct = round(((melted - liquid) / melted) * 100, 2)
#         else:
#             loss_pct = 0

#         row_burning_loss.append(loss_pct)

#     data.append(row_burning_loss)
    


#     # Row 8: Co2 Mould Bunch Weight
#     row_bunch_weight = ["Co2 Mould Bunch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         bunch_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_bunch_weight.append(bunch_weight)
#     data.append(row_bunch_weight)

#     # Row 9: Co2 Mould Cast Weight
#     row_cast_weight = ["Co2 Mould Cast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         cast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_cast_weight.append(cast_weight)
#     data.append(row_cast_weight)

#     # Row 10: HPML Mould Cast Weight
#     row_hpml_cast_weight = ["HPML Mould Cast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_cast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_hpml_cast_weight.append(hpml_cast_weight)
#     data.append(row_hpml_cast_weight)

#     # Row 11: HPML Mould Bunch Weight
#     row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_bunch_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_hpml_bunch_weight.append(hpml_bunch_weight)
#     data.append(row_hpml_bunch_weight)

#     # Row 12: No-Bake Mould Bunch Weight
#     row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_bunch_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_nb_bunch_weight.append(nb_bunch_weight)
#     data.append(row_nb_bunch_weight)

#     # Row 13: No-Bake Mould Cast Weight
#     row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_cast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_nb_cast_weight.append(nb_cast_weight)
#     data.append(row_nb_cast_weight)

#     # Row 14: Jolt Squeeze Mould Bunch Weight
#     row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_bunch_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_js_bunch_weight.append(js_bunch_weight)
#     data.append(row_js_bunch_weight)

#     # Row 15: Jolt Squeeze Mould Cast Weight
#     row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_cast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_js_cast_weight.append(js_cast_weight)
#     data.append(row_js_cast_weight)

#     # Row 16: Green Sand Hand Mould Bunch Weight
#     row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_bunch_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_gs_bunch_weight.append(gs_bunch_weight)
#     data.append(row_gs_bunch_weight)

#     # Row 17: Green Sand Hand Mould Cast Weight
#     row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_cast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_gs_cast_weight.append(gs_cast_weight)
#     data.append(row_gs_cast_weight)

#     # Row 18: Fettling Weight
#     row_fettling_weight = ["Fettling Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         fettling_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_fettling_weight)
#                 FROM `tabFettling`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_fettling_weight.append(fettling_weight)
#     data.append(row_fettling_weight)

#     # Row 19: Finishing Weight
#     row_finishing_weight = ["Finishing Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         finishing_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_finishing_weight)
#                 FROM `tabFinishing`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_finishing_weight.append(finishing_weight)
#     data.append(row_finishing_weight)

#     # Row 20: Finished Stock Weight
#     row_fs_stock = ["Finished Stock Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'FInished Good - SHIW'
#                 AND i.item_group = 'Finished Goods'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_fs_stock.append(stock_qty)
#     data.append(row_fs_stock)
#     # Row 21: WIP Weight
#     row_wip_weight = ["WIP Weight"]
#     wip_warehouses = (
#         "Pouring - SHIW",
#         "Shake Out - SHIW",
#         "Short Blast - SHIW",
#         "Long Blast - SHIW",
#         "Jolt Squeeze - SHIW",
#         "Green Sand Hand Mould - SHIW",
#         "First Line Rejection - SHIW",
#         "Fettling - SHIW",
#         "Finishing - SHIW",
#     )
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         placeholders = ','.join(['%s'] * len(wip_warehouses))
#         query = f"""
#             SELECT SUM(sle.actual_qty)
#             FROM `tabStock Ledger Entry` sle
#             WHERE sle.posting_date <= %s
#             AND sle.warehouse IN ({placeholders})
#             AND sle.is_cancelled = 0
#         """
#         params = [date_str] + list(wip_warehouses)
#         wip_weight = frappe.db.sql(query, params, as_list=True)[0][0] or 0
#         row_wip_weight.append(wip_weight)
#     data.append(row_wip_weight)
#     # Row 22: Heat Loss Wt
#     row_heat_loss = ["Heat Loss Wt"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         loss_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(loss_liquid_metal)
#                 FROM `tabDaily Heat Loss`
#                 WHERE date = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_heat_loss.append(loss_qty)
#     data.append(row_heat_loss)
#     # Row 23: Pouring Weight
#     row_pouring_weight = ["Pouring Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
        
#         pouring_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_pouring_weight)
#                 FROM `tabPouring`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_pouring_weight.append(pouring_weight)
#     data.append(row_pouring_weight)

#     # Row 24: Shakeout Weight
#     row_shakeout_weight = ["Shakeout Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shakeout_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shakeout_cast_weight)
#                 FROM `tabShake Out`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_shakeout_weight.append(shakeout_weight)
#     data.append(row_shakeout_weight)
#     # Row 25: Shotblast Weight
#     row_shotblast_weight = ["Shotblast Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shotblast_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shot_blast_cast_weight)
#                 FROM `tabShot Blast`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_shotblast_weight.append(shotblast_weight)
#     data.append(row_shotblast_weight)
#     # Row 26: Rejection Weight
#     row_rejection_weight = ["Rejection Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         rejection_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_flr_cast_weight)
#                 FROM `tabFirst Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rejection_weight.append(rejection_weight)
#     data.append(row_rejection_weight)
#     # Row 27: Deviation WT
#     row_deviation_wt = ["Deviation WT"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         deviation_wt = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_deviation_weight)
#                 FROM `tabFirst Line Deviation`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_deviation_wt.append(deviation_wt)
#     data.append(row_deviation_wt)
#     # Row 28: Repair WT
#     row_repair_wt = ["Repair WT"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         repair_wt = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_repair_weight)
#                 FROM `tabRepair`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_repair_wt.append(repair_wt)
#     data.append(row_repair_wt)
#     # Row 29: Rejection Weight (Second Line)
#     row_second_rejection_weight = ["Rejection Weight (Second Line)"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         second_rejection_weight = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(rejected_wt)
#                 FROM `tabSecond Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_second_rejection_weight.append(second_rejection_weight)
#     data.append(row_second_rejection_weight)
#     # Row 30: Heat Treatment Weight
#     row_heat_treatment_wt = ["Heat Treatment Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         heat_treatment_wt = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_heat_treatment)
#                 FROM `tabHeat Treatment`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_heat_treatment_wt.append(heat_treatment_wt)
#     data.append(row_heat_treatment_wt)
#     # Row 22: Wastage and Spillage
#     row_wastage_spillage = ["Wastage and Spillage"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_wastage = 0
#         # Step 1: Fetch all Pouring docs on this date
#         pouring_docs = frappe.get_all(
#             "Pouring",
#             filters={"date": date_str},
#             fields=["name", "total_pouring_weight"]
#         )
#         for pouring in pouring_docs:
#             pouring_weight = pouring.total_pouring_weight or 0
#             unique_heat_nos = set()
#             # Step 2: Get unique heat_nos from child table
#             mould_batches = frappe.get_all(
#                 "Mould Batch",
#                 filters={"parent": pouring.name},
#                 fields=["heat_no"]
#             )
#             for mb in mould_batches:
#                 if mb.heat_no:
#                     unique_heat_nos.add(mb.heat_no)
#             # Step 3: For each unique heat, calculate b
#             total_b = 0
#             for heat_no in unique_heat_nos:
#                 heat_doc = frappe.get_value(
#                     "Heat",
#                     heat_no,
#                     ["liquid_balence", "foundry_return_existing", "liquid_metal_pig"],
#                     as_dict=True,
#                 )
#                 if heat_doc:
#                     liquid_balence = heat_doc.liquid_balence or 0
#                     return_existing = heat_doc.foundry_return_existing or 0
#                     pig = heat_doc.liquid_metal_pig or 0
#                     b = liquid_balence - (return_existing + pig)
#                     total_b += b
#             # Step 4: b - a (total_b - pouring_weight)
#             wastage = total_b - pouring_weight
#             total_wastage += wastage
#         row_wastage_spillage.append(total_wastage)
#     data.append(row_wastage_spillage)
#     # Row 23: Foundry Return Generated Weight
#     row_foundry_return = ["Foundry Return Generated Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_qty = 0
#         # Step 1: Get Stock Entries of type Pouring for that date
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Pouring",
#                 "custom_date": date_str
#             },
#             pluck="name"
#         )
#         # Step 2: Loop through Stock Entry Detail rows
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se,
#                     "t_warehouse": "Estimated Foundry Return  - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             for item in items:
#                 total_qty += item.qty or 0
#         row_foundry_return.append(total_qty)
#     data.append(row_foundry_return)
#     # Row 24: Pending Order WT
#     row_pending_order = ["Pending Order WT"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = frappe.db.get_value(
#     "Sales Order",
#     {"transaction_date": date_str},
#     "SUM(total_qty)"
#         )or 0
#         row_pending_order.append(total_weight)
#     data.append(row_pending_order)
#     # Row 24: Orders Received Weight
#     row_pend_order = ["Orders Received Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = frappe.db.get_value(
#         "Sales Order",
#         {"delivery_date": date_str},
#         "SUM(total_qty)"
#         )or 0
#         row_pend_order.append(total_weight)
#     data.append(row_pend_order)
#     # Row 25: Total Foundry Return Physical WT
#     row_foundry_return_physical = ["Total Foundry Return Physical WT"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         # Get Stock Entries of type 'Material Issue' on this date
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Material Issue",
#                 "posting_date": date_str
#             },
#             fields=["name"]
#         )
#         total_qty = 0
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se.name,
#                     "s_warehouse": "Estimated Foundry Return  - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_qty += sum(item.qty or 0 for item in items)
#         total_qty = round(total_qty, 2)
#         print(f"{date_str}: Foundry Return Physical Qty = {total_qty}")  # Debug
#         row_foundry_return_physical.append(total_qty)
#     data.append(row_foundry_return_physical)
#     # Row 25: Dispatch Weight
#     row_dispatch_weight = ["Dispatch Weight"]
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         # Get Delivery Notes for this date
#         delivery_notes = frappe.get_all(
#             "Delivery Note",
#             filters={"posting_date": date_str},
#             fields=["total_net_weight"]
#         )
#         total_dispatch_weight = sum(dn.total_net_weight or 0 for dn in delivery_notes)
#         total_dispatch_weight = round(total_dispatch_weight, 2)  
#         row_dispatch_weight.append(total_dispatch_weight)
#     data.append(row_dispatch_weight)
#     return columns, data








#should be changed like this
# import frappe
# import calendar
# from datetime import datetime

# def execute(filters=None):
#     if not filters:
#         return [], []

#     month = filters.get("month")
#     year = int(filters.get("year") or datetime.now().year)
#     month_index = list(calendar.month_name).index(month)
#     days_in_month = calendar.monthrange(year, month_index)[1]

#     # Parse selected_days (e.g., "1,2,7,9,25")
#     selected_days_raw = filters.get("selected_days") or ""
#     selected_days = set(
#         int(day.strip()) for day in selected_days_raw.split(",") if day.strip().isdigit()
#     )

#     # Column headers
#     columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)] + ["Total"]

#     def get_date(day):
#         return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

#     data = []

#     # Row: Raw Materials Received
#     row_raw_materials = ["Raw Materials Received"]
#     total_qty = 0

#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         accepted_qty = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(pri.qty)
#                 FROM `tabPurchase Receipt` pr
#                 JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#                 JOIN `tabItem` i ON i.name = pri.item_code
#                 WHERE pr.posting_date = %s
#                 AND i.item_group = 'Raw Material'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_raw_materials.append(accepted_qty)

#         # Sum only if this day is selected (or if no days selected, include all)
#         if not selected_days or day in selected_days:
#             total_qty += accepted_qty

#     row_raw_materials.append(total_qty)
#     data.append(row_raw_materials)

#     return columns, data






# import frappe
# import calendar
# from datetime import datetime

# def flt(value, precision=2):
#     try:
#         return round(float(value or 0), precision)
#     except (ValueError, TypeError):
#         return 0.0

# def execute(filters=None):
#     if not filters:
#         return [], []

#     month = filters.get("month")
#     year = int(filters.get("year") or datetime.now().year)
#     month_index = list(calendar.month_name).index(month)
#     days_in_month = calendar.monthrange(year, month_index)[1]

#     # Parse selected_days (e.g., "1,2,7,9,25")
#     selected_days_raw = filters.get("selected_days") or ""
#     selected_days = set(
#         int(day.strip()) for day in selected_days_raw.split(",") if day.strip().isdigit()
#     )

#     # Column headers
#     columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)] + ["Total"]

#     def get_date(day):
#         return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

#     data = []

#     # Row 1: Raw Materials Received
#     row_raw_materials = ["Raw Materials Received"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         accepted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(pri.qty)
#                 FROM `tabPurchase Receipt` pr
#                 JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#                 JOIN `tabItem` i ON i.name = pri.item_code
#                 WHERE pr.posting_date = %s
#                 AND i.item_group = 'Raw Material'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_raw_materials.append(accepted_qty)
#         if not selected_days or day in selected_days:
#             total_qty += accepted_qty
#     row_raw_materials.append(flt(total_qty))
#     data.append(row_raw_materials)

#     # Row 2: Raw Materials Melted
#     row_rm_melted = ["Raw Materials Melted"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rm_melted.append(melted_qty)
#         if not selected_days or day in selected_days:
#             total_qty += melted_qty
#     row_rm_melted.append(flt(total_qty))
#     data.append(row_rm_melted)

#     # Row 3: Raw Materials Stock
#     row_rm_stock = ["Raw Materials Stock"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Stores - SHIW'
#                 AND i.item_group = 'Raw Material'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rm_stock.append(stock_qty)
#         if not selected_days or day in selected_days:
#             total_qty += stock_qty
#     row_rm_stock.append(flt(total_qty))
#     data.append(row_rm_stock)

#     # Row 4: Liquid Metal Generated
#     row_liquid_metal = ["Liquid Metal Generated"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         liquid_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_balence)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_liquid_metal.append(liquid_qty)
#         if not selected_days or day in selected_days:
#             total_qty += liquid_qty
#     row_liquid_metal.append(flt(total_qty))
#     data.append(row_liquid_metal)

#     # Row 5: Liquid Metal Returned to Furnace
#     row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         returned_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(foundry_return_existing)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_returned_to_furnace.append(returned_qty)
#         if not selected_days or day in selected_days:
#             total_qty += returned_qty
#     row_returned_to_furnace.append(flt(total_qty))
#     data.append(row_returned_to_furnace)

#     # Row 6: Liquid Metal Pigged
#     row_liquid_metal_pig = ["Liquid Metal Pigged"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pig_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_metal_pig)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_liquid_metal_pig.append(pig_qty)
#         if not selected_days or day in selected_days:
#             total_qty += pig_qty
#     row_liquid_metal_pig.append(flt(total_qty))
#     data.append(row_liquid_metal_pig)

#     # Row 7: Burning Loss %
#     row_melted_excl_3a = []
#     total_melted_excl_3a = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty_filtered = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1 AND material_grade != '3A - 1 Ton Furnace'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_melted_excl_3a.append(melted_qty_filtered)
#         if not selected_days or day in selected_days:
#             total_melted_excl_3a += melted_qty_filtered
#     row_burning_loss = ["Burning Loss %"]
#     total_loss_pct = 0
#     valid_days = 0
#     for i in range(days_in_month):
#         melted = flt(row_melted_excl_3a[i])
#         liquid = flt(row_liquid_metal[i + 1])
#         loss_pct = flt(((melted - liquid) / melted) * 100 if melted > 0 else 0)
#         row_burning_loss.append(loss_pct)
#         if not selected_days or (i + 1) in selected_days:
#             total_loss_pct += loss_pct
#             valid_days += 1
#     total_loss_pct = flt(total_loss_pct / valid_days if valid_days > 0 else 0)
#     row_burning_loss.append(total_loss_pct)
#     data.append(row_burning_loss)

#     # Row 8: Co2 Mould Bunch Weight
#     row_bunch_weight = ["Co2 Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_bunch_weight.append(bunch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += bunch_weight
#     row_bunch_weight.append(flt(total_qty))
#     data.append(row_bunch_weight)

#     # Row 9: Co2 Mould Cast Weight
#     row_cast_weight = ["Co2 Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_cast_weight.append(cast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += cast_weight
#     row_cast_weight.append(flt(total_qty))
#     data.append(row_cast_weight)

#     # Row 10: HPML Mould Cast Weight
#     row_hpml_cast_weight = ["HPML Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_hpml_cast_weight.append(hpml_cast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += hpml_cast_weight
#     row_hpml_cast_weight.append(flt(total_qty))
#     data.append(row_hpml_cast_weight)

#     # Row 11: HPML Mould Bunch Weight
#     row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_hpml_bunch_weight.append(hpml_bunch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += hpml_bunch_weight
#     row_hpml_bunch_weight.append(flt(total_qty))
#     data.append(row_hpml_bunch_weight)

#     # Row 12: No-Bake Mould Bunch Weight
#     row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_nb_bunch_weight.append(nb_bunch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += nb_bunch_weight
#     row_nb_bunch_weight.append(flt(total_qty))
#     data.append(row_nb_bunch_weight)

#     # Row 13: No-Bake Mould Cast Weight
#     row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_nb_cast_weight.append(nb_cast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += nb_cast_weight
#     row_nb_cast_weight.append(flt(total_qty))
#     data.append(row_nb_cast_weight)

#     # Row 14: Jolt Squeeze Mould Bunch Weight
#     row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_js_bunch_weight.append(js_bunch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += js_bunch_weight
#     row_js_bunch_weight.append(flt(total_qty))
#     data.append(row_js_bunch_weight)

#     # Row 15: Jolt Squeeze Mould Cast Weight
#     row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_js_cast_weight.append(js_cast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += js_cast_weight
#     row_js_cast_weight.append(flt(total_qty))
#     data.append(row_js_cast_weight)

#     # Row 16: Green Sand Hand Mould Bunch Weight
#     row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_gs_bunch_weight.append(gs_bunch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += gs_bunch_weight
#     row_gs_bunch_weight.append(flt(total_qty))
#     data.append(row_gs_bunch_weight)

#     # Row 17: Green Sand Hand Mould Cast Weight
#     row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_gs_cast_weight.append(gs_cast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += gs_cast_weight
#     row_gs_cast_weight.append(flt(total_qty))
#     data.append(row_gs_cast_weight)

#     # Row 18: Fettling Weight
#     row_fettling_weight = ["Fettling Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         fettling_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_fettling_weight)
#                 FROM `tabFettling`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_fettling_weight.append(fettling_weight)
#         if not selected_days or day in selected_days:
#             total_qty += fettling_weight
#     row_fettling_weight.append(flt(total_qty))
#     data.append(row_fettling_weight)

#     # Row 19: Finishing Weight
#     row_finishing_weight = ["Finishing Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         finishing_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_finishing_weight)
#                 FROM `tabFinishing`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_finishing_weight.append(finishing_weight)
#         if not selected_days or day in selected_days:
#             total_qty += finishing_weight
#     row_finishing_weight.append(flt(total_qty))
#     data.append(row_finishing_weight)

#     # Row 20: Finished Stock Weight
#     row_fs_stock = ["Finished Stock Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Finished Goods - SHIW'
#                 AND i.item_group = 'Finished Goods'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_fs_stock.append(stock_qty)
#         if not selected_days or day in selected_days:
#             total_qty += stock_qty
#     row_fs_stock.append(flt(total_qty))
#     data.append(row_fs_stock)

#     # Row 21: WIP Weight
#     row_wip_weight = ["WIP Weight"]
#     total_qty = 0
#     wip_warehouses = (
#         "Pouring - SHIW",
#         "Shake Out - SHIW",
#         "Short Blast - SHIW",
#         "Long Blast - SHIW",
#         "Jolt Squeeze - SHIW",
#         "Green Sand Hand Mould - SHIW",
#         "First Line Rejection - SHIW",
#         "Fettling - SHIW",
#         "Finishing - SHIW",
#     )
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         placeholders = ','.join(['%s'] * len(wip_warehouses))
#         query = f"""
#             SELECT SUM(sle.actual_qty)
#             FROM `tabStock Ledger Entry` sle
#             WHERE sle.posting_date <= %s
#             AND sle.warehouse IN ({placeholders})
#             AND sle.is_cancelled = 0
#         """
#         params = [date_str] + list(wip_warehouses)
#         wip_weight = flt(frappe.db.sql(query, params, as_list=True)[0][0] or 0)
#         row_wip_weight.append(wip_weight)
#         if not selected_days or day in selected_days:
#             total_qty += wip_weight
#     row_wip_weight.append(flt(total_qty))
#     data.append(row_wip_weight)

#     # Row 22: Heat Loss Wt
#     row_heat_loss = ["Heat Loss Wt"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         loss_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(loss_liquid_metal)
#                 FROM `tabDaily Heat Loss`
#                 WHERE date = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_heat_loss.append(loss_qty)
#         if not selected_days or day in selected_days:
#             total_qty += loss_qty
#     row_heat_loss.append(flt(total_qty))
#     data.append(row_heat_loss)

#     # Row 23: Pouring Weight
#     row_pouring_weight = ["Pouring Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pouring_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_pouring_weight)
#                 FROM `tabPouring`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_pouring_weight.append(pouring_weight)
#         if not selected_days or day in selected_days:
#             total_qty += pouring_weight
#     row_pouring_weight.append(flt(total_qty))
#     data.append(row_pouring_weight)

#     # Row 24: Shakeout Weight
#     row_shakeout_weight = ["Shakeout Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shakeout_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shakeout_cast_weight)
#                 FROM `tabShake Out`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_shakeout_weight.append(shakeout_weight)
#         if not selected_days or day in selected_days:
#             total_qty += shakeout_weight
#     row_shakeout_weight.append(flt(total_qty))
#     data.append(row_shakeout_weight)

#     # Row 25: Shotblast Weight
#     row_shotblast_weight = ["Shotblast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shotblast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shot_blast_cast_weight)
#                 FROM `tabShot Blast`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_shotblast_weight.append(shotblast_weight)
#         if not selected_days or day in selected_days:
#             total_qty += shotblast_weight
#     row_shotblast_weight.append(flt(total_qty))
#     data.append(row_shotblast_weight)

#     # Row 26: Rejection Weight
#     row_rejection_weight = ["Rejection Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_flr_cast_weight)
#                 FROM `tabFirst Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_rejection_weight.append(rejection_weight)
#         if not selected_days or day in selected_days:
#             total_qty += rejection_weight
#     row_rejection_weight.append(flt(total_qty))
#     data.append(row_rejection_weight)

#     # Row 27: Deviation WT
#     row_deviation_wt = ["Deviation WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         deviation_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_deviation_weight)
#                 FROM `tabFirst Line Deviation`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_deviation_wt.append(deviation_wt)
#         if not selected_days or day in selected_days:
#             total_qty += deviation_wt
#     row_deviation_wt.append(flt(total_qty))
#     data.append(row_deviation_wt)

#     # Row 28: Repair WT
#     row_repair_wt = ["Repair WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         repair_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_repair_weight)
#                 FROM `tabRepair`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_repair_wt.append(repair_wt)
#         if not selected_days or day in selected_days:
#             total_qty += repair_wt
#     row_repair_wt.append(flt(total_qty))
#     data.append(row_repair_wt)

#     # Row 29: Rejection Weight (Second Line)
#     row_second_rejection_weight = ["Rejection Weight (Second Line)"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         second_rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(rejected_wt)
#                 FROM `tabSecond Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_second_rejection_weight.append(second_rejection_weight)
#         if not selected_days or day in selected_days:
#             total_qty += second_rejection_weight
#     row_second_rejection_weight.append(flt(total_qty))
#     data.append(row_second_rejection_weight)

#     # Row 30: Heat Treatment Weight
#     row_heat_treatment_wt = ["Heat Treatment Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         heat_treatment_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_heat_treatment)
#                 FROM `tabHeat Treatment`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0]
#             or 0
#         )
#         row_heat_treatment_wt.append(heat_treatment_wt)
#         if not selected_days or day in selected_days:
#             total_qty += heat_treatment_wt
#     row_heat_treatment_wt.append(flt(total_qty))
#     data.append(row_heat_treatment_wt)

#     # Row 31: Wastage and Spillage
#     row_wastage_spillage = ["Wastage and Spillage"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_wastage = 0
#         pouring_docs = frappe.get_all(
#             "Pouring",
#             filters={"date": date_str},
#             fields=["name", "total_pouring_weight"]
#         )
#         for pouring in pouring_docs:
#             pouring_weight = flt(pouring.total_pouring_weight or 0)
#             unique_heat_nos = set()
#             mould_batches = frappe.get_all(
#                 "Mould Batch",
#                 filters={"parent": pouring.name},
#                 fields=["heat_no"]
#             )
#             for mb in mould_batches:
#                 if mb.heat_no:
#                     unique_heat_nos.add(mb.heat_no)
#             total_b = 0
#             for heat_no in unique_heat_nos:
#                 heat_doc = frappe.get_value(
#                     "Heat",
#                     heat_no,
#                     ["liquid_balence", "foundry_return_existing", "liquid_metal_pig"],
#                     as_dict=True,
#                 )
#                 if heat_doc:
#                     liquid_balence = flt(heat_doc.liquid_balence or 0)
#                     return_existing = flt(heat_doc.foundry_return_existing or 0)
#                     pig = flt(heat_doc.liquid_metal_pig or 0)
#                     b = liquid_balence - (return_existing + pig)
#                     total_b += b
#             wastage = flt(total_b - pouring_weight)
#             total_wastage += wastage
#         row_wastage_spillage.append(flt(total_wastage))
#         if not selected_days or day in selected_days:
#             total_qty += total_wastage
#     row_wastage_spillage.append(flt(total_qty))
#     data.append(row_wastage_spillage)

#     # Row 32: Foundry Return Generated Weight
#     row_foundry_return = ["Foundry Return Generated Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_se_qty = 0
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Pouring",
#                 "custom_date": date_str
#             },
#             pluck="name"
#         )
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se,
#                     "t_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return.append(total_se_qty)
#         if not selected_days or day in selected_days:
#             total_qty += total_se_qty
#     row_foundry_return.append(flt(total_qty))
#     data.append(row_foundry_return)

#     # Row 33: Pending Order WT
#     row_pending_order = ["Pending Order WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"transaction_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_pending_order.append(total_weight)
#         if not selected_days or day in selected_days:
#             total_qty += total_weight
#     row_pending_order.append(flt(total_qty))
#     data.append(row_pending_order)

#     # Row 34: Orders Received Weight
#     row_orders_received = ["Orders Received Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"delivery_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_orders_received.append(total_weight)
#         if not selected_days or day in selected_days:
#             total_qty += total_weight
#     row_orders_received.append(flt(total_qty))
#     data.append(row_orders_received)

#     # Row 35: Total Foundry Return Physical WT
#     row_foundry_return_physical = ["Total Foundry Return Physical WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Material Issue",
#                 "posting_date": date_str
#             },
#             fields=["name"]
#         )
#         total_se_qty = 0
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se.name,
#                     "s_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return_physical.append(total_se_qty)
#         if not selected_days or day in selected_days:
#             total_qty += total_se_qty
#     row_foundry_return_physical.append(flt(total_qty))
#     data.append(row_foundry_return_physical)

#     # Row 36: Dispatch Weight
#     row_dispatch_weight = ["Dispatch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         delivery_notes = frappe.get_all(
#             "Delivery Note",
#             filters={"posting_date": date_str},
#             fields=["custom_total_weight_rate__"]
#         )
#         total_dispatch_weight = flt(sum(dn.custom_total_weight_rate__ or 0 for dn in delivery_notes))
#         row_dispatch_weight.append(total_dispatch_weight)
#         if not selected_days or day in selected_days:
#             total_qty += total_dispatch_weight
#     row_dispatch_weight.append(flt(total_qty))
#     data.append(row_dispatch_weight)

#     return columns, data



#original code
# import frappe
# import calendar
# from datetime import datetime

# def flt(value, precision=2):
#     try:
#         return round(float(value or 0), precision)
#     except (ValueError, TypeError):
#         return 0.0

# def execute(filters=None):
#     if not filters:
#         return [], []

#     month = filters.get("month")
#     year = int(filters.get("year") or datetime.now().year)
#     month_index = list(calendar.month_name).index(month)
#     days_in_month = calendar.monthrange(year, month_index)[1]

#     # Parse start_day and end_day
#     start_day = int(filters.get("start_day") or 1)
#     end_day = int(filters.get("end_day") or days_in_month)
#     # Validate start_day and end_day
#     start_day = max(1, min(start_day, days_in_month))
#     end_day = max(start_day, min(end_day, days_in_month))
#     use_range = start_day and end_day and start_day <= end_day

#     # Parse selected_days (e.g., "1,2,7,9,25")
#     selected_days_raw = filters.get("selected_days") or ""
#     selected_days = set(
#         int(day.strip()) for day in selected_days_raw.split(",") if day.strip().isdigit() and 1 <= int(day.strip()) <= days_in_month
#     )

#     # Column headers
#     columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)] + ["Total"]

#     def get_date(day):
#         return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

#     data = []

#     # Row 1: Raw Materials Received
#     row_raw_materials = ["Raw Materials Received"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         accepted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(pri.qty)
#                 FROM `tabPurchase Receipt` pr
#                 JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#                 JOIN `tabItem` i ON i.name = pri.item_code
#                 WHERE pr.posting_date = %s
#                 AND i.item_group = 'Raw Material'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_raw_materials.append(accepted_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += accepted_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += accepted_qty
#         else:
#             total_qty += accepted_qty
#     row_raw_materials.append(flt(total_qty))
#     data.append(row_raw_materials)

#     # Row 2: Raw Materials Melted
#     row_rm_melted = ["Raw Materials Melted"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rm_melted.append(melted_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += melted_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += melted_qty
#         else:
#             total_qty += melted_qty
#     row_rm_melted.append(flt(total_qty))
#     data.append(row_rm_melted)

#     # Row 3: Raw Materials Stock
#     row_rm_stock = ["Raw Materials Stock"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Stores - SHIW'
#                 AND i.item_group = 'Raw Material'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rm_stock.append(stock_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += stock_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += stock_qty
#         else:
#             total_qty += stock_qty
#     row_rm_stock.append(flt(total_qty))
#     data.append(row_rm_stock)

#     # Row 4: Liquid Metal Generated
#     row_liquid_metal = ["Liquid Metal Generated"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         liquid_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_balence)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_liquid_metal.append(liquid_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += liquid_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += liquid_qty
#         else:
#             total_qty += liquid_qty
#     row_liquid_metal.append(flt(total_qty))
#     data.append(row_liquid_metal)

#     # Row 5: Liquid Metal Returned to Furnace
#     row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         returned_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(foundry_return_existing)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_returned_to_furnace.append(returned_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += returned_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += returned_qty
#         else:
#             total_qty += returned_qty
#     row_returned_to_furnace.append(flt(total_qty))
#     data.append(row_returned_to_furnace)

#     # Row 6: Liquid Metal Pigged
#     row_liquid_metal_pig = ["Liquid Metal Pigged"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pig_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_metal_pig)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_liquid_metal_pig.append(pig_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += pig_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += pig_qty
#         else:
#             total_qty += pig_qty
#     row_liquid_metal_pig.append(flt(total_qty))
#     data.append(row_liquid_metal_pig)

#     # Row 7: Burning Loss %
#     row_melted_excl_3a = []
#     total_melted_excl_3a = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty_filtered = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1 AND material_grade != '3A - 1 Ton Furnace'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_melted_excl_3a.append(melted_qty_filtered)
#         if use_range and start_day <= day <= end_day:
#             total_melted_excl_3a += melted_qty_filtered
#         elif selected_days and day in selected_days:
#             total_melted_excl_3a += melted_qty_filtered
#         else:
#             total_melted_excl_3a += melted_qty_filtered
#     row_burning_loss = ["Burning Loss %"]
#     total_loss_pct = 0
#     valid_days = 0
#     for i in range(days_in_month):
#         melted = flt(row_melted_excl_3a[i])
#         liquid = flt(row_liquid_metal[i + 1])
#         loss_pct = flt(((melted - liquid) / melted) * 100 if melted > 0 else 0)
#         row_burning_loss.append(loss_pct)
#         if use_range:
#             if start_day <= (i + 1) <= end_day:
#                 total_loss_pct += loss_pct
#                 valid_days += 1
#         elif selected_days:
#             if (i + 1) in selected_days:
#                 total_loss_pct += loss_pct
#                 valid_days += 1
#         else:
#             total_loss_pct += loss_pct
#             valid_days += 1
#     total_loss_pct = flt(total_loss_pct / valid_days if valid_days > 0 else 0)
#     row_burning_loss.append(total_loss_pct)
#     data.append(row_burning_loss)

#     # Row 8: Co2 Mould Bunch Weight
#     row_bunch_weight = ["Co2 Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_bunch_weight.append(bunch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += bunch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += bunch_weight
#         else:
#             total_qty += bunch_weight
#     row_bunch_weight.append(flt(total_qty))
#     data.append(row_bunch_weight)

#     # Row 9: Co2 Mould Cast Weight
#     row_cast_weight = ["Co2 Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_cast_weight.append(cast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += cast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += cast_weight
#         else:
#             total_qty += cast_weight
#     row_cast_weight.append(flt(total_qty))
#     data.append(row_cast_weight)

#     # Row 10: HPML Mould Cast Weight
#     row_hpml_cast_weight = ["HPML Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_hpml_cast_weight.append(hpml_cast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += hpml_cast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += hpml_cast_weight
#         else:
#             total_qty += hpml_cast_weight
#     row_hpml_cast_weight.append(flt(total_qty))
#     data.append(row_hpml_cast_weight)

#     # Row 11: HPML Mould Bunch Weight
#     row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_hpml_bunch_weight.append(hpml_bunch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += hpml_bunch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += hpml_bunch_weight
#         else:
#             total_qty += hpml_bunch_weight
#     row_hpml_bunch_weight.append(flt(total_qty))
#     data.append(row_hpml_bunch_weight)

#     # Row 12: No-Bake Mould Bunch Weight
#     row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_nb_bunch_weight.append(nb_bunch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += nb_bunch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += nb_bunch_weight
#         else:
#             total_qty += nb_bunch_weight
#     row_nb_bunch_weight.append(flt(total_qty))
#     data.append(row_nb_bunch_weight)

#     # Row 13: No-Bake Mould Cast Weight
#     row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_nb_cast_weight.append(nb_cast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += nb_cast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += nb_cast_weight
#         else:
#             total_qty += nb_cast_weight
#     row_nb_cast_weight.append(flt(total_qty))
#     data.append(row_nb_cast_weight)

#     # Row 14: Jolt Squeeze Mould Bunch Weight
#     row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_js_bunch_weight.append(js_bunch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += js_bunch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += js_bunch_weight
#         else:
#             total_qty += js_bunch_weight
#     row_js_bunch_weight.append(flt(total_qty))
#     data.append(row_js_bunch_weight)

#     # Row 15: Jolt Squeeze Mould Cast Weight
#     row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_js_cast_weight.append(js_cast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += js_cast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += js_cast_weight
#         else:
#             total_qty += js_cast_weight
#     row_js_cast_weight.append(flt(total_qty))
#     data.append(row_js_cast_weight)

#     # Row 16: Green Sand Hand Mould Bunch Weight
#     row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_gs_bunch_weight.append(gs_bunch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += gs_bunch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += gs_bunch_weight
#         else:
#             total_qty += gs_bunch_weight
#     row_gs_bunch_weight.append(flt(total_qty))
#     data.append(row_gs_bunch_weight)

#     # Row 17: Green Sand Hand Mould Cast Weight
#     row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_gs_cast_weight.append(gs_cast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += gs_cast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += gs_cast_weight
#         else:
#             total_qty += gs_cast_weight
#     row_gs_cast_weight.append(flt(total_qty))
#     data.append(row_gs_cast_weight)

#     # Row 18: Fettling Weight
#     row_fettling_weight = ["Fettling Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         fettling_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_fettling_weight)
#                 FROM `tabFettling`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_fettling_weight.append(fettling_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += fettling_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += fettling_weight
#         else:
#             total_qty += fettling_weight
#     row_fettling_weight.append(flt(total_qty))
#     data.append(row_fettling_weight)

#     # Row 19: Finishing Weight
#     row_finishing_weight = ["Finishing Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         finishing_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_finishing_weight)
#                 FROM `tabFinishing`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_finishing_weight.append(finishing_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += finishing_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += finishing_weight
#         else:
#             total_qty += finishing_weight
#     row_finishing_weight.append(flt(total_qty))
#     data.append(row_finishing_weight)

#     # Row 20: Finished Stock Weight
#     row_fs_stock = ["Finished Stock Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Finished Goods - SHIW'
#                 AND i.item_group = 'Finished Goods'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_fs_stock.append(stock_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += stock_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += stock_qty
#         else:
#             total_qty += stock_qty
#     row_fs_stock.append(flt(total_qty))
#     data.append(row_fs_stock)

#     # Row 21: WIP Weight
#     row_wip_weight = ["WIP Weight"]
#     total_qty = 0
#     wip_warehouses = (
#         "Pouring - SHIW",
#         "Shake Out - SHIW",
#         "Short Blast - SHIW",
#         "Long Blast - SHIW",
#         "Jolt Squeeze - SHIW",
#         "Green Sand Hand Mould - SHIW",
#         "First Line Rejection - SHIW",
#         "Fettling - SHIW",
#         "Finishing - SHIW",
#     )
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         placeholders = ','.join(['%s'] * len(wip_warehouses))
#         query = f"""
#             SELECT SUM(sle.actual_qty)
#             FROM `tabStock Ledger Entry` sle
#             WHERE sle.posting_date <= %s
#             AND sle.warehouse IN ({placeholders})
#             AND sle.is_cancelled = 0
#         """
#         params = [date_str] + list(wip_warehouses)
#         wip_weight = flt(frappe.db.sql(query, params, as_list=True)[0][0] or 0)
#         row_wip_weight.append(wip_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += wip_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += wip_weight
#         else:
#             total_qty += wip_weight
#     row_wip_weight.append(flt(total_qty))
#     data.append(row_wip_weight)

#     # Row 22: Heat Loss Wt
#     row_heat_loss = ["Heat Loss Wt"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         loss_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(loss_liquid_metal)
#                 FROM `tabDaily Heat Loss`
#                 WHERE date = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_heat_loss.append(loss_qty)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += loss_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += loss_qty
#         else:
#             total_qty += loss_qty
#     row_heat_loss.append(flt(total_qty))
#     data.append(row_heat_loss)

#     # Row 23: Pouring Weight
#     row_pouring_weight = ["Pouring Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pouring_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_pouring_weight)
#                 FROM `tabPouring`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_pouring_weight.append(pouring_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += pouring_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += pouring_weight
#         else:
#             total_qty += pouring_weight
#     row_pouring_weight.append(flt(total_qty))
#     data.append(row_pouring_weight)

#     # Row 24: Shakeout Weight
#     row_shakeout_weight = ["Shakeout Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shakeout_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shakeout_cast_weight)
#                 FROM `tabShake Out`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_shakeout_weight.append(shakeout_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += shakeout_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += shakeout_weight
#         else:
#             total_qty += shakeout_weight
#     row_shakeout_weight.append(flt(total_qty))
#     data.append(row_shakeout_weight)

#     # Row 25: Shotblast Weight
#     row_shotblast_weight = ["Shotblast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shotblast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shot_blast_cast_weight)
#                 FROM `tabShot Blast`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_shotblast_weight.append(shotblast_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += shotblast_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += shotblast_weight
#         else:
#             total_qty += shotblast_weight
#     row_shotblast_weight.append(flt(total_qty))
#     data.append(row_shotblast_weight)

#     # Row 26: Rejection Weight
#     row_rejection_weight = ["Rejection Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_flr_cast_weight)
#                 FROM `tabFirst Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rejection_weight.append(rejection_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += rejection_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += rejection_weight
#         else:
#             total_qty += rejection_weight
#     row_rejection_weight.append(flt(total_qty))
#     data.append(row_rejection_weight)

#     # Row 27: Deviation WT
#     row_deviation_wt = ["Deviation WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         deviation_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_deviation_weight)
#                 FROM `tabFirst Line Deviation`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_deviation_wt.append(deviation_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += deviation_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += deviation_wt
#         else:
#             total_qty += deviation_wt
#     row_deviation_wt.append(flt(total_qty))
#     data.append(row_deviation_wt)

#     # Row 28: Repair WT
#     row_repair_wt = ["Repair WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         repair_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_repair_weight)
#                 FROM `tabRepair`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_repair_wt.append(repair_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += repair_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += repair_wt
#         else:
#             total_qty += repair_wt
#     row_repair_wt.append(flt(total_qty))
#     data.append(row_repair_wt)

#     # Row 29: Rejection Weight (Second Line)
#     row_second_rejection_weight = ["Rejection Weight (Second Line)"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         second_rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(rejected_wt)
#                 FROM `tabSecond Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_second_rejection_weight.append(second_rejection_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += second_rejection_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += second_rejection_weight
#         else:
#             total_qty += second_rejection_weight
#     row_second_rejection_weight.append(flt(total_qty))
#     data.append(row_second_rejection_weight)

#     # Row 30: Heat Treatment Weight
#     row_heat_treatment_wt = ["Heat Treatment Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         heat_treatment_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_heat_treatment)
#                 FROM `tabHeat Treatment`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_heat_treatment_wt.append(heat_treatment_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += heat_treatment_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += heat_treatment_wt
#         else:
#             total_qty += heat_treatment_wt
#     row_heat_treatment_wt.append(flt(total_qty))
#     data.append(row_heat_treatment_wt)

#     # Row 31: Wastage and Spillage
#     row_wastage_spillage = ["Wastage and Spillage"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_wastage = 0
#         pouring_docs = frappe.get_all(
#             "Pouring",
#             filters={"date": date_str},
#             fields=["name", "total_pouring_weight"]
#         )
#         for pouring in pouring_docs:
#             pouring_weight = flt(pouring.total_pouring_weight or 0)
#             unique_heat_nos = set()
#             mould_batches = frappe.get_all(
#                 "Mould Batch",
#                 filters={"parent": pouring.name},
#                 fields=["heat_no"]
#             )
#             for mb in mould_batches:
#                 if mb.heat_no:
#                     unique_heat_nos.add(mb.heat_no)
#             total_b = 0
#             for heat_no in unique_heat_nos:
#                 heat_doc = frappe.get_value(
#                     "Heat",
#                     heat_no,
#                     ["liquid_balence", "foundry_return_existing", "liquid_metal_pig"],
#                     as_dict=True,
#                 )
#                 if heat_doc:
#                     liquid_balence = flt(heat_doc.liquid_balence or 0)
#                     return_existing = flt(heat_doc.foundry_return_existing or 0)
#                     pig = flt(heat_doc.liquid_metal_pig or 0)
#                     b = flt(liquid_balence - (return_existing + pig))
#                     total_b += b
#             wastage = flt(total_b - pouring_weight)
#             total_wastage += wastage
#         row_wastage_spillage.append(flt(total_wastage))
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_wastage
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_wastage
#         else:
#             total_qty += total_wastage
#     row_wastage_spillage.append(flt(total_qty))
#     data.append(row_wastage_spillage)

#     # Row 32: Foundry Return Generated Weight
#     row_foundry_return = ["Foundry Return Generated Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_se_qty = 0
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Pouring",
#                 "custom_date": date_str
#             },
#             pluck="name"
#         )
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se,
#                     "t_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return.append(flt(total_se_qty))
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_se_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_se_qty
#         else:
#             total_qty += total_se_qty
#     row_foundry_return.append(flt(total_qty))
#     data.append(row_foundry_return)

#     # Row 33: Pending Order WT
#     row_pending_order = ["Pending Order WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"transaction_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_pending_order.append(total_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_weight
#         else:
#             total_qty += total_weight
#     row_pending_order.append(flt(total_qty))
#     data.append(row_pending_order)

#     # Row 34: Orders Received Weight
#     row_orders_received = ["Orders Received Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"delivery_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_orders_received.append(total_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_weight
#         else:
#             total_qty += total_weight
#     row_orders_received.append(flt(total_qty))
#     data.append(row_orders_received)

#     # Row 35: Total Foundry Return Physical WT
#     row_foundry_return_physical = ["Total Foundry Return Physical WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Material Issue",
#                 "posting_date": date_str
#             },
#             fields=["name"]
#         )
#         total_se_qty = 0
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se.name,
#                     "s_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return_physical.append(flt(total_se_qty))
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_se_qty
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_se_qty
#         else:
#             total_qty += total_se_qty
#     row_foundry_return_physical.append(flt(total_qty))
#     data.append(row_foundry_return_physical)

#     # Row 36: Dispatch Weight
#     row_dispatch_weight = ["Dispatch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         delivery_notes = frappe.get_all(
#             "Delivery Note",
#             filters={"posting_date": date_str},
#             fields=["custom_total_weight_rate__"]
#         )
#         total_dispatch_weight = flt(sum(dn.custom_total_weight_rate__ or 0 for dn in delivery_notes))
#         row_dispatch_weight.append(total_dispatch_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += total_dispatch_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += total_dispatch_weight
#         else:
#             total_qty += total_dispatch_weight
#     row_dispatch_weight.append(flt(total_qty))
#     data.append(row_dispatch_weight)

#     return columns, data











































#currect code 
# import frappe
# import calendar
# from datetime import datetime

# def flt(value, precision=2):
#     try:
#         return round(float(value or 0), precision)
#     except (ValueError, TypeError):
#         return 0.0

# def execute(filters=None):
#     if not filters:
#         filters = {}

#     month = filters.get("month")
#     year = int(filters.get("year") or datetime.now().year)
#     month_index = list(calendar.month_name).index(month)
#     days_in_month = calendar.monthrange(year, month_index)[1]

#     # Parse start_day and end_day
#     start_day = int(filters.get("start_day") or 1)
#     end_day = int(filters.get("end_day") or days_in_month)
#     # Validate start_day and end_day
#     start_day = max(1, min(start_day, days_in_month))
#     end_day = max(start_day, min(end_day, days_in_month))

#     # Parse selected_days (e.g., "1,2,7,9,25")
#     selected_days_raw = filters.get("selected_days") or ""
#     selected_days = set(
#         int(day.strip()) for day in selected_days_raw.split(",") if day.strip().isdigit() and 1 <= int(day.strip()) <= days_in_month
#     )

#     # Column headers
#     columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)] + ["Total"]

#     def get_date(day):
#         return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

#     data = []

#     # Row 1: Raw Materials Received
#     row_raw_materials = ["Raw Materials Received"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         accepted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(pri.qty)
#                 FROM `tabPurchase Receipt` pr
#                 JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
#                 JOIN `tabItem` i ON i.name = pri.item_code
#                 WHERE pr.posting_date = %s
#                 AND i.item_group = 'Raw Material'
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_raw_materials.append(accepted_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += accepted_qty
#         elif start_day <= day <= end_day:
#             total_qty += accepted_qty
#     row_raw_materials.append(flt(total_qty))
#     data.append(row_raw_materials)

#     # Row 2: Raw Materials Melted
#     row_rm_melted = ["Raw Materials Melted"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rm_melted.append(melted_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += melted_qty
#         elif start_day <= day <= end_day:
#             total_qty += melted_qty
#     row_rm_melted.append(flt(total_qty))
#     data.append(row_rm_melted)

#     # Row 3: Raw Materials Stock
#     row_rm_stock = ["Raw Materials Stock"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Stores - SHIW'
#                 AND i.item_group = 'Raw Material'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rm_stock.append(stock_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += stock_qty
#         elif start_day <= day <= end_day:
#             total_qty += stock_qty
#     row_rm_stock.append(flt(total_qty))
#     data.append(row_rm_stock)

#     # Row 4: Liquid Metal Generated
#     row_liquid_metal = ["Liquid Metal Generated"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         liquid_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_balence)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_liquid_metal.append(liquid_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += liquid_qty
#         elif start_day <= day <= end_day:
#             total_qty += liquid_qty
#     row_liquid_metal.append(flt(total_qty))
#     data.append(row_liquid_metal)

#     # Row 5: Liquid Metal Returned to Furnace
#     row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         returned_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(foundry_return_existing)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_returned_to_furnace.append(returned_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += returned_qty
#         elif start_day <= day <= end_day:
#             total_qty += returned_qty
#     row_returned_to_furnace.append(flt(total_qty))
#     data.append(row_returned_to_furnace)

#     # Row 6: Liquid Metal Pigged
#     row_liquid_metal_pig = ["Liquid Metal Pigged"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pig_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(liquid_metal_pig)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_liquid_metal_pig.append(pig_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += pig_qty
#         elif start_day <= day <= end_day:
#             total_qty += pig_qty
#     row_liquid_metal_pig.append(flt(total_qty))
#     data.append(row_liquid_metal_pig)

#     # Row 7: Burning Loss %
#     row_melted_excl_3a = []
#     total_melted_excl_3a = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         melted_qty_filtered = flt(
#             frappe.db.sql(
#                 """
#                  SELECT SUM(total_charge_mix_in_kg)
#                 FROM `tabHeat`
#                 WHERE `date` = %s AND docstatus = 1
#                 AND furnace_no NOT IN ('1A - 200 Kg Furnace', '1B - 200 Kg Furnace')
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_melted_excl_3a.append(melted_qty_filtered)
#         if selected_days and day in selected_days:
#             total_melted_excl_3a += melted_qty_filtered
#         elif not selected_days and start_day <= day <= end_day:
#             total_melted_excl_3a += melted_qty_filtered
#     row_burning_loss = ["Burning Loss %"]
#     total_loss_pct = 0
#     valid_days = 0
#     for i in range(days_in_month):
#         melted = flt(row_melted_excl_3a[i])
#         liquid = flt(row_liquid_metal[i + 1])
#         loss_pct = flt(((melted - liquid) / melted) * 100 if melted > 0 else 0)
#         row_burning_loss.append(loss_pct)
#         if selected_days:
#             if (i + 1) in selected_days:
#                 total_loss_pct += loss_pct
#                 valid_days += 1
#         elif start_day <= (i + 1) <= end_day:
#             total_loss_pct += loss_pct
#             valid_days += 1
#     total_loss_pct = flt(total_loss_pct / valid_days if valid_days > 0 else 0)
#     row_burning_loss.append(total_loss_pct)
#     data.append(row_burning_loss)

#     # Row 8: Co2 Mould Bunch Weight
#     row_bunch_weight = ["Co2 Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_bunch_weight.append(bunch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += bunch_weight
#         elif start_day <= day <= end_day:
#             total_qty += bunch_weight
#     row_bunch_weight.append(flt(total_qty))
#     data.append(row_bunch_weight)

#     # Row 9: Co2 Mould Cast Weight
#     row_cast_weight = ["Co2 Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabCo2 Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_cast_weight.append(cast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += cast_weight
#         elif start_day <= day <= end_day:
#             total_qty += cast_weight
#     row_cast_weight.append(flt(total_qty))
#     data.append(row_cast_weight)

#     # Row 10: HPML Mould Cast Weight
#     row_hpml_cast_weight = ["HPML Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_hpml_cast_weight.append(hpml_cast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += hpml_cast_weight
#         elif start_day <= day <= end_day:
#             total_qty += hpml_cast_weight
#     row_hpml_cast_weight.append(flt(total_qty))
#     data.append(row_hpml_cast_weight)

#     # Row 11: HPML Mould Bunch Weight
#     row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         hpml_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabHPML Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_hpml_bunch_weight.append(hpml_bunch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += hpml_bunch_weight
#         elif start_day <= day <= end_day:
#             total_qty += hpml_bunch_weight
#     row_hpml_bunch_weight.append(flt(total_qty))
#     data.append(row_hpml_bunch_weight)

#     # Row 12: No-Bake Mould Bunch Weight
#     row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_nb_bunch_weight.append(nb_bunch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += nb_bunch_weight
#         elif start_day <= day <= end_day:
#             total_qty += nb_bunch_weight
#     row_nb_bunch_weight.append(flt(total_qty))
#     data.append(row_nb_bunch_weight)

#     # Row 13: No-Bake Mould Cast Weight
#     row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         nb_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabNo-Bake Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_nb_cast_weight.append(nb_cast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += nb_cast_weight
#         elif start_day <= day <= end_day:
#             total_qty += nb_cast_weight
#     row_nb_cast_weight.append(flt(total_qty))
#     data.append(row_nb_cast_weight)

#     # Row 14: Jolt Squeeze Mould Bunch Weight
#     row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_js_bunch_weight.append(js_bunch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += js_bunch_weight
#         elif start_day <= day <= end_day:
#             total_qty += js_bunch_weight
#     row_js_bunch_weight.append(flt(total_qty))
#     data.append(row_js_bunch_weight)

#     # Row 15: Jolt Squeeze Mould Cast Weight
#     row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         js_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabJolt Squeeze Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_js_cast_weight.append(js_cast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += js_cast_weight
#         elif start_day <= day <= end_day:
#             total_qty += js_cast_weight
#     row_js_cast_weight.append(flt(total_qty))
#     data.append(row_js_cast_weight)

#     # Row 16: Green Sand Hand Mould Bunch Weight
#     row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_bunch_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_bunch_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_gs_bunch_weight.append(gs_bunch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += gs_bunch_weight
#         elif start_day <= day <= end_day:
#             total_qty += gs_bunch_weight
#     row_gs_bunch_weight.append(flt(total_qty))
#     data.append(row_gs_bunch_weight)

#     # Row 17: Green Sand Hand Mould Cast Weight
#     row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         gs_cast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_cast_weight)
#                 FROM `tabGreen Sand Hand Mould Batch`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_gs_cast_weight.append(gs_cast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += gs_cast_weight
#         elif start_day <= day <= end_day:
#             total_qty += gs_cast_weight
#     row_gs_cast_weight.append(flt(total_qty))
#     data.append(row_gs_cast_weight)

#     # Row 18: Fettling Weight
#     row_fettling_weight = ["Fettling Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         fettling_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_fettling_weight)
#                 FROM `tabFettling`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_fettling_weight.append(fettling_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += fettling_weight
#         elif start_day <= day <= end_day:
#             total_qty += fettling_weight
#     row_fettling_weight.append(flt(total_qty))
#     data.append(row_fettling_weight)

#     # Row 19: Finishing Weight
#     row_finishing_weight = ["Finishing Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         finishing_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_finishing_weight)
#                 FROM `tabFinishing`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_finishing_weight.append(finishing_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += finishing_weight
#         elif start_day <= day <= end_day:
#             total_qty += finishing_weight
#     row_finishing_weight.append(flt(total_qty))
#     data.append(row_finishing_weight)

#     # Row 20: Finished Stock Weight
#     row_fs_stock = ["Finished Stock Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(sle.actual_qty)
#                 FROM `tabStock Ledger Entry` sle
#                 JOIN `tabItem` i ON sle.item_code = i.name
#                 WHERE sle.posting_date <= %s
#                 AND sle.warehouse = 'Finished Goods - SHIW'
#                 AND i.item_group = 'Finished Goods'
#                 AND sle.is_cancelled = 0
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_fs_stock.append(stock_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += stock_qty
#         elif start_day <= day <= end_day:
#             total_qty += stock_qty
#     row_fs_stock.append(flt(total_qty))
#     data.append(row_fs_stock)

#     # Row 21: WIP Weight
#     row_wip_weight = ["WIP Weight"]
#     total_qty = 0
#     wip_warehouses = (
#         "Pouring - SHIW",
#         "Shake Out - SHIW",
#         "Short Blast - SHIW",
#         "Long Blast - SHIW",
#         "Jolt Squeeze - SHIW",
#         "Green Sand Hand Mould - SHIW",
#         "First Line Rejection - SHIW",
#         "Fettling - SHIW",
#         "Finishing - SHIW",
#     )
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         placeholders = ','.join(['%s'] * len(wip_warehouses))
#         query = f"""
#             SELECT SUM(sle.actual_qty)
#             FROM `tabStock Ledger Entry` sle
#             WHERE sle.posting_date <= %s
#             AND sle.warehouse IN ({placeholders})
#             AND sle.is_cancelled = 0
#         """
#         params = [date_str] + list(wip_warehouses)
#         wip_weight = flt(frappe.db.sql(query, params, as_list=True)[0][0] or 0)
#         row_wip_weight.append(wip_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += wip_weight
#         elif start_day <= day <= end_day:
#             total_qty += wip_weight
#     row_wip_weight.append(flt(total_qty))
#     data.append(row_wip_weight)

#     # Row 22: Heat Loss Wt
#     row_heat_loss = ["Heat Loss Wt"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         loss_qty = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(loss_liquid_metal)
#                 FROM `tabDaily Heat Loss`
#                 WHERE date = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_heat_loss.append(loss_qty)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += loss_qty
#         elif start_day <= day <= end_day:
#             total_qty += loss_qty
#     row_heat_loss.append(flt(total_qty))
#     data.append(row_heat_loss)

#     # Row 23: Pouring Weight
#     row_pouring_weight = ["Pouring Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         pouring_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_pouring_weight)
#                 FROM `tabPouring`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_pouring_weight.append(pouring_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += pouring_weight
#         elif start_day <= day <= end_day:
#             total_qty += pouring_weight
#     row_pouring_weight.append(flt(total_qty))
#     data.append(row_pouring_weight)

#     # Row 24: Shakeout Weight
#     row_shakeout_weight = ["Shakeout Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shakeout_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shakeout_cast_weight)
#                 FROM `tabShake Out`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_shakeout_weight.append(shakeout_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += shakeout_weight
#         elif start_day <= day <= end_day:
#             total_qty += shakeout_weight
#     row_shakeout_weight.append(flt(total_qty))
#     data.append(row_shakeout_weight)

#     # Row 25: Shotblast Weight
#     row_shotblast_weight = ["Shotblast Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         shotblast_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_shot_blast_cast_weight)
#                 FROM `tabShot Blast`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_shotblast_weight.append(shotblast_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += shotblast_weight
#         elif start_day <= day <= end_day:
#             total_qty += shotblast_weight
#     row_shotblast_weight.append(flt(total_qty))
#     data.append(row_shotblast_weight)

#     # Row 26: Rejection Weight
#     row_rejection_weight = ["Rejection Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_flr_cast_weight)
#                 FROM `tabFirst Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_rejection_weight.append(rejection_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += rejection_weight
#         elif start_day <= day <= end_day:
#             total_qty += rejection_weight
#     row_rejection_weight.append(flt(total_qty))
#     data.append(row_rejection_weight)

#     # Row 27: Deviation WT
#     row_deviation_wt = ["Deviation WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         deviation_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_deviation_weight)
#                 FROM `tabFirst Line Deviation`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_deviation_wt.append(deviation_wt)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += deviation_wt
#         elif start_day <= day <= end_day:
#             total_qty += deviation_wt
#     row_deviation_wt.append(flt(total_qty))
#     data.append(row_deviation_wt)

#     # Row 28: Repair WT
#     row_repair_wt = ["Repair WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         repair_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_repair_weight)
#                 FROM `tabRepair`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_repair_wt.append(repair_wt)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += repair_wt
#         elif start_day <= day <= end_day:
#             total_qty += repair_wt
#     row_repair_wt.append(flt(total_qty))
#     data.append(row_repair_wt)

#     # Row 29: Rejection Weight (Second Line)
#     row_second_rejection_weight = ["Rejection Weight (Second Line)"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         second_rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(rejected_wt)
#                 FROM `tabSecond Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_second_rejection_weight.append(second_rejection_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += second_rejection_weight
#         elif start_day <= day <= end_day:
#             total_qty += second_rejection_weight
#     row_second_rejection_weight.append(flt(total_qty))
#     data.append(row_second_rejection_weight)

#     # Row 30: Heat Treatment Weight
#     row_heat_treatment_wt = ["Heat Treatment Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         heat_treatment_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_heat_treatment)
#                 FROM `tabHeat Treatment`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_heat_treatment_wt.append(heat_treatment_wt)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += heat_treatment_wt
#         elif start_day <= day <= end_day:
#             total_qty += heat_treatment_wt
#     row_heat_treatment_wt.append(flt(total_qty))
#     data.append(row_heat_treatment_wt)

#     # Row 31: Wastage and Spillage
#     row_wastage_spillage = ["Wastage and Spillage"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_wastage = 0
#         pouring_docs = frappe.get_all(
#             "Pouring",
#             filters={"date": date_str},
#             fields=["name", "total_pouring_weight"]
#         )
#         for pouring in pouring_docs:
#             pouring_weight = flt(pouring.total_pouring_weight or 0)
#             unique_heat_nos = set()
#             mould_batches = frappe.get_all(
#                 "Mould Batch",
#                 filters={"parent": pouring.name},
#                 fields=["heat_no"]
#             )
#             for mb in mould_batches:
#                 if mb.heat_no:
#                     unique_heat_nos.add(mb.heat_no)
#             total_b = 0
#             for heat_no in unique_heat_nos:
#                 heat_doc = frappe.get_value(
#                     "Heat",
#                     heat_no,
#                     ["liquid_balence", "foundry_return_existing", "liquid_metal_pig"],
#                     as_dict=True,
#                 )
#                 if heat_doc:
#                     liquid_balence = flt(heat_doc.liquid_balence or 0)
#                     return_existing = flt(heat_doc.foundry_return_existing or 0)
#                     pig = flt(heat_doc.liquid_metal_pig or 0)
#                     b = flt(liquid_balence - (return_existing + pig))
#                     total_b += b
#             wastage = flt(total_b - pouring_weight)
#             total_wastage += wastage
#         row_wastage_spillage.append(flt(total_wastage))
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_wastage
#         elif start_day <= day <= end_day:
#             total_qty += total_wastage
#     row_wastage_spillage.append(flt(total_qty))
#     data.append(row_wastage_spillage)

#     # Row 32: Foundry Return Generated Weight
#     row_foundry_return = ["Foundry Return Generated Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_se_qty = 0
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Pouring",
#                 "custom_date": date_str
#             },
#             pluck="name"
#         )
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se,
#                     "t_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return.append(flt(total_se_qty))
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_se_qty
#         elif start_day <= day <= end_day:
#             total_qty += total_se_qty
#     row_foundry_return.append(flt(total_qty))
#     data.append(row_foundry_return)

#     # Row 33: Pending Order WT
#     row_pending_order = ["Pending Order WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"transaction_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_pending_order.append(total_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_weight
#         elif start_day <= day <= end_day:
#             total_qty += total_weight
#     row_pending_order.append(flt(total_qty))
#     data.append(row_pending_order)

#     # Row 34: Orders Received Weight
#     row_orders_received = ["Orders Received Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         total_weight = flt(
#             frappe.db.get_value(
#                 "Sales Order",
#                 {"delivery_date": date_str},
#                 "SUM(total_qty)"
#             ) or 0
#         )
#         row_orders_received.append(total_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_weight
#         elif start_day <= day <= end_day:
#             total_qty += total_weight
#     row_orders_received.append(flt(total_qty))
#     data.append(row_orders_received)

#     # Row 35: Total Foundry Return Physical WT
#     row_foundry_return_physical = ["Total Foundry Return Physical WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         stock_entries = frappe.get_all(
#             "Stock Entry",
#             filters={
#                 "stock_entry_type": "Material Issue",
#                 "posting_date": date_str
#             },
#             fields=["name"]
#         )
#         total_se_qty = 0
#         for se in stock_entries:
#             items = frappe.get_all(
#                 "Stock Entry Detail",
#                 filters={
#                     "parent": se.name,
#                     "s_warehouse": "Estimated Foundry Return - SHIW"
#                 },
#                 fields=["qty"]
#             )
#             total_se_qty += flt(sum(item.qty or 0 for item in items))
#         row_foundry_return_physical.append(flt(total_se_qty))
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_se_qty
#         elif start_day <= day <= end_day:
#             total_qty += total_se_qty
#     row_foundry_return_physical.append(flt(total_qty))
#     data.append(row_foundry_return_physical)

#     # Row 36: Dispatch Weight
#     row_dispatch_weight = ["Dispatch Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         delivery_notes = frappe.get_all(
#             "Delivery Note",
#             filters={"posting_date": date_str},
#             fields=["total_net_weight"]
#         )
#         total_dispatch_weight = flt(sum(dn.total_net_weight or 0 for dn in delivery_notes))
#         row_dispatch_weight.append(total_dispatch_weight)
#         if selected_days:
#             if day in selected_days:
#                 total_qty += total_dispatch_weight
#         elif start_day <= day <= end_day:
#             total_qty += total_dispatch_weight
#     row_dispatch_weight.append(flt(total_qty))
#     data.append(row_dispatch_weight)

#     return columns, data # # Row 27: Deviation WT
#     row_deviation_wt = ["Deviation WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         deviation_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_deviation_weight)
#                 FROM `tabFirst Line Deviation`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_deviation_wt.append(deviation_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += deviation_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += deviation_wt
#         else:
#             total_qty += deviation_wt
#     row_deviation_wt.append(flt(total_qty))
#     data.append(row_deviation_wt)

#     # Row 28: Repair WT
#     row_repair_wt = ["Repair WT"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         repair_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_repair_weight)
#                 FROM `tabRepair`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_repair_wt.append(repair_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += repair_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += repair_wt
#         else:
#             total_qty += repair_wt
#     row_repair_wt.append(flt(total_qty))
#     data.append(row_repair_wt)

#     # Row 29: Rejection Weight (Second Line)
#     row_second_rejection_weight = ["Rejection Weight (Second Line)"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         second_rejection_weight = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(rejected_wt)
#                 FROM `tabSecond Line Rejection`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_second_rejection_weight.append(second_rejection_weight)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += second_rejection_weight
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += second_rejection_weight
#         else:
#             total_qty += second_rejection_weight
#     row_second_rejection_weight.append(flt(total_qty))
#     data.append(row_second_rejection_weight)

#     # Row 30: Heat Treatment Weight
#     row_heat_treatment_wt = ["Heat Treatment Weight"]
#     total_qty = 0
#     for day in range(1, days_in_month + 1):
#         date_str = get_date(day)
#         heat_treatment_wt = flt(
#             frappe.db.sql(
#                 """
#                 SELECT SUM(total_heat_treatment)
#                 FROM `tabHeat Treatment`
#                 WHERE `date` = %s
#                 """,
#                 (date_str,),
#                 as_list=True,
#             )[0][0] or 0
#         )
#         row_heat_treatment_wt.append(heat_treatment_wt)
#         if use_range:
#             if start_day <= day <= end_day:
#                 total_qty += heat_treatment_wt
#         elif selected_days:
#             if day in selected_days:
#                 total_qty += heat_treatment_wt
#         else:
#             total_qty += heat_treatment_wt
#     row_heat_treatment_wt.append(flt(total_qty))
#     data.append(row_heat_treatment_wt)
#     return columns, data







import frappe
import calendar
from datetime import datetime

def flt(value, precision=2):
    try:
        return round(float(value or 0), precision)
    except (ValueError, TypeError):
        return 0.0

def execute(filters=None):
    if not filters:
        filters = {}

    month = filters.get("month")
    year = int(filters.get("year") or datetime.now().year)
    month_index = list(calendar.month_name).index(month)
    days_in_month = calendar.monthrange(year, month_index)[1]

    # Parse start_day and end_day
    start_day = int(filters.get("start_day") or 1)
    end_day = int(filters.get("end_day") or days_in_month)
    # Validate start_day and end_day
    start_day = max(1, min(start_day, days_in_month))
    end_day = max(start_day, min(end_day, days_in_month))

    # Parse selected_days (e.g., "1,2,7,9,25")
    selected_days_raw = filters.get("selected_days") or ""
    selected_days = set(
        int(day.strip()) for day in selected_days_raw.split(",") if day.strip().isdigit() and 1 <= int(day.strip()) <= days_in_month
    )

    # Column headers
    columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]+["Total"]

    def get_date(day):
        return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

    data = []

    # Row 1: Raw Materials Received
    row_raw_materials = ["Raw Materials Received"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        accepted_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(pri.qty)
                FROM `tabPurchase Receipt` pr
                JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
                JOIN `tabItem` i ON i.name = pri.item_code
                WHERE pr.posting_date = %s
                AND i.item_group = 'Raw Material'
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_raw_materials.append(accepted_qty)
        if selected_days:
            if day in selected_days:
                total_qty += accepted_qty
        elif start_day <= day <= end_day:
            total_qty += accepted_qty
    row_raw_materials.append(flt(total_qty))
    data.append(row_raw_materials)

    # Row 2: Raw Materials Melted
    row_rm_melted = ["Raw Materials Melted"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        melted_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_charge_mix_in_kg)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_rm_melted.append(melted_qty)
        if selected_days:
            if day in selected_days:
                total_qty += melted_qty
        elif start_day <= day <= end_day:
            total_qty += melted_qty
    row_rm_melted.append(flt(total_qty))
    data.append(row_rm_melted)

    # Row 3: Raw Materials Stock
    row_rm_stock = ["Raw Materials Stock"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        stock_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(sle.actual_qty)
                FROM `tabStock Ledger Entry` sle
                JOIN `tabItem` i ON sle.item_code = i.name
                WHERE sle.posting_date <= %s
                AND sle.warehouse = 'Stores - SHIW'
                AND i.item_group = 'Raw Material'
                AND sle.is_cancelled = 0
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_rm_stock.append(stock_qty)
        if selected_days:
            if day in selected_days:
                total_qty += stock_qty
        elif start_day <= day <= end_day:
            total_qty += stock_qty
    row_rm_stock.append(flt(total_qty))
    data.append(row_rm_stock)

    # Row 4: Liquid Metal Generated
    row_liquid_metal = ["Liquid Metal Generated"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        liquid_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(liquid_balence)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_liquid_metal.append(liquid_qty)
        if selected_days:
            if day in selected_days:
                total_qty += liquid_qty
        elif start_day <= day <= end_day:
            total_qty += liquid_qty
    row_liquid_metal.append(flt(total_qty))
    data.append(row_liquid_metal)

    # Row 5: Liquid Metal Returned to Furnace
    row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        returned_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(foundry_return_existing)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_returned_to_furnace.append(returned_qty)
        if selected_days:
            if day in selected_days:
                total_qty += returned_qty
        elif start_day <= day <= end_day:
            total_qty += returned_qty
    row_returned_to_furnace.append(flt(total_qty))
    data.append(row_returned_to_furnace)

    # Row 6: Liquid Metal Pigged
    row_liquid_metal_pig = ["Liquid Metal Pigged"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        pig_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(liquid_metal_pig)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_liquid_metal_pig.append(pig_qty)
        if selected_days:
            if day in selected_days:
                total_qty += pig_qty
        elif start_day <= day <= end_day:
            total_qty += pig_qty
    row_liquid_metal_pig.append(flt(total_qty))
    data.append(row_liquid_metal_pig)

    # Row 7: Burning Loss %
    row_melted_excl_3a = []
    total_melted_excl_3a = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        melted_qty_filtered = flt(
            frappe.db.sql(
                """
                 SELECT SUM(total_charge_mix_in_kg)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                AND furnace_no NOT IN ('1A - 200 Kg Furnace', '1B - 200 Kg Furnace')
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_melted_excl_3a.append(melted_qty_filtered)
        if selected_days and day in selected_days:
            total_melted_excl_3a += melted_qty_filtered
        elif not selected_days and start_day <= day <= end_day:
            total_melted_excl_3a += melted_qty_filtered
    row_burning_loss = ["Burning Loss %"]
    total_loss_pct = 0
    valid_days = 0
    for i in range(days_in_month):
        melted = flt(row_melted_excl_3a[i])
        liquid = flt(row_liquid_metal[i + 1])
        loss_pct = flt(((melted - liquid) / melted) * 100 if melted > 0 else 0)
        row_burning_loss.append(loss_pct)
        if selected_days:
            if (i + 1) in selected_days:
                total_loss_pct += loss_pct
                valid_days += 1
        elif start_day <= (i + 1) <= end_day:
            total_loss_pct += loss_pct
            valid_days += 1
    total_loss_pct = flt(total_loss_pct / valid_days if valid_days > 0 else 0)
    row_burning_loss.append(total_loss_pct)
    data.append(row_burning_loss)

    # Row 8: Co2 Mould Bunch Weight
    row_bunch_weight = ["Co2 Mould Bunch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        bunch_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabCo2 Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_bunch_weight.append(bunch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += bunch_weight
        elif start_day <= day <= end_day:
            total_qty += bunch_weight
    row_bunch_weight.append(flt(total_qty))
    data.append(row_bunch_weight)

    # Row 9: Co2 Mould Cast Weight
    row_cast_weight = ["Co2 Mould Cast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        cast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabCo2 Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_cast_weight.append(cast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += cast_weight
        elif start_day <= day <= end_day:
            total_qty += cast_weight
    row_cast_weight.append(flt(total_qty))
    data.append(row_cast_weight)

    # Row 10: HPML Mould Cast Weight
    row_hpml_cast_weight = ["HPML Mould Cast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        hpml_cast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabHPML Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_hpml_cast_weight.append(hpml_cast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += hpml_cast_weight
        elif start_day <= day <= end_day:
            total_qty += hpml_cast_weight
    row_hpml_cast_weight.append(flt(total_qty))
    data.append(row_hpml_cast_weight)

    # Row 11: HPML Mould Bunch Weight
    row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        hpml_bunch_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabHPML Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_hpml_bunch_weight.append(hpml_bunch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += hpml_bunch_weight
        elif start_day <= day <= end_day:
            total_qty += hpml_bunch_weight
    row_hpml_bunch_weight.append(flt(total_qty))
    data.append(row_hpml_bunch_weight)

    # Row 12: No-Bake Mould Bunch Weight
    row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        nb_bunch_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabNo-Bake Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_nb_bunch_weight.append(nb_bunch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += nb_bunch_weight
        elif start_day <= day <= end_day:
            total_qty += nb_bunch_weight
    row_nb_bunch_weight.append(flt(total_qty))
    data.append(row_nb_bunch_weight)

    # Row 13: No-Bake Mould Cast Weight
    row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        nb_cast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabNo-Bake Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_nb_cast_weight.append(nb_cast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += nb_cast_weight
        elif start_day <= day <= end_day:
            total_qty += nb_cast_weight
    row_nb_cast_weight.append(flt(total_qty))
    data.append(row_nb_cast_weight)

    # Row 14: Jolt Squeeze Mould Bunch Weight
    row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        js_bunch_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabJolt Squeeze Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_js_bunch_weight.append(js_bunch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += js_bunch_weight
        elif start_day <= day <= end_day:
            total_qty += js_bunch_weight
    row_js_bunch_weight.append(flt(total_qty))
    data.append(row_js_bunch_weight)

    # Row 15: Jolt Squeeze Mould Cast Weight
    row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        js_cast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabJolt Squeeze Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_js_cast_weight.append(js_cast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += js_cast_weight
        elif start_day <= day <= end_day:
            total_qty += js_cast_weight
    row_js_cast_weight.append(flt(total_qty))
    data.append(row_js_cast_weight)

    # Row 16: Green Sand Hand Mould Bunch Weight
    row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        gs_bunch_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabGreen Sand Hand Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_gs_bunch_weight.append(gs_bunch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += gs_bunch_weight
        elif start_day <= day <= end_day:
            total_qty += gs_bunch_weight
    row_gs_bunch_weight.append(flt(total_qty))
    data.append(row_gs_bunch_weight)

    # Row 17: Green Sand Hand Mould Cast Weight
    row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        gs_cast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabGreen Sand Hand Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_gs_cast_weight.append(gs_cast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += gs_cast_weight
        elif start_day <= day <= end_day:
            total_qty += gs_cast_weight
    row_gs_cast_weight.append(flt(total_qty))
    data.append(row_gs_cast_weight)

    # Row 18: Fettling Weight
    row_fettling_weight = ["Fettling Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        fettling_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_fettling_weight)
                FROM `tabFettling`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_fettling_weight.append(fettling_weight)
        if selected_days:
            if day in selected_days:
                total_qty += fettling_weight
        elif start_day <= day <= end_day:
            total_qty += fettling_weight
    row_fettling_weight.append(flt(total_qty))
    data.append(row_fettling_weight)

    # Row 19: Finishing Weight
    row_finishing_weight = ["Finishing Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        finishing_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_finishing_weight)
                FROM `tabFinishing`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_finishing_weight.append(finishing_weight)
        if selected_days:
            if day in selected_days:
                total_qty += finishing_weight
        elif start_day <= day <= end_day:
            total_qty += finishing_weight
    row_finishing_weight.append(flt(total_qty))
    data.append(row_finishing_weight)

    # Row 20: Finished Stock Weight
    row_fs_stock = ["Finished Stock Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        stock_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(sle.actual_qty)
                FROM `tabStock Ledger Entry` sle
                JOIN `tabItem` i ON sle.item_code = i.name
                WHERE sle.posting_date <= %s
                AND sle.warehouse = 'Finished Goods - SHIW'
                AND i.item_group = 'Finished Goods'
                AND sle.is_cancelled = 0
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_fs_stock.append(stock_qty)
        if selected_days:
            if day in selected_days:
                total_qty += stock_qty
        elif start_day <= day <= end_day:
            total_qty += stock_qty
    row_fs_stock.append(flt(total_qty))
    data.append(row_fs_stock)

    # Row 21: WIP Weight
    row_wip_weight = ["WIP Weight"]
    total_qty = 0
    wip_warehouses = (
        "Pouring - SHIW",
        "Shake Out - SHIW",
        "Short Blast - SHIW",
        "Long Blast - SHIW",
        "Jolt Squeeze - SHIW",
        "Green Sand Hand Mould - SHIW",
        "First Line Rejection - SHIW",
        "Fettling - SHIW",
        "Finishing - SHIW",
    )
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        placeholders = ','.join(['%s'] * len(wip_warehouses))
        query = f"""
            SELECT SUM(sle.actual_qty)
            FROM `tabStock Ledger Entry` sle
            WHERE sle.posting_date <= %s
            AND sle.warehouse IN ({placeholders})
            AND sle.is_cancelled = 0
        """
        params = [date_str] + list(wip_warehouses)
        wip_weight = flt(frappe.db.sql(query, params, as_list=True)[0][0] or 0)
        row_wip_weight.append(wip_weight)
        if selected_days:
            if day in selected_days:
                total_qty += wip_weight
        elif start_day <= day <= end_day:
            total_qty += wip_weight
    row_wip_weight.append(flt(total_qty))
    data.append(row_wip_weight)

    # Row 22: Heat Loss Wt
    row_heat_loss = ["Heat Loss Wt"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        loss_qty = flt(
            frappe.db.sql(
                """
                SELECT SUM(loss_liquid_metal)
                FROM `tabDaily Heat Loss`
                WHERE date = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_heat_loss.append(loss_qty)
        if selected_days:
            if day in selected_days:
                total_qty += loss_qty
        elif start_day <= day <= end_day:
            total_qty += loss_qty
    row_heat_loss.append(flt(total_qty))
    data.append(row_heat_loss)

    # Row 23: Pouring Weight
    row_pouring_weight = ["Pouring Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        pouring_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_pouring_weight)
                FROM `tabPouring`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_pouring_weight.append(pouring_weight)
        if selected_days:
            if day in selected_days:
                total_qty += pouring_weight
        elif start_day <= day <= end_day:
            total_qty += pouring_weight
    row_pouring_weight.append(flt(total_qty))
    data.append(row_pouring_weight)

    # Row 24: Shakeout Weight
    row_shakeout_weight = ["Shakeout Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        shakeout_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_shakeout_cast_weight)
                FROM `tabShake Out`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_shakeout_weight.append(shakeout_weight)
        if selected_days:
            if day in selected_days:
                total_qty += shakeout_weight
        elif start_day <= day <= end_day:
            total_qty += shakeout_weight
    row_shakeout_weight.append(flt(total_qty))
    data.append(row_shakeout_weight)

    # Row 25: Shotblast Weight
    row_shotblast_weight = ["Shotblast Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        shotblast_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_shot_blast_cast_weight)
                FROM `tabShot Blast`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_shotblast_weight.append(shotblast_weight)
        if selected_days:
            if day in selected_days:
                total_qty += shotblast_weight
        elif start_day <= day <= end_day:
            total_qty += shotblast_weight
    row_shotblast_weight.append(flt(total_qty))
    data.append(row_shotblast_weight)

    # Row 26: Rejection Weight
    row_rejection_weight = ["Rejection Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        rejection_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_flr_cast_weight)
                FROM `tabFirst Line Rejection`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_rejection_weight.append(rejection_weight)
        if selected_days:
            if day in selected_days:
                total_qty += rejection_weight
        elif start_day <= day <= end_day:
            total_qty += rejection_weight
    row_rejection_weight.append(flt(total_qty))
    data.append(row_rejection_weight)

    # Row 27: Deviation WT
    row_deviation_wt = ["Deviation WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        deviation_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_deviation_weight)
                FROM `tabFirst Line Deviation`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_deviation_wt.append(deviation_wt)
        if selected_days:
            if day in selected_days:
                total_qty += deviation_wt
        elif start_day <= day <= end_day:
            total_qty += deviation_wt
    row_deviation_wt.append(flt(total_qty))
    data.append(row_deviation_wt)

    # Row 28: Repair WT
    row_repair_wt = ["Repair WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        repair_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_repair_weight)
                FROM `tabRepair`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_repair_wt.append(repair_wt)
        if selected_days:
            if day in selected_days:
                total_qty += repair_wt
        elif start_day <= day <= end_day:
            total_qty += repair_wt
    row_repair_wt.append(flt(total_qty))
    data.append(row_repair_wt)

    # Row 29: Rejection Weight (Second Line)
    row_second_rejection_weight = ["Rejection Weight (Second Line)"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        second_rejection_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(rejected_wt)
                FROM `tabSecond Line Rejection`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_second_rejection_weight.append(second_rejection_weight)
        if selected_days:
            if day in selected_days:
                total_qty += second_rejection_weight
        elif start_day <= day <= end_day:
            total_qty += second_rejection_weight
    row_second_rejection_weight.append(flt(total_qty))
    data.append(row_second_rejection_weight)

    # Row 30: Heat Treatment Weight
    row_heat_treatment_wt = ["Heat Treatment Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        heat_treatment_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_heat_treatment)
                FROM `tabHeat Treatment`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_heat_treatment_wt.append(heat_treatment_wt)
        if selected_days:
            if day in selected_days:
                total_qty += heat_treatment_wt
        elif start_day <= day <= end_day:
            total_qty += heat_treatment_wt
    row_heat_treatment_wt.append(flt(total_qty))
    data.append(row_heat_treatment_wt)

    # Row 31: Wastage and Spillage
    row_wastage_spillage = ["Wastage and Spillage"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        total_wastage = 0
        pouring_docs = frappe.get_all(
            "Pouring",
            filters={"date": date_str},
            fields=["name", "total_pouring_weight"]
        )
        for pouring in pouring_docs:
            pouring_weight = flt(pouring.total_pouring_weight or 0)
            unique_heat_nos = set()
            mould_batches = frappe.get_all(
                "Mould Batch",
                filters={"parent": pouring.name},
                fields=["heat_no"]
            )
            for mb in mould_batches:
                if mb.heat_no:
                    unique_heat_nos.add(mb.heat_no)
            total_b = 0
            for heat_no in unique_heat_nos:
                heat_doc = frappe.get_value(
                    "Heat",
                    heat_no,
                    ["liquid_balence", "foundry_return_existing", "liquid_metal_pig"],
                    as_dict=True,
                )
                if heat_doc:
                    liquid_balence = flt(heat_doc.liquid_balence or 0)
                    return_existing = flt(heat_doc.foundry_return_existing or 0)
                    pig = flt(heat_doc.liquid_metal_pig or 0)
                    b = flt(liquid_balence - (return_existing + pig))
                    total_b += b
            wastage = flt(total_b - pouring_weight)
            total_wastage += wastage
        row_wastage_spillage.append(flt(total_wastage))
        if selected_days:
            if day in selected_days:
                total_qty += total_wastage
        elif start_day <= day <= end_day:
            total_qty += total_wastage
    row_wastage_spillage.append(flt(total_qty))
    data.append(row_wastage_spillage)

    # Row 32: Foundry Return Generated Weight
    row_foundry_return = ["Foundry Return Generated Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        total_se_qty = 0
        stock_entries = frappe.get_all(
            "Stock Entry",
            filters={
                "stock_entry_type": "Pouring",
                "custom_date": date_str
            },
            pluck="name"
        )
        for se in stock_entries:
            items = frappe.get_all(
                "Stock Entry Detail",
                filters={
                    "parent": se,
                    "t_warehouse": "Estimated Foundry Return - SHIW"
                },
                fields=["qty"]
            )
            total_se_qty += flt(sum(item.qty or 0 for item in items))
        row_foundry_return.append(flt(total_se_qty))
        if selected_days:
            if day in selected_days:
                total_qty += total_se_qty
        elif start_day <= day <= end_day:
            total_qty += total_se_qty
    row_foundry_return.append(flt(total_qty))
    data.append(row_foundry_return)

    # Row 33: Pending Order WT
    row_pending_order = ["Pending Order WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        total_weight = flt(
            frappe.db.get_value(
                "Sales Order",
                {"transaction_date": date_str},
                "SUM(total_qty)"
            ) or 0
        )
        row_pending_order.append(total_weight)
        if selected_days:
            if day in selected_days:
                total_qty += total_weight
        elif start_day <= day <= end_day:
            total_qty += total_weight
    row_pending_order.append(flt(total_qty))
    data.append(row_pending_order)

    # Row 34: Orders Received Weight
    row_orders_received = ["Orders Received Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        total_weight = flt(
            frappe.db.get_value(
                "Sales Order",
                {"delivery_date": date_str},
                "SUM(total_qty)"
            ) or 0
        )
        row_orders_received.append(total_weight)
        if selected_days:
            if day in selected_days:
                total_qty += total_weight
        elif start_day <= day <= end_day:
            total_qty += total_weight
    row_orders_received.append(flt(total_qty))
    data.append(row_orders_received)

    # Row 35: Total Foundry Return Physical WT
    row_foundry_return_physical = ["Total Foundry Return Physical WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        stock_entries = frappe.get_all(
            "Stock Entry",
            filters={
                "stock_entry_type": "Material Issue",
                "posting_date": date_str
            },
            fields=["name"]
        )
        total_se_qty = 0
        for se in stock_entries:
            items = frappe.get_all(
                "Stock Entry Detail",
                filters={
                    "parent": se.name,
                    "s_warehouse": "Estimated Foundry Return - SHIW"
                },
                fields=["qty"]
            )
            total_se_qty += flt(sum(item.qty or 0 for item in items))
        row_foundry_return_physical.append(flt(total_se_qty))
        if selected_days:
            if day in selected_days:
                total_qty += total_se_qty
        elif start_day <= day <= end_day:
            total_qty += total_se_qty
    row_foundry_return_physical.append(flt(total_qty))
    data.append(row_foundry_return_physical)

    # Row 36: Dispatch Weight
    row_dispatch_weight = ["Dispatch Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        delivery_notes = frappe.get_all(
            "Delivery Note",
            filters={"posting_date": date_str},
            fields=["total_net_weight"]
        )
        total_dispatch_weight = flt(sum(dn.total_net_weight or 0 for dn in delivery_notes))
        row_dispatch_weight.append(total_dispatch_weight)
        if selected_days:
            if day in selected_days:
                total_qty += total_dispatch_weight
        elif start_day <= day <= end_day:
            total_qty += total_dispatch_weight
    row_dispatch_weight.append(flt(total_qty))
    data.append(row_dispatch_weight)

    return columns, data # # Row 27: Deviation WT
    row_deviation_wt = ["Deviation WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        deviation_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_deviation_weight)
                FROM `tabFirst Line Deviation`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_deviation_wt.append(deviation_wt)
        if use_range:
            if start_day <= day <= end_day:
                total_qty += deviation_wt
        elif selected_days:
            if day in selected_days:
                total_qty += deviation_wt
        else:
            total_qty += deviation_wt
    row_deviation_wt.append(flt(total_qty))
    data.append(row_deviation_wt)

    # Row 28: Repair WT
    row_repair_wt = ["Repair WT"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        repair_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_repair_weight)
                FROM `tabRepair`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_repair_wt.append(repair_wt)
        if use_range:
            if start_day <= day <= end_day:
                total_qty += repair_wt
        elif selected_days:
            if day in selected_days:
                total_qty += repair_wt
        else:
            total_qty += repair_wt
    row_repair_wt.append(flt(total_qty))
    data.append(row_repair_wt)

    # Row 29: Rejection Weight (Second Line)
    row_second_rejection_weight = ["Rejection Weight (Second Line)"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        second_rejection_weight = flt(
            frappe.db.sql(
                """
                SELECT SUM(rejected_wt)
                FROM `tabSecond Line Rejection`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_second_rejection_weight.append(second_rejection_weight)
        if use_range:
            if start_day <= day <= end_day:
                total_qty += second_rejection_weight
        elif selected_days:
            if day in selected_days:
                total_qty += second_rejection_weight
        else:
            total_qty += second_rejection_weight
    row_second_rejection_weight.append(flt(total_qty))
    data.append(row_second_rejection_weight)

    # Row 30: Heat Treatment Weight
    row_heat_treatment_wt = ["Heat Treatment Weight"]
    total_qty = 0
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        heat_treatment_wt = flt(
            frappe.db.sql(
                """
                SELECT SUM(total_heat_treatment)
                FROM `tabHeat Treatment`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0] or 0
        )
        row_heat_treatment_wt.append(heat_treatment_wt)
        if use_range:
            if start_day <= day <= end_day:
                total_qty += heat_treatment_wt
        elif selected_days:
            if day in selected_days:
                total_qty += heat_treatment_wt
        else:
            total_qty += heat_treatment_wt
    row_heat_treatment_wt.append(flt(total_qty))
    data.append(row_heat_treatment_wt)
    return columns, data
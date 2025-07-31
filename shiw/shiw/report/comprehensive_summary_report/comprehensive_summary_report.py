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



import frappe
import calendar


def execute(filters=None):
    if not filters:
        return [], []

    month = filters.get("month")
    year = int(filters.get("year"))
    month_index = list(calendar.month_name).index(month)
    days_in_month = calendar.monthrange(year, month_index)[1]

    # Column headers
    columns = ["Description"] + [f"{day}-{month[:3]}" for day in range(1, days_in_month + 1)]

    def get_date(day):
        return f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"

    data = []

    # Row 1: Raw Materials Received
    row_raw_materials = ["Raw Materials Received"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        accepted_qty = (
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
            )[0][0]
            or 0
        )
        row_raw_materials.append(accepted_qty)
    data.append(row_raw_materials)

    # Row 2: Raw Materials Melted
    row_rm_melted = ["Raw Materials Melted"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        melted_qty = (
            frappe.db.sql(
                """
                SELECT SUM(total_charge_mix_in_kg)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_rm_melted.append(melted_qty)
    data.append(row_rm_melted)

    # Row 3: Raw Materials Stock
    row_rm_stock = ["Raw Materials Stock"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        stock_qty = (
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
            )[0][0]
            or 0
        )
        row_rm_stock.append(stock_qty)
    data.append(row_rm_stock)

    # Row 4: Liquid Metal Generated
    row_liquid_metal = ["Liquid Metal Generated"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        liquid_qty = (
            frappe.db.sql(
                """
                SELECT SUM(liquid_balence)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_liquid_metal.append(liquid_qty)
    data.append(row_liquid_metal)

    # Row 5: Liquid Metal Returned to Furnace
    row_returned_to_furnace = ["Liquid Metal Returned to Furnace"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        returned_qty = (
            frappe.db.sql(
                """
                SELECT SUM(foundry_return_existing)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_returned_to_furnace.append(returned_qty)
    data.append(row_returned_to_furnace)

    # Row 6: Liquid Metal Pigged
    row_liquid_metal_pig = ["Liquid Metal Pigged"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        pig_qty = (
            frappe.db.sql(
                """
                SELECT SUM(liquid_metal_pig)
                FROM `tabHeat`
                WHERE `date` = %s AND docstatus = 1
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_liquid_metal_pig.append(pig_qty)
    data.append(row_liquid_metal_pig)

    # # Row 7: Burning Loss %
    # row_burning_loss = ["Burning Loss %"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     loss_pct = (
    #         frappe.db.sql(
    #             """
    #             SELECT AVG(burning_loss)
    #             FROM `tabHeat`
    #             WHERE `date` = %s AND docstatus = 1
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_burning_loss.append(round(loss_pct, 2))
    # data.append(row_burning_loss)
    row_burning_loss = ["Burning Loss %"]
    for i in range(1, days_in_month + 1):
        melted = row_rm_melted[i] or 0
        liquid = row_liquid_metal[i] or 0

        if melted > 0:
            loss_pct = round(((melted - liquid) / melted) * 100, 2)
        else:
            loss_pct = 0

        row_burning_loss.append(loss_pct)

    data.append(row_burning_loss)


    # Row 8: Co2 Mould Bunch Weight
    row_bunch_weight = ["Co2 Mould Bunch Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        bunch_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabCo2 Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_bunch_weight.append(bunch_weight)
    data.append(row_bunch_weight)

    # Row 9: Co2 Mould Cast Weight
    row_cast_weight = ["Co2 Mould Cast Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        cast_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabCo2 Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_cast_weight.append(cast_weight)
    data.append(row_cast_weight)

    # Row 10: HPML Mould Cast Weight
    row_hpml_cast_weight = ["HPML Mould Cast Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        hpml_cast_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabHPML Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_hpml_cast_weight.append(hpml_cast_weight)
    data.append(row_hpml_cast_weight)

    # Row 11: HPML Mould Bunch Weight
    row_hpml_bunch_weight = ["HPML Mould Bunch Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        hpml_bunch_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabHPML Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_hpml_bunch_weight.append(hpml_bunch_weight)
    data.append(row_hpml_bunch_weight)

    # Row 12: No-Bake Mould Bunch Weight
    row_nb_bunch_weight = ["No-Bake Mould Bunch Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        nb_bunch_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabNo-Bake Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_nb_bunch_weight.append(nb_bunch_weight)
    data.append(row_nb_bunch_weight)

    # Row 13: No-Bake Mould Cast Weight
    row_nb_cast_weight = ["No-Bake Mould Cast Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        nb_cast_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabNo-Bake Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_nb_cast_weight.append(nb_cast_weight)
    data.append(row_nb_cast_weight)

    # Row 14: Jolt Squeeze Mould Bunch Weight
    row_js_bunch_weight = ["Jolt Squeeze Mould Bunch Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        js_bunch_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_bunch_weight)
                FROM `tabJolt Squeeze Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_js_bunch_weight.append(js_bunch_weight)
    data.append(row_js_bunch_weight)

    # Row 15: Jolt Squeeze Mould Cast Weight
    row_js_cast_weight = ["Jolt Squeeze Mould Cast Weight"]
    for day in range(1, days_in_month + 1):
        date_str = get_date(day)
        js_cast_weight = (
            frappe.db.sql(
                """
                SELECT SUM(total_cast_weight)
                FROM `tabJolt Squeeze Mould Batch`
                WHERE `date` = %s
                """,
                (date_str,),
                as_list=True,
            )[0][0]
            or 0
        )
        row_js_cast_weight.append(js_cast_weight)
    data.append(row_js_cast_weight)

    # # Row 16: Green Sand Hand Mould Bunch Weight
    # row_gs_bunch_weight = ["Green Sand Hand Mould Bunch Weight"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     gs_bunch_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_bunch_weight)
    #             FROM `tabGreen Sand Hand Mould Batch`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_gs_bunch_weight.append(gs_bunch_weight)
    # data.append(row_gs_bunch_weight)

    # # Row 17: Green Sand Hand Mould Cast Weight
    # row_gs_cast_weight = ["Green Sand Hand Mould Cast Weight"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     gs_cast_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_cast_weight)
    #             FROM `tabGreen Sand Hand Mould Batch`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_gs_cast_weight.append(gs_cast_weight)
    # data.append(row_gs_cast_weight)

    # # Row 18: Fettling Weight
    # row_fettling_weight = ["Fettling Weight"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     fettling_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_fettling_weight)
    #             FROM `tabFettling`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_fettling_weight.append(fettling_weight)
    # data.append(row_fettling_weight)

    # # Row 19: Finishing Weight
    # row_finishing_weight = ["Finishing Weight"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     finishing_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_finishing_weight)
    #             FROM `tabFinishing`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_finishing_weight.append(finishing_weight)
    # data.append(row_finishing_weight)

    # # Row 20: Finished Stock Weight
    # row_fs_stock = ["Finished Stock Weight"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     stock_qty = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(sle.actual_qty)
    #             FROM `tabStock Ledger Entry` sle
    #             JOIN `tabItem` i ON sle.item_code = i.name
    #             WHERE sle.posting_date <= %s
    #             AND sle.warehouse = 'FInished Good - SHIW'
    #             AND i.item_group = 'Finished Goods'
    #             AND sle.is_cancelled = 0
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_fs_stock.append(stock_qty)
    # data.append(row_fs_stock)

    # # Row 21: WIP Weight
    # row_wip_weight = ["WIP Weight"]
    # wip_warehouses = (
    #     "Pouring - SHIW",
    #     "Shake Out - SHIW",
    #     "Short Blast - SHIW",
    #     "Long Blast - SHIW",
    #     "Jolt Squeeze - SHIW",
    #     "Green Sand Hand Mould - SHIW",
    #     "First Line Rejection - SHIW",
    #     "Fettling - SHIW",
    #     "Finishing - SHIW",
    # )
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     placeholders = ','.join(['%s'] * len(wip_warehouses))
    #     query = f"""
    #         SELECT SUM(sle.actual_qty)
    #         FROM `tabStock Ledger Entry` sle
    #         WHERE sle.posting_date <= %s
    #         AND sle.warehouse IN ({placeholders})
    #         AND sle.is_cancelled = 0
    #     """
    #     params = [date_str] + list(wip_warehouses)
    #     wip_weight = frappe.db.sql(query, params, as_list=True)[0][0] or 0
    #     row_wip_weight.append(wip_weight)
    # data.append(row_wip_weight)

    # # Row 22: Heat Loss Wt
    # row_heat_loss = ["Heat Loss Wt"]
    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
    #     loss_qty = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(loss_liquid_metal)
    #             FROM `tabDaily Heat Loss`
    #             WHERE date = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )
    #     row_heat_loss.append(loss_qty)
    # data.append(row_heat_loss)

    # # Row 23: Pouring Weight
    # row_pouring_weight = ["Pouring Weight"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)
        
    #     pouring_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_pouring_weight)
    #             FROM `tabPouring`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_pouring_weight.append(pouring_weight)

    # data.append(row_pouring_weight)

    # # Row 24: Shakeout Weight
    # row_shakeout_weight = ["Shakeout Weight"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     shakeout_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_shakeout_cast_weight)
    #             FROM `tabShake Out`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_shakeout_weight.append(shakeout_weight)

    # data.append(row_shakeout_weight)

    # # Row 25: Shotblast Weight
    # row_shotblast_weight = ["Shotblast Weight"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     shotblast_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_shot_blast_cast_weight)
    #             FROM `tabShot Blast`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_shotblast_weight.append(shotblast_weight)

    # data.append(row_shotblast_weight)

    # # Row 26: Rejection Weight
    # row_rejection_weight = ["Rejection Weight"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     rejection_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_flr_cast_weight)
    #             FROM `tabFirst Line Rejection`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_rejection_weight.append(rejection_weight)

    # data.append(row_rejection_weight)

    # # Row 27: Deviation WT
    # row_deviation_wt = ["Deviation WT"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     deviation_wt = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_deviation_weight)
    #             FROM `tabFirst Line Deviation`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_deviation_wt.append(deviation_wt)

    # data.append(row_deviation_wt)


    # # Row 28: Repair WT
    # row_repair_wt = ["Repair WT"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     repair_wt = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_repair_weight)
    #             FROM `tabRepair`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_repair_wt.append(repair_wt)

    # data.append(row_repair_wt)

    # # Row 29: Rejection Weight (Second Line)
    # row_second_rejection_weight = ["Rejection Weight (Second Line)"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     second_rejection_weight = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(rejected_wt)
    #             FROM `tabSecond Line Rejection`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_second_rejection_weight.append(second_rejection_weight)

    # data.append(row_second_rejection_weight)

    # # Row 30: Heat Treatment Weight
    # row_heat_treatment_wt = ["Heat Treatment Weight"]

    # for day in range(1, days_in_month + 1):
    #     date_str = get_date(day)

    #     heat_treatment_wt = (
    #         frappe.db.sql(
    #             """
    #             SELECT SUM(total_heat_treatment)
    #             FROM `tabHeat Treatment`
    #             WHERE `date` = %s
    #             """,
    #             (date_str,),
    #             as_list=True,
    #         )[0][0]
    #         or 0
    #     )

    #     row_heat_treatment_wt.append(heat_treatment_wt)

    # data.append(row_heat_treatment_wt)





    return columns, data
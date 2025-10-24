# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt


# import frappe

# WAREHOUSE = "Stores - SHIW"

# def execute(filters=None):
#     filters = filters or {}
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
#         {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
#         {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
#         {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
#     ]

# def get_data(filters):
#     # Build filter list properly (avoid dict-with-operators issues)
#     flt_list = []
#     if filters.get("custom_department"):
#         flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
#     if filters.get("item"):  # Link to Item returns the Item's name (item_code)
#         flt_list.append(["Item", "name", "=", filters["item"]])

#     items = frappe.get_all(
#         "Item",
#         filters=flt_list,
#         fields=[
#             "name",
#             "item_name",
#             "stock_uom as uom",
#             "custom_department",
#             "custom_minimum_stock",
#             "custom_maximum_stock",
#         ],
#         order_by="item_name asc"
#     )

#     data = []
#     for it in items:
#         store_qty = frappe.db.get_value(
#             "Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty"
#         ) or 0

#         data.append({
#             "custom_department": it.custom_department,
#             "item_name": it.item_name,
#             "uom": it.uom,
#             "store_qty": store_qty,
#             "custom_minimum_stock": it.custom_minimum_stock,
#             "custom_maximum_stock": it.custom_maximum_stock,
#         })
#     return data


# import frappe

# WAREHOUSE = "Stores - SHIW"

# def execute(filters=None):
#     filters = filters or {}
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data


# def get_columns():
#     return [
#         {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
#         {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
#         {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
#         {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
#     ]


# def get_data(filters):
#     flt_list = []
#     if filters.get("custom_department"):
#         flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
#     if filters.get("item"):
#         flt_list.append(["Item", "name", "=", filters["item"]])

#     items = frappe.get_all(
#         "Item",
#         filters=flt_list,
#         fields=[
#             "name",
#             "item_name",
#             "stock_uom as uom",
#             "custom_department",
#             "custom_minimum_stock",
#             "custom_maximum_stock",
#         ],
#         order_by="item_name asc"
#     )

#     data = []
#     for it in items:
#         store_qty = frappe.db.get_value(
#             "Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty"
#         ) or 0

#         # Determine color status
#         color_status = "green"
#         if it.custom_minimum_stock and store_qty < it.custom_minimum_stock:
#             color_status = "red"
#         elif it.custom_maximum_stock and store_qty > it.custom_maximum_stock:
#             color_status = "purple"

#         # Apply filter for color if chosen
#         if filters.get("color_status") and filters["color_status"] != color_status:
#             continue

#         data.append({
#             "custom_department": it.custom_department,
#             "item_name": it.item_name,
#             "uom": it.uom,
#             "store_qty": store_qty,
#             "custom_minimum_stock": it.custom_minimum_stock,
#             "custom_maximum_stock": it.custom_maximum_stock,
#         })
#     return data


# import frappe

# WAREHOUSE = "Stores - SHIW"

# def execute(filters=None):
#     filters = filters or {}
#     columns = get_columns()
#     data = get_data(filters)

#     # If user selected a "color filter", apply it here
#     if filters.get("color_filter"):
#         data = [row for row in data if row["status"] == filters["color_filter"]]

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
#         {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
#         {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
#         {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
#         # hidden helper column
#         {"label": "Status", "fieldname": "status", "fieldtype": "Data", "hidden": 1},
#     ]


# def get_data(filters):
#     flt_list = []
#     if filters.get("custom_department"):
#         flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
#     if filters.get("item"):
#         flt_list.append(["Item", "name", "=", filters["item"]])

#     items = frappe.get_all(
#         "Item",
#         filters=flt_list,
#         fields=[
#             "name",
#             "item_name",
#             "stock_uom as uom",
#             "custom_department",
#             "custom_minimum_stock",
#             "custom_maximum_stock",
#         ],
#         order_by="item_name asc"
#     )

#     data = []
#     for it in items:
#         store_qty = frappe.db.get_value(
#             "Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty"
#         ) or 0

#         # Determine status
#         if store_qty < (it.custom_minimum_stock or 0):
#             status = "Red"
#         elif (it.custom_minimum_stock or 0) <= store_qty <= (it.custom_maximum_stock or 0):
#             status = "Green"
#         else:
#             status = "Purple"

#         data.append({
#             "custom_department": it.custom_department,
#             "item_name": it.item_name,
#             "uom": it.uom,
#             "store_qty": store_qty,
#             "custom_minimum_stock": it.custom_minimum_stock,
#             "custom_maximum_stock": it.custom_maximum_stock,
#             "status": status,  # hidden column for filtering
#         })
#     return data


import frappe

WAREHOUSE = "Stores - SHIW"


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)

	# If user selected a "color filter", apply it here
	if filters.get("color_filter"):
		data = [row for row in data if row["status"] == filters["color_filter"]]

	return columns, data


def get_columns():
	return [
		{"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
		{"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
		{"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
		{"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
		{"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
		{
			"label": "Balance Valuation",
			"fieldname": "balance_valuation",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": "Excess Stock Valuation",
			"fieldname": "excess_stock_valuation",
			"fieldtype": "Currency",
			"width": 180,
		},
		# hidden helper column
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "hidden": 1},
	]


def get_data(filters):
	flt_list = []
	if filters.get("custom_department"):
		flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
	if filters.get("item"):
		flt_list.append(["Item", "name", "=", filters["item"]])

	items = frappe.get_all(
		"Item",
		filters=flt_list,
		fields=[
			"name",
			"item_name",
			"stock_uom as uom",
			"custom_department",
			"custom_minimum_stock",
			"custom_maximum_stock",
		],
		order_by="item_name asc",
	)

	data = []
	for it in items:
		store_qty = (
			frappe.db.get_value("Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty") or 0
		)

		# Get stock value and valuation rate from Bin table
		bin_data = (
			frappe.db.get_value(
				"Bin",
				{"item_code": it.name, "warehouse": WAREHOUSE},
				["stock_value", "valuation_rate"],
				as_dict=True,
			)
			or {}
		)

		stock_value = bin_data.get("stock_value") or 0
		valuation_rate = bin_data.get("valuation_rate") or 0

		min_qty = it.custom_minimum_stock or 0
		max_qty = it.custom_maximum_stock or 0

		# Calculate excess stock valuation
		excess_stock_valuation = 0
		if store_qty > max_qty:
			excess_qty = store_qty - max_qty
			excess_stock_valuation = excess_qty * valuation_rate

		# Determine status
		if store_qty < min_qty:
			status = "Red"
		elif min_qty <= store_qty <= max_qty:
			status = "Green"
		else:
			status = "Purple"

		data.append(
			{
				"custom_department": it.custom_department,
				"item_name": it.item_name,
				"uom": it.uom,
				"store_qty": store_qty,
				"custom_minimum_stock": min_qty,
				"custom_maximum_stock": max_qty,
				"balance_valuation": stock_value,
				"excess_stock_valuation": excess_stock_valuation,
				"status": status,  # hidden column for filtering
			}
		)
	return data

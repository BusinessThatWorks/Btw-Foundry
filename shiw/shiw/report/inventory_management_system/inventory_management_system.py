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


# import frappe

# WAREHOUSE = "Stores - SHIW"


# def execute(filters=None):
# 	filters = filters or {}
# 	columns = get_columns()
# 	data = get_data(filters)

# 	# If user selected a "color filter", apply it here
# 	if filters.get("color_filter"):
# 		data = [row for row in data if row["status"] == filters["color_filter"]]

# 	return columns, data


# def get_columns():
# 	return [
# 		{"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
# 		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
# 		{"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
# 		{"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
# 		{"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
# 		{"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
# 		{
# 			"label": "Balance Valuation",
# 			"fieldname": "balance_valuation",
# 			"fieldtype": "Currency",
# 			"width": 150,
# 		},
# 		{
# 			"label": "Excess Stock Valuation",
# 			"fieldname": "excess_stock_valuation",
# 			"fieldtype": "Currency",
# 			"width": 180,
# 		},
# 		{
# 			"label": "Open Indent",
# 			"fieldname": "open_indent",
# 			"fieldtype": "Float",
# 			"width": 120,
# 		},
# 		{
# 			"label": "Open PO",
# 			"fieldname": "open_po",
# 			"fieldtype": "Float",
# 			"width": 120,
# 		},
# 		{
# 			"label": "Open Transit",
# 			"fieldname": "open_transit",
# 			"fieldtype": "Float",
# 			"width": 120,
# 		},
# 		# hidden helper column
# 		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "hidden": 1},
# 	]


# def get_data(filters):
# 	flt_list = []
# 	if filters.get("custom_department"):
# 		flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
# 	if filters.get("item"):
# 		flt_list.append(["Item", "name", "=", filters["item"]])

# 	items = frappe.get_all(
# 		"Item",
# 		filters=flt_list,
# 		fields=[
# 			"name",
# 			"item_name",
# 			"stock_uom as uom",
# 			"custom_department",
# 			"custom_minimum_stock",
# 			"custom_maximum_stock",
# 		],
# 		order_by="item_name asc",
# 	)

# 	data = []
# 	for it in items:
# 		store_qty = (
# 			frappe.db.get_value("Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty") or 0
# 		)

# 		# Get stock value and valuation rate from Bin table
# 		bin_data = (
# 			frappe.db.get_value(
# 				"Bin",
# 				{"item_code": it.name, "warehouse": WAREHOUSE},
# 				["stock_value", "valuation_rate"],
# 				as_dict=True,
# 			)
# 			or {}
# 		)

# 		stock_value = bin_data.get("stock_value") or 0
# 		valuation_rate = bin_data.get("valuation_rate") or 0

# 		min_qty = it.custom_minimum_stock or 0
# 		max_qty = it.custom_maximum_stock or 0

# 		# Calculate excess stock valuation
# 		excess_stock_valuation = 0
# 		if store_qty > max_qty:
# 			excess_qty = store_qty - max_qty
# 			excess_stock_valuation = excess_qty * valuation_rate

# 		# Get open indent quantity (Material Requests not linked to PO)
# 		open_indent_qty = get_open_indent_quantity(it.name)

# 		# Get open PO quantity (Purchase Orders not yet received)
# 		open_po_qty = get_open_po_quantity(it.name)

# 		# Get open transit quantity (Items in transit)
# 		open_transit_qty = get_open_transit_quantity(it.name)

# 		# Determine status
# 		if store_qty < min_qty:
# 			status = "Red"
# 		elif min_qty <= store_qty <= max_qty:
# 			status = "Green"
# 		else:
# 			status = "Purple"

# 		data.append(
# 			{
# 				"custom_department": it.custom_department,
# 				"item_name": it.item_name,
# 				"uom": it.uom,
# 				"store_qty": store_qty,
# 				"custom_minimum_stock": min_qty,
# 				"custom_maximum_stock": max_qty,
# 				"balance_valuation": stock_value,
# 				"excess_stock_valuation": excess_stock_valuation,
# 				"open_indent": open_indent_qty,
# 				"open_po": open_po_qty,
# 				"open_transit": open_transit_qty,
# 				"status": status,  # hidden column for filtering
# 			}
# 		)
# 	return data


# def get_open_indent_quantity(item_code):
# 	"""
# 	Get open indent quantity for an item.
# 	Open indent = Material Requests that are NOT linked to any Purchase Order Item
# 	"""
# 	try:
# 		# Get all material request IDs that are linked to Purchase Order Items
# 		linked_mr_ids = frappe.db.sql(
# 			"""
# 			SELECT DISTINCT material_request
# 			FROM `tabPurchase Order Item`
# 			WHERE material_request IS NOT NULL AND material_request != ''
# 		""",
# 			as_list=True,
# 		)

# 		linked_mr_list = [row[0] for row in linked_mr_ids] if linked_mr_ids else []

# 		# Get open material requests (not linked to any PO)
# 		open_mr_conditions = ""
# 		if linked_mr_list:
# 			open_mr_conditions = f"AND mr.name NOT IN ({','.join(['%s'] * len(linked_mr_list))})"

# 		# Get quantities from open material requests for this item
# 		open_indent_qty = frappe.db.sql(
# 			f"""
# 			SELECT SUM(ifnull(mri.qty, 0))
# 			FROM `tabMaterial Request` mr
# 			INNER JOIN `tabMaterial Request Item` mri ON mr.name = mri.parent
# 			WHERE mr.docstatus = 1
# 			AND mr.status != 'Completed'
# 			AND mri.item_code = %s
# 			{open_mr_conditions}
# 		""",
# 			[item_code, *linked_mr_list],
# 			as_list=True,
# 		)

# 		return float(open_indent_qty[0][0] or 0) if open_indent_qty and open_indent_qty[0][0] else 0
# 	except Exception as e:
# 		frappe.log_error(f"Error getting open indent for {item_code}: {str(e)}")
# 		return 0


# def get_open_po_quantity(item_code):
# 	"""
# 	Get open PO quantity for an item.
# 	Open PO = Purchase Orders that don't have corresponding Purchase Receipts
# 	"""
# 	try:
# 		# Get quantities from Purchase Orders that don't have Purchase Receipts
# 		open_po_qty = frappe.db.sql(
# 			"""
# 			SELECT SUM(ifnull(poi.qty, 0))
# 			FROM `tabPurchase Order` po
# 			INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
# 			LEFT JOIN `tabPurchase Receipt Item` pri ON po.name = pri.purchase_order
# 			WHERE po.docstatus = 1
# 			AND po.status IN ('To Receive and Bill', 'To Bill', 'To Receive')
# 			AND poi.item_code = %s
# 			AND pri.purchase_order IS NULL
# 		""",
# 			[item_code],
# 			as_list=True,
# 		)

# 		return float(open_po_qty[0][0] or 0) if open_po_qty and open_po_qty[0][0] else 0
# 	except Exception as e:
# 		frappe.log_error(f"Error getting open PO for {item_code}: {str(e)}")
# 		return 0


# def get_open_transit_quantity(item_code):
# 	"""
# 	Get open transit quantity for an item.
# 	Open Transit = Items that are in transit (Material Transfer entries)
# 	"""
# 	try:
# 		# Get quantities from Stock Entries that are Material Transfers
# 		open_transit_qty = frappe.db.sql(
# 			"""
# 			SELECT SUM(ifnull(se_item.qty, 0))
# 			FROM `tabStock Entry` se
# 			INNER JOIN `tabStock Entry Detail` se_item ON se.name = se_item.parent
# 			WHERE se.docstatus = 1
# 			AND se.purpose = 'Material Transfer'
# 			AND se_item.item_code = %s
# 			AND se_item.t_warehouse = %s
# 		""",
# 			[item_code, WAREHOUSE],
# 			as_list=True,
# 		)

# 		return float(open_transit_qty[0][0] or 0) if open_transit_qty and open_transit_qty[0][0] else 0
# 	except Exception as e:
# 		frappe.log_error(f"Error getting open transit for {item_code}: {str(e)}")
# 		return 0

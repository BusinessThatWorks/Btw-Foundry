# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	columns = [
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{"fieldname": "actual_qty", "label": "Actual Qty", "fieldtype": "Float", "width": 100},
		{"fieldname": "required_bom_qty", "label": "Required BOM Qty", "fieldtype": "Float", "width": 130},
		{
			"fieldname": "custom_department",
			"label": "Department",
			"fieldtype": "Data",
			"width": 120,
		},
		{"fieldname": "open_indent", "label": "Open Indent", "fieldtype": "Float", "width": 100},
		{"fieldname": "open_po", "label": "Open PO", "fieldtype": "Float", "width": 100},
		{"fieldname": "combined_stock", "label": "Combined Stock", "fieldtype": "Float", "width": 120},
	]
	return columns


def get_data(filters):
	data = []

	# Require a Production Plan selection; without it, show no rows
	if not filters or not filters.get("production_plan"):
		return data

	# Build the base query
	query = """
		SELECT
			mrpi.item_code,
			mrpi.actual_qty,
			mrpi.required_bom_qty,
			i.custom_department,
			0 as open_indent,
			0 as open_po,
			0 as combined_stock
		FROM `tabProduction Plan` pp
		LEFT JOIN `tabMaterial Request Plan Item` mrpi ON pp.name = mrpi.parent
		LEFT JOIN `tabItem` i ON i.name = mrpi.item_code
		WHERE pp.docstatus != 2
	"""

	# Add filters if provided
	if filters:
		if filters.get("production_plan"):
			query += " AND pp.name = %(production_plan)s"
		if filters.get("item_code"):
			query += " AND mrpi.item_code = %(item_code)s"
		if filters.get("department"):
			query += " AND i.custom_department = %(department)s"

	query += " ORDER BY mrpi.item_code"

	data = frappe.db.sql(query, filters, as_dict=True)

	# Enrich each row with open indent and open PO like Inventory Management System
	for row in data:
		item_code = row.get("item_code")
		if not item_code:
			continue
		row["open_indent"] = get_open_indent_quantity(item_code)
		row["open_po"] = get_open_po_quantity(item_code)
		# Calculate combined stock as actual_qty + open_po + open_indent
		actual_qty = row.get("actual_qty") or 0
		open_po = row.get("open_po") or 0
		open_indent = row.get("open_indent") or 0
		row["combined_stock"] = actual_qty + open_po + open_indent
	return data


def get_open_indent_quantity(item_code):
	"""
	Get open indent quantity for an item.
	Open indent = Material Requests that are NOT linked to any Purchase Order Item
	"""
	try:
		# Get all material request IDs that are linked to Purchase Order Items
		linked_mr_ids = frappe.db.sql(
			"""
			SELECT DISTINCT material_request
			FROM `tabPurchase Order Item`
			WHERE material_request IS NOT NULL AND material_request != ''
		""",
			as_list=True,
		)

		linked_mr_list = [row[0] for row in linked_mr_ids] if linked_mr_ids else []

		# Get open material requests (not linked to any PO)
		open_mr_conditions = ""
		if linked_mr_list:
			open_mr_conditions = f"AND mr.name NOT IN ({','.join(['%s'] * len(linked_mr_list))})"

		# Get quantities from open material requests for this item
		open_indent_qty = frappe.db.sql(
			f"""
			SELECT SUM(ifnull(mri.qty, 0))
			FROM `tabMaterial Request` mr
			INNER JOIN `tabMaterial Request Item` mri ON mr.name = mri.parent
			WHERE mr.docstatus = 1
			AND mr.status != 'Completed'
			AND mri.item_code = %s
			{open_mr_conditions}
		""",
			[item_code, *linked_mr_list],
			as_list=True,
		)

		return float(open_indent_qty[0][0] or 0) if open_indent_qty and open_indent_qty[0][0] else 0
	except Exception as e:
		frappe.log_error(f"Error getting open indent for {item_code}: {str(e)}")
		return 0


def get_open_po_quantity(item_code):
	"""
	Get open PO quantity for an item.
	Open PO = Purchase Orders that don't have corresponding Purchase Receipts
	"""
	try:
		# Get quantities from Purchase Orders that don't have Purchase Receipts
		open_po_qty = frappe.db.sql(
			"""
			SELECT SUM(ifnull(poi.qty, 0))
			FROM `tabPurchase Order` po
			INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
			LEFT JOIN `tabPurchase Receipt Item` pri ON po.name = pri.purchase_order
			WHERE po.docstatus = 1
			AND po.status IN ('To Receive and Bill', 'To Bill', 'To Receive')
			AND poi.item_code = %s
			AND pri.purchase_order IS NULL
		""",
			[item_code],
			as_list=True,
		)

		return float(open_po_qty[0][0] or 0) if open_po_qty and open_po_qty[0][0] else 0
	except Exception as e:
		frappe.log_error(f"Error getting open PO for {item_code}: {str(e)}")
		return 0

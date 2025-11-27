# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
import re


def execute(filters=None):
	filters = filters or {}

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data


def sanitize_fieldname(name):
	"""Convert operation name to a valid fieldname"""
	# Replace spaces, hyphens, and special characters with underscores
	fieldname = re.sub(r"[^a-zA-Z0-9_]", "_", str(name))
	# Remove multiple consecutive underscores
	fieldname = re.sub(r"_+", "_", fieldname)
	# Remove leading/trailing underscores
	fieldname = fieldname.strip("_")
	# Ensure it starts with a letter or underscore
	if fieldname and not fieldname[0].isalpha() and fieldname[0] != "_":
		fieldname = f"op_{fieldname}"
	return fieldname or "operation"


def get_columns(filters):
	"""Get columns dynamically including operation columns"""
	columns = [
		{
			"label": "Sales Order ID",
			"fieldname": "sales_order_id",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150,
		},
		{
			"label": "Customer Name",
			"fieldname": "customer_name",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},
		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": "Qty Manufactured", "fieldname": "qty_manufactured", "fieldtype": "Float", "width": 120},
	]

	# Get all unique operations to create dynamic columns
	operations = get_all_operations(filters)

	# Add operation columns
	for operation in operations:
		fieldname = sanitize_fieldname(operation)
		columns.append({"label": operation, "fieldname": fieldname, "fieldtype": "Float", "width": 120})

	return columns


def get_all_operations(filters):
	"""Get all unique operation names from Work Order Operations"""
	conditions = get_conditions(filters)

	query = f"""
		SELECT DISTINCT woo.operation
		FROM `tabWork Order` wo
		INNER JOIN `tabWork Order Operation` woo ON woo.parent = wo.name
		INNER JOIN `tabSales Order` so ON so.name = wo.sales_order
		WHERE {conditions}
		AND wo.docstatus != 2
		AND woo.operation IS NOT NULL
		ORDER BY woo.operation
	"""

	operations = frappe.db.sql(query, filters, as_list=True)
	return [op[0] for op in operations]


def get_conditions(filters):
	"""Build WHERE conditions based on filters"""
	conditions = ["1=1"]

	if filters.get("sales_order_id"):
		conditions.append("so.name = %(sales_order_id)s")

	if filters.get("customer_name"):
		conditions.append("so.customer = %(customer_name)s")

	return " AND ".join(conditions)


def get_data(filters):
	"""Get report data"""
	conditions = get_conditions(filters)

	# Get all unique operations
	operations = get_all_operations(filters)
	operation_map = {op: sanitize_fieldname(op) for op in operations}

	# Main query to get Sales Order Items with Work Order data
	query = f"""
		SELECT
			so.name AS sales_order_id,
			so.customer AS customer_name,
			soi.item_code AS item_code,
			soi.item_name AS item_name,
			wo.name AS work_order,
			wo.production_item AS production_item,
			wo.qty AS qty_manufactured
		FROM
			`tabSales Order` so
		INNER JOIN
			`tabSales Order Item` soi ON soi.parent = so.name
		LEFT JOIN
			`tabWork Order` wo ON wo.sales_order = so.name
			AND wo.production_item = soi.item_code
			AND wo.docstatus != 2
		WHERE {conditions}
		ORDER BY so.name, soi.item_code, wo.name
	"""

	rows = frappe.db.sql(query, filters, as_dict=True)

	# Get operations data for each work order
	work_order_operations = get_work_order_operations(filters)

	# Group data by sales_order_id, item_code
	grouped_data = {}

	for row in rows:
		key = f"{row.sales_order_id}||{row.item_code}"

		if key not in grouped_data:
			grouped_data[key] = {
				"sales_order_id": row.sales_order_id,
				"customer_name": row.customer_name,
				"item_name": row.item_name,
				"qty_manufactured": 0,
			}
			# Initialize all operation columns to 0
			for op in operations:
				grouped_data[key][operation_map[op]] = 0

		# Sum up qty_manufactured
		if row.qty_manufactured:
			grouped_data[key]["qty_manufactured"] += row.qty_manufactured

		# Add operation completed_qty if work order exists
		if row.work_order and row.work_order in work_order_operations:
			for op_data in work_order_operations[row.work_order]:
				op_name = op_data.get("operation")
				if op_name in operation_map:
					fieldname = operation_map[op_name]
					completed_qty = op_data.get("completed_qty", 0) or 0
					grouped_data[key][fieldname] += completed_qty

	# Convert to list
	data = list(grouped_data.values())

	return data


def get_work_order_operations(filters):
	"""Get all work order operations grouped by work order"""
	conditions = get_conditions(filters)

	query = f"""
		SELECT
			wo.name AS work_order,
			woo.operation,
			woo.completed_qty
		FROM
			`tabWork Order` wo
		INNER JOIN
			`tabWork Order Operation` woo ON woo.parent = wo.name
		INNER JOIN
			`tabSales Order` so ON so.name = wo.sales_order
		WHERE {conditions}
		AND wo.docstatus != 2
		AND woo.operation IS NOT NULL
		ORDER BY wo.name, woo.idx
	"""

	rows = frappe.db.sql(query, filters, as_dict=True)

	# Group by work_order
	work_order_ops = {}
	for row in rows:
		wo_name = row.work_order
		if wo_name not in work_order_ops:
			work_order_ops[wo_name] = []
		work_order_ops[wo_name].append({"operation": row.operation, "completed_qty": row.completed_qty})

	return work_order_ops

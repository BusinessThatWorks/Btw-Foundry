# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	filters = filters or {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	"""Get fixed columns for the report"""
	return [
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
		{
			"label": "Work Order",
			"fieldname": "work_order",
			"fieldtype": "Link",
			"options": "Work Order",
			"width": 150,
		},
		{"label": "Operation", "fieldname": "operation", "fieldtype": "Data", "width": 150},
		{"label": "Planned Qty", "fieldname": "planned_qty", "fieldtype": "Float", "width": 120},
		{"label": "Completed Qty", "fieldname": "completed_qty", "fieldtype": "Float", "width": 120},
		{"label": "Pending Qty", "fieldname": "pending_qty", "fieldtype": "Float", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
	]


def get_conditions(filters):
	"""Build WHERE conditions based on filters"""
	conditions = ["1=1"]

	if filters.get("sales_order_id"):
		conditions.append("so.name = %(sales_order_id)s")

	if filters.get("customer_name"):
		conditions.append("so.customer = %(customer_name)s")

	if filters.get("status"):
		# We'll filter status after data is fetched since it's calculated
		pass

	return " AND ".join(conditions)


def get_data(filters):
	"""Get report data - one row per Sales Order + Item + Work Order + Operation"""
	conditions = get_conditions(filters)

	# Main query to get Sales Order Items with Work Order and Operation data
	query = f"""
		SELECT
			so.name AS sales_order_id,
			so.customer AS customer_name,
			soi.item_code AS item_code,
			soi.item_name AS item_name,
			wo.name AS work_order,
			wo.qty AS planned_qty,
			woo.operation AS operation,
			COALESCE(woo.completed_qty, 0) AS completed_qty
		FROM
			`tabSales Order` so
		INNER JOIN
			`tabSales Order Item` soi ON soi.parent = so.name
		INNER JOIN
			`tabWork Order` wo ON wo.sales_order = so.name
			AND wo.production_item = soi.item_code
			AND wo.docstatus != 2
		INNER JOIN
			`tabWork Order Operation` woo ON woo.parent = wo.name
		WHERE {conditions}
		AND woo.operation IS NOT NULL
		ORDER BY so.name, soi.item_code, wo.name, woo.idx
	"""

	rows = frappe.db.sql(query, filters, as_dict=True)

	# Process rows to calculate pending qty and status
	data = []
	for row in rows:
		planned_qty = row.get("planned_qty", 0) or 0
		completed_qty = row.get("completed_qty", 0) or 0
		pending_qty = planned_qty - completed_qty

		# Determine status based on pending and completed qty
		if pending_qty == 0:
			status = "Completed"
		elif completed_qty == 0 and pending_qty > 0:
			status = "Not Started"
		else:
			status = "Pending"

		data_row = {
			"sales_order_id": row.get("sales_order_id"),
			"customer_name": row.get("customer_name"),
			"item_name": row.get("item_name"),
			"work_order": row.get("work_order"),
			"operation": row.get("operation"),
			"planned_qty": planned_qty,
			"completed_qty": completed_qty,
			"pending_qty": pending_qty,
			"status": status,
		}

		# Apply status filter if provided
		if filters.get("status"):
			if data_row["status"] != filters.get("status"):
				continue

		data.append(data_row)

	return data

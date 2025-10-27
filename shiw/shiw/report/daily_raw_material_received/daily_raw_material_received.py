# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt
# will deploy tomorrow
import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# Script Report: Raw Material Receipts


# def execute(filters=None):
# 	columns = [
# 		{
# 			"label": "ID",
# 			"fieldname": "purchase_receipt",
# 			"fieldtype": "Link",
# 			"options": "Purchase Receipt",
# 			"width": 120,
# 		},
# 		{
# 			"label": "Purchase Order",
# 			"fieldname": "purchase_order",
# 			"fieldtype": "Link",
# 			"options": "Purchase Order",
# 			"width": 150,
# 		},
# 		{
# 			"label": "Supplier",
# 			"fieldname": "supplier",
# 			"fieldtype": "Link",
# 			"options": "Supplier",
# 			"width": 150,
# 		},
# 		{"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
# 		{
# 			"label": "Item Group",
# 			"fieldname": "item_group",
# 			"fieldtype": "Link",
# 			"options": "Item Group",
# 			"width": 130,
# 		},
# 		{"label": "Accepted Quantity", "fieldname": "accepted_qty", "fieldtype": "Float", "width": 130},
# 		{"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 100},
# 		{"label": "Rejected Quantity", "fieldname": "rejected_qty", "fieldtype": "Float", "width": 130},
# 	]

# 	conditions = ""
# 	values = {}

# 	if filters.get("from_date"):
# 		conditions += " AND pr.posting_date >= %(from_date)s"
# 		values["from_date"] = filters["from_date"]

# 	if filters.get("to_date"):
# 		conditions += " AND pr.posting_date <= %(to_date)s"
# 		values["to_date"] = filters["to_date"]

# 	if filters.get("purchase_receipt"):
# 		conditions += " AND pr.name = %(purchase_receipt)s"
# 		values["purchase_receipt"] = filters["purchase_receipt"]

# 	if filters.get("supplier"):
# 		conditions += " AND pr.supplier = %(supplier)s"
# 		values["supplier"] = filters["supplier"]

# 	if filters.get("item_code"):
# 		conditions += " AND pri.item_code = %(item_code)s"
# 		values["item_code"] = filters["item_code"]

# 	if filters.get("item_group"):
# 		conditions += " AND i.item_group = %(item_group)s"
# 		values["item_group"] = filters["item_group"]

# 	data = frappe.db.sql(
# 		f"""
#         SELECT
#             pr.name AS purchase_receipt,
#             pri.purchase_order AS purchase_order,
#             pr.supplier AS supplier,
#             pri.item_code AS item_code,
#             i.item_group AS item_group,
#             pri.qty AS accepted_qty,
#             pri.rejected_qty AS rejected_qty,
#             pri.amount AS amount
#         FROM
#             `tabPurchase Receipt` pr
#         JOIN
#             `tabPurchase Receipt Item` pri ON pr.name = pri.parent
#         JOIN
#             `tabItem` i ON pri.item_code = i.name
#         WHERE
#             i.item_group = 'Raw Material'
#             AND pri.qty >= 0
#             {conditions}
#         ORDER BY
#             pr.posting_date DESC
#     """,
# 		values,
# 		as_dict=True,
# 	)

# 	return columns, data

# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	filters = filters or {}

# 	columns = get_columns()
# 	data = get_data(filters)

# 	return columns, data


# def get_columns():
# 	return [
# 		{
# 			"label": "Material Request",
# 			"fieldname": "material_request",
# 			"fieldtype": "Link",
# 			"options": "Material Request",
# 			"width": 150,
# 		},
# 		{"label": "Indent Date", "fieldname": "indent_date", "fieldtype": "Date", "width": 100},
# 		{"label": "MR Status", "fieldname": "mr_status", "fieldtype": "Data", "width": 100},
# 		{
# 			"label": "Item Code",
# 			"fieldname": "item_code",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 180},
# 		{"label": "Requested Qty", "fieldname": "requested_qty", "fieldtype": "Float", "width": 120},
# 		{"label": "UOM", "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 80},
# 		{
# 			"label": "Purchase Order",
# 			"fieldname": "purchase_order",
# 			"fieldtype": "Link",
# 			"options": "Purchase Order",
# 			"width": 150,
# 		},
# 		{"label": "PO Status", "fieldname": "po_status", "fieldtype": "Data", "width": 100},
# 		{"label": "Ordered Qty", "fieldname": "ordered_qty", "fieldtype": "Float", "width": 120},
# 		{"label": "PO UOM", "fieldname": "po_uom", "fieldtype": "Link", "options": "UOM", "width": 80},
# 		{"label": "PO Rate", "fieldname": "po_rate", "fieldtype": "Currency", "width": 120},
# 		{"label": "Discount", "fieldname": "discount", "fieldtype": "Currency", "width": 120},
# 		{"label": "Item Amount", "fieldname": "item_amount", "fieldtype": "Currency", "width": 120},
# 		{
# 			"label": "Supplier",
# 			"fieldname": "supplier",
# 			"fieldtype": "Link",
# 			"options": "Supplier",
# 			"width": 150,
# 		},
# 		{"label": "PO Date", "fieldname": "po_date", "fieldtype": "Date", "width": 100},
# 		{"label": "Required By", "fieldname": "required_by", "fieldtype": "Date", "width": 100},
# 		{"label": "PO Grand Total", "fieldname": "po_grand_total", "fieldtype": "Currency", "width": 150},
# 		{
# 			"label": "Purchase Receipt",
# 			"fieldname": "purchase_receipt",
# 			"fieldtype": "Link",
# 			"options": "Purchase Receipt",
# 			"width": 150,
# 		},
# 		{"label": "Received Qty", "fieldname": "received_qty", "fieldtype": "Float", "width": 120},
# 		{"label": "Receipt Date", "fieldname": "receipt_date", "fieldtype": "Date", "width": 100},
# 		{"label": "PR Grand Total", "fieldname": "pr_grand_total", "fieldtype": "Currency", "width": 150},
# 		{
# 			"label": "Purchase Invoice",
# 			"fieldname": "purchase_invoice",
# 			"fieldtype": "Link",
# 			"options": "Purchase Invoice",
# 			"width": 150,
# 		},
# 		{"label": "PI Status", "fieldname": "pi_status", "fieldtype": "Data", "width": 100},
# 		{"label": "PI ID", "fieldname": "purchase_invoice", "fieldtype": "Data", "width": 120},
# 		{"label": "Invoiced Qty", "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 120},
# 		{"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
# 	]


# def get_data(filters):
# 	conditions = """
#         mr.docstatus = 1
#         AND mr.transaction_date BETWEEN %(from_date)s AND %(to_date)s
#     """

# 	if filters.get("item_code"):
# 		conditions += " AND mri.item_code = %(item_code)s"

# 	# Main query for Material Request chain
# 	main_query = f"""
#         SELECT
#             mr.name AS material_request,
#             mr.transaction_date AS indent_date,
#             mr.workflow_state AS mr_status,

#             mri.item_code,
#             mri.item_name,
#             mri.qty AS requested_qty,
#             mri.uom,

#             po.name AS purchase_order,
#             po.workflow_state AS po_status,
#             poi.qty AS ordered_qty,
#             poi.uom AS po_uom,
#             poi.rate AS po_rate,
#             poi.discount_amount AS discount,
#             poi.amount AS item_amount,
#             po.supplier,
#             po.transaction_date AS po_date,
#             po.schedule_date AS required_by,
#             po.grand_total AS po_grand_total,

#             pr.name AS purchase_receipt,
#             pri.qty AS received_qty,
#             pr.posting_date AS receipt_date,
#             pr.grand_total AS pr_grand_total,

#             pi.name AS purchase_invoice,
#             pi.workflow_state AS pi_status,
#             pii.qty AS invoiced_qty,
#             pi.posting_date AS invoice_date

#         FROM
#             `tabMaterial Request` mr
#         LEFT JOIN
#             `tabMaterial Request Item` mri ON mri.parent = mr.name
#         LEFT JOIN
#             `tabPurchase Order Item` poi
#                 ON poi.material_request_item = mri.name
#                 AND EXISTS (
#                     SELECT 1
#                     FROM `tabPurchase Order` po_sub
#                     WHERE po_sub.name = poi.parent
#                     AND po_sub.docstatus = 1
#                     AND po_sub.workflow_state != 'Cancelled'
#                 )
#         LEFT JOIN
#             `tabPurchase Order` po
#                 ON po.name = poi.parent
#                 AND po.docstatus = 1
#                 AND po.workflow_state != 'Cancelled'
#         LEFT JOIN
#             `tabPurchase Receipt Item` pri ON pri.purchase_order_item = poi.name
#         LEFT JOIN
#             `tabPurchase Receipt` pr ON pr.name = pri.parent AND pr.docstatus = 1
#         LEFT JOIN
#             `tabPurchase Invoice Item` pii
#                 ON (pii.purchase_order = po.name OR pii.purchase_receipt = pr.name)
#         LEFT JOIN
#             `tabPurchase Invoice` pi ON pi.name = pii.parent AND pi.docstatus = 1

#         WHERE {conditions}
#         ORDER BY mr.name, mri.item_code
#     """

# 	# Query for ALL Purchase Invoices within date range (regardless of links)
# 	pi_conditions = """
#         pi.docstatus = 1
#         AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
#     """

# 	if filters.get("item_code"):
# 		pi_conditions += " AND pii.item_code = %(item_code)s"

# 	pi_query = f"""
#         SELECT
#             mr.name AS material_request,
#             mr.transaction_date AS indent_date,
#             mr.workflow_state AS mr_status,

#             pii.item_code,
#             pii.item_name,
#             pii.qty AS requested_qty,
#             pii.uom,

#             po.name AS purchase_order,
#             po.workflow_state AS po_status,
#             pii.qty AS ordered_qty,
#             pii.uom AS po_uom,
#             pii.rate AS po_rate,
#             pii.discount_amount AS discount,
#             pii.amount AS item_amount,
#             pi.supplier,
#             pi.posting_date AS po_date,
#             po.schedule_date AS required_by,
#             pi.grand_total AS po_grand_total,

#             pr.name AS purchase_receipt,
#             pri.qty AS received_qty,
#             pr.posting_date AS receipt_date,
#             pr.grand_total AS pr_grand_total,

#             pi.name AS purchase_invoice,
#             pi.workflow_state AS pi_status,
#             pii.qty AS invoiced_qty,
#             pi.posting_date AS invoice_date

#         FROM
#             `tabPurchase Invoice` pi
#         LEFT JOIN
#             `tabPurchase Invoice Item` pii ON pii.parent = pi.name
#         LEFT JOIN
#             `tabPurchase Receipt` pr ON pr.name = pii.purchase_receipt
#         LEFT JOIN
#             `tabPurchase Receipt Item` pri ON pri.parent = pr.name AND pri.item_code = pii.item_code
#         LEFT JOIN
#             `tabPurchase Order Item` poi ON poi.name = pri.purchase_order_item
#         LEFT JOIN
#             `tabPurchase Order` po ON po.name = poi.parent
#         LEFT JOIN
#             `tabMaterial Request Item` mri ON mri.name = poi.material_request_item
#         LEFT JOIN
#             `tabMaterial Request` mr ON mr.name = mri.parent
#         WHERE {pi_conditions}
#         ORDER BY pi.name, pii.item_code
#     """

# 	# Execute both queries and combine results
# 	main_data = frappe.db.sql(main_query, filters, as_dict=True)
# 	pi_data = frappe.db.sql(pi_query, filters, as_dict=True)

# 	# Always get ALL Purchase Invoices to ensure they show up (simplified)
# 	all_pi_query = """
# 		SELECT
# 			NULL AS material_request,
# 			NULL AS indent_date,
# 			NULL AS mr_status,

# 			pii.item_code,
# 			pii.item_name,
# 			pii.qty AS requested_qty,
# 			pii.uom,

# 			po.name AS purchase_order,
# 			po.workflow_state AS po_status,
# 			pii.qty AS ordered_qty,
# 			pii.uom AS po_uom,
# 			pii.rate AS po_rate,
# 			pii.discount_amount AS discount,
# 			pii.amount AS item_amount,
# 			pi.supplier,
# 			pi.posting_date AS po_date,
# 			NULL AS required_by,
# 			pi.grand_total AS po_grand_total,

# 			pr.name AS purchase_receipt,
# 			NULL AS received_qty,
# 			pr.posting_date AS receipt_date,
# 			pr.grand_total AS pr_grand_total,

# 			pi.name AS purchase_invoice,
# 			pi.workflow_state AS pi_status,
# 			pii.qty AS invoiced_qty,
# 			pi.posting_date AS invoice_date

# 		FROM
# 			`tabPurchase Invoice` pi
# 		LEFT JOIN
# 			`tabPurchase Invoice Item` pii ON pii.parent = pi.name
# 		LEFT JOIN
# 			`tabPurchase Receipt` pr ON pr.name = pii.purchase_receipt
# 		LEFT JOIN
# 			`tabPurchase Order` po ON po.name = pii.purchase_order
# 		WHERE pi.docstatus = 1
# 		AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
# 		ORDER BY pi.name, pii.item_code
# 	"""
# 	all_pi_data = frappe.db.sql(all_pi_query, filters, as_dict=True)

# 	# Combine with existing pi_data
# 	pi_data = pi_data + all_pi_data

# 	# Remove duplicates based on purchase_invoice name
# 	seen_pis = set()
# 	unique_pi_data = []
# 	for row in pi_data:
# 		if row["purchase_invoice"] and row["purchase_invoice"] not in seen_pis:
# 			seen_pis.add(row["purchase_invoice"])
# 			unique_pi_data.append(row)

# 	# Combine results
# 	all_data = main_data + unique_pi_data

# 	return all_data


import frappe


def execute(filters=None):
	filters = filters or {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		{
			"label": "Material Request",
			"fieldname": "material_request",
			"fieldtype": "Link",
			"options": "Material Request",
			"width": 150,
		},
		{"label": "Indent Date", "fieldname": "indent_date", "fieldtype": "Date", "width": 100},
		{"label": "MR Status", "fieldname": "mr_status", "fieldtype": "Data", "width": 100},
		{
			"label": "Item Code",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 180},
		{"label": "Requested Qty", "fieldname": "requested_qty", "fieldtype": "Float", "width": 120},
		{"label": "UOM", "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 80},
		{
			"label": "Purchase Order",
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 150,
		},
		{"label": "PO Workflow State", "fieldname": "po_status", "fieldtype": "Data", "width": 140},
		{"label": "PO Status", "fieldname": "po_doc_status", "fieldtype": "Data", "width": 120},
		{"label": "Ordered Qty", "fieldname": "ordered_qty", "fieldtype": "Float", "width": 120},
		{"label": "PO UOM", "fieldname": "po_uom", "fieldtype": "Link", "options": "UOM", "width": 80},
		{"label": "PO Rate", "fieldname": "po_rate", "fieldtype": "Currency", "width": 120},
		{"label": "Discount", "fieldname": "discount", "fieldtype": "Currency", "width": 120},
		{"label": "Item Amount", "fieldname": "item_amount", "fieldtype": "Currency", "width": 120},
		{
			"label": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 150,
		},
		{"label": "PO Date", "fieldname": "po_date", "fieldtype": "Date", "width": 100},
		{"label": "Required By", "fieldname": "required_by", "fieldtype": "Date", "width": 100},
		{"label": "PO Grand Total", "fieldname": "po_grand_total", "fieldtype": "Currency", "width": 150},
		{
			"label": "Purchase Receipt",
			"fieldname": "purchase_receipt",
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 150,
		},
		{"label": "Received Qty", "fieldname": "received_qty", "fieldtype": "Float", "width": 120},
		{"label": "Receipt Date", "fieldname": "receipt_date", "fieldtype": "Date", "width": 100},
		{
			"label": "Purchase Invoice",
			"fieldname": "purchase_invoice",
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 150,
		},
		{"label": "Invoiced Qty", "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 120},
		{"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
	]


def get_data(filters):
	conditions = """
        mr.docstatus = 1
        AND mr.transaction_date BETWEEN %(from_date)s AND %(to_date)s
    """

	if filters.get("item_code"):
		conditions += " AND mri.item_code = %(item_code)s"

	query = f"""
        SELECT
            mr.name AS material_request,
            mr.transaction_date AS indent_date,
            mr.status AS mr_status,

            mri.item_code,
            mri.item_name,
            mri.qty AS requested_qty,
            mri.uom,

            po.name AS purchase_order,
            po.workflow_state AS po_status,
            po.status AS po_doc_status,
            poi.qty AS ordered_qty,
            poi.uom AS po_uom,
            poi.rate AS po_rate,
            poi.discount_amount AS discount,
            poi.amount AS item_amount,
            po.supplier,
            po.transaction_date AS po_date,
            po.schedule_date AS required_by,
            po.grand_total AS po_grand_total,

            pr.name AS purchase_receipt,
            pri.qty AS received_qty,
            pr.posting_date AS receipt_date,

            pi.name AS purchase_invoice,
            pii.qty AS invoiced_qty,
            pi.posting_date AS invoice_date

        FROM
            `tabMaterial Request` mr
        LEFT JOIN
            `tabMaterial Request Item` mri ON mri.parent = mr.name
        LEFT JOIN
            `tabPurchase Order Item` poi 
                ON poi.material_request_item = mri.name
                AND EXISTS (
                    SELECT 1 
                    FROM `tabPurchase Order` po_sub 
                    WHERE po_sub.name = poi.parent 
                    AND po_sub.docstatus = 1 
                    AND po_sub.workflow_state != 'Cancelled'
                )
        LEFT JOIN
            `tabPurchase Order` po 
                ON po.name = poi.parent 
                AND po.docstatus = 1 
                AND po.workflow_state != 'Cancelled'
        LEFT JOIN
            `tabPurchase Receipt Item` pri ON pri.purchase_order_item = poi.name
        LEFT JOIN
            `tabPurchase Receipt` pr ON pr.name = pri.parent AND pr.docstatus = 1
        LEFT JOIN
            `tabPurchase Invoice Item` pii ON pii.purchase_receipt = pr.name
                AND pii.item_code = pri.item_code
                AND pii.docstatus = 1
        LEFT JOIN
            `tabPurchase Invoice` pi ON pi.name = pii.parent AND pi.docstatus = 1

        WHERE {conditions}

        ORDER BY mr.name, mri.item_code
    """

	return frappe.db.sql(query, filters, as_dict=True)

# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters=None):
	base = [
		{
			"label": "Sales Order ID",
			"fieldname": "sales_order_id",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150,
		},
		{"label": "Creation Date", "fieldname": "transaction_date", "fieldtype": "Date", "width": 120},
		{"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date", "width": 120},
		{
			"label": "Item Name",
			"fieldname": "item_name",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
		{
			"label": "Default Tooling",
			"fieldname": "default_tooling",
			"fieldtype": "Link",
			"options": "New Tooling",
			"width": 150,
		},
		{
			"label": "Pattern ID",
			"fieldname": "pattern_id",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": "Cavity",
			"fieldname": "cavity",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": "Moulding System",
			"fieldname": "moulding_system",
			"fieldtype": "Link",
			"options": "Mould Master",
			"width": 150,
		},
		{
			"label": "Mould No",
			"fieldname": "mould_no",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": "Mould Time",
			"fieldname": "mould_time",
			"fieldtype": "Float",
			"width": 120,
		},
	]

	return base


def get_data(filters):
	data = []

	try:
		# Normalize and enforce date range defaults to current month
		from frappe.utils import today, get_first_day, get_last_day, getdate

		filters = filters or {}
		fd = filters.get("from_date")
		td = filters.get("to_date")
		if not fd or not td:
			cur = today()
			fd = fd or get_first_day(cur)
			td = td or get_last_day(cur)
		# Convert to date strings and normalize optional exact filters
		filters["from_date"] = str(getdate(fd))
		filters["to_date"] = str(getdate(td))
		if filters.get("sales_order"):
			filters["sales_order"] = str(filters.get("sales_order")).strip()
		if filters.get("item_code"):
			filters["item_code"] = str(filters.get("item_code")).strip()

		# Build the SQL query to join Sales Order, Sales Order Item, Item, and Grade Master tables
		query = """
            SELECT 
                so.name AS sales_order_id,
                so.transaction_date,
                so.delivery_date,
                soi.item_code AS item_name,
                soi.qty
            FROM `tabSales Order` so
            INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
            INNER JOIN `tabItem` i ON i.name = soi.item_code
            LEFT JOIN `tabGrade Master` gm ON gm.name = i.custom_grade_
            WHERE so.docstatus = 1
        """

		# Always constrain by date range
		query += " AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s"
		# Optional filters
		if filters.get("sales_order"):
			query += " AND so.name = %(sales_order)s"
		if filters.get("item_code"):
			query += " AND soi.item_code = %(item_code)s"

		query += " ORDER BY so.name, soi.idx"

		# Execute the query
		data = frappe.db.sql(query, filters, as_dict=True)

		# Convert None values to 0 for numeric fields and enrich with tooling data
		for row in data:
			row["qty"] = row["qty"] or 0

			# Initialize new fields
			row["default_tooling"] = None
			row["pattern_id"] = None
			row["cavity"] = None
			row["moulding_system"] = None
			row["mould_no"] = 0.0
			row["mould_time"] = 0.0

			# Get item code
			item_code = row.get("item_name")
			if not item_code:
				continue

			# Get custom_default_tooling from Item
			default_tooling_id = frappe.db.get_value("Item", item_code, "custom_default_tooling")
			if not default_tooling_id:
				continue

			row["default_tooling"] = default_tooling_id

			# Get New Tooling document
			try:
				tooling_doc = frappe.get_doc("New Tooling", default_tooling_id)
			except Exception:
				continue

			# Get moulding_system from New Tooling
			moulding_system_id = tooling_doc.get("moulding_system")
			row["moulding_system"] = moulding_system_id

			# Get cycle_time_to_create_1_mould from Mould Master
			cycle_time = 0.0
			if moulding_system_id:
				cycle_time = (
					frappe.db.get_value("Mould Master", moulding_system_id, "cycle_time_to_create_1_mould")
					or 0.0
				)

			# Helper function to extract item name from pattern item format
			# Format: "PTRN - Cast Steel Sp. Bearing Plate-9799 (9628) - 01455"
			# Extract: "Cast Steel Sp. Bearing Plate-9799 (9628)"
			# This matches the logic used in pouring.py
			def extract_item_name_from_pattern(pattern_item_name):
				if not pattern_item_name:
					return ""
				# Remove "PTRN - " prefix and extract item name before last " - "
				item_name = (pattern_item_name or "").replace("PTRN - ", "").rsplit("-", 1)[0].strip()
				return item_name

			# Find matching row in details_table
			# The item_code from Sales Order Item should match the extracted pattern item name
			matched_row = None
			debug_info = []  # For debugging

			for detail_row in tooling_doc.details_table:
				pattern_item_doc_name = detail_row.get("item") or ""

				# First, try to extract item name from the pattern document name
				pattern_item_extracted = extract_item_name_from_pattern(pattern_item_doc_name)

				# Also get the actual item_name from the New Pattern Manufacturing Details document
				# This is more reliable as it's the direct link to Item
				pattern_item_name_from_doc = None
				if pattern_item_doc_name:
					try:
						pattern_item_name_from_doc = frappe.db.get_value(
							"New Pattern Manufacturing Details", pattern_item_doc_name, "item_name"
						)
					except Exception:
						pass

				# Debug logging
				debug_info.append(
					{
						"pattern_doc": pattern_item_doc_name,
						"extracted": pattern_item_extracted,
						"item_name_from_doc": pattern_item_name_from_doc,
					}
				)

				# Match with the item_code from Sales Order Item
				# Try both the extracted name and the direct item_name field
				if pattern_item_extracted == item_code or pattern_item_name_from_doc == item_code:
					matched_row = detail_row
					break

			# Log debug info if no match found (for troubleshooting)
			if not matched_row and default_tooling_id:
				frappe.log_error(
					f"Mould Capacity Planning: No match found for item '{item_code}' in tooling '{default_tooling_id}'. "
					f"Debug info: {debug_info}",
					"Mould Capacity Planning Debug",
				)

			if matched_row:
				# Get cavity and pattern_id from matched row
				cavity = matched_row.get("cavity")
				pattern_id = matched_row.get("pattern_id")

				row["cavity"] = int(cavity) if cavity else None
				row["pattern_id"] = pattern_id

				# Calculate mould_no and mould_time
				if cavity and float(cavity) > 0:
					qty = float(row["qty"]) or 0.0
					mould_no = qty / float(cavity)
					row["mould_no"] = mould_no

					# Calculate mould_time = (qty / cavity) * cycle_time_to_create_1_mould
					if cycle_time > 0:
						row["mould_time"] = mould_no * float(cycle_time)

		# Subtotals per Sales Order
		grouped = []
		current_so = None
		acc = {}

		def add_subtotal_row(so_id, acc_vals):
			if not so_id:
				return
			row = {k: None for k in (data[0].keys() if data else [])}
			row["sales_order_id"] = f"Total for {so_id}"
			for key in [
				"qty",
				"mould_no",
				"mould_time",
			]:
				if key in acc_vals:
					row[key] = acc_vals.get(key, 0.0)
			row["bold"] = 1
			grouped.append(row)

		for r in data:
			so = r.get("sales_order_id")
			if current_so is None:
				current_so = so
			elif so != current_so:
				add_subtotal_row(current_so, acc)
				acc = {}
				current_so = so
			grouped.append(r)
			for key in [
				"qty",
				"mould_no",
				"mould_time",
			]:
				if key in r and isinstance(r.get(key), (int, float)):
					acc[key] = acc.get(key, 0.0) + float(r.get(key) or 0.0)

		add_subtotal_row(current_so, acc)
		data = grouped

		frappe.log_error(
			f"Mould Capacity Planning: Retrieved {len(data)} records", "Mould Capacity Planning Report"
		)

	except Exception as e:
		frappe.log_error(f"Error in Mould Capacity Planning: {str(e)}", "Mould Capacity Planning Error")
		frappe.msgprint(f"Error generating report: {str(e)}")

	return data

# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
	if not filters:
		filters = {}

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	item_filter = filters.get("item_name")

	# Get all rejection reasons - we'll populate this dynamically from actual data
	rejection_reasons = []

	# Dictionary to store item-wise rejection data
	# Structure: {item_name: {rejection_reason: total_quantity}}
	item_rejection_data = {}

	# Get all unique items from both rejection types within date range
	all_items = set()

	# FIRST LINE REJECTIONS
	first_line_docs = frappe.get_all(
		"First Line Rejection",
		filters={"docstatus": 1, "date": ["between", [from_date, to_date]]},
		fields=["name"],
	)

	for doc in first_line_docs:
		child_rows = frappe.get_all(
			"First Line Inspection Report",
			filters={"parent": doc.name},
			fields=["item_name", "rejection", "total_cast_weight"],
		)
		for row in child_rows:
			item_name = row.item_name
			rejection_reason = row.rejection
			weight = row.total_cast_weight or 0

			all_items.add(item_name)

			if item_name not in item_rejection_data:
				item_rejection_data[item_name] = {}

			if rejection_reason not in item_rejection_data[item_name]:
				item_rejection_data[item_name][rejection_reason] = 0

			item_rejection_data[item_name][rejection_reason] += weight

	# SECOND LINE REJECTIONS
	second_line_docs = frappe.get_all(
		"Second Line Rejection",
		filters={"docstatus": 1, "date": ["between", [from_date, to_date]]},
		fields=["name"],
	)

	for doc in second_line_docs:
		child_rows = frappe.get_all(
			"Second Line Rejection Table",
			filters={"parent": doc.name},
			fields=["item_name", "rejection_reason", "rejected_qty", "cast_weight_in_kg"],
		)
		for row in child_rows:
			item_name = row.item_name
			rejection_reason = row.rejection_reason
			rejected_qty = row.rejected_qty or 0
			cast_weight_per_pc = row.cast_weight_in_kg or 0
			# Calculate total weight: cast_weight_in_kg * rejected_qty
			total_weight = cast_weight_per_pc * rejected_qty

			all_items.add(item_name)

			if item_name not in item_rejection_data:
				item_rejection_data[item_name] = {}

			if rejection_reason not in item_rejection_data[item_name]:
				item_rejection_data[item_name][rejection_reason] = 0

			item_rejection_data[item_name][rejection_reason] += total_weight

	# Get all unique rejection reasons from actual data that have non-zero values
	actual_reasons_found = set()
	for item_data in item_rejection_data.values():
		for reason, weight in item_data.items():
			if weight > 0:  # Only include reasons with actual weight impact
				actual_reasons_found.add(reason)

	# Use only the rejection reasons that actually have weight impact
	rejection_reasons = sorted(actual_reasons_found)

	# Prepare data for report
	data = []

	# Calculate total weight first to use for percentage calculation
	total_weight_all_items = 0
	for item_name in sorted(all_items):
		# Apply item filter if specified
		if item_filter and item_name != item_filter:
			continue

		item_total = 0
		for reason in rejection_reasons:
			quantity = item_rejection_data.get(item_name, {}).get(reason, 0)
			item_total += quantity
		total_weight_all_items += item_total

	# Add item rows
	for item_name in sorted(all_items):
		# Apply item filter if specified
		if item_filter and item_name != item_filter:
			continue

		row = {"item_name": item_name}

		# Add total rejected quantity for this item
		total_rejected = 0
		for reason in rejection_reasons:
			quantity = item_rejection_data.get(item_name, {}).get(reason, 0)
			row[reason] = quantity
			total_rejected += quantity

		row["total_rejected"] = total_rejected

		# Calculate percentage: (item_total / total_weight_all_items) * 100
		if total_weight_all_items > 0:
			percentage = (total_rejected / total_weight_all_items) * 100
		else:
			percentage = 0
		row["percentage"] = round(percentage, 2)

		data.append(row)

	# Prepare columns
	columns = [
		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 200}
	]

	# Add columns for each rejection reason
	for reason in rejection_reasons:
		columns.append(
			{"label": reason, "fieldname": reason, "fieldtype": "Float", "width": 120, "precision": 2}
		)

	# Add total column
	columns.append(
		{
			"label": "Total Rejected Weight (Kg)",
			"fieldname": "total_rejected",
			"fieldtype": "Float",
			"width": 150,
			"precision": 2,
		}
	)

	# Add percentage column
	columns.append(
		{
			"label": "Percentage (%)",
			"fieldname": "percentage",
			"fieldtype": "Float",
			"width": 120,
			"precision": 2,
		}
	)

	return columns, data

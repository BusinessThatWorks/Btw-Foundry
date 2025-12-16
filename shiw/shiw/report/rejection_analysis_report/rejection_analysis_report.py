# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
	if not filters:
		filters = {}

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	item_filter = filters.get("item_name")
	rejection_type = filters.get("rejection_type") or "Both"

	include_first = rejection_type in ("Both", "First Line")
	include_second = rejection_type in ("Both", "Second Line")

	# Get all rejection reasons - we'll populate this dynamically from actual data
	rejection_reasons = []

	# Dictionary to store item-wise rejection data
	# Structure: {item_name: {rejection_reason: total_quantity}}
	item_rejection_data = {}

	# Get all unique items from both rejection types within date range
	all_items = set()

	# Dictionary to store first line rejection percentages
	# Structure: {item_name: {"total_quantity": sum, "total_rejected": sum}}
	first_line_rejection_data = {}

	# Dictionary to store second line rejection percentages
	# Structure: {item_name: {"total_available": sum, "total_rejected": sum}}
	second_line_rejection_data = {}

	# FIRST LINE REJECTIONS
	first_line_docs = (
		frappe.get_all(
			"First Line Rejection",
			filters={"docstatus": 1, "date": ["between", [from_date, to_date]]},
			fields=["name"],
		)
		if include_first
		else []
	)

	for doc in first_line_docs:
		child_rows = frappe.get_all(
			"First Line Inspection Report",
			filters={"parent": doc.name},
			fields=["item_name", "rejection", "total_cast_weight", "quantity", "quantity_rejected"],
		)

		# Track items in this document to avoid double-counting quantity
		# Structure: {item_name: quantity} for this document
		items_in_doc = {}

		for row in child_rows:
			item_name = row.item_name
			rejection_reason = row.rejection
			weight = row.total_cast_weight or 0
			quantity = row.quantity or 0
			quantity_rejected = row.quantity_rejected or 0

			all_items.add(item_name)

			# Store rejection weight data
			if item_name not in item_rejection_data:
				item_rejection_data[item_name] = {}

			if rejection_reason not in item_rejection_data[item_name]:
				item_rejection_data[item_name][rejection_reason] = 0

			item_rejection_data[item_name][rejection_reason] += weight

			# Store first line rejection percentage data
			if item_name not in first_line_rejection_data:
				first_line_rejection_data[item_name] = {"total_quantity": 0, "total_rejected": 0}

			# For quantity: only count once per document per item (use max to handle any inconsistencies)
			# For quantity_rejected: sum all rejection quantities
			if item_name not in items_in_doc:
				# First time seeing this item in this document
				items_in_doc[item_name] = quantity
				first_line_rejection_data[item_name]["total_quantity"] += quantity
			else:
				# If we've seen this item in this doc before, use the max quantity (in case of inconsistencies)
				existing_quantity = items_in_doc[item_name]
				if quantity > existing_quantity:
					# Adjust: remove old quantity, add new (larger) quantity
					first_line_rejection_data[item_name]["total_quantity"] -= existing_quantity
					first_line_rejection_data[item_name]["total_quantity"] += quantity
					items_in_doc[item_name] = quantity

			# Always sum quantity_rejected (each row represents a different rejection reason)
			first_line_rejection_data[item_name]["total_rejected"] += quantity_rejected

	# SECOND LINE REJECTIONS
	second_line_docs = (
		frappe.get_all(
			"Second Line Rejection",
			filters={"docstatus": 1, "date": ["between", [from_date, to_date]]},
			fields=["name"],
		)
		if include_second
		else []
	)

	for doc in second_line_docs:
		child_rows = frappe.get_all(
			"Second Line Rejection Table",
			filters={"parent": doc.name},
			fields=[
				"item_name",
				"rejection_reason",
				"rejected_qty",
				"cast_weight_in_kg",
				"available_quantity",
			],
		)

		# Track items in this document to avoid double-counting available_quantity
		# Structure: {item_name: available_quantity} for this document
		items_in_doc = {}

		for row in child_rows:
			item_name = row.item_name
			rejection_reason = row.rejection_reason
			rejected_qty = row.rejected_qty or 0
			cast_weight_per_pc = row.cast_weight_in_kg or 0
			available_quantity = row.available_quantity or 0
			# Calculate total weight: cast_weight_in_kg * rejected_qty
			total_weight = cast_weight_per_pc * rejected_qty

			all_items.add(item_name)

			# Store rejection weight data
			if item_name not in item_rejection_data:
				item_rejection_data[item_name] = {}

			if rejection_reason not in item_rejection_data[item_name]:
				item_rejection_data[item_name][rejection_reason] = 0

			item_rejection_data[item_name][rejection_reason] += total_weight

			# Store second line rejection percentage data
			if item_name not in second_line_rejection_data:
				second_line_rejection_data[item_name] = {"total_available": 0, "total_rejected": 0}

			# For available_quantity: only count once per document per item (use max to handle any inconsistencies)
			# For rejected_qty: sum all rejection quantities
			if item_name not in items_in_doc:
				# First time seeing this item in this document
				items_in_doc[item_name] = available_quantity
				second_line_rejection_data[item_name]["total_available"] += available_quantity
			else:
				# If we've seen this item in this doc before, use the max available_quantity (in case of inconsistencies)
				existing_available = items_in_doc[item_name]
				if available_quantity > existing_available:
					# Adjust: remove old available_quantity, add new (larger) available_quantity
					second_line_rejection_data[item_name]["total_available"] -= existing_available
					second_line_rejection_data[item_name]["total_available"] += available_quantity
					items_in_doc[item_name] = available_quantity

			# Always sum rejected_qty (each row represents a different rejection reason)
			second_line_rejection_data[item_name]["total_rejected"] += rejected_qty

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

		# Calculate First Line Rejection Production Loss %
		first_line_data = first_line_rejection_data.get(item_name, {"total_quantity": 0, "total_rejected": 0})
		if first_line_data["total_quantity"] > 0:
			first_line_percentage = (
				first_line_data["total_rejected"] / first_line_data["total_quantity"]
			) * 100
		else:
			first_line_percentage = 0
		row["first_line_rejection_percentage"] = round(first_line_percentage, 2)

		# Calculate Second Line Rejection Production Loss %
		second_line_data = second_line_rejection_data.get(
			item_name, {"total_available": 0, "total_rejected": 0}
		)
		if second_line_data["total_available"] > 0:
			second_line_percentage = (
				second_line_data["total_rejected"] / second_line_data["total_available"]
			) * 100
		else:
			second_line_percentage = 0
		row["second_line_rejection_percentage"] = round(second_line_percentage, 2)

		# Calculate Production Rejection % (combined from both lines)
		# Total production = first line quantity + second line available quantity
		# Total rejected = first line rejected + second line rejected
		total_production = first_line_data["total_quantity"] + second_line_data["total_available"]
		total_rejected_production = first_line_data["total_rejected"] + second_line_data["total_rejected"]
		if total_production > 0:
			production_rejection_percentage = (total_rejected_production / total_production) * 100
		else:
			production_rejection_percentage = 0
		row["production_rejection_percentage"] = round(production_rejection_percentage, 2)

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

	# Add the three new percentage columns after Item Name
	columns.append(
		{
			"label": "First Line Rejection Production Loss %",
			"fieldname": "first_line_rejection_percentage",
			"fieldtype": "Float",
			"width": 180,
			"precision": 2,
		}
	)
	columns.append(
		{
			"label": "Second Line Rejection Production Loss %",
			"fieldname": "second_line_rejection_percentage",
			"fieldtype": "Float",
			"width": 200,
			"precision": 2,
		}
	)
	columns.append(
		{
			"label": "Production Rejection %",
			"fieldname": "production_rejection_percentage",
			"fieldtype": "Float",
			"width": 150,
			"precision": 2,
		}
	)

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

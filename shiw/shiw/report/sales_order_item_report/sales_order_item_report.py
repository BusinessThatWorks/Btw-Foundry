# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters=None):
	filters = filters or {}
	selected = set()
	raw = filters.get("furnace_options") or ""
	if isinstance(raw, str):
		parts = [s.strip() for s in raw.split("\n") if s.strip()]
		if len(parts) <= 1:
			parts = [s.strip() for s in raw.split(",") if s.strip()]
		selected = set(parts)

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
		{"label": "Item Bunch Weight", "fieldname": "item_bunch_weight", "fieldtype": "Float", "width": 150},
		{"label": "Grade", "fieldname": "grade", "fieldtype": "Data", "width": 120},
		{"label": "Grade Group", "fieldname": "grade_group", "fieldtype": "Data", "width": 120},
		{"label": "Total Weight", "fieldname": "total_quantity", "fieldtype": "Float", "width": 150},
		{
			"label": "1 Ton Furnace (kg/min)",
			"fieldname": "throughput_1t",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": "500 kg Furnace (kg/min)",
			"fieldname": "throughput_500kg",
			"fieldtype": "Float",
			"width": 200,
		},
		{
			"label": "200 kg Furnace (kg/min)",
			"fieldname": "throughput_200kg",
			"fieldtype": "Float",
			"width": 200,
		},
		# Total estimated heats (by Sales Order) columns
		{
			"label": "Total Estimated Heats by 1 Ton",
			"fieldname": "total_est_heats_1t",
			"fieldtype": "Float",
			"width": 220,
		},
		{
			"label": "Total Estimated Heats by 500 kg",
			"fieldname": "total_est_heats_500kg",
			"fieldtype": "Float",
			"width": 230,
		},
		{
			"label": "Total Estimated Heats by 200 kg",
			"fieldname": "total_est_heats_200kg",
			"fieldtype": "Float",
			"width": 230,
		},
	]

	optional = []
	# Only add estimated columns when user selected at least one furnace
	if selected and ("1T" in selected):
		optional.append(
			{"label": "Estimated 1 Ton Time", "fieldname": "est_time_1t", "fieldtype": "Float", "width": 180}
		)
	if selected and ("500kg" in selected):
		optional.append(
			{
				"label": "Estimated 500 kg Time",
				"fieldname": "est_time_500kg",
				"fieldtype": "Float",
				"width": 190,
			}
		)
	if selected and ("200kg" in selected):
		optional.append(
			{
				"label": "Estimated 200 kg Time",
				"fieldname": "est_time_200kg",
				"fieldtype": "Float",
				"width": 190,
			}
		)

	# Derived pairs if both bases are selected
	if selected and ("1T" in selected) and ("500kg" in selected):
		optional.append(
			{
				"label": "Estimated 1T + 500kg Time",
				"fieldname": "est_time_1t_500kg",
				"fieldtype": "Float",
				"width": 210,
			}
		)
	if selected and ("1T" in selected) and ("200kg" in selected):
		optional.append(
			{
				"label": "Estimated 1T + 200kg Time",
				"fieldname": "est_time_1t_200kg",
				"fieldtype": "Float",
				"width": 210,
			}
		)
	if selected and ("500kg" in selected) and ("200kg" in selected):
		optional.append(
			{
				"label": "Estimated 500kg + 200kg Time",
				"fieldname": "est_time_500kg_200kg",
				"fieldtype": "Float",
				"width": 230,
			}
		)
	# Triple combination if all three are selected
	if selected and ("1T" in selected) and ("500kg" in selected) and ("200kg" in selected):
		optional.append(
			{
				"label": "Estimated 1T + 500kg + 200kg Time",
				"fieldname": "est_time_1t_500kg_200kg",
				"fieldtype": "Float",
				"width": 260,
			}
		)

	return base + optional


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
		if filters.get("grade"):
			filters["grade"] = str(filters.get("grade")).strip()
		if filters.get("grade_group"):
			filters["grade_group"] = str(filters.get("grade_group")).strip()

		# Helper to safely fetch throughput by furnace capacity
		def get_throughput_by_capacity(capacity_kg):
			try:
				# Get all furnaces with this capacity
				all_furnaces = frappe.db.get_all(
					"Furnace - Master",
					filters={"furnace_capacity__in_kg": capacity_kg},
					fields=["name", "furnace_name", "custom_throughput", "furnace_capacity__in_kg"],
				)

				if not all_furnaces:
					return 0.0

				# If multiple furnaces, use the one with the highest throughput
				highest_throughput = 0.0
				for furnace in all_furnaces:
					throughput = furnace.get("custom_throughput", 0) or 0
					if throughput > highest_throughput:
						highest_throughput = throughput

				return float(highest_throughput)
			except Exception:
				return 0.0

		# Fetch the three furnace throughput values once
		throughput_1t = get_throughput_by_capacity(1000)
		throughput_500kg = get_throughput_by_capacity(500)
		throughput_200kg = get_throughput_by_capacity(200)

		# Helper to fetch average heat time (Duration) and convert to minutes
		def get_avg_heat_time_minutes(capacity_kg):
			try:
				val = frappe.db.get_value(
					"Furnace - Master",
					{"furnace_capacity__in_kg": capacity_kg},
					"average_heat_time",
				)
				# Duration is typically stored as seconds (int/float). Convert to minutes.
				secs = float(val) if val not in [None, ""] else 0.0
				return secs / 60.0 if secs else 0.0
			except Exception:
				return 0.0

		avg_heat_time_1t_min = get_avg_heat_time_minutes(1000)
		avg_heat_time_500kg_min = get_avg_heat_time_minutes(500)
		avg_heat_time_200kg_min = get_avg_heat_time_minutes(200)

		# Build the SQL query to join Sales Order, Sales Order Item, Item, and Grade Master tables
		query = """
            SELECT 
                so.name AS sales_order_id,
                so.transaction_date,
                so.delivery_date,
                soi.item_code AS item_name,
                soi.qty,
                i.custom_bunch_weight_per_mould AS item_bunch_weight,
                i.custom_grade_ AS grade,
                gm.grade_group,
                (soi.qty * i.custom_bunch_weight_per_mould) AS total_quantity
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
		if filters.get("grade"):
			query += " AND i.custom_grade_ = %(grade)s"
		if filters.get("grade_group"):
			query += " AND gm.grade_group = %(grade_group)s"

		query += " ORDER BY so.name, soi.idx"

		# Execute the query
		data = frappe.db.sql(query, filters, as_dict=True)

		# Convert None values to 0 for numeric fields
		for row in data:
			row["qty"] = row["qty"] or 0
			row["item_bunch_weight"] = row["item_bunch_weight"] or 0
			row["total_quantity"] = row["total_quantity"] or 0
			row["grade"] = row["grade"] or ""
			row["grade_group"] = row["grade_group"] or ""
			row["throughput_1t"] = throughput_1t
			row["throughput_500kg"] = throughput_500kg
			row["throughput_200kg"] = throughput_200kg

			# Estimated times (safe division)
			tq = float(row["total_quantity"]) or 0.0

			def safe_div(n, d):
				try:
					d = float(d)
					return (float(n) / d) if d not in [None, 0.0] else 0.0
				except Exception:
					return 0.0

			row["est_time_1t"] = safe_div(tq, throughput_1t)
			row["est_time_500kg"] = safe_div(tq, throughput_500kg)
			row["est_time_200kg"] = safe_div(tq, throughput_200kg)
			row["est_time_1t_500kg"] = safe_div(tq, (throughput_1t + throughput_500kg))
			row["est_time_1t_200kg"] = safe_div(tq, (throughput_1t + throughput_200kg))
			row["est_time_500kg_200kg"] = safe_div(tq, (throughput_500kg + throughput_200kg))
			row["est_time_1t_500kg_200kg"] = safe_div(
				tq, (throughput_1t + throughput_500kg + throughput_200kg)
			)

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
				"total_quantity",
				"est_time_1t",
				"est_time_500kg",
				"est_time_200kg",
				"est_time_1t_500kg",
				"est_time_1t_200kg",
				"est_time_500kg_200kg",
				"est_time_1t_500kg_200kg",
			]:
				if key in acc_vals:
					row[key] = acc_vals.get(key, 0.0)

			# Compute total estimated heats per furnace capacity on subtotal row
			def div(n, d):
				try:
					return (float(n) / float(d)) if d not in [None, 0.0] else 0.0
				except Exception:
					return 0.0

			est_1t_min = acc_vals.get("est_time_1t", 0.0)
			est_500_min = acc_vals.get("est_time_500kg", 0.0)
			est_200_min = acc_vals.get("est_time_200kg", 0.0)
			row["total_est_heats_1t"] = div(est_1t_min, avg_heat_time_1t_min)
			row["total_est_heats_500kg"] = div(est_500_min, avg_heat_time_500kg_min)
			row["total_est_heats_200kg"] = div(est_200_min, avg_heat_time_200kg_min)
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
				"total_quantity",
				"est_time_1t",
				"est_time_500kg",
				"est_time_200kg",
				"est_time_1t_500kg",
				"est_time_1t_200kg",
				"est_time_500kg_200kg",
				"est_time_1t_500kg_200kg",
			]:
				if key in r and isinstance(r.get(key), (int, float)):
					acc[key] = acc.get(key, 0.0) + float(r.get(key) or 0.0)

		add_subtotal_row(current_so, acc)
		data = grouped

		frappe.log_error(f"Sales Order Item Report: Retrieved {len(data)} records", "Sales Order Report")

	except Exception as e:
		frappe.log_error(f"Error in Sales Order Item Report: {str(e)}", "Sales Order Report Error")
		frappe.msgprint(f"Error generating report: {str(e)}")

	return data

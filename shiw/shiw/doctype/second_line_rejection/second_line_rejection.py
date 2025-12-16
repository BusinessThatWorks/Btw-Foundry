# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SecondLineRejection(Document):
	def on_submit(self):
		"""Create and submit Stock Entry for foundry return items after submission"""
		# ----------------------------------------------------------------------
		# 🔁 Automatic Stock Entry on Second Line Rejection Submit (Material Receipt)
		# ----------------------------------------------------------------------

		# 1. Get the target warehouse
		TARGET_WH = "Estimated Foundry Return  - SHIW"

		if not frappe.db.exists("Warehouse", TARGET_WH):
			frappe.throw(f"❌ Warehouse '{TARGET_WH}' does not exist.")

		# 2. Float utility
		def flt(val):
			try:
				return float(val) if val not in [None, ""] else 0.0
			except Exception:
				return 0.0

		# 3. Aggregate total_weight by foundry_return item AND rejection_stage
		# Structure: {(foundry_return_item_code, rejection_stage): total_weight}
		# Weight = cast_weight_in_kg * rejected_qty
		foundry_return_map = {}

		# Process each row in table_scpn (Second Line Rejection Table)
		for row in self.table_scpn or []:
			item_name = getattr(row, "item_name", None)
			rejected_qty = flt(getattr(row, "rejected_qty", 0) or 0)
			cast_weight_in_kg = flt(getattr(row, "cast_weight_in_kg", 0) or 0)
			rejection_stage = getattr(row, "rejection_stage", None)

			if not item_name:
				continue

			if rejected_qty <= 0 or cast_weight_in_kg <= 0:
				continue

			# Validate rejection_stage is provided
			if not rejection_stage:
				frappe.throw(
					f"Row {row.idx}: Rejection Stage is required for item '{item_name}'. "
					"Please select 'Fettling' or 'Finishing'."
				)

			# Validate rejection_stage is Fettling or Finishing
			if rejection_stage not in ["Fettling", "Finishing"]:
				frappe.throw(
					f"Row {row.idx}: Rejection Stage '{rejection_stage}' is invalid for item '{item_name}'. "
					"Only 'Fettling' or 'Finishing' are allowed."
				)

			# Calculate weight: cast_weight * rejected_qty
			total_weight = cast_weight_in_kg * rejected_qty

			if total_weight <= 0:
				continue

			# Get grade from Item doctype
			grade = frappe.db.get_value("Item", item_name, "custom_grade_")

			if not grade:
				frappe.throw(
					f"Row {row.idx}: Item '{item_name}' does not have a grade assigned. "
					"Please assign a grade to the item."
				)

			# Get foundry_return item from Grade Master
			grade_master = frappe.get_doc("Grade Master", grade)
			if not grade_master:
				frappe.throw(f"Row {row.idx}: Grade Master '{grade}' not found for item '{item_name}'.")

			foundry_return_item = grade_master.foundry_return
			if not foundry_return_item:
				frappe.throw(
					f"Row {row.idx}: Grade Master '{grade}' does not have a Foundry Return item configured "
					f"for item '{item_name}'."
				)

			# Validate foundry_return item exists
			if not frappe.db.exists("Item", foundry_return_item):
				frappe.throw(
					f"Row {row.idx}: Foundry Return item '{foundry_return_item}' from Grade Master '{grade}' "
					f"does not exist for item '{item_name}'."
				)

			# Create key for grouping: (foundry_return_item, rejection_stage)
			key = (foundry_return_item, rejection_stage)

			# Sum total_weight for same foundry_return item and rejection_stage combination
			if key not in foundry_return_map:
				foundry_return_map[key] = 0.0

			foundry_return_map[key] += total_weight

		# 5. Build stock entry items with target warehouse only
		items = []
		for (foundry_return_item, rejection_stage), total_qty in foundry_return_map.items():
			if total_qty <= 0:
				continue

			item_dict = {
				"item_code": foundry_return_item,
				"qty": total_qty,
				"t_warehouse": TARGET_WH,
			}
			items.append(item_dict)

		# 6. Create and submit Stock Entry
		if items:
			try:
				# Create stock entry using new_doc
				stock_entry = frappe.new_doc("Stock Entry")
				stock_entry.stock_entry_type = "Material Receipt"
				stock_entry.remarks = f"Auto Material Receipt from Second Line Rejection {self.name}"

				# Add items with target warehouse only
				for item_data in items:
					stock_entry.append(
						"items",
						{
							"item_code": item_data["item_code"],
							"qty": item_data["qty"],
							"t_warehouse": item_data["t_warehouse"],
						},
					)

				# Insert the stock entry
				stock_entry.insert(ignore_permissions=True)

				# Submit the stock entry
				stock_entry.submit()

				# Link back to Second Line Rejection
				self.db_set("linked_stock_entry", stock_entry.name)

				frappe.msgprint(f"✅ Stock Entry Created: {stock_entry.name}")
			except Exception as e:
				frappe.log_error(
					f"Error creating Stock Entry for Second Line Rejection {self.name}: {str(e)}"
				)
				frappe.throw(f"Failed to create Stock Entry: {str(e)}")
		else:
			frappe.msgprint("⚠️ No items found for Stock Entry creation.")

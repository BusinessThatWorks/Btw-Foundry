# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FirstLineRejection(Document):
	def on_submit(self):
		"""Create and submit Stock Entry for foundry return items after submission"""
		# ----------------------------------------------------------------------
		# 🔁 Automatic Stock Entry on First Line Rejection Submit (Material Transfer)
		# ----------------------------------------------------------------------

		# 1. Get source and target warehouses
		SOURCE_WH = "Short Blast - SHIW"
		TARGET_WH = "Estimated Foundry Return  - SHIW"

		if not frappe.db.exists("Warehouse", SOURCE_WH):
			frappe.throw(f"❌ Source Warehouse '{SOURCE_WH}' does not exist.")

		if not frappe.db.exists("Warehouse", TARGET_WH):
			frappe.throw(f"❌ Target Warehouse '{TARGET_WH}' does not exist.")

		# 2. Float utility
		def flt(val):
			try:
				return float(val) if val not in [None, ""] else 0.0
			except Exception:
				return 0.0

		# 3. Aggregate total_cast_weight by foundry_return item
		# Structure: {foundry_return_item_code: total_weight}
		foundry_return_map = {}

		# Process each row in table_yncx (First Line Inspection Report)
		for row in self.table_yncx or []:
			item_name = getattr(row, "item_name", None)
			total_cast_weight = flt(getattr(row, "total_cast_weight", 0) or 0)

			if not item_name:
				continue

			if total_cast_weight <= 0:
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

			# Sum total_cast_weight for same foundry_return item
			if foundry_return_item not in foundry_return_map:
				foundry_return_map[foundry_return_item] = 0.0

			foundry_return_map[foundry_return_item] += total_cast_weight

		# 4. Build stock entry items with source warehouse
		items = []
		for foundry_return_item, total_qty in foundry_return_map.items():
			if total_qty <= 0:
				continue

			item_dict = {
				"item_code": foundry_return_item,
				"qty": total_qty,
				"s_warehouse": SOURCE_WH,
				"t_warehouse": TARGET_WH,
			}
			items.append(item_dict)

		# 5. Create and submit Stock Entry
		if items:
			try:
				# Create stock entry using new_doc (better for Material Transfer)
				stock_entry = frappe.new_doc("Stock Entry")
				stock_entry.stock_entry_type = "Material Transfer"
				stock_entry.remarks = f"Auto Material Transfer from First Line Rejection {self.name}"

				# Add items with source and target warehouses
				for item_data in items:
					stock_entry.append(
						"items",
						{
							"item_code": item_data["item_code"],
							"qty": item_data["qty"],
							"s_warehouse": item_data["s_warehouse"],
							"t_warehouse": item_data["t_warehouse"],
						},
					)

				# Insert the stock entry
				stock_entry.insert(ignore_permissions=True)

				# Submit the stock entry
				stock_entry.submit()

				# Link back to First Line Rejection
				self.db_set("linked_stock_entry", stock_entry.name)

				frappe.msgprint(f"✅ Stock Entry Created: {stock_entry.name}")
			except Exception as e:
				frappe.log_error(f"Error creating Stock Entry for First Line Rejection {self.name}: {str(e)}")
				frappe.throw(f"Failed to create Stock Entry: {str(e)}")
		else:
			frappe.msgprint("⚠️ No items found for Stock Entry creation.")

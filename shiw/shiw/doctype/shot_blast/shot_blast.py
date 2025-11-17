# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


def flt(val):
	try:
		return float(val) if val not in [None, ""] else 0.0
	except Exception:
		return 0.0


class ShotBlast(Document):
	def on_submit(self):
		"""Create and submit Stock Entry for shot blast items after submission"""
		items = []

		# Validate warehouses
		source_warehouse = "Shake Out - SHIW"
		target_warehouse = "Short Blast - SHIW"

		if not frappe.db.exists("Warehouse", source_warehouse):
			frappe.throw(f"Warehouse '{source_warehouse}' does not exist")
		if not frappe.db.exists("Warehouse", target_warehouse):
			frappe.throw(f"Warehouse '{target_warehouse}' does not exist")

		# Process table_short rows
		for row in self.table_short:
			if not row.item_name:
				continue

			short_qty = flt(row.short_blast_quantity)
			shakeout_qty = flt(row.shakeout_quantity)

			if short_qty > 0:
				# Validate short_qty doesn't exceed shakeout_qty
				if short_qty > shakeout_qty:
					frappe.throw(
						f"Error: Shot Blast Quantity ({short_qty}) for item {row.item_name} "
						f"exceeds Shakeout Quantity ({shakeout_qty})."
					)

				items.append(
					{
						"item_code": row.item_name,
						"qty": short_qty,
						"s_warehouse": source_warehouse,
						"t_warehouse": target_warehouse,
						"custom_pouring_id": row.pouring_id,
					}
				)

		# Create and submit Stock Entry
		if items:
			try:
				se = frappe.new_doc("Stock Entry")
				se.stock_entry_type = "Material Transfer"
				se.custom_date = self.date
				se.custom_shift_type = self.shift_type
				se.custom_process_type = "Short Blast"
				se.remarks = f"Auto-created from Shot Blast: {self.name}"

				for item in items:
					se.append("items", item)

				se.insert(ignore_permissions=True)
				se.submit()

				# Link back to Shot Blast document
				self.db_set("linked_stock_entry", se.name)

				# Success Message
				frappe.msgprint(f"✅ Stock Entry Created and Submitted: {se.name}")
			except Exception as e:
				frappe.throw(f"Failed to create or submit Stock Entry: {str(e)}")
		else:
			frappe.msgprint("⚠️ No valid quantities to create Stock Entry.")

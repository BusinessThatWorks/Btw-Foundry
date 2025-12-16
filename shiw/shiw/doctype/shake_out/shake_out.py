# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


def flt(val):
	try:
		return float(val) if val not in [None, ""] else 0.0
	except Exception:
		return 0.0


class ShakeOut(Document):
	def on_submit(self):
		"""Create and submit Stock Entry for shake out items after submission"""
		stock_items = []

		# Validate warehouses
		source_warehouse = "Pouring - SHIW"
		target_warehouse = "Shake Out - SHIW"

		if not frappe.db.exists("Warehouse", source_warehouse):
			frappe.throw(f"Warehouse '{source_warehouse}' does not exist")
		if not frappe.db.exists("Warehouse", target_warehouse):
			frappe.throw(f"Warehouse '{target_warehouse}' does not exist")

		# Process table_abc rows
		for row in self.table_abc:
			if row.item_name and flt(row.shake_out_qty) > 0:
				shake_out_qty = flt(row.shake_out_qty)
				prod_cast_qty = flt(row.prod_cast)

				# Validate shake_out_qty doesn't exceed prod_cast
				if shake_out_qty > prod_cast_qty:
					frappe.throw(
						f"Error: Shake Out Quantity ({shake_out_qty}) for item {row.item_name} "
						f"exceeds Production Cast Quantity ({prod_cast_qty})."
					)

				stock_items.append(
					{
						"item_code": row.item_name,
						"qty": shake_out_qty,
						"custom_pouring_id": row.pouring_id,
						"s_warehouse": source_warehouse,
						"t_warehouse": target_warehouse,
					}
				)

		# Create and submit Stock Entry
		if not stock_items:
			frappe.msgprint("⚠️ No valid items to create Stock Entry.")
		else:
			se_doc = frappe.get_doc(
				{
					"doctype": "Stock Entry",
					"stock_entry_type": "Material Transfer",
					"items": stock_items,
					"custom_date": self.date,
					"custom_shift_type": self.shift_type,
					"custom_process_type": "Shake Out",
					"remarks": f"Auto-created from Shake Out: {self.name}",
				}
			)

			se_doc.insert(ignore_permissions=True)
			se_doc.submit()

			self.db_set("linked_stock_entry", se_doc.name)
			frappe.msgprint(f"✅ Stock Entry Created and Submitted: {se_doc.name}")

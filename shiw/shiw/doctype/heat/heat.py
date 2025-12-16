# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Heat(Document):
	def onload(self):
		"""Set field properties when form loads and log load event"""
		self.set_field_properties()

	def before_save(self):
		"""Lightweight pre-save hook to confirm method is called"""
		pass

	def before_validate(self):
		"""Dynamically modify field properties before validation"""
		self.set_field_properties()

		# If downtime is checked, clear mandatory child table rows to avoid validation errors
		if self.custom_is_downtime:
			# Clear the charge_mix_component_item table to avoid validation errors
			if hasattr(self, "charge_mix_component_item") and self.charge_mix_component_item:
				self.charge_mix_component_item = []

			# Clear the table_vkjb table to avoid validation errors
			if hasattr(self, "table_vkjb") and self.table_vkjb:
				self.table_vkjb = []

	def on_submit(self):
		"""Create and submit Stock Entry for charge mix component items after submission"""
		# ----------------------------------------------------------------------
		# 🔁 Automatic Stock Entry on Heat Submit (Material Issue)
		# ----------------------------------------------------------------------

		# 1. Dynamically get the exact warehouse "name" field
		company_name = "Shree Hanuman Iron Works"
		warehouse_label = "Estimated Foundry Return"

		SOURCE_WH = frappe.db.get_value(
			"Warehouse", {"warehouse_name": warehouse_label, "company": company_name}, "name"
		)

		if not SOURCE_WH:
			frappe.throw(f"❌ Could not find warehouse '{warehouse_label}' for company '{company_name}'.")

		# 2. Float utility
		def flt(val):
			try:
				return float(val) if val not in [None, ""] else 0.0
			except Exception:
				return 0.0

		# 3. Get liquid_metal_pig and slag_metal from parent Heat document
		liquid_metal_pig = flt(getattr(self, "liquid_metal_pig", 0) or 0)
		slag_metal = flt(getattr(self, "slag_metal", 0) or 0)

		# 4. Build stock entry items
		items = []
		for row in self.charge_mix_component_item or []:
			if getattr(row, "is_stock_entry", 0):
				weight = flt(getattr(row, "weight", 0) or 0)

				# Calculate qty as weight + liquid_metal_pig + slag_metal
				qty = weight + liquid_metal_pig + slag_metal

				if qty <= 0:
					frappe.throw(
						f"Row {row.idx}: Total quantity (weight + liquid_metal_pig + slag_metal) must be > 0."
					)

				item_code = getattr(row, "item", None)
				if not item_code or not frappe.db.exists("Item", item_code):
					frappe.throw(f"Row {row.idx}: Item '{item_code}' not found.")

				item_dict = {
					"item_code": item_code,
					"qty": qty,
					"s_warehouse": SOURCE_WH,
				}
				items.append(item_dict)

		# 5. Create and submit Stock Entry
		if items:
			stock_entry = frappe.get_doc(
				{
					"doctype": "Stock Entry",
					"stock_entry_type": "Material Issue",
					"items": items,
					"remarks": f"Auto Material Issue from Heat {self.name}",
				}
			)

			# Explicitly set qty for each item after doc creation (in case it gets reset)
			for idx, item_row in enumerate(stock_entry.items):
				original_qty = items[idx]["qty"]
				item_row.qty = original_qty

			stock_entry.insert()

			# Reload to get actual stored values
			stock_entry.reload()

			# Set qty again before submit (in case it was reset during insert)
			for idx, item_row in enumerate(stock_entry.items):
				if idx < len(items):
					original_qty = items[idx]["qty"]
					item_row.qty = original_qty

			stock_entry.submit()

			# Link back to Heat
			self.db_set("linked_stock_entry", stock_entry.name)

			frappe.msgprint(f"✅ Stock Entry Created: {stock_entry.name}")

	def validate(self):
		"""Override validation when downtime is checked"""
		# Set global flag for child tables to check
		frappe.local.heat_downtime_mode = bool(self.custom_is_downtime)

		if self.custom_is_downtime:
			# Skip all validation when downtime is checked
			return

		# Normal validation will proceed if downtime is not checked

	def set_field_properties(self):
		"""Dynamically set mandatory field properties"""
		is_downtime = self.get("custom_is_downtime", 0)

		# Get the meta object
		meta = frappe.get_meta(self.doctype)

		# Main form mandatory fields
		mandatory_fields = [
			"melter",
			"date",
			"pouring_person",
			"furnace_no",
			"material_grade",
			"ladle_no",
			"lining_heat_no",
			"foundry_return_existing",
			"liquid_metal_pig",
			"furnace_holding_time",
			"shift_type",
		]

		# Set main form field properties
		for field in mandatory_fields:
			field_obj = meta.get_field(field)
			if field_obj:
				field_obj.reqd = not is_downtime

		# Child table mandatory fields
		child_table_fields = {
			"charge_mix_component_item": ["item", "weight", "amount"],
			"table_vkjb": ["item", "uom", "quantity"],
		}

		# Set child table field properties
		for table_field, child_fields in child_table_fields.items():
			table_field_obj = meta.get_field(table_field)
			if table_field_obj:
				child_doctype = table_field_obj.options
				child_meta = frappe.get_meta(child_doctype)

				for child_field in child_fields:
					child_field_obj = child_meta.get_field(child_field)
					if child_field_obj:
						child_field_obj.reqd = not is_downtime

				# Also set the table field itself to non-mandatory when downtime is checked
				table_field_obj.reqd = not is_downtime

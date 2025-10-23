# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Heat(Document):
	def onload(self):
		"""Set field properties when form loads and log load event"""
		frappe.log_error(f"🔥 HEAT ONLOAD CALLED for Heat {self.name}", "Heat Debug")
		self.set_field_properties()
	
	def before_save(self):
		"""Lightweight pre-save hook to confirm method is called"""
		frappe.log_error(f"🔥 HEAT BEFORE_SAVE CALLED for Heat {self.name}", "Heat Debug")
	
	def before_validate(self):
		"""Dynamically modify field properties before validation"""
		self.set_field_properties()
		
		# If downtime is checked, clear mandatory child table rows to avoid validation errors
		if self.custom_is_downtime:
			# Clear the charge_mix_component_item table to avoid validation errors
			if hasattr(self, 'charge_mix_component_item') and self.charge_mix_component_item:
				self.charge_mix_component_item = []
				frappe.log_error("Cleared charge_mix_component_item table due to downtime mode", "Heat Debug")
			
			# Clear the table_vkjb table to avoid validation errors  
			if hasattr(self, 'table_vkjb') and self.table_vkjb:
				self.table_vkjb = []
				frappe.log_error("Cleared table_vkjb table due to downtime mode", "Heat Debug")

	def on_submit(self):
		"""Create and submit Stock Entry for charge mix component items after submission"""
		frappe.log_error(f"🔥 HEAT AFTER_SUBMIT CALLED for Heat {self.name}", "Heat Debug")
		
		# ----------------------------------------------------------------------
		# 🔁 Automatic Stock Entry on Heat Submit (Material Issue)
		# ----------------------------------------------------------------------

		# 1. Dynamically get the exact warehouse "name" field
		company_name = "Shree Hanuman Iron Works"
		warehouse_label = "Estimated Foundry Return"

		SOURCE_WH = frappe.db.get_value(
			"Warehouse",
			{"warehouse_name": warehouse_label, "company": company_name},
			"name"
		)

		if not SOURCE_WH:
			frappe.throw(f"❌ Could not find warehouse '{warehouse_label}' for company '{company_name}'.")

		# 2. Float utility
		def flt(val):
			try:
				return float(val) if val not in [None, ""] else 0.0
			except Exception:
				return 0.0

		# 3. Build stock entry items
		items = []
		for row in (self.charge_mix_component_item or []):
			if getattr(row, 'is_stock_entry', 0):
				qty = flt(getattr(row, 'weight', 0))

				if qty <= 0:
					frappe.throw(f"Row {row.idx}: Weight must be > 0.")

				item_code = getattr(row, 'item', None)
				if not item_code or not frappe.db.exists("Item", item_code):
					frappe.throw(f"Row {row.idx}: Item '{item_code}' not found.")

				items.append({
					"item_code": item_code,
					"qty": qty,
					"s_warehouse": SOURCE_WH,
				})

		# 4. Create and submit Stock Entry
		if items:
			stock_entry = frappe.get_doc({
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Issue",
				"items": items,
				"remarks": f"Auto Material Issue from Heat {self.name}"
			})
			stock_entry.insert()
			stock_entry.submit()

			# 5. Link back to Heat
			self.db_set("linked_stock_entry", stock_entry.name)

			frappe.log_error(f"🔥 Stock Entry Created: {stock_entry.name}", "Heat Debug")
			frappe.msgprint(f"✅ Stock Entry Created: {stock_entry.name}")
		else:
			frappe.log_error("🔥 No rows marked for stock entry – skipping creation", "Heat Debug")
			frappe.msgprint("✅ No rows marked for stock entry – skipping creation.")
		
		frappe.log_error(f"🔥 HEAT AFTER_SUBMIT COMPLETED for Heat {self.name}", "Heat Debug")
	
	def validate(self):
		"""Override validation when downtime is checked"""
		frappe.log_error(f"Heat validate called. Downtime status: {self.custom_is_downtime}", "Heat Debug")
		
		# Set global flag for child tables to check
		frappe.local.heat_downtime_mode = bool(self.custom_is_downtime)
		frappe.log_error(f"Set global downtime flag to: {frappe.local.heat_downtime_mode}", "Heat Debug")
		
		if self.custom_is_downtime:
			# Skip all validation when downtime is checked
			frappe.log_error("Skipping validation due to downtime mode", "Heat Debug")
			return
		
		# Normal validation will proceed if downtime is not checked
		frappe.log_error("Proceeding with normal validation", "Heat Debug")
	
	def set_field_properties(self):
		"""Dynamically set mandatory field properties"""
		is_downtime = self.get('custom_is_downtime', 0)
		
		# Debug logging
		frappe.log_error(f"Heat set_field_properties called. Downtime: {is_downtime}", "Heat Debug")
		
		# Get the meta object
		meta = frappe.get_meta(self.doctype)
		
		# Main form mandatory fields
		mandatory_fields = [
			'melter', 'date', 'pouring_person', 'furnace_no', 
			'material_grade', 'ladle_no', 'lining_heat_no',
			'foundry_return_existing', 'liquid_metal_pig', 
			'furnace_holding_time', 'shift_type'
		]
		
		# Set main form field properties
		for field in mandatory_fields:
			field_obj = meta.get_field(field)
			if field_obj:
				old_reqd = field_obj.reqd
				field_obj.reqd = not is_downtime
				frappe.log_error(f"Field {field}: {old_reqd} -> {field_obj.reqd}", "Heat Debug")
		
		# Child table mandatory fields
		child_table_fields = {
			'charge_mix_component_item': ['item', 'weight', 'amount'],
			'table_vkjb': ['item', 'uom', 'quantity']
		}
		
		# Set child table field properties - THIS IS THE KEY FIX
		for table_field, child_fields in child_table_fields.items():
			table_field_obj = meta.get_field(table_field)
			if table_field_obj:
				child_doctype = table_field_obj.options
				child_meta = frappe.get_meta(child_doctype)
				
				frappe.log_error(f"Processing child doctype: {child_doctype}", "Heat Debug")
				
				for child_field in child_fields:
					child_field_obj = child_meta.get_field(child_field)
					if child_field_obj:
						old_reqd = child_field_obj.reqd
						child_field_obj.reqd = not is_downtime
						frappe.log_error(f"Child field {child_doctype}.{child_field}: {old_reqd} -> {child_field_obj.reqd}", "Heat Debug")
					else:
						frappe.log_error(f"Child field {child_field} not found in {child_doctype}", "Heat Debug")
				
				# CRITICAL: Also set the table field itself to non-mandatory when downtime is checked
				table_field_obj.reqd = not is_downtime
				frappe.log_error(f"Table field {table_field}: {old_reqd} -> {table_field_obj.reqd}", "Heat Debug")

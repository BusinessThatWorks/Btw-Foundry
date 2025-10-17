# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Heat(Document):
	def onload(self):
		"""Set field properties when form loads"""
		self.set_field_properties()
	
	def before_validate(self):
		"""Dynamically modify field properties before validation"""
		self.set_field_properties()
	
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

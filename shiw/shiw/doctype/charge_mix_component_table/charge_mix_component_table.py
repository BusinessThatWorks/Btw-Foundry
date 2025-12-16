# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Chargemixcomponenttable(Document):
	def validate(self):
		"""Override validation if parent Heat document has downtime checked"""
		frappe.log_error(
			f"Charge mix component table validate called. Parent: {self.parent}, ParentType: {self.parenttype}",
			"Heat Debug",
		)

		# Check if we're in downtime mode using a global flag
		downtime_mode = getattr(frappe.local, "heat_downtime_mode", False)
		frappe.log_error(f"Global downtime mode flag: {downtime_mode}", "Heat Debug")

		# Check if this child table belongs to a Heat document with downtime
		if self.parent and self.parenttype == "Heat":
			try:
				parent_doc = frappe.get_doc(self.parenttype, self.parent)
				downtime_status = parent_doc.get("custom_is_downtime")
				frappe.log_error(f"Parent Heat doc found. Downtime status: {downtime_status}", "Heat Debug")

				if downtime_status:
					frappe.log_error(
						f"Skipping Charge mix component table validation due to downtime mode in Heat {self.parent}",
						"Heat Debug",
					)
					return
			except Exception as e:
				frappe.log_error(f"Error checking parent doc: {str(e)}", "Heat Debug")

		# Also check global flag
		if downtime_mode:
			frappe.log_error(
				f"Skipping Charge mix component table validation due to global downtime mode flag",
				"Heat Debug",
			)
			return

		# Normal validation will proceed if not in downtime mode
		frappe.log_error("Proceeding with normal Charge mix component table validation", "Heat Debug")
		# Call the parent class validate method for normal validation
		super().validate()

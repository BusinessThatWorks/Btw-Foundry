# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def setup_salary_structure_formula_fields():
	"""Setup custom fields for salary structure formula calculation"""

	custom_fields = {
		"Salary Detail": [
			{
				"fieldname": "custom_amount_formula",
				"fieldtype": "Small Text",
				"label": "Formula",
				"description": "Enter Python expression using earnings abbreviations (e.g., B, HRA). Example: 1800 if B > 15000 else B * 12/100",
				"insert_after": "statistical_component",
				"allow_on_submit": 1,
				"depends_on": "eval:doc.statistical_component==0",
				"module": "HR",
			},
			{
				"fieldname": "custom_calculated_amount",
				"fieldtype": "Currency",
				"label": "Calculated Amount",
				"description": "This field will be automatically calculated based on the formula",
				"insert_after": "custom_amount_formula",
				"read_only": 1,
				"allow_on_submit": 1,
				"depends_on": "eval:doc.custom_amount_formula",
				"module": "HR",
			},
		]
	}

	try:
		create_custom_fields(custom_fields, update=True)
		frappe.db.commit()
		print("✅ Custom fields for Salary Structure formula calculation have been created successfully!")
		return True
	except Exception as e:
		frappe.log_error(f"Error creating custom fields: {str(e)}", "Salary Structure Setup Error")
		print(f"❌ Error creating custom fields: {str(e)}")
		return False


def remove_salary_structure_formula_fields():
	"""Remove custom fields for salary structure formula calculation"""

	custom_fields_to_remove = [
		{"dt": "Salary Detail", "fieldname": "custom_amount_formula"},
		{"dt": "Salary Detail", "fieldname": "custom_calculated_amount"},
	]

	try:
		for field in custom_fields_to_remove:
			if frappe.db.exists("Custom Field", field):
				frappe.delete_doc("Custom Field", frappe.db.get_value("Custom Field", field, "name"))

		frappe.db.commit()
		print("✅ Custom fields for Salary Structure formula calculation have been removed successfully!")
		return True
	except Exception as e:
		frappe.log_error(f"Error removing custom fields: {str(e)}", "Salary Structure Setup Error")
		print(f"❌ Error removing custom fields: {str(e)}")
		return False


if __name__ == "__main__":
	# This can be run from the console to setup the fields
	setup_salary_structure_formula_fields()

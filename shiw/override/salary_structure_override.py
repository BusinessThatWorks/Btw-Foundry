# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


def add_custom_fields_to_salary_structure():
	"""Add custom fields to Salary Structure Deductions if they don't exist"""

	# Check if custom_amount_formula field exists
	if not frappe.db.exists(
		"Custom Field", {"dt": "Salary Detail", "fieldname": "custom_amount_formula"}
	):
		custom_field = frappe.get_doc(
			{
				"doctype": "Custom Field",
				"dt": "Salary Detail",
				"fieldname": "custom_amount_formula",
				"fieldtype": "Small Text",
				"label": "Formula",
				"description": "Enter Python expression using earnings abbreviations (e.g., B, HRA). Example: 1800 if B > 15000 else B * 12/100",
				"insert_after": "statistical_component",
				"allow_on_submit": 1,
				"depends_on": "eval:doc.statistical_component==0",
				"module": "HR",
			}
		)
		custom_field.insert(ignore_permissions=True)
		frappe.db.commit()
		frappe.msgprint("Added custom_amount_formula field to Salary Structure Deductions")

	# Check if custom_calculated_amount field exists
	if not frappe.db.exists(
		"Custom Field", {"dt": "Salary Detail", "fieldname": "custom_calculated_amount"}
	):
		custom_field = frappe.get_doc(
			{
				"doctype": "Custom Field",
				"dt": "Salary Detail",
				"fieldname": "custom_calculated_amount",
				"fieldtype": "Currency",
				"label": "Calculated Amount",
				"description": "This field will be automatically calculated based on the formula",
				"insert_after": "custom_amount_formula",
				"read_only": 1,
				"allow_on_submit": 1,
				"depends_on": "eval:doc.custom_amount_formula",
				"module": "HR",
			}
		)
		custom_field.insert(ignore_permissions=True)
		frappe.db.commit()
		frappe.msgprint("Added custom_calculated_amount field to Salary Structure Deductions")


def calculate_salary_structure_deductions(doc, method):
	"""Calculate deduction amounts using formulas when salary structure is saved"""
	try:
		from shiw.api.salary_formula_calculator import evaluate_formula

		# Get earnings context
		earnings_context = {}
		for earning in doc.earnings:
			if earning.abbreviation:
				earnings_context[earning.abbreviation] = earning.amount or 0.0

		# Calculate each deduction
		for deduction in doc.deductions:
			if hasattr(deduction, "custom_amount_formula") and deduction.custom_amount_formula:
				try:
					calculated_amount = evaluate_formula(deduction.custom_amount_formula, earnings_context)
					deduction.amount = calculated_amount
					if hasattr(deduction, "custom_calculated_amount"):
						deduction.custom_calculated_amount = calculated_amount
				except Exception as e:
					frappe.log_error(
						f"Error calculating deduction {deduction.component}: {str(e)}",
						"Salary Structure Formula Error",
					)
					deduction.amount = 0.0
					if hasattr(deduction, "custom_calculated_amount"):
						deduction.custom_calculated_amount = 0.0

	except Exception as e:
		frappe.log_error(
			f"Error in calculate_salary_structure_deductions: {str(e)}", "Salary Structure Formula Error"
		)


def validate_salary_structure_formulas(doc, method):
	"""Validate all formulas in salary structure before saving"""
	try:
		from shiw.api.salary_formula_calculator import evaluate_formula

		for deduction in doc.deductions:
			if hasattr(deduction, "custom_amount_formula") and deduction.custom_amount_formula:
				try:
					# Test the formula with sample values
					sample_context = {"B": 23700, "HRA": 13300, "DA": 5000}  # Sample data
					evaluate_formula(deduction.custom_amount_formula, sample_context)
				except Exception as e:
					frappe.throw(f"Invalid formula in deduction '{deduction.component}': {str(e)}")

	except Exception as e:
		frappe.log_error(
			f"Error in validate_salary_structure_formulas: {str(e)}", "Salary Structure Formula Error"
		)

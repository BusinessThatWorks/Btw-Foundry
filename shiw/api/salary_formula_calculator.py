# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
import json
import ast
import operator


@frappe.whitelist()
def test_api():
	"""Simple test endpoint to check if API is working"""
	print("🔧 Test API called")
	return {"success": True, "message": "API is working"}


@frappe.whitelist()
def calculate_formula_amount(formula, earnings_data=None):
	"""
	API endpoint to calculate formula amount for salary deductions

	Args:
		formula (str): The formula to evaluate
		earnings_data (dict): Earnings data for context

	Returns:
		dict: Result with calculated amount and any errors
	"""
	try:
		print(f"🔧 API: calculate_formula_amount called with formula: {formula}")
		print(f"🔧 API: earnings_data: {earnings_data}")

		if not formula:
			print("🔧 API: No formula provided")
			return {"success": True, "amount": 0.0, "message": "No formula provided"}

		# Create context from earnings data (normalize anything the client sends)
		context = normalize_context(earnings_data)
		print(f"🔧 API: Using context: {context}")

		# Calculate the amount
		amount = evaluate_formula(formula, context)
		print(f"🔧 API: Calculated amount: {amount}")

		result = {"success": True, "amount": amount, "message": f"Formula calculated successfully: {amount}"}
		print(f"🔧 API: Returning result: {result}")
		return result

	except Exception as e:
		print(f"🔧 API: Error occurred: {str(e)}")
		frappe.log_error(f"Formula calculation error: {str(e)}", "Salary Formula Calculator Error")
		return {"success": False, "amount": 0.0, "message": f"Error calculating formula: {str(e)}"}


@frappe.whitelist()
def validate_formula(formula, earnings_data=None):
	"""
	API endpoint to validate a formula without calculating

	Args:
		formula (str): The formula to validate
		earnings_data (dict): Sample earnings data for testing

	Returns:
		dict: Validation result
	"""
	try:
		if not formula:
			return {"success": True, "valid": True, "sample_result": 0.0, "message": "No formula provided"}

		# Create context
		context = earnings_data or {"B": 23700, "HRA": 13300}  # Sample data

		# Test the formula
		result = evaluate_formula(formula, context)

		return {"success": True, "valid": True, "sample_result": result, "message": "Formula is valid"}

	except Exception as e:
		return {
			"success": False,
			"valid": False,
			"sample_result": 0.0,
			"message": f"Invalid formula: {str(e)}",
		}


def evaluate_formula(formula, context=None):
	"""
	Safely evaluate a Python formula expression

	Args:
		formula (str): The formula to evaluate
		context (dict): Variables to use in the formula

	Returns:
		float: The calculated result
	"""
	print(f"🧮 evaluate_formula called with: {formula}")
	print(f"🧮 context: {context}")

	if not formula:
		print("🧮 No formula provided, returning 0")
		return 0.0

	if context is None:
		context = {}

	# Create a safe evaluation context
	safe_dict = {
		"__builtins__": {},
		# Math functions
		"abs": abs,
		"round": round,
		"min": min,
		"max": max,
		"sum": sum,
		# Math operators
		"True": True,
		"False": False,
		"None": None,
	}

	# Add context variables
	safe_dict.update(normalize_context(context))
	print(f"🧮 Safe dict: {safe_dict}")

	try:
		# Parse and compile the expression
		expr = ast.parse(formula, mode="eval")
		print(f"🧮 Parsed expression: {expr}")

		# Check for dangerous operations
		for node in ast.walk(expr):
			if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
				# Allow only safe function calls
				if isinstance(node, ast.Call):
					if not isinstance(node.func, ast.Name):
						raise ValueError("Only simple function calls are allowed")
					if node.func.id not in safe_dict:
						raise ValueError(f"Function '{node.func.id}' is not allowed")
			elif isinstance(node, ast.Attribute):
				raise ValueError("Attribute access is not allowed")
			elif isinstance(node, ast.Subscript):
				raise ValueError("Subscript access is not allowed")

		# Provide default value 0 for any undefined variable names
		undefined_names = set()
		for node in ast.walk(expr):
			if isinstance(node, ast.Name):
				if node.id not in safe_dict:
					undefined_names.add(node.id)
		for name in undefined_names:
			safe_dict[name] = 0.0
		if undefined_names:
			print(f"🧮 Filled undefined names with 0: {sorted(list(undefined_names))}")

		# Evaluate the expression
		result = eval(compile(expr, "<string>", "eval"), safe_dict)
		print(f"🧮 Evaluation result: {result}")

		# Ensure result is numeric
		if not isinstance(result, (int, float)):
			raise ValueError("Formula must return a numeric value")

		final_result = float(result)
		print(f"🧮 Final result: {final_result}")
		return final_result

	except Exception as e:
		print(f"🧮 Error in evaluate_formula: {str(e)}")
		raise ValueError(f"Formula evaluation error: {str(e)}")


# --- helpers ---
def normalize_context(raw):
	"""Ensure the earnings context is a plain dict[str, float].

	Handles cases where frappe.call serializes data as JSON strings or lists of
	pairs. Any invalid shapes return an empty dict instead of raising.
	"""
	try:
		if not raw:
			return {}
		# If it's already a dict-like mapping
		if isinstance(raw, dict):
			mapping = {str(k): _to_float(v) for k, v in raw.items()}
			_augment_with_gross(mapping)
			return mapping
		# Sometimes comes as JSON string
		if isinstance(raw, str):
			try:
				parsed = json.loads(raw)
				mapping = normalize_context(parsed)
				_augment_with_gross(mapping)
				return mapping
			except Exception:
				return {}
		# List of pairs [["B", 20000], ["HRA", 10000]]
		if isinstance(raw, (list, tuple)):
			result = {}
			for item in raw:
				if isinstance(item, (list, tuple)) and len(item) == 2:
					key, val = item
					result[str(key)] = _to_float(val)
				elif isinstance(item, dict):
					# try common shapes
					key = item.get("key") or item.get("abbr") or item.get("name")
					val = item.get("value") or item.get("amount") or item.get("val")
					if key is not None and val is not None:
						result[str(key)] = _to_float(val)
			_augment_with_gross(result)
			return result
		return {}
	except Exception:
		return {}


def _to_float(v):
	try:
		return float(v) if v not in [None, ""] else 0.0
	except Exception:
		return 0.0


def _augment_with_gross(mapping):
	"""Add common aggregate aliases like gross_pay/total_earnings to mapping."""
	try:
		total = sum(_to_float(v) for v in mapping.values())
		mapping.setdefault('gross_pay', total)
		mapping.setdefault('gross', total)
		mapping.setdefault('GROSS_PAY', total)
		mapping.setdefault('total_earnings', total)
		mapping.setdefault('TOTAL_EARNINGS', total)
	except Exception:
		pass


@frappe.whitelist()
def get_earnings_context(salary_structure_name):
	"""
	Get earnings context from a salary structure

	Args:
		salary_structure_name (str): Name of the salary structure

	Returns:
		dict: Earnings context with abbreviations as keys
	"""
	try:
		salary_structure = frappe.get_doc("Salary Structure", salary_structure_name)
		context = {}

		for earning in salary_structure.earnings:
			if earning.abbreviation:
				context[earning.abbreviation] = earning.amount or 0.0

		return {"success": True, "context": context, "message": "Earnings context retrieved successfully"}

	except Exception as e:
		frappe.log_error(f"Error getting earnings context: {str(e)}", "Salary Formula Calculator Error")
		return {"success": False, "context": {}, "message": f"Error retrieving earnings context: {str(e)}"}


@frappe.whitelist()
def calculate_all_deductions(salary_structure_name):
	"""
	Calculate all deductions for a salary structure using their formulas

	Args:
		salary_structure_name (str): Name of the salary structure

	Returns:
		dict: Result with updated deduction amounts
	"""
	try:
		salary_structure = frappe.get_doc("Salary Structure", salary_structure_name)

		# Get earnings context
		earnings_context = {}
		for earning in salary_structure.earnings:
			if earning.abbreviation:
				earnings_context[earning.abbreviation] = earning.amount or 0.0

		# Calculate each deduction
		updated_deductions = []
		for deduction in salary_structure.deductions:
			if deduction.custom_amount_formula:
				try:
					calculated_amount = evaluate_formula(deduction.custom_amount_formula, earnings_context)
					deduction.amount = calculated_amount
					updated_deductions.append({"component": deduction.component, "amount": calculated_amount})
				except Exception as e:
					frappe.log_error(
						f"Error calculating deduction {deduction.component}: {str(e)}",
						"Salary Formula Calculator Error",
					)
					updated_deductions.append(
						{"component": deduction.component, "amount": 0.0, "error": str(e)}
					)

		# Save the document
		salary_structure.save()

		return {
			"success": True,
			"updated_deductions": updated_deductions,
			"message": "All deductions calculated successfully",
		}

	except Exception as e:
		frappe.log_error(f"Error calculating all deductions: {str(e)}", "Salary Formula Calculator Error")
		return {
			"success": False,
			"updated_deductions": [],
			"message": f"Error calculating deductions: {str(e)}",
		}

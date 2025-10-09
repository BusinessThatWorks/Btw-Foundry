import frappe
import json


@frappe.whitelist()
def get_departments_for_items(items=None):
	frappe.log_error("Server Script triggered", "get_departments_for_items")

	if not items:
		frappe.log_error("No items received", "get_departments_for_items")
		return {}

	try:
		# Convert string input to Python list if needed
		if isinstance(items, str):
			frappe.log_error(f"Parsing JSON items: {len(items)} chars", "get_departments_for_items")
			items = json.loads(items)
		elif not isinstance(items, (list, tuple)):
			frappe.log_error(f"Invalid items format: {type(items)}", "get_departments_for_items")
			return {}

		result = {}
		for item_code in items:
			if not item_code:
				continue

			frappe.log_error(f"Searching for: {item_code[:20]}...", "get_departments_for_items")

			# Query Item doctype by item_code (primary method)
			item_doc = frappe.db.get_value(
				"Item",
				filters={"item_code": item_code},
				fieldname=["name", "item_code", "item_name", "custom_department"],
				as_dict=True,
			)

			if item_doc and item_doc.name:
				dept = item_doc.custom_department or ""
				result[item_code] = dept
				frappe.log_error(
					f"Found {item_code[:15]}... → {dept}",
					"get_departments_for_items",
				)
			else:
				# Fallback to item_name if item_code fails
				item_name_doc = frappe.db.get_value(
					"Item",
					filters={"item_name": item_code},
					fieldname=["name", "item_code", "item_name", "custom_department"],
					as_dict=True,
				)
				if item_name_doc and item_name_doc.name:
					dept = item_name_doc.custom_department or ""
					result[item_code] = dept
					frappe.log_error(
						f"Found by name {item_code[:15]}... → {dept}",
						"get_departments_for_items",
					)
				else:
					result[item_code] = ""
					frappe.log_error(
						f"Not found: {item_code[:20]}...",
						"get_departments_for_items",
					)

		frappe.log_error(f"Final result: {len(result)} items", "get_departments_for_items")
		return result

	except Exception as e:
		frappe.log_error(f"Error in get_departments_for_items: {str(e)[:100]}", "get_departments_for_items")
		return {}

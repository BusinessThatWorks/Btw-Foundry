import frappe


@frappe.whitelist(allow_guest=False)
def get_pouring_id_for_shotbrust(item_code=None, custom_date=None, custom_shift_type=None):
	"""
	Fetch the custom_pouring_id for a given item_code, custom_date, and custom_shift_type
	from Stock Entry Detail and Stock Entry, ensuring the stock_entry_type is 'Material Transfer'
	and custom_process_type is 'Shake Out'.

	Args:
	    item_code (str): The item code to filter Stock Entry Detail.
	    custom_date (str): The date to match in Stock Entry.
	    custom_shift_type (str): The shift type to match in Stock Entry.

	Returns:
	    dict: Contains custom_pouring_id if found, or an error message.
	"""
	# Validate inputs
	if not item_code:
		return {"error": "Missing item_code"}

	stock_details = frappe.get_all(
		"Stock Entry Detail", filters={"item_code": item_code}, fields=["custom_pouring_id", "parent"]
	)

	for detail in stock_details:
		entry = frappe.db.get_value(
			"Stock Entry",
			detail.parent,
			["stock_entry_type", "custom_date", "custom_shift_type", "custom_process_type"],
			as_dict=True,
		)

		if (
			entry.stock_entry_type == "Material Transfer"
			and str(entry.custom_date) == str(custom_date)
			and entry.custom_shift_type == custom_shift_type
			and entry.custom_process_type == "Shake Out"
			and detail.custom_pouring_id
		):
			return {"custom_pouring_id": detail.custom_pouring_id}

	return {"error": "No pouring ID found matching all conditions"}

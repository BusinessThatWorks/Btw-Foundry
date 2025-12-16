import frappe


@frappe.whitelist(allow_guest=False)
def get_items_from_shakeout_stock_entries(date=None, shift_type=None):
	debug_log = [
		f"Fetching items for custom_date: {date}, custom_shift_type: {shift_type}, custom_process_type: Shake Out"
	]

	try:
		# Fetch Stock Entries with correct custom filters
		stock_entries = frappe.get_all(
			"Stock Entry",
			filters={
				"stock_entry_type": "Material Transfer",
				"custom_date": date,
				"custom_shift_type": shift_type,
				"custom_process_type": "Shake Out",
			},
			fields=["name"],
		)

		debug_log.append(f"Found Stock Entries: {[se.name for se in stock_entries]}")

		item_codes = []
		for entry in stock_entries:
			details = frappe.get_all(
				"Stock Entry Detail", filters={"parent": entry.name}, fields=["item_code"]
			)
			codes = [d.item_code for d in details]
			debug_log.append(f"Entry {entry.name}: Items - {codes}")
			item_codes.extend(codes)

		unique_items = list(set(item_codes))
		debug_log.append(f"Final unique item list: {unique_items}")

		return unique_items

	except Exception as e:
		frappe.log_error(f"Error in get_items_from_shakeout_stock_entries: {str(e)}")
		return []

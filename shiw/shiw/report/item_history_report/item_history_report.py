import frappe
from frappe.utils import getdate, formatdate
from frappe import _


def execute(filters=None):
	filters = filters or {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def _to_float(value):
	"""Return value as float, or 0.0 if not convertible."""
	try:
		return float(value)
	except Exception:
		return 0.0


def get_columns():
	return [
		{
			"label": "Item Code",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"label": "Item Name",
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Item Group",
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 120,
		},
		{
			"label": "Creation Date",
			"fieldname": "creation",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Current Valuation Rate",
			"fieldname": "current_valuation_rate",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": "Version Date",
			"fieldname": "version_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Previous Valuation Rate",
			"fieldname": "previous_valuation_rate",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": "Change Amount",
			"fieldname": "change_amount",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": "Change %",
			"fieldname": "change_percentage",
			"fieldtype": "Percent",
			"width": 100,
		},
		{
			"label": "Modified By",
			"fieldname": "modified_by",
			"fieldtype": "Data",
			"width": 120,
		},
	]


def get_data(filters):
	# Get finished goods items
	where_conditions = ["i.item_group = 'Finished Goods'", "i.docstatus != 2"]
	params = {}

	if filters.get("from_date"):
		where_conditions.append("i.creation >= %(from_date)s")
		params["from_date"] = getdate(filters.get("from_date"))

	if filters.get("to_date"):
		where_conditions.append("i.creation <= %(to_date)s")
		params["to_date"] = getdate(filters.get("to_date"))

	if filters.get("item_code"):
		where_conditions.append("i.name LIKE %(item_code)s")
		params["item_code"] = f"%{filters.get('item_code')}%"

	if filters.get("item_name"):
		where_conditions.append("i.item_name LIKE %(item_name)s")
		params["item_name"] = f"%{filters.get('item_name')}%"

	where_clause = " AND ".join(where_conditions)

	# Get all finished goods items
	items = frappe.db.sql(
		f"""
		SELECT 
			i.name as item_code,
			i.item_name,
			i.item_group,
			i.creation,
			i.valuation_rate as current_valuation_rate,
			i.modified_by
		FROM `tabItem` i
		WHERE {where_clause}
		ORDER BY i.creation DESC
	""",
		params,
		as_dict=True,
	)

	result = []

	for item in items:
		# Get version history for this item
		versions = get_item_version_history(item["item_code"])

		if versions:
			# Add each version change as a separate row
			for i, version in enumerate(versions):
				change_amount = 0
				change_percentage = 0

				if i > 0:
					# Calculate change from previous version
					prev_version = versions[i - 1]
					current_rate = _to_float(version["valuation_rate"])
					prev_rate = _to_float(prev_version["valuation_rate"])
					change_amount = current_rate - prev_rate
					if prev_rate > 0:
						change_percentage = (change_amount / prev_rate) * 100

				result.append(
					{
						"item_code": item["item_code"],
						"item_name": item["item_name"],
						"item_group": item["item_group"],
						"creation": item["creation"],
						"current_valuation_rate": item["current_valuation_rate"],
						"version_date": version["creation"],
						"previous_valuation_rate": _to_float(version["valuation_rate"]),
						"change_amount": change_amount,
						"change_percentage": change_percentage,
						"modified_by": version["modified_by"],
					}
				)
		else:
			# No version history, just show current item
			result.append(
				{
					"item_code": item["item_code"],
					"item_name": item["item_name"],
					"item_group": item["item_group"],
					"creation": item["creation"],
					"current_valuation_rate": _to_float(item["current_valuation_rate"]),
					"version_date": item["creation"],
					"previous_valuation_rate": _to_float(item["current_valuation_rate"]),
					"change_amount": 0,
					"change_percentage": 0,
					"modified_by": item["modified_by"],
				}
			)

	return result


def get_item_version_history(item_code):
	"""Get version history for an item's valuation_rate changes"""
	try:
		# Get all versions of the item
		versions = frappe.get_all(
			"Version",
			filters={"ref_doctype": "Item", "docname": item_code},
			fields=["name", "creation", "modified_by", "data"],
			order_by="creation desc",
		)

		version_data = []

		for version in versions:
			try:
				# Parse the version data
				import json

				data = json.loads(version.data) if version.data else {}

				# Check if valuation_rate changed in this version
				changed_fields = data.get("changed", [])
				valuation_rate_changed = False
				new_valuation_rate = None

				for field in changed_fields:
					if field[0] == "valuation_rate":
						valuation_rate_changed = True
						new_valuation_rate = field[2]  # New value
						break

				if valuation_rate_changed and new_valuation_rate is not None:
					version_data.append(
						{
							"creation": version.creation,
							"valuation_rate": new_valuation_rate,
							"modified_by": version.modified_by,
						}
					)
			except:
				continue

		return version_data

	except Exception as e:
		frappe.log_error(f"Error getting version history for {item_code}: {str(e)}")
		return []

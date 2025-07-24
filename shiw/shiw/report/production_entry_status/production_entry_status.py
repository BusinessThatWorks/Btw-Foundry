# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# import frappe
# from frappe.utils import getdate


# def execute(filters=None):
# 	from_date = getdate(filters.get("from_date"))
# 	to_date = getdate(filters.get("to_date"))

# 	columns = [
# 		{"label": "Doctype", "fieldname": "doctype", "fieldtype": "Data", "width": 200},
# 		{"label": "Owner (User ID)", "fieldname": "owner", "fieldtype": "Data", "width": 200},
# 		{"label": "Full Name", "fieldname": "full_name", "fieldtype": "Data", "width": 200},
# 		{"label": "Count", "fieldname": "count", "fieldtype": "Int", "width": 100},
# 	]

# 	data = []

# 	# Filter only SHIW module doctypes
# 	doctypes = [
# 		d.name
# 		for d in frappe.get_all("DocType", filters={"module": "shiw", "istable": 0, "issingle": 0})
# 		if frappe.db.has_table(d.name)
# 	]

# 	for doctype in doctypes:
# 		try:
# 			result = frappe.db.sql(
# 				f"""
#                 SELECT
#                     %(doctype)s AS doctype,
#                     d.owner AS owner,
#                     u.full_name AS full_name,
#                     COUNT(*) AS count
#                 FROM `tab{doctype}` d
#                 JOIN `tabUser` u ON u.name = d.owner
#                 WHERE DATE(d.creation) BETWEEN %(from_date)s AND %(to_date)s
#                 GROUP BY d.owner, u.full_name
#             """,
# 				{"from_date": from_date, "to_date": to_date, "doctype": doctype},
# 				as_dict=True,
# 			)

# 			if result:
# 				data.extend(result)

# 		except Exception as e:
# 			frappe.logger().warning(f"⚠ Skipped {doctype}: {str(e)}")
# 			continue

# 	return columns, data


import frappe
from frappe.utils import getdate


def execute(filters=None):
	from_date = getdate(filters.get("from_date"))
	to_date = getdate(filters.get("to_date"))

	columns = [
		{"label": "Doctype", "fieldname": "doctype", "fieldtype": "Data", "width": 300},
		{"label": "Count", "fieldname": "count", "fieldtype": "Int", "width": 120},
	]

	data = []

	# Get all DocTypes from the SHIW module
	doctypes = [
		d.name
		for d in frappe.get_all("DocType", filters={"module": "shiw", "istable": 0, "issingle": 0})
		if frappe.db.has_table(d.name)
	]

	for doctype in doctypes:
		try:
			count = frappe.db.count(doctype, {"creation": ["between", [from_date, to_date]]})

			if count:
				data.append({"doctype": doctype, "count": count})

		except Exception as e:
			frappe.logger().warning(f"⚠ Error in {doctype}: {str(e)}")

	return columns, data

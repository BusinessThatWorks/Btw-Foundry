# # Copyright (c) 2025, beetashoke chakraborty and contributors
# # For license information, please see license.txt

# # import frappe


# # def execute(filters=None):
# # 	columns, data = [], []
# # 	return columns, data


# import frappe


# def execute(filters=None):
# 	columns = [
# 		{
# 			"label": "Pouring ID",
# 			"fieldname": "pouring_id",
# 			"fieldtype": "Link",
# 			"options": "Pouring",
# 			"width": 150,
# 		},
# 		{"label": "Moulding System", "fieldname": "moulding_system", "fieldtype": "Data", "width": 150},
# 		{
# 			"label": "Tooling ID",
# 			"fieldname": "tooling_id",
# 			"fieldtype": "Link",
# 			"options": "New Tooling",
# 			"width": 150,
# 		},
# 		{"label": "Tooling", "fieldname": "tooling_from_mould_table", "fieldtype": "Data", "width": 150},
# 		{
# 			"label": "Item Code",
# 			"fieldname": "item_code",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 200,
# 		},
# 	]

# 	data = []

# 	pouring_docs = frappe.get_all("Pouring", fields=["name"])
# 	for pouring in pouring_docs:
# 		doc = frappe.get_doc("Pouring", pouring.name)

# 		for row in doc.mould_batch:
# 			tooling_id = row.tooling_id
# 			moulding_system = row.moulding_system
# 			mould_no = row.mould_no

# 			if not (tooling_id and moulding_system and mould_no):
# 				continue

# 			# try:
# 			# 	mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			# except:
# 			# 	continue  # Skip if not found

# 			try:
# 				mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			except frappe.DoesNotExistError:
# 				frappe.msgprint(
# 					f"❌ Mould Doc not found → Pouring ID: {pouring.name}, Doctype: {moulding_system}, Name: {mould_no}"
# 				)
# 				continue
# 			except Exception as e:
# 				frappe.msgprint(f"⚠️ Unexpected Error in Pouring {pouring.name}: {e}")
# 				continue

# 			for mt_row in mould_doc.mould_table:
# 				if mt_row.tooling != tooling_id:
# 					continue

# 				tooling_from_mould_table = mt_row.tooling

# 				# Fetch New Tooling Doc
# 				tooling_doc = frappe.get_doc("New Tooling", tooling_id)

# 				for detail_row in tooling_doc.details_table:
# 					item_raw = detail_row.item
# 					if not item_raw:
# 						continue

# 					# Parse item code (remove "PTRN - ", and strip suffix)
# 					item_code = item_raw.replace("PTRN - ", "").rsplit("-", 1)[0].strip()

# 					data.append(
# 						{
# 							"pouring_id": pouring.name,
# 							"moulding_system": moulding_system,
# 							"tooling_id": tooling_id,
# 							"tooling_from_mould_table": tooling_from_mould_table,
# 							"item_code": item_code,
# 						}
# 					)

# 	return columns, data


# import frappe


# def flt(val):
# 	return float(val) if val not in [None, "", 0] else 0.0


# def execute(filters=None):
# 	columns = [
# 		{
# 			"label": "Pouring ID",
# 			"fieldname": "pouring_id",
# 			"fieldtype": "Link",
# 			"options": "Pouring",
# 			"width": 150,
# 		},
# 		{"label": "Moulding System", "fieldname": "moulding_system", "fieldtype": "Data", "width": 150},
# 		{
# 			"label": "Tooling ID",
# 			"fieldname": "tooling_id",
# 			"fieldtype": "Link",
# 			"options": "New Tooling",
# 			"width": 150,
# 		},
# 		{"label": "Tooling", "fieldname": "tooling_from_mould_table", "fieldtype": "Data", "width": 150},
# 		{
# 			"label": "Item Code",
# 			"fieldname": "item_code",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 200,
# 		},
# 		{"label": "Heat", "fieldname": "heat", "fieldtype": "Link", "options": "Heat", "width": 150},
# 		{
# 			"label": "Charge Mix Valuation",
# 			"fieldname": "charge_mix_value",
# 			"fieldtype": "Currency",
# 			"width": 180,
# 		},
# 	]

# 	data = []

# 	pouring_docs = frappe.get_all("Pouring", fields=["name"])
# 	for pouring in pouring_docs:
# 		doc = frappe.get_doc("Pouring", pouring.name)

# 		for row in doc.mould_batch:
# 			tooling_id = row.tooling_id
# 			moulding_system = row.moulding_system
# 			mould_no = row.mould_no
# 			heat = row.heat_no
# 			charge_mix_value = 0.0

# 			if heat:
# 				try:
# 					heat_doc = frappe.get_doc("Heat", heat)
# 					charge_mix_value = flt(heat_doc.total_charge_mix_valuation)
# 				except:
# 					frappe.msgprint(f"⚠️ Heat doc not found: {heat}")

# 			if not (tooling_id and moulding_system and mould_no):
# 				continue

# 			try:
# 				mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			except frappe.DoesNotExistError:
# 				frappe.msgprint(
# 					f"❌ Mould Doc not found → Pouring ID: {pouring.name}, Doctype: {moulding_system}, Name: {mould_no}"
# 				)
# 				continue
# 			except Exception as e:
# 				frappe.msgprint(f"⚠️ Unexpected Error in Pouring {pouring.name}: {e}")
# 				continue

# 			for mt_row in mould_doc.mould_table:
# 				if mt_row.tooling != tooling_id:
# 					continue

# 				tooling_from_mould_table = mt_row.tooling

# 				try:
# 					tooling_doc = frappe.get_doc("New Tooling", tooling_id)
# 				except:
# 					frappe.msgprint(f"⚠️ Tooling doc not found: {tooling_id}")
# 					continue

# 				for detail_row in tooling_doc.details_table:
# 					item_raw = detail_row.item
# 					if not item_raw:
# 						continue

# 					# Parse item code (remove "PTRN - ", and suffix)
# 					item_code = item_raw.replace("PTRN - ", "").rsplit("-", 1)[0].strip()

# 					data.append(
# 						{
# 							"pouring_id": pouring.name,
# 							"moulding_system": moulding_system,
# 							"tooling_id": tooling_id,
# 							"tooling_from_mould_table": tooling_from_mould_table,
# 							"item_code": item_code,
# 							"heat": heat,
# 							"charge_mix_value": charge_mix_value,
# 						}
# 					)

# 	return columns, data

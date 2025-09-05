# # Copyright (c) 2025, beetashoke chakraborty and contributors
# # For license information, please see license.txt

# # import frappe


# # def execute(filters=None):
# # 	columns, data = [], []
# # 	return columns, data


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
# 		{"label": "Mould Batch No", "fieldname": "mould_no", "fieldtype": "Data", "width": 150},
# 		{
# 			"label": "Tooling ID",
# 			"fieldname": "tooling_id",
# 			"fieldtype": "Link",
# 			"options": "New Tooling",
# 			"width": 150,
# 		},
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
# 			"width": 150,
# 		},
# 		{
# 			"label": "Charge Mix Item",
# 			"fieldname": "charge_item",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Charge Mix Weight", "fieldname": "charge_weight", "fieldtype": "Float", "width": 120},
# 		{"label": "Charge Mix Rate", "fieldname": "charge_item_rate", "fieldtype": "Currency", "width": 120},
# 		{"label": "Charge Mix Amount", "fieldname": "charge_amount", "fieldtype": "Currency", "width": 130},
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
# 			charge_mix_table = []

# 			if not (tooling_id and moulding_system and mould_no):
# 				continue

# 			# Load mould doc
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

# 			# Match tooling inside mould table
# 			for mt_row in mould_doc.mould_table:
# 				if mt_row.tooling != tooling_id:
# 					continue

# 				try:
# 					tooling_doc = frappe.get_doc("New Tooling", tooling_id)
# 				except:
# 					frappe.msgprint(f"⚠️ Tooling doc not found: {tooling_id}")
# 					continue

# 				for detail_row in tooling_doc.details_table:
# 					item_raw = detail_row.item
# 					if not item_raw:
# 						continue

# 					# Clean item code
# 					item_code = item_raw.replace("PTRN - ", "").rsplit("-", 1)[0].strip()

# 					# Load heat and charge mix details
# 					if heat:
# 						try:
# 							heat_doc = frappe.get_doc("Heat", heat)
# 							charge_mix_value = flt(heat_doc.total_charge_mix_valuation)
# 							charge_mix_table = heat_doc.get("charge_mix_component_item") or []
# 						except:
# 							frappe.msgprint(f"⚠️ Heat doc not found: {heat}")

# 					# If no charge mix component rows, still show row
# 					if not charge_mix_table:
# 						data.append(
# 							{
# 								"pouring_id": pouring.name,
# 								"moulding_system": moulding_system,
# 								"mould_no": mould_no,
# 								"tooling_id": tooling_id,
# 								"item_code": item_code,
# 								"heat": heat,
# 								"charge_mix_value": charge_mix_value,
# 								"charge_item": "",
# 								"charge_weight": 0,
# 								"charge_item_rate": 0,
# 								"charge_amount": 0,
# 							}
# 						)
# 					else:
# 						for mix_row in charge_mix_table:
# 							data.append(
# 								{
# 									"pouring_id": pouring.name,
# 									"moulding_system": moulding_system,
# 									"mould_no": mould_no,
# 									"tooling_id": tooling_id,
# 									"item_code": item_code,
# 									"heat": heat,
# 									"charge_mix_value": charge_mix_value,
# 									"charge_item": mix_row.item,
# 									"charge_weight": flt(mix_row.weight),
# 									"charge_item_rate": flt(mix_row.item_rate),
# 									"charge_amount": flt(mix_row.amount),
# 								}
# 							)

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
# 			"width": 140,
# 		},
# 		{"label": "Moulding System", "fieldname": "moulding_system", "fieldtype": "Data", "width": 130},
# 		{"label": "Mould Batch No", "fieldname": "mould_batch_no", "fieldtype": "Data", "width": 130},
# 		{
# 			"label": "Tooling ID",
# 			"fieldname": "tooling_id",
# 			"fieldtype": "Link",
# 			"options": "New Tooling",
# 			"width": 130,
# 		},
# 		{
# 			"label": "Item Code",
# 			"fieldname": "item_code",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Heat", "fieldname": "heat", "fieldtype": "Link", "options": "Heat", "width": 100},
# 		{
# 			"label": "Charge Mix Valuation",
# 			"fieldname": "charge_mix_value",
# 			"fieldtype": "Currency",
# 			"width": 150,
# 		},
# 		{
# 			"label": "Charge Mix Item",
# 			"fieldname": "charge_item",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Charge Mix Weight", "fieldname": "charge_weight", "fieldtype": "Float", "width": 130},
# 		{"label": "Charge Mix Rate", "fieldname": "charge_item_rate", "fieldtype": "Currency", "width": 130},
# 		{"label": "Charge Mix Amount", "fieldname": "charge_amount", "fieldtype": "Currency", "width": 130},
# 		{
# 			"label": "Consumption Item",
# 			"fieldname": "cons_item",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},
# 		{"label": "Consumption Weight (kg)", "fieldname": "cons_weight", "fieldtype": "Float", "width": 150},
# 		{"label": "Consumption Rate", "fieldname": "cons_rate", "fieldtype": "Currency", "width": 130},
# 		{"label": "Consumption Amount", "fieldname": "cons_amount", "fieldtype": "Currency", "width": 130},
# 		{
# 			"label": "Total Consumption Valuation",
# 			"fieldname": "total_consumption",
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
# 			charge_mix_table = []
# 			total_consumption = 0.0
# 			consumption_table = []

# 			if not (tooling_id and moulding_system and mould_no):
# 				continue

# 			# Load mould batch doc
# 			try:
# 				mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			except:
# 				continue

# 			# Load charge mix data
# 			if heat:
# 				try:
# 					heat_doc = frappe.get_doc("Heat", heat)
# 					charge_mix_value = flt(heat_doc.total_charge_mix_valuation)
# 					charge_mix_table = heat_doc.get("charge_mix_component_item") or []
# 				except:
# 					pass

# 			# Load consumption info
# 			total_consumption = flt(mould_doc.total_consumption_valuation)
# 			consumption_table = mould_doc.get("consumption_mould") or []

# 			# Match tooling in mould table
# 			for mt_row in mould_doc.mould_table:
# 				if mt_row.tooling != tooling_id:
# 					continue

# 				try:
# 					tooling_doc = frappe.get_doc("New Tooling", tooling_id)
# 				except:
# 					continue

# 				for detail_row in tooling_doc.details_table:
# 					item_raw = detail_row.item
# 					if not item_raw:
# 						continue
# 					item_code = item_raw.replace("PTRN - ", "").rsplit("-", 1)[0].strip()

# 					# Combine charge mix and consumption combinations
# 					if not charge_mix_table:
# 						charge_mix_table = [{"item": "", "weight": 0, "item_rate": 0, "amount": 0}]
# 					if not consumption_table:
# 						consumption_table = [
# 							{"item": "", "uom": "", "weight_in_kg": 0, "rate": 0, "amount": 0}
# 						]

# 					for mix_row in charge_mix_table:
# 						for cons_row in consumption_table:
# 							data.append(
# 								{
# 									"pouring_id": pouring.name,
# 									"moulding_system": moulding_system,
# 									"mould_batch_no": mould_no,
# 									"tooling_id": tooling_id,
# 									"item_code": item_code,
# 									"heat": heat,
# 									"charge_mix_value": charge_mix_value,
# 									"charge_item": mix_row.get("item"),
# 									"charge_weight": flt(mix_row.get("weight")),
# 									"charge_item_rate": flt(mix_row.get("item_rate")),
# 									"charge_amount": flt(mix_row.get("amount")),
# 									"cons_item": cons_row.get("item"),
# 									"uom": cons_row.get("uom"),
# 									"cons_weight": flt(cons_row.get("weight_in_kg")),
# 									"cons_rate": flt(cons_row.get("rate")),
# 									"cons_amount": flt(cons_row.get("amount")),
# 									"total_consumption": total_consumption,
# 								}
# 							)

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
# 			"width": 140,
# 		},
# 		{"label": "Moulding System", "fieldname": "moulding_system", "fieldtype": "Data", "width": 130},
# 		{"label": "Mould Batch No", "fieldname": "mould_batch_no", "fieldtype": "Data", "width": 130},
# 		{
# 			"label": "Tooling ID",
# 			"fieldname": "tooling_id",
# 			"fieldtype": "Link",
# 			"options": "New Tooling",
# 			"width": 130,
# 		},
# 		{
# 			"label": "Item Code",
# 			"fieldname": "item_code",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Heat", "fieldname": "heat", "fieldtype": "Link", "options": "Heat", "width": 100},
# 		{
# 			"label": "Charge Mix Valuation",
# 			"fieldname": "charge_mix_value",
# 			"fieldtype": "Currency",
# 			"width": 150,
# 		},
# 		{
# 			"label": "Charge Mix Item",
# 			"fieldname": "charge_item",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "Charge Mix Weight", "fieldname": "charge_weight", "fieldtype": "Float", "width": 130},
# 		{"label": "Charge Mix Rate", "fieldname": "charge_item_rate", "fieldtype": "Currency", "width": 130},
# 		{"label": "Charge Mix Amount", "fieldname": "charge_amount", "fieldtype": "Currency", "width": 130},
# 		{
# 			"label": "Consumption Item",
# 			"fieldname": "cons_item",
# 			"fieldtype": "Link",
# 			"options": "Item",
# 			"width": 150,
# 		},
# 		{"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},
# 		{"label": "Consumption Weight (kg)", "fieldname": "cons_weight", "fieldtype": "Float", "width": 150},
# 		{"label": "Consumption Rate", "fieldname": "cons_rate", "fieldtype": "Currency", "width": 130},
# 		{"label": "Consumption Amount", "fieldname": "cons_amount", "fieldtype": "Currency", "width": 130},
# 		{
# 			"label": "Total Consumption Valuation",
# 			"fieldname": "total_consumption",
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

# 			if not (tooling_id and moulding_system and mould_no):
# 				continue

# 			try:
# 				mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			except:
# 				continue

# 			# Load Charge Mix from Heat
# 			charge_mix_value = 0.0
# 			charge_mix_table = []
# 			if heat:
# 				try:
# 					heat_doc = frappe.get_doc("Heat", heat)
# 					charge_mix_value = flt(heat_doc.total_charge_mix_valuation)
# 					charge_mix_table = heat_doc.get("charge_mix_component_item") or []
# 				except:
# 					pass

# 			# Load Consumption
# 			total_consumption = flt(mould_doc.total_consumption_valuation)
# 			consumption_table = mould_doc.get("consumption_mould") or []

# 			# Match tooling with mould_table
# 			for mt_row in mould_doc.get("mould_table", []):
# 				if mt_row.tooling != tooling_id:
# 					continue

# 				try:
# 					tooling_doc = frappe.get_doc("New Tooling", tooling_id)
# 				except:
# 					continue

# 				for detail_row in tooling_doc.details_table:
# 					item_raw = detail_row.item
# 					if not item_raw:
# 						continue
# 					item_code = item_raw.replace("PTRN - ", "").rsplit("-", 1)[0].strip()

# 					if not charge_mix_table:
# 						charge_mix_table = [{"item": "", "weight": 0, "item_rate": 0, "amount": 0}]
# 					if not consumption_table:
# 						consumption_table = [
# 							{"item": "", "uom": "", "weight_in_kg": 0, "rate": 0, "amount": 0}
# 						]

# 					for mix_row in charge_mix_table:
# 						for cons_row in consumption_table:
# 							data.append(
# 								{
# 									"pouring_id": pouring.name,
# 									"moulding_system": moulding_system,
# 									"mould_batch_no": mould_no,
# 									"tooling_id": tooling_id,
# 									"item_code": item_code,
# 									"heat": heat,
# 									"charge_mix_value": charge_mix_value,
# 									"charge_item": mix_row.get("item"),
# 									"charge_weight": flt(mix_row.get("weight")),
# 									"charge_item_rate": flt(mix_row.get("item_rate")),
# 									"charge_amount": flt(mix_row.get("amount")),
# 									"cons_item": cons_row.get("item"),
# 									"uom": cons_row.get("uom"),
# 									"cons_weight": flt(cons_row.get("weight_in_kg")),
# 									"cons_rate": flt(cons_row.get("rate")),
# 									"cons_amount": flt(cons_row.get("amount")),
# 									"total_consumption": total_consumption,
# 								}
# 							)

# 	return columns, data

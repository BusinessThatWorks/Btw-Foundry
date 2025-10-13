# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class Pouring(Document):
# 	pass


# import frappe
# from frappe.model.document import Document


# def flt(val):
# 	return float(val) if val not in [None, ""] else 0.0


# class Pouring(Document):
# 	def on_submit(self):
# 		tooling_qty_map = {}
# 		updated_moulds = []
# 		item_rows = []
# 		grade_return_map = {}  # { grade: { total_qty: float, tooling_ids: set } }

# 		# Validate warehouses
# 		pouring_warehouse = "Pouring - SHIW"
# 		foundry_return_warehouse = "Estimated Foundry Return  - SHIW"

# 		if not frappe.db.exists("Warehouse", pouring_warehouse):
# 			frappe.throw(f"Warehouse '{pouring_warehouse}' does not exist")
# 		if not frappe.db.exists("Warehouse", foundry_return_warehouse):
# 			frappe.throw(f"Warehouse '{foundry_return_warehouse}' does not exist")

# 		# Step 1: Aggregate total pouring quantity per tooling
# 		for row in self.mould_batch:
# 			tooling_id = row.tooling_id
# 			qty = flt(row.pouring_quantity)
# 			if tooling_id:
# 				tooling_qty_map[tooling_id] = tooling_qty_map.get(tooling_id, 0) + qty

# 		# Step 2: Validate and reduce mould quantities
# 		for row in self.mould_batch:
# 			tooling_id = row.tooling_id
# 			moulding_system = row.moulding_system
# 			mould_no = row.mould_no
# 			qty = flt(row.pouring_quantity)
# 			if not (tooling_id and moulding_system and mould_no):
# 				continue
# 			mould_doc = frappe.get_doc(moulding_system, mould_no)
# 			for table_row in mould_doc.mould_table:
# 				if table_row.tooling == tooling_id:
# 					available = flt(table_row.mould_quantity)
# 					if qty > available:
# 						frappe.throw(
# 							f"Pouring quantity ({qty}) exceeds available mould quantity ({available}) "
# 							f"for tooling {tooling_id}"
# 						)
# 					table_row.mould_quantity = available - qty
# 					updated_moulds.append(
# 						f"🛠️ {tooling_id}: {available} → {table_row.mould_quantity} in {mould_no}"
# 					)
# 					break
# 			mould_doc.save(ignore_permissions=True)

# 		if updated_moulds:
# 			frappe.msgprint("\n".join(["✅ Mould Quantities Updated:", *updated_moulds]))

# 		# Step 3: Build item list from tooling details and track foundry return by grade
# 		for tooling_id, qty_total in tooling_qty_map.items():
# 			tooling_doc = frappe.get_doc("New Tooling", tooling_id)
# 			grade = tooling_doc.grade or ""
# 			foundry_return_weight = flt(tooling_doc.runner_riser_weight)

# 			frappe.log_error(
# 				f"Tooling: {tooling_id}, Grade: {grade}, Runner Riser Weight: {foundry_return_weight}, Qty Total: {qty_total}",
# 				"Pouring Debug",
# 			)

# 			for d in tooling_doc.details_table:
# 				item_code = (d.item or "").replace("PTRN - ", "").rsplit("-", 1)[0].strip()
# 				cavity = flt(d.cavity)

# 				if not item_code:
# 					continue

# 				item_qty = qty_total * cavity

# 				if not frappe.db.exists("Item", item_code):
# 					frappe.throw(f"Item '{item_code}' does not exist for tooling {tooling_id}")
# 				if not frappe.db.get_value("Item", item_code, "is_stock_item"):
# 					frappe.throw(f"Item '{item_code}' is not a stock item for tooling {tooling_id}")

# 				rate = 0.0
# 				price_list = frappe.get_all(
# 					"Item Price", filters={"item_code": item_code}, fields=["price_list_rate"], limit=1
# 				)
# 				if price_list:
# 					rate = flt(price_list[0].price_list_rate)

# 				item_row = {
# 					"s_warehouse": "",
# 					"t_warehouse": pouring_warehouse,
# 					"item_code": item_code,
# 					"qty": item_qty,
# 					"basic_rate": rate,
# 					"custom_pouring_id": self.name,
# 					"is_finished_item": 1,
# 					"custom_grade": grade,
# 					"custom_estimated_foundry_return": foundry_return_weight,
# 					"custom_tooling_id": tooling_id,
# 				}

# 				item_rows.append(item_row)

# 				if grade:
# 					return_qty = item_qty * foundry_return_weight
# 					if return_qty < 0:
# 						frappe.throw(
# 							f"Negative foundry return quantity ({return_qty}) for grade {grade} "
# 							f"from tooling {tooling_id} (item_qty: {item_qty}, foundry_return_weight: {foundry_return_weight})"
# 						)
# 					if grade not in grade_return_map:
# 						grade_return_map[grade] = {"total_qty": 0.0, "tooling_ids": set()}
# 					grade_return_map[grade]["total_qty"] = grade_return_map[grade]["total_qty"] + return_qty
# 					grade_return_map[grade]["tooling_ids"].add(tooling_id)

# 		# Step 4: Add foundry return items
# 		for grade, data in grade_return_map.items():
# 			total_return_qty = data["total_qty"]
# 			tooling_ids = data["tooling_ids"]

# 			# Get foundry return item from Grade Master
# 			grade_master = frappe.get_doc("Grade Master", grade)
# 			if not grade_master:
# 				frappe.throw(f"Grade Master document not found for grade: {grade}")

# 			item_code = grade_master.foundry_return
# 			if not item_code:
# 				frappe.throw(f"Foundry Return field is empty in Grade Master for grade: {grade}")

# 			if not frappe.db.exists("Item", item_code):
# 				frappe.throw(
# 					f"Item '{item_code}' does not exist for grade {grade} (tooling: {', '.join(tooling_ids)})"
# 				)
# 			if not frappe.db.get_value("Item", item_code, "is_stock_item"):
# 				frappe.throw(
# 					f"Item '{item_code}' is not a stock item for grade {grade} (tooling: {', '.join(tooling_ids)})"
# 				)

# 			if total_return_qty <= 0:
# 				frappe.throw(
# 					f"Non-positive foundry return quantity ({total_return_qty}) for item {item_code} "
# 					f"(grade: {grade}, tooling: {', '.join(tooling_ids)})"
# 				)

# 			item_rows.append(
# 				{
# 					"s_warehouse": "",
# 					"t_warehouse": foundry_return_warehouse,
# 					"item_code": item_code,
# 					"qty": total_return_qty,
# 					"basic_rate": 0.0,
# 					"custom_pouring_id": self.name,
# 					"is_finished_item": 1,
# 					"custom_grade": grade,
# 					"custom_tooling_id": ", ".join(tooling_ids),
# 				}
# 			)

# 		# ✅ Aggregation of identical items
# 		aggregated_items = {}
# 		for row in item_rows:
# 			key = (row["item_code"], row["s_warehouse"], row["t_warehouse"], row["custom_grade"])
# 			if key not in aggregated_items:
# 				aggregated_items[key] = row.copy()
# 			else:
# 				aggregated_items[key]["qty"] = aggregated_items[key]["qty"] + row["qty"]

# 		item_rows = list(aggregated_items.values())

# 		# Step 5: Create Stock Entry
# 		if item_rows:
# 			debug_rows = []
# 			fractional_errors = []

# 			for i, row in enumerate(item_rows, start=1):
# 				item_info = frappe.db.get_value(
# 					"Item", row["item_code"], ["item_name", "stock_uom"], as_dict=True
# 				)

# 				item_name = item_info.item_name if item_info else row["item_code"]
# 				uom = item_info.stock_uom if item_info else "N/A"
# 				tooling_id = row.get("custom_tooling_id") or "N/A"

# 				debug_rows.append(
# 					f"Row {i}: {item_name} ({row['item_code']}) | Qty {row['qty']} | UOM {uom} | 🔧 Tooling: {tooling_id}"
# 				)

# 				if uom in ["Nos", "PCS", "Piece", "Unit"] and not float(row["qty"]).is_integer():
# 					fractional_errors.append(
# 						f"❌ Row {i}: {item_name} ({row['item_code']}) has fractional Qty {row['qty']} {uom} | Tooling: {tooling_id}"
# 					)

# 			frappe.msgprint("<br>".join(debug_rows))
# 			frappe.log_error("\n".join(debug_rows), "Debug Pouring Stock Entry Rows")

# 			if fractional_errors:
# 				frappe.throw("<br>".join(fractional_errors))

# 			se = frappe.get_doc(
# 				{
# 					"doctype": "Stock Entry",
# 					"stock_entry_type": "Pouring",
# 					"custom_process_type": "Pouring",
# 					"items": item_rows,
# 					"custom_date": self.date,
# 					"custom_shift_type": self.shift_type,
# 				}
# 			)
# 			se.insert()
# 			se.submit()
# 			self.db_set("linked_stock_entry", se.name)
# 			frappe.msgprint(f"✅ Stock Entry {se.name} created and linked.")
# 		else:
# 			frappe.msgprint("⚠️ No valid items found for Stock Entry.")


import frappe
from frappe.model.document import Document


def flt(val):
	return float(val) if val not in [None, ""] else 0.0


class Pouring(Document):
	def on_submit(self):
		tooling_qty_map = {}
		updated_moulds = []
		item_rows = []
		grade_return_map = {}  # { grade: { total_qty: float, tooling_ids: set } }

		# Validate warehouses
		pouring_warehouse = "Pouring - SHIW"
		foundry_return_warehouse = "Estimated Foundry Return  - SHIW"

		if not frappe.db.exists("Warehouse", pouring_warehouse):
			frappe.throw(f"Warehouse '{pouring_warehouse}' does not exist")
		if not frappe.db.exists("Warehouse", foundry_return_warehouse):
			frappe.throw(f"Warehouse '{foundry_return_warehouse}' does not exist")

		# Step 1: Aggregate total pouring quantity per tooling
		for row in self.mould_batch:
			tooling_id = row.tooling_id
			qty = flt(row.pouring_quantity)
			if tooling_id:
				tooling_qty_map[tooling_id] = tooling_qty_map.get(tooling_id, 0) + qty

		# Step 2: Validate and reduce mould quantities
		for row in self.mould_batch:
			tooling_id = row.tooling_id
			moulding_system = row.moulding_system
			mould_no = row.mould_no
			qty = flt(row.pouring_quantity)
			if not (tooling_id and moulding_system and mould_no):
				continue
			mould_doc = frappe.get_doc(moulding_system, mould_no)
			for table_row in mould_doc.mould_table:
				if table_row.tooling == tooling_id:
					available = flt(table_row.mould_quantity)
					if qty > available:
						frappe.throw(
							f"Pouring quantity ({qty}) exceeds available mould quantity ({available}) "
							f"for tooling {tooling_id}"
						)
					table_row.mould_quantity = available - qty
					updated_moulds.append(
						f"🛠️ {tooling_id}: {available} → {table_row.mould_quantity} in {mould_no}"
					)
					break
			mould_doc.save(ignore_permissions=True)

		if updated_moulds:
			frappe.msgprint("\n".join(["✅ Mould Quantities Updated:", *updated_moulds]))

		# Step 3: Build item list from tooling details and track foundry return by grade
		for tooling_id, qty_total in tooling_qty_map.items():
			tooling_doc = frappe.get_doc("New Tooling", tooling_id)
			grade = tooling_doc.grade or ""
			foundry_return_weight = flt(tooling_doc.runner_riser_weight)

			frappe.log_error(
				f"Tooling: {tooling_id}, Grade: {grade}, Runner Riser Weight: {foundry_return_weight}, Qty Total: {qty_total}",
				"Pouring Debug",
			)

			for d in tooling_doc.details_table:
				item_code = (d.item or "").replace("PTRN - ", "").rsplit("-", 1)[0].strip()
				cavity = flt(d.cavity)

				if not item_code:
					continue

				item_qty = qty_total * cavity

				if not frappe.db.exists("Item", item_code):
					frappe.throw(f"Item '{item_code}' does not exist for tooling {tooling_id}")
				if not frappe.db.get_value("Item", item_code, "is_stock_item"):
					frappe.throw(f"Item '{item_code}' is not a stock item for tooling {tooling_id}")

				rate = 0.0
				price_list = frappe.get_all(
					"Item Price", filters={"item_code": item_code}, fields=["price_list_rate"], limit=1
				)
				if price_list:
					rate = flt(price_list[0].price_list_rate)

				item_row = {
					"s_warehouse": "",
					"t_warehouse": pouring_warehouse,
					"item_code": item_code,
					"qty": item_qty,
					"basic_rate": rate,
					"custom_pouring_id": self.name,
					"is_finished_item": 1,
					"custom_grade": grade,
					"custom_estimated_foundry_return": foundry_return_weight,
					"custom_tooling_id": tooling_id,
				}

				item_rows.append(item_row)

				if grade:
					return_qty = item_qty * foundry_return_weight
					if return_qty < 0:
						frappe.throw(
							f"Negative foundry return quantity ({return_qty}) for grade {grade} "
							f"from tooling {tooling_id} (item_qty: {item_qty}, foundry_return_weight: {foundry_return_weight})"
						)
					if grade not in grade_return_map:
						grade_return_map[grade] = {"total_qty": 0.0, "tooling_ids": set()}
					grade_return_map[grade]["total_qty"] = grade_return_map[grade]["total_qty"] + return_qty
					grade_return_map[grade]["tooling_ids"].add(tooling_id)

		# Step 4: Add foundry return items
		for grade, data in grade_return_map.items():
			total_return_qty = data["total_qty"]
			tooling_ids = data["tooling_ids"]

			# Get foundry return item from Grade Master
			grade_master = frappe.get_doc("Grade Master", grade)
			if not grade_master:
				frappe.throw(f"Grade Master document not found for grade: {grade}")

			item_code = grade_master.foundry_return
			if not item_code:
				frappe.throw(f"Foundry Return field is empty in Grade Master for grade: {grade}")

			if not frappe.db.exists("Item", item_code):
				frappe.throw(
					f"Item '{item_code}' does not exist for grade {grade} (tooling: {', '.join(tooling_ids)})"
				)
			if not frappe.db.get_value("Item", item_code, "is_stock_item"):
				frappe.throw(
					f"Item '{item_code}' is not a stock item for grade {grade} (tooling: {', '.join(tooling_ids)})"
				)

			if total_return_qty <= 0:
				frappe.throw(
					f"Non-positive foundry return quantity ({total_return_qty}) for item {item_code} "
					f"(grade: {grade}, tooling: {', '.join(tooling_ids)})"
				)

			item_rows.append(
				{
					"s_warehouse": "",
					"t_warehouse": foundry_return_warehouse,
					"item_code": item_code,
					"qty": total_return_qty,
					"basic_rate": 0.0,
					"custom_pouring_id": self.name,
					"is_finished_item": 1,
					"custom_grade": grade,
					"custom_tooling_id": ", ".join(tooling_ids),
				}
			)

		# ✅ Aggregation of identical items
		aggregated_items = {}
		for row in item_rows:
			key = (row["item_code"], row["s_warehouse"], row["t_warehouse"], row["custom_grade"])
			if key not in aggregated_items:
				aggregated_items[key] = row.copy()
			else:
				aggregated_items[key]["qty"] = aggregated_items[key]["qty"] + row["qty"]

		item_rows = list(aggregated_items.values())

		# Step 5: Create Stock Entry
		if item_rows:
			debug_rows = []
			fractional_errors = []

			for i, row in enumerate(item_rows, start=1):
				item_info = frappe.db.get_value(
					"Item", row["item_code"], ["item_name", "stock_uom"], as_dict=True
				)

				item_name = item_info.item_name if item_info else row["item_code"]
				uom = item_info.stock_uom if item_info else "N/A"
				tooling_id = row.get("custom_tooling_id") or "N/A"

				debug_rows.append(
					f"Row {i}: {item_name} ({row['item_code']}) | Qty {row['qty']} | UOM {uom} | 🔧 Tooling: {tooling_id}"
				)

				if uom in ["Nos", "PCS", "Piece", "Unit"] and not float(row["qty"]).is_integer():
					fractional_errors.append(
						f"❌ Row {i}: {item_name} ({row['item_code']}) has fractional Qty {row['qty']} {uom} | Tooling: {tooling_id}"
					)

			frappe.msgprint("<br>".join(debug_rows))
			frappe.log_error("\n".join(debug_rows), "Debug Pouring Stock Entry Rows")

			if fractional_errors:
				frappe.throw("<br>".join(fractional_errors))

			se = frappe.get_doc(
				{
					"doctype": "Stock Entry",
					"stock_entry_type": "Pouring",
					"custom_process_type": "Pouring",
					"items": item_rows,
					"custom_date": self.date,
					"custom_shift_type": self.shift_type,
				}
			)
			se.insert()
			se.submit()
			self.db_set("linked_stock_entry", se.name)
			frappe.msgprint(f"✅ Stock Entry {se.name} created and linked.")
		else:
			frappe.msgprint("⚠️ No valid items found for Stock Entry.")

	def on_cancel(self):
		restored_quantities = []

		for row in self.mould_batch:
			pouring_qty = row.pouring_quantity or 0
			doctype = row.moulding_system
			mould_no = row.mould_no
			tooling_id = row.tooling_id

			if not (doctype and mould_no and tooling_id):
				continue

			try:
				mould_doc = frappe.get_doc(doctype, mould_no)
				for mould_row in mould_doc.mould_table:
					if mould_row.tooling == tooling_id:
						mould_row.mould_quantity = (mould_row.mould_quantity or 0) + pouring_qty
						restored_quantities.append(
							f"{tooling_id} → {pouring_qty} restored (new qty: {mould_row.mould_quantity})"
						)
						break

				mould_doc.save(ignore_permissions=True)
			except Exception as e:
				frappe.log_error(f"Error while updating mould quantity on cancel: {e}")

		if restored_quantities:
			frappe.msgprint(
				"Restored pouring quantities:<br>" + "<br>".join(restored_quantities),
				title="Mould Quantity Updated",
				indicator="green",
			)

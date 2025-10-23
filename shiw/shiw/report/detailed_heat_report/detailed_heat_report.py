# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
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







import frappe

# Helper functions
def flt(val):
    try:
        return float(val) if val not in [None, "", 0] else 0.0
    except Exception:
        return 0.0

def flt_blank(val):
    try:
        f = float(val)
        if f == 0:
            return None
        return f
    except Exception:
        return None

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Parent ID", "fieldname": "parent_id", "fieldtype": "Link", "options": "Pouring", "width": 140},
        {"label": "Moulding System", "fieldname": "moulding_system", "fieldtype": "Data", "width": 180},
        {"label": "Mould Batch No", "fieldname": "mould_batch_no", "fieldtype": "Data", "width": 180},
        {"label": "Tooling ID", "fieldname": "tooling_id", "fieldtype": "Link", "options": "New Tooling", "width": 180},
        {"label": "Heat", "fieldname": "heat_no", "fieldtype": "Link", "options": "Heat", "width": 110},
        {"label": "Charge Mix Valuation", "fieldname": "charge_mix_value", "fieldtype": "Currency", "width": 150},
        {"label": "Charge Mix Item", "fieldname": "charge_item", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "Charge Mix Weight", "fieldname": "charge_weight", "fieldtype": "Float", "width": 120},
        {"label": "Charge Mix Rate", "fieldname": "charge_item_rate", "fieldtype": "Currency", "width": 130},
        {"label": "Charge Mix Amount", "fieldname": "charge_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Consumption Item", "fieldname": "cons_item", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 70},
        {"label": "Consumption Weight (kg)", "fieldname": "cons_weight", "fieldtype": "Float", "width": 140},
        {"label": "Consumption Rate", "fieldname": "cons_rate", "fieldtype": "Currency", "width": 130},
        {"label": "Consumption Amount", "fieldname": "cons_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Total Consumption Valuation", "fieldname": "total_consumption", "fieldtype": "Currency", "width": 180},
    ]

def get_data(filters):
    data = []
    try:
        # Fetch Charge Mix rows
        charge_rows = frappe.db.sql("""
            SELECT
                p.name AS parent_id,
                mb.mould_no AS mb_no,
                mb.tooling_id,
                mb.moulding_system,
                h.name AS heat_no,
                h.total_charge_mix_valuation AS charge_mix_value,
                cm.item AS charge_item,
                cm.weight AS charge_weight,
                cm.item_rate AS charge_item_rate,
                cm.amount AS charge_amount
            FROM `tabPouring` p
            JOIN `tabMould Batch` mb ON mb.parent = p.name
            JOIN `tabHeat` h ON h.name = mb.heat_no
            JOIN `tabCharge mix component table` cm ON cm.parent = h.name
            ORDER BY p.name, mb.idx, h.name, cm.idx
        """, as_dict=True)

        # Fetch Consumption rows
        consumption_rows = frappe.db.sql("""
            SELECT
                p.name AS parent_id,
                mb.mould_no AS mb_no,
                mb.tooling_id,
                mb.moulding_system,
                cm.item AS cons_item,
                cm.uom AS uom,
                cm.weight_in_kg AS cons_weight,
                cm.rate AS cons_rate,
                cm.amount AS cons_amount,
                mb.heat_no AS heat_no
            FROM `tabPouring` p
            JOIN `tabMould Batch` mb ON mb.parent = p.name
            JOIN `tabConsumption-Mould` cm ON cm.parent = mb.mould_no
            ORDER BY p.name, mb.idx, cm.idx
        """, as_dict=True)

        # Group rows by parent_id -> (mould_no, heat_no)
        grouped = {}
        for r in charge_rows:
            parent = r["parent_id"]
            key = (r["mb_no"], r["heat_no"])
            grouped.setdefault(parent, {"parent_info": r, "rows": {}})
            grouped[parent]["rows"].setdefault(key, {"charge": [], "consumption": []})
            grouped[parent]["rows"][key]["charge"].append(r)

        for r in consumption_rows:
            parent = r["parent_id"]
            key = (r["mb_no"], r.get("heat_no") or "")
            grouped.setdefault(parent, {"parent_info": r, "rows": {}})
            grouped[parent]["rows"].setdefault(key, {"charge": [], "consumption": []})
            grouped[parent]["rows"][key]["consumption"].append(r)

        # Sort grouped data by parent_id
        sorted_groups = sorted(grouped.items())
        
        # Build final rows with smart display + expand/collapse functionality
        for parent_id, parent_grp in sorted_groups:
            parent_info = parent_grp["parent_info"]
            rows = parent_grp["rows"]
            first_row = True

            # Track last displayed values for smart display
            last_parent = None
            last_moulding_system = None
            last_mould_no = None
            last_tooling_id = None
            last_heat_no = None

            # Total consumption valuation once per parent
            total_consumption = 0.0
            try:
                if parent_info.get("moulding_system") and parent_info.get("mb_no"):
                    total_consumption = flt(frappe.db.get_value(
                        parent_info.get("moulding_system"),
                        parent_info.get("mb_no"),
                        "total_consumption_valuation"
                    ) or 0.0)
            except Exception:
                total_consumption = 0.0

            for (mb_no, heat_no), rgrp in rows.items():
                charge_list = rgrp.get("charge") or []
                cons_list = rgrp.get("consumption") or []

                max_len = max(len(charge_list), len(cons_list), 1)
                charge_mix_value = flt(charge_list[0].get("charge_mix_value") or 0.0) if charge_list else None

                for i in range(max_len):
                    ch = charge_list[i] if i < len(charge_list) else {}
                    co = cons_list[i] if i < len(cons_list) else {}

                    # Smart display: show only if changed from previous row
                    parent_val = parent_id if first_row else ""
                    moulding_system_val = ch.get("moulding_system") or co.get("moulding_system") or parent_info.get("moulding_system")
                    if moulding_system_val == last_moulding_system:
                        moulding_system_val = ""
                    else:
                        last_moulding_system = moulding_system_val

                    mould_no_val = ch.get("mb_no") or co.get("mb_no")
                    if mould_no_val == last_mould_no:
                        mould_no_val = ""
                    else:
                        last_mould_no = mould_no_val

                    tooling_val = ch.get("tooling_id") or co.get("tooling_id")
                    if tooling_val == last_tooling_id:
                        tooling_val = ""
                    else:
                        last_tooling_id = tooling_val

                    heat_val = ch.get("heat_no") or heat_no
                    if heat_val == last_heat_no:
                        heat_val = ""
                    else:
                        last_heat_no = heat_val

                    row = {
                        "parent_id": parent_val,
                        "moulding_system": moulding_system_val,
                        "mould_batch_no": mould_no_val,
                        "tooling_id": tooling_val,
                        "heat_no": heat_val,
                        "charge_mix_value": charge_mix_value if first_row else None,
                        "charge_item": ch.get("charge_item"),
                        "charge_weight": flt_blank(ch.get("charge_weight")),
                        "charge_item_rate": flt_blank(ch.get("charge_item_rate")),
                        "charge_amount": flt_blank(ch.get("charge_amount")),
                        "cons_item": co.get("cons_item"),
                        "uom": co.get("uom"),
                        "cons_weight": flt_blank(co.get("cons_weight")),
                        "cons_rate": flt_blank(co.get("cons_rate")),
                        "cons_amount": flt_blank(co.get("cons_amount")),
                        "total_consumption": total_consumption if first_row else None,
                        "indent": 0 if first_row else 1,  # First row is parent, others are children
                    }

                    data.append(row)
                    first_row = False

        return data

    except Exception as e:
        frappe.log_error(f"Exception in get_data: {str(e)}", "Pouring Error")
        return data

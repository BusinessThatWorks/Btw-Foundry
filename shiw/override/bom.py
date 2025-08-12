









# import frappe
# from frappe import enqueue
# from shiw.api.bom import get_updated_item_rates

# # ✅ 1. Apply custom rates before save (works during draft/save)
# def apply_custom_rates_on_save(doc, method):
#     items = [{"item_code": row.item_code, "item_name": row.item_name} for row in doc.items]
#     updated_rates = get_updated_item_rates(items)

#     for row in doc.items:
#         rate_data = updated_rates.get(row.item_code)
#         if rate_data:
#             row.rate = rate_data["rate"]
#             row.amount = row.rate * row.qty

# # ✅ 2. Schedule rate fix after submit (works after ERP overwrites your values)
# def enqueue_post_submit_rate_fix(doc, method):
#     enqueue("shiw.override.bom.fix_bom_item_rates", queue='default', timeout=60, job_name=f"Fix BOM Rates {doc.name}", bom_name=doc.name)

# # ✅ 3. Actually fixes BOM Item rates after ERPNext finishes submission logic
# def fix_bom_item_rates(bom_name):
#     doc = frappe.get_doc("BOM", bom_name)

#     items = [{"item_code": row.item_code, "item_name": row.item_name, "name": row.name, "qty": row.qty} for row in doc.items]
#     updated_rates = get_updated_item_rates(items)

#     for row in items:
#         rate_data = updated_rates.get(row["item_code"])
#         if rate_data:
#             rate = rate_data["rate"]
#             amount = rate * row["qty"]
#             frappe.db.set_value("BOM Item", row["name"], "rate", rate)
#             frappe.db.set_value("BOM Item", row["name"], "amount", amount)

#     # (Optional) update total cost field
#     total = sum(rate_data["rate"] * row["qty"] for row in items if row["item_code"] in updated_rates)
#     frappe.db.set_value("BOM", bom_name, "total_cost", total)
#     frappe.db.commit()
    






# # # import frappe
# # # import json
# # # from frappe import _
# # # from frappe.utils.background_jobs import enqueue

# # # @frappe.whitelist()
# # # def get_updated_item_rates(items):
# # #     if isinstance(items, str):
# # #         items = json.loads(items)

# # #     out = {}

# # #     for row in items:
# # #         item_code = row.get("item_code")
# # #         item_name = row.get("item_name", "")

# # #         if not item_code:
# # #             continue

# # #         warehouse = (
# # #             "Estimated Foundry Return - SHIW"
# # #             if "Foundry Return" in item_name
# # #             else "Stores - SHIW"
# # #         )

# # #         result = frappe.db.sql("""
# # #             SELECT
# # #                 SUM(actual_qty) AS total_qty,
# # #                 SUM(valuation_rate * actual_qty) AS total_value
# # #             FROM `tabBin`
# # #             WHERE item_code = %s AND warehouse = %s
# # #         """, (item_code, warehouse), as_dict=True)

# # #         total_qty = result[0].total_qty or 0
# # #         total_value = result[0].total_value or 0

# # #         if total_qty > 0:
# # #             rate = round(total_value / total_qty, 2)
# # #             out[item_code] = {
# # #                 "rate": rate,
# # #                 "total_qty": total_qty,
# # #                 "total_value": total_value
# # #             }

# # #     return out


# # # def apply_custom_rates_on_save(doc, method=None):
# # #     for row in doc.items:
# # #         if not row.item_code:
# # #             continue

# # #         warehouse = (
# # #             "Estimated Foundry Return - SHIW"
# # #             if "Foundry Return" in (row.item_name or "")
# # #             else "Stores - SHIW"
# # #         )

# # #         result = frappe.db.sql("""
# # #             SELECT
# # #                 SUM(actual_qty) AS total_qty,
# # #                 SUM(valuation_rate * actual_qty) AS total_value
# # #             FROM `tabBin`
# # #             WHERE item_code = %s AND warehouse = %s
# # #         """, (row.item_code, warehouse), as_dict=True)

# # #         total_qty = result[0].total_qty or 0
# # #         total_value = result[0].total_value or 0

# # #         if total_qty > 0:
# # #             row.rate = round(total_value / total_qty, 2)
# # #             row.amount = round(row.rate * row.qty, 2)

# # #     doc.raw_material_cost = round(sum(row.amount for row in doc.items), 2)


# # # def enqueue_post_submit_rate_fix(doc, method=None):
# # #     enqueue(
# # #         "shiw.override.bom.fix_bom_item_rates",
# # #         queue="short",
# # #         timeout=60,
# # #         docname=doc.name
# # #     )


# # # def fix_bom_item_rates(docname):
# # #     doc = frappe.get_doc("BOM", docname)

# # #     for row in doc.items:
# # #         if not row.item_code:
# # #             continue

# # #         warehouse = (
# # #             "Estimated Foundry Return - SHIW"
# # #             if "Foundry Return" in (row.item_name or "")
# # #             else "Stores - SHIW"
# # #         )

# # #         result = frappe.db.sql("""
# # #             SELECT
# # #                 SUM(actual_qty) AS total_qty,
# # #                 SUM(valuation_rate * actual_qty) AS total_value
# # #             FROM `tabBin`
# # #             WHERE item_code = %s AND warehouse = %s
# # #         """, (row.item_code, warehouse), as_dict=True)

# # #         total_qty = result[0].total_qty or 0
# # #         total_value = result[0].total_value or 0

# # #         if total_qty > 0:
# # #             row.rate = round(total_value / total_qty, 2)
# # #             row.amount = round(row.rate * row.qty, 2)

# # #     doc.raw_material_cost = round(sum(row.amount for row in doc.items), 2)
# # #     doc.save(ignore_permissions=True)







# # import frappe
# # from frappe.utils import flt
# # from erpnext.manufacturing.doctype.bom.bom import BOM as ERPNextBOM

# # class CustomBOM(ERPNextBOM):
# #     def __init__(self, *args, **kwargs):
# #         super(CustomBOM, self).__init__(*args, **kwargs)
# #         self._update_after_submit = True

# #     def validate(self):
# #         super().validate()
# #         for row in self.items:
# #             row.amount = flt(row.rate * row.qty, 2)
# #         self.raw_material_cost = flt(sum(row.amount for row in self.items), 2)
# #         self._original_raw_material_cost = self.raw_material_cost


# # @frappe.whitelist()
# # def get_updated_item_rates(items):
# #     updated_items = []
# #     for item in items:
# #         rate = frappe.db.get_value("Item Price", {"item_code": item["item_code"]}, "price_list_rate") or 0
# #         updated_items.append({
# #             "item_code": item["item_code"],
# #             "rate": flt(rate, 2)
# #         })
# #     return updated_items


# # # def fix_bom_item_rates(bom_name):
# # #     doc = frappe.get_doc("BOM", bom_name)

# # #     for row in doc.items:
# # #         row.amount = flt(row.rate * row.qty, 2)
# # #         frappe.db.set_value("BOM Item", row.name, "amount", row.amount)

# # #     raw_material_cost = flt(sum(row.amount for row in doc.items), 2)
# # #     frappe.db.set_value("BOM", bom_name, "raw_material_cost", raw_material_cost)
# # #     frappe.db.set_value("BOM", bom_name, "_original_raw_material_cost", raw_material_cost)

# # @frappe.whitelist()
# # def fix_bom_item_rates(bom_name):
# #     doc = frappe.get_doc("BOM", bom_name)

# #     for row in doc.items:
# #         row.amount = flt(row.rate * row.qty, 2)
# #         frappe.db.set_value("BOM Item", row.name, "amount", row.amount)

# #     raw_material_cost = flt(sum(row.amount for row in doc.items), 2)

# #     doc.flags.ignore_validate_update_after_submit = True
# #     doc.raw_material_cost = raw_material_cost
# #     doc.total_raw_material_cost = raw_material_cost
# #     doc.total_cost = raw_material_cost + flt(doc.operating_cost or 0)
# #     doc.base_raw_material_cost = doc.raw_material_cost
# #     doc.base_total_operating_cost = flt(doc.operating_cost or 0)
# #     doc.base_total_cost = doc.total_cost

# #     doc._original_raw_material_cost = doc.raw_material_cost

# #     doc.save(ignore_permissions=True)

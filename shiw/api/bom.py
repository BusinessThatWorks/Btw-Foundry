# # import frappe
# # import json

# # @frappe.whitelist()
# # def get_updated_item_rates(items):
# #     if isinstance(items, str):
# #         items = json.loads(items)

# #     out = {}

# #     for row in items:
# #         item_code = row.get("item_code")
# #         item_name = row.get("item_name", "")

# #         if not item_code:
# #             continue

# #         warehouse = (
# #             "Estimated Foundry Return - SHIW"
# #             if "Foundry Return" in item_name
# #             else "Stores - SHIW"
# #         )

# #         sle = frappe.db.get_all(
# #             "Stock Ledger Entry",
# #             filters={
# #                 "item_code": item_code,
# #                 "warehouse": warehouse,
# #             },
# #             fields=["valuation_rate"],
# #             order_by="posting_date desc, posting_time desc",
# #             limit=1
# #         )

# #         if sle:
# #             out[item_code] = sle[0].valuation_rate

# #     return out




# # import frappe
# # import json

# # @frappe.whitelist()
# # def get_updated_item_rates(items):
# #     if isinstance(items, str):
# #         items = json.loads(items)

# #     out = {}

# #     for row in items:
# #         item_code = row.get("item_code")
# #         item_name = row.get("item_name", "")

# #         if not item_code:
# #             continue

# #         # Warehouse logic based on item name
# #         warehouse = (
# #             "Estimated Foundry Return - SHIW"
# #             if "Foundry Return" in item_name
# #             else "Stores - SHIW"
# #         )

# #         # Use total valuation / total qty instead of just last SLE
# #         result = frappe.db.sql("""
# #             SELECT
# #                 SUM(actual_qty) AS qty,
# #                 SUM(stock_value_difference) AS value
# #             FROM `tabStock Ledger Entry`
# #             WHERE item_code = %s AND warehouse = %s
# #         """, (item_code, warehouse), as_dict=True)

# #         qty = result[0].qty or 0
# #         val = result[0].value or 0

# #         # Set the calculated valuation rate (same as Stock Balance logic)
# #         out[item_code] = (val / qty) if qty else 0

# #     return out





# import frappe
# import json

# @frappe.whitelist()
# def get_updated_item_rates(items):
#     if isinstance(items, str):
#         items = json.loads(items)

#     out = {}

#     for row in items:
#         item_code = row.get("item_code")
#         item_name = row.get("item_name", "")

#         if not item_code:
#             continue

#         # Decide warehouse based on item name
#         warehouse = (
#             "Estimated Foundry Return - SHIW"
#             if "Foundry Return" in item_name
#             else "Stores - SHIW"
#         )

#         # Get latest stock balance: SUM(actual_qty), SUM(stock_value) till date
#         result = frappe.db.sql("""
#             SELECT
#                 SUM(actual_qty) AS balance_qty,
#                 SUM(stock_value) AS balance_value
#             FROM `tabBin`
#             WHERE item_code = %s AND warehouse = %s
#         """, (item_code, warehouse), as_dict=True)

#         qty = result[0].balance_qty or 0
#         value = result[0].balance_value or 0

#         # Avoid division by zero
#         rate = value / qty if qty else 0

#         out[item_code] = {
#             "warehouse": warehouse,
#             "balance_qty": qty,
#             "balance_value": value,
#             "rate": rate
#         }

#     return out




# import frappe
# import json

# @frappe.whitelist()
# def get_updated_item_rates(items):
#     if isinstance(items, str):
#         items = json.loads(items)

#     out = {}

#     for row in items:
#         item_code = row.get("item_code")
#         item_name = row.get("item_name", "")

#         if not item_code:
#             continue

#         warehouse = (
#             "Estimated Foundry Return - SHIW"
#             if "Foundry Return" in item_name
#             else "Stores - SHIW"
#         )

#         # Get total qty and value in selected warehouse
#         result = frappe.db.sql("""
#             SELECT
#                 SUM(actual_qty) AS total_qty,
#                 SUM(valuation_rate * actual_qty) AS total_value
#             FROM `tabBin`
#             WHERE item_code = %s AND warehouse = %s
#         """, (item_code, warehouse), as_dict=True)

#         total_qty = result[0].total_qty or 0
#         total_value = result[0].total_value or 0

#         if total_qty > 0:
#             rate = total_value / total_qty
#             out[item_code] = {
#                 "rate": rate,
#                 "total_qty": total_qty,
#                 "total_value": total_value
#             }

#     return out




import frappe
import json

@frappe.whitelist()
def get_updated_item_rates(items):
    if isinstance(items, str):
        items = json.loads(items)

    out = {}

    for row in items:
        item_code = row.get("item_code")
        item_name = row.get("item_name", "")

        if not item_code:
            continue

        warehouse = (
            "Estimated Foundry Return - SHIW"
            if "Foundry Return" in item_name
            else "Stores - SHIW"
        )

        # Get total qty and value in selected warehouse
        result = frappe.db.sql("""
            SELECT
                SUM(actual_qty) AS total_qty,
                SUM(valuation_rate * actual_qty) AS total_value
            FROM `tabBin`
            WHERE item_code = %s AND warehouse = %s
        """, (item_code, warehouse), as_dict=True)

        total_qty = result[0].total_qty or 0
        total_value = result[0].total_value or 0

        if total_qty > 0:
            rate = total_value / total_qty
            out[item_code] = {
                "rate": round(rate, 2),
                "total_qty": round(total_qty, 2),
                "total_value": round(total_value, 2)
            }

    return out

# import frappe
# from shiw.api.bom import get_updated_item_rates  # reuse your server-side logic

# def custom_bom_rates(doc, method):
#     items = [{"item_code": row.item_code, "item_name": row.item_name} for row in doc.items]
#     updated_rates = get_updated_item_rates(items)

#     for row in doc.items:
#         rate_data = updated_rates.get(row.item_code)
#         if rate_data:
#             row.rate = rate_data["rate"]
#             row.amount = row.rate * row.qty




# import frappe
# from shiw.api.bom import get_updated_item_rates

# # This still works before save
# def custom_bom_rates(doc, method):
#     items = [{"item_code": row.item_code, "item_name": row.item_name} for row in doc.items]
#     updated_rates = get_updated_item_rates(items)

#     for row in doc.items:
#         rate_data = updated_rates.get(row.item_code)
#         if rate_data:
#             row.rate = rate_data["rate"]
#             row.amount = row.rate * row.qty

# # ✅ This will enforce rates AFTER ERPNext finishes submission
# def fix_rates_after_submit(doc, method):
#     items = [{"item_code": row.item_code, "item_name": row.item_name, "name": row.name, "qty": row.qty} for row in doc.items]
#     updated_rates = get_updated_item_rates(items)

#     for row in items:
#         rate_data = updated_rates.get(row["item_code"])
#         if rate_data:
#             rate = rate_data["rate"]
#             amount = rate * row["qty"]
#             frappe.db.set_value("BOM Item", row["name"], "rate", rate)
#             frappe.db.set_value("BOM Item", row["name"], "amount", amount)

#     frappe.db.commit()  # 🔒 Commit the manual update


import frappe
from frappe import enqueue
from shiw.api.bom import get_updated_item_rates

# ✅ 1. Apply custom rates before save (works during draft/save)
def apply_custom_rates_on_save(doc, method):
    items = [{"item_code": row.item_code, "item_name": row.item_name} for row in doc.items]
    updated_rates = get_updated_item_rates(items)

    for row in doc.items:
        rate_data = updated_rates.get(row.item_code)
        if rate_data:
            row.rate = rate_data["rate"]
            row.amount = row.rate * row.qty

# ✅ 2. Schedule rate fix after submit (works after ERP overwrites your values)
def enqueue_post_submit_rate_fix(doc, method):
    enqueue("shiw.override.bom.fix_bom_item_rates", queue='default', timeout=60, job_name=f"Fix BOM Rates {doc.name}", bom_name=doc.name)

# ✅ 3. Actually fixes BOM Item rates after ERPNext finishes submission logic
def fix_bom_item_rates(bom_name):
    doc = frappe.get_doc("BOM", bom_name)

    items = [{"item_code": row.item_code, "item_name": row.item_name, "name": row.name, "qty": row.qty} for row in doc.items]
    updated_rates = get_updated_item_rates(items)

    for row in items:
        rate_data = updated_rates.get(row["item_code"])
        if rate_data:
            rate = rate_data["rate"]
            amount = rate * row["qty"]
            frappe.db.set_value("BOM Item", row["name"], "rate", rate)
            frappe.db.set_value("BOM Item", row["name"], "amount", amount)

    # (Optional) update total cost field
    total = sum(rate_data["rate"] * row["qty"] for row in items if row["item_code"] in updated_rates)
    frappe.db.set_value("BOM", bom_name, "total_cost", total)
    frappe.db.commit()
    
# from frappe.utils import flt
# from decimal import Decimal, ROUND_HALF_UP

# def rounded(val, precision=2):
#     return float(Decimal(val or 0).quantize(Decimal('1.' + '0' * precision), rounding=ROUND_HALF_UP))

# def fix_bom_item_rates(bom_name):
#     doc = frappe.get_doc("BOM", bom_name)

#     for row in doc.items:
#         row.rate = rounded(row.rate, 2)
#         row.amount = rounded(row.qty * row.rate, 2)

#     doc.total_cost = rounded(doc.total_cost, 2)
#     doc.raw_material_cost = rounded(doc.raw_material_cost, 2)
#     doc.operating_cost = rounded(doc.operating_cost, 2)
#     doc.total_cost = rounded(doc.total_cost, 2)

#     doc.flags.ignore_validate_update_after_submit = True
#     doc.flags.ignore_validate = True
#     doc.flags.ignore_mandatory = True

#     doc.save(ignore_permissions=True)


# # @frappe.whitelist()
# def fix_bom_item_rates(bom_name):
#     bom = frappe.get_doc("BOM", bom_name)

#     bom.ignore_validate_update_after_submit = True
#     bom.ignore_on_update = True  # (Optional: avoids running triggers like notifications)

#     total = 0.0
#     for item in bom.items:
#         if item.rate:
#             item.amount = round(item.rate * item.qty, 2)
#             total += item.amount

#     bom.total_cost = round(total, 2)
#     bom.total_raw_material_cost = bom.total_cost
#     bom.raw_material_cost = bom.total_cost
#     bom.base_raw_material_cost = bom.raw_material_cost
#     bom.base_total_cost = bom.total_cost
#     bom.base_total_operating_cost = bom.total_operating_cost or 0.0
#     bom.total_cost += bom.total_operating_cost or 0.0

#     bom.save()
#     frappe.db.commit()


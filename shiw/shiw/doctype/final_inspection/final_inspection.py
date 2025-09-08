# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt



# from frappe.model.document import Document
import frappe
# from frappe import _
# from frappe.utils import flt

# class Finalinspection(Document):
#     def on_submit(self):
#         items = []

#         for row in self.table_jikz:
#             if row.item_name and flt(row.gn_qty) > 0:
#                 gn_qty = flt(row.gn_qty)
#                 finished_qty = flt(row.finished_qty)

#                 if gn_qty > finished_qty:
#                     frappe.throw(_("Error: Gauging Quantity ({0}) for item {1} exceeds Finished Quantity ({2}).").format(
#                         gn_qty, row.item_name, finished_qty))

#                 # Decide target warehouse
#                 target_warehouse = "Sample Warehouse - SHIW" if row.is_sample else "Finished Good - SHIW"

#                 # Validate warehouses
#                 for warehouse in ["Finishing - SHIW", target_warehouse]:
#                     if not frappe.db.exists("Warehouse", warehouse):
#                         frappe.throw(_("Warehouse {0} does not exist.").format(warehouse))

#                 items.append({
#                     "item_code": row.item_name,
#                     "qty": gn_qty,
#                     "s_warehouse": "Finishing - SHIW",
#                     "t_warehouse": target_warehouse
#                 })

#         if not items:
#             frappe.throw(_("⚠️ No valid items to create Stock Entry."))

#         try:
#             stock_entry = frappe.get_doc({
#                 "doctype": "Stock Entry",
#                 "stock_entry_type": "Material Transfer",
#                 "items": items,
#                 "custom_date": self.date,
#                 "custom_shift_type": self.shift_type,
#                 "custom_process_type": "Gauging - Inspection",
#                 "remarks": f"Auto-created from Gauging - Inspection: {self.name}"
#             })

#             stock_entry.insert()
#             stock_entry.submit()
#             self.linked_stock_entry = stock_entry.name
#             frappe.db.set_value(self.doctype, self.name, "linked_stock_entry", stock_entry.name)
#             frappe.db.commit()

#             frappe.msgprint(_("✅ Stock Entry Created and Submitted: {0}").format(stock_entry.name))
#         except Exception as e:
#             frappe.throw(_("Failed to create or submit Stock Entry: {0}").format(str(e)))
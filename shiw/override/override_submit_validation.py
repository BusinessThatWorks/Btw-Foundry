# import frappe
# from frappe.model.base_document import BaseDocument
# from frappe.model.meta import get_meta

# def patched_validate_update_after_submit(self):
#     if self.flags.ignore_validate_update_after_submit:
#         return

#     meta = get_meta(self.doctype)
#     changed = self.get_all_changes()

#     for df in meta.fields:
#         if (
#             df.allow_on_submit
#             and df.fieldname in changed
#         ):
#             db_val = self.get_db_value(df.fieldname)
#             current_val = self.get(df.fieldname)

#             # Only apply float precision logic to raw_material_cost
#             if df.fieldtype == "Float" and df.fieldname == "raw_material_cost":
#                 db_val = round(float(db_val or 0), 2)
#                 current_val = round(float(current_val or 0), 2)

#             if db_val != current_val:
#                 frappe.throw(
#                     f"Not allowed to change {df.label or df.fieldname} after submission from {db_val} to {current_val}",
#                     frappe.exceptions.UpdateAfterSubmitError
#                 )

# # Patch the method at runtime
# BaseDocument._validate_update_after_submit = patched_validate_update_after_submit

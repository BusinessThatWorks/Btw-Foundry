# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# import frappe

# DOCTYPES = [
#     "Co2 Mould Batch",
#     "Green Sand Hand Mould Batch",
#     "No-Bake Mould Batch",
#     "Jolt Squeeze Mould Batch",
#     "HPML Mould Batch"
# ]

# def execute(filters=None):
#     columns = get_columns()
#     data = []

#     for doctype in DOCTYPES:
#         docs = frappe.get_all(
#             doctype,
#             fields=["name", "total_cast_weight", "total_bunch_weight"],
#         )

#         for d in docs:
#             # fetch child table
#             mould_rows = frappe.get_all(
#                 "New Mould Table",
#                 filters={"parent": d.name, "parenttype": doctype},
#                 fields=["tooling"]
#             )

#             total_yield = 0
#             tooling_count = len(mould_rows)

#             for row in mould_rows:
#                 if row.tooling:
#                     yield_val = frappe.db.get_value("New Tooling", row.tooling, "yield")
#                     if yield_val:
#                         total_yield += float(yield_val)

#             avg_yield = total_yield / tooling_count if tooling_count else 0

#             data.append({
#                 "doctype_name": doctype,
#                 "id": d.name,
#                 "total_cast_weight": d.total_cast_weight,
#                 "total_bunch_weight": d.total_bunch_weight,
#                 "avg_yield": avg_yield,
#                 "no_of_batches": 1,   # each row = 1 batch
#                 "no_of_tooling": tooling_count
#             })

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Doctype Name", "fieldname": "doctype_name", "fieldtype": "Data", "width": 200},
#         {"label": "ID", "fieldname": "id", "fieldtype": "Data", "width": 180},
#         {"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Total Bunch Weight", "fieldname": "total_bunch_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Avg Yield", "fieldname": "avg_yield", "fieldtype": "Float", "precision": 2, "width": 120},
#         {"label": "No of Batches", "fieldname": "no_of_batches", "fieldtype": "Int", "width": 120},
#         {"label": "No of Tooling", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
#     ]




# import frappe

# DOCTYPES = [
#     "Co2 Mould Batch",
#     "Green Sand Hand Mould Batch",
#     "No-Bake Mould Batch",
#     "Jolt Squeeze Mould Batch",
#     "HPML Mould Batch"
# ]

# def execute(filters=None):
#     columns = get_columns()
#     data = []

#     for doctype in DOCTYPES:
#         docs = frappe.get_all(
#             doctype,
#             fields=["name", "total_cast_weight", "total_bunch_weight"],
#         )

#         for d in docs:
#             # fetch child rows (toolings)
#             mould_rows = frappe.get_all(
#                 "New Mould Table",
#                 filters={"parent": d.name, "parenttype": doctype},
#                 fields=["tooling"]
#             )

#             tooling_count = len(mould_rows)
#             total_yield = 0
#             yields = []

#             frappe.msgprint(f"📦 Processing Doc: <b>{doctype}</b> | ID: <b>{d.name}</b>")
#             frappe.msgprint(f"Found <b>{tooling_count}</b> tooling rows in mould_table")

#             for row in mould_rows:
#                 if row.tooling:
#                     yield_val = frappe.db.get_value("New Tooling", row.tooling, "yield")
#                     frappe.msgprint(f"🔧 Tooling: <b>{row.tooling}</b> | Yield: <b>{yield_val}</b>")

#                     if yield_val:
#                         total_yield += float(yield_val)
#                         yields.append(float(yield_val))

#             avg_yield = total_yield / tooling_count if tooling_count else 0

#             frappe.msgprint(f"✅ Yield Values: {yields}")
#             frappe.msgprint(f"➡️ Total Yield: {total_yield}, Count: {tooling_count}, Avg: {avg_yield}")

#             data.append({
#                 "doctype_name": doctype,
#                 "id": d.name,
#                 "total_cast_weight": d.total_cast_weight,
#                 "total_bunch_weight": d.total_bunch_weight,
#                 "avg_yield": avg_yield,
#                 "no_of_batches": 1,   # one row = one batch
#                 "no_of_tooling": tooling_count
#             })

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Doctype Name", "fieldname": "doctype_name", "fieldtype": "Data", "width": 200},
#         {"label": "ID", "fieldname": "id", "fieldtype": "Data", "width": 180},
#         {"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Total Bunch Weight", "fieldname": "total_bunch_weight", "fieldtype": "Float", "width": 150},
#         {"label": "Avg Yield", "fieldname": "avg_yield", "fieldtype": "Float", "precision": 2, "width": 120},
#         {"label": "No of Batches", "fieldname": "no_of_batches", "fieldtype": "Int", "width": 120},
#         {"label": "No of Tooling", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
#     ]




import frappe

DOCTYPES = [
    "Co2 Mould Batch",
    "Green Sand Hand Mould Batch",
    "No-Bake Mould Batch",
    "Jolt Squeeze Mould Batch",
    "HPML Mould Batch"
]

def execute(filters=None):
    columns = get_columns()
    data = []

    for doctype in DOCTYPES:
        docs = frappe.get_all(
            doctype,
            fields=["name", "total_cast_weight", "total_bunch_weight"],
        )

        for d in docs:
            # fetch child rows (toolings)
            mould_rows = frappe.get_all(
                "New Mould Table",
                filters={"parent": d.name, "parenttype": doctype},
                fields=["tooling"]
            )

            tooling_count = len(mould_rows)
            total_yield = 0

            for row in mould_rows:
                if row.tooling:
                    yield_val = frappe.db.get_value("New Tooling", row.tooling, "yield")
                    if yield_val:
                        total_yield += float(yield_val)

            avg_yield = total_yield / tooling_count if tooling_count else 0

            data.append({
                "doctype_name": doctype,
                "id": d.name,
                "total_cast_weight": d.total_cast_weight,
                "total_bunch_weight": d.total_bunch_weight,
                "avg_yield": avg_yield,
                "no_of_batches": 1,   # one row = one batch
                "no_of_tooling": tooling_count
            })

    return columns, data


def get_columns():
    return [
        {"label": "Doctype Name", "fieldname": "doctype_name", "fieldtype": "Data", "width": 200},
        {"label": "ID", "fieldname": "id", "fieldtype": "Data", "width": 180},
        {"label": "Total Cast Weight", "fieldname": "total_cast_weight", "fieldtype": "Float", "width": 150},
        {"label": "Total Bunch Weight", "fieldname": "total_bunch_weight", "fieldtype": "Float", "width": 150},
        {"label": "Avg Yield", "fieldname": "avg_yield", "fieldtype": "Float", "precision": 2, "width": 120},
        {"label": "No of Batches", "fieldname": "no_of_batches", "fieldtype": "Int", "width": 120},
        {"label": "No of Tooling", "fieldname": "no_of_tooling", "fieldtype": "Int", "width": 120},
    ]

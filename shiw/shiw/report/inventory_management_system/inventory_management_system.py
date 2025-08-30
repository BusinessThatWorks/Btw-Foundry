# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data



# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data()
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
#         {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 100},
#         {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 120},
#         {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 120},
#     ]

# def get_data():
#     # Fetch Items with required fields
#     items = frappe.get_all(
#         "Item",
#         fields=[
#             "name",
#             "item_name",
#             "stock_uom as uom",
#             "custom_department",
#             "custom_minimum_stock",
#             "custom_maximum_stock"
#         ]
#     )

#     data = []
#     for item in items:
#         # Fetch available quantity in "Stores - SHIW"
#         store_qty = frappe.db.get_value(
#             "Bin",
#             {"item_code": item.name, "warehouse": "Stores - SHIW"},
#             "actual_qty"
#         ) or 0

#         data.append({
#             "custom_department": item.custom_department,
#             "item_name": item.item_name,
#             "uom": item.uom,
#             "store_qty": store_qty,
#             "custom_minimum_stock": item.custom_minimum_stock,
#             "custom_maximum_stock": item.custom_maximum_stock
#         })

#     return data




# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
#         {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 100},
#         {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 120},
#         {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 120},
#     ]

# def get_data(filters):
#     conditions = {}
#     if filters.get("custom_department"):
#         conditions["custom_department"] = filters["custom_department"]
#     if filters.get("item_name"):
#         conditions["item_name"] = ["like", f"%{filters['item_name']}%"]

#     items = frappe.get_all(
#         "Item",
#         filters=conditions,
#         fields=[
#             "name",
#             "item_name",
#             "stock_uom as uom",
#             "custom_department",
#             "custom_minimum_stock",
#             "custom_maximum_stock"
#         ]
#     )

#     data = []
#     for item in items:
#         # Fetch available quantity in "Stores - SHIW"
#         store_qty = frappe.db.get_value(
#             "Bin",
#             {"item_code": item.name, "warehouse": "Stores - SHIW"},
#             "actual_qty"
#         ) or 0

#         data.append({
#             "custom_department": item.custom_department,
#             "item_name": item.item_name,
#             "uom": item.uom,
#             "store_qty": store_qty,
#             "custom_minimum_stock": item.custom_minimum_stock,
#             "custom_maximum_stock": item.custom_maximum_stock
#         })

#     return data



import frappe

WAREHOUSE = "Stores - SHIW"

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Department", "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 90},
        {"label": "Store Qty", "fieldname": "store_qty", "fieldtype": "Float", "width": 120},
        {"label": "Min Qty", "fieldname": "custom_minimum_stock", "fieldtype": "Float", "width": 110},
        {"label": "Max Qty", "fieldname": "custom_maximum_stock", "fieldtype": "Float", "width": 110},
    ]

def get_data(filters):
    # Build filter list properly (avoid dict-with-operators issues)
    flt_list = []
    if filters.get("custom_department"):
        flt_list.append(["Item", "custom_department", "=", filters["custom_department"]])
    if filters.get("item"):  # Link to Item returns the Item's name (item_code)
        flt_list.append(["Item", "name", "=", filters["item"]])

    items = frappe.get_all(
        "Item",
        filters=flt_list,
        fields=[
            "name",
            "item_name",
            "stock_uom as uom",
            "custom_department",
            "custom_minimum_stock",
            "custom_maximum_stock",
        ],
        order_by="item_name asc"
    )

    data = []
    for it in items:
        store_qty = frappe.db.get_value(
            "Bin", {"item_code": it.name, "warehouse": WAREHOUSE}, "actual_qty"
        ) or 0

        data.append({
            "custom_department": it.custom_department,
            "item_name": it.item_name,
            "uom": it.uom,
            "store_qty": store_qty,
            "custom_minimum_stock": it.custom_minimum_stock,
            "custom_maximum_stock": it.custom_maximum_stock,
        })
    return data

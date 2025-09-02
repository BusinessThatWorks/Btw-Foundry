# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data




# import frappe

# def execute(filters=None):
#     filters = filters or {}

#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
#         {"label": "Total Charge Mix (Kg)", "fieldname": "total_charge_mix_in_kg", "fieldtype": "Float", "width": 180},
#         {"label": "Liquid Balance", "fieldname": "liquid_balence", "fieldtype": "Float", "width": 160},
#         {"label": "Burning Loss", "fieldname": "burning_loss", "fieldtype": "Float", "width": 160},
#     ]


# def get_data(filters):
#     if not filters.get("date"):
#         return []

#     date = filters.get("date")

#     # Aggregate sums for the given date
#     result = frappe.db.sql(
#         """
#         SELECT 
#             %(date)s as date,
#             SUM(total_charge_mix_in_kg) as total_charge_mix_in_kg,
#             SUM(liquid_balence) as liquid_balence,
#             SUM(burning_loss) as burning_loss
#         FROM `tabHeat`
#         WHERE date = %(date)s
#         """,
#         {"date": date},
#         as_dict=True
#     )

#     return result



import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Heat ID", "fieldname": "name", "fieldtype": "Link", "options": "Heat", "width": 150},
        {"label": "Total Charge Mix (Kg)", "fieldname": "total_charge_mix_in_kg", "fieldtype": "Float", "width": 180},
        {"label": "Liquid Balance", "fieldname": "liquid_balence", "fieldtype": "Float", "width": 160},
        {"label": "Burning Loss", "fieldname": "burning_loss", "fieldtype": "Float", "width": 160},
    ]


def get_data():
    return frappe.db.sql(
        """
        SELECT 
            name,
            date,
            total_charge_mix_in_kg,
            liquid_balence,
            burning_loss
        FROM `tabHeat`
        ORDER BY date ASC, name ASC
        """,
        as_dict=True,
    )

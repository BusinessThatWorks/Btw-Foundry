# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data




import frappe
from frappe.utils import nowdate

def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    shift_type = filters.get("shift_type")
    reason = filters.get("reason_for_heat_loss")

    conditions = ["parent.docstatus = 1"]
    values = {}

    # If dates provided, use them; else default to all till today
    if from_date and to_date:
        conditions.append("parent.date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = from_date
        values["to_date"] = to_date
    else:
        # Show all till today
        conditions.append("parent.date <= %(today)s")
        values["today"] = nowdate()

    if shift_type:
        conditions.append("parent.shift_type = %(shift_type)s")
        values["shift_type"] = shift_type

    if reason:
        conditions.append("child.reason_for_heat_loss = %(reason)s")
        values["reason"] = reason

    condition_str = " AND ".join(conditions)

    query = f"""
        SELECT
            child.reason_for_heat_loss,
            SUM(child.weight_in_kg) AS total_weight
        FROM
            `tabReason For Heat Loss Table` AS child
        INNER JOIN
            `tabDaily Heat Loss` AS parent ON child.parent = parent.name
        WHERE {condition_str}
        GROUP BY
            child.reason_for_heat_loss
        ORDER BY
            total_weight DESC
    """

    data = frappe.db.sql(query, values, as_dict=True)

    columns = [
        {"label": "Reason for Heat Loss", "fieldname": "reason_for_heat_loss", "fieldtype": "Data", "width": 400},
        {"label": "Total Weight (kg)", "fieldname": "total_weight", "fieldtype": "Float", "width": 150},
    ]

    return columns, data

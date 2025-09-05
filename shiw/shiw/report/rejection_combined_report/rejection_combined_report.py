# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data



import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    shift_type = filters.get("shift_type")
    item_name = filters.get("item_name")
    rejection_type = filters.get("rejection_type")
    
    # Handle MultiSelect fields
    rejection_reasons = set(filters.get("rejection_reason", "").split(",")) if filters.get("rejection_reason") else set()
    rejection_stages = set(filters.get("rejection_stage", "").split(",")) if filters.get("rejection_stage") else set()

    data = []

    def matches_filters(row_item, row_reason, row_stage, doc_shift):
        if item_name and row_item != item_name:
            return False
        if rejection_reasons and row_reason not in rejection_reasons:
            return False
        if rejection_stages and row_stage not in rejection_stages:
            return False
        if shift_type and shift_type != "Both" and doc_shift != shift_type:
            return False
        return True

    # FIRST LINE
    if rejection_type in (None, "", "First Line", "Both"):
        first_line_docs = frappe.get_all("First Line Rejection", filters={
            "docstatus": 1,
            "date": ["between", [from_date, to_date]]
        }, fields=["name", "date", "shift_type"])

        for doc in first_line_docs:
            child_rows = frappe.get_all("First Line Inspection Report",
                filters={"parent": doc.name},
                fields=["item_name", "rejection", "quantity_rejected", "rejection_stage"]
            )
            for row in child_rows:
                if matches_filters(row.item_name, row.rejection, row.rejection_stage, doc.shift_type):
                    data.append({
                        "rejection_type": "First Line",
                        "id": doc.name,
                        "date": doc.date,
                        "shift_type": doc.shift_type,
                        "item_name": row.item_name,
                        "rejection_reason": row.rejection,
                        "quantity_rejected": row.quantity_rejected,
                        "rejection_stage": row.rejection_stage,
                    })

    # SECOND LINE
    if rejection_type in (None, "", "Second Line", "Both"):
        second_line_docs = frappe.get_all("Second Line Rejection", filters={
            "docstatus": 1,
            "date": ["between", [from_date, to_date]]
        }, fields=["name", "date", "shift_type"])

        for doc in second_line_docs:
            child_rows = frappe.get_all("Second Line Rejection Table",
                filters={"parent": doc.name},
                fields=["item_name", "rejection_reason", "rejected_qty", "rejection_stage"]
            )
            for row in child_rows:
                if matches_filters(row.item_name, row.rejection_reason, row.rejection_stage, doc.shift_type):
                    data.append({
                        "rejection_type": "Second Line",
                        "id": doc.name,
                        "date": doc.date,
                        "shift_type": doc.shift_type,
                        "item_name": row.item_name,
                        "rejection_reason": row.rejection_reason,
                        "quantity_rejected": row.rejected_qty,
                        "rejection_stage": row.rejection_stage,
                    })

    columns = [
        {"label": "Rejection Type", "fieldname": "rejection_type", "fieldtype": "Data"},
        {"label": "ID", "fieldname": "id", "fieldtype": "Link", "options": "First Line Rejection"},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date"},
        {"label": "Shift", "fieldname": "shift_type", "fieldtype": "Data"},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Link", "options": "Item"},
        {"label": "Rejection Reason", "fieldname": "rejection_reason", "fieldtype": "Data"},
        {"label": "Quantity Rejected", "fieldname": "quantity_rejected", "fieldtype": "Float"},
        {"label": "Rejection Stage", "fieldname": "rejection_stage", "fieldtype": "Data"},
    ]

    return columns, data

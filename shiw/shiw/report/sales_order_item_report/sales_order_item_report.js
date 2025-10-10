// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order Item Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "sales_order",
            "label": "Sales Order",
            "fieldtype": "Link",
            "options": "Sales Order"
        },
        {
            "fieldname": "item_code",
            "label": "Item",
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "grade",
            "label": "Grade",
            "fieldtype": "Link",
            "options": "Grade Master"
        },
        {
            "fieldname": "grade_group",
            "label": "Grade Group",
            "fieldtype": "Link",
            "options": "Grade Group"
        },
        {
            "fieldname": "furnace_options",
            "label": "Furnace Filter",
            "fieldtype": "MultiSelect",
            "description": "Select one or more furnaces to show estimated time columns (1T, 500kg, 200kg).",
            "options": ["1T", "500kg", "200kg"].join('\n')
        }
    ]
};

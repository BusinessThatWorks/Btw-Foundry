// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Rejection Analysis Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_days(frappe.datetime.get_today(), -30)
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "item_name",
            label: "Item",
            fieldtype: "Link",
            options: "Item",
            get_query: function () {
                return {
                    filters: {
                        "item_group": "Finished Goods"
                    }
                }
            }
        },
        {
            fieldname: "rejection_type",
            label: "Rejection Type",
            fieldtype: "Select",
            options: "\nFirst Line\nSecond Line\nBoth",
            default: "Both"
        }
    ],


    onload: function () {
        // Set default date range to last 30 days
        if (!frappe.query_report.get_filter_value("from_date")) {
            frappe.query_report.set_filter_value("from_date", frappe.datetime.add_days(frappe.datetime.get_today(), -30));
        }
        if (!frappe.query_report.get_filter_value("to_date")) {
            frappe.query_report.set_filter_value("to_date", frappe.datetime.get_today());
        }
    }
};

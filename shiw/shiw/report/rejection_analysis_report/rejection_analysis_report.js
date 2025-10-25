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
        }
    ],

    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Highlight totals row
        if (row.item_name === "TOTAL") {
            if (column.fieldname === "item_name") {
                return `<span style="color: #2c3e50; font-weight: bold; background-color: #ecf0f1; padding: 5px;">${value}</span>`;
            } else {
                return `<span style="color: #2c3e50; font-weight: bold; background-color: #ecf0f1; padding: 5px;">${value}</span>`;
            }
        }

        // Highlight non-zero values in rejection reason columns
        if (column.fieldname !== "item_name" && column.fieldname !== "total_rejected" && value > 0) {
            return `<span style="color: #e74c3c; font-weight: bold;">${value}</span>`;
        }

        // Highlight total rejected column
        if (column.fieldname === "total_rejected" && value > 0) {
            return `<span style="color: #c0392b; font-weight: bold; background-color: #f8d7da;">${value}</span>`;
        }

        // Keep percentage column normal
        if (column.fieldname === "percentage") {
            return value;
        }

        return value;
    },

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

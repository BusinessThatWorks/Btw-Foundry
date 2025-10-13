// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Asset Maintenance Log Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "asset_name",
            "label": __("Asset Name"),
            "fieldtype": "Link",
            "options": "Asset"
        },
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "maintenance_type",
            "label": __("Maintenance Type"),
            "fieldtype": "Select",
            "options": ["", "Preventive", "Corrective", "Breakdown"]
        },
        {
            "fieldname": "maintenance_status",
            "label": __("Maintenance Status"),
            "fieldtype": "Select",
            "options": ["", "Pending", "Completed", "Overdue", "Cancelled"]
        },
        {
            "fieldname": "assign_to_name",
            "label": __("Assign To Name"),
            "fieldtype": "Data"
        }
    ],

    "formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Color coding for maintenance status
        if (column.fieldname === "maintenance_status") {
            if (data.maintenance_status === "Overdue") {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            } else if (data.maintenance_status === "Completed") {
                value = `<span style="color: green; font-weight: bold;">${value}</span>`;
            } else if (data.maintenance_status === "Pending") {
                value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
            }
        }

        // Highlight overdue due dates
        if (column.fieldname === "due_date" && data.due_date) {
            const dueDate = new Date(data.due_date);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (dueDate < today && data.maintenance_status !== "Completed") {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            }
        }

        return value;
    },

    "onload": function (report) {
        // Add custom button for exporting to Excel
        report.page.add_inner_button(__("Export to Excel"), function () {
            report.export_to_excel();
        });
    }
};

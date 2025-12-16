// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Asset Maintenance Schedule Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "asset_name",
            "label": __("Asset Name"),
            "fieldtype": "Link",
            "options": "Asset"
        },
        {
            "fieldname": "asset_category",
            "label": __("Asset Category"),
            "fieldtype": "Link",
            "options": "Asset Category"
        },
        {
            "fieldname": "maintenance_team",
            "label": __("Maintenance Team"),
            "fieldtype": "Link",
            "options": "Asset Maintenance Team"
        },
        {
            "fieldname": "maintenance_status",
            "label": __("Maintenance Status"),
            "fieldtype": "Select",
            "options": ["", "Planned", "Pending", "Completed", "Overdue", "Cancelled"]
        },
        {
            "fieldname": "maintenance_type",
            "label": __("Maintenance Type"),
            "fieldtype": "Select",
            "options": ["", "Preventive Maintenance", "Corrective Maintenance", "Breakdown Maintenance"]
        }
    ],

    "formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Highlight overdue maintenance tasks
        if (column.fieldname === "maintenance_status" && data.maintenance_status === "Overdue") {
            value = `<span style="color: red; font-weight: bold;">${value}</span>`;
        }

        // Highlight completed maintenance tasks
        if (column.fieldname === "maintenance_status" && data.maintenance_status === "Completed") {
            value = `<span style="color: green; font-weight: bold;">${value}</span>`;
        }

        // Highlight pending maintenance tasks
        if (column.fieldname === "maintenance_status" && data.maintenance_status === "Pending") {
            value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
        }

        // Highlight planned maintenance tasks
        if (column.fieldname === "maintenance_status" && data.maintenance_status === "Planned") {
            value = `<span style="color: blue; font-weight: bold;">${value}</span>`;
        }

        // Format dates
        if (column.fieldname === "next_due_date" && data.next_due_date) {
            const due_date = new Date(data.next_due_date);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (due_date < today && data.maintenance_status !== "Completed") {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            }
        }

        return value;
    },

    "onload": function (report) {
        // No defaults enforced; user can optionally set a date range
    }
};

// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Production Plan Report"] = {
	"filters": [
		{
			"fieldname": "production_plan",
			"label": "Production Plan",
			"fieldtype": "Link",
			"options": "Production Plan",
			"reqd": 1,
			"on_change": function (query_report) {
				const value = query_report.get_values().production_plan;
				if (!value) {
					query_report.set_filter_value("posting_date", "");
					return;
				}
				frappe.db.get_value("Production Plan", value, "posting_date").then(r => {
					const dateVal = (r && r.message && r.message.posting_date) ? r.message.posting_date : "";
					query_report.set_filter_value("posting_date", dateVal);
				});
			}
		},
		{
			"fieldname": "posting_date",
			"label": "Posting Date",
			"fieldtype": "Date",
			"read_only": 1
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Select",
			"options": ""
		}
	],
	onload: function (report) {
		// Load Select options from Item.custom_department DocField
		frappe.model.with_doctype("Item", function () {
			const df = frappe.meta.get_docfield("Item", "custom_department");
			const opts = (df && df.options) ? df.options.split("\n") : [];
			const filter = report.get_filter("department");
			if (filter) {
				filter.df.options = [""].concat(opts).join("\n");
				if (filter.refresh_input) {
					filter.refresh_input();
				} else if (filter.refresh) {
					filter.refresh();
				}
			}
		});
	}
};

// No extra onload needed; handled by filter on_change above

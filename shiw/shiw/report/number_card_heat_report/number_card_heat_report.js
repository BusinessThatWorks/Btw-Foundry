// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Number card Heat report"] = {
// 	"filters": [
// 		{
// 			"fieldname": "date",
// 			"label": "Date",
// 			"fieldtype": "Date",
// 			"reqd": 1
// 		}

// 	]
// };


frappe.query_reports["Number card Heat report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1), // optional default: 1 month ago
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.get_today(),
			"reqd": 1
		}
	]
};


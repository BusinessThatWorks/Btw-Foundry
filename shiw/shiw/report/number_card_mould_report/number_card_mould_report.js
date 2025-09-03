// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Number Card Mould report"] = {
// 	"filters": [

// 	]
// };



frappe.query_reports["Number Card Mould report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)  // last 1 month by default
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "doctype_name",
			"label": "Batch Doctype",
			"fieldtype": "Select",
			"options": [
				"All",
				"Co2 Mould Batch",
				"Green Sand Hand Mould Batch",
				"No-Bake Mould Batch",
				"Jolt Squeeze Mould Batch",
				"HPML Mould Batch"
			],
			"default": "All"
		}
	]
}


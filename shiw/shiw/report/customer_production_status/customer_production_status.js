// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Production Status"] = {
	"filters": [
		{
			"fieldname": "sales_order_id",
			"label": __("Sales Order ID"),
			"fieldtype": "Link",
			"options": "Sales Order"
		},
		{
			"fieldname": "customer_name",
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nCompleted\nPending\nNot Started"
		}
	]
};

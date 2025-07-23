// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Comprehensive Summary Report"] = {
// 	"filters": [

// 	]
// };


frappe.query_reports["Comprehensive Summary Report"] = {
	filters: [
		{
			fieldname: "month",
			label: "Month",
			fieldtype: "Select",
			options: [
				"January", "February", "March", "April", "May", "June",
				"July", "August", "September", "October", "November", "December"
			],
			default: frappe.datetime.str_to_obj(frappe.datetime.get_today()).toLocaleString("default", { month: "long" })
		},
		{
			fieldname: "year",
			label: "Year",
			fieldtype: "Int",
			default: new Date().getFullYear()
		}
	]
};

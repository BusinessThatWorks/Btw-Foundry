// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Comprehensive Summary Report"] = {
// 	"filters": [

// 	]
// };


// frappe.query_reports["Comprehensive Summary Report"] = {
// 	filters: [
// 		{
// 			fieldname: "month",
// 			label: "Month",
// 			fieldtype: "Select",
// 			options: [
// 				"January", "February", "March", "April", "May", "June",
// 				"July", "August", "September", "October", "November", "December"
// 			],
// 			default: frappe.datetime.str_to_obj(frappe.datetime.get_today()).toLocaleString("default", { month: "long" })
// 		},
// 		{
// 			fieldname: "year",
// 			label: "Year",
// 			fieldtype: "Int",
// 			default: new Date().getFullYear()
// 		}
// 	]
// };




//should go with this
frappe.query_reports["Comprehensive Summary Report"] = {
	"filters": [
		{
			"fieldname": "month",
			"label": "Month",
			"fieldtype": "Select",
			"options": "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			"reqd": 1
		},
		{
			"fieldname": "year",
			"label": "Year",
			"fieldtype": "Int",
			// "default": "{{ frappe.utils.nowdate()[:4] | int }}"
		},
		{
			"fieldname": "start_day",
			"label": "Start Day",
			"fieldtype": "Int",
			"default": 1
		},
		{
			"fieldname": "end_day",
			"label": "End Day",
			"fieldtype": "Int",
			"default": 31
		},
		{
			"fieldname": "selected_days",
			"label": "Selected Days",
			"fieldtype": "MultiSelect",
			"description": "Comma-separated days like 1,2,7,9,25"
		}

	]
}

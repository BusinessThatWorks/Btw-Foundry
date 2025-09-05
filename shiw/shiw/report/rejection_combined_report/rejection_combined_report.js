// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Rejection Combined Report"] = {
// 	"filters": [

// 	]
// };



frappe.query_reports["Rejection Combined Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date"
		},
		{
			fieldname: "item_name",
			label: "Item",
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname: "shift_type",
			label: "Shift Type",
			fieldtype: "Select",
			options: "\nDay Shift\nNight Shift"
		},
		{
			fieldname: "rejection_type",
			label: "Rejection Type",
			fieldtype: "Select",
			options: "\nFirst Line\nSecond Line\nBoth"
		},
		{
			fieldname: "rejection_reason",
			label: "Rejection Reason",
			fieldtype: "MultiSelect",
			options: [
				"Cold Metal",
				"Sand Drop",
				"Misrun/Cold Shut",
				"Sand Wash",
				"Soft Ramming",
				"Mismatch",
				"Shrinkage",
				"Blowhole",
				"Pinhole",
				"Short Pouring",
				"Metal Penetration",
				"Crack",
				"Slag Inclusion",
				"Core Defect",
				"Gas Void",
				"Bad Surface",
				"Improper Cast Mark"
			].join('\n')
		},
		{
			fieldname: "rejection_stage",
			label: "Rejection Stage",
			fieldtype: "MultiSelect",
			options: [
				"Pouring",
				"Shake Out",
				"Shot Blast",
				"Fettling",
				"Finishing"
			].join('\n')
		}
	],

	previous_row: {},

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		// Simulate merged cells for these columns
		let group_fields = ["Rejection Type", "ID", "Date", "Shift"];

		if (group_fields.includes(column.label)) {
			if (frappe.query_reports["Rejection Combined Report"].previous_row[column.label] === value) {
				return "";
			} else {
				frappe.query_reports["Rejection Combined Report"].previous_row[column.label] = value;
			}
		}

		return value;
	},

	onload: function () {
		// Reset on load
		frappe.query_reports["Rejection Combined Report"].previous_row = {};
	}
};

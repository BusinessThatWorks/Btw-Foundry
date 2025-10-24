// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Daily Raw Material Received"] = {
// 	"filters": [

// 	]
// };



frappe.query_reports["Daily Raw Material Received"] = {
	filters: [
		// {
		// 	fieldname: "from_date",
		// 	label: "From Date",
		// 	fieldtype: "Date",
		// 	default: frappe.datetime.month_start(),
		// 	reqd: 1
		// },
		// {
		// 	fieldname: "to_date",
		// 	label: "To Date",
		// 	fieldtype: "Date",
		// 	default: frappe.datetime.month_end(),
		// 	reqd: 1
		// },
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "purchase_receipt",
			label: "Purchase Receipt",
			fieldtype: "Link",
			options: "Purchase Receipt"
		},
		{
			fieldname: "supplier",
			label: "Supplier",
			fieldtype: "Link",
			options: "Supplier"
		},
		{
			fieldname: "item_code",
			label: "Item",
			fieldtype: "Link",
			options: "Item",
			get_query: () => {
				return {
					filters: {
						item_group: "Raw Material"
					}
				};
			}
		},
		{
			fieldname: "item_group",
			label: "Item Group",
			fieldtype: "Link",
			options: "Item Group"
		}
	],





	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "accepted_qty") {
			return `<span style="color: green; font-weight: bold;">${value}</span>`;
		}

		if (column.fieldname === "rejected_qty") {
			return `<span style="color: red; font-weight: bold;">${value}</span>`;
		}

		if (column.fieldname === "amount") {
			return `<span style="color: blue; font-weight: bold;">${value}</span>`;
		}

		if (column.fieldname === "item_group") {
			return `<span style="color: purple; font-weight: bold;">${value}</span>`;
		}

		return value;
	}
};
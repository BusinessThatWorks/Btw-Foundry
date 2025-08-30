// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [

// 	]
// };




// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [
// 		{
// 			fieldname: "custom_department",
// 			label: "Department",
// 			fieldtype: "Data",
// 			reqd: 0
// 		},
// 		{
// 			fieldname: "item_name",
// 			label: "Item Name",
// 			fieldtype: "Data",
// 			reqd: 0
// 		}
// 	],

// 	formatter: function (value, row, column, data, default_formatter) {
// 		value = default_formatter(value, row, column, data);

// 		if (column.fieldname == "store_qty" && data) {
// 			let min = data.custom_minimum_stock || 0;
// 			let max = data.custom_maximum_stock || 0;
// 			let qty = data.store_qty || 0;

// 			if (qty < min) {
// 				value = `<span style="color:red;font-weight:bold">${value}</span>`;
// 			} else if (qty > max) {
// 				value = `<span style="color:purple;font-weight:bold">${value}</span>`;
// 			} else {
// 				value = `<span style="color:green;font-weight:bold">${value}</span>`;
// 			}
// 		}
// 		return value;
// 	}
// };



frappe.query_reports["Inventory Management System"] = {
	"filters": [
		{
			fieldname: "custom_department",
			label: "Department",
			fieldtype: "Select",
			options: [
				"", // All
				"Mould Box",
				"Co2",
				"Co2 Core",
				"Co2 Hand Mould",
				"Core",
				"Core Suiter Machine",
				"Fettling",
				"Fettling/Finishing",
				"Finished",
				"Green Sand",
				"Grinding",
				"Gs",
				"Gs Core",
				"Gs Hand Mould",
				"Hpml",
				"Hpml Core",
				"Instruments",
				"Jolt Squeeze",
				"Laboratory",
				"Labortary",
				"Maintenance",
				"Match Plate",
				"Melting",
				"Miscellaneous",
				"MiscellaneousMatch Plate",
				"Moulding",
				"Nobake",
				"Nobake Core",
				"Pattern Shop",
				"Quality",
				"Shakeout",
				"Shortblast"
			].join("\n")
		},
		{
			fieldname: "item",
			label: "Item",
			fieldtype: "Link",
			options: "Item",
			reqd: 0
		}
	],

	// Your color logic (kept as-is)
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "store_qty" && data) {
			const q = Number(data.store_qty || 0);
			const minq = Number(data.custom_minimum_stock || 0);
			const maxq = Number(data.custom_maximum_stock || 0);

			if (q < minq) {
				value = `<span style="color:red; font-weight:bold">${q}</span>`;
			} else if (q <= maxq) {
				value = `<span style="color:green; font-weight:bold">${q}</span>`;
			} else {
				value = `<span style="color:purple; font-weight:bold">${q}</span>`;
			}
		}
		return value;
	}
};

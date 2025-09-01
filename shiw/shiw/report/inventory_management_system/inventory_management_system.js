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


//only number colour
// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [
// 		{
// 			fieldname: "custom_department",
// 			label: "Department",
// 			fieldtype: "Select",
// 			options: [
// 				"", // All
// 				"Mould Box",
// 				"Co2",
// 				"Co2 Core",
// 				"Co2 Hand Mould",
// 				"Core",
// 				"Core Suiter Machine",
// 				"Fettling",
// 				"Fettling/Finishing",
// 				"Finished",
// 				"Green Sand",
// 				"Grinding",
// 				"Gs",
// 				"Gs Core",
// 				"Gs Hand Mould",
// 				"Hpml",
// 				"Hpml Core",
// 				"Instruments",
// 				"Jolt Squeeze",
// 				"Laboratory",
// 				"Labortary",
// 				"Maintenance",
// 				"Match Plate",
// 				"Melting",
// 				"Miscellaneous",
// 				"MiscellaneousMatch Plate",
// 				"Moulding",
// 				"Nobake",
// 				"Nobake Core",
// 				"Pattern Shop",
// 				"Quality",
// 				"Shakeout",
// 				"Shortblast"
// 			].join("\n")
// 		},
// 		{
// 			fieldname: "item",
// 			label: "Item",
// 			fieldtype: "Link",
// 			options: "Item",
// 			reqd: 0
// 		}
// 	],

// 	// Your color logic (kept as-is)
// 	formatter: function (value, row, column, data, default_formatter) {
// 		value = default_formatter(value, row, column, data);

// 		if (column.fieldname === "store_qty" && data) {
// 			const q = Number(data.store_qty || 0);
// 			const minq = Number(data.custom_minimum_stock || 0);
// 			const maxq = Number(data.custom_maximum_stock || 0);

// 			if (q < minq) {
// 				value = `<span style="color:red; font-weight:bold">${q}</span>`;
// 			} else if (q <= maxq) {
// 				value = `<span style="color:green; font-weight:bold">${q}</span>`;
// 			} else {
// 				value = `<span style="color:purple; font-weight:bold">${q}</span>`;
// 			}
// 		}
// 		return value;
// 	}
// };




//only number cell background colour
// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [
// 		{
// 			fieldname: "custom_department",
// 			label: "Department",
// 			fieldtype: "Select",
// 			options: [
// 				"", // All
// 				"Mould Box",
// 				"Co2",
// 				"Co2 Core",
// 				"Co2 Hand Mould",
// 				"Core",
// 				"Core Suiter Machine",
// 				"Fettling",
// 				"Fettling/Finishing",
// 				"Finished",
// 				"Green Sand",
// 				"Grinding",
// 				"Gs",
// 				"Gs Core",
// 				"Gs Hand Mould",
// 				"Hpml",
// 				"Hpml Core",
// 				"Instruments",
// 				"Jolt Squeeze",
// 				"Laboratory",
// 				"Labortary",
// 				"Maintenance",
// 				"Match Plate",
// 				"Melting",
// 				"Miscellaneous",
// 				"MiscellaneousMatch Plate",
// 				"Moulding",
// 				"Nobake",
// 				"Nobake Core",
// 				"Pattern Shop",
// 				"Quality",
// 				"Shakeout",
// 				"Shortblast"
// 			].join("\n")
// 		},
// 		{
// 			fieldname: "item",
// 			label: "Item",
// 			fieldtype: "Link",
// 			options: "Item",
// 			reqd: 0
// 		}
// 	],

// 	formatter: function (value, row, column, data, default_formatter) {
// 		value = default_formatter(value, row, column, data);

// 		if (column.fieldname === "store_qty" && data) {
// 			const q = Number(data.store_qty || 0);
// 			const minq = Number(data.custom_minimum_stock || 0);
// 			const maxq = Number(data.custom_maximum_stock || 0);

// 			let bgColor = "";
// 			if (q < minq) {
// 				bgColor = "red";
// 			} else if (q <= maxq) {
// 				bgColor = "lightgreen";
// 			} else {
// 				bgColor = "violet";
// 			}

// 			value = `<span style="background-color:${bgColor}; padding:2px 6px; border-radius:4px; display:inline-block;">${q}</span>`;
// 		}
// 		return value;
// 	}
// };


// square colour
// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [
// 		{
// 			fieldname: "custom_department",
// 			label: "Department",
// 			fieldtype: "Select",
// 			options: [
// 				"", // All
// 				"Mould Box",
// 				"Co2",
// 				"Co2 Core",
// 				"Co2 Hand Mould",
// 				"Core",
// 				"Core Suiter Machine",
// 				"Fettling",
// 				"Fettling/Finishing",
// 				"Finished",
// 				"Green Sand",
// 				"Grinding",
// 				"Gs",
// 				"Gs Core",
// 				"Gs Hand Mould",
// 				"Hpml",
// 				"Hpml Core",
// 				"Instruments",
// 				"Jolt Squeeze",
// 				"Laboratory",
// 				"Labortary",
// 				"Maintenance",
// 				"Match Plate",
// 				"Melting",
// 				"Miscellaneous",
// 				"MiscellaneousMatch Plate",
// 				"Moulding",
// 				"Nobake",
// 				"Nobake Core",
// 				"Pattern Shop",
// 				"Quality",
// 				"Shakeout",
// 				"Shortblast"
// 			].join("\n")
// 		},
// 		{
// 			fieldname: "item",
// 			label: "Item",
// 			fieldtype: "Link",
// 			options: "Item",
// 			reqd: 0
// 		}
// 	],

// 	formatter: function (value, row, column, data, default_formatter) {
// 		value = default_formatter(value, row, column, data);

// 		if (column.fieldname === "store_qty" && data) {
// 			const q = Number(data.store_qty || 0);
// 			const minq = Number(data.custom_minimum_stock || 0);
// 			const maxq = Number(data.custom_maximum_stock || 0);

// 			let bgColor = "";
// 			let textColor = "black";

// 			if (q < minq) {
// 				bgColor = "red";
// 				textColor = "white";
// 			} else if (q <= maxq) {
// 				bgColor = "lightgreen";
// 				textColor = "black";
// 			} else {
// 				bgColor = "violet";
// 				textColor = "white";
// 			}

// 			// Full cell background color
// 			value = `<div style="
// 				background-color:${bgColor};
// 				color:${textColor};
// 				width:100%;
// 				height:100%;
// 				padding:4px;
// 				box-sizing:border-box;
// 			">${q}</div>`;
// 		}
// 		return value;
// 	}
// };



//rounded colour
// frappe.query_reports["Inventory Management System"] = {
// 	"filters": [
// 		{
// 			fieldname: "custom_department",
// 			label: "Department",
// 			fieldtype: "Select",
// 			options: [
// 				"", // All
// 				"Mould Box",
// 				"Co2",
// 				"Co2 Core",
// 				"Co2 Hand Mould",
// 				"Core",
// 				"Core Suiter Machine",
// 				"Fettling",
// 				"Fettling/Finishing",
// 				"Finished",
// 				"Green Sand",
// 				"Grinding",
// 				"Gs",
// 				"Gs Core",
// 				"Gs Hand Mould",
// 				"Hpml",
// 				"Hpml Core",
// 				"Instruments",
// 				"Jolt Squeeze",
// 				"Laboratory",
// 				"Labortary",
// 				"Maintenance",
// 				"Match Plate",
// 				"Melting",
// 				"Miscellaneous",
// 				"MiscellaneousMatch Plate",
// 				"Moulding",
// 				"Nobake",
// 				"Nobake Core",
// 				"Pattern Shop",
// 				"Quality",
// 				"Shakeout",
// 				"Shortblast"
// 			].join("\n")
// 		},
// 		{
// 			fieldname: "item",
// 			label: "Item",
// 			fieldtype: "Link",
// 			options: "Item",
// 			reqd: 0
// 		}
// 	],

// 	formatter: function (value, row, column, data, default_formatter) {
// 		value = default_formatter(value, row, column, data);

// 		if (column.fieldname === "store_qty" && data) {
// 			const q = Number(data.store_qty || 0);
// 			const minq = Number(data.custom_minimum_stock || 0);
// 			const maxq = Number(data.custom_maximum_stock || 0);

// 			let bgColor = "";
// 			let textColor = "black";
// 			if (q < minq) {
// 				bgColor = "red";
// 				textColor = "white";
// 			} else if (q <= maxq) {
// 				bgColor = "lightgreen";
// 				textColor = "black";
// 			} else {
// 				bgColor = "violet";
// 				textColor = "white";
// 			}

// 			// full cell background with rounded corners
// 			value = `<div style="
// 				background-color:${bgColor};
// 				color:${textColor};
// 				width:100%;
// 				height:100%;
// 				padding:4px;
// 				box-sizing:border-box;
// 				border-radius:8px;">
// 				${q}
// 				</div>`;
// 		}
// 		return value;
// 	}
// };





//final script
frappe.query_reports["Inventory Management System"] = {
    filters: [
        {
            fieldname: "custom_department",
            label: "Department",
            fieldtype: "Select",
            options: [
                "",
                "Mould Box", "Co2", "Co2 Core", "Co2 Hand Mould", "Core",
                "Core Suiter Machine", "Fettling", "Fettling/Finishing",
                "Finished", "Green Sand", "Grinding", "Gs", "Gs Core", "Gs Hand Mould",
                "Hpml", "Hpml Core", "Instruments", "Jolt Squeeze", "Laboratory",
                "Labortary", "Maintenance", "Match Plate", "Melting", "Miscellaneous",
                "MiscellaneousMatch Plate", "Moulding", "Nobake", "Nobake Core",
                "Pattern Shop", "Quality", "Shakeout", "Shortblast"
            ],
            width: "180"
        },
        {
            fieldname: "item",
            label: "Item",
            fieldtype: "Link",
            options: "Item",
            width: "220"
        },
        {
            fieldname: "color_filter",
            label: "Color",
            fieldtype: "Select",
            options: ["", "Red", "Green", "Purple"], // matches Python "status"
            width: "120"
        }
    ],

    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "store_qty" && data) {
            let bg = "";
            if (data.status === "Red") bg = "#ff4d4d";       // red
            else if (data.status === "Green") bg = "#4dff88"; // green
            else if (data.status === "Purple") bg = "#b84dff"; // purple

            return `<div style="background-color:${bg}; 
                                border-radius:12px; 
                                padding:4px; 
                                text-align:center;">
                        ${data.store_qty}
                    </div>`;
        }
        return value;
    }
};

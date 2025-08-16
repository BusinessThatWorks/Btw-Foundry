// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Daily Heat Loss report"] = {
// 	"filters": [

// 	]
// };



frappe.query_reports["Daily Heat Loss report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",

		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",

		},
		{
			fieldname: "shift_type",
			label: "Shift Type",
			fieldtype: "Select",
			options: "\nDay shift\nNight shift"
		},
		{
			fieldname: "reason_for_heat_loss",
			label: "Reason for Heat Loss",
			fieldtype: "Select",
			options: [
				"",
				"Over Achieved",
				"Manpower Issue",
				"Power Problem",
				"Ladle Not Available",
				"No Mould in HPML",
				"Stopper Jam",
				"Chemistry Out",
				"Grade Change",
				"Rusted Scrap Boiling Heat Slow Running",
				"Sintering Heat",
				"Ladle Breakdown",
				"Cold Furnace",
				"Sampling",
				"Patching Heat",
				"Lack Of Raw Material",
				"High Water Temp",
				"Furnace Repairing",
				"Bariman issue",
				"Power cut",
				"No mould in JS",
				"Crane man unavailable",
				"Scrap problem",
				"Pattern change",
				"Heat change",
				"Nozzle Leakage",
				"Due to both 1 ton furnaces running at the same time",
				"Furnace starts late",
				"Furnace hold",
				"Nozzle Break",
				"SS Heat take time",
				"Furnace Breakdown",
				"DI Heat Change",
				"Chemistry High",
				"Mixed scrap",
				"Ladle heating issue",
				"Furnace stop",
				"Grade change"
			].join("\n")
		}
	]
};

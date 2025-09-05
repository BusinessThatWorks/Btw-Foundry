// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.query_reports["Detailed heat report"] = {
// 	"filters": [

// 	]
// };


frappe.query_reports["Detailed heat report"] = {
	filters: [
		{
			fieldname: "row_no",
			label: "Row No",
			fieldtype: "Int"
		}
	],

	onload: function (report) {
		report.page.add_inner_button("Go To Row", function () {
			let row_no = report.get_values().row_no;
			if (!row_no) {
				frappe.msgprint("Please enter a Row No.");
				return;
			}

			let total_rows = report.datatable.datamanager.rowCount;
			if (row_no < 1 || row_no > total_rows) {
				frappe.msgprint(`Row ${row_no} not found. Total rows: ${total_rows}`);
				return;
			}

			// row index in 0-based
			let rowIndex = row_no - 1;

			// Height of one row
			let rowHeight = report.datatable.options.rowHeight || 35;

			// Target scroll position
			let scrollTop = rowIndex * rowHeight;

			// Scroll the datatable's scroll container
			let scrollContainer = report.datatable.bodyScrollable;
			if (scrollContainer) {
				scrollContainer.scrollTop = scrollTop;

				// wait a bit for DOM to render that row, then highlight
				setTimeout(() => {
					let rows = scrollContainer.querySelectorAll(".dt-row");
					let targetRow = rows[0]; // fallback
					rows.forEach(r => {
						let idx = parseInt(r.getAttribute("data-row-index"));
						if (idx === rowIndex) targetRow = r;
					});

					if (targetRow) {
						targetRow.style.backgroundColor = "#ffff99";
						setTimeout(() => targetRow.style.backgroundColor = "", 3000);
					}
				}, 300);
			} else {
				frappe.msgprint("Could not access scroll container.");
			}
		});
	}
};







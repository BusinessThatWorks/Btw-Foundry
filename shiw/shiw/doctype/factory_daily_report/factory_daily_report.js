// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Factory Daily Report", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Factory Daily Report', {
    date: function (frm) {
        if (!frm.doc.date) {
            console.log("No date selected, clearing child table");
            frm.clear_table("factory_daily_report");
            frm.refresh_field("factory_daily_report");
            return;
        }

        console.log("Date selected:", frm.doc.date);
        console.log("Fetching category totals from server...");

        frappe.call({
            method: "shiw.shiw.doctype.factory_daily_report.factory_daily_report.get_activity_totals",
            args: {
                date: frm.doc.date
            },
            callback: function (r) {
                console.log("Server response:", r.message);

                frm.clear_table("factory_daily_report");

                if (r.message && r.message.length) {
                    r.message.forEach(row => {
                        console.log(`Adding row for activity: ${row.activity}`);
                        let child = frm.add_child("factory_daily_report");
                        child.activity = row.activity;
                        child.total_man_power = row.total_man_power;
                        child.total_labour_cost = row.total_labour_cost;
                        child.total_consumption_cost = row.total_consumption_cost;
                        child.day_shift_man_power = row.day_shift_man_power;
                        child.day_shift_labour_cost = row.day_shift_labour_cost;
                        child.day_shift_consumption_cost = row.day_shift_consumption_cost;
                        child.night_shift_man_power = row.night_shift_man_power;
                        child.night_shift_labour_cost = row.night_shift_labour_cost;
                        child.night_shift_consumption_cost = row.night_shift_consumption_cost;
                    });
                } else {
                    console.log("No data found for this date");
                }

                frm.refresh_field("factory_daily_report");
            }
        });
    }
});

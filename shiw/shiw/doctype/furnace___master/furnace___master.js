// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Furnace - Master", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Furnace - Master", {

    refresh: function(frm) {
        calculate_throughput(frm);
    },

    average_heat_time: function(frm) { calculate_throughput(frm); },
    custom_patching: function(frm) { calculate_throughput(frm); },
    custom_patching_time_in_min: function(frm) { calculate_throughput(frm); },
    custom_lining_heat_in_min: function(frm) { calculate_throughput(frm); },
    custom_lining_time_in_min: function(frm) { calculate_throughput(frm); },
    custom_patching_cycle: function(frm) { calculate_throughput(frm); },
    furnace_capacity__in_kg: function(frm) { calculate_throughput(frm); }

});

function calculate_throughput(frm) {
    console.log("=== Starting Calculation ===");

    // Step 1: Convert average_heat_time to minutes
    let avg_minutes = 0;
    if (frm.doc.average_heat_time) {
        avg_minutes = Math.floor(frm.doc.average_heat_time / 60);
    }
    avg_minutes = parseFloat(avg_minutes.toFixed(2));
    console.log("Average Heat Time (min):", avg_minutes);

    // Step 2: Patching calculation
    let patching_total_time = (frm.doc.custom_patching || 0) * avg_minutes;
    patching_total_time += (frm.doc.custom_patching_time_in_min || 0);
    patching_total_time = parseFloat(patching_total_time.toFixed(2));
    console.log("Patching Total Time (min):", patching_total_time);

    // Step 3: Lining repair
    let custom_lining_repair_time = (frm.doc.custom_lining_heat_in_min || 0) + 
                                    (frm.doc.custom_lining_time_in_min || 0);
    custom_lining_repair_time = parseFloat(custom_lining_repair_time.toFixed(2));
    console.log("Custom Lining Repair Time (min):", custom_lining_repair_time);

    frm.set_value("custom_lining_repair_time", custom_lining_repair_time);

    // Step 4 + 5: Total cycle time (using cycle-1 instead of cycle)
    let cycle_count = (frm.doc.custom_patching_cycle || 0);
    let total_cycle_time = patching_total_time * Math.max(cycle_count - 1, 0);
    total_cycle_time = parseFloat(total_cycle_time.toFixed(2));
    console.log("Total Cycle Time (min):", total_cycle_time);

    // Step 6: Add lining repair
    let x = total_cycle_time + custom_lining_repair_time;
    x = parseFloat(x.toFixed(2));
    console.log("X (Total Time including Lining Repair):", x);

    // Step 7: Total ton (still cycle * patching)
    let total_ton = (cycle_count * (frm.doc.custom_patching || 0));
    total_ton = parseFloat(total_ton.toFixed(2));
    console.log("Total Ton:", total_ton);

    // Step 8: Final throughput
    let final_value = 0;
    if (x > 0) {
        final_value = (total_ton * (frm.doc.furnace_capacity__in_kg || 0)) / x;
        final_value = parseFloat(final_value.toFixed(2));
    }
    console.log("Custom Throughput (2 dec):", final_value);

    frm.set_value("custom_throughput", final_value);
}

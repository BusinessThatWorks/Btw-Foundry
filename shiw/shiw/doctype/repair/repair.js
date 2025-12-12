// Child table script for "Repair Table"
frappe.ui.form.on('Repair Table', {
    // Trigger when item_name is selected
    item_name: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Item selected: ${row.item_name}, Cast Weight: ${row.cast_weight_in_kg}`);
        // Calculate total_cast_weight if repairing_qty exists
        if (row.repairing_qty && row.cast_weight_in_kg) {
            row.total_cast_weight = row.cast_weight_in_kg * row.repairing_qty;
            console.log(`Calculated total_cast_weight for row: ${row.total_cast_weight}`);
            frm.refresh_field('table_neky');
            update_total_repair_weight(frm);
        }
    },

    // Trigger when repairing_qty is changed
    repairing_qty: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Repairing Qty changed: ${row.repairing_qty}`);
        // Calculate total_cast_weight if cast_weight_in_kg exists
        if (row.cast_weight_in_kg && row.repairing_qty) {
            row.total_cast_weight = row.cast_weight_in_kg * row.repairing_qty;
            console.log(`Calculated total_cast_weight for row: ${row.total_cast_weight}`);
            frm.refresh_field('table_neky');
            update_total_repair_weight(frm);
        }
    },

    // Trigger when a row is removed
    table_neky_remove: function (frm) {
        console.log('Row removed from Repair Table');
        update_total_repair_weight(frm);
    }
});

// Function to calculate and update total_repair_weight in parent doctype
function update_total_repair_weight(frm) {
    let total = 0;
    // Sum total_cast_weight from all child table rows
    (frm.doc.table_neky || []).forEach(row => {
        if (row.total_cast_weight) {
            total += row.total_cast_weight;
        }
    });
    // Update parent field
    frm.set_value('total_repair_weight', total);
    console.log(`Updated total_repair_weight: ${total}`);
}

// Child table script for "Consumption-Mould"
frappe.ui.form.on('Consumption-Mould', {
    weight_in_kg: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Weight changed: ${row.weight_in_kg}`);
        calculate_consumption_amount(frm, row);
    },

    rate: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Rate changed: ${row.rate}`);
        calculate_consumption_amount(frm, row);
    },

    table_rlyc_remove: function (frm) {
        console.log('Row removed from Consumption-Mould');
        update_total_consumption_valuation(frm);
    }
});

// Calculate amount for a single Consumption-Mould row
function calculate_consumption_amount(frm, row) {
    if (row.weight_in_kg && row.rate) {
        row.amount = row.weight_in_kg * row.rate;
    } else {
        row.amount = 0;
    }
    console.log(`Calculated amount for row: ${row.amount}`);
    frm.refresh_field('table_rlyc');
    update_total_consumption_valuation(frm);
}

// Sum all amount values from Consumption-Mould child table
function update_total_consumption_valuation(frm) {
    let total = 0;
    (frm.doc.table_rlyc || []).forEach(row => {
        if (row.amount) {
            total += row.amount;
        }
    });
    frm.set_value('total_consumption_valuation', total);
    console.log(`Updated total_consumption_valuation: ${total}`);
}

// Trigger on parent form refresh to ensure calculations
frappe.ui.form.on('Repair', {
    refresh: function (frm) {
        console.log('Repair form refreshed');
        update_total_repair_weight(frm);
        update_total_consumption_valuation(frm);
    }
});

// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Repair", {
// 	refresh(frm) {

// 	},
// });

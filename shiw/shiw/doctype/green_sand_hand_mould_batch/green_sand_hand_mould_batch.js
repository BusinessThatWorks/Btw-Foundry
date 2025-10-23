// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Green Sand Hand Mould Batch", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Green Sand Hand Mould Batch', {
    refresh: function(frm) {
        console.log('Form refreshed, calculating total consumption valuation and updating parent totals');
        calculate_total_consumption(frm);
        update_parent_totals(frm);
    }
});

frappe.ui.form.on('Consumption-Mould', {
    item: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Item changed for row ${cdn}: ${row.item}`);

        if (row.item) {
            // Check if item name contains (some number + kg)
            const match = row.item.match(/\((\d+)\s*kg\)/i);
            if (match) {
                console.log(`Detected weight pattern in item: ${match[1]} kg`);

                if (row.used_in_kg && row.weight_per_unit) {
                    row.weight_in_kg = flt(row.used_in_kg) / flt(row.weight_per_unit);
                    console.log(`Auto-set weight_in_kg = used_in_kg / weight_per_unit = ${row.used_in_kg} / ${row.weight_per_unit} = ${row.weight_in_kg}`);
                } else {
                    console.log(`Missing used_in_kg or weight_per_unit for row ${cdn}, skipping auto calculation.`);
                }
            } else {
                console.log(`Item ${row.item} does not have a weight pattern like (19 kg), skipping special logic.`);
            }
        }

        frm.refresh_field('consumption_mould');
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },

    used_in_kg: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Used_in_kg changed for row ${cdn}: ${row.used_in_kg}`);

        if (row.item && /\(\d+\s*kg\)/i.test(row.item) && row.weight_per_unit) {
            row.weight_in_kg = flt(row.used_in_kg) / flt(row.weight_per_unit);
            console.log(`Recalculated weight_in_kg due to used_in_kg change: ${row.weight_in_kg}`);
            frm.refresh_field('consumption_mould');
        }

        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },

    weight_per_unit: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(`Weight_per_unit changed for row ${cdn}: ${row.weight_per_unit}`);

        if (row.item && /\(\d+\s*kg\)/i.test(row.item) && row.used_in_kg) {
            row.weight_in_kg = flt(row.used_in_kg) / flt(row.weight_per_unit);
            console.log(`Recalculated weight_in_kg due to weight_per_unit change: ${row.weight_in_kg}`);
            frm.refresh_field('consumption_mould');
        }

        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },

    weight_in_kg: function(frm, cdt, cdn) {
        console.log(`Weight changed for row ${cdn}: ${locals[cdt][cdn].weight_in_kg}`);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },

    rate: function(frm, cdt, cdn) {
        console.log(`Rate changed for row ${cdn}: ${locals[cdt][cdn].rate}`);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },

    table_mcjm_remove: function(frm, cdt, cdn) {
        console.log(`Row ${cdn} removed from consumption_mould`);
        calculate_total_consumption(frm);
    }
});

frappe.ui.form.on('New Mould Table', {
    start_no: function(frm, cdt, cdn) {
        console.log("Start No changed for row:", cdn);
        calculate_mould_quantity(cdt, cdn, frm);
    },
    end_no: function(frm, cdt, cdn) {
        console.log("End No changed for row:", cdn);
        calculate_mould_quantity(cdt, cdn, frm);
    },
    cast_weight: function(frm, cdt, cdn) {
        console.log("Cast Weight changed for row:", cdn);
        calculate_mould_quantity(cdt, cdn, frm);
    },
    bunch_weight: function(frm, cdt, cdn) {
        console.log("Bunch Weight changed for row:", cdn);
        calculate_mould_quantity(cdt, cdn, frm);
    },
    new_mould_table_add: function(frm, cdt, cdn) {
        console.log("New row added:", cdn);
        frappe.after_ajax(() => {
            update_parent_totals(frm);
        });
    },
    new_mould_table_remove: function(frm, cdt, cdn) {
        console.log("Row removed:", cdn);
        frappe.after_ajax(() => {
            update_parent_totals(frm);
        });
    }
});

// Function to calculate amount for a single row
function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.weight_in_kg && row.rate) {
        row.amount = flt(row.weight_in_kg) * flt(row.rate);
        console.log(`Calculated amount for row ${cdn}: ${row.amount} (weight: ${row.weight_in_kg}, rate: ${row.rate})`);
    } else {
        row.amount = 0;
        console.log(`Amount set to 0 for row ${cdn} (weight: ${row.weight_in_kg}, rate: ${row.rate})`);
    }
    frm.refresh_field('consumption_mould');
}

// Function to calculate total_consumption_valuation
function calculate_total_consumption(frm) {
    let total = 0;
    if (frm.doc.consumption_mould && Array.isArray(frm.doc.consumption_mould)) {
        frm.doc.consumption_mould.forEach(function(row) {
            total += flt(row.amount);
            console.log(`Adding amount for row ${row.name}: ${row.amount}, Running total: ${total}`);
        });
    } else {
        console.log('Child table consumption_mould is undefined or empty');
    }
    frm.set_value('total_consumption_valuation', total);
    console.log(`Total consumption valuation set to: ${total}`);
}

function calculate_mould_quantity(cdt, cdn, frm) {
    let row = locals[cdt][cdn];
    console.log("Row data:", row);

    if (row.start_no && row.end_no) {
        if (row.end_no >= row.start_no) {
            let quantity = (row.end_no - row.start_no) + 1;
            console.log(`Calculated mould_quantity: ${quantity} (end_no: ${row.end_no} - start_no: ${row.start_no})`);
            frappe.model.set_value(cdt, cdn, 'mould_quantity', quantity);
            frappe.model.set_value(cdt, cdn, 'remaining_mould', quantity);

            // Calculate total_cast_weight and total_bunch_weight
            if (row.cast_weight) {
                let total_cast_weight = row.remaining_mould * row.cast_weight;
                console.log(`Calculated total_cast_weight: ${total_cast_weight} (remaining_mould: ${row.remaining_mould} * cast_weight: ${row.cast_weight})`);
                frappe.model.set_value(cdt, cdn, 'total_cast_weight', total_cast_weight);
            } else {
                frappe.model.set_value(cdt, cdn, 'total_cast_weight', 0);
            }

            if (row.bunch_weight) {
                let total_bunch_weight = row.remaining_mould * row.bunch_weight;
                console.log(`Calculated total_bunch_weight: ${total_bunch_weight} (remaining_mould: ${row.remaining_mould} * bunch_weight: ${row.bunch_weight})`);
                frappe.model.set_value(cdt, cdn, 'total_bunch_weight', total_bunch_weight);
            } else {
                frappe.model.set_value(cdt, cdn, 'total_bunch_weight', 0);
            }
        } else {
            console.log(`Error: end_no (${row.end_no}) is less than start_no (${row.start_no})`);
            frappe.model.set_value(cdt, cdn, 'mould_quantity', 0);
            frappe.model.set_value(cdt, cdn, 'remaining_mould', 0);
            frappe.model.set_value(cdt, cdn, 'total_cast_weight', 0);
            frappe.model.set_value(cdt, cdn, 'total_bunch_weight', 0);
            frappe.msgprint({
                title: "Invalid Input",
                message: "End No cannot be smaller than Start No.",
                indicator: "red"
            });
        }
    } else {
        // Reset fields if start_no or end_no is missing
        frappe.model.set_value(cdt, cdn, 'mould_quantity', 0);
        frappe.model.set_value(cdt, cdn, 'remaining_mould', 0);
        frappe.model.set_value(cdt, cdn, 'total_cast_weight', 0);
        frappe.model.set_value(cdt, cdn, 'total_bunch_weight', 0);
    }

    // Refresh the form to ensure child table is updated, then update parent totals
    frappe.after_ajax(() => {
        frm.refresh_field('mould_table');
        update_parent_totals(frm);
    });
}

function update_parent_totals(frm) {
    let total_cast_weight = 0;
    let total_bunch_weight = 0;

    // Check if mould_table exists and is an array
    if (frm.doc.mould_table && Array.isArray(frm.doc.mould_table)) {
        console.log("Child table rows:", frm.doc.mould_table);
        frm.doc.mould_table.forEach(row => {
            console.log(`Row ${row.name}: total_cast_weight=${row.total_cast_weight}, total_bunch_weight=${row.total_bunch_weight}`);
            total_cast_weight += parseFloat(row.total_cast_weight) || 0;
            total_bunch_weight += parseFloat(row.total_bunch_weight) || 0;
        });
    } else {
        console.log("No rows in mould_table or table is undefined");
    }

    console.log(`Total Cast Weight: ${total_cast_weight}, Total Bunch Weight: ${total_bunch_weight}`);

    // Update parent doctype fields
    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_cast_weight', total_cast_weight);
    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_bunch_weight', total_bunch_weight);
}
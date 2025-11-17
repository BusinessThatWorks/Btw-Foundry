// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt


function calculate_avg_rejection(frm) {
    let total = 0, count = 0;
    if (frm.doc.rejection_table) {
        frm.doc.rejection_table.forEach(row => {
            if (row.rejection != null) {
                total += flt(row.rejection);
                count++;
            }
        });
    }
    let avg = (count > 0) ? (total / count) : 0;
    frm.set_value("rejected_qty", flt(avg, 2));
    frm.refresh_field("rejected_qty");
    console.log("📊 Live avg rejection:", avg);
}

// Clear row fields in table_yncx
function clear_flr_row_fields(cdt, cdn, frm) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;
    let row = locals[cdt][cdn];
    if ("item_name" in row) frappe.model.set_value(cdt, cdn, "item_name", "");
    if ("quantity" in row) frappe.model.set_value(cdt, cdn, "quantity", null);
    if ("quantity_rejected" in row) frappe.model.set_value(cdt, cdn, "quantity_rejected", null);

    let grid_row = frm.fields_dict["table_yncx"].grid.grid_rows_by_docname[cdn];
    if (grid_row) {
        let item_field = grid_row.get_field("item_name");
        if (item_field) {
            item_field.df.options = "";
            item_field.refresh();
        }
    }
}

// Enable/disable item_name field in specific row
function toggle_flr_item_name_field(frm, cdt, cdn, enabled) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;
    let grid_row = frm.fields_dict["table_yncx"].grid.grid_rows_by_docname[cdn];
    if (grid_row) {
        let item_field = grid_row.get_field("item_name");
        if (item_field) {
            item_field.$input.prop("disabled", !enabled);
            if (!enabled) {
                frappe.model.set_value(cdt, cdn, "item_name", "");
                item_field.df.options = "";
                item_field.refresh();
            }
        }
    }
}

// Fetch available item_name options based on pouring_id for that row
function fetch_flr_items(frm, cdt, cdn) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;
    let row = locals[cdt][cdn];
    const pouring_id = row.pouring_id;
    console.log("pouring_id:", pouring_id);

    if (pouring_id && pouring_id.includes(" - ")) {
        toggle_flr_item_name_field(frm, cdt, cdn, true);
        const parts = pouring_id.split(" - ");
        if (parts.length < 4) return;

        const custom_date = parts[1];
        const custom_shift_type = parts[2];

        frappe.call({
            method: "get_items_by_pouring_id_for_flrj",
            args: { date: custom_date, shift_type: custom_shift_type, pouring_id: pouring_id },
            callback: function (r) {
                if (r.message && Array.isArray(r.message)) {
                    let grid_row = frm.fields_dict["table_yncx"].grid.grid_rows_by_docname[cdn];
                    if (grid_row) {
                        let item_field = grid_row.get_field("item_name");
                        if (item_field) {
                            item_field.df.options = r.message.join("\n");
                            item_field.refresh();
                            frappe.model.set_value(cdt, cdn, "item_name", "");
                        }
                    }
                } else {
                    frappe.msgprint("⚠️ No items returned for this Pouring ID.");
                }
            }
        });
    } else {
        toggle_flr_item_name_field(frm, cdt, cdn, false);
    }
}

// Calculate total rejected quantity across child rows
function calculate_total_qty_rejected(frm) {
    let total = 0;
    if (frm.doc.table_yncx) {
        frm.doc.table_yncx.forEach(row => {
            total += parseFloat(row.quantity_rejected) || 0;
        });
    }
    frm.set_value('total_qty_rejected', total);
    frm.refresh_field('total_qty_rejected');
}

// Update row totals based on quantity_rejected, cast_weight, bunch_weight
function update_row_totals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row && row.quantity_rejected != null && row.cast_weight != null && row.bunch_weight != null) {
        let qty_rejected = flt(row.quantity_rejected || 0);
        let cast_weight = flt(row.cast_weight || 0);
        let bunch_weight = flt(row.bunch_weight || 0);
        let total_cast_weight = qty_rejected * cast_weight;
        let total_bunch_weight = qty_rejected * bunch_weight;
        frappe.model.set_value(cdt, cdn, "total_cast_weight", flt(total_cast_weight));
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", flt(total_bunch_weight));
    } else {
        frappe.model.set_value(cdt, cdn, "total_cast_weight", 0);
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", 0);
    }
    calculate_totals(frm);
}

// Calculate total cast and bunch weights across child rows
function calculate_totals(frm) {
    let total_qty_rejected = 0, total_flr_cast_weight = 0, total_flr_bunch_weight = 0;
    if (frm.doc.table_yncx) {
        frm.doc.table_yncx.forEach(row => {
            total_qty_rejected += parseFloat(row.quantity_rejected) || 0;
            total_flr_cast_weight += flt(row.total_cast_weight || 0);
            total_flr_bunch_weight += flt(row.total_bunch_weight || 0);
        });
    }
    frm.set_value('total_qty_rejected', total_qty_rejected);
    frm.set_value('total_flr_cast_weight', flt(total_flr_cast_weight));
    frm.set_value('total_flr_bunch_weight', flt(total_flr_bunch_weight));
    frm.refresh_field('total_qty_rejected');
    frm.refresh_field('total_flr_cast_weight');
    frm.refresh_field('total_flr_bunch_weight');
}

// Update rejection_table based on table_yncx
function update_rejection_table(frm) {
    if (!frm.doc.table_yncx || frm.doc.table_yncx.length === 0) {
        frm.clear_table('rejection_table');
        frm.set_value('rejected_qty', 0);
        frm.refresh_field('rejection_table');
        frm.refresh_field('rejected_qty');
        return;
    }

    let items = {};
    frm.doc.table_yncx.forEach(row => {
        if (row.item_name) {
            if (!items[row.item_name]) {
                items[row.item_name] = { quantity: flt(row.quantity || 0), quantity_rejected: flt(row.quantity_rejected || 0) };
            } else {
                items[row.item_name].quantity_rejected += flt(row.quantity_rejected || 0);
            }
        }
    });

    frm.clear_table('rejection_table');
    let rejection_values = [];
    Object.keys(items).forEach(item_name => {
        let total_qty = items[item_name].quantity;
        let total_rej = items[item_name].quantity_rejected;
        let rejection_perc = (total_qty > 0) ? flt((total_rej / total_qty) * 100, 2) : 0;
        let new_row = frm.add_child('rejection_table');
        new_row.item_name = item_name;
        new_row.quantity = total_qty;
        new_row.rejection = rejection_perc;
        rejection_values.push(rejection_perc);
    });

    frm.refresh_field('rejection_table');
    calculate_avg_rejection(frm); // ✅ update parent field
}

// -----------------------
// Main event handlers
// -----------------------
frappe.ui.form.on("First Line Inspection Report", {
    pouring_id: function (frm, cdt, cdn) {
        clear_flr_row_fields(cdt, cdn, frm);
        fetch_flr_items(frm, cdt, cdn);
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    },

    item_name: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        const item_code = row.item_name;
        const pouring_id = row.pouring_id;
        if (!item_code) {
            frappe.model.set_value(cdt, cdn, "quantity", null);
            calculate_total_qty_rejected(frm);
            update_rejection_table(frm);
            return;
        }
        if (pouring_id && pouring_id.includes(" - ")) {
            const parts = pouring_id.split(" - ");
            if (parts.length < 4) {
                frappe.msgprint("⚠️ Invalid Pouring ID format.");
                frappe.model.set_value(cdt, cdn, "quantity", null);
                calculate_total_qty_rejected(frm);
                update_rejection_table(frm);
                return;
            }
            const custom_date = parts[1];
            const custom_shift_type = parts[2];
            frappe.call({
                method: "frappe.client.get",
                args: { doctype: "Item", name: item_code },
                callback: function (r) {
                    if (r.message) {
                        let cast_weight = flt(r.message.custom_cast_weight_per_pc || 0);
                        let bunch_weight = flt(r.message.custom_bunch_weight_per_mould || 0);
                        frappe.model.set_value(cdt, cdn, "cast_weight", cast_weight);
                        frappe.model.set_value(cdt, cdn, "bunch_weight", bunch_weight);
                        update_row_totals(frm, cdt, cdn);
                    } else {
                        frappe.msgprint("⚠️ Item data not available.");
                        frappe.model.set_value(cdt, cdn, "cast_weight", 0);
                        frappe.model.set_value(cdt, cdn, "bunch_weight", 0);
                        update_row_totals(frm, cdt, cdn);
                    }
                    update_rejection_table(frm);
                }
            });
            frappe.call({
                method: "get_qty_by_item_for_pouring_id",
                args: { item_code: item_code, date: custom_date, shift_type: custom_shift_type },
                callback: function (r) {
                    if (r.message && r.message.qty != null) {
                        frappe.model.set_value(cdt, cdn, "quantity", r.message.qty);
                    } else {
                        frappe.model.set_value(cdt, cdn, "quantity", null);
                    }
                    calculate_total_qty_rejected(frm);
                    update_rejection_table(frm);
                }
            });
        } else {
            frappe.msgprint("⚠️ Invalid Pouring ID format.");
            frappe.model.set_value(cdt, cdn, "quantity", null);
            calculate_total_qty_rejected(frm);
            update_rejection_table(frm);
        }
    },

    quantity_rejected: function (frm, cdt, cdn) {
        update_row_totals(frm, cdt, cdn);
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    },

    table_yncx_add: function (frm, cdt, cdn) {
        clear_flr_row_fields(cdt, cdn, frm);
        toggle_flr_item_name_field(frm, cdt, cdn, false);
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    },

    table_yncx_remove: function (frm) {
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    },

    refresh: function (frm) {
        frm.fields_dict["table_yncx"].grid.grid_rows.forEach(row => {
            const cdt = row.doc.doctype, cdn = row.doc.name;
            if (!locals[cdt] || !locals[cdt][cdn]) return;
            const row_doc = locals[cdt][cdn];
            toggle_flr_item_name_field(frm, cdt, cdn, !!row_doc.pouring_id);
        });
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    },

    onload: function (frm) {
        calculate_total_qty_rejected(frm);
        update_rejection_table(frm);
    }
});

// ✅ Live update parent rejected_qty when rejection_table is edited manually
frappe.ui.form.on("Rejection Table", {
    rejection: function (frm, cdt, cdn) {
        calculate_avg_rejection(frm);
    },
    rejection_table_remove: function (frm) {
        calculate_avg_rejection(frm);
    }
});

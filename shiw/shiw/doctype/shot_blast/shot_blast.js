// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Shot Blast", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Shot Blast", {
    onload: function (frm) {
        setTimeout(() => {
            const grid = frm.fields_dict["table_short"]?.grid;
            if (!grid || !grid.wrapper) {
                console.warn("⛔ table_short grid not found");
                return;
            }

            console.log("✅ Setting up item_name focus listener");
            grid.wrapper.on("focusin", function (e) {
                const $target = $(e.target);
                if ($target.attr("data-fieldname") !== "item_name") return;

                const grid_row_el = $target.closest(".grid-row");
                const grid_row = $(grid_row_el).data("grid_row");
                if (!grid_row) return;

                // Get fresh values from fields
                const row_date = grid_row.get_field("date")?.value || frm.doc.date;
                const row_shift = grid_row.get_field("shift_type")?.value || frm.doc.shift_type;
                console.log("🕵️‍♂️ item_name clicked", "📅 Date:", row_date, "🌙 Shift Type:", row_shift);

                if (!row_date || !row_shift) {
                    console.warn("⚠️ Missing date or shift_type");
                    return;
                }

                // Fetch item options from backend
                frappe.call({
                    method: "shiw.api.get_items_from_shakeout_stock_entries.get_items_from_shakeout_stock_entries",
                    args: { date: row_date, shift_type: row_shift },
                    callback: function (r) {
                        if (r.message && Array.isArray(r.message)) {
                            const field = grid_row.get_field("item_name");
                            if (field) {
                                field.df.options = r.message.join("\n");
                                field.refresh();
                                frappe.model.set_value(grid_row.doc.doctype, grid_row.doc.name, "item_name", "");
                            }
                        } else {
                            console.error("❌ Failed to get item list");
                            frappe.msgprint("⚠️ No items returned from server.");
                        }
                    }
                });
            });
        }, 300);

        // Initial sum calculation
        update_totals_and_sums(frm);
    },

    refresh: function (frm) {
        update_totals_and_sums(frm); // Update sums on refresh
    }
});

frappe.ui.form.on("Shakeout Table", {
    date: function (frm, cdt, cdn) {
        clear_row_fields(frm, cdt, cdn);
        fetch_available_items(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after date change
    },

    shift_type: function (frm, cdt, cdn) {
        clear_row_fields(frm, cdt, cdn);
        fetch_available_items(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after shift_type change
    },

    item_name: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row || !row.item_name || !row.date || !row.shift_type) {
            frappe.model.set_value(cdt, cdn, "item_name", "");
            return;
        }

        // Fetch item weights from Item doctype
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Item",
                name: row.item_name
            },
            callback: function (r) {
                if (r.message) {
                    let cast_weight = flt(r.message.custom_cast_weight_per_pc || 0);
                    let bunch_weight = flt(r.message.custom_bunch_weight_per_mould || 0);
                    console.log("📏 Fetched from Item:", {
                        item_code: row.item_name,
                        custom_cast_weight_per_pc: r.message.custom_cast_weight_per_pc,
                        custom_bunch_weight_per_mould: r.message.custom_bunch_weight_per_mould,
                        cast_weight: cast_weight,
                        bunch_weight: bunch_weight
                    });

                    if (cast_weight === 0 || bunch_weight === 0) {
                        console.warn("⚠️ One or both weights are zero or missing for item:", row.item_name);
                    }

                    frappe.model.set_value(cdt, cdn, "casting_weight_in_kg", cast_weight);
                    frappe.model.set_value(cdt, cdn, "bunch_weight_in_kg", bunch_weight);

                    // Update totals after setting weights
                    update_totals(frm, cdt, cdn);
                    update_totals_and_sums(frm);
                } else {
                    console.error("❌ Item not found:", row.item_name);
                    frappe.msgprint("⚠️ Item data not available.");
                    frappe.model.set_value(cdt, cdn, "casting_weight_in_kg", 0);
                    frappe.model.set_value(cdt, cdn, "bunch_weight_in_kg", 0);
                    update_totals(frm, cdt, cdn);
                    update_totals_and_sums(frm);
                }
            },
            error: function (err) {
                console.error("❌ Error fetching item data:", err);
                frappe.msgprint("⚠️ Error fetching item data from server.");
                frappe.model.set_value(cdt, cdn, "casting_weight_in_kg", 0);
                frappe.model.set_value(cdt, cdn, "bunch_weight_in_kg", 0);
                update_totals(frm, cdt, cdn);
                update_totals_and_sums(frm);
            }
        });

        // Fetch shakeout quantity
        frappe.call({
            method: "shiw.api.get_recent_shakeout_qty.get_recent_shakeout_qty",
            args: {
                item_code: row.item_name,
                custom_date: row.date,
                custom_shift_type: row.shift_type
            },
            callback: function (r) {
                if (r.message && r.message.qty != null) {
                    frappe.model.set_value(cdt, cdn, "shakeout_quantity", flt(r.message.qty));
                } else {
                    frappe.msgprint("⚠️ No quantity found for this item.");
                    frappe.model.set_value(cdt, cdn, "shakeout_quantity", 0);
                }
                update_totals(frm, cdt, cdn);
                update_totals_and_sums(frm);
            }
        });

        // Fetch pouring ID
        frappe.call({
            method: "shiw.api.get_pouring_id_for_shotbrust.get_pouring_id_for_shotbrust",
            args: {
                item_code: row.item_name,
                custom_date: row.date,
                custom_shift_type: row.shift_type
            },
            callback: function (r) {
                if (r.message && r.message.custom_pouring_id) {
                    frappe.model.set_value(cdt, cdn, "pouring_id", r.message.custom_pouring_id);
                } else {
                    frappe.msgprint(r.message?.error || "⚠️ No pouring ID found.");
                    frappe.model.set_value(cdt, cdn, "pouring_id", "");
                }
            }
        });
    },

    short_blast_quantity: function (frm, cdt, cdn) {
        update_totals(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after short_blast_quantity change
    },

    table_short_add: function (frm, cdt, cdn) {
        clear_row_fields(frm, cdt, cdn);
        toggle_item_name_field(frm, cdt, cdn, false);
        update_totals_and_sums(frm); // Update sums after adding a row
    }
});

function clear_row_fields(frm, cdt, cdn) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;
    let row = locals[cdt][cdn];

    // Clear fields
    ["item_name", "shakeout_quantity", "short_blast_quantity", "pouring_id", "casting_weight_in_kg", "bunch_weight_in_kg", "total_cast_weight", "total_bunch_weight"].forEach(field => {
        if (field in row) frappe.model.set_value(cdt, cdn, field, field === "casting_weight_in_kg" || field === "bunch_weight_in_kg" || field === "total_cast_weight" || field === "total_bunch_weight" ? 0 : "");
    });

    // Reset item_name field options
    let grid_row = frm.fields_dict["table_short"].grid.grid_rows_by_docname[cdn];
    if (grid_row) {
        let item_field = grid_row.get_field("item_name");
        if (item_field) {
            item_field.df.options = "";
            item_field.refresh();
        }
    }
}

function toggle_item_name_field(frm, cdt, cdn, enabled) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;

    let grid_row = frm.fields_dict["table_short"].grid.grid_rows_by_docname[cdn];
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

function fetch_available_items(frm, cdt, cdn) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;
    let row = locals[cdt][cdn];

    toggle_item_name_field(frm, cdt, cdn, !!(row.date && row.shift_type));

    if (row.date && row.shift_type) {
        frappe.call({
            method: "shiw.api.get_items_from_shakeout_stock_entries.get_items_from_shakeout_stock_entries",
            args: { date: row.date, shift_type: row.shift_type },
            callback: function (r) {
                if (r.message && Array.isArray(r.message)) {
                    let grid_row = frm.fields_dict["table_short"].grid.grid_rows_by_docname[cdn];
                    if (grid_row) {
                        let item_field = grid_row.get_field("item_name");
                        if (item_field) {
                            item_field.df.options = r.message.join("\n");
                            item_field.refresh();
                        }
                    }
                } else {
                    frappe.msgprint("⚠️ No items returned from server.");
                }
            }
        });
    }
}

function update_totals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row && row.short_blast_quantity != null && row.casting_weight_in_kg != null && row.bunch_weight_in_kg != null) {
        let short_blast_qty = flt(row.short_blast_quantity || 0);
        let casting_weight = flt(row.casting_weight_in_kg || 0);
        let bunch_weight = flt(row.bunch_weight_in_kg || 0);

        let total_cast_weight = short_blast_qty * casting_weight;
        let total_bunch_weight = short_blast_qty * bunch_weight;

        console.log("🔢 Calculated total_cast_weight:", total_cast_weight, "total_bunch_weight:", total_bunch_weight);

        frappe.model.set_value(cdt, cdn, "total_cast_weight", flt(total_cast_weight));
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", flt(total_bunch_weight));
    } else {
        if (row.short_blast_quantity == null) console.warn("⚠️ short_blast_quantity is missing or null");
        if (row.casting_weight_in_kg == null) console.warn("⚠️ casting_weight_in_kg is missing or null");
        if (row.bunch_weight_in_kg == null) console.warn("⚠️ bunch_weight_in_kg is missing or null");
        frappe.model.set_value(cdt, cdn, "total_cast_weight", 0);
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", 0);
    }
}

function update_totals_and_sums(frm) {
    let total_shot_blast_cast_weight = 0;
    let total_shot_blast_bunch_weight = 0;

    if (frm.doc.table_short) {
        frm.doc.table_short.forEach(row => {
            total_shot_blast_cast_weight += flt(row.total_cast_weight || 0);
            total_shot_blast_bunch_weight += flt(row.total_bunch_weight || 0);
        });
        console.log("📊 Summed total_shot_blast_cast_weight:", total_shot_blast_cast_weight, "total_shot_blast_bunch_weight:", total_shot_blast_bunch_weight);
    } else {
        console.log("⚠️ No table_short rows found");
    }

    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_shot_blast_cast_weight', flt(total_shot_blast_cast_weight));
    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_shot_blast_bunch_weight', flt(total_shot_blast_bunch_weight));
}
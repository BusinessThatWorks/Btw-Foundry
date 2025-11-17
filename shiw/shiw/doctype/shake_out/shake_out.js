// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Shake Out", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Shake Out', {
    onload: function (frm) {
        setTimeout(() => {
            const grid = frm.fields_dict["table_abc"]?.grid;
            if (!grid || !grid.wrapper) {
                console.warn("⛔ table_abc grid not found");
                return;
            }

            console.log("✅ Setting up item_name focus listener");
            grid.wrapper.on("focusin", function (e) {
                const $target = $(e.target);
                if ($target.attr("data-fieldname") === "item_name") {
                    const grid_row_el = $target.closest(".grid-row");
                    const grid_row = $(grid_row_el).data("grid_row");

                    if (grid_row) {
                        const row_date = grid_row.get_field("date")?.value || frm.doc.date;
                        const row_shift = grid_row.get_field("shift_type")?.value || frm.doc.shift_type;
                        console.log("🕵️‍♂️ item_name clicked, Date:", row_date, "Shift Type:", row_shift);

                        if (!row_date || !row_shift) {
                            console.warn("⚠️ Missing date or shift_type");
                            return;
                        }

                        frappe.call({
                            method: "shiw.api.get_items_from_pouring_stock_entries.get_items_from_pouring_stock_entries",
                            args: {
                                date: row_date,
                                shift_type: row_shift
                            },
                            callback: function (r) {
                                if (r.message && Array.isArray(r.message)) {
                                    const item_options = r.message;
                                    console.log("📦 Got item options:", item_options);

                                    const field = grid_row.get_field('item_name');
                                    if (field) {
                                        field.df.options = item_options.join('\n');
                                        field.refresh();
                                        frappe.model.set_value(grid_row.doc.doctype, grid_row.doc.name, 'item_name', '');
                                    }
                                } else {
                                    console.error("❌ Failed to get item list");
                                    frappe.msgprint("⚠️ No items returned from server.");
                                }
                            },
                            error: function (err) {
                                console.error("❌ Error fetching item options:", err);
                                frappe.msgprint("⚠️ Error fetching items from server.");
                            }
                        });
                    }
                }
            });
        }, 300);

        frm.fields_dict["table_abc"].grid.grid_rows.forEach(row => {
            toggle_item_name_field(frm, row.doc.doctype, row.doc.name, row.doc.date && row.doc.shift_type);
        });
        update_totals_and_sums(frm); // Initial sum calculation
    },

    on_submit: function (frm) {
        console.log(`🔵 Shake Out Document Submitted: ${frm.doc.name}`);
        // ✅ Stock Entry will be handled by server script now.
    },

    refresh: function (frm) {
        update_totals_and_sums(frm); // Update sums on refresh
    }
});

frappe.ui.form.on('Treatment Table', {
    date: function (frm, cdt, cdn) {
        clear_row_fields(cdt, cdn);
        fetch_available_items(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after date change
    },

    shift_type: function (frm, cdt, cdn) {
        clear_row_fields(cdt, cdn);
        fetch_available_items(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after shift_type change
    },

    item_name: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.date || !row.shift_type) {
            frappe.model.set_value(cdt, cdn, "item_name", "");

            return;
        }

        if (row.item_name) {
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
                            bunch_weight: bunch_weight,
                            full_response: r.message
                        });

                        if (cast_weight === 0 || bunch_weight === 0) {
                            console.warn("⚠️ One or both weights are zero or missing for item:", row.item_name);
                        }

                        frappe.model.set_value(cdt, cdn, "casting_weight_in_kg", cast_weight);
                        frappe.model.set_value(cdt, cdn, "bunch_weight_in_kg", bunch_weight);

                        // Fetch recent pouring quantity
                        frappe.call({
                            method: "shiw.api.get_recent_pouring_qty.get_recent_pouring_qty",
                            args: {
                                item_code: row.item_name,
                                custom_date: row.date,
                                custom_shift_type: row.shift_type
                            },
                            callback: function (r) {
                                if (r.message && r.message.qty != null) {
                                    frappe.model.set_value(cdt, cdn, "prod_cast", flt(r.message.qty));
                                } else {
                                    frappe.msgprint("⚠️ No quantity found for this item.");
                                    frappe.model.set_value(cdt, cdn, "prod_cast", 0);
                                }
                                update_totals(frm, cdt, cdn);
                                update_totals_and_sums(frm);
                            },
                            error: function (err) {
                                console.error("❌ Error fetching pouring qty:", err);
                                frappe.msgprint("⚠️ Error fetching pouring quantity.");
                                frappe.model.set_value(cdt, cdn, "prod_cast", 0);
                                update_totals(frm, cdt, cdn);
                                update_totals_and_sums(frm);
                            }
                        });

                        // Fetch pouring ID
                        frappe.call({
                            method: "shiw.api.get_pouring_id_by_item.get_pouring_id_by_item",
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
                            },
                            error: function (err) {
                                console.error("❌ Error fetching pouring ID:", err);
                                frappe.msgprint("⚠️ Error fetching pouring ID.");
                                frappe.model.set_value(cdt, cdn, "pouring_id", "");
                            }
                        });

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
        }
    },

    shake_out_qty: function (frm, cdt, cdn) {
        update_totals(frm, cdt, cdn);
        update_totals_and_sums(frm); // Update sums after shake_out_qty change
    },

    table_abc_add: function (frm, cdt, cdn) {
        clear_row_fields(cdt, cdn);
        toggle_item_name_field(frm, cdt, cdn, false);
        update_totals_and_sums(frm); // Update sums after adding a row
    }
});

function clear_row_fields(cdt, cdn) {
    if (!locals[cdt] || !locals[cdt][cdn]) return;

    let row = locals[cdt][cdn];
    if ("item_name" in row) frappe.model.set_value(cdt, cdn, "item_name", "");
    if ("prod_cast" in row) frappe.model.set_value(cdt, cdn, "prod_cast", 0);
    if ("shake_out_qty" in row) frappe.model.set_value(cdt, cdn, "shake_out_qty", 0);
    if ("pouring_id" in row) frappe.model.set_value(cdt, cdn, "pouring_id", "");
    if ("casting_weight_in_kg" in row) frappe.model.set_value(cdt, cdn, "casting_weight_in_kg", 0);
    if ("bunch_weight_in_kg" in row) frappe.model.set_value(cdt, cdn, "bunch_weight_in_kg", 0);
    if ("total_casting_weight" in row) frappe.model.set_value(cdt, cdn, "total_casting_weight", 0);
    if ("total_bunch_weight" in row) frappe.model.set_value(cdt, cdn, "total_bunch_weight", 0);

    let grid_row = cur_frm.fields_dict["table_abc"].grid.grid_rows_by_docname[cdn];
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

    let grid_row = frm.fields_dict["table_abc"].grid.grid_rows_by_docname[cdn];
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
            method: "shiw.api.get_items_from_pouring_stock_entries.get_items_from_pouring_stock_entries",
            args: {
                date: row.date,
                shift_type: row.shift_type
            },
            callback: function (r) {
                if (r.message && Array.isArray(r.message)) {
                    let grid_row = frm.fields_dict["table_abc"].grid.grid_rows_by_docname[cdn];
                    if (grid_row) {
                        let item_field = grid_row.get_field("item_name");
                        if (item_field) {
                            item_field.df.options = r.message.join("\n");
                            item_field.refresh();
                        }
                    }
                } else {
                    console.error("❌ Failed to fetch items for date:", row.date, "shift:", row.shift_type);
                    frappe.msgprint("⚠️ No items returned from server.");
                }
            },
            error: function (err) {
                console.error("❌ Error fetching available items:", err);
                frappe.msgprint("⚠️ Error fetching items from server.");
            }
        });
    }
}

function update_totals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row && row.shake_out_qty != null && row.casting_weight_in_kg != null && row.bunch_weight_in_kg != null) {
        let shake_out_qty = flt(row.shake_out_qty || 0);
        let casting_weight = flt(row.casting_weight_in_kg || 0);
        let bunch_weight = flt(row.bunch_weight_in_kg || 0);

        let total_casting_weight = shake_out_qty * casting_weight;
        let total_bunch_weight = shake_out_qty * bunch_weight;

        console.log("🔢 Calculated total_casting_weight:", total_casting_weight, "total_bunch_weight:", total_bunch_weight);

        frappe.model.set_value(cdt, cdn, "total_casting_weight", flt(total_casting_weight));
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", flt(total_bunch_weight));
    } else {
        if (row.shake_out_qty == null) console.warn("⚠️ shake_out_qty is missing or null");
        if (row.casting_weight_in_kg == null) console.warn("⚠️ casting_weight_in_kg is missing or null");
        if (row.bunch_weight_in_kg == null) console.warn("⚠️ bunch_weight_in_kg is missing or null");
        frappe.model.set_value(cdt, cdn, "total_casting_weight", 0);
        frappe.model.set_value(cdt, cdn, "total_bunch_weight", 0);
    }
}

function update_totals_and_sums(frm) {
    let total_shakeout_cast_weight = 0;
    let total_shakeout_bunch_weight = 0;

    if (frm.doc.table_abc) {
        frm.doc.table_abc.forEach(row => {
            total_shakeout_cast_weight += flt(row.total_casting_weight || 0);
            total_shakeout_bunch_weight += flt(row.total_bunch_weight || 0);
        });
        console.log("📊 Summed total_shakeout_cast_weight:", total_shakeout_cast_weight, "total_shakeout_bunch_weight:", total_shakeout_bunch_weight);
    } else {
        console.log("⚠️ No table_abc rows found");
    }

    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_shakeout_cast_weight', flt(total_shakeout_cast_weight));
    frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_shakeout_bunch_weight', flt(total_shakeout_bunch_weight));
}
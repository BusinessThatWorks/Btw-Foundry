// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

const STAGE_WAREHOUSE = {
    "Finishing": "Finishing - SHIW",
    "Fettling": "Fettling - SHIW",
};

const fetchTokensByRow = Object.create(null); // guard against stale ajax responses
let isRebuildingTable = false; // guard against infinite refresh loops
let isRefreshing = false; // guard against refresh handler loops
let formInitialized = new Set(); // track which forms have been initialized

function toFloat(v) {
    const n = parseFloat(String(v ?? "").replace(/,/g, ""));
    return Number.isFinite(n) ? n : 0;
}

function round2(v) {
    return Math.round((toFloat(v) + Number.EPSILON) * 100) / 100;
}

// Clear key fields for a new/blank row
function clear_row_fields(cdt, cdn) {
    console.log(`Clearing fields for row: ${cdn}`);
    frappe.model.set_value(cdt, cdn, "item_name", null);
    frappe.model.set_value(cdt, cdn, "rejection_stage", null);
    frappe.model.set_value(cdt, cdn, "available_quantity", null);
    frappe.model.set_value(cdt, cdn, "rejected_qty", null);
    frappe.model.set_value(cdt, cdn, "cast_weight_in_kg", null);
}

// Fetch on-hand qty for the row's item + stage (with stale-response guard)
function fetch_available_quantity(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    const item_code = row.item_name;
    const stage = row.rejection_stage;

    if (!item_code || !stage) {
        console.log(`Skipping fetch: item_code=${item_code}, stage=${stage}`);
        frappe.model.set_value(cdt, cdn, "available_quantity", null);
        return;
    }

    const warehouse = STAGE_WAREHOUSE[stage] || null;
    if (!warehouse) {
        console.log(`No valid warehouse for stage: ${stage}`);
        frappe.model.set_value(cdt, cdn, "available_quantity", null);
        return;
    }

    const token = `${item_code}|${warehouse}|${Date.now()}`;
    fetchTokensByRow[cdn] = token;

    console.log(`Fetching available quantity for item: ${item_code}, warehouse: ${warehouse}`);
    frappe.call({
        method: "get_qty_for_fettling",   // whitelisted server script
        args: { item_code, warehouse },
        freeze: false,
        callback: function (r) {
            // Ignore stale responses
            if (fetchTokensByRow[cdn] !== token) {
                console.log("Stale qty response ignored for row:", cdn);
                return;
            }
            const qty = (r && r.message && ("qty" in r.message)) ? toFloat(r.message.qty) : 0;
            console.log(`Fetched available quantity: ${qty}`);
            frappe.model.set_value(cdt, cdn, "available_quantity", qty);
        },
        error: function (err) {
            if (fetchTokensByRow[cdn] !== token) return;
            console.error("Error fetching qty:", err);
            frappe.model.set_value(cdt, cdn, "available_quantity", 0);
        }
    });
}

// Recompute totals: sum(rejected_qty) and sum(rejected_qty * cast_weight_in_kg)
function recompute_totals(frm) {
    const rows = frm.doc.table_scpn || [];
    let total_qty = 0;
    let total_weight = 0;

    rows.forEach(row => {
        const q = toFloat(row.rejected_qty);
        const wtkg = toFloat(row.cast_weight_in_kg);
        total_qty += q;
        total_weight += q * wtkg;
    });

    const tq = round2(total_qty);
    const tw = round2(total_weight);

    console.log(`Totals -> quantity: ${tq}, weight: ${tw}`);
    // Use frappe.model.set_value to avoid triggering refresh
    frappe.model.set_value(frm.doctype, frm.docname, "total_rejected_quantity", tq);
    frappe.model.set_value(frm.doctype, frm.docname, "rejected_wt", tw);
}

// --- NEW helper: recompute average rejection% ---
function recompute_avg_rejection(frm) {
    const rows = frm.doc.rejection_table || [];
    if (!rows.length) {
        frappe.model.set_value(frm.doctype, frm.docname, "rejected_qty", 0);
        return;
    }

    let total = 0;
    rows.forEach(r => {
        total += toFloat(r.rejection);
    });

    const avg = round2(total / rows.length);
    console.log(`Avg rejection% across table: ${avg}`);
    // Use frappe.model.set_value to avoid triggering refresh
    frappe.model.set_value(frm.doctype, frm.docname, "rejected_qty", avg);
}

// --- Rebuild Rejection Table from all rows ---
function rebuild_rejection_table(frm) {
    // Prevent infinite loops
    if (isRebuildingTable) {
        return;
    }

    // Don't rebuild if form is being saved/submitted
    if (frm.is_saving || frm.is_submitting) {
        return;
    }

    isRebuildingTable = true;

    try {
        const rows = frm.doc.table_scpn || [];

        // Group by item_name only - sum quantities across different rejection stages
        const grouped = {};

        rows.forEach(row => {
            const item = row.item_name;
            const available_qty = toFloat(row.available_quantity);
            const rejected_qty = toFloat(row.rejected_qty);

            if (!item || !available_qty) return;  // skip incomplete rows

            // Group by item_name only - sum quantities even if rejection_stage is different
            if (!grouped[item]) {
                grouped[item] = {
                    item_name: item,
                    total_available_qty: 0,
                    total_rejected_qty: 0
                };
            }

            // Sum quantities for same item (across all rejection stages)
            grouped[item].total_available_qty += available_qty;
            grouped[item].total_rejected_qty += rejected_qty;
        });

        // Clear and rebuild rejection_table
        frm.clear_table("rejection_table");

        Object.keys(grouped).forEach(item_name => {
            const group = grouped[item_name];
            const rejection_pct = group.total_available_qty > 0
                ? round2((group.total_rejected_qty / group.total_available_qty) * 100)
                : 0;

            let child = frm.add_child("rejection_table");
            child.item_name = group.item_name;
            child.quantity = group.total_available_qty;
            child.rejection = rejection_pct;
        });

        // Refresh field without triggering form refresh
        // Only refresh if the form is not currently being refreshed
        if (!isRefreshing) {
            frm.refresh_field("rejection_table");
        }

        // Update parent avg rejection% immediately (no delay needed)
        recompute_avg_rejection(frm);
        isRebuildingTable = false;
    } catch (error) {
        isRebuildingTable = false;
        console.error("Error in rebuild_rejection_table:", error);
    }
}

// --- Parent Doc Events ---
frappe.ui.form.on("Second Line Rejection", {
    refresh: function (frm) {
        console.log("Second Line Rejection form refreshed");

        // Prevent refresh loop - if already refreshing, skip
        if (isRefreshing || isRebuildingTable) {
            console.log("Skipping refresh handler - already processing");
            return;
        }

        // Get form identifier (name or __islocal for new docs)
        const formId = frm.doc.name || frm.doc.__islocal || 'new';

        // Only recompute if form is in draft status and not currently saving/submitting
        if (frm.doc.docstatus === 0 && !frm.is_saving && !frm.is_submitting) {
            // Only run initialization logic once per form load
            // Skip if form was already initialized in this session
            if (!formInitialized.has(formId)) {
                formInitialized.add(formId);

                // Set flag to prevent recursive calls
                isRefreshing = true;

                // Use setTimeout to avoid refresh loop - run after form is fully loaded
                setTimeout(() => {
                    // Double-check conditions before running
                    if (frm.doc && frm.doc.docstatus === 0 && !frm.is_saving && !frm.is_submitting && !isRebuildingTable) {
                        try {
                            // Only recompute totals on initial load
                            // Don't rebuild rejection_table here - it's handled by child table events
                            // This prevents refresh loops
                            if (frm.doc.table_scpn && frm.doc.table_scpn.length > 0) {
                                recompute_totals(frm);
                                // Only rebuild rejection_table if it's empty (initial load)
                                if (!frm.doc.rejection_table || frm.doc.rejection_table.length === 0) {
                                    rebuild_rejection_table(frm);
                                }
                            }
                        } catch (error) {
                            console.error("Error in refresh handler:", error);
                        }
                    }
                    // Reset flag after processing
                    isRefreshing = false;
                }, 150);
            } else {
                // Form already initialized, just ensure totals are correct
                // Don't rebuild table to avoid refresh loops
                if (frm.doc.table_scpn && frm.doc.table_scpn.length > 0) {
                    recompute_totals(frm);
                }
            }
        } else {
            // If form is submitted or saving, remove from initialized set and reset flag
            formInitialized.delete(formId);
            isRefreshing = false;
        }
    },

    validate: function (frm) {
        console.log("Validating Second Line Rejection form");
        // Only recompute totals during validate, don't rebuild table to avoid refresh issues
        recompute_totals(frm);

        const bad_rows = [];
        (frm.doc.table_scpn || []).forEach((row, idx) => {
            const rejected = toFloat(row.rejected_qty);
            const available = toFloat(row.available_quantity);
            if (rejected > available) {
                bad_rows.push({ idx: idx + 1, item: row.item_name, rejected, available });
            }
        });

        if (bad_rows.length) {
            const msg = bad_rows.map(r =>
                `Row ${r.idx}: Item ${r.item} → Rejected (${r.rejected}) > Available (${r.available})`
            ).join("<br>");
            frappe.throw(__(`Rejected Qty cannot exceed Available Quantity:<br>${msg}`));
        }
    },

    table_scpn_remove: function (frm) {
        console.log("Row removed from table_scpn");
        recompute_totals(frm);
        rebuild_rejection_table(frm);
    },

    table_scpn_add: function (frm, cdt, cdn) {
        console.log("New row added to table_scpn");
        clear_row_fields(cdt, cdn);
    }
});

// --- Child Table Events (Second Line Rejection Table) ---
frappe.ui.form.on("Second Line Rejection Table", {
    item_name: function (frm, cdt, cdn) {
        console.log(`Item changed in row: ${cdn}`);
        fetch_available_quantity(frm, cdt, cdn);
        recompute_totals(frm);
        rebuild_rejection_table(frm);
    },

    rejection_stage: function (frm, cdt, cdn) {
        console.log(`Rejection stage changed in row: ${cdn}`);
        fetch_available_quantity(frm, cdt, cdn);
        rebuild_rejection_table(frm);
    },

    rejected_qty: function (frm, cdt, cdn) {
        console.log(`Rejected qty changed in row: ${cdn}`);
        recompute_totals(frm);
        rebuild_rejection_table(frm);
    },

    cast_weight_in_kg: function (frm) {
        recompute_totals(frm);
    },

    available_quantity: function (frm, cdt, cdn) {
        rebuild_rejection_table(frm);
    }
});

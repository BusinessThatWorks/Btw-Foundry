// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Final inspection", {
// 	refresh(frm) {

// 	},
// });




// frappe.ui.form.on("Final inspection", {
//     refresh(frm) {
//         function clear_row_fields(cdt, cdn, frm) {
//             const row = locals[cdt][cdn];
//             if (!row) return;

//             console.log("🧹 Clearing row fields for:", cdn);

//             frappe.model.set_value(cdt, cdn, "item_name", "");
//             frappe.model.set_value(cdt, cdn, "finished_qty", null);
//             frappe.model.set_value(cdt, cdn, "gn_qty", null);

//             const grid_row = frm.fields_dict["table_jikz"].grid.grid_rows_by_docname[cdn];
//             if (grid_row) {
//                 const item_field = grid_row.get_field("item_name");
//                 if (item_field) {
//                     item_field.df.options = "";
//                     item_field.refresh();
//                 }
//             }
//         }

//         frappe.ui.form.on("Inspection Table", {
//             item_name(frm, cdt, cdn) {
//                 const row = locals[cdt][cdn];
//                 const item_name = row.item_name;

//                 console.log("🟡 Item Name changed:", item_name);

//                 if (!item_name) {
//                     console.warn("⚠️ No item name provided, clearing finished_qty");
//                     frappe.model.set_value(cdt, cdn, "finished_qty", null);
//                     return;
//                 }

//                 console.log("📡 Calling server script get_qty_for_fettling with:", {
//                     item_name: item_name, // Changed from item_code to item_name
//                     warehouse: "Finishing - SHIW"
//                 });

//                 frappe.call({
//                     method: "shiw.api.get_qty_for_fettling.get_qty_for_fettling",
//                     args: {
//                         item_name: item_name,
//                         warehouse: "Finishing - SHIW"
//                     },
//                     callback(r) {
//                         console.log("📥 Server response:", r.message);

//                         if (r.message && r.message.qty != null) {
//                             console.log("✅ Setting finished_qty to:", r.message.qty);
//                             frappe.model.set_value(cdt, cdn, "finished_qty", r.message.qty);
//                         } else {
//                             console.warn("❌ No quantity returned from server. Message:", r.message?.message);
//                             frappe.msgprint(r.message?.message || "⚠️ Could not fetch quantity.");
//                             frappe.model.set_value(cdt, cdn, "finished_qty", null);
//                         }
//                     }
//                 });
//             },

//             table_jikz_add(frm, cdt, cdn) {
//                 console.log("➕ New row added to Inspection Table:", cdn);
//                 clear_row_fields(cdt, cdn, frm);
//             }
//         });
//     },
// });

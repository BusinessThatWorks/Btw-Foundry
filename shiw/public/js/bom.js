


// frappe.ui.form.on("BOM", {
//     refresh(frm) {
//         frm.add_custom_button("Update Item Rates", async function () {
//             const items = frm.doc.items.map(row => ({
//                 item_code: row.item_code,
//                 item_name: row.item_name
//             }));

//             console.log("Sending to server:", items);

//             try {
//                 const res = await frappe.call({
//                     method: "shiw.api.bom.get_updated_item_rates",
//                     args: { items }
//                 });

//                 const rates = res.message || {};
//                 console.log("Server response:", rates);

//                 frm.doc.items.forEach(row => {
//                     const rate_data = rates[row.item_code];
//                     if (rate_data) {
//                         console.log(`Updating ${row.item_code}:`, rate_data);

//                         frappe.model.set_value(row.doctype, row.name, "rate", rate_data.rate);
//                         frappe.model.set_value(row.doctype, row.name, "amount", rate_data.rate * row.qty);
//                     }
//                 });

//                 frm.refresh_field("items");
//             } catch (err) {
//                 console.error("Error fetching rates:", err);
//             }
//         });
//     }
// });





// // frappe.ui.form.on('BOM', {
// //     refresh(frm) {
// //         if (!frm.is_new()) {
// //             frm.add_custom_button("Update Item Rates", () => {
// //                 frappe.call({
// //                     method: "shiw.override.bom.update_bom_item_rates_directly",
// //                     args: {
// //                         bom_name: frm.doc.name
// //                     },
// //                     callback: function (r) {
// //                         frappe.msgprint(r.message);
// //                     }
// //                 });
// //             });
// //         }
// //     }
// // });





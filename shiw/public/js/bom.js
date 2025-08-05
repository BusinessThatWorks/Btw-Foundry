// frappe.ui.form.on("BOM", {
//     refresh: function (frm) {
//         frm.add_custom_button("Update Item Rates", function () {
//             // Collect items to pass to server
//             const items = frm.doc.items.map(row => ({
//                 item_code: row.item_code,
//                 item_name: row.item_name
//             }));

//             // Call server method
//             frappe.call({
//                 method: "shiw.api.bom.get_updated_item_rates",
//                 args: { items },
//                 callback: function (r) {
//                     if (!r.message) return;

//                     const rates = r.message;

//                     frm.doc.items.forEach(row => {
//                         if (rates[row.item_code]) {
//                             row.rate = rates[row.item_code];
//                             row.amount = row.rate * row.qty;
//                         }
//                     });

//                     frm.refresh_field("items");
//                     frappe.msgprint("Rates updated from Stock Ledger.");
//                 }
//             });
//         });
//     }
// });



// frappe.ui.form.on("BOM", {
//     refresh: function (frm) {
//         frm.add_custom_button("Update Item Rates", function () {
//             console.log("🔘 Button clicked: Update Item Rates");

//             // Prepare items to send
//             const items = frm.doc.items.map(row => ({
//                 item_code: row.item_code,
//                 item_name: row.item_name
//             }));

//             console.log("📦 Sending items to server:", items);

//             frappe.call({
//                 method: "shiw.api.bom.get_updated_item_rates",  // 🔁 adjust path if needed
//                 args: { items },
//                 callback: function (r) {
//                     console.log("📡 Raw response:", r);

//                     if (!r.message) {
//                         console.warn("⚠️ No response received from server.");
//                         frappe.msgprint("No rates were returned.");
//                         return;
//                     }

//                     const rates = r.message;
//                     console.log("✅ Received rates:", rates);

//                     frm.doc.items.forEach(row => {
//                         const updated_rate = rates[row.item_code];
//                         if (updated_rate !== undefined) {
//                             console.log(`🔄 Updating ${row.item_code}: ${row.rate} → ${updated_rate}`);
//                             row.rate = updated_rate;
//                             row.amount = row.rate * row.qty;
//                         } else {
//                             console.log(`❌ No rate found for ${row.item_code}`);
//                         }
//                     });

//                     frm.refresh_field("items");
//                     frappe.msgprint("Rates updated from Stock Ledger.");
//                 },
//                 error: function (err) {
//                     console.error("🚨 Server error:", err);
//                 }
//             });
//         });
//     }
// });



// frappe.ui.form.on("BOM", {
//     refresh(frm) {
//         frm.add_custom_button("Update Item Rates", async function () {
//             const items = frm.doc.items.map(row => ({
//                 item_code: row.item_code,
//                 item_name: row.item_name
//             }));

//             console.log("Sending items to server:", items);

//             const res = await frappe.call({
//                 method: "shiw.api.bom.get_updated_item_rates",
//                 args: { items },
//             });

//             const rates = res.message || {};
//             console.log("Received rates:", rates);

//             frm.doc.items.forEach((row) => {
//                 const rate_info = rates[row.item_code];
//                 if (rate_info) {
//                     console.log("Updating", row.item_name + ":", rate_info);

//                     frappe.model.set_value(row.doctype, row.name, "rate", rate_info.rate);
//                     frappe.model.set_value(row.doctype, row.name, "amount", flt(rate_info.rate) * flt(row.qty));
//                 }
//             });

//             frm.refresh_field("items");
//         });
//     }
// });




frappe.ui.form.on("BOM", {
    refresh(frm) {
        frm.add_custom_button("Update Item Rates", async function () {
            const items = frm.doc.items.map(row => ({
                item_code: row.item_code,
                item_name: row.item_name
            }));

            console.log("Sending to server:", items);

            try {
                const res = await frappe.call({
                    method: "shiw.api.bom.get_updated_item_rates",
                    args: { items }
                });

                const rates = res.message || {};
                console.log("Server response:", rates);

                frm.doc.items.forEach(row => {
                    const rate_data = rates[row.item_code];
                    if (rate_data) {
                        console.log(`Updating ${row.item_code}:`, rate_data);

                        frappe.model.set_value(row.doctype, row.name, "rate", rate_data.rate);
                        frappe.model.set_value(row.doctype, row.name, "amount", rate_data.rate * row.qty);
                    }
                });

                frm.refresh_field("items");
            } catch (err) {
                console.error("Error fetching rates:", err);
            }
        });
    }
});











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
//                 frappe.msgprint("✅ Custom item rates updated from button.");
//             } catch (err) {
//                 console.error("Error fetching rates:", err);
//             }
//         });
//     },

//     after_submit(frm) {
//         frappe.msgprint("✅ Custom item rates have been re-applied after Submit.");
//     }
// });

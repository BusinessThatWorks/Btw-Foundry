frappe.ui.form.on("Production Plan", {
    get_department(frm) {
        console.log("🟢 Get Department button clicked");
        console.log("🔍 Form document:", frm.doc);
        console.log("🔍 MR Items:", frm.doc.mr_items);

        if (!frm.doc.mr_items || frm.doc.mr_items.length === 0) {
            frappe.msgprint("No items found in Material Request Plan table.");
            console.log("⚠️ No mr_items found");
            return;
        }

        // Get item_codes instead of item_names for better accuracy
        const item_codes = frm.doc.mr_items.map(d => d.item_code).filter(code => code);
        console.log("📦 Sending item codes to server:", item_codes);

        if (item_codes.length === 0) {
            frappe.msgprint("No item codes found in the table.");
            return;
        }

        console.log("🚀 Making API call to: shiw.api.get_departments_for_items.get_departments_for_items");

        frappe.call({
            method: "shiw.api.get_departments_for_items.get_departments_for_items",
            args: { items: item_codes },
            callback: function (r) {
                console.log("🧾 Raw server response:", r);
                console.log("🧾 Response message:", r.message);
                console.log("🧾 Response exc:", r.exc);

                if (r.message && Object.keys(r.message).length > 0) {
                    frm.doc.mr_items.forEach(row => {
                        const dept = r.message[row.item_code];
                        if (dept) {
                            row.custom_department = dept;
                            console.log(`✅ Updated ${row.item_code} → ${dept}`);
                        } else {
                            row.custom_department = "";
                            console.log(`⚠️ No department found for ${row.item_code}`);
                        }
                    });
                    frm.refresh_field("mr_items");
                    frappe.msgprint("Departments updated successfully!");
                } else {
                    frappe.msgprint("No departments found for the given items.");
                    console.log("❌ Empty or invalid response from server");
                }
            },
            error: function (r) {
                console.error("❌ API call failed:", r);
                frappe.msgprint("Error calling API: " + (r.message || "Unknown error"));
            }
        });
    }
});

// Auto-fetch department when item_code changes in Material Request Plan Item
frappe.ui.form.on("Material Request Plan Item", {
    item_code(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            console.log(`🔄 Auto-fetching department for item_code: ${row.item_code}`);

            // Trigger the fetch_from functionality
            frappe.model.trigger("item_code", "fetch_from", row, row.doctype);

            // Also manually fetch if needed
            frappe.call({
                method: "shiw.api.get_departments_for_items.get_departments_for_items",
                args: { items: [row.item_code] },
                callback: function (r) {
                    if (r.message && r.message[row.item_code]) {
                        row.custom_department = r.message[row.item_code];
                        frm.refresh_field("mr_items");
                        console.log(`✅ Auto-updated ${row.item_code} → ${r.message[row.item_code]}`);
                    }
                }
            });
        }
    }
});
console.log("Ultimate Test: JS file loaded and executed!");



frappe.ui.form.on('No-Bake Mould Batch', {
    // Optional: if you want to do something on parent form load
    refresh: function (frm) {
        console.log("No-Bake Mould Batch form loaded");
    }
});

// // Listen to changes in child table 'New Mould Table' fields
// frappe.ui.form.on('New Mould Table', {
//     start_no: function (frm, cdt, cdn) {
//         console.log("Start No changed for child row:", cdn);
//         calculate_mould_quantity(cdt, cdn);
//     },
//     end_no: function (frm, cdt, cdn) {
//         console.log("End No changed for child row:", cdn);
//         calculate_mould_quantity(cdt, cdn);
//     }
// });

// function calculate_mould_quantity(cdt, cdn) {
//     let row = locals[cdt][cdn];
//     console.log("Row data:", row);

//     if (row.start_no && row.end_no) {
//         if (row.end_no >= row.start_no) {
//             let quantity = (row.end_no - row.start_no) + 1;
//             console.log(`Calculated mould_quantity: ${quantity} (end_no: ${row.end_no} - start_no: ${row.start_no})`);
//             frappe.model.set_value(cdt, cdn, 'mould_quantity', quantity);
//             frappe.model.set_value(cdt, cdn, 'remaining_mould', quantity);
//         } else {
//             console.error(`Error: end_no (${row.end_no}) is less than start_no (${row.start_no})`);
//             frappe.model.set_value(cdt, cdn, 'mould_quantity', 0);
//             frappe.model.set_value(cdt, cdn, 'remaining_mould', 0);
//             frappe.msgprint({
//                 title: "Invalid Input",
//                 message: "End No cannot be smaller than Start No.",
//                 indicator: "red"
//             });
//         }
//     } else {
//         console.log("Start No or End No is not set yet");
//     }
// }
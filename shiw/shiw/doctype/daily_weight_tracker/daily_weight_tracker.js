// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Weight Tracker", {
// 	refresh(frm) {

// 	},
// });




if (!window._diff_highlight_style_added) {
    const style = document.createElement('style');
    style.innerHTML = `
        .highlight-diff-red {
            color: red !important;
            font-weight: bold;
        }
        .highlight-diff-green {
            color: green !important;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
    window._diff_highlight_style_added = true;
}

frappe.ui.form.on('Daily Weight Tracker Table', {
    item: function (frm, cdt, cdn) {
        setTimeout(() => calculate_weight_and_difference(frm, cdt, cdn), 300);
    },
    quantity: function (frm, cdt, cdn) {
        calculate_weight_and_difference(frm, cdt, cdn);
    },
    total_weight_in_kg: function (frm, cdt, cdn) {
        calculate_weight_and_difference(frm, cdt, cdn);
    }
});

function calculate_weight_and_difference(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    const qty = row.quantity || 0;
    const total_wt = row.total_weight_in_kg || 0;

    if (qty && total_wt) {
        const weight = total_wt / qty;
        console.log(`✅ weight = ${total_wt} / ${qty} = ${weight}`);

        frappe.model.set_value(cdt, cdn, 'weight', weight).then(() => {
            const updated = locals[cdt][cdn];
            const book = updated.book_weight || 0;
            // const diff = book - weight;
            const diff = weight - book;
            console.log(`✅ difference = ${book} - ${weight} = ${diff}`);

            frappe.model.set_value(cdt, cdn, 'difference', diff).then(() => {
                // Compute percentage difference = (difference / book_weight) * 100
                const percent = (book && !isNaN(book)) ? ((diff / book) * 100) : 0;
                frappe.model.set_value(cdt, cdn, 'difference_percent', percent).then(() => {
                    setTimeout(() => highlight_difference_field(frm, cdn), 200);
                });
            });
        });
    } else {
        console.log("⚠️ Missing quantity or total_weight_in_kg");
    }
}

function highlight_difference_field(frm, cdn) {
    const grid = frm.fields_dict['table_btjs'].grid;
    const grid_row = grid.get_row(cdn);
    if (!grid_row) return;

    const $row = $(grid_row.wrapper);
    const $field = $row.find('[data-fieldname="difference"]');
    if (!$field.length) {
        console.warn('⚠️ Difference field DOM not found');
        return;
    }

    // Clean up old styles
    $field.removeClass("highlight-diff-green highlight-diff-red");

    let text = $field.text().trim();
    text = text.replace(/[^\d\.\-]/g, '');  // Keep digits, dot, minus
    const num = parseFloat(text);

    if (!isNaN(num)) {
        if (num > 0) {
            $field.addClass("highlight-diff-green");
            console.log("🟢 difference > 0 → green");
        } else if (num < 0) {
            $field.addClass("highlight-diff-red");
            console.log("🔴 difference < 0 → red");
        } else {
            console.log("⚪ difference = 0 → no color");
        }
    } else {
        console.log("❓ Not a number:", text);
    }
}












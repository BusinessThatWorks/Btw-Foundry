// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Heat Loss", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Daily Heat Loss', {
    target_liquid_metal(frm) {
        console.log('Target Liquid Metal changed:', frm.doc.target_liquid_metal);
        calculate_values(frm);
    },

    achieved_liquid_metal(frm) {
        console.log('Achieved Liquid Metal changed:', frm.doc.achieved_liquid_metal);
        calculate_values(frm);
    }
});

function calculate_values(frm) {
    let target = frm.doc.target_liquid_metal;
    let achieved = frm.doc.achieved_liquid_metal;

    console.log('Calculating values...');
    console.log('Target:', target);
    console.log('Achieved:', achieved);

    if (target && achieved && target != 0) {
        let loss_liquid_metal = 0;
        let achieved_percent = 0;
        let loss_percent = 0;

        if (achieved <= target) {
            loss_liquid_metal = target - achieved;
            achieved_percent = (achieved / target) * 100;
            loss_percent = 100 - achieved_percent;
        } else {
            // Achieved is greater than target: no loss
            loss_liquid_metal = 0;
            loss_percent = 0;
            achieved_percent = (achieved / target) * 100; // optionally reflect actual performance
        }

        frm.set_value('loss_liquid_metal', loss_liquid_metal);
        frm.set_value('achieved', achieved_percent.toFixed(2));
        frm.set_value('loss', loss_percent.toFixed(2));

        console.log('Set loss_liquid_metal:', loss_liquid_metal);
        console.log('Set achieved (%):', achieved_percent.toFixed(2));
        console.log('Set loss (%):', loss_percent.toFixed(2));
    } else {
        console.log('Insufficient data to calculate (maybe target is zero or missing values).');
    }
}


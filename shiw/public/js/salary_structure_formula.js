// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Salary Structure Formula Calculator
// This file extends the existing Salary Structure doctype with formula calculation capabilities

frappe.ui.form.on('Salary Structure', {
    refresh: function (frm) {
        console.log('🔧 Salary Structure form refreshed - adding custom buttons');

        // Add custom button to calculate all deductions
        frm.add_custom_button(__('Calculate Deductions'), function () {
            console.log('🔢 Calculate Deductions button clicked');
            calculate_all_deductions(frm);
        }, __('Actions'));

        // Add help button for formula syntax
        frm.add_custom_button(__('Formula Help'), function () {
            console.log('❓ Formula Help button clicked');
            show_formula_help();
        }, __('Help'));

        // Add button to enter formula
        frm.add_custom_button(__('Enter Formula'), function () {
            console.log('📝 Enter Formula button clicked');
            show_formula_input_dialog(frm);
        }, __('Actions'));

        // Add test API button
        frm.add_custom_button(__('Test API'), function () {
            console.log('🧪 Test API button clicked');
            test_api_connection();
        }, __('Actions'));

        console.log('✅ Custom buttons added to Salary Structure form');
    },

    earnings: function (frm, cdt, cdn) {
        // Recalculate deductions when earnings change
        calculate_all_deductions(frm);
    }
});

frappe.ui.form.on('Salary Detail', {
    custom_amount_formula: function (frm, cdt, cdn) {
        console.log('📊 custom_amount_formula field changed');
        // Validate and calculate formula when it changes
        const row = locals[cdt][cdn];
        console.log('📊 Row data:', row);
        console.log('📊 custom_amount_formula value:', row.custom_amount_formula, 'Type:', typeof row.custom_amount_formula);

        if (row.custom_amount_formula && typeof row.custom_amount_formula === 'string') {
            // Only calculate if it looks like a formula (contains letters or operators)
            if (row.custom_amount_formula.match(/[a-zA-Z+\-*/()]/)) {
                console.log('🔍 Formula detected, calculating...');
                validate_and_calculate_formula(frm, cdt, cdn);
            } else {
                console.log('🔍 Not a formula, skipping calculation');
            }
        } else {
            console.log('🔍 No formula or not a string, skipping calculation');
        }
    },

    // Also respond when the standard 'formula' field changes
    formula: function (frm, cdt, cdn) {
        console.log('🧾 standard formula field changed');
        const row = locals[cdt][cdn];
        console.log('🧾 Row data:', row);
        if (row.formula && typeof row.formula === 'string') {
            if (row.formula.match(/[a-zA-Z+\-*/()]/)) {
                console.log('🧾 Detected formula in standard field → compute custom_amount_formula');
                validate_and_calculate_formula_from_standard_field(frm, cdt, cdn);
            }
        }
    },

    component: function (frm, cdt, cdn) {
        // Auto-generate abbreviation from component name
        const row = locals[cdt][cdn];
        if (row.component && !row.abbreviation) {
            const abbreviation = generate_abbreviation(row.component);
            frappe.model.set_value(cdt, cdn, 'abbreviation', abbreviation);
        }
    }
});

function calculate_all_deductions(frm) {
    // Show loading indicator
    frm.dashboard.add_comment(__('Calculating deductions...'), 'blue', true);

    // Get earnings context
    const earnings_context = get_earnings_context(frm);

    // Calculate each deduction
    let calculation_promises = [];

    frm.doc.deductions.forEach((deduction, index) => {
        // Prefer standard 'formula' if present; fallback to custom field holding an expression
        if (deduction.formula || (typeof deduction.custom_amount_formula === 'string' && deduction.custom_amount_formula.match(/[a-zA-Z+\-*/()]/))) {
            const promise = calculate_deduction_amount(frm, 'deductions', deduction.name, earnings_context, deduction.formula);
            calculation_promises.push(promise);
        }
    });

    // Wait for all calculations to complete
    Promise.all(calculation_promises).then(() => {
        // Recalculate totals
        calculate_totals(frm);

        // Remove loading indicator
        frm.dashboard.clear_comment();
        frm.dashboard.add_comment(__('Deductions calculated successfully'), 'green', true);

        // Refresh the form
        frm.refresh_fields();
    }).catch((error) => {
        frm.dashboard.clear_comment();
        frm.dashboard.add_comment(__('Error calculating deductions'), 'red', true);
        console.error('Error calculating deductions:', error);
    });
}

function validate_and_calculate_formula(frm, cdt, cdn) {
    console.log('🧮 validate_and_calculate_formula called');
    const row = locals[cdt][cdn];
    console.log('🧮 Row:', row);

    if (!row.custom_amount_formula) {
        console.log('🧮 No formula found, returning');
        return;
    }

    // Get earnings context
    const earnings_context = get_earnings_context(frm);
    console.log('🧮 Earnings context:', earnings_context);

    console.log('🧮 Making API call to calculate formula:', row.custom_amount_formula);

    // Calculate formula and show result in the same field
    frappe.call({
        method: 'shiw.api.salary_formula_calculator.calculate_formula_amount',
        args: {
            formula: row.custom_amount_formula,
            earnings_data: earnings_context
        },
        callback: function (r) {
            console.log('🧮 API Response:', r);
            console.log('🧮 API Response message:', r.message);
            console.log('🧮 API Response success:', r.message ? r.message.success : 'undefined');

            if (r && r.message && r.message.success) {
                // Show calculated result in the same field (since it's a Currency field)
                const calculated_amount = r.message.amount;
                console.log('🧮 Calculated amount:', calculated_amount);

                // Update the field to show the calculated amount
                frappe.model.set_value(cdt, cdn, 'custom_amount_formula', calculated_amount);

                // Also update the amount field if it exists
                frappe.model.set_value(cdt, cdn, 'amount', calculated_amount);

                console.log('🧮 Fields updated successfully');

                // Show a message with the formula and result
                frappe.msgprint({
                    title: __('Formula Calculated'),
                    message: `Formula: ${row.custom_amount_formula}<br>Result: ${calculated_amount}`,
                    indicator: 'green'
                });
            } else {
                console.log('🧮 API Error or no success:', r);
                console.log('🧮 Error details:', r.message);
                // Show error message
                frappe.msgprint({
                    title: __('Formula Error'),
                    message: r.message ? r.message.message : 'API call failed or returned no data',
                    indicator: 'red'
                });
            }
        },
        error: function (err) {
            console.log('🧮 API Call Error:', err);
            frappe.msgprint({
                title: __('API Error'),
                message: `API call failed: ${err.message || 'Unknown error'}`,
                indicator: 'red'
            });
        }
    });
}

// Same as above but reads from built-in 'formula' field and writes result to 'custom_amount_formula'
function validate_and_calculate_formula_from_standard_field(frm, cdt, cdn) {
    console.log('🧮 validate_and_calculate_formula_from_standard_field called');
    const row = locals[cdt][cdn];
    const formula = row.formula;
    if (!formula) {
        console.log('🧮 No formula in standard field');
        return;
    }
    const earnings_context = get_earnings_context(frm);
    console.log('🧮 Earnings context:', earnings_context);
    frappe.call({
        method: 'shiw.api.salary_formula_calculator.calculate_formula_amount',
        args: { formula, earnings_data: earnings_context },
        callback: function (r) {
            console.log('🧮 API Response (std formula):', r);
            if (r && r.message && r.message.success) {
                const calculated_amount = r.message.amount;
                // write into custom_amount_formula (Currency) and amount as well for visibility
                frappe.model.set_value(cdt, cdn, 'custom_amount_formula', calculated_amount);
                frappe.model.set_value(cdt, cdn, 'amount', calculated_amount);
                console.log('🧮 Updated custom_amount_formula =', calculated_amount);
            } else {
                frappe.msgprint({
                    title: __('Formula Error'),
                    message: r.message ? r.message.message : 'API call failed or returned no data',
                    indicator: 'red'
                });
            }
        },
        error: function (err) {
            console.log('🧮 API Call Error (std formula):', err);
        }
    });
}

function calculate_deduction_amount(frm, cdt, cdn, earnings_context) {
    const row = locals[cdt][cdn];

    if (!row.custom_amount_formula) {
        return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'shiw.api.salary_formula_calculator.calculate_formula_amount',
            args: {
                formula: row.custom_amount_formula,
                earnings_data: earnings_context
            },
            callback: function (r) {
                if (r.message && r.message.success) {
                    // Show calculated result in the same field (since it's a Currency field)
                    const calculated_amount = r.message.amount;

                    // Update the field to show the calculated amount
                    frappe.model.set_value(cdt, cdn, 'custom_amount_formula', calculated_amount);

                    // Also update the amount field if it exists
                    frappe.model.set_value(cdt, cdn, 'amount', calculated_amount);

                    resolve(calculated_amount);
                } else {
                    frappe.msgprint({
                        title: __('Calculation Error'),
                        message: r.message ? r.message.message : 'Error calculating amount',
                        indicator: 'red'
                    });
                    reject(new Error(r.message ? r.message.message : 'Error calculating amount'));
                }
            }
        });
    });
}

function get_earnings_context(frm) {
    console.log('💰 Getting earnings context');
    const context = {};

    if (frm.doc.earnings) {
        console.log('💰 Earnings found:', frm.doc.earnings);
        frm.doc.earnings.forEach(earning => {
            // ERPNext child row uses 'abbr' for abbreviation. Fall back to 'abbreviation' if present.
            const key = (earning.abbr || earning.abbreviation || '').toString().trim();
            const val = Number(earning.amount || 0);
            if (key) {
                context[key] = val;
                console.log('💰 Added to context:', key, '=', val);
            } else {
                console.log('💰 Skipped row without abbr:', earning);
            }
        });
    } else {
        console.log('💰 No earnings found');
    }

    console.log('💰 Final context:', context);
    return context;
}

function calculate_totals(frm) {
    let total_earnings = 0;
    let total_deductions = 0;

    // Calculate total earnings
    if (frm.doc.earnings) {
        frm.doc.earnings.forEach(earning => {
            if (earning.amount) {
                total_earnings += earning.amount;
            }
        });
    }

    // Calculate total deductions
    if (frm.doc.deductions) {
        frm.doc.deductions.forEach(deduction => {
            if (deduction.amount) {
                total_deductions += deduction.amount;
            }
        });
    }

    // Update totals
    frm.set_value('total_earnings', total_earnings);
    frm.set_value('total_deductions', total_deductions);
    frm.set_value('net_salary', total_earnings - total_deductions);
}

function generate_abbreviation(component_name) {
    // Generate abbreviation from component name
    // Examples: "Basic" -> "B", "House Rent Allowance" -> "HRA"
    const words = component_name.split(' ');

    if (words.length === 1) {
        // Single word - take first few characters
        return words[0].substring(0, 3).toUpperCase();
    } else {
        // Multiple words - take first letter of each word
        return words.map(word => word.charAt(0).toUpperCase()).join('');
    }
}

function show_formula_input_dialog(frm) {
    // Get current deductions
    const deductions = frm.doc.deductions || [];

    if (deductions.length === 0) {
        frappe.msgprint(__('Please add some deductions first'));
        return;
    }

    // Create options for deductions
    const deduction_options = deductions.map((d, index) => ({
        label: `${d.component || 'Deduction ' + (index + 1)}`,
        value: index
    }));

    const d = new frappe.ui.Dialog({
        title: __('Enter Formula for Deduction'),
        fields: [
            {
                label: __('Select Deduction'),
                fieldname: 'deduction_index',
                fieldtype: 'Select',
                options: deduction_options,
                reqd: 1
            },
            {
                label: __('Formula'),
                fieldname: 'formula',
                fieldtype: 'Small Text',
                reqd: 1,
                description: 'Enter Python expression using earnings abbreviations (e.g., B, HRA)'
            }
        ],
        primary_action_label: __('Calculate'),
        primary_action: function (values) {
            const deduction = deductions[values.deduction_index];
            if (deduction) {
                // Set the formula in the custom_amount_formula field
                frappe.model.set_value('Salary Detail', deduction.name, 'custom_amount_formula', values.formula);

                // Calculate the formula
                const earnings_context = get_earnings_context(frm);
                frappe.call({
                    method: 'shiw.api.salary_formula_calculator.calculate_formula_amount',
                    args: {
                        formula: values.formula,
                        earnings_data: earnings_context
                    },
                    callback: function (r) {
                        if (r.message && r.message.success) {
                            const calculated_amount = r.message.amount;
                            frappe.model.set_value('Salary Detail', deduction.name, 'custom_amount_formula', calculated_amount);
                            frappe.model.set_value('Salary Detail', deduction.name, 'amount', calculated_amount);

                            frappe.msgprint({
                                title: __('Formula Calculated'),
                                message: `Formula: ${values.formula}<br>Result: ${calculated_amount}`,
                                indicator: 'green'
                            });

                            d.hide();
                            frm.refresh_fields();
                        } else {
                            frappe.msgprint({
                                title: __('Formula Error'),
                                message: r.message ? r.message.message : 'Invalid formula',
                                indicator: 'red'
                            });
                        }
                    }
                });
            }
        }
    });

    d.show();
}

function test_api_connection() {
    console.log('🧪 Testing API connection...');

    frappe.call({
        method: 'shiw.api.salary_formula_calculator.test_api',
        args: {},
        callback: function (r) {
            console.log('🧪 Test API Response:', r);
            if (r && r.message && r.message.success) {
                frappe.msgprint({
                    title: __('API Test'),
                    message: 'API is working correctly!',
                    indicator: 'green'
                });
            } else {
                frappe.msgprint({
                    title: __('API Test Failed'),
                    message: 'API is not responding correctly',
                    indicator: 'red'
                });
            }
        },
        error: function (err) {
            console.log('🧪 Test API Error:', err);
            frappe.msgprint({
                title: __('API Test Error'),
                message: `API test failed: ${err.message || 'Unknown error'}`,
                indicator: 'red'
            });
        }
    });
}

function show_formula_help() {
    const help_content = `
		<div style="max-width: 600px;">
			<h4>Formula Help</h4>
			<p>You can use Python expressions in the formula field. Here are some examples:</p>
			
			<h5>Basic Examples:</h5>
			<ul>
				<li><strong>Simple calculation:</strong> <code>B * 12/100</code> (12% of Basic)</li>
				<li><strong>Fixed amount:</strong> <code>1800</code></li>
				<li><strong>Using multiple earnings:</strong> <code>(B + HRA) * 0.1</code></li>
			</ul>
			
			<h5>Conditional Examples:</h5>
			<ul>
				<li><strong>Simple condition:</strong> <code>1800 if B > 15000 else B * 12/100</code></li>
				<li><strong>Multiple conditions:</strong> <code>0 if (B+HRA) <= 10000 else 110 if 10001 < (B+HRA) <= 15000 else 200</code></li>
				<li><strong>Range-based:</strong> <code>100 if B < 10000 else 200 if B < 20000 else 300</code></li>
			</ul>
			
			<h5>Available Variables:</h5>
			<p>Use the abbreviations from the Earnings table (e.g., B, HRA, DA, etc.)</p>
			
			<h5>Supported Functions:</h5>
			<p><code>abs, round, min, max, sum</code></p>
			
			<h5>Operators:</h5>
			<p><code>+, -, *, /, %, **, ==, !=, &lt;, &gt;, &lt;=, &gt;=, and, or, not</code></p>
			
			<h5>Tips:</h5>
			<ul>
				<li>Always use parentheses for complex expressions</li>
				<li>Test your formula with sample data first</li>
				<li>Use descriptive abbreviations for earnings components</li>
			</ul>
		</div>
	`;

    frappe.msgprint({
        title: __('Formula Help'),
        message: help_content,
        indicator: 'blue'
    });
}

// Add real-time formula validation
frappe.ui.form.on('Salary Detail', {
    custom_amount_formula: function (frm, cdt, cdn) {
        // Debounce the validation to avoid too many API calls
        clearTimeout(window.formula_validation_timeout);
        window.formula_validation_timeout = setTimeout(() => {
            validate_and_calculate_formula(frm, cdt, cdn);
        }, 1000); // Wait 1 second after user stops typing
    }
});

// Add formula syntax highlighting (basic)
frappe.ui.form.on('Salary Detail', {
    custom_amount_formula: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.custom_amount_formula) {
            // Add visual feedback for formula validation
            const field = frm.fields_dict.deductions.grid.grid_rows_by_docname[cdn].get_field('custom_amount_formula');
            if (field) {
                // Remove existing classes
                field.$input.removeClass('formula-valid formula-invalid');

                // Add loading class
                field.$input.addClass('formula-loading');

                // Validate formula
                frappe.call({
                    method: 'shiw.api.salary_formula_calculator.validate_formula',
                    args: {
                        formula: row.custom_amount_formula,
                        earnings_data: get_earnings_context(frm)
                    },
                    callback: function (r) {
                        field.$input.removeClass('formula-loading');
                        if (r.message && r.message.success) {
                            field.$input.addClass('formula-valid');
                        } else {
                            field.$input.addClass('formula-invalid');
                        }
                    }
                });
            }
        }
    }
});

// Add CSS for formula validation feedback
$(document).ready(function () {
    $('<style>')
        .prop('type', 'text/css')
        .html(`
			.formula-valid {
				border-color: #28a745 !important;
				background-color: #d4edda !important;
			}
			.formula-invalid {
				border-color: #dc3545 !important;
				background-color: #f8d7da !important;
			}
			.formula-loading {
				border-color: #ffc107 !important;
				background-color: #fff3cd !important;
			}
		`)
        .appendTo('head');
});

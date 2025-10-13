// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Pouring", {
// 	refresh(frm) {

// 	},
// });





// Utility function for float conversion
function flt(value) {
    return parseFloat(value) || 0;
}

frappe.ui.form.on('Pouring', {
    onload: function (frm) {
        console.log("Pouring form onload triggered");
        setTimeout(() => {
            console.log("Inside setTimeout for grid wrapper setup");
            const grid = frm.fields_dict["mould_batch"]?.grid;
            if (!grid || !grid.wrapper) {
                console.log("Grid or grid wrapper not found, exiting onload focusin setup");
                return;
            }
            console.log("Grid wrapper found, setting up focusin event");

            grid.wrapper.on("focusin", function (e) {
                console.log("Focusin event triggered on grid wrapper");
                const $target = $(e.target);
                console.log("Target element data-fieldname:", $target.attr("data-fieldname"));
                const grid_row_el = $target.closest(".grid-row");
                const grid_row = $(grid_row_el).data("grid_row");

                if (!grid_row || !grid_row.doc) {
                    console.log("Grid row or doc not found, exiting focusin handler");
                    return;
                }
                console.log("Grid row found, docname:", grid_row.doc.name);

                // Handle mould_no focus
                if ($target.attr("data-fieldname") === "mould_no") {
                    console.log("Focus on mould_no field");
                    const doctype_name = grid_row.get_field("moulding_system")?.value;
                    console.log("Doctype name (moulding_system):", doctype_name);
                    if (!doctype_name) {
                        console.log("No doctype_name, exiting mould_no focus handler");
                        return;
                    }

                    console.log("Making frappe.call to get mould list for doctype:", doctype_name);
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: doctype_name,
                            fields: ["name"],
                            limit_page_length: 1000
                        },
                        callback: function (r) {
                            console.log("frappe.call get_list response received for mould_no");
                            if (r.message) {
                                const mould_names = r.message.map(d => d.name);
                                console.log("Mould names fetched:", mould_names);
                                const mould_field = grid_row.get_field("mould_no");
                                if (mould_field) {
                                    mould_field.df.options = mould_names.join("\n");
                                    mould_field.refresh();
                                    console.log("Updated mould_no field options and refreshed");
                                }

                                frappe.model.set_value(grid_row.doc.doctype, grid_row.doc.name, "mould_no", "");
                                console.log("Set mould_no to empty string");
                                frappe.modelk.set_value(grid_row.doc.doctype, grid_row.doc.name, "tooling_id", "");
                                console.log("Set tooling_id to empty string");
                            } else {
                                console.log("No mould names returned in response");
                            }
                        }
                    });
                }

                // Handle tooling_id focus
                if ($target.attr("data-fieldname") === "tooling_id") {
                    console.log("Focus on tooling_id field");
                    const moulding_system = grid_row.get_field("moulding_system")?.value;
                    const mould_no = grid_row.get_field("mould_no")?.value;
                    console.log("Moulding system:", moulding_system, "Mould no:", mould_no);
                    if (!moulding_system || !mould_no) {
                        console.log("Moulding system or mould_no missing, exiting tooling_id focus handler");
                        return;
                    }

                    console.log("Making frappe.call to get mould details for:", moulding_system, mould_no);
                    frappe.call({
                        method: "frappe.client.get",
                        args: {
                            doctype: moulding_system,
                            name: mould_no
                        },
                        callback: function (r) {
                            console.log("frappe.call get response received for toolin_id");
                            if (r.message) {
                                let tooling_options = (r.message.mould_table || [])
                                    .map(item => item.tooling)
                                    .filter(Boolean);
                                console.log("Tooling options fetched:", tooling_options);

                                const field = grid_row.get_field('tooling_id');
                                if (field) {
                                    field.df.options = tooling_options.join('\n');
                                    field.refresh();
                                    console.log("Updated tooling_id field options and refreshed");
                                    frappe.model.set_value(grid_row.doc.doctype, grid_row.doc.name, 'tooling_id', '');
                                    console.log("Set tooling_id to empty string");
                                } else {
                                    console.log("tooling_id field not found");
                                }
                            } else {
                                console.log("No mould details returned in response");
                            }
                        }
                    });
                }
            });
        }, 300);
        console.log("setTimeout scheduled for 300ms");
    },

    refresh: function (frm) {
        console.log('Form refreshed, calculating total consumption valuation');
        calculate_total_consumption(frm);
    },

    mould_batch: function (frm) {
        console.log("mould_batch event triggered, updating total_pouring_weight");
        update_total_cast_weight(frm);
        console.log("Finished updating total_pouring_weight");
    }
});

frappe.ui.form.on('Mould Batch', {
    mould_batch_add: function (frm, cdt, cdn) {
        console.log("New Mould Batch row added, cdt:", cdt, "cdn:", cdn);
        frappe.model.set_value(cdt, cdn, 'mould_no', '');
        console.log("Set mould_no to empty string for new row");
        frappe.model.set_value(cdt, cdn, 'tooling_id', '');
        console.log("Set tooling_id to empty string for new row");
        frappe.model.set_value(cdt, cdn, 'quantity_available', '');
        console.log("Set quantity_available to empty string for new row");
        update_total_cast_weight(frm);
        console.log("Updated total_pouring_weight after adding new row");
    },

    moulding_system: function (frm, cdt, cdn) {
        console.log("moulding_system changed for row, cdt:", cdt, "cdn:", cdn);
        let row = locals[cdt][cdn];
        console.log("Current row data:", row);
        if (!row.moulding_system) {
            console.log("No moulding_system selected, resetting fields");
            frappe.model.set_value(cdt, cdn, 'mould_no', '');
            console.log("Set mould_no to empty string");
            frappe.model.set_value(cdt, cdn, 'tooling_id', '');
            console.log("Set tooling_id to empty string");
            frappe.model.set_value(cdt, cdn, 'quantity_available', '');
            console.log("Set quantity_available to empty string");
            update_total_cast_weight(frm);
            console.log("Updated total_pouring_weight after resetting fields");
            return;
        }

        console.log("Making frappe.call to get mould list for moulding_system:", row.moulding_system);
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: row.moulding_system,
                fields: ["name"],
                limit: 1000
            },
            callback: function (r) {
                console.log("frappe.call get_list response received for moulding_system");
                if (r.message) {
                    let mould_names = r.message.map(d => d.name);
                    console.log("Mould names fetched:", mould_names);
                    frm.fields_dict['mould_batch'].grid.update_docfield_property(
                        'mould_no',
                        'options',
                        mould_names.join('\n')
                    );
                    console.log("Updated mould_no field options in grid");

                    frappe.model.set_value(cdt, cdn, 'mould_no', '');
                    console.log("Set mould_no to empty string");
                    frappe.model.set_value(cdt, cdn, 'tooling_id', '');
                    console.log("Set tooling_id to empty string");
                    frappe.model.set_value(cdt, cdn, 'quantity_available', '');
                    console.log("Set quantity_available to empty string");
                    update_total_cast_weight(frm);
                    console.log("Updated total_pouring_weight after moulding_system change");
                } else {
                    console.log("No mould names returned in response");
                }
            }
        });
    },

    mould_no: function (frm, cdt, cdn) {
        console.log("mould_no changed for row, cdt:", cdt, "cdn:", cdn);
        let row = locals[cdt][cdn];
        console.log("Current row data:", row);
        let doctype_name = row.moulding_system;
        let mould_doc_name = row.mould_no;
        console.log("Doctype name:", doctype_name, "Mould doc name:", mould_doc_name);
        if (!doctype_name || !mould_doc_name) {
            console.log("Missing doctype_name or mould_doc_name, exiting mould_no handler");
            return;
        }

        console.log("Making frappe.call to get mould details for:", doctype_name, mould_doc_name);
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: doctype_name,
                name: mould_doc_name
            },
            callback: function (r) {
                console.log("frappe.call get response received for mould_no");
                if (r.message) {
                    let tooling_options = (r.message.mould_table || [])
                        .map(item => item.tooling)
                        .filter(Boolean);
                    console.log("Tooling options fetched:", tooling_options);

                    let grid_row = frm.fields_dict['mould_batch'].grid.grid_rows_by_docname[cdn];
                    let tooling_field = grid_row?.get_field('tooling_id');
                    if (tooling_field) {
                        tooling_field.df.options = tooling_options.join('\n');
                        tooling_field.refresh();
                        console.log("Updated tooling_id field options and refreshed");
                    } else {
                        console.log("tooling_id field not found");
                    }

                    frappe.model.set_value(cdt, cdn, 'tooling_id', '');
                    console.log("Set tooling_id to empty string");
                    frappe.model.set_value(cdt, cdn, 'quantity_available', '');
                    console.log("Set quantity_available to empty string");
                    update_total_cast_weight(frm);
                    console.log("Updated total_pouring_weight after mould_no change");
                } else {
                    console.log("No mould details returned in response");
                }
            }
        });
    },

    tooling_id: function (frm, cdt, cdn) {
        console.log("tooling_id changed for row, cdt:", cdt, "cdn:", cdn);
        let row = locals[cdt][cdn];
        console.log("Current row data:", row);
        let doctype_name = row.moulding_system;
        let mould_doc_name = row.mould_no;
        let selected_tooling = row.tooling_id;
        console.log("Doctype name:", doctype_name, "Mould doc name:", mould_doc_name, "Selected tooling:", selected_tooling);

        if (!doctype_name || !mould_doc_name || !selected_tooling) {
            console.log("Missing doctype_name, mould_doc_name, or selected_tooling, resetting fields");
            frappe.model.set_value(cdt, cdn, 'cast_weight', 0);
            console.log("Set cast_weight to 0");
            frappe.model.set_value(cdt, cdn, 'total_cast_weight', 0);
            console.log("Set total_cast_weight to 0");
            update_total_cast_weight(frm);
            console.log("Updated total_pouring_weight after invalid tooling_id");
            return;
        }

        // Fetch total_casting_weight directly from the New Tooling doctype, avoiding child tables
        console.log("Making frappe.call to get tooling details for:", selected_tooling);
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "New Tooling",
                name: selected_tooling
            },
            callback: function (r) {
                console.log("frappe.call get response received for New Tooling. Full response:", JSON.stringify(r.message, null, 2));
                if (r.message) {
                    let cast_weight = r.message.total_casting_weight || 0;
                    console.log("Fetched cast_weight (total_casting_weight) from New Tooling doctype:", cast_weight);
                    frappe.model.set_value(cdt, cdn, 'cast_weight', cast_weight);
                    console.log("Set cast_weight to:", cast_weight);

                    let pouring_quantity = row.pouring_quantity || 0;
                    console.log("Current pouring_quantity:", pouring_quantity);
                    let total_cast_weight = pouring_quantity * cast_weight;
                    frappe.model.set_value(cdt, cdn, 'total_cast_weight', total_cast_weight);
                    console.log("Set total_cast_weight to:", total_cast_weight);
                } else {
                    console.log("No data found in New Tooling document, resetting fields");
                    frappe.model.set_value(cdt, cdn, 'cast_weight', 0);
                    console.log("Set cast_weight to 0");
                    frappe.model.set_value(cdt, cdn, 'total_cast_weight', 0);
                    console.log("Set total_cast_weight to 0");
                }
                update_total_cast_weight(frm);
                console.log("Updated total_pouring_weight after tooling_id change");
            }
        });

        // Fetch quantity_available from mould_table (optional, if still needed)
        console.log("Making frappe.call to get mould details for:", doctype_name, mould_doc_name);
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: doctype_name,
                name: mould_doc_name
            },
            callback: function (r) {
                console.log("frappe.call get response received for mould_no to check quantity");
                if (r.message) {
                    let matched_row = (r.message.mould_table || [])
                        .find(item => item.tooling === selected_tooling);
                    console.log("Matched row in mould_table:", matched_row);
                    if (matched_row && matched_row.mould_quantity) {
                        let qty = matched_row.mould_quantity || 0;
                        console.log("Fetched quantity_available:", qty);
                        frappe.model.set_value(cdt, cdn, 'quantity_available', qty);
                    } else {
                        console.log("No matching tooling or quantity found, setting quantity_available to 0");
                        frappe.model.set_value(cdt, cdn, 'quantity_available', 0);
                    }
                } else {
                    console.log("No mould details returned in response");
                }
            }
        });
    },

    pouring_quantity: function (frm, cdt, cdn) {
        console.log("pouring_quantity changed for row, cdt:", cdt, "cdn:", cdn);
        let row = locals[cdt][cdn];
        console.log("Current row data:", row);
        let pouring_quantity = row.pouring_quantity || 0;
        let cast_weight = row.cast_weight || 0;
        console.log("Pouring quantity:", pouring_quantity, "Cast weight:", cast_weight);

        // Calculate and set total_cast_weight for the row
        let total_cast_weight = pouring_quantity * cast_weight;
        frappe.model.set_value(cdt, cdn, 'total_cast_weight', total_cast_weight);
        console.log("Set total_cast_weight to:", total_cast_weight);
        update_total_cast_weight(frm);
        console.log("Updated total_pouring_weight after pouring_quantity change");
    }
});

frappe.ui.form.on('Consumption-Mould', {
    weight_in_kg: function (frm, cdt, cdn) {
        console.log(`Weight changed for row ${cdn}: ${locals[cdt][cdn].weight_in_kg} `);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },
    rate: function (frm, cdt, cdn) {
        console.log(`Rate changed for row ${cdn}: ${locals[cdt][cdn].rate} `);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },
    consumption_mould_remove: function (frm, cdt, cdn) {
        console.log(`Row ${cdn} removed from consumption_mould`);
        calculate_total_consumption(frm);
    }
});

// Function to calculate and update total_pouring_weight in the parent doctype
function update_total_cast_weight(frm) {
    console.log("Calculating total_pouring_weight");
    let total = 0;
    if (frm.doc.mould_batch) {
        frm.doc.mould_batch.forEach(row => {
            console.log("Row total_cast_weight:", row.total_cast_weight);
            total += flt(row.total_cast_weight || 0);
        });
        console.log("Sum of total_cast_weight:", total);
    } else {
        console.log("No mould_batch rows found");
    }
    frm.set_value('total_pouring_weight', total);
    console.log("Set total_pouring_weight to:", total);
}

// Function to calculate amount for a single row
function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.weight_in_kg && row.rate) {
        row.amount = flt(row.weight_in_kg) * flt(row.rate);
        console.log(`Calculated amount for row ${cdn}: ${row.amount} (weight: ${row.weight_in_kg}, rate: ${row.rate})`);
    } else {
        row.amount = 0;
        console.log(`Amount set to 0 for row ${cdn}(weight: ${row.weight_in_kg}, rate: ${row.rate})`);
    }
    frm.refresh_field('consumption_mould');
}

// Function to calculate total_consumption_valuation
function calculate_total_consumption(frm) {
    let total = 0;
    if (frm.doc.consumption_mould && Array.isArray(frm.doc.consumption_mould)) {
        frm.doc.consumption_mould.forEach(function (row) {
            total += flt(row.amount);
            console.log(`Adding amount for row ${row.name}: ${row.amount}, Running total: ${total} `);
        });
    } else {
        console.log('Child table consumption_mould is undefined or empty');
    }
    frm.set_value('total_consumption_valuation', total);
    console.log(`Total consumption valuation set to: ${total} `);
}

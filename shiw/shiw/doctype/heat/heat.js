// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.ui.form.on("Heat", {
    refresh(frm) {
        console.log("🔥 Heat form refresh event triggered");
        // Initialize mandatory field state based on downtime status
        update_mandatory_fields(frm);

        // Calculate totals and consumption valuation
        console.log('🔥 Heat form refresh event triggered, calculating totals and consumption valuation');
        calculate_totals(frm);
        calculate_total_consumption(frm);
    },
    onload: function(frm) {
        console.log('Form loaded, calculating totals');
        calculate_totals(frm);
    },
    before_save: function(frm) {
        console.log('Before save, checking furnace_holding_time');
        if (!frm.doc.furnace_holding_time) {
            frm.set_value('furnace_holding_time', '00:00:00');
        }
    },
    heat_start_at: function(frm) {
        console.log('Heat start time changed, calculating melting time');
        calculate_melting_time(frm);
    },
    heat_end_at: function(frm) {
        console.log('Heat end time changed, calculating melting time');
        calculate_melting_time(frm);
    },
    
    custom_is_downtime(frm) {
        console.log("🔥 custom_is_downtime changed to:", frm.doc.custom_is_downtime);
        
        // When downtime checkbox changes, update mandatory fields
        update_mandatory_fields(frm);
        
        // If downtime is checked, clear the child tables to avoid validation errors
        if (frm.doc.custom_is_downtime) {
            console.log("🔥 Downtime checked - clearing child tables");
            
            // Clear charge_mix_component_item table
            if (frm.doc.charge_mix_component_item && frm.doc.charge_mix_component_item.length > 0) {
                frm.clear_table('charge_mix_component_item');
                frm.refresh_field('charge_mix_component_item');
                console.log("🔥 Cleared charge_mix_component_item table");
            }
            
            // Clear table_vkjb table
            if (frm.doc.table_vkjb && frm.doc.table_vkjb.length > 0) {
                frm.clear_table('table_vkjb');
                frm.refresh_field('table_vkjb');
                console.log("🔥 Cleared table_vkjb table");
            }
        }
    },
    
    // Handle child table events to ensure mandatory field changes are applied
    charge_mix_component_item(frm, cdt, cdn) {
        console.log("🔥 charge_mix_component_item event triggered");
        // Refresh mandatory field state when child table changes
        setTimeout(() => {
            update_mandatory_fields(frm);
        }, 100);

        // Also recalculate totals when rows change
        calculate_totals(frm);
    },
    
    table_vkjb(frm, cdt, cdn) {
        console.log("🔥 table_vkjb event triggered");
        // Refresh mandatory field state when child table changes
        setTimeout(() => {
            update_mandatory_fields(frm);
        }, 100);

        // Also recalculate consumption valuation
        calculate_total_consumption(frm);
    },

    charge_mix_component_item_add: function(frm) {
        console.log('Charge mix component item added, calculating totals');
        calculate_totals(frm);
    },
    charge_mix_component_item_remove: function(frm) {
        console.log('Charge mix component item removed, calculating totals');
        calculate_totals(frm);
    }
});

function update_mandatory_fields(frm) {
    console.log("🔥 update_mandatory_fields function called");
    
    // List of all mandatory fields that should become non-mandatory during downtime
    const mandatory_fields = [
        'melter',
        'date', 
        'pouring_person',
        'furnace_no',
        'material_grade',
        'ladle_no',
        'lining_heat_no',
        'charge_mix_component_item',
        'foundry_return_existing',
        'liquid_metal_pig',
        'furnace_holding_time',
        'table_vkjb',
        'shift_type'
    ];
    
    // Child table mandatory fields configuration
    const child_table_mandatory_fields = {
        'charge_mix_component_item': ['item', 'weight', 'amount'],
        'table_vkjb': ['item', 'uom', 'quantity']
    };
    
    // If downtime is checked, make all mandatory fields non-mandatory
    // If downtime is unchecked, restore original mandatory status
    const is_downtime = frm.doc.custom_is_downtime;
    
    console.log('🔥 Downtime mode:', is_downtime);
    console.log('🔥 Downtime type:', typeof is_downtime);
    console.log('🔥 Will set fields to reqd:', !is_downtime);
    
    // Handle main form mandatory fields
    console.log('🔥 Processing main form fields...');
    mandatory_fields.forEach(fieldname => {
        const field = frm.get_field(fieldname);
        if (field) {
            console.log(`🔥 Setting main field ${fieldname} to reqd:`, !is_downtime);
            frm.set_df_property(fieldname, 'reqd', !is_downtime);
        } else {
            console.log(`🔥 Main field ${fieldname} not found!`);
        }
    });
    
    // Handle child table mandatory fields
    console.log('🔥 Processing child table fields...');
    Object.keys(child_table_mandatory_fields).forEach(table_fieldname => {
        const table_field = frm.get_field(table_fieldname);
        if (table_field) {
            const mandatory_table_fields = child_table_mandatory_fields[table_fieldname];
            
            console.log(`🔥 Found child table ${table_fieldname} with fields:`, mandatory_table_fields);
            console.log(`🔥 Table field object:`, table_field);
            console.log(`🔥 Table field df:`, table_field.df);
            
            // CRITICAL: Set the table field itself to non-mandatory when downtime is checked
            console.log(`🔥 Setting table field ${table_fieldname} to reqd:`, !is_downtime);
            frm.set_df_property(table_fieldname, 'reqd', !is_downtime);
            
            // Update each mandatory field in the child table
            mandatory_table_fields.forEach(child_fieldname => {
                // Get the child table's meta data
                const child_doctype = table_field.df.options;
                
                console.log(`🔥 Setting child field ${child_fieldname} in ${child_doctype} to reqd:`, !is_downtime);

                // Update the child table field property on the grid column definition
                if (table_field.grid) {
                    const grid_col = table_field.grid.get_field(child_fieldname);
                    if (grid_col && grid_col.df) {
                        console.log(`🔥 Updating grid column df for ${child_fieldname}:`, !is_downtime);
                        grid_col.df.reqd = !is_downtime;
                    } else if (table_field.grid.meta && table_field.grid.meta.fields) {
                        // Fallback: mutate grid meta
                        const metaField = table_field.grid.meta.fields.find(f => f.fieldname === child_fieldname);
                        if (metaField) {
                            console.log(`🔥 Fallback update of grid meta for ${child_fieldname}:`, !is_downtime);
                            metaField.reqd = !is_downtime;
                        } else {
                            console.log(`🔥 Child field ${child_fieldname} not found on grid`);
                        }
                    } else {
                        console.log(`🔥 Grid meta not available for ${table_fieldname}`);
                    }
                }
            });
            
            // Refresh the child table
            if (table_field.grid) {
                console.log(`🔥 Refreshing grid for ${table_fieldname}`);
                table_field.grid.refresh();
            } else {
                console.log(`🔥 No grid found for ${table_fieldname}`);
            }
        } else {
            console.log(`🔥 Child table field ${table_fieldname} not found!`);
        }
    });
    
    // Refresh the form to update the UI
    console.log('🔥 Refreshing form fields...');
    frm.refresh_fields();
    
    // Force refresh of child tables to apply field property changes
    Object.keys(child_table_mandatory_fields).forEach(table_fieldname => {
        const table_field = frm.get_field(table_fieldname);
        if (table_field && table_field.grid) {
            console.log(`🔥 Force refreshing grid for ${table_fieldname}`);
            table_field.grid.refresh();
        }
    });
    
    console.log('🔥 update_mandatory_fields function completed');
}

// ---------------- Additional Calculations & Child Doctype Handlers ----------------

frappe.ui.form.on('Charge mix component table', {
    weight: function(frm, cdt, cdn) {
        console.log(`Weight changed for row ${cdn}: ${locals[cdt][cdn].weight}`);
        update_row_amount(cdt, cdn);
        calculate_totals(frm);
    },
    item_rate: function(frm, cdt, cdn) {
        console.log(`Item rate changed for row ${cdn}: ${locals[cdt][cdn].item_rate}`);
        update_row_amount(cdt, cdn);
        calculate_totals(frm);
    }
});

frappe.ui.form.on('Heat-Ladle Consumption Table', {
    quantity: function(frm, cdt, cdn) {
        console.log(`Quantity changed for row ${cdn}: ${locals[cdt][cdn].quantity}`);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },
    rate: function(frm, cdt, cdn) {
        console.log(`Rate changed for row ${cdn}: ${locals[cdt][cdn].rate}`);
        calculate_row_amount(frm, cdt, cdn);
        calculate_total_consumption(frm);
    },
    table_vkjb_remove: function(frm, cdt, cdn) {
        console.log(`Row ${cdn} removed from table_vkjb`);
        calculate_total_consumption(frm);
    }
});

function round2(val) {
    return Math.round((val + Number.EPSILON) * 100) / 100;
}

function update_row_amount(cdt, cdn) {
    const row   = locals[cdt][cdn];
    const wt    = parseFloat(row.weight) || 0;
    const rate  = parseFloat(row.item_rate) || 0;
    const value = round2(wt * rate);

    frappe.model.set_value(cdt, cdn, 'amount', value);
    frappe.model.set_value(cdt, cdn, 'weight', round2(wt));
    frappe.model.set_value(cdt, cdn, 'item_rate', round2(rate));
}

function calculate_totals(frm) {
    let total_weight    = 0;
    let total_valuation = 0;

    (frm.doc.charge_mix_component_item || []).forEach(row => {
        const wt   = parseFloat(row.weight) || 0;
        const rate = parseFloat(row.item_rate) || 0;

        total_weight    += wt;
        total_valuation += wt * rate;
    });

    frm.set_value({
        total_charge_mix_in_kg    : round2(total_weight),
        total_charge_mix_valuation: round2(total_valuation)
    });

    frm.refresh_field(['total_charge_mix_in_kg', 'total_charge_mix_valuation']);
}

function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.quantity && row.rate) {
        row.amount = flt(row.quantity) * flt(row.rate);
        console.log(`Calculated amount for row ${cdn}: ${row.amount} (quantity: ${row.quantity}, rate: ${row.rate})`);
    } else {
        row.amount = 0;
        console.log(`Amount set to 0 for row ${cdn} (quantity: ${row.quantity}, rate: ${row.rate})`);
    }
    frm.refresh_field('table_vkjb');
}

function calculate_total_consumption(frm) {
    let total = 0;
    if (frm.doc.table_vkjb && Array.isArray(frm.doc.table_vkjb)) {
        frm.doc.table_vkjb.forEach(function(row) {
            total += flt(row.amount);
            console.log(`Adding amount for row ${row.name}: ${row.amount}, Running total: ${total}`);
        });
    } else {
        console.log('Child table table_vkjb is undefined or empty');
    }
    frm.set_value('total_ladle_consumption_valuation', total);
    console.log(`Total consumption valuation set to: ${total}`);
}

function calculate_melting_time(frm) {
    if (frm.doc.heat_start_at && frm.doc.heat_end_at) {
        let start_time = moment(frm.doc.heat_start_at, "HH:mm:ss");
        let end_time = moment(frm.doc.heat_end_at, "HH:mm:ss");

        if (end_time.isBefore(start_time)) {
            end_time.add(1, 'days');
        }

        let duration = moment.duration(end_time.diff(start_time));
        let hours = Math.floor(duration.asHours());
        let minutes = duration.minutes();
        let seconds = duration.seconds();

        let formatted_duration = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        frm.set_value('melting_time', formatted_duration);
    }
}

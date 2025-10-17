// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

frappe.ui.form.on("Heat", {
    refresh(frm) {
        console.log("🔥 Heat form refresh event triggered");
        // Initialize mandatory field state based on downtime status
        update_mandatory_fields(frm);
    },
    
    custom_is_downtime(frm) {
        console.log("🔥 custom_is_downtime changed to:", frm.doc.custom_is_downtime);
        // When downtime checkbox changes, update mandatory fields
        update_mandatory_fields(frm);
    },
    
    // Handle child table events to ensure mandatory field changes are applied
    charge_mix_component_item(frm, cdt, cdn) {
        console.log("🔥 charge_mix_component_item event triggered");
        // Refresh mandatory field state when child table changes
        setTimeout(() => {
            update_mandatory_fields(frm);
        }, 100);
    },
    
    table_vkjb(frm, cdt, cdn) {
        console.log("🔥 table_vkjb event triggered");
        // Refresh mandatory field state when child table changes
        setTimeout(() => {
            update_mandatory_fields(frm);
        }, 100);
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
                
                // Update the child table field property globally
                frappe.model.set_df_property(child_doctype, child_fieldname, 'reqd', !is_downtime);
                
                // Also update the field in the current form's child table meta
                if (table_field.grid && table_field.grid.meta && table_field.grid.meta.fields) {
                    const child_field = table_field.grid.meta.fields.find(f => f.fieldname === child_fieldname);
                    if (child_field) {
                        console.log(`🔥 Updating grid meta for ${child_fieldname}:`, !is_downtime);
                        child_field.reqd = !is_downtime;
                    } else {
                        console.log(`🔥 Child field ${child_fieldname} not found in grid meta!`);
                    }
                } else {
                    console.log(`🔥 Grid or grid meta not available for ${table_fieldname}`);
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
    console.log('🔥 update_mandatory_fields function completed');
}

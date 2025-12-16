// Daily Costing client script to pull Repair total_repair_weight
// based on date and shift_type

frappe.ui.form.on("Daily Costing", {
    date: function (frm) {
        console.log("[Daily Costing] Date changed:", frm.doc.date);
        fetch_repair_weight_for_daily_costing(frm);
        fetch_heat_values_for_daily_costing(frm);
        fetch_hpml_values_for_daily_costing(frm);
        fetch_js_values_for_daily_costing(frm);
        fetch_no_bake_values_for_daily_costing(frm);
        fetch_green_sand_values_for_daily_costing(frm);
        fetch_co2_values_for_daily_costing(frm);
        fetch_core_values_for_daily_costing(frm);
        fetch_shotblast_values_for_daily_costing(frm);
        fetch_fettling_values_for_daily_costing(frm);
        fetch_finishing_values_for_daily_costing(frm);
    },

    shift_type: function (frm) {
        console.log("[Daily Costing] Shift Type changed:", frm.doc.shift_type);
        fetch_repair_weight_for_daily_costing(frm);
        fetch_heat_values_for_daily_costing(frm);
        fetch_hpml_values_for_daily_costing(frm);
        fetch_js_values_for_daily_costing(frm);
        fetch_no_bake_values_for_daily_costing(frm);
        fetch_green_sand_values_for_daily_costing(frm);
        fetch_co2_values_for_daily_costing(frm);
        fetch_core_values_for_daily_costing(frm);
        fetch_shotblast_values_for_daily_costing(frm);
        fetch_fettling_values_for_daily_costing(frm);
        fetch_finishing_values_for_daily_costing(frm);
    },

    refresh: function (frm) {
        console.log("[Daily Costing] Form refreshed. Current values:", {
            date: frm.doc.date,
            shift_type: frm.doc.shift_type,
            repairing_weight: frm.doc.repairing_weight,
            liquid_metal: frm.doc.liquid_metal,
            liquid_metal_cost: frm.doc.liquid_metal_cost,
            ladle_cost: frm.doc.ladle_cost,
            liquid_metal_cost_per_kg: frm.doc.liquid_metal_cost_per_kg,
            ladle_cost_per_kg: frm.doc.ladle_cost_per_kg,
            hpml_weight: frm.doc.hpml_weight,
            hpml_cost: frm.doc.hpml_cost,
            hpml_cost_per_kg: frm.doc.hpml_cost_per_kg,
            js_weight: frm.doc.js_weight,
            js_cost: frm.doc.js_cost,
            js_cost_per_kg: frm.doc.js_cost_per_kg,
            no_bake_weight: frm.doc.no_bake_weight,
            no_bake_cost: frm.doc.no_bake_cost,
            no_bake_cost_per_kg: frm.doc.no_bake_cost_per_kg,
            green_sand_weight: frm.doc.green_sand_weight,
            green_sand_cost: frm.doc.green_sand_cost,
            green_sand_cost_per_kg: frm.doc.green_sand_cost_per_kg,
            co2_weight: frm.doc.co2_weight,
            co2_cost: frm.doc.co2_cost,
            co2_cost_per_kg: frm.doc.co2_cost_per_kg,
        });
    },
});

function fetch_repair_weight_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Repair] Fetch function called with:", {
        date,
        shift_type,
    });

    // Only proceed when both fields are set
    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Repair] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_repair_weight_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Repair] Server response for repair values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Repair] Error while fetching repair values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                // No matching Repair records found
                frm.set_value("repairing_weight", 0);
                frm.set_value("repairing_cost", 0);
                frm.set_value("repairing_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Repair] No Repair records found for given date and shift_type. Reset Repair fields to 0.",
                );
                return;
            }

            if (data.repairing_weight != null) {
                frm.set_value("repairing_weight", data.repairing_weight);
            }
            if (data.repairing_cost != null) {
                frm.set_value("repairing_cost", data.repairing_cost);
            }
            if (data.repairing_cost_per_kg != null) {
                frm.set_value("repairing_cost_per_kg", data.repairing_cost_per_kg);
            }

            console.log("[Daily Costing][Repair] Updated Repair fields:", {
                repairing_weight: data.repairing_weight,
                repairing_cost: data.repairing_cost,
                repairing_cost_per_kg: data.repairing_cost_per_kg,
            });
        },
    });
}

function fetch_hpml_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][HPML] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][HPML] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_hpml_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][HPML] Server response for HPML values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][HPML] Error while fetching HPML values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                // No matching HPML Mould Batch records
                frm.set_value("hpml_weight", 0);
                frm.set_value("hpml_cost", 0);
                frm.set_value("hpml_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][HPML] No HPML Mould Batch records found for given date and shift_type. Reset HPML fields to 0.",
                );
                return;
            }

            if (data.hpml_weight != null) {
                frm.set_value("hpml_weight", data.hpml_weight);
            }
            if (data.hpml_cost != null) {
                frm.set_value("hpml_cost", data.hpml_cost);
            }
            if (data.hpml_cost_per_kg != null) {
                frm.set_value("hpml_cost_per_kg", data.hpml_cost_per_kg);
            }

            console.log("[Daily Costing][HPML] Updated HPML fields:", {
                hpml_weight: data.hpml_weight,
                hpml_cost: data.hpml_cost,
                hpml_cost_per_kg: data.hpml_cost_per_kg,
            });
        },
    });
}

function fetch_js_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][JS] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][JS] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_js_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][JS] Server response for JS values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][JS] Error while fetching JS values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("js_weight", 0);
                frm.set_value("js_cost", 0);
                frm.set_value("js_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][JS] No Jolt Squeeze Mould Batch records found for given date and shift_type. Reset JS fields to 0.",
                );
                return;
            }

            if (data.js_weight != null) {
                frm.set_value("js_weight", data.js_weight);
            }
            if (data.js_cost != null) {
                frm.set_value("js_cost", data.js_cost);
            }
            if (data.js_cost_per_kg != null) {
                frm.set_value("js_cost_per_kg", data.js_cost_per_kg);
            }

            console.log("[Daily Costing][JS] Updated JS fields:", {
                js_weight: data.js_weight,
                js_cost: data.js_cost,
                js_cost_per_kg: data.js_cost_per_kg,
            });
        },
    });
}

function fetch_no_bake_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][No Bake] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][No Bake] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_no_bake_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][No Bake] Server response for No Bake values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][No Bake] Error while fetching No Bake values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("no_bake_weight", 0);
                frm.set_value("no_bake_cost", 0);
                frm.set_value("no_bake_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][No Bake] No No-Bake Mould Batch records found for given date and shift_type. Reset No Bake fields to 0.",
                );
                return;
            }

            if (data.no_bake_weight != null) {
                frm.set_value("no_bake_weight", data.no_bake_weight);
            }
            if (data.no_bake_cost != null) {
                frm.set_value("no_bake_cost", data.no_bake_cost);
            }
            if (data.no_bake_cost_per_kg != null) {
                frm.set_value("no_bake_cost_per_kg", data.no_bake_cost_per_kg);
            }

            console.log("[Daily Costing][No Bake] Updated No Bake fields:", {
                no_bake_weight: data.no_bake_weight,
                no_bake_cost: data.no_bake_cost,
                no_bake_cost_per_kg: data.no_bake_cost_per_kg,
            });
        },
    });
}

function fetch_green_sand_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Green Sand] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Green Sand] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_green_sand_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Green Sand] Server response for Green Sand values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Green Sand] Error while fetching Green Sand values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("green_sand_weight", 0);
                frm.set_value("green_sand_cost", 0);
                frm.set_value("green_sand_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Green Sand] No Green Sand Hand Mould Batch records found for given date and shift_type. Reset Green Sand fields to 0.",
                );
                return;
            }

            if (data.green_sand_weight != null) {
                frm.set_value("green_sand_weight", data.green_sand_weight);
            }
            if (data.green_sand_cost != null) {
                frm.set_value("green_sand_cost", data.green_sand_cost);
            }
            if (data.green_sand_cost_per_kg != null) {
                frm.set_value(
                    "green_sand_cost_per_kg",
                    data.green_sand_cost_per_kg,
                );
            }

            console.log(
                "[Daily Costing][Green Sand] Updated Green Sand fields:",
                {
                    green_sand_weight: data.green_sand_weight,
                    green_sand_cost: data.green_sand_cost,
                    green_sand_cost_per_kg: data.green_sand_cost_per_kg,
                },
            );
        },
    });
}

function fetch_co2_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Co2] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Co2] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_co2_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Co2] Server response for Co2 values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Co2] Error while fetching Co2 values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("co2_weight", 0);
                frm.set_value("co2_cost", 0);
                frm.set_value("co2_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Co2] No Co2 Mould Batch records found for given date and shift_type. Reset Co2 fields to 0.",
                );
                return;
            }

            if (data.co2_weight != null) {
                frm.set_value("co2_weight", data.co2_weight);
            }
            if (data.co2_cost != null) {
                frm.set_value("co2_cost", data.co2_cost);
            }
            if (data.co2_cost_per_kg != null) {
                frm.set_value("co2_cost_per_kg", data.co2_cost_per_kg);
            }

            console.log("[Daily Costing][Co2] Updated Co2 fields:", {
                co2_weight: data.co2_weight,
                co2_cost: data.co2_cost,
                co2_cost_per_kg: data.co2_cost_per_kg,
            });
        },
    });
}

function fetch_heat_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Heat] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Heat] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_heat_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Heat] Server response for Heat values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Heat] Error while fetching Heat values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("liquid_metal", 0);
                frm.set_value("liquid_metal_cost", 0);
                frm.set_value("ladle_cost", 0);
                frm.set_value("liquid_metal_cost_per_kg", 0);
                frm.set_value("ladle_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Heat] No Heat records found for given date and shift_type. Reset Heat fields to 0.",
                );
                return;
            }

            if (data.liquid_metal != null) {
                frm.set_value("liquid_metal", data.liquid_metal);
            }
            if (data.liquid_metal_cost != null) {
                frm.set_value("liquid_metal_cost", data.liquid_metal_cost);
            }
            if (data.ladle_cost != null) {
                frm.set_value("ladle_cost", data.ladle_cost);
            }
            if (data.liquid_metal_cost_per_kg != null) {
                frm.set_value("liquid_metal_cost_per_kg", data.liquid_metal_cost_per_kg);
            }
            if (data.ladle_cost_per_kg != null) {
                frm.set_value("ladle_cost_per_kg", data.ladle_cost_per_kg);
            }

            console.log("[Daily Costing][Heat] Updated Heat fields:", {
                liquid_metal: data.liquid_metal,
                liquid_metal_cost: data.liquid_metal_cost,
                ladle_cost: data.ladle_cost,
                liquid_metal_cost_per_kg: data.liquid_metal_cost_per_kg,
                ladle_cost_per_kg: data.ladle_cost_per_kg,
            });
        },
    });
}

function fetch_core_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Core] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Core] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_core_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Core] Server response for Core values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Core] Error while fetching Core values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("core_weight", 0);
                frm.set_value("core_cost", 0);
                frm.set_value("core_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Core] No Core Production records found for given date and shift_type. Reset Core fields to 0.",
                );
                return;
            }

            if (data.core_weight != null) {
                frm.set_value("core_weight", data.core_weight);
            }
            if (data.core_cost != null) {
                frm.set_value("core_cost", data.core_cost);
            }
            if (data.core_cost_per_kg != null) {
                frm.set_value("core_cost_per_kg", data.core_cost_per_kg);
            }

            console.log("[Daily Costing][Core] Updated Core fields:", {
                core_weight: data.core_weight,
                core_cost: data.core_cost,
                core_cost_per_kg: data.core_cost_per_kg,
            });
        },
    });
}

function fetch_shotblast_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Shot Blast] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Shot Blast] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_shotblast_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Shot Blast] Server response for Shot Blast values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Shot Blast] Error while fetching Shot Blast values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("shotblast_weight", 0);
                frm.set_value("shotblast_cost", 0);
                frm.set_value("shotblast_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Shot Blast] No Shot Blast records found for given date and shift_type. Reset Shot Blast fields to 0.",
                );
                return;
            }

            if (data.shotblast_weight != null) {
                frm.set_value("shotblast_weight", data.shotblast_weight);
            }
            if (data.shotblast_cost != null) {
                frm.set_value("shotblast_cost", data.shotblast_cost);
            }
            if (data.shotblast_cost_per_kg != null) {
                frm.set_value("shotblast_cost_per_kg", data.shotblast_cost_per_kg);
            }

            console.log("[Daily Costing][Shot Blast] Updated Shot Blast fields:", {
                shotblast_weight: data.shotblast_weight,
                shotblast_cost: data.shotblast_cost,
                shotblast_cost_per_kg: data.shotblast_cost_per_kg,
            });
        },
    });
}

function fetch_fettling_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Fettling] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Fettling] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_fettling_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Fettling] Server response for Fettling values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Fettling] Error while fetching Fettling values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("fettling_weight", 0);
                frm.set_value("fettling_cost", 0);
                frm.set_value("fettling_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Fettling] No Fettling records found for given date and shift_type. Reset Fettling fields to 0.",
                );
                return;
            }

            if (data.fettling_weight != null) {
                frm.set_value("fettling_weight", data.fettling_weight);
            }
            if (data.fettling_cost != null) {
                frm.set_value("fettling_cost", data.fettling_cost);
            }
            if (data.fettling_cost_per_kg != null) {
                frm.set_value("fettling_cost_per_kg", data.fettling_cost_per_kg);
            }

            console.log("[Daily Costing][Fettling] Updated Fettling fields:", {
                fettling_weight: data.fettling_weight,
                fettling_cost: data.fettling_cost,
                fettling_cost_per_kg: data.fettling_cost_per_kg,
            });
        },
    });
}

function fetch_finishing_values_for_daily_costing(frm) {
    const { date, shift_type } = frm.doc || {};

    console.log("[Daily Costing][Finishing] Fetch function called with:", {
        date,
        shift_type,
    });

    if (!date || !shift_type) {
        console.log(
            "[Daily Costing][Finishing] Skipping fetch. Missing date or shift_type.",
        );
        return;
    }

    frappe.call({
        method:
            "shiw.shiw.doctype.daily_costing.daily_costing.get_finishing_values_for_daily_costing",
        args: {
            date: date,
            shift_type: shift_type,
        },
        callback: function (r) {
            console.log(
                "[Daily Costing][Finishing] Server response for Finishing values:",
                r,
            );

            if (!r || r.exc) {
                console.error(
                    "[Daily Costing][Finishing] Error while fetching Finishing values",
                    r && r.exc,
                );
                return;
            }

            const data = r.message || {};

            if (Object.keys(data).length === 0) {
                frm.set_value("finishing_weight", 0);
                frm.set_value("finishing_cost", 0);
                frm.set_value("finishing_cost_per_kg", 0);
                console.log(
                    "[Daily Costing][Finishing] No Finishing records found for given date and shift_type. Reset Finishing fields to 0.",
                );
                return;
            }

            if (data.finishing_weight != null) {
                frm.set_value("finishing_weight", data.finishing_weight);
            }
            if (data.finishing_cost != null) {
                frm.set_value("finishing_cost", data.finishing_cost);
            }
            if (data.finishing_cost_per_kg != null) {
                frm.set_value("finishing_cost_per_kg", data.finishing_cost_per_kg);
            }

            console.log("[Daily Costing][Finishing] Updated Finishing fields:", {
                finishing_weight: data.finishing_weight,
                finishing_cost: data.finishing_cost,
                finishing_cost_per_kg: data.finishing_cost_per_kg,
            });
        },
    });
}
// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Costing", {
// 	refresh(frm) {

// 	},
// });

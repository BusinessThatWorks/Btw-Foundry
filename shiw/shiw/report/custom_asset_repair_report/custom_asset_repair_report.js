frappe.query_reports["Custom Asset Repair report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Failure Date",
            fieldtype: "Datetime",
            default: frappe.datetime.add_days(frappe.datetime.now_datetime(), -7),
            reqd: 0,
        },
        {
            fieldname: "to_date",
            label: "To Failure Date",
            fieldtype: "Datetime",
            default: frappe.datetime.now_datetime(),
            reqd: 0,
        },
        {
            fieldname: "asset",
            label: "Asset",
            fieldtype: "Link",
            options: "Asset",
            reqd: 0,
        },
        {
            fieldname: "status",
            label: "Repair Status",
            fieldtype: "Select",
            options: "\nOpen\nWork in Progress\nCompleted\nCancelled",
            reqd: 0,
        },
        {
            fieldname: "type",
            label: "Electrical/Mechanical",
            fieldtype: "Select",
            options: "\nElectrical\nMechanical",
            reqd: 0,
        },
        {
            fieldname: "attended_by",
            label: "Attended By",
            fieldtype: "Data",
            reqd: 0,
        },
    ],
};



// Purchase Invoice Tracker Report JavaScript
frappe.query_reports["Purchase Invoice Tracker"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier"
        },
        {
            "fieldname": "workflow_status",
            "label": __("Workflow Status"),
            "fieldtype": "Select",
            "options": ""
        }
    ]
};

// Populate Workflow Status options dynamically from existing Purchase Invoices
frappe.call({
    method: 'frappe.client.get_list',
    args: {
        doctype: 'Purchase Invoice',
        fields: ['workflow_state'],
        limit_page_length: 1000,
        distinct: true
    },
    callback: function (r) {
        if (r.message) {
            const statuses = new Set();
            r.message.forEach(row => {
                if (row.workflow_state) statuses.add(row.workflow_state);
            });
            const report = frappe.query_reports["Purchase Invoice Tracker"];
            const fld = report.filters.find(f => f.fieldname === 'workflow_status');
            if (fld) {
                fld.options = [''].concat(Array.from(statuses).sort());
            }
        }
    }
});

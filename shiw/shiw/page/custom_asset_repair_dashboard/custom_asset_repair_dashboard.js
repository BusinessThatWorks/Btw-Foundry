// Custom Asset Repair Dashboard - rich desk page powered by the existing report
if (!frappe.pages['custom-asset-repair-dashboard']) {
    frappe.pages['custom-asset-repair-dashboard'] = {};
}

frappe.pages['custom-asset-repair-dashboard'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Custom Asset Repair Dashboard'),
        single_column: true,
    });

    const state = {
        page,
        wrapper,
        controls: {},
        $cards: null,
        $charts: null,
        $table: null,
    };

    buildLayout(state);
    createFilters(state);
    bindHandlers(state);
    setDefaultDates(state);
    refresh(state);
};

function buildLayout(state) {
    // Clear
    state.page.main.empty();

    // Filter Bar
    const $filters = $('<div class="card-filterbar" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;background:#f8f9fa;padding:16px;border-radius:8px;margin-bottom:16px;"></div>');
    state.page.main.append($filters);
    state.$filters = $filters;

    // KPI Cards container
    const $cards = $('<div class="card-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px;"></div>');
    state.page.main.append($cards);
    state.$cards = $cards;

    // Charts row
    const $chartsRow = $('<div class="row" style="margin:0 -8px;gap:0;"></div>');
    const $colLeft = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Repairs by Status') + '</h5></div><div class="card-body"><div id="card-status-chart" style="height:280px;"></div></div></div></div>');
    const $colRight = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Repairs by Type') + '</h5></div><div class="card-body"><div id="card-type-chart" style="height:280px;"></div></div></div></div>');
    state.page.main.append($chartsRow.append($colLeft).append($colRight));
    state.$charts = { status: $('#card-status-chart'), type: $('#card-type-chart') };

    // Downtime Analysis Chart
    const $downtimeRow = $('<div class="row" style="margin:0 -8px;gap:0;"></div>');
    const $downtimeCol = $('<div class="col-md-12" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Downtime Analysis (Last 7 Days)') + '</h5></div><div class="card-body"><div id="card-downtime-chart" style="height:300px;"></div></div></div></div>');
    state.page.main.append($downtimeRow.append($downtimeCol));
    state.$charts.downtime = $('#card-downtime-chart');

    // Table preview
    const tableCardHtml = `
		<div class="card" style="margin-top:8px;">
			<div class="card-header" style="display:flex;align-items:center;justify-content:space-between;">
				<h5 style="margin:0;">${__('All Repair Records')}</h5>
				<div><button class="btn btn-sm btn-secondary" id="card-open-report">${__('Open Full Report')}</button></div>
			</div>
			<div class="card-body"><div id="card-table" style="max-height:600px;overflow-y:auto;"></div></div>
		</div>
	`;
    const $tableCard = $(tableCardHtml);
    state.page.main.append($tableCard);
    state.$table = $('#card-table');
}

function createFilters(state) {
    const addCtrl = (df) => {
        const $wrap = $('<div style="min-width:210px;"></div>').appendTo(state.$filters);
        const ctrl = frappe.ui.form.make_control({ parent: $wrap.get(0), df, render_input: true });
        state.controls[df.fieldname] = ctrl;
        return ctrl;
    };

    addCtrl({ fieldtype: 'Datetime', label: __('From Failure Date'), fieldname: 'from_date' });
    addCtrl({ fieldtype: 'Datetime', label: __('To Failure Date'), fieldname: 'to_date' });
    addCtrl({ fieldtype: 'Link', label: __('Asset'), fieldname: 'asset', options: 'Asset' });
    addCtrl({ fieldtype: 'Select', label: __('Repair Status'), fieldname: 'status', options: '\nOpen\nWork in Progress\nCompleted\nCancelled' });
    addCtrl({ fieldtype: 'Select', label: __('Type'), fieldname: 'type', options: '\nElectrical\nMechanical' });
    addCtrl({ fieldtype: 'Data', label: __('Attended By'), fieldname: 'attended_by' });

    const $btns = $('<div style="display:flex;gap:8px;align-items:end;"></div>').appendTo(state.$filters);
    state.$refresh = $('<button class="btn btn-primary">' + __('Refresh') + '</button>').appendTo($btns);
}

function bindHandlers(state) {
    state.$refresh.on('click', () => refresh(state));
    // Auto-refresh on filter change
    Object.values(state.controls).forEach((ctrl) => {
        if (ctrl && ctrl.$input) {
            $(ctrl.$input).on('change', () => refresh(state));
        }
    });
    $(document).on('click', '#card-open-report', () => {
        const params = new URLSearchParams(getFilters(state));
        window.open('/app/query-report/Custom%20Asset%20Repair%20report?' + params.toString(), '_blank');
    });
}

function setDefaultDates(state) {
    // Last 7 days by default
    const end = frappe.datetime.now_datetime();
    const start = frappe.datetime.add_days(frappe.datetime.now_datetime(), -7);
    state.controls.from_date.set_value(start);
    state.controls.to_date.set_value(end);
}

function getFilters(state) {
    const f = {};
    Object.keys(state.controls).forEach((k) => {
        const v = state.controls[k].get_value();
        if (v) f[k] = v;
    });
    return f;
}

function refresh(state) {
    state.page.set_indicator(__('Loading...'), 'blue');
    fetchReportData(getFilters(state)).then((rows) => {
        state.page.clear_indicator();
        renderCards(state, rows);
        renderCharts(state, rows);
        renderTable(state, rows);
    }).catch((err) => {
        state.page.clear_indicator();
        console.error('Dashboard load error', err);
        frappe.msgprint(__('Error loading dashboard data'));
    });
}

function fetchReportData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Custom Asset Repair report',
                filters: JSON.stringify(filters || {}),
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                let data = [];
                if (r.message) {
                    if (Array.isArray(r.message)) data = r.message;
                    else if (Array.isArray(r.message.result)) data = r.message.result;
                    else if (Array.isArray(r.message.data)) data = r.message.data;
                }
                resolve(data || []);
            },
            error: reject,
        });
    });
}

function renderCards(state, rows) {
    const total = rows.length;
    const byStatus = groupCount(rows, 'repair_status');
    const byType = groupCount(rows, 'custom_electricalmechanical');
    const totalDowntime = rows.reduce((sum, r) => sum + (parseFloat(r.downtime) || 0), 0);
    const avgDowntime = total > 0 ? totalDowntime / total : 0;
    const totalProdLoss = rows.reduce((sum, r) => sum + (parseFloat(r.custom_production_loss_in_tons) || 0), 0);
    const criticalRepairs = rows.filter(r => parseFloat(r.downtime) > 480).length; // > 8 hours

    const cards = [
        { label: __('Total Repairs'), value: total, indicator: 'Blue', datatype: 'Int' },
        { label: __('Open'), value: byStatus['Open'] || 0, indicator: 'Orange', datatype: 'Int' },
        { label: __('In Progress'), value: byStatus['Work in Progress'] || 0, indicator: 'Blue', datatype: 'Int' },
        { label: __('Completed'), value: byStatus['Completed'] || 0, indicator: 'Green', datatype: 'Int' },
        { label: __('Total Downtime (hrs)'), value: (totalDowntime / 60).toFixed(1), indicator: 'Red', datatype: 'Float', precision: 1 },
        { label: __('Avg Downtime (hrs)'), value: (avgDowntime / 60).toFixed(1), indicator: 'Purple', datatype: 'Float', precision: 1 },
        { label: __('Production Loss (tons)'), value: totalProdLoss.toFixed(2), indicator: 'Red', datatype: 'Float', precision: 2 },
        { label: __('Critical Repairs (>8hrs)'), value: criticalRepairs, indicator: 'Red', datatype: 'Int' },
    ];

    state.$cards.empty();
    cards.forEach((c) => state.$cards.append(createCard(c)));
}

function renderCharts(state, rows) {
    // Status Pie
    const byStatus = groupCount(rows, 'repair_status');
    const sLabels = Object.keys(byStatus);
    const sValues = sLabels.map((k) => byStatus[k]);
    state.$charts.status.empty();
    if (sLabels.length > 0) {
        new frappe.Chart(state.$charts.status.get(0), {
            data: { labels: sLabels, datasets: [{ name: __('Count'), values: sValues }] },
            type: 'pie', height: 260, colors: ['#3498db', '#f39c12', '#27ae60', '#e74c3c', '#6c757d']
        });
    }

    // Type Bar
    const byType = groupCount(rows, 'custom_electricalmechanical');
    const tLabels = Object.keys(byType);
    const tValues = tLabels.map((k) => byType[k]);
    state.$charts.type.empty();
    if (tLabels.length > 0) {
        new frappe.Chart(state.$charts.type.get(0), {
            data: { labels: tLabels, datasets: [{ name: __('Count'), values: tValues }] },
            type: 'bar', height: 260, colors: ['#1abc9c', '#e67e22']
        });
    }

    // Downtime Trend (last 7 days)
    renderDowntimeChart(state, rows);
}

function renderDowntimeChart(state, rows) {
    // Group by date and sum downtime for last 7 days
    const dailyDowntime = {};
    const today = new Date();

    // Initialize last 7 days with 0 downtime
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];
        dailyDowntime[dateStr] = 0;
    }

    // Add actual downtime data
    rows.forEach(row => {
        if (row.failure_date) {
            const date = row.failure_date.split(' ')[0]; // Get date part only
            if (dailyDowntime.hasOwnProperty(date)) {
                dailyDowntime[date] += (parseFloat(row.downtime) || 0);
            }
        }
    });

    const dates = Object.keys(dailyDowntime).sort();
    const downtimeValues = dates.map(date => dailyDowntime[date] / 60); // Convert to hours

    state.$charts.downtime.empty();
    new frappe.Chart(state.$charts.downtime.get(0), {
        data: {
            labels: dates.map(d => frappe.datetime.str_to_user(d)),
            datasets: [{ name: __('Downtime (Hours)'), values: downtimeValues }]
        },
        type: 'line', height: 280, colors: ['#e74c3c']
    });
}

function renderTable(state, rows) {
    const sorted = [...rows].sort((a, b) => new Date(b.failure_date || '1900-01-01') - new Date(a.failure_date || '1900-01-01'));
    const allRepairs = sorted; // Show all repairs

    const $table = $('<table class="table table-sm table-striped" style="margin:0;">\
		<thead><tr>\
		<th>' + __('Asset ID') + '</th>\
		<th>' + __('Asset Name') + '</th>\
		<th>' + __('Failure Date') + '</th>\
		<th>' + __('Status') + '</th>\
		<th>' + __('Type') + '</th>\
		<th>' + __('Downtime (hrs)') + '</th>\
		<th>' + __('Attended By') + '</th>\
		<th>' + __('Production Loss (tons)') + '</th>\
		<th>' + __('Description') + '</th>\
		</tr></thead><tbody></tbody></table>');

    const $tb = $table.find('tbody');
    allRepairs.forEach((r) => {
        const downtimeHours = r.downtime ? (parseFloat(r.downtime) / 60).toFixed(1) : '0';
        const prodLoss = r.custom_production_loss_in_tons ? parseFloat(r.custom_production_loss_in_tons).toFixed(2) : '0';
        $tb.append('<tr>\
			<td>' + frappe.utils.escape_html(r.asset || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.asset_name || '') + '</td>\
			<td>' + (r.failure_date ? frappe.datetime.str_to_user(r.failure_date) : '') + '</td>\
			<td><span class="badge badge-' + getStatusColor(r.repair_status) + '">' + frappe.utils.escape_html(r.repair_status || '') + '</span></td>\
			<td>' + frappe.utils.escape_html(r.custom_electricalmechanical || '') + '</td>\
			<td>' + downtimeHours + '</td>\
			<td>' + frappe.utils.escape_html(r.attend_by || '') + '</td>\
			<td>' + prodLoss + '</td>\
			<td>' + frappe.utils.escape_html((r.description || '').substring(0, 50) + (r.description && r.description.length > 50 ? '...' : '')) + '</td>\
		</tr>');
    });

    state.$table.empty().append($table);
}

function getStatusColor(status) {
    const colors = {
        'Open': 'warning',
        'Work in Progress': 'info',
        'Completed': 'success',
        'Cancelled': 'secondary'
    };
    return colors[status] || 'secondary';
}

function createCard(card) {
    const indicator = (card.indicator || 'blue').toString().toLowerCase();
    return $('<div class="number-card" style="background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.06);position:relative;overflow:hidden;">\
		<div style="position:absolute;top:0;left:0;right:0;height:4px;background:' + getIndicatorColor(indicator) + '"></div>\
		<div style="text-align:center;">\
			<div style="font-size:2rem;font-weight:700;color:#2c3e50;">' + frappe.format(card.value || 0, { fieldtype: card.datatype || 'Int', precision: card.precision || 0 }) + '</div>\
			<div style="font-size:0.95rem;color:#7f8c8d;">' + frappe.utils.escape_html(card.label || '') + '</div>\
		</div>\
	</div>');
}

function getIndicatorColor(indicator) {
    const colors = {
        'green': 'linear-gradient(90deg,#27ae60,#229954)',
        'red': 'linear-gradient(90deg,#e74c3c,#c0392b)',
        'orange': 'linear-gradient(90deg,#f39c12,#e67e22)',
        'purple': 'linear-gradient(90deg,#9b59b6,#8e44ad)',
        'blue': 'linear-gradient(90deg,#3498db,#2980b9)'
    };
    return colors[indicator] || colors.blue;
}

function groupCount(rows, key) {
    const map = {};
    (rows || []).forEach((r) => {
        const v = (r[key] || '').toString();
        map[v] = (map[v] || 0) + 1;
    });
    return map;
}

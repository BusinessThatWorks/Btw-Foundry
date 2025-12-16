// Custom Asset Maintenance Dashboard - rich desk page powered by the existing report
if (!frappe.pages['custom-asset-maintenance-dashboard']) {
    frappe.pages['custom-asset-maintenance-dashboard'] = {};
}

frappe.pages['custom-asset-maintenance-dashboard'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Custom Asset Maintenance Dashboard'),
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

    // Create tabs container
    const $tabsContainer = $('<div class="nav nav-tabs" id="camd-tabs" role="tablist" style="margin-bottom: 20px;"></div>');
    state.page.main.append($tabsContainer);

    // Tab 1: Maintenance Schedule
    const $tab1 = $('<button class="nav-link active" id="schedule-tab" data-bs-toggle="tab" data-bs-target="#schedule-pane" type="button" role="tab" aria-controls="schedule-pane" aria-selected="true">' + __('Maintenance Schedule') + '</button>');
    $tabsContainer.append($tab1);

    // Tab 2: Maintenance Log
    const $tab2 = $('<button class="nav-link" id="log-tab" data-bs-toggle="tab" data-bs-target="#log-pane" type="button" role="tab" aria-controls="log-pane" aria-selected="false">' + __('Maintenance Log') + '</button>');
    $tabsContainer.append($tab2);

    // Tab content container
    const $tabContent = $('<div class="tab-content" id="camd-tab-content"></div>');
    state.page.main.append($tabContent);

    // Tab 1 Content: Original Maintenance Schedule Dashboard
    const $schedulePane = $('<div class="tab-pane fade show active" id="schedule-pane" role="tabpanel" aria-labelledby="schedule-tab"></div>');
    $tabContent.append($schedulePane);

    // Filter Bar for Schedule Tab
    const $filters = $('<div class="camd-filterbar" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;background:#f8f9fa;padding:16px;border-radius:8px;margin-bottom:16px;"></div>');
    $schedulePane.append($filters);
    state.$filters = $filters;

    // KPI Cards container
    const $cards = $('<div class="camd-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px;"></div>');
    $schedulePane.append($cards);
    state.$cards = $cards;

    // Charts row
    const $chartsRow = $('<div class="row" style="margin:0 -8px;gap:0;"></div>');
    const $colLeft = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Tasks by Status') + '</h5></div><div class="card-body"><div id="camd-status-chart" style="height:280px;"></div></div></div></div>');
    const $colRight = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Tasks by Type') + '</h5></div><div class="card-body"><div id="camd-type-chart" style="height:280px;"></div></div></div></div>');
    $schedulePane.append($chartsRow.append($colLeft).append($colRight));
    state.$charts = { status: $('#camd-status-chart'), type: $('#camd-type-chart') };

    // Table preview (fixed markup)
    const tableCardHtml = `
		<div class="card" style="margin-top:8px;">
			<div class="card-header" style="display:flex;align-items:center;justify-content:space-between;">
				<h5 style="margin:0;">${__('All Maintenance Tasks')}</h5>
				<div><button class="btn btn-sm btn-secondary" id="camd-open-report">${__('Open Full Report')}</button></div>
			</div>
			<div class="card-body"><div id="camd-table" style="overflow-x:auto;"></div></div>
		</div>
	`;
    const $tableCard = $(tableCardHtml);
    $schedulePane.append($tableCard);
    state.$table = $('#camd-table');

    // Tab 2 Content: Maintenance Log Dashboard
    const $logPane = $('<div class="tab-pane fade" id="log-pane" role="tabpanel" aria-labelledby="log-tab"></div>');
    $tabContent.append($logPane);

    // Filter Bar for Log Tab
    const $logFilters = $('<div class="camd-log-filterbar" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;background:#f8f9fa;padding:16px;border-radius:8px;margin-bottom:16px;"></div>');
    $logPane.append($logFilters);
    state.$logFilters = $logFilters;

    // KPI Cards container for Log
    const $logCards = $('<div class="camd-log-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px;"></div>');
    $logPane.append($logCards);
    state.$logCards = $logCards;

    // Charts row for Log
    const $logChartsRow = $('<div class="row" style="margin:0 -8px;gap:0;"></div>');
    const $logColLeft = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Log Status Distribution') + '</h5></div><div class="card-body"><div id="camd-log-status-chart" style="height:280px;"></div></div></div></div>');
    const $logColRight = $('<div class="col-md-6" style="padding:8px;"><div class="card"><div class="card-header"><h5 style="margin:0;">' + __('Log Type Distribution') + '</h5></div><div class="card-body"><div id="camd-log-type-chart" style="height:280px;"></div></div></div></div>');
    $logPane.append($logChartsRow.append($logColLeft).append($logColRight));
    state.$logCharts = { status: $('#camd-log-status-chart'), type: $('#camd-log-type-chart') };

    // Table preview for Log
    const logTableCardHtml = `
		<div class="card" style="margin-top:8px;">
			<div class="card-header" style="display:flex;align-items:center;justify-content:space-between;">
				<h5 style="margin:0;">${__('All Maintenance Logs')}</h5>
				<div><button class="btn btn-sm btn-secondary" id="camd-open-log-report">${__('Open Full Log Report')}</button></div>
			</div>
			<div class="card-body"><div id="camd-log-table" style="overflow-x:auto;"></div></div>
		</div>
	`;
    const $logTableCard = $(logTableCardHtml);
    $logPane.append($logTableCard);
    state.$logTable = $('#camd-log-table');
}

function createFilters(state) {
    // Create filters for Schedule tab
    const addCtrl = (df, container = state.$filters) => {
        const $wrap = $('<div style="min-width:210px;"></div>').appendTo(container);
        const ctrl = frappe.ui.form.make_control({ parent: $wrap.get(0), df, render_input: true });
        state.controls[df.fieldname] = ctrl;
        return ctrl;
    };

    // Schedule tab filters
    addCtrl({ fieldtype: 'Date', label: __('From Date'), fieldname: 'from_date' });
    addCtrl({ fieldtype: 'Date', label: __('To Date'), fieldname: 'to_date' });
    addCtrl({ fieldtype: 'Link', label: __('Asset Name'), fieldname: 'asset_name', options: 'Asset' });
    addCtrl({ fieldtype: 'Link', label: __('Asset Category'), fieldname: 'asset_category', options: 'Asset Category' });
    addCtrl({ fieldtype: 'Link', label: __('Item Code'), fieldname: 'item_code', options: 'Item' });
    addCtrl({ fieldtype: 'Link', label: __('Maintenance Team'), fieldname: 'maintenance_team', options: 'Asset Maintenance Team' });
    addCtrl({ fieldtype: 'Select', label: __('Maintenance Status'), fieldname: 'maintenance_status', options: '\nPlanned\nPending\nCompleted\nOverdue\nCancelled' });
    addCtrl({ fieldtype: 'Select', label: __('Maintenance Type'), fieldname: 'maintenance_type', options: '\nPreventive Maintenance\nCorrective Maintenance\nBreakdown Maintenance' });
    addCtrl({ fieldtype: 'Select', label: __('Assign To'), fieldname: 'assign_to_name', options: '' });

    const $btns = $('<div style="display:flex;gap:8px;align-items:end;"></div>').appendTo(state.$filters);
    state.$refresh = $('<button class="btn btn-primary">' + __('Refresh') + '</button>').appendTo($btns);

    // Create filters for Log tab
    const addLogCtrl = (df) => {
        const $wrap = $('<div style="min-width:210px;"></div>').appendTo(state.$logFilters);
        const ctrl = frappe.ui.form.make_control({ parent: $wrap.get(0), df, render_input: true });
        state.logControls[df.fieldname] = ctrl;
        return ctrl;
    };

    // Initialize log controls object
    state.logControls = {};

    // Log tab filters
    addLogCtrl({ fieldtype: 'Date', label: __('From Date'), fieldname: 'log_from_date' });
    addLogCtrl({ fieldtype: 'Date', label: __('To Date'), fieldname: 'log_to_date' });
    addLogCtrl({ fieldtype: 'Link', label: __('Asset Name'), fieldname: 'log_asset_name', options: 'Asset' });
    addLogCtrl({ fieldtype: 'Link', label: __('Item Code'), fieldname: 'log_item_code', options: 'Item' });
    addLogCtrl({ fieldtype: 'Select', label: __('Maintenance Type'), fieldname: 'log_maintenance_type', options: '\nPreventive Maintenance\nCorrective Maintenance\nBreakdown Maintenance' });
    addLogCtrl({ fieldtype: 'Select', label: __('Maintenance Status'), fieldname: 'log_maintenance_status', options: '\nPlanned\nPending\nCompleted\nOverdue\nCancelled' });
    addLogCtrl({ fieldtype: 'Select', label: __('Assign To Name'), fieldname: 'log_assign_to_name', options: '' });

    const $logBtns = $('<div style="display:flex;gap:8px;align-items:end;"></div>').appendTo(state.$logFilters);
    state.$logRefresh = $('<button class="btn btn-primary">' + __('Refresh') + '</button>').appendTo($logBtns);

    // Populate user dropdowns with full names
    populateUserDropdowns(state);
}

function populateUserDropdowns(state) {
    // Fetch users and populate dropdowns
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'User',
            fields: ['name', 'full_name'],
            filters: { enabled: 1 },
            limit_page_length: 0
        },
        callback: function (r) {
            if (r.message) {
                const userOptions = ['']; // Start with empty option
                r.message.forEach(user => {
                    const displayName = user.full_name || user.name;
                    userOptions.push(displayName);
                });

                // Update schedule tab assign to dropdown
                if (state.controls.assign_to_name && state.controls.assign_to_name.$input) {
                    const $select = state.controls.assign_to_name.$input;
                    $select.empty();
                    userOptions.forEach(option => {
                        $select.append(new Option(option, option));
                    });
                }

                // Update log tab assign to dropdown
                if (state.logControls.log_assign_to_name && state.logControls.log_assign_to_name.$input) {
                    const $select = state.logControls.log_assign_to_name.$input;
                    $select.empty();
                    userOptions.forEach(option => {
                        $select.append(new Option(option, option));
                    });
                }
            }
        }
    });
}

function bindHandlers(state) {
    // Schedule tab handlers
    state.$refresh.on('click', () => refresh(state));
    // Auto-refresh on filter change for schedule tab
    Object.values(state.controls).forEach((ctrl) => {
        if (ctrl && ctrl.$input) {
            $(ctrl.$input).on('change', () => refresh(state));
        }
    });
    $(document).on('click', '#camd-open-report', () => {
        const params = new URLSearchParams(getFilters(state));
        window.open('/app/query-report/Custom%20Asset%20Maintenance%20Schedule%20Report?' + params.toString(), '_blank');
    });

    // Log tab handlers
    state.$logRefresh.on('click', () => refreshLog(state));
    // Auto-refresh on filter change for log tab
    Object.values(state.logControls).forEach((ctrl) => {
        if (ctrl && ctrl.$input) {
            $(ctrl.$input).on('change', () => refreshLog(state));
        }
    });
    $(document).on('click', '#camd-open-log-report', () => {
        const params = new URLSearchParams(getLogFilters(state));
        window.open('/app/query-report/Custom%20Asset%20Maintenance%20Log%20Report?' + params.toString(), '_blank');
    });

    // Tab change handlers
    $('#schedule-tab').on('click', () => {
        $('#schedule-tab').addClass('active').attr('aria-selected', 'true');
        $('#log-tab').removeClass('active').attr('aria-selected', 'false');
        $('#schedule-pane').addClass('active show');
        $('#log-pane').removeClass('active show');
    });

    $('#log-tab').on('click', () => {
        $('#log-tab').addClass('active').attr('aria-selected', 'true');
        $('#schedule-tab').removeClass('active').attr('aria-selected', 'false');
        $('#log-pane').addClass('active show');
        $('#schedule-pane').removeClass('active show');

        if (!state.logDataLoaded) {
            refreshLog(state);
        }
    });
}

function setDefaultDates(state) {
    // Current month by default for schedule tab
    const start = frappe.datetime.month_start();
    const end = frappe.datetime.month_end();
    state.controls.from_date.set_value(start);
    state.controls.to_date.set_value(end);

    // Set default dates for log tab
    state.logControls.log_from_date.set_value(start);
    state.logControls.log_to_date.set_value(end);
}

function getFilters(state) {
    const f = {};
    Object.keys(state.controls).forEach((k) => {
        const v = state.controls[k].get_value();
        if (v) f[k] = v;
    });
    return f;
}

function getLogFilters(state) {
    const f = {};
    Object.keys(state.logControls).forEach((k) => {
        const v = state.logControls[k].get_value();
        if (v) {
            // Map log filter names to report filter names
            const mappedKey = k.replace('log_', '');
            f[mappedKey] = v;
        }
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
        // Silently handle dashboard load errors
        frappe.msgprint(__('Error loading dashboard data'));
    });
}

function refreshLog(state) {
    state.page.set_indicator(__('Loading Log Data...'), 'blue');
    fetchLogReportData(getLogFilters(state)).then((rows) => {
        state.page.clear_indicator();
        renderLogCards(state, rows);
        renderLogCharts(state, rows);
        renderLogTable(state, rows);
        state.logDataLoaded = true;
    }).catch((err) => {
        state.page.clear_indicator();
        // Silently handle log dashboard load errors

        // Show a message that the report is not available yet
        state.$logCards.html('<div class="alert alert-info" style="margin: 20px;">' +
            __('Asset Maintenance Log Report is not available yet. Please create the Asset Maintenance Log doctype first.') +
            '</div>');
        state.$logCharts.status.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' +
            __('Report not available') + '</div>');
        state.$logCharts.type.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' +
            __('Report not available') + '</div>');
        state.$logTable.html('<div class="alert alert-info" style="margin: 20px;">' +
            __('Asset Maintenance Log Report is not available yet.') + '</div>');

        state.logDataLoaded = true;
    });
}

function fetchReportData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Custom Asset Maintenance Schedule Report',
                filters: JSON.stringify(filters || {}),
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                let data = [];
                try {
                    if (r && r.message) {
                        if (Array.isArray(r.message)) data = r.message;
                        else if (Array.isArray(r.message.result)) data = r.message.result;
                        else if (Array.isArray(r.message.data)) data = r.message.data;
                    }
                } catch (e) {
                    // Silently handle parsing errors
                }
                resolve(data || []);
            },
            error: (err) => {
                // Silently handle fetch errors
                resolve([]); // Return empty array instead of rejecting
            },
        });
    });
}

function fetchLogReportData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Custom Asset Maintenance Log Report',
                filters: JSON.stringify(filters || {}),
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                let data = [];
                try {
                    if (r && r.message) {
                        if (Array.isArray(r.message)) data = r.message;
                        else if (Array.isArray(r.message.result)) data = r.message.result;
                        else if (Array.isArray(r.message.data)) data = r.message.data;
                    }
                } catch (e) {
                    // Silently handle parsing errors
                }
                resolve(data || []);
            },
            error: (err) => {
                // Silently handle fetch errors
                resolve([]); // Return empty array instead of rejecting
            },
        });
    });
}

function renderCards(state, rows) {
    const total = rows.length;
    const byStatus = groupCount(rows, 'maintenance_status');
    const byType = groupCount(rows, 'maintenance_type');
    const dueSoon = rows.filter((r) => isDueInDays(r.next_due_date, 7) && (r.maintenance_status || '').toLowerCase() !== 'completed').length;

    const cards = [
        { label: __('Total Tasks'), value: total, indicator: 'Blue', datatype: 'Int' },
        { label: __('Planned'), value: byStatus['Planned'] || 0, indicator: 'Blue', datatype: 'Int' },
        { label: __('Pending'), value: byStatus['Pending'] || 0, indicator: 'Orange', datatype: 'Int' },
        { label: __('Completed'), value: byStatus['Completed'] || 0, indicator: 'Green', datatype: 'Int' },
        { label: __('Overdue'), value: byStatus['Overdue'] || 0, indicator: 'Red', datatype: 'Int' },
        { label: __('Due in 7 Days'), value: dueSoon, indicator: 'Purple', datatype: 'Int' },
    ];

    state.$cards.empty();
    cards.forEach((c) => state.$cards.append(createCard(c)));
}

function renderCharts(state, rows) {
    // Status Pie Chart
    const byStatus = groupCount(rows, 'maintenance_status');
    const sLabels = Object.keys(byStatus).filter(k => byStatus[k] > 0);
    const sValues = sLabels.map((k) => byStatus[k]);

    // Clear existing chart safely
    state.$charts.status.empty();

    if (sLabels.length > 0 && sValues.length > 0 && sValues.every(v => v > 0 && v < 10000)) {
        try {
            // Create chart with error suppression
            const chart = new frappe.Chart(state.$charts.status.get(0), {
                data: {
                    labels: sLabels,
                    datasets: [{
                        name: __('Count'),
                        values: sValues
                    }]
                },
                type: 'pie',
                height: 260,
                colors: ['#3498db', '#f39c12', '#27ae60', '#e74c3c', '#6c757d']
            });

            // Suppress any chart-related console errors
            if (chart && chart.svg) {
                const originalError = console.error;
                console.error = function () {
                    const args = Array.prototype.slice.call(arguments);
                    if (args.some(arg => typeof arg === 'string' &&
                        (arg.includes('negative value') || arg.includes('width') || arg.includes('height')))) {
                        return; // Suppress chart-related errors
                    }
                    originalError.apply(console, arguments);
                };

                // Restore console.error after a short delay
                setTimeout(() => {
                    console.error = originalError;
                }, 100);
            }
        } catch (e) {
            // Fallback to text summary if chart fails
            const statusSummary = sLabels.map(k => `${k}: ${byStatus[k]}`).join(', ');
            state.$charts.status.html(`
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:260px;color:#6c757d;padding:20px;">
                    <h6 style="margin-bottom:15px;color:#333;">Maintenance Status Summary</h6>
                    <div style="text-align:center;line-height:1.6;">${statusSummary || 'No data available'}</div>
                </div>
            `);
        }
    } else {
        state.$charts.status.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' + __('No data available') + '</div>');
    }

    // Type Bar Chart
    const byType = groupCount(rows, 'maintenance_type');
    const tLabels = Object.keys(byType).filter(k => byType[k] > 0);
    const tValues = tLabels.map((k) => byType[k]);

    // Clear existing chart safely
    state.$charts.type.empty();

    if (tLabels.length > 0 && tValues.length > 0 && tValues.every(v => v > 0 && v < 10000)) {
        try {
            // Create chart with error suppression
            const chart = new frappe.Chart(state.$charts.type.get(0), {
                data: {
                    labels: tLabels,
                    datasets: [{
                        name: __('Count'),
                        values: tValues
                    }]
                },
                type: 'bar',
                height: 260,
                colors: ['#1abc9c']
            });

            // Suppress any chart-related console errors
            if (chart && chart.svg) {
                const originalError = console.error;
                console.error = function () {
                    const args = Array.prototype.slice.call(arguments);
                    if (args.some(arg => typeof arg === 'string' &&
                        (arg.includes('negative value') || arg.includes('width') || arg.includes('height')))) {
                        return; // Suppress chart-related errors
                    }
                    originalError.apply(console, arguments);
                };

                // Restore console.error after a short delay
                setTimeout(() => {
                    console.error = originalError;
                }, 100);
            }
        } catch (e) {
            // Fallback to text summary if chart fails
            const typeSummary = tLabels.map(k => `${k}: ${byType[k]}`).join(', ');
            state.$charts.type.html(`
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:260px;color:#6c757d;padding:20px;">
                    <h6 style="margin-bottom:15px;color:#333;">Maintenance Type Summary</h6>
                    <div style="text-align:center;line-height:1.6;">${typeSummary || 'No data available'}</div>
                </div>
            `);
        }
    } else {
        state.$charts.type.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' + __('No data available') + '</div>');
    }
}

function renderTable(state, rows) {
    const sorted = [...rows].sort((a, b) => (new Date(a.next_due_date || '2100-01-01')) - (new Date(b.next_due_date || '2100-01-01')));
    // Show all tasks instead of limiting to 15
    const allTasks = sorted;

    const $table = $('<table class="table table-sm table-striped" style="margin:0;">\
		<thead><tr>\
		<th>' + __('Asset Name') + '</th>\
		<th>' + __('Item Code') + '</th>\
		<th>' + __('Item Name') + '</th>\
		<th>' + __('Maintenance Team') + '</th>\
		<th>' + __('Task') + '</th>\
		<th>' + __('Status') + '</th>\
		<th>' + __('Type') + '</th>\
		<th>' + __('Assign To') + '</th>\
		<th>' + __('Next Due') + '</th>\
		<th>' + __('Last Completion') + '</th>\
		</tr></thead><tbody></tbody></table>');

    const $tb = $table.find('tbody');
    allTasks.forEach((r) => {
        $tb.append('<tr>\
			<td>' + frappe.utils.escape_html(r.asset_name || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.item_code || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.item_name || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_team || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_task || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_status || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_type || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.assign_to_name || '') + '</td>\
			<td>' + (r.next_due_date ? frappe.datetime.str_to_user(r.next_due_date) : '') + '</td>\
			<td>' + (r.last_completion_date ? frappe.datetime.str_to_user(r.last_completion_date) : '') + '</td>\
		</tr>');
    });

    state.$table.empty().append($table);
}

// Log-specific rendering functions
function renderLogCards(state, rows) {
    const total = rows.length;
    const byStatus = groupCount(rows, 'maintenance_status');
    const byType = groupCount(rows, 'maintenance_type');
    const completed = byStatus['Completed'] || 0;
    const overdue = byStatus['Overdue'] || 0;
    const pending = byStatus['Pending'] || 0;

    const cards = [
        { label: __('Total Logs'), value: total, indicator: 'Blue', datatype: 'Int' },
        { label: __('Completed'), value: completed, indicator: 'Green', datatype: 'Int' },
        { label: __('Pending'), value: pending, indicator: 'Orange', datatype: 'Int' },
        { label: __('Overdue'), value: overdue, indicator: 'Red', datatype: 'Int' },
        { label: __('Preventive'), value: byType['Preventive'] || 0, indicator: 'Blue', datatype: 'Int' },
        { label: __('Corrective'), value: byType['Corrective'] || 0, indicator: 'Purple', datatype: 'Int' },
    ];

    state.$logCards.empty();
    cards.forEach((c) => state.$logCards.append(createCard(c)));
}

function renderLogCharts(state, rows) {
    // Status Pie Chart
    const byStatus = groupCount(rows, 'maintenance_status');
    const sLabels = Object.keys(byStatus).filter(k => byStatus[k] > 0);
    const sValues = sLabels.map((k) => byStatus[k]);

    // Clear existing chart safely
    state.$logCharts.status.empty();

    if (sLabels.length > 0 && sValues.length > 0 && sValues.every(v => v > 0 && v < 10000)) {
        try {
            // Create chart with error suppression
            const chart = new frappe.Chart(state.$logCharts.status.get(0), {
                data: {
                    labels: sLabels,
                    datasets: [{
                        name: __('Count'),
                        values: sValues
                    }]
                },
                type: 'pie',
                height: 260,
                colors: ['#27ae60', '#f39c12', '#e74c3c', '#6c757d']
            });

            // Suppress any chart-related console errors
            if (chart && chart.svg) {
                const originalError = console.error;
                console.error = function () {
                    const args = Array.prototype.slice.call(arguments);
                    if (args.some(arg => typeof arg === 'string' &&
                        (arg.includes('negative value') || arg.includes('width') || arg.includes('height')))) {
                        return; // Suppress chart-related errors
                    }
                    originalError.apply(console, arguments);
                };

                // Restore console.error after a short delay
                setTimeout(() => {
                    console.error = originalError;
                }, 100);
            }
        } catch (e) {
            // Fallback to text summary if chart fails
            const statusSummary = sLabels.map(k => `${k}: ${byStatus[k]}`).join(', ');
            state.$logCharts.status.html(`
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:260px;color:#6c757d;padding:20px;">
                    <h6 style="margin-bottom:15px;color:#333;">Maintenance Status Summary</h6>
                    <div style="text-align:center;line-height:1.6;">${statusSummary || 'No data available'}</div>
                </div>
            `);
        }
    } else {
        state.$logCharts.status.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' + __('No data available') + '</div>');
    }

    // Type Bar Chart
    const byType = groupCount(rows, 'maintenance_type');
    const tLabels = Object.keys(byType).filter(k => byType[k] > 0);
    const tValues = tLabels.map((k) => byType[k]);

    // Clear existing chart safely
    state.$logCharts.type.empty();

    if (tLabels.length > 0 && tValues.length > 0 && tValues.every(v => v > 0 && v < 10000)) {
        try {
            // Create chart with error suppression
            const chart = new frappe.Chart(state.$logCharts.type.get(0), {
                data: {
                    labels: tLabels,
                    datasets: [{
                        name: __('Count'),
                        values: tValues
                    }]
                },
                type: 'bar',
                height: 260,
                colors: ['#1abc9c']
            });

            // Suppress any chart-related console errors
            if (chart && chart.svg) {
                const originalError = console.error;
                console.error = function () {
                    const args = Array.prototype.slice.call(arguments);
                    if (args.some(arg => typeof arg === 'string' &&
                        (arg.includes('negative value') || arg.includes('width') || arg.includes('height')))) {
                        return; // Suppress chart-related errors
                    }
                    originalError.apply(console, arguments);
                };

                // Restore console.error after a short delay
                setTimeout(() => {
                    console.error = originalError;
                }, 100);
            }
        } catch (e) {
            // Fallback to text summary if chart fails
            const typeSummary = tLabels.map(k => `${k}: ${byType[k]}`).join(', ');
            state.$logCharts.type.html(`
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:260px;color:#6c757d;padding:20px;">
                    <h6 style="margin-bottom:15px;color:#333;">Maintenance Type Summary</h6>
                    <div style="text-align:center;line-height:1.6;">${typeSummary || 'No data available'}</div>
                </div>
            `);
        }
    } else {
        state.$logCharts.type.html('<div style="display:flex;align-items:center;justify-content:center;height:260px;color:#6c757d;">' + __('No data available') + '</div>');
    }
}

function renderLogTable(state, rows) {
    const sorted = [...rows].sort((a, b) => (new Date(b.due_date || '1900-01-01')) - (new Date(a.due_date || '1900-01-01')));
    const allLogs = sorted;

    const $table = $('<table class="table table-sm table-striped" style="margin:0;">\
		<thead><tr>\
		<th>' + __('Asset Name') + '</th>\
		<th>' + __('Item Code') + '</th>\
		<th>' + __('Item Name') + '</th>\
		<th>' + __('Task Name') + '</th>\
		<th>' + __('Status') + '</th>\
		<th>' + __('Type') + '</th>\
		<th>' + __('Due Date') + '</th>\
		<th>' + __('Completion Date') + '</th>\
		<th>' + __('Assign To') + '</th>\
		<th>' + __('Actions Performed') + '</th>\
		</tr></thead><tbody></tbody></table>');

    const $tb = $table.find('tbody');
    allLogs.forEach((r) => {
        $tb.append('<tr>\
			<td>' + frappe.utils.escape_html(r.asset_name || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.item_code || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.item_name || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.task_name || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_status || '') + '</td>\
			<td>' + frappe.utils.escape_html(r.maintenance_type || '') + '</td>\
			<td>' + (r.due_date ? frappe.datetime.str_to_user(r.due_date) : '') + '</td>\
			<td>' + (r.completion_date ? frappe.datetime.str_to_user(r.completion_date) : '') + '</td>\
			<td>' + frappe.utils.escape_html(r.assign_to_name || '') + '</td>\
			<td>' + frappe.utils.escape_html((r.actions_performed || '').substring(0, 50) + (r.actions_performed && r.actions_performed.length > 50 ? '...' : '')) + '</td>\
		</tr>');
    });

    state.$logTable.empty().append($table);
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
    try {
        (rows || []).forEach((r) => {
            if (r && typeof r === 'object' && r.hasOwnProperty(key)) {
                const v = (r[key] || '').toString().trim();
                if (v && v !== 'null' && v !== 'undefined') {
                    map[v] = (map[v] || 0) + 1;
                }
            }
        });
    } catch (e) {
        // Silently handle errors
    }
    return map;
}

function isDueInDays(dateStr, days) {
    if (!dateStr) return false;
    try {
        const d = new Date(dateStr);
        const now = new Date();
        const lim = new Date(now.getFullYear(), now.getMonth(), now.getDate() + days);
        return d >= now && d <= lim;
    } catch (e) { return false; }
}


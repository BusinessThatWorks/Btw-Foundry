// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Ensure the page is registered before adding event handlers
if (!frappe.pages['floor-production-plan-page']) {
    frappe.pages['floor-production-plan-page'] = {};
}

frappe.pages['floor-production-plan-page'].on_page_load = function (wrapper) {
    console.log('Floor Production Plan Dashboard page loading...');

    // Build page shell
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Floor Production Plan Dashboard',
        single_column: true,
    });

    const state = { page, wrapper, filters: {}, $cards: null, controls: {} };

    // Initialize dashboard components
    initializeDashboard(state);
};

frappe.pages['floor-production-plan-page'].on_page_show = function () {
    console.log('Floor Production Plan Dashboard shown');
    // Initialize charts when page is shown
    if (document.getElementById('departmentChart')) {
        loadChartJS().then(() => {
            initializeCharts();
        });
    }
};

function initializeDashboard(state) {
    // Clear main content
    state.page.main.empty();

    // Create filter bar
    createFilterBar(state);

    // Create content containers
    createContentContainers(state);

    // Set default values
    setDefaultFilters(state);

    // Bind event handlers
    bindEventHandlers(state);

    // Load initial data
    refreshDashboard(state);
}

function createFilterBar(state) {
    // Main filter container
    const $filterBar = $('<div class="production-filters" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:16px;justify-content:space-between;background:#f8f9fa;padding:16px;border-radius:8px;"></div>');

    // Filter controls container
    const $filterControls = $('<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;"></div>');

    // Individual filter wrappers
    const $productionPlanWrap = $('<div style="min-width:300px;"></div>');
    const $itemWrap = $('<div style="min-width:200px;"></div>');
    const $departmentWrap = $('<div style="min-width:200px;"></div>');
    const $statusWrap = $('<div style="min-width:180px;"></div>');
    const $btnWrap = $('<div style="display:flex;align-items:end;gap:8px;"></div>');

    // Assemble filter controls
    $filterControls.append($productionPlanWrap).append($itemWrap).append($departmentWrap).append($statusWrap);
    $filterBar.append($filterControls).append($btnWrap);
    $(state.page.main).append($filterBar);

    // Create filter controls
    createFilterControls(state, $productionPlanWrap, $itemWrap, $departmentWrap, $statusWrap, $btnWrap);
}

function createFilterControls(state, $productionPlanWrap, $itemWrap, $departmentWrap, $statusWrap, $btnWrap) {
    // Production Plan control
    state.controls.production_plan = frappe.ui.form.make_control({
        parent: $productionPlanWrap.get(0),
        df: {
            fieldtype: 'Link',
            label: 'Production Plan',
            fieldname: 'production_plan',
            options: 'Production Plan',
            reqd: 1,
        },
        render_input: true,
    });

    // Item Code control
    state.controls.item_code = frappe.ui.form.make_control({
        parent: $itemWrap.get(0),
        df: {
            fieldtype: 'Link',
            label: 'Item Code',
            fieldname: 'item_code',
            options: 'Item',
            reqd: 0,
        },
        render_input: true,
    });

    // Department control
    state.controls.department = frappe.ui.form.make_control({
        parent: $departmentWrap.get(0),
        df: {
            fieldtype: 'Select',
            label: 'Department',
            fieldname: 'department',
            options: '',
            reqd: 0,
        },
        render_input: true,
    });

    // Status control
    state.controls.status = frappe.ui.form.make_control({
        parent: $statusWrap.get(0),
        df: {
            fieldtype: 'Select',
            label: 'Status',
            fieldname: 'status',
            options: '\nSufficient\nIn Transit\nShortage',
            reqd: 0,
        },
        render_input: true,
    });

    // Load department options
    loadDepartmentOptions(state);

    // Buttons
    const $refreshBtn = $('<button class="btn btn-primary">Refresh</button>');
    const $exportBtn = $('<button class="btn btn-outline-secondary">Export</button>');

    $btnWrap.append($refreshBtn).append($exportBtn);

    // Store button references
    state.controls.refreshBtn = $refreshBtn;
    state.controls.exportBtn = $exportBtn;

    // Apply styling to form controls
    setTimeout(() => {
        $(state.controls.production_plan.$input).css({
            'border': '1px solid #000000',
            'border-radius': '4px',
            'padding': '8px 12px',
            'height': '36px',
            'line-height': '1.4'
        });
        $(state.controls.item_code.$input).css({
            'border': '1px solid #000000',
            'border-radius': '4px',
            'padding': '8px 12px',
            'height': '36px',
            'line-height': '1.4'
        });
        $(state.controls.department.$input).css({
            'border': '1px solid #000000',
            'border-radius': '4px',
            'padding': '8px 12px',
            'height': '36px',
            'line-height': '1.4'
        });
        $(state.controls.status.$input).css({
            'border': '1px solid #000000',
            'border-radius': '4px',
            'padding': '8px 12px',
            'height': '36px',
            'line-height': '1.4'
        });
    }, 100);
}

function createContentContainers(state) {
    // Summary cards container
    state.$cards = $('<div class="number-cards-container" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:16px;"></div>');
    $(state.page.main).append(state.$cards);

    // Charts container
    state.$charts = $('<div class="charts-container" style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px;"></div>');
    $(state.page.main).append(state.$charts);

    // Data table container (placed AFTER charts per user request)
    state.$table = $('<div class="data-table-container" style="background:white;border-radius:8px;padding:20px;box-shadow:0 2px 4px rgba(0,0,0,0.1);"></div>');
    $(state.page.main).append(state.$table);
}

function setDefaultFilters(state) {
    // Set default values if any
    // This will be populated from URL parameters or defaults
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function bindEventHandlers(state) {
    // Create debounced refresh function for this state
    const debouncedRefresh = debounce(() => {
        refreshDashboard(state);
    }, 500);

    // Helper function to bind Link field events
    function bindLinkFieldEvents(control, refreshFn) {
        if (!control) return;

        // Wait for control to be fully initialized
        setTimeout(() => {
            // Handle change event on input
            if (control.$input) {
                $(control.$input).on('change', refreshFn);
            }

            // For Frappe Link fields, find the actual input element
            let $linkInput = null;
            if (control.$wrapper) {
                // Try multiple selectors to find the Link field input
                $linkInput = control.$wrapper.find('input[data-fieldname]').first();
                if (!$linkInput.length) {
                    $linkInput = control.$wrapper.find('input.form-control').first();
                }
                if (!$linkInput.length) {
                    $linkInput = control.$wrapper.find('input').first();
                }
            }

            if ($linkInput && $linkInput.length) {
                // Create a local debounced refresh for this input
                const debouncedInputRefresh = debounce(refreshFn, 500);

                $linkInput.on('change', refreshFn);
                // Listen to blur event (when user selects from dropdown)
                $linkInput.on('blur', function () {
                    setTimeout(refreshFn, 150);
                });
                // Listen to input events for typing - use debounced version
                $linkInput.on('input', function () {
                    debouncedInputRefresh();
                });
            }

            // Listen to wrapper events
            if (control.$wrapper) {
                control.$wrapper.on('change', refreshFn);
            }

            // Override onchange in df if it doesn't exist
            if (control.df && control.df.onchange === undefined) {
                control.df.onchange = function () {
                    refreshFn();
                };
            }

            // Also try to hook into Frappe's link field selection event
            // This uses event delegation on the document to catch dropdown selections
            $(document).on('awesomplete-selectcomplete', `[data-fieldname="${control.df.fieldname}"]`, refreshFn);
        }, 200);
    }

    // Production Plan filter - Link field (auto-refresh)
    bindLinkFieldEvents(state.controls.production_plan, () => refreshDashboard(state));

    // Item Code filter - Link field (auto-refresh)
    bindLinkFieldEvents(state.controls.item_code, () => refreshDashboard(state));

    // Department filter - Select field
    $(state.controls.department.$input).on('change', () => refreshDashboard(state));

    // Status filter - Select field
    $(state.controls.status.$input).on('change', () => refreshDashboard(state));

    // Button events
    state.controls.refreshBtn.on('click', () => refreshDashboard(state));
    state.controls.exportBtn.on('click', () => openExportDialog(state));
}

function refreshDashboard(state) {
    console.log('Refreshing floor production plan dashboard...');

    const filters = getFilters(state);

    if (!filters.production_plan) {
        showError(state, 'Please select a Production Plan');
        return;
    }

    // Show loading state
    state.page.set_indicator('Loading production plan data...', 'blue');

    // Fetch data
    fetchProductionPlanData(filters).then((data) => {
        state.page.clear_indicator();
        renderDashboardData(state, data);
    }).catch((error) => {
        state.page.clear_indicator();
        console.error('Dashboard refresh error:', error);
        showError(state, 'An error occurred while loading data');
    });
}

function getFilters(state) {
    return {
        production_plan: state.controls.production_plan.get_value(),
        item_code: state.controls.item_code.get_value(),
        department: state.controls.department.get_value(),
        status: state.controls.status.get_value()
    };
}

function fetchProductionPlanData(filters) {
    return new Promise((resolve, reject) => {
        // Fetch report data and total_planned_qty in parallel
        const reportPromise = new Promise((res, rej) => {
            frappe.call({
                method: 'frappe.desk.query_report.run',
                args: {
                    report_name: 'Production Plan Report',
                    filters: filters,
                    ignore_prepared_report: 1,
                },
                callback: (r) => {
                    if (r.message && r.message.result) {
                        res({ data: r.message.result, columns: r.message.columns || [] });
                    } else {
                        res({ data: [], columns: [] });
                    }
                },
                error: rej
            });
        });

        const plannedQtyPromise = new Promise((res) => {
            if (!filters.production_plan) {
                res(0);
                return;
            }
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Production Plan',
                    fieldname: 'total_planned_qty',
                    filters: { name: filters.production_plan }
                },
                callback: (r) => {
                    const v = r && r.message ? (r.message.total_planned_qty || 0) : 0;
                    res(v);
                },
                error: () => res(0)
            });
        });

        Promise.all([reportPromise, plannedQtyPromise])
            .then(([report, totalPlannedQty]) => {
                // Filter data based on status if provided
                let filteredData = report.data;
                if (filters.status) {
                    filteredData = filterDataByStatus(report.data, filters.status);
                }

                const summary = calculateSummaryStats(filteredData, { totalPlannedQty });
                resolve({
                    summary,
                    raw_data: filteredData,
                    columns: report.columns
                });
            })
            .catch(reject);
    });
}

function filterDataByStatus(data, status) {
    if (!status || !data) return data;

    return data.filter(row => {
        const actual = row.actual_qty || 0;
        const required = row.required_bom_qty || 0;
        const combined = row.combined_stock || 0;

        let rowStatus;
        if (actual >= required) {
            rowStatus = 'Sufficient';
        } else if (combined >= required) {
            rowStatus = 'In Transit';
        } else {
            rowStatus = 'Shortage';
        }

        return rowStatus === status;
    });
}

function calculateSummaryStats(data, extras) {
    if (!data || data.length === 0) {
        return [];
    }

    // Calculate totals
    const totalItems = data.length;
    const totalActualQty = data.reduce((sum, row) => sum + (row.actual_qty || 0), 0);
    const totalRequiredQty = data.reduce((sum, row) => sum + (row.required_bom_qty || 0), 0);
    const totalOpenIndent = data.reduce((sum, row) => sum + (row.open_indent || 0), 0);
    const totalOpenPO = data.reduce((sum, row) => sum + (row.open_po || 0), 0);
    const totalCombinedStock = data.reduce((sum, row) => sum + (row.combined_stock || 0), 0);

    // Calculate shortage items
    const shortageItems = data.filter(row => (row.actual_qty || 0) < (row.required_bom_qty || 0));
    const shortageCount = shortageItems.length;

    // Calculate departments
    const departments = [...new Set(data.map(row => row.custom_department).filter(dept => dept))];
    const departmentCount = departments.length;

    const cards = [
        {
            value: totalItems,
            label: 'Total Raw Material Used',
            datatype: 'Int',
            indicator: 'Blue',
            description: 'Total number of raw materials in production plan'
        },
        {
            value: totalActualQty,
            label: 'Total Actual Qty',
            datatype: 'Float',
            indicator: 'Green',
            description: 'Total actual quantity available',
            precision: 2
        },
        {
            value: totalRequiredQty,
            label: 'Total Required Qty',
            datatype: 'Float',
            indicator: 'Orange',
            description: 'Total required quantity for production',
            precision: 2
        },
        {
            value: shortageCount,
            label: 'Shortage Items',
            datatype: 'Int',
            indicator: 'Red',
            description: 'Items with insufficient quantity'
        },
        {
            value: totalOpenIndent,
            label: 'Total Open Indent',
            datatype: 'Float',
            indicator: 'Purple',
            description: 'Total quantity in open material requests',
            precision: 2
        },
        {
            value: totalOpenPO,
            label: 'Total Open PO',
            datatype: 'Float',
            indicator: 'Teal',
            description: 'Total quantity in open purchase orders',
            precision: 2
        },
        {
            value: totalCombinedStock,
            label: 'Total Combined Stock',
            datatype: 'Float',
            indicator: 'Black',
            description: 'Total available stock (actual + open indent + open PO)',
            precision: 2
        },
        {
            value: departmentCount,
            label: 'Departments',
            datatype: 'Int',
            indicator: 'Brown',
            description: 'Number of departments involved'
        }
    ];

    // Append Total Planned Quantity if available
    const totalPlannedQty = extras && extras.totalPlannedQty ? extras.totalPlannedQty : 0;
    if (totalPlannedQty) {
        cards.unshift({
            value: totalPlannedQty,
            label: 'Total Planned Quantity',
            datatype: 'Float',
            indicator: 'Purple',
            description: 'Total planned quantity from selected Production Plan',
            precision: 2
        });
    }

    return cards;
}

function renderDashboardData(state, data) {
    // Render summary cards
    renderSummaryCards(state, data.summary);

    // Render charts BEFORE table
    renderCharts(state, data.raw_data);

    // Render data table AFTER charts
    renderDataTable(state, data.raw_data, data.columns);
}

function renderSummaryCards(state, summary) {
    state.$cards.empty();

    if (!summary || summary.length === 0) {
        state.$cards.append(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:24px;grid-column:1/-1;">
                <i class="fa fa-info-circle" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>No summary data available</div>
            </div>
        `);
        return;
    }

    // Hide unwanted number cards
    const hiddenLabels = new Set([
        'Total Actual Qty',
        'Total Required Qty',
        'Total Open Indent',
        'Total Open PO',
        'Total Combined Stock'
    ]);

    const visibleCards = summary.filter(card => !hiddenLabels.has(card.label));

    if (visibleCards.length === 0) {
        return; // nothing to render
    }

    visibleCards.forEach((card) => {
        const $card = createCard(card);
        state.$cards.append($card);
    });
}

function createCard(card) {
    const indicator = (card.indicator || 'blue').toString().toLowerCase();

    // Format value based on datatype and precision
    let value;
    if (card.datatype === 'Int') {
        value = format_number(card.value || 0, null, 0);
    } else if (card.datatype === 'Float') {
        const precision = card.precision !== undefined ? card.precision : 2;
        value = format_number(card.value || 0, null, precision);
    } else {
        value = format_number(card.value || 0);
    }

    const prefixedValue = card.prefix ? `${card.prefix} ${value}` : value;
    const description = card.description ? `<div class="card-description" style="font-size:0.85rem;color:#95a5a6;margin-top:4px;">${frappe.utils.escape_html(card.description)}</div>` : '';

    return $(`
        <div class="number-card" style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 4px 12px rgba(0,0,0,0.1);position:relative;overflow:hidden;transition:transform 0.2s ease,box-shadow 0.2s ease;">
            <div class="card-indicator" style="position:absolute;top:0;left:0;right:0;height:4px;background:${getIndicatorColor(indicator)}"></div>
            <div class="card-content" style="text-align:center;">
                <div class="card-value" style="font-size:2.4rem;font-weight:700;color:#2c3e50;margin-bottom:8px;">${prefixedValue}</div>
                <div class="card-label" style="font-size:1rem;color:#7f8c8d;font-weight:500;">${frappe.utils.escape_html(card.label || '')}</div>
                ${description}
            </div>
        </div>
    `);
}

function getIndicatorColor(indicator) {
    const colors = {
        'green': 'linear-gradient(90deg,#27ae60,#229954)',
        'black': 'linear-gradient(90deg,#34495e,#2c3e50)',
        'red': 'linear-gradient(90deg,#e74c3c,#c0392b)',
        'orange': 'linear-gradient(90deg,#f39c12,#e67e22)',
        'purple': 'linear-gradient(90deg,#9b59b6,#8e44ad)',
        'teal': 'linear-gradient(90deg,#1abc9c,#16a085)',
        'brown': 'linear-gradient(90deg,#795548,#6d4c41)',
        'blue': 'linear-gradient(90deg,#3498db,#2980b9)'
    };
    return colors[indicator] || colors.blue;
}

function renderDataTable(state, data, columns) {
    if (!data || data.length === 0) {
        state.$table.html(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:40px;">
                <i class="fa fa-info-circle" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>No data available for selected criteria</div>
            </div>
        `);
        return;
    }

    const tableHtml = `
        <div class="table-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
            <h3 style="margin:0;color:#2c3e50;">Item Details</h3>
            <div class="table-actions">
                <button class="btn btn-sm btn-outline-secondary" onclick="exportTableData()">
                    <i class="fa fa-download"></i> Export
                </button>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-striped table-hover" style="width:100%;border-collapse:collapse;">
                <thead style="background:#f8f9fa;">
                    <tr>
                        <th style="padding:12px;text-align:left;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Item Code</th>
                        <th style="padding:12px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Quantity Requirement</th>
                        <th style="padding:12px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Quantity in Stock</th>
                        <th style="padding:12px;text-align:center;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Status</th>
                        <th style="padding:12px;text-align:left;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Department</th>
                        <th style="padding:12px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Indented but not Ordered</th>
                        <th style="padding:12px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Ordered but not Received</th>
                        <th style="padding:12px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Combined Stock</th>
                        <th style="padding:12px;text-align:center;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(row => renderTableRow(row)).join('')}
                </tbody>
            </table>
        </div>
    `;

    state.$table.html(tableHtml);
}

function renderTableRow(row) {
    const actual = row.actual_qty || 0;
    const required = row.required_bom_qty || 0;
    const combined = row.combined_stock || 0;

    let statusBadge;
    if (actual >= required) {
        statusBadge = `<span class="badge badge-success">Sufficient</span>`;
    } else if (combined >= required) {
        statusBadge = `<span class="badge badge-warning">In Transit</span>`;
    } else {
        statusBadge = `<span class="badge badge-danger">Shortage</span>`;
    }

    return `
        <tr style="border-bottom:1px solid #e9ecef;">
            <td style="padding:12px;border-bottom:1px solid #e9ecef;">
                <a href="/app/item/${row.item_code}" target="_blank" style="color:#007bff;text-decoration:none;font-weight:500;">
                    ${row.item_code || ''}
                </a>
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:right;font-family:monospace;font-weight:500;">
                ${format_number(required, null, 2)}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:right;font-family:monospace;font-weight:500;">
                ${format_number(actual, null, 2)}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:center;">
                ${statusBadge}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;">
                ${row.custom_department || '-'}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:right;font-family:monospace;font-weight:500;">
                ${format_number(row.open_indent || 0, null, 2)}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:right;font-family:monospace;font-weight:500;">
                ${format_number(row.open_po || 0, null, 2)}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:right;font-family:monospace;font-weight:500;">
                ${format_number(combined, null, 2)}
            </td>
            <td style="padding:12px;border-bottom:1px solid #e9ecef;text-align:center;">
                <button class="btn btn-sm btn-outline-primary" onclick="viewItemDetails('${row.item_code}')">
                    <i class="fa fa-eye"></i>
                </button>
            </td>
        </tr>
    `;
}

function renderCharts(state, data) {
    if (!data || data.length === 0) {
        state.$charts.html(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:40px;grid-column:1/-1;">
                <i class="fa fa-chart-bar" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>No data available for charts</div>
            </div>
        `);
        return;
    }

    // Department distribution chart
    const departmentData = calculateDepartmentData(data);
    const departmentChartHtml = `
        <div class="chart-container" style="background:white;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            <h4 style="margin-bottom:20px;color:#2c3e50;">Department Distribution</h4>
            <div style="position:relative;height:250px;width:100%;">
                <canvas id="departmentChart"></canvas>
            </div>
        </div>
    `;

    // Stock status chart - make it compact
    const stockData = calculateStockStatusData(data);
    const stockChartHtml = `
        <div class="chart-container" style="background:white;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            <h4 style="margin-bottom:20px;color:#2c3e50;">Stock Status Overview</h4>
            <div style="position:relative;height:250px;width:100%;">
                <canvas id="stockChart"></canvas>
            </div>
        </div>
    `;

    state.$charts.html(departmentChartHtml + stockChartHtml);

    // Initialize charts after DOM is updated
    setTimeout(() => {
        loadChartJS().then(() => {
            // Add a small delay to ensure DOM is ready
            setTimeout(() => {
                initializeCharts(departmentData, stockData);
            }, 50);
        }).catch((error) => {
            console.warn('Chart.js could not be loaded:', error);
            // Show fallback message
            state.$charts.html(`
                <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:40px;grid-column:1/-1;">
                    <i class="fa fa-chart-bar" style="font-size:2rem;margin-bottom:12px;"></i>
                    <div>Charts require Chart.js library to be loaded</div>
                </div>
            `);
        });
    }, 200);
}

function calculateDepartmentData(data) {
    const departmentCounts = {};
    data.forEach(row => {
        const dept = row.custom_department || 'Unknown';
        departmentCounts[dept] = (departmentCounts[dept] || 0) + 1;
    });

    return {
        labels: Object.keys(departmentCounts),
        data: Object.values(departmentCounts),
        colors: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
    };
}

function calculateStockStatusData(data) {
    let sufficient = 0;
    let inTransit = 0; // previously pending
    let shortage = 0;

    data.forEach(row => {
        const actual = row.actual_qty || 0;
        const required = row.required_bom_qty || 0;
        const combined = row.combined_stock || 0;

        if (actual >= required) {
            sufficient++;
        } else if (combined >= required) {
            inTransit++;
        } else {
            shortage++;
        }
    });

    return {
        labels: ['Sufficient', 'In Transit', 'Shortage'],
        data: [sufficient, inTransit, shortage],
        colors: ['#27ae60', '#f39c12', '#e74c3c']
    };
}

function initializeCharts(departmentData, stockData) {
    // Check if Chart.js is available
    if (!window.Chart) {
        console.warn('Chart.js is not available');
        return;
    }

    console.log('Initializing charts with data:', { departmentData, stockData });

    // Department Chart
    const deptCtx = document.getElementById('departmentChart');
    if (deptCtx && departmentData && departmentData.labels.length > 0) {
        try {
            // Destroy existing chart if it exists
            if (deptCtx.chart) {
                deptCtx.chart.destroy();
            }

            deptCtx.chart = new Chart(deptCtx, {
                type: 'bar',
                data: {
                    labels: departmentData.labels,
                    datasets: [{
                        label: 'Items',
                        data: departmentData.data,
                        backgroundColor: departmentData.colors,
                        borderWidth: 2,
                        borderColor: '#fff',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 1000,
                        easing: 'easeInOutQuart'
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const label = context.label || '';
                                    const value = context.parsed.y;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
            console.log('Department chart created successfully');
        } catch (error) {
            console.error('Error creating department chart:', error);
        }
    } else {
        console.warn('Department chart not created - missing data or element');
    }

    // Stock Status Chart - make it more compact
    const stockCtx = document.getElementById('stockChart');
    if (stockCtx && stockData && stockData.labels.length > 0) {
        try {
            // Destroy existing chart if it exists
            if (stockCtx.chart) {
                stockCtx.chart.destroy();
            }

            stockCtx.chart = new Chart(stockCtx, {
                type: 'bar',
                data: {
                    labels: stockData.labels,
                    datasets: [{
                        label: 'Items',
                        data: stockData.data,
                        backgroundColor: stockData.colors,
                        borderWidth: 2,
                        borderColor: '#fff',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 1000,
                        easing: 'easeInOutQuart'
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const label = context.label || '';
                                    const value = context.parsed.y;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
            console.log('Stock chart created successfully');
        } catch (error) {
            console.error('Error creating stock chart:', error);
        }
    } else {
        console.warn('Stock chart not created - missing data or element');
    }
}

function exportData(state) {
    // Export functionality
    console.log('Exporting data...');

    // Get current data
    const filters = getFilters(state);
    if (!filters.production_plan) {
        frappe.msgprint('Please select a Production Plan first');
        return;
    }

    // Call the report with export
    frappe.call({
        method: 'frappe.desk.query_report.export_query',
        args: {
            report_name: 'Production Plan Report',
            file_format_type: 'Excel',
            filters: filters
        },
        callback: function (r) {
            if (r.message) {
                // Download the file
                window.open(r.message, '_blank');
            } else {
                frappe.msgprint('Export failed. Please try again.');
            }
        },
        error: function (err) {
            console.error('Export error:', err);
            frappe.msgprint('Export failed. Please try again.');
        }
    });
}

function exportTableData() {
    // Export table data
    console.log('Exporting table data...');

    // Get the current table data
    const table = document.querySelector('.table');
    if (!table) {
        frappe.msgprint('No table data to export');
        return;
    }

    // Create CSV content
    let csvContent = '';
    const rows = table.querySelectorAll('tr');

    rows.forEach((row, index) => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => {
            let text = cell.textContent.trim();
            // Remove HTML tags and clean up
            text = text.replace(/"/g, '""');
            return `"${text}"`;
        });
        csvContent += rowData.join(',') + '\n';
    });

    // Create and download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `floor_production_plan_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Open export dialog to choose format
function openExportDialog(state) {
    const d = new frappe.ui.Dialog({
        title: 'Export',
        fields: [
            {
                fieldname: 'format',
                fieldtype: 'Select',
                label: 'Format',
                options: ['PDF', 'Excel', 'CSV'].join('\n'),
                default: 'PDF',
                reqd: 1
            }
        ],
        primary_action_label: 'Download',
        primary_action(values) {
            const fmt = values.format;
            if (fmt === 'PDF') {
                exportAsPDF(state);
            } else if (fmt === 'Excel') {
                exportData(state);
            } else if (fmt === 'CSV') {
                exportTableData();
            }
            d.hide();
        }
    });
    d.show();
}

// Load libs for PDF export
function loadPdfLibs() {
    return new Promise((resolve, reject) => {
        const haveH2C = !!window.html2canvas;
        const haveJSPDF = !!(window.jspdf || window.jsPDF);
        const tasks = [];

        if (!haveH2C) {
            tasks.push(new Promise((res, rej) => {
                const s = document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
                s.onload = () => res();
                s.onerror = () => rej(new Error('html2canvas load failed'));
                document.head.appendChild(s);
            }));
        }

        if (!haveJSPDF) {
            tasks.push(new Promise((res, rej) => {
                const s = document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js';
                s.onload = () => res();
                s.onerror = () => rej(new Error('jsPDF load failed'));
                document.head.appendChild(s);
            }));
        }

        const ensureAutoTable = () => {
            try {
                const jsPDFNS = window.jspdf || window.jsPDF;
                const J = jsPDFNS && (jsPDFNS.jsPDF || jsPDFNS);
                const hasAutoTable = !!(J && J.API && J.API.autoTable);
                if (hasAutoTable) {
                    resolve();
                    return;
                }
            } catch (e) {
                // fallthrough to load plugin
            }

            // Load jsPDF-AutoTable plugin
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/jspdf-autotable@3.8.2/dist/jspdf.plugin.autotable.min.js';
            s.onload = () => resolve();
            s.onerror = () => reject(new Error('jsPDF-AutoTable load failed'));
            document.head.appendChild(s);
        };

        if (tasks.length === 0) {
            // jsPDF may already be present; still ensure autotable
            ensureAutoTable();
        } else {
            Promise.all(tasks).then(() => ensureAutoTable()).catch(reject);
        }
    });
}

// Export colorful PDF of cards + charts
function exportAsPDF(state) {
    const filters = getFilters(state);
    if (!filters.production_plan) {
        frappe.msgprint('Please select a Production Plan first');
        return;
    }

    loadPdfLibs().then(() => {
        const h2c = window.html2canvas;
        const jsPDFNS = window.jspdf || window.jsPDF;
        const jsPDF = jsPDFNS.jsPDF || jsPDFNS;
        // STEP 1: Build a temporary container ONLY for title + filters + cards + charts
        const tempSummary = document.createElement('div');
        tempSummary.style.background = '#ffffff';
        tempSummary.style.padding = '16px';
        tempSummary.style.width = '1000px';
        tempSummary.style.boxSizing = 'border-box';

        const title = document.createElement('div');
        title.style.fontSize = '18px';
        title.style.fontWeight = '700';
        title.style.marginBottom = '12px';
        title.style.color = '#2c3e50';
        title.textContent = 'Floor Production Plan Dashboard — Summary & Charts';
        tempSummary.appendChild(title);

        const filterBarSummary = document.createElement('div');
        filterBarSummary.style.fontSize = '12px';
        filterBarSummary.style.margin = '0 0 12px 0';
        filterBarSummary.style.color = '#576574';
        const filterParts = [];
        if (filters.production_plan) filterParts.push(`Production Plan: ${filters.production_plan}`);
        if (filters.item_code) filterParts.push(`Item: ${filters.item_code}`);
        if (filters.department) filterParts.push(`Department: ${filters.department}`);
        if (filters.status) filterParts.push(`Status: ${filters.status}`);
        filterBarSummary.textContent = `Filters — ${filterParts.join(' | ') || 'None'}`;
        tempSummary.appendChild(filterBarSummary);

        if (state.$cards && state.$cards[0]) {
            const cloneCards = state.$cards[0].cloneNode(true);
            tempSummary.appendChild(cloneCards);
        }

        if (state.$charts && state.$charts[0]) {
            const chartsWrapper = document.createElement('div');
            chartsWrapper.style.display = 'grid';
            chartsWrapper.style.gridTemplateColumns = '1fr 1fr';
            chartsWrapper.style.gap = '20px';
            chartsWrapper.style.marginTop = '16px';

            // Get chart containers with their headings
            const chartContainers = state.$charts[0].querySelectorAll('.chart-container');
            const sourceCanvases = state.$charts[0].querySelectorAll('canvas');

            chartContainers.forEach((container, index) => {
                try {
                    // Get the heading from the container
                    const heading = container.querySelector('h4');
                    const headingText = heading ? heading.textContent : '';

                    // Get the corresponding canvas
                    const canvas = sourceCanvases[index];
                    if (!canvas) return;

                    const img = document.createElement('img');
                    img.src = canvas.toDataURL('image/png');
                    img.style.width = '100%';
                    img.style.height = 'auto';
                    img.style.background = '#ffffff';

                    const card = document.createElement('div');
                    card.style.background = '#ffffff';
                    card.style.borderRadius = '8px';
                    card.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                    card.style.padding = '20px';

                    // Add heading if it exists
                    if (headingText) {
                        const headingElement = document.createElement('div');
                        headingElement.style.fontSize = '16px';
                        headingElement.style.fontWeight = '600';
                        headingElement.style.color = '#2c3e50';
                        headingElement.style.marginBottom = '20px';
                        headingElement.textContent = headingText;
                        card.appendChild(headingElement);
                    }

                    card.appendChild(img);
                    chartsWrapper.appendChild(card);
                } catch (e) {
                    console.error('Error processing chart for PDF:', e);
                }
            });

            if (chartsWrapper.children.length > 0) {
                const chartsTitle = document.createElement('div');
                chartsTitle.textContent = 'Charts';
                chartsTitle.style.margin = '16px 0 8px 0';
                chartsTitle.style.fontWeight = '600';
                chartsTitle.style.color = '#2c3e50';
                tempSummary.appendChild(chartsTitle);
                tempSummary.appendChild(chartsWrapper);
            }
        }

        document.body.appendChild(tempSummary);

        const pdf = new jsPDF('p', 'mm', 'a4');
        const margin = 10;
        const pageWidth = 210 - margin * 2;
        const pageHeight = 297 - margin * 2;

        // Render summary to images (may take multiple pages)
        h2c(tempSummary, { scale: 2, useCORS: true, backgroundColor: '#ffffff', windowWidth: 1000 }).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const imgWidth = pageWidth;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            let heightLeft = imgHeight;
            let position = margin;

            pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;

            while (heightLeft > 0) {
                pdf.addPage();
                position = heightLeft - imgHeight + margin;
                pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }

            // Compute startY on the last page so table can begin on same page if space remains
            const usedOnLastPage = imgHeight % pageHeight; // visible height on last page
            let tableStartY = usedOnLastPage === 0 ? margin : margin + usedOnLastPage + 6; // small gap
            // If not enough room for table header, bump to new page
            if (tableStartY > (margin + pageHeight - 20)) {
                pdf.addPage();
                tableStartY = margin;
            }

            // Clean up the temp summary container
            document.body.removeChild(tempSummary);

            // STEP 2: Append the data table using jsPDF-AutoTable to avoid row breaks
            try {
                const tableRoot = state.$table && state.$table[0] ? state.$table[0] : null;
                const domTable = tableRoot ? tableRoot.querySelector('table') : null;
                if (!domTable) {
                    pdf.save(`floor_production_plan_${filters.production_plan}_summary.pdf`);
                    return;
                }

                const headerTexts = Array.from(domTable.querySelectorAll('thead th')).map(th => th.textContent.trim());
                // Drop the last column (Actions) if present
                const columnCount = Math.max(0, headerTexts.length - 1);
                const head = [headerTexts.slice(0, columnCount)];

                const body = Array.from(domTable.querySelectorAll('tbody tr')).map(tr => {
                    const cells = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
                    return cells.slice(0, columnCount);
                });

                // Determine index of Status column in the exported set
                const statusColIndex = head[0].findIndex(h => h.toLowerCase() === 'status');

                pdf.autoTable({
                    head,
                    body,
                    startY: tableStartY,
                    margin: { left: margin, right: margin },
                    theme: 'grid',
                    styles: { fontSize: 8, cellPadding: 2 },
                    headStyles: { fillColor: [248, 249, 250], textColor: 44 },
                    rowPageBreak: 'avoid',
                    didParseCell: (data) => {
                        if (data.section === 'body') {
                            // Zebra striping for readability (skip Status col so its color dominates)
                            if (data.row.index % 2 === 0 && data.column.index !== statusColIndex) {
                                data.cell.styles.fillColor = [251, 252, 253];
                            }

                            if (statusColIndex !== -1 && data.column.index === statusColIndex) {
                                const v = String(data.cell.raw || '').toLowerCase();
                                // Lighter, badge-like colors
                                // Sufficient: light green bg, dark green text
                                if (v.includes('sufficient')) {
                                    data.cell.styles.fillColor = [235, 248, 240]; // #EBF8F0
                                    data.cell.styles.textColor = [27, 94, 32];   // dark green
                                } else if (v.includes('pending') || v.includes('in transit')) {
                                    data.cell.styles.fillColor = [255, 246, 230]; // light orange
                                    data.cell.styles.textColor = [183, 110, 0];   // amber
                                } else if (v.includes('shortage')) {
                                    data.cell.styles.fillColor = [255, 235, 238]; // light red
                                    data.cell.styles.textColor = [183, 28, 28];   // red
                                }
                                data.cell.styles.halign = 'center';
                                data.cell.styles.fontStyle = 'normal';
                                data.cell.styles.cellPadding = 2.5;
                            }
                        }
                    },
                    didDrawPage: (data) => {
                        pdf.setFontSize(12);
                        pdf.setTextColor(44);
                        pdf.text('Item Details', margin, 8 + 2);
                    },
                    margin: { top: 14, left: margin, right: margin }
                });

                pdf.save(`floor_production_plan_${filters.production_plan}_summary.pdf`);
            } catch (e) {
                console.error('AutoTable generation failed:', e);
                pdf.save(`floor_production_plan_${filters.production_plan}_summary.pdf`);
            }
        }).catch((err) => {
            console.error('PDF render failed:', err);
            document.body.removeChild(tempSummary);
            frappe.msgprint('Failed to create PDF. Please try again.');
        });
    }).catch((err) => {
        console.error('PDF libs load error:', err);
        frappe.msgprint('Could not load PDF libraries. Check your network and try again.');
    });
}

function viewItemDetails(itemCode) {
    // Open item details
    frappe.set_route('Form', 'Item', itemCode);
}

function showError(state, message) {
    // Show error message
    state.$cards.empty();
    state.$cards.append(`
        <div class="alert alert-danger" style="background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;padding:16px;border-radius:8px;grid-column:1/-1;">
            <i class="fa fa-exclamation-triangle" style="margin-right:8px;"></i>
            ${frappe.utils.escape_html(message)}
        </div>
    `);
}

// Global functions for HTML onclick handlers
window.refreshData = function () {
    // This will be called from HTML
    console.log('Refresh data called from HTML');
};

window.exportData = function () {
    // This will be called from HTML
    console.log('Export data called from HTML');
};

window.toggleView = function () {
    // This will be called from HTML
    console.log('Toggle view called from HTML');
};

window.viewItemDetails = function (itemCode) {
    // This will be called from HTML
    frappe.set_route('Form', 'Item', itemCode);
};

// Load department options
function loadDepartmentOptions(state) {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Item',
            filters: [
                ['custom_department', 'is', 'set']
            ],
            fields: ['custom_department'],
            group_by: 'custom_department',
            limit_page_length: 0
        },
        callback: function (r) {
            if (r.message) {
                const departments = r.message.map(item => item.custom_department).filter(dept => dept);
                const options = ['', ...departments.sort()];

                // Update the department control options
                state.controls.department.df.options = options.join('\n');
                state.controls.department.refresh();

                console.log('Department options loaded:', departments);
            }
        },
        error: function (err) {
            console.error('Error loading department options:', err);
        }
    });
}

// Chart.js loading function
function loadChartJS() {
    return new Promise((resolve, reject) => {
        // Check if Chart.js is already loaded
        if (window.Chart) {
            resolve();
            return;
        }

        // Try to load Chart.js from CDN
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js';
        script.onload = () => {
            console.log('Chart.js loaded successfully');
            resolve();
        };
        script.onerror = () => {
            console.error('Failed to load Chart.js from CDN');
            reject(new Error('Chart.js could not be loaded'));
        };
        document.head.appendChild(script);
    });
}


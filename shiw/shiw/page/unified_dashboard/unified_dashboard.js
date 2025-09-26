// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Ensure the page is registered before adding event handlers
if (!frappe.pages['unified-dashboard']) {
    frappe.pages['unified-dashboard'] = {};
}

frappe.pages['unified-dashboard'].on_page_load = function (wrapper) {
    console.log('Unified Foundry Dashboard page loading...');

    // Build page shell
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Unified Foundry Dashboard'),
        single_column: true,
    });

    // Initialize dashboard state
    const state = {
        page,
        wrapper,
        filters: {},
        $cards: null,
        $tabs: null,
        controls: {},
        currentTab: 'overview'
    };

    // Initialize dashboard components
    initializeDashboard(state);
};

frappe.pages['unified-dashboard'].on_page_show = function () {
    console.log('Unified Foundry Dashboard shown');
};

function initializeDashboard(state) {
    // Clear main content
    state.page.main.empty();

    // Create filter bar
    createFilterBar(state);

    // Create tabbed interface
    createTabbedInterface(state);

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
    const $filterBar = $('<div class="unified-filters" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:16px;justify-content:space-between;background:#f8f9fa;padding:16px;border-radius:8px;"></div>');

    // Filter controls container
    const $filterControls = $('<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;"></div>');

    // Individual filter wrappers
    const $fromWrap = $('<div style="min-width:200px;"></div>');
    const $toWrap = $('<div style="min-width:200px;"></div>');
    const $furnaceWrap = $('<div style="min-width:220px;"></div>');
    const $batchTypeWrap = $('<div style="min-width:220px;"></div>');
    const $btnWrap = $('<div style="display:flex;align-items:end;gap:8px;"></div>');

    // Assemble filter controls
    $filterControls.append($fromWrap).append($toWrap).append($furnaceWrap).append($batchTypeWrap);
    $filterBar.append($filterControls).append($btnWrap);
    $(state.page.main).append($filterBar);

    // Create filter controls
    createFilterControls(state, $fromWrap, $toWrap, $furnaceWrap, $batchTypeWrap, $btnWrap);
}

function createFilterControls(state, $fromWrap, $toWrap, $furnaceWrap, $batchTypeWrap, $btnWrap) {
    // Date controls
    state.controls.from_date = frappe.ui.form.make_control({
        parent: $fromWrap.get(0),
        df: {
            fieldtype: 'Date',
            label: __('From Date'),
            fieldname: 'from_date',
            reqd: 1,
        },
        render_input: true,
    });

    state.controls.to_date = frappe.ui.form.make_control({
        parent: $toWrap.get(0),
        df: {
            fieldtype: 'Date',
            label: __('To Date'),
            fieldname: 'to_date',
            reqd: 1,
        },
        render_input: true,
    });

    // Furnace control
    state.controls.furnace_no = frappe.ui.form.make_control({
        parent: $furnaceWrap.get(0),
        df: {
            fieldtype: 'Link',
            label: __('Furnace'),
            fieldname: 'furnace_no',
            options: 'Furnace - Master',
            reqd: 0,
        },
        render_input: true,
    });

    // Batch type control
    state.controls.batch_type = frappe.ui.form.make_control({
        parent: $batchTypeWrap.get(0),
        df: {
            fieldtype: 'Select',
            label: __('Mould Type'),
            fieldname: 'batch_type',
            options: [
                'All',
                'Co2 Mould Batch',
                'Green Sand Hand Mould Batch',
                'No-Bake Mould Batch',
                'Jolt Squeeze Mould Batch',
                'HPML Mould Batch'
            ],
            reqd: 0,
        },
        render_input: true,
    });

    // Buttons
    const $refreshBtn = $('<button class="btn btn-primary">' + __('Refresh') + '</button>');

    $btnWrap.append($refreshBtn);

    // Store button references
    state.controls.refreshBtn = $refreshBtn;
}

function createTabbedInterface(state) {
    // Tab container
    const $tabContainer = $('<div class="unified-tabs" style="margin-bottom:20px;"></div>');
    const $tabList = $('<ul class="nav nav-tabs" role="tablist" style="border-bottom:2px solid #dee2e6;"></ul>');

    // Tab content container
    const $tabContent = $('<div class="tab-content" style="margin-top:20px;"></div>');

    // Create tabs
    const tabs = [
        { id: 'overview', label: __('Overview'), icon: 'fa fa-tachometer' },
        { id: 'heat', label: __('Heat Process'), icon: 'fa fa-fire' },
        { id: 'heatloss', label: __('Heat Loss'), icon: 'fa fa-thermometer-empty' },
        { id: 'mould', label: __('Mould Process'), icon: 'fa fa-cube' }
    ];

    tabs.forEach((tab, index) => {
        const $tabItem = $(`
            <li class="nav-item" role="presentation">
                <button class="nav-link ${index === 0 ? 'active' : ''}" 
                        id="${tab.id}-tab" 
                        data-bs-toggle="tab" 
                        data-bs-target="#${tab.id}-content" 
                        type="button" 
                        role="tab" 
                        style="border:none;background:none;padding:12px 20px;color:#6c757d;font-weight:500;cursor:pointer;">
                    <i class="${tab.icon}" style="margin-right:8px;"></i>${tab.label}
                </button>
            </li>
        `);

        const $tabPane = $(`
            <div class="tab-pane fade ${index === 0 ? 'show active' : ''}" 
                 id="${tab.id}-content" 
                 role="tabpanel" 
                 style="min-height:400px;">
            </div>
        `);

        $tabList.append($tabItem);
        $tabContent.append($tabPane);

        // Store references
        if (!state.$tabs) state.$tabs = {};
        state.$tabs[tab.id] = { $item: $tabItem, $content: $tabPane };
    });

    $tabContainer.append($tabList).append($tabContent);
    $(state.page.main).append($tabContainer);
}

function createContentContainers(state) {
    // Create cards containers for each tab
    Object.keys(state.$tabs).forEach(tabId => {
        const $cardsContainer = $('<div class="number-cards-container" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:16px;"></div>');
        state.$tabs[tabId].$content.append($cardsContainer);

        if (!state.$cards) state.$cards = {};
        state.$cards[tabId] = $cardsContainer;

        // Also create table containers if they don't exist
        const $existingTablesContainer = state.$tabs[tabId].$content.find(`#${tabId}-tables`);
        if ($existingTablesContainer.length === 0) {
            const $tablesContainer = $(`
                <div class="detailed-data-section">
                    <h3>${tabId === 'heat' ? __('Heat Details') : tabId === 'heatloss' ? __('Heat Loss Details') : tabId === 'mould' ? __('Mould Details') : __('Overview Details')}</h3>
                    ${tabId === 'heat' ? '<div id="heat-perkg-chart" style="margin-bottom:16px;"></div>' : ''}
                    ${tabId === 'heatloss' ? '<div id="heatloss-reason-chart" style="margin-bottom:16px;"></div>' : ''}
                    <div class="data-tables-container" id="${tabId}-tables"></div>
                </div>
            `);
            state.$tabs[tabId].$content.append($tablesContainer);
        }
    });
}

function setDefaultFilters(state) {
    // Set default date range
    state.controls.from_date.set_value(frappe.datetime.month_start());
    state.controls.to_date.set_value(frappe.datetime.month_end());
    state.controls.batch_type.set_value('All');
}

function bindEventHandlers(state) {
    // Filter change events
    $(state.controls.from_date.$input).on('change', () => refreshDashboard(state));
    $(state.controls.to_date.$input).on('change', () => refreshDashboard(state));
    $(state.controls.furnace_no.$input).on('change', () => refreshDashboard(state));
    $(state.controls.batch_type.$input).on('change', () => refreshDashboard(state));

    // Button events
    state.controls.refreshBtn.on('click', () => refreshDashboard(state));

    // Tab change events
    Object.keys(state.$tabs).forEach(tabId => {
        state.$tabs[tabId].$item.find('button').on('click', () => {
            state.currentTab = tabId;
            updateTabStyles(state);

            // Show/hide tab content
            $('.tab-pane').removeClass('show active');
            $(`#${tabId}-content`).addClass('show active');

            // Update tab buttons
            $('.nav-link').removeClass('active');
            $(`#${tabId}-tab`).addClass('active');

            // Trigger refresh for the current tab
            refreshDashboard(state);
        });
    });
}

function updateTabStyles(state) {
    // Update active tab styling
    Object.keys(state.$tabs).forEach(tabId => {
        const $button = state.$tabs[tabId].$item.find('button');
        if (tabId === state.currentTab) {
            $button.addClass('active').css({
                'color': '#007bff',
                'border-bottom': '2px solid #007bff'
            });
        } else {
            $button.removeClass('active').css({
                'color': '#6c757d',
                'border-bottom': 'none'
            });
        }
    });
}

function refreshDashboard(state) {
    console.log('Refreshing unified dashboard...');

    const filters = getFilters(state);

    if (!filters.from_date || !filters.to_date) {
        showError(state, __('Please select both From Date and To Date'));
        return;
    }

    // Show loading state
    state.page.set_indicator(__('Loading dashboard data...'), 'blue');

    // Fetch data for each section
    Promise.all([
        fetchHeatData(filters),
        fetchHeatLossData(filters),
        fetchMouldData(filters)
    ]).then(([heatData, heatLossData, mouldData]) => {
        state.page.clear_indicator();

        // Create overview data
        const overviewData = createOverviewData(heatData, mouldData);

        // Render all sections
        renderDashboardData(state, {
            overview: {
                ...overviewData,
                raw_data: {
                    heat: heatData.raw_data || [],
                    mould: mouldData.raw_data || []
                }
            },
            heat: heatData,
            heatloss: heatLossData,
            mould: mouldData
        });
    }).catch((error) => {
        state.page.clear_indicator();
        console.error('Dashboard refresh error:', error);
        showError(state, __('An error occurred while loading data'));
    });
}

function fetchHeatData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Number card Heat report',
                filters: filters,
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.report_summary) {
                    resolve({
                        summary: r.message.report_summary,
                        raw_data: r.message.result || []
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function fetchHeatLossData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Number Card Heat Loss report',
                filters: filters,
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                const base = { summary: [], raw_data: [], reasons: [] };
                if (r.message) {
                    base.summary = r.message.report_summary || [];
                    base.raw_data = r.message.result || [];
                }
                // If summary missing, compute averages from raw_data so cards still render
                if (!base.summary || base.summary.length === 0) {
                    const rows = base.raw_data || [];
                    const n = rows.length;
                    let sum_target = 0, sum_ach_liq = 0, sum_ach_pct = 0, sum_loss_liq = 0;
                    rows.forEach(row => {
                        sum_target += Number(row.target_liquid_metal || 0);
                        sum_ach_liq += Number(row.achieved_liquid_metal || 0);
                        sum_ach_pct += Number(row.achieved || 0);
                        sum_loss_liq += Number(row.loss_liquid_metal || 0);
                    });
                    const avg = (sum, d) => d > 0 ? (sum / d) : 0;
                    base.summary = [
                        { value: avg(sum_target, n), label: __('Target Liquid Metal (Avg)'), datatype: 'Float', precision: 2, indicator: 'Blue' },
                        { value: avg(sum_ach_liq, n), label: __('Achieved Liquid Metal (Avg)'), datatype: 'Float', precision: 2, indicator: 'Green' },
                        { value: avg(sum_ach_pct, n), label: __('% Achieved (Avg)'), datatype: 'Float', precision: 2, indicator: 'Teal' },
                        { value: avg(sum_loss_liq, n), label: __('Loss Liquid Metal (Avg)'), datatype: 'Float', precision: 2, indicator: 'Orange' }
                    ];
                }
                // Fetch reasons table rows
                frappe.call({
                    method: 'shiw.shiw.page.unified_dashboard.unified_dashboard.get_heat_loss_reasons',
                    args: { filters: filters },
                    callback: (reasonsRes) => {
                        base.reasons = reasonsRes.message || [];
                        resolve(base);
                    },
                    error: () => resolve(base)
                });
            },
            error: reject
        });
    });
}

function fetchMouldData(filters) {
    return new Promise((resolve, reject) => {
        // Prepare mould-specific filters
        const mouldFilters = {
            from_date: filters.from_date,
            to_date: filters.to_date
        };

        // Add batch type filter if specified
        if (filters.batch_type && filters.batch_type !== 'All') {
            mouldFilters.doctype_name = filters.batch_type;
        }

        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'Number Card Mould report',
                filters: mouldFilters,
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.report_summary) {
                    resolve({
                        summary: r.message.report_summary,
                        raw_data: r.message.result || []
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function createOverviewData(heatData, mouldData) {
    const heatSummary = heatData.summary || [];
    const mouldSummary = mouldData.summary || [];

    // Extract key metrics
    const totalHeats = findCardValue(heatSummary, 'Total Number of Heat') || 0;
    const totalChargeMix = findCardValue(heatSummary, 'Total Charge Mix') || 0;
    const liquidBalance = findCardValue(heatSummary, 'Liquid Balance') || 0;
    const burningLossPct = findCardValue(heatSummary, 'Burning Loss') || 0;

    const totalBatches = findCardValue(mouldSummary, 'Total Number of Batches') || 0;
    const totalCastWeight = findCardValue(mouldSummary, 'Total Cast Weight') || 0;
    const totalBunchWeight = findCardValue(mouldSummary, 'Total Bunch Weight') || 0;
    const avgYield = findCardValue(mouldSummary, 'Average Yield') || 0;
    const totalTooling = findCardValue(mouldSummary, 'Total Number of Tooling') || 0;
    const estimatedFoundryReturn = findCardValue(mouldSummary, 'Estimated Foundry Return') || 0;

    // Calculate combined metrics
    const totalProductionWeight = totalCastWeight + totalBunchWeight;
    const overallEfficiency = totalChargeMix > 0 ? (liquidBalance / totalChargeMix) * 100 : 0;

    return {
        summary: [
            {
                value: overallEfficiency,
                label: __('Overall Efficiency (%)'),
                datatype: 'Float',
                precision: 2,
                indicator: 'Green',
                description: __('Liquid balance efficiency')
            },
            {
                value: burningLossPct,
                label: __('Overall Burning Loss (%)'),
                datatype: 'Float',
                precision: 2,
                indicator: 'Orange',
                description: __('Heat process burning loss')
            },
            {
                value: estimatedFoundryReturn,
                label: __('Estimated Foundry Return'),
                datatype: 'Float',
                precision: 2,
                indicator: 'Purple',
                description: __('')
            },
            {
                value: avgYield,
                label: __('Average Mould Yield'),
                datatype: 'Float',
                precision: 2,
                indicator: 'Teal',
                description: __('Average yield across all mould types')
            },
            {
                value: totalTooling,
                label: __('Total Tooling Used'),
                datatype: 'Int',
                indicator: 'Brown',
                description: __('Total tooling across all mould batches')
            }
        ],
        metrics: {
            total_heats: totalHeats,
            total_batches: totalBatches,
            total_production_weight: totalProductionWeight,
            overall_efficiency: overallEfficiency,
            burning_loss_pct: burningLossPct,
            avg_yield: avgYield
        }
    };
}

function findCardValue(summary, labelContains) {
    const card = summary.find(card => card.label && card.label.includes(labelContains));
    return card ? card.value : 0;
}

function getFilters(state) {
    return {
        from_date: state.controls.from_date.get_value(),
        to_date: state.controls.to_date.get_value(),
        furnace_no: state.controls.furnace_no.get_value(),
        batch_type: state.controls.batch_type.get_value()
    };
}

function renderDashboardData(state, data) {
    // Render data for each tab
    renderTabData(state, 'overview', data.overview);
    renderTabData(state, 'heat', data.heat);
    renderTabData(state, 'heatloss', data.heatloss);
    renderTabData(state, 'mould', data.mould);
}

function renderTabData(state, tabId, tabData) {
    const $cardsContainer = state.$cards[tabId];
    const $tablesContainer = $(`#${tabId}-tables`);

    // Clear containers
    $cardsContainer.empty();
    $tablesContainer.empty();

    const hasSummary = tabData && tabData.summary && tabData.summary.length > 0;
    const hasRaw = tabData && tabData.raw_data && tabData.raw_data.length > 0;
    const hasReasons = tabId === 'heatloss' && tabData && tabData.reasons && tabData.reasons.length > 0;

    if (!hasSummary && !hasRaw && !hasReasons) {
        $cardsContainer.append(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:24px;grid-column:1/-1;">
                <i class="fa fa-info-circle" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>${__('No data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    // Render cards
    (tabData.summary || []).forEach((card) => {
        const $card = createCard(card);
        $cardsContainer.append($card);
    });

    // If heat tab, append cards for Foundry Return Existing and Liquid Metal Pig if not present
    if (tabId === 'heat') {
        const hasReturnCard = (tabData.summary || []).some(c => (c.label || '').includes('Foundry Return Existing'));
        const hasPigCard = (tabData.summary || []).some(c => (c.label || '').includes('Liquid Metal Pig'));

        // Compute totals from raw_data to ensure number cards are present
        if (!hasReturnCard || !hasPigCard) {
            let totalReturnExisting = 0;
            let totalLiquidMetalPig = 0;
            (tabData.raw_data || []).forEach(row => {
                totalReturnExisting += Number(row.foundry_return_existing || 0);
                totalLiquidMetalPig += Number(row.liquid_metal_pig || 0);
            });

            if (!hasReturnCard) {
                $cardsContainer.append(createCard({
                    value: totalReturnExisting,
                    label: __('Foundry Return Existing'),
                    datatype: 'Float',
                    precision: 2,
                    indicator: 'Purple'
                }));
            }
            if (!hasPigCard) {
                $cardsContainer.append(createCard({
                    value: totalLiquidMetalPig,
                    label: __('Liquid Metal Pig'),
                    datatype: 'Float',
                    precision: 2,
                    indicator: 'Teal'
                }));
            }
        }
    }

    // Render chart for heat tab
    if (tabId === 'heat') {
        renderPerKgCostChart(tabData.raw_data || []);
    }
    if (tabId === 'heatloss') {
        renderHeatLossReasonChart(tabData.reasons || []);
    }

    // Render detailed tables
    if (tabData.raw_data && tabData.raw_data.length > 0) {
        renderDetailedTables($tablesContainer, tabId, tabData.raw_data);
    }
    if (tabId === 'heatloss' && tabData.reasons && tabData.reasons.length > 0) {
        renderHeatLossTable($tablesContainer, tabData);
    }
}

function renderDetailedTables($container, tabId, rawData) {
    if (tabId === 'heat') {
        renderHeatTable($container, rawData);
    } else if (tabId === 'mould') {
        renderMouldTable($container, rawData);
    } else if (tabId === 'heatloss') {
        // handled separately to include reasons
    } else if (tabId === 'overview') {
        renderOverviewTables($container, rawData);
    }
}

function renderHeatLossTable($container, heatLossData) {
    const reasons = heatLossData.reasons || [];
    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Reasons For Heat Loss')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Date')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Reason')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Weight (Kg)')}</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    `);

    const $tbody = $table.find('tbody');
    reasons.forEach(r => {
        const dateStr = r.date ? frappe.datetime.str_to_user(r.date) : '';
        const $tr = $(`
            <tr style="border-bottom: 1px solid #e9ecef;">
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left; white-space: nowrap;">${dateStr}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.utils.escape_html(r.reason_for_heat_loss || '')}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(r.weight_in_kg || 0, { fieldtype: 'Float', precision: 2 })}</td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderHeatLossReasonChart(reasonsData) {
    const container = document.getElementById('heatloss-reason-chart');
    if (!container) return;
    container.innerHTML = '';

    if (!reasonsData || reasonsData.length === 0) {
        container.innerHTML = `<div class="no-data-message" style="padding:12px;">${__('No data for chart')}</div>`;
        return;
    }

    // Aggregate weight by reason across selected date range
    const reasonTotals = {};
    reasonsData.forEach(r => {
        const reason = r.reason_for_heat_loss || __('Unknown');
        const wt = Number(r.weight_in_kg || 0);
        reasonTotals[reason] = (reasonTotals[reason] || 0) + wt;
    });

    const labels = Object.keys(reasonTotals);
    const values = labels.map(l => reasonTotals[l]);

    new frappe.Chart(container, {
        title: __('Heat Loss by Reason'),
        data: {
            labels: labels,
            datasets: [
                { name: __('Weight (Kg)'), type: 'bar', values: values }
            ]
        },
        type: 'bar',
        height: 240,
        colors: ['#e67e22'],
        axisOptions: { xAxisMode: 'tick', yAxisMode: 'span' },
        tooltipOptions: {
            formatTooltipX: d => d,
            formatTooltipY: d => frappe.format(d, { fieldtype: 'Float', precision: 2 })
        }
    });
}

function renderHeatTable($container, heatData) {
    if (!heatData || heatData.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No heat data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Heat Entries')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Heat Entry')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Grade')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Furnace No')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Total Charge Mix (Kg)')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Liquid Balance')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Foundry Return Existing')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Liquid Metal Pig')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Per Kg Cost (₹)')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Burning Loss (%)')}</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
    `);

    const $tbody = $table.find('tbody');

    heatData.forEach((row) => {
        let burningLossPct = 0;
        if (row.total_charge_mix_in_kg > 0 && row.liquid_balence > 0) {
            burningLossPct = ((row.total_charge_mix_in_kg - row.liquid_balence) / row.total_charge_mix_in_kg * 100);
        } else if (row.liquid_balence === 0) {
            burningLossPct = 0; // When liquid balance is 0, burning loss should be 0%
        }

        const $tr = $(`
            <tr style="border-bottom: 1px solid #e9ecef;">
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/heat/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.material_grade || ''}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.furnace_no || ''}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.total_charge_mix_in_kg || 0, { fieldtype: 'Float', precision: 2 })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.liquid_balence || 0, { fieldtype: 'Float', precision: 2 })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.foundry_return_existing || 0, { fieldtype: 'Float', precision: 2 })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.liquid_metal_pig || 0, { fieldtype: 'Float', precision: 2 })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.per_kg_cost || 0, { fieldtype: 'Float', precision: 2 })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right; white-space: nowrap;">${burningLossPct.toFixed(2)}%</td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderMouldTable($container, mouldData) {
    if (!mouldData || mouldData.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No mould data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    // Group data by doctype
    const groupedData = {};
    mouldData.forEach((row) => {
        const doctype = row.doctype_name || 'Unknown';
        if (!groupedData[doctype]) {
            groupedData[doctype] = [];
        }
        groupedData[doctype].push(row);
    });

    Object.keys(groupedData).forEach((doctype) => {
        const data = groupedData[doctype];
        const $table = $(`
            <div class="data-table" style="width: 100%; margin-bottom: 30px;">
                <h4>${__(doctype)}</h4>
                <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                    <thead>
                        <tr>
                            <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Batch Name')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Total Cast Weight')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Total Bunch Weight')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Tooling Count')}</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        `);

        const $tbody = $table.find('tbody');

        data.forEach((row) => {
            const $tr = $(`
                <tr style="border-bottom: 1px solid #e9ecef;">
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/${doctype.toLowerCase().replace(/\s+/g, '-')}/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.total_cast_weight || 0, { fieldtype: 'Float', precision: 2 })}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.total_bunch_weight || 0, { fieldtype: 'Float', precision: 2 })}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${row.no_of_tooling || 0}</td>
                </tr>
            `);
            $tbody.append($tr);
        });

        $container.append($table);
    });
}

function renderOverviewTables($container, overviewData) {
    // For overview, we'll show a summary of both heat and mould data
    if (overviewData.heat && overviewData.heat.length > 0) {
        const $heatTable = $(`
            <div class="data-table" style="width: 100%; margin-bottom: 30px;">
                <h4>${__('Recent Heat Entries')}</h4>
                <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                    <thead>
                        <tr>
                            <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Heat Entry')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Grade')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Furnace No')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Total Charge Mix (Kg)')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Liquid Balance')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Per Kg Cost (₹)')}</th>
                            <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Burning Loss (%)')}</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        `);

        const $heatTbody = $heatTable.find('tbody');

        // Show only first 5 heat entries
        overviewData.heat.slice(0, 5).forEach((row) => {
            let burningLossPct = 0;
            if (row.total_charge_mix_in_kg > 0 && row.liquid_balence > 0) {
                burningLossPct = ((row.total_charge_mix_in_kg - row.liquid_balence) / row.total_charge_mix_in_kg * 100);
            } else if (row.liquid_balence === 0) {
                burningLossPct = 0; // When liquid balance is 0, burning loss should be 0%
            }

            const $tr = $(`
                <tr style="border-bottom: 1px solid #e9ecef;">
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/heat/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.material_grade || ''}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.furnace_no || ''}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.total_charge_mix_in_kg || 0, { fieldtype: 'Float', precision: 2 })}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.liquid_balence || 0, { fieldtype: 'Float', precision: 2 })}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.per_kg_cost || 0, { fieldtype: 'Float', precision: 2 })}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right; white-space: nowrap;">${burningLossPct.toFixed(2)}%</td>
                </tr>
            `);
            $heatTbody.append($tr);
        });

        $container.append($heatTable);
    }

    if (overviewData.mould && overviewData.mould.length > 0) {
        const $mouldTable = $(`
            <div class="data-table">
                <h4>${__('Recent Mould Batches')}</h4>
                <table>
                    <thead>
                        <tr>
                            <th>${__('Batch Name')}</th>
                            <th>${__('Batch Type')}</th>
                            <th>${__('Total Cast Weight')}</th>
                            <th>${__('Total Bunch Weight')}</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        `);

        const $mouldTbody = $mouldTable.find('tbody');

        // Show only first 5 mould entries
        overviewData.mould.slice(0, 5).forEach((row) => {
            const $tr = $(`
                <tr>
                    <td><a href="/app/${(row.doctype_name || 'mould-batch').toLowerCase().replace(/\s+/g, '-')}/${row.name}" class="link-cell">${row.name}</a></td>
                    <td>${__(row.doctype_name || 'Unknown')}</td>
                    <td>${format_number(row.total_cast_weight || 0, null, 3)}</td>
                    <td>${format_number(row.total_bunch_weight || 0, null, 3)}</td>
                </tr>
            `);
            $mouldTbody.append($tr);
        });

        $container.append($mouldTable);
    }
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

    const description = card.description ? `<div class="card-description" style="font-size:0.85rem;color:#95a5a6;margin-top:4px;">${frappe.utils.escape_html(card.description)}</div>` : '';

    return $(`
        <div class="number-card" style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 4px 12px rgba(0,0,0,0.1);position:relative;overflow:hidden;transition:transform 0.2s ease,box-shadow 0.2s ease;">
            <div class="card-indicator" style="position:absolute;top:0;left:0;right:0;height:4px;background:${getIndicatorColor(indicator)}"></div>
            <div class="card-content" style="text-align:center;">
                <div class="card-value" style="font-size:2.4rem;font-weight:700;color:#2c3e50;margin-bottom:8px;">${value}</div>
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

function showError(state, message) {
    // Show error in current tab
    const $cardsContainer = state.$cards[state.currentTab];
    $cardsContainer.empty();
    $cardsContainer.append(`
        <div class="alert alert-danger" style="background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;padding:16px;border-radius:8px;grid-column:1/-1;">
            <i class="fa fa-exclamation-triangle" style="margin-right:8px;"></i>
            ${frappe.utils.escape_html(message)}
        </div>
    `);
}

function renderPerKgCostChart(heatData) {
    const container = document.getElementById('heat-perkg-chart');
    if (!container) return;

    // Clear previous chart
    container.innerHTML = '';

    if (!heatData || heatData.length === 0) {
        container.innerHTML = `<div class="no-data-message" style="padding:12px;">${__('No data for chart')}</div>`;
        return;
    }

    // Build labels (dates) and values (per kg cost)
    const labels = [];
    const values = [];

    heatData.forEach(row => {
        const dateStr = row.date ? frappe.datetime.str_to_user(row.date) : '';
        labels.push(dateStr || row.name);
        const perKg = typeof row.per_kg_cost === 'number' ? row.per_kg_cost : 0;
        values.push(perKg);
    });

    // Create chart
    const chart = new frappe.Chart(container, {
        title: __('Per Kg Cost Trend'),
        data: {
            labels: labels,
            datasets: [
                {
                    name: __('Per Kg Cost'),
                    type: 'line',
                    values: values
                }
            ]
        },
        type: 'axis-mixed',
        height: 240,
        colors: ['#1f77b4'],
        axisOptions: {
            xAxisMode: 'tick',
            yAxisMode: 'span',
            xIsSeries: true
        },
        lineOptions: {
            regionFill: 1,
            hideDots: 0
        },
        tooltipOptions: {
            formatTooltipX: d => d,
            formatTooltipY: d => frappe.format(d, { fieldtype: 'Currency' })
        }
    });
}


// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Ensure the page is registered before adding event handlers
if (!frappe.pages['procurement-tracker-dashboard']) {
    frappe.pages['procurement-tracker-dashboard'] = {};
}

frappe.pages['procurement-tracker-dashboard'].on_page_load = function (wrapper) {
    console.log('Procurement Tracker Dashboard page loading...');

    // Build page shell
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Procurement Tracker Dashboard'),
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

frappe.pages['procurement-tracker-dashboard'].on_page_show = function () {
    console.log('Procurement Tracker Dashboard shown');
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
    const $filterBar = $('<div class="procurement-filters" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:16px;justify-content:space-between;background:#f8f9fa;padding:16px;border-radius:8px;"></div>');

    // Filter controls container
    const $filterControls = $('<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;"></div>');

    // Individual filter wrappers
    const $fromWrap = $('<div style="min-width:200px;"></div>');
    const $toWrap = $('<div style="min-width:200px;"></div>');
    const $supplierWrap = $('<div style="min-width:220px;"></div>');
    const $wfStatusWrap = $('<div style="min-width:220px;"></div>');
    const $btnWrap = $('<div style="display:flex;align-items:end;gap:8px;"></div>');

    // Assemble filter controls
    $filterControls.append($fromWrap).append($toWrap).append($supplierWrap).append($wfStatusWrap);
    $filterBar.append($filterControls).append($btnWrap);
    $(state.page.main).append($filterBar);

    // Create filter controls
    createFilterControls(state, $fromWrap, $toWrap, $supplierWrap, $wfStatusWrap, $btnWrap);
}

function createFilterControls(state, $fromWrap, $toWrap, $supplierWrap, $wfStatusWrap, $btnWrap) {
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

    // Supplier control
    state.controls.supplier = frappe.ui.form.make_control({
        parent: $supplierWrap.get(0),
        df: {
            fieldtype: 'Link',
            label: __('Supplier'),
            fieldname: 'supplier',
            options: 'Supplier',
            reqd: 0,
        },
        render_input: true,
    });

    // Global Workflow Status filter
    state.controls.workflow_status = frappe.ui.form.make_control({
        parent: $wfStatusWrap.get(0),
        df: {
            fieldtype: 'Select',
            label: __('Workflow Status'),
            fieldname: 'workflow_status',
            options: ['', 'Draft', 'Waiting For Review', 'Waiting For Approval', 'Approved', 'Rejected', 'Completed', 'Cancelled'],
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
    const $tabContainer = $('<div class="procurement-tabs" style="margin-bottom:20px;"></div>');
    const $tabList = $('<ul class="nav nav-tabs" role="tablist" style="border-bottom:2px solid #dee2e6;"></ul>');

    // Tab content container
    const $tabContent = $('<div class="tab-content" style="margin-top:20px;"></div>');

    // Create tabs
    const tabs = [
        { id: 'overview', label: __('Overview'), icon: 'fa fa-tachometer' },
        { id: 'material_request', label: __('Material Request'), icon: 'fa fa-file-text' },
        { id: 'purchase_order', label: __('Purchase Order'), icon: 'fa fa-shopping-cart' },
        { id: 'purchase_receipt', label: __('Purchase Receipt'), icon: 'fa fa-truck' },
        { id: 'purchase_invoice', label: __('Purchase Invoice'), icon: 'fa fa-file-invoice' }
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

        // Create section-specific filters for non-overview tabs
        if (tabId !== 'overview') {
            createSectionFilters(state, tabId);
        }

        // Create table containers
        const $tablesContainer = $(`
            <div class="detailed-data-section">
                <h3>${getSectionTitle(tabId)}</h3>
                <div class="data-tables-container" id="${tabId}-tables"></div>
            </div>
        `);
        state.$tabs[tabId].$content.append($tablesContainer);
    });
}

function createSectionFilters(state, tabId) {
    const $sectionFilters = $(`
        <div class="section-filters" style="background:#f1f3f4;padding:12px;border-radius:6px;margin-bottom:16px;">
            <div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;">
                <div id="${tabId}-status-filter" style="min-width:180px;"></div>
                <div id="${tabId}-id-filter" style="min-width:180px;"></div>
                <div id="${tabId}-item-filter" style="min-width:200px;"></div>
            </div>
        </div>
    `);

    // Insert before cards container
    state.$tabs[tabId].$content.find('.number-cards-container').before($sectionFilters);

    // Create section-specific filter controls
    createSectionFilterControls(state, tabId);
}

function createSectionFilterControls(state, tabId) {
    // Status filter
    const statusField = getStatusFieldName(tabId);
    const statusOptions = getStatusOptions(tabId);
    state.controls[`${tabId}_status`] = frappe.ui.form.make_control({
        parent: $(`#${tabId}-status-filter`).get(0),
        df: {
            fieldtype: 'Select',
            label: __('Workflow Status'),
            fieldname: `${tabId}_status`,
            options: statusOptions,
            reqd: 0,
        },
        render_input: true,
    });

    // Add border styling to status filter input
    setTimeout(() => {
        $(`#${tabId}-status-filter .form-control`).css({
            'border': '1px solid #ced4da',
            'border-radius': '4px',
            'padding': '6px 12px'
        });
    }, 100);

    // ID filter
    const idField = getIdFieldName(tabId);
    state.controls[`${tabId}_id`] = frappe.ui.form.make_control({
        parent: $(`#${tabId}-id-filter`).get(0),
        df: {
            fieldtype: 'Data',
            label: __('ID'),
            fieldname: `${tabId}_id`,
            reqd: 0,
        },
        render_input: true,
    });

    // Add border styling to ID filter input
    setTimeout(() => {
        $(`#${tabId}-id-filter .form-control`).css({
            'border': '1px solid #ced4da',
            'border-radius': '4px',
            'padding': '6px 12px'
        });
    }, 100);

    // Item name filter
    state.controls[`${tabId}_item_name`] = frappe.ui.form.make_control({
        parent: $(`#${tabId}-item-filter`).get(0),
        df: {
            fieldtype: 'Link',
            options: 'Item',
            label: __('Item'),
            fieldname: `${tabId}_item_name`,
            reqd: 0,
        },
        render_input: true,
    });

    // Add border styling to item filter input
    setTimeout(() => {
        $(`#${tabId}-item-filter .form-control`).css({
            'border': '1px solid #ced4da',
            'border-radius': '4px',
            'padding': '6px 12px'
        });
    }, 100);
}

function getStatusFieldName(tabId) {
    const statusFields = {
        'material_request': 'mr_status',
        'purchase_order': 'po_status',
        'purchase_receipt': 'pr_status',
        'purchase_invoice': 'pi_status'
    };
    return statusFields[tabId] || 'status';
}

function getIdFieldName(tabId) {
    const idFields = {
        'material_request': 'mr_id',
        'purchase_order': 'po_id',
        'purchase_receipt': 'pr_id',
        'purchase_invoice': 'pi_id'
    };
    return idFields[tabId] || 'id';
}

function getSectionTitle(tabId) {
    const titles = {
        'overview': __('Procurement Overview'),
        'material_request': __('Material Request Details'),
        'purchase_order': __('Purchase Order Details'),
        'purchase_receipt': __('Purchase Receipt Details'),
        'purchase_invoice': __('Purchase Invoice Details')
    };
    return titles[tabId] || __('Details');
}

function setDefaultFilters(state) {
    // Set default date range
    state.controls.from_date.set_value(frappe.datetime.month_start());
    state.controls.to_date.set_value(frappe.datetime.month_end());
}

function bindEventHandlers(state) {
    // Main filter change events
    $(state.controls.from_date.$input).on('change', () => refreshDashboard(state));
    $(state.controls.to_date.$input).on('change', () => refreshDashboard(state));
    $(state.controls.supplier.$input).on('change', () => refreshDashboard(state));
    $(state.controls.workflow_status.$input).on('change', () => refreshDashboard(state));

    // Section filter change events
    Object.keys(state.$tabs).forEach(tabId => {
        if (tabId !== 'overview') {
            $(state.controls[`${tabId}_status`].$input).on('change', () => refreshDashboard(state));
            $(state.controls[`${tabId}_id`].$input).on('change', () => refreshDashboard(state));
            $(state.controls[`${tabId}_item_name`].$input).on('change', () => refreshDashboard(state));
        }
    });

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
    console.log('Refreshing procurement dashboard...');

    const filters = getFilters(state);

    if (!filters.from_date || !filters.to_date) {
        showError(state, __('Please select both From Date and To Date'));
        return;
    }

    // Show loading state
    state.page.set_indicator(__('Loading dashboard data...'), 'blue');

    // Fetch data for all sections
    Promise.all([
        fetchProcurementData(filters),
        fetchMaterialRequestData(filters, state),
        fetchPurchaseOrderData(filters, state),
        fetchPurchaseReceiptData(filters, state),
        fetchPurchaseInvoiceData(filters, state)
    ]).then(([procurementData, mrData, poData, prData, piData]) => {
        state.page.clear_indicator();

        // Create overview data
        const overviewData = createProcurementOverviewData(procurementData, mrData, poData, prData, piData);

        // Render all sections
        renderDashboardData(state, {
            overview: overviewData,
            material_request: mrData,
            purchase_order: poData,
            purchase_receipt: prData,
            purchase_invoice: piData
        });
    }).catch((error) => {
        state.page.clear_indicator();
        console.error('Dashboard refresh error:', error);
        showError(state, __('An error occurred while loading data'));
    });
}

function fetchProcurementData(filters) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'New Procurement Tracker',
                filters: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    item_code: filters.item_name || ''
                },
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.result) {
                    resolve(r.message.result || []);
                } else {
                    resolve([]);
                }
            },
            error: reject
        });
    });
}

function fetchMaterialRequestData(filters, state) {
    return new Promise((resolve, reject) => {
        // Use the procurement tracker report to get data with workflow_state
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'New Procurement Tracker',
                filters: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    item_code: filters.item_name || ''
                },
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.result) {
                    let procurementData = r.message.result;

                    // Extract unique Material Requests from procurement data
                    const materialRequests = [];
                    const seenMRs = new Set();

                    procurementData.forEach(row => {
                        if (row.material_request && !seenMRs.has(row.material_request)) {
                            seenMRs.add(row.material_request);
                            materialRequests.push({
                                name: row.material_request,
                                transaction_date: row.indent_date,
                                workflow_state: row.mr_status,
                                status: row.mr_status // Use workflow_state as status for display
                            });
                        }
                    });

                    // Apply additional filters
                    let filteredData = materialRequests;

                    // Apply status filter
                    if (filters.mr_status) {
                        filteredData = filteredData.filter(mr => mr.workflow_state === filters.mr_status);
                    }

                    // Apply global workflow status filter if provided
                    if (filters.workflow_status) {
                        filteredData = filteredData.filter(mr => mr.workflow_state === filters.workflow_status);
                    }

                    // Apply ID filter
                    if (filters.mr_id) {
                        filteredData = filteredData.filter(mr => mr.name.toLowerCase().includes(filters.mr_id.toLowerCase()));
                    }

                    // Apply item filter if specified - filter the original procurement data first
                    if (filters.item_name) {
                        const itemFilteredProcurementData = procurementData.filter(row =>
                            row.item_code === filters.item_name
                        );

                        // Extract unique Material Requests from item-filtered data
                        const itemFilteredMRs = [];
                        const seenItemFilteredMRs = new Set();

                        itemFilteredProcurementData.forEach(row => {
                            if (row.material_request && !seenItemFilteredMRs.has(row.material_request)) {
                                seenItemFilteredMRs.add(row.material_request);
                                itemFilteredMRs.push({
                                    name: row.material_request,
                                    transaction_date: row.indent_date,
                                    workflow_state: row.mr_status,
                                    status: row.mr_status
                                });
                            }
                        });

                        // Apply other filters to item-filtered data
                        filteredData = itemFilteredMRs;
                    }

                    // Create status summary based on workflow_state
                    const statusCounts = {};
                    filteredData.forEach(item => {
                        const status = item.workflow_state || 'Draft';
                        statusCounts[status] = (statusCounts[status] || 0) + 1;
                    });

                    const summary = Object.keys(statusCounts).map(status => ({
                        value: statusCounts[status],
                        label: `${status} Material Requests`,
                        datatype: 'Int',
                        indicator: getStatusIndicator(status),
                        description: `Material requests with ${status} status`
                    }));

                    // Update status options based on actual data
                    updateStatusOptions('material_request', filteredData, state);

                    resolve({
                        summary: summary,
                        raw_data: filteredData
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function filterMaterialRequestsByItemName(materialRequests, itemName) {
    return new Promise((resolve, reject) => {
        if (!itemName) {
            resolve(materialRequests);
            return;
        }

        // Get all material request names
        const mrNames = materialRequests.map(mr => mr.name);

        if (mrNames.length === 0) {
            resolve([]);
            return;
        }

        // Fetch Material Request Items that match the item name
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Material Request Item',
                filters: [
                    ['Material Request Item', 'parent', 'in', mrNames],
                    ['Material Request Item', 'item_name', 'like', `%${itemName}%`]
                ],
                fields: ['parent'],
                limit_page_length: 1000
            },
            callback: (r) => {
                if (r.message) {
                    // Get unique parent names
                    const filteredParentNames = [...new Set(r.message.map(item => item.parent))];

                    // Filter material requests to only include those with matching items
                    const filteredMRs = materialRequests.filter(mr =>
                        filteredParentNames.includes(mr.name)
                    );

                    resolve(filteredMRs);
                } else {
                    resolve([]);
                }
            },
            error: reject
        });
    });
}

function filterPurchaseOrdersByItemName(purchaseOrders, itemName) {
    return new Promise((resolve, reject) => {
        if (!itemName) {
            resolve(purchaseOrders);
            return;
        }

        const poNames = purchaseOrders.map(po => po.name);

        if (poNames.length === 0) {
            resolve([]);
            return;
        }

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Purchase Order Item',
                filters: [
                    ['Purchase Order Item', 'parent', 'in', poNames],
                    ['Purchase Order Item', 'item_name', 'like', `%${itemName}%`]
                ],
                fields: ['parent'],
                limit_page_length: 1000
            },
            callback: (r) => {
                if (r.message) {
                    const filteredParentNames = [...new Set(r.message.map(item => item.parent))];
                    const filteredPOs = purchaseOrders.filter(po =>
                        filteredParentNames.includes(po.name)
                    );
                    resolve(filteredPOs);
                } else {
                    resolve([]);
                }
            },
            error: reject
        });
    });
}

function filterPurchaseReceiptsByItemName(purchaseReceipts, itemName) {
    return new Promise((resolve, reject) => {
        if (!itemName) {
            resolve(purchaseReceipts);
            return;
        }

        const prNames = purchaseReceipts.map(pr => pr.name);

        if (prNames.length === 0) {
            resolve([]);
            return;
        }

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Purchase Receipt Item',
                filters: [
                    ['Purchase Receipt Item', 'parent', 'in', prNames],
                    ['Purchase Receipt Item', 'item_name', 'like', `%${itemName}%`]
                ],
                fields: ['parent'],
                limit_page_length: 1000
            },
            callback: (r) => {
                if (r.message) {
                    const filteredParentNames = [...new Set(r.message.map(item => item.parent))];
                    const filteredPRs = purchaseReceipts.filter(pr =>
                        filteredParentNames.includes(pr.name)
                    );
                    resolve(filteredPRs);
                } else {
                    resolve([]);
                }
            },
            error: reject
        });
    });
}

function filterPurchaseInvoicesByItemName(purchaseInvoices, itemName) {
    return new Promise((resolve, reject) => {
        if (!itemName) {
            resolve(purchaseInvoices);
            return;
        }

        const piNames = purchaseInvoices.map(pi => pi.name);

        if (piNames.length === 0) {
            resolve([]);
            return;
        }

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Purchase Invoice Item',
                filters: [
                    ['Purchase Invoice Item', 'parent', 'in', piNames],
                    ['Purchase Invoice Item', 'item_name', 'like', `%${itemName}%`]
                ],
                fields: ['parent'],
                limit_page_length: 1000
            },
            callback: (r) => {
                if (r.message) {
                    const filteredParentNames = [...new Set(r.message.map(item => item.parent))];
                    const filteredPIs = purchaseInvoices.filter(pi =>
                        filteredParentNames.includes(pi.name)
                    );
                    resolve(filteredPIs);
                } else {
                    resolve([]);
                }
            },
            error: reject
        });
    });
}

function fetchPurchaseOrderData(filters, state) {
    return new Promise((resolve, reject) => {
        // Use the procurement tracker report to get data with workflow_state
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'New Procurement Tracker',
                filters: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    item_code: filters.item_name || ''
                },
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.result) {
                    let procurementData = r.message.result;

                    // Extract unique Purchase Orders from procurement data
                    const purchaseOrders = [];
                    const seenPOs = new Set();

                    procurementData.forEach(row => {
                        if (row.purchase_order && !seenPOs.has(row.purchase_order)) {
                            seenPOs.add(row.purchase_order);
                            purchaseOrders.push({
                                name: row.purchase_order,
                                transaction_date: row.po_date,
                                workflow_state: row.po_status,
                                status: row.po_status, // Use workflow_state as status for display
                                supplier: row.supplier,
                                grand_total: row.po_grand_total
                            });
                        }
                    });

                    // Apply additional filters
                    let filteredData = purchaseOrders;

                    // Apply status filter
                    if (filters.po_status) {
                        filteredData = filteredData.filter(po => po.workflow_state === filters.po_status);
                    }

                    // Apply global workflow status filter if provided
                    if (filters.workflow_status) {
                        filteredData = filteredData.filter(po => po.workflow_state === filters.workflow_status);
                    }

                    // Apply ID filter
                    if (filters.po_id) {
                        filteredData = filteredData.filter(po => po.name.toLowerCase().includes(filters.po_id.toLowerCase()));
                    }

                    // Apply supplier filter if specified
                    if (filters.supplier) {
                        filteredData = filteredData.filter(po => po.supplier === filters.supplier);
                    }

                    // Apply item filter if specified - filter the original procurement data first
                    if (filters.item_name) {
                        const itemFilteredProcurementData = procurementData.filter(row =>
                            row.item_code === filters.item_name
                        );

                        // Extract unique Purchase Orders from item-filtered data
                        const itemFilteredPOs = [];
                        const seenItemFilteredPOs = new Set();

                        itemFilteredProcurementData.forEach(row => {
                            if (row.purchase_order && !seenItemFilteredPOs.has(row.purchase_order)) {
                                seenItemFilteredPOs.add(row.purchase_order);
                                itemFilteredPOs.push({
                                    name: row.purchase_order,
                                    transaction_date: row.po_date,
                                    workflow_state: row.po_status,
                                    status: row.po_status,
                                    supplier: row.supplier,
                                    grand_total: row.po_grand_total
                                });
                            }
                        });

                        // Apply other filters to item-filtered data
                        filteredData = itemFilteredPOs;
                    }

                    // Apply status filter
                    if (filters.po_status) {
                        filteredData = filteredData.filter(po => po.workflow_state === filters.po_status);
                    }

                    // Apply ID filter
                    if (filters.po_id) {
                        filteredData = filteredData.filter(po => po.name.toLowerCase().includes(filters.po_id.toLowerCase()));
                    }

                    // Apply supplier filter
                    if (filters.supplier) {
                        filteredData = filteredData.filter(po => po.supplier === filters.supplier);
                    }

                    // Create status summary based on workflow_state
                    const statusCounts = {};
                    filteredData.forEach(item => {
                        const status = item.workflow_state || 'Draft';
                        statusCounts[status] = (statusCounts[status] || 0) + 1;
                    });

                    const summary = Object.keys(statusCounts).map(status => ({
                        value: statusCounts[status],
                        label: `${status} Purchase Orders`,
                        datatype: 'Int',
                        indicator: getStatusIndicator(status),
                        description: `Purchase orders with ${status} status`
                    }));

                    // Update status options based on actual data
                    updateStatusOptions('purchase_order', procurementData, state);

                    resolve({
                        summary: summary,
                        raw_data: filteredData
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function fetchPurchaseReceiptData(filters, state) {
    return new Promise((resolve, reject) => {
        // Use the procurement tracker report to get data with workflow_state
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'New Procurement Tracker',
                filters: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    item_code: filters.item_name || ''
                },
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.result) {
                    let procurementData = r.message.result;

                    // Extract unique Purchase Receipts from procurement data
                    const purchaseReceipts = [];
                    const seenPRs = new Set();

                    procurementData.forEach(row => {
                        if (row.purchase_receipt && !seenPRs.has(row.purchase_receipt)) {
                            seenPRs.add(row.purchase_receipt);
                            purchaseReceipts.push({
                                name: row.purchase_receipt,
                                posting_date: row.receipt_date,
                                workflow_state: 'Completed', // Purchase Receipts are typically completed when created
                                status: 'Completed', // Use workflow_state as status for display
                                supplier: row.supplier,
                                grand_total: row.pr_grand_total || 0
                            });
                        }
                    });

                    // Apply additional filters
                    let filteredData = purchaseReceipts;

                    // Apply status filter
                    if (filters.pr_status) {
                        filteredData = filteredData.filter(pr => pr.workflow_state === filters.pr_status);
                    }

                    // Apply global workflow status filter if provided
                    if (filters.workflow_status) {
                        filteredData = filteredData.filter(pr => pr.workflow_state === filters.workflow_status);
                    }

                    // Apply ID filter
                    if (filters.pr_id) {
                        filteredData = filteredData.filter(pr => pr.name.toLowerCase().includes(filters.pr_id.toLowerCase()));
                    }

                    // Apply supplier filter if specified
                    if (filters.supplier) {
                        filteredData = filteredData.filter(pr => pr.supplier === filters.supplier);
                    }

                    // Apply item filter if specified - filter the original procurement data first
                    if (filters.item_name) {
                        const itemFilteredProcurementData = procurementData.filter(row =>
                            row.item_code === filters.item_name
                        );

                        // Extract unique Purchase Receipts from item-filtered data
                        const itemFilteredPRs = [];
                        const seenItemFilteredPRs = new Set();

                        itemFilteredProcurementData.forEach(row => {
                            if (row.purchase_receipt && !seenItemFilteredPRs.has(row.purchase_receipt)) {
                                seenItemFilteredPRs.add(row.purchase_receipt);
                                itemFilteredPRs.push({
                                    name: row.purchase_receipt,
                                    posting_date: row.receipt_date,
                                    workflow_state: 'Completed',
                                    status: 'Completed',
                                    supplier: row.supplier,
                                    grand_total: row.pr_grand_total || 0
                                });
                            }
                        });

                        // Apply other filters to item-filtered data
                        filteredData = itemFilteredPRs;
                    }

                    // Apply status filter
                    if (filters.pr_status) {
                        filteredData = filteredData.filter(pr => pr.workflow_state === filters.pr_status);
                    }

                    // Apply ID filter
                    if (filters.pr_id) {
                        filteredData = filteredData.filter(pr => pr.name.toLowerCase().includes(filters.pr_id.toLowerCase()));
                    }

                    // Apply supplier filter
                    if (filters.supplier) {
                        filteredData = filteredData.filter(pr => pr.supplier === filters.supplier);
                    }

                    // Create status summary based on workflow_state
                    const statusCounts = {};
                    filteredData.forEach(item => {
                        const status = item.workflow_state || 'Draft';
                        statusCounts[status] = (statusCounts[status] || 0) + 1;
                    });

                    const summary = Object.keys(statusCounts).map(status => ({
                        value: statusCounts[status],
                        label: `${status} Purchase Receipts`,
                        datatype: 'Int',
                        indicator: getStatusIndicator(status),
                        description: `Purchase receipts with ${status} status`
                    }));

                    // Update status options based on actual data
                    updateStatusOptions('purchase_receipt', procurementData, state);

                    resolve({
                        summary: summary,
                        raw_data: filteredData
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function fetchPurchaseInvoiceData(filters, state) {
    return new Promise((resolve, reject) => {
        // Use the procurement tracker report to get data with workflow_state
        frappe.call({
            method: 'frappe.desk.query_report.run',
            args: {
                report_name: 'New Procurement Tracker',
                filters: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    item_code: filters.item_name || ''
                },
                ignore_prepared_report: 1,
            },
            callback: (r) => {
                if (r.message && r.message.result) {
                    let procurementData = r.message.result;

                    // Extract unique Purchase Invoices from procurement data
                    const purchaseInvoices = [];
                    const seenPIs = new Set();

                    procurementData.forEach(row => {
                        if (row.purchase_invoice && !seenPIs.has(row.purchase_invoice)) {
                            seenPIs.add(row.purchase_invoice);
                            purchaseInvoices.push({
                                name: row.purchase_invoice,
                                posting_date: row.invoice_date,
                                workflow_state: 'Completed', // Purchase Invoices are typically completed when created
                                status: 'Completed', // Use workflow_state as status for display
                                supplier: row.supplier,
                                grand_total: 0 // Not available in procurement tracker
                            });
                        }
                    });

                    // Apply additional filters
                    let filteredData = purchaseInvoices;

                    // Apply status filter
                    if (filters.pi_status) {
                        filteredData = filteredData.filter(pi => pi.workflow_state === filters.pi_status);
                    }

                    // Apply global workflow status filter if provided
                    if (filters.workflow_status) {
                        filteredData = filteredData.filter(pi => pi.workflow_state === filters.workflow_status);
                    }

                    // Apply ID filter
                    if (filters.pi_id) {
                        filteredData = filteredData.filter(pi => pi.name.toLowerCase().includes(filters.pi_id.toLowerCase()));
                    }

                    // Apply supplier filter if specified
                    if (filters.supplier) {
                        filteredData = filteredData.filter(pi => pi.supplier === filters.supplier);
                    }

                    // Apply item filter if specified - filter the original procurement data first
                    if (filters.item_name) {
                        const itemFilteredProcurementData = procurementData.filter(row =>
                            row.item_code === filters.item_name
                        );

                        // Extract unique Purchase Invoices from item-filtered data
                        const itemFilteredPIs = [];
                        const seenItemFilteredPIs = new Set();

                        itemFilteredProcurementData.forEach(row => {
                            if (row.purchase_invoice && !seenItemFilteredPIs.has(row.purchase_invoice)) {
                                seenItemFilteredPIs.add(row.purchase_invoice);
                                itemFilteredPIs.push({
                                    name: row.purchase_invoice,
                                    posting_date: row.invoice_date,
                                    workflow_state: 'Completed',
                                    status: 'Completed',
                                    supplier: row.supplier,
                                    grand_total: 0
                                });
                            }
                        });

                        // Apply other filters to item-filtered data
                        filteredData = itemFilteredPIs;
                    }

                    // Apply status filter
                    if (filters.pi_status) {
                        filteredData = filteredData.filter(pi => pi.workflow_state === filters.pi_status);
                    }

                    // Apply ID filter
                    if (filters.pi_id) {
                        filteredData = filteredData.filter(pi => pi.name.toLowerCase().includes(filters.pi_id.toLowerCase()));
                    }

                    // Apply supplier filter
                    if (filters.supplier) {
                        filteredData = filteredData.filter(pi => pi.supplier === filters.supplier);
                    }

                    // Create status summary based on workflow_state
                    const statusCounts = {};
                    filteredData.forEach(item => {
                        const status = item.workflow_state || 'Draft';
                        statusCounts[status] = (statusCounts[status] || 0) + 1;
                    });

                    const summary = Object.keys(statusCounts).map(status => ({
                        value: statusCounts[status],
                        label: `${status} Purchase Invoices`,
                        datatype: 'Int',
                        indicator: getStatusIndicator(status),
                        description: `Purchase invoices with ${status} status`
                    }));

                    // Update status options based on actual data
                    updateStatusOptions('purchase_invoice', procurementData, state);

                    resolve({
                        summary: summary,
                        raw_data: filteredData
                    });
                } else {
                    resolve({ summary: [], raw_data: [] });
                }
            },
            error: reject
        });
    });
}

function createProcurementOverviewData(procurementData, mrData, poData, prData, piData) {
    // Calculate totals
    const totalMr = mrData.summary.reduce((sum, card) => sum + (card.value || 0), 0);
    const totalPo = poData.summary.reduce((sum, card) => sum + (card.value || 0), 0);
    const totalPr = prData.summary.reduce((sum, card) => sum + (card.value || 0), 0);
    const totalPi = piData.summary.reduce((sum, card) => sum + (card.value || 0), 0);

    return {
        summary: [
            {
                value: totalMr,
                label: __('Total Material Requests'),
                datatype: 'Int',
                indicator: 'Blue',
                description: __('Total material requests in the period')
            },
            {
                value: totalPo,
                label: __('Total Purchase Orders'),
                datatype: 'Int',
                indicator: 'Green',
                description: __('Total purchase orders created')
            },
            {
                value: totalPr,
                label: __('Total Purchase Receipts'),
                datatype: 'Int',
                indicator: 'Orange',
                description: __('Total purchase receipts received')
            },
            {
                value: totalPi,
                label: __('Total Purchase Invoices'),
                datatype: 'Int',
                indicator: 'Purple',
                description: __('Total purchase invoices processed')
            }
        ],
        raw_data: procurementData
    };
}

function getStatusOptions(tabId) {
    // Start empty; options will be updated dynamically from data for all tabs
    return [''];
}

function updateStatusOptions(tabId, data, state) {
    const statusSet = new Set();

    if (tabId === 'material_request') {
        data.forEach(row => {
            if (row.workflow_state) {
                statusSet.add(row.workflow_state);
            }
        });
    } else if (tabId === 'purchase_order') {
        data.forEach(row => {
            if (row.po_status) {
                statusSet.add(row.po_status);
            }
        });
    } else if (tabId === 'purchase_receipt') {
        data.forEach(row => {
            if (row.purchase_receipt) {
                statusSet.add('Completed'); // Purchase Receipts are typically completed
            }
        });
    } else if (tabId === 'purchase_invoice') {
        data.forEach(row => {
            if (row.purchase_invoice) {
                statusSet.add('Completed'); // Purchase Invoices are typically completed
            }
        });
    }

    const statusOptions = ['', ...Array.from(statusSet).sort()];

    // Update the dropdown options
    const statusControl = state.controls[`${tabId}_status`];
    if (statusControl) {
        statusControl.df.options = statusOptions;
        statusControl.refresh();
    }

    return statusOptions;
}

function getStatusIndicator(status) {
    const statusIndicators = {
        // Workflow states from Material Request and Purchase Order images
        'Draft': 'Blue',
        'Waiting For Review': 'Orange',
        'Waiting For Approval': 'Yellow',
        'Approved': 'Green',
        'Rejected': 'Red',
        // Standard status values
        'Submitted': 'Orange',
        'To Approve': 'Yellow',
        'To Receive': 'Teal',
        'To Bill': 'Purple',
        'Completed': 'Green',
        'Cancelled': 'Red',
        'Closed': 'Grey',
        // Additional workflow state values
        'Partially Received': 'Orange',
        'Partially Ordered': 'Yellow',
        'Pending': 'Blue',
        'Ordered': 'Green',
        'Received': 'Green',
        'Invoiced': 'Purple',
        'To Order': 'Yellow',
        'To Receive': 'Teal',
        'To Bill': 'Purple'
    };
    return statusIndicators[status] || 'Blue';
}

function getFilters(state) {
    const filters = {
        from_date: state.controls.from_date.get_value(),
        to_date: state.controls.to_date.get_value(),
        supplier: state.controls.supplier.get_value(),
        workflow_status: state.controls.workflow_status.get_value()
    };

    // Add section-specific filters
    Object.keys(state.$tabs).forEach(tabId => {
        if (tabId !== 'overview') {
            const statusField = getStatusFieldName(tabId);
            const idField = getIdFieldName(tabId);

            filters[statusField] = state.controls[`${tabId}_status`].get_value();
            filters[idField] = state.controls[`${tabId}_id`].get_value();

            // Get item_name from the current active tab only
            if (state.currentTab === tabId) {
                filters.item_name = state.controls[`${tabId}_item_name`].get_value();
            }
        }
    });

    return filters;
}

function renderDashboardData(state, data) {
    // Render data for each tab
    renderTabData(state, 'overview', data.overview);
    renderTabData(state, 'material_request', data.material_request);
    renderTabData(state, 'purchase_order', data.purchase_order);
    renderTabData(state, 'purchase_receipt', data.purchase_receipt);
    renderTabData(state, 'purchase_invoice', data.purchase_invoice);
}

function renderTabData(state, tabId, tabData) {
    const $cardsContainer = state.$cards[tabId];
    const $tablesContainer = $(`#${tabId}-tables`);

    // Clear containers
    $cardsContainer.empty();
    $tablesContainer.empty();

    if (!tabData || !tabData.summary || !tabData.summary.length) {
        $cardsContainer.append(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:24px;grid-column:1/-1;">
                <i class="fa fa-info-circle" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>${__('No data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    // Render cards
    tabData.summary.forEach((card) => {
        const $card = createCard(card);
        $cardsContainer.append($card);
    });

    // Render detailed tables
    if (tabData.raw_data && tabData.raw_data.length > 0) {
        renderDetailedTables($tablesContainer, tabId, tabData.raw_data);
    }
}

function renderDetailedTables($container, tabId, rawData) {
    if (tabId === 'material_request') {
        renderMaterialRequestTable($container, rawData);
    } else if (tabId === 'purchase_order') {
        renderPurchaseOrderTable($container, rawData);
    } else if (tabId === 'purchase_receipt') {
        renderPurchaseReceiptTable($container, rawData);
    } else if (tabId === 'purchase_invoice') {
        renderPurchaseInvoiceTable($container, rawData);
    } else if (tabId === 'overview') {
        renderOverviewTables($container, rawData);
    }
}

function renderMaterialRequestTable($container, data) {
    if (!data || data.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No material request data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Material Requests')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Material Request')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Date')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Workflow Status')}</th>
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
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/material-request/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.transaction_date, { fieldtype: 'Date' })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><span class="badge badge-${getStatusClass(row.status)}">${row.status || 'Draft'}</span></td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderPurchaseOrderTable($container, data) {
    if (!data || data.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No purchase order data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Purchase Orders')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Purchase Order')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Date')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Workflow Status')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Supplier')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Grand Total')}</th>
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
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/purchase-order/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.transaction_date, { fieldtype: 'Date' })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><span class="badge badge-${getStatusClass(row.status)}">${row.status || 'Draft'}</span></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.supplier || ''}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.grand_total || 0, { fieldtype: 'Currency' })}</td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderPurchaseReceiptTable($container, data) {
    if (!data || data.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No purchase receipt data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Purchase Receipts')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Purchase Receipt')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Date')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Workflow Status')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Supplier')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Grand Total')}</th>
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
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/purchase-receipt/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.posting_date, { fieldtype: 'Date' })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><span class="badge badge-${getStatusClass(row.status)}">${row.status || 'Draft'}</span></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.supplier || ''}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.grand_total || 0, { fieldtype: 'Currency' })}</td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderPurchaseInvoiceTable($container, data) {
    if (!data || data.length === 0) {
        $container.append(`
            <div class="no-data-message">
                <div>${__('No purchase invoice data available for selected criteria')}</div>
            </div>
        `);
        return;
    }

    const $table = $(`
        <div class="data-table" style="width: 100%; margin-bottom: 30px;">
            <h4>${__('Purchase Invoices')}</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Purchase Invoice')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Date')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Workflow Status')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Supplier')}</th>
                        <th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Grand Total')}</th>
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
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><a href="/app/purchase-invoice/${row.name}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.name}</a></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.posting_date, { fieldtype: 'Date' })}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;"><span class="badge badge-${getStatusClass(row.status)}">${row.status || 'Draft'}</span></td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.supplier || ''}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.grand_total || 0, { fieldtype: 'Currency' })}</td>
            </tr>
        `);
        $tbody.append($tr);
    });

    $container.append($table);
}

function renderOverviewTables($container, overviewData) {
    // For overview, we'll show a summary of all procurement data
    $container.append(`
        <div class="overview-summary" style="background:#f8f9fa;padding:20px;border-radius:8px;margin-bottom:20px;">
            <h4>${__('Procurement Summary')}</h4>
            <p>${__('This overview provides a high-level view of all procurement activities across Material Requests, Purchase Orders, Purchase Receipts, and Purchase Invoices.')}</p>
            <p>${__('Use the individual tabs to view detailed information and apply specific filters for each procurement stage.')}</p>
        </div>
    `);
}

function getStatusClass(status) {
    const statusClasses = {
        'Approved': 'success',
        'Rejected': 'danger',
        'Draft': 'secondary',
        'Submitted': 'info',
        'To Approve': 'warning',
        'To Receive': 'primary',
        'To Bill': 'info',
        'Completed': 'success',
        'Cancelled': 'danger',
        'Closed': 'dark'
    };
    return statusClasses[status] || 'secondary';
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
    } else if (card.datatype === 'Currency') {
        value = format_number(card.value || 0, null, 2);
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


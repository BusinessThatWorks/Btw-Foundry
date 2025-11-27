// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Ensure the page is registered before adding event handlers
if (!frappe.pages['customer-production-status']) {
	frappe.pages['customer-production-status'] = {};
}

frappe.pages['customer-production-status'].on_page_load = function (wrapper) {
	console.log('Customer Production Dashboard page loading...');

	// Build page shell
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Customer Production Status'),
		single_column: true,
	});

	// Initialize dashboard state
	const state = {
		page,
		wrapper,
		filters: {},
		controls: {},
		$cards: null,
		$tableContainer: null,
		refreshTimeout: null, // For debouncing auto-refresh
	};

	// Initialize dashboard components
	initializeDashboard(state);
};

frappe.pages['customer-production-status'].on_page_show = function () {
	console.log('Customer Production Dashboard shown');
};

function initializeDashboard(state) {
	// Clear main content
	state.page.main.empty();

	// Create filter bar
	createFilterBar(state);

	// Create summary cards container
	createSummaryCards(state);

	// Create data table container
	createDataTable(state);

	// Bind event handlers
	bindEventHandlers(state);

	// Load initial data
	refreshDashboard(state);
}

function createFilterBar(state) {
	// Main filter container
	const $filterBar = $('<div class="customer-prod-filters" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:20px;justify-content:space-between;background:#f8f9fa;padding:20px;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05);"></div>');

	// Filter controls container
	const $filterControls = $('<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;flex:1;"></div>');

	// Individual filter wrappers
	const $salesOrderWrap = $('<div style="min-width:220px;"></div>');
	const $customerWrap = $('<div style="min-width:220px;"></div>');
	const $btnWrap = $('<div style="display:flex;align-items:end;gap:8px;"></div>');

	// Assemble filter controls
	$filterControls.append($salesOrderWrap).append($customerWrap);
	$filterBar.append($filterControls).append($btnWrap);
	$(state.page.main).append($filterBar);

	// Create filter controls
	createFilterControls(state, $salesOrderWrap, $customerWrap, $btnWrap);
}

function createFilterControls(state, $salesOrderWrap, $customerWrap, $btnWrap) {
	// Debounce function for auto-refresh (shared across all controls)
	const debouncedRefresh = () => {
		if (state.refreshTimeout) {
			clearTimeout(state.refreshTimeout);
		}
		state.refreshTimeout = setTimeout(() => {
			refreshDashboard(state);
		}, 300); // Wait 300ms after last change before refreshing
	};

	// Sales Order control
	state.controls.sales_order_id = frappe.ui.form.make_control({
		parent: $salesOrderWrap.get(0),
		df: {
			fieldtype: 'Link',
			label: __('Sales Order ID'),
			fieldname: 'sales_order_id',
			options: 'Sales Order',
			reqd: 0,
			onchange: debouncedRefresh, // Auto-refresh on change
		},
		render_input: true,
	});

	// Customer control
	state.controls.customer_name = frappe.ui.form.make_control({
		parent: $customerWrap.get(0),
		df: {
			fieldtype: 'Link',
			label: __('Customer Name'),
			fieldname: 'customer_name',
			options: 'Customer',
			reqd: 0,
			onchange: debouncedRefresh, // Auto-refresh on change
		},
		render_input: true,
	});

	// Refresh button
	const $refreshBtn = $('<button class="btn btn-primary" style="padding:10px 20px;font-weight:500;"><i class="fa fa-refresh" style="margin-right:6px;"></i>' + __('Refresh') + '</button>');

	$btnWrap.append($refreshBtn);

	// Store button reference
	state.controls.refreshBtn = $refreshBtn;
}

function createSummaryCards(state) {
	const $cardsContainer = $('<div class="customer-prod-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-bottom:24px;"></div>');
	$(state.page.main).append($cardsContainer);
	state.$cards = $cardsContainer;
}

function createDataTable(state) {
	const $tableSection = $(`
        <div class="customer-prod-table-section" style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:16px;border-bottom:2px solid #e9ecef;">
                <h3 style="margin:0;color:#2c3e50;font-size:1.5rem;font-weight:600;">
                    <i class="fa fa-table" style="margin-right:8px;color:#007bff;"></i>${__('Production Details')}
                </h3>
            </div>
            <div class="data-table-container" style="overflow-x:auto;"></div>
        </div>
    `);
	$(state.page.main).append($tableSection);
	state.$tableContainer = $tableSection.find('.data-table-container');
}

function bindEventHandlers(state) {
	// Shared debounce function for auto-refresh
	const debouncedRefresh = () => {
		if (state.refreshTimeout) {
			clearTimeout(state.refreshTimeout);
		}
		state.refreshTimeout = setTimeout(() => {
			refreshDashboard(state);
		}, 300);
	};

	// Additional event listeners as backup (onchange in df should handle it, but this ensures it works)
	$(state.controls.sales_order_id.$input).on('change', debouncedRefresh);
	$(state.controls.sales_order_id.$input).on('blur', debouncedRefresh);

	$(state.controls.customer_name.$input).on('change', debouncedRefresh);
	$(state.controls.customer_name.$input).on('blur', debouncedRefresh);

	// Button events (refresh button still available for manual refresh)
	state.controls.refreshBtn.on('click', () => {
		if (state.refreshTimeout) clearTimeout(state.refreshTimeout);
		refreshDashboard(state);
	});
}

function refreshDashboard(state) {
	console.log('Refreshing customer production dashboard...');

	const filters = getFilters(state);

	// Show loading state
	state.page.set_indicator(__('Loading production data...'), 'blue');

	// Fetch data using report API (consistent with other dashboards)
	frappe.call({
		method: 'frappe.desk.query_report.run',
		args: {
			report_name: 'Customer Production Status',
			filters: filters,
			ignore_prepared_report: 1,
		},
		callback: (r) => {
			state.page.clear_indicator();

			if (r.message) {
				renderDashboardData(state, {
					columns: r.message.columns || [],
					data: r.message.result || [],
				});
			} else {
				showError(state, __('An error occurred while loading data'));
			}
		},
		error: (r) => {
			state.page.clear_indicator();
			console.error('Dashboard refresh error:', r);
			showError(state, __('An error occurred while loading data'));
		}
	});
}

function getFilters(state) {
	return {
		sales_order_id: state.controls.sales_order_id.get_value(),
		customer_name: state.controls.customer_name.get_value(),
	};
}

function renderDashboardData(state, response) {
	const { columns, data } = response;

	// Clear containers
	state.$cards.empty();
	state.$tableContainer.empty();

	if (!data || data.length === 0) {
		state.$cards.append(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:40px;grid-column:1/-1;background:#f8f9fa;border-radius:12px;border:2px dashed #dee2e6;">
                <i class="fa fa-info-circle" style="font-size:3rem;margin-bottom:16px;color:#95a5a6;"></i>
                <div style="font-size:1.1rem;font-weight:500;">${__('No production data available for selected criteria')}</div>
            </div>
        `);
		state.$tableContainer.append(`
            <div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:40px;">
                <i class="fa fa-info-circle" style="font-size:2rem;margin-bottom:12px;"></i>
                <div>${__('No data to display')}</div>
            </div>
        `);
		return;
	}

	// Calculate summary metrics
	const summary = calculateSummary(data);

	// Render summary cards
	renderSummaryCards(state, summary);

	// Render data table
	renderDataTable(state, columns, data);
}

function calculateSummary(data) {
	let totalQtyManufactured = 0;
	const uniqueCustomers = new Set();
	const uniqueSalesOrders = new Set();
	const uniqueItems = new Set();

	data.forEach((row) => {
		if (row.qty_manufactured) {
			totalQtyManufactured += parseFloat(row.qty_manufactured) || 0;
		}
		if (row.customer_name) {
			uniqueCustomers.add(row.customer_name);
		}
		if (row.sales_order_id) {
			uniqueSalesOrders.add(row.sales_order_id);
		}
		if (row.item_name) {
			uniqueItems.add(row.item_name);
		}
	});

	return {
		totalQtyManufactured: totalQtyManufactured,
		uniqueCustomers: uniqueCustomers.size,
		uniqueSalesOrders: uniqueSalesOrders.size,
		uniqueItems: uniqueItems.size,
	};
}

function renderSummaryCards(state, summary) {
	const cards = [
		{
			value: summary.uniqueSalesOrders,
			label: __('Total Sales Orders'),
			icon: 'fa fa-file-text-o',
			color: '#3498db',
			description: __('Number of unique sales orders'),
		},
		{
			value: summary.uniqueCustomers,
			label: __('Total Customers'),
			icon: 'fa fa-users',
			color: '#2ecc71',
			description: __('Number of unique customers'),
		},
		{
			value: summary.uniqueItems,
			label: __('Total Items'),
			icon: 'fa fa-cube',
			color: '#9b59b6',
			description: __('Number of unique items'),
		},
		{
			value: format_number(summary.totalQtyManufactured, null, 2),
			label: __('Total Qty Manufactured'),
			icon: 'fa fa-industry',
			color: '#e67e22',
			description: __('Total quantity manufactured'),
		},
	];

	cards.forEach((card) => {
		const $card = createCard(card);
		state.$cards.append($card);
	});
}

function createCard(card) {
	return $(`
        <div class="customer-prod-card" style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 4px 12px rgba(0,0,0,0.1);position:relative;overflow:hidden;transition:transform 0.2s ease,box-shadow 0.2s ease;border-top:4px solid ${card.color};">
            <div class="card-content" style="display:flex;align-items:center;gap:16px;">
                <div class="card-icon" style="width:60px;height:60px;border-radius:12px;background:${card.color}15;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    <i class="${card.icon}" style="font-size:1.8rem;color:${card.color};"></i>
                </div>
                <div class="card-info" style="flex:1;">
                    <div class="card-value" style="font-size:2rem;font-weight:700;color:#2c3e50;margin-bottom:4px;line-height:1.2;">${card.value}</div>
                    <div class="card-label" style="font-size:0.95rem;color:#7f8c8d;font-weight:500;margin-bottom:4px;">${frappe.utils.escape_html(card.label)}</div>
                    ${card.description ? `<div class="card-description" style="font-size:0.8rem;color:#95a5a6;margin-top:4px;">${frappe.utils.escape_html(card.description)}</div>` : ''}
                </div>
            </div>
        </div>
    `);
}

function renderDataTable(state, columns, data) {
	if (!columns || columns.length === 0 || !data || data.length === 0) {
		return;
	}

	// Create table
	const $table = $(`
        <table class="customer-prod-table" style="width:100%;border-collapse:collapse;background:#fff;min-width:800px;">
            <thead>
                <tr style="background:#f8f9fa;">
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    `);

	const $thead = $table.find('thead tr');
	const $tbody = $table.find('tbody');

	// Render headers
	columns.forEach((col) => {
		const $th = $(`
            <th style="padding:14px 16px;text-align:${col.fieldtype === 'Float' || col.fieldtype === 'Int' ? 'right' : 'left'};font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;white-space:nowrap;font-size:0.9rem;">
                ${frappe.utils.escape_html(col.label || col.fieldname)}
            </th>
        `);
		$thead.append($th);
	});

	// Render rows
	data.forEach((row) => {
		const $tr = $('<tr style="border-bottom:1px solid #e9ecef;transition:background-color 0.2s ease;"></tr>');

		columns.forEach((col) => {
			const fieldname = col.fieldname;
			let value = row[fieldname] || '';

			// Format value based on fieldtype
			if (col.fieldtype === 'Link' && value) {
				const linkUrl = `/app/${col.options.toLowerCase().replace(/\s+/g, '-')}/${value}`;
				value = `<a href="${linkUrl}" class="link-cell" style="color:#007bff;text-decoration:none;cursor:pointer;font-weight:500;">${frappe.utils.escape_html(value)}</a>`;
			} else if (col.fieldtype === 'Float' || col.fieldtype === 'Int') {
				value = format_number(value || 0, null, col.fieldtype === 'Int' ? 0 : 2);
			} else {
				value = frappe.utils.escape_html(value || '');
			}

			const $td = $(`
                <td style="padding:12px 16px;color:#495057;text-align:${col.fieldtype === 'Float' || col.fieldtype === 'Int' ? 'right' : 'left'};font-size:0.9rem;">
                    ${value}
                </td>
            `);
			$tr.append($td);
		});

		// Add hover effect
		$tr.on('mouseenter', function () {
			$(this).css('background-color', '#f8f9fa');
		});
		$tr.on('mouseleave', function () {
			$(this).css('background-color', 'transparent');
		});

		$tbody.append($tr);
	});

	state.$tableContainer.append($table);
}

function showError(state, message) {
	// Show error in cards container
	state.$cards.empty();
	state.$cards.append(`
        <div class="alert alert-danger" style="background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;padding:20px;border-radius:12px;grid-column:1/-1;">
            <i class="fa fa-exclamation-triangle" style="margin-right:8px;"></i>
            ${frappe.utils.escape_html(message)}
        </div>
    `);
}


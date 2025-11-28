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
	const $statusWrap = $('<div style="min-width:200px;"></div>');
	const $btnWrap = $('<div style="display:flex;align-items:end;gap:8px;"></div>');

	// Assemble filter controls
	$filterControls.append($salesOrderWrap).append($customerWrap).append($statusWrap);
	$filterBar.append($filterControls).append($btnWrap);
	$(state.page.main).append($filterBar);

	// Create filter controls
	createFilterControls(state, $salesOrderWrap, $customerWrap, $statusWrap, $btnWrap);
}

function createFilterControls(state, $salesOrderWrap, $customerWrap, $statusWrap, $btnWrap) {
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

	// Status control
	state.controls.status = frappe.ui.form.make_control({
		parent: $statusWrap.get(0),
		df: {
			fieldtype: 'Select',
			label: __('Status'),
			fieldname: 'status',
			options: '\nCompleted\nPending\nNot Started',
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
	const $cardsContainer = $('<div class="customer-prod-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:24px;"></div>');
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

	$(state.controls.status.$input).on('change', debouncedRefresh);
	$(state.controls.status.$input).on('blur', debouncedRefresh);

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
	const filters = {
		sales_order_id: state.controls.sales_order_id.get_value(),
		customer_name: state.controls.customer_name.get_value(),
	};

	// Only add status filter if a value is selected
	const statusValue = state.controls.status.get_value();
	if (statusValue) {
		filters.status = statusValue;
	}

	return filters;
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

	// Calculate in_progress_qty for each row based on operation chain
	const dataWithInProgress = calculateInProgress(data);

	// Calculate summary metrics
	const summary = calculateSummary(dataWithInProgress);

	// Render summary cards
	renderSummaryCards(state, summary);

	// Render data table
	renderDataTable(state, columns, dataWithInProgress);
}

function calculateInProgress(data) {
	// Group data by work_order to process operation chains
	// The data is already ordered by woo.idx from the SQL query, so we maintain that order
	const groupedByWorkOrder = {};

	// Group rows by work_order while maintaining order
	data.forEach((row, index) => {
		const workOrder = row.work_order || 'unknown';
		if (!groupedByWorkOrder[workOrder]) {
			groupedByWorkOrder[workOrder] = [];
		}
		// Store original index to maintain overall order
		groupedByWorkOrder[workOrder].push({ ...row, originalIndex: index });
	});

	// Process each work order's operation chain
	const processedData = [];

	// Process work orders in the order they appear
	Object.keys(groupedByWorkOrder).forEach(workOrder => {
		const operations = groupedByWorkOrder[workOrder];

		// Operations should already be in sequence order (by woo.idx from SQL)
		// But ensure they're sorted by original index to maintain sequence
		operations.sort((a, b) => a.originalIndex - b.originalIndex);

		// Calculate in_progress for each operation in the chain
		let previousCompletedQty = 0;

		operations.forEach((row, idx) => {
			const completedQty = parseFloat(row.completed_qty) || 0;

			// In Progress calculation:
			// - First operation: in_progress = 0 (nothing came before it)
			// - Subsequent operations: in_progress = previous_completed_qty - current_completed_qty
			//   This represents: quantity received from previous operation minus quantity completed in current operation
			let inProgressQty = 0;
			if (idx === 0) {
				// First operation in chain: nothing came before, so in_progress = 0
				inProgressQty = 0;
			} else {
				// Subsequent operations: 
				// in_progress = what came from previous operation - what we completed in current operation
				inProgressQty = Math.max(0, previousCompletedQty - completedQty);
			}

			// Add in_progress_qty to the row
			row.in_progress_qty = inProgressQty;

			// Update previous completed qty for next iteration
			// The quantity that moves to next operation is what was completed in current operation
			previousCompletedQty = completedQty;

			processedData.push(row);
		});
	});

	// Sort back to original order to maintain the display sequence
	return processedData.sort((a, b) => a.originalIndex - b.originalIndex);
}

function calculateSummary(data) {
	let totalPlannedQty = 0;
	let totalCompletedQty = 0;
	let totalPendingQty = 0;
	const uniqueCustomers = new Set();
	const uniqueSalesOrders = new Set();
	const uniqueItems = new Set();
	const uniqueWorkOrders = new Set();
	const statusCounts = {
		'Completed': 0,
		'Pending': 0,
		'Not Started': 0
	};

	data.forEach((row) => {
		const plannedQty = parseFloat(row.planned_qty) || 0;
		const completedQty = parseFloat(row.completed_qty) || 0;
		const pendingQty = parseFloat(row.pending_qty) || 0;

		totalPlannedQty += plannedQty;
		totalCompletedQty += completedQty;
		totalPendingQty += pendingQty;

		if (row.customer_name) {
			uniqueCustomers.add(row.customer_name);
		}
		if (row.sales_order_id) {
			uniqueSalesOrders.add(row.sales_order_id);
		}
		if (row.item_name) {
			uniqueItems.add(row.item_name);
		}
		if (row.work_order) {
			uniqueWorkOrders.add(row.work_order);
		}
		if (row.status && statusCounts.hasOwnProperty(row.status)) {
			statusCounts[row.status]++;
		}
	});

	const completionPercentage = totalPlannedQty > 0
		? ((totalCompletedQty / totalPlannedQty) * 100).toFixed(2)
		: 0;

	return {
		totalPlannedQty: totalPlannedQty,
		totalCompletedQty: totalCompletedQty,
		totalPendingQty: totalPendingQty,
		completionPercentage: completionPercentage,
		uniqueCustomers: uniqueCustomers.size,
		uniqueSalesOrders: uniqueSalesOrders.size,
		uniqueItems: uniqueItems.size,
		uniqueWorkOrders: uniqueWorkOrders.size,
		statusCounts: statusCounts,
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
			value: format_number(summary.totalPlannedQty, null, 2),
			label: __('Total Planned Qty'),
			icon: 'fa fa-calendar-check-o',
			color: '#34495e',
			description: __('Total planned quantity'),
		},
		{
			value: format_number(summary.totalCompletedQty, null, 2),
			label: __('Total Completed Qty'),
			icon: 'fa fa-check-circle',
			color: '#27ae60',
			description: __('Total completed quantity'),
		},
		{
			value: format_number(summary.totalPendingQty, null, 2),
			label: __('Total Pending Qty'),
			icon: 'fa fa-clock-o',
			color: '#f39c12',
			description: __('Total pending quantity'),
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
        <table class="customer-prod-table" style="width:100%;border-collapse:collapse;background:#fff;min-width:1000px;">
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

	// Find indices for planned_qty and completed_qty
	let plannedQtyIndex = -1;
	let completedQtyIndex = -1;

	columns.forEach((col, index) => {
		if (col.fieldname === 'planned_qty') {
			plannedQtyIndex = index;
		}
		if (col.fieldname === 'completed_qty') {
			completedQtyIndex = index;
		}
	});

	// Render headers and insert In Progress between Planned Qty and Completed Qty
	columns.forEach((col, index) => {
		const $th = $(`
            <th style="padding:14px 16px;text-align:${col.fieldtype === 'Float' || col.fieldtype === 'Int' ? 'right' : 'left'};font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;white-space:nowrap;font-size:0.9rem;">
                ${frappe.utils.escape_html(col.label || col.fieldname)}
            </th>
        `);
		$thead.append($th);

		// Insert In Progress header after Planned Qty (before Completed Qty)
		if (index === plannedQtyIndex) {
			const $inProgressTh = $(`
				<th style="padding:14px 16px;text-align:right;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;white-space:nowrap;font-size:0.9rem;">
					${__('In Progress')}
				</th>
			`);
			$thead.append($inProgressTh);
		}
	});

	// Add Progress column header at the end
	const $progressTh = $(`
        <th style="padding:14px 16px;text-align:center;font-weight:600;color:#495057;border-bottom:2px solid #dee2e6;white-space:nowrap;font-size:0.9rem;min-width:200px;">
            ${__('Progress')}
        </th>
    `);
	$thead.append($progressTh);

	// Render rows
	data.forEach((row) => {
		const $tr = $('<tr style="border-bottom:1px solid #e9ecef;transition:background-color 0.2s ease;"></tr>');

		// Get in_progress_qty for this row
		const inProgressQty = parseFloat(row.in_progress_qty) || 0;
		const isInProgressZero = inProgressQty === 0;

		columns.forEach((col, index) => {
			const fieldname = col.fieldname;
			let value = row[fieldname] || '';

			// Format value based on fieldtype
			if (col.fieldtype === 'Link' && value) {
				const linkUrl = `/app/${col.options.toLowerCase().replace(/\s+/g, '-')}/${value}`;
				value = `<a href="${linkUrl}" class="link-cell" style="color:#007bff;text-decoration:none;cursor:pointer;font-weight:500;">${frappe.utils.escape_html(value)}</a>`;
			} else if (col.fieldtype === 'Float' || col.fieldtype === 'Int') {
				value = format_number(value || 0, null, col.fieldtype === 'Int' ? 0 : 2);
			} else if (fieldname === 'status') {
				// Add color coding for status
				let statusColor = '#95a5a6'; // default gray
				let statusBg = '#ecf0f1';
				if (value === 'Completed') {
					statusColor = '#27ae60';
					statusBg = '#d5f4e6';
				} else if (value === 'Pending') {
					statusColor = '#f39c12';
					statusBg = '#fef5e7';
				} else if (value === 'Not Started') {
					statusColor = '#e74c3c';
					statusBg = '#fadbd8';
				}
				value = `<span style="display:inline-block;padding:4px 12px;border-radius:12px;background:${statusBg};color:${statusColor};font-weight:500;font-size:0.85rem;">${frappe.utils.escape_html(value)}</span>`;
			} else {
				value = frappe.utils.escape_html(value || '');
			}

			const $td = $(`
                <td style="padding:12px 16px;color:#495057;text-align:${col.fieldtype === 'Float' || col.fieldtype === 'Int' ? 'right' : 'left'};font-size:0.9rem;">
                    ${value}
                </td>
            `);
			$tr.append($td);

			// Insert In Progress column after Planned Qty (before Completed Qty)
			if (index === plannedQtyIndex) {
				// Green color when in_progress = 0, orange otherwise
				const inProgressColor = isInProgressZero ? '#27ae60' : '#f39c12';
				const $inProgressTd = $(`
					<td style="padding:12px 16px;text-align:right;font-size:0.9rem;font-weight:500;color:${inProgressColor};">
						${format_number(inProgressQty, null, 2)}
					</td>
				`);
				$tr.append($inProgressTd);
			}
		});

		// Add Progress bar column
		// Progress percentage = completed_qty / (completed_qty + in_progress_qty)
		const completedQty = parseFloat(row.completed_qty) || 0;
		const totalQty = completedQty + inProgressQty;
		const progressPercentage = totalQty > 0 ? Math.min((completedQty / totalQty) * 100, 100) : 0;

		// Determine progress bar color based on status
		let progressColor = '#3498db'; // default blue
		if (row.status === 'Completed') {
			progressColor = '#27ae60'; // green
		} else if (row.status === 'Not Started') {
			progressColor = '#e74c3c'; // red
		} else if (row.status === 'Pending') {
			progressColor = '#f39c12'; // orange
		}

		const progressBar = `
			<div style="display:flex;align-items:center;gap:8px;">
				<div style="flex:1;background:#ecf0f1;border-radius:10px;height:24px;overflow:hidden;position:relative;box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);">
					<div style="height:100%;background:${progressColor};width:${progressPercentage}%;transition:width 0.3s ease;border-radius:10px;display:flex;align-items:center;justify-content:center;min-width:${progressPercentage > 0 ? '30px' : '0'};">
						${progressPercentage > 10 ? `<span style="color:#fff;font-size:0.75rem;font-weight:600;text-shadow:0 1px 2px rgba(0,0,0,0.2);">${progressPercentage.toFixed(1)}%</span>` : ''}
					</div>
				</div>
				<div style="min-width:50px;text-align:right;font-size:0.85rem;color:#7f8c8d;font-weight:500;">
					${progressPercentage.toFixed(1)}%
				</div>
			</div>
		`;

		const $progressTd = $(`
			<td style="padding:12px 16px;font-size:0.9rem;">
				${progressBar}
			</td>
		`);
		$tr.append($progressTd);

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


// Copyright (c) 2025, beetashoke chakraborty and contributors
// For license information, please see license.txt

// Ensure the page is registered before adding event handlers
if (!frappe.pages['heat-dashboard']) {
    frappe.pages['heat-dashboard'] = {};
}

frappe.pages['heat-dashboard'].on_page_load = function (wrapper) {
    console.log('Heat Dashboard page loading...');

    // Build page shell like ERPNext's sales_funnel
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Heat Dashboard'),
        single_column: true,
    });

    const state = { page, wrapper, filters: {}, $cards: null, controls: {} };

    // Main containers
    page.main.empty();

    // In-page filter bar (reliable across desk setups)
    const $filterBar = $('<div class="heat-filters" style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:12px;justify-content:space-between;"></div>');
    const $filterControls = $('<div style="display:flex;gap:12px;align-items:end;flex-wrap:wrap;"></div>');
    const $fromWrap = $('<div style="min-width:220px;"></div>');
    const $toWrap = $('<div style="min-width:220px;"></div>');
    const $furnaceWrap = $('<div style="min-width:220px;"></div>');
    const $btnWrap = $('<div style="display:flex;align-items:end;"></div>');
    $filterControls.append($fromWrap).append($toWrap).append($furnaceWrap);
    $filterBar.append($filterControls).append($btnWrap);
    $(page.main).append($filterBar);

    // Controls
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

    // Defaults
    state.controls.from_date.set_value(frappe.datetime.month_start());
    state.controls.to_date.set_value(frappe.datetime.month_end());

    // Refresh button
    const $refreshBtn = $('<button class="btn btn-primary">' + __('Refresh') + '</button>');
    $refreshBtn.on('click', () => refresh(state));
    $btnWrap.append($refreshBtn);

    // Auto refresh on change
    $(state.controls.from_date.$input).on('change', () => refresh(state));
    $(state.controls.to_date.$input).on('change', () => refresh(state));

    // For Link field, we need to handle multiple events
    $(state.controls.furnace_no.$input).on('change', () => {
        console.log('Furnace change event triggered');
        refresh(state);
    });
    $(state.controls.furnace_no.$input).on('blur', () => {
        console.log('Furnace blur event triggered');
        refresh(state);
    });
    // Also listen to the control's internal change event
    state.controls.furnace_no.$wrapper.on('change', () => {
        console.log('Furnace wrapper change event triggered');
        refresh(state);
    });

    // Content containers
    state.$cards = $('<div class="number-cards-container" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:16px;"></div>');
    $(page.main).append(state.$cards);

    // First load
    console.log('Triggering initial refresh...');
    refresh(state);
};

frappe.pages['heat-dashboard'].on_page_show = function () {
    console.log('Heat Dashboard shown');
};

function refresh(state) {
    console.log('Refresh function called');
    const from_date = state.controls.from_date.get_value();
    const to_date = state.controls.to_date.get_value();
    const furnace_no = state.controls.furnace_no.get_value();

    console.log('Filter values:', { from_date, to_date, furnace_no });

    if (!from_date || !to_date) {
        console.log('Missing date values, returning');
        return;
    }

    console.log('Setting loading indicator...');
    state.page.set_indicator(__('Loading'), 'blue');

    // Build filters object
    const filters = { from_date, to_date };
    if (furnace_no) {
        filters.furnace_no = furnace_no;
    }

    console.log('Calling report API with filters:', filters);
    frappe.call({
        method: 'frappe.desk.query_report.run',
        args: {
            report_name: 'Number card Heat report',
            filters: filters,
            ignore_prepared_report: 1,
        },
        callback: (r) => {
            console.log('Report API response:', r);
            state.page.clear_indicator();
            if (!r.message) {
                console.log('No message in response');
                render_error(state, __('No data returned'));
                return;
            }
            console.log('Rendering cards...');
            render_cards(state, r.message.report_summary || []);
        },
        error: (err) => {
            console.log('Report API error:', err);
            state.page.clear_indicator();
            render_error(state, __('Failed to load data'));
        },
    });
}

function render_cards(state, summary) {
    state.$cards.empty();
    if (!summary.length) {
        state.$cards.append(`<div class="no-data-message" style="text-align:center;color:#7f8c8d;padding:24px;grid-column:1/-1;">${__('No data for selected range')}</div>`);
        return;
    }

    summary.forEach((card) => {
        const indicator = (card.indicator || 'blue').toString().toLowerCase();

        // Format value based on datatype and precision
        let value;
        if (card.datatype === 'Int') {
            // Integer values should have no decimal places
            value = format_number(card.value || 0, null, 0);
        } else if (card.datatype === 'Float') {
            // Float values should use the specified precision (default to 2 if not specified)
            const precision = card.precision !== undefined ? card.precision : 2;
            value = format_number(card.value || 0, null, precision);
        } else {
            // Default formatting for other types
            value = format_number(card.value || 0);
        }

        const $card = $(`
			<div class="number-card" style="background:#fff;border-radius:10px;padding:20px;box-shadow:0 4px 6px rgba(0,0,0,0.08);position:relative;overflow:hidden;">
				<div class="card-indicator" style="position:absolute;top:0;left:0;right:0;height:4px;background:${indicator_color(indicator)}"></div>
				<div class="card-content" style="text-align:center;">
					<div class="card-value" style="font-size:2.2rem;font-weight:700;color:#2c3e50;margin-bottom:8px;">${value}</div>
					<div class="card-label" style="font-size:1rem;color:#7f8c8d;font-weight:500;">${frappe.utils.escape_html(card.label || '')}</div>
				</div>
			</div>
		`);
        state.$cards.append($card);
    });
}



function render_error(state, msg) {
    state.$cards.empty();
    state.$cards.append(`<div class="alert alert-danger" style="background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;padding:12px;border-radius:6px;grid-column:1/-1;">${frappe.utils.escape_html(msg)}</div>`);
}

function indicator_color(indicator) {
    switch (indicator) {
        case 'green': return 'linear-gradient(90deg,#27ae60,#229954)';
        case 'black': return 'linear-gradient(90deg,#34495e,#2c3e50)';
        case 'red': return 'linear-gradient(90deg,#e74c3c,#c0392b)';
        case 'blue':
        default: return 'linear-gradient(90deg,#3498db,#2980b9)';
    }
}

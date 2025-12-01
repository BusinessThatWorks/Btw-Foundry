frappe.pages['sales-order-throughput-dashboard'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Sales Order Dashboard',
        single_column: true
    });

    const $container = $('<div class="so-dashboard-container"></div>').appendTo(page.body);

    // Main tabs: Heat and Mould
    const $main_tabs_container = $('<div class="mt-3"></div>').appendTo($container);
    const $main_nav_tabs = $(
        '<ul class="nav nav-tabs" role="tablist">\
			<li class="nav-item"><a class="nav-link active" role="tab" data-target="#heat-main-tab">Heat</a></li>\
			<li class="nav-item"><a class="nav-link" role="tab" data-target="#mould-main-tab">Mould</a></li>\
		</ul>'
    ).appendTo($main_tabs_container);
    const $main_tab_content = $('<div class="tab-content"></div>').appendTo($main_tabs_container);

    // Heat main tab
    const $heat_main_tab = $('<div class="tab-pane fade show active" id="heat-main-tab" role="tabpanel"></div>').appendTo($main_tab_content);

    // Mould main tab
    const $mould_main_tab = $('<div class="tab-pane fade" id="mould-main-tab" role="tabpanel"></div>').appendTo($main_tab_content);

    // ========== HEAT TAB CONTENT ==========
    // Create number cards section
    const $cards_section = $('<div class="row mb-4"></div>').appendTo($heat_main_tab);

    // Number cards
    const $card1 = $('<div class="col-md-3 mb-3"></div>').appendTo($cards_section);
    const $card2 = $('<div class="col-md-3 mb-3"></div>').appendTo($cards_section);
    const $card3 = $('<div class="col-md-3 mb-3"></div>').appendTo($cards_section);
    const $card4 = $('<div class="col-md-3 mb-3"></div>').appendTo($cards_section);

    // Neutral, minimal cards (no colors)
    const baseCardStyle = 'background:#fff; color:#1f2937; border:none; border-top:4px solid #e5e7eb; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.05)';
    const bodyStyle = 'padding:18px 16px;';
    const titleStyle = 'margin:0; font-size:12px; color:#6b7280; font-weight:600;';
    const valueStyle = 'margin:4px 0 2px; font-size:36px; font-weight:700; letter-spacing:0.3px; color:#111827;';
    const subStyle = 'color:#6b7280; font-size:12px;';

    const $total_weight_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($card1);
    const $heat_1t_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($card2);
    const $heat_500kg_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($card3);
    const $heat_200kg_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($card4);

    // Card content
    $total_weight_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Weight</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="total-weight-value">0.00</h2>
			<small style="` + subStyle + `">kg</small>
		</div>
	`);

    $heat_1t_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Estimated Heats</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="heat-1t-value">0.00</h2>
			<small style="` + subStyle + `">1 Ton Furnace</small>
		</div>
	`);

    $heat_500kg_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Estimated Heats</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="heat-500kg-value">0.00</h2>
			<small style="` + subStyle + `">500kg Furnace</small>
		</div>
	`);

    $heat_200kg_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Estimated Heats</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="heat-200kg-value">0.00</h2>
			<small style="` + subStyle + `">200kg Furnace</small>
		</div>
	`);

    // Create filter section with better layout
    const $filters = $('<div class="form-section" style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;"></div>').appendTo($heat_main_tab);
    $('<div class="section-head" style="font-weight: bold; margin-bottom: 15px; color: #333;">Filters</div>').appendTo($filters);

    // Create three rows for better spacing
    const $filter_row1 = $('<div class="row" style="margin-bottom: 15px;"></div>').appendTo($filters);
    const $filter_row2 = $('<div class="row" style="margin-bottom: 15px;"></div>').appendTo($filters);
    const $filter_row3 = $('<div class="row" style="margin-bottom: 15px;"></div>').appendTo($filters);

    // Create filter controls with better layout
    // Row 1: Date filters
    const $from_date_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($filter_row1);
    const from_date_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Date',
            label: 'From Date',
            fieldname: 'from_date',
            default: frappe.datetime.get_today()
        },
        parent: $from_date_col,
        render_input: true
    });

    const $to_date_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($filter_row1);
    const to_date_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Date',
            label: 'To Date',
            fieldname: 'to_date',
            default: frappe.datetime.get_today()
        },
        parent: $to_date_col,
        render_input: true
    });

    const $sales_order_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($filter_row1);
    const sales_order_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Sales Order',
            fieldname: 'sales_order',
            options: 'Sales Order'
        },
        parent: $sales_order_col,
        render_input: true
    });

    const $item_col = $('<div class="col-md-3"></div>').appendTo($filter_row1);
    const item_code_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Item',
            fieldname: 'item_code',
            options: 'Item'
        },
        parent: $item_col,
        render_input: true
    });

    // Row 2: Grade and Grade Group filters
    const $grade_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($filter_row2);
    const grade_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Grade',
            fieldname: 'grade',
            options: 'Grade Master'
        },
        parent: $grade_col,
        render_input: true
    });

    const $grade_group_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($filter_row2);
    const grade_group_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Grade Group',
            fieldname: 'grade_group',
            options: 'Grade Group'
        },
        parent: $grade_group_col,
        render_input: true
    });

    // Row 3: Furnace filter and refresh button
    const $furnace_col = $('<div class="col-md-6" style="padding-right: 10px;"></div>').appendTo($filter_row3);
    const furnace_options_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'MultiSelect',
            label: 'Furnace Filter',
            fieldname: 'furnace_options',
            options: ['1T', '500kg', '200kg'].join('\n'),
            description: 'Select one or more furnaces to show estimated time columns (1T, 500kg, 200kg).'
        },
        parent: $furnace_col,
        render_input: true
    });

    // Refresh button in its own column
    const $refresh_col = $('<div class="col-md-6" style="display: flex; align-items: end; padding-top: 20px;"></div>').appendTo($filter_row3);
    const $refresh_btn = $('<button class="btn btn-primary" style="width: 120px;">Refresh</button>').appendTo($refresh_col);

    // Tabs for Data and Totals views (Heat tab)
    const $tabs_container = $('<div class="mt-3"></div>').appendTo($heat_main_tab);
    const $nav_tabs = $(
        '<ul class="nav nav-tabs" role="tablist">\
			<li class="nav-item"><a class="nav-link active" role="tab" data-target="#so-data-tab">Data</a></li>\
			<li class="nav-item"><a class="nav-link" role="tab" data-target="#so-totals-tab">Totals</a></li>\
		</ul>'
    ).appendTo($tabs_container);
    const $tab_content = $('<div class="tab-content"></div>').appendTo($tabs_container);
    const $data_tab = $('<div class="tab-pane fade show active" id="so-data-tab" role="tabpanel"></div>').appendTo($tab_content);
    const $totals_tab = $('<div class="tab-pane fade" id="so-totals-tab" role="tabpanel"></div>').appendTo($tab_content);

    // Containers inside tabs
    const $table_container = $('<div class="table-container mt-3"></div>').appendTo($data_tab);
    const $totals_container = $('<div class="totals-container mt-3"></div>').appendTo($totals_tab);

    let last_result = null;

    // ========== MOULD TAB CONTENT ==========
    // Mould number cards (3 cards)
    const $mould_cards_section = $('<div class="row mb-4"></div>').appendTo($mould_main_tab);

    const $mould_card1 = $('<div class="col-md-4 mb-3"></div>').appendTo($mould_cards_section);
    const $mould_card2 = $('<div class="col-md-4 mb-3"></div>').appendTo($mould_cards_section);
    const $mould_card3 = $('<div class="col-md-4 mb-3"></div>').appendTo($mould_cards_section);

    const $mould_total_qty_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($mould_card1);
    const $mould_total_mould_no_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($mould_card2);
    const $mould_total_time_card = $('<div class="card text-center" style="' + baseCardStyle + '"></div>').appendTo($mould_card3);

    // Mould card contents
    $mould_total_qty_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Mould Quantity</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="mould-total-qty-value">0.00</h2>
			<small style="` + subStyle + `"></small>
		</div>
	`);

    $mould_total_mould_no_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Mould No</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="mould-total-mould-no-value">0</h2>
			<small style="` + subStyle + `"></small>
		</div>
	`);

    $mould_total_time_card.html(`
		<div class="card-body" style="` + bodyStyle + `">
			<h5 class="card-title" style="` + titleStyle + `">Total Mould Time</h5>
			<h2 class="card-text" style="` + valueStyle + `" id="mould-total-time-value">0 days</h2>
			<small style="` + subStyle + `"></small>
		</div>
	`);

    // Create filter section for Mould tab
    const $mould_filters = $('<div class="form-section" style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;"></div>').appendTo($mould_main_tab);
    $('<div class="section-head" style="font-weight: bold; margin-bottom: 15px; color: #333;">Filters</div>').appendTo($mould_filters);

    const $mould_filter_row = $('<div class="row" style="margin-bottom: 15px;"></div>').appendTo($mould_filters);

    // Mould filters: from_date, to_date, sales_order, item_code
    const $mould_from_date_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($mould_filter_row);
    const mould_from_date_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Date',
            label: 'From Date',
            fieldname: 'from_date',
            default: frappe.datetime.get_today()
        },
        parent: $mould_from_date_col,
        render_input: true
    });

    const $mould_to_date_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($mould_filter_row);
    const mould_to_date_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Date',
            label: 'To Date',
            fieldname: 'to_date',
            default: frappe.datetime.get_today()
        },
        parent: $mould_to_date_col,
        render_input: true
    });

    const $mould_sales_order_col = $('<div class="col-md-3" style="padding-right: 10px;"></div>').appendTo($mould_filter_row);
    const mould_sales_order_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Sales Order',
            fieldname: 'sales_order',
            options: 'Sales Order'
        },
        parent: $mould_sales_order_col,
        render_input: true
    });

    const $mould_item_col = $('<div class="col-md-3"></div>').appendTo($mould_filter_row);
    const mould_item_code_ctrl = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            label: 'Item',
            fieldname: 'item_code',
            options: 'Item'
        },
        parent: $mould_item_col,
        render_input: true
    });

    // Refresh button for Mould tab
    const $mould_refresh_row = $('<div class="row" style="margin-bottom: 15px;"></div>').appendTo($mould_filters);
    const $mould_refresh_col = $('<div class="col-md-12" style="display: flex; align-items: end; padding-top: 20px;"></div>').appendTo($mould_refresh_row);
    const $mould_refresh_btn = $('<button class="btn btn-primary" style="width: 120px;">Refresh</button>').appendTo($mould_refresh_col);

    // Tabs for Data and Totals views (Mould tab)
    const $mould_tabs_container = $('<div class="mt-3"></div>').appendTo($mould_main_tab);
    const $mould_nav_tabs = $(
        '<ul class="nav nav-tabs" role="tablist">\
			<li class="nav-item"><a class="nav-link active" role="tab" data-target="#mould-data-tab">Data</a></li>\
			<li class="nav-item"><a class="nav-link" role="tab" data-target="#mould-totals-tab">Totals</a></li>\
		</ul>'
    ).appendTo($mould_tabs_container);
    const $mould_tab_content = $('<div class="tab-content"></div>').appendTo($mould_tabs_container);
    const $mould_data_tab = $('<div class="tab-pane fade show active" id="mould-data-tab" role="tabpanel"></div>').appendTo($mould_tab_content);
    const $mould_totals_tab = $('<div class="tab-pane fade" id="mould-totals-tab" role="tabpanel"></div>').appendTo($mould_tab_content);

    // Containers inside Mould tabs
    const $mould_table_container = $('<div class="table-container mt-3"></div>').appendTo($mould_data_tab);
    const $mould_totals_container = $('<div class="totals-container mt-3"></div>').appendTo($mould_totals_tab);

    let last_mould_result = null;

    function update_number_cards(data) {
        if (!data || !data.result || !data.result.length) {
            $('#total-weight-value').text('0.00');
            $('#heat-1t-value').text('0.00');
            $('#heat-500kg-value').text('0.00');
            $('#heat-200kg-value').text('0.00');
            return;
        }

        // Filter only the total rows (subtotal rows)
        const total_rows = data.result.filter(row => row && row.bold);

        let total_weight = 0;
        let total_heat_1t = 0;
        let total_heat_500kg = 0;
        let total_heat_200kg = 0;

        total_rows.forEach(row => {
            // Sum total_quantity (Total Weight)
            if (row.total_quantity && typeof row.total_quantity === 'number') {
                total_weight += row.total_quantity;
            }

            // Sum total_est_heats_1t
            if (row.total_est_heats_1t && typeof row.total_est_heats_1t === 'number') {
                total_heat_1t += row.total_est_heats_1t;
            }

            // Sum total_est_heats_500kg
            if (row.total_est_heats_500kg && typeof row.total_est_heats_500kg === 'number') {
                total_heat_500kg += row.total_est_heats_500kg;
            }

            // Sum total_est_heats_200kg
            if (row.total_est_heats_200kg && typeof row.total_est_heats_200kg === 'number') {
                total_heat_200kg += row.total_est_heats_200kg;
            }
        });

        // Update the cards
        $('#total-weight-value').text(total_weight.toFixed(2));
        $('#heat-1t-value').text(total_heat_1t.toFixed(2));
        $('#heat-500kg-value').text(total_heat_500kg.toFixed(2));
        $('#heat-200kg-value').text(total_heat_200kg.toFixed(2));
    }

    // Mould tab functions
    function formatMouldTime(value) {
        if (value === null || value === undefined || isNaN(Number(value))) {
            return '';
        }

        // Assume mould_time is in minutes → convert to seconds
        let totalSeconds = Math.floor(Number(value) * 60);

        const days = Math.floor(totalSeconds / (24 * 60 * 60));
        totalSeconds %= (24 * 60 * 60);
        const hours = Math.floor(totalSeconds / (60 * 60));
        totalSeconds %= (60 * 60);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;

        const parts = [];
        if (days) {
            parts.push(days + ' day');
        }
        if (hours) {
            parts.push(hours + ' hour');
        }
        if (minutes) {
            parts.push(minutes + ' min');
        }
        if (seconds) {
            parts.push(seconds + ' sec');
        }

        // If everything was zero, show "0 days"
        if (!parts.length) {
            return '0 days';
        }

        return parts.join(' ');
    }

    function update_mould_number_cards(data) {
        if (!data || !data.result || !data.result.length) {
            $('#mould-total-qty-value').text('0.00');
            $('#mould-total-mould-no-value').text('0');
            $('#mould-total-time-value').text('0 days');
            return;
        }

        const total_rows = data.result.filter(row => row && row.bold);

        let total_qty = 0;
        let total_mould_no = 0;
        let total_mould_time = 0;

        total_rows.forEach(row => {
            if (row.qty && typeof row.qty === 'number') {
                total_qty += row.qty;
            }
            if (row.mould_no && typeof row.mould_no === 'number') {
                total_mould_no += row.mould_no;
            }
            if (row.mould_time && typeof row.mould_time === 'number') {
                total_mould_time += row.mould_time;
            }
        });

        $('#mould-total-qty-value').text(total_qty.toFixed(2));
        $('#mould-total-mould-no-value').text(Math.round(total_mould_no));
        $('#mould-total-time-value').text(formatMouldTime(total_mould_time));
    }

    async function load_mould_data() {
        try {
            const filters = {
                from_date: mould_from_date_ctrl.get_value(),
                to_date: mould_to_date_ctrl.get_value(),
                sales_order: mould_sales_order_ctrl.get_value(),
                item_code: mould_item_code_ctrl.get_value()
            };

            // Call the Mould Capacity Planning report
            const result = await frappe.call({
                method: 'frappe.desk.query_report.run',
                args: {
                    report_name: 'Mould Capacity Planning',
                    filters: filters
                }
            });

            last_mould_result = result.message;
            render_mould_table(last_mould_result);
            render_mould_totals(last_mould_result);
            update_mould_number_cards(last_mould_result);

        } catch (error) {
            console.error('Error loading mould data:', error);
            frappe.msgprint('Error loading mould data: ' + error.message);
        }
    }

    function render_mould_table(data) {
        $mould_table_container.empty();

        if (!data || !data.result || !data.result.length) {
            $mould_table_container.html('<div class="text-muted">No data found</div>');
            return;
        }

        const columns = data.columns || [];
        const rows = data.result || [];

        // Create table with better styling
        const $table = $('<table class="table table-bordered table-striped" style="font-size: 13px; margin-top: 0;"></table>').appendTo($mould_table_container);

        // Header
        const $thead = $('<thead></thead>').appendTo($table);
        const $header_row = $('<tr></tr>').appendTo($thead);

        columns.forEach(col => {
            const $th = $('<th style="background-color: #f8f9fa; font-weight: bold; padding: 12px 8px; border: 1px solid #dee2e6;"></th>').text(col.label || col.fieldname || col);
            if (col.width) $th.css('width', col.width + 'px');
            $th.appendTo($header_row);
        });

        // Body
        const $tbody = $('<tbody></tbody>').appendTo($table);

        rows.forEach(row => {
            const $tr = $('<tr></tr>').appendTo($tbody);

            // Style subtotal rows
            if (row.bold) {
                $tr.css('font-weight', 'bold').css('background-color', '#e9ecef').css('border-top', '2px solid #007bff');
            }

            columns.forEach(col => {
                const fieldname = col.fieldname || col;
                const value = row[fieldname];

                const $td = $('<td style="padding: 8px; border: 1px solid #dee2e6;"></td>').appendTo($tr);

                if (value === null || value === undefined) {
                    $td.text('');
                } else if (fieldname === 'mould_no' && typeof value === 'number') {
                    // Show mould no as integer
                    $td.text(Math.round(value));
                } else if (fieldname === 'mould_time' && typeof value === 'number') {
                    // Show mould time as Day Hour Min Sec
                    $td.text(formatMouldTime(value));
                } else if (typeof value === 'number') {
                    // Default numeric formatting
                    $td.text(Number(value).toFixed(2));
                } else {
                    $td.text(String(value));
                }
            });
        });
    }

    function render_mould_totals(data) {
        $mould_totals_container.empty();

        if (!data || !data.columns || !data.result || !data.result.length) {
            $mould_totals_container.html('<div class="text-muted">No totals available</div>');
            return;
        }

        const columns = (data.columns || []).map(c => (typeof c === 'string' ? { fieldname: c, label: c } : c));
        const rows = (data.result || []).filter(r => r && r.bold); // only subtotal rows per SO

        if (!rows.length) {
            $mould_totals_container.html('<div class="text-muted">No subtotal rows found</div>');
            return;
        }

        // Determine which columns have values in subtotal rows (keep first col always)
        const hasValueInAnySubtotal = (col) => rows.some(r => {
            const v = r[col.fieldname || col.label];
            return v !== null && v !== undefined && v !== '';
        });
        const visibleColumns = columns.filter((col, idx) => idx === 0 || hasValueInAnySubtotal(col));

        const $table = $('<table class="table table-bordered table-striped" style="font-size: 13px; margin-top: 0;"></table>').appendTo($mould_totals_container);
        const $thead = $('<thead></thead>').appendTo($table);
        const $header_row = $('<tr></tr>').appendTo($thead);
        visibleColumns.forEach(col => {
            const $th = $('<th style="background-color: #f8f9fa; font-weight: bold; padding: 10px 8px; border: 1px solid #dee2e6;"></th>').text(col.label || col.fieldname || col);
            if (col.width) $th.css('width', col.width + 'px');
            $th.appendTo($header_row);
        });

        const $tbody = $('<tbody></tbody>').appendTo($table);
        rows.forEach(row => {
            const $tr = $('<tr></tr>').appendTo($tbody);
            $tr.css('font-weight', 'bold').css('background-color', '#f5f7fb').css('border-top', '2px solid #3b82f6');

            visibleColumns.forEach(col => {
                const fieldname = col.fieldname || col;
                const value = row[fieldname];
                const isNumber = typeof value === 'number';
                const $td = $('<td style="padding: 8px; border: 1px solid #dee2e6;' + (isNumber ? ' text-align:right;' : '') + '"></td>').appendTo($tr);

                if (value === null || value === undefined) {
                    $td.text('');
                } else if (fieldname === 'mould_no' && isNumber) {
                    // Show mould no as integer in totals
                    $td.text(Math.round(value));
                } else if (fieldname === 'mould_time' && isNumber) {
                    // Show mould time as Day Hour Min Sec in totals
                    $td.text(formatMouldTime(value));
                } else if (isNumber) {
                    $td.text(Number(value).toFixed(2));
                } else {
                    $td.text(String(value));
                }
            });
        });
    }

    async function load_data() {
        try {
            const filters = {
                from_date: from_date_ctrl.get_value(),
                to_date: to_date_ctrl.get_value(),
                sales_order: sales_order_ctrl.get_value(),
                item_code: item_code_ctrl.get_value(),
                grade: grade_ctrl.get_value(),
                grade_group: grade_group_ctrl.get_value(),
                furnace_options: furnace_options_ctrl.get_value()
            };

            // Call the report directly using frappe.desk.query_report.run
            const result = await frappe.call({
                method: 'frappe.desk.query_report.run',
                args: {
                    report_name: 'Sales Order Item Report',
                    filters: filters
                }
            });

            last_result = result.message;
            render_table(last_result);
            render_totals(last_result);
            update_number_cards(last_result);

        } catch (error) {
            console.error('Error loading data:', error);
            frappe.msgprint('Error loading data: ' + error.message);
        }
    }

    function render_table(data) {
        $table_container.empty();

        if (!data || !data.result || !data.result.length) {
            $table_container.html('<div class="text-muted">No data found</div>');
            return;
        }

        const columns = data.columns || [];
        const rows = data.result || [];

        // Create table with better styling
        const $table = $('<table class="table table-bordered table-striped" style="font-size: 13px; margin-top: 0;"></table>').appendTo($table_container);

        // Header
        const $thead = $('<thead></thead>').appendTo($table);
        const $header_row = $('<tr></tr>').appendTo($thead);

        columns.forEach(col => {
            const $th = $('<th style="background-color: #f8f9fa; font-weight: bold; padding: 12px 8px; border: 1px solid #dee2e6;"></th>').text(col.label || col.fieldname || col);
            if (col.width) $th.css('width', col.width + 'px');
            $th.appendTo($header_row);
        });

        // Body
        const $tbody = $('<tbody></tbody>').appendTo($table);

        rows.forEach(row => {
            const $tr = $('<tr></tr>').appendTo($tbody);

            // Style subtotal rows
            if (row.bold) {
                $tr.css('font-weight', 'bold').css('background-color', '#e9ecef').css('border-top', '2px solid #007bff');
            }

            columns.forEach(col => {
                const fieldname = col.fieldname || col;
                const value = row[fieldname];

                const $td = $('<td style="padding: 8px; border: 1px solid #dee2e6;"></td>').appendTo($tr);

                if (value === null || value === undefined) {
                    $td.text('');
                } else if (typeof value === 'number') {
                    // Format numbers to 2 decimal places
                    $td.text(Number(value).toFixed(2));
                } else {
                    $td.text(String(value));
                }
            });
        });
    }

    function render_totals(data) {
        $totals_container.empty();

        if (!data || !data.columns || !data.result || !data.result.length) {
            $totals_container.html('<div class="text-muted">No totals available</div>');
            return;
        }

        const columns = (data.columns || []).map(c => (typeof c === 'string' ? { fieldname: c, label: c } : c));
        const rows = (data.result || []).filter(r => r && r.bold); // only subtotal rows per SO

        if (!rows.length) {
            $totals_container.html('<div class="text-muted">No subtotal rows found</div>');
            return;
        }

        // Determine which columns have values in subtotal rows (keep first col always)
        const hasValueInAnySubtotal = (col) => rows.some(r => {
            const v = r[col.fieldname || col.label];
            return v !== null && v !== undefined && v !== '';
        });
        const visibleColumns = columns.filter((col, idx) => idx === 0 || hasValueInAnySubtotal(col));

        const $table = $('<table class="table table-bordered table-striped" style="font-size: 13px; margin-top: 0;"></table>').appendTo($totals_container);
        const $thead = $('<thead></thead>').appendTo($table);
        const $header_row = $('<tr></tr>').appendTo($thead);
        visibleColumns.forEach(col => {
            const $th = $('<th style="background-color: #f8f9fa; font-weight: bold; padding: 10px 8px; border: 1px solid #dee2e6;"></th>').text(col.label || col.fieldname || col);
            if (col.width) $th.css('width', col.width + 'px');
            $th.appendTo($header_row);
        });

        const $tbody = $('<tbody></tbody>').appendTo($table);
        rows.forEach(row => {
            const $tr = $('<tr></tr>').appendTo($tbody);
            $tr.css('font-weight', 'bold').css('background-color', '#f5f7fb').css('border-top', '2px solid #3b82f6');

            visibleColumns.forEach(col => {
                const fieldname = col.fieldname || col;
                const value = row[fieldname];
                const isNumber = typeof value === 'number';
                const $td = $('<td style="padding: 8px; border: 1px solid #dee2e6;' + (isNumber ? ' text-align:right;' : '') + '"></td>').appendTo($tr);
                if (value === null || value === undefined) {
                    $td.text('');
                } else if (isNumber) {
                    $td.text(Number(value).toFixed(2));
                } else {
                    $td.text(String(value));
                }
            });
        });
    }

    // Event handlers
    $refresh_btn.on('click', load_data);
    $mould_refresh_btn.on('click', load_mould_data);

    // Manual tab toggling for main tabs (Heat/Mould)
    $main_nav_tabs.on('click', 'a.nav-link', function (e) {
        e.preventDefault();
        const target = $(this).data('target');
        $main_nav_tabs.find('a.nav-link').removeClass('active');
        $(this).addClass('active');
        $main_tab_content.children('.tab-pane').removeClass('show active');
        $(target).addClass('show active');
    });

    // Manual tab toggling for Heat tab sub-tabs (Data/Totals)
    $nav_tabs.on('click', 'a.nav-link', function (e) {
        e.preventDefault();
        const target = $(this).data('target');
        $nav_tabs.find('a.nav-link').removeClass('active');
        $(this).addClass('active');
        $tab_content.children('.tab-pane').removeClass('show active');
        $(target).addClass('show active');
    });

    // Manual tab toggling for Mould tab sub-tabs (Data/Totals)
    $mould_nav_tabs.on('click', 'a.nav-link', function (e) {
        e.preventDefault();
        const target = $(this).data('target');
        $mould_nav_tabs.find('a.nav-link').removeClass('active');
        $(this).addClass('active');
        $mould_tab_content.children('.tab-pane').removeClass('show active');
        $(target).addClass('show active');
    });

    // Load data on page load
    load_data();
    load_mould_data();
};

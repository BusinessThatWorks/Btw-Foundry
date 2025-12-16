// Initialize dashboard when DOM is ready
$(document).ready(function () {
    // Initialize dashboard
    initializeDashboard();

    // Set default date range (last 30 days)
    const today = new Date();
    const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));

    $('#from-date').val(thirtyDaysAgo.toISOString().split('T')[0]);
    $('#to-date').val(today.toISOString().split('T')[0]);

    // Event handlers
    $('#refresh-btn').on('click', function () {
        loadDashboardData();
    });

    $('#export-btn').on('click', function () {
        exportData();
    });

    // Load initial data
    loadDashboardData();
});

function initializeDashboard() {
    // Initialize table container
    $('#item-history-table').html('<div class="loading">Loading data...</div>');
}

function loadDashboardData() {
    const filters = getFilters();

    // Show loading state
    showLoadingState();

    // Fetch data from report
    frappe.call({
        method: 'frappe.desk.query_report.run',
        args: {
            report_name: 'Item History Report',
            filters: JSON.stringify(filters)
        },
        callback: function (response) {
            hideLoadingState();
            console.log('Full response:', response); // Debug log

            if (response && response.message) {
                // Try different possible data locations
                let data = [];
                if (response.message.result) {
                    data = response.message.result;
                } else if (response.message.data) {
                    data = response.message.data;
                } else if (Array.isArray(response.message)) {
                    data = response.message;
                }

                console.log('Item History Data:', data); // Debug log
                console.log('Data type:', typeof data);
                console.log('Is array:', Array.isArray(data));

                if (data && Array.isArray(data) && data.length > 0) {
                    renderDashboard(data);
                } else {
                    console.log('No valid data found in response');
                    $('#item-history-table').html('<div class="text-center text-muted">No data found for the selected criteria</div>');
                }
            } else {
                console.log('No message in response:', response);
                $('#item-history-table').html('<div class="text-center text-muted">No data found for the selected criteria</div>');
            }
        },
        error: function (err) {
            hideLoadingState();
            console.error('Item History Dashboard Error:', err);
            frappe.msgprint(__('Error loading data: ') + (err.message || err));
        }
    });
}

function getFilters() {
    return {
        from_date: $('#from-date').val(),
        to_date: $('#to-date').val(),
        item_code: $('#item-code').val(),
        item_name: $('#item-name').val()
    };
}

function showLoadingState() {
    $('#total-items').text('Loading...');
    $('#items-with-changes').text('Loading...');
    $('#total-changes').text('Loading...');
    $('#avg-change-percent').text('Loading...');
    $('#item-history-table').html('<div class="loading">Loading data...</div>');
}

function hideLoadingState() {
    // Clear loading states but keep the elements
}

function renderDashboard(data) {
    console.log('renderDashboard called with data:', data);
    console.log('Data length:', data ? data.length : 'undefined');

    if (!data || !Array.isArray(data) || data.length === 0) {
        console.log('No valid data to render');
        $('#item-history-table').html('<div class="text-center text-muted">No data found</div>');
        return;
    }

    // Simple table display
    let tableHtml = '<table class="table table-striped table-bordered"><thead><tr>';
    tableHtml += '<th>Item Code</th><th>Item Name</th><th>Creation Date</th><th>Current Rate</th>';
    tableHtml += '<th>Version Date</th><th>Previous Rate</th><th>Change Amount</th><th>Change %</th><th>Modified By</th>';
    tableHtml += '</tr></thead><tbody>';

    data.forEach(row => {
        tableHtml += '<tr>';
        tableHtml += '<td>' + (row.item_code || '') + '</td>';
        tableHtml += '<td>' + (row.item_name || '') + '</td>';
        tableHtml += '<td>' + (row.creation || '') + '</td>';
        tableHtml += '<td>' + (row.current_valuation_rate || 0) + '</td>';
        tableHtml += '<td>' + (row.version_date || '') + '</td>';
        tableHtml += '<td>' + (row.previous_valuation_rate || 0) + '</td>';
        tableHtml += '<td>' + (row.change_amount || 0) + '</td>';
        tableHtml += '<td>' + (row.change_percentage || 0) + '</td>';
        tableHtml += '<td>' + (row.modified_by || '') + '</td>';
        tableHtml += '</tr>';
    });

    tableHtml += '</tbody></table>';

    console.log('Looking for #item-history-table element:', $('#item-history-table').length);
    console.log('Element found:', $('#item-history-table')[0]);

    if ($('#item-history-table').length === 0) {
        console.log('item-history-table element not found, creating it');
        // Create the element if it doesn't exist
        $('body').append('<div id="item-history-table" style="padding: 20px;"></div>');
    }

    $('#item-history-table').html(tableHtml);
    console.log('Table rendered with', data.length, 'rows');
    console.log('Table HTML length:', tableHtml.length);
    console.log('Element HTML after setting:', $('#item-history-table').html().length);
}

function calculateSummary(data) {
    const totalItems = new Set(data.map(row => row.item_code)).size;
    const itemsWithChanges = new Set(data.filter(row => row.change_amount !== 0).map(row => row.item_code)).size;
    const totalChanges = data.filter(row => row.change_amount !== 0).length;
    const avgChangePercent = data.length > 0 ?
        data.reduce((sum, row) => sum + (row.change_percentage || 0), 0) / data.length : 0;

    return {
        totalItems,
        itemsWithChanges,
        totalChanges,
        avgChangePercent: Math.round(avgChangePercent * 100) / 100
    };
}

function updateSummaryCards(summary) {
    console.log('Updating summary cards with:', summary);
    console.log('Total items element:', $('#total-items').length);
    console.log('Items with changes element:', $('#items-with-changes').length);

    $('#total-items').text(summary.totalItems);
    $('#items-with-changes').text(summary.itemsWithChanges);
    $('#total-changes').text(summary.totalChanges);
    $('#avg-change-percent').text(summary.avgChangePercent + '%');

    console.log('Summary cards updated');
}

function renderValuationChart(data) {
    let container = document.getElementById('valuation-chart');
    if (!container) {
        // Try to find or create the container
        const chartsSection = document.querySelector('.charts-section');
        if (chartsSection) {
            // Create the container if it doesn't exist
            const chartDiv = document.createElement('div');
            chartDiv.id = 'valuation-chart';
            chartDiv.style.height = '300px';
            chartDiv.style.width = '100%';
            chartsSection.querySelector('.col-md-6:first-child .card-body').appendChild(chartDiv);
            container = chartDiv;
        } else {
            console.error('Charts section not found');
            return;
        }
    }

    // Clear previous content
    container.innerHTML = '';

    if (!data || data.length === 0) {
        container.innerHTML = '<div class="text-center text-muted">No data for chart</div>';
        return;
    }

    // Group data by date for time series
    const chartData = {};

    data.forEach(row => {
        if (row.version_date) {
            const date = row.version_date;
            if (!chartData[date]) {
                chartData[date] = {
                    date: date,
                    items: 0,
                    avgRate: 0,
                    totalRate: 0
                };
            }
            chartData[date].items++;
            chartData[date].totalRate += row.previous_valuation_rate || 0;
        }
    });

    // Calculate average rates
    Object.values(chartData).forEach(point => {
        point.avgRate = point.totalRate / point.items;
    });

    const chartDataArray = Object.values(chartData).sort((a, b) => new Date(a.date) - new Date(b.date));

    if (chartDataArray.length === 0) {
        container.innerHTML = '<div class="text-center text-muted">No chart data available</div>';
        return;
    }

    try {
        const chart = new frappe.Chart(container, {
            data: {
                labels: chartDataArray.map(d => d.date),
                datasets: [{
                    name: 'Average Valuation Rate',
                    values: chartDataArray.map(d => d.avgRate)
                }]
            },
            type: 'line',
            height: 250,
            colors: ['#007bff']
        });
    } catch (error) {
        console.error('Error rendering valuation chart:', error);
        container.innerHTML = '<div class="text-center text-muted">Error rendering chart</div>';
    }
}

function renderChangeDistributionChart(data) {
    let container = document.getElementById('change-distribution-chart');
    if (!container) {
        // Try to find or create the container
        const chartsSection = document.querySelector('.charts-section');
        if (chartsSection) {
            // Create the container if it doesn't exist
            const chartDiv = document.createElement('div');
            chartDiv.id = 'change-distribution-chart';
            chartDiv.style.height = '300px';
            chartDiv.style.width = '100%';
            chartsSection.querySelector('.col-md-6:last-child .card-body').appendChild(chartDiv);
            container = chartDiv;
        } else {
            console.error('Charts section not found');
            return;
        }
    }

    // Clear previous content
    container.innerHTML = '';

    if (!data || data.length === 0) {
        container.innerHTML = '<div class="text-center text-muted">No data for chart</div>';
        return;
    }

    // Categorize changes
    const categories = {
        'Increase (>10%)': 0,
        'Increase (1-10%)': 0,
        'No Change': 0,
        'Decrease (1-10%)': 0,
        'Decrease (>10%)': 0
    };

    data.forEach(row => {
        const changePercent = row.change_percentage || 0;
        if (changePercent > 10) {
            categories['Increase (>10%)']++;
        } else if (changePercent > 0) {
            categories['Increase (1-10%)']++;
        } else if (changePercent === 0) {
            categories['No Change']++;
        } else if (changePercent > -10) {
            categories['Decrease (1-10%)']++;
        } else {
            categories['Decrease (>10%)']++;
        }
    });

    try {
        const chart = new frappe.Chart(container, {
            data: {
                labels: Object.keys(categories),
                datasets: [{
                    name: 'Number of Changes',
                    values: Object.values(categories)
                }]
            },
            type: 'pie',
            height: 250,
            colors: ['#28a745', '#20c997', '#6c757d', '#fd7e14', '#dc3545']
        });
    } catch (error) {
        console.error('Error rendering change distribution chart:', error);
        container.innerHTML = '<div class="text-center text-muted">Error rendering chart</div>';
    }
}

function renderDataTable(data) {
    console.log('renderDataTable called with data:', data);
    console.log('Data type:', typeof data);
    console.log('Data length:', data ? data.length : 'undefined');
    console.log('Is array:', Array.isArray(data));
    console.log('Table container exists:', $('#item-history-table').length);

    if (!data || !Array.isArray(data) || data.length === 0) {
        console.log('No valid data for table');
        $('#item-history-table').html('<div class="text-center text-muted">No data found</div>');
        return;
    }

    const $table = $(`
		<div class="data-table" style="width: 100%; margin-bottom: 30px;">
			<table style="width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
				<thead>
					<tr>
						<th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Item Code')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Item Name')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Creation Date')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Current Rate')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Version Date')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Previous Rate')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Change Amount')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Change %')}</th>
						<th style="background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6;">${__('Modified By')}</th>
					</tr>
				</thead>
				<tbody>
				</tbody>
			</table>
		</div>
	`);

    const $tbody = $table.find('tbody');

    console.log('About to iterate over data, length:', data.length);

    data.forEach((row, index) => {
        console.log(`Processing row ${index}:`, row);
        const changeAmount = row.change_amount || 0;
        const changePercent = row.change_percentage || 0;
        const changeClass = changeAmount > 0 ? 'positive-change' : changeAmount < 0 ? 'negative-change' : '';

        const $tr = $(`
			<tr style="border-bottom: 1px solid #e9ecef;">
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">
					<a href="/app/item/${row.item_code}" class="link-cell" style="color: #007bff; text-decoration: none; cursor: pointer;">${row.item_code || ''}</a>
				</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.item_name || ''}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.creation, { fieldtype: 'Date' })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.current_valuation_rate || 0, { fieldtype: 'Currency', precision: 2 })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${frappe.format(row.version_date, { fieldtype: 'Date' })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right;">${frappe.format(row.previous_valuation_rate || 0, { fieldtype: 'Currency', precision: 2 })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right; white-space: nowrap;" class="${changeClass}">${frappe.format(changeAmount, { fieldtype: 'Currency', precision: 2 })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: right; white-space: nowrap;" class="${changeClass}">${frappe.format(changePercent, { fieldtype: 'Percent', precision: 2 })}</td>
				<td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057; text-align: left;">${row.modified_by || ''}</td>
			</tr>
		`);
        $tbody.append($tr);
    });

    console.log('Setting table HTML');
    $('#item-history-table').html($table);
    console.log('Table HTML set, length:', $('#item-history-table').html().length);
}

function exportData() {
    const filters = getFilters();

    // Create a form to submit the export request
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/api/method/frappe.desk.query_report.export_query';
    form.target = '_blank';

    // Add form fields
    const fields = {
        report_name: 'Item History Report',
        filters: JSON.stringify(filters),
        file_format_type: 'Excel'
    };

    Object.keys(fields).forEach(key => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = fields[key];
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}



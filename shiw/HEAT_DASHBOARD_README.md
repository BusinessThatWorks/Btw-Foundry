# Heat Dashboard

A comprehensive dashboard for monitoring Heat-related metrics including Total Charge Mix, Liquid Balance, and Burning Loss.

## Features

- **Number Cards Display**: Visual representation of key metrics
  - Total Charge Mix (Kg) - Blue indicator
  - Liquid Balance - Black indicator
  - Burning Loss - Green indicator

- **Dynamic Date Filtering**: 
  - From Date and To Date filters
  - Auto-updates when date range changes
  - Defaults to current month

- **Real-time Data**: 
  - Aggregates data from Heat doctype
  - Updates based on selected date range
  - Shows detailed data table

## Access Methods

### Method 1: Direct URL Access
Navigate to: `/heat-dashboard`

### Method 2: From Frappe Desk
1. Go to **Desk** in your Frappe/ERPNext system
2. Navigate to **Pages** 
3. Look for **"Heat Dashboard"**
4. Click to open

### Method 3: From Reports Menu
1. Go to **Reports** 
2. Find **"Number card Heat report"**
3. This provides the same data in report format

## Usage

1. **Select Date Range**: Choose From Date and To Date
2. **View Number Cards**: See aggregated metrics at a glance
3. **Review Details**: Check the detailed data table below
4. **Auto-refresh**: Data updates automatically when dates change

## Technical Details

- **Backend**: Python controller (`heat_dashboard.py`)
- **Frontend**: HTML template with responsive design
- **Data Source**: Heat doctype aggregation
- **Styling**: Custom CSS with modern design
- **Responsive**: Works on desktop and mobile devices

## Files Created

- `shiw/shiw/pages/heat_dashboard.py` - Main controller
- `shiw/shiw/pages/heat_dashboard.html` - Web template
- `shiw/shiw/pages/heat_dashboard.js` - JavaScript functionality
- `shiw/shiw/pages/heat_dashboard_desk.py` - Desk version controller
- `shiw/shiw/pages/heat_dashboard_desk.html` - Desk template
- `shiw/fixtures/heat_dashboard_page.json` - Page registration

## Dependencies

- Existing `number_card_heat_report` report
- Heat doctype with required fields
- Frappe framework

## Permissions

The dashboard inherits permissions from the underlying Heat doctype and report.

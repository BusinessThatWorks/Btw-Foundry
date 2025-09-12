# Procurement Tracker Dashboard

## Overview
The Procurement Tracker Dashboard provides a comprehensive view of all procurement activities in your system. It's designed similar to the Unified Dashboard but focused specifically on procurement processes.

## Features

### 5 Main Sections:

1. **📊 Overview Section**
   - Total Material Requests count
   - Total Purchase Orders count  
   - Total Purchase Receipts count
   - Total Purchase Invoices count
   - Total Procurement Value (sum of all transactions)

2. **📋 Material Request Section**
   - Number cards showing status breakdown (Approved, Rejected, Draft, etc.)
   - Filters: Date range, Status, ID, Item Name
   - Detailed table with Material Request data

3. **🛒 Purchase Order Section**
   - Number cards showing status breakdown
   - Filters: Date range, Status, ID, Item Name, Supplier
   - Detailed table with Purchase Order data

4. **🚚 Purchase Receipt Section**
   - Number cards showing status breakdown
   - Filters: Date range, Status, ID, Item Name, Supplier
   - Detailed table with Purchase Receipt data

5. **🧾 Purchase Invoice Section**
   - Number cards showing status breakdown
   - Filters: Date range, Status, ID, Item Name, Supplier
   - Detailed table with Purchase Invoice data

## How to Access

### Method 1: Direct Dashboard Access
Navigate to: `/app/procurement-tracker-dashboard`

### Method 2: Landing Page
Visit: `/app/www/procurement_tracker_dashboard.html`

## Key Features

✅ **Number Cards**: Each section shows status-based number cards (just like unified dashboard)
✅ **Advanced Filtering**: Date range, status, ID, item name, and supplier filters
✅ **Detailed Tables**: Below each section's number cards, showing relevant data
✅ **Responsive Design**: Modern UI with tabbed interface
✅ **Export Functionality**: Export to procurement tracker report
✅ **Status Indicators**: Color-coded status badges and indicators
✅ **Direct Links**: Click on any document ID to open the actual document

## Technical Details

- **Frontend**: JavaScript with Frappe UI components
- **Data Source**: Uses existing Frappe client methods and the "New Procurement Tracker" report
- **No Custom Backend**: Relies on standard Frappe APIs for reliability
- **Responsive**: Works on desktop and mobile devices

## Troubleshooting

### If the dashboard doesn't load:
1. Make sure you have the required permissions (System Manager, Purchase Manager, or Purchase User)
2. Check that the "New Procurement Tracker" report exists and is working
3. Verify that you have Material Request, Purchase Order, Purchase Receipt, and Purchase Invoice data

### If filters don't work:
1. Ensure you have selected both From Date and To Date
2. Check that the date range contains data
3. Verify that the status values exist in your system

## Data Requirements

The dashboard works with standard Frappe procurement documents:
- Material Request (with workflow_state field)
- Purchase Order (with workflow_state field)
- Purchase Receipt (with workflow_state field)
- Purchase Invoice (with workflow_state field)

## Customization

To customize the dashboard:
1. Edit the JavaScript file: `shiw/shiw/page/procurement_tracker_dashboard/procurement_tracker_dashboard.js`
2. Modify the HTML landing page: `shiw/www/procurement_tracker_dashboard.html`
3. Update the page configuration: `shiw/shiw/page/procurement_tracker_dashboard/procurement_tracker_dashboard.json`

## Support

For issues or questions about the Procurement Tracker Dashboard, please check:
1. Browser console for JavaScript errors
2. Frappe logs for backend errors
3. Ensure all required permissions are granted






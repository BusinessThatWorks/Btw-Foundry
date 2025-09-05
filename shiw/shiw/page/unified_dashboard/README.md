# Unified Foundry Dashboard

A comprehensive dashboard that combines Heat and Mould process metrics in a single, unified interface following Frappe best practices.

## Features

### 🎯 **Overview Tab**
- **Total Production Units**: Combined count of Heat and Mould batches
- **Total Production Weight**: Combined cast and bunch weight in Kg
- **Overall Efficiency**: Liquid balance efficiency percentage
- **Overall Burning Loss**: Heat process burning loss percentage
- **Average Mould Yield**: Average yield across all mould types
- **Total Tooling Used**: Total tooling across all mould batches

### 🔥 **Heat Process Tab**
- **Total Number of Heat**: Integer count (no decimals)
- **Total Charge Mix (Kg)**: Float with 2 decimal places
- **Liquid Balance**: Float with 2 decimal places
- **Burning Loss (%)**: Percentage with 2 decimal places

### 🧱 **Mould Process Tab**
- **Total Number of Batches**: Integer count
- **Total Cast Weight**: Float with 3 decimal places
- **Total Bunch Weight**: Float with 3 decimal places
- **Average Yield**: Float with 2 decimal places
- **Total Number of Tooling**: Integer count

## Technical Implementation

### File Structure
```
shiw/shiw/page/unified_dashboard/
├── __init__.py                    # Module initialization
├── unified_dashboard.json         # Page configuration
├── unified_dashboard.py           # Backend logic
├── unified_dashboard.js           # Frontend logic
├── unified_dashboard.html         # HTML template
└── README.md                      # This file
```

### Backend Architecture

#### Key Functions
- `get_unified_dashboard_data()`: Main data aggregation function
- `get_heat_dashboard_data()`: Heat process data retrieval
- `get_mould_dashboard_data()`: Mould process data retrieval
- `get_overview_data()`: Combined metrics calculation
- `export_data()`: Data export functionality

#### Error Handling
- Comprehensive try-catch blocks
- Proper error logging with `frappe.log_error()`
- User-friendly error messages
- Graceful degradation on failures

### Frontend Architecture

#### State Management
- Centralized state object for all dashboard data
- Proper event handling and state updates
- Responsive UI updates

#### Component Structure
- **Filter Bar**: Date range, furnace, and batch type filters
- **Tab Navigation**: Overview, Heat, and Mould tabs
- **Card Grid**: Responsive grid layout for KPI cards
- **Loading States**: Proper loading indicators

#### Styling
- Modern, responsive design
- CSS Grid for card layout
- Smooth transitions and hover effects
- Mobile-friendly interface

## Usage

### Accessing the Dashboard
1. Navigate to the dashboard page in Frappe
2. Select date range (required)
3. Optionally filter by furnace or batch type
4. Click "Refresh" to load data
5. Switch between tabs to view different metrics

### Filtering Options
- **Date Range**: From Date and To Date (required)
- **Furnace**: Filter by specific furnace (optional)
- **Batch Type**: Filter by mould batch type (optional)

### Export Functionality
- Click "Export" button to download data
- Exports all dashboard data in JSON format
- Includes report metadata and filters applied

## Best Practices Implemented

### Frappe Standards
- ✅ Proper page registration and lifecycle management
- ✅ Use of `frappe.ui.make_app_page()` for page creation
- ✅ Consistent error handling with `frappe.log_error()`
- ✅ Proper use of `@frappe.whitelist()` decorators
- ✅ Internationalization with `__()` function
- ✅ Proper field control creation with `frappe.ui.form.make_control()`

### Code Quality
- ✅ Modular function design
- ✅ Comprehensive error handling
- ✅ Proper logging and debugging
- ✅ Clean separation of concerns
- ✅ Responsive design principles
- ✅ Accessibility considerations

### Performance
- ✅ Efficient data aggregation
- ✅ Minimal DOM manipulation
- ✅ Proper event delegation
- ✅ Optimized CSS with modern layouts

## Data Flow

1. **User Interaction**: User selects filters and clicks refresh
2. **Frontend Request**: JavaScript calls backend API
3. **Data Aggregation**: Backend fetches data from existing reports
4. **Processing**: Data is combined and formatted
5. **Response**: Formatted data returned to frontend
6. **Rendering**: Cards are dynamically created and displayed

## Dependencies

### Backend Dependencies
- Existing Heat report: `shiw.report.number_card_heat_report`
- Existing Mould report: `shiw.report.number_card_mould_report`
- Frappe framework utilities

### Frontend Dependencies
- jQuery (provided by Frappe)
- Font Awesome icons
- Bootstrap CSS classes (for styling)

## Configuration

### Page Configuration (`unified_dashboard.json`)
- Standard Frappe page configuration
- Proper role assignments
- Module association

### Permissions
- **System Manager**: Full access
- **Foundry- SHIW**: Full access

## Troubleshooting

### Common Issues
1. **No data displayed**: Check date range and filters
2. **Loading errors**: Check browser console for JavaScript errors
3. **Export failures**: Verify file permissions in `/tmp` directory

### Debug Information
- All API calls are logged to browser console
- Backend errors are logged to Frappe error log
- Loading states provide user feedback

## Future Enhancements

### Planned Features
- [ ] Real-time data updates
- [ ] Advanced filtering options
- [ ] Chart visualizations
- [ ] Custom date ranges (last 7 days, last 30 days, etc.)
- [ ] Email report functionality
- [ ] Mobile app integration

### Performance Optimizations
- [ ] Data caching
- [ ] Lazy loading for large datasets
- [ ] Progressive web app features

## Contributing

When contributing to this dashboard:

1. Follow Frappe coding standards
2. Add proper error handling
3. Include comprehensive logging
4. Test on multiple screen sizes
5. Update this README for new features

## License

This module is part of the SHIW application and follows the same license terms.


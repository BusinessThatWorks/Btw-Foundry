# Production Plan Dashboard

A comprehensive and beautiful dashboard for monitoring production plans, stock levels, and procurement status in the SHIW ERP system.

## Overview

The Production Plan Dashboard provides a modern, interactive interface to view and analyze production plan data with real-time insights into:

- **Production Plan Selection**: Choose from available production plans
- **Item-wise Analysis**: Detailed breakdown of actual vs required quantities
- **Department Filtering**: Filter data by specific departments
- **Stock Status Monitoring**: Track actual stock, open indents, and purchase orders
- **Visual Analytics**: Interactive charts and summary cards
- **Export Capabilities**: Export data for further analysis

## Features

### 🎯 Core Functionality

1. **Production Plan Selection**
   - Dropdown selection of available production plans
   - Automatic data loading when plan is selected
   - Real-time filtering and updates

2. **Advanced Filtering**
   - Filter by Item Code
   - Filter by Department
   - Real-time filter application
   - Clear filter options

3. **Summary Dashboard**
   - 8 key performance indicators
   - Color-coded status indicators
   - Real-time calculations
   - Responsive card layout

4. **Detailed Data Table**
   - Sortable columns
   - Status indicators (Sufficient/Pending/Shortage)
   - Direct links to item details
   - Export functionality

5. **Visual Analytics**
   - Department distribution pie chart
   - Stock status bar chart
   - Interactive Chart.js integration
   - Responsive chart design

### 🎨 UI/UX Features

1. **Modern Design**
   - Gradient headers and buttons
   - Card-based layout
   - Smooth animations and transitions
   - Professional color scheme

2. **Responsive Layout**
   - Mobile-friendly design
   - Adaptive grid layouts
   - Touch-friendly controls
   - Optimized for all screen sizes

3. **Interactive Elements**
   - Hover effects on cards and buttons
   - Loading indicators
   - Error handling with user-friendly messages
   - Smooth transitions

## File Structure

```
shiw/shiw/page/production_plan_page/
├── __init__.py
├── production_plan_page.py      # Backend logic and data processing
├── production_plan_page.html    # Frontend template and styling
├── production_plan_page.js      # Interactive functionality and charts
└── production_plan_page.json    # Page configuration
```

## Technical Implementation

### Backend (Python)

- **Data Integration**: Uses the existing Production Plan Report
- **Summary Calculations**: Real-time KPI calculations
- **Error Handling**: Comprehensive error logging and user feedback
- **Performance**: Optimized database queries

### Frontend (HTML/CSS)

- **Modern CSS**: Flexbox and Grid layouts
- **Responsive Design**: Mobile-first approach
- **Accessibility**: Proper ARIA labels and semantic HTML
- **Performance**: Optimized CSS and minimal dependencies

### JavaScript

- **Interactive Features**: Real-time filtering and updates
- **Chart Integration**: Chart.js for data visualization
- **Error Handling**: User-friendly error messages
- **Export Functionality**: Data export capabilities

## Key Metrics Displayed

1. **Total Items**: Number of items in the production plan
2. **Total Actual Qty**: Current stock quantity
3. **Total Required Qty**: Required quantity for production
4. **Shortage Items**: Items with insufficient quantity
5. **Total Open Indent**: Quantity in pending material requests
6. **Total Open PO**: Quantity in pending purchase orders
7. **Total Combined Stock**: Total available stock (actual + indent + PO)
8. **Departments**: Number of departments involved

## Status Indicators

- **Sufficient**: Actual quantity >= Required quantity (Green)
- **Pending**: Combined stock >= Required quantity (Orange)
- **Shortage**: Combined stock < Required quantity (Red)

## Usage

1. **Access the Dashboard**
   - Navigate to `/production-plan-page` in your browser
   - Or access through the ERPNext interface

2. **Select Production Plan**
   - Choose a production plan from the dropdown
   - Data will automatically load

3. **Apply Filters**
   - Use Item Code filter for specific items
   - Use Department filter for department-specific view
   - Click "Apply Filters" to update the view

4. **Analyze Data**
   - Review summary cards for key metrics
   - Examine detailed table for item-wise data
   - Use charts for visual analysis

5. **Export Data**
   - Use export buttons to download data
   - Export functionality for further analysis

## Customization

### Adding New Metrics

To add new summary metrics, modify the `calculate_summary_stats()` function in `production_plan_page.py`:

```python
def calculate_summary_stats(data):
    # Add your custom calculations here
    custom_metric = calculate_custom_value(data)
    
    summary.append({
        "value": custom_metric,
        "label": _("Custom Metric"),
        "datatype": "Float",
        "indicator": "Blue",
        "description": _("Description of custom metric"),
        "precision": 2
    })
```

### Styling Customization

Modify the CSS in `production_plan_page.html` to customize:
- Colors and themes
- Layout and spacing
- Typography
- Animations

### Chart Customization

Update the chart configuration in `production_plan_page.js`:
- Chart types
- Colors and styling
- Data processing
- Interactive features

## Dependencies

- **Backend**: Frappe Framework, Production Plan Report
- **Frontend**: Chart.js (for data visualization)
- **Styling**: Custom CSS with modern design principles

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance Considerations

- **Lazy Loading**: Charts load only when needed
- **Efficient Queries**: Optimized database queries
- **Caching**: Appropriate data caching strategies
- **Responsive Images**: Optimized for different screen sizes

## Security

- **Input Validation**: All user inputs are validated
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Proper HTML escaping
- **Access Control**: Respects ERPNext permissions

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live data
2. **Advanced Analytics**: More sophisticated chart types
3. **Bulk Actions**: Mass operations on items
4. **Custom Reports**: User-defined report generation
5. **Mobile App**: Native mobile application
6. **API Integration**: REST API for external systems

## Troubleshooting

### Common Issues

1. **Charts Not Loading**
   - Ensure Chart.js is loaded
   - Check browser console for errors
   - Verify data is available

2. **Data Not Updating**
   - Check production plan selection
   - Verify filters are applied correctly
   - Check network connectivity

3. **Styling Issues**
   - Clear browser cache
   - Check CSS conflicts
   - Verify responsive breakpoints

### Debug Mode

Enable debug mode by adding `?debug=1` to the URL for additional logging and error information.

## Support

For technical support or feature requests, please contact the development team or create an issue in the project repository.

---

**Version**: 1.0.0  
**Last Updated**: January 27, 2025  
**Author**: SHIW Development Team


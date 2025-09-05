# Heat Dashboard Troubleshooting Guide

## Issue: Dashboard Not Working

If your Heat Dashboard is not working, follow these steps:

### 1. Check File Structure
Ensure your files are in the correct location:
```
shiw/shiw/page/heat_dashboard/
├── __init__.py
├── heat_dashboard.json
├── heat_dashboard.html
├── heat_dashboard.js
├── heat_dashboard.py
├── heat_dashboard_desk.html
└── heat_dashboard_desk.py
```

### 2. Verify JSON Configuration
Check `heat_dashboard.json`:
- `"page_name": "heat_dashboard"` (with underscore, not hyphen)
- `"doctype": "Page"`
- `"module": "shiw"`

### 3. Check Hooks Configuration
In `shiw/hooks.py`, ensure:
```python
page_js = {"heat_dashboard": "shiw/page/heat_dashboard/heat_dashboard.js"}

fixtures = [
    {"doctype": "Custom Field", "filters": {"module": "shiw"}},
    {"doctype": "Page", "filters": {"module": "shiw"}},
]
```

### 4. Clear Frappe Cache
Run these commands in your Frappe bench:
```bash
bench clear-cache
bench migrate
bench build
```

### 5. Restart Frappe Server
```bash
bench restart
```

### 6. Access Methods

#### Method 1: Direct URL
Navigate to: `http://your-domain/heat-dashboard`

#### Method 2: From Desk
1. Go to **Desk**
2. Navigate to **Pages**
3. Look for **"Heat Dashboard"**
4. Click to open

#### Method 3: From Reports
1. Go to **Reports**
2. Find **"Number card Heat report"**
3. This provides the same data

### 7. Check Browser Console
Open browser developer tools (F12) and check for JavaScript errors.

**Common JavaScript Error**: If you see `Uncaught SyntaxError: Failed to execute 'appendChild' on 'Node': Unexpected identifier 'DOMContentLoaded'`, this means there's inline JavaScript in the HTML template that conflicts with Frappe's page system.

**Fix**: Remove any `<script>` tags from the HTML template and move JavaScript functionality to the `.js` file.

**Common JavaScript Error**: If you see `Cannot set properties of undefined (setting 'on_page_load')`, this means the page name in JavaScript doesn't match the page name in the JSON file.

**Fix**: Ensure the page name in `frappe.pages['page-name']` matches the `"name"` field in the JSON file (use hyphens, not underscores).

### 8. Check Frappe Logs
Look for errors in:
```bash
bench tail-logs
```

### 9. Verify Python Files
Test compilation:
```bash
python3 -m py_compile shiw/shiw/page/heat_dashboard/heat_dashboard.py
python3 -m py_compile shiw/shiw/page/heat_dashboard/heat_dashboard_desk.py
```

### 10. Common Issues

#### Issue: Page not found
- Check if the page is properly registered in Frappe
- Verify the route in the JSON file

#### Issue: No data displayed
- Check if Heat doctype has data
- Verify date range selection
- Check if the report module is working

#### Issue: JavaScript errors
- Check if the JS file path is correct in hooks.py
- Verify the JS file exists and is valid

### 11. Test the Report Separately
First test if the underlying report works:
1. Go to **Reports**
2. Run **"Number card Heat report"**
3. If this works, the dashboard should work too

### 12. Permissions
Ensure your user has:
- Read access to Heat doctype
- Access to the Page doctype
- Proper role assignments

## Still Not Working?

If the dashboard still doesn't work after following these steps:

1. Check Frappe version compatibility
2. Verify all dependencies are installed
3. Check if there are any conflicting customizations
4. Try creating a simple test page first
5. Contact support with specific error messages

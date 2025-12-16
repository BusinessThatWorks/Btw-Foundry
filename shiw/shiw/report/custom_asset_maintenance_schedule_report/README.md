# Custom Asset Maintenance Schedule Report

## Overview
This report provides a comprehensive view of asset maintenance schedules and their associated tasks. It displays information from both the Asset Maintenance doctype and its child table Asset Maintenance Task.

## Features
- **Asset Information**: Shows asset name, category, item code, and item name
- **Maintenance Team Details**: Displays maintenance team and manager information
- **Task Details**: Shows maintenance tasks with their status, type, and scheduling information
- **Date Filtering**: Filter by date range to view maintenance schedules for specific periods
- **Status Highlighting**: Color-coded status indicators for easy identification
- **Overdue Detection**: Automatically highlights overdue maintenance tasks

## Fields Included

### From Asset Maintenance:
- Asset Name
- Asset Category
- Item Code
- Item Name
- Maintenance Team
- Maintenance Manager Name

### From Asset Maintenance Task (Child Table):
- Maintenance Task
- Maintenance Status
- Maintenance Type
- Start Date
- End Date
- Periodicity
- Assign To Name
- Next Due Date
- Last Completion Date

## Filters Available
- **From Date**: Start date for the report period
- **To Date**: End date for the report period
- **Asset Name**: Filter by specific asset
- **Asset Category**: Filter by asset category
- **Maintenance Team**: Filter by maintenance team
- **Maintenance Status**: Filter by task status (Pending, Completed, Overdue, Cancelled)
- **Maintenance Type**: Filter by maintenance type (Preventive, Corrective, Breakdown)

## Usage
1. Navigate to Reports > Custom > Custom Asset Maintenance Schedule Report
2. Set your desired date range and filters
3. Click "Update" to generate the report
4. The report will show all maintenance tasks within the specified criteria

## Color Coding
- **Red**: Overdue maintenance tasks
- **Green**: Completed maintenance tasks
- **Orange**: Pending maintenance tasks

## Technical Details
- **Report Type**: Script Report
- **Module**: shiw
- **Doctype**: Asset Maintenance
- **Child Table**: Asset Maintenance Task
- **Roles**: System Manager, Maintenance User

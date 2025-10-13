# Custom Asset Maintenance Log Report

## Overview
This report provides a comprehensive view of asset maintenance logs and their associated tasks. It displays detailed information from the Asset Maintenance Log doctype, including maintenance activities, task assignments, and completion status.

## Features
- **Asset Information**: Shows asset maintenance reference, asset name, item code, and item name
- **Task Details**: Displays task information including task name, maintenance type, and periodicity
- **Date Tracking**: Shows due dates and completion dates for maintenance activities
- **Status Monitoring**: Tracks maintenance status with color-coded indicators
- **Assignment Details**: Shows assigned personnel and their contact information
- **Action Documentation**: Records actions performed during maintenance

## Fields Included

### From Asset Maintenance Log:
- **Asset Maintenance**: Reference to the parent Asset Maintenance document
- **Asset Name**: Name of the asset being maintained
- **Item Code**: Item code of the asset
- **Item Name**: Name of the item/asset
- **Task**: Reference to the Asset Maintenance Task
- **Task Name**: Name of the maintenance task
- **Maintenance Type**: Type of maintenance (Preventive, Corrective, Breakdown)
- **Periodicity**: Frequency of maintenance
- **Due Date**: Scheduled due date for maintenance
- **Completion Date**: Actual completion date
- **Description**: Description of the maintenance activity
- **Maintenance Status**: Current status (Pending, Completed, Overdue, Cancelled)
- **Assign To Name**: Name of the person assigned to the task
- **Task Assignee Email**: Email of the assigned person
- **Actions Performed**: Detailed actions taken during maintenance

## Filters Available
- **From Date**: Start date for the report period
- **To Date**: End date for the report period
- **Asset Name**: Filter by specific asset
- **Item Code**: Filter by specific item code
- **Maintenance Type**: Filter by maintenance type (Preventive, Corrective, Breakdown)
- **Maintenance Status**: Filter by task status (Pending, Completed, Overdue, Cancelled)
- **Assign To Name**: Filter by assigned personnel

## Usage
1. Navigate to Reports > Custom > Custom Asset Maintenance Log Report
2. Set your desired date range and filters
3. Click "Update" to generate the report
4. The report will show all maintenance log entries within the specified criteria

## Color Coding
- **Red**: Overdue maintenance tasks and overdue due dates
- **Green**: Completed maintenance tasks
- **Orange**: Pending maintenance tasks

## Export Features
- Export to Excel functionality available
- Custom export button for easy data extraction

## Technical Details
- **Report Type**: Script Report
- **Module**: shiw
- **Reference Doctype**: Asset Maintenance Log
- **Roles**: System Manager, Maintenance User

## Dependencies
- Asset Maintenance Log doctype must exist in the system
- Asset Maintenance doctype (for parent reference)
- Asset Maintenance Task doctype (for task reference)
- Asset doctype (for asset information)
- Item doctype (for item information)

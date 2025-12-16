# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters=None):
	columns = [
		{
			"label": "Asset Maintenance",
			"fieldname": "asset_maintenance",
			"fieldtype": "Link",
			"options": "Asset Maintenance",
			"width": 150,
		},
		{
			"label": "Asset Name",
			"fieldname": "asset_name",
			"fieldtype": "Link",
			"options": "Asset",
			"width": 150,
		},
		{
			"label": "Item Code",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{
			"label": "Item Name",
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Task",
			"fieldname": "task",
			"fieldtype": "Link",
			"options": "Asset Maintenance Task",
			"width": 150,
		},
		{
			"label": "Task Name",
			"fieldname": "task_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Maintenance Type",
			"fieldname": "maintenance_type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Periodicity",
			"fieldname": "periodicity",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": "Due Date",
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Completion Date",
			"fieldname": "completion_date",
			"fieldtype": "Date",
			"width": 150,
		},
		{
			"label": "Description",
			"fieldname": "description",
			"fieldtype": "Small Text",
			"width": 250,
		},
		{
			"label": "Maintenance Status",
			"fieldname": "maintenance_status",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Assign To Name",
			"fieldname": "assign_to_name",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Task Assignee Email",
			"fieldname": "task_assignee_email",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": "Actions Performed",
			"fieldname": "actions_performed",
			"fieldtype": "Small Text",
			"width": 250,
		},
	]
	return columns


def get_data(filters):
	data = []

	try:
		# Normalize filters
		filters = filters or {}
		fd = filters.get("from_date")
		td = filters.get("to_date")
		if fd:
			filters["from_date"] = str(getdate(fd))
		if td:
			filters["to_date"] = str(getdate(td))

		# Build the main query for Asset Maintenance Log
		query = """
			SELECT 
				aml.asset_maintenance,
				aml.asset_name,
				aml.item_code,
				aml.item_name,
				aml.task,
				aml.task_name,
				aml.maintenance_type,
				aml.periodicity,
				aml.due_date,
				aml.completion_date,
				aml.description,
				aml.maintenance_status,
				aml.assign_to_name,
				aml.task_assignee_email,
				aml.actions_performed
			FROM `tabAsset Maintenance Log` aml
			WHERE aml.docstatus != 2
		"""

		# Add date filters if provided
		if filters.get("from_date") and filters.get("to_date"):
			query += " AND aml.due_date BETWEEN %(from_date)s AND %(to_date)s"

		# Add optional filters
		if filters.get("asset_name"):
			query += " AND aml.asset_name = %(asset_name)s"
		if filters.get("item_code"):
			query += " AND aml.item_code = %(item_code)s"
		if filters.get("maintenance_type"):
			query += " AND aml.maintenance_type = %(maintenance_type)s"
		if filters.get("maintenance_status"):
			query += " AND aml.maintenance_status = %(maintenance_status)s"
		if filters.get("assign_to_name"):
			query += " AND aml.assign_to_name = %(assign_to_name)s"

		query += " ORDER BY aml.asset_name, aml.due_date, aml.idx"

		# Execute the query
		data = frappe.db.sql(query, filters, as_dict=True)

		# Convert None values to empty strings for text fields
		for row in data:
			row["asset_maintenance"] = row["asset_maintenance"] or ""
			row["asset_name"] = row["asset_name"] or ""
			row["item_code"] = row["item_code"] or ""
			row["item_name"] = row["item_name"] or ""
			row["task"] = row["task"] or ""
			row["task_name"] = row["task_name"] or ""
			row["maintenance_type"] = row["maintenance_type"] or ""
			row["periodicity"] = row["periodicity"] or ""
			row["description"] = row["description"] or ""
			row["maintenance_status"] = row["maintenance_status"] or ""
			row["assign_to_name"] = row["assign_to_name"] or ""
			row["task_assignee_email"] = row["task_assignee_email"] or ""
			row["actions_performed"] = row["actions_performed"] or ""

		frappe.log_error(
			f"Custom Asset Maintenance Log Report: Retrieved {len(data)} records",
			"Asset Maintenance Log Report",
		)

	except Exception as e:
		frappe.log_error(
			f"Error in Custom Asset Maintenance Log Report: {str(e)}", "Asset Maintenance Log Report Error"
		)
		frappe.msgprint(f"Error generating report: {str(e)}")

	return data

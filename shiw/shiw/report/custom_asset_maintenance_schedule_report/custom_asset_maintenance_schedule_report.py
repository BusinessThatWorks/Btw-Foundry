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
			"label": "Asset Name",
			"fieldname": "asset_name",
			"fieldtype": "Link",
			"options": "Asset",
			"width": 150,
		},
		{
			"label": "Asset Category",
			"fieldname": "asset_category",
			"fieldtype": "Link",
			"options": "Asset Category",
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
			"label": "Maintenance Team",
			"fieldname": "maintenance_team",
			"fieldtype": "Link",
			"options": "Asset Maintenance Team",
			"width": 150,
		},
		{
			"label": "Maintenance Manager",
			"fieldname": "maintenance_manager_name",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": "Maintenance Task",
			"fieldname": "maintenance_task",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Maintenance Status",
			"fieldname": "maintenance_status",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Maintenance Type",
			"fieldname": "maintenance_type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Start Date",
			"fieldname": "start_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "End Date",
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Periodicity",
			"fieldname": "periodicity",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": "Assign To",
			"fieldname": "assign_to_name",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": "Next Due Date",
			"fieldname": "next_due_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Last Completion Date",
			"fieldname": "last_completion_date",
			"fieldtype": "Date",
			"width": 150,
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

		# Helper to build query by parent table name
		def build_query(parent_table_alias: str, parent_table_sql: str) -> str:
			return f"""
				SELECT 
					{parent_table_alias}.asset_name,
					{parent_table_alias}.asset_category,
					{parent_table_alias}.item_code,
					{parent_table_alias}.item_name,
					{parent_table_alias}.maintenance_team,
					{parent_table_alias}.maintenance_manager_name,
					amt.maintenance_task,
					amt.maintenance_status,
					amt.maintenance_type,
					amt.start_date,
					amt.end_date,
					amt.periodicity,
					amt.assign_to_name,
					amt.next_due_date,
					amt.last_completion_date
				FROM {parent_table_sql} {parent_table_alias}
				INNER JOIN `tabAsset Maintenance Task` amt ON amt.parent = {parent_table_alias}.name
				WHERE {parent_table_alias}.docstatus != 2
			"""

		# Use Asset Maintenance as the primary parent table
		parent_table_label = "Asset Maintenance"
		parent_table_sql = "`tabAsset Maintenance`"
		alias = "am"
		query = build_query(alias, parent_table_sql)

		# Constrain by date range only if both dates are provided
		if filters.get("from_date") and filters.get("to_date"):
			query += " AND amt.start_date BETWEEN %(from_date)s AND %(to_date)s"

		# Optional filters
		if filters.get("asset_name"):
			query += f" AND {alias}.asset_name = %(asset_name)s"
		if filters.get("asset_category"):
			query += f" AND {alias}.asset_category = %(asset_category)s"
		if filters.get("maintenance_team"):
			query += f" AND {alias}.maintenance_team = %(maintenance_team)s"
		if filters.get("maintenance_status"):
			query += " AND amt.maintenance_status = %(maintenance_status)s"
		if filters.get("maintenance_type"):
			query += " AND amt.maintenance_type = %(maintenance_type)s"

		query += f" ORDER BY {alias}.asset_name, amt.start_date, amt.idx"

		# Execute the query; fallback if Asset Maintenance table is missing
		try:
			data = frappe.db.sql(query, filters, as_dict=True)
		except Exception as ex:
			msg = str(ex)
			if "doesn't exist" in msg and "Asset Maintenance" in msg:
				# Retry with Asset Maintenance Schedule
				parent_table_label = "Asset Maintenance Schedule"
				parent_table_sql = "`tabAsset Maintenance Schedule`"
				alias = "ams"
				query = build_query(alias, parent_table_sql)
				if filters.get("from_date") and filters.get("to_date"):
					query += " AND amt.start_date BETWEEN %(from_date)s AND %(to_date)s"
				if filters.get("asset_name"):
					query += f" AND {alias}.asset_name = %(asset_name)s"
				if filters.get("asset_category"):
					query += f" AND {alias}.asset_category = %(asset_category)s"
				if filters.get("maintenance_team"):
					query += f" AND {alias}.maintenance_team = %(maintenance_team)s"
				if filters.get("maintenance_status"):
					query += " AND amt.maintenance_status = %(maintenance_status)s"
				if filters.get("maintenance_type"):
					query += " AND amt.maintenance_type = %(maintenance_type)s"
				query += f" ORDER BY {alias}.asset_name, amt.start_date, amt.idx"
				data = frappe.db.sql(query, filters, as_dict=True)
			else:
				raise

		# Convert None values to empty strings for text fields
		for row in data:
			row["asset_name"] = row["asset_name"] or ""
			row["asset_category"] = row["asset_category"] or ""
			row["item_code"] = row["item_code"] or ""
			row["item_name"] = row["item_name"] or ""
			row["maintenance_team"] = row["maintenance_team"] or ""
			row["maintenance_manager_name"] = row["maintenance_manager_name"] or ""
			row["maintenance_task"] = row["maintenance_task"] or ""
			row["maintenance_status"] = row["maintenance_status"] or ""
			row["maintenance_type"] = row["maintenance_type"] or ""
			row["periodicity"] = row["periodicity"] or ""
			row["assign_to_name"] = row["assign_to_name"] or ""

		frappe.log_error(
			f"Custom Asset Maintenance Schedule Report: Retrieved {len(data)} records",
			"Asset Maintenance Report",
		)

	except Exception as e:
		frappe.log_error(
			f"Error in Custom Asset Maintenance Schedule Report: {str(e)}", "Asset Maintenance Report Error"
		)
		frappe.msgprint(f"Error generating report: {str(e)}")

	return data

# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, flt, getdate
import json
from datetime import datetime


@frappe.whitelist()
def get_unified_dashboard_data(filters=None):
	"""
	Get unified dashboard data combining Heat and Mould metrics.

	Args:
	    filters (dict): Date range and other filters

	Returns:
	    dict: Combined data for all dashboard sections
	"""
	try:
		filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}

		# Validate required filters
		if not filters.get("from_date") or not filters.get("to_date"):
			return {"success": False, "message": _("From Date and To Date are required"), "data": {}}

		# Get data for each section
		heat_data = get_heat_dashboard_data(filters)
		mould_data = get_mould_dashboard_data(filters)

		# Extract the actual data from the response
		heat_data_actual = heat_data.get("data", {"summary": [], "raw_data": []})
		mould_data_actual = mould_data.get("data", {"summary": [], "raw_data": []})

		overview_data = get_overview_data(filters, heat_data_actual, mould_data_actual)

		return {
			"success": True,
			"data": {"overview": overview_data, "heat": heat_data_actual, "mould": mould_data_actual},
		}

	except Exception as e:
		frappe.log_error(f"Unified Dashboard Error: {str(e)}", "Unified Dashboard")
		return {"success": False, "message": _("An error occurred while fetching dashboard data"), "data": {}}


@frappe.whitelist()
def get_heat_dashboard_data(filters=None):
	"""Get Heat dashboard data using existing report logic."""
	try:
		filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}

		from shiw.report.number_card_heat_report.number_card_heat_report import get_data, get_report_summary

		heat_data = get_data(filters)
		heat_summary = get_report_summary(heat_data)

		return {"success": True, "data": {"summary": heat_summary, "raw_data": heat_data}}
	except Exception as e:
		frappe.log_error(f"Heat Dashboard Data Error: {str(e)}", "Unified Dashboard")
		return {"success": False, "message": str(e), "data": {"summary": [], "raw_data": []}}


@frappe.whitelist()
def get_mould_dashboard_data(filters=None):
	"""Get Mould dashboard data using existing report logic."""
	try:
		filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}

		from shiw.report.number_card_mould_report.number_card_mould_report import get_data, get_report_summary

		mould_data = get_data(filters)
		mould_summary = get_report_summary(mould_data)

		return {"success": True, "data": {"summary": mould_summary, "raw_data": mould_data}}
	except Exception as e:
		frappe.log_error(f"Mould Dashboard Data Error: {str(e)}", "Unified Dashboard")
		return {"success": False, "message": str(e), "data": {"summary": [], "raw_data": []}}


def get_overview_data(filters, heat_data, mould_data):
	"""Generate combined overview metrics."""
	try:
		overview_summary = []

		# Extract key metrics
		heat_summary = heat_data.get("summary", [])
		mould_summary = mould_data.get("summary", [])

		# Find specific metrics
		total_heats = next(
			(card["value"] for card in heat_summary if "Total Number of Heat" in card["label"]), 0
		)
		total_charge_mix = next(
			(card["value"] for card in heat_summary if "Total Charge Mix" in card["label"]), 0
		)
		liquid_balance = next(
			(card["value"] for card in heat_summary if "Liquid Balance" in card["label"]), 0
		)
		burning_loss_pct = next(
			(card["value"] for card in heat_summary if "Burning Loss" in card["label"]), 0
		)

		total_batches = next(
			(card["value"] for card in mould_summary if "Total Number of Batches" in card["label"]), 0
		)
		total_cast_weight = next(
			(card["value"] for card in mould_summary if "Total Cast Weight" in card["label"]), 0
		)
		total_bunch_weight = next(
			(card["value"] for card in mould_summary if "Total Bunch Weight" in card["label"]), 0
		)
		avg_yield = next((card["value"] for card in mould_summary if "Average Yield" in card["label"]), 0)
		total_tooling = next(
			(card["value"] for card in mould_summary if "Total Number of Tooling" in card["label"]), 0
		)
		estimated_foundry_return = next(
			(card["value"] for card in mould_summary if "Estimated Foundry Return" in card["label"]), 0
		)

		# Calculate combined metrics
		total_production_weight = flt(total_cast_weight + total_bunch_weight, 2)
		overall_efficiency = 0
		if total_charge_mix > 0:
			overall_efficiency = flt((liquid_balance / total_charge_mix) * 100, 2)

		# Create overview cards
		overview_summary = [
			{
				"value": overall_efficiency,
				"label": _("Overall Efficiency (%)"),
				"datatype": "Float",
				"precision": 2,
				"indicator": "Green",
				"description": _("Liquid balance efficiency"),
			},
			{
				"value": burning_loss_pct,
				"label": _("Overall Burning Loss (%)"),
				"datatype": "Float",
				"precision": 2,
				"indicator": "Orange",
				"description": _("Heat process burning loss"),
			},
			{
				"value": estimated_foundry_return,
				"label": _("Estimated Foundry Return"),
				"datatype": "Float",
				"precision": 2,
				"indicator": "Purple",
				"description": _("Bunch weight minus cast weight"),
			},
			{
				"value": avg_yield,
				"label": _("Average Mould Yield"),
				"datatype": "Float",
				"precision": 2,
				"indicator": "Teal",
				"description": _("Average yield across all mould types"),
			},
			{
				"value": total_tooling,
				"label": _("Total Tooling Used"),
				"datatype": "Int",
				"indicator": "Brown",
				"description": _("Total tooling across all mould batches"),
			},
		]

		return {
			"summary": overview_summary,
			"metrics": {
				"total_heats": total_heats,
				"total_batches": total_batches,
				"total_production_weight": total_production_weight,
				"overall_efficiency": overall_efficiency,
				"burning_loss_pct": burning_loss_pct,
				"avg_yield": avg_yield,
			},
		}

	except Exception as e:
		frappe.log_error(f"Overview Data Error: {str(e)}", "Unified Dashboard")
		return {"summary": [], "metrics": {}}


@frappe.whitelist()
def get_furnace_options():
	"""Get available furnace options for filter dropdown."""
	try:
		furnaces = frappe.get_all(
			"Furnace - Master", fields=["name", "furnace_name"], order_by="furnace_name"
		)
		return [{"value": f.name, "label": f.furnace_name} for f in furnaces]
	except Exception as e:
		frappe.log_error(f"Furnace Options Error: {str(e)}", "Unified Dashboard")
		return []


@frappe.whitelist()
def get_batch_type_options():
	"""Get available batch type options for filter dropdown."""
	return [
		{"value": "All", "label": _("All Types")},
		{"value": "Co2 Mould Batch", "label": _("CO2 Mould Batch")},
		{"value": "Green Sand Hand Mould Batch", "label": _("Green Sand Hand Mould Batch")},
		{"value": "No-Bake Mould Batch", "label": _("No-Bake Mould Batch")},
		{"value": "Jolt Squeeze Mould Batch", "label": _("Jolt Squeeze Mould Batch")},
		{"value": "HPML Mould Batch", "label": _("HPML Mould Batch")},
	]


@frappe.whitelist()
def export_data(from_date=None, to_date=None, furnace_no=None, batch_type=None):
	"""
	Export unified dashboard data to Excel/CSV format.

	Args:
	    from_date (str): Start date
	    to_date (str): End date
	    furnace_no (str): Furnace filter
	    batch_type (str): Batch type filter

	Returns:
	    dict: Export data with download link
	"""
	try:
		# Validate parameters
		if not from_date or not to_date:
			frappe.throw(_("From Date and To Date are required for export"))

		# Build filters
		filters = {"from_date": from_date, "to_date": to_date}

		if furnace_no:
			filters["furnace_no"] = furnace_no
		if batch_type and batch_type != "All":
			filters["batch_type"] = batch_type

		# Get data
		heat_data = get_heat_dashboard_data(filters)
		mould_data = get_mould_dashboard_data(filters)
		overview_data = get_overview_data(filters, heat_data, mould_data)

		# Prepare export data
		export_data = {
			"report_info": {
				"title": "Unified Foundry Dashboard Report",
				"generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"date_range": f"{from_date} to {to_date}",
				"filters": {"furnace": furnace_no or "All", "batch_type": batch_type or "All"},
			},
			"overview": {
				"metrics": overview_data.get("metrics", {}),
				"cards": overview_data.get("summary", []),
			},
			"heat_process": {
				"cards": heat_data.get("summary", []),
				"raw_data": heat_data.get("raw_data", []),
			},
			"mould_process": {
				"cards": mould_data.get("summary", []),
				"raw_data": mould_data.get("raw_data", []),
			},
		}

		# Create file
		filename = f"unified_dashboard_{from_date}_to_{to_date}.json"
		file_path = f"/tmp/{filename}"

		with open(file_path, "w") as f:
			json.dump(export_data, f, indent=2, default=str)

		# Return download information
		return {
			"success": True,
			"message": _("Export completed successfully"),
			"filename": filename,
			"file_path": file_path,
			"download_url": f"/api/method/shiw.page.unified_dashboard.unified_dashboard.download_export?filename={filename}",
		}

	except Exception as e:
		frappe.log_error(f"Export Error: {str(e)}", "Unified Dashboard Export")
		return {"success": False, "message": _("Export failed: {0}").format(str(e))}


@frappe.whitelist()
def download_export(filename=None):
	"""Download exported file."""
	try:
		if not filename:
			frappe.throw(_("Filename is required"))

		file_path = f"/tmp/{filename}"

		if not frappe.utils.file_manager.file_exists(file_path):
			frappe.throw(_("Export file not found"))

		# Set response headers for download
		frappe.response.filename = filename
		frappe.response.filecontent = frappe.utils.file_manager.read_file(file_path)
		frappe.response.type = "download"

	except Exception as e:
		frappe.log_error(f"Download Export Error: {str(e)}", "Unified Dashboard Export")
		frappe.throw(_("Download failed: {0}").format(str(e)))

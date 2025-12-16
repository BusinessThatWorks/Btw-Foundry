# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DailyCosting(Document):
	pass


@frappe.whitelist()
def get_repair_weight_for_daily_costing(date: str, shift_type: str):
	"""
	Return SUM of total_repair_weight and total_consumption_valuation from Repair doctype
	for given date and shift_type.
	Used by Daily Costing form to auto-fill repairing_weight, repairing_cost, and repairing_cost_per_kg.
	"""
	if not date or not shift_type:
		return {}

	# Fetch all matching Repair docs and sum total_repair_weight and total_consumption_valuation
	repair_docs = frappe.get_all(
		"Repair",
		# Both Daily Costing and Repair have a proper Date field named "date",
		# so we can filter directly by the same value (YYYY-MM-DD).
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_repair_weight", "total_consumption_valuation"],
	)

	total_weight = 0
	total_consumption_valuation = 0

	for doc in repair_docs:
		if doc.get("total_repair_weight"):
			total_weight += float(doc.get("total_repair_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	repairing_cost_per_kg = 0
	if total_weight:
		repairing_cost_per_kg = total_consumption_valuation / total_weight

	# Optional: log for debugging on server side
	frappe.logger().info(
		{
			"message": "Fetched summed repair values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"total_weight": total_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"repairing_cost_per_kg": repairing_cost_per_kg,
			"matched_repair_docs": [d.get("name") for d in repair_docs],
		}
	)

	# If nothing matched, return empty dict
	if not repair_docs:
		return {}

	return {
		"repairing_weight": total_weight,
		"repairing_cost": total_consumption_valuation,
		"repairing_cost_per_kg": repairing_cost_per_kg,
	}


@frappe.whitelist()
def get_hpml_values_for_daily_costing(date: str, shift_type: str):
	"""
	Return aggregated values from HPML Mould Batch for given date and shift_type.
	- total_cast_weight  -> hpml_weight
	- total_consumption_valuation -> hpml_cost
	- hpml_cost_per_kg = total_consumption_valuation / total_cast_weight (if weight > 0)
	"""
	if not date or not shift_type:
		return {}

	hpml_docs = frappe.get_all(
		"HPML Mould Batch",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in hpml_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	hpml_cost_per_kg = 0
	if total_cast_weight:
		hpml_cost_per_kg = total_consumption_valuation / total_cast_weight

	# Log for debugging
	frappe.logger().info(
		{
			"message": "Fetched HPML values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_hpml_docs": [d.get("name") for d in hpml_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"hpml_cost_per_kg": hpml_cost_per_kg,
		}
	)

	if not hpml_docs:
		return {}

	return {
		"hpml_weight": total_cast_weight,
		"hpml_cost": total_consumption_valuation,
		"hpml_cost_per_kg": hpml_cost_per_kg,
	}


@frappe.whitelist()
def get_js_values_for_daily_costing(date: str, shift_type: str):
	"""
	Jolt Squeeze Mould Batch aggregates:
	- total_cast_weight  -> js_weight
	- total_consumption_valuation -> js_cost
	- js_cost_per_kg = total_consumption_valuation / total_cast_weight
	"""
	if not date or not shift_type:
		return {}

	js_docs = frappe.get_all(
		"Jolt Squeeze Mould Batch",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in js_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	js_cost_per_kg = 0
	if total_cast_weight:
		js_cost_per_kg = total_consumption_valuation / total_cast_weight

	frappe.logger().info(
		{
			"message": "Fetched JS values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_js_docs": [d.get("name") for d in js_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"js_cost_per_kg": js_cost_per_kg,
		}
	)

	if not js_docs:
		return {}

	return {
		"js_weight": total_cast_weight,
		"js_cost": total_consumption_valuation,
		"js_cost_per_kg": js_cost_per_kg,
	}


@frappe.whitelist()
def get_no_bake_values_for_daily_costing(date: str, shift_type: str):
	"""
	No-Bake Mould Batch aggregates:
	- total_cast_weight  -> no_bake_weight
	- total_consumption_valuation -> no_bake_cost
	- no_bake_cost_per_kg = total_consumption_valuation / total_cast_weight
	"""
	if not date or not shift_type:
		return {}

	nb_docs = frappe.get_all(
		"No-Bake Mould Batch",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in nb_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	no_bake_cost_per_kg = 0
	if total_cast_weight:
		no_bake_cost_per_kg = total_consumption_valuation / total_cast_weight

	frappe.logger().info(
		{
			"message": "Fetched No-Bake values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_nb_docs": [d.get("name") for d in nb_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"no_bake_cost_per_kg": no_bake_cost_per_kg,
		}
	)

	if not nb_docs:
		return {}

	return {
		"no_bake_weight": total_cast_weight,
		"no_bake_cost": total_consumption_valuation,
		"no_bake_cost_per_kg": no_bake_cost_per_kg,
	}


@frappe.whitelist()
def get_green_sand_values_for_daily_costing(date: str, shift_type: str):
	"""
	Green Sand Hand Mould Batch aggregates:
	- total_cast_weight  -> green_sand_weight
	- total_consumption_valuation -> green_sand_cost
	- green_sand_cost_per_kg = total_consumption_valuation / total_cast_weight
	"""
	if not date or not shift_type:
		return {}

	gs_docs = frappe.get_all(
		"Green Sand Hand Mould Batch",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in gs_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	green_sand_cost_per_kg = 0
	if total_cast_weight:
		green_sand_cost_per_kg = total_consumption_valuation / total_cast_weight

	frappe.logger().info(
		{
			"message": "Fetched Green Sand values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_gs_docs": [d.get("name") for d in gs_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"green_sand_cost_per_kg": green_sand_cost_per_kg,
		}
	)

	if not gs_docs:
		return {}

	return {
		"green_sand_weight": total_cast_weight,
		"green_sand_cost": total_consumption_valuation,
		"green_sand_cost_per_kg": green_sand_cost_per_kg,
	}


@frappe.whitelist()
def get_co2_values_for_daily_costing(date: str, shift_type: str):
	"""
	Co2 Mould Batch aggregates:
	- total_cast_weight  -> co2_weight
	- total_consumption_valuation -> co2_cost
	- co2_cost_per_kg = total_consumption_valuation / total_cast_weight
	"""
	if not date or not shift_type:
		return {}

	co2_docs = frappe.get_all(
		"Co2 Mould Batch",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in co2_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	co2_cost_per_kg = 0
	if total_cast_weight:
		co2_cost_per_kg = total_consumption_valuation / total_cast_weight

	frappe.logger().info(
		{
			"message": "Fetched Co2 values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_co2_docs": [d.get("name") for d in co2_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"co2_cost_per_kg": co2_cost_per_kg,
		}
	)

	if not co2_docs:
		return {}

	return {
		"co2_weight": total_cast_weight,
		"co2_cost": total_consumption_valuation,
		"co2_cost_per_kg": co2_cost_per_kg,
	}


@frappe.whitelist()
def get_heat_values_for_daily_costing(date: str, shift_type: str):
	"""
	Heat doctype aggregates:
	- liquid_balence -> liquid_metal
	- total_charge_mix_valuation -> liquid_metal_cost
	- total_ladle_consumption_valuation -> ladle_cost
	- liquid_metal_cost_per_kg = total_charge_mix_valuation / liquid_balence
	- ladle_cost_per_kg = total_ladle_consumption_valuation / liquid_balence
	"""
	if not date or not shift_type:
		return {}

	heat_docs = frappe.get_all(
		"Heat",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "liquid_balence", "total_charge_mix_valuation", "total_ladle_consumption_valuation"],
	)

	total_liquid_balance = 0
	total_charge_mix_valuation = 0
	total_ladle_consumption_valuation = 0

	for doc in heat_docs:
		if doc.get("liquid_balence"):
			total_liquid_balance += float(doc.get("liquid_balence") or 0)
		if doc.get("total_charge_mix_valuation"):
			total_charge_mix_valuation += float(doc.get("total_charge_mix_valuation") or 0)
		if doc.get("total_ladle_consumption_valuation"):
			total_ladle_consumption_valuation += float(doc.get("total_ladle_consumption_valuation") or 0)

	liquid_metal_cost_per_kg = 0
	ladle_cost_per_kg = 0
	if total_liquid_balance:
		liquid_metal_cost_per_kg = total_charge_mix_valuation / total_liquid_balance
		ladle_cost_per_kg = total_ladle_consumption_valuation / total_liquid_balance

	frappe.logger().info(
		{
			"message": "Fetched Heat values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_heat_docs": [d.get("name") for d in heat_docs],
			"total_liquid_balance": total_liquid_balance,
			"total_charge_mix_valuation": total_charge_mix_valuation,
			"total_ladle_consumption_valuation": total_ladle_consumption_valuation,
			"liquid_metal_cost_per_kg": liquid_metal_cost_per_kg,
			"ladle_cost_per_kg": ladle_cost_per_kg,
		}
	)

	if not heat_docs:
		return {}

	return {
		"liquid_metal": total_liquid_balance,
		"liquid_metal_cost": total_charge_mix_valuation,
		"ladle_cost": total_ladle_consumption_valuation,
		"liquid_metal_cost_per_kg": liquid_metal_cost_per_kg,
		"ladle_cost_per_kg": ladle_cost_per_kg,
	}


@frappe.whitelist()
def get_core_values_for_daily_costing(date: str, shift_type: str):
	"""
	Core Production aggregates:
	- total_cast_weight  -> core_weight
	- total_consumption_valuation -> core_cost
	- core_cost_per_kg = total_consumption_valuation / total_cast_weight
	"""
	if not date or not shift_type:
		return {}

	core_docs = frappe.get_all(
		"Core Production",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_cast_weight", "total_consumption_valuation"],
	)

	total_cast_weight = 0
	total_consumption_valuation = 0

	for doc in core_docs:
		if doc.get("total_cast_weight"):
			total_cast_weight += float(doc.get("total_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	core_cost_per_kg = 0
	if total_cast_weight:
		core_cost_per_kg = total_consumption_valuation / total_cast_weight

	frappe.logger().info(
		{
			"message": "Fetched Core Production values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_core_docs": [d.get("name") for d in core_docs],
			"total_cast_weight": total_cast_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"core_cost_per_kg": core_cost_per_kg,
		}
	)

	if not core_docs:
		return {}

	return {
		"core_weight": total_cast_weight,
		"core_cost": total_consumption_valuation,
		"core_cost_per_kg": core_cost_per_kg,
	}


@frappe.whitelist()
def get_shotblast_values_for_daily_costing(date: str, shift_type: str):
	"""
	Shot Blast aggregates:
	- total_shot_blast_cast_weight  -> shotblast_weight
	- total_consumption_valuation -> shotblast_cost
	- shotblast_cost_per_kg = total_consumption_valuation / total_shot_blast_cast_weight
	"""
	if not date or not shift_type:
		return {}

	shotblast_docs = frappe.get_all(
		"Shot Blast",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_shot_blast_cast_weight", "total_consumption_valuation"],
	)

	total_weight = 0
	total_consumption_valuation = 0

	for doc in shotblast_docs:
		if doc.get("total_shot_blast_cast_weight"):
			total_weight += float(doc.get("total_shot_blast_cast_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	shotblast_cost_per_kg = 0
	if total_weight:
		shotblast_cost_per_kg = total_consumption_valuation / total_weight

	frappe.logger().info(
		{
			"message": "Fetched Shot Blast values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_shotblast_docs": [d.get("name") for d in shotblast_docs],
			"total_weight": total_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"shotblast_cost_per_kg": shotblast_cost_per_kg,
		}
	)

	if not shotblast_docs:
		return {}

	return {
		"shotblast_weight": total_weight,
		"shotblast_cost": total_consumption_valuation,
		"shotblast_cost_per_kg": shotblast_cost_per_kg,
	}


@frappe.whitelist()
def get_fettling_values_for_daily_costing(date: str, shift_type: str):
	"""
	Fettling aggregates:
	- total_fettling_weight  -> fettling_weight
	- total_consumption_valuation -> fettling_cost
	- fettling_cost_per_kg = total_consumption_valuation / total_fettling_weight
	"""
	if not date or not shift_type:
		return {}

	fettling_docs = frappe.get_all(
		"Fettling",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_fettling_weight", "total_consumption_valuation"],
	)

	total_weight = 0
	total_consumption_valuation = 0

	for doc in fettling_docs:
		if doc.get("total_fettling_weight"):
			total_weight += float(doc.get("total_fettling_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	fettling_cost_per_kg = 0
	if total_weight:
		fettling_cost_per_kg = total_consumption_valuation / total_weight

	frappe.logger().info(
		{
			"message": "Fetched Fettling values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_fettling_docs": [d.get("name") for d in fettling_docs],
			"total_weight": total_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"fettling_cost_per_kg": fettling_cost_per_kg,
		}
	)

	if not fettling_docs:
		return {}

	return {
		"fettling_weight": total_weight,
		"fettling_cost": total_consumption_valuation,
		"fettling_cost_per_kg": fettling_cost_per_kg,
	}


@frappe.whitelist()
def get_finishing_values_for_daily_costing(date: str, shift_type: str):
	"""
	Finishing aggregates:
	- total_finishing_weight  -> finishing_weight
	- total_consumption_valuation -> finishing_cost
	- finishing_cost_per_kg = total_consumption_valuation / total_finishing_weight
	"""
	if not date or not shift_type:
		return {}

	finishing_docs = frappe.get_all(
		"Finishing",
		filters={"date": date, "shift_type": shift_type},
		fields=["name", "total_finishing_weight", "total_consumption_valuation"],
	)

	total_weight = 0
	total_consumption_valuation = 0

	for doc in finishing_docs:
		if doc.get("total_finishing_weight"):
			total_weight += float(doc.get("total_finishing_weight") or 0)
		if doc.get("total_consumption_valuation"):
			total_consumption_valuation += float(doc.get("total_consumption_valuation") or 0)

	finishing_cost_per_kg = 0
	if total_weight:
		finishing_cost_per_kg = total_consumption_valuation / total_weight

	frappe.logger().info(
		{
			"message": "Fetched Finishing values for Daily Costing",
			"date": date,
			"shift_type": shift_type,
			"matched_finishing_docs": [d.get("name") for d in finishing_docs],
			"total_weight": total_weight,
			"total_consumption_valuation": total_consumption_valuation,
			"finishing_cost_per_kg": finishing_cost_per_kg,
		}
	)

	if not finishing_docs:
		return {}

	return {
		"finishing_weight": total_weight,
		"finishing_cost": total_consumption_valuation,
		"finishing_cost_per_kg": finishing_cost_per_kg,
	}

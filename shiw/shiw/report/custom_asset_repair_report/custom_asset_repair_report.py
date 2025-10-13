import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters or {})
	return columns, data


def get_columns():
	return [
		{"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "Asset Repair", "width": 140},
		{"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 160},
		{"label": "Asset Name", "fieldname": "asset_name", "fieldtype": "Data", "width": 180},
		{"label": "Failure Date", "fieldname": "failure_date", "fieldtype": "Datetime", "width": 160},
		{"label": "Completion Date", "fieldname": "completion_date", "fieldtype": "Datetime", "width": 160},
		{"label": "Status", "fieldname": "repair_status", "fieldtype": "Data", "width": 120},
		{"label": "Time (min)", "fieldname": "custom_time_in_minutes_", "fieldtype": "Float", "width": 120},
		{"label": "Downtime (min)", "fieldname": "downtime", "fieldtype": "Float", "width": 130},
		{"label": "Attend By", "fieldname": "attend_by", "fieldtype": "Data", "width": 180},
		{
			"label": "Elec/Mech",
			"fieldname": "custom_electricalmechanical",
			"fieldtype": "Select",
			"width": 140,
		},
		{"label": "Remarks", "fieldname": "custom_remarks", "fieldtype": "Small Text", "width": 220},
		{
			"label": "Prod Loss (tons)",
			"fieldname": "custom_production_loss_in_tons",
			"fieldtype": "Float",
			"width": 150,
		},
		{"label": "Description", "fieldname": "description", "fieldtype": "Small Text", "width": 220},
		{
			"label": "Actions Performed",
			"fieldname": "actions_performed",
			"fieldtype": "Small Text",
			"width": 220,
		},
		{
			"label": "Action of Breakdown",
			"fieldname": "custom_action_of_breakdown",
			"fieldtype": "Small Text",
			"width": 220,
		},
	]


def get_conditions(filters):
	conditions = []
	values = {}

	if filters.get("from_date"):
		conditions.append("ar.failure_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("ar.failure_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	if filters.get("asset"):
		conditions.append("ar.asset = %(asset)s")
		values["asset"] = filters["asset"]
	if filters.get("status"):
		conditions.append("ar.repair_status = %(status)s")
		values["status"] = filters["status"]
	if filters.get("type"):
		conditions.append("ar.custom_electricalmechanical = %(type)s")
		values["type"] = filters["type"]
	if filters.get("attended_by"):
		conditions.append("aba.attend_by = %(attended_by)s")
		values["attended_by"] = filters["attended_by"]

	where = (" where " + " and ".join(conditions)) if conditions else ""
	return where, values


def get_data(filters):
	where, values = get_conditions(filters)
	query = f"""
		select
			ar.name,
			ar.asset,
			ar.asset_name,
			ar.failure_date,
			ar.completion_date,
			ar.repair_status,
			ar.custom_time_in_minutes_,
			ar.downtime,
			coalesce(group_concat(distinct aba.attend_by order by aba.idx separator ', '), '') as attend_by,
			ar.custom_electricalmechanical,
			ar.custom_remarks,
			ar.custom_production_loss_in_tons,
			ar.description,
			ar.actions_performed,
			ar.custom_action_of_breakdown
		from `tabAsset Repair` ar
		left join `tabAttend By Asset Repair` aba on aba.parent = ar.name
		{where}
		group by ar.name
		order by ar.failure_date desc, ar.name desc
	"""
	return frappe.db.sql(query, values=values, as_dict=True)

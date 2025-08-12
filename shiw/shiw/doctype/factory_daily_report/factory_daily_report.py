# Copyright (c) 2025, beetashoke chakraborty and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FactoryDailyReport(Document):
	pass




# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": "HPML Mould Batch",
#         "Jolt Squeeze Mould Batch": "Jolt Squeeze Mould Batch"
#     }

#     result = []

#     for activity_label, doctype_name in activities.items():
#         frappe.logger().info(f"Fetching sums for {activity_label} on {date}")

#         data = frappe.db.get_all(
#             doctype_name,
#             filters={"date": date},
#             fields=[
#                 "sum(total_man_power) as total_man_power",
#                 "sum(total_labour_cost) as total_labour_cost",
#                 "sum(total_consumption_valuation) as total_consumption_cost"
#             ]
#         )

#         totals = data[0] if data else {}
#         result.append({
#             "activity": activity_label,
#             "total_man_power": totals.get("total_man_power") or 0,
#             "total_labour_cost": totals.get("total_labour_cost") or 0,
#             "total_consumption_cost": totals.get("total_consumption_cost") or 0
#         })

#     frappe.logger().info(f"Final aggregated result: {result}")
#     return result




#current code

# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         frappe.logger().info(f"Fetching sums for {activity_label} on {date}")

#         if activity_label == "Heat":
#             # Heat's special rules: first doc's total_man_power, sum others
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=["total_man_power", "total_labour_cost", config["consumption_field"]],
#                 order_by="creation asc"
#             )
#             if heat_docs:
#                 total_man_power = heat_docs[0].total_man_power or 0
#                 total_labour_cost = sum(d.total_labour_cost or 0 for d in heat_docs)
#                 total_consumption_cost = sum(d[config["consumption_field"]] or 0 for d in heat_docs)
#             else:
#                 total_man_power = total_labour_cost = total_consumption_cost = 0

#         else:
#             # Normal sum for other activities
#             data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )
#             totals = data[0] if data else {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost
#         })

#     frappe.logger().info(f"Final aggregated result: {result}")
#     return result



# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         frappe.logger().info(f"Fetching sums for {activity_label} on {date}")

#         # initialize all fields (totals + shift-wise)
#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label == "Heat":
#             # Heat's special rules: first doc's total_man_power, sum others
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=["total_man_power", "total_labour_cost", config["consumption_field"], "shift_type"],
#                 order_by="creation asc"
#             )

#             if heat_docs:
#                 # overall totals (keep special rule: first heat's total_man_power)
#                 total_man_power = heat_docs[0].get("total_man_power") or 0
#                 total_labour_cost = sum(d.get("total_labour_cost") or 0 for d in heat_docs)
#                 total_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in heat_docs)

#                 # shift wise sums (sum across all heat docs by shift)
#                 for d in heat_docs:
#                     shift = (d.get("shift_type") or "").strip()
#                     if shift == "Day Shift":
#                         day_shift_man_power += d.get("total_man_power") or 0
#                         day_shift_labour_cost += d.get("total_labour_cost") or 0
#                         day_shift_consumption_cost += d.get(config["consumption_field"]) or 0
#                     elif shift == "Night Shift":
#                         night_shift_man_power += d.get("total_man_power") or 0
#                         night_shift_labour_cost += d.get("total_labour_cost") or 0
#                         night_shift_consumption_cost += d.get(config["consumption_field"]) or 0

#             else:
#                 # nothing found -> all zeros (already initialized)

#                 pass

#         else:
#             # Normal sum for other activities (totals)
#             data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )
#             totals = data[0] if data else {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             # Day shift sums
#             day_data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )
#             day_totals = day_data[0] if day_data else {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             # Night shift sums
#             night_data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )
#             night_totals = night_data[0] if night_data else {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#         # append activity row with totals and shift breakdown
#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     frappe.logger().info(f"Final aggregated result: {result}")
#     return result




# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         frappe.logger().info(f"Fetching sums for {activity_label} on {date}")

#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label == "Heat":
#             # Fetch all heat docs for that date
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=["total_man_power", "total_labour_cost", config["consumption_field"], "shift_type"],
#                 order_by="creation asc"
#             )

#             if heat_docs:
#                 # Overall totals: first doc man power, sum others normally
#                 total_man_power = heat_docs[0].get("total_man_power") or 0
#                 total_labour_cost = sum(d.get("total_labour_cost") or 0 for d in heat_docs)
#                 total_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in heat_docs)

#                 # Shift-wise sums: independent of the "first doc" rule
#                 day_shift_man_power = sum(
#                     d.get("total_man_power") or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"
#                 )
#                 day_shift_labour_cost = sum(
#                     d.get("total_labour_cost") or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"
#                 )
#                 day_shift_consumption_cost = sum(
#                     d.get(config["consumption_field"]) or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"
#                 )

#                 night_shift_man_power = sum(
#                     d.get("total_man_power") or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"
#                 )
#                 night_shift_labour_cost = sum(
#                     d.get("total_labour_cost") or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"
#                 )
#                 night_shift_consumption_cost = sum(
#                     d.get(config["consumption_field"]) or 0 for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"
#                 )

#         else:
#             # Normal activities (HPML, Jolt Squeeze)
#             totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )[0] or {}

#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             # Day shift
#             day_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             # Night shift
#             night_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     frappe.logger().info(f"Final aggregated result: {result}")
#     return result





# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         frappe.logger().info(f"Fetching sums for {activity_label} on {date}")

#         # init
#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label == "Heat":
#             # fetch all Heat docs for the date, ordered by creation so first-per-shift is deterministic
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "name",
#                     "total_man_power",
#                     "total_labour_cost",
#                     config["consumption_field"],
#                     "shift_type",
#                     "creation"
#                 ],
#                 order_by="creation asc"
#             )

#             if heat_docs:
#                 # overall sums across all heat docs
#                 total_labour_cost = sum(d.get("total_labour_cost") or 0 for d in heat_docs)
#                 total_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in heat_docs)

#                 # group by shift, capture first doc's man_power per shift and sums per shift
#                 shifts = {}
#                 for d in heat_docs:
#                     shift = (d.get("shift_type") or "").strip() or "Unknown"
#                     if shift not in shifts:
#                         # first seen doc for this shift -> record its man_power as first_man_power
#                         shifts[shift] = {
#                             "first_man_power": d.get("total_man_power") or 0,
#                             "labour_sum": 0,
#                             "consumption_sum": 0
#                         }
#                     # accumulate sums for that shift
#                     shifts[shift]["labour_sum"] += d.get("total_labour_cost") or 0
#                     shifts[shift]["consumption_sum"] += d.get(config["consumption_field"]) or 0

#                 # map Day Shift and Night Shift (if present), also compute total_man_power as sum of firsts
#                 total_man_power = 0
#                 for shift_name, vals in shifts.items():
#                     total_man_power += vals["first_man_power"]
#                     if shift_name == "Day Shift":
#                         day_shift_man_power = vals["first_man_power"]
#                         day_shift_labour_cost = vals["labour_sum"]
#                         day_shift_consumption_cost = vals["consumption_sum"]
#                     elif shift_name == "Night Shift":
#                         night_shift_man_power = vals["first_man_power"]
#                         night_shift_labour_cost = vals["labour_sum"]
#                         night_shift_consumption_cost = vals["consumption_sum"]
#                     else:
#                         # If there are other shift names, they still contribute to totals.
#                         # Optionally handle them if you want.
#                         pass

#             # else: remain zeros

#         else:
#             # Non-Heat activities (same as your working logic)
#             data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )
#             totals = data[0] if data else {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             # Day shift sums
#             day_data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )
#             day_totals = day_data[0] if day_data else {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             # Night shift sums
#             night_data = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )
#             night_totals = night_data[0] if night_data else {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#         # append result
#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     frappe.logger().info(f"Final aggregated result: {result}")
#     return result































# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         print(f"\n=== Processing activity: {activity_label} for date {date} ===")

#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label == "Heat":
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "name",
#                     "total_man_power",
#                     "total_labour_cost",
#                     config["consumption_field"],
#                     "shift_type",
#                     "creation"
#                 ],
#                 order_by="creation asc"
#             )

#             print(f"Fetched Heat docs: {heat_docs}")

#             if heat_docs:
#                 # Separate into Day and Night shifts
#                 day_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"]
#                 night_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"]

#                 print(f"Day shift docs: {day_shift_docs}")
#                 print(f"Night shift docs: {night_shift_docs}")

#                 # Day shift calculations
#                 if day_shift_docs:
#                     day_shift_man_power = day_shift_docs[0].get("total_man_power") or 0
#                     day_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in day_shift_docs)
#                     day_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in day_shift_docs)
#                     print(f"Day shift → manpower: {day_shift_man_power}, labour: {day_shift_labour_cost}, consumption: {day_shift_consumption_cost}")

#                 # Night shift calculations
#                 if night_shift_docs:
#                     night_shift_man_power = night_shift_docs[0].get("total_man_power") or 0
#                     night_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in night_shift_docs)
#                     night_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in night_shift_docs)
#                     print(f"Night shift → manpower: {night_shift_man_power}, labour: {night_shift_labour_cost}, consumption: {night_shift_consumption_cost}")

#                 # Totals
#                 total_man_power = day_shift_man_power + night_shift_man_power
#                 total_labour_cost = day_shift_labour_cost + night_shift_labour_cost
#                 total_consumption_cost = day_shift_consumption_cost + night_shift_consumption_cost

#                 print(f"TOTALS → manpower: {total_man_power}, labour: {total_labour_cost}, consumption: {total_consumption_cost}")

#         else:
#             # Non-Heat (unchanged)
#             print(f"Fetching Non-Heat totals for {activity_label}")
#             totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )[0] or {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             print(f"Non-Heat totals: {totals}")

#             # Day shift
#             day_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             print(f"Day shift totals: {day_totals}")

#             # Night shift
#             night_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#             print(f"Night shift totals: {night_totals}")

#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     print("\n=== FINAL RESULT ===")
#     print(result)
#     return result





# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat": {
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         },
#         "Co2 Mould Batch": {
#             "doctype": "Co2 Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Green Sand Hand Mould Batch": {
#             "doctype": "Green Sand Hand Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "No-Bake Mould Batch": {
#             "doctype": "No-Bake Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Pouring": {
#             "doctype": "Pouring",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Shake Out": {
#             "doctype": "Shake Out",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Shot Blast": {
#             "doctype": "Shot Blast",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Fettling": {
#             "doctype": "Fettling",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Finishing": {
#             "doctype": "Finishing",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Paint": {
#             "doctype": "Paint",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Repair": {
#             "doctype": "Repair",
#             "consumption_field": "total_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         print(f"\n=== Processing activity: {activity_label} for date {date} ===")

#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label == "Heat":
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "name",
#                     "total_man_power",
#                     "total_labour_cost",
#                     config["consumption_field"],
#                     "shift_type",
#                     "creation"
#                 ],
#                 order_by="creation asc"
#             )

#             print(f"Fetched Heat docs: {heat_docs}")

#             if heat_docs:
#                 # Separate into Day and Night shifts
#                 day_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"]
#                 night_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"]

#                 print(f"Day shift docs: {day_shift_docs}")
#                 print(f"Night shift docs: {night_shift_docs}")

#                 # Day shift calculations
#                 if day_shift_docs:
#                     day_shift_man_power = day_shift_docs[0].get("total_man_power") or 0
#                     day_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in day_shift_docs)
#                     day_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in day_shift_docs)

#                 # Night shift calculations
#                 if night_shift_docs:
#                     night_shift_man_power = night_shift_docs[0].get("total_man_power") or 0
#                     night_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in night_shift_docs)
#                     night_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in night_shift_docs)

#                 # Totals
#                 total_man_power = day_shift_man_power + night_shift_man_power
#                 total_labour_cost = day_shift_labour_cost + night_shift_labour_cost
#                 total_consumption_cost = day_shift_consumption_cost + night_shift_consumption_cost

#         else:
#             # Non-Heat activities
#             totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )[0] or {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             # Day shift
#             day_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             # Night shift
#             night_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     print("\n=== FINAL RESULT ===")
#     print(result)
#     return result













#actuall code


# import frappe

# @frappe.whitelist()
# def get_activity_totals(date):
#     activities = {
#         "HPML Mould Batch": {
#             "doctype": "HPML Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Jolt Squeeze Mould Batch": {
#             "doctype": "Jolt Squeeze Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat-ladle": { 
#             "doctype": "Heat",
#             "consumption_field": "total_ladle_consumption_valuation"
#         },
#         "Heat-charge": {  # new activity
#             "doctype": "Heat",
#             "consumption_field": "total_charge_mix_valuation"
#         },
#         "Co2 Mould Batch": {
#             "doctype": "Co2 Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Green Sand Hand Mould Batch": {
#             "doctype": "Green Sand Hand Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "No-Bake Mould Batch": {
#             "doctype": "No-Bake Mould Batch",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Pouring": {
#             "doctype": "Pouring",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Shake Out": {
#             "doctype": "Shake Out",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Shot Blast": {
#             "doctype": "Shot Blast",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Fettling": {
#             "doctype": "Fettling",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Finishing": {
#             "doctype": "Finishing",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Paint": {
#             "doctype": "Paint",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Repair": {
#             "doctype": "Repair",
#             "consumption_field": "total_consumption_valuation"
#         },
#         "Heat Treatment": {
#             "doctype": "Heat Treatment",
#             "consumption_field": "total_consumption_valuation"
#         }
#     }

#     result = []

#     for activity_label, config in activities.items():
#         print(f"\n=== Processing activity: {activity_label} for date {date} ===")

#         total_man_power = total_labour_cost = total_consumption_cost = 0
#         day_shift_man_power = night_shift_man_power = 0
#         day_shift_labour_cost = night_shift_labour_cost = 0
#         day_shift_consumption_cost = night_shift_consumption_cost = 0

#         if activity_label in ["Heat", "Heat-charge"]:
#             heat_docs = frappe.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "name",
#                     "total_man_power",
#                     "total_labour_cost",
#                     config["consumption_field"],
#                     "shift_type",
#                     "creation"
#                 ],
#                 order_by="creation asc"
#             )

#             print(f"Fetched {activity_label} docs: {heat_docs}")

#             if heat_docs:
#                 # Separate into Day and Night shifts
#                 day_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"]
#                 night_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"]

#                 print(f"Day shift docs: {day_shift_docs}")
#                 print(f"Night shift docs: {night_shift_docs}")

#                 # Day shift calculations
#                 if day_shift_docs:
#                     day_shift_man_power = day_shift_docs[0].get("total_man_power") or 0
#                     day_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in day_shift_docs)
#                     day_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in day_shift_docs)

#                 # Night shift calculations
#                 if night_shift_docs:
#                     night_shift_man_power = night_shift_docs[0].get("total_man_power") or 0
#                     night_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in night_shift_docs)
#                     night_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in night_shift_docs)

#                 # Totals
#                 total_man_power = day_shift_man_power + night_shift_man_power
#                 total_labour_cost = day_shift_labour_cost + night_shift_labour_cost
#                 total_consumption_cost = day_shift_consumption_cost + night_shift_consumption_cost

#         else:
#             # Non-Heat activities
#             totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date},
#                 fields=[
#                     "sum(total_man_power) as total_man_power",
#                     "sum(total_labour_cost) as total_labour_cost",
#                     f"sum({config['consumption_field']}) as total_consumption_cost"
#                 ]
#             )[0] or {}
#             total_man_power = totals.get("total_man_power") or 0
#             total_labour_cost = totals.get("total_labour_cost") or 0
#             total_consumption_cost = totals.get("total_consumption_cost") or 0

#             # Day shift
#             day_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Day Shift"},
#                 fields=[
#                     "sum(total_man_power) as day_shift_man_power",
#                     "sum(total_labour_cost) as day_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as day_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             day_shift_man_power = day_totals.get("day_shift_man_power") or 0
#             day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
#             day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

#             # Night shift
#             night_totals = frappe.db.get_all(
#                 config["doctype"],
#                 filters={"date": date, "shift_type": "Night Shift"},
#                 fields=[
#                     "sum(total_man_power) as night_shift_man_power",
#                     "sum(total_labour_cost) as night_shift_labour_cost",
#                     f"sum({config['consumption_field']}) as night_shift_consumption_cost"
#                 ]
#             )[0] or {}
#             night_shift_man_power = night_totals.get("night_shift_man_power") or 0
#             night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
#             night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

#         result.append({
#             "activity": activity_label,
#             "total_man_power": total_man_power,
#             "total_labour_cost": total_labour_cost,
#             "total_consumption_cost": total_consumption_cost,
#             "day_shift_man_power": day_shift_man_power,
#             "night_shift_man_power": night_shift_man_power,
#             "day_shift_labour_cost": day_shift_labour_cost,
#             "night_shift_labour_cost": night_shift_labour_cost,
#             "day_shift_consumption_cost": day_shift_consumption_cost,
#             "night_shift_consumption_cost": night_shift_consumption_cost
#         })

#     print("\n=== FINAL RESULT ===")
#     print(result)
#     return result




import frappe

@frappe.whitelist()
def get_activity_totals(date):
    activities = {
        "HPML Mould Batch": {
            "doctype": "HPML Mould Batch",
            "consumption_field": "total_consumption_valuation"
        },
        "Jolt Squeeze Mould Batch": {
            "doctype": "Jolt Squeeze Mould Batch",
            "consumption_field": "total_consumption_valuation"
        },
        "Heat": {
            "doctype": "Heat",
            "consumption_field": "total_ladle_consumption_valuation"
        },
        "Heat-charge": {  # new activity
            "doctype": "Heat",
            "consumption_field": "total_charge_mix_valuation"
        },
        "Co2 Mould Batch": {
            "doctype": "Co2 Mould Batch",
            "consumption_field": "total_consumption_valuation"
        },
        "Green Sand Hand Mould Batch": {
            "doctype": "Green Sand Hand Mould Batch",
            "consumption_field": "total_consumption_valuation"
        },
        "No-Bake Mould Batch": {
            "doctype": "No-Bake Mould Batch",
            "consumption_field": "total_consumption_valuation"
        },
        "Pouring": {
            "doctype": "Pouring",
            "consumption_field": "total_consumption_valuation"
        },
        "Shake Out": {
            "doctype": "Shake Out",
            "consumption_field": "total_consumption_valuation"
        },
        "Shot Blast": {
            "doctype": "Shot Blast",
            "consumption_field": "total_consumption_valuation"
        },
        "Fettling": {
            "doctype": "Fettling",
            "consumption_field": "total_consumption_valuation"
        },
        "Finishing": {
            "doctype": "Finishing",
            "consumption_field": "total_consumption_valuation"
        },
        "Paint": {
            "doctype": "Paint",
            "consumption_field": "total_consumption_valuation"
        },
        "Repair": {
            "doctype": "Repair",
            "consumption_field": "total_consumption_valuation"
        }
    }

    result = []

    def build_sum_field(field, alias=None):
        alias = alias or field
        return f"sum({field}) as `{alias}`"

    for activity_label, config in activities.items():
        print(f"\n=== Processing activity: {activity_label} for date {date} ===")

        total_man_power = total_labour_cost = total_consumption_cost = 0
        day_shift_man_power = night_shift_man_power = 0
        day_shift_labour_cost = night_shift_labour_cost = 0
        day_shift_consumption_cost = night_shift_consumption_cost = 0

        # Get fieldnames of the doctype
        doctype_fields = frappe.get_meta(config["doctype"]).fields
        fieldnames = [f.fieldname for f in doctype_fields]

        if activity_label in ["Heat", "Heat-charge"]:
            fields = ["name"]
            if "total_man_power" in fieldnames:
                fields.append("total_man_power")
            if "total_labour_cost" in fieldnames:
                fields.append("total_labour_cost")
            if config["consumption_field"] in fieldnames:
                fields.append(config["consumption_field"])
            if "shift_type" in fieldnames:
                fields.append("shift_type")
            if "creation" in fieldnames:
                fields.append("creation")

            heat_docs = frappe.get_all(
                config["doctype"],
                filters={"date": date},
                fields=fields,
                order_by="creation asc"
            )

            print(f"Fetched {activity_label} docs: {heat_docs}")

            if heat_docs:
                day_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Day Shift"]
                night_shift_docs = [d for d in heat_docs if (d.get("shift_type") or "").strip() == "Night Shift"]

                print(f"Day shift docs: {day_shift_docs}")
                print(f"Night shift docs: {night_shift_docs}")

                if day_shift_docs:
                    day_shift_man_power = day_shift_docs[0].get("total_man_power") or 0
                    day_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in day_shift_docs)
                    day_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in day_shift_docs)

                if night_shift_docs:
                    night_shift_man_power = night_shift_docs[0].get("total_man_power") or 0
                    night_shift_labour_cost = sum(d.get("total_labour_cost") or 0 for d in night_shift_docs)
                    night_shift_consumption_cost = sum(d.get(config["consumption_field"]) or 0 for d in night_shift_docs)

                total_man_power = day_shift_man_power + night_shift_man_power
                total_labour_cost = day_shift_labour_cost + night_shift_labour_cost
                total_consumption_cost = day_shift_consumption_cost + night_shift_consumption_cost

        else:
            # Non-Heat activities
            fields = []
            if "total_man_power" in fieldnames:
                fields.append(build_sum_field("total_man_power"))
            if "total_labour_cost" in fieldnames:
                fields.append(build_sum_field("total_labour_cost"))
            if config["consumption_field"] in fieldnames:
                fields.append(build_sum_field(config["consumption_field"], "total_consumption_cost"))

            if fields:
                totals = frappe.db.get_all(
                    config["doctype"],
                    filters={"date": date},
                    fields=fields
                )
                totals = totals[0] if totals else {}
            else:
                totals = {}

            total_man_power = totals.get("total_man_power") or 0
            total_labour_cost = totals.get("total_labour_cost") or 0
            total_consumption_cost = totals.get("total_consumption_cost") or 0

            day_fields = []
            if "total_man_power" in fieldnames:
                day_fields.append(build_sum_field("total_man_power", "day_shift_man_power"))
            if "total_labour_cost" in fieldnames:
                day_fields.append(build_sum_field("total_labour_cost", "day_shift_labour_cost"))
            if config["consumption_field"] in fieldnames:
                day_fields.append(build_sum_field(config["consumption_field"], "day_shift_consumption_cost"))

            if day_fields:
                day_totals = frappe.db.get_all(
                    config["doctype"],
                    filters={"date": date, "shift_type": "Day Shift"},
                    fields=day_fields
                )
                day_totals = day_totals[0] if day_totals else {}
            else:
                day_totals = {}

            day_shift_man_power = day_totals.get("day_shift_man_power") or 0
            day_shift_labour_cost = day_totals.get("day_shift_labour_cost") or 0
            day_shift_consumption_cost = day_totals.get("day_shift_consumption_cost") or 0

            night_fields = []
            if "total_man_power" in fieldnames:
                night_fields.append(build_sum_field("total_man_power", "night_shift_man_power"))
            if "total_labour_cost" in fieldnames:
                night_fields.append(build_sum_field("total_labour_cost", "night_shift_labour_cost"))
            if config["consumption_field"] in fieldnames:
                night_fields.append(build_sum_field(config["consumption_field"], "night_shift_consumption_cost"))

            if night_fields:
                night_totals = frappe.db.get_all(
                    config["doctype"],
                    filters={"date": date, "shift_type": "Night Shift"},
                    fields=night_fields
                )
                night_totals = night_totals[0] if night_totals else {}
            else:
                night_totals = {}

            night_shift_man_power = night_totals.get("night_shift_man_power") or 0
            night_shift_labour_cost = night_totals.get("night_shift_labour_cost") or 0
            night_shift_consumption_cost = night_totals.get("night_shift_consumption_cost") or 0

        result.append({
            "activity": activity_label,
            "total_man_power": total_man_power,
            "total_labour_cost": total_labour_cost,
            "total_consumption_cost": total_consumption_cost,
            "day_shift_man_power": day_shift_man_power,
            "night_shift_man_power": night_shift_man_power,
            "day_shift_labour_cost": day_shift_labour_cost,
            "night_shift_labour_cost": night_shift_labour_cost,
            "day_shift_consumption_cost": day_shift_consumption_cost,
            "night_shift_consumption_cost": night_shift_consumption_cost
        })

    print("\n=== FINAL RESULT ===")
    print(result)
    return result

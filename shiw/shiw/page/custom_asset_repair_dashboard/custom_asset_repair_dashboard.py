import frappe
from frappe import _


def get_context(context):
	context.title = _("Custom Asset Repair Dashboard")
	context.no_cache = 1

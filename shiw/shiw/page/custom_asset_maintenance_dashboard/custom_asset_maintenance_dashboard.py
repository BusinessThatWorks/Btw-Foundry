import frappe
from frappe import _


def get_context(context):
	context.title = _("Custom Asset Maintenance Dashboard")
	context.no_cache = 1


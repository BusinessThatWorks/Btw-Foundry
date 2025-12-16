import frappe
from frappe import _


def get_context(context):
	context.title = _("Item History Dashboard")
	context.no_cache = 1


import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist()
def send_daily_critical_stock_email():
	"""
	Simple function to send daily critical stock email
	Call this manually or set up a cron job
	"""
	try:
		frappe.log_error("📧 Sending daily critical stock email", "Daily Email")

		# Import and run the critical stock notification
		from .critical_stock_notification import check_critical_stock_and_notify

		# Run the notification
		result = check_critical_stock_and_notify()

		frappe.log_error(f"✅ Daily email sent: {result.get('success', False)}", "Daily Email")

		return result

	except Exception as e:
		error_msg = f"Failed to send daily email: {str(e)}"
		frappe.log_error(error_msg, "Daily Email")
		return {"success": False, "message": error_msg}


@frappe.whitelist()
def test_daily_email():
	"""
	Test the daily email function
	"""
	return send_daily_critical_stock_email()



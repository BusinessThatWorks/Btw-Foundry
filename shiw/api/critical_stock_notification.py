import frappe
from frappe import _
from frappe.utils import get_datetime, format_datetime, get_url
import json


@frappe.whitelist()
def check_critical_stock_and_notify():
	"""
	Check critical items with low stock and send email notification
	This function can be called manually or via scheduled job
	"""
	try:
		# Get all critical items
		critical_items = get_critical_items_with_low_stock()

		if not critical_items:
			# Send "all good" notification even when no low stock items
			frappe.log_error(
				"No critical items with low stock found - sending all good notification",
				"Critical Stock Notification",
			)
			send_all_good_notification()
			return {
				"success": True,
				"message": "All critical items have sufficient stock - notification sent",
				"items": [],
			}

		# Send email notification for low stock items
		send_low_stock_notification(critical_items)

		return {
			"success": True,
			"message": f"Email sent for {len(critical_items)} critical items with low stock",
			"items": critical_items,
		}

	except Exception as e:
		frappe.log_error(f"Error in critical stock notification: {str(e)}", "Critical Stock Notification")
		return {"success": False, "message": f"Error: {str(e)}"}


def get_critical_items_with_low_stock():
	"""
	Get all critical items that have stock below minimum level
	"""
	warehouse = "Stores - SHIW"
	low_stock_items = []

	# Get all items marked as critical
	critical_items = frappe.get_all(
		"Item",
		filters={"custom_is_critical": 1, "disabled": 0},
		fields=["name", "item_name", "item_code", "custom_minimum_stock", "stock_uom"],
	)

	frappe.log_error(f"Found {len(critical_items)} critical items", "Critical Stock Notification")

	for item in critical_items:
		# Get current stock from Bin table
		current_stock = (
			frappe.db.get_value("Bin", {"item_code": item.name, "warehouse": warehouse}, "actual_qty") or 0
		)

		min_stock = item.custom_minimum_stock or 0

		# Check if current stock is below minimum
		if current_stock < min_stock:
			low_stock_items.append(
				{
					"item_code": item.item_code,
					"item_name": item.item_name,
					"current_stock": current_stock,
					"minimum_stock": min_stock,
					"stock_uom": item.stock_uom,
					"warehouse": warehouse,
					"shortage": min_stock - current_stock,
				}
			)

			frappe.log_error(
				f"Low stock: {item.item_name} - Current: {current_stock}, Min: {min_stock}",
				"Critical Stock Notification",
			)

	return low_stock_items


def send_low_stock_notification(low_stock_items):
	"""
	Send email notification for low stock items
	"""
	recipient_email = "beetashoke.chakraborty@clapgrow.com"

	# Create email subject
	subject = f"🚨 CRITICAL STOCK ALERT - {len(low_stock_items)} Items Below Minimum Stock"

	# Create email content
	message = create_email_content(low_stock_items)

	# Send email
	try:
		frappe.sendmail(
			recipients=[recipient_email],
			subject=subject,
			message=message,
			header=["Critical Stock Alert", "red"],
			now=True,  # Send immediately, don't queue
		)

		frappe.log_error(f"Email sent successfully to {recipient_email}", "Critical Stock Notification")

	except Exception as e:
		frappe.log_error(f"Failed to send email: {str(e)}", "Critical Stock Notification")
		raise e


def send_all_good_notification():
	"""
	Send email notification when all critical items have sufficient stock
	"""
	recipient_email = "beetashoke.chakraborty@clapgrow.com"

	# Create email subject
	subject = "✅ CRITICAL STOCK STATUS - All Items Have Sufficient Stock"

	# Create email content
	message = create_all_good_email_content()

	# Send email
	try:
		frappe.sendmail(
			recipients=[recipient_email],
			subject=subject,
			message=message,
			header=["Stock Status OK", "green"],
			now=True,  # Send immediately, don't queue
		)

		frappe.log_error(
			f"All good notification sent successfully to {recipient_email}", "Critical Stock Notification"
		)

	except Exception as e:
		frappe.log_error(f"Failed to send all good email: {str(e)}", "Critical Stock Notification")
		raise e


def create_email_content(low_stock_items):
	"""
	Create HTML email content for low stock notification
	"""
	# Get current date and time
	current_time = format_datetime(get_datetime(), "dd-MM-yyyy HH:mm:ss")

	# Start building HTML content
	html_content = f"""
	<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
		<div style="background-color: #ff4444; color: white; padding: 20px; text-align: center;">
			<h1>🚨 CRITICAL STOCK ALERT</h1>
			<p style="margin: 0; font-size: 18px;">{len(low_stock_items)} Items Below Minimum Stock Level</p>
			<p style="margin: 5px 0 0 0; font-size: 14px;">Alert Time: {current_time}</p>
		</div>
		
		<div style="padding: 20px; background-color: #f9f9f9;">
			<h2 style="color: #333; margin-top: 0;">Items Requiring Immediate Attention:</h2>
			
			<table style="width: 100%; border-collapse: collapse; margin-top: 20px; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
				<thead>
					<tr style="background-color: #333; color: white;">
						<th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Item Code</th>
						<th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Item Name</th>
						<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Current Stock</th>
						<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Minimum Stock</th>
						<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Shortage</th>
						<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">UOM</th>
					</tr>
				</thead>
				<tbody>
	"""

	# Add rows for each low stock item
	for item in low_stock_items:
		# Determine row color based on severity
		row_color = "#ffebee" if item["shortage"] > 10 else "#fff3e0"

		html_content += f"""
					<tr style="background-color: {row_color};">
						<td style="padding: 12px; border-bottom: 1px solid #ddd; font-weight: bold;">{item["item_code"]}</td>
						<td style="padding: 12px; border-bottom: 1px solid #ddd;">{item["item_name"]}</td>
						<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center; color: #d32f2f; font-weight: bold;">{item["current_stock"]}</td>
						<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item["minimum_stock"]}</td>
						<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center; color: #d32f2f; font-weight: bold;">{item["shortage"]}</td>
						<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item["stock_uom"]}</td>
					</tr>
		"""

	# Close table and add footer
	html_content += f"""
				</tbody>
			</table>
			
			<div style="margin-top: 30px; padding: 20px; background-color: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px;">
				<h3 style="color: #1976d2; margin-top: 0;">📋 Action Required:</h3>
				<ul style="color: #333; line-height: 1.6;">
					<li>Review the above items and initiate procurement process</li>
					<li>Check with suppliers for availability and delivery timelines</li>
					<li>Consider emergency procurement for critical items</li>
					<li>Update minimum stock levels if needed</li>
				</ul>
			</div>
			
			<div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 4px; text-align: center;">
				<p style="margin: 0; color: #666; font-size: 14px;">
					This is an automated alert from SHIW ERP System.<br>
					Please take immediate action to avoid production delays.
				</p>
			</div>
		</div>
	</div>
	"""

	return html_content


def create_all_good_email_content():
	"""
	Create HTML email content for all good notification
	"""
	# Get current date and time
	current_time = format_datetime(get_datetime(), "dd-MM-yyyy HH:mm:ss")

	# Get critical items summary
	critical_items = frappe.get_all(
		"Item",
		filters={"custom_is_critical": 1, "disabled": 0},
		fields=["name", "item_name", "item_code", "custom_minimum_stock", "stock_uom"],
	)

	# Start building HTML content
	html_content = f"""
	<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
		<div style="background-color: #4caf50; color: white; padding: 20px; text-align: center;">
			<h1>✅ CRITICAL STOCK STATUS - ALL GOOD</h1>
			<p style="margin: 0; font-size: 18px;">All Critical Items Have Sufficient Stock</p>
			<p style="margin: 5px 0 0 0; font-size: 14px;">Status Check: {current_time}</p>
		</div>
		
		<div style="padding: 20px; background-color: #f9f9f9;">
			<h2 style="color: #333; margin-top: 0;">📊 Critical Items Summary:</h2>
			
			<div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
				<h3 style="color: #4caf50; margin-top: 0;">✅ All Critical Items Status</h3>
				<p style="color: #666; margin-bottom: 20px;">The following critical items have sufficient stock levels:</p>
				
				<table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
					<thead>
						<tr style="background-color: #4caf50; color: white;">
							<th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Item Code</th>
							<th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Item Name</th>
							<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Minimum Stock</th>
							<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">UOM</th>
							<th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Status</th>
						</tr>
					</thead>
					<tbody>
	"""

	# Add rows for each critical item
	for item in critical_items:
		# Get current stock for this item
		current_stock = (
			frappe.db.get_value("Bin", {"item_code": item.name, "warehouse": "Stores - SHIW"}, "actual_qty")
			or 0
		)

		html_content += f"""
						<tr style="background-color: #e8f5e8;">
							<td style="padding: 12px; border-bottom: 1px solid #ddd; font-weight: bold;">{item.item_code}</td>
							<td style="padding: 12px; border-bottom: 1px solid #ddd;">{item.item_name}</td>
							<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item.custom_minimum_stock}</td>
							<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item.stock_uom}</td>
							<td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center; color: #4caf50; font-weight: bold;">✅ Sufficient ({current_stock})</td>
						</tr>
		"""

	# Close table and add footer
	html_content += f"""
					</tbody>
				</table>
			</div>
			
			<div style="margin-top: 30px; padding: 20px; background-color: #e8f5e8; border-left: 4px solid #4caf50; border-radius: 4px;">
				<h3 style="color: #2e7d32; margin-top: 0;">🎉 Great News!</h3>
				<ul style="color: #333; line-height: 1.6;">
					<li>All critical items have stock levels above their minimum requirements</li>
					<li>No immediate procurement actions are needed</li>
					<li>Continue monitoring stock levels regularly</li>
				</ul>
			</div>
			
			<div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 4px; text-align: center;">
				<p style="margin: 0; color: #666; font-size: 14px;">
					This is an automated status report from SHIW ERP System.<br>
					Next check will be performed tomorrow.
				</p>
			</div>
		</div>
	</div>
	"""

	return html_content


@frappe.whitelist()
def test_critical_stock_notification():
	"""
	Test function to manually trigger critical stock notification
	Useful for testing the email functionality
	"""
	return check_critical_stock_and_notify()


@frappe.whitelist()
def get_critical_stock_summary():
	"""
	Get summary of critical stock status without sending email
	Useful for dashboard or manual checking
	"""
	try:
		low_stock_items = get_critical_items_with_low_stock()

		# Get total critical items count
		total_critical_items = frappe.db.count("Item", {"custom_is_critical": 1, "disabled": 0})

		return {
			"success": True,
			"total_critical_items": total_critical_items,
			"low_stock_count": len(low_stock_items),
			"low_stock_items": low_stock_items,
			"warehouse": "Stores - SHIW",
		}

	except Exception as e:
		frappe.log_error(f"Error getting critical stock summary: {str(e)}", "Critical Stock Notification")
		return {"success": False, "message": f"Error: {str(e)}"}

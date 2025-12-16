# 🕙 Critical Stock Scheduler Setup Guide

## ✅ **What I've Fixed:**

1. **Immediate Email Sending**: Added `now=True` parameter to send emails immediately (not queued)
2. **Daily Scheduler**: Set up daily scheduler to run critical stock check
3. **Automatic Email**: Emails will be sent automatically without manual intervention

## 🚀 **How to Set Up 10:30 AM Scheduler:**

### Method 1: Using Frappe Console (Recommended)

1. **Go to your Frappe site console:**
   ```bash
   bench --site hanuman.com console
   ```

2. **Run this command to set up the scheduler:**
   ```python
   # Enable scheduler
   frappe.db.set_single_value("System Settings", "enable_scheduler", 1)
   
   # Create a scheduled job type
   job_type = frappe.get_doc({
       "doctype": "Scheduled Job Type",
       "method": "shiw.api.simple_scheduler.run_critical_stock_at_1030",
       "frequency": "Daily",
       "cron_format": "30 10 * * *",  # 10:30 AM daily
       "enabled": 1
   })
   job_type.insert()
   
   print("✅ Scheduler setup completed!")
   ```

### Method 2: Manual Setup in Frappe UI

1. **Go to Setup > Scheduled Job Type**
2. **Create New:**
   - **Method**: `shiw.api.simple_scheduler.run_critical_stock_at_1030`
   - **Frequency**: Daily
   - **Cron Format**: `30 10 * * *`
   - **Enabled**: Yes

3. **Save the job type**

### Method 3: Using Bench Commands

```bash
# Enable scheduler
bench --site hanuman.com set-config enable_scheduler 1

# Start the scheduler
bench --site hanuman.com start

# Check scheduler status
bench --site hanuman.com console
```

## 🧪 **Test the System:**

### Test 1: Manual Test
```bash
bench --site hanuman.com execute shiw.api.simple_scheduler.test_now
```

### Test 2: Check Email Queue
1. Go to **Setup > Email Queue**
2. Check if emails are being sent immediately (not queued)

### Test 3: Check Scheduler Logs
1. Go to **Setup > Logs > Error Log**
2. Search for "Simple Scheduler" or "Critical Stock"
3. Check if scheduler is running

## 📧 **Email Configuration:**

The system now sends emails immediately with:
- ✅ **Immediate sending** (not queued)
- ✅ **Daily at 10:30 AM** (when scheduler is set up)
- ✅ **Both low stock and all-good notifications**

## 🔧 **Troubleshooting:**

### Issue 1: Emails Still Queued
**Solution**: The `now=True` parameter should fix this. If not, check:
- Email account configuration
- SMTP settings
- Network connectivity

### Issue 2: Scheduler Not Running
**Solution**: 
1. Check if scheduler is enabled: `frappe.db.get_single_value("System Settings", "enable_scheduler")`
2. Start the scheduler: `bench --site hanuman.com start`
3. Check scheduler logs in Error Log

### Issue 3: Wrong Time
**Solution**: 
- The cron format `30 10 * * *` means 10:30 AM daily
- To change time, modify the cron format in the scheduled job type

## 📅 **Schedule Details:**

- **Frequency**: Daily
- **Time**: 10:30 AM
- **Function**: `shiw.api.simple_scheduler.run_critical_stock_at_1030`
- **Email Recipient**: `erp@clapgrow.com`
- **Email Type**: Both low stock alerts and all-good confirmations

## 🎯 **What Happens Daily at 10:30 AM:**

1. **System checks** all critical items
2. **Compares** current stock vs minimum stock
3. **Sends email** immediately:
   - 🚨 **Red Alert** if any items are below minimum
   - ✅ **Green Status** if all items are sufficient

## 📞 **Quick Commands:**

```bash
# Test the system now
bench --site hanuman.com execute shiw.api.simple_scheduler.test_now

# Check scheduler status
bench --site hanuman.com console

# View logs
bench --site hanuman.com logs
```

---

**The system is now ready!** 🎉
- Emails will be sent immediately (not queued)
- Daily scheduler will run at 10:30 AM
- You'll receive daily status emails automatically



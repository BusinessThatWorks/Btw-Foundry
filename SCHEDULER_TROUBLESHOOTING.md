# 🔧 SCHEDULER TROUBLESHOOTING - 11:51 AM Daily

## 🚨 **Issue: No Email at 11:51 AM**

### **Possible Causes:**
1. **Scheduler not running** - The Frappe scheduler process isn't started
2. **Job type not created** - Scheduled job type doesn't exist
3. **Scheduler disabled** - Scheduler is disabled in System Settings
4. **Time zone issues** - Server time vs Frappe time mismatch

## ✅ **What I've Fixed:**

1. **Updated time** - Changed to 11:51 AM in hooks.py
2. **Created job type** - Scheduled job type now exists
3. **Tested function** - Manual test works perfectly

## 🔧 **Troubleshooting Steps:**

### Step 1: Check if Scheduler is Running
```bash
# Check if bench processes are running
ps aux | grep bench

# Check if scheduler process is running
ps aux | grep schedule
```

### Step 2: Start Scheduler
```bash
# Start the bench processes
bench start

# Or start just the scheduler
bench --site hanuman.com enable-scheduler
```

### Step 3: Check Scheduler Status
```bash
# Check if scheduler is enabled
bench --site hanuman.com console
# Then run: frappe.db.get_single_value("System Settings", "enable_scheduler")
```

### Step 4: Test Manual Trigger
```bash
# Test the function manually
bench --site hanuman.com execute shiw.api.scheduler_diagnostic.test_scheduler_now
```

## 🕙 **Current Configuration:**

### **In hooks.py:**
```python
scheduler_events = {
    "cron": {
        "51 11 * * *": ["shiw.api.simple_daily_email.send_daily_critical_stock_email"],  # 11:51 AM daily
    },
}
```

### **Scheduled Job Type:**
- **Method**: `shiw.api.simple_daily_email.send_daily_critical_stock_email`
- **Frequency**: Daily
- **Cron Format**: `51 11 * * *`
- **Status**: Created and enabled

## 🧪 **Test Commands:**

### Test 1: Manual Test (Run Now)
```bash
bench --site hanuman.com execute shiw.api.simple_daily_email.send_daily_critical_stock_email
```

### Test 2: Scheduler Diagnostic
```bash
bench --site hanuman.com execute shiw.api.scheduler_diagnostic.check_scheduler_status
```

### Test 3: Force Run
```bash
bench --site hanuman.com execute shiw.api.scheduler_diagnostic.force_run_scheduler
```

## 📊 **Monitoring:**

### Check Error Logs:
1. Go to **Setup > Logs > Error Log**
2. Search for "Scheduler Test" or "Daily Email"
3. Look for success/failure messages

### Check Scheduled Jobs:
1. Go to **Setup > Scheduled Job Type**
2. Look for "simple_daily_email.send_daily_critical_stock_email"
3. Check if it's enabled

### Check Scheduled Job Logs:
1. Go to **Setup > Scheduled Job Log**
2. Look for recent entries
3. Check status and next run time

## 🚨 **Common Issues & Solutions:**

### Issue 1: Scheduler Not Running
**Solution**: 
```bash
# Start the scheduler
bench start

# Or enable scheduler
bench --site hanuman.com enable-scheduler
```

### Issue 2: Job Type Not Created
**Solution**: 
```bash
# Create the job type
bench --site hanuman.com execute shiw.api.scheduler_diagnostic.create_scheduled_job_type
```

### Issue 3: Time Zone Issues
**Solution**: 
1. Check server time: `date`
2. Check Frappe time: `bench --site hanuman.com console`
3. Adjust cron time if needed

### Issue 4: Scheduler Disabled
**Solution**: 
1. Go to **Setup > System Settings**
2. Enable "Enable Scheduler"
3. Save the settings

## 📅 **Next Steps:**

1. **Start scheduler**: `bench start`
2. **Test manually**: Run the test command
3. **Wait for 11:51 AM**: Check if email is sent
4. **Monitor logs**: Check Error Log for scheduler entries

## 🎯 **Expected Behavior:**

- **Daily at 11:51 AM**: Scheduler runs automatically
- **Email sent**: To erp@clapgrow.com
- **Logs created**: In Error Log
- **No manual intervention**: Fully automated

---

**Current Time**: Check if it's close to 11:51 AM  
**Scheduler Status**: Check if running  
**Next Test**: Wait for 11:51 AM or test manually


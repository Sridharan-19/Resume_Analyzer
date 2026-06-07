# QUICK REFERENCE CARD

## Command Cheat Sheet

```bash
# SETUP
.\.venv\Scripts\Activate.ps1          # Activate environment
pip install -r requirements.txt        # Install dependencies
cp .env.example .env                   # Create credentials file
# Edit .env with your credentials

# RUNNING MODES
python -m src.main run_once            # Run once (immediate)
python -m src.main                     # Run scheduled (daily)
Ctrl+C                                 # Stop scheduled mode

# MANUAL REVIEW (dry_run=true) - RECOMMENDED FIRST
# Edit config.yaml: apply_settings -> dry_run: true
python -m src.main run_once
# Result: Resumes tailored, URLs provided, no auto-submit

# AUTOMATED APPLY (dry_run=false)
# Edit config.yaml: apply_settings -> dry_run: false
# Edit .env: Add LinkedIn/Indeed credentials
python -m src.main run_once
# Result: Browser opens, auto-applies to jobs

# MONITORING
tail -f logs/resume_analyzer.log       # View logs live
type logs/resume_analyzer.log          # View all logs
ls logs/apply_attempt_*.png            # View error screenshots

# DATABASE
sqlite3 application_history.db         # Open database
SELECT * FROM applications;            # View all applications
SELECT status, COUNT(*) FROM applications GROUP BY status;  # Stats

# EXPORT
python -c "
from src.application_tracker import ApplicationTracker
tracker = ApplicationTracker()
tracker.export_report('applications.csv')
"                                      # Export to CSV
```

---

## Configuration Quick Reference

### Recommended Setup (Manual First)
```yaml
# config.yaml
apply_settings:
  dry_run: true           # ← Manual review mode
  browser:
    headless: true        # Browser hidden
  rate_limit:
    enabled: true
    delay_between_apps: 5
```

### For Automation
```yaml
apply_settings:
  dry_run: false          # ← Automated mode
  browser:
    headless: false       # ← Show browser (for testing)
  rate_limit:
    enabled: true
    delay_between_apps: 5
```

### For Production
```yaml
apply_settings:
  dry_run: false
  browser:
    headless: true        # ← Hide browser
  rate_limit:
    enabled: true
    delay_between_apps: 5
    max_apps_per_hour: 10
```

---

## File Locations

| Item | Location |
|------|----------|
| Your Resume | `resumes/base_resume.txt` |
| Tailored Resumes | `resumes/tailored/` |
| Logs | `logs/resume_analyzer.log` |
| Database | `application_history.db` |
| Config | `config.yaml` |
| Credentials | `.env` (git-ignored) |
| Setup Guide | `AUTOMATED_APPLY_SETUP.md` |
| Full Docs | `README.md` |

---

## Credentials Template (.env)

```
# LinkedIn
LINKEDIN_EMAIL=your-email@gmail.com
LINKEDIN_PASSWORD=your-password

# Indeed
INDEED_EMAIL=your-email@gmail.com
INDEED_PASSWORD=your-password

# Gmail (for notifications - optional)
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# Notification
NOTIFICATION_EMAIL=your-email@gmail.com
```

---

## What Gets Created

After running `python -m src.main run_once`:

```
resumes/tailored/
  ├── tailored_Company1_DataScientist.txt
  ├── tailored_Company2_GenAIEngineer.txt
  └── application_report_20250607_090000.txt

logs/
  ├── resume_analyzer.log
  └── apply_attempt_1717771200.png  (if error)

application_history.db               (Auto-created)
```

---

## Status Indicators

### Application Statuses
- `pending` - Prepared, not yet applied
- `ready_for_manual_review` - Ready to manually apply (dry_run mode)
- `applied` - Successfully auto-applied
- `failed` - Auto-apply failed
- `error` - Error during process
- `already_applied` - Duplicate application blocked

### Log Levels
- `INFO` - Normal operation
- `WARNING` - Something unexpected but continuing
- `ERROR` - Error occurred

---

## Troubleshooting Matrix

| Problem | Cause | Solution |
|---------|-------|----------|
| No jobs found | Internet/API issue | Check logs, verify internet |
| ChromeDriver error | Not installed | Download from chromedriver.chromium.org |
| No applications submitted | dry_run=true | Change to dry_run=false |
| Credentials invalid | Wrong format/characters | Edit .env, test in browser |
| Button not found | Site changed/specific handling | Try headless=false, update selector |
| Rate limited | Too many apps/hour | Increase delay_between_apps |
| Email not working | Wrong credentials | Use app password for Gmail |

---

## Daily Workflow

```bash
# Morning (One-time setup)
.\.venv\Scripts\Activate.ps1
python -m src.main run_once
# Check: resumes/tailored/
# Apply manually or enable automation

# Evening (Check results)
tail logs/resume_analyzer.log
sqlite3 application_history.db "SELECT COUNT(*) FROM applications;"

# Weekly (Review performance)
python -c "
from src.application_tracker import ApplicationTracker
tracker = ApplicationTracker()
print(tracker.get_application_stats())
tracker.export_report('weekly_report.csv')
"
```

---

## Features Checklist

### Job Search
- [ ] RemoteOK enabled
- [ ] Indeed enabled
- [ ] LinkedIn enabled
- [ ] AngelList enabled
- [ ] Target roles configured

### Resume Tailoring
- [ ] Base resume loaded
- [ ] Role-specific tailoring enabled
- [ ] Tailored resumes generated

### Applications
- [ ] Manual mode tested (dry_run=true)
- [ ] Credentials configured (.env)
- [ ] Auto mode ready (dry_run=false)
- [ ] Rate limiting enabled
- [ ] Error handling working

### Tracking
- [ ] Database created
- [ ] Applications tracked
- [ ] Report generation working
- [ ] Logs available

### Scheduling
- [ ] Daily time configured
- [ ] Scheduler tested
- [ ] Email notifications (optional)

---

## Useful Queries

```sql
-- All applications
SELECT job_title, company, status, applied_at FROM applications;

-- By status
SELECT status, COUNT(*) FROM applications GROUP BY status;

-- Today's applications
SELECT COUNT(*) FROM applications WHERE DATE(applied_at) = DATE('now');

-- Failed applications
SELECT job_title, company, result FROM applications WHERE status='failed';

-- Success rate
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN status='applied' THEN 1 ELSE 0 END) as successful,
  ROUND(100.0 * SUM(CASE WHEN status='applied' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM applications;
```

---

## Environment Variables

```bash
# Browser
BROWSER_HEADLESS=true|false
BROWSER_DRIVER_PATH=/path/to/chromedriver

# Rate Limiting
MAX_APPS_PER_HOUR=10
DELAY_BETWEEN_APPS=5
MAX_RETRY_ATTEMPTS=3

# Notifications
SEND_NOTIFICATIONS=true|false
```

---

## Files Modified

- ✅ `config.yaml` - Updated with automation options
- ✅ `requirements.txt` - Added browser automation libraries
- ✅ `README.md` - Updated with new features
- ✅ `src/main.py` - Enhanced with automation
- ✅ `src/apply.py` - New automated handlers
- ✅ `.env.example` - Credentials template

## Files Created

- ✅ `src/browser_automation.py` - Selenium wrapper
- ✅ `src/job_apply_handlers.py` - Job board handlers
- ✅ `src/credentials.py` - Credential management
- ✅ `src/application_tracker.py` - Application database
- ✅ `AUTOMATED_APPLY_SETUP.md` - Setup guide
- ✅ `TRANSFORMATION_SUMMARY.md` - This summary

---

**For more details, see: AUTOMATED_APPLY_SETUP.md**

# AUTOMATED JOB APPLY - SETUP GUIDE

## Overview

Your Resume Analyzer has been upgraded to **automatically apply to jobs** across multiple platforms. This guide explains how to enable and configure automated applications.

## ⚠️ IMPORTANT SECURITY NOTES

1. **Never commit credentials to Git**
   - Use `.env` file (it's in `.gitignore`)
   - Keep credentials private

2. **Use App Passwords, Not Regular Passwords**
   - For Gmail: Use app passwords (myaccount.google.com/apppasswords)
   - For work accounts: Use OAuth tokens if available

3. **Test with dry_run=true First**
   - Always test with manual review mode first
   - Verify resumes and applications before enabling automation

---

## Step 1: Setup Environment File

### Copy the template:
```bash
cp .env.example .env
```

### Edit `.env` with your credentials:
```
LINKEDIN_EMAIL=your-email@gmail.com
LINKEDIN_PASSWORD=your-password

INDEED_EMAIL=your-email@gmail.com
INDEED_PASSWORD=your-password

GMAIL_EMAIL=your-gmail@gmail.com
GMAIL_APP_PASSWORD=your-app-password

NOTIFICATION_EMAIL=your-email@gmail.com
```

---

## Step 2: Verify Configuration

### Check config.yaml settings:

**For Manual Mode (Recommended for First Run):**
```yaml
apply_settings:
  dry_run: true           # ← Keep this TRUE for now
```

**For Automated Mode:**
```yaml
apply_settings:
  dry_run: false          # ← Set to FALSE to enable automation
  browser:
    headless: true        # ← Show browser (false) for debugging
    timeout_seconds: 30
  rate_limit:
    enabled: true
    delay_between_apps: 5
    max_apps_per_hour: 10
```

---

## Step 3: Install Browser Driver

### Download ChromeDriver:

1. Check your Chrome version: `chrome://version/`
2. Download matching ChromeDriver from: https://chromedriver.chromium.org/
3. Add to PATH or specify in `.env`:
   ```
   BROWSER_DRIVER_PATH=/path/to/chromedriver
   ```

### Or use automatic detection:
The system will try to auto-detect ChromeDriver (requires it in PATH)

---

## Step 4: First Run - Manual Mode (RECOMMENDED)

### Run with dry_run=true (preparation mode):
```bash
python -m src.main run_once
```

**What you'll see:**
- ✅ Jobs searched and filtered
- ✅ Resumes tailored for each role
- ✅ Application report generated
- ✅ Ready for manual submission
- ❌ NO automatic submissions yet

**What to do:**
1. Check `resumes/tailored/` for tailored resumes
2. Read `application_report_*.txt`
3. Review each job opportunity
4. Manually visit URLs and apply

---

## Step 5: Enable Automated Applying

### Update config.yaml:
```yaml
apply_settings:
  dry_run: false          # ← ENABLE automation
  browser:
    headless: false       # ← Show browser (change to true later)
```

### Run with browser visible (for testing):
```bash
python -m src.main run_once
```

**Browser will:**
1. Open job postings
2. Click "Apply" buttons
3. Upload your tailored resume
4. Fill out forms
5. Submit applications

---

## Step 6: Monitor Applications

### Check application tracking database:
```bash
# View all applications
sqlite3 application_history.db "SELECT * FROM applications;"

# Export report
python -c "
from src.application_tracker import ApplicationTracker
tracker = ApplicationTracker()
tracker.export_report('applications.csv')
print('Report exported to applications.csv')
"
```

### View logs:
```bash
tail logs/resume_analyzer.log
```

---

## Troubleshooting

### Issue: "ChromeDriver not found"
**Solution:**
1. Download ChromeDriver matching your Chrome version
2. Add to PATH: 
   ```bash
   # Windows: Add chromedriver.exe directory to PATH
   # Linux/Mac: cp chromedriver /usr/local/bin/
   ```
3. Or set in .env:
   ```
   BROWSER_DRIVER_PATH=/full/path/to/chromedriver
   ```

### Issue: "LinkedIn Easy Apply button not found"
**Solution:**
- LinkedIn may require manual login first
- Try with `headless=false` to debug
- Some jobs don't have Easy Apply enabled

### Issue: "Applications not being submitted"
**Solution:**
- Check logs: `tail logs/resume_analyzer.log`
- Enable screenshots: Check `logs/apply_attempt_*.png`
- Test with single job first
- Try `headless=false` to see what's happening

### Issue: "Credentials not working"
**Solution:**
- Verify credentials in `.env`
- For Gmail: Use app password (not regular password)
- For LinkedIn: Try a test login in browser first
- Check for special characters that need escaping

---

## Configuration Options

### Browser Settings:
```yaml
browser:
  headless: true              # true = no GUI, false = show browser
  timeout_seconds: 30         # Wait time for elements
  screenshot_on_error: true   # Save screenshot on failure
```

### Rate Limiting:
```yaml
rate_limit:
  enabled: true
  delay_between_apps: 5       # Seconds between applications
  max_apps_per_hour: 10       # Prevent blocking
```

### Retry Logic:
```yaml
retry:
  enabled: true
  max_attempts: 3             # Retry failed applications
  wait_seconds: 5
```

### Notifications:
```yaml
notifications:
  enabled: false
  email_on_success: false
  email_on_failure: false
```

---

## Best Practices

### 1. Start with Manual Mode
```bash
# Keep dry_run=true initially
python -m src.main run_once
# Review results before automation
```

### 2. Test with Single Application
- Run with sample job first
- Watch browser (headless=false)
- Fix any issues before bulk applications

### 3. Monitor Applications
```bash
# Check logs frequently
tail -f logs/resume_analyzer.log

# Check database
sqlite3 application_history.db "SELECT status, COUNT(*) FROM applications GROUP BY status;"
```

### 4. Use Rate Limiting
- Don't apply to >10 jobs/hour (avoid blocking)
- Use 5-10 second delays between applications
- Respect job board terms of service

### 5. Backup Credentials Securely
- Keep `.env` file backed up
- Never share `.env` file
- Rotate passwords periodically

---

## Supported Job Boards

| Board | Status | Notes |
|-------|--------|-------|
| LinkedIn | ✅ Supported | Easy Apply only |
| Indeed | ✅ Supported | Most postings |
| AngelList | ✅ Supported | Startups |
| Generic Sites | ⚠️ Experimental | May need customization |

---

## Advanced: Custom Job Boards

To add support for other job boards:

1. Create handler in `src/job_apply_handlers.py`:
```python
class CustomBoardHandler(JobApplyHandler):
    def apply(self, job: Dict, resume_path: str) -> bool:
        # Implement custom logic
        pass
```

2. Register in `get_apply_handler()` function

3. Update config with new source

---

## Scheduled Automatic Runs

### Run daily at 9:00 AM:
```bash
python -m src.main
# (No "run_once" argument = scheduled mode)
```

**This will:**
- Run at 9:00 AM daily
- Search jobs
- Tailor resumes
- Apply automatically (if configured)
- Send notifications (if configured)
- Press Ctrl+C to stop

---

## Safety Checklist

Before enabling automation, verify:

- [ ] `.env` file is created with credentials
- [ ] `dry_run=true` for first test
- [ ] ChromeDriver is installed
- [ ] Tailored resumes are correct
- [ ] Application report reviewed manually
- [ ] Browser visible (`headless=false`) for debugging
- [ ] Rate limiting enabled (prevent blocking)
- [ ] Logs are being generated
- [ ] Database tracking is working
- [ ] Tested with 1-2 jobs before bulk applying

---

## What's Next?

1. ✅ Setup `.env` credentials
2. ✅ Run with `dry_run=true` (manual review mode)
3. ✅ Review tailored resumes and applications
4. ✅ Test with 1-2 jobs in `headless=false` mode
5. ✅ Enable `dry_run=false` for automation
6. ✅ Set up scheduled daily runs
7. ✅ Monitor application tracking database
8. ✅ Adjust targeting based on results

---

**For questions:** Check logs in `logs/resume_analyzer.log`

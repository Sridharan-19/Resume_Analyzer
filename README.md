# Resume_Analyzer - Automated Job Search & Resume Tailoring System

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Feature](https://img.shields.io/badge/feature-Automated%20Apply-red)

## 🚀 NEW: Automated Job Applications

**Resume Analyzer now includes AUTOMATED JOB APPLICATION capabilities!**

Apply to jobs automatically across LinkedIn, Indeed, AngelList, and more with:
- ✅ Automated form filling
- ✅ Resume upload
- ✅ Application tracking
- ✅ Rate limiting & safety features
- ✅ Manual review mode (recommended first)

See [AUTOMATED_APPLY_SETUP.md](AUTOMATED_APPLY_SETUP.md) for detailed setup instructions.

---

## Overview

Resume_Analyzer is an intelligent job search automation tool designed to help you find and automatically apply for global remote opportunities in **Data Science**, **Generative AI**, **AIML**, and **ML Engineering** roles. 

### Key Features

✅ **Multi-Source Job Scraping**
- Searches RemoteOK, Indeed, LinkedIn, AngelList, and more
- Filters for remote-only positions globally
- Targets 4 specific job roles

✅ **Intelligent Resume Tailoring**
- Analyzes job descriptions using TF-IDF and semantic analysis
- Creates role-specific resume versions
- Highlights relevant skills and experience
- Improves ATS (Applicant Tracking System) matching

✅ **Automated Job Applications** ⭐ NEW
- Auto-apply to jobs across multiple platforms
- Secure credential management
- Browser automation with Selenium
- Application tracking database
- Rate limiting to avoid blocking
- Dry-run mode for manual review first

✅ **Scheduled Pipeline**
- Daily job searches (configurable time)
- Batch resume generation
- Application readiness reports
- Automatic submissions (with manual review option)

✅ **Role-Specific Optimization**
- **Data Scientist**: Focus on analytics, ML, statistical modeling
- **Gen AI Engineer**: Emphasis on LLM, RAG, prompt engineering, agentic AI
- **AIML Engineer**: Deep learning, computer vision, transformers
- **ML Engineer**: Model development, feature engineering, production systems

---

## Quick Start

### 1. Setup Environment

```powershell
# Clone/navigate to project
cd D:\My_Projects\Resume_Analyzer

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (including automation libraries)
pip install -r requirements.txt
```

### 2. Configure Your Profile

**Your Resume:**
- Your actual resume is in `resumes/base_resume.txt` ✅ Already loaded
- The system tailors this resume for each job

### 3. Choose Application Mode

#### Option A: Manual Review Mode (Recommended First)
```yaml
# config.yaml
apply_settings:
  dry_run: true   # ← Prepare applications, don't submit
```

```bash
python -m src.main run_once
# Reviews jobs, tailors resumes, shows URLs for manual submission
```

#### Option B: Fully Automated Mode
```yaml
# config.yaml
apply_settings:
  dry_run: false  # ← Automatically submit applications
```

**IMPORTANT:** Set up credentials first! See Step 4 below.

### 4. Setup Credentials (For Automated Apply)

**Copy template:**
```bash
cp .env.example .env
```

**Edit `.env` with your credentials:**
```
LINKEDIN_EMAIL=your-email@gmail.com
LINKEDIN_PASSWORD=your-password

INDEED_EMAIL=your-email@gmail.com
INDEED_PASSWORD=your-password
```

**⚠️ Security:** Never commit `.env` to version control!

See [AUTOMATED_APPLY_SETUP.md](AUTOMATED_APPLY_SETUP.md) for full setup instructions.

### 5. Run the Pipeline

**Test Mode (Manual Submission):**
```powershell
python -m src.main run_once
```

**Automated Mode:**
```powershell
# Ensure dry_run=false and .env is configured
python -m src.main run_once
```

**Scheduled Mode (Daily):**
```powershell
python -m src.main
# Runs daily at configured time (see config.yaml)
```

---

## What Happens When You Run It

### Manual Review Mode (dry_run=true)
```
┌─────────────────────────────────────────────────────────┐
│ 1. SEARCH JOBS                                          │
├─────────────────────────────────────────────────────────┤
│ 2. FILTER FOR REMOTE + TARGET ROLES                    │
├─────────────────────────────────────────────────────────┤
│ 3. TAILOR RESUME FOR EACH JOB                          │
├─────────────────────────────────────────────────────────┤
│ 4. GENERATE APPLICATION REPORT                         │
├─────────────────────────────────────────────────────────┤
│ 5. PREPARE LINKS FOR MANUAL SUBMISSION                 │
│    ✅ You review and manually apply                    │
└─────────────────────────────────────────────────────────┘
```

### Automated Mode (dry_run=false)
```
┌─────────────────────────────────────────────────────────┐
│ 1. SEARCH JOBS                                          │
├─────────────────────────────────────────────────────────┤
│ 2. FILTER FOR REMOTE + TARGET ROLES                    │
├─────────────────────────────────────────────────────────┤
│ 3. TAILOR RESUME FOR EACH JOB                          │
├─────────────────────────────────────────────────────────┤
│ 4. OPEN BROWSER & AUTO-APPLY                           │
│    - Click Apply buttons                               │
│    - Fill forms                                        │
│    - Upload resume                                     │
│    - Submit                                            │
├─────────────────────────────────────────────────────────┤
│ 5. TRACK APPLICATION IN DATABASE                       │
├─────────────────────────────────────────────────────────┤
│ 6. GENERATE REPORT WITH RESULTS                        │
└─────────────────────────────────────────────────────────┘
```

### Output Files

```
resumes/
  ├── base_resume.txt                    (Your main resume)
  └── tailored/
      ├── tailored_Company_DataScientist.txt
      ├── application_report_20250607_090000.txt
      └── ... (one per job)

logs/
  ├── resume_analyzer.log                (Execution logs)
  └── apply_attempt_*.png                (Screenshots on error)

application_history.db                   (Application tracking)
applications.csv                         (Export report)
```

---

## File Structure

```
Resume_Analyzer/
├── AUTOMATED_APPLY_SETUP.md             ← Start here for automation!
├── README.md                            (This file)
├── config.yaml                          (Your configuration)
├── config.example.yaml                  (Configuration template)
├── .env.example                         (Credentials template)
├── requirements.txt                     (Python dependencies)
│
├── resumes/
│   ├── base_resume.txt                  (Your resume - Sri's profile)
│   └── tailored/                        (Generated tailored resumes)
│
├── src/
│   ├── __init__.py
│   ├── main.py                          (Pipeline orchestrator)
│   ├── resume_tailer.py                 (Resume tailoring engine)
│   ├── apply.py                         (Application handler)
│   ├── credentials.py                   (Secure credential management)
│   ├── browser_automation.py            (Selenium wrapper)
│   ├── job_apply_handlers.py            (Job board-specific logic)
│   ├── application_tracker.py           (Track submitted applications)
│   └── scrapers/
│       └── example_scraper.py           (Job scraping implementations)
│
└── logs/
    └── resume_analyzer.log              (Pipeline execution logs)
```

---

## Your Resume Profile

**Status:** ✅ Loaded and configured

**Background:**
- Senior Data Scientist with **7+ years** production experience
- Contact: sridharanchandran1904@gmail.com | +91 7598998545
- LinkedIn: https://www.linkedin.com/in/sridharan-c-055466148/
- GitHub: https://github.com/Sridharan-19
- Portfolio: https://eportfolio.mygreatlearning.com/sridharan22

**Specialized in:**
- Generative AI, Agentic AI, LLM systems, IDP
- PyTorch, TensorFlow, RAG, LangChain, Transformers
- Azure, AWS, GCP cloud platforms

**Target Roles:**
1. **Data Scientist** - Analytics & ML expertise
2. **Gen AI Engineer** - LLM & RAG focus
3. **AIML Engineer** - Deep learning & CV
4. **ML Engineer** - Production models & MLOps

---

## Automated Apply - Key Features

### Security
- ✅ Credentials stored in `.env` (never in code)
- ✅ App passwords supported (Gmail, etc.)
- ✅ No credentials logged

### Safety
- ✅ Dry-run mode for manual review first
- ✅ Rate limiting (prevent blocking)
- ✅ Application tracking (no duplicates)
- ✅ Error handling & screenshots

### Supported Platforms
| Platform | Auto-Apply | Status |
|----------|-----------|--------|
| LinkedIn | Easy Apply | ✅ Supported |
| Indeed | Standard Form | ✅ Supported |
| AngelList | Native Apply | ✅ Supported |
| Generic | Any Site | ⚠️ Experimental |

---

## Configuration Examples

### Example 1: Manual Mode (Recommended First)
```yaml
run_time:
  hour: 9
  minute: 0

apply_settings:
  dry_run: true           # Manual review
  manual_review: true
```

### Example 2: Fully Automated
```yaml
apply_settings:
  dry_run: false          # Auto-apply
  browser:
    headless: true        # No GUI
  rate_limit:
    enabled: true
    delay_between_apps: 5
```

### Example 3: Scheduled Daily
```yaml
run_time:
  hour: 9
  minute: 0

schedule_daily(config)    # Runs every day at 9 AM
```

---

## Quick Commands

### Setup
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup credentials
cp .env.example .env
# Edit .env with your credentials
```

### Running
```powershell
# Test with manual review
python -m src.main run_once

# Auto-apply (if configured)
python -m src.main run_once

# Scheduled daily
python -m src.main

# View logs
type logs/resume_analyzer.log

# Check applications
sqlite3 application_history.db "SELECT * FROM applications;"
```

---

## Troubleshooting

### Common Issues

**"ChromeDriver not found"**
- Download matching ChromeDriver from https://chromedriver.chromium.org/
- Add to PATH or set in `.env`

**"Credentials not working"**
- For Gmail: Use app password (not regular password)
- For LinkedIn: Test login manually first

**"Applications not submitting"**
- Check logs: `tail logs/resume_analyzer.log`
- Try `headless: false` to debug
- Review screenshots: `ls logs/apply_attempt_*.png`

**"No jobs found"**
- Check internet connection
- Verify job board APIs are accessible
- Check logs for API errors

---

## Next Steps

1. ✅ [Read AUTOMATED_APPLY_SETUP.md for detailed setup](AUTOMATED_APPLY_SETUP.md)
2. ✅ Run with `dry_run=true` (manual review first)
3. ✅ Review tailored resumes
4. ✅ Test with 1-2 jobs before bulk automation
5. ✅ Set up `.env` credentials
6. ✅ Enable `dry_run=false` for automation
7. ✅ Configure scheduled daily runs
8. ✅ Monitor application tracking

---

## Support

- **Setup Help:** See [AUTOMATED_APPLY_SETUP.md](AUTOMATED_APPLY_SETUP.md)
- **Issues:** Check `logs/resume_analyzer.log`
- **Database:** `sqlite3 application_history.db`
- **Enhancement:** Modify `src/` for custom behavior

---

## License

MIT License - Feel free to modify and use

---

**Ready to automate your job search?** Start with the setup guide: [AUTOMATED_APPLY_SETUP.md](AUTOMATED_APPLY_SETUP.md)


## Overview

Resume_Analyzer is an intelligent job search automation tool designed to help you find and apply for global remote opportunities in **Data Science**, **Generative AI**, **AIML**, and **ML Engineering** roles. 

### Key Features

✅ **Multi-Source Job Scraping**
- Searches RemoteOK, Indeed, LinkedIn, AngelList, and more
- Filters for remote-only positions globally
- Targets 4 specific job roles

✅ **Intelligent Resume Tailoring**
- Analyzes job descriptions using TF-IDF and semantic analysis
- Creates role-specific resume versions
- Highlights relevant skills and experience
- Improves ATS (Applicant Tracking System) matching

✅ **Automated Pipeline**
- Scheduled daily job searches
- Batch resume generation
- Application readiness reports
- Manual review before submission

✅ **Role-Specific Optimization**
- **Data Scientist**: Focus on analytics, ML, statistical modeling
- **Gen AI Engineer**: Emphasis on LLM, RAG, prompt engineering, agentic AI
- **AIML Engineer**: Deep learning, computer vision, transformers
- **ML Engineer**: Model development, feature engineering, production systems

---

## Quick Start

### 1. Setup Environment

```powershell
# Clone/navigate to project
cd D:\My_Projects\Resume_Analyzer

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Your Profile

**Your Resume:**
- Your actual resume has been loaded into `resumes/base_resume.txt`
- The system will tailor this resume for each job

**Job Board Configurations:**
```bash
# Copy example config (already done)
# Update for your preferences
```

### 3. Setup Configuration

Edit `config.yaml` (or use example):

```yaml
resume_path: "resumes/base_resume.txt"

run_time:
  hour: 9      # Daily run time
  minute: 0

target_roles:
  - "Data Scientist"
  - "Gen AI Engineer"
  - "AIML Engineer"
  - "ML Engineer"

location_requirements:
  remote_only: true
  countries: ["Global", "USA", "Canada", "UK", "Germany", "India", "Australia"]

apply_settings:
  dry_run: true  # Set to false for automated submissions
  manual_review: true
```

### 4. Run the Pipeline

**Run Once (for testing):**
```powershell
python -m src.main run_once
```

**Run Scheduled (continuous background mode):**
```powershell
python -m src.main
```

**Display Help:**
```powershell
python -m src.main --help
```

---

## What Happens When You Run It

### Pipeline Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. LOAD CONFIGURATION                                   │
│    └─ Read target roles, job sources, scheduling        │
├─────────────────────────────────────────────────────────┤
│ 2. FETCH JOBS FROM MULTIPLE SOURCES                    │
│    ├─ RemoteOK (specialized remote jobs)               │
│    ├─ Indeed (large job board)                         │
│    ├─ LinkedIn (professional network)                  │
│    └─ AngelList (startup ecosystem)                    │
├─────────────────────────────────────────────────────────┤
│ 3. FILTER JOBS                                         │
│    ├─ Remove non-remote positions                      │
│    ├─ Keep only target roles                           │
│    └─ Exclude entry-level/intern positions             │
├─────────────────────────────────────────────────────────┤
│ 4. TAILOR RESUME FOR EACH JOB                          │
│    ├─ Analyze job description                          │
│    ├─ Extract role type (Data Scientist/Gen AI/etc)    │
│    ├─ Identify matching skills in your resume          │
│    └─ Create role-specific tailored resume             │
├─────────────────────────────────────────────────────────┤
│ 5. PREPARE APPLICATION                                 │
│    ├─ Generate apply-ready documentation               │
│    ├─ Create application report                        │
│    └─ Save all tailored resumes                        │
├─────────────────────────────────────────────────────────┤
│ 6. OUTPUT REPORT                                       │
│    ├─ List all opportunities found                     │
│    ├─ Show tailored resume locations                   │
│    ├─ Provide application URLs                         │
│    └─ Ready for manual submission or automation        │
└─────────────────────────────────────────────────────────┘
```

### Output Files

After running the pipeline:

```
resumes/
  ├── base_resume.txt              (Your main resume)
  └── tailored/
      ├── tailored_Company_DataScientist.txt
      ├── tailored_Company_GenAIEngineer.txt
      ├── application_report_20250607_090000.txt
      └── ... (one per job opportunity)

logs/
  └── resume_analyzer.log           (Execution logs)
```

---

## File Structure

```
Resume_Analyzer/
├── config.example.yaml             # Configuration template
├── config.yaml                     # Your configuration (create after copying example)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── resumes/
│   ├── base_resume.txt             # Your actual resume (updated with Sri's resume)
│   └── tailored/                   # Generated tailored resumes
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # Main pipeline orchestrator
│   ├── resume_tailer.py            # Resume tailoring engine
│   ├── apply.py                    # Application handler & reporting
│   └── scrapers/
│       └── example_scraper.py      # Job scraping implementations
│
└── logs/
    └── resume_analyzer.log         # Pipeline execution logs
```

---

## Your Resume Profile

**Current Status:** ✅ Loaded and configured

**Background:**
- Senior Data Scientist with **7+ years** of production experience
- Specialized in: Generative AI, Agentic AI, LLM systems, IDP
- Expert in: PyTorch, TensorFlow, RAG, LangChain, Transformers
- Cloud Proficiency: Azure, AWS, GCP

**Target Roles:**
1. **Data Scientist** - Leveraging analytics & ML modeling expertise
2. **Gen AI Engineer** - Emphasizing LLM, RAG, prompt engineering
3. **AIML Engineer** - Highlighting deep learning & computer vision
4. **ML Engineer** - Production model development & MLOps

**Relevant Skills Matched:**
- Machine Learning: Scikit-learn, XGBoost, RandomForest, Time Series
- Deep Learning: PyTorch, TensorFlow, Transformers
- Gen AI: LangChain, RAG, Agentic AI, GPT, Claude, Gemini
- NLP: NER, Classification, Semantic Search, PubMedBERT, DeBERTa
- Computer Vision: YOLO, EfficientNet, Image Processing
- Cloud/MLOps: Azure, AWS, GCP, Docker, CI/CD

**Key Accomplishments Highlighted:**
- ✓ Designed 15+ Agentic AI enterprise solutions
- ✓ Built end-to-end IDP systems for insurance (20+ agencies)
- ✓ Achieved 91% demand forecasting accuracy
- ✓ Delivered 18% sales increase via ML cross-sell
- ✓ 7+ years architecting production AI systems

---

## Configuration Examples

### Example 1: Daily Scheduled Search

```yaml
# Runs every day at 9:00 AM
run_time:
  hour: 9
  minute: 0

target_roles:
  - "Data Scientist"
  - "Gen AI Engineer"

location_requirements:
  remote_only: true
```

### Example 2: Multiple Job Sources

```yaml
scrapers:
  - type: "remoteok"
    enabled: true
  - type: "indeed"
    enabled: true
  - type: "linkedin"
    enabled: true
  - type: "angellist"
    enabled: true
```

### Example 3: Role-Specific Tailoring

```yaml
tailoring:
  enabled: true
  strategy: "role-specific"  # Different tailoring per role
  highlight_relevant_projects: true
  add_skill_matching: true
```

---

## Job Boards Supported

| Source | Type | Coverage | Remote Filter | Notes |
|--------|------|----------|---------------|-------|
| **RemoteOK** | API | 50K+ remote jobs | Native | Best for remote-first jobs |
| **Indeed** | Scraping | 1M+ jobs | Manual | Largest job board |
| **LinkedIn** | Limited | Millions | Manual | Professional network |
| **AngelList** | API | Startup focused | Native | Good for AI startups |
| **We Work Remotely** | RSS/Scraping | 10K+ | Native | Remote specialist |
| **FlexJobs** | API | Vetted jobs | Native | Premium curated |

---

## Advanced Usage

### Automatic Application Submission (Experimental)

**WARNING:** Enable only with careful testing and security measures.

To enable automated submissions:

1. Update `config.yaml`:
```yaml
apply_settings:
  dry_run: false
```

2. Implement site-specific automation in `src/apply.py`:
   - Use Selenium/Playwright for web forms
   - Integrate job board APIs
   - Set up secure credential management

3. Test with a single job first

### Custom Scrapers

Add new job sources in `src/scrapers/example_scraper.py`:

```python
def _fetch_your_source_jobs() -> List[Dict]:
    """Fetch from your custom source."""
    jobs = []
    # Implement scraping logic
    return jobs
```

### Resume Customization

Modify resume tailoring strategy in `src/resume_tailer.py`:

```python
ROLE_KEYWORDS = {
    "Your Role": [
        "keyword1", "keyword2", ...
    ]
}
```

---

## Troubleshooting

### Issue: "Config not found"
**Solution:** Copy `config.example.yaml` to `config.yaml`:
```bash
cp config.example.yaml config.yaml
```

### Issue: "Resume not found"
**Solution:** Ensure `base_resume.txt` exists in `resumes/` directory

### Issue: No jobs found
**Solution:** 
- Check internet connection
- Verify job board APIs are accessible
- Review logs: `logs/resume_analyzer.log`

### Issue: Import errors
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ **Created:** Your actual resume profile in `base_resume.txt`
2. ✅ **Configured:** Job sources and target roles
3. ✅ **Implemented:** Role-specific resume tailoring
4. 🔲 **TODO:** 
   - Run `python -m src.main run_once` for first test
   - Review `resumes/tailored/` for tailored resumes
   - Manually apply to top 5 opportunities
   - Collect feedback and refine targeting
   - Set up scheduled runs for continuous updates

---

## Best Practices

1. **Review Before Applying**
   - Read each tailored resume
   - Check job description alignment
   - Ensure quality before submission

2. **Track Applications**
   - Keep notes on submitted applications
   - Track response dates
   - Follow up after 2 weeks

3. **Refine Your Search**
   - Adjust target roles as needed
   - Update resume based on feedback
   - Remove companies that don't respond

4. **Optimize for ATS**
   - Use standard formatting
   - Include keywords naturally
   - Avoid graphics/tables in resume

5. **Security & Privacy**
   - Keep credentials secure
   - Don't enable auto-submit without testing
   - Review all applications before submission

---

## Support & Contribution

- **Issues?** Check logs in `logs/resume_analyzer.log`
- **Enhancements?** Modify `src/` files for custom behavior
- **Documentation?** See configuration examples above

---

## License

MIT License - Feel free to modify and use

---

## Quick Command Reference

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run once
python -m src.main run_once

# Run scheduled
python -m src.main

# Install dependencies
pip install -r requirements.txt

# View logs
type logs/resume_analyzer.log

# Check tailored resumes
ls resumes/tailored/

# Stop scheduler (running in terminal)
Ctrl + C
```

---

**Status:** Ready for deployment! Your resume has been configured for the 4 target roles with intelligent tailoring enabled. Start with `python -m src.main run_once` for the first test run.

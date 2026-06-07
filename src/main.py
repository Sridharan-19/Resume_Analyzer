"""
Resume Analyzer - Automated job search and resume tailoring pipeline.
Searches remote job opportunities, tailors resume to match, and applies automatically or prepares for manual submission.
"""

import os
import sys
import yaml
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from src.scrapers.example_scraper import fetch_jobs, fetch_jobs_for_role
from src.resume_tailer import tailor_resume_for_job, _extract_job_role
from src.apply import apply_to_job, prepare_application_report

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger("resume_analyzer")

ROOT = os.path.dirname(os.path.dirname(__file__))


def load_config(path="config.yaml"):
    """Load configuration from YAML file."""
    if not os.path.exists(path):
        log.warning("Config not found at %s, using example config.", path)
        path = os.path.join(ROOT, "config.example.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def filter_jobs_by_criteria(jobs, config):
    """
    Filter jobs based on location, role, and other criteria.
    
    Args:
        jobs: List of job dictionaries
        config: Configuration dictionary
    
    Returns:
        Filtered list of jobs
    """
    target_roles = config.get("target_roles", [])
    location_req = config.get("location_requirements", {})
    remote_only = location_req.get("remote_only", True)
    
    filtered = []
    
    for job in jobs:
        # Check if remote
        location = job.get("location", "").lower()
        if remote_only and "remote" not in location:
            continue
        
        # Check if target role
        title = job.get("title", "").lower()
        is_target_role = any(role.lower() in title for role in target_roles)
        if not is_target_role:
            continue
        
        # Check for exclusions
        if any(exclude in title for exclude in ["intern", "entry-level", "junior junior"]):
            continue
        
        filtered.append(job)
    
    return filtered


def run_pipeline(config):
    """
    Execute the full job search and resume tailoring pipeline.
    
    Args:
        config: Configuration dictionary
    """
    log.info("="*80)
    log.info("RESUME ANALYZER PIPELINE STARTED: %s", datetime.now().isoformat())
    log.info("="*80)
    
    resume_path = config.get("resume_path", "resumes/base_resume.txt")
    target_roles = config.get("target_roles", [])
    apply_config = config.get("apply_settings", {})
    dry_run = apply_config.get("dry_run", True)
    
    if not os.path.exists(resume_path):
        log.error("Resume not found at: %s", resume_path)
        return
    
    jobs = []
    
    # Fetch jobs from configured scrapers
    scrapers_config = config.get("scrapers", [])
    log.info("Configured scrapers: %d", len(scrapers_config))
    
    for scraper in scrapers_config:
        if not scraper.get("enabled", True):
            continue
        
        scraper_type = scraper.get("type", "")
        log.info("Fetching jobs from: %s", scraper_type)
        
        try:
            scraped_jobs = fetch_jobs(source=scraper_type)
            jobs.extend(scraped_jobs)
            log.info("✓ Found %d jobs from %s", len(scraped_jobs), scraper_type)
        except Exception as e:
            log.warning("✗ Error fetching from %s: %s", scraper_type, str(e))
    
    log.info("-"*80)
    log.info("Total jobs fetched: %d", len(jobs))
    
    # Filter jobs
    filtered_jobs = filter_jobs_by_criteria(jobs, config)
    log.info("After filtering (remote + target roles): %d", len(filtered_jobs))
    
    # Process each job
    applications = []
    tailoring_config = config.get("tailoring", {})
    
    # Get browser settings
    browser_config = apply_config.get("browser", {})
    headless = browser_config.get("headless", True)
    
    for i, job in enumerate(filtered_jobs, 1):
        log.info("\n[%d/%d] Processing: %s @ %s", i, len(filtered_jobs), 
                job.get("title", "Unknown"), job.get("company", "Unknown"))
        
        try:
            # Tailor resume
            tailored_path = tailor_resume_for_job(resume_path, job)
            
            # Apply to job (manual or automated based on dry_run setting)
            apply_info = apply_to_job(
                job.get("apply_url"),
                tailored_path,
                job,
                dry_run=dry_run,
                headless=headless
            )
            
            applications.append({
                "job": job,
                "tailored_resume": tailored_path,
                "apply_info": apply_info
            })
            
            # Rate limiting
            if apply_config.get("rate_limit", {}).get("enabled", True) and not dry_run:
                delay = apply_config.get("rate_limit", {}).get("delay_between_apps", 5)
                time.sleep(delay)
            
        except Exception as e:
            log.error("Error processing job %s: %s", job.get("title"), str(e))
            continue
    
    # Generate report
    log.info("\n" + "="*80)
    log.info("PIPELINE SUMMARY")
    log.info("="*80)
    log.info("Total applications processed: %d", len(applications))
    
    # Group by role type
    by_role = {}
    for app in applications:
        role = _extract_job_role(app["job"].get("title", ""))
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(app)
    
    for role, apps in by_role.items():
        log.info("  %s: %d applications", role, len(apps))
    
    # Create report file
    report = prepare_application_report(applications, config)
    report_path = os.path.join(config.get("output_directory", "resumes/tailored"), 
                               f"application_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log.info("\nApplication report saved: %s", report_path)
    
    # Log application mode
    if dry_run:
        log.info("MODE: Manual Review (dry_run=true)")
    else:
        log.info("MODE: Automated Apply (dry_run=false)")
    
    log.info("="*80)
    log.info("Pipeline completed at: %s", datetime.now().isoformat())
    log.info("="*80)


def schedule_daily(config):
    """Schedule pipeline to run daily."""
    sched = BackgroundScheduler()
    run_time = config.get("run_time", {"hour": 9, "minute": 0})
    hour = run_time.get("hour", 9)
    minute = run_time.get("minute", 0)
    
    sched.add_job(lambda: run_pipeline(config), 'cron', hour=hour, minute=minute)
    sched.start()
    
    log.info("Scheduler started (daily at %02d:%02d)", hour, minute)
    log.info("Press Ctrl+C to stop the scheduler")
    
    try:
        # keep running
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        log.info("Shutting down scheduler...")
        sched.shutdown()


def main():
    """Main entry point."""
    cfg = load_config()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "run_once":
            log.info("Running pipeline once...")
            run_pipeline(cfg)
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
Resume Analyzer - Automated Job Search & Resume Tailoring

Usage:
  python -m src.main              Run scheduler (daily at configured time)
  python -m src.main run_once     Run pipeline once immediately
  python -m src.main --help       Show this help message

Configuration:
  Edit config.yaml to configure job sources, target roles, and scheduling.
  Default config location: config.yaml (falls back to config.example.yaml)
            """)
            return
    
    # Default: run scheduler
    schedule_daily(cfg)


if __name__ == "__main__":
    main()


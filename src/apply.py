"""
Application handling and tracking module.
Manages job applications with dry-run and automated submission options.
Supports multiple job boards with dedicated handlers.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from src.application_tracker import ApplicationTracker
from src.job_apply_handlers import get_apply_handler
from src.credentials import CredentialManager

log = logging.getLogger(__name__)

# Global tracker instance
tracker = ApplicationTracker()


def apply_to_job(apply_url: str, resume_path: str, job: Dict = None, 
                 dry_run: bool = True, headless: bool = True) -> Dict:
    """
    Apply to a job posting (manual or automated).
    
    Args:
        apply_url: URL where application can be submitted
        resume_path: Path to tailored resume for this job
        job: Job details dictionary
        dry_run: If True, only prepare without submitting
        headless: Run browser in headless mode (no GUI)
    
    Returns:
        Application info dictionary
    """
    job = job or {}
    
    apply_info = {
        "timestamp": datetime.now().isoformat(),
        "job_title": job.get("title", "Unknown"),
        "company": job.get("company", "Unknown"),
        "apply_url": apply_url,
        "resume_path": resume_path,
        "status": "pending",
        "dry_run": dry_run,
    }
    
    # Check if already applied
    if tracker.is_already_applied(apply_url):
        log.warning(f"Already applied to: {apply_url}")
        apply_info["status"] = "already_applied"
        return apply_info
    
    # Record application attempt
    tracker.add_application(job, resume_path, status="pending")
    
    if dry_run:
        # Manual review mode
        log.info("DRY-RUN: Prepared application for %s @ %s", 
                apply_info["job_title"], apply_info["company"])
        log.info("  URL: %s", apply_url)
        log.info("  Resume: %s", resume_path)
        apply_info["status"] = "ready_for_manual_review"
        tracker.log_audit(apply_url, "DRY_RUN", "Prepared for manual submission")
        
        print(f"\n{'='*80}")
        print(f"APPLICATION READY: Manual Submission")
        print(f"{'='*80}")
        print(f"Job Title: {apply_info['job_title']}")
        print(f"Company: {apply_info['company']}")
        print(f"Location: {job.get('location', 'Not specified')}")
        print(f"Salary: {job.get('salary_range', 'Not specified')}")
        print(f"\nTailored Resume: {resume_path}")
        print(f"Apply URL: {apply_url}")
        print(f"\nNext Steps:")
        print(f"1. Open the URL in your browser")
        print(f"2. Review the job description")
        print(f"3. Upload the tailored resume")
        print(f"4. Complete any required fields")
        print(f"5. Submit application")
        print(f"{'='*80}\n")
        
        return apply_info
    
    # Automated submission mode
    return _apply_automated(job, resume_path, apply_info, headless)


def _apply_automated(job: Dict, resume_path: str, apply_info: Dict, 
                     headless: bool = True) -> Dict:
    """
    Attempt automated application submission.
    
    Args:
        job: Job details
        resume_path: Path to tailored resume
        apply_info: Application info dict to update
        headless: Run browser in headless mode
    
    Returns:
        Updated application info
    """
    log.info(f"AUTOMATED: Attempting to apply to {job.get('title')} @ {job.get('company')}")
    
    try:
        # Get appropriate handler for job source
        job_source = job.get('source', 'generic')
        handler = get_apply_handler(job_source, headless=headless)
        
        # Attempt application
        success = handler.apply(job, resume_path)
        
        if success:
            apply_info["status"] = "applied"
            log.info(f"Application successful: {job.get('apply_url')}")
            tracker.update_application_status(job.get('apply_url'), "applied")
            tracker.log_audit(job.get('apply_url'), "AUTO_SUBMIT_SUCCESS", 
                            f"Applied via {job_source}")
        else:
            apply_info["status"] = "apply_failed"
            log.warning(f"Application failed: {job.get('apply_url')}")
            tracker.update_application_status(job.get('apply_url'), "failed", 
                                            "Automated submission failed")
            tracker.log_audit(job.get('apply_url'), "AUTO_SUBMIT_FAILED", 
                            f"Failed to apply via {job_source}")
    
    except Exception as e:
        log.error(f"Error in automated application: {e}")
        apply_info["status"] = "error"
        tracker.update_application_status(job.get('apply_url'), "error", str(e))
        tracker.log_audit(job.get('apply_url'), "AUTO_SUBMIT_ERROR", str(e))
    
    return apply_info


def prepare_application_report(applications: List[Dict], config: Dict) -> str:
    """
    Generate a comprehensive application report.
    
    Args:
        applications: List of application dictionaries
        config: Configuration dictionary
    
    Returns:
        Report text
    """
    report = []
    report.append("="*100)
    report.append("RESUME ANALYZER - APPLICATION REPORT")
    report.append("="*100)
    report.append(f"\nGenerated: {datetime.now().isoformat()}")
    report.append(f"Total Applications: {len(applications)}")
    report.append("\n")
    
    # Group by role
    by_role = {}
    for app in applications:
        job = app.get("job", {})
        role = job.get("role_type", "Unknown")
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(app)
    
    # Summary by role
    report.append("SUMMARY BY ROLE")
    report.append("-"*100)
    for role, apps in sorted(by_role.items()):
        report.append(f"  {role}: {len(apps)} applications")
    report.append("\n")
    
    # Detailed applications
    report.append("DETAILED APPLICATION LIST")
    report.append("="*100)
    
    for i, app in enumerate(applications, 1):
        job = app.get("job", {})
        
        report.append(f"\n[{i}] {job.get('title', 'Unknown')} @ {job.get('company', 'Unknown')}")
        report.append("-"*100)
        report.append(f"Location:         {job.get('location', 'Not specified')}")
        report.append(f"Salary:           {job.get('salary_range', 'Not specified')}")
        report.append(f"Source:           {job.get('source', 'Unknown')}")
        report.append(f"Posted Date:      {job.get('posted_date', 'Unknown')}")
        report.append(f"Apply URL:        {job.get('apply_url', 'N/A')}")
        report.append(f"Tailored Resume:  {app.get('tailored_resume', 'N/A')}")
        report.append(f"Status:           {app.get('apply_info', {}).get('status', 'Unknown')}")
        
        description = job.get('description', '')
        if description:
            report.append(f"\nJob Description (first 500 chars):")
            report.append(description[:500] + "...\n")
    
    report.append("\n" + "="*100)
    report.append("NEXT STEPS")
    report.append("="*100)
    report.append("""
1. Review each application's details above
2. Open the tailored resume file in the editor
3. Visit the Apply URL and submit your application
4. Keep track of submitted applications
5. Follow up with companies after 1-2 weeks

TIPS FOR SUCCESS:
• Customize your cover letter (if requested) based on the tailored resume
• Highlight the role-specific accomplishments in your tailored resume
• Check your email for application confirmations
• Track application dates for follow-ups
• Update your resume based on feedback/rejections

For questions or issues, review the application report above.
    """.strip())
    
    return "\n".join(report)


def save_application_history(applications: List[Dict], history_path: str = "application_history.txt"):
    """
    Save application history for tracking.
    
    Args:
        applications: List of applications
        history_path: Path to save history file
    """
    with open(history_path, 'a', encoding='utf-8') as f:
        for app in applications:
            job = app.get("job", {})
            f.write(f"{datetime.now().isoformat()} | {job.get('title')} @ {job.get('company')} | {job.get('apply_url')}\n")
    
    log.info("Application history saved: %s", history_path)


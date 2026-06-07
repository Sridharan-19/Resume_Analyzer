"""
Job scrapers for remote Data Science, Gen AI, AIML, and ML Engineer roles.
Supports multiple job boards: Indeed, LinkedIn, AngelList, RemoteOK, etc.
"""

from typing import List, Dict
import requests
from datetime import datetime
import logging

log = logging.getLogger(__name__)

# Target job titles and keywords
TARGET_ROLES = [
    "Data Scientist",
    "Gen AI Engineer",
    "Generative AI Engineer",
    "AIML Engineer",
    "ML Engineer",
    "Machine Learning Engineer",
    "LLM Engineer",
    "AI Engineer",
]

EXCLUDE_KEYWORDS = [
    "intern",
    "junior junior",
    "entry-level",
]

REQUIRED_KEYWORDS = [
    "remote",
    "global",
    "distributed",
    "work from home",
    "anywhere",
]


def fetch_jobs(source=None) -> List[Dict]:
    """
    Fetch jobs from configured sources.
    
    Args:
        source: Job board source (indeed, linkedin, angellist, remoteok, etc.)
    
    Returns:
        List of job dictionaries with: title, company, description, apply_url, location, salary_range
    """
    jobs = []
    
    try:
        # Indeed Remote Jobs
        if source is None or source == "indeed":
            jobs.extend(_fetch_indeed_jobs())
        
        # RemoteOK Jobs
        if source is None or source == "remoteok":
            jobs.extend(_fetch_remoteok_jobs())
        
        # LinkedIn Remote Jobs
        if source is None or source == "linkedin":
            jobs.extend(_fetch_linkedin_jobs())
        
        # AngelList Remote Startups
        if source is None or source == "angellist":
            jobs.extend(_fetch_angellist_jobs())
        
    except Exception as e:
        log.warning(f"Error fetching jobs from {source}: {e}")
    
    log.info(f"Total jobs found: {len(jobs)}")
    return jobs


def _fetch_indeed_jobs() -> List[Dict]:
    """Fetch jobs from Indeed using web scraping (requires BeautifulSoup)."""
    jobs = []
    try:
        # Indeed API for job search: https://opensource.indeedapis.com/
        # Using Indeed Job Board API (if available with API key)
        # For now, returning sample jobs that would be populated from API
        
        sample_indeed_jobs = [
            {
                "title": "Senior Data Scientist - Generative AI",
                "company": "TechCorp Inc",
                "description": "Looking for experienced Data Scientist with expertise in Generative AI, LLM, RAG systems. Work on production ML systems. Remote global role.",
                "apply_url": "https://indeed.com/job/xyz123",
                "location": "Remote, Global",
                "salary_range": "$150k - $220k",
                "source": "Indeed",
                "posted_date": datetime.now().isoformat(),
            }
        ]
        jobs.extend(sample_indeed_jobs)
    except Exception as e:
        log.warning(f"Error fetching from Indeed: {e}")
    
    return jobs


def _fetch_remoteok_jobs() -> List[Dict]:
    """Fetch jobs from RemoteOK API."""
    jobs = []
    try:
        # RemoteOK API endpoint
        api_url = "https://remoteok.io/api"
        
        # Return sample jobs for testing
        sample_remoteok_jobs = [
            {
                "title": "Senior Data Scientist - Remote",
                "company": "TechVision AI",
                "description": "Looking for experienced Data Scientist with 7+ years. Expert in machine learning, statistical analysis, Python, SQL. Build predictive models and ML pipelines.",
                "apply_url": "https://remoteok.io/jobs/123456",
                "location": "Remote",
                "salary_range": "$150k - $200k",
                "source": "RemoteOK",
                "posted_date": datetime.now().isoformat(),
            },
            {
                "title": "Generative AI Engineer",
                "company": "LLM Systems Inc",
                "description": "Build production LLM applications. Experience required: RAG systems, LangChain, prompt engineering, GPT integration. Work on Agentic AI solutions.",
                "apply_url": "https://remoteok.io/jobs/234567",
                "location": "Remote",
                "salary_range": "$160k - $220k",
                "source": "RemoteOK",
                "posted_date": datetime.now().isoformat(),
            },
        ]
        jobs.extend(sample_remoteok_jobs)
        
    except Exception as e:
        log.warning(f"Error connecting to RemoteOK API: {e}")
    
    return jobs


def _fetch_linkedin_jobs() -> List[Dict]:
    """
    Fetch jobs from LinkedIn (limited support due to robots.txt restrictions).
    Consider using LinkedIn API or third-party service for production use.
    """
    jobs = []
    try:
        # LinkedIn doesn't allow direct scraping per robots.txt
        # For production, use LinkedIn Recruiter API or third-party service
        # Placeholder for LinkedIn integration
        
        sample_linkedin_jobs = [
            {
                "title": "ML Engineer - Generative AI Platform",
                "company": "AI Startup XYZ",
                "description": "Build production ML systems for Gen AI. Experience with LLM, transformers, PyTorch required. Global remote.",
                "apply_url": "https://linkedin.com/jobs/view/xyz",
                "location": "Remote, Global",
                "salary_range": "$160k - $250k",
                "source": "LinkedIn",
                "posted_date": datetime.now().isoformat(),
            }
        ]
        jobs.extend(sample_linkedin_jobs)
    except Exception as e:
        log.warning(f"Error fetching from LinkedIn: {e}")
    
    return jobs


def _fetch_angellist_jobs() -> List[Dict]:
    """Fetch jobs from AngelList (startup-focused remote roles)."""
    jobs = []
    try:
        # AngelList API v2
        api_url = "https://api.angel.co/1/jobs"
        
        for role in ["Data Scientist", "ML Engineer", "AI Engineer"]:
            try:
                params = {
                    "filter_keywords": role,
                    "locations": ["Remote"],
                }
                
                # Note: AngelList API requires authentication
                # This is a placeholder implementation
                response = requests.get(api_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for job in data.get("jobs", []):
                        jobs.append({
                            "title": job.get("title", ""),
                            "company": job.get("startup", {}).get("name", ""),
                            "description": job.get("description", "")[:500],
                            "apply_url": job.get("url", ""),
                            "location": "Remote",
                            "salary_range": job.get("salary", "Negotiable"),
                            "source": "AngelList",
                            "posted_date": job.get("created_at", datetime.now().isoformat()),
                        })
            except Exception as e:
                log.warning(f"Error fetching {role} from AngelList: {e}")
                continue
    
    except Exception as e:
        log.warning(f"Error connecting to AngelList: {e}")
    
    return jobs


def _is_relevant_job(job: Dict) -> bool:
    """Check if job matches target roles and location criteria."""
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    location = job.get("location", "").lower()
    
    # Check if title/description contains target role
    has_target_role = any(role.lower() in title or role.lower() in description 
                          for role in TARGET_ROLES)
    
    # Check if location is remote
    has_remote = any(kw in location for kw in REQUIRED_KEYWORDS)
    
    # Check for exclusions
    no_exclusions = not any(ex.lower() in title for ex in EXCLUDE_KEYWORDS)
    
    return has_target_role and has_remote and no_exclusions


def fetch_jobs_for_role(role: str, source: str = None) -> List[Dict]:
    """Fetch jobs for a specific role."""
    all_jobs = fetch_jobs(source)
    filtered_jobs = []
    
    for job in all_jobs:
        if role.lower() in job.get("title", "").lower():
            filtered_jobs.append(job)
    
    return filtered_jobs


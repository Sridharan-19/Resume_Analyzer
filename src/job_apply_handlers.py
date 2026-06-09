"""
Job board-specific application handlers.
Implements automated apply logic for different job portals.
"""

import logging
import time
import os
from typing import Dict, Optional
from src.browser_automation import BrowserAutomation
from src.credentials import CredentialManager
from selenium.webdriver.common.by import By

log = logging.getLogger(__name__)


class JobApplyHandler:
    """Base class for job application handlers."""
    
    def __init__(self, headless=True):
        self.browser = BrowserAutomation(headless=headless)
        self.headless = headless
    
    def apply(self, job: Dict, resume_path: str) -> bool:
        """
        Apply to a job. Implemented by subclasses.
        
        Args:
            job: Job dictionary with title, apply_url, etc.
            resume_path: Path to tailored resume
        
        Returns:
            True if application successful
        """
        raise NotImplementedError("Subclasses must implement apply()")
    
    def close(self):
        """Close browser."""
        self.browser.close()


class LinkedInApplyHandler(JobApplyHandler):
    """Handler for LinkedIn Easy Apply applications."""
    
    def apply(self, job: Dict, resume_path: str) -> bool:
        """
        Apply to LinkedIn job posting.
        
        Args:
            job: Job dictionary
            resume_path: Path to tailored resume
        
        Returns:
            True if successful
        """
        log.info(f"LinkedIn apply handler: {job.get('title')}")
        
        # Check credentials
        if not CredentialManager.validate_linkedin_credentials():
            log.error("LinkedIn credentials not configured")
            return False
        
        email, password = CredentialManager.get_linkedin_credentials()
        
        try:
            # Initialize browser
            if not self.browser.setup_chrome_driver():
                return False
            
            # Open job posting
            apply_url = job.get('apply_url', '')
            if not apply_url:
                log.error("No apply URL provided")
                return False
            
            if not self.browser.open_page(apply_url):
                return False
            
            # Check if Easy Apply button exists
            easy_apply_selector = "button[aria-label*='Easy Apply']"
            if not self.browser.wait_for_element(easy_apply_selector):
                log.warning("Easy Apply button not found, may need manual login")
                # Could implement login logic here
                return False
            
            # Click Easy Apply
            if not self.browser.click_element(easy_apply_selector):
                return False
            
            log.info("LinkedIn application submitted successfully")
            return True
        
        except Exception as e:
            log.error(f"Error applying to LinkedIn job: {e}")
            return False
        
        finally:
            self.close()


class WellfoundApplyHandler(JobApplyHandler):
    """Handler for Wellfound (formerly AngelList) job applications."""
    
    def apply(self, job: Dict, resume_path: str) -> bool:
        """
        Apply to Wellfound job posting.
        
        Args:
            job: Job dictionary
            resume_path: Path to tailored resume
        
        Returns:
            True if successful
        """
        log.info(f"Wellfound apply handler: {job.get('title')}")
        
        # Check credentials
        if not CredentialManager.validate_wellfound_credentials():
            log.error("Wellfound credentials not configured")
            return False
        
        email, password = CredentialManager.get_wellfound_credentials()
        
        try:
            # Initialize browser
            if not self.browser.setup_chrome_driver():
                return False
            
            # Go to login page first
            login_url = "https://wellfound.com/login"
            if not self.browser.open_page(login_url):
                return False
            
            # Wait for email input and fill it
            email_selectors = ["input[name='email']", "input#user_email", "input[type='email']"]
            email_filled = False
            for selector in email_selectors:
                if self.browser.fill_input(selector, email):
                    email_filled = True
                    break
            
            if not email_filled:
                log.error("Could not find email input on Wellfound login page")
                return False
            
            # Fill password
            password_selectors = ["input[name='password']", "input#user_password", "input[type='password']"]
            password_filled = False
            for selector in password_selectors:
                if self.browser.fill_input(selector, password):
                    password_filled = True
                    break
            
            if not password_filled:
                log.error("Could not find password input on Wellfound login page")
                return False
            
            # Click login
            login_buttons = ["input[type='submit']", "button[type='submit']", "button:contains('Log in')", ".c-button"]
            logged_in = False
            for button in login_buttons:
                if self.browser.click_element(button):
                    logged_in = True
                    break
            
            if not logged_in:
                log.error("Could not click log in button")
                return False
            
            # Wait a few seconds for login redirection
            time.sleep(5)
            
            # Open job posting
            apply_url = job.get('apply_url', '')
            if not apply_url:
                log.error("No apply URL provided")
                return False
            
            if not self.browser.open_page(apply_url):
                return False
            
            # Look for Wellfound apply/interest buttons
            apply_buttons = [
                "button[data-test='apply-button']",
                "button:contains('Apply')",
                "button:contains('Interested')",
                ".c-apply-button",
                "button:contains('Apply now')"
            ]
            
            applied = False
            for selector in apply_buttons:
                if self.browser.click_element(selector):
                    applied = True
                    break
            
            if not applied:
                log.warning("Wellfound Apply button not found")
                return False
            
            log.info("Wellfound application submitted successfully")
            return True
        
        except Exception as e:
            log.error(f"Error applying to Wellfound job: {e}")
            return False
        
        finally:
            self.close()


class GenericJobApplyHandler(JobApplyHandler):
    """Generic handler for any job board."""
    
    def apply(self, job: Dict, resume_path: str) -> bool:
        """
        Generic job application logic.
        
        Args:
            job: Job dictionary
            resume_path: Path to tailored resume
        
        Returns:
            True if successful
        """
        log.info(f"Generic apply handler: {job.get('title')}")
        
        try:
            if not self.browser.setup_chrome_driver():
                return False
            
            apply_url = job.get('apply_url', '')
            if not apply_url:
                log.error("No apply URL provided")
                return False
            
            if not self.browser.open_page(apply_url):
                return False
            
            log.info("Page opened, looking for application form...")
            
            # Take screenshot for debugging
            screenshot_path = f"logs/apply_attempt_{int(time.time())}.png"
            self.browser.take_screenshot(screenshot_path)
            log.info(f"Screenshot saved: {screenshot_path}")
            
            # Try common apply button selectors
            apply_buttons = [
                "button[type='submit']",
                "button:contains('Apply')",
                "button:contains('Submit')",
                "[class*='apply']",
                "[class*='submit']"
            ]
            
            for button in apply_buttons:
                if self.browser.click_element(button):
                    log.info(f"Clicked button: {button}")
                    return True
            
            log.warning("Could not find apply button")
            return False
        
        except Exception as e:
            log.error(f"Error in generic apply: {e}")
            return False
        
        finally:
            self.close()


def get_apply_handler(job_source: str, headless=True) -> JobApplyHandler:
    """
    Get appropriate apply handler for job source.
    
    Args:
        job_source: Job board source name
        headless: Run browser in headless mode
    
    Returns:
        JobApplyHandler instance
    """
    source_lower = job_source.lower() if job_source else ""
    
    if "linkedin" in source_lower:
        return LinkedInApplyHandler(headless=headless)
    elif "wellfound" in source_lower or "angellist" in source_lower:
        return WellfoundApplyHandler(headless=headless)
    else:
        return GenericJobApplyHandler(headless=headless)

"""
Browser automation wrapper for job applications.
Supports Selenium and Playwright for cross-platform compatibility.
"""

import logging
import time
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

log = logging.getLogger(__name__)


class BrowserAutomation:
    """Handles browser automation for job applications."""
    
    def __init__(self, headless=True, timeout=15):
        """
        Initialize browser automation.
        
        Args:
            headless: Run browser in headless mode (no GUI)
            timeout: Default wait timeout in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
    
    def setup_chrome_driver(self):
        """Initialize Chrome WebDriver."""
        try:
            options = ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(self.timeout)
            log.info("Chrome WebDriver initialized")
            return True
        
        except Exception as e:
            log.error(f"Failed to initialize Chrome WebDriver: {e}")
            return False
    
    def open_page(self, url: str) -> bool:
        """
        Open a URL in the browser.
        
        Args:
            url: URL to open
        
        Returns:
            True if successful
        """
        try:
            log.info(f"Opening URL: {url}")
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            return True
        except Exception as e:
            log.error(f"Failed to open URL: {e}")
            return False
    
    def click_element(self, selector: str, by=By.CSS_SELECTOR, wait=True) -> bool:
        """
        Click an element on the page.
        
        Args:
            selector: Element selector
            by: Selector type (CSS_SELECTOR, XPATH, ID, etc.)
            wait: Wait for element to be clickable
        
        Returns:
            True if successful
        """
        try:
            if wait:
                element = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((by, selector))
                )
            else:
                element = self.driver.find_element(by, selector)
            
            element.click()
            log.info(f"Clicked element: {selector}")
            time.sleep(1)
            return True
        
        except TimeoutException:
            log.error(f"Element not found or not clickable: {selector}")
            return False
        except Exception as e:
            log.error(f"Failed to click element: {e}")
            return False
    
    def fill_input(self, selector: str, text: str, by=By.CSS_SELECTOR) -> bool:
        """
        Fill an input field.
        
        Args:
            selector: Input element selector
            text: Text to enter
            by: Selector type
        
        Returns:
            True if successful
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            element.clear()
            element.send_keys(text)
            log.info(f"Filled input field: {selector}")
            return True
        
        except Exception as e:
            log.error(f"Failed to fill input: {e}")
            return False
    
    def upload_file(self, file_input_selector: str, file_path: str, by=By.CSS_SELECTOR) -> bool:
        """
        Upload a file to a file input.
        
        Args:
            file_input_selector: File input element selector
            file_path: Path to file to upload
            by: Selector type
        
        Returns:
            True if successful
        """
        try:
            file_input = self.driver.find_element(by, file_input_selector)
            file_input.send_keys(file_path)
            log.info(f"Uploaded file: {file_path}")
            time.sleep(1)
            return True
        
        except Exception as e:
            log.error(f"Failed to upload file: {e}")
            return False
    
    def get_text(self, selector: str, by=By.CSS_SELECTOR) -> Optional[str]:
        """
        Get text content of an element.
        
        Args:
            selector: Element selector
            by: Selector type
        
        Returns:
            Text content or None
        """
        try:
            element = self.driver.find_element(by, selector)
            return element.text
        except Exception as e:
            log.error(f"Failed to get text: {e}")
            return None
    
    def wait_for_element(self, selector: str, by=By.CSS_SELECTOR, timeout=None) -> bool:
        """
        Wait for an element to appear.
        
        Args:
            selector: Element selector
            by: Selector type
            timeout: Wait timeout in seconds
        
        Returns:
            True if element found
        """
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, selector))
            )
            return True
        except TimeoutException:
            log.warning(f"Timeout waiting for element: {selector}")
            return False
    
    def execute_script(self, script: str, *args):
        """
        Execute JavaScript in the page.
        
        Args:
            script: JavaScript code
            args: Arguments to pass to script
        
        Returns:
            Result of script execution
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            log.error(f"Failed to execute script: {e}")
            return None
    
    def get_page_source(self) -> str:
        """Get current page HTML source."""
        return self.driver.page_source
    
    def take_screenshot(self, filepath: str):
        """
        Take a screenshot of current page.
        
        Args:
            filepath: Path to save screenshot
        """
        try:
            self.driver.save_screenshot(filepath)
            log.info(f"Screenshot saved: {filepath}")
        except Exception as e:
            log.error(f"Failed to take screenshot: {e}")
    
    def close(self):
        """Close the browser."""
        try:
            if self.driver:
                self.driver.quit()
                log.info("Browser closed")
        except Exception as e:
            log.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.setup_chrome_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

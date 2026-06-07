"""
Secure credential management for automated job applications.
Stores and retrieves credentials from .env file (never in code).
"""

import os
import logging
from dotenv import load_dotenv

log = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class CredentialManager:
    """Manages secure credential storage and retrieval."""
    
    # Credential keys
    LINKEDIN_EMAIL = "LINKEDIN_EMAIL"
    LINKEDIN_PASSWORD = "LINKEDIN_PASSWORD"
    INDEED_EMAIL = "INDEED_EMAIL"
    INDEED_PASSWORD = "INDEED_PASSWORD"
    GMAIL_EMAIL = "GMAIL_EMAIL"
    GMAIL_APP_PASSWORD = "GMAIL_APP_PASSWORD"
    NOTIFICATION_EMAIL = "NOTIFICATION_EMAIL"
    
    @staticmethod
    def get_credential(key: str, default=None) -> str:
        """
        Retrieve a credential from environment variables.
        
        Args:
            key: Credential key (e.g., LINKEDIN_EMAIL)
            default: Default value if not found
        
        Returns:
            Credential value or default
        """
        value = os.getenv(key, default)
        if value is None:
            log.warning(f"Credential not found: {key}")
        return value
    
    @staticmethod
    def set_credential(key: str, value: str):
        """
        Set a credential in environment.
        
        Args:
            key: Credential key
            value: Credential value
        """
        os.environ[key] = value
        log.info(f"Credential set: {key}")
    
    @staticmethod
    def validate_linkedin_credentials() -> bool:
        """Check if LinkedIn credentials are available."""
        email = CredentialManager.get_credential(CredentialManager.LINKEDIN_EMAIL)
        password = CredentialManager.get_credential(CredentialManager.LINKEDIN_PASSWORD)
        return bool(email and password)
    
    @staticmethod
    def validate_indeed_credentials() -> bool:
        """Check if Indeed credentials are available."""
        email = CredentialManager.get_credential(CredentialManager.INDEED_EMAIL)
        password = CredentialManager.get_credential(CredentialManager.INDEED_PASSWORD)
        return bool(email and password)
    
    @staticmethod
    def get_linkedin_credentials() -> tuple:
        """Get LinkedIn email and password."""
        email = CredentialManager.get_credential(CredentialManager.LINKEDIN_EMAIL)
        password = CredentialManager.get_credential(CredentialManager.LINKEDIN_PASSWORD)
        return email, password
    
    @staticmethod
    def get_indeed_credentials() -> tuple:
        """Get Indeed email and password."""
        email = CredentialManager.get_credential(CredentialManager.INDEED_EMAIL)
        password = CredentialManager.get_credential(CredentialManager.INDEED_PASSWORD)
        return email, password
    
    @staticmethod
    def get_notification_email() -> str:
        """Get notification email address."""
        return CredentialManager.get_credential(
            CredentialManager.NOTIFICATION_EMAIL,
            CredentialManager.get_credential(CredentialManager.GMAIL_EMAIL)
        )

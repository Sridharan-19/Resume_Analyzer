"""
Application tracking database.
Tracks submitted applications and prevents duplicate submissions.
"""

import sqlite3
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

log = logging.getLogger(__name__)

DB_PATH = "application_history.db"


class ApplicationTracker:
    """Tracks job applications in SQLite database."""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database and tables."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create applications table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                apply_url TEXT UNIQUE NOT NULL,
                resume_path TEXT,
                status TEXT DEFAULT 'pending',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                result TEXT,
                notes TEXT
            )
            """)
            
            # Create audit log table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                FOREIGN KEY(application_id) REFERENCES applications(id)
            )
            """)
            
            self.conn.commit()
            log.info(f"Database initialized: {self.db_path}")
        
        except Exception as e:
            log.error(f"Error initializing database: {e}")
    
    def add_application(self, job: Dict, resume_path: str, status: str = "pending") -> bool:
        """
        Add a new application record.
        
        Args:
            job: Job dictionary
            resume_path: Path to tailored resume
            status: Application status (pending, applied, failed, etc.)
        
        Returns:
            True if successful
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
            INSERT INTO applications 
            (job_title, company, apply_url, resume_path, status)
            VALUES (?, ?, ?, ?, ?)
            """, (
                job.get('title', ''),
                job.get('company', ''),
                job.get('apply_url', ''),
                resume_path,
                status
            ))
            
            self.conn.commit()
            log.info(f"Application recorded: {job.get('title')} @ {job.get('company')}")
            return True
        
        except sqlite3.IntegrityError:
            log.warning(f"Duplicate application: {job.get('apply_url')}")
            return False
        except Exception as e:
            log.error(f"Error adding application: {e}")
            return False
    
    def update_application_status(self, apply_url: str, status: str, result: str = None) -> bool:
        """
        Update application status.
        
        Args:
            apply_url: Job apply URL
            status: New status (applied, failed, rejected, etc.)
            result: Additional result details
        
        Returns:
            True if successful
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
            UPDATE applications 
            SET status = ?, result = ?
            WHERE apply_url = ?
            """, (status, result, apply_url))
            
            self.conn.commit()
            log.info(f"Application status updated: {apply_url} -> {status}")
            return True
        
        except Exception as e:
            log.error(f"Error updating application: {e}")
            return False
    
    def is_already_applied(self, apply_url: str) -> bool:
        """
        Check if already applied to this URL.
        
        Args:
            apply_url: Job apply URL
        
        Returns:
            True if already applied
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM applications WHERE apply_url = ?", (apply_url,))
            return cursor.fetchone() is not None
        except Exception as e:
            log.error(f"Error checking application: {e}")
            return False
    
    def get_applications(self, status: str = None) -> List[Dict]:
        """
        Get applications from database.
        
        Args:
            status: Filter by status (optional)
        
        Returns:
            List of application dictionaries
        """
        try:
            cursor = self.conn.cursor()
            
            if status:
                cursor.execute("SELECT * FROM applications WHERE status = ?", (status,))
            else:
                cursor.execute("SELECT * FROM applications")
            
            columns = [description[0] for description in cursor.description]
            applications = []
            
            for row in cursor.fetchall():
                applications.append(dict(zip(columns, row)))
            
            return applications
        
        except Exception as e:
            log.error(f"Error retrieving applications: {e}")
            return []
    
    def get_application_stats(self) -> Dict:
        """
        Get application statistics.
        
        Returns:
            Dictionary with stats
        """
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total applications
            cursor.execute("SELECT COUNT(*) FROM applications")
            stats['total'] = cursor.fetchone()[0]
            
            # By status
            cursor.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
            stats['by_status'] = dict(cursor.fetchall())
            
            # Today's applications
            cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE DATE(applied_at) = DATE('now')
            """)
            stats['today'] = cursor.fetchone()[0]
            
            return stats
        
        except Exception as e:
            log.error(f"Error getting stats: {e}")
            return {}
    
    def log_audit(self, apply_url: str, action: str, details: str = None) -> bool:
        """
        Log an audit entry.
        
        Args:
            apply_url: Job apply URL
            action: Action performed
            details: Additional details
        
        Returns:
            True if successful
        """
        try:
            cursor = self.conn.cursor()
            
            # Get application ID
            cursor.execute("SELECT id FROM applications WHERE apply_url = ?", (apply_url,))
            result = cursor.fetchone()
            
            if not result:
                return False
            
            app_id = result[0]
            
            cursor.execute("""
            INSERT INTO audit_log (application_id, action, details)
            VALUES (?, ?, ?)
            """, (app_id, action, details))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            log.error(f"Error logging audit: {e}")
            return False
    
    def export_report(self, filepath: str = "application_report.csv") -> bool:
        """
        Export applications to CSV report.
        
        Args:
            filepath: Path to save report
        
        Returns:
            True if successful
        """
        try:
            import csv
            
            applications = self.get_applications()
            
            if not applications:
                log.warning("No applications to export")
                return False
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=applications[0].keys())
                writer.writeheader()
                writer.writerows(applications)
            
            log.info(f"Report exported: {filepath}")
            return True
        
        except Exception as e:
            log.error(f"Error exporting report: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        try:
            if self.conn:
                self.conn.close()
                log.info("Database connection closed")
        except Exception as e:
            log.error(f"Error closing database: {e}")

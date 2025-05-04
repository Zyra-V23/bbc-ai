"""
Database handler for the Smart Contract Audit Companion
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .config import config

class Database:
    """SQLite database handler for the application"""
    
    def __init__(self, db_path: Path = config.DB_PATH):
        """Initialize the database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Ensure the directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Connect to the database
        self.initialize()
    
    def initialize(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            self._create_tables()
            
            # Commit changes
            self.conn.commit()
            
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        # Programs table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            contract_address TEXT,
            blockchain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tasks table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            dependency_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id)
        )
        ''')
        
        # Findings table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER NOT NULL,
            task_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT DEFAULT 'medium',
            cvss_score REAL DEFAULT 0.0,
            cvss_vector TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id),
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
        ''')
        
        # Whitelist table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            organization TEXT,
            signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # AI Analysis table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER NOT NULL,
            contract_code TEXT NOT NULL,
            analysis_result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id)
        )
        ''')
    
    def add_program(self, name: str, description: str = "", 
                   contract_address: str = "", blockchain: str = "") -> int:
        """Add a new audit program to the database"""
        try:
            self.cursor.execute('''
            INSERT INTO programs (name, description, contract_address, blockchain)
            VALUES (?, ?, ?, ?)
            ''', (name, description, contract_address, blockchain))
            
            self.conn.commit()
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding program: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_programs(self) -> List[Dict[str, Any]]:
        """Get all audit programs"""
        try:
            self.cursor.execute('''
            SELECT * FROM programs ORDER BY id DESC
            ''')
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Error getting programs: {str(e)}")
            raise
    
    def get_program(self, program_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific audit program by ID"""
        try:
            self.cursor.execute('''
            SELECT * FROM programs WHERE id = ?
            ''', (program_id,))
            
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logging.error(f"Error getting program {program_id}: {str(e)}")
            raise
    
    def add_task(self, program_id: int, title: str, priority: str = "medium",
                status: str = "pending", description: str = "", 
                dependency_ids: str = "") -> int:
        """Add a new task to an audit program"""
        try:
            self.cursor.execute('''
            INSERT INTO tasks (program_id, title, priority, status, description, dependency_ids)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (program_id, title, priority, status, description, dependency_ids))
            
            self.conn.commit()
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding task: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_tasks(self, program_id: int = None) -> List[Dict[str, Any]]:
        """Get all tasks, optionally filtered by program ID"""
        try:
            if program_id is not None:
                self.cursor.execute('''
                SELECT * FROM tasks WHERE program_id = ? ORDER BY id ASC
                ''', (program_id,))
            else:
                self.cursor.execute('''
                SELECT * FROM tasks ORDER BY program_id ASC, id ASC
                ''')
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Error getting tasks: {str(e)}")
            raise
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Update the status of a task"""
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.cursor.execute('''
            UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?
            ''', (status, now, task_id))
            
            self.conn.commit()
            
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error updating task status: {str(e)}")
            self.conn.rollback()
            return False
    
    def add_finding(self, program_id: int, task_id: int, title: str, 
                   severity: str, status: str = "pending", description: str = "",
                   cvss_score: float = 0.0, cvss_vector: str = "") -> int:
        """Add a new finding/vulnerability to an audit program"""
        try:
            self.cursor.execute('''
            INSERT INTO findings (program_id, task_id, title, severity, status, description, cvss_score, cvss_vector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (program_id, task_id, title, severity, status, description, cvss_score, cvss_vector))
            
            self.conn.commit()
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding finding: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_findings(self, program_id: int = None, task_id: int = None) -> List[Dict[str, Any]]:
        """Get all findings, optionally filtered by program ID or task ID"""
        try:
            if program_id is not None and task_id is not None:
                self.cursor.execute('''
                SELECT * FROM findings WHERE program_id = ? AND task_id = ? ORDER BY id ASC
                ''', (program_id, task_id))
            elif program_id is not None:
                self.cursor.execute('''
                SELECT * FROM findings WHERE program_id = ? ORDER BY id ASC
                ''', (program_id,))
            elif task_id is not None:
                self.cursor.execute('''
                SELECT * FROM findings WHERE task_id = ? ORDER BY id ASC
                ''', (task_id,))
            else:
                self.cursor.execute('''
                SELECT * FROM findings ORDER BY program_id ASC, task_id ASC, id ASC
                ''')
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Error getting findings: {str(e)}")
            raise
    
    def add_to_whitelist(self, email: str, name: str = "", organization: str = "") -> int:
        """Add a contact to the whitelist database"""
        try:
            self.cursor.execute('''
            INSERT INTO whitelist (email, name, organization)
            VALUES (?, ?, ?)
            ''', (email, name, organization))
            
            self.conn.commit()
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding to whitelist: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_whitelist(self) -> List[Dict[str, Any]]:
        """Get all whitelist contacts"""
        try:
            self.cursor.execute('''
            SELECT * FROM whitelist ORDER BY id ASC
            ''')
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Error getting whitelist: {str(e)}")
            raise
    
    def save_ai_analysis(self, program_id: int, contract_code: str, 
                        analysis_result: str) -> int:
        """Save an AI analysis result to the database"""
        try:
            self.cursor.execute('''
            INSERT INTO ai_analyses (program_id, contract_code, analysis_result)
            VALUES (?, ?, ?)
            ''', (program_id, contract_code, analysis_result))
            
            self.conn.commit()
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error saving AI analysis: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_ai_analyses(self, program_id: int) -> List[Dict[str, Any]]:
        """Get all AI analyses for a specific program"""
        try:
            self.cursor.execute('''
            SELECT * FROM ai_analyses WHERE program_id = ? ORDER BY id DESC
            ''', (program_id,))
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Error getting AI analyses: {str(e)}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
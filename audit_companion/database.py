"""
Database handler for the Smart Contract Audit Companion
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .config import config


class Database:
    """SQLite database handler for the application"""
    
    def __init__(self, db_path: Path = config.DB_PATH):
        """Initialize the database connection"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.initialize()
    
    def initialize(self):
        """Initialize the database and create tables if they don't exist"""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connect to the database
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
        # Create tables if they don't exist
        self._create_tables()
        
    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        # Program table to store overall smart contract audit programs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            contract_address TEXT,
            blockchain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tasks table to store audit tasks
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            program_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            dependency_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE
        )
        ''')
        
        # Findings table to store audit findings/vulnerabilities
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY,
            program_id INTEGER,
            task_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT NOT NULL,
            cvss_score REAL,
            cvss_vector TEXT,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
        )
        ''')
        
        # Whitelist table to store marketing contacts
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            organization TEXT,
            signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # AI Analysis table to store results from Anthropic
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY,
            program_id INTEGER,
            contract_code TEXT,
            analysis_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE
        )
        ''')
        
        self.connection.commit()
    
    def add_program(self, name: str, description: str = "", 
                   contract_address: str = "", blockchain: str = "") -> int:
        """Add a new audit program to the database"""
        self.cursor.execute('''
        INSERT INTO programs (name, description, contract_address, blockchain)
        VALUES (?, ?, ?, ?)
        ''', (name, description, contract_address, blockchain))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_programs(self) -> List[Dict[str, Any]]:
        """Get all audit programs"""
        self.cursor.execute('SELECT * FROM programs ORDER BY created_at DESC')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_program(self, program_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific audit program by ID"""
        self.cursor.execute('SELECT * FROM programs WHERE id = ?', (program_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def add_task(self, program_id: int, title: str, priority: str = "medium",
                status: str = "pending", description: str = "", 
                dependency_ids: str = "") -> int:
        """Add a new task to an audit program"""
        self.cursor.execute('''
        INSERT INTO tasks (program_id, title, priority, status, description, dependency_ids)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (program_id, title, priority, status, description, dependency_ids))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_tasks(self, program_id: int = None) -> List[Dict[str, Any]]:
        """Get all tasks, optionally filtered by program ID"""
        if program_id:
            self.cursor.execute('''
            SELECT * FROM tasks WHERE program_id = ? ORDER BY id
            ''', (program_id,))
        else:
            self.cursor.execute('SELECT * FROM tasks ORDER BY program_id, id')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Update the status of a task"""
        self.cursor.execute('''
        UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (status, task_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def add_finding(self, program_id: int, task_id: int, title: str, 
                   severity: str, status: str = "pending", description: str = "",
                   cvss_score: float = 0.0, cvss_vector: str = "") -> int:
        """Add a new finding/vulnerability to an audit program"""
        self.cursor.execute('''
        INSERT INTO findings (program_id, task_id, title, severity, status, 
                             description, cvss_score, cvss_vector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (program_id, task_id, title, severity, status, 
             description, cvss_score, cvss_vector))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_findings(self, program_id: int = None, task_id: int = None) -> List[Dict[str, Any]]:
        """Get all findings, optionally filtered by program ID or task ID"""
        if program_id and task_id:
            self.cursor.execute('''
            SELECT * FROM findings WHERE program_id = ? AND task_id = ? 
            ORDER BY cvss_score DESC
            ''', (program_id, task_id))
        elif program_id:
            self.cursor.execute('''
            SELECT * FROM findings WHERE program_id = ? ORDER BY cvss_score DESC
            ''', (program_id,))
        elif task_id:
            self.cursor.execute('''
            SELECT * FROM findings WHERE task_id = ? ORDER BY cvss_score DESC
            ''', (task_id,))
        else:
            self.cursor.execute('SELECT * FROM findings ORDER BY cvss_score DESC')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_to_whitelist(self, email: str, name: str = "", organization: str = "") -> int:
        """Add a contact to the whitelist database"""
        try:
            self.cursor.execute('''
            INSERT INTO whitelist (email, name, organization)
            VALUES (?, ?, ?)
            ''', (email, name, organization))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email already exists in whitelist
            return -1
    
    def get_whitelist(self) -> List[Dict[str, Any]]:
        """Get all whitelist contacts"""
        self.cursor.execute('SELECT * FROM whitelist ORDER BY signup_date DESC')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def save_ai_analysis(self, program_id: int, contract_code: str, 
                        analysis_result: str) -> int:
        """Save an AI analysis result to the database"""
        self.cursor.execute('''
        INSERT INTO ai_analysis (program_id, contract_code, analysis_result)
        VALUES (?, ?, ?)
        ''', (program_id, contract_code, analysis_result))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_ai_analyses(self, program_id: int) -> List[Dict[str, Any]]:
        """Get all AI analyses for a specific program"""
        self.cursor.execute('''
        SELECT * FROM ai_analysis WHERE program_id = ? ORDER BY created_at DESC
        ''', (program_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()

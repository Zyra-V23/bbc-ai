"""
Data models for the Smart Contract Audit Companion
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


@dataclass
class Program:
    """Represents a smart contract audit program"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    contract_address: str = ""
    blockchain: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        """Create a Program instance from a dictionary"""
        program = cls()
        program.id = data.get('id')
        program.name = data.get('name', '')
        program.description = data.get('description', '')
        program.contract_address = data.get('contract_address', '')
        program.blockchain = data.get('blockchain', '')
        
        # Handle datetime conversion
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                program.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                program.created_at = data['created_at']
                
        if 'updated_at' in data:
            if isinstance(data['updated_at'], str):
                program.updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            else:
                program.updated_at = data['updated_at']
        
        return program


@dataclass
class Task:
    """Represents an audit task"""
    id: Optional[int] = None
    program_id: Optional[int] = None
    title: str = ""
    description: str = ""
    priority: str = "medium"  # high, medium, low
    status: str = "pending"   # pending, in_progress, completed, blocked
    dependency_ids: str = ""  # Comma-separated list of task IDs
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def dependencies(self) -> List[int]:
        """Get task dependencies as a list of IDs"""
        if not self.dependency_ids:
            return []
        
        return [int(id.strip()) for id in self.dependency_ids.split(',') if id.strip()]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary"""
        task = cls()
        task.id = data.get('id')
        task.program_id = data.get('program_id')
        task.title = data.get('title', '')
        task.description = data.get('description', '')
        task.priority = data.get('priority', 'medium')
        task.status = data.get('status', 'pending')
        task.dependency_ids = data.get('dependency_ids', '')
        
        # Handle datetime conversion
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                task.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                task.created_at = data['created_at']
                
        if 'updated_at' in data:
            if isinstance(data['updated_at'], str):
                task.updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            else:
                task.updated_at = data['updated_at']
        
        return task


@dataclass
class Finding:
    """Represents an audit finding or vulnerability"""
    id: Optional[int] = None
    program_id: Optional[int] = None
    task_id: Optional[int] = None
    title: str = ""
    description: str = ""
    severity: str = "medium"  # critical, high, medium, low, info
    cvss_score: float = 0.0
    cvss_vector: str = ""
    status: str = "pending"   # pending, confirmed, rejected, fixed
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Finding':
        """Create a Finding instance from a dictionary"""
        finding = cls()
        finding.id = data.get('id')
        finding.program_id = data.get('program_id')
        finding.task_id = data.get('task_id')
        finding.title = data.get('title', '')
        finding.description = data.get('description', '')
        finding.severity = data.get('severity', 'medium')
        finding.cvss_score = float(data.get('cvss_score', 0.0))
        finding.cvss_vector = data.get('cvss_vector', '')
        finding.status = data.get('status', 'pending')
        
        # Handle datetime conversion
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                finding.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                finding.created_at = data['created_at']
                
        if 'updated_at' in data:
            if isinstance(data['updated_at'], str):
                finding.updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            else:
                finding.updated_at = data['updated_at']
        
        return finding


@dataclass
class WhitelistContact:
    """Represents a contact on the marketing whitelist"""
    id: Optional[int] = None
    email: str = ""
    name: str = ""
    organization: str = ""
    signup_date: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WhitelistContact':
        """Create a WhitelistContact instance from a dictionary"""
        contact = cls()
        contact.id = data.get('id')
        contact.email = data.get('email', '')
        contact.name = data.get('name', '')
        contact.organization = data.get('organization', '')
        
        # Handle datetime conversion
        if 'signup_date' in data:
            if isinstance(data['signup_date'], str):
                contact.signup_date = datetime.fromisoformat(data['signup_date'].replace('Z', '+00:00'))
            else:
                contact.signup_date = data['signup_date']
        
        return contact


@dataclass
class AIAnalysis:
    """Represents an AI-assisted analysis result"""
    id: Optional[int] = None
    program_id: Optional[int] = None
    contract_code: str = ""
    analysis_result: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIAnalysis':
        """Create an AIAnalysis instance from a dictionary"""
        analysis = cls()
        analysis.id = data.get('id')
        analysis.program_id = data.get('program_id')
        analysis.contract_code = data.get('contract_code', '')
        analysis.analysis_result = data.get('analysis_result', '')
        
        # Handle datetime conversion
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                analysis.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                analysis.created_at = data['created_at']
        
        return analysis
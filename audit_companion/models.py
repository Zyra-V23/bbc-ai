"""
Data models for the Smart Contract Audit Companion
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


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
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            contract_address=data.get('contract_address', ''),
            blockchain=data.get('blockchain', ''),
            created_at=datetime.fromisoformat(data.get('created_at')) 
                if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now()),
            updated_at=datetime.fromisoformat(data.get('updated_at'))
                if isinstance(data.get('updated_at'), str) else data.get('updated_at', datetime.now())
        )


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
    
    @property
    def dependencies(self) -> List[int]:
        """Get task dependencies as a list of IDs"""
        if not self.dependency_ids:
            return []
        return [int(id_str.strip()) for id_str in self.dependency_ids.split(',') if id_str.strip()]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary"""
        return cls(
            id=data.get('id'),
            program_id=data.get('program_id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            dependency_ids=data.get('dependency_ids', ''),
            created_at=datetime.fromisoformat(data.get('created_at')) 
                if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now()),
            updated_at=datetime.fromisoformat(data.get('updated_at'))
                if isinstance(data.get('updated_at'), str) else data.get('updated_at', datetime.now())
        )


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
        return cls(
            id=data.get('id'),
            program_id=data.get('program_id'),
            task_id=data.get('task_id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            severity=data.get('severity', 'medium'),
            cvss_score=float(data.get('cvss_score', 0.0)),
            cvss_vector=data.get('cvss_vector', ''),
            status=data.get('status', 'pending'),
            created_at=datetime.fromisoformat(data.get('created_at')) 
                if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now()),
            updated_at=datetime.fromisoformat(data.get('updated_at'))
                if isinstance(data.get('updated_at'), str) else data.get('updated_at', datetime.now())
        )


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
        return cls(
            id=data.get('id'),
            email=data.get('email', ''),
            name=data.get('name', ''),
            organization=data.get('organization', ''),
            signup_date=datetime.fromisoformat(data.get('signup_date')) 
                if isinstance(data.get('signup_date'), str) else data.get('signup_date', datetime.now())
        )


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
        return cls(
            id=data.get('id'),
            program_id=data.get('program_id'),
            contract_code=data.get('contract_code', ''),
            analysis_result=data.get('analysis_result', ''),
            created_at=datetime.fromisoformat(data.get('created_at')) 
                if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now())
        )

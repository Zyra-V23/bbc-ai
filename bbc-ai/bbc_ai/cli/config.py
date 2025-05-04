"""
Configuration settings for the Smart Contract Audit Companion
"""

import os
import sys
import pathlib
from dataclasses import dataclass, field

class Colors:
    SUCCESS = "#00FF00"  # green
    WARNING = "#FFFF00"  # yellow
    ERROR = "#FF0000"    # red
    INFO = "#00FFFF"     # cyan
    DEFAULT = "#FFFFFF"  # white

    HIGH_PRIORITY = "#FF0000"     # red
    MEDIUM_PRIORITY = "#FFFF00"   # yellow
    LOW_PRIORITY = "#00FFFF"      # cyan

    PENDING = "#FFCC00"    # orange
    IN_PROGRESS = "#00CCFF"  # light blue
    COMPLETED = "#00FF00"  # green
    BLOCKED = "#FF6666"    # light red

@dataclass
class AppConfig:
    """Application configuration"""
    APP_NAME: str = "Bug Bounty Companion"
    VERSION: str = "0.1.0"
    
    # Paths
    HOME_DIR: pathlib.Path = pathlib.Path.home()
    APP_DIR: pathlib.Path = HOME_DIR / ".audit-companion"
    DATA_DIR: pathlib.Path = APP_DIR / "data"
    
    # Database
    DB_PATH: pathlib.Path = DATA_DIR / "audit_companion.db"
    
    # Anthropic API settings
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    
    # Alpha Phase
    DEFAULT_CSV_PATH: pathlib.Path = APP_DIR / "alpha_testers.csv"
    
    # Marketing
    ALPHA_PHASE_PROMPT: str = ("Join our exclusive Alpha Phase for early access and help shape the Bug Bounty Companion! "
                              "Limited spots available for security researchers!")
    SCARCITY_MESSAGE: str = "Only 20 security researchers will get early access to test our MCP technology! Act now!"
    EARLY_ACCESS_BENEFITS: str = ("✓ Access to our MCP (Model Context Protocol) for finding bugs\n"
                                 "✓ Support for multiple smart contract languages\n"
                                 "✓ Priority AI report generation\n"
                                 "✓ Advanced CVSS calculation templates\n"
                                 "✓ Direct feedback channel to the developer")
    MVP_DESCRIPTION: str = ("Streamline your smart contract audit workflow with AI-assisted "
                           "analysis, comprehensive task tracking, and professional "
                           "vulnerability reporting. Built by security researchers for "
                           "security researchers.")
    
    def __post_init__(self):
        """Ensure required directories exist"""
        # Create directories if they don't exist
        self.APP_DIR.mkdir(exist_ok=True)
        self.DATA_DIR.mkdir(exist_ok=True)

# Create global config instance
config = AppConfig()

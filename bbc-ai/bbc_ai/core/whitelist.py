"""
Whitelist management for marketing and early access features
"""

import os
import csv
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from bbc_ai.cli.config import config


def validate_email(email: str) -> bool:
    """
    Validate an email address
    
    Args:
        email: Email address to validate
        
    Returns:
        True if the email is valid, False otherwise
    """
    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def export_whitelist_to_csv(contacts: List[Dict[str, Any]], 
                          filepath: Optional[Path] = None) -> bool:
    """
    Export whitelist contacts to a CSV file
    
    Args:
        contacts: List of whitelist contacts
        filepath: Path to save the CSV file (default: config.DEFAULT_CSV_PATH)
        
    Returns:
        True if export was successful, False otherwise
    """
    if not filepath:
        filepath = config.DEFAULT_CSV_PATH
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['id', 'email', 'name', 'organization', 'signup_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in contacts:
                # Format the signup_date if it's a datetime object
                if isinstance(contact.get('signup_date'), datetime):
                    contact['signup_date'] = contact['signup_date'].strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow(contact)
        
        return True
    except Exception as e:
        print(f"Error exporting whitelist to CSV: {str(e)}")
        return False


def import_whitelist_from_csv(filepath: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Import whitelist contacts from a CSV file
    
    Args:
        filepath: Path to the CSV file (default: config.DEFAULT_CSV_PATH)
        
    Returns:
        List of imported contacts
    """
    if not filepath:
        filepath = config.DEFAULT_CSV_PATH
    
    if not os.path.exists(filepath):
        return []
    
    try:
        contacts = []
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contacts.append(row)
        
        return contacts
    except Exception as e:
        print(f"Error importing whitelist from CSV: {str(e)}")
        return []


def display_marketing_message():
    """Display marketing message about the tool's features"""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    console.print("\n[bold green]Smart Contract Audit Companion[/]")
    console.print(Panel(
        config.MVP_DESCRIPTION,
        title="Elevate Your Smart Contract Audits",
        border_style="green"
    ))
    
    console.print("\n[bold yellow]⚡ Early Access Program ⚡[/]")
    console.print(config.SCARCITY_MESSAGE)
    console.print("\n[cyan]Benefits Include:[/]")
    console.print(config.EARLY_ACCESS_BENEFITS)

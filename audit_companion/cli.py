"""
Command-line interface for the Smart Contract Audit Companion
"""

import os
import sys
from typing import Optional, List, Dict, Any
import pathlib

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from rich.table import Table
from rich.prompt import Prompt, Confirm

from .config import config, Colors
from .ai_integration import SmartContractAnalyzer
from .contract_analyzer import SolidityParser
from .cvss import CVSSCalculator
from .vulnerability_db import VulnerabilityDatabase

# Initialize the CLI app
app = typer.Typer(add_completion=False)
console = Console()

# If this is imported by a WSGI server like gunicorn, we need to prevent execution
if 'gunicorn' in sys.modules:
    def dummy_command():
        pass
    
    app.command()(dummy_command)

else:
    # Create proper CLI app
    @app.callback()
    def main():
        """Smart Contract Audit Companion - CLI tool for security researchers"""
        console.print(Panel(
            f"[bold]{config.APP_NAME}[/bold] [dim]v{config.VERSION}[/dim]",
            subtitle="A CLI tool for security researchers",
            expand=False
        ))
    
    @app.command("help")
    def show_help():
        """Show help information"""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description")
        
        help_table.add_row("program", "Manage audit programs")
        help_table.add_row("task", "Manage audit tasks") 
        help_table.add_row("finding", "Manage audit findings")
        help_table.add_row("whitelist", "Manage marketing whitelist")
        help_table.add_row("analyze", "Analyze a smart contract using AI")
        help_table.add_row("triage", "Triage a vulnerability using AI")
        help_table.add_row("cvss", "Calculate CVSS score for a vulnerability")
        help_table.add_row("vulndb", "Access vulnerability database")
        help_table.add_row("exit/quit", "Exit the application")
        
        console.print(help_table)
    
    @app.command("program")
    def program_commands(cmd: str = typer.Argument(..., help="Command: list, add, show"),
                      id: Optional[int] = typer.Argument(None, help="Program ID")):
        """Manage audit programs"""
        if cmd == "list":
            console.print("Listing all audit programs...")
            # Placeholder for database interaction
            programs = [
                {"id": 1, "name": "Example DeFi Protocol", "description": "Audit of a yield farming protocol"},
                {"id": 2, "name": "NFT Marketplace", "description": "Security review of NFT trading platform"}
            ]
            
            if not programs:
                console.print("[yellow]No audit programs found.[/yellow]")
                return
            
            table = Table(title="Audit Programs")
            table.add_column("ID", style="dim")
            table.add_column("Name", style="cyan")
            table.add_column("Description")
            
            for program in programs:
                table.add_row(str(program["id"]), program["name"], program["description"])
            
            console.print(table)
            
        elif cmd == "add":
            console.print("Adding a new audit program...")
            name = Prompt.ask("Program name")
            description = Prompt.ask("Description", default="")
            contract_address = Prompt.ask("Contract address (optional)", default="")
            blockchain = Prompt.ask("Blockchain (optional)", default="Ethereum")
            
            # Placeholder for database insert
            program_id = 3  # This would be the new ID from DB
            
            console.print(f"[green]Program added successfully with ID: {program_id}[/green]")
            
        elif cmd == "show" and id is not None:
            console.print(f"Showing details for program #{id}...")
            # Placeholder for database query
            program = {
                "id": id,
                "name": "Example Program",
                "description": "This is an example audit program",
                "contract_address": "0x1234...",
                "blockchain": "Ethereum",
                "created_at": "2025-05-01"
            }
            
            if not program:
                console.print(f"[red]Program #{id} not found.[/red]")
                return
            
            console.print(Panel(
                f"[bold cyan]{program['name']}[/bold cyan]\n\n"
                f"[bold]Description:[/bold] {program['description']}\n"
                f"[bold]Contract:[/bold] {program['contract_address']}\n"
                f"[bold]Blockchain:[/bold] {program['blockchain']}\n"
                f"[bold]Created:[/bold] {program['created_at']}",
                title=f"Program #{id}",
                expand=False
            ))
            
        else:
            console.print("[red]Invalid command. Use: program list|add|show[/red]")
    
    @app.command("task")
    def task_commands(cmd: str = typer.Argument(..., help="Command: list, add, status"),
                   id: Optional[int] = typer.Argument(None, help="Task ID or Program ID"),
                   value: Optional[str] = typer.Argument(None, help="Status value")):
        """Manage audit tasks"""
        if cmd == "list":
            program_id = id
            console.print(f"Listing tasks for program #{program_id}..." if program_id else "Listing all tasks...")
            
            # Placeholder for database query
            tasks = [
                {"id": 1, "program_id": 1, "title": "Review token contract", "status": "completed", "priority": "high"},
                {"id": 2, "program_id": 1, "title": "Audit staking functions", "status": "in_progress", "priority": "medium"},
                {"id": 3, "program_id": 2, "title": "Check marketplace fees", "status": "pending", "priority": "low"}
            ]
            
            if program_id:
                tasks = [t for t in tasks if t["program_id"] == program_id]
            
            if not tasks:
                console.print("[yellow]No tasks found.[/yellow]")
                return
            
            table = Table(title="Audit Tasks")
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Status")
            table.add_column("Priority")
            
            for task in tasks:
                # Set color based on status
                status_color = Colors.PENDING
                if task["status"] == "completed":
                    status_color = Colors.COMPLETED
                elif task["status"] == "in_progress":
                    status_color = Colors.IN_PROGRESS
                elif task["status"] == "blocked":
                    status_color = Colors.BLOCKED
                
                # Set color based on priority
                priority_color = Colors.MEDIUM_PRIORITY
                if task["priority"] == "high":
                    priority_color = Colors.HIGH_PRIORITY
                elif task["priority"] == "low":
                    priority_color = Colors.LOW_PRIORITY
                
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    f"[{status_color}]{task['status']}[/{status_color}]",
                    f"[{priority_color}]{task['priority']}[/{priority_color}]"
                )
            
            console.print(table)
            
        elif cmd == "add" and id is not None:
            program_id = id
            console.print(f"Adding a new task to program #{program_id}...")
            
            title = Prompt.ask("Task title")
            description = Prompt.ask("Description", default="")
            priority = Prompt.ask("Priority", choices=["high", "medium", "low"], default="medium")
            
            # Placeholder for database insert
            task_id = 4  # This would be the new ID from DB
            
            console.print(f"[green]Task added successfully with ID: {task_id}[/green]")
            
        elif cmd == "status" and id is not None and value is not None:
            task_id = id
            new_status = value
            
            if new_status not in ["pending", "in_progress", "completed", "blocked"]:
                console.print("[red]Invalid status. Use: pending, in_progress, completed, or blocked[/red]")
                return
            
            console.print(f"Updating task #{task_id} status to '{new_status}'...")
            
            # Placeholder for database update
            success = True
            
            if success:
                status_color = Colors.PENDING
                if new_status == "completed":
                    status_color = Colors.COMPLETED
                elif new_status == "in_progress":
                    status_color = Colors.IN_PROGRESS
                elif new_status == "blocked":
                    status_color = Colors.BLOCKED
                
                console.print(f"[green]Task status updated to [{status_color}]{new_status}[/{status_color}][/green]")
            else:
                console.print(f"[red]Failed to update task status.[/red]")
            
        else:
            console.print("[red]Invalid command. Use: task list|add|status[/red]")
    
    @app.command("finding")
    def finding_commands(cmd: str = typer.Argument(..., help="Command: list, add, show"),
                      id: Optional[int] = typer.Argument(None, help="Finding ID or Program ID"),
                      task_id: Optional[int] = typer.Argument(None, help="Task ID")):
        """Manage audit findings"""
        if cmd == "list":
            program_id = id
            console.print(f"Listing findings for program #{program_id}..." if program_id else "Listing all findings...")
            
            # Placeholder for database query
            findings = [
                {"id": 1, "program_id": 1, "task_id": 1, "title": "Reentrancy in withdraw function", "severity": "high", "cvss_score": 8.5},
                {"id": 2, "program_id": 1, "task_id": 2, "title": "Missing zero address check", "severity": "medium", "cvss_score": 5.2},
                {"id": 3, "program_id": 2, "task_id": 3, "title": "Unchecked return value", "severity": "low", "cvss_score": 3.1}
            ]
            
            if program_id:
                findings = [f for f in findings if f["program_id"] == program_id]
            
            if not findings:
                console.print("[yellow]No findings found.[/yellow]")
                return
            
            table = Table(title="Audit Findings")
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Severity")
            table.add_column("CVSS")
            table.add_column("Task ID")
            
            for finding in findings:
                # Set color based on severity
                severity_color = Colors.MEDIUM_PRIORITY
                if finding["severity"] == "critical" or finding["severity"] == "high":
                    severity_color = Colors.HIGH_PRIORITY
                elif finding["severity"] == "low" or finding["severity"] == "info":
                    severity_color = Colors.LOW_PRIORITY
                
                table.add_row(
                    str(finding["id"]),
                    finding["title"],
                    f"[{severity_color}]{finding['severity']}[/{severity_color}]",
                    f"{finding['cvss_score']:.1f}",
                    str(finding["task_id"])
                )
            
            console.print(table)
            
        elif cmd == "add" and id is not None and task_id is not None:
            program_id = id
            console.print(f"Adding a new finding to program #{program_id}, task #{task_id}...")
            
            title = Prompt.ask("Finding title")
            severity = Prompt.ask("Severity", choices=["critical", "high", "medium", "low", "info"], default="medium")
            description = Prompt.ask("Description", default="")
            
            use_cvss = Confirm.ask("Calculate CVSS score?", default=False)
            cvss_score = 0.0
            cvss_vector = ""
            
            if use_cvss:
                console.print("Launching CVSS calculator...")
                result = CVSSCalculator.interactive_calculator()
                cvss_score = result["score"]
                cvss_vector = result["vector"]
                console.print(f"CVSS Score: [cyan]{cvss_score:.1f}[/cyan] ({result['severity']})")
            else:
                cvss_score = Prompt.ask("Enter CVSS score manually (0.0-10.0)", default="5.0")
                try:
                    cvss_score = float(cvss_score)
                except ValueError:
                    cvss_score = 5.0
            
            # Placeholder for database insert
            finding_id = 4  # This would be the new ID from DB
            
            console.print(f"[green]Finding added successfully with ID: {finding_id}[/green]")
            
        elif cmd == "show" and id is not None:
            finding_id = id
            console.print(f"Showing details for finding #{finding_id}...")
            
            # Placeholder for database query
            finding = {
                "id": finding_id,
                "program_id": 1,
                "task_id": 1,
                "title": "Reentrancy in withdraw function",
                "description": "The withdraw function is vulnerable to reentrancy attacks because it transfers ETH before updating the user's balance.",
                "severity": "high",
                "cvss_score": 8.5,
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                "status": "pending",
                "created_at": "2025-05-01"
            }
            
            if not finding:
                console.print(f"[red]Finding #{finding_id} not found.[/red]")
                return
            
            severity_color = Colors.MEDIUM_PRIORITY
            if finding["severity"] == "critical" or finding["severity"] == "high":
                severity_color = Colors.HIGH_PRIORITY
            elif finding["severity"] == "low" or finding["severity"] == "info":
                severity_color = Colors.LOW_PRIORITY
            
            console.print(Panel(
                f"[bold cyan]{finding['title']}[/bold cyan]\n\n"
                f"[bold]Description:[/bold] {finding['description']}\n\n"
                f"[bold]Severity:[/bold] [{severity_color}]{finding['severity']}[/{severity_color}]\n"
                f"[bold]CVSS Score:[/bold] {finding['cvss_score']:.1f}\n"
                f"[bold]CVSS Vector:[/bold] {finding['cvss_vector']}\n"
                f"[bold]Status:[/bold] {finding['status']}\n"
                f"[bold]Program ID:[/bold] {finding['program_id']}\n"
                f"[bold]Task ID:[/bold] {finding['task_id']}\n"
                f"[bold]Created:[/bold] {finding['created_at']}",
                title=f"Finding #{finding_id}",
                expand=False
            ))
            
        else:
            console.print("[red]Invalid command. Use: finding list|add|show[/red]")
    
    @app.command("whitelist")
    def whitelist_commands(cmd: str = typer.Argument(..., help="Command: add, list, export"),
                         filepath: Optional[str] = typer.Argument(None, help="Export filepath")):
        """Manage marketing whitelist"""
        if cmd == "add":
            console.print(Panel(
                f"[bold]{config.WHITELIST_PROMPT}[/bold]\n\n"
                f"{config.SCARCITY_MESSAGE}\n\n"
                f"{config.EARLY_ACCESS_BENEFITS}",
                title="Join the Whitelist",
                expand=False
            ))
            
            email = Prompt.ask("Your email")
            name = Prompt.ask("Your name (optional)", default="")
            organization = Prompt.ask("Your organization (optional)", default="")
            
            # Validate email format (basic check)
            if "@" not in email or "." not in email:
                console.print("[red]Invalid email format. Please try again.[/red]")
                return
            
            # Placeholder for database insert
            success = True
            
            if success:
                console.print(f"[green]Thanks! {email} has been added to our exclusive whitelist.[/green]")
                console.print("You'll be notified when premium features become available!")
            else:
                console.print(f"[red]Failed to add to whitelist. Please try again later.[/red]")
                
        elif cmd == "list":
            console.print("Listing whitelist contacts...")
            
            # Placeholder for database query
            contacts = [
                {"id": 1, "email": "john@example.com", "name": "John Doe", "organization": "Security Labs"},
                {"id": 2, "email": "alice@example.com", "name": "Alice Smith", "organization": "Smart Contract Audits"},
                {"id": 3, "email": "bob@example.com", "name": "Bob Johnson", "organization": ""}
            ]
            
            if not contacts:
                console.print("[yellow]No whitelist contacts found.[/yellow]")
                return
            
            table = Table(title="Whitelist Contacts")
            table.add_column("ID", style="dim")
            table.add_column("Email", style="cyan")
            table.add_column("Name")
            table.add_column("Organization")
            
            for contact in contacts:
                table.add_row(
                    str(contact["id"]),
                    contact["email"],
                    contact["name"] or "-",
                    contact["organization"] or "-"
                )
            
            console.print(table)
            
        elif cmd == "export" and filepath is not None:
            console.print(f"Exporting whitelist to {filepath}...")
            
            # Placeholder for database query and CSV export
            contact_count = 3
            
            try:
                # Create directory if it doesn't exist
                output_path = pathlib.Path(filepath)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # In a real implementation, we would write the CSV here
                with open(filepath, "w") as f:
                    f.write("id,email,name,organization\n")
                    f.write("1,john@example.com,John Doe,Security Labs\n")
                    f.write("2,alice@example.com,Alice Smith,Smart Contract Audits\n")
                    f.write("3,bob@example.com,Bob Johnson,\n")
                
                console.print(f"[green]Successfully exported {contact_count} contacts to {filepath}[/green]")
            except Exception as e:
                console.print(f"[red]Export failed: {str(e)}[/red]")
            
        else:
            console.print("[red]Invalid command. Use: whitelist add|list|export[/red]")
    
    @app.command("analyze")
    def analyze_contract():
        """Analyze a smart contract using AI"""
        console.print(Panel("Smart Contract Analysis Tool", 
                           subtitle="Powered by Anthropic Claude AI"))
        
        file_path = Prompt.ask("Enter the path to the Solidity file")
        
        try:
            with open(file_path, "r") as file:
                contract_code = file.read()
            
            analysis_type = Prompt.ask(
                "Choose analysis type", 
                choices=["security", "gas", "logic", "general"], 
                default="security"
            )
            
            with console.status(f"Analyzing contract ({analysis_type} focus)..."):
                analyzer = SmartContractAnalyzer()
                result = analyzer.analyze_contract(contract_code, analysis_type)
            
            if result["success"]:
                console.print(Panel(
                    result["analysis"],
                    title=f"{analysis_type.capitalize()} Analysis Results",
                    expand=True
                ))
            else:
                console.print(f"[red]Analysis failed: {result.get('error', 'Unknown error')}[/red]")
                
        except FileNotFoundError:
            console.print(f"[red]File not found: {file_path}[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
    
    @app.command("triage")
    def triage_vulnerability():
        """Triage a vulnerability using AI"""
        console.print(Panel("Vulnerability Triage Assistant", 
                           subtitle="Powered by Anthropic Claude AI"))
        
        description = Prompt.ask("Describe the vulnerability", console=console)
        
        with console.status("Analyzing vulnerability..."):
            analyzer = SmartContractAnalyzer()
            result = analyzer.triage_vulnerability(description)
        
        if result["success"]:
            console.print(Panel(
                result["triage"],
                title="Vulnerability Triage Results",
                expand=True
            ))
        else:
            console.print(f"[red]Triage failed: {result.get('error', 'Unknown error')}[/red]")
    
    @app.command("cvss")
    def calculate_cvss():
        """Calculate CVSS score for a vulnerability"""
        console.print(Panel("CVSS v3.1 Calculator", 
                           subtitle="Common Vulnerability Scoring System"))
        
        result = CVSSCalculator.interactive_calculator()
        
        severity_color = Colors.MEDIUM_PRIORITY
        if result["severity"] == "Critical" or result["severity"] == "High":
            severity_color = Colors.HIGH_PRIORITY
        elif result["severity"] == "Low":
            severity_color = Colors.LOW_PRIORITY
        
        console.print("\nResults:")
        console.print(f"CVSS Score: [bold]{result['score']:.1f}[/bold] ([{severity_color}]{result['severity']}[/{severity_color}])")
        console.print(f"CVSS Vector: [dim]{result['vector']}[/dim]")
    
    @app.command("exit")
    def exit_app():
        """Exit the application"""
        console.print("[yellow]Exiting application. Goodbye![/yellow]")
        sys.exit(0)
    
    @app.command("vulndb")
    def vulnerability_db_commands(cmd: str = typer.Argument(..., help="Command: initialize, search, list, show, check"),
                               id: Optional[int] = typer.Argument(None, help="Vulnerability ID"),
                               query: Optional[str] = typer.Argument(None, help="Search query or category")):
        """
        Access the vulnerability database
        
        Commands:
        - initialize: Create and seed the vulnerability database
        - search: Search for vulnerabilities by keyword
        - list: List vulnerabilities (all or by category/tag)
        - show: Show details of a specific vulnerability
        - check: Check a contract file for known vulnerabilities
        """
        # Initialize the vulnerability database
        try:
            db = VulnerabilityDatabase()
            
            if cmd == "initialize":
                console.print("Initializing vulnerability database...")
                
                # Seed the database with common vulnerabilities
                if db.seed_common_vulnerabilities():
                    console.print("[green]Successfully initialized and seeded vulnerability database.[/green]")
                else:
                    console.print("[red]Failed to initialize vulnerability database.[/red]")
            
            elif cmd == "search" and query is not None:
                console.print(f"Searching for vulnerabilities matching '{query}'...")
                
                results = db.search_vulnerabilities(query)
                
                if not results:
                    console.print("[yellow]No vulnerabilities found matching the search query.[/yellow]")
                    return
                
                table = Table(title=f"Search Results for '{query}'")
                table.add_column("ID", style="dim")
                table.add_column("Name")
                table.add_column("Category")
                table.add_column("Severity")
                table.add_column("CVSS")
                
                for vuln in results:
                    # Set color based on severity
                    severity_color = Colors.MEDIUM_PRIORITY
                    if vuln["severity"] == "critical" or vuln["severity"] == "high":
                        severity_color = Colors.HIGH_PRIORITY
                    elif vuln["severity"] == "low" or vuln["severity"] == "info":
                        severity_color = Colors.LOW_PRIORITY
                    
                    table.add_row(
                        str(vuln["id"]),
                        vuln["name"],
                        vuln["category_name"] or "Uncategorized",
                        f"[{severity_color}]{vuln['severity']}[/{severity_color}]",
                        f"{vuln['cvss_score']:.1f}" if vuln["cvss_score"] else "N/A"
                    )
                
                console.print(table)
            
            elif cmd == "list":
                category_name = query
                console.print("Listing all vulnerabilities..." if not category_name else
                             f"Listing vulnerabilities in category '{category_name}'...")
                
                # Get list of categories first
                categories = db.get_categories()
                category_id = None
                
                if category_name:
                    # Find category ID by name
                    for cat in categories:
                        if cat["name"].lower() == category_name.lower():
                            category_id = cat["id"]
                            break
                    
                    if category_id is None:
                        console.print(f"[red]Category '{category_name}' not found.[/red]")
                        return
                
                vulnerabilities = db.get_vulnerabilities(category_id=category_id)
                
                if not vulnerabilities:
                    console.print("[yellow]No vulnerabilities found.[/yellow]")
                    return
                
                table = Table(title="Common Smart Contract Vulnerabilities")
                table.add_column("ID", style="dim")
                table.add_column("Name")
                table.add_column("Category")
                table.add_column("Severity")
                table.add_column("CVSS")
                
                for vuln in vulnerabilities:
                    # Set color based on severity
                    severity_color = Colors.MEDIUM_PRIORITY
                    if vuln["severity"] == "critical" or vuln["severity"] == "high":
                        severity_color = Colors.HIGH_PRIORITY
                    elif vuln["severity"] == "low" or vuln["severity"] == "info":
                        severity_color = Colors.LOW_PRIORITY
                    
                    table.add_row(
                        str(vuln["id"]),
                        vuln["name"],
                        vuln["category_name"] or "Uncategorized",
                        f"[{severity_color}]{vuln['severity']}[/{severity_color}]",
                        f"{vuln['cvss_score']:.1f}" if vuln["cvss_score"] else "N/A"
                    )
                
                console.print(table)
                
                # Also display available categories
                cat_table = Table(title="Available Categories")
                cat_table.add_column("ID", style="dim")
                cat_table.add_column("Name")
                cat_table.add_column("Description")
                
                for cat in categories:
                    cat_table.add_row(
                        str(cat["id"]),
                        cat["name"],
                        cat["description"] or ""
                    )
                
                console.print(cat_table)
            
            elif cmd == "show" and id is not None:
                console.print(f"Showing details for vulnerability #{id}...")
                
                vuln = db.get_vulnerability(id)
                
                if vuln is None:
                    console.print(f"[red]Vulnerability #{id} not found.[/red]")
                    return
                
                # Set color based on severity
                severity_color = Colors.MEDIUM_PRIORITY
                if vuln["severity"] == "critical" or vuln["severity"] == "high":
                    severity_color = Colors.HIGH_PRIORITY
                elif vuln["severity"] == "low" or vuln["severity"] == "info":
                    severity_color = Colors.LOW_PRIORITY
                
                # Handle tags
                tags_str = ", ".join(vuln.get("tags", [])) if vuln.get("tags") else "None"
                
                console.print(Panel(
                    f"[bold cyan]{vuln['name']}[/bold cyan]\n\n"
                    f"[bold]Category:[/bold] {vuln['category_name'] or 'Uncategorized'}\n"
                    f"[bold]Severity:[/bold] [{severity_color}]{vuln['severity']}[/{severity_color}]\n"
                    f"[bold]CVSS Score:[/bold] {vuln['cvss_score']:.1f}\n"
                    f"[bold]CVSS Vector:[/bold] {vuln['cvss_vector'] or 'N/A'}\n\n"
                    f"[bold]Description:[/bold]\n{vuln['description']}\n\n"
                    f"[bold]Recommendation:[/bold]\n{vuln['recommendation'] or 'No recommendation provided.'}\n\n"
                    f"[bold]Tags:[/bold] {tags_str}\n",
                    title=f"Vulnerability #{id}",
                    expand=False
                ))
                
                if vuln.get("code_sample"):
                    console.print("[bold]Vulnerable Code Example:[/bold]")
                    console.print(Panel(vuln["code_sample"], title="Code Sample"))
                
                if vuln.get("reference_links"):
                    console.print("[bold]References:[/bold]")
                    for ref in vuln["reference_links"].split("\n"):
                        if ref.strip():
                            console.print(f"- {ref.strip()}")
            
            elif cmd == "check":
                file_path = query
                if not file_path:
                    file_path = Prompt.ask("Enter the path to the Solidity contract file")
                
                try:
                    with open(file_path, 'r') as f:
                        contract_code = f.read()
                    
                    console.print(f"Checking contract at '{file_path}' for known vulnerabilities...")
                    
                    # Extract basic info about the contract
                    contract_info = SolidityParser.extract_contract_info(contract_code)
                    console.print(Panel(
                        f"[bold]Contracts:[/bold] {', '.join(contract_info.get('contracts', ['Unknown']))}\n"
                        f"[bold]Imports:[/bold] {', '.join(contract_info.get('imports', ['None']))}\n"
                        f"[bold]Libraries:[/bold] {', '.join(contract_info.get('libraries', ['None']))}\n"
                        f"[bold]Inheritance:[/bold] {', '.join(contract_info.get('inheritance', ['None']))}",
                        title="Contract Information",
                        expand=False
                    ))
                    
                    # Check for vulnerabilities using the database
                    detected_vulnerabilities = db.check_code_for_vulnerabilities(contract_code)
                    
                    if not detected_vulnerabilities:
                        console.print("[green]No known vulnerabilities detected.[/green]")
                        console.print("[yellow]Note: Absence of detected vulnerabilities does not guarantee security.[/yellow]")
                        return
                    
                    console.print(f"[red]Found {len(detected_vulnerabilities)} potential vulnerabilities:[/red]")
                    
                    table = Table(title="Potential Vulnerabilities")
                    table.add_column("ID", style="dim")
                    table.add_column("Name")
                    table.add_column("Severity")
                    table.add_column("Category")
                    
                    for vuln in detected_vulnerabilities:
                        # Set color based on severity
                        severity_color = Colors.MEDIUM_PRIORITY
                        if vuln["severity"] == "critical" or vuln["severity"] == "high":
                            severity_color = Colors.HIGH_PRIORITY
                        elif vuln["severity"] == "low" or vuln["severity"] == "info":
                            severity_color = Colors.LOW_PRIORITY
                        
                        table.add_row(
                            str(vuln["id"]),
                            vuln["name"],
                            f"[{severity_color}]{vuln['severity']}[/{severity_color}]",
                            vuln["category_name"] or "Uncategorized"
                        )
                    
                    console.print(table)
                    console.print("[yellow]Note: These are pattern-based detections and may include false positives.[/yellow]")
                    console.print("[yellow]Use 'vulndb show <id>' to get more details about each vulnerability.[/yellow]")
                    
                except FileNotFoundError:
                    console.print(f"[red]File not found: {file_path}[/red]")
                except Exception as e:
                    console.print(f"[red]Error analyzing contract: {str(e)}[/red]")
            
            else:
                console.print("[red]Invalid command. Use: vulndb initialize|search|list|show|check[/red]")
            
            # Close the database connection
            db.close()
            
        except Exception as e:
            console.print(f"[red]Error accessing vulnerability database: {str(e)}[/red]")
    
    @app.command("quit")
    def quit_app():
        """Alias for exit"""
        exit_app()

# If this file is run directly, start the CLI app
if __name__ == "__main__":
    app()

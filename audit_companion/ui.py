"""
Terminal UI components for Smart Contract Audit Companion
"""

from typing import List, Dict, Any, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.style import Style
from rich import box

from .config import Colors, config
from .models import Program, Task, Finding


# Initialize Rich console
console = Console()


def print_header():
    """Print the application header"""
    console.print(f"\n[bold white]{config.APP_NAME}[/] [cyan]v{config.VERSION}[/]", justify="center")
    console.print("[dim]Smart Contract Security Research Workflow Tool[/]", justify="center")
    console.print("\n")


def print_footer():
    """Print the application footer"""
    console.print("\n[dim]Type 'help' to see available commands[/]", justify="center")


def print_error(message: str):
    """Print an error message"""
    console.print(f"[{Colors.ERROR}]ERROR: {message}[/]")


def print_success(message: str):
    """Print a success message"""
    console.print(f"[{Colors.SUCCESS}]{message}[/]")


def print_warning(message: str):
    """Print a warning message"""
    console.print(f"[{Colors.WARNING}]{message}[/]")


def print_info(message: str):
    """Print an info message"""
    console.print(f"[{Colors.INFO}]{message}[/]")


def display_programs(programs: List[Dict[str, Any]]):
    """Display a table of audit programs"""
    if not programs:
        console.print(Panel("No audit programs found. Create one with 'program add'.", 
                           title="Audit Programs", border_style="cyan"))
        return
    
    table = Table(title="Smart Contract Audit Programs", box=box.ROUNDED)
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="white bold")
    table.add_column("Contract Address", style="green")
    table.add_column("Blockchain", style="yellow")
    table.add_column("Created", style="dim")
    
    # Add rows
    for program in programs:
        table.add_row(
            str(program['id']),
            program['name'],
            program['contract_address'] or "N/A",
            program['blockchain'] or "N/A",
            program['created_at'].split('.')[0] if isinstance(program['created_at'], str) 
                else program['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        )
    
    console.print(table)


def display_program_details(program: Dict[str, Any], tasks: List[Dict[str, Any]], 
                          findings: List[Dict[str, Any]]):
    """Display detailed information about an audit program"""
    if not program:
        print_error("Program not found.")
        return
    
    # Program panel
    program_panel = Panel(
        f"[bold white]{program['name']}[/]\n\n"
        f"[cyan]Description:[/] {program['description'] or 'N/A'}\n"
        f"[cyan]Contract:[/] {program['contract_address'] or 'N/A'}\n"
        f"[cyan]Blockchain:[/] {program['blockchain'] or 'N/A'}\n"
        f"[cyan]Created:[/] {program['created_at'].split('.')[0] if isinstance(program['created_at'], str) else program['created_at'].strftime('%Y-%m-%d %H:%M:%S')}",
        title=f"Program #{program['id']}",
        border_style="cyan"
    )
    
    console.print(program_panel)
    
    # Tasks table
    if tasks:
        tasks_table = Table(title="Audit Tasks", box=box.ROUNDED)
        
        tasks_table.add_column("ID", style="cyan", no_wrap=True)
        tasks_table.add_column("Title", style="white")
        tasks_table.add_column("Priority", style="yellow")
        tasks_table.add_column("Status", style="green")
        tasks_table.add_column("Dependencies", style="dim")
        
        for task in tasks:
            # Set priority color
            priority_style = {
                "high": f"[{Colors.HIGH_PRIORITY}]high[/]",
                "medium": f"[{Colors.MEDIUM_PRIORITY}]medium[/]",
                "low": f"[{Colors.LOW_PRIORITY}]low[/]"
            }.get(task['priority'].lower(), task['priority'])
            
            # Set status color
            status_style = {
                "pending": f"[{Colors.PENDING}]pending[/]",
                "in_progress": f"[{Colors.IN_PROGRESS}]in_progress[/]",
                "completed": f"[{Colors.COMPLETED}]completed[/]",
                "blocked": f"[{Colors.BLOCKED}]blocked[/]"
            }.get(task['status'].lower(), task['status'])
            
            tasks_table.add_row(
                str(task['id']),
                task['title'],
                priority_style,
                status_style,
                task['dependency_ids'] or "None"
            )
        
        console.print(tasks_table)
    else:
        console.print(Panel("No tasks found for this program. Add a task with 'task add'.", 
                           title="Audit Tasks", border_style="yellow"))
    
    # Findings table
    if findings:
        findings_table = Table(title="Audit Findings", box=box.ROUNDED)
        
        findings_table.add_column("ID", style="cyan", no_wrap=True)
        findings_table.add_column("Title", style="white")
        findings_table.add_column("Severity", style="red")
        findings_table.add_column("CVSS", style="yellow")
        findings_table.add_column("Status", style="green")
        
        for finding in findings:
            # Set severity color
            severity_style = {
                "critical": "[bright_red]critical[/]",
                "high": f"[{Colors.HIGH_PRIORITY}]high[/]",
                "medium": f"[{Colors.MEDIUM_PRIORITY}]medium[/]",
                "low": f"[{Colors.LOW_PRIORITY}]low[/]",
                "info": "[blue]info[/]"
            }.get(finding['severity'].lower(), finding['severity'])
            
            # Set status color
            status_style = {
                "pending": f"[{Colors.PENDING}]pending[/]",
                "confirmed": f"[{Colors.COMPLETED}]confirmed[/]",
                "rejected": f"[{Colors.BLOCKED}]rejected[/]",
                "fixed": "[blue]fixed[/]"
            }.get(finding['status'].lower(), finding['status'])
            
            findings_table.add_row(
                str(finding['id']),
                finding['title'],
                severity_style,
                str(finding['cvss_score']),
                status_style
            )
        
        console.print(findings_table)
    else:
        console.print(Panel("No findings recorded for this program. Add a finding with 'finding add'.", 
                           title="Audit Findings", border_style="red"))


def display_tasks(tasks: List[Dict[str, Any]], program_id: Optional[int] = None):
    """Display a table of audit tasks"""
    if not tasks:
        title = f"Audit Tasks for Program #{program_id}" if program_id else "All Audit Tasks"
        console.print(Panel("No tasks found. Create one with 'task add'.", 
                           title=title, border_style="yellow"))
        return
    
    title = f"Audit Tasks for Program #{program_id}" if program_id else "All Audit Tasks"
    table = Table(title=title, box=box.ROUNDED)
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Program", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Dependencies", style="dim")
    
    # Add rows
    for task in tasks:
        # Set priority color
        priority_style = {
            "high": f"[{Colors.HIGH_PRIORITY}]high[/]",
            "medium": f"[{Colors.MEDIUM_PRIORITY}]medium[/]",
            "low": f"[{Colors.LOW_PRIORITY}]low[/]"
        }.get(task['priority'].lower(), task['priority'])
        
        # Set status color
        status_style = {
            "pending": f"[{Colors.PENDING}]pending[/]",
            "in_progress": f"[{Colors.IN_PROGRESS}]in_progress[/]",
            "completed": f"[{Colors.COMPLETED}]completed[/]",
            "blocked": f"[{Colors.BLOCKED}]blocked[/]"
        }.get(task['status'].lower(), task['status'])
        
        table.add_row(
            str(task['id']),
            str(task['program_id']),
            task['title'],
            priority_style,
            status_style,
            task['dependency_ids'] or "None"
        )
    
    console.print(table)


def display_findings(findings: List[Dict[str, Any]], program_id: Optional[int] = None):
    """Display a table of audit findings"""
    if not findings:
        title = f"Findings for Program #{program_id}" if program_id else "All Audit Findings"
        console.print(Panel("No findings found. Create one with 'finding add'.", 
                           title=title, border_style="red"))
        return
    
    title = f"Findings for Program #{program_id}" if program_id else "All Audit Findings"
    table = Table(title=title, box=box.ROUNDED)
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Program", style="cyan", no_wrap=True)
    table.add_column("Task", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Severity", style="red")
    table.add_column("CVSS", style="yellow")
    table.add_column("Status", style="green")
    
    # Add rows
    for finding in findings:
        # Set severity color
        severity_style = {
            "critical": "[bright_red]critical[/]",
            "high": f"[{Colors.HIGH_PRIORITY}]high[/]",
            "medium": f"[{Colors.MEDIUM_PRIORITY}]medium[/]",
            "low": f"[{Colors.LOW_PRIORITY}]low[/]",
            "info": "[blue]info[/]"
        }.get(finding['severity'].lower(), finding['severity'])
        
        # Set status color
        status_style = {
            "pending": f"[{Colors.PENDING}]pending[/]",
            "confirmed": f"[{Colors.COMPLETED}]confirmed[/]",
            "rejected": f"[{Colors.BLOCKED}]rejected[/]",
            "fixed": "[blue]fixed[/]"
        }.get(finding['status'].lower(), finding['status'])
        
        table.add_row(
            str(finding['id']),
            str(finding['program_id']),
            str(finding['task_id']),
            finding['title'],
            severity_style,
            str(finding['cvss_score']),
            status_style
        )
    
    console.print(table)


def display_finding_details(finding: Dict[str, Any]):
    """Display detailed information about a finding"""
    if not finding:
        print_error("Finding not found.")
        return
    
    # Set severity color
    severity_style = {
        "critical": "bright_red",
        "high": Colors.HIGH_PRIORITY,
        "medium": Colors.MEDIUM_PRIORITY,
        "low": Colors.LOW_PRIORITY,
        "info": "blue"
    }.get(finding['severity'].lower(), "white")
    
    # Create a panel with finding details
    finding_panel = Panel(
        f"[bold white]{finding['title']}[/]\n\n"
        f"[cyan]Description:[/]\n{finding['description'] or 'N/A'}\n\n"
        f"[cyan]Severity:[/] [{severity_style}]{finding['severity']}[/]\n"
        f"[cyan]CVSS Score:[/] {finding['cvss_score']}\n"
        f"[cyan]CVSS Vector:[/] {finding['cvss_vector'] or 'N/A'}\n"
        f"[cyan]Status:[/] {finding['status']}\n"
        f"[cyan]Program ID:[/] {finding['program_id']}\n"
        f"[cyan]Task ID:[/] {finding['task_id']}\n"
        f"[cyan]Created:[/] {finding['created_at'].split('.')[0] if isinstance(finding['created_at'], str) else finding['created_at'].strftime('%Y-%m-%d %H:%M:%S')}",
        title=f"Finding #{finding['id']}",
        border_style=severity_style
    )
    
    console.print(finding_panel)


def prompt_program_details() -> Dict[str, str]:
    """Prompt the user for details about a new audit program"""
    console.print("\n[bold]Create New Audit Program[/]")
    
    name = Prompt.ask("[cyan]Program Name[/]")
    description = Prompt.ask("[cyan]Description[/]", default="")
    contract_address = Prompt.ask("[cyan]Contract Address[/]", default="")
    blockchain = Prompt.ask("[cyan]Blockchain[/]", default="")
    
    return {
        "name": name,
        "description": description,
        "contract_address": contract_address,
        "blockchain": blockchain
    }


def prompt_task_details(program_id: int) -> Dict[str, Any]:
    """Prompt the user for details about a new audit task"""
    console.print(f"\n[bold]Create New Task for Program #{program_id}[/]")
    
    title = Prompt.ask("[cyan]Task Title[/]")
    description = Prompt.ask("[cyan]Description[/]", default="")
    
    priority_options = {
        "h": "high",
        "m": "medium",
        "l": "low"
    }
    priority_choice = Prompt.ask(
        "[cyan]Priority[/]", 
        choices=list(priority_options.keys()) + list(priority_options.values()),
        default="m"
    )
    priority = priority_options.get(priority_choice, priority_choice)
    
    dependency_ids = Prompt.ask("[cyan]Dependencies (comma-separated task IDs)[/]", default="")
    
    return {
        "program_id": program_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "dependency_ids": dependency_ids
    }


def prompt_finding_details(program_id: int, task_id: int) -> Dict[str, Any]:
    """Prompt the user for details about a new finding"""
    console.print(f"\n[bold]Create New Finding for Program #{program_id}, Task #{task_id}[/]")
    
    title = Prompt.ask("[cyan]Finding Title[/]")
    description = Prompt.ask("[cyan]Description[/]", default="")
    
    severity_options = {
        "c": "critical",
        "h": "high",
        "m": "medium",
        "l": "low",
        "i": "info"
    }
    severity_choice = Prompt.ask(
        "[cyan]Severity[/]", 
        choices=list(severity_options.keys()) + list(severity_options.values()),
        default="m"
    )
    severity = severity_options.get(severity_choice, severity_choice)
    
    cvss_score = Prompt.ask("[cyan]CVSS Score (0.0-10.0)[/]", default="0.0")
    try:
        cvss_score = float(cvss_score)
        if cvss_score < 0 or cvss_score > 10:
            print_warning("Invalid CVSS score. Using 0.0.")
            cvss_score = 0.0
    except ValueError:
        print_warning("Invalid CVSS score. Using 0.0.")
        cvss_score = 0.0
        
    cvss_vector = Prompt.ask("[cyan]CVSS Vector[/]", default="")
    
    return {
        "program_id": program_id,
        "task_id": task_id,
        "title": title,
        "description": description,
        "severity": severity,
        "cvss_score": cvss_score,
        "cvss_vector": cvss_vector,
        "status": "pending"
    }


def prompt_contract_for_analysis() -> Tuple[str, str]:
    """Prompt the user for a smart contract to analyze"""
    console.print("\n[bold]Smart Contract Analysis[/]")
    
    analysis_type_options = {
        "s": "security",
        "g": "gas",
        "l": "logic",
        "a": "all"
    }
    
    analysis_type_choice = Prompt.ask(
        "[cyan]Analysis Type (s: security, g: gas, l: logic, a: all)[/]",
        choices=list(analysis_type_options.keys()),
        default="s"
    )
    analysis_type = analysis_type_options.get(analysis_type_choice, "security")
    
    console.print("[cyan]Enter/Paste Smart Contract Code (Ctrl+D or Ctrl+Z on a new line to finish):[/]")
    contract_lines = []
    
    try:
        while True:
            line = input()
            contract_lines.append(line)
    except EOFError:
        contract_code = "\n".join(contract_lines)
    
    return contract_code, analysis_type


def prompt_vulnerability_for_triage() -> str:
    """Prompt the user for a vulnerability description to triage"""
    console.print("\n[bold]Vulnerability Triage with AI[/]")
    
    console.print("[cyan]Enter/Paste Vulnerability Description (Ctrl+D or Ctrl+Z on a new line to finish):[/]")
    description_lines = []
    
    try:
        while True:
            line = input()
            description_lines.append(line)
    except EOFError:
        description = "\n".join(description_lines)
    
    return description


def display_whitelist_signup_form() -> Dict[str, str]:
    """Display whitelist signup form and collect user information"""
    console.print(Panel(config.WHITELIST_PROMPT, title="Exclusive Access", border_style="green"))
    console.print(f"[green bold]{config.SCARCITY_MESSAGE}[/]")
    console.print(f"\n[cyan]Early Access Benefits:[/]\n{config.EARLY_ACCESS_BENEFITS}")
    
    email = Prompt.ask("[cyan]Email Address[/]")
    name = Prompt.ask("[cyan]Name[/]", default="")
    organization = Prompt.ask("[cyan]Organization[/]", default="")
    
    # Confirm signup
    if Confirm.ask("[green]Join our exclusive whitelist?[/]", default=True):
        console.print(Panel("Thank you for signing up! You're on your way to premium features.", 
                           title="Success", border_style="green"))
        return {"email": email, "name": name, "organization": organization}
    
    return {}


def display_whitelist_contacts(contacts: List[Dict[str, Any]]):
    """Display a table of whitelist contacts"""
    if not contacts:
        console.print(Panel("No contacts on the whitelist yet.", 
                           title="Whitelist Contacts", border_style="cyan"))
        return
    
    table = Table(title="Whitelist Contacts", box=box.ROUNDED)
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Email", style="white")
    table.add_column("Name", style="green")
    table.add_column("Organization", style="yellow")
    table.add_column("Signup Date", style="dim")
    
    # Add rows
    for contact in contacts:
        table.add_row(
            str(contact['id']),
            contact['email'],
            contact['name'] or "N/A",
            contact['organization'] or "N/A",
            contact['signup_date'].split('.')[0] if isinstance(contact['signup_date'], str) 
                else contact['signup_date'].strftime("%Y-%m-%d %H:%M:%S")
        )
    
    console.print(table)


def display_help():
    """Display help information with available commands"""
    console.print("\n[bold]Available Commands:[/]")
    
    help_table = Table(box=box.ROUNDED)
    help_table.add_column("Command", style="cyan")
    help_table.add_column("Description", style="white")
    help_table.add_column("Usage", style="green")
    
    # Program commands
    help_table.add_row(
        "program list", 
        "List all audit programs", 
        "program list"
    )
    help_table.add_row(
        "program add", 
        "Add a new audit program", 
        "program add"
    )
    help_table.add_row(
        "program show", 
        "Show details of a program", 
        "program show <id>"
    )
    
    # Task commands
    help_table.add_row(
        "task list", 
        "List all tasks or tasks for a program", 
        "task list [program_id]"
    )
    help_table.add_row(
        "task add", 
        "Add a new task to a program", 
        "task add <program_id>"
    )
    help_table.add_row(
        "task status", 
        "Update task status", 
        "task status <id> <status>"
    )
    
    # Finding commands
    help_table.add_row(
        "finding list", 
        "List all findings or findings for a program", 
        "finding list [program_id]"
    )
    help_table.add_row(
        "finding add", 
        "Add a new finding to a task", 
        "finding add <program_id> <task_id>"
    )
    help_table.add_row(
        "finding show", 
        "Show details of a finding", 
        "finding show <id>"
    )
    
    # AI commands
    help_table.add_row(
        "analyze", 
        "Analyze a smart contract with AI", 
        "analyze"
    )
    help_table.add_row(
        "triage", 
        "Triage a vulnerability with AI", 
        "triage"
    )
    
    # Whitelist commands
    help_table.add_row(
        "whitelist add", 
        "Add a contact to the whitelist", 
        "whitelist add"
    )
    help_table.add_row(
        "whitelist list", 
        "List all whitelist contacts", 
        "whitelist list"
    )
    
    # Other commands
    help_table.add_row(
        "exit/quit", 
        "Exit the application", 
        "exit"
    )
    help_table.add_row(
        "help", 
        "Show this help message", 
        "help"
    )
    
    console.print(help_table)


def display_ai_analysis_result(result: Dict[str, Any]):
    """Display AI analysis results for a smart contract"""
    if not result.get("success", False):
        print_error(f"Analysis failed: {result.get('error', 'Unknown error')}")
        return
    
    analysis_type = result.get("type", "security")
    title_text = f"AI Analysis: {analysis_type.capitalize()}"
    
    console.print(Panel(
        result.get("analysis", "No analysis results available."),
        title=title_text,
        border_style="cyan",
        width=100,
        expand=False
    ))


def display_ai_triage_result(result: Dict[str, Any]):
    """Display AI triage results for a vulnerability"""
    if not result.get("success", False):
        print_error(f"Triage failed: {result.get('error', 'Unknown error')}")
        return
    
    console.print(Panel(
        result.get("triage", "No triage results available."),
        title="AI Vulnerability Triage",
        border_style="cyan",
        width=100,
        expand=False
    ))

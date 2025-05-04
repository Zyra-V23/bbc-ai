# Smart Contract Audit Companion

A CLI-based tool for security researchers to manage and organize their smart contract audit workflow, with integrated AI-powered analysis.

## Features

- **AI-Powered Contract Analysis**: Analyze smart contracts for security vulnerabilities, gas optimizations, and logical issues using Anthropic's Claude AI.
- **Audit Program Management**: Create and manage multiple audit programs, each with their own tasks and findings.
- **Task Tracking**: Track the status of individual audit tasks with color-coded priorities and statuses.
- **Vulnerability Reporting**: Document and categorize findings with severity ratings and CVSS scores.
- **CVSS Calculator**: Built-in CVSS v3.1 calculator for standardized vulnerability scoring.
- **Whitelist Management**: Collect and manage email contacts for feature updates and marketing.
- **Rich Terminal UI**: Color-coded terminal interface for easy navigation and information display.
- **Solidity Parser**: Basic static analysis of Solidity contracts to identify common vulnerabilities.

## Requirements

- Python 3.8+
- Anthropic API key (for AI-assisted features)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-contract-audit-companion.git
cd smart-contract-audit-companion

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the CLI tool:

```bash
python cli_runner.py
```

### Available Commands

- `help` - Show available commands
- `program` - Manage audit programs
- `task` - Manage audit tasks
- `finding` - Manage audit findings
- `whitelist` - Manage marketing whitelist
- `analyze` - Analyze a smart contract using AI
- `triage` - Triage a vulnerability using AI
- `cvss` - Calculate CVSS score for a vulnerability
- `exit/quit` - Exit the application

### Command Examples

```bash
# List all audit programs
python cli_runner.py program list

# Show details of a specific program
python cli_runner.py program show 1

# List tasks for a specific program
python cli_runner.py task list 1

# List all findings
python cli_runner.py finding list

# Update a task status
python cli_runner.py task status 2 completed

# Calculate a CVSS score
python cli_runner.py cvss

# Analyze a smart contract
python cli_runner.py analyze
```

## AI-Powered Analysis

The tool uses Anthropic's Claude AI to analyze smart contracts. It can perform several types of analysis:

1. **Security Analysis**: Identifies potential vulnerabilities and security issues
2. **Gas Optimization**: Suggests improvements for gas efficiency
3. **Logic Review**: Reviews the business logic of the contract
4. **General Analysis**: Comprehensive review covering security, gas, logic, and best practices

## CVSS Calculator

The built-in CVSS v3.1 calculator helps standardize vulnerability severity ratings. It includes:

- Base score metrics (Attack Vector, Attack Complexity, etc.)
- Temporal score metrics (optional)
- Environmental score metrics (optional)
- Severity classification (None, Low, Medium, High, Critical)
- Vector string generation

## Static Analysis

The tool includes a basic Solidity parser that can detect common vulnerabilities through pattern matching:

- Reentrancy vulnerabilities
- Use of tx.origin for authentication
- Unchecked external calls
- Unbounded loops
- Self-destruct usage
- External calls inside loops
- Weak randomness sources
- Missing zero address validation

## License

MIT
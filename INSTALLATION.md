# Installation Guide

This document provides instructions for installing and setting up the Smart Contract Audit Companion CLI tool.

## Requirements

- Python 3.8+
- The following Python packages:
  - anthropic
  - typer
  - rich
  - email-validator
  - flask
  - flask-sqlalchemy
  - gunicorn
  - psycopg2-binary

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-contract-audit-companion.git
   cd smart-contract-audit-companion
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install anthropic typer rich email-validator flask flask-sqlalchemy gunicorn psycopg2-binary
   ```

4. **Set your Anthropic API key**
   
   You need an API key from Anthropic to use the AI-assisted features:
   
   ```bash
   # On Linux/macOS
   export ANTHROPIC_API_KEY=your_api_key_here
   
   # On Windows
   set ANTHROPIC_API_KEY=your_api_key_here
   ```

   You can obtain an API key from [Anthropic's website](https://console.anthropic.com/).

5. **Run the application**
   ```bash
   python cli_runner.py
   ```

## Troubleshooting

- **API Key Issues**: If you receive errors about the Anthropic API key, ensure it's correctly set in your environment.
- **Module Not Found Errors**: Make sure all dependencies are installed correctly.
- **Database Errors**: The application uses SQLite by default; ensure the directory is writable.

## Directory Structure

- `audit_companion/` - Main application code
- `cli_runner.py` - CLI application entry point
- `main.py` - WSGI application for web deployment
- `sample_contract.sol` - Example Solidity contract for testing

## Setup for Development

For development purposes, you may want to install additional packages:

```bash
pip install pytest black flake8
```

To run tests:

```bash
pytest
```
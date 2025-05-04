#!/usr/bin/env python3
"""
Smart Contract Audit Companion with Anthropic AI Integration
A CLI-based tool for security researchers to organize their workflow
"""

import os
import sys
import typer
from typing import Optional

# This is needed to make the package importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the CLI app
from audit_companion.cli import app

# Make this file callable as a Flask app for gunicorn
def dummy_wsgi_app(environ, start_response):
    """Dummy WSGI application for gunicorn"""
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    
    start_response(status, headers)
    return [b'Smart Contract Audit Companion CLI Tool\n\nThis is a terminal-based application.\nPlease run it from the command line with: python cli_runner.py']

# This is the Flask-like app object that gunicorn looks for
app = dummy_wsgi_app

# When run directly, start the CLI
if __name__ == "__main__":
    # Run the CLI app
    from audit_companion.cli import app as cli_app
    cli_app()

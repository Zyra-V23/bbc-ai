#!/usr/bin/env python3
"""
Smart Contract Audit Companion CLI Runner
"""

import os
import sys
import logging
from bbc_ai.cli import app
# Add dotenv support to load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If dotenv is not installed, skip (but recommend installing it)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Ensure ANTHROPIC_API_KEY is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY environment variable not set.")
        print("AI-assisted features will not be available.")
        print("Set your API key with: export ANTHROPIC_API_KEY=your_key_here")

    # If no arguments, show help
    if len(sys.argv) == 1:
        app(["--help"])
    else:
        app()

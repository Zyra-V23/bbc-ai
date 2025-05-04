#!/usr/bin/env python3
"""
Smart Contract Audit Companion CLI Runner
"""

import os
import sys
import logging
from audit_companion.cli import app

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
    
    # Run the CLI app
    app()

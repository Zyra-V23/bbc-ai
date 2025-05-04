#!/usr/bin/env python3
"""
Simple test of Anthropic API
"""
import os
import sys
import anthropic
from anthropic import Anthropic

def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    print("Testing Anthropic API connection...")
    
    try:
        # Initialize client
        client = Anthropic(api_key=api_key)
        model = "claude-3-5-sonnet-20241022"  # Latest model
        
        # Simple prompt
        prompt = "Hello Claude, can you briefly explain what a smart contract audit is?"
        
        # Call API
        response = client.messages.create(
            model=model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Display result
        print("\nAPI Response:")
        print("-" * 80)
        print(response.content[0].text)
        print("-" * 80)
        print("API test successful!")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
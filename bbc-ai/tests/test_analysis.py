#!/usr/bin/env python3
"""
Test script for automated contract analysis
"""
import os
import sys
from bbc_ai.core.ai_integration import SmartContractAnalyzer

def main():
    # Check for the Anthropic API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("Please set your Anthropic API key with:")
        print("export ANTHROPIC_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Read the sample contract
    with open("sample_contract.sol", "r") as file:
        contract_code = file.read()
    
    # Initialize the AI analyzer
    analyzer = SmartContractAnalyzer()
    
    # Print header
    print("\n" + "="*80)
    print("SMART CONTRACT SECURITY ANALYSIS".center(80))
    print("="*80 + "\n")
    
    # Perform analysis
    print("Analyzing contract for security vulnerabilities...\n")
    result = analyzer.analyze_contract(contract_code, "security")
    
    if result["success"]:
        print(result["analysis"])
    else:
        print(f"Analysis failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE".center(80))
    print("="*80)

if __name__ == "__main__":
    main()
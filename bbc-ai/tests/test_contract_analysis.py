#!/usr/bin/env python3
"""
Comprehensive test of contract analysis
"""
import os
import sys
from bbc_ai.core.ai_integration import SmartContractAnalyzer
from bbc_ai.core.contract_analyzer import SolidityParser

def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    # Read sample contract
    try:
        with open("sample_contract.sol", "r") as file:
            contract_code = file.read()
    except Exception as e:
        print(f"ERROR: Failed to read sample contract file: {str(e)}")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("SMART CONTRACT ANALYSIS TOOL".center(80))
    print("="*80 + "\n")
    
    # First perform automated static analysis
    print("PHASE 1: STATIC ANALYSIS".center(80))
    print("-"*80)
    
    # Parse the contract for basic information
    contract_info = SolidityParser.extract_contract_info(contract_code)
    
    # Display contract stats
    print("Contract Information:")
    print(f"  - Solidity Version: {contract_info.get('solidity_version', 'Unknown')}")
    print(f"  - License: {contract_info.get('license', 'Unknown')}")
    print(f"  - Contracts Found: {len(contract_info.get('contracts', []))}")
    
    for i, contract in enumerate(contract_info.get('contracts', []), 1):
        print(f"\nContract #{i}: {contract.get('name', 'Unnamed')}")
        print(f"  - Functions: {len(contract.get('functions', []))}")
        print(f"  - State Variables: {len(contract.get('state_variables', []))}")
        
        print("\n  Functions:")
        for func in contract.get('functions', []):
            visibility = func.get('visibility', 'unknown')
            mutability = func.get('mutability', '')
            print(f"    - {func.get('name', 'unnamed')} ({visibility}{' ' + mutability if mutability else ''})")
    
    # Quick vulnerability scan
    print("\nQuick Vulnerability Scan:")
    findings = SolidityParser.check_common_vulnerabilities(contract_code)
    
    if findings:
        print(f"Found {len(findings)} potential issues:")
        for i, finding in enumerate(findings, 1):
            print(f"  {i}. [{finding['severity'].upper()}] {finding['title']}")
            print(f"     {finding.get('description', 'No description')}")
    else:
        print("No obvious vulnerabilities detected in static analysis.")
    
    # Now perform AI-based analysis
    print("\n\nPHASE 2: AI-ASSISTED ANALYSIS".center(80))
    print("-"*80)
    
    analyzer = SmartContractAnalyzer()
    
    # Security analysis
    print("\nPerforming security analysis...")
    security_result = analyzer.analyze_contract(contract_code, "security")
    if security_result["success"]:
        print("\nSecurity Analysis Results:")
        print(security_result["analysis"])
    else:
        print(f"Security analysis failed: {security_result.get('error', 'Unknown error')}")
    
    # Gas optimization analysis
    print("\n\nPerforming gas optimization analysis...")
    gas_result = analyzer.analyze_contract(contract_code, "gas")
    if gas_result["success"]:
        print("\nGas Optimization Results:")
        print(gas_result["analysis"])
    else:
        print(f"Gas analysis failed: {gas_result.get('error', 'Unknown error')}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE".center(80))
    print("="*80)

if __name__ == "__main__":
    main()

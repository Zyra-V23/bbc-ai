"""
Anthropic AI integration for smart contract analysis
"""

import os
import sys
import logging
import traceback
from typing import Dict, Any, Optional

import anthropic
from anthropic import Anthropic

from .config import config

class SmartContractAnalyzer:
    """Uses Anthropic's Claude to analyze smart contracts"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Anthropic client"""
        # Use provided API key or get from config/environment
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            logging.error("Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable.")
            sys.exit(1)
        
        try:
            # Initialize Anthropic client
            # The newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
            self.client = Anthropic(api_key=self.api_key)
            self.model = config.ANTHROPIC_MODEL
        except Exception as e:
            logging.error(f"Failed to initialize Anthropic client: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
    
    def analyze_contract(self, contract_code: str, analysis_type: str = "security") -> Dict[str, Any]:
        """
        Analyze a smart contract using Claude AI
        
        Args:
            contract_code: The Solidity code to analyze
            analysis_type: Type of analysis (security, gas, logic, etc.)
            
        Returns:
            Dict with analysis results
        """
        try:
            # Create prompt based on analysis type
            if analysis_type == "security":
                prompt = self._create_security_audit_prompt(contract_code)
            elif analysis_type == "gas":
                prompt = self._create_gas_optimization_prompt(contract_code)
            elif analysis_type == "logic":
                prompt = self._create_logic_review_prompt(contract_code)
            else:
                prompt = self._create_general_analysis_prompt(contract_code)
            
            # Get response from Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "success": True,
                "analysis": response.content[0].text,
                "model": self.model,
                "type": analysis_type
            }
            
        except Exception as e:
            logging.error(f"Error during contract analysis: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "analysis": "Analysis failed. Please try again later."
            }
    
    def triage_vulnerability(self, description: str) -> Dict[str, Any]:
        """
        Use Claude to triage and suggest CVSS score for a vulnerability
        
        Args:
            description: Description of the vulnerability
            
        Returns:
            Dict with triage results including suggested CVSS
        """
        try:
            prompt = self._create_triage_prompt(description)
            
            # Get response from Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "success": True,
                "triage": response.content[0].text,
                "model": self.model
            }
            
        except Exception as e:
            logging.error(f"Error during vulnerability triage: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "triage": "Triage failed. Please try again later."
            }
    
    def _create_security_audit_prompt(self, contract_code: str) -> str:
        """Create a prompt for security audit analysis"""
        return f"""You are an expert smart contract security auditor. Please analyze the following Solidity smart contract code for security vulnerabilities.

For each vulnerability found, please:
1. Describe the vulnerability
2. Rate its severity (Critical, High, Medium, Low, or Informational)
3. Explain the potential impact
4. Suggest a remediation approach with a code example

Also, provide a summary of the contract's overall security posture and identify any high-risk areas that require special attention.

Here is the smart contract code:

```solidity
{contract_code}
```
"""

    def _create_gas_optimization_prompt(self, contract_code: str) -> str:
        """Create a prompt for gas optimization analysis"""
        return f"""You are an expert smart contract gas optimization specialist. Please analyze the following Solidity smart contract code for gas inefficiencies.

For each gas inefficiency found, please:
1. Describe the inefficiency
2. Estimate the potential gas savings
3. Explain why it's inefficient
4. Suggest an optimized implementation with a code example

Also, provide a summary of the contract's overall gas efficiency and identify any particularly expensive operations that could be optimized.

Here is the smart contract code:

```solidity
{contract_code}
```
"""

    def _create_logic_review_prompt(self, contract_code: str) -> str:
        """Create a prompt for logic/business logic review"""
        return f"""You are an expert smart contract logic reviewer. Please analyze the following Solidity smart contract code for logical issues or bugs.

For each logical issue found, please:
1. Describe the issue
2. Rate its severity (Critical, High, Medium, Low, or Informational)
3. Explain the potential impact on business operations
4. Suggest a fix with a code example

Also, provide a summary of the contract's overall logical correctness and identify any areas where the implementation might not match the likely intended behavior.

Here is the smart contract code:

```solidity
{contract_code}
```
"""

    def _create_general_analysis_prompt(self, contract_code: str) -> str:
        """Create a prompt for general contract analysis"""
        return f"""You are an expert smart contract auditor. Please analyze the following Solidity smart contract code comprehensively, covering:

1. Security vulnerabilities
2. Gas optimization opportunities
3. Code quality and maintainability issues
4. Logical correctness
5. Compliance with best practices

For each issue found, please:
1. Describe the issue
2. Rate its severity or importance
3. Explain the potential impact
4. Suggest improvements with code examples where applicable

Also, provide a summary of the contract's overall quality and identify strengths and weaknesses.

Here is the smart contract code:

```solidity
{contract_code}
```
"""

    def _create_triage_prompt(self, description: str) -> str:
        """Create a prompt for vulnerability triage"""
        return f"""You are an expert smart contract security auditor. Please analyze the following vulnerability description and help triage it:

1. Summarize the vulnerability in your own words
2. Classify it according to known vulnerability types (e.g., reentrancy, integer overflow)
3. Estimate its severity (Critical, High, Medium, Low, or Informational)
4. Suggest a CVSS v3.1 vector string and score
5. Recommend next steps for verification and remediation

Here is the vulnerability description:

{description}
"""

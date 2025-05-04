"""
Smart contract analysis utilities
"""

import re
from typing import Dict, Any, List, Optional

class SolidityParser:
    """Simple parser for Solidity smart contracts"""
    
    @staticmethod
    def extract_contract_info(source_code: str) -> Dict[str, Any]:
        """
        Extract basic information from a Solidity smart contract
        
        Args:
            source_code: Solidity source code
            
        Returns:
            Dict with contract info
        """
        result = {
            "license": None,
            "solidity_version": None,
            "contracts": []
        }
        
        # Extract license
        license_match = re.search(r'\/\/\s*SPDX-License-Identifier:\s*([^\n]+)', source_code)
        if license_match:
            result["license"] = license_match.group(1).strip()
        
        # Extract Solidity version
        pragma_match = re.search(r'pragma\s+solidity\s+([^;]+);', source_code)
        if pragma_match:
            result["solidity_version"] = pragma_match.group(1).strip()
        
        # Extract contracts
        contract_matches = re.finditer(r'contract\s+(\w+)(?:\s+is\s+([^\{]+))?\s*\{([^\}]+(?:\{[^\}]*\}[^\}]*)*)\}', source_code)
        
        for contract_match in contract_matches:
            contract_name = contract_match.group(1).strip()
            inheritance = contract_match.group(2).strip() if contract_match.group(2) else ""
            contract_body = contract_match.group(3)
            
            contract_info = {
                "name": contract_name,
                "inheritance": [base.strip() for base in inheritance.split(',')] if inheritance else [],
                "functions": [],
                "state_variables": []
            }
            
            # Extract functions
            function_matches = re.finditer(r'function\s+(\w+)\s*\(([^\)]*)\)(?:\s+external|\s+public|\s+internal|\s+private)?(?:\s+view|\s+pure)?(?:\s+returns\s*\([^\)]*\))?\s*(?:\{|;)', contract_body)
            
            for function_match in function_matches:
                function_name = function_match.group(1).strip()
                function_params = function_match.group(2).strip()
                
                # Extract visibility and mutability
                visibility_match = re.search(r'(external|public|internal|private)', function_match.group(0))
                visibility = visibility_match.group(0) if visibility_match else "internal"  # Default visibility
                
                mutability_match = re.search(r'(view|pure)', function_match.group(0))
                mutability = mutability_match.group(0) if mutability_match else ""
                
                contract_info["functions"].append({
                    "name": function_name,
                    "parameters": function_params,
                    "visibility": visibility,
                    "mutability": mutability
                })
            
            # Extract state variables
            # This is a simplified approach; a complete parser would be more complex
            var_matches = re.finditer(r'(uint|int|address|bool|string|bytes\d*)\s+(?:public|private|internal)?\s+(\w+)\s*;', contract_body)
            for var_match in var_matches:
                var_type = var_match.group(1).strip()
                var_name = var_match.group(2).strip()
                
                contract_info["state_variables"].append({
                    "name": var_name,
                    "type": var_type
                })
            
            result["contracts"].append(contract_info)
        
        return result
    
    @staticmethod
    def check_common_vulnerabilities(source_code: str) -> List[Dict[str, Any]]:
        """
        Check for common Solidity vulnerabilities using pattern matching
        
        Args:
            source_code: Solidity source code
            
        Returns:
            List of potential vulnerability findings
        """
        findings = []
        
        # Check for reentrancy
        if re.search(r'\.call\{value:', source_code) and re.search(r'require\(.*balance', source_code):
            # If a contract has both .call{value:...} and checks balances, it might be vulnerable
            if not re.search(r'ReentrancyGuard', source_code) and not re.search(r'nonReentrant', source_code):
                findings.append({
                    "title": "Potential Reentrancy Vulnerability",
                    "description": "The contract uses low-level .call with value transfer but may not implement reentrancy guards.",
                    "severity": "high"
                })
        
        # Check for tx.origin authentication
        if re.search(r'tx\.origin', source_code):
            findings.append({
                "title": "Use of tx.origin for Authentication",
                "description": "Using tx.origin for authentication is vulnerable to phishing attacks. Use msg.sender instead.",
                "severity": "medium"
            })
        
        # Check for unchecked external calls
        if re.search(r'\.call\(', source_code) and not re.search(r'require\(.*\.call', source_code):
            findings.append({
                "title": "Unchecked External Call",
                "description": "External call results should be checked to handle failures properly.",
                "severity": "medium"
            })
        
        # Check for unbounded loops
        if re.search(r'for\s*\([^;]*;\s*[^;]*;\s*[^\)]*\)', source_code):
            findings.append({
                "title": "Unbounded Loop",
                "description": "Contract contains loops that may iterate over unbounded data structures, risking gas limits.",
                "severity": "low"
            })
        
        # Check for self-destruct usage
        if re.search(r'(selfdestruct|suicide)\s*\(', source_code):
            findings.append({
                "title": "Use of selfdestruct",
                "description": "Contract can be self-destructed. Ensure this function is properly protected.",
                "severity": "info"
            })
        
        # Check for calls inside loops
        if re.search(r'for\s*\([^{]*\{[^}]*\.(call|send|transfer)', source_code):
            findings.append({
                "title": "External Call Inside Loop",
                "description": "Performing external calls inside loops can lead to DoS conditions.",
                "severity": "high"
            })
            
        # Check for weak randomness
        if re.search(r'block\.(timestamp|difficulty|coinbase|number)', source_code):
            findings.append({
                "title": "Weak Randomness Source",
                "description": "Using block properties as randomness sources is predictable and can be manipulated by miners.",
                "severity": "medium"
            })
        
        # Check for missing zero address validation
        if re.search(r'address\s+.*=', source_code) and not re.search(r'require\(.*!=\s*address\(0\)', source_code):
            findings.append({
                "title": "Missing Zero Address Validation",
                "description": "Contract may not validate against zero addresses, risking fund loss or contract locking.",
                "severity": "low"
            })
            
        return findings

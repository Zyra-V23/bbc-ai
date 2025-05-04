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
        info = {
            "contracts": [],
            "imports": [],
            "libraries": [],
            "inheritance": []
        }
        
        # Find pragma statement
        pragma_match = re.search(r'pragma\s+solidity\s+([^;]+);', source_code)
        if pragma_match:
            info["pragma"] = pragma_match.group(1).strip()
        
        # Find imports
        import_matches = re.findall(r'import\s+[\'"]([^\'"]+)[\'"]', source_code)
        info["imports"] = import_matches
        
        # Find contract definitions
        contract_matches = re.findall(r'contract\s+(\w+)(?:\s+is\s+([^{]+))?', source_code)
        for match in contract_matches:
            contract_name = match[0].strip()
            info["contracts"].append(contract_name)
            
            # Check for inheritance
            if match[1]:
                inheritance = [i.strip() for i in match[1].split(',')]
                info["inheritance"].extend(inheritance)
        
        # Find library definitions
        library_matches = re.findall(r'library\s+(\w+)', source_code)
        info["libraries"] = library_matches
        
        return info
    
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
        
        # Check for reentrancy vulnerabilities (basic pattern)
        if re.search(r'\.call\{value:.*\}\([^\)]*\).*[\s\S]*-=', source_code):
            findings.append({
                "name": "Potential Reentrancy Vulnerability",
                "description": "The contract appears to perform an external call before updating state. "
                               "This pattern may lead to reentrancy attacks.",
                "severity": "high",
                "recommendation": "Follow the checks-effects-interactions pattern: first perform state "
                                 "changes, then interact with external contracts."
            })
        
        # Check for tx.origin usage
        if re.search(r'tx\.origin\s*==', source_code):
            findings.append({
                "name": "Use of tx.origin for Authorization",
                "description": "The contract uses tx.origin for authorization, which can lead to phishing attacks.",
                "severity": "high",
                "recommendation": "Use msg.sender instead of tx.origin for authorization."
            })
        
        # Check for unchecked send/transfer
        if re.search(r'\.send\([^\)]+\);(?!\s*(?:require|assert|if))', source_code):
            findings.append({
                "name": "Unchecked Send Return Value",
                "description": "The contract does not check the return value of send() function calls.",
                "severity": "medium",
                "recommendation": "Always check the return value of send() or use transfer() instead."
            })
        
        # Check for unsafe delegatecall
        if re.search(r'\.delegatecall\(', source_code):
            findings.append({
                "name": "Use of delegatecall",
                "description": "The contract uses delegatecall, which can be dangerous if not properly secured.",
                "severity": "medium",
                "recommendation": "Be careful with delegatecall. Ensure the target contract is trusted and validate all inputs."
            })
        
        # Check for version-specific issues
        pragma_match = re.search(r'pragma\s+solidity\s+([^;]+);', source_code)
        if pragma_match:
            pragma_version = pragma_match.group(1).strip()
            if pragma_version.startswith(('<', '^')) and ('0.8.0' not in pragma_version):
                # Check for pre-0.8.0 without SafeMath
                if (not re.search(r'using\s+SafeMath', source_code) and 
                    re.search(r'(?<!\+\+|--|\+=|-=|\*=|/=)(\+|-|\*|/)(?![^\n]*\bSafeMath\b)', source_code)):
                    findings.append({
                        "name": "Potential Integer Overflow/Underflow",
                        "description": f"The contract uses Solidity {pragma_version} without SafeMath library "
                                      "for arithmetic operations.",
                        "severity": "high",
                        "recommendation": "Use SafeMath library for arithmetic operations or upgrade to Solidity 0.8.0+."
                    })
        
        return findings
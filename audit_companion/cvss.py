"""
CVSS (Common Vulnerability Scoring System) calculator for the Smart Contract Audit Companion
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

@dataclass
class CVSSMetrics:
    """CVSS v3.1 Metrics"""
    # Base Score Metrics
    attack_vector: str = "N"  # N, A, L, P
    attack_complexity: str = "H"  # H, L
    privileges_required: str = "H"  # N, L, H
    user_interaction: str = "R"  # N, R
    scope: str = "U"  # U, C
    confidentiality: str = "N"  # N, L, H
    integrity: str = "N"  # N, L, H
    availability: str = "N"  # N, L, H
    
    # Temporal Score Metrics (optional)
    exploit_code_maturity: Optional[str] = None  # X, H, F, P, U
    remediation_level: Optional[str] = None  # X, U, W, T, O
    report_confidence: Optional[str] = None  # X, C, R, U
    
    # Environmental Score Metrics (optional)
    confidentiality_req: Optional[str] = None  # X, H, M, L
    integrity_req: Optional[str] = None  # X, H, M, L
    availability_req: Optional[str] = None  # X, H, M, L
    
    modified_attack_vector: Optional[str] = None  # X, N, A, L, P
    modified_attack_complexity: Optional[str] = None  # X, H, L
    modified_privileges_required: Optional[str] = None  # X, N, L, H
    modified_user_interaction: Optional[str] = None  # X, N, R
    modified_scope: Optional[str] = None  # X, U, C
    modified_confidentiality: Optional[str] = None  # X, N, L, H
    modified_integrity: Optional[str] = None  # X, N, L, H
    modified_availability: Optional[str] = None  # X, N, L, H

class CVSSCalculator:
    """
    Calculator for CVSS v3.1 scores based on metrics
    
    Based on the CVSS v3.1 specification: https://www.first.org/cvss/v3.1/specification-document
    """
    # Weight constants based on CVSS v3.1 specification
    _weights = {
        "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2},
        "AC": {"H": 0.44, "L": 0.77},
        "PR": {
            "U": {"N": 0.85, "L": 0.62, "H": 0.27},  # Unchanged scope
            "C": {"N": 0.85, "L": 0.68, "H": 0.5}    # Changed scope
        },
        "UI": {"N": 0.85, "R": 0.62},
        "S": {"U": 0, "C": 1},
        "CIA": {"N": 0, "L": 0.22, "H": 0.56}
    }
    
    _temporal_weights = {
        "E": {"X": 1, "H": 1, "F": 0.97, "P": 0.94, "U": 0.91},
        "RL": {"X": 1, "U": 1, "W": 0.97, "T": 0.96, "O": 0.95},
        "RC": {"X": 1, "C": 1, "R": 0.96, "U": 0.92}
    }
    
    _env_weights = {
        "CR-IR-AR": {"X": 1, "H": 1.5, "M": 1, "L": 0.5}
    }
    
    # Metric definitions for CLI interface
    _metric_options = {
        "AV": {
            "name": "Attack Vector",
            "options": {
                "N": "Network - Remotely exploitable",
                "A": "Adjacent - Requires local network access",
                "L": "Local - Requires local access",
                "P": "Physical - Requires physical access"
            }
        },
        "AC": {
            "name": "Attack Complexity",
            "options": {
                "L": "Low - No specialized conditions needed",
                "H": "High - Specific conditions required"
            }
        },
        "PR": {
            "name": "Privileges Required",
            "options": {
                "N": "None - No privileges required",
                "L": "Low - Basic user privileges needed",
                "H": "High - Administrative privileges needed"
            }
        },
        "UI": {
            "name": "User Interaction",
            "options": {
                "N": "None - No user interaction required",
                "R": "Required - User interaction needed"
            }
        },
        "S": {
            "name": "Scope",
            "options": {
                "U": "Unchanged - Impact only within vulnerable component",
                "C": "Changed - Impact extends beyond the vulnerable component"
            }
        },
        "C": {
            "name": "Confidentiality",
            "options": {
                "N": "None - No impact to confidentiality",
                "L": "Low - Limited information disclosure",
                "H": "High - Total information disclosure"
            }
        },
        "I": {
            "name": "Integrity",
            "options": {
                "N": "None - No integrity impact",
                "L": "Low - Limited integrity impact",
                "H": "High - Serious integrity impact"
            }
        },
        "A": {
            "name": "Availability",
            "options": {
                "N": "None - No availability impact",
                "L": "Low - Limited availability impact",
                "H": "High - Total availability loss"
            }
        }
    }
    
    @staticmethod
    def calculate_base_score(metrics: CVSSMetrics) -> float:
        """Calculate the CVSS Base Score from metrics"""
        # Calculate Impact sub-score (ISS)
        impact_sub_score = CVSSCalculator._calculate_impact_subscore(metrics)
        
        # Calculate Exploitability sub-score (ESS)
        exploitability_sub_score = CVSSCalculator._calculate_exploitability_subscore(metrics)
        
        # Calculate Base Score
        if impact_sub_score <= 0:
            return 0.0
        
        if metrics.scope == "U":  # Unchanged
            base_score = min(10, 7.52 * impact_sub_score + 0.44 * exploitability_sub_score)
        else:  # Changed
            base_score = min(10, 7.52 * (impact_sub_score + 0.18) + 0.44 * exploitability_sub_score)
        
        # Round up to 1 decimal place
        return round(base_score * 10) / 10
    
    @staticmethod
    def _calculate_impact_subscore(metrics: CVSSMetrics) -> float:
        """Calculate the Impact Sub-Score"""
        # Get impact weights for CIA
        c_weight = CVSSCalculator._weights["CIA"][metrics.confidentiality]
        i_weight = CVSSCalculator._weights["CIA"][metrics.integrity]
        a_weight = CVSSCalculator._weights["CIA"][metrics.availability]
        
        # Calculate ISS base
        iss_base = 1 - ((1 - c_weight) * (1 - i_weight) * (1 - a_weight))
        
        # Apply scope
        if metrics.scope == "U":  # Unchanged
            return 6.42 * iss_base
        else:  # Changed
            return 7.52 * (iss_base - 0.029) - 3.25 * (iss_base - 0.02) ** 15
    
    @staticmethod
    def _calculate_exploitability_subscore(metrics: CVSSMetrics) -> float:
        """Calculate the Exploitability Sub-Score"""
        # Get weights
        av_weight = CVSSCalculator._weights["AV"][metrics.attack_vector]
        ac_weight = CVSSCalculator._weights["AC"][metrics.attack_complexity]
        pr_weight = CVSSCalculator._weights["PR"][metrics.scope][metrics.privileges_required]
        ui_weight = CVSSCalculator._weights["UI"][metrics.user_interaction]
        
        # Calculate ESS
        return 8.22 * av_weight * ac_weight * pr_weight * ui_weight
    
    @staticmethod
    def calculate_temporal_score(base_score: float, metrics: CVSSMetrics) -> float:
        """Calculate the CVSS Temporal Score from the Base Score and temporal metrics"""
        # If temporal metrics aren't provided, return base score
        if (not metrics.exploit_code_maturity or
            not metrics.remediation_level or
            not metrics.report_confidence):
            return base_score
        
        # Get weights
        e_weight = CVSSCalculator._temporal_weights["E"].get(metrics.exploit_code_maturity, 1)
        rl_weight = CVSSCalculator._temporal_weights["RL"].get(metrics.remediation_level, 1)
        rc_weight = CVSSCalculator._temporal_weights["RC"].get(metrics.report_confidence, 1)
        
        # Calculate temporal score
        temporal_score = base_score * e_weight * rl_weight * rc_weight
        
        # Round to 1 decimal place
        return round(temporal_score * 10) / 10
    
    @staticmethod
    def parse_vector_string(vector_string: str) -> CVSSMetrics:
        """Parse a CVSS v3.1 vector string into a CVSSMetrics object"""
        metrics = CVSSMetrics()
        
        # Remove prefix if present
        if vector_string.startswith("CVSS:3.1/"):
            vector_string = vector_string[9:]
        
        # Split into components
        for component in vector_string.split("/"):
            if not component:
                continue
                
            parts = component.split(":")
            if len(parts) != 2:
                continue
                
            metric, value = parts
            
            # Set the appropriate metric
            if metric == "AV":
                metrics.attack_vector = value
            elif metric == "AC":
                metrics.attack_complexity = value
            elif metric == "PR":
                metrics.privileges_required = value
            elif metric == "UI":
                metrics.user_interaction = value
            elif metric == "S":
                metrics.scope = value
            elif metric == "C":
                metrics.confidentiality = value
            elif metric == "I":
                metrics.integrity = value
            elif metric == "A":
                metrics.availability = value
            elif metric == "E":
                metrics.exploit_code_maturity = value
            elif metric == "RL":
                metrics.remediation_level = value
            elif metric == "RC":
                metrics.report_confidence = value
            # Environmental metrics parsing would go here
        
        return metrics
    
    @staticmethod
    def generate_vector_string(metrics: CVSSMetrics) -> str:
        """Generate a CVSS v3.1 vector string from metrics"""
        vector_parts = [
            f"AV:{metrics.attack_vector}",
            f"AC:{metrics.attack_complexity}",
            f"PR:{metrics.privileges_required}",
            f"UI:{metrics.user_interaction}",
            f"S:{metrics.scope}",
            f"C:{metrics.confidentiality}",
            f"I:{metrics.integrity}",
            f"A:{metrics.availability}"
        ]
        
        # Add temporal metrics if present
        if metrics.exploit_code_maturity:
            vector_parts.append(f"E:{metrics.exploit_code_maturity}")
        if metrics.remediation_level:
            vector_parts.append(f"RL:{metrics.remediation_level}")
        if metrics.report_confidence:
            vector_parts.append(f"RC:{metrics.report_confidence}")
        
        # Environmental metrics would go here
        
        return "CVSS:3.1/" + "/".join(vector_parts)
    
    @staticmethod
    def score_to_severity(score: float) -> str:
        """Convert a CVSS score to a severity rating"""
        if score == 0.0:
            return "None"
        elif 0.1 <= score <= 3.9:
            return "Low"
        elif 4.0 <= score <= 6.9:
            return "Medium"
        elif 7.0 <= score <= 8.9:
            return "High"
        else:  # 9.0 - 10.0
            return "Critical"
    
    @staticmethod
    def interactive_calculator() -> Dict[str, Any]:
        """
        Interactive CVSS calculator that prompts for metrics and returns the score
        
        Returns:
            Dict with score, vector, and severity
        """
        console.print("\nCVSS v3.1 Calculator - Base Metrics\n")
        
        # Initialize metrics
        metrics = CVSSMetrics()
        
        # Display options for each metric and get user input
        table = Table(title="CVSS Base Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Options")
        
        for metric_id, metric_info in CVSSCalculator._metric_options.items():
            options_text = "\n".join([
                f"{key}: {desc}" for key, desc in metric_info["options"].items()
            ])
            table.add_row(metric_info["name"], options_text)
        
        console.print(table)
        console.print("")
        
        # Attack Vector (AV)
        metrics.attack_vector = Prompt.ask(
            "Attack Vector (AV)",
            choices=list(CVSSCalculator._metric_options["AV"]["options"].keys()),
            default="N"
        )
        
        # Attack Complexity (AC)
        metrics.attack_complexity = Prompt.ask(
            "Attack Complexity (AC)",
            choices=list(CVSSCalculator._metric_options["AC"]["options"].keys()),
            default="L"
        )
        
        # Privileges Required (PR)
        metrics.privileges_required = Prompt.ask(
            "Privileges Required (PR)",
            choices=list(CVSSCalculator._metric_options["PR"]["options"].keys()),
            default="N"
        )
        
        # User Interaction (UI)
        metrics.user_interaction = Prompt.ask(
            "User Interaction (UI)",
            choices=list(CVSSCalculator._metric_options["UI"]["options"].keys()),
            default="N"
        )
        
        # Scope (S)
        metrics.scope = Prompt.ask(
            "Scope (S)",
            choices=list(CVSSCalculator._metric_options["S"]["options"].keys()),
            default="U"
        )
        
        # Confidentiality (C)
        metrics.confidentiality = Prompt.ask(
            "Confidentiality Impact (C)",
            choices=list(CVSSCalculator._metric_options["C"]["options"].keys()),
            default="L"
        )
        
        # Integrity (I)
        metrics.integrity = Prompt.ask(
            "Integrity Impact (I)",
            choices=list(CVSSCalculator._metric_options["I"]["options"].keys()),
            default="L"
        )
        
        # Availability (A)
        metrics.availability = Prompt.ask(
            "Availability Impact (A)",
            choices=list(CVSSCalculator._metric_options["A"]["options"].keys()),
            default="L"
        )
        
        # Calculate score
        score = CVSSCalculator.calculate_base_score(metrics)
        vector = CVSSCalculator.generate_vector_string(metrics)
        severity = CVSSCalculator.score_to_severity(score)
        
        return {
            "score": score,
            "vector": vector,
            "severity": severity,
            "metrics": metrics
        }

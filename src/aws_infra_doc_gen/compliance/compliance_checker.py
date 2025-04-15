"""Compliance Checker.

This module validates AWS infrastructure against security and compliance rules.
"""

from typing import Dict, List, Any
import json
import yaml
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ComplianceChecker:
    """Checks AWS infrastructure for compliance with security rules."""
    
    def __init__(self, rules_file: str):
        """Initialize the compliance checker.
        
        Args:
            rules_file: Path to YAML file containing compliance rules
        """
        self.rules = self._load_rules(rules_file)
    
    def _load_rules(self, rules_file: str) -> Dict:
        """Load compliance rules from YAML file."""
        try:
            with open(rules_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading rules file: {e}")
            raise
    
    def check_compliance(self, resources: Dict[str, List[Dict[str, Any]]]) -> Dict:
        """Check resources against compliance rules.
        
        Args:
            resources: Dictionary of AWS resources by type
            
        Returns:
            Dictionary containing compliance results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_resources': 0,
                'compliant': 0,
                'non_compliant': 0
            },
            'violations': []
        }
        
        for resource_type, resource_list in resources.items():
            type_rules = self.rules.get(resource_type, {})
            if not type_rules:
                continue
                
            results['summary']['total_resources'] += len(resource_list)
            
            for resource in resource_list:
                violations = self._check_resource(resource, type_rules)
                
                if violations:
                    results['summary']['non_compliant'] += 1
                    results['violations'].append({
                        'resource_type': resource_type,
                        'resource_id': self._get_resource_id(resource),
                        'violations': violations
                    })
                else:
                    results['summary']['compliant'] += 1
        
        return results
    
    def _check_resource(self, resource: Dict, rules: Dict) -> List[Dict]:
        """Check a single resource against its type-specific rules."""
        violations = []
        
        for rule_name, rule_config in rules.items():
            if not self._evaluate_rule(resource, rule_config):
                violations.append({
                    'rule': rule_name,
                    'description': rule_config.get('description', ''),
                    'severity': rule_config.get('severity', 'medium')
                })
        
        return violations
    
    def _evaluate_rule(self, resource: Dict, rule: Dict) -> bool:
        """Evaluate a single rule against a resource."""
        condition = rule.get('condition', {})
        operator = condition.get('operator')
        field = condition.get('field')
        expected = condition.get('value')
        
        if not all([operator, field]):
            logger.warning(f"Invalid rule configuration: {rule}")
            return True
        
        try:
            actual = self._get_field_value(resource, field)
            
            if operator == 'equals':
                return actual == expected
            elif operator == 'not_equals':
                return actual != expected
            elif operator == 'exists':
                return actual is not None
            elif operator == 'not_exists':
                return actual is None
            elif operator == 'contains':
                return expected in actual
            elif operator == 'not_contains':
                return expected not in actual
            elif operator == 'greater_than':
                return actual > expected
            elif operator == 'less_than':
                return actual < expected
            else:
                logger.warning(f"Unsupported operator: {operator}")
                return True
                
        except Exception as e:
            logger.error(f"Error evaluating rule: {e}")
            return True
    
    def _get_field_value(self, resource: Dict, field: str) -> Any:
        """Get a field value from a resource, supporting nested fields."""
        parts = field.split('.')
        value = resource
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        
        return value
    
    def _get_resource_id(self, resource: Dict) -> str:
        """Get a unique identifier for a resource."""
        for id_field in ['id', 'name', 'identifier', 'arn']:
            if id_field in resource:
                return resource[id_field]
        return str(resource)
    
    def generate_report(self, results: Dict, format: str = 'json') -> str:
        """Generate a compliance report in the specified format.
        
        Args:
            results: Compliance check results
            format: Output format ('json' or 'html')
            
        Returns:
            Report content as string
        """
        if format == 'json':
            return json.dumps(results, indent=2)
        elif format == 'html':
            return self._generate_html_report(results)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_html_report(self, results: Dict) -> str:
        """Generate an HTML compliance report."""
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AWS Infrastructure Compliance Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .summary { margin: 20px 0; }
                .violation { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
                .high { color: red; }
                .medium { color: orange; }
                .low { color: yellow; }
            </style>
        </head>
        <body>
            <h1>AWS Infrastructure Compliance Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Generated: {timestamp}</p>
                <p>Total Resources: {total}</p>
                <p>Compliant: {compliant}</p>
                <p>Non-Compliant: {non_compliant}</p>
            </div>
            <div class="violations">
                <h2>Violations</h2>
                {violations}
            </div>
        </body>
        </html>
        """
        
        violations_html = ""
        for v in results['violations']:
            violations_html += f"""
                <div class="violation">
                    <h3>{v['resource_type']}: {v['resource_id']}</h3>
                    <ul>
                    {''.join([
                        f'<li class="{violation["severity"]}">{violation["rule"]}: {violation["description"]}</li>'
                        for violation in v['violations']
                    ])}
                    </ul>
                </div>
            """
        
        return template.format(
            timestamp=results['timestamp'],
            total=results['summary']['total_resources'],
            compliant=results['summary']['compliant'],
            non_compliant=results['summary']['non_compliant'],
            violations=violations_html
        )
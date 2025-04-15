"""Tests for compliance checker."""

import unittest
from unittest.mock import mock_open, patch
from src.aws_infra_doc_gen.compliance.compliance_checker import ComplianceChecker

class TestComplianceChecker(unittest.TestCase):
    """Test cases for ComplianceChecker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rules_yaml = """
        ec2:
          encryption_enabled:
            description: "EBS volumes must be encrypted"
            severity: high
            condition:
              field: "block_device_mappings.ebs.encrypted"
              operator: "equals"
              value: true
          
        s3:
          encryption_enabled:
            description: "S3 buckets must have encryption enabled"
            severity: high
            condition:
              field: "encryption"
              operator: "exists"
        """
        
        with patch('builtins.open', mock_open(read_data=self.rules_yaml)):
            self.checker = ComplianceChecker('dummy_path')
    
    def test_check_ec2_compliance(self):
        """Test EC2 compliance checking."""
        resources = {
            'ec2': [
                {
                    'id': 'i-1234567890',
                    'block_device_mappings': {
                        'ebs': {
                            'encrypted': False
                        }
                    }
                }
            ]
        }
        
        results = self.checker.check_compliance(resources)
        
        self.assertEqual(results['summary']['total_resources'], 1)
        self.assertEqual(results['summary']['non_compliant'], 1)
        self.assertEqual(len(results['violations']), 1)
        self.assertEqual(results['violations'][0]['resource_type'], 'ec2')
    
    def test_check_s3_compliance(self):
        """Test S3 compliance checking."""
        resources = {
            's3': [
                {
                    'name': 'test-bucket',
                    'encryption': {
                        'type': 'AES256'
                    }
                },
                {
                    'name': 'test-bucket-2',
                    'encryption': None
                }
            ]
        }
        
        results = self.checker.check_compliance(resources)
        
        self.assertEqual(results['summary']['total_resources'], 2)
        self.assertEqual(results['summary']['compliant'], 1)
        self.assertEqual(results['summary']['non_compliant'], 1)
    
    def test_evaluate_rule_equals(self):
        """Test rule evaluation with equals operator."""
        resource = {'field': 'value'}
        rule = {
            'condition': {
                'field': 'field',
                'operator': 'equals',
                'value': 'value'
            }
        }
        
        result = self.checker._evaluate_rule(resource, rule)
        self.assertTrue(result)
        
        rule['condition']['value'] = 'wrong'
        result = self.checker._evaluate_rule(resource, rule)
        self.assertFalse(result)
    
    def test_evaluate_rule_exists(self):
        """Test rule evaluation with exists operator."""
        resource = {'field': 'value'}
        rule = {
            'condition': {
                'field': 'field',
                'operator': 'exists'
            }
        }
        
        result = self.checker._evaluate_rule(resource, rule)
        self.assertTrue(result)
        
        resource = {'other_field': 'value'}
        result = self.checker._evaluate_rule(resource, rule)
        self.assertFalse(result)
    
    def test_get_field_value(self):
        """Test nested field value retrieval."""
        resource = {
            'level1': {
                'level2': {
                    'level3': 'value'
                }
            }
        }
        
        value = self.checker._get_field_value(resource, 'level1.level2.level3')
        self.assertEqual(value, 'value')
        
        value = self.checker._get_field_value(resource, 'nonexistent.field')
        self.assertIsNone(value)
    
    def test_generate_report(self):
        """Test report generation."""
        results = {
            'timestamp': '2023-01-01T00:00:00Z',
            'summary': {
                'total_resources': 2,
                'compliant': 1,
                'non_compliant': 1
            },
            'violations': [
                {
                    'resource_type': 'ec2',
                    'resource_id': 'i-1234567890',
                    'violations': [
                        {
                            'rule': 'encryption_enabled',
                            'description': 'EBS volumes must be encrypted',
                            'severity': 'high'
                        }
                    ]
                }
            ]
        }
        
        # Test JSON report
        json_report = self.checker.generate_report(results, 'json')
        self.assertIn('timestamp', json_report)
        self.assertIn('violations', json_report)
        
        # Test HTML report
        html_report = self.checker.generate_report(results, 'html')
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('AWS Infrastructure Compliance Report', html_report)
        self.assertIn('encryption_enabled', html_report)

if __name__ == '__main__':
    unittest.main()
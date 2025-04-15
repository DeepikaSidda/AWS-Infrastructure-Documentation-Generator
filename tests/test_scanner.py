"""Tests for AWS resource scanner."""

import unittest
from unittest.mock import MagicMock, patch
from src.aws_infra_doc_gen.scanner.aws_scanner import AWSResourceScanner

class TestAWSResourceScanner(unittest.TestCase):
    """Test cases for AWSResourceScanner."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scanner = AWSResourceScanner('us-east-1')
    
    @patch('boto3.Session')
    def test_scan_ec2(self, mock_session):
        """Test EC2 instance scanning."""
        # Mock EC2 client and responses
        mock_ec2 = MagicMock()
        mock_session.return_value.client.return_value = mock_ec2
        
        mock_ec2.get_paginator.return_value.paginate.return_value = [{
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-1234567890',
                    'InstanceType': 't3.micro',
                    'State': {'Name': 'running'},
                    'VpcId': 'vpc-123456',
                    'SubnetId': 'subnet-123456',
                    'Tags': [{'Key': 'Name', 'Value': 'test-instance'}],
                    'SecurityGroups': [{'GroupId': 'sg-123456', 'GroupName': 'test-sg'}],
                    'LaunchTime': '2023-01-01T00:00:00Z'
                }]
            }]
        }]
        
        # Test scanner
        resources = self.scanner.scan_resources(['ec2'])
        
        # Verify results
        self.assertIn('ec2', resources)
        self.assertEqual(len(resources['ec2']), 1)
        self.assertEqual(resources['ec2'][0]['id'], 'i-1234567890')
        self.assertEqual(resources['ec2'][0]['type'], 't3.micro')
    
    @patch('boto3.Session')
    def test_scan_s3(self, mock_session):
        """Test S3 bucket scanning."""
        # Mock S3 client and responses
        mock_s3 = MagicMock()
        mock_session.return_value.client.return_value = mock_s3
        
        mock_s3.list_buckets.return_value = {
            'Buckets': [{
                'Name': 'test-bucket',
                'CreationDate': '2023-01-01T00:00:00Z'
            }]
        }
        
        mock_s3.get_bucket_encryption.return_value = {
            'ServerSideEncryptionConfiguration': {
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        }
        
        mock_s3.get_bucket_location.return_value = {
            'LocationConstraint': 'us-east-1'
        }
        
        # Test scanner
        resources = self.scanner.scan_resources(['s3'])
        
        # Verify results
        self.assertIn('s3', resources)
        self.assertEqual(len(resources['s3']), 1)
        self.assertEqual(resources['s3'][0]['name'], 'test-bucket')
        self.assertIsNotNone(resources['s3'][0]['encryption'])
    
    @patch('boto3.Session')
    def test_scan_rds(self, mock_session):
        """Test RDS instance scanning."""
        # Mock RDS client and responses
        mock_rds = MagicMock()
        mock_session.return_value.client.return_value = mock_rds
        
        mock_rds.get_paginator.return_value.paginate.return_value = [{
            'DBInstances': [{
                'DBInstanceIdentifier': 'test-db',
                'DBInstanceClass': 'db.t3.micro',
                'Engine': 'mysql',
                'DBInstanceStatus': 'available',
                'Endpoint': {
                    'Address': 'test-db.123456.region.rds.amazonaws.com',
                    'Port': 3306
                },
                'MultiAZ': True,
                'StorageType': 'gp2',
                'AllocatedStorage': 20,
                'StorageEncrypted': True
            }]
        }]
        
        # Test scanner
        resources = self.scanner.scan_resources(['rds'])
        
        # Verify results
        self.assertIn('rds', resources)
        self.assertEqual(len(resources['rds']), 1)
        self.assertEqual(resources['rds'][0]['identifier'], 'test-db')
        self.assertTrue(resources['rds'][0]['storage']['encrypted'])
    
    @patch('boto3.Session')
    def test_scan_lambda(self, mock_session):
        """Test Lambda function scanning."""
        # Mock Lambda client and responses
        mock_lambda = MagicMock()
        mock_session.return_value.client.return_value = mock_lambda
        
        mock_lambda.get_paginator.return_value.paginate.return_value = [{
            'Functions': [{
                'FunctionName': 'test-function',
                'Runtime': 'python3.9',
                'Handler': 'index.handler',
                'Role': 'arn:aws:iam::123456789012:role/test-role',
                'MemorySize': 128,
                'Timeout': 30,
                'LastModified': '2023-01-01T00:00:00Z',
                'VpcConfig': {
                    'SubnetIds': ['subnet-123456'],
                    'SecurityGroupIds': ['sg-123456']
                }
            }]
        }]
        
        # Test scanner
        resources = self.scanner.scan_resources(['lambda'])
        
        # Verify results
        self.assertIn('lambda', resources)
        self.assertEqual(len(resources['lambda']), 1)
        self.assertEqual(resources['lambda'][0]['name'], 'test-function')
        self.assertEqual(resources['lambda'][0]['runtime'], 'python3.9')

if __name__ == '__main__':
    unittest.main()
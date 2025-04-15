"""AWS Resource Scanner.

This module handles the discovery and metadata collection of AWS resources.
"""

import boto3
from typing import Dict, List, Any
import logging
import json
from datetime import datetime




logger = logging.getLogger(__name__)

class AWSResourceScanner:
    """Scanner for discovering and collecting AWS resource information."""
    
    def __init__(self, region: str):
        """Initialize the scanner.
        
        Args:
            region: AWS region to scan
        """
        self.region = region
        self.session = boto3.Session(region_name=region)
        
    def scan_resources(self, resource_types: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Scan AWS resources of specified types.
        
        Args:
            resource_types: List of AWS resource types to scan (e.g., ['ec2', 's3'])
            
        Returns:
            Dictionary mapping resource types to lists of resource metadata
        """
        resources = {}
        
        for resource_type in resource_types:
            method_name = f"_scan_{resource_type}"
            if hasattr(self, method_name):
                scanner = getattr(self, method_name)
                resources[resource_type] = scanner()
            else:
                logger.warning(f"Scanner for {resource_type} not implemented")
                
        return resources
    
    def _scan_ec2(self) -> List[Dict[str, Any]]:
        """Scan EC2 instances."""
        ec2 = self.session.client('ec2')
        instances = []
        
        paginator = ec2.get_paginator('describe_instances')
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'vpc_id': instance.get('VpcId'),
                        'subnet_id': instance.get('SubnetId'),
                        'tags': instance.get('Tags', []),
                        'security_groups': instance.get('SecurityGroups', []),
                        'launch_time': instance.get('LaunchTime'),
                    })
        
        return instances
    
    def _scan_s3(self) -> List[Dict[str, Any]]:
        """Scan S3 buckets."""
        s3 = self.session.client('s3')
        buckets = []
        
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            try:
                encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
            except s3.exceptions.ClientError:
                encryption = None
                
            buckets.append({
                'name': bucket['Name'],
                'creation_date': bucket['CreationDate'],
                'encryption': encryption.get('ServerSideEncryptionConfiguration') if encryption else None,
                'location': s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'],
            })
            
        return buckets
    
    def _scan_rds(self) -> List[Dict[str, Any]]:
        """Scan RDS instances."""
        rds = self.session.client('rds')
        instances = []
        
        paginator = rds.get_paginator('describe_db_instances')
        for page in paginator.paginate():
            for instance in page['DBInstances']:
                instances.append({
                    'identifier': instance['DBInstanceIdentifier'],
                    'class': instance['DBInstanceClass'],
                    'engine': instance['Engine'],
                    'status': instance['DBInstanceStatus'],
                    'endpoint': instance.get('Endpoint'),
                    'multi_az': instance['MultiAZ'],
                    'storage': {
                        'type': instance['StorageType'],
                        'size': instance['AllocatedStorage'],
                        'encrypted': instance['StorageEncrypted'],
                    }
                })
                
        return instances
    
    def _scan_lambda(self) -> List[Dict[str, Any]]:
        """Scan Lambda functions."""
        lambda_client = self.session.client('lambda')
        functions = []
        
        paginator = lambda_client.get_paginator('list_functions')
        for page in paginator.paginate():
            for function in page['Functions']:
                functions.append({
                    'name': function['FunctionName'],
                    'runtime': function['Runtime'],
                    'handler': function['Handler'],
                    'role': function['Role'],
                    'memory': function['MemorySize'],
                    'timeout': function['Timeout'],
                    'last_modified': function['LastModified'],
                    'vpc_config': function.get('VpcConfig'),
                })
                
        return functions
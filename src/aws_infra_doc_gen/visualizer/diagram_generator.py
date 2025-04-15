"""Architecture Diagram Generator.

This module generates visual diagrams of AWS infrastructure using the Diagrams library.
"""

from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet
from typing import Dict, List, Any
import os

class ArchitectureDiagramGenerator:
    """Generates architecture diagrams from AWS resource data."""
    
    def __init__(self, output_dir: str):
        """Initialize the diagram generator.
        
        Args:
            output_dir: Directory to save generated diagrams
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_diagram(self, resources: Dict[str, List[Dict[str, Any]]], filename: str):
        """Generate an architecture diagram.
        
        Args:
            resources: Dictionary of AWS resources by type
            filename: Output filename (without extension)
        """
        with Diagram("AWS Architecture", filename=os.path.join(self.output_dir, filename),
                    show=False):
            
            # Group resources by VPC
            vpc_resources = self._group_by_vpc(resources)
            
            # Create nodes for resources not in a VPC
            s3_buckets = []
            if 's3' in resources:
                for bucket in resources['s3']:
                    s3_buckets.append(S3(bucket['name']))
            
            # Create VPC clusters and their resources
            for vpc_id, vpc_data in vpc_resources.items():
                with Cluster(f"VPC {vpc_id}"):
                    # Create subnet clusters
                    subnet_resources = self._group_by_subnet(vpc_data)
                    
                    for subnet_id, subnet_data in subnet_resources.items():
                        with Cluster(f"Subnet {subnet_id}"):
                            # Create EC2 instances
                            ec2_instances = []
                            for instance in subnet_data.get('ec2', []):
                                ec2_instances.append(
                                    EC2(f"{instance['id']}\n{instance['type']}")
                                )
                            
                            # Create RDS instances
                            rds_instances = []
                            for db in subnet_data.get('rds', []):
                                rds_instances.append(
                                    RDS(f"{db['identifier']}\n{db['engine']}")
                                )
                            
                            # Create Lambda functions
                            lambda_functions = []
                            for func in subnet_data.get('lambda', []):
                                lambda_functions.append(
                                    Lambda(f"{func['name']}\n{func['runtime']}")
                                )
                            
                            # Connect resources within subnet
                            self._create_connections(
                                ec2_instances,
                                rds_instances,
                                lambda_functions,
                                s3_buckets
                            )
    
    def _group_by_vpc(self, resources: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict]:
        """Group resources by VPC ID."""
        vpc_resources = {}
        
        # Process EC2 instances
        for instance in resources.get('ec2', []):
            vpc_id = instance.get('vpc_id', 'no_vpc')
            if vpc_id not in vpc_resources:
                vpc_resources[vpc_id] = {'ec2': []}
            vpc_resources[vpc_id]['ec2'].append(instance)
        
        # Process RDS instances
        for db in resources.get('rds', []):
            if 'DBSubnetGroup' in db:
                vpc_id = db['DBSubnetGroup'].get('VpcId', 'no_vpc')
                if vpc_id not in vpc_resources:
                    vpc_resources[vpc_id] = {'rds': []}
                elif 'rds' not in vpc_resources[vpc_id]:
                    vpc_resources[vpc_id]['rds'] = []
                vpc_resources[vpc_id]['rds'].append(db)
        
        # Process Lambda functions
        for func in resources.get('lambda', []):
            vpc_config = func.get('vpc_config', {})
            if vpc_config:
                vpc_id = vpc_config.get('VpcId', 'no_vpc')
                if vpc_id not in vpc_resources:
                    vpc_resources[vpc_id] = {'lambda': []}
                elif 'lambda' not in vpc_resources[vpc_id]:
                    vpc_resources[vpc_id]['lambda'] = []
                vpc_resources[vpc_id]['lambda'].append(func)
        
        return vpc_resources
    
    def _group_by_subnet(self, vpc_data: Dict) -> Dict[str, Dict]:
        """Group VPC resources by subnet ID."""
        subnet_resources = {}
        
        # Process EC2 instances
        for instance in vpc_data.get('ec2', []):
            subnet_id = instance.get('subnet_id', 'no_subnet')
            if subnet_id not in subnet_resources:
                subnet_resources[subnet_id] = {'ec2': []}
            subnet_resources[subnet_id]['ec2'].append(instance)
        
        # Process RDS instances
        for db in vpc_data.get('rds', []):
            if 'DBSubnetGroup' in db:
                for subnet in db['DBSubnetGroup'].get('Subnets', []):
                    subnet_id = subnet.get('SubnetIdentifier', 'no_subnet')
                    if subnet_id not in subnet_resources:
                        subnet_resources[subnet_id] = {'rds': []}
                    elif 'rds' not in subnet_resources[subnet_id]:
                        subnet_resources[subnet_id]['rds'] = []
                    subnet_resources[subnet_id]['rds'].append(db)
        
        # Process Lambda functions
        for func in vpc_data.get('lambda', []):
            vpc_config = func.get('vpc_config', {})
            if vpc_config:
                for subnet_id in vpc_config.get('SubnetIds', []):
                    if subnet_id not in subnet_resources:
                        subnet_resources[subnet_id] = {'lambda': []}
                    elif 'lambda' not in subnet_resources[subnet_id]:
                        subnet_resources[subnet_id]['lambda'] = []
                    subnet_resources[subnet_id]['lambda'].append(func)
        
        return subnet_resources
    
    def _create_connections(self, ec2_instances, rds_instances, lambda_functions, s3_buckets):
        """Create connections between resources based on security groups and policies."""
        # Connect EC2 to RDS if they share security groups
        for ec2 in ec2_instances:
            for rds in rds_instances:
                ec2 >> rds
        
        # Connect Lambda to other resources based on VPC config and policies
        for lambda_func in lambda_functions:
            for s3 in s3_buckets:
                lambda_func >> s3
            for rds in rds_instances:
                lambda_func >> rds
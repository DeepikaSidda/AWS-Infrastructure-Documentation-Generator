"""Change Tracker.

This module tracks changes in AWS infrastructure over time.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import boto3
import git
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class ChangeTracker:
    """Tracks changes in AWS infrastructure."""
    
    def __init__(self, storage_type: str, **kwargs):
        """Initialize the change tracker.
        
        Args:
            storage_type: Where to store changes ('git' or 's3')
            **kwargs: Additional arguments for storage configuration
        """
        self.storage_type = storage_type
        self.storage_config = kwargs
        
        if storage_type == 's3':
            self.s3_client = boto3.client('s3')
            self.bucket_name = kwargs.get('bucket_name')
            if not self.bucket_name:
                raise ValueError("bucket_name is required for S3 storage")
        elif storage_type == 'git':
            self.repo_path = kwargs.get('repo_path')
            if not self.repo_path:
                raise ValueError("repo_path is required for Git storage")
            self._init_git_repo()
    
    def _init_git_repo(self):
        """Initialize or open Git repository."""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        
        try:
            self.repo = git.Repo(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            self.repo = git.Repo.init(self.repo_path)
    
    def save_snapshot(self, resources: Dict[str, List[Dict[str, Any]]]):
        """Save a snapshot of the current infrastructure state.
        
        Args:
            resources: Dictionary of AWS resources by type
        """
        timestamp = datetime.now().isoformat()
        snapshot = {
            'timestamp': timestamp,
            'resources': resources
        }
        
        if self.storage_type == 's3':
            self._save_to_s3(snapshot, timestamp)
        else:  # git
            self._save_to_git(snapshot, timestamp)
    
    def _save_to_s3(self, snapshot: Dict, timestamp: str):
        """Save snapshot to S3."""
        key = f"snapshots/{timestamp}.json"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(snapshot, indent=2)
            )
        except ClientError as e:
            logger.error(f"Error saving to S3: {e}")
            raise
    
    def _save_to_git(self, snapshot: Dict, timestamp: str):
        """Save snapshot to Git repository."""
        file_path = os.path.join(self.repo_path, f"snapshot_{timestamp}.json")
        
        with open(file_path, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        self.repo.index.add([file_path])
        self.repo.index.commit(f"Infrastructure snapshot {timestamp}")
    
    def get_changes(self, start_time: str, end_time: str = None) -> List[Dict]:
        """Get infrastructure changes between two points in time.
        
        Args:
            start_time: ISO format timestamp for start of period
            end_time: ISO format timestamp for end of period (default: now)
            
        Returns:
            List of changes detected between snapshots
        """
        if not end_time:
            end_time = datetime.now().isoformat()
        
        start_snapshot = self._get_snapshot(start_time)
        end_snapshot = self._get_snapshot(end_time)
        
        return self._compare_snapshots(start_snapshot, end_snapshot)
    
    def _get_snapshot(self, timestamp: str) -> Dict:
        """Retrieve a specific snapshot."""
        if self.storage_type == 's3':
            return self._get_s3_snapshot(timestamp)
        else:  # git
            return self._get_git_snapshot(timestamp)
    
    def _get_s3_snapshot(self, timestamp: str) -> Dict:
        """Get snapshot from S3."""
        key = f"snapshots/{timestamp}.json"
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return json.loads(response['Body'].read())
        except ClientError as e:
            logger.error(f"Error reading from S3: {e}")
            raise
    
    def _get_git_snapshot(self, timestamp: str) -> Dict:
        """Get snapshot from Git repository."""
        file_path = os.path.join(self.repo_path, f"snapshot_{timestamp}.json")
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Snapshot not found: {timestamp}")
            raise
    
    def _compare_snapshots(self, old: Dict, new: Dict) -> List[Dict]:
        """Compare two snapshots and identify changes.
        
        Returns:
            List of changes with type (added/removed/modified) and details
        """
        changes = []
        
        for resource_type in set(old['resources'].keys()) | set(new['resources'].keys()):
            old_resources = {
                self._resource_id(r): r
                for r in old['resources'].get(resource_type, [])
            }
            new_resources = {
                self._resource_id(r): r
                for r in new['resources'].get(resource_type, [])
            }
            
            # Find added resources
            for resource_id in set(new_resources.keys()) - set(old_resources.keys()):
                changes.append({
                    'type': 'added',
                    'resource_type': resource_type,
                    'resource_id': resource_id,
                    'details': new_resources[resource_id]
                })
            
            # Find removed resources
            for resource_id in set(old_resources.keys()) - set(new_resources.keys()):
                changes.append({
                    'type': 'removed',
                    'resource_type': resource_type,
                    'resource_id': resource_id,
                    'details': old_resources[resource_id]
                })
            
            # Find modified resources
            for resource_id in set(old_resources.keys()) & set(new_resources.keys()):
                if old_resources[resource_id] != new_resources[resource_id]:
                    changes.append({
                        'type': 'modified',
                        'resource_type': resource_type,
                        'resource_id': resource_id,
                        'old': old_resources[resource_id],
                        'new': new_resources[resource_id]
                    })
        
        return changes
    
    def _resource_id(self, resource: Dict) -> str:
        """Get unique identifier for a resource."""
        if 'id' in resource:
            return resource['id']
        elif 'name' in resource:
            return resource['name']
        elif 'identifier' in resource:
            return resource['identifier']
        else:
            return json.dumps(sorted(resource.items()))
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.aws.security import IdentityAndAccessManagementIam

# Set diagram attributes for better visualization
with Diagram("Swastyashe Architecture", show=True, direction="LR"):
    # Create API Gateway as entry point
    api = APIGateway("API Gateway")
    
    with Cluster("Backend Services"):
        # Lambda functions for different features
        lambda_auth = Lambda("Auth Handler")
        lambda_health = Lambda("Health Recommendations")
        lambda_user = Lambda("User Management")
        lambda_subscription = Lambda("Subscription Handler")
        
        # Group Lambda functions
        lambdas = [lambda_auth, lambda_health, lambda_user, lambda_subscription]
        
        # DynamoDB tables
        with Cluster("DynamoDB Tables"):
            db_users = Dynamodb("Users Table")
            db_health = Dynamodb("Health Data")
            db_subscriptions = Dynamodb("Subscriptions")
            
        # Security and Monitoring
        iam = IdentityAndAccessManagementIam("IAM Roles")
        monitoring = Cloudwatch("CloudWatch Logs")

    # Define relationships
    api >> lambdas

    lambda_auth >> db_users
    lambda_health >> db_health
    lambda_user >> db_users
    lambda_subscription >> db_subscriptions

    # IAM and monitoring connections
    iam >> lambdas
    lambdas >> monitoring

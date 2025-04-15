

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.programming.framework import React
from diagrams.aws.security import IAMRole

# Set some styling attributes
graph_attr = {
    "fontsize": "45",
    "bgcolor": "white"
}

# Create the diagram
with Diagram("Serverless Registration Form Architecture", 
            show=True, 
            direction="LR",
            graph_attr=graph_attr):
    
    # Frontend
    with Cluster("Frontend"):
        frontend = React("Registration Form")

    # AWS Cloud
    with Cluster("AWS Cloud"):
        # API Gateway with edge attributes
        api = APIGateway("API Gateway")

        # Backend Services
        with Cluster("Backend Services"):
            lambda_fn = Lambda("Registration Handler")
            
            # Monitoring and Logging
            with Cluster("Monitoring"):
                cloudwatch = Cloudwatch("CloudWatch Logs")
            
            # Security
            with Cluster("Security"):
                iam_role = IAMRole("Lambda Role")
                iam = IAM("IAM")

            # Database
            with Cluster("Database"):
                dynamodb = Dynamodb("Registration Table")

        # Define relationships with custom edges
        frontend >> Edge(color="blue", style="bold") >> api
        api >> Edge(color="green") >> lambda_fn
        lambda_fn >> Edge(color="red") >> dynamodb
        
        # Security and monitoring connections
        iam - Edge(color="orange", style="dashed") - iam_role
        iam_role - Edge(color="orange", style="dashed") - lambda_fn
        lambda_fn >> Edge(color="purple", style="dotted") >> cloudwatch

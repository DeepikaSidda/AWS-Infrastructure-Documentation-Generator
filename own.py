from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.security import IAM, SecurityHub
from diagrams.aws.management import Config, Cloudwatch
from diagrams.aws.network import VPC
from diagrams.programming.language import Python
from diagrams.aws.security import IAMRole
from diagrams.aws.analytics import Analytics

# Diagram styling
graph_attr = {
    "fontsize": "45",
    "bgcolor": "white",
    "splines": "spline"
}

with Diagram("AWS Infrastructure Documentation Tool Architecture", 
            show=True, 
            direction="TB",
            graph_attr=graph_attr):

    # Tool Core
    with Cluster("Documentation Tool Core"):
        scanner = Python("Infrastructure Scanner")
        diagram_gen = Python("Diagram Generator")
        doc_gen = Python("Doc Generator")
        change_tracker = Python("Change Tracker")
        compliance_checker = Python("Compliance Checker")

    # AWS Infrastructure Being Scanned
    with Cluster("AWS Infrastructure Under Scan"):
        with Cluster("Compute Resources"):
            ec2 = EC2("EC2 Instances")
            lambda_fn = Lambda("Lambda Functions")

        with Cluster("Storage"):
            s3 = S3("S3 Buckets")
            rds = RDS("RDS Databases")

        with Cluster("Networking"):
            vpc = VPC("VPC Config")

    # Security and Compliance
    with Cluster("Security & Compliance"):
        iam = IAM("IAM Policies")
        security_hub = SecurityHub("Security Hub")
        config = Config("AWS Config")

    # Output Storage and Monitoring
    with Cluster("Documentation Storage & Monitoring"):
        with Cluster("Output Storage"):
            docs_bucket = S3("Documentation Bucket")
            snapshot_bucket = S3("Snapshot Storage")
        
        with Cluster("Monitoring"):
            cloudwatch = Cloudwatch("CloudWatch Logs")

    # Analysis and Reporting
    with Cluster("Analysis & Reporting"):
        analytics = Analytics("Change Analytics")
        report_gen = Python("Report Generator")

    # Define relationships
    # Scanning Flow
    scanner >> Edge(color="blue", label="scan") >> [ec2, lambda_fn, s3, rds, vpc]
    scanner >> Edge(color="orange", label="verify") >> iam

    # Documentation Generation
    scanner >> Edge(color="green") >> diagram_gen
    scanner >> Edge(color="green") >> doc_gen
    
    # Change Tracking
    scanner >> Edge(color="red", style="dashed") >> change_tracker
    change_tracker >> Edge(color="red") >> snapshot_bucket
    change_tracker >> Edge(color="red", style="dotted") >> analytics

    # Compliance Checking
    compliance_checker << Edge(color="purple") << [security_hub, config]
    compliance_checker >> Edge(color="purple", style="bold") >> report_gen

    # Output Storage
    diagram_gen >> Edge(color="black") >> docs_bucket
    doc_gen >> Edge(color="black") >> docs_bucket
    report_gen >> Edge(color="black") >> docs_bucket

    # Monitoring
    [scanner, change_tracker, compliance_checker] >> Edge(color="brown", style="dotted") >> cloudwatch

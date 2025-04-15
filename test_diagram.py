from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import VPC

with Diagram("Simple AWS Architecture", show=True):
    vpc = VPC("VPC")
    ec2 = EC2("Web Server")
    db = RDS("Database")
    
    ec2 >> db

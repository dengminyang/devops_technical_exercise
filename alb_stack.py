from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct

class AlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create an Internet-facing Application Load Balancer in Public Subnets
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "PublicALB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )

        # 2. Add an HTTP Listener (Port 80)
        # Note: In a production environment, you would use port 443 with an ACM SSL Certificate.
        listener = self.alb.add_listener(
            "HttpListener",
            port=80,
            open=True
        )

        # 3. Create a Default Target Group 
        # (This is where your ECS tasks, Lambda, or EC2 instances will register to receive traffic)
        self.target_group = listener.add_targets(
            "DefaultTargetGroup",
            port=80,
            targets=[] # You will attach your compute targets here later
        )

        # Optional: Add a health check configuration to the target group
        self.target_group.configure_health_check(
            path="/",
            interval=Duration.seconds(30)
        )
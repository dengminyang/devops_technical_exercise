from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct


class ComputeStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create an ECS Cluster inside the private subnets of our VPC
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # 2. Define the Fargate Service with an Application Load Balancer (ALB) entry point
        self.fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "WebFargateService",
            cluster=cluster,
            cpu=256,  # 0.25 vCPU (Cost-conscious baseline)
            memory_limit_mib=512,  # 512 MB RAM
            desired_count=2,  # Multi-AZ redundancy for high availability
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(
                    "amazon/amazon-ecs-sample"
                ),  # Placeholder app image
                container_port=80,
            ),
            public_load_balancer=True,  # ALB sits in public subnets; tasks sit in private subnets
        )

        # Configure health check grace period for container startup
        self.fargate_service.target_group.configure_health_check(
            path="/", interval=Duration.seconds(30)
        )

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_s3 as s3,
)
from constructs import Construct

class DataStorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. PostgreSQL Database via Amazon RDS (placed in Isolated Subnets)
        self.database = rds.DatabaseInstance(
            self, "PostgresDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            vpc=vpc,
            # Place DB in strictly isolated subnets with zero internet routing
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            # Cost-conscious choice: t3.micro keeps baseline costs minimal for validation
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            allocated_storage=20,
            max_allocated_storage=50,
            deletion_protection=False,  # Set to True in a true production environment
            removal_policy=RemovalPolicy.DESTROY  # Allows easy cleanup during testing
        )

        # 2. S3 Bucket with Secure Access Controls
        self.secure_bucket = s3.Bucket(
            self, "SecureAppStorage",
            # Encrypt objects using S3-managed keys by default
            encryption=s3.BucketEncryption.S3_MANAGED,
            # Completely block public access (prevents accidental public exposure)
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            # Enforce TLS/HTTPS for all incoming data transfers
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True  # Convenient for testing teardowns
        )
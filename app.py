#!/usr/bin/env python3
import aws_cdk as cdk

from vpc_stack import VpcStack
from compute_stack import ComputeStack
from data_storage_stack import DataStorageStack

app = cdk.App()

# 1. Deploy the VPC Stack first (it forms the secure networking foundation)
vpc_stack = VpcStack(app, "ProductionVpcStack")

# 2. Deploy the Compute Stack (ECS + ALB), passing the shared VPC reference
compute_stack = ComputeStack(app, "ProductionComputeStack", vpc=vpc_stack.vpc)

# 3. Deploy the Data & Storage Stack (RDS Postgres + S3), passing the shared VPC reference
data_storage_stack = DataStorageStack(
    app, "ProductionDataStorageStack", vpc=vpc_stack.vpc
)

app.synth()

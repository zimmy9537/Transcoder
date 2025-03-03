"""
Transcoder stack
"""

from aws_cdk import Stack
from constructs import Construct

from cdk.constructs.iam_construct import IamConstruct
from cdk.constructs.lambda_construct import LambdaConstruct
from cdk.constructs.api_construct import ApiConstruct
from cdk.constructs.s3_construct import S3Construct
from cdk.constructs.construct_helper import ConstructHelper

class ServiceStack(Stack):
    """Transcoder CDK Stack definition"""

    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)
        
        construct_helper = ConstructHelper(self)

        # Initialize IAM construct
        iam_construct = IamConstruct(
            self,
            "IamConstruct",
            construct_helper
        )

        # Initialize Lambda construct
        lambda_construct = LambdaConstruct(
            self,
            "LambdaConstruct",
            iam_construct.lambda_role,
            construct_helper
        )

        # Initialize APi Gateway construct
        ApiConstruct(
            self,
            "ApiConstruct",
            iam_construct.api_gateway_role,
            iam_construct.api_gateway_policy_document,
            lambda_construct.lambda_functions,
            construct_helper
        )

        # Initialize S3 construct
        S3Construct(
            self,
            "S3Construct",
            construct_helper
        )

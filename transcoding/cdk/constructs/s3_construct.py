"""
S3 Construct
Deploy:
    - S3 Bucket
    - S3 Bucket Policy
"""

from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import RemovalPolicy

buckets = ["videostore"]

class S3Construct(Construct):
    """S3 Constructs CDK definition"""

    def __init__(
            self, scope: Construct, stack_id: str, construct_helper, **kwargs
    ) -> None:
        """
        Following parameters are required to create an S3 Construct:
        - stack_id
        Args:
            scope (Construct): CDK stack
            stack_id (str): Stack ID
        Returns:
            None
        """
        super().__init__(scope, stack_id, **kwargs)

        self.construct_helper = construct_helper

        for bucket in buckets:
            self.create_s3_bucket(bucket)
    
    def create_s3_bucket(self, bucket_name: str) -> None:
        """
        Create S3 Bucket
        """
        self.bucket = s3.Bucket(
            self,
            self.construct_helper.get_resource_name(bucket_name),
            bucket_name=self.construct_helper.get_resource_name(bucket_name),
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY
        )

        self.bucket.add_cors_rule(
            allowed_methods=[
                s3.HttpMethods.GET,
                s3.HttpMethods.PUT,
                s3.HttpMethods.POST,
            ],
            allowed_origins=["*"],
            allowed_headers=["*"]
        )

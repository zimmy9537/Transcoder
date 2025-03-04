"""
IAM Construct
Deploy:
    - IAM Role
    - IAM Policy
"""

from constructs import Construct
from aws_cdk import aws_iam as iam


class IamConstruct(Construct):
    """IAM Constructs CDK definition"""

    def __init__(
        self, scope: Construct, stack_id: str, construct_helper, **kwargs
    ) -> None:
        """
        Following parameters are required to create an IAM Construct:
        - stack_id
        Args:
            scope (Construct): CDK stack
            stack_id (str): Stack ID
        Returns:
            None
        """
        super().__init__(scope, stack_id, **kwargs)

        self.construct_helper = construct_helper

        # create policies
        self.create_s3_policy()
        self.create_api_gateway_policy()
        self.create_apigateway_read_policy()
        self.create_lambda_policy()
        self.create_cloud_watch_policy()

        # create roles
        self.create_api_gateway_role()
        self.create_lambda_role()

    def create_s3_policy(self) -> None:
        """
        Create S3 Policy
        """
        s3_policy_statement = iam.PolicyStatement(
            actions=[
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:DeleteObject",
            ],
            effect=iam.Effect.ALLOW,
            resources=["*"],
            sid="S3PolicyStatement",
        )

        self.s3_policy_document = iam.PolicyDocument(statements=[s3_policy_statement])

    def create_api_gateway_policy(self) -> None:
        """
        Create API Gateway Policy
        """
        api_gateway_policy_statement = iam.PolicyStatement(
            actions=["execute-api:Invoke"],
            effect=iam.Effect.ALLOW,
            resources=["execute-api:/*/*/*"],
            sid="APIGatewayPolicyStatement",
            principals=[iam.AnyPrincipal()],
        )

        self.api_gateway_policy_document = iam.PolicyDocument(
            statements=[api_gateway_policy_statement]
        )

    def create_apigateway_read_policy(self) -> None:
        """
        Create API Gateway Read Policy
        """
        apigateway_read_policy_statement = iam.PolicyStatement(
            actions=["apigateway:GET"],
            effect=iam.Effect.ALLOW,
            resources=["*"],
            sid="APIGatewayReadPolicyStatement",
        )

        self.apigateway_read_policy_document = iam.PolicyDocument(
            statements=[apigateway_read_policy_statement]
        )

    def create_lambda_policy(self) -> None:
        """
        Create Lambda Policy
        """
        lambda_policy_statement = iam.PolicyStatement(
            actions=[
                "lambda:CreateEventSourceMapping",
                "lambda:ListEventSourceMappings",
                "lambda:ListFunctions",
            ],
            effect=iam.Effect.ALLOW,
            resources=["*"],
            sid="LambdaPolicyStatement",
        )

        self.lambda_policy_document = iam.PolicyDocument(
            statements=[lambda_policy_statement]
        )
    
    def create_cloud_watch_policy(self) -> None:
        """
        Create Cloud Watch Policy
        """
        cloud_watch_policy_statement = iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
            ],
            effect=iam.Effect.ALLOW,
            resources=["*"],
            sid="CloudWatchPolicyStatement",
        )

        self.cloud_watch_policy_document = iam.PolicyDocument(
            statements=[cloud_watch_policy_statement]
        )

    def create_api_gateway_role(self) -> None:
        """
        Create API Gateway Role
        """
        self.api_gateway_role = iam.Role(
            self,
            self.construct_helper.get_resource_name("api-gateway-role"),
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            inline_policies={"S3Policy": self.s3_policy_document},
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonAPIGatewayPushToCloudWatchLogs"
                )
            ]
        )

    def create_lambda_role(self) -> None:
        """
        Create Lambda Role
        """
        self.lambda_role = iam.Role(
            self,
            self.construct_helper.get_resource_name("lambda-role"),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "LambdaPolicy": self.lambda_policy_document,
                "S3Policy": self.s3_policy_document,
                "APIGatewayReadPolicy": self.apigateway_read_policy_document,
                "CloudWatchPolicy": self.cloud_watch_policy_document,
            },
        )

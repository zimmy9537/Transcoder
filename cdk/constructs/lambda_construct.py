"""
Lambda Construct

Deploy:
    - Lambda function
"""

import os
from constructs import Construct
from aws_cdk import aws_lambda as _lambda
from aws_cdk import Duration
from aws_cdk import aws_iam as iam

class LambdaConstruct(Construct):
    """"
    Lambda Construct
    """

    def __init__(self, scope: Construct, stack_id: str, lambda_role: iam.Role, construct_helper, **kwargs) -> None:
        """
        Following parameters are required to create a Lambda Construct:
        - create_layers
        - create_lambda_roles
        _ create lambda
        Args:
            scope (Construct): CDK stack
            stack_id (str): Stack ID
            lambda_role (iam.Role): Lambda Role
            construct_helper (ConstructHelper): Construct helper
        Returns:
            None
        """

        super().__init__(scope, stack_id, **kwargs)

        self.construct_helper = construct_helper

        self.lambda_data = self.construct_helper.read_config_data("lambda.json")

        self.lambda_role = lambda_role

        # Create Layers
        self.create_layers()

        # Create Lambda Functions
        self.create_lambda()
    
    def create_layers(self) -> None:
        """
        Create Lambda Layers
        """
        self.common_layer = _lambda.LayerVersion(
            self,
            self.construct_helper.get_resource_name("common-layer"),
            code=_lambda.AssetCode(
                os.path.join(os.getcwd(), "service", "handlers", "layers", "common")
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="Common Layer for Lambda Functions"
        )

        self.external_layer = _lambda.LayerVersion(
            self,
            self.construct_helper.get_resource_name("external-layer"),
            code=_lambda.AssetCode(
                os.path.join(os.getcwd(), "service", "handlers", "layers", "external")
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="External Layer for Lambda Functions"
        )
    
    def create_lambda(self):
        """
        Create Lambda Functions
        """
        self.lambda_functions = {}
        for lambda_config in self.lambda_data:
            self.lambda_functions[lambda_config.get("name")] = self.get_lambda(lambda_config)

        
    
    def get_lambda(self, lambda_config):
        """
        Get each Lambda Function from lambda.json
        Args:
            lambda_config (dict): Lambda Config
        Returns:
            _lambda.Function: Lambda Function
        """

        lambda_name = lambda_config.get("name")

        lambda_resource_name = self.construct_helper.get_resource_name(lambda_name)

        mandatory_layers = [self.common_layer, self.external_layer]
        
        environment = {}
        for env in lambda_config.get("environment"):
            environment[env] = self.construct_helper.get_parameter_value(env)
        
        lambda_function = _lambda.Function(
            self,
            lambda_resource_name,
            function_name=lambda_resource_name,
            timeout= Duration.seconds(lambda_config.get("timeout")),
            memory_size=lambda_config.get("memory_size"),
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(
                os.path.join(os.getcwd(), "service", "handlers", "lambdas", lambda_name)
            ),
            role=self.lambda_role,
            handler = "lambda_handler.lambda_handler",
            layers=mandatory_layers,
            environment=environment,
            tracing=_lambda.Tracing.ACTIVE
        )

        return lambda_function

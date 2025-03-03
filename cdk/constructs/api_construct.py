"""
API Construct

Deploy:
    - API Gateway
    - Lambda Integration
"""

from constructs import Construct
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda

class ApiConstruct(Construct):
    """
    API Construct
    """

    def __init__(self, scope: Construct, stack_id:str, api_gateway_role: iam.Role, api_gateway_policy_document: iam.PolicyDocument, lambda_functions:list, construct_helper, **kwargs) -> None:
        """
        Following parameters are required to create an API Construct:
        - api_gateway_role
        - api_gateway_policy_document
        - lambda_functions
        Args:
            scope (Construct): CDK stack
            stack_id (str): Stack ID
            api_gateway_role (iam.Role): API Gateway Role
            api_gateway_policy_document (iam.PolicyDocument): API Gateway Policy Document
            lambda_functions (list): Lambda Functions
            construct_helper (ConstructHelper): Construct Helper
        Returns:
            None
        """

        super().__init__(scope, stack_id, **kwargs)

        self.api_gateway_role = api_gateway_role
        self.api_gateway_policy_document = api_gateway_policy_document
        self.lambda_functions = lambda_functions
        self.construct_helper = construct_helper

        api_resources_data = self.construct_helper.read_config_data("api_resources.json")

        self.backend_api_endpoints = api_resources_data["backend_api_endpoints"]

        self.create_api_gateway()

        self.apigw_add_endpoints()

    def create_api_gateway(self) -> None:
        """
        Create API Gateway
        """
        api_name = self.construct_helper.get_resource_name("transcoder-api")
        self.api_gateway = apigateway.RestApi(
            self,
            api_name,
            rest_api_name=api_name,
            description="API Gateway for Transcoder Service",
            policy=self.api_gateway_policy_document,
            cloud_watch_role=True
        )

        suffix = self.construct_helper.get_parameter_value("SUFFIX")

        deployment = apigateway.Deployment(self, id="deployment-api", api=self.api_gateway)
        
        stage_name = suffix
        
        stage = apigateway.Stage(
            self,
            id = f"{stage_name}-api",
            deployment = deployment,
            stage_name = stage_name,
            tracing_enabled= True,
            metrics_enabled= True,
            logging_level= apigateway.MethodLoggingLevel.INFO,
        )

        self.api_gateway.deployment_stage = stage

    def apigw_add_endpoints(self):
        """
        Generate integration and method response
        Create resource and integrate with lambda function
        Add CORS to the API Gateway
        """

        for resource_name, methods in self.backend_api_endpoints.items():
            for method_config in methods:
                lambda_name = method_config["LAMBDA"]
                method_type = method_config["METHOD"]
                request_params = method_config.get("REQUEST_PARAMETER", {})

                # Find the Lambda function object from the list
                lambda_function = self._find_lambda_function(lambda_name)
                if not lambda_function:
                    raise ValueError(f"Lambda function {lambda_name} not found")

                # Create the resource in API Gateway
                api_resource = self.api_gateway.root.add_resource(resource_name)

                # Create the Lambda Integration
                integration = apigateway.LambdaIntegration(lambda_function, proxy=True)

                # Add method with request parameters if defined
                api_resource.add_method(
                    method_type,
                    integration,
                    authorization_type=apigateway.AuthorizationType.NONE,
                    request_parameters=request_params if request_params else None,
                )

                # Enable CORS if needed
                self._add_cors(api_resource, method_type)

    def _find_lambda_function(self, lambda_name: str) -> _lambda.Function:
        """
        Finds the Lambda function from the list based on the function name.
        Args:
            lambda_name (str): The name of the Lambda function to find
        Returns:
            _lambda.Function: The Lambda function if found, else None
        """
        for function_name, function in self.lambda_functions.items():
            if function_name == lambda_name:
                return function
        return None

    def _add_cors(self, api_resource: apigateway.IResource, method_type: str):
        """
        Adds CORS configuration to a resource.
        Args:
            api_resource (apigateway.IResource): The API Gateway resource to add CORS to
            method_type (str): The HTTP method type (GET, POST, etc.)
        """
        if method_type in ["GET", "POST", "OPTIONS"]:
            api_resource.add_cors_preflight(
                allow_origins=["*"],  # Allow all origins, but restrict as needed
                allow_methods=["GET", "POST", "OPTIONS"],
                allow_headers=["*"],  # You can restrict this as needed
            )


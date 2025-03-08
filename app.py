"""
App file to deploy the stack
"""

from aws_cdk import App, Environment

from cdk.constructs.service_stack import ServiceStack


def launch(app, env, environment):
    """
    Launch function to deploy the stack
    Args:
        app(App): CDK App
        env(dict): Environment
        environment(str): Environment name
    """
    app.node.set_context("env", environment)

    ServiceStack(app, f"TranscodingStack-{environment}", env=env)


if __name__ == "__main__":
    app = App()

    environment = "int"
    env = Environment(region="us-east-1", account="211125591634")
    launch(app, env, environment)

    app.synth()

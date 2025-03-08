"""
response wrapper for lambda response management
"""

from http import HTTPStatus

from aws_lambda_powertools import Logger

logger = Logger()

def generate_response(func):
    """
    Lambda response generator
    Args:
        func (function): Function to be wrapped
    Returns:
        function: Wrapped function
    """

    def wrapper(event, context):
        try:
            logger.info(f"starting to generate response for event - {event}")
            result = func(event, context)

            response = {
                "statusCode": result["statusCode"],
                "body": {"message": result["message"]}
            }

            data = result.get("body")

            if data is not None:
                response["body"]["data"] = data
        
        except Exception as err:
            logger.info(f"The exception is - {str(err)}")
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST.value,
                "body": {"message": str(err)}
            }
        
        logger.info(f"response generated - {response}")
        return response
    
    return wrapper

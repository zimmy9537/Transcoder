"""
Lambda to initialize transcoding
"""

from typing import Any

def lambda_handler(event: dict[str, Any], _) -> dict[str, Any]:
    """
    Lambda handler function to initialize transcoding
    Args:
        event (dict): Event data
    Returns:
        dict: Response
    """
    print(event)
    return {
        "statusCode": 200,
        "body": "Hello from transcoder lambda!"
    }

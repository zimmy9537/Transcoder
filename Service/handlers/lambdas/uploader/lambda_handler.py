"""
Lambda for uploading files to s3
"""

from typing import Any

def lambda_handler(event: dict[str, Any], _) -> dict[str, Any]:
    """
    Lambda handler function to upload files to s3
    Args:
        event (dict): Event data
    Returns:
        dict: Response
    """
    return {
        "statusCode": 200,
        "body": "Hello from uploader lambda!"
    }
"""
Lambda for uploading files to s3
"""

from typing import Any
from upload_manager import UploadManager

uploadManager = UploadManager()

def lambda_handler(event: dict[str, Any], _) -> dict[str, Any]:
    """
    Lambda handler function to upload files to s3
    Args:
        event (dict): Event data
    Returns:
        dict: Response
    """
    
    queryparam = event["queryStringParameters"]

    file_name = queryparam["fileName"]
    user_id = queryparam["userId"]
    
    response = uploadManager.generate_s3_put_presigned_url(file_name, user_id)

    return response

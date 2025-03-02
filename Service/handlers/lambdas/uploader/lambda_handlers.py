"""
Lambda for uploading files to s3
"""

def lambda_handler(event, context):
    """
    Lambda handler function to upload files to s3
    Args:
        event (dict): Event data
        context (object): Context data
    Returns:
        dict: Response
    """
    return {
        "statusCode": 200,
        "body": "Hello from uploader lambda!"
    }
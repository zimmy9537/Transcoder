"""
Lambda to initialize transcoding
"""

def lambda_handler(event, context):
    """
    Lambda handler function to initialize transcoding
    Args:
        event (dict): Event data
        context (object): Context data
    Returns:
        dict: Response
    """
    return {
        "statusCode": 200,
        "body": "Hello from transcoder lambda!"
    }

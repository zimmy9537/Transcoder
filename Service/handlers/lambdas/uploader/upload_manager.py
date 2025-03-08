"""
Manager for uploading the video
"""

import boto3
import os
import time
from http import HTTPStatus
from aws_lambda_powertools import Logger

from botocore.config import Config

suffix = os.environ.get("SUFFIX", "int")
bucket = f"uploader-{suffix}"
config = Config(signature_version="s3v4")

logger = Logger()

class UploadManager:
    """
    Video upload management
    """

    @staticmethod
    def generate_s3_put_presigned_url(file_name: str, user_id: str) -> str:
        """
        Generate S3 put URL
        Args:
            file_name (str): Filename
            user_id (str): User ID
        Returns:
            str: S3 put presigned URL
        """
        s3_client = boto3.client("s3", config=config)
        try:
            presigned_url = s3_client.generate_presigned_post(
                Bucket=bucket,
                Key=f"uploads/{user_id}/{time.time()}/{file_name}",
                ExpiresIn=900,
            )

            return {
                "statusCode": HTTPStatus.OK.value,
                "message": "Presigned URL generated successfully",
                "body": presigned_url,
            }
        except Exception as err:
            logger.info(f"The exception is - {str(err)}")
            raise Exception("Error in generating presigned URL")

"""
# functions
- upload_file
- download_file
    - download_from_standard
    - download_from_glacier
        - restore_from_glacier
        - check_obj_status
- search_keyword_global
    - search_keyword_s3
    - search_keyword_local

Author: William Wright
"""

import os

# import logging

import boto3
from botocore.exceptions import ClientError


class AwsStorageMgmt:
    def __init__(self):
        self.s3_resour = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.bucket = os.getenv("AWS_BUCKET")
        self.object_name = os.getenv("AWS_BUCKET_PATH")

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        from click import echo

        echo(
            f"uploading: {file_name} \nto S3 bucket: {os.getenv('AWS_BUCKET')}/{os.getenv('AWS_BUCKET_PATH')}/{file_name}"
        )
        if not object_name:
            object_name = os.path.join(self.object_name, file_name)
        else:
            object_name = os.path.join(object_name, file_name)

        try:
            # response = self.s3_client.upload_file(file_name, self.bucket, object_name)
            with open(file_name, "rb") as data:
                self.s3_client.upload_fileobj(data, self.bucket, object_name)
        except ClientError as e:
            # logging.error(e)
            echo(e)
            echo("success? False\n")
            return False
        echo("success? True\n")
        return True

    def download_file(self, file_name, object_name=None):
        """Download file from S3 to local
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html

        :param file_name: download to this file name
        :param bucket: Bucket to download from
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if not object_name:
            object_name = file_name
        else:
            object_name = os.path.join(object_name, file_name)

        try:
            # response = self.s3_client.download_file(self.bucket, object_name, file_name)
            with open(file_name, "wb") as data:
                self.s3_client.download_fileobj(self.bucket, object_name, data)
        except ClientError as e:
            # logging.error(e)
            echo(e)
            echo("success? False")
            return False
        echo("success? True")
        return True

    def restore_from_glacier(self, file_name, object_name=None):
        """Restore object from Glacier tier for download
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.restore_object

        :param file_name: download to this file name
        :param bucket: Bucket to download from
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        response = self.s3_client.restore_object(
            Bucket=self.bucket,
            Key=object_name,
            RestoreRequest={
                "Days": 10,
                "GlacierJobParameters": {
                    "Tier": "Expedited",
                },
            },
        )
        return response

    def get_bucket_object_keys(self):
        my_bucket = self.s3_resour.Bucket(os.getenv("AWS_MEDIA_BUCKET"))
        # my_bucket = s3_resour.Bucket('media-backup-files')
        return [obj.key for obj in my_bucket.objects.all()]

    def check_obj_status(self, file_name, object_name=None):
        """check_obj_status docstring
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object

        :param file_name: download to this file name
        :param bucket: Bucket to download from
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        response = self.s3_client.head_object(
            Bucket=self.bucket,
            Key=file_name,
        )
        return response

    def download_from_glacier(self, file_name, object_name=None):
        """download_from_glacier docstring"""
        import time

        self.restore_from_glacier(self.s3_client, file_name, self.bucket, object_name=None)
        resored = False
        while resored == False:
            time.sleep(30)
            response = check_obj_status()
            if response == "":
                restored = True
            print("checking...")

        response = self.download_file(file_name=file_name)
        return response

    # def search_keyword_s3(self):
    #     """search for keywork in S3 media files"""
    #     return

    # def search_keyword_local(self):
    #     """search for keyword among local media files"""
    #     return

    # def search_keyword_global(self):
    #     """search_keyword docstring

    #     :param file_name: download to this file name
    #     :param bucket: Bucket to download from
    #     :param object_name: S3 object name. If not specified then file_name is used
    #     :return: True if file was uploaded, else False
    #     """
    #     return

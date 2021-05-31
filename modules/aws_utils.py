"""
utility functions for general use
Author: William Wright
"""

import os
import logging

import boto3
from botocore.exceptions import ClientError


def upload_file(s3_client, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        # response = s3_client.upload_file(file_name, bucket, object_name)
        with open(file_name, 'rb') as data:
            s3.upload_fileobj(data, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(s3_client, file_name, bucket, object_name=None):
    """Download file from S3 to local
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html

    :param file_name: download to this file name
    :param bucket: Bucket to download from
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        # response = s3_client.download_file(bucket, object_name, file_name)
        with open(file_name, 'wb') as data:
            s3_client.download_fileobj(bucket, object_name, data)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def restore_from_glacier(s3_client, file_name, bucket, object_name=None):
    """Restore object from Glacier tier for download
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.restore_object

    :param file_name: download to this file name
    :param bucket: Bucket to download from
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    response = s3_client.restore_object(
        Bucket=bucket,
        Key=object_name,
        RestoreRequest={
            "Days": 10,
            "GlacierJobParameters": {
                "Tier": "Expedited",
            },
        },
    )
    return response


def search_keyword_s3():
    """search for keywork in S3 media files"""
    return

def search_keyword_local():
    """search for keyword among local media files"""
    return

def search_keyword_global():
    """search_keyword docstring


    :param file_name: download to this file name
    :param bucket: Bucket to download from
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    return


def check_obj_status(s3_client, file_name, bucket, object_name=None):
    """check_obj_status docstring
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object

    :param file_name: download to this file name
    :param bucket: Bucket to download from
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    response = s3_client.head_object(
        Bucket=bucket,
        Key=file_name,
    )
    return response


def download_from_glacier(s3_client, file_name, bucket, object_name=None):
    """download_from_glacier docstring"""
    import time
    restore_from_glacier(s3_client, file_name, bucket, object_name=None):
    while resored==False:
        check_obj_status()
        time.sleep(60)
    return

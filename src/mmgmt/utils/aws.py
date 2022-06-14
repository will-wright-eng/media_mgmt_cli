"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html

# aws = AwsSecretMgmt()
# secret_name = "test/test_secret"
# secret = aws.get_secret(secret_name)

# secret_name = 'test/test_secret_2'
# secret_string = json.dumps(secret)
# aws.create_secret(secret_string,secret_name)

## write aws secrets to local

from .aws import AwsSecretMgmt

aws_secret = AwsSecretMgmt()

def write_secret_to_local_config(project_name):
    config = ConfigHandler(project_name)
    secrets_prefix = "projects/dev"
    secret = aws_secret.get_secret(os.path.join(secrets_prefix, project_name))
    config.write_config_file_from_dict(config_dict=secret)
    return config.print_configs()

for project_name in projects:
    write_secret_to_local_config(project_name)

    
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
"""

import os
import json
import base64
import pathlib
import configparser
from time import sleep

import boto3
from click import echo
from botocore.exceptions import ClientError

from .config import config_handler


class AwsStorageMgmt:
    def __init__(self):
        self.s3_resour = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.bucket = os.getenv("AWS_BUCKET", None)
        self.object_prefix = os.getenv("AWS_BUCKET_PATH", None)
        if (self.bucket is None) or (self.object_prefix is None):
            # get values from config file
            config = config_handler
            if config.check_config_exists():
                # export configs to env vars
                # TODO: this doesn't work --> create bash file that runs in .zshrc via source
                config.export_configs()
            else:
                echo("config file does not exist, run `mmgmt configure`")

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        echo(
            f"uploading: {file_name} \nto S3 bucket: {os.getenv('AWS_BUCKET')}/{os.getenv('AWS_BUCKET_PATH')}/{file_name}"
        )
        if not object_name:
            object_name = os.path.join(self.object_prefix, file_name)
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

    def download_file(self, object_name: str):
        """Download file from S3 to local
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html

        :param file_name: download to this file name
        :param bucket: Bucket to download from
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        file_name = object_name.split("/")[-1]

        try:
            with open(file_name, "wb") as data:
                self.s3_client.download_fileobj(self.bucket, object_name, data)
        except ClientError as e:
            echo("success? False")
            os.remove(file_name)
            status = self.get_obj_restore_status(object_name)
            if status == "incomplete":
                echo("restore in process")
                echo(json.dumps(aws.obj_head, indent=4, sort_keys=True, default=str))
            elif e.response["Error"]["Code"] == "InvalidObjectState":
                self.download_from_glacier(object_name=object_name)
                return True
            return False
        echo("success? True")
        return True

    def get_bucket_object_keys(self):
        my_bucket = self.s3_resour.Bucket(os.getenv("AWS_MEDIA_BUCKET"))
        return [obj.key for obj in my_bucket.objects.all()]

    def get_obj_head(self, object_name: str):
        response = self.s3_client.head_object(
            Bucket=self.bucket,
            Key=object_name,
        )
        self.obj_head = response
        return response

    def get_obj_restore_status(self, object_name):
        """check_obj_status docstring
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object

        :param file_name: download to this file name
        :param bucket: Bucket to download from
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        response = self.get_obj_head(object_name)
        try:
            resp_string = response["Restore"]
            echo(resp_string)
            if ("ongoing-request" in resp_string) and ("true" in resp_string):
                status = "incomplete"
            elif ("ongoing-request" in resp_string) and ("false" in resp_string):
                status = "complete"
            else:
                status = "unknown"
        except Exception as e:
            status = str(e)
        echo(status)
        return status

    def restore_from_glacier(self, object_name: str, restore_tier: str):
        """Restore object from Glacier tier for download
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.restore_object

        :param bucket: Bucket to download from
        :param object_name: S3 object name
        :return:
        """
        response = self.s3_client.restore_object(
            Bucket=self.bucket,
            Key=object_name,
            RestoreRequest={
                "Days": 10,
                "GlacierJobParameters": {
                    "Tier": restore_tier,
                },
            },
        )
        return response

    def download_from_glacier(self, object_name: str):
        """download_from_glacier docstring"""

        self.get_obj_head(object_name)
        try:
            tier = self.obj_head["StorageClass"]
            if tier == "DEEP_ARCHIVE":
                restore_tier = "Standard"
            elif tier == "GLACIER":
                restore_tier = "Expedited"
        except KeyError as e:
            echo(f"KeyError: {str(e)}, object not in glacier storage -- check control flow")
            return

        echo(f"restoring object from {tier}: {object_name}")
        self.restore_from_glacier(object_name=object_name, restore_tier=restore_tier)
        if tier == "GLACIER":
            restored = False
            while restored == False:
                sleep(30)
                echo("checking...")
                status = self.get_obj_restore_status(object_name)
                if status == "incomplete":
                    pass
                elif status == "complete":
                    echo("restored = True")
                    restored = True
                else:
                    echo(f"status: {status}, exiting...")
                    return

            echo("downloading restored file")
            return self.download_file(object_name=object_name)
        else:
            echo(f"object in {tier}, object will be restored in 12-24 hours")
            return


aws = AwsStorageMgmt()


def get_default_region() -> str:
    p = pathlib.Path.home() / ".aws" / "config"
    config = configparser.ConfigParser()
    config.read(p)
    return config["default"]["region"]


class AwsSecretMgmt:
    def __init__(self):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        self.client = session.client(service_name="secretsmanager", region_name=get_default_region())

    def get_secret(self, secret_name):
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                return json.loads(secret)
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    def get_secrets_list(self):
        return self.client.list_secrets()

    def create_secret(self, secret_string, secret_name, description="string description"):
        try:
            response = self.client.create_secret(
                Name=secret_name,
                Description=description,
                SecretString=secret_string,
            )
            return response
        except ClientError as e:
            return e

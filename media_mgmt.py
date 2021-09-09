"""mmgmt cli docstring"""

import logging

import click
import boto3

import modules.utils as utils
import modules.aws_utils as aws_utils

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

filename = "modules/config.yml"
configs = utils.load_configs(filename)["s3_test"]
logger.info(configs)

s3_client = boto3.resource("s3")
bucket = configs["bucket"]


@click.group()
def mmgmt():
    pass


@click.command()
@click.option("-t", "--storage-tier", "tier", default="standard")
@click.option("-f", "--filename", "filename", required=False)
def upload(tier, filename):
    if "filename" in locals():
        click.echo(f"Uploading {filename} to S3")
    else:
        filename = None
        click.echo(f"Uploading all Media files to S3")

    if tier != "standard":
        print("add arguements to upload")
        pass
    else:
        aws.upload_file(s3_client, filename, bucket, object_name=None)


mmgmt.add_command(upload)


@click.command()
@click.option("-f", "--filename", "filename", required=True)
def download(filename):
    click.echo(f"Downloading {filename} from S3...")


mmgmt.add_command(download)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option("-f", "--filename", "filename", required=True)
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt=f"Are you sure you want to delete?",
)
def delete(filename):
    click.echo(f"{filename} dropped from S3")


mmgmt.add_command(delete)


@click.command()
@click.option("-w", "--keyword", "keyword", required=True)
@click.option("-l", "--location", "location", required=False)
def search(keyword, location):
    if "location" in locals():
        click.echo(f"Searching {location} for {keyword}...")
    else:
        click.echo(f"Searching local and S3 for {keyword}...")


mmgmt.add_command(search)

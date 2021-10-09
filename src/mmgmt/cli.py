"""mmgmt cli docstring"""

import os
from pathlib import Path

import click
import boto3

from .utils.aws import AwsStorageMgmt
from .utils import utils as utils

aws = AwsStorageMgmt()


@click.group()
def mmgmt():
    pass


@click.command()
# @click.option("-t", "--storage-tier", "tier", default="standard")
@click.option("-f", "--filename", "filename", required=False)
def upload(tier, filename):
    p = Path(__file__).parent
    localfiles = os.listdir(p)
    if filename in localfiles:
        click.echo(f"Uploading {filename} to S3...")
        aws.upload_file(file_name=filename)
    else:
        # filename = None
        # click.echo(f"Uploading all Media files to S3")
        click.echo(f"Invalid filename")
        click.echo(f"Multi-file upload incomplete, exiting without upload")
        return False

    return True


@click.command()
@click.option("-f", "--filename", "filename", required=True)
def download(filename):
    click.echo(f"Downloading {filename} from S3...")


@click.command()
@click.option("-f", "--filename", "filename", required=True)
@click.option(
    "--yes",
    is_flag=True,
    callback=utils.abort_if_false,
    expose_value=False,
    prompt=f"Are you sure you want to delete?",
)
def delete(filename):
    click.echo(f"{filename} dropped from S3")


@click.command()
@click.option("-w", "--keyword", "keyword", required=True)
@click.option("-l", "--location", "location", required=False)
def search(keyword, location):
    if "location" in locals():
        click.echo(f"Searching {location} for {keyword}...")
    else:
        click.echo(f"Searching local and S3 for {keyword}...")


mmgmt.add_command(upload)
mmgmt.add_command(download)
mmgmt.add_command(delete)
mmgmt.add_command(search)

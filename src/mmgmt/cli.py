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
@click.option("-f", "--file-or-dir", "file-or-directory", required=False)
def upload(file_or_dir=None) -> bool:
    p = Path(__file__).parent
    localfiles = os.listdir(p)
    files_created = []
    try:
        if file_or_dir:
            if file_or_dir in localfiles:
                click.echo(f"Uploading {file_or_dir} to S3...")
                zip_file = utils.zip_process(file_or_dir)
                files_created.append(zip_file)
                aws.upload_file(file_name=zip_file)
            else:
                click.echo(f"Invalid file_or_dir")
                return False
        else:
            click.echo(f"Uploading all Media objects to S3")
            click.echo(f"Multi-file upload incomplete, exiting without upload")
            for file in localfiles:
                click.echo(f"Uploading {file}...")
                zip_file = utils.zip_process(file_or_dir)
                files_created.append(zip_file)
                aws.upload_file(file_name=zip_file)
    except Exception as e:
        print(e)
    finally:
        # remove all zip files from dir
        if files_created:
            for file in files_created:
                os.remove(file)
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

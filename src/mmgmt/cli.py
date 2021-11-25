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
@click.option("-f", "--file-or-dir", "file_or_dir", required=False, default=None)
@click.option("-c", "--compression", "compression", required=False, default="gzip")
def upload(file_or_dir, compression):
    p = Path(".")
    localfiles = os.listdir(p)
    files_created = []
    try:
        if file_or_dir:
            # extract this code segment into function -- DRY
            if file_or_dir == "all":
                click.echo(f"uploading all media objects to S3")
                for file_or_dir in localfiles:
                    if compression == "zip":
                        file_created = utils.zip_process(file_or_dir)
                    elif compression == "gzip":
                        file_created = utils.gzip_process(file_or_dir)
                    files_created.append(file_created)
                    resp = aws.upload_file(file_name=file_created)
            elif file_or_dir in localfiles:
                click.echo("file found, compressing...")
                # TODO: add check to see if zip file exists <-- this one
                # or add flag that tells the control flow to skip the zip_process
                # add clean_string method to zip_process method
                if compression == "zip":
                    file_created = utils.zip_process(file_or_dir)
                elif compression == "gzip":
                    file_created = utils.gzip_process(file_or_dir)
                files_created.append(file_created)
                resp = aws.upload_file(file_name=file_created)
            else:
                click.echo(f"invalid file or directory")
                return False
        else:
            click.echo("invalid file_or_dir command")
    except Exception as e:
        click.echo(e)
    finally:
        # remove all created files from dir
        if files_created:
            for file in files_created:
                os.remove(file)


@click.command()
@click.option("-k", "--keyword", "keyword", required=True)
@click.option("-l", "--location", "location", required=False, default="global")
# @click.option("-l", "--location", "location", required=False, default="global")
# add verbose flag that outputs details on size, location, and full_path
# turn `matches` list into `output` list of dicts, appending info dict for each file
def search(keyword, location):
    click.echo(f"Searching {location} for {keyword}...")

    if location == "local":
        files = utils.files_in_media_dir()

    elif location == "s3":
        # get objects from s3 bucket
        files = aws.get_bucket_object_keys()
    elif location == "global":
        # do both
        files = utils.files_in_media_dir() + aws.get_bucket_object_keys()
    else:
        click.echo("invalid location")

    # click.echo(str(files))
    matches = []
    for file in files:
        if utils.keyword_in_string(keyword, file):
            matches.append(file)

    if len(matches) >= 1:
        # print("more than 1 match, be more specific\n")
        # print("\n".join(matches))
        click.echo("at least one match found\n")
        click.echo("\n".join(matches))
        return True
    else:
        click.echo("no matches found\n")
        return False


@click.command()
@click.option("-f", "--filename", "filename", required=True)
def download(filename):
    click.echo(f"Downloading {filename} from S3...")
    click.echo("command not yet complete")


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
    click.echo("command not yet complete")


@click.command()
def ls():
    p = Path(".")
    localfiles = os.listdir(p)
    for file in localfiles:
        # click.echo(file)
        utils.click_echo(file)


mmgmt.add_command(upload)
mmgmt.add_command(download)
mmgmt.add_command(delete)
mmgmt.add_command(search)
mmgmt.add_command(ls)

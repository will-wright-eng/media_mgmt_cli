"""mmgmt cli docstring"""

import os
import json
from pathlib import Path
from typing import List

import click
import boto3

from .utils.aws import aws
from .utils import utils as utils


@click.group()
def mmgmt():
    pass


# TODO: add check to see if zip file exists <-- this one
# or add flag that tells the control flow to skip the zip_process
# add clean_string method to zip_process method
# add filter to localfiles to exclude .DS_Store (all systems files)
@click.command()
@click.option("-f", "--file-or-dir", "file_or_dir", required=False, default=None)
@click.option("-c", "--compression", "compression", required=False, default="gzip")
def upload(file_or_dir, compression):
    p = Path(".")
    localfiles = os.listdir(p)
    files_created = []
    try:
        if file_or_dir:
            if file_or_dir == "all":
                click.echo(f"uploading all media objects to S3")
                for _file_or_dir in localfiles:
                    click.echo(f"{_file_or_dir}, compressing...")
                    files_created.append(utils.upload_file_or_dir(_file_or_dir, compression))
            elif file_or_dir in localfiles:
                click.echo("file found, compressing...")
                files_created.append(utils.upload_file_or_dir(file_or_dir, compression))
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
    files = utils.get_files(location=location)

    click.echo(f"Searching {location} for {keyword}...")
    matches = []
    for file in files:
        if utils.keyword_in_string(keyword, file):
            matches.append(file)

    if len(matches) >= 1:
        click.echo("at least one match found\n")
        click.echo("\n".join(matches))
        utils.get_storage_tier(matches)
        return True
    else:
        click.echo("no matches found\n")
        return False


@click.command()
@click.option("-f", "--filename", "filename", required=True)
def download(filename):
    click.echo(f"Downloading {filename} from S3...")
    aws.download_file(object_name=filename)


@click.command()
@click.option("-f", "--filename", "filename", required=True)
def get_status(filename):
    aws.get_obj_head(object_name=filename)
    click.echo(json.dumps(aws.obj_head, indent=4, sort_keys=True, default=str))


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
    # use as test: media_uploads/Tron_Legacy_(2010)_BRRip_XvidHD_720p-NPW.zip
    click.echo(f"{filename} dropped from S3")
    click.echo("jk, command not yet complete")


@click.command()
@click.option("-l", "--location", "location", required=False, default="here")
def ls(location):
    if location in ("local", "s3", "global"):
        files = utils.get_files(location=location)
    else:
        p = Path(".")
        files = os.listdir(p)

    for file in files:
        click.echo(file)


mmgmt.add_command(upload)
mmgmt.add_command(download)
mmgmt.add_command(delete)
mmgmt.add_command(search)
mmgmt.add_command(ls)
mmgmt.add_command(get_status)
